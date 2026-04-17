"""Tests for aws_util.aio.s3 -- 100 % line coverage."""
from __future__ import annotations

import io
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.s3 import (
    PresignedUrl,
    S3Object,
    S3ObjectVersion,
    batch_copy,
    copy_object,
    delete_object,
    delete_prefix,
    download_as_text,
    download_bytes,
    download_file,
    generate_presigned_post,
    get_object,
    get_object_metadata,
    list_object_versions,
    list_objects,
    move_object,
    multipart_upload,
    object_exists,
    presigned_url,
    read_json,
    read_jsonl,
    sync_folder,
    upload_bytes,
    upload_file,
    upload_fileobj,
    write_json,
    abort_multipart_upload,
    complete_multipart_upload,
    create_bucket,
    create_bucket_metadata_configuration,
    create_bucket_metadata_table_configuration,
    create_multipart_upload,
    create_session,
    delete_bucket,
    delete_bucket_analytics_configuration,
    delete_bucket_cors,
    delete_bucket_encryption,
    delete_bucket_intelligent_tiering_configuration,
    delete_bucket_inventory_configuration,
    delete_bucket_lifecycle,
    delete_bucket_metadata_configuration,
    delete_bucket_metadata_table_configuration,
    delete_bucket_metrics_configuration,
    delete_bucket_ownership_controls,
    delete_bucket_policy,
    delete_bucket_replication,
    delete_bucket_tagging,
    delete_bucket_website,
    delete_object_tagging,
    delete_objects,
    delete_public_access_block,
    get_bucket_accelerate_configuration,
    get_bucket_acl,
    get_bucket_analytics_configuration,
    get_bucket_cors,
    get_bucket_encryption,
    get_bucket_intelligent_tiering_configuration,
    get_bucket_inventory_configuration,
    get_bucket_lifecycle,
    get_bucket_lifecycle_configuration,
    get_bucket_location,
    get_bucket_logging,
    get_bucket_metadata_configuration,
    get_bucket_metadata_table_configuration,
    get_bucket_metrics_configuration,
    get_bucket_notification,
    get_bucket_notification_configuration,
    get_bucket_ownership_controls,
    get_bucket_policy,
    get_bucket_policy_status,
    get_bucket_replication,
    get_bucket_request_payment,
    get_bucket_tagging,
    get_bucket_versioning,
    get_bucket_website,
    get_object_acl,
    get_object_attributes,
    get_object_legal_hold,
    get_object_lock_configuration,
    get_object_retention,
    get_object_tagging,
    get_object_torrent,
    get_public_access_block,
    head_bucket,
    head_object,
    list_bucket_analytics_configurations,
    list_bucket_intelligent_tiering_configurations,
    list_bucket_inventory_configurations,
    list_bucket_metrics_configurations,
    list_buckets,
    list_directory_buckets,
    list_multipart_uploads,
    list_objects_v2,
    list_parts,
    put_bucket_accelerate_configuration,
    put_bucket_acl,
    put_bucket_analytics_configuration,
    put_bucket_cors,
    put_bucket_encryption,
    put_bucket_intelligent_tiering_configuration,
    put_bucket_inventory_configuration,
    put_bucket_lifecycle,
    put_bucket_lifecycle_configuration,
    put_bucket_logging,
    put_bucket_metrics_configuration,
    put_bucket_notification,
    put_bucket_notification_configuration,
    put_bucket_ownership_controls,
    put_bucket_policy,
    put_bucket_replication,
    put_bucket_request_payment,
    put_bucket_tagging,
    put_bucket_versioning,
    put_bucket_website,
    put_object,
    put_object_acl,
    put_object_legal_hold,
    put_object_lock_configuration,
    put_object_retention,
    put_object_tagging,
    put_public_access_block,
    rename_object,
    restore_object,
    select_object_content,
    update_bucket_metadata_inventory_table_configuration,
    update_bucket_metadata_journal_table_configuration,
    upload_part,
    upload_part_copy,
    write_get_object_response,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    c.paginate = AsyncMock(return_value=[])
    return c


# ---------------------------------------------------------------------------
# upload_file
# ---------------------------------------------------------------------------


async def test_upload_file_ok(monkeypatch, tmp_path):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    f = tmp_path / "file.txt"
    f.write_bytes(b"data")
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"data"),
    )
    await upload_file("bucket", "key", str(f))
    mc.call.assert_awaited_once()
    kw = mc.call.call_args
    assert kw[1]["Bucket"] == "bucket"


async def test_upload_file_with_content_type(monkeypatch, tmp_path):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"data"),
    )
    await upload_file("bucket", "key", "f.json", content_type="application/json")
    kw = mc.call.call_args[1]
    assert kw["ContentType"] == "application/json"


async def test_upload_file_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"data"),
    )
    with pytest.raises(RuntimeError, match="Failed to upload"):
        await upload_file("bucket", "key", "f.txt")


# ---------------------------------------------------------------------------
# upload_bytes
# ---------------------------------------------------------------------------


