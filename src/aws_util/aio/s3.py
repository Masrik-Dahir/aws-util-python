"""Native async S3 utilities — real non-blocking I/O via :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import hashlib
import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import IO, Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error
from aws_util.s3 import (
    AbortMultipartUploadResult,
    CompleteMultipartUploadResult,
    CreateBucketResult,
    CreateMultipartUploadResult,
    CreateSessionResult,
    DeleteObjectsResult,
    DeleteObjectTaggingResult,
    GetBucketAccelerateConfigurationResult,
    GetBucketAclResult,
    GetBucketAnalyticsConfigurationResult,
    GetBucketCorsResult,
    GetBucketEncryptionResult,
    GetBucketIntelligentTieringConfigurationResult,
    GetBucketInventoryConfigurationResult,
    GetBucketLifecycleConfigurationResult,
    GetBucketLifecycleResult,
    GetBucketLocationResult,
    GetBucketLoggingResult,
    GetBucketMetadataConfigurationResult,
    GetBucketMetadataTableConfigurationResult,
    GetBucketMetricsConfigurationResult,
    GetBucketNotificationConfigurationResult,
    GetBucketNotificationResult,
    GetBucketOwnershipControlsResult,
    GetBucketPolicyResult,
    GetBucketPolicyStatusResult,
    GetBucketReplicationResult,
    GetBucketRequestPaymentResult,
    GetBucketTaggingResult,
    GetBucketVersioningResult,
    GetBucketWebsiteResult,
    GetObjectAclResult,
    GetObjectAttributesResult,
    GetObjectLegalHoldResult,
    GetObjectLockConfigurationResult,
    GetObjectRetentionResult,
    GetObjectTaggingResult,
    GetObjectTorrentResult,
    GetPublicAccessBlockResult,
    HeadBucketResult,
    HeadObjectResult,
    ListBucketAnalyticsConfigurationsResult,
    ListBucketIntelligentTieringConfigurationsResult,
    ListBucketInventoryConfigurationsResult,
    ListBucketMetricsConfigurationsResult,
    ListBucketsResult,
    ListDirectoryBucketsResult,
    ListMultipartUploadsResult,
    ListObjectsV2Result,
    ListPartsResult,
    PresignedUrl,
    PutBucketLifecycleConfigurationResult,
    PutObjectAclResult,
    PutObjectLegalHoldResult,
    PutObjectLockConfigurationResult,
    PutObjectResult,
    PutObjectRetentionResult,
    PutObjectTaggingResult,
    RestoreObjectResult,
    S3Object,
    S3ObjectVersion,
    SelectObjectContentResult,
    UploadPartCopyResult,
    UploadPartResult,
)

__all__ = [
    "AbortMultipartUploadResult",
    "CompleteMultipartUploadResult",
    "CreateBucketResult",
    "CreateMultipartUploadResult",
    "CreateSessionResult",
    "DeleteObjectTaggingResult",
    "DeleteObjectsResult",
    "GetBucketAccelerateConfigurationResult",
    "GetBucketAclResult",
    "GetBucketAnalyticsConfigurationResult",
    "GetBucketCorsResult",
    "GetBucketEncryptionResult",
    "GetBucketIntelligentTieringConfigurationResult",
    "GetBucketInventoryConfigurationResult",
    "GetBucketLifecycleConfigurationResult",
    "GetBucketLifecycleResult",
    "GetBucketLocationResult",
    "GetBucketLoggingResult",
    "GetBucketMetadataConfigurationResult",
    "GetBucketMetadataTableConfigurationResult",
    "GetBucketMetricsConfigurationResult",
    "GetBucketNotificationConfigurationResult",
    "GetBucketNotificationResult",
    "GetBucketOwnershipControlsResult",
    "GetBucketPolicyResult",
    "GetBucketPolicyStatusResult",
    "GetBucketReplicationResult",
    "GetBucketRequestPaymentResult",
    "GetBucketTaggingResult",
    "GetBucketVersioningResult",
    "GetBucketWebsiteResult",
    "GetObjectAclResult",
    "GetObjectAttributesResult",
    "GetObjectLegalHoldResult",
    "GetObjectLockConfigurationResult",
    "GetObjectRetentionResult",
    "GetObjectTaggingResult",
    "GetObjectTorrentResult",
    "GetPublicAccessBlockResult",
    "HeadBucketResult",
    "HeadObjectResult",
    "ListBucketAnalyticsConfigurationsResult",
    "ListBucketIntelligentTieringConfigurationsResult",
    "ListBucketInventoryConfigurationsResult",
    "ListBucketMetricsConfigurationsResult",
    "ListBucketsResult",
    "ListDirectoryBucketsResult",
    "ListMultipartUploadsResult",
    "ListObjectsV2Result",
    "ListPartsResult",
    "PresignedUrl",
    "PutBucketLifecycleConfigurationResult",
    "PutObjectAclResult",
    "PutObjectLegalHoldResult",
    "PutObjectLockConfigurationResult",
    "PutObjectResult",
    "PutObjectRetentionResult",
    "PutObjectTaggingResult",
    "RestoreObjectResult",
    "S3Object",
    "S3ObjectVersion",
    "SelectObjectContentResult",
    "UploadPartCopyResult",
    "UploadPartResult",
    "abort_multipart_upload",
    "batch_copy",
    "complete_multipart_upload",
    "copy_object",
    "create_bucket",
    "create_bucket_metadata_configuration",
    "create_bucket_metadata_table_configuration",
    "create_multipart_upload",
    "create_session",
    "delete_bucket",
    "delete_bucket_analytics_configuration",
    "delete_bucket_cors",
    "delete_bucket_encryption",
    "delete_bucket_intelligent_tiering_configuration",
    "delete_bucket_inventory_configuration",
    "delete_bucket_lifecycle",
    "delete_bucket_metadata_configuration",
    "delete_bucket_metadata_table_configuration",
    "delete_bucket_metrics_configuration",
    "delete_bucket_ownership_controls",
    "delete_bucket_policy",
    "delete_bucket_replication",
    "delete_bucket_tagging",
    "delete_bucket_website",
    "delete_object",
    "delete_object_tagging",
    "delete_objects",
    "delete_prefix",
    "delete_public_access_block",
    "download_as_text",
    "download_bytes",
    "download_file",
    "generate_presigned_post",
    "get_bucket_accelerate_configuration",
    "get_bucket_acl",
    "get_bucket_analytics_configuration",
    "get_bucket_cors",
    "get_bucket_encryption",
    "get_bucket_intelligent_tiering_configuration",
    "get_bucket_inventory_configuration",
    "get_bucket_lifecycle",
    "get_bucket_lifecycle_configuration",
    "get_bucket_location",
    "get_bucket_logging",
    "get_bucket_metadata_configuration",
    "get_bucket_metadata_table_configuration",
    "get_bucket_metrics_configuration",
    "get_bucket_notification",
    "get_bucket_notification_configuration",
    "get_bucket_ownership_controls",
    "get_bucket_policy",
    "get_bucket_policy_status",
    "get_bucket_replication",
    "get_bucket_request_payment",
    "get_bucket_tagging",
    "get_bucket_versioning",
    "get_bucket_website",
    "get_object",
    "get_object_acl",
    "get_object_attributes",
    "get_object_legal_hold",
    "get_object_lock_configuration",
    "get_object_metadata",
    "get_object_retention",
    "get_object_tagging",
    "get_object_torrent",
    "get_public_access_block",
    "head_bucket",
    "head_object",
    "list_bucket_analytics_configurations",
    "list_bucket_intelligent_tiering_configurations",
    "list_bucket_inventory_configurations",
    "list_bucket_metrics_configurations",
    "list_buckets",
    "list_directory_buckets",
    "list_multipart_uploads",
    "list_object_versions",
    "list_objects",
    "list_objects_v2",
    "list_parts",
    "move_object",
    "multipart_upload",
    "object_exists",
    "presigned_url",
    "put_bucket_accelerate_configuration",
    "put_bucket_acl",
    "put_bucket_analytics_configuration",
    "put_bucket_cors",
    "put_bucket_encryption",
    "put_bucket_intelligent_tiering_configuration",
    "put_bucket_inventory_configuration",
    "put_bucket_lifecycle",
    "put_bucket_lifecycle_configuration",
    "put_bucket_logging",
    "put_bucket_metrics_configuration",
    "put_bucket_notification",
    "put_bucket_notification_configuration",
    "put_bucket_ownership_controls",
    "put_bucket_policy",
    "put_bucket_replication",
    "put_bucket_request_payment",
    "put_bucket_tagging",
    "put_bucket_versioning",
    "put_bucket_website",
    "put_object",
    "put_object_acl",
    "put_object_legal_hold",
    "put_object_lock_configuration",
    "put_object_retention",
    "put_object_tagging",
    "put_public_access_block",
    "read_json",
    "read_jsonl",
    "rename_object",
    "restore_object",
    "select_object_content",
    "sync_folder",
    "update_bucket_metadata_inventory_table_configuration",
    "update_bucket_metadata_journal_table_configuration",
    "upload_bytes",
    "upload_file",
    "upload_fileobj",
    "upload_part",
    "upload_part_copy",
    "write_get_object_response",
    "write_json",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def upload_file(
    bucket: str,
    key: str,
    file_path: str | Path,
    content_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Upload a local file to S3.

    Args:
        bucket: Destination S3 bucket name.
        key: Destination object key (path inside the bucket).
        file_path: Absolute or relative path to the local file.
        content_type: Optional ``Content-Type`` header, e.g.
            ``"application/json"``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the upload fails.
    """
    data = await asyncio.to_thread(Path(file_path).read_bytes)
    kwargs: dict[str, Any] = {"Bucket": bucket, "Key": key, "Body": data}
    if content_type:
        kwargs["ContentType"] = content_type
    try:
        client = async_client("s3", region_name)
        await client.call("PutObject", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to upload {file_path!r} to s3://{bucket}/{key}") from exc


async def upload_bytes(
    bucket: str,
    key: str,
    data: bytes | IO[bytes],
    content_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Upload raw bytes or a file-like object to S3.

    Args:
        bucket: Destination S3 bucket name.
        key: Destination object key.
        data: Bytes or binary file-like object to upload.
        content_type: Optional ``Content-Type`` header.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the upload fails.
    """
    raw = data if isinstance(data, bytes) else data.read()
    kwargs: dict[str, Any] = {"Bucket": bucket, "Key": key, "Body": raw}
    if content_type:
        kwargs["ContentType"] = content_type
    try:
        client = async_client("s3", region_name)
        await client.call("PutObject", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to upload bytes to s3://{bucket}/{key}") from exc


async def download_file(
    bucket: str,
    key: str,
    dest_path: str | Path,
    region_name: str | None = None,
) -> None:
    """Download an S3 object to a local file.

    Args:
        bucket: Source S3 bucket name.
        key: Source object key.
        dest_path: Local path where the file will be written.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the download fails.
    """
    try:
        client = async_client("s3", region_name)
        resp = await client.call("GetObject", Bucket=bucket, Key=key)
        body = resp["Body"]
        if isinstance(body, bytes):
            content = body
        else:
            content = await asyncio.to_thread(body.read)
        await asyncio.to_thread(Path(dest_path).write_bytes, content)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to download s3://{bucket}/{key} to {dest_path!r}"
        ) from exc


async def download_bytes(
    bucket: str,
    key: str,
    version_id: str | None = None,
    region_name: str | None = None,
) -> bytes:
    """Download an S3 object and return its contents as bytes.

    Args:
        bucket: Source S3 bucket name.
        key: Source object key.
        version_id: Optional S3 version ID to download a specific
            version.
        region_name: AWS region override.

    Returns:
        The object body as ``bytes``.

    Raises:
        RuntimeError: If the download fails.
    """
    try:
        client = async_client("s3", region_name)
        kwargs: dict[str, Any] = {"Bucket": bucket, "Key": key}
        if version_id is not None:
            kwargs["VersionId"] = version_id
        resp = await client.call("GetObject", **kwargs)
        body = resp["Body"]
        if isinstance(body, bytes):
            return body
        return await asyncio.to_thread(body.read)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to download s3://{bucket}/{key}") from exc


async def list_objects(
    bucket: str,
    prefix: str = "",
    region_name: str | None = None,
) -> list[S3Object]:
    """List objects in a bucket, optionally filtered by prefix.

    Handles pagination automatically.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix filter.  An empty string lists all objects.
        region_name: AWS region override.

    Returns:
        A list of :class:`S3Object` instances ordered by key.

    Raises:
        RuntimeError: If the list operation fails.
    """
    try:
        client = async_client("s3", region_name)
        raw_items = await client.paginate(
            "ListObjectsV2",
            result_key="Contents",
            token_input="ContinuationToken",
            token_output="NextContinuationToken",
            Bucket=bucket,
            Prefix=prefix,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to list objects in s3://{bucket}/{prefix}") from exc
    return [
        S3Object(
            bucket=bucket,
            key=item["Key"],
            size=item.get("Size"),
            last_modified=item.get("LastModified"),
            etag=item.get("ETag", "").strip('"') or None,
        )
        for item in raw_items
    ]


async def object_exists(
    bucket: str,
    key: str,
    region_name: str | None = None,
) -> bool:
    """Check whether an S3 object exists without downloading it.

    Uses a ``HeadObject`` request which is cheaper than ``GetObject``.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        region_name: AWS region override.

    Returns:
        ``True`` if the object exists, ``False`` if it does not.

    Raises:
        RuntimeError: If the check fails for a reason other than a missing
            object (e.g. permission denied).
    """
    try:
        client = async_client("s3", region_name)
        await client.call("HeadObject", Bucket=bucket, Key=key)
        return True
    except RuntimeError as exc:
        err_str = str(exc)
        if "404" in err_str or "NoSuchKey" in err_str or "Not Found" in err_str:
            return False
        raise wrap_aws_error(exc, f"Failed to check existence of s3://{bucket}/{key}") from exc


async def delete_object(
    bucket: str,
    key: str,
    region_name: str | None = None,
) -> None:
    """Delete a single object from S3.

    Args:
        bucket: S3 bucket name.
        key: Object key to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    try:
        client = async_client("s3", region_name)
        await client.call("DeleteObject", Bucket=bucket, Key=key)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete s3://{bucket}/{key}") from exc


async def copy_object(
    src_bucket: str,
    src_key: str,
    dst_bucket: str,
    dst_key: str,
    region_name: str | None = None,
) -> None:
    """Server-side copy of an S3 object (no data transfer through the client).

    Args:
        src_bucket: Source bucket name.
        src_key: Source object key.
        dst_bucket: Destination bucket name.
        dst_key: Destination object key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the copy fails.
    """
    try:
        client = async_client("s3", region_name)
        await client.call(
            "CopyObject",
            CopySource={"Bucket": src_bucket, "Key": src_key},
            Bucket=dst_bucket,
            Key=dst_key,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to copy s3://{src_bucket}/{src_key} \u2192 s3://{dst_bucket}/{dst_key}"
        ) from exc


async def presigned_url(
    bucket: str,
    key: str,
    expires_in: int = 3600,
    operation: str = "get_object",
    region_name: str | None = None,
) -> PresignedUrl:
    """Generate a pre-signed URL for an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        expires_in: Validity duration in seconds.  Defaults to ``3600``
            (one hour).
        operation: The S3 API operation to sign.  Use ``"get_object"`` for
            download URLs and ``"put_object"`` for upload URLs.
        region_name: AWS region override.

    Returns:
        A :class:`PresignedUrl` containing the URL and metadata.

    Raises:
        RuntimeError: If URL generation fails.
    """
    # Pre-signed URL generation requires the boto3 client directly;
    # delegate to a thread since it's a lightweight signing operation.
    from aws_util._client import get_client

    try:
        url: str = await asyncio.to_thread(
            lambda: get_client("s3", region_name).generate_presigned_url(
                ClientMethod=operation,
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to generate pre-signed URL for s3://{bucket}/{key}"
        ) from exc
    return PresignedUrl(url=url, bucket=bucket, key=key, expires_in=expires_in)


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def read_json(
    bucket: str,
    key: str,
    region_name: str | None = None,
) -> Any:
    """Download an S3 object and deserialise it as JSON.

    Args:
        bucket: S3 bucket name.
        key: Object key pointing to a JSON file.
        region_name: AWS region override.

    Returns:
        The deserialised Python value (dict, list, str, etc.).

    Raises:
        RuntimeError: If the download fails.
        ValueError: If the object is not valid JSON.
    """
    raw = await download_bytes(bucket, key, region_name=region_name)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"s3://{bucket}/{key} is not valid JSON: {exc}") from exc


async def write_json(
    bucket: str,
    key: str,
    data: Any,
    indent: int | None = None,
    region_name: str | None = None,
) -> None:
    """Serialise *data* to JSON and upload it to S3.

    Args:
        bucket: S3 bucket name.
        key: Destination object key.
        data: JSON-serialisable Python value.
        indent: Pretty-print indentation level.  ``None`` produces compact JSON.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the upload fails.
    """
    payload = json.dumps(data, indent=indent).encode("utf-8")
    await upload_bytes(
        bucket,
        key,
        payload,
        content_type="application/json",
        region_name=region_name,
    )


async def read_jsonl(
    bucket: str,
    key: str,
    region_name: str | None = None,
) -> AsyncIterator[Any]:
    """Download a newline-delimited JSON (JSONL) file from S3 and yield lines.

    Args:
        bucket: S3 bucket name.
        key: Object key pointing to a JSONL file.
        region_name: AWS region override.

    Yields:
        One deserialised Python value per non-empty line.

    Raises:
        RuntimeError: If the download fails.
        ValueError: If a line is not valid JSON.
    """
    raw = await download_bytes(bucket, key, region_name=region_name)
    for i, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            yield json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"s3://{bucket}/{key} line {i} is not valid JSON: {exc}") from exc


async def sync_folder(
    local_path: str | Path,
    bucket: str,
    prefix: str = "",
    delete_removed: bool = False,
    region_name: str | None = None,
) -> dict[str, int]:
    """Upload an entire local directory tree to S3, skipping unchanged files.

    Compares local file ETag (MD5) against the S3 object ETag and only
    uploads files that are new or modified.

    Args:
        local_path: Root of the local directory to sync.
        bucket: Destination S3 bucket.
        prefix: S3 key prefix prepended to all uploaded keys.
        delete_removed: If ``True``, delete S3 objects under *prefix* that no
            longer exist locally.
        region_name: AWS region override.

    Returns:
        A dict with counts: ``{"uploaded": n, "skipped": n, "deleted": n}``.

    Raises:
        RuntimeError: If any upload or delete fails.
    """
    local_root = Path(local_path)
    if not local_root.is_dir():
        raise ValueError(f"{local_path!r} is not a directory")

    existing: dict[str, str] = {
        obj.key: obj.etag or ""
        for obj in await list_objects(bucket, prefix=prefix, region_name=region_name)
    }

    counts = {"uploaded": 0, "skipped": 0, "deleted": 0}
    local_keys: set[str] = set()
    upload_tasks: list[Any] = []

    for file_path in local_root.rglob("*"):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(local_root).as_posix()
        s3_key = f"{prefix.rstrip('/')}/{rel}".lstrip("/") if prefix else rel
        local_keys.add(s3_key)

        file_bytes = await asyncio.to_thread(file_path.read_bytes)
        md5 = hashlib.md5(file_bytes).hexdigest()
        if existing.get(s3_key) == md5:
            counts["skipped"] += 1
            continue

        upload_tasks.append((s3_key, file_path))

    # Upload changed files concurrently
    async def _upload(s3_key: str, fp: Path) -> None:
        await upload_file(bucket, s3_key, fp, region_name=region_name)

    if upload_tasks:
        await asyncio.gather(*[_upload(k, fp) for k, fp in upload_tasks])
    counts["uploaded"] = len(upload_tasks)

    if delete_removed:
        delete_tasks = [s3_key for s3_key in existing if s3_key not in local_keys]
        if delete_tasks:
            await asyncio.gather(
                *[delete_object(bucket, k, region_name=region_name) for k in delete_tasks]
            )
        counts["deleted"] = len(delete_tasks)

    return counts


async def multipart_upload(
    bucket: str,
    key: str,
    file_path: str | Path,
    part_size_mb: int = 50,
    region_name: str | None = None,
) -> None:
    """Upload a large file to S3 using multipart upload.

    Splits the file into *part_size_mb* chunks and uploads them in sequence.
    The multipart upload is aborted automatically if any part fails.

    Prefer this over :func:`upload_file` for files > 100 MB.

    Args:
        bucket: Destination S3 bucket.
        key: Destination object key.
        file_path: Path to the local file.
        part_size_mb: Size of each part in megabytes (minimum 5 MB, default
            50 MB).
        region_name: AWS region override.

    Raises:
        ValueError: If *part_size_mb* is less than 5.
        RuntimeError: If the upload fails.
    """
    if part_size_mb < 5:
        raise ValueError("part_size_mb must be at least 5 MB")

    client = async_client("s3", region_name)
    part_size = part_size_mb * 1024 * 1024
    fp = Path(file_path)
    file_bytes = await asyncio.to_thread(fp.read_bytes)

    mpu = await client.call("CreateMultipartUpload", Bucket=bucket, Key=key)
    upload_id = mpu["UploadId"]
    parts: list[dict[str, Any]] = []

    try:
        part_number = 1
        offset = 0
        while offset < len(file_bytes):
            chunk = file_bytes[offset : offset + part_size]
            resp = await client.call(
                "UploadPart",
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=chunk,
            )
            parts.append({"PartNumber": part_number, "ETag": resp["ETag"]})
            part_number += 1
            offset += part_size

        await client.call(
            "CompleteMultipartUpload",
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )
    except Exception as exc:
        await client.call(
            "AbortMultipartUpload",
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
        )
        raise wrap_aws_error(exc, f"Multipart upload failed for s3://{bucket}/{key}") from exc


async def delete_prefix(
    bucket: str,
    prefix: str,
    region_name: str | None = None,
) -> int:
    """Delete all S3 objects whose key starts with *prefix*.

    Uses batch delete (up to 1 000 objects per request) to minimise API calls.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix to delete (e.g. ``"logs/2023/"``).
        region_name: AWS region override.

    Returns:
        Total number of objects deleted.

    Raises:
        RuntimeError: If any list or delete call fails.
    """
    try:
        client = async_client("s3", region_name)
        all_items = await client.paginate(
            "ListObjectsV2",
            result_key="Contents",
            token_input="ContinuationToken",
            token_output="NextContinuationToken",
            Bucket=bucket,
            Prefix=prefix,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"delete_prefix failed for s3://{bucket}/{prefix}") from exc

    if not all_items:
        return 0

    deleted_count = 0
    # Batch delete in groups of 1000
    for i in range(0, len(all_items), 1000):
        batch = all_items[i : i + 1000]
        keys = [{"Key": obj["Key"]} for obj in batch]
        try:
            await client.call(
                "DeleteObjects",
                Bucket=bucket,
                Delete={"Objects": keys, "Quiet": True},
            )
            deleted_count += len(keys)
        except RuntimeError as exc:
            raise wrap_aws_error(exc, f"delete_prefix failed for s3://{bucket}/{prefix}") from exc

    return deleted_count


async def move_object(
    src_bucket: str,
    src_key: str,
    dst_bucket: str,
    dst_key: str,
    region_name: str | None = None,
) -> None:
    """Move an S3 object by copying it to a new location then deleting the source.

    Args:
        src_bucket: Source bucket.
        src_key: Source object key.
        dst_bucket: Destination bucket.
        dst_key: Destination object key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the copy or delete fails.
    """
    await copy_object(src_bucket, src_key, dst_bucket, dst_key, region_name=region_name)
    await delete_object(src_bucket, src_key, region_name=region_name)


async def get_object_metadata(
    bucket: str,
    key: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Fetch the metadata of an S3 object without downloading its body.

    Uses ``HeadObject`` which is faster and cheaper than ``GetObject``.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        region_name: AWS region override.

    Returns:
        A dict with ``content_type``, ``content_length``, ``last_modified``,
        ``etag``, and ``metadata`` (user-defined metadata) keys.

    Raises:
        RuntimeError: If the object does not exist or the call fails.
    """
    try:
        client = async_client("s3", region_name)
        resp = await client.call("HeadObject", Bucket=bucket, Key=key)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to get metadata for s3://{bucket}/{key}") from exc
    return {
        "content_type": resp.get("ContentType"),
        "content_length": resp.get("ContentLength"),
        "last_modified": resp.get("LastModified"),
        "etag": resp.get("ETag", "").strip('"') or None,
        "metadata": resp.get("Metadata", {}),
    }


async def batch_copy(
    copies: list[dict[str, str]],
    region_name: str | None = None,
) -> None:
    """Copy multiple S3 objects concurrently.

    Each entry in *copies* must be a dict with ``"src_bucket"``,
    ``"src_key"``, ``"dst_bucket"``, and ``"dst_key"`` keys.

    Args:
        copies: List of copy-operation dicts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If any copy operation fails.
    """
    errors: list[str] = []

    async def _copy(op: dict[str, str]) -> None:
        try:
            await copy_object(
                op["src_bucket"],
                op["src_key"],
                op["dst_bucket"],
                op["dst_key"],
                region_name=region_name,
            )
        except RuntimeError as exc:
            errors.append(str(exc))

    await asyncio.gather(*[_copy(op) for op in copies])

    if errors:
        raise AwsServiceError(f"batch_copy had {len(errors)} failure(s): {errors[0]}")


async def download_as_text(
    bucket: str,
    key: str,
    encoding: str = "utf-8",
    region_name: str | None = None,
) -> str:
    """Download an S3 object and return its contents as a string.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        encoding: Text encoding to use when decoding the bytes (default
            ``"utf-8"``).
        region_name: AWS region override.

    Returns:
        The object body decoded as a string.

    Raises:
        RuntimeError: If the download fails.
    """
    raw = await download_bytes(bucket, key, region_name=region_name)
    return raw.decode(encoding)


async def generate_presigned_post(
    bucket: str,
    key: str,
    max_size_mb: int = 10,
    expires_in: int = 3600,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Generate a pre-signed POST policy for browser-based S3 uploads.

    The returned dict contains ``url`` and ``fields`` which can be used in an
    HTML form or a ``requests.post`` call directly from the client without
    exposing AWS credentials.

    Args:
        bucket: Target S3 bucket.
        key: Object key (may include ``${filename}`` for browser uploads).
        max_size_mb: Maximum file size the client may upload (default 10 MB).
        expires_in: Policy validity in seconds (default 3600).
        region_name: AWS region override.

    Returns:
        A dict with ``"url"`` and ``"fields"`` keys.

    Raises:
        RuntimeError: If the policy generation fails.
    """
    from aws_util._client import get_client

    conditions = [["content-length-range", 1, max_size_mb * 1024 * 1024]]
    try:
        return await asyncio.to_thread(
            lambda: get_client("s3", region_name).generate_presigned_post(
                Bucket=bucket,
                Key=key,
                Conditions=conditions,
                ExpiresIn=expires_in,
            )
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to generate presigned POST for s3://{bucket}/{key}"
        ) from exc


async def get_object(
    bucket: str,
    key: str,
    version_id: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Fetch an S3 object and return the full response.

    Unlike :func:`download_bytes`, the response ``Body`` is returned
    as raw bytes that the caller can process directly.

    Args:
        bucket: S3 bucket name.
        key: Object key.
        version_id: Optional version ID for versioned buckets.
        region_name: AWS region override.

    Returns:
        The parsed ``GetObject`` response dict, with ``Body`` as
        bytes.

    Raises:
        RuntimeError: If the download fails.
    """
    try:
        client = async_client("s3", region_name)
        kwargs: dict[str, Any] = {"Bucket": bucket, "Key": key}
        if version_id is not None:
            kwargs["VersionId"] = version_id
        return await client.call("GetObject", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to get s3://{bucket}/{key}") from exc


async def list_object_versions(
    bucket: str,
    prefix: str = "",
    region_name: str | None = None,
) -> list[S3ObjectVersion]:
    """List all versions of objects in a versioned S3 bucket.

    Handles pagination automatically.

    Args:
        bucket: S3 bucket name.
        prefix: Key prefix filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`S3ObjectVersion` instances.

    Raises:
        RuntimeError: If the list operation fails.
    """
    from aws_util.s3 import list_object_versions as _sync

    try:
        return await asyncio.to_thread(_sync, bucket, prefix, region_name)
    except RuntimeError:
        raise


async def upload_fileobj(
    bucket: str,
    key: str,
    fileobj: IO[bytes],
    content_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Upload a file-like object to S3 using managed transfer.

    Uses boto3's ``upload_fileobj`` which automatically handles
    multipart uploads for large objects.

    Args:
        bucket: Destination S3 bucket name.
        key: Destination object key.
        fileobj: A binary file-like object (must support ``.read()``).
        content_type: Optional ``Content-Type`` header.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the upload fails.
    """
    from aws_util.s3 import upload_fileobj as _sync

    try:
        await asyncio.to_thread(_sync, bucket, key, fileobj, content_type, region_name)
    except RuntimeError:
        raise


async def abort_multipart_upload(
    bucket: str,
    key: str,
    upload_id: str,
    *,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    if_match_initiated_time: str | None = None,
    region_name: str | None = None,
) -> AbortMultipartUploadResult:
    """Abort multipart upload.

    Args:
        bucket: Bucket.
        key: Key.
        upload_id: Upload id.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        if_match_initiated_time: If match initiated time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["UploadId"] = upload_id
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if if_match_initiated_time is not None:
        kwargs["IfMatchInitiatedTime"] = if_match_initiated_time
    try:
        resp = await client.call("AbortMultipartUpload", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to abort multipart upload") from exc
    return AbortMultipartUploadResult(
        request_charged=resp.get("RequestCharged"),
    )


async def complete_multipart_upload(
    bucket: str,
    key: str,
    upload_id: str,
    *,
    multipart_upload: dict[str, Any] | None = None,
    checksum_crc32: str | None = None,
    checksum_crc32_c: str | None = None,
    checksum_crc64_nvme: str | None = None,
    checksum_sha1: str | None = None,
    checksum_sha256: str | None = None,
    checksum_type: str | None = None,
    mpu_object_size: int | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    region_name: str | None = None,
) -> CompleteMultipartUploadResult:
    """Complete multipart upload.

    Args:
        bucket: Bucket.
        key: Key.
        upload_id: Upload id.
        multipart_upload: Multipart upload.
        checksum_crc32: Checksum crc32.
        checksum_crc32_c: Checksum crc32 c.
        checksum_crc64_nvme: Checksum crc64 nvme.
        checksum_sha1: Checksum sha1.
        checksum_sha256: Checksum sha256.
        checksum_type: Checksum type.
        mpu_object_size: Mpu object size.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        if_match: If match.
        if_none_match: If none match.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["UploadId"] = upload_id
    if multipart_upload is not None:
        kwargs["MultipartUpload"] = multipart_upload
    if checksum_crc32 is not None:
        kwargs["ChecksumCRC32"] = checksum_crc32
    if checksum_crc32_c is not None:
        kwargs["ChecksumCRC32C"] = checksum_crc32_c
    if checksum_crc64_nvme is not None:
        kwargs["ChecksumCRC64NVME"] = checksum_crc64_nvme
    if checksum_sha1 is not None:
        kwargs["ChecksumSHA1"] = checksum_sha1
    if checksum_sha256 is not None:
        kwargs["ChecksumSHA256"] = checksum_sha256
    if checksum_type is not None:
        kwargs["ChecksumType"] = checksum_type
    if mpu_object_size is not None:
        kwargs["MpuObjectSize"] = mpu_object_size
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    if if_none_match is not None:
        kwargs["IfNoneMatch"] = if_none_match
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    try:
        resp = await client.call("CompleteMultipartUpload", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to complete multipart upload") from exc
    return CompleteMultipartUploadResult(
        location=resp.get("Location"),
        bucket=resp.get("Bucket"),
        key=resp.get("Key"),
        expiration=resp.get("Expiration"),
        e_tag=resp.get("ETag"),
        checksum_crc32=resp.get("ChecksumCRC32"),
        checksum_crc32_c=resp.get("ChecksumCRC32C"),
        checksum_crc64_nvme=resp.get("ChecksumCRC64NVME"),
        checksum_sha1=resp.get("ChecksumSHA1"),
        checksum_sha256=resp.get("ChecksumSHA256"),
        checksum_type=resp.get("ChecksumType"),
        server_side_encryption=resp.get("ServerSideEncryption"),
        version_id=resp.get("VersionId"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        request_charged=resp.get("RequestCharged"),
    )


async def create_bucket(
    bucket: str,
    *,
    acl: str | None = None,
    create_bucket_configuration: dict[str, Any] | None = None,
    grant_full_control: str | None = None,
    grant_read: str | None = None,
    grant_read_acp: str | None = None,
    grant_write: str | None = None,
    grant_write_acp: str | None = None,
    object_lock_enabled_for_bucket: bool | None = None,
    object_ownership: str | None = None,
    region_name: str | None = None,
) -> CreateBucketResult:
    """Create bucket.

    Args:
        bucket: Bucket.
        acl: Acl.
        create_bucket_configuration: Create bucket configuration.
        grant_full_control: Grant full control.
        grant_read: Grant read.
        grant_read_acp: Grant read acp.
        grant_write: Grant write.
        grant_write_acp: Grant write acp.
        object_lock_enabled_for_bucket: Object lock enabled for bucket.
        object_ownership: Object ownership.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if acl is not None:
        kwargs["ACL"] = acl
    if create_bucket_configuration is not None:
        kwargs["CreateBucketConfiguration"] = create_bucket_configuration
    if grant_full_control is not None:
        kwargs["GrantFullControl"] = grant_full_control
    if grant_read is not None:
        kwargs["GrantRead"] = grant_read
    if grant_read_acp is not None:
        kwargs["GrantReadACP"] = grant_read_acp
    if grant_write is not None:
        kwargs["GrantWrite"] = grant_write
    if grant_write_acp is not None:
        kwargs["GrantWriteACP"] = grant_write_acp
    if object_lock_enabled_for_bucket is not None:
        kwargs["ObjectLockEnabledForBucket"] = object_lock_enabled_for_bucket
    if object_ownership is not None:
        kwargs["ObjectOwnership"] = object_ownership
    try:
        resp = await client.call("CreateBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bucket") from exc
    return CreateBucketResult(
        location=resp.get("Location"),
        bucket_arn=resp.get("BucketArn"),
    )


async def create_bucket_metadata_configuration(
    bucket: str,
    metadata_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create bucket metadata configuration.

    Args:
        bucket: Bucket.
        metadata_configuration: Metadata configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["MetadataConfiguration"] = metadata_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("CreateBucketMetadataConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bucket metadata configuration") from exc
    return None


async def create_bucket_metadata_table_configuration(
    bucket: str,
    metadata_table_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create bucket metadata table configuration.

    Args:
        bucket: Bucket.
        metadata_table_configuration: Metadata table configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["MetadataTableConfiguration"] = metadata_table_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("CreateBucketMetadataTableConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bucket metadata table configuration") from exc
    return None


async def create_multipart_upload(
    bucket: str,
    key: str,
    *,
    acl: str | None = None,
    cache_control: str | None = None,
    content_disposition: str | None = None,
    content_encoding: str | None = None,
    content_language: str | None = None,
    content_type: str | None = None,
    expires: str | None = None,
    grant_full_control: str | None = None,
    grant_read: str | None = None,
    grant_read_acp: str | None = None,
    grant_write_acp: str | None = None,
    metadata: dict[str, Any] | None = None,
    server_side_encryption: str | None = None,
    storage_class: str | None = None,
    website_redirect_location: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    ssekms_key_id: str | None = None,
    ssekms_encryption_context: str | None = None,
    bucket_key_enabled: bool | None = None,
    request_payer: str | None = None,
    tagging: str | None = None,
    object_lock_mode: str | None = None,
    object_lock_retain_until_date: str | None = None,
    object_lock_legal_hold_status: str | None = None,
    expected_bucket_owner: str | None = None,
    checksum_algorithm: str | None = None,
    checksum_type: str | None = None,
    region_name: str | None = None,
) -> CreateMultipartUploadResult:
    """Create multipart upload.

    Args:
        bucket: Bucket.
        key: Key.
        acl: Acl.
        cache_control: Cache control.
        content_disposition: Content disposition.
        content_encoding: Content encoding.
        content_language: Content language.
        content_type: Content type.
        expires: Expires.
        grant_full_control: Grant full control.
        grant_read: Grant read.
        grant_read_acp: Grant read acp.
        grant_write_acp: Grant write acp.
        metadata: Metadata.
        server_side_encryption: Server side encryption.
        storage_class: Storage class.
        website_redirect_location: Website redirect location.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        ssekms_key_id: Ssekms key id.
        ssekms_encryption_context: Ssekms encryption context.
        bucket_key_enabled: Bucket key enabled.
        request_payer: Request payer.
        tagging: Tagging.
        object_lock_mode: Object lock mode.
        object_lock_retain_until_date: Object lock retain until date.
        object_lock_legal_hold_status: Object lock legal hold status.
        expected_bucket_owner: Expected bucket owner.
        checksum_algorithm: Checksum algorithm.
        checksum_type: Checksum type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if acl is not None:
        kwargs["ACL"] = acl
    if cache_control is not None:
        kwargs["CacheControl"] = cache_control
    if content_disposition is not None:
        kwargs["ContentDisposition"] = content_disposition
    if content_encoding is not None:
        kwargs["ContentEncoding"] = content_encoding
    if content_language is not None:
        kwargs["ContentLanguage"] = content_language
    if content_type is not None:
        kwargs["ContentType"] = content_type
    if expires is not None:
        kwargs["Expires"] = expires
    if grant_full_control is not None:
        kwargs["GrantFullControl"] = grant_full_control
    if grant_read is not None:
        kwargs["GrantRead"] = grant_read
    if grant_read_acp is not None:
        kwargs["GrantReadACP"] = grant_read_acp
    if grant_write_acp is not None:
        kwargs["GrantWriteACP"] = grant_write_acp
    if metadata is not None:
        kwargs["Metadata"] = metadata
    if server_side_encryption is not None:
        kwargs["ServerSideEncryption"] = server_side_encryption
    if storage_class is not None:
        kwargs["StorageClass"] = storage_class
    if website_redirect_location is not None:
        kwargs["WebsiteRedirectLocation"] = website_redirect_location
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if ssekms_key_id is not None:
        kwargs["SSEKMSKeyId"] = ssekms_key_id
    if ssekms_encryption_context is not None:
        kwargs["SSEKMSEncryptionContext"] = ssekms_encryption_context
    if bucket_key_enabled is not None:
        kwargs["BucketKeyEnabled"] = bucket_key_enabled
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if tagging is not None:
        kwargs["Tagging"] = tagging
    if object_lock_mode is not None:
        kwargs["ObjectLockMode"] = object_lock_mode
    if object_lock_retain_until_date is not None:
        kwargs["ObjectLockRetainUntilDate"] = object_lock_retain_until_date
    if object_lock_legal_hold_status is not None:
        kwargs["ObjectLockLegalHoldStatus"] = object_lock_legal_hold_status
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if checksum_type is not None:
        kwargs["ChecksumType"] = checksum_type
    try:
        resp = await client.call("CreateMultipartUpload", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create multipart upload") from exc
    return CreateMultipartUploadResult(
        abort_date=resp.get("AbortDate"),
        abort_rule_id=resp.get("AbortRuleId"),
        bucket=resp.get("Bucket"),
        key=resp.get("Key"),
        upload_id=resp.get("UploadId"),
        server_side_encryption=resp.get("ServerSideEncryption"),
        sse_customer_algorithm=resp.get("SSECustomerAlgorithm"),
        sse_customer_key_md5=resp.get("SSECustomerKeyMD5"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        ssekms_encryption_context=resp.get("SSEKMSEncryptionContext"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        request_charged=resp.get("RequestCharged"),
        checksum_algorithm=resp.get("ChecksumAlgorithm"),
        checksum_type=resp.get("ChecksumType"),
    )


async def create_session(
    bucket: str,
    *,
    session_mode: str | None = None,
    server_side_encryption: str | None = None,
    ssekms_key_id: str | None = None,
    ssekms_encryption_context: str | None = None,
    bucket_key_enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateSessionResult:
    """Create session.

    Args:
        bucket: Bucket.
        session_mode: Session mode.
        server_side_encryption: Server side encryption.
        ssekms_key_id: Ssekms key id.
        ssekms_encryption_context: Ssekms encryption context.
        bucket_key_enabled: Bucket key enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if session_mode is not None:
        kwargs["SessionMode"] = session_mode
    if server_side_encryption is not None:
        kwargs["ServerSideEncryption"] = server_side_encryption
    if ssekms_key_id is not None:
        kwargs["SSEKMSKeyId"] = ssekms_key_id
    if ssekms_encryption_context is not None:
        kwargs["SSEKMSEncryptionContext"] = ssekms_encryption_context
    if bucket_key_enabled is not None:
        kwargs["BucketKeyEnabled"] = bucket_key_enabled
    try:
        resp = await client.call("CreateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create session") from exc
    return CreateSessionResult(
        server_side_encryption=resp.get("ServerSideEncryption"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        ssekms_encryption_context=resp.get("SSEKMSEncryptionContext"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        credentials=resp.get("Credentials"),
    )


async def delete_bucket(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket") from exc
    return None


async def delete_bucket_analytics_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket analytics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketAnalyticsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket analytics configuration") from exc
    return None


async def delete_bucket_cors(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket cors.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketCors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket cors") from exc
    return None


async def delete_bucket_encryption(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket encryption.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket encryption") from exc
    return None


async def delete_bucket_intelligent_tiering_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket intelligent tiering configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketIntelligentTieringConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to delete bucket intelligent tiering configuration"
        ) from exc
    return None


async def delete_bucket_inventory_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket inventory configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketInventoryConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket inventory configuration") from exc
    return None


async def delete_bucket_lifecycle(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket lifecycle.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketLifecycle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket lifecycle") from exc
    return None


async def delete_bucket_metadata_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket metadata configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketMetadataConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket metadata configuration") from exc
    return None


async def delete_bucket_metadata_table_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket metadata table configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketMetadataTableConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket metadata table configuration") from exc
    return None


async def delete_bucket_metrics_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket metrics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketMetricsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket metrics configuration") from exc
    return None


async def delete_bucket_ownership_controls(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket ownership controls.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketOwnershipControls", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket ownership controls") from exc
    return None


async def delete_bucket_policy(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket policy.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket policy") from exc
    return None


async def delete_bucket_replication(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket replication.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket replication") from exc
    return None


async def delete_bucket_tagging(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket tagging.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket tagging") from exc
    return None


async def delete_bucket_website(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete bucket website.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeleteBucketWebsite", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket website") from exc
    return None


async def delete_object_tagging(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> DeleteObjectTaggingResult:
    """Delete object tagging.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("DeleteObjectTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete object tagging") from exc
    return DeleteObjectTaggingResult(
        version_id=resp.get("VersionId"),
    )


async def delete_objects(
    bucket: str,
    delete: dict[str, Any],
    *,
    mfa: str | None = None,
    request_payer: str | None = None,
    bypass_governance_retention: bool | None = None,
    expected_bucket_owner: str | None = None,
    checksum_algorithm: str | None = None,
    region_name: str | None = None,
) -> DeleteObjectsResult:
    """Delete objects.

    Args:
        bucket: Bucket.
        delete: Delete.
        mfa: Mfa.
        request_payer: Request payer.
        bypass_governance_retention: Bypass governance retention.
        expected_bucket_owner: Expected bucket owner.
        checksum_algorithm: Checksum algorithm.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Delete"] = delete
    if mfa is not None:
        kwargs["MFA"] = mfa
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if bypass_governance_retention is not None:
        kwargs["BypassGovernanceRetention"] = bypass_governance_retention
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    try:
        resp = await client.call("DeleteObjects", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete objects") from exc
    return DeleteObjectsResult(
        deleted=resp.get("Deleted"),
        request_charged=resp.get("RequestCharged"),
        errors=resp.get("Errors"),
    )


async def delete_public_access_block(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete public access block.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("DeletePublicAccessBlock", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete public access block") from exc
    return None


async def get_bucket_accelerate_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    request_payer: str | None = None,
    region_name: str | None = None,
) -> GetBucketAccelerateConfigurationResult:
    """Get bucket accelerate configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        request_payer: Request payer.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    try:
        resp = await client.call("GetBucketAccelerateConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket accelerate configuration") from exc
    return GetBucketAccelerateConfigurationResult(
        status=resp.get("Status"),
        request_charged=resp.get("RequestCharged"),
    )


async def get_bucket_acl(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketAclResult:
    """Get bucket acl.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketAcl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket acl") from exc
    return GetBucketAclResult(
        owner=resp.get("Owner"),
        grants=resp.get("Grants"),
    )


async def get_bucket_analytics_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketAnalyticsConfigurationResult:
    """Get bucket analytics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketAnalyticsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket analytics configuration") from exc
    return GetBucketAnalyticsConfigurationResult(
        analytics_configuration=resp.get("AnalyticsConfiguration"),
    )


async def get_bucket_cors(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketCorsResult:
    """Get bucket cors.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketCors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket cors") from exc
    return GetBucketCorsResult(
        cors_rules=resp.get("CORSRules"),
    )


async def get_bucket_encryption(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketEncryptionResult:
    """Get bucket encryption.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket encryption") from exc
    return GetBucketEncryptionResult(
        server_side_encryption_configuration=resp.get("ServerSideEncryptionConfiguration"),
    )


async def get_bucket_intelligent_tiering_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketIntelligentTieringConfigurationResult:
    """Get bucket intelligent tiering configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketIntelligentTieringConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket intelligent tiering configuration") from exc
    return GetBucketIntelligentTieringConfigurationResult(
        intelligent_tiering_configuration=resp.get("IntelligentTieringConfiguration"),
    )


async def get_bucket_inventory_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketInventoryConfigurationResult:
    """Get bucket inventory configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketInventoryConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket inventory configuration") from exc
    return GetBucketInventoryConfigurationResult(
        inventory_configuration=resp.get("InventoryConfiguration"),
    )


async def get_bucket_lifecycle(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketLifecycleResult:
    """Get bucket lifecycle.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketLifecycle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket lifecycle") from exc
    return GetBucketLifecycleResult(
        rules=resp.get("Rules"),
    )


async def get_bucket_lifecycle_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketLifecycleConfigurationResult:
    """Get bucket lifecycle configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketLifecycleConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket lifecycle configuration") from exc
    return GetBucketLifecycleConfigurationResult(
        rules=resp.get("Rules"),
        transition_default_minimum_object_size=resp.get("TransitionDefaultMinimumObjectSize"),
    )


async def get_bucket_location(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketLocationResult:
    """Get bucket location.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketLocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket location") from exc
    return GetBucketLocationResult(
        location_constraint=resp.get("LocationConstraint"),
    )


async def get_bucket_logging(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketLoggingResult:
    """Get bucket logging.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketLogging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket logging") from exc
    return GetBucketLoggingResult(
        logging_enabled=resp.get("LoggingEnabled"),
    )


async def get_bucket_metadata_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketMetadataConfigurationResult:
    """Get bucket metadata configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketMetadataConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket metadata configuration") from exc
    return GetBucketMetadataConfigurationResult(
        get_bucket_metadata_configuration_result=resp.get("GetBucketMetadataConfigurationResult"),
    )


async def get_bucket_metadata_table_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketMetadataTableConfigurationResult:
    """Get bucket metadata table configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketMetadataTableConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket metadata table configuration") from exc
    return GetBucketMetadataTableConfigurationResult(
        get_bucket_metadata_table_configuration_result=resp.get(
            "GetBucketMetadataTableConfigurationResult"
        ),
    )


async def get_bucket_metrics_configuration(
    bucket: str,
    id: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketMetricsConfigurationResult:
    """Get bucket metrics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketMetricsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket metrics configuration") from exc
    return GetBucketMetricsConfigurationResult(
        metrics_configuration=resp.get("MetricsConfiguration"),
    )


async def get_bucket_notification(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketNotificationResult:
    """Get bucket notification.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketNotification", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket notification") from exc
    return GetBucketNotificationResult(
        topic_configuration=resp.get("TopicConfiguration"),
        queue_configuration=resp.get("QueueConfiguration"),
        cloud_function_configuration=resp.get("CloudFunctionConfiguration"),
    )


async def get_bucket_notification_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketNotificationConfigurationResult:
    """Get bucket notification configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketNotificationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket notification configuration") from exc
    return GetBucketNotificationConfigurationResult(
        topic_configurations=resp.get("TopicConfigurations"),
        queue_configurations=resp.get("QueueConfigurations"),
        lambda_function_configurations=resp.get("LambdaFunctionConfigurations"),
        event_bridge_configuration=resp.get("EventBridgeConfiguration"),
    )


async def get_bucket_ownership_controls(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketOwnershipControlsResult:
    """Get bucket ownership controls.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketOwnershipControls", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket ownership controls") from exc
    return GetBucketOwnershipControlsResult(
        ownership_controls=resp.get("OwnershipControls"),
    )


async def get_bucket_policy(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketPolicyResult:
    """Get bucket policy.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket policy") from exc
    return GetBucketPolicyResult(
        policy=resp.get("Policy"),
    )


async def get_bucket_policy_status(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketPolicyStatusResult:
    """Get bucket policy status.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketPolicyStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket policy status") from exc
    return GetBucketPolicyStatusResult(
        policy_status=resp.get("PolicyStatus"),
    )


async def get_bucket_replication(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketReplicationResult:
    """Get bucket replication.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket replication") from exc
    return GetBucketReplicationResult(
        replication_configuration=resp.get("ReplicationConfiguration"),
    )


async def get_bucket_request_payment(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketRequestPaymentResult:
    """Get bucket request payment.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketRequestPayment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket request payment") from exc
    return GetBucketRequestPaymentResult(
        payer=resp.get("Payer"),
    )


async def get_bucket_tagging(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketTaggingResult:
    """Get bucket tagging.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket tagging") from exc
    return GetBucketTaggingResult(
        tag_set=resp.get("TagSet"),
    )


async def get_bucket_versioning(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketVersioningResult:
    """Get bucket versioning.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketVersioning", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket versioning") from exc
    return GetBucketVersioningResult(
        status=resp.get("Status"),
        mfa_delete=resp.get("MFADelete"),
    )


async def get_bucket_website(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetBucketWebsiteResult:
    """Get bucket website.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetBucketWebsite", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket website") from exc
    return GetBucketWebsiteResult(
        redirect_all_requests_to=resp.get("RedirectAllRequestsTo"),
        index_document=resp.get("IndexDocument"),
        error_document=resp.get("ErrorDocument"),
        routing_rules=resp.get("RoutingRules"),
    )


async def get_object_acl(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectAclResult:
    """Get object acl.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectAcl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object acl") from exc
    return GetObjectAclResult(
        owner=resp.get("Owner"),
        grants=resp.get("Grants"),
        request_charged=resp.get("RequestCharged"),
    )


async def get_object_attributes(
    bucket: str,
    key: str,
    object_attributes: list[str],
    *,
    version_id: str | None = None,
    max_parts: int | None = None,
    part_number_marker: int | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectAttributesResult:
    """Get object attributes.

    Args:
        bucket: Bucket.
        key: Key.
        object_attributes: Object attributes.
        version_id: Version id.
        max_parts: Max parts.
        part_number_marker: Part number marker.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["ObjectAttributes"] = object_attributes
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if max_parts is not None:
        kwargs["MaxParts"] = max_parts
    if part_number_marker is not None:
        kwargs["PartNumberMarker"] = part_number_marker
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object attributes") from exc
    return GetObjectAttributesResult(
        delete_marker=resp.get("DeleteMarker"),
        last_modified=resp.get("LastModified"),
        version_id=resp.get("VersionId"),
        request_charged=resp.get("RequestCharged"),
        e_tag=resp.get("ETag"),
        checksum=resp.get("Checksum"),
        object_parts=resp.get("ObjectParts"),
        storage_class=resp.get("StorageClass"),
        object_size=resp.get("ObjectSize"),
    )


async def get_object_legal_hold(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectLegalHoldResult:
    """Get object legal hold.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectLegalHold", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object legal hold") from exc
    return GetObjectLegalHoldResult(
        legal_hold=resp.get("LegalHold"),
    )


async def get_object_lock_configuration(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectLockConfigurationResult:
    """Get object lock configuration.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectLockConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object lock configuration") from exc
    return GetObjectLockConfigurationResult(
        object_lock_configuration=resp.get("ObjectLockConfiguration"),
    )


async def get_object_retention(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectRetentionResult:
    """Get object retention.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectRetention", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object retention") from exc
    return GetObjectRetentionResult(
        retention=resp.get("Retention"),
    )


async def get_object_tagging(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    expected_bucket_owner: str | None = None,
    request_payer: str | None = None,
    region_name: str | None = None,
) -> GetObjectTaggingResult:
    """Get object tagging.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        expected_bucket_owner: Expected bucket owner.
        request_payer: Request payer.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    try:
        resp = await client.call("GetObjectTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object tagging") from exc
    return GetObjectTaggingResult(
        version_id=resp.get("VersionId"),
        tag_set=resp.get("TagSet"),
    )


async def get_object_torrent(
    bucket: str,
    key: str,
    *,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetObjectTorrentResult:
    """Get object torrent.

    Args:
        bucket: Bucket.
        key: Key.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetObjectTorrent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get object torrent") from exc
    return GetObjectTorrentResult(
        body=resp.get("Body"),
        request_charged=resp.get("RequestCharged"),
    )


async def get_public_access_block(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> GetPublicAccessBlockResult:
    """Get public access block.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("GetPublicAccessBlock", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get public access block") from exc
    return GetPublicAccessBlockResult(
        public_access_block_configuration=resp.get("PublicAccessBlockConfiguration"),
    )


async def head_bucket(
    bucket: str,
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> HeadBucketResult:
    """Head bucket.

    Args:
        bucket: Bucket.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("HeadBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to head bucket") from exc
    return HeadBucketResult(
        bucket_arn=resp.get("BucketArn"),
        bucket_location_type=resp.get("BucketLocationType"),
        bucket_location_name=resp.get("BucketLocationName"),
        bucket_region=resp.get("BucketRegion"),
        access_point_alias=resp.get("AccessPointAlias"),
    )


async def head_object(
    bucket: str,
    key: str,
    *,
    if_match: str | None = None,
    if_modified_since: str | None = None,
    if_none_match: str | None = None,
    if_unmodified_since: str | None = None,
    range: str | None = None,
    response_cache_control: str | None = None,
    response_content_disposition: str | None = None,
    response_content_encoding: str | None = None,
    response_content_language: str | None = None,
    response_content_type: str | None = None,
    response_expires: str | None = None,
    version_id: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    request_payer: str | None = None,
    part_number: int | None = None,
    expected_bucket_owner: str | None = None,
    checksum_mode: str | None = None,
    region_name: str | None = None,
) -> HeadObjectResult:
    """Head object.

    Args:
        bucket: Bucket.
        key: Key.
        if_match: If match.
        if_modified_since: If modified since.
        if_none_match: If none match.
        if_unmodified_since: If unmodified since.
        range: Range.
        response_cache_control: Response cache control.
        response_content_disposition: Response content disposition.
        response_content_encoding: Response content encoding.
        response_content_language: Response content language.
        response_content_type: Response content type.
        response_expires: Response expires.
        version_id: Version id.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        request_payer: Request payer.
        part_number: Part number.
        expected_bucket_owner: Expected bucket owner.
        checksum_mode: Checksum mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    if if_modified_since is not None:
        kwargs["IfModifiedSince"] = if_modified_since
    if if_none_match is not None:
        kwargs["IfNoneMatch"] = if_none_match
    if if_unmodified_since is not None:
        kwargs["IfUnmodifiedSince"] = if_unmodified_since
    if range is not None:
        kwargs["Range"] = range
    if response_cache_control is not None:
        kwargs["ResponseCacheControl"] = response_cache_control
    if response_content_disposition is not None:
        kwargs["ResponseContentDisposition"] = response_content_disposition
    if response_content_encoding is not None:
        kwargs["ResponseContentEncoding"] = response_content_encoding
    if response_content_language is not None:
        kwargs["ResponseContentLanguage"] = response_content_language
    if response_content_type is not None:
        kwargs["ResponseContentType"] = response_content_type
    if response_expires is not None:
        kwargs["ResponseExpires"] = response_expires
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if part_number is not None:
        kwargs["PartNumber"] = part_number
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if checksum_mode is not None:
        kwargs["ChecksumMode"] = checksum_mode
    try:
        resp = await client.call("HeadObject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to head object") from exc
    return HeadObjectResult(
        delete_marker=resp.get("DeleteMarker"),
        accept_ranges=resp.get("AcceptRanges"),
        expiration=resp.get("Expiration"),
        restore=resp.get("Restore"),
        archive_status=resp.get("ArchiveStatus"),
        last_modified=resp.get("LastModified"),
        content_length=resp.get("ContentLength"),
        checksum_crc32=resp.get("ChecksumCRC32"),
        checksum_crc32_c=resp.get("ChecksumCRC32C"),
        checksum_crc64_nvme=resp.get("ChecksumCRC64NVME"),
        checksum_sha1=resp.get("ChecksumSHA1"),
        checksum_sha256=resp.get("ChecksumSHA256"),
        checksum_type=resp.get("ChecksumType"),
        e_tag=resp.get("ETag"),
        missing_meta=resp.get("MissingMeta"),
        version_id=resp.get("VersionId"),
        cache_control=resp.get("CacheControl"),
        content_disposition=resp.get("ContentDisposition"),
        content_encoding=resp.get("ContentEncoding"),
        content_language=resp.get("ContentLanguage"),
        content_type=resp.get("ContentType"),
        content_range=resp.get("ContentRange"),
        expires=resp.get("Expires"),
        website_redirect_location=resp.get("WebsiteRedirectLocation"),
        server_side_encryption=resp.get("ServerSideEncryption"),
        metadata=resp.get("Metadata"),
        sse_customer_algorithm=resp.get("SSECustomerAlgorithm"),
        sse_customer_key_md5=resp.get("SSECustomerKeyMD5"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        storage_class=resp.get("StorageClass"),
        request_charged=resp.get("RequestCharged"),
        replication_status=resp.get("ReplicationStatus"),
        parts_count=resp.get("PartsCount"),
        tag_count=resp.get("TagCount"),
        object_lock_mode=resp.get("ObjectLockMode"),
        object_lock_retain_until_date=resp.get("ObjectLockRetainUntilDate"),
        object_lock_legal_hold_status=resp.get("ObjectLockLegalHoldStatus"),
    )


async def list_bucket_analytics_configurations(
    bucket: str,
    *,
    continuation_token: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> ListBucketAnalyticsConfigurationsResult:
    """List bucket analytics configurations.

    Args:
        bucket: Bucket.
        continuation_token: Continuation token.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("ListBucketAnalyticsConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bucket analytics configurations") from exc
    return ListBucketAnalyticsConfigurationsResult(
        is_truncated=resp.get("IsTruncated"),
        continuation_token=resp.get("ContinuationToken"),
        next_continuation_token=resp.get("NextContinuationToken"),
        analytics_configuration_list=resp.get("AnalyticsConfigurationList"),
    )


async def list_bucket_intelligent_tiering_configurations(
    bucket: str,
    *,
    continuation_token: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> ListBucketIntelligentTieringConfigurationsResult:
    """List bucket intelligent tiering configurations.

    Args:
        bucket: Bucket.
        continuation_token: Continuation token.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("ListBucketIntelligentTieringConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list bucket intelligent tiering configurations"
        ) from exc
    return ListBucketIntelligentTieringConfigurationsResult(
        is_truncated=resp.get("IsTruncated"),
        continuation_token=resp.get("ContinuationToken"),
        next_continuation_token=resp.get("NextContinuationToken"),
        intelligent_tiering_configuration_list=resp.get("IntelligentTieringConfigurationList"),
    )


async def list_bucket_inventory_configurations(
    bucket: str,
    *,
    continuation_token: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> ListBucketInventoryConfigurationsResult:
    """List bucket inventory configurations.

    Args:
        bucket: Bucket.
        continuation_token: Continuation token.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("ListBucketInventoryConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bucket inventory configurations") from exc
    return ListBucketInventoryConfigurationsResult(
        continuation_token=resp.get("ContinuationToken"),
        inventory_configuration_list=resp.get("InventoryConfigurationList"),
        is_truncated=resp.get("IsTruncated"),
        next_continuation_token=resp.get("NextContinuationToken"),
    )


async def list_bucket_metrics_configurations(
    bucket: str,
    *,
    continuation_token: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> ListBucketMetricsConfigurationsResult:
    """List bucket metrics configurations.

    Args:
        bucket: Bucket.
        continuation_token: Continuation token.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("ListBucketMetricsConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bucket metrics configurations") from exc
    return ListBucketMetricsConfigurationsResult(
        is_truncated=resp.get("IsTruncated"),
        continuation_token=resp.get("ContinuationToken"),
        next_continuation_token=resp.get("NextContinuationToken"),
        metrics_configuration_list=resp.get("MetricsConfigurationList"),
    )


async def list_buckets(
    *,
    max_buckets: int | None = None,
    continuation_token: str | None = None,
    prefix: str | None = None,
    bucket_region: str | None = None,
    region_name: str | None = None,
) -> ListBucketsResult:
    """List buckets.

    Args:
        max_buckets: Max buckets.
        continuation_token: Continuation token.
        prefix: Prefix.
        bucket_region: Bucket region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    if max_buckets is not None:
        kwargs["MaxBuckets"] = max_buckets
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if prefix is not None:
        kwargs["Prefix"] = prefix
    if bucket_region is not None:
        kwargs["BucketRegion"] = bucket_region
    try:
        resp = await client.call("ListBuckets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list buckets") from exc
    return ListBucketsResult(
        buckets=resp.get("Buckets"),
        owner=resp.get("Owner"),
        continuation_token=resp.get("ContinuationToken"),
        prefix=resp.get("Prefix"),
    )


async def list_directory_buckets(
    *,
    continuation_token: str | None = None,
    max_directory_buckets: int | None = None,
    region_name: str | None = None,
) -> ListDirectoryBucketsResult:
    """List directory buckets.

    Args:
        continuation_token: Continuation token.
        max_directory_buckets: Max directory buckets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if max_directory_buckets is not None:
        kwargs["MaxDirectoryBuckets"] = max_directory_buckets
    try:
        resp = await client.call("ListDirectoryBuckets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list directory buckets") from exc
    return ListDirectoryBucketsResult(
        buckets=resp.get("Buckets"),
        continuation_token=resp.get("ContinuationToken"),
    )


async def list_multipart_uploads(
    bucket: str,
    *,
    delimiter: str | None = None,
    encoding_type: str | None = None,
    key_marker: str | None = None,
    max_uploads: int | None = None,
    prefix: str | None = None,
    upload_id_marker: str | None = None,
    expected_bucket_owner: str | None = None,
    request_payer: str | None = None,
    region_name: str | None = None,
) -> ListMultipartUploadsResult:
    """List multipart uploads.

    Args:
        bucket: Bucket.
        delimiter: Delimiter.
        encoding_type: Encoding type.
        key_marker: Key marker.
        max_uploads: Max uploads.
        prefix: Prefix.
        upload_id_marker: Upload id marker.
        expected_bucket_owner: Expected bucket owner.
        request_payer: Request payer.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if delimiter is not None:
        kwargs["Delimiter"] = delimiter
    if encoding_type is not None:
        kwargs["EncodingType"] = encoding_type
    if key_marker is not None:
        kwargs["KeyMarker"] = key_marker
    if max_uploads is not None:
        kwargs["MaxUploads"] = max_uploads
    if prefix is not None:
        kwargs["Prefix"] = prefix
    if upload_id_marker is not None:
        kwargs["UploadIdMarker"] = upload_id_marker
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    try:
        resp = await client.call("ListMultipartUploads", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list multipart uploads") from exc
    return ListMultipartUploadsResult(
        bucket=resp.get("Bucket"),
        key_marker=resp.get("KeyMarker"),
        upload_id_marker=resp.get("UploadIdMarker"),
        next_key_marker=resp.get("NextKeyMarker"),
        prefix=resp.get("Prefix"),
        delimiter=resp.get("Delimiter"),
        next_upload_id_marker=resp.get("NextUploadIdMarker"),
        max_uploads=resp.get("MaxUploads"),
        is_truncated=resp.get("IsTruncated"),
        uploads=resp.get("Uploads"),
        common_prefixes=resp.get("CommonPrefixes"),
        encoding_type=resp.get("EncodingType"),
        request_charged=resp.get("RequestCharged"),
    )


async def list_objects_v2(
    bucket: str,
    *,
    delimiter: str | None = None,
    encoding_type: str | None = None,
    max_keys: int | None = None,
    prefix: str | None = None,
    continuation_token: str | None = None,
    fetch_owner: bool | None = None,
    start_after: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    optional_object_attributes: list[str] | None = None,
    region_name: str | None = None,
) -> ListObjectsV2Result:
    """List objects v2.

    Args:
        bucket: Bucket.
        delimiter: Delimiter.
        encoding_type: Encoding type.
        max_keys: Max keys.
        prefix: Prefix.
        continuation_token: Continuation token.
        fetch_owner: Fetch owner.
        start_after: Start after.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        optional_object_attributes: Optional object attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if delimiter is not None:
        kwargs["Delimiter"] = delimiter
    if encoding_type is not None:
        kwargs["EncodingType"] = encoding_type
    if max_keys is not None:
        kwargs["MaxKeys"] = max_keys
    if prefix is not None:
        kwargs["Prefix"] = prefix
    if continuation_token is not None:
        kwargs["ContinuationToken"] = continuation_token
    if fetch_owner is not None:
        kwargs["FetchOwner"] = fetch_owner
    if start_after is not None:
        kwargs["StartAfter"] = start_after
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if optional_object_attributes is not None:
        kwargs["OptionalObjectAttributes"] = optional_object_attributes
    try:
        resp = await client.call("ListObjectsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list objects v2") from exc
    return ListObjectsV2Result(
        is_truncated=resp.get("IsTruncated"),
        contents=resp.get("Contents"),
        name=resp.get("Name"),
        prefix=resp.get("Prefix"),
        delimiter=resp.get("Delimiter"),
        max_keys=resp.get("MaxKeys"),
        common_prefixes=resp.get("CommonPrefixes"),
        encoding_type=resp.get("EncodingType"),
        key_count=resp.get("KeyCount"),
        continuation_token=resp.get("ContinuationToken"),
        next_continuation_token=resp.get("NextContinuationToken"),
        start_after=resp.get("StartAfter"),
        request_charged=resp.get("RequestCharged"),
    )


async def list_parts(
    bucket: str,
    key: str,
    upload_id: str,
    *,
    max_parts: int | None = None,
    part_number_marker: int | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    region_name: str | None = None,
) -> ListPartsResult:
    """List parts.

    Args:
        bucket: Bucket.
        key: Key.
        upload_id: Upload id.
        max_parts: Max parts.
        part_number_marker: Part number marker.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["UploadId"] = upload_id
    if max_parts is not None:
        kwargs["MaxParts"] = max_parts
    if part_number_marker is not None:
        kwargs["PartNumberMarker"] = part_number_marker
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    try:
        resp = await client.call("ListParts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list parts") from exc
    return ListPartsResult(
        abort_date=resp.get("AbortDate"),
        abort_rule_id=resp.get("AbortRuleId"),
        bucket=resp.get("Bucket"),
        key=resp.get("Key"),
        upload_id=resp.get("UploadId"),
        part_number_marker=resp.get("PartNumberMarker"),
        next_part_number_marker=resp.get("NextPartNumberMarker"),
        max_parts=resp.get("MaxParts"),
        is_truncated=resp.get("IsTruncated"),
        parts=resp.get("Parts"),
        initiator=resp.get("Initiator"),
        owner=resp.get("Owner"),
        storage_class=resp.get("StorageClass"),
        request_charged=resp.get("RequestCharged"),
        checksum_algorithm=resp.get("ChecksumAlgorithm"),
        checksum_type=resp.get("ChecksumType"),
    )


async def put_bucket_accelerate_configuration(
    bucket: str,
    accelerate_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    checksum_algorithm: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket accelerate configuration.

    Args:
        bucket: Bucket.
        accelerate_configuration: Accelerate configuration.
        expected_bucket_owner: Expected bucket owner.
        checksum_algorithm: Checksum algorithm.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["AccelerateConfiguration"] = accelerate_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    try:
        await client.call("PutBucketAccelerateConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket accelerate configuration") from exc
    return None


async def put_bucket_acl(
    bucket: str,
    *,
    acl: str | None = None,
    access_control_policy: dict[str, Any] | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    grant_full_control: str | None = None,
    grant_read: str | None = None,
    grant_read_acp: str | None = None,
    grant_write: str | None = None,
    grant_write_acp: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket acl.

    Args:
        bucket: Bucket.
        acl: Acl.
        access_control_policy: Access control policy.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        grant_full_control: Grant full control.
        grant_read: Grant read.
        grant_read_acp: Grant read acp.
        grant_write: Grant write.
        grant_write_acp: Grant write acp.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if acl is not None:
        kwargs["ACL"] = acl
    if access_control_policy is not None:
        kwargs["AccessControlPolicy"] = access_control_policy
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if grant_full_control is not None:
        kwargs["GrantFullControl"] = grant_full_control
    if grant_read is not None:
        kwargs["GrantRead"] = grant_read
    if grant_read_acp is not None:
        kwargs["GrantReadACP"] = grant_read_acp
    if grant_write is not None:
        kwargs["GrantWrite"] = grant_write
    if grant_write_acp is not None:
        kwargs["GrantWriteACP"] = grant_write_acp
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketAcl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket acl") from exc
    return None


async def put_bucket_analytics_configuration(
    bucket: str,
    id: str,
    analytics_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket analytics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        analytics_configuration: Analytics configuration.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    kwargs["AnalyticsConfiguration"] = analytics_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketAnalyticsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket analytics configuration") from exc
    return None


async def put_bucket_cors(
    bucket: str,
    cors_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket cors.

    Args:
        bucket: Bucket.
        cors_configuration: Cors configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["CORSConfiguration"] = cors_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketCors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket cors") from exc
    return None


async def put_bucket_encryption(
    bucket: str,
    server_side_encryption_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket encryption.

    Args:
        bucket: Bucket.
        server_side_encryption_configuration: Server side encryption configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["ServerSideEncryptionConfiguration"] = server_side_encryption_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket encryption") from exc
    return None


async def put_bucket_intelligent_tiering_configuration(
    bucket: str,
    id: str,
    intelligent_tiering_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket intelligent tiering configuration.

    Args:
        bucket: Bucket.
        id: Id.
        intelligent_tiering_configuration: Intelligent tiering configuration.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    kwargs["IntelligentTieringConfiguration"] = intelligent_tiering_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketIntelligentTieringConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket intelligent tiering configuration") from exc
    return None


async def put_bucket_inventory_configuration(
    bucket: str,
    id: str,
    inventory_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket inventory configuration.

    Args:
        bucket: Bucket.
        id: Id.
        inventory_configuration: Inventory configuration.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    kwargs["InventoryConfiguration"] = inventory_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketInventoryConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket inventory configuration") from exc
    return None


async def put_bucket_lifecycle(
    bucket: str,
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    lifecycle_configuration: dict[str, Any] | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket lifecycle.

    Args:
        bucket: Bucket.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        lifecycle_configuration: Lifecycle configuration.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if lifecycle_configuration is not None:
        kwargs["LifecycleConfiguration"] = lifecycle_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketLifecycle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket lifecycle") from exc
    return None


async def put_bucket_lifecycle_configuration(
    bucket: str,
    *,
    checksum_algorithm: str | None = None,
    lifecycle_configuration: dict[str, Any] | None = None,
    expected_bucket_owner: str | None = None,
    transition_default_minimum_object_size: str | None = None,
    region_name: str | None = None,
) -> PutBucketLifecycleConfigurationResult:
    """Put bucket lifecycle configuration.

    Args:
        bucket: Bucket.
        checksum_algorithm: Checksum algorithm.
        lifecycle_configuration: Lifecycle configuration.
        expected_bucket_owner: Expected bucket owner.
        transition_default_minimum_object_size: Transition default minimum object size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if lifecycle_configuration is not None:
        kwargs["LifecycleConfiguration"] = lifecycle_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if transition_default_minimum_object_size is not None:
        kwargs["TransitionDefaultMinimumObjectSize"] = transition_default_minimum_object_size
    try:
        resp = await client.call("PutBucketLifecycleConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket lifecycle configuration") from exc
    return PutBucketLifecycleConfigurationResult(
        transition_default_minimum_object_size=resp.get("TransitionDefaultMinimumObjectSize"),
    )


async def put_bucket_logging(
    bucket: str,
    bucket_logging_status: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket logging.

    Args:
        bucket: Bucket.
        bucket_logging_status: Bucket logging status.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["BucketLoggingStatus"] = bucket_logging_status
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketLogging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket logging") from exc
    return None


async def put_bucket_metrics_configuration(
    bucket: str,
    id: str,
    metrics_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket metrics configuration.

    Args:
        bucket: Bucket.
        id: Id.
        metrics_configuration: Metrics configuration.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Id"] = id
    kwargs["MetricsConfiguration"] = metrics_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketMetricsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket metrics configuration") from exc
    return None


async def put_bucket_notification(
    bucket: str,
    notification_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket notification.

    Args:
        bucket: Bucket.
        notification_configuration: Notification configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["NotificationConfiguration"] = notification_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketNotification", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket notification") from exc
    return None


async def put_bucket_notification_configuration(
    bucket: str,
    notification_configuration: dict[str, Any],
    *,
    expected_bucket_owner: str | None = None,
    skip_destination_validation: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket notification configuration.

    Args:
        bucket: Bucket.
        notification_configuration: Notification configuration.
        expected_bucket_owner: Expected bucket owner.
        skip_destination_validation: Skip destination validation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["NotificationConfiguration"] = notification_configuration
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if skip_destination_validation is not None:
        kwargs["SkipDestinationValidation"] = skip_destination_validation
    try:
        await client.call("PutBucketNotificationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket notification configuration") from exc
    return None


async def put_bucket_ownership_controls(
    bucket: str,
    ownership_controls: dict[str, Any],
    *,
    content_md5: str | None = None,
    expected_bucket_owner: str | None = None,
    checksum_algorithm: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket ownership controls.

    Args:
        bucket: Bucket.
        ownership_controls: Ownership controls.
        content_md5: Content md5.
        expected_bucket_owner: Expected bucket owner.
        checksum_algorithm: Checksum algorithm.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["OwnershipControls"] = ownership_controls
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    try:
        await client.call("PutBucketOwnershipControls", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket ownership controls") from exc
    return None


async def put_bucket_policy(
    bucket: str,
    policy: str,
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    confirm_remove_self_bucket_access: bool | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket policy.

    Args:
        bucket: Bucket.
        policy: Policy.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        confirm_remove_self_bucket_access: Confirm remove self bucket access.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Policy"] = policy
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if confirm_remove_self_bucket_access is not None:
        kwargs["ConfirmRemoveSelfBucketAccess"] = confirm_remove_self_bucket_access
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket policy") from exc
    return None


async def put_bucket_replication(
    bucket: str,
    replication_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    token: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket replication.

    Args:
        bucket: Bucket.
        replication_configuration: Replication configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        token: Token.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["ReplicationConfiguration"] = replication_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if token is not None:
        kwargs["Token"] = token
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket replication") from exc
    return None


async def put_bucket_request_payment(
    bucket: str,
    request_payment_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket request payment.

    Args:
        bucket: Bucket.
        request_payment_configuration: Request payment configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["RequestPaymentConfiguration"] = request_payment_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketRequestPayment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket request payment") from exc
    return None


async def put_bucket_tagging(
    bucket: str,
    tagging: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket tagging.

    Args:
        bucket: Bucket.
        tagging: Tagging.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Tagging"] = tagging
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket tagging") from exc
    return None


async def put_bucket_versioning(
    bucket: str,
    versioning_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    mfa: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket versioning.

    Args:
        bucket: Bucket.
        versioning_configuration: Versioning configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        mfa: Mfa.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["VersioningConfiguration"] = versioning_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if mfa is not None:
        kwargs["MFA"] = mfa
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketVersioning", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket versioning") from exc
    return None


async def put_bucket_website(
    bucket: str,
    website_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put bucket website.

    Args:
        bucket: Bucket.
        website_configuration: Website configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["WebsiteConfiguration"] = website_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutBucketWebsite", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put bucket website") from exc
    return None


async def put_object(
    bucket: str,
    key: str,
    *,
    acl: str | None = None,
    body: bytes | None = None,
    cache_control: str | None = None,
    content_disposition: str | None = None,
    content_encoding: str | None = None,
    content_language: str | None = None,
    content_length: int | None = None,
    content_md5: str | None = None,
    content_type: str | None = None,
    checksum_algorithm: str | None = None,
    checksum_crc32: str | None = None,
    checksum_crc32_c: str | None = None,
    checksum_crc64_nvme: str | None = None,
    checksum_sha1: str | None = None,
    checksum_sha256: str | None = None,
    expires: str | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    grant_full_control: str | None = None,
    grant_read: str | None = None,
    grant_read_acp: str | None = None,
    grant_write_acp: str | None = None,
    write_offset_bytes: int | None = None,
    metadata: dict[str, Any] | None = None,
    server_side_encryption: str | None = None,
    storage_class: str | None = None,
    website_redirect_location: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    ssekms_key_id: str | None = None,
    ssekms_encryption_context: str | None = None,
    bucket_key_enabled: bool | None = None,
    request_payer: str | None = None,
    tagging: str | None = None,
    object_lock_mode: str | None = None,
    object_lock_retain_until_date: str | None = None,
    object_lock_legal_hold_status: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> PutObjectResult:
    """Put object.

    Args:
        bucket: Bucket.
        key: Key.
        acl: Acl.
        body: Body.
        cache_control: Cache control.
        content_disposition: Content disposition.
        content_encoding: Content encoding.
        content_language: Content language.
        content_length: Content length.
        content_md5: Content md5.
        content_type: Content type.
        checksum_algorithm: Checksum algorithm.
        checksum_crc32: Checksum crc32.
        checksum_crc32_c: Checksum crc32 c.
        checksum_crc64_nvme: Checksum crc64 nvme.
        checksum_sha1: Checksum sha1.
        checksum_sha256: Checksum sha256.
        expires: Expires.
        if_match: If match.
        if_none_match: If none match.
        grant_full_control: Grant full control.
        grant_read: Grant read.
        grant_read_acp: Grant read acp.
        grant_write_acp: Grant write acp.
        write_offset_bytes: Write offset bytes.
        metadata: Metadata.
        server_side_encryption: Server side encryption.
        storage_class: Storage class.
        website_redirect_location: Website redirect location.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        ssekms_key_id: Ssekms key id.
        ssekms_encryption_context: Ssekms encryption context.
        bucket_key_enabled: Bucket key enabled.
        request_payer: Request payer.
        tagging: Tagging.
        object_lock_mode: Object lock mode.
        object_lock_retain_until_date: Object lock retain until date.
        object_lock_legal_hold_status: Object lock legal hold status.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if acl is not None:
        kwargs["ACL"] = acl
    if body is not None:
        kwargs["Body"] = body
    if cache_control is not None:
        kwargs["CacheControl"] = cache_control
    if content_disposition is not None:
        kwargs["ContentDisposition"] = content_disposition
    if content_encoding is not None:
        kwargs["ContentEncoding"] = content_encoding
    if content_language is not None:
        kwargs["ContentLanguage"] = content_language
    if content_length is not None:
        kwargs["ContentLength"] = content_length
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if content_type is not None:
        kwargs["ContentType"] = content_type
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if checksum_crc32 is not None:
        kwargs["ChecksumCRC32"] = checksum_crc32
    if checksum_crc32_c is not None:
        kwargs["ChecksumCRC32C"] = checksum_crc32_c
    if checksum_crc64_nvme is not None:
        kwargs["ChecksumCRC64NVME"] = checksum_crc64_nvme
    if checksum_sha1 is not None:
        kwargs["ChecksumSHA1"] = checksum_sha1
    if checksum_sha256 is not None:
        kwargs["ChecksumSHA256"] = checksum_sha256
    if expires is not None:
        kwargs["Expires"] = expires
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    if if_none_match is not None:
        kwargs["IfNoneMatch"] = if_none_match
    if grant_full_control is not None:
        kwargs["GrantFullControl"] = grant_full_control
    if grant_read is not None:
        kwargs["GrantRead"] = grant_read
    if grant_read_acp is not None:
        kwargs["GrantReadACP"] = grant_read_acp
    if grant_write_acp is not None:
        kwargs["GrantWriteACP"] = grant_write_acp
    if write_offset_bytes is not None:
        kwargs["WriteOffsetBytes"] = write_offset_bytes
    if metadata is not None:
        kwargs["Metadata"] = metadata
    if server_side_encryption is not None:
        kwargs["ServerSideEncryption"] = server_side_encryption
    if storage_class is not None:
        kwargs["StorageClass"] = storage_class
    if website_redirect_location is not None:
        kwargs["WebsiteRedirectLocation"] = website_redirect_location
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if ssekms_key_id is not None:
        kwargs["SSEKMSKeyId"] = ssekms_key_id
    if ssekms_encryption_context is not None:
        kwargs["SSEKMSEncryptionContext"] = ssekms_encryption_context
    if bucket_key_enabled is not None:
        kwargs["BucketKeyEnabled"] = bucket_key_enabled
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if tagging is not None:
        kwargs["Tagging"] = tagging
    if object_lock_mode is not None:
        kwargs["ObjectLockMode"] = object_lock_mode
    if object_lock_retain_until_date is not None:
        kwargs["ObjectLockRetainUntilDate"] = object_lock_retain_until_date
    if object_lock_legal_hold_status is not None:
        kwargs["ObjectLockLegalHoldStatus"] = object_lock_legal_hold_status
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("PutObject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object") from exc
    return PutObjectResult(
        expiration=resp.get("Expiration"),
        e_tag=resp.get("ETag"),
        checksum_crc32=resp.get("ChecksumCRC32"),
        checksum_crc32_c=resp.get("ChecksumCRC32C"),
        checksum_crc64_nvme=resp.get("ChecksumCRC64NVME"),
        checksum_sha1=resp.get("ChecksumSHA1"),
        checksum_sha256=resp.get("ChecksumSHA256"),
        checksum_type=resp.get("ChecksumType"),
        server_side_encryption=resp.get("ServerSideEncryption"),
        version_id=resp.get("VersionId"),
        sse_customer_algorithm=resp.get("SSECustomerAlgorithm"),
        sse_customer_key_md5=resp.get("SSECustomerKeyMD5"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        ssekms_encryption_context=resp.get("SSEKMSEncryptionContext"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        size=resp.get("Size"),
        request_charged=resp.get("RequestCharged"),
    )


async def put_object_acl(
    bucket: str,
    key: str,
    *,
    acl: str | None = None,
    access_control_policy: dict[str, Any] | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    grant_full_control: str | None = None,
    grant_read: str | None = None,
    grant_read_acp: str | None = None,
    grant_write: str | None = None,
    grant_write_acp: str | None = None,
    request_payer: str | None = None,
    version_id: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> PutObjectAclResult:
    """Put object acl.

    Args:
        bucket: Bucket.
        key: Key.
        acl: Acl.
        access_control_policy: Access control policy.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        grant_full_control: Grant full control.
        grant_read: Grant read.
        grant_read_acp: Grant read acp.
        grant_write: Grant write.
        grant_write_acp: Grant write acp.
        request_payer: Request payer.
        version_id: Version id.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if acl is not None:
        kwargs["ACL"] = acl
    if access_control_policy is not None:
        kwargs["AccessControlPolicy"] = access_control_policy
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if grant_full_control is not None:
        kwargs["GrantFullControl"] = grant_full_control
    if grant_read is not None:
        kwargs["GrantRead"] = grant_read
    if grant_read_acp is not None:
        kwargs["GrantReadACP"] = grant_read_acp
    if grant_write is not None:
        kwargs["GrantWrite"] = grant_write
    if grant_write_acp is not None:
        kwargs["GrantWriteACP"] = grant_write_acp
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("PutObjectAcl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object acl") from exc
    return PutObjectAclResult(
        request_charged=resp.get("RequestCharged"),
    )


async def put_object_legal_hold(
    bucket: str,
    key: str,
    *,
    legal_hold: dict[str, Any] | None = None,
    request_payer: str | None = None,
    version_id: str | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> PutObjectLegalHoldResult:
    """Put object legal hold.

    Args:
        bucket: Bucket.
        key: Key.
        legal_hold: Legal hold.
        request_payer: Request payer.
        version_id: Version id.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if legal_hold is not None:
        kwargs["LegalHold"] = legal_hold
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("PutObjectLegalHold", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object legal hold") from exc
    return PutObjectLegalHoldResult(
        request_charged=resp.get("RequestCharged"),
    )


async def put_object_lock_configuration(
    bucket: str,
    *,
    object_lock_configuration: dict[str, Any] | None = None,
    request_payer: str | None = None,
    token: str | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> PutObjectLockConfigurationResult:
    """Put object lock configuration.

    Args:
        bucket: Bucket.
        object_lock_configuration: Object lock configuration.
        request_payer: Request payer.
        token: Token.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    if object_lock_configuration is not None:
        kwargs["ObjectLockConfiguration"] = object_lock_configuration
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if token is not None:
        kwargs["Token"] = token
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("PutObjectLockConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object lock configuration") from exc
    return PutObjectLockConfigurationResult(
        request_charged=resp.get("RequestCharged"),
    )


async def put_object_retention(
    bucket: str,
    key: str,
    *,
    retention: dict[str, Any] | None = None,
    request_payer: str | None = None,
    version_id: str | None = None,
    bypass_governance_retention: bool | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> PutObjectRetentionResult:
    """Put object retention.

    Args:
        bucket: Bucket.
        key: Key.
        retention: Retention.
        request_payer: Request payer.
        version_id: Version id.
        bypass_governance_retention: Bypass governance retention.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if retention is not None:
        kwargs["Retention"] = retention
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if bypass_governance_retention is not None:
        kwargs["BypassGovernanceRetention"] = bypass_governance_retention
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("PutObjectRetention", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object retention") from exc
    return PutObjectRetentionResult(
        request_charged=resp.get("RequestCharged"),
    )


async def put_object_tagging(
    bucket: str,
    key: str,
    tagging: dict[str, Any],
    *,
    version_id: str | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    request_payer: str | None = None,
    region_name: str | None = None,
) -> PutObjectTaggingResult:
    """Put object tagging.

    Args:
        bucket: Bucket.
        key: Key.
        tagging: Tagging.
        version_id: Version id.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        request_payer: Request payer.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["Tagging"] = tagging
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    try:
        resp = await client.call("PutObjectTagging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put object tagging") from exc
    return PutObjectTaggingResult(
        version_id=resp.get("VersionId"),
    )


async def put_public_access_block(
    bucket: str,
    public_access_block_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put public access block.

    Args:
        bucket: Bucket.
        public_access_block_configuration: Public access block configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["PublicAccessBlockConfiguration"] = public_access_block_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("PutPublicAccessBlock", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put public access block") from exc
    return None


async def rename_object(
    bucket: str,
    key: str,
    rename_source: str,
    *,
    destination_if_match: str | None = None,
    destination_if_none_match: str | None = None,
    destination_if_modified_since: str | None = None,
    destination_if_unmodified_since: str | None = None,
    source_if_match: str | None = None,
    source_if_none_match: str | None = None,
    source_if_modified_since: str | None = None,
    source_if_unmodified_since: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Rename object.

    Args:
        bucket: Bucket.
        key: Key.
        rename_source: Rename source.
        destination_if_match: Destination if match.
        destination_if_none_match: Destination if none match.
        destination_if_modified_since: Destination if modified since.
        destination_if_unmodified_since: Destination if unmodified since.
        source_if_match: Source if match.
        source_if_none_match: Source if none match.
        source_if_modified_since: Source if modified since.
        source_if_unmodified_since: Source if unmodified since.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["RenameSource"] = rename_source
    if destination_if_match is not None:
        kwargs["DestinationIfMatch"] = destination_if_match
    if destination_if_none_match is not None:
        kwargs["DestinationIfNoneMatch"] = destination_if_none_match
    if destination_if_modified_since is not None:
        kwargs["DestinationIfModifiedSince"] = destination_if_modified_since
    if destination_if_unmodified_since is not None:
        kwargs["DestinationIfUnmodifiedSince"] = destination_if_unmodified_since
    if source_if_match is not None:
        kwargs["SourceIfMatch"] = source_if_match
    if source_if_none_match is not None:
        kwargs["SourceIfNoneMatch"] = source_if_none_match
    if source_if_modified_since is not None:
        kwargs["SourceIfModifiedSince"] = source_if_modified_since
    if source_if_unmodified_since is not None:
        kwargs["SourceIfUnmodifiedSince"] = source_if_unmodified_since
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        await client.call("RenameObject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to rename object") from exc
    return None


async def restore_object(
    bucket: str,
    key: str,
    *,
    version_id: str | None = None,
    restore_request: dict[str, Any] | None = None,
    request_payer: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> RestoreObjectResult:
    """Restore object.

    Args:
        bucket: Bucket.
        key: Key.
        version_id: Version id.
        restore_request: Restore request.
        request_payer: Request payer.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if restore_request is not None:
        kwargs["RestoreRequest"] = restore_request
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("RestoreObject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore object") from exc
    return RestoreObjectResult(
        request_charged=resp.get("RequestCharged"),
        restore_output_path=resp.get("RestoreOutputPath"),
    )


async def select_object_content(
    bucket: str,
    key: str,
    expression: str,
    expression_type: str,
    input_serialization: dict[str, Any],
    output_serialization: dict[str, Any],
    *,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    request_progress: dict[str, Any] | None = None,
    scan_range: dict[str, Any] | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> SelectObjectContentResult:
    """Select object content.

    Args:
        bucket: Bucket.
        key: Key.
        expression: Expression.
        expression_type: Expression type.
        input_serialization: Input serialization.
        output_serialization: Output serialization.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        request_progress: Request progress.
        scan_range: Scan range.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["Expression"] = expression
    kwargs["ExpressionType"] = expression_type
    kwargs["InputSerialization"] = input_serialization
    kwargs["OutputSerialization"] = output_serialization
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if request_progress is not None:
        kwargs["RequestProgress"] = request_progress
    if scan_range is not None:
        kwargs["ScanRange"] = scan_range
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("SelectObjectContent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to select object content") from exc
    return SelectObjectContentResult(
        payload=resp.get("Payload"),
    )


async def update_bucket_metadata_inventory_table_configuration(
    bucket: str,
    inventory_table_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update bucket metadata inventory table configuration.

    Args:
        bucket: Bucket.
        inventory_table_configuration: Inventory table configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["InventoryTableConfiguration"] = inventory_table_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("UpdateBucketMetadataInventoryTableConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to update bucket metadata inventory table configuration"
        ) from exc
    return None


async def update_bucket_metadata_journal_table_configuration(
    bucket: str,
    journal_table_configuration: dict[str, Any],
    *,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update bucket metadata journal table configuration.

    Args:
        bucket: Bucket.
        journal_table_configuration: Journal table configuration.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["JournalTableConfiguration"] = journal_table_configuration
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        await client.call("UpdateBucketMetadataJournalTableConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to update bucket metadata journal table configuration"
        ) from exc
    return None


async def upload_part(
    bucket: str,
    key: str,
    part_number: int,
    upload_id: str,
    *,
    body: bytes | None = None,
    content_length: int | None = None,
    content_md5: str | None = None,
    checksum_algorithm: str | None = None,
    checksum_crc32: str | None = None,
    checksum_crc32_c: str | None = None,
    checksum_crc64_nvme: str | None = None,
    checksum_sha1: str | None = None,
    checksum_sha256: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> UploadPartResult:
    """Upload part.

    Args:
        bucket: Bucket.
        key: Key.
        part_number: Part number.
        upload_id: Upload id.
        body: Body.
        content_length: Content length.
        content_md5: Content md5.
        checksum_algorithm: Checksum algorithm.
        checksum_crc32: Checksum crc32.
        checksum_crc32_c: Checksum crc32 c.
        checksum_crc64_nvme: Checksum crc64 nvme.
        checksum_sha1: Checksum sha1.
        checksum_sha256: Checksum sha256.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["Key"] = key
    kwargs["PartNumber"] = part_number
    kwargs["UploadId"] = upload_id
    if body is not None:
        kwargs["Body"] = body
    if content_length is not None:
        kwargs["ContentLength"] = content_length
    if content_md5 is not None:
        kwargs["ContentMD5"] = content_md5
    if checksum_algorithm is not None:
        kwargs["ChecksumAlgorithm"] = checksum_algorithm
    if checksum_crc32 is not None:
        kwargs["ChecksumCRC32"] = checksum_crc32
    if checksum_crc32_c is not None:
        kwargs["ChecksumCRC32C"] = checksum_crc32_c
    if checksum_crc64_nvme is not None:
        kwargs["ChecksumCRC64NVME"] = checksum_crc64_nvme
    if checksum_sha1 is not None:
        kwargs["ChecksumSHA1"] = checksum_sha1
    if checksum_sha256 is not None:
        kwargs["ChecksumSHA256"] = checksum_sha256
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    try:
        resp = await client.call("UploadPart", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to upload part") from exc
    return UploadPartResult(
        server_side_encryption=resp.get("ServerSideEncryption"),
        e_tag=resp.get("ETag"),
        checksum_crc32=resp.get("ChecksumCRC32"),
        checksum_crc32_c=resp.get("ChecksumCRC32C"),
        checksum_crc64_nvme=resp.get("ChecksumCRC64NVME"),
        checksum_sha1=resp.get("ChecksumSHA1"),
        checksum_sha256=resp.get("ChecksumSHA256"),
        sse_customer_algorithm=resp.get("SSECustomerAlgorithm"),
        sse_customer_key_md5=resp.get("SSECustomerKeyMD5"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        request_charged=resp.get("RequestCharged"),
    )


async def upload_part_copy(
    bucket: str,
    copy_source: str,
    key: str,
    part_number: int,
    upload_id: str,
    *,
    copy_source_if_match: str | None = None,
    copy_source_if_modified_since: str | None = None,
    copy_source_if_none_match: str | None = None,
    copy_source_if_unmodified_since: str | None = None,
    copy_source_range: str | None = None,
    sse_customer_algorithm: str | None = None,
    sse_customer_key: str | None = None,
    sse_customer_key_md5: str | None = None,
    copy_source_sse_customer_algorithm: str | None = None,
    copy_source_sse_customer_key: str | None = None,
    copy_source_sse_customer_key_md5: str | None = None,
    request_payer: str | None = None,
    expected_bucket_owner: str | None = None,
    expected_source_bucket_owner: str | None = None,
    region_name: str | None = None,
) -> UploadPartCopyResult:
    """Upload part copy.

    Args:
        bucket: Bucket.
        copy_source: Copy source.
        key: Key.
        part_number: Part number.
        upload_id: Upload id.
        copy_source_if_match: Copy source if match.
        copy_source_if_modified_since: Copy source if modified since.
        copy_source_if_none_match: Copy source if none match.
        copy_source_if_unmodified_since: Copy source if unmodified since.
        copy_source_range: Copy source range.
        sse_customer_algorithm: Sse customer algorithm.
        sse_customer_key: Sse customer key.
        sse_customer_key_md5: Sse customer key md5.
        copy_source_sse_customer_algorithm: Copy source sse customer algorithm.
        copy_source_sse_customer_key: Copy source sse customer key.
        copy_source_sse_customer_key_md5: Copy source sse customer key md5.
        request_payer: Request payer.
        expected_bucket_owner: Expected bucket owner.
        expected_source_bucket_owner: Expected source bucket owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Bucket"] = bucket
    kwargs["CopySource"] = copy_source
    kwargs["Key"] = key
    kwargs["PartNumber"] = part_number
    kwargs["UploadId"] = upload_id
    if copy_source_if_match is not None:
        kwargs["CopySourceIfMatch"] = copy_source_if_match
    if copy_source_if_modified_since is not None:
        kwargs["CopySourceIfModifiedSince"] = copy_source_if_modified_since
    if copy_source_if_none_match is not None:
        kwargs["CopySourceIfNoneMatch"] = copy_source_if_none_match
    if copy_source_if_unmodified_since is not None:
        kwargs["CopySourceIfUnmodifiedSince"] = copy_source_if_unmodified_since
    if copy_source_range is not None:
        kwargs["CopySourceRange"] = copy_source_range
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if sse_customer_key is not None:
        kwargs["SSECustomerKey"] = sse_customer_key
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if copy_source_sse_customer_algorithm is not None:
        kwargs["CopySourceSSECustomerAlgorithm"] = copy_source_sse_customer_algorithm
    if copy_source_sse_customer_key is not None:
        kwargs["CopySourceSSECustomerKey"] = copy_source_sse_customer_key
    if copy_source_sse_customer_key_md5 is not None:
        kwargs["CopySourceSSECustomerKeyMD5"] = copy_source_sse_customer_key_md5
    if request_payer is not None:
        kwargs["RequestPayer"] = request_payer
    if expected_bucket_owner is not None:
        kwargs["ExpectedBucketOwner"] = expected_bucket_owner
    if expected_source_bucket_owner is not None:
        kwargs["ExpectedSourceBucketOwner"] = expected_source_bucket_owner
    try:
        resp = await client.call("UploadPartCopy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to upload part copy") from exc
    return UploadPartCopyResult(
        copy_source_version_id=resp.get("CopySourceVersionId"),
        copy_part_result=resp.get("CopyPartResult"),
        server_side_encryption=resp.get("ServerSideEncryption"),
        sse_customer_algorithm=resp.get("SSECustomerAlgorithm"),
        sse_customer_key_md5=resp.get("SSECustomerKeyMD5"),
        ssekms_key_id=resp.get("SSEKMSKeyId"),
        bucket_key_enabled=resp.get("BucketKeyEnabled"),
        request_charged=resp.get("RequestCharged"),
    )


async def write_get_object_response(
    request_route: str,
    request_token: str,
    *,
    body: bytes | None = None,
    status_code: int | None = None,
    error_code: str | None = None,
    error_message: str | None = None,
    accept_ranges: str | None = None,
    cache_control: str | None = None,
    content_disposition: str | None = None,
    content_encoding: str | None = None,
    content_language: str | None = None,
    content_length: int | None = None,
    content_range: str | None = None,
    content_type: str | None = None,
    checksum_crc32: str | None = None,
    checksum_crc32_c: str | None = None,
    checksum_crc64_nvme: str | None = None,
    checksum_sha1: str | None = None,
    checksum_sha256: str | None = None,
    delete_marker: bool | None = None,
    e_tag: str | None = None,
    expires: str | None = None,
    expiration: str | None = None,
    last_modified: str | None = None,
    missing_meta: int | None = None,
    metadata: dict[str, Any] | None = None,
    object_lock_mode: str | None = None,
    object_lock_legal_hold_status: str | None = None,
    object_lock_retain_until_date: str | None = None,
    parts_count: int | None = None,
    replication_status: str | None = None,
    request_charged: str | None = None,
    restore: str | None = None,
    server_side_encryption: str | None = None,
    sse_customer_algorithm: str | None = None,
    ssekms_key_id: str | None = None,
    sse_customer_key_md5: str | None = None,
    storage_class: str | None = None,
    tag_count: int | None = None,
    version_id: str | None = None,
    bucket_key_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Write get object response.

    Args:
        request_route: Request route.
        request_token: Request token.
        body: Body.
        status_code: Status code.
        error_code: Error code.
        error_message: Error message.
        accept_ranges: Accept ranges.
        cache_control: Cache control.
        content_disposition: Content disposition.
        content_encoding: Content encoding.
        content_language: Content language.
        content_length: Content length.
        content_range: Content range.
        content_type: Content type.
        checksum_crc32: Checksum crc32.
        checksum_crc32_c: Checksum crc32 c.
        checksum_crc64_nvme: Checksum crc64 nvme.
        checksum_sha1: Checksum sha1.
        checksum_sha256: Checksum sha256.
        delete_marker: Delete marker.
        e_tag: E tag.
        expires: Expires.
        expiration: Expiration.
        last_modified: Last modified.
        missing_meta: Missing meta.
        metadata: Metadata.
        object_lock_mode: Object lock mode.
        object_lock_legal_hold_status: Object lock legal hold status.
        object_lock_retain_until_date: Object lock retain until date.
        parts_count: Parts count.
        replication_status: Replication status.
        request_charged: Request charged.
        restore: Restore.
        server_side_encryption: Server side encryption.
        sse_customer_algorithm: Sse customer algorithm.
        ssekms_key_id: Ssekms key id.
        sse_customer_key_md5: Sse customer key md5.
        storage_class: Storage class.
        tag_count: Tag count.
        version_id: Version id.
        bucket_key_enabled: Bucket key enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("s3", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RequestRoute"] = request_route
    kwargs["RequestToken"] = request_token
    if body is not None:
        kwargs["Body"] = body
    if status_code is not None:
        kwargs["StatusCode"] = status_code
    if error_code is not None:
        kwargs["ErrorCode"] = error_code
    if error_message is not None:
        kwargs["ErrorMessage"] = error_message
    if accept_ranges is not None:
        kwargs["AcceptRanges"] = accept_ranges
    if cache_control is not None:
        kwargs["CacheControl"] = cache_control
    if content_disposition is not None:
        kwargs["ContentDisposition"] = content_disposition
    if content_encoding is not None:
        kwargs["ContentEncoding"] = content_encoding
    if content_language is not None:
        kwargs["ContentLanguage"] = content_language
    if content_length is not None:
        kwargs["ContentLength"] = content_length
    if content_range is not None:
        kwargs["ContentRange"] = content_range
    if content_type is not None:
        kwargs["ContentType"] = content_type
    if checksum_crc32 is not None:
        kwargs["ChecksumCRC32"] = checksum_crc32
    if checksum_crc32_c is not None:
        kwargs["ChecksumCRC32C"] = checksum_crc32_c
    if checksum_crc64_nvme is not None:
        kwargs["ChecksumCRC64NVME"] = checksum_crc64_nvme
    if checksum_sha1 is not None:
        kwargs["ChecksumSHA1"] = checksum_sha1
    if checksum_sha256 is not None:
        kwargs["ChecksumSHA256"] = checksum_sha256
    if delete_marker is not None:
        kwargs["DeleteMarker"] = delete_marker
    if e_tag is not None:
        kwargs["ETag"] = e_tag
    if expires is not None:
        kwargs["Expires"] = expires
    if expiration is not None:
        kwargs["Expiration"] = expiration
    if last_modified is not None:
        kwargs["LastModified"] = last_modified
    if missing_meta is not None:
        kwargs["MissingMeta"] = missing_meta
    if metadata is not None:
        kwargs["Metadata"] = metadata
    if object_lock_mode is not None:
        kwargs["ObjectLockMode"] = object_lock_mode
    if object_lock_legal_hold_status is not None:
        kwargs["ObjectLockLegalHoldStatus"] = object_lock_legal_hold_status
    if object_lock_retain_until_date is not None:
        kwargs["ObjectLockRetainUntilDate"] = object_lock_retain_until_date
    if parts_count is not None:
        kwargs["PartsCount"] = parts_count
    if replication_status is not None:
        kwargs["ReplicationStatus"] = replication_status
    if request_charged is not None:
        kwargs["RequestCharged"] = request_charged
    if restore is not None:
        kwargs["Restore"] = restore
    if server_side_encryption is not None:
        kwargs["ServerSideEncryption"] = server_side_encryption
    if sse_customer_algorithm is not None:
        kwargs["SSECustomerAlgorithm"] = sse_customer_algorithm
    if ssekms_key_id is not None:
        kwargs["SSEKMSKeyId"] = ssekms_key_id
    if sse_customer_key_md5 is not None:
        kwargs["SSECustomerKeyMD5"] = sse_customer_key_md5
    if storage_class is not None:
        kwargs["StorageClass"] = storage_class
    if tag_count is not None:
        kwargs["TagCount"] = tag_count
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if bucket_key_enabled is not None:
        kwargs["BucketKeyEnabled"] = bucket_key_enabled
    try:
        await client.call("WriteGetObjectResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to write get object response") from exc
    return None