async def test_upload_bytes_raw(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    await upload_bytes("bucket", "key", b"raw")
    mc.call.assert_awaited_once()


async def test_upload_bytes_filelike(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    buf = io.BytesIO(b"data")
    await upload_bytes("bucket", "key", buf, content_type="text/plain")
    kw = mc.call.call_args[1]
    assert kw["ContentType"] == "text/plain"


async def test_upload_bytes_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to upload bytes"):
        await upload_bytes("bucket", "key", b"data")


# ---------------------------------------------------------------------------
# download_file
# ---------------------------------------------------------------------------


async def test_download_file_bytes_body(monkeypatch, tmp_path):
    mc = _mc({"Body": b"content"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    dest = tmp_path / "out.txt"
    to_thread_calls = []

    async def fake_to_thread(fn, *args):
        to_thread_calls.append((fn, args))
        if callable(fn) and args:
            return fn(*args)
        return fn() if callable(fn) else fn

    monkeypatch.setattr("aws_util.aio.s3.asyncio.to_thread", fake_to_thread)
    await download_file("bucket", "key", str(dest))
    assert dest.read_bytes() == b"content"


async def test_download_file_stream_body(monkeypatch, tmp_path):
    body_mock = MagicMock()
    body_mock.read.return_value = b"streamed"
    mc = _mc({"Body": body_mock})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    dest = tmp_path / "out.txt"

    call_log = []

    async def fake_to_thread(fn, *args):
        call_log.append(fn)
        if callable(fn) and args:
            return fn(*args)
        return fn() if callable(fn) else fn

    monkeypatch.setattr("aws_util.aio.s3.asyncio.to_thread", fake_to_thread)
    await download_file("bucket", "key", str(dest))
    assert dest.read_bytes() == b"streamed"


async def test_download_file_error(monkeypatch, tmp_path):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to download"):
        await download_file("bucket", "key", str(tmp_path / "out.txt"))


# ---------------------------------------------------------------------------
# download_bytes
# ---------------------------------------------------------------------------


async def test_download_bytes_bytes_body(monkeypatch):
    mc = _mc({"Body": b"raw"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await download_bytes("bucket", "key")
    assert result == b"raw"


async def test_download_bytes_stream_body(monkeypatch):
    body_mock = MagicMock()
    body_mock.read.return_value = b"streamed"
    mc = _mc({"Body": body_mock})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"streamed"),
    )
    result = await download_bytes("bucket", "key")
    assert result == b"streamed"


async def test_download_bytes_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to download"):
        await download_bytes("bucket", "key")


# ---------------------------------------------------------------------------
# list_objects
# ---------------------------------------------------------------------------


async def test_list_objects_ok(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(
        return_value=[
            {"Key": "a.txt", "Size": 10, "LastModified": "2024-01-01", "ETag": '"abc"'},
            {"Key": "b.txt"},
        ]
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await list_objects("bucket", prefix="pre/")
    assert len(result) == 2
    assert isinstance(result[0], S3Object)
    assert result[0].key == "a.txt"
    assert result[0].etag == "abc"
    assert result[1].etag is None


async def test_list_objects_empty_etag(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(return_value=[{"Key": "c.txt", "ETag": ""}])
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await list_objects("bucket")
    assert result[0].etag is None


async def test_list_objects_error(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to list"):
        await list_objects("bucket")


# ---------------------------------------------------------------------------
# object_exists
# ---------------------------------------------------------------------------


async def test_object_exists_true(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    assert await object_exists("bucket", "key") is True


async def test_object_exists_404(monkeypatch):
    mc = _mc(se=RuntimeError("404 Not Found"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    assert await object_exists("bucket", "key") is False


async def test_object_exists_nosuchkey(monkeypatch):
    mc = _mc(se=RuntimeError("NoSuchKey"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    assert await object_exists("bucket", "key") is False


async def test_object_exists_not_found(monkeypatch):
    mc = _mc(se=RuntimeError("Not Found"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    assert await object_exists("bucket", "key") is False


async def test_object_exists_other_error(monkeypatch):
    mc = _mc(se=RuntimeError("permission denied"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to check existence"):
        await object_exists("bucket", "key")


# ---------------------------------------------------------------------------
# delete_object
# ---------------------------------------------------------------------------


async def test_delete_object_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    await delete_object("bucket", "key")
    mc.call.assert_awaited_once()


async def test_delete_object_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to delete"):
        await delete_object("bucket", "key")


# ---------------------------------------------------------------------------
# copy_object
# ---------------------------------------------------------------------------


async def test_copy_object_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    await copy_object("src-bk", "src-k", "dst-bk", "dst-k")
    mc.call.assert_awaited_once()


async def test_copy_object_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to copy"):
        await copy_object("src", "sk", "dst", "dk")


# ---------------------------------------------------------------------------
# presigned_url
# ---------------------------------------------------------------------------


async def test_presigned_url_ok(monkeypatch):
    fake_client = MagicMock()
    fake_client.generate_presigned_url.return_value = "https://example.com/signed"
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value="https://example.com/signed"),
    )
    result = await presigned_url("bucket", "key", expires_in=900)
    assert isinstance(result, PresignedUrl)
    assert result.url == "https://example.com/signed"
    assert result.expires_in == 900


async def test_presigned_url_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(side_effect=Exception("sig fail")),
    )
    with pytest.raises(RuntimeError, match="Failed to generate pre-signed URL"):
        await presigned_url("bucket", "key")


# ---------------------------------------------------------------------------
# read_json
# ---------------------------------------------------------------------------


async def test_read_json_ok(monkeypatch):
    mc = _mc({"Body": json.dumps({"x": 1}).encode()})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await read_json("bucket", "data.json")
    assert result == {"x": 1}


async def test_read_json_invalid(monkeypatch):
    mc = _mc({"Body": b"not json"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(ValueError, match="not valid JSON"):
        await read_json("bucket", "data.json")


# ---------------------------------------------------------------------------
# write_json
# ---------------------------------------------------------------------------


async def test_write_json_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    await write_json("bucket", "data.json", {"x": 1}, indent=2)
    mc.call.assert_awaited_once()
    kw = mc.call.call_args[1]
    assert kw["ContentType"] == "application/json"


# ---------------------------------------------------------------------------
# read_jsonl
# ---------------------------------------------------------------------------


async def test_read_jsonl_ok(monkeypatch):
    payload = b'{"a":1}\n\n{"b":2}\n'
    mc = _mc({"Body": payload})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    items = [item async for item in read_jsonl("bucket", "data.jsonl")]
    assert items == [{"a": 1}, {"b": 2}]


async def test_read_jsonl_invalid_line(monkeypatch):
    payload = b'{"a":1}\nnot_json\n'
    mc = _mc({"Body": payload})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(ValueError, match="line 2 is not valid JSON"):
        async for _ in read_jsonl("bucket", "data.jsonl"):
            pass


# ---------------------------------------------------------------------------
# sync_folder
# ---------------------------------------------------------------------------


async def test_sync_folder_not_a_dir(monkeypatch):
    with pytest.raises(ValueError, match="is not a directory"):
        await sync_folder("/nonexistent/path", "bucket")


async def test_sync_folder_upload_and_skip(monkeypatch, tmp_path):
    """Upload new/changed files, skip unchanged ones."""
    import hashlib

    # Setup local dir
    (tmp_path / "new.txt").write_bytes(b"new")
    (tmp_path / "same.txt").write_bytes(b"same")

    same_md5 = hashlib.md5(b"same").hexdigest()

    # Mock list_objects to return the unchanged file
    mc = _mc()
    mc.paginate = AsyncMock(
        return_value=[{"Key": "same.txt", "ETag": f'"{same_md5}"'}]
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)

    # list_objects is called via client.paginate -> returns S3Objects with etag == same_md5
    # We need to mock list_objects at a higher level since sync_folder calls it
    from aws_util.aio import s3 as s3_mod

    async def fake_list_objects(bucket, prefix="", region_name=None):
        return [S3Object(bucket=bucket, key="same.txt", etag=same_md5)]

    monkeypatch.setattr(s3_mod, "list_objects", fake_list_objects)

    # Mock upload_file
    uploaded = []

    async def fake_upload_file(bucket, key, fp, region_name=None):
        uploaded.append(key)

    monkeypatch.setattr(s3_mod, "upload_file", fake_upload_file)

    # Mock asyncio.to_thread to read file bytes
    async def fake_to_thread(fn, *args):
        if callable(fn) and not args:
            return fn()
        return fn(*args) if args else fn

    monkeypatch.setattr("aws_util.aio.s3.asyncio.to_thread", fake_to_thread)

    result = await sync_folder(tmp_path, "bucket")
    assert result["uploaded"] == 1
    assert result["skipped"] == 1
    assert result["deleted"] == 0
    assert "new.txt" in uploaded


async def test_sync_folder_delete_removed(monkeypatch, tmp_path):
    """Delete S3 objects that no longer exist locally."""
    (tmp_path / "keep.txt").write_bytes(b"keep")

    from aws_util.aio import s3 as s3_mod

    # Keys in S3 include the prefix; "pre/keep.txt" maps to local "keep.txt"
    async def fake_list_objects(bucket, prefix="", region_name=None):
        return [
            S3Object(bucket=bucket, key="pre/keep.txt", etag="no-match"),
            S3Object(bucket=bucket, key="pre/gone.txt", etag="xyz"),
        ]

    monkeypatch.setattr(s3_mod, "list_objects", fake_list_objects)

    uploaded_keys = []

    async def fake_upload_file(bucket, key, fp, region_name=None):
        uploaded_keys.append(key)

    monkeypatch.setattr(s3_mod, "upload_file", fake_upload_file)

    deleted_keys = []

    async def fake_delete_object(bucket, key, region_name=None):
        deleted_keys.append(key)

    monkeypatch.setattr(s3_mod, "delete_object", fake_delete_object)

    async def fake_to_thread(fn, *args):
        if callable(fn) and not args:
            return fn()
        return fn(*args) if args else fn

    monkeypatch.setattr("aws_util.aio.s3.asyncio.to_thread", fake_to_thread)

    result = await sync_folder(tmp_path, "bucket", prefix="pre/", delete_removed=True)
    assert result["deleted"] == 1
    assert "pre/gone.txt" in deleted_keys


async def test_sync_folder_subdir_files(monkeypatch, tmp_path):
    """Verify subdirectory files are included."""
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.txt").write_bytes(b"nested")

    from aws_util.aio import s3 as s3_mod

    async def fake_list_objects(bucket, prefix="", region_name=None):
        return []

    monkeypatch.setattr(s3_mod, "list_objects", fake_list_objects)

    uploaded_keys = []

    async def fake_upload_file(bucket, key, fp, region_name=None):
        uploaded_keys.append(key)

    monkeypatch.setattr(s3_mod, "upload_file", fake_upload_file)

    async def fake_to_thread(fn, *args):
        if callable(fn) and not args:
            return fn()
        return fn(*args) if args else fn

    monkeypatch.setattr("aws_util.aio.s3.asyncio.to_thread", fake_to_thread)

    result = await sync_folder(tmp_path, "bucket")
    assert result["uploaded"] == 1
    assert "sub/nested.txt" in uploaded_keys


async def test_sync_folder_no_upload_tasks(monkeypatch, tmp_path):
    """Empty directory results in no uploads."""
    from aws_util.aio import s3 as s3_mod

    async def fake_list_objects(bucket, prefix="", region_name=None):
        return []

    monkeypatch.setattr(s3_mod, "list_objects", fake_list_objects)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b""),
    )
    result = await sync_folder(tmp_path, "bucket")
    assert result == {"uploaded": 0, "skipped": 0, "deleted": 0}


# ---------------------------------------------------------------------------
# multipart_upload
# ---------------------------------------------------------------------------


async def test_multipart_upload_ok(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(
        side_effect=[
            {"UploadId": "uid123"},  # CreateMultipartUpload
            {"ETag": '"e1"'},  # UploadPart 1
            {"ETag": '"e2"'},  # UploadPart 2
            {},  # CompleteMultipartUpload
        ]
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"x" * (5 * 1024 * 1024 + 100)),
    )
    await multipart_upload("bucket", "key", "file.bin", part_size_mb=5)
    assert mc.call.await_count == 4


async def test_multipart_upload_small_part_error(monkeypatch):
    with pytest.raises(ValueError, match="part_size_mb must be at least 5"):
        await multipart_upload("bucket", "key", "file.bin", part_size_mb=2)


async def test_multipart_upload_abort_on_failure(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(
        side_effect=[
            {"UploadId": "uid123"},  # CreateMultipartUpload
            RuntimeError("part fail"),  # UploadPart fails
            {},  # AbortMultipartUpload
        ]
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=b"x" * (6 * 1024 * 1024)),
    )
    with pytest.raises(RuntimeError, match="Multipart upload failed"):
        await multipart_upload("bucket", "key", "file.bin", part_size_mb=5)


# ---------------------------------------------------------------------------
# delete_prefix
# ---------------------------------------------------------------------------


async def test_delete_prefix_empty(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(return_value=[])
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    count = await delete_prefix("bucket", "logs/")
    assert count == 0


async def test_delete_prefix_ok(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(
        return_value=[{"Key": "logs/a.txt"}, {"Key": "logs/b.txt"}]
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    count = await delete_prefix("bucket", "logs/")
    assert count == 2
    mc.call.assert_awaited_once()


async def test_delete_prefix_paginate_error(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_prefix failed"):
        await delete_prefix("bucket", "logs/")


async def test_delete_prefix_delete_error(monkeypatch):
    mc = _mc()
    mc.paginate = AsyncMock(return_value=[{"Key": "k1"}])
    mc.call = AsyncMock(side_effect=RuntimeError("del fail"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_prefix failed"):
        await delete_prefix("bucket", "logs/")


# ---------------------------------------------------------------------------
# move_object
# ---------------------------------------------------------------------------


async def test_move_object_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    await move_object("src-bk", "src-k", "dst-bk", "dst-k")
    assert mc.call.await_count == 2


# ---------------------------------------------------------------------------
# get_object_metadata
# ---------------------------------------------------------------------------


async def test_get_object_metadata_ok(monkeypatch):
    mc = _mc(
        {
            "ContentType": "text/plain",
            "ContentLength": 42,
            "LastModified": "2024-01-01",
            "ETag": '"abc123"',
            "Metadata": {"custom": "val"},
        }
    )
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await get_object_metadata("bucket", "key")
    assert result["content_type"] == "text/plain"
    assert result["content_length"] == 42
    assert result["etag"] == "abc123"
    assert result["metadata"] == {"custom": "val"}


async def test_get_object_metadata_empty_etag(monkeypatch):
    mc = _mc({"ETag": "", "Metadata": {}})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await get_object_metadata("bucket", "key")
    assert result["etag"] is None


async def test_get_object_metadata_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to get metadata"):
        await get_object_metadata("bucket", "key")


# ---------------------------------------------------------------------------
# batch_copy
# ---------------------------------------------------------------------------


async def test_batch_copy_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    copies = [
        {"src_bucket": "a", "src_key": "k1", "dst_bucket": "b", "dst_key": "k2"},
    ]
    await batch_copy(copies)


async def test_batch_copy_with_error(monkeypatch):
    mc = _mc(se=RuntimeError("copy fail"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    copies = [
        {"src_bucket": "a", "src_key": "k1", "dst_bucket": "b", "dst_key": "k2"},
    ]
    with pytest.raises(RuntimeError, match="batch_copy had 1 failure"):
        await batch_copy(copies)


# ---------------------------------------------------------------------------
# download_as_text
# ---------------------------------------------------------------------------


async def test_download_as_text_ok(monkeypatch):
    mc = _mc({"Body": "hello world".encode("utf-8")})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await download_as_text("bucket", "key")
    assert result == "hello world"


# ---------------------------------------------------------------------------
# generate_presigned_post
# ---------------------------------------------------------------------------


async def test_generate_presigned_post_ok(monkeypatch):
    expected = {"url": "https://s3.example.com/", "fields": {"key": "val"}}
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=expected),
    )
    result = await generate_presigned_post("bucket", "key", max_size_mb=5)
    assert result == expected


async def test_generate_presigned_post_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(side_effect=Exception("fail")),
    )
    with pytest.raises(RuntimeError, match="Failed to generate presigned POST"):
        await generate_presigned_post("bucket", "key")


# ---------------------------------------------------------------------------
# download_bytes — with version_id
# ---------------------------------------------------------------------------


async def test_download_bytes_with_version_id(monkeypatch):
    mc = _mc({"Body": b"versioned"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await download_bytes("bucket", "key", version_id="v1")
    assert result == b"versioned"
    kw = mc.call.call_args[1]
    assert kw["VersionId"] == "v1"


# ---------------------------------------------------------------------------
# get_object
# ---------------------------------------------------------------------------


async def test_get_object_ok(monkeypatch):
    mc = _mc({"Body": b"body", "ContentType": "text/plain"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await get_object("bucket", "key")
    assert isinstance(result, dict)
    assert result["Body"] == b"body"
    assert result["ContentType"] == "text/plain"


async def test_get_object_with_version_id(monkeypatch):
    mc = _mc({"Body": b"v2-body"})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    result = await get_object("bucket", "key", version_id="v2")
    assert result["Body"] == b"v2-body"
    kw = mc.call.call_args[1]
    assert kw["VersionId"] == "v2"


async def test_get_object_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to get"):
        await get_object("bucket", "key")


# ---------------------------------------------------------------------------
# list_object_versions
# ---------------------------------------------------------------------------


async def test_list_object_versions_ok(monkeypatch):
    versions = [
        S3ObjectVersion(
            bucket="bucket",
            key="file.txt",
            version_id="v1",
            is_latest=True,
        ),
    ]
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=versions),
    )
    result = await list_object_versions("bucket", prefix="pre/")
    assert len(result) == 1
    assert isinstance(result[0], S3ObjectVersion)
    assert result[0].version_id == "v1"


async def test_list_object_versions_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_object_versions("bucket")


# ---------------------------------------------------------------------------
# upload_fileobj
# ---------------------------------------------------------------------------


async def test_upload_fileobj_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    buf = io.BytesIO(b"file data")
    await upload_fileobj("bucket", "key", buf, content_type="application/pdf")


async def test_upload_fileobj_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.s3.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("upload fail")),
    )
    buf = io.BytesIO(b"data")
    with pytest.raises(RuntimeError, match="upload fail"):
        await upload_fileobj("bucket", "key", buf)


# ---------------------------------------------------------------------------
# S3ObjectVersion re-export
# ---------------------------------------------------------------------------


def test_s3_object_version_reexport():
    from aws_util.s3 import S3ObjectVersion as Original

    assert S3ObjectVersion is Original


async def test_abort_multipart_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await abort_multipart_upload("test-bucket", "test-key", "test-upload_id", )
    mock_client.call.assert_called_once()


async def test_abort_multipart_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await abort_multipart_upload("test-bucket", "test-key", "test-upload_id", )


async def test_complete_multipart_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await complete_multipart_upload("test-bucket", "test-key", "test-upload_id", )
    mock_client.call.assert_called_once()


async def test_complete_multipart_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await complete_multipart_upload("test-bucket", "test-key", "test-upload_id", )


async def test_create_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bucket("test-bucket", )
    mock_client.call.assert_called_once()


async def test_create_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bucket("test-bucket", )


async def test_create_bucket_metadata_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bucket_metadata_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_create_bucket_metadata_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bucket_metadata_configuration("test-bucket", {}, )


async def test_create_bucket_metadata_table_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bucket_metadata_table_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_create_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bucket_metadata_table_configuration("test-bucket", {}, )


async def test_create_multipart_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_multipart_upload("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_create_multipart_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_multipart_upload("test-bucket", "test-key", )


async def test_create_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_session("test-bucket", )
    mock_client.call.assert_called_once()


async def test_create_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_session("test-bucket", )


async def test_delete_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket("test-bucket", )


async def test_delete_bucket_analytics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_analytics_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_analytics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_analytics_configuration("test-bucket", "test-id", )


async def test_delete_bucket_cors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_cors("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_cors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_cors("test-bucket", )


async def test_delete_bucket_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_encryption("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_encryption("test-bucket", )


async def test_delete_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", )


async def test_delete_bucket_inventory_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_inventory_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_inventory_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_inventory_configuration("test-bucket", "test-id", )


async def test_delete_bucket_lifecycle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_lifecycle("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_lifecycle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_lifecycle("test-bucket", )


async def test_delete_bucket_metadata_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_metadata_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_metadata_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_metadata_configuration("test-bucket", )


async def test_delete_bucket_metadata_table_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_metadata_table_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_metadata_table_configuration("test-bucket", )


async def test_delete_bucket_metrics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_metrics_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_metrics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_metrics_configuration("test-bucket", "test-id", )


async def test_delete_bucket_ownership_controls(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_ownership_controls("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_ownership_controls_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_ownership_controls("test-bucket", )


async def test_delete_bucket_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_policy("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_policy("test-bucket", )


async def test_delete_bucket_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_replication("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_replication("test-bucket", )


async def test_delete_bucket_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_tagging("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_tagging("test-bucket", )


async def test_delete_bucket_website(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_website("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_website_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_website("test-bucket", )


async def test_delete_object_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_object_tagging("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_delete_object_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_object_tagging("test-bucket", "test-key", )


async def test_delete_objects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_objects("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_delete_objects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_objects("test-bucket", {}, )


async def test_delete_public_access_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_public_access_block("test-bucket", )
    mock_client.call.assert_called_once()


async def test_delete_public_access_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_public_access_block("test-bucket", )


async def test_get_bucket_accelerate_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_accelerate_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_accelerate_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_accelerate_configuration("test-bucket", )


async def test_get_bucket_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_acl("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_acl("test-bucket", )


async def test_get_bucket_analytics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_analytics_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_bucket_analytics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_analytics_configuration("test-bucket", "test-id", )


async def test_get_bucket_cors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_cors("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_cors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_cors("test-bucket", )


async def test_get_bucket_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_encryption("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_encryption("test-bucket", )


async def test_get_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", )


async def test_get_bucket_inventory_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_inventory_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_bucket_inventory_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_inventory_configuration("test-bucket", "test-id", )


async def test_get_bucket_lifecycle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_lifecycle("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_lifecycle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_lifecycle("test-bucket", )


async def test_get_bucket_lifecycle_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_lifecycle_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_lifecycle_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_lifecycle_configuration("test-bucket", )


async def test_get_bucket_location(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_location("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_location_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_location("test-bucket", )


async def test_get_bucket_logging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_logging("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_logging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_logging("test-bucket", )


async def test_get_bucket_metadata_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_metadata_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_metadata_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_metadata_configuration("test-bucket", )


async def test_get_bucket_metadata_table_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_metadata_table_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_metadata_table_configuration("test-bucket", )


async def test_get_bucket_metrics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_metrics_configuration("test-bucket", "test-id", )
    mock_client.call.assert_called_once()


async def test_get_bucket_metrics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_metrics_configuration("test-bucket", "test-id", )


async def test_get_bucket_notification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_notification("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_notification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_notification("test-bucket", )


async def test_get_bucket_notification_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_notification_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_notification_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_notification_configuration("test-bucket", )


async def test_get_bucket_ownership_controls(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_ownership_controls("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_ownership_controls_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_ownership_controls("test-bucket", )


async def test_get_bucket_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_policy("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_policy("test-bucket", )


async def test_get_bucket_policy_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_policy_status("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_policy_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_policy_status("test-bucket", )


async def test_get_bucket_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_replication("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_replication("test-bucket", )


async def test_get_bucket_request_payment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_request_payment("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_request_payment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_request_payment("test-bucket", )


async def test_get_bucket_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_tagging("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_tagging("test-bucket", )


async def test_get_bucket_versioning(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_versioning("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_versioning_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_versioning("test-bucket", )


async def test_get_bucket_website(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_website("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_bucket_website_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_website("test-bucket", )


async def test_get_object_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_acl("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_get_object_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_acl("test-bucket", "test-key", )


async def test_get_object_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_attributes("test-bucket", "test-key", [], )
    mock_client.call.assert_called_once()


async def test_get_object_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_attributes("test-bucket", "test-key", [], )


async def test_get_object_legal_hold(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_legal_hold("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_get_object_legal_hold_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_legal_hold("test-bucket", "test-key", )


async def test_get_object_lock_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_lock_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_object_lock_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_lock_configuration("test-bucket", )


async def test_get_object_retention(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_retention("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_get_object_retention_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_retention("test-bucket", "test-key", )


async def test_get_object_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_tagging("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_get_object_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_tagging("test-bucket", "test-key", )


async def test_get_object_torrent(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_object_torrent("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_get_object_torrent_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_object_torrent("test-bucket", "test-key", )


async def test_get_public_access_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_public_access_block("test-bucket", )
    mock_client.call.assert_called_once()


async def test_get_public_access_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_public_access_block("test-bucket", )


async def test_head_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await head_bucket("test-bucket", )
    mock_client.call.assert_called_once()


async def test_head_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await head_bucket("test-bucket", )


async def test_head_object(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await head_object("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_head_object_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await head_object("test-bucket", "test-key", )


async def test_list_bucket_analytics_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bucket_analytics_configurations("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_bucket_analytics_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bucket_analytics_configurations("test-bucket", )


async def test_list_bucket_intelligent_tiering_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bucket_intelligent_tiering_configurations("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_bucket_intelligent_tiering_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bucket_intelligent_tiering_configurations("test-bucket", )


async def test_list_bucket_inventory_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bucket_inventory_configurations("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_bucket_inventory_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bucket_inventory_configurations("test-bucket", )


async def test_list_bucket_metrics_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bucket_metrics_configurations("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_bucket_metrics_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bucket_metrics_configurations("test-bucket", )


async def test_list_buckets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_buckets()
    mock_client.call.assert_called_once()


async def test_list_buckets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_buckets()


async def test_list_directory_buckets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_directory_buckets()
    mock_client.call.assert_called_once()


async def test_list_directory_buckets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_directory_buckets()


async def test_list_multipart_uploads(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_multipart_uploads("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_multipart_uploads_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_multipart_uploads("test-bucket", )


async def test_list_objects_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_objects_v2("test-bucket", )
    mock_client.call.assert_called_once()


async def test_list_objects_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_objects_v2("test-bucket", )


async def test_list_parts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_parts("test-bucket", "test-key", "test-upload_id", )
    mock_client.call.assert_called_once()


async def test_list_parts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_parts("test-bucket", "test-key", "test-upload_id", )


async def test_put_bucket_accelerate_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_accelerate_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_accelerate_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_accelerate_configuration("test-bucket", {}, )


async def test_put_bucket_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_acl("test-bucket", )
    mock_client.call.assert_called_once()


async def test_put_bucket_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_acl("test-bucket", )


async def test_put_bucket_analytics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_analytics_configuration("test-bucket", "test-id", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_analytics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_analytics_configuration("test-bucket", "test-id", {}, )


async def test_put_bucket_cors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_cors("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_cors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_cors("test-bucket", {}, )


async def test_put_bucket_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_encryption("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_encryption("test-bucket", {}, )


async def test_put_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, )


async def test_put_bucket_inventory_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_inventory_configuration("test-bucket", "test-id", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_inventory_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_inventory_configuration("test-bucket", "test-id", {}, )


async def test_put_bucket_lifecycle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_lifecycle("test-bucket", )
    mock_client.call.assert_called_once()


async def test_put_bucket_lifecycle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_lifecycle("test-bucket", )


async def test_put_bucket_lifecycle_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_lifecycle_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_put_bucket_lifecycle_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_lifecycle_configuration("test-bucket", )


async def test_put_bucket_logging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_logging("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_logging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_logging("test-bucket", {}, )


async def test_put_bucket_metrics_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_metrics_configuration("test-bucket", "test-id", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_metrics_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_metrics_configuration("test-bucket", "test-id", {}, )


async def test_put_bucket_notification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_notification("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_notification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_notification("test-bucket", {}, )


async def test_put_bucket_notification_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_notification_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_notification_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_notification_configuration("test-bucket", {}, )


async def test_put_bucket_ownership_controls(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_ownership_controls("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_ownership_controls_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_ownership_controls("test-bucket", {}, )


async def test_put_bucket_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_policy("test-bucket", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_bucket_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_policy("test-bucket", "test-policy", )


async def test_put_bucket_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_replication("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_replication("test-bucket", {}, )


async def test_put_bucket_request_payment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_request_payment("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_request_payment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_request_payment("test-bucket", {}, )


async def test_put_bucket_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_tagging("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_tagging("test-bucket", {}, )


async def test_put_bucket_versioning(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_versioning("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_versioning_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_versioning("test-bucket", {}, )


async def test_put_bucket_website(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_bucket_website("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_bucket_website_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_bucket_website("test-bucket", {}, )


async def test_put_object(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_put_object_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object("test-bucket", "test-key", )


async def test_put_object_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object_acl("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_put_object_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object_acl("test-bucket", "test-key", )


async def test_put_object_legal_hold(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object_legal_hold("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_put_object_legal_hold_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object_legal_hold("test-bucket", "test-key", )


async def test_put_object_lock_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object_lock_configuration("test-bucket", )
    mock_client.call.assert_called_once()


async def test_put_object_lock_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object_lock_configuration("test-bucket", )


async def test_put_object_retention(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object_retention("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_put_object_retention_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object_retention("test-bucket", "test-key", )


async def test_put_object_tagging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_object_tagging("test-bucket", "test-key", {}, )
    mock_client.call.assert_called_once()


async def test_put_object_tagging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_object_tagging("test-bucket", "test-key", {}, )


async def test_put_public_access_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_public_access_block("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_put_public_access_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_public_access_block("test-bucket", {}, )


async def test_rename_object(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await rename_object("test-bucket", "test-key", "test-rename_source", )
    mock_client.call.assert_called_once()


async def test_rename_object_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rename_object("test-bucket", "test-key", "test-rename_source", )


async def test_restore_object(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_object("test-bucket", "test-key", )
    mock_client.call.assert_called_once()


async def test_restore_object_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_object("test-bucket", "test-key", )


async def test_select_object_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", {}, {}, )
    mock_client.call.assert_called_once()


async def test_select_object_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", {}, {}, )


async def test_update_bucket_metadata_inventory_table_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bucket_metadata_inventory_table_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_update_bucket_metadata_inventory_table_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bucket_metadata_inventory_table_configuration("test-bucket", {}, )


async def test_update_bucket_metadata_journal_table_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bucket_metadata_journal_table_configuration("test-bucket", {}, )
    mock_client.call.assert_called_once()


async def test_update_bucket_metadata_journal_table_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bucket_metadata_journal_table_configuration("test-bucket", {}, )


async def test_upload_part(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_part("test-bucket", "test-key", 1, "test-upload_id", )
    mock_client.call.assert_called_once()


async def test_upload_part_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_part("test-bucket", "test-key", 1, "test-upload_id", )


async def test_upload_part_copy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_part_copy("test-bucket", "test-copy_source", "test-key", 1, "test-upload_id", )
    mock_client.call.assert_called_once()


async def test_upload_part_copy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_part_copy("test-bucket", "test-copy_source", "test-key", 1, "test-upload_id", )


async def test_write_get_object_response(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    await write_get_object_response("test-request_route", "test-request_token", )
    mock_client.call.assert_called_once()


async def test_write_get_object_response_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.s3.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await write_get_object_response("test-request_route", "test-request_token", )


@pytest.mark.asyncio
async def test_get_object_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object("test-bucket", "test-key", version_id="test-version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_abort_multipart_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import abort_multipart_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await abort_multipart_upload("test-bucket", "test-key", "test-upload_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", if_match_initiated_time="test-if_match_initiated_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_complete_multipart_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import complete_multipart_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await complete_multipart_upload("test-bucket", "test-key", "test-upload_id", multipart_upload=True, checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", checksum_type="test-checksum_type", mpu_object_size=1, request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", if_match="test-if_match", if_none_match="test-if_none_match", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import create_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await create_bucket("test-bucket", acl="test-acl", create_bucket_configuration={}, grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", object_lock_enabled_for_bucket="test-object_lock_enabled_for_bucket", object_ownership="test-object_ownership", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import create_bucket_metadata_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await create_bucket_metadata_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import create_bucket_metadata_table_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await create_bucket_metadata_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_multipart_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import create_multipart_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await create_multipart_upload("test-bucket", "test-key", acl="test-acl", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_type="test-content_type", expires="test-expires", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write_acp="test-grant_write_acp", metadata="test-metadata", server_side_encryption="test-server_side_encryption", storage_class="test-storage_class", website_redirect_location="test-website_redirect_location", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", request_payer="test-request_payer", tagging="test-tagging", object_lock_mode="test-object_lock_mode", object_lock_retain_until_date="test-object_lock_retain_until_date", object_lock_legal_hold_status="test-object_lock_legal_hold_status", expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", checksum_type="test-checksum_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import create_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await create_session("test-bucket", session_mode="test-session_mode", server_side_encryption="test-server_side_encryption", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_analytics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_analytics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_cors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_cors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_cors("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_encryption("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_intelligent_tiering_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_inventory_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_inventory_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_lifecycle
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_lifecycle("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_metadata_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_metadata_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_metadata_table_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_metadata_table_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_metrics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_metrics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_ownership_controls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_ownership_controls("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_policy("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_replication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_replication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_replication("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_tagging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_website_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_bucket_website
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_bucket_website("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_object_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_object_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_object_tagging("test-bucket", "test-key", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_objects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_objects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_objects("test-bucket", True, mfa="test-mfa", request_payer="test-request_payer", bypass_governance_retention=True, expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_public_access_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import delete_public_access_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await delete_public_access_block("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_accelerate_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_accelerate_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_accelerate_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_acl("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_analytics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_analytics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_cors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_cors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_cors("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_encryption("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_intelligent_tiering_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_inventory_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_inventory_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_lifecycle
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_lifecycle("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_lifecycle_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_lifecycle_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_lifecycle_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_location_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_location
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_location("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_logging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_logging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_logging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_metadata_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_metadata_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_metadata_table_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_metadata_table_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_metrics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_metrics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_notification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_notification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_notification("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_notification_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_notification_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_notification_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_ownership_controls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_ownership_controls("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_policy("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_policy_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_policy_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_policy_status("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_replication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_replication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_replication("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_request_payment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_request_payment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_request_payment("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_tagging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_versioning_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_versioning
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_versioning("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_website_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_bucket_website
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_bucket_website("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_acl("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_attributes("test-bucket", "test-key", "test-object_attributes", version_id="test-version_id", max_parts=1, part_number_marker="test-part_number_marker", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_legal_hold_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_legal_hold
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_legal_hold("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_lock_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_lock_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_lock_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_retention_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_retention
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_retention("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_tagging("test-bucket", "test-key", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_object_torrent_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_object_torrent
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_object_torrent("test-bucket", "test-key", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_public_access_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import get_public_access_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await get_public_access_block("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_head_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import head_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await head_bucket("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_head_object_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import head_object
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await head_object("test-bucket", "test-key", if_match="test-if_match", if_modified_since="test-if_modified_since", if_none_match="test-if_none_match", if_unmodified_since="test-if_unmodified_since", range="test-range", response_cache_control="test-response_cache_control", response_content_disposition="test-response_content_disposition", response_content_encoding="test-response_content_encoding", response_content_language="test-response_content_language", response_content_type="test-response_content_type", response_expires="test-response_expires", version_id="test-version_id", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", part_number="test-part_number", expected_bucket_owner="test-expected_bucket_owner", checksum_mode="test-checksum_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bucket_analytics_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_bucket_analytics_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_bucket_analytics_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bucket_intelligent_tiering_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_bucket_intelligent_tiering_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_bucket_intelligent_tiering_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bucket_inventory_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_bucket_inventory_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_bucket_inventory_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bucket_metrics_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_bucket_metrics_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_bucket_metrics_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_buckets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_buckets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_buckets(max_buckets=1, continuation_token="test-continuation_token", prefix="test-prefix", bucket_region="test-bucket_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_directory_buckets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_directory_buckets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_directory_buckets(continuation_token="test-continuation_token", max_directory_buckets=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_multipart_uploads_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_multipart_uploads
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_multipart_uploads("test-bucket", delimiter=1, encoding_type="test-encoding_type", key_marker="test-key_marker", max_uploads=1, prefix="test-prefix", upload_id_marker="test-upload_id_marker", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_objects_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_objects_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_objects_v2("test-bucket", delimiter=1, encoding_type="test-encoding_type", max_keys=1, prefix="test-prefix", continuation_token="test-continuation_token", fetch_owner="test-fetch_owner", start_after="test-start_after", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", optional_object_attributes="test-optional_object_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_parts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import list_parts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await list_parts("test-bucket", "test-key", "test-upload_id", max_parts=1, part_number_marker="test-part_number_marker", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_accelerate_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_accelerate_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_accelerate_configuration("test-bucket", {}, expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_acl("test-bucket", acl="test-acl", access_control_policy="{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_analytics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_analytics_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_cors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_cors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_cors("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_encryption("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_intelligent_tiering_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_inventory_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_inventory_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_lifecycle
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_lifecycle("test-bucket", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", lifecycle_configuration={}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_lifecycle_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_lifecycle_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_lifecycle_configuration("test-bucket", checksum_algorithm="test-checksum_algorithm", lifecycle_configuration={}, expected_bucket_owner="test-expected_bucket_owner", transition_default_minimum_object_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_logging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_logging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_logging("test-bucket", "test-bucket_logging_status", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_metrics_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_metrics_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_notification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_notification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_notification("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_notification_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_notification_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_notification_configuration("test-bucket", {}, expected_bucket_owner="test-expected_bucket_owner", skip_destination_validation=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_ownership_controls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_ownership_controls("test-bucket", "test-ownership_controls", content_md5="test-content_md5", expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_policy("test-bucket", "{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", confirm_remove_self_bucket_access=True, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_replication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_replication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_replication("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", token="test-token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_request_payment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_request_payment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_request_payment("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_tagging("test-bucket", "test-tagging", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_versioning_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_versioning
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_versioning("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", mfa="test-mfa", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_bucket_website_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_bucket_website
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_bucket_website("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object("test-bucket", "test-key", acl="test-acl", body="test-body", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_length="test-content_length", content_md5="test-content_md5", content_type="test-content_type", checksum_algorithm="test-checksum_algorithm", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", expires="test-expires", if_match="test-if_match", if_none_match="test-if_none_match", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write_acp="test-grant_write_acp", write_offset_bytes="test-write_offset_bytes", metadata="test-metadata", server_side_encryption="test-server_side_encryption", storage_class="test-storage_class", website_redirect_location="test-website_redirect_location", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", request_payer="test-request_payer", tagging="test-tagging", object_lock_mode="test-object_lock_mode", object_lock_retain_until_date="test-object_lock_retain_until_date", object_lock_legal_hold_status="test-object_lock_legal_hold_status", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object_acl("test-bucket", "test-key", acl="test-acl", access_control_policy="{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", request_payer="test-request_payer", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_legal_hold_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object_legal_hold
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object_legal_hold("test-bucket", "test-key", legal_hold="test-legal_hold", request_payer="test-request_payer", version_id="test-version_id", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_lock_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object_lock_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object_lock_configuration("test-bucket", object_lock_configuration={}, request_payer="test-request_payer", token="test-token", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_retention_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object_retention
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object_retention("test-bucket", "test-key", retention="test-retention", request_payer="test-request_payer", version_id="test-version_id", bypass_governance_retention=True, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_object_tagging_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_object_tagging
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_object_tagging("test-bucket", "test-key", "test-tagging", version_id="test-version_id", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_public_access_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import put_public_access_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await put_public_access_block("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_rename_object_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import rename_object
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await rename_object("test-bucket", "test-key", "test-rename_source", destination_if_match="test-destination_if_match", destination_if_none_match="test-destination_if_none_match", destination_if_modified_since="test-destination_if_modified_since", destination_if_unmodified_since="test-destination_if_unmodified_since", source_if_match="test-source_if_match", source_if_none_match="test-source_if_none_match", source_if_modified_since="test-source_if_modified_since", source_if_unmodified_since="test-source_if_unmodified_since", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_object_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import restore_object
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await restore_object("test-bucket", "test-key", version_id="test-version_id", restore_request="test-restore_request", request_payer="test-request_payer", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_select_object_content_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import select_object_content
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", "test-input_serialization", "test-output_serialization", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_progress="test-request_progress", scan_range="test-scan_range", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bucket_metadata_inventory_table_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import update_bucket_metadata_inventory_table_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await update_bucket_metadata_inventory_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bucket_metadata_journal_table_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import update_bucket_metadata_journal_table_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await update_bucket_metadata_journal_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_upload_part_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import upload_part
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await upload_part("test-bucket", "test-key", "test-part_number", "test-upload_id", body="test-body", content_length="test-content_length", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_upload_part_copy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import upload_part_copy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await upload_part_copy("test-bucket", "test-copy_source", "test-key", "test-part_number", "test-upload_id", copy_source_if_match="test-copy_source_if_match", copy_source_if_modified_since="test-copy_source_if_modified_since", copy_source_if_none_match="test-copy_source_if_none_match", copy_source_if_unmodified_since="test-copy_source_if_unmodified_since", copy_source_range="test-copy_source_range", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", copy_source_sse_customer_algorithm="test-copy_source_sse_customer_algorithm", copy_source_sse_customer_key="test-copy_source_sse_customer_key", copy_source_sse_customer_key_md5="test-copy_source_sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", expected_source_bucket_owner="test-expected_source_bucket_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_write_get_object_response_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.s3 import write_get_object_response
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.s3.async_client", lambda *a, **kw: mock_client)
    await write_get_object_response("test-request_route", "test-request_token", body="test-body", status_code="test-status_code", error_code="test-error_code", error_message="test-error_message", accept_ranges="test-accept_ranges", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_length="test-content_length", content_range="test-content_range", content_type="test-content_type", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", delete_marker=True, e_tag="test-e_tag", expires="test-expires", expiration="test-expiration", last_modified="test-last_modified", missing_meta="test-missing_meta", metadata="test-metadata", object_lock_mode="test-object_lock_mode", object_lock_legal_hold_status="test-object_lock_legal_hold_status", object_lock_retain_until_date="test-object_lock_retain_until_date", parts_count=1, replication_status="test-replication_status", request_charged="test-request_charged", restore="test-restore", server_side_encryption="test-server_side_encryption", sse_customer_algorithm="test-sse_customer_algorithm", ssekms_key_id="test-ssekms_key_id", sse_customer_key_md5="test-sse_customer_key_md5", storage_class="test-storage_class", tag_count=1, version_id="test-version_id", bucket_key_enabled="test-bucket_key_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()
