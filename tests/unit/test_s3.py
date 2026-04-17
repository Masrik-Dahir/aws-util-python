"""Tests for aws_util.s3 module."""
from __future__ import annotations


from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.s3 import (
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

REGION = "us-east-1"
BUCKET = "test-bucket"


# ---------------------------------------------------------------------------
# upload_bytes / download_bytes
# ---------------------------------------------------------------------------


def test_upload_and_download_bytes(s3_client):
    upload_bytes(BUCKET, "data/test.bin", b"hello bytes", region_name=REGION)
    result = download_bytes(BUCKET, "data/test.bin", region_name=REGION)
    assert result == b"hello bytes"


def test_upload_bytes_with_content_type(s3_client):
    upload_bytes(
        BUCKET,
        "data/test.json",
        b'{"a":1}',
        content_type="application/json",
        region_name=REGION,
    )
    result = download_bytes(BUCKET, "data/test.json", region_name=REGION)
    assert result == b'{"a":1}'


def test_upload_bytes_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.put_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "bucket not found"}},
        "PutObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload bytes"):
        upload_bytes("noexist", "key", b"data", region_name=REGION)


def test_download_bytes_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "not found"}},
        "GetObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to download"):
        download_bytes(BUCKET, "nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# upload_file / download_file
# ---------------------------------------------------------------------------


def test_upload_file_and_download_file(s3_client, tmp_path):
    src = tmp_path / "source.txt"
    src.write_bytes(b"file content")
    upload_file(BUCKET, "dir/source.txt", src, region_name=REGION)

    dest = tmp_path / "dest.txt"
    download_file(BUCKET, "dir/source.txt", dest, region_name=REGION)
    assert dest.read_bytes() == b"file content"


def test_upload_file_with_content_type(s3_client, tmp_path):
    src = tmp_path / "page.html"
    src.write_bytes(b"<html/>")
    upload_file(BUCKET, "page.html", src, content_type="text/html", region_name=REGION)
    result = download_bytes(BUCKET, "page.html", region_name=REGION)
    assert result == b"<html/>"


def test_upload_file_runtime_error(monkeypatch, tmp_path):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    src = tmp_path / "f.txt"
    src.write_bytes(b"x")

    mock_client = MagicMock()
    mock_client.upload_file.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "UploadFile",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload"):
        upload_file("noexist", "k", src, region_name=REGION)


def test_download_file_runtime_error(monkeypatch, tmp_path):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.download_file.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "not found"}},
        "DownloadFile",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to download"):
        download_file(BUCKET, "nonexistent", tmp_path / "dest.txt", region_name=REGION)


# ---------------------------------------------------------------------------
# list_objects
# ---------------------------------------------------------------------------


def test_list_objects_empty(s3_client):
    result = list_objects(BUCKET, region_name=REGION)
    assert result == []


def test_list_objects_with_objects(s3_client):
    upload_bytes(BUCKET, "a.txt", b"a", region_name=REGION)
    upload_bytes(BUCKET, "b.txt", b"b", region_name=REGION)
    result = list_objects(BUCKET, region_name=REGION)
    keys = [obj.key for obj in result]
    assert "a.txt" in keys
    assert "b.txt" in keys


def test_list_objects_with_prefix(s3_client):
    upload_bytes(BUCKET, "prefix/a.txt", b"a", region_name=REGION)
    upload_bytes(BUCKET, "other/b.txt", b"b", region_name=REGION)
    result = list_objects(BUCKET, prefix="prefix/", region_name=REGION)
    keys = [obj.key for obj in result]
    assert "prefix/a.txt" in keys
    assert "other/b.txt" not in keys


def test_list_objects_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "ListObjectsV2",
    )
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list objects"):
        list_objects(BUCKET, region_name=REGION)


# ---------------------------------------------------------------------------
# object_exists
# ---------------------------------------------------------------------------


def test_object_exists_true(s3_client):
    upload_bytes(BUCKET, "exists.txt", b"x", region_name=REGION)
    assert object_exists(BUCKET, "exists.txt", region_name=REGION) is True


def test_object_exists_false(s3_client):
    assert object_exists(BUCKET, "nonexistent.txt", region_name=REGION) is False


def test_object_exists_other_error_raises(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.head_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "HeadObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to check existence"):
        object_exists(BUCKET, "key", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_object
# ---------------------------------------------------------------------------


def test_delete_object(s3_client):
    upload_bytes(BUCKET, "todel.txt", b"x", region_name=REGION)
    delete_object(BUCKET, "todel.txt", region_name=REGION)
    assert object_exists(BUCKET, "todel.txt", region_name=REGION) is False


def test_delete_object_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.delete_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "DeleteObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete"):
        delete_object(BUCKET, "key", region_name=REGION)


# ---------------------------------------------------------------------------
# copy_object
# ---------------------------------------------------------------------------


def test_copy_object(s3_client):
    upload_bytes(BUCKET, "src/file.txt", b"copy-me", region_name=REGION)
    copy_object(BUCKET, "src/file.txt", BUCKET, "dst/file.txt", region_name=REGION)
    result = download_bytes(BUCKET, "dst/file.txt", region_name=REGION)
    assert result == b"copy-me"


def test_copy_object_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.copy_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "not found"}},
        "CopyObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy"):
        copy_object(BUCKET, "src", BUCKET, "dst", region_name=REGION)


# ---------------------------------------------------------------------------
# move_object
# ---------------------------------------------------------------------------


def test_move_object(s3_client):
    upload_bytes(BUCKET, "move/src.txt", b"move-me", region_name=REGION)
    move_object(BUCKET, "move/src.txt", BUCKET, "move/dst.txt", region_name=REGION)
    assert object_exists(BUCKET, "move/dst.txt", region_name=REGION) is True
    assert object_exists(BUCKET, "move/src.txt", region_name=REGION) is False


# ---------------------------------------------------------------------------
# presigned_url
# ---------------------------------------------------------------------------


def test_presigned_url_get_object(s3_client):
    upload_bytes(BUCKET, "presigned.txt", b"x", region_name=REGION)
    result = presigned_url(BUCKET, "presigned.txt", expires_in=60, region_name=REGION)
    assert result.url.startswith("https://")
    assert result.bucket == BUCKET
    assert result.key == "presigned.txt"
    assert result.expires_in == 60


def test_presigned_url_put_object(s3_client):
    result = presigned_url(
        BUCKET, "upload.txt", operation="put_object", region_name=REGION
    )
    assert result.url.startswith("https://")


def test_presigned_url_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.generate_presigned_url.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "GeneratePresignedUrl",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate pre-signed URL"):
        presigned_url(BUCKET, "k", region_name=REGION)


# ---------------------------------------------------------------------------
# read_json / write_json
# ---------------------------------------------------------------------------


def test_write_json_and_read_json(s3_client):
    data = {"hello": "world", "number": 42}
    write_json(BUCKET, "data.json", data, region_name=REGION)
    result = read_json(BUCKET, "data.json", region_name=REGION)
    assert result == data


def test_write_json_with_indent(s3_client):
    write_json(BUCKET, "pretty.json", {"x": 1}, indent=2, region_name=REGION)
    raw = download_bytes(BUCKET, "pretty.json", region_name=REGION)
    assert b"\n" in raw  # indented output


def test_read_json_invalid_content(s3_client):
    upload_bytes(BUCKET, "bad.json", b"not-json", region_name=REGION)
    with pytest.raises(ValueError, match="not valid JSON"):
        read_json(BUCKET, "bad.json", region_name=REGION)


# ---------------------------------------------------------------------------
# read_jsonl
# ---------------------------------------------------------------------------


def test_read_jsonl_yields_objects(s3_client):
    content = b'{"a":1}\n{"b":2}\n{"c":3}\n'
    upload_bytes(BUCKET, "data.jsonl", content, region_name=REGION)
    result = list(read_jsonl(BUCKET, "data.jsonl", region_name=REGION))
    assert result == [{"a": 1}, {"b": 2}, {"c": 3}]


def test_read_jsonl_skips_empty_lines(s3_client):
    content = b'{"a":1}\n\n{"b":2}\n'
    upload_bytes(BUCKET, "sparse.jsonl", content, region_name=REGION)
    result = list(read_jsonl(BUCKET, "sparse.jsonl", region_name=REGION))
    assert result == [{"a": 1}, {"b": 2}]


def test_read_jsonl_invalid_line_raises(s3_client):
    content = b'{"a":1}\nnot-json\n'
    upload_bytes(BUCKET, "bad.jsonl", content, region_name=REGION)
    with pytest.raises(ValueError, match="line 2 is not valid JSON"):
        list(read_jsonl(BUCKET, "bad.jsonl", region_name=REGION))


# ---------------------------------------------------------------------------
# get_object_metadata
# ---------------------------------------------------------------------------


def test_get_object_metadata(s3_client):
    upload_bytes(BUCKET, "meta.txt", b"metadata test", content_type="text/plain", region_name=REGION)
    meta = get_object_metadata(BUCKET, "meta.txt", region_name=REGION)
    assert meta["content_length"] == len(b"metadata test")
    assert "content_type" in meta


def test_get_object_metadata_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.head_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "not found"}},
        "HeadObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get metadata"):
        get_object_metadata(BUCKET, "key", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_prefix
# ---------------------------------------------------------------------------


def test_delete_prefix(s3_client):
    upload_bytes(BUCKET, "logs/a.txt", b"a", region_name=REGION)
    upload_bytes(BUCKET, "logs/b.txt", b"b", region_name=REGION)
    upload_bytes(BUCKET, "keep/c.txt", b"c", region_name=REGION)
    count = delete_prefix(BUCKET, "logs/", region_name=REGION)
    assert count == 2
    assert object_exists(BUCKET, "keep/c.txt", region_name=REGION) is True


def test_delete_prefix_empty(s3_client):
    count = delete_prefix(BUCKET, "nonexistent/", region_name=REGION)
    assert count == 0


def test_delete_prefix_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "ListObjectsV2",
    )
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_prefix failed"):
        delete_prefix(BUCKET, "prefix/", region_name=REGION)


# ---------------------------------------------------------------------------
# sync_folder
# ---------------------------------------------------------------------------


def test_sync_folder_uploads_new_files(s3_client, tmp_path):
    (tmp_path / "a.txt").write_bytes(b"file-a")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_bytes(b"file-b")
    counts = sync_folder(tmp_path, BUCKET, region_name=REGION)
    assert counts["uploaded"] == 2
    assert counts["skipped"] == 0


def test_sync_folder_skips_unchanged_files(s3_client, tmp_path):
    (tmp_path / "same.txt").write_bytes(b"content")
    sync_folder(tmp_path, BUCKET, region_name=REGION)
    # Second sync should skip unchanged file
    counts = sync_folder(tmp_path, BUCKET, region_name=REGION)
    assert counts["skipped"] == 1
    assert counts["uploaded"] == 0


def test_sync_folder_deletes_removed(s3_client, tmp_path):
    (tmp_path / "keep.txt").write_bytes(b"keep")
    sync_folder(tmp_path, BUCKET, prefix="sync/", region_name=REGION)
    # Upload another object directly that won't be in local folder
    upload_bytes(BUCKET, "sync/extra.txt", b"extra", region_name=REGION)
    counts = sync_folder(
        tmp_path, BUCKET, prefix="sync/", delete_removed=True, region_name=REGION
    )
    assert counts["deleted"] == 1


def test_sync_folder_not_a_directory(tmp_path):
    f = tmp_path / "file.txt"
    f.write_bytes(b"x")
    with pytest.raises(ValueError, match="is not a directory"):
        sync_folder(f, BUCKET, region_name=REGION)


def test_sync_folder_with_prefix(s3_client, tmp_path):
    (tmp_path / "x.txt").write_bytes(b"x")
    counts = sync_folder(tmp_path, BUCKET, prefix="myprefix", region_name=REGION)
    assert counts["uploaded"] == 1
    assert object_exists(BUCKET, "myprefix/x.txt", region_name=REGION)


# ---------------------------------------------------------------------------
# multipart_upload
# ---------------------------------------------------------------------------


def test_multipart_upload_too_small_part_size(s3_client, tmp_path):
    f = tmp_path / "big.bin"
    f.write_bytes(b"x" * 100)
    with pytest.raises(ValueError, match="at least 5 MB"):
        multipart_upload(BUCKET, "big.bin", f, part_size_mb=4, region_name=REGION)


def test_multipart_upload_success(s3_client, tmp_path):
    f = tmp_path / "big.bin"
    # 6 MB file to trigger at least one part
    f.write_bytes(b"A" * (6 * 1024 * 1024))
    multipart_upload(BUCKET, "big.bin", f, part_size_mb=5, region_name=REGION)
    result = download_bytes(BUCKET, "big.bin", region_name=REGION)
    assert len(result) == 6 * 1024 * 1024


def test_multipart_upload_failure_aborts(s3_client, tmp_path, monkeypatch):
    """When a part upload fails, the multipart upload is aborted."""
    import aws_util.s3 as s3mod

    f = tmp_path / "big.bin"
    f.write_bytes(b"A" * (6 * 1024 * 1024))

    real_get_client = s3mod.get_client
    calls = {"count": 0}

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)
        if service == "s3" and calls["count"] == 0:
            calls["count"] += 1

            def failing_upload_part(**kwargs):
                raise RuntimeError("Simulated part failure")

            client.upload_part = failing_upload_part
        return client

    monkeypatch.setattr(s3mod, "get_client", patched_get_client)
    with pytest.raises(RuntimeError, match="Multipart upload failed"):
        multipart_upload(BUCKET, "big.bin", f, part_size_mb=5, region_name=REGION)


# ---------------------------------------------------------------------------
# batch_copy
# ---------------------------------------------------------------------------


def test_batch_copy_copies_all(s3_client):
    upload_bytes(BUCKET, "bc/src1.txt", b"s1", region_name=REGION)
    upload_bytes(BUCKET, "bc/src2.txt", b"s2", region_name=REGION)
    batch_copy(
        [
            {"src_bucket": BUCKET, "src_key": "bc/src1.txt", "dst_bucket": BUCKET, "dst_key": "bc/dst1.txt"},
            {"src_bucket": BUCKET, "src_key": "bc/src2.txt", "dst_bucket": BUCKET, "dst_key": "bc/dst2.txt"},
        ],
        region_name=REGION,
    )
    assert download_bytes(BUCKET, "bc/dst1.txt", region_name=REGION) == b"s1"
    assert download_bytes(BUCKET, "bc/dst2.txt", region_name=REGION) == b"s2"


def test_batch_copy_raises_on_failure():
    with pytest.raises(RuntimeError, match="batch_copy had"):
        batch_copy(
            [{"src_bucket": "noexist", "src_key": "k", "dst_bucket": BUCKET, "dst_key": "d"}],
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# download_as_text
# ---------------------------------------------------------------------------


def test_download_as_text(s3_client):
    upload_bytes(BUCKET, "text.txt", "héllo wörld".encode("utf-8"), region_name=REGION)
    result = download_as_text(BUCKET, "text.txt", encoding="utf-8", region_name=REGION)
    assert result == "héllo wörld"


# ---------------------------------------------------------------------------
# generate_presigned_post
# ---------------------------------------------------------------------------


def test_generate_presigned_post(s3_client):
    result = generate_presigned_post(BUCKET, "upload.bin", max_size_mb=5, region_name=REGION)
    assert "url" in result
    assert "fields" in result


def test_generate_presigned_post_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.generate_presigned_post.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "GeneratePresignedPost",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate presigned POST"):
        generate_presigned_post(BUCKET, "k", region_name=REGION)


# ---------------------------------------------------------------------------
# download_bytes — version_id branch
# ---------------------------------------------------------------------------


def test_download_bytes_with_version_id(s3_client):
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    s3_client.put_object(Bucket=BUCKET, Key="versioned.txt", Body=b"v1")
    resp2 = s3_client.put_object(Bucket=BUCKET, Key="versioned.txt", Body=b"v2")
    v2_id = resp2["VersionId"]

    # Latest should be v2
    assert download_bytes(BUCKET, "versioned.txt", region_name=REGION) == b"v2"

    # Fetch the specific version
    result = download_bytes(
        BUCKET, "versioned.txt", version_id=v2_id, region_name=REGION
    )
    assert result == b"v2"


# ---------------------------------------------------------------------------
# get_object
# ---------------------------------------------------------------------------


def test_get_object_returns_body(s3_client):
    upload_bytes(BUCKET, "obj.txt", b"hello object", region_name=REGION)
    resp = get_object(BUCKET, "obj.txt", region_name=REGION)
    assert resp["Body"].read() == b"hello object"
    assert "ContentLength" in resp


def test_get_object_with_version_id(s3_client):
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    r1 = s3_client.put_object(Bucket=BUCKET, Key="ver.txt", Body=b"first")
    s3_client.put_object(Bucket=BUCKET, Key="ver.txt", Body=b"second")
    v1_id = r1["VersionId"]

    resp = get_object(BUCKET, "ver.txt", version_id=v1_id, region_name=REGION)
    assert resp["Body"].read() == b"first"


def test_get_object_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.get_object.side_effect = ClientError(
        {"Error": {"Code": "NoSuchKey", "Message": "not found"}},
        "GetObject",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get"):
        get_object(BUCKET, "nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# list_object_versions
# ---------------------------------------------------------------------------


def test_list_object_versions_multiple(s3_client):
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    s3_client.put_object(Bucket=BUCKET, Key="doc.txt", Body=b"v1")
    s3_client.put_object(Bucket=BUCKET, Key="doc.txt", Body=b"v2")
    s3_client.put_object(Bucket=BUCKET, Key="doc.txt", Body=b"v3")

    versions = list_object_versions(BUCKET, region_name=REGION)
    assert len(versions) == 3
    assert all(isinstance(v, S3ObjectVersion) for v in versions)
    assert all(v.key == "doc.txt" for v in versions)
    assert all(v.bucket == BUCKET for v in versions)
    # Exactly one version should be marked latest
    latest = [v for v in versions if v.is_latest]
    assert len(latest) == 1


def test_list_object_versions_empty(s3_client):
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    versions = list_object_versions(BUCKET, region_name=REGION)
    assert versions == []


def test_list_object_versions_with_prefix(s3_client):
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    s3_client.put_object(Bucket=BUCKET, Key="alpha/a.txt", Body=b"a1")
    s3_client.put_object(Bucket=BUCKET, Key="alpha/a.txt", Body=b"a2")
    s3_client.put_object(Bucket=BUCKET, Key="beta/b.txt", Body=b"b1")

    versions = list_object_versions(BUCKET, prefix="alpha/", region_name=REGION)
    assert len(versions) == 2
    assert all(v.key.startswith("alpha/") for v in versions)


def test_list_object_versions_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.list_object_versions.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "ListObjectVersions",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list versions"):
        list_object_versions(BUCKET, region_name=REGION)


# ---------------------------------------------------------------------------
# upload_fileobj
# ---------------------------------------------------------------------------


def test_upload_fileobj_from_bytesio(s3_client):
    import io

    fileobj = io.BytesIO(b"fileobj content")
    upload_fileobj(BUCKET, "fileobj.txt", fileobj, region_name=REGION)
    result = download_bytes(BUCKET, "fileobj.txt", region_name=REGION)
    assert result == b"fileobj content"


def test_upload_fileobj_with_content_type(s3_client):
    import io

    fileobj = io.BytesIO(b'{"key": "value"}')
    upload_fileobj(
        BUCKET,
        "data.json",
        fileobj,
        content_type="application/json",
        region_name=REGION,
    )
    result = download_bytes(BUCKET, "data.json", region_name=REGION)
    assert result == b'{"key": "value"}'
    meta = get_object_metadata(BUCKET, "data.json", region_name=REGION)
    assert meta["content_type"] == "application/json"


def test_upload_fileobj_runtime_error(monkeypatch):
    import io
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.s3 as s3mod

    mock_client = MagicMock()
    mock_client.upload_fileobj.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "not found"}},
        "UploadFileobj",
    )
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload fileobj"):
        upload_fileobj("noexist", "key", io.BytesIO(b"data"), region_name=REGION)


def test_list_object_versions_delete_markers(s3_client):
    """Delete markers appear as S3ObjectVersion with is_delete_marker=True."""
    s3_client.put_bucket_versioning(
        Bucket=BUCKET,
        VersioningConfiguration={"Status": "Enabled"},
    )
    s3_client.put_object(Bucket=BUCKET, Key="to-delete.txt", Body=b"v1")
    s3_client.delete_object(Bucket=BUCKET, Key="to-delete.txt")

    versions = list_object_versions(BUCKET, region_name=REGION)
    markers = [v for v in versions if v.is_delete_marker]
    assert len(markers) >= 1
    assert markers[0].key == "to-delete.txt"


def test_list_object_versions_pagination(s3_client, monkeypatch):
    """Pagination loop continues when IsTruncated is True."""
    import aws_util.s3 as s3mod
    from unittest.mock import MagicMock

    page1 = {
        "IsTruncated": True,
        "Versions": [
            {"Key": "a.txt", "VersionId": "v1", "IsLatest": True},
        ],
        "DeleteMarkers": [],
        "NextKeyMarker": "a.txt",
        "NextVersionIdMarker": "v1",
    }
    page2 = {
        "IsTruncated": False,
        "Versions": [
            {"Key": "b.txt", "VersionId": "v2", "IsLatest": True},
        ],
        "DeleteMarkers": [],
    }
    mock_client = MagicMock()
    mock_client.list_object_versions.side_effect = [page1, page2]
    monkeypatch.setattr(s3mod, "get_client", lambda *a, **kw: mock_client)

    versions = list_object_versions(BUCKET, region_name=REGION)
    assert len(versions) == 2
    assert versions[0].key == "a.txt"
    assert versions[1].key == "b.txt"
    assert mock_client.list_object_versions.call_count == 2


def test_abort_multipart_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.abort_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    abort_multipart_upload("test-bucket", "test-key", "test-upload_id", region_name=REGION)
    mock_client.abort_multipart_upload.assert_called_once()


def test_abort_multipart_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.abort_multipart_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "abort_multipart_upload",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to abort multipart upload"):
        abort_multipart_upload("test-bucket", "test-key", "test-upload_id", region_name=REGION)


def test_complete_multipart_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    complete_multipart_upload("test-bucket", "test-key", "test-upload_id", region_name=REGION)
    mock_client.complete_multipart_upload.assert_called_once()


def test_complete_multipart_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_multipart_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "complete_multipart_upload",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete multipart upload"):
        complete_multipart_upload("test-bucket", "test-key", "test-upload_id", region_name=REGION)


def test_create_bucket(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket("test-bucket", region_name=REGION)
    mock_client.create_bucket.assert_called_once()


def test_create_bucket_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bucket",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create bucket"):
        create_bucket("test-bucket", region_name=REGION)


def test_create_bucket_metadata_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket_metadata_configuration("test-bucket", {}, region_name=REGION)
    mock_client.create_bucket_metadata_configuration.assert_called_once()


def test_create_bucket_metadata_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bucket_metadata_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create bucket metadata configuration"):
        create_bucket_metadata_configuration("test-bucket", {}, region_name=REGION)


def test_create_bucket_metadata_table_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket_metadata_table_configuration("test-bucket", {}, region_name=REGION)
    mock_client.create_bucket_metadata_table_configuration.assert_called_once()


def test_create_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_table_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bucket_metadata_table_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create bucket metadata table configuration"):
        create_bucket_metadata_table_configuration("test-bucket", {}, region_name=REGION)


def test_create_multipart_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_multipart_upload("test-bucket", "test-key", region_name=REGION)
    mock_client.create_multipart_upload.assert_called_once()


def test_create_multipart_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_multipart_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_multipart_upload",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create multipart upload"):
        create_multipart_upload("test-bucket", "test-key", region_name=REGION)


def test_create_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_session("test-bucket", region_name=REGION)
    mock_client.create_session.assert_called_once()


def test_create_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_session",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create session"):
        create_session("test-bucket", region_name=REGION)


def test_delete_bucket(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket("test-bucket", region_name=REGION)
    mock_client.delete_bucket.assert_called_once()


def test_delete_bucket_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket"):
        delete_bucket("test-bucket", region_name=REGION)


def test_delete_bucket_analytics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_analytics_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.delete_bucket_analytics_configuration.assert_called_once()


def test_delete_bucket_analytics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_analytics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_analytics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket analytics configuration"):
        delete_bucket_analytics_configuration("test-bucket", "test-id", region_name=REGION)


def test_delete_bucket_cors(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_cors("test-bucket", region_name=REGION)
    mock_client.delete_bucket_cors.assert_called_once()


def test_delete_bucket_cors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_cors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_cors",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket cors"):
        delete_bucket_cors("test-bucket", region_name=REGION)


def test_delete_bucket_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_encryption("test-bucket", region_name=REGION)
    mock_client.delete_bucket_encryption.assert_called_once()


def test_delete_bucket_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_encryption",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket encryption"):
        delete_bucket_encryption("test-bucket", region_name=REGION)


def test_delete_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.delete_bucket_intelligent_tiering_configuration.assert_called_once()


def test_delete_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_intelligent_tiering_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_intelligent_tiering_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket intelligent tiering configuration"):
        delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", region_name=REGION)


def test_delete_bucket_inventory_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_inventory_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.delete_bucket_inventory_configuration.assert_called_once()


def test_delete_bucket_inventory_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_inventory_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_inventory_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket inventory configuration"):
        delete_bucket_inventory_configuration("test-bucket", "test-id", region_name=REGION)


def test_delete_bucket_lifecycle(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_lifecycle("test-bucket", region_name=REGION)
    mock_client.delete_bucket_lifecycle.assert_called_once()


def test_delete_bucket_lifecycle_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_lifecycle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_lifecycle",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket lifecycle"):
        delete_bucket_lifecycle("test-bucket", region_name=REGION)


def test_delete_bucket_metadata_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metadata_configuration("test-bucket", region_name=REGION)
    mock_client.delete_bucket_metadata_configuration.assert_called_once()


def test_delete_bucket_metadata_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_metadata_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket metadata configuration"):
        delete_bucket_metadata_configuration("test-bucket", region_name=REGION)


def test_delete_bucket_metadata_table_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metadata_table_configuration("test-bucket", region_name=REGION)
    mock_client.delete_bucket_metadata_table_configuration.assert_called_once()


def test_delete_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_table_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_metadata_table_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket metadata table configuration"):
        delete_bucket_metadata_table_configuration("test-bucket", region_name=REGION)


def test_delete_bucket_metrics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metrics_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.delete_bucket_metrics_configuration.assert_called_once()


def test_delete_bucket_metrics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_metrics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_metrics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket metrics configuration"):
        delete_bucket_metrics_configuration("test-bucket", "test-id", region_name=REGION)


def test_delete_bucket_ownership_controls(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_ownership_controls("test-bucket", region_name=REGION)
    mock_client.delete_bucket_ownership_controls.assert_called_once()


def test_delete_bucket_ownership_controls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_ownership_controls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_ownership_controls",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket ownership controls"):
        delete_bucket_ownership_controls("test-bucket", region_name=REGION)


def test_delete_bucket_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_policy("test-bucket", region_name=REGION)
    mock_client.delete_bucket_policy.assert_called_once()


def test_delete_bucket_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_policy",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket policy"):
        delete_bucket_policy("test-bucket", region_name=REGION)


def test_delete_bucket_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_replication("test-bucket", region_name=REGION)
    mock_client.delete_bucket_replication.assert_called_once()


def test_delete_bucket_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_replication",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket replication"):
        delete_bucket_replication("test-bucket", region_name=REGION)


def test_delete_bucket_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_tagging("test-bucket", region_name=REGION)
    mock_client.delete_bucket_tagging.assert_called_once()


def test_delete_bucket_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket tagging"):
        delete_bucket_tagging("test-bucket", region_name=REGION)


def test_delete_bucket_website(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_website("test-bucket", region_name=REGION)
    mock_client.delete_bucket_website.assert_called_once()


def test_delete_bucket_website_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bucket_website.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_website",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bucket website"):
        delete_bucket_website("test-bucket", region_name=REGION)


def test_delete_object_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_object_tagging("test-bucket", "test-key", region_name=REGION)
    mock_client.delete_object_tagging.assert_called_once()


def test_delete_object_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_object_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_object_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete object tagging"):
        delete_object_tagging("test-bucket", "test-key", region_name=REGION)


def test_delete_objects(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_objects.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_objects("test-bucket", {}, region_name=REGION)
    mock_client.delete_objects.assert_called_once()


def test_delete_objects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_objects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_objects",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete objects"):
        delete_objects("test-bucket", {}, region_name=REGION)


def test_delete_public_access_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_public_access_block("test-bucket", region_name=REGION)
    mock_client.delete_public_access_block.assert_called_once()


def test_delete_public_access_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_access_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_public_access_block",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete public access block"):
        delete_public_access_block("test-bucket", region_name=REGION)


def test_get_bucket_accelerate_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_accelerate_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_accelerate_configuration("test-bucket", region_name=REGION)
    mock_client.get_bucket_accelerate_configuration.assert_called_once()


def test_get_bucket_accelerate_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_accelerate_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_accelerate_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket accelerate configuration"):
        get_bucket_accelerate_configuration("test-bucket", region_name=REGION)


def test_get_bucket_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_acl("test-bucket", region_name=REGION)
    mock_client.get_bucket_acl.assert_called_once()


def test_get_bucket_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_acl",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket acl"):
        get_bucket_acl("test-bucket", region_name=REGION)


def test_get_bucket_analytics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_analytics_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.get_bucket_analytics_configuration.assert_called_once()


def test_get_bucket_analytics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_analytics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_analytics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket analytics configuration"):
        get_bucket_analytics_configuration("test-bucket", "test-id", region_name=REGION)


def test_get_bucket_cors(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_cors("test-bucket", region_name=REGION)
    mock_client.get_bucket_cors.assert_called_once()


def test_get_bucket_cors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_cors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_cors",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket cors"):
        get_bucket_cors("test-bucket", region_name=REGION)


def test_get_bucket_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_encryption("test-bucket", region_name=REGION)
    mock_client.get_bucket_encryption.assert_called_once()


def test_get_bucket_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_encryption",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket encryption"):
        get_bucket_encryption("test-bucket", region_name=REGION)


def test_get_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.get_bucket_intelligent_tiering_configuration.assert_called_once()


def test_get_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_intelligent_tiering_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_intelligent_tiering_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket intelligent tiering configuration"):
        get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", region_name=REGION)


def test_get_bucket_inventory_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_inventory_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.get_bucket_inventory_configuration.assert_called_once()


def test_get_bucket_inventory_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_inventory_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_inventory_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket inventory configuration"):
        get_bucket_inventory_configuration("test-bucket", "test-id", region_name=REGION)


def test_get_bucket_lifecycle(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_lifecycle("test-bucket", region_name=REGION)
    mock_client.get_bucket_lifecycle.assert_called_once()


def test_get_bucket_lifecycle_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_lifecycle",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket lifecycle"):
        get_bucket_lifecycle("test-bucket", region_name=REGION)


def test_get_bucket_lifecycle_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_lifecycle_configuration("test-bucket", region_name=REGION)
    mock_client.get_bucket_lifecycle_configuration.assert_called_once()


def test_get_bucket_lifecycle_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_lifecycle_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket lifecycle configuration"):
        get_bucket_lifecycle_configuration("test-bucket", region_name=REGION)


def test_get_bucket_location(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_location.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_location("test-bucket", region_name=REGION)
    mock_client.get_bucket_location.assert_called_once()


def test_get_bucket_location_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_location.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_location",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket location"):
        get_bucket_location("test-bucket", region_name=REGION)


def test_get_bucket_logging(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_logging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_logging("test-bucket", region_name=REGION)
    mock_client.get_bucket_logging.assert_called_once()


def test_get_bucket_logging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_logging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_logging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket logging"):
        get_bucket_logging("test-bucket", region_name=REGION)


def test_get_bucket_metadata_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metadata_configuration("test-bucket", region_name=REGION)
    mock_client.get_bucket_metadata_configuration.assert_called_once()


def test_get_bucket_metadata_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_metadata_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket metadata configuration"):
        get_bucket_metadata_configuration("test-bucket", region_name=REGION)


def test_get_bucket_metadata_table_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metadata_table_configuration("test-bucket", region_name=REGION)
    mock_client.get_bucket_metadata_table_configuration.assert_called_once()


def test_get_bucket_metadata_table_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_table_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_metadata_table_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket metadata table configuration"):
        get_bucket_metadata_table_configuration("test-bucket", region_name=REGION)


def test_get_bucket_metrics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metrics_configuration("test-bucket", "test-id", region_name=REGION)
    mock_client.get_bucket_metrics_configuration.assert_called_once()


def test_get_bucket_metrics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_metrics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_metrics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket metrics configuration"):
        get_bucket_metrics_configuration("test-bucket", "test-id", region_name=REGION)


def test_get_bucket_notification(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_notification.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_notification("test-bucket", region_name=REGION)
    mock_client.get_bucket_notification.assert_called_once()


def test_get_bucket_notification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_notification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_notification",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket notification"):
        get_bucket_notification("test-bucket", region_name=REGION)


def test_get_bucket_notification_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_notification_configuration("test-bucket", region_name=REGION)
    mock_client.get_bucket_notification_configuration.assert_called_once()


def test_get_bucket_notification_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_notification_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_notification_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket notification configuration"):
        get_bucket_notification_configuration("test-bucket", region_name=REGION)


def test_get_bucket_ownership_controls(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_ownership_controls("test-bucket", region_name=REGION)
    mock_client.get_bucket_ownership_controls.assert_called_once()


def test_get_bucket_ownership_controls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_ownership_controls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_ownership_controls",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket ownership controls"):
        get_bucket_ownership_controls("test-bucket", region_name=REGION)


def test_get_bucket_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_policy("test-bucket", region_name=REGION)
    mock_client.get_bucket_policy.assert_called_once()


def test_get_bucket_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_policy",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket policy"):
        get_bucket_policy("test-bucket", region_name=REGION)


def test_get_bucket_policy_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_policy_status.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_policy_status("test-bucket", region_name=REGION)
    mock_client.get_bucket_policy_status.assert_called_once()


def test_get_bucket_policy_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_policy_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_policy_status",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket policy status"):
        get_bucket_policy_status("test-bucket", region_name=REGION)


def test_get_bucket_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_replication("test-bucket", region_name=REGION)
    mock_client.get_bucket_replication.assert_called_once()


def test_get_bucket_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_replication",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket replication"):
        get_bucket_replication("test-bucket", region_name=REGION)


def test_get_bucket_request_payment(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_request_payment.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_request_payment("test-bucket", region_name=REGION)
    mock_client.get_bucket_request_payment.assert_called_once()


def test_get_bucket_request_payment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_request_payment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_request_payment",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket request payment"):
        get_bucket_request_payment("test-bucket", region_name=REGION)


def test_get_bucket_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_tagging("test-bucket", region_name=REGION)
    mock_client.get_bucket_tagging.assert_called_once()


def test_get_bucket_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket tagging"):
        get_bucket_tagging("test-bucket", region_name=REGION)


def test_get_bucket_versioning(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_versioning.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_versioning("test-bucket", region_name=REGION)
    mock_client.get_bucket_versioning.assert_called_once()


def test_get_bucket_versioning_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_versioning.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_versioning",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket versioning"):
        get_bucket_versioning("test-bucket", region_name=REGION)


def test_get_bucket_website(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_website("test-bucket", region_name=REGION)
    mock_client.get_bucket_website.assert_called_once()


def test_get_bucket_website_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_bucket_website.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_website",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get bucket website"):
        get_bucket_website("test-bucket", region_name=REGION)


def test_get_object_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_acl("test-bucket", "test-key", region_name=REGION)
    mock_client.get_object_acl.assert_called_once()


def test_get_object_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_acl",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object acl"):
        get_object_acl("test-bucket", "test-key", region_name=REGION)


def test_get_object_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_attributes.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_attributes("test-bucket", "test-key", [], region_name=REGION)
    mock_client.get_object_attributes.assert_called_once()


def test_get_object_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_attributes",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object attributes"):
        get_object_attributes("test-bucket", "test-key", [], region_name=REGION)


def test_get_object_legal_hold(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_legal_hold.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_legal_hold("test-bucket", "test-key", region_name=REGION)
    mock_client.get_object_legal_hold.assert_called_once()


def test_get_object_legal_hold_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_legal_hold.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_legal_hold",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object legal hold"):
        get_object_legal_hold("test-bucket", "test-key", region_name=REGION)


def test_get_object_lock_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_lock_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_lock_configuration("test-bucket", region_name=REGION)
    mock_client.get_object_lock_configuration.assert_called_once()


def test_get_object_lock_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_lock_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_lock_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object lock configuration"):
        get_object_lock_configuration("test-bucket", region_name=REGION)


def test_get_object_retention(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_retention.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_retention("test-bucket", "test-key", region_name=REGION)
    mock_client.get_object_retention.assert_called_once()


def test_get_object_retention_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_retention.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_retention",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object retention"):
        get_object_retention("test-bucket", "test-key", region_name=REGION)


def test_get_object_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_tagging("test-bucket", "test-key", region_name=REGION)
    mock_client.get_object_tagging.assert_called_once()


def test_get_object_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object tagging"):
        get_object_tagging("test-bucket", "test-key", region_name=REGION)


def test_get_object_torrent(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_torrent.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_torrent("test-bucket", "test-key", region_name=REGION)
    mock_client.get_object_torrent.assert_called_once()


def test_get_object_torrent_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_object_torrent.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_object_torrent",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get object torrent"):
        get_object_torrent("test-bucket", "test-key", region_name=REGION)


def test_get_public_access_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_public_access_block("test-bucket", region_name=REGION)
    mock_client.get_public_access_block.assert_called_once()


def test_get_public_access_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_public_access_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_public_access_block",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get public access block"):
        get_public_access_block("test-bucket", region_name=REGION)


def test_head_bucket(monkeypatch):
    mock_client = MagicMock()
    mock_client.head_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    head_bucket("test-bucket", region_name=REGION)
    mock_client.head_bucket.assert_called_once()


def test_head_bucket_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.head_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "head_bucket",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to head bucket"):
        head_bucket("test-bucket", region_name=REGION)


def test_head_object(monkeypatch):
    mock_client = MagicMock()
    mock_client.head_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    head_object("test-bucket", "test-key", region_name=REGION)
    mock_client.head_object.assert_called_once()


def test_head_object_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.head_object.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "head_object",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to head object"):
        head_object("test-bucket", "test-key", region_name=REGION)


def test_list_bucket_analytics_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_analytics_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_analytics_configurations("test-bucket", region_name=REGION)
    mock_client.list_bucket_analytics_configurations.assert_called_once()


def test_list_bucket_analytics_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_analytics_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bucket_analytics_configurations",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list bucket analytics configurations"):
        list_bucket_analytics_configurations("test-bucket", region_name=REGION)


def test_list_bucket_intelligent_tiering_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_intelligent_tiering_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_intelligent_tiering_configurations("test-bucket", region_name=REGION)
    mock_client.list_bucket_intelligent_tiering_configurations.assert_called_once()


def test_list_bucket_intelligent_tiering_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_intelligent_tiering_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bucket_intelligent_tiering_configurations",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list bucket intelligent tiering configurations"):
        list_bucket_intelligent_tiering_configurations("test-bucket", region_name=REGION)


def test_list_bucket_inventory_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_inventory_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_inventory_configurations("test-bucket", region_name=REGION)
    mock_client.list_bucket_inventory_configurations.assert_called_once()


def test_list_bucket_inventory_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_inventory_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bucket_inventory_configurations",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list bucket inventory configurations"):
        list_bucket_inventory_configurations("test-bucket", region_name=REGION)


def test_list_bucket_metrics_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_metrics_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_metrics_configurations("test-bucket", region_name=REGION)
    mock_client.list_bucket_metrics_configurations.assert_called_once()


def test_list_bucket_metrics_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bucket_metrics_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bucket_metrics_configurations",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list bucket metrics configurations"):
        list_bucket_metrics_configurations("test-bucket", region_name=REGION)


def test_list_buckets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_buckets.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_buckets(region_name=REGION)
    mock_client.list_buckets.assert_called_once()


def test_list_buckets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_buckets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_buckets",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list buckets"):
        list_buckets(region_name=REGION)


def test_list_directory_buckets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_directory_buckets.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_directory_buckets(region_name=REGION)
    mock_client.list_directory_buckets.assert_called_once()


def test_list_directory_buckets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_directory_buckets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_directory_buckets",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list directory buckets"):
        list_directory_buckets(region_name=REGION)


def test_list_multipart_uploads(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_multipart_uploads.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_multipart_uploads("test-bucket", region_name=REGION)
    mock_client.list_multipart_uploads.assert_called_once()


def test_list_multipart_uploads_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_multipart_uploads.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_multipart_uploads",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list multipart uploads"):
        list_multipart_uploads("test-bucket", region_name=REGION)


def test_list_objects_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_objects_v2.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_objects_v2("test-bucket", region_name=REGION)
    mock_client.list_objects_v2.assert_called_once()


def test_list_objects_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_objects_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_objects_v2",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list objects v2"):
        list_objects_v2("test-bucket", region_name=REGION)


def test_list_parts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_parts.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_parts("test-bucket", "test-key", "test-upload_id", region_name=REGION)
    mock_client.list_parts.assert_called_once()


def test_list_parts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_parts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_parts",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list parts"):
        list_parts("test-bucket", "test-key", "test-upload_id", region_name=REGION)


def test_put_bucket_accelerate_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_accelerate_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_accelerate_configuration("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_accelerate_configuration.assert_called_once()


def test_put_bucket_accelerate_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_accelerate_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_accelerate_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket accelerate configuration"):
        put_bucket_accelerate_configuration("test-bucket", {}, region_name=REGION)


def test_put_bucket_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_acl("test-bucket", region_name=REGION)
    mock_client.put_bucket_acl.assert_called_once()


def test_put_bucket_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_acl",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket acl"):
        put_bucket_acl("test-bucket", region_name=REGION)


def test_put_bucket_analytics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_analytics_configuration("test-bucket", "test-id", {}, region_name=REGION)
    mock_client.put_bucket_analytics_configuration.assert_called_once()


def test_put_bucket_analytics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_analytics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_analytics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket analytics configuration"):
        put_bucket_analytics_configuration("test-bucket", "test-id", {}, region_name=REGION)


def test_put_bucket_cors(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_cors("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_cors.assert_called_once()


def test_put_bucket_cors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_cors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_cors",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket cors"):
        put_bucket_cors("test-bucket", {}, region_name=REGION)


def test_put_bucket_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_encryption("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_encryption.assert_called_once()


def test_put_bucket_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_encryption",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket encryption"):
        put_bucket_encryption("test-bucket", {}, region_name=REGION)


def test_put_bucket_intelligent_tiering_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, region_name=REGION)
    mock_client.put_bucket_intelligent_tiering_configuration.assert_called_once()


def test_put_bucket_intelligent_tiering_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_intelligent_tiering_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_intelligent_tiering_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket intelligent tiering configuration"):
        put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, region_name=REGION)


def test_put_bucket_inventory_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_inventory_configuration("test-bucket", "test-id", {}, region_name=REGION)
    mock_client.put_bucket_inventory_configuration.assert_called_once()


def test_put_bucket_inventory_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_inventory_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_inventory_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket inventory configuration"):
        put_bucket_inventory_configuration("test-bucket", "test-id", {}, region_name=REGION)


def test_put_bucket_lifecycle(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_lifecycle("test-bucket", region_name=REGION)
    mock_client.put_bucket_lifecycle.assert_called_once()


def test_put_bucket_lifecycle_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_lifecycle",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket lifecycle"):
        put_bucket_lifecycle("test-bucket", region_name=REGION)


def test_put_bucket_lifecycle_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_lifecycle_configuration("test-bucket", region_name=REGION)
    mock_client.put_bucket_lifecycle_configuration.assert_called_once()


def test_put_bucket_lifecycle_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_lifecycle_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket lifecycle configuration"):
        put_bucket_lifecycle_configuration("test-bucket", region_name=REGION)


def test_put_bucket_logging(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_logging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_logging("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_logging.assert_called_once()


def test_put_bucket_logging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_logging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_logging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket logging"):
        put_bucket_logging("test-bucket", {}, region_name=REGION)


def test_put_bucket_metrics_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_metrics_configuration("test-bucket", "test-id", {}, region_name=REGION)
    mock_client.put_bucket_metrics_configuration.assert_called_once()


def test_put_bucket_metrics_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_metrics_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_metrics_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket metrics configuration"):
        put_bucket_metrics_configuration("test-bucket", "test-id", {}, region_name=REGION)


def test_put_bucket_notification(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_notification.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_notification("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_notification.assert_called_once()


def test_put_bucket_notification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_notification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_notification",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket notification"):
        put_bucket_notification("test-bucket", {}, region_name=REGION)


def test_put_bucket_notification_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_notification_configuration("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_notification_configuration.assert_called_once()


def test_put_bucket_notification_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_notification_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_notification_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket notification configuration"):
        put_bucket_notification_configuration("test-bucket", {}, region_name=REGION)


def test_put_bucket_ownership_controls(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_ownership_controls("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_ownership_controls.assert_called_once()


def test_put_bucket_ownership_controls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_ownership_controls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_ownership_controls",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket ownership controls"):
        put_bucket_ownership_controls("test-bucket", {}, region_name=REGION)


def test_put_bucket_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_policy("test-bucket", "test-policy", region_name=REGION)
    mock_client.put_bucket_policy.assert_called_once()


def test_put_bucket_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_policy",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket policy"):
        put_bucket_policy("test-bucket", "test-policy", region_name=REGION)


def test_put_bucket_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_replication("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_replication.assert_called_once()


def test_put_bucket_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_replication",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket replication"):
        put_bucket_replication("test-bucket", {}, region_name=REGION)


def test_put_bucket_request_payment(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_request_payment.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_request_payment("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_request_payment.assert_called_once()


def test_put_bucket_request_payment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_request_payment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_request_payment",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket request payment"):
        put_bucket_request_payment("test-bucket", {}, region_name=REGION)


def test_put_bucket_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_tagging("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_tagging.assert_called_once()


def test_put_bucket_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket tagging"):
        put_bucket_tagging("test-bucket", {}, region_name=REGION)


def test_put_bucket_versioning(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_versioning.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_versioning("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_versioning.assert_called_once()


def test_put_bucket_versioning_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_versioning.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_versioning",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket versioning"):
        put_bucket_versioning("test-bucket", {}, region_name=REGION)


def test_put_bucket_website(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_website("test-bucket", {}, region_name=REGION)
    mock_client.put_bucket_website.assert_called_once()


def test_put_bucket_website_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_bucket_website.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_bucket_website",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put bucket website"):
        put_bucket_website("test-bucket", {}, region_name=REGION)


def test_put_object(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object("test-bucket", "test-key", region_name=REGION)
    mock_client.put_object.assert_called_once()


def test_put_object_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object"):
        put_object("test-bucket", "test-key", region_name=REGION)


def test_put_object_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_acl("test-bucket", "test-key", region_name=REGION)
    mock_client.put_object_acl.assert_called_once()


def test_put_object_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object_acl",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object acl"):
        put_object_acl("test-bucket", "test-key", region_name=REGION)


def test_put_object_legal_hold(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_legal_hold.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_legal_hold("test-bucket", "test-key", region_name=REGION)
    mock_client.put_object_legal_hold.assert_called_once()


def test_put_object_legal_hold_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_legal_hold.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object_legal_hold",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object legal hold"):
        put_object_legal_hold("test-bucket", "test-key", region_name=REGION)


def test_put_object_lock_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_lock_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_lock_configuration("test-bucket", region_name=REGION)
    mock_client.put_object_lock_configuration.assert_called_once()


def test_put_object_lock_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_lock_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object_lock_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object lock configuration"):
        put_object_lock_configuration("test-bucket", region_name=REGION)


def test_put_object_retention(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_retention.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_retention("test-bucket", "test-key", region_name=REGION)
    mock_client.put_object_retention.assert_called_once()


def test_put_object_retention_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_retention.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object_retention",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object retention"):
        put_object_retention("test-bucket", "test-key", region_name=REGION)


def test_put_object_tagging(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_tagging("test-bucket", "test-key", {}, region_name=REGION)
    mock_client.put_object_tagging.assert_called_once()


def test_put_object_tagging_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_object_tagging.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_object_tagging",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put object tagging"):
        put_object_tagging("test-bucket", "test-key", {}, region_name=REGION)


def test_put_public_access_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_public_access_block("test-bucket", {}, region_name=REGION)
    mock_client.put_public_access_block.assert_called_once()


def test_put_public_access_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_public_access_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_public_access_block",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put public access block"):
        put_public_access_block("test-bucket", {}, region_name=REGION)


def test_rename_object(monkeypatch):
    mock_client = MagicMock()
    mock_client.rename_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    rename_object("test-bucket", "test-key", "test-rename_source", region_name=REGION)
    mock_client.rename_object.assert_called_once()


def test_rename_object_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rename_object.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rename_object",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rename object"):
        rename_object("test-bucket", "test-key", "test-rename_source", region_name=REGION)


def test_restore_object(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    restore_object("test-bucket", "test-key", region_name=REGION)
    mock_client.restore_object.assert_called_once()


def test_restore_object_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_object.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_object",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore object"):
        restore_object("test-bucket", "test-key", region_name=REGION)


def test_select_object_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_object_content.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", {}, {}, region_name=REGION)
    mock_client.select_object_content.assert_called_once()


def test_select_object_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_object_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "select_object_content",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to select object content"):
        select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", {}, {}, region_name=REGION)


def test_update_bucket_metadata_inventory_table_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_inventory_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    update_bucket_metadata_inventory_table_configuration("test-bucket", {}, region_name=REGION)
    mock_client.update_bucket_metadata_inventory_table_configuration.assert_called_once()


def test_update_bucket_metadata_inventory_table_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_inventory_table_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bucket_metadata_inventory_table_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update bucket metadata inventory table configuration"):
        update_bucket_metadata_inventory_table_configuration("test-bucket", {}, region_name=REGION)


def test_update_bucket_metadata_journal_table_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_journal_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    update_bucket_metadata_journal_table_configuration("test-bucket", {}, region_name=REGION)
    mock_client.update_bucket_metadata_journal_table_configuration.assert_called_once()


def test_update_bucket_metadata_journal_table_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_journal_table_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bucket_metadata_journal_table_configuration",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update bucket metadata journal table configuration"):
        update_bucket_metadata_journal_table_configuration("test-bucket", {}, region_name=REGION)


def test_upload_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_part.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    upload_part("test-bucket", "test-key", 1, "test-upload_id", region_name=REGION)
    mock_client.upload_part.assert_called_once()


def test_upload_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_part",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload part"):
        upload_part("test-bucket", "test-key", 1, "test-upload_id", region_name=REGION)


def test_upload_part_copy(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_part_copy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    upload_part_copy("test-bucket", "test-copy_source", "test-key", 1, "test-upload_id", region_name=REGION)
    mock_client.upload_part_copy.assert_called_once()


def test_upload_part_copy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_part_copy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_part_copy",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload part copy"):
        upload_part_copy("test-bucket", "test-copy_source", "test-key", 1, "test-upload_id", region_name=REGION)


def test_write_get_object_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.write_get_object_response.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    write_get_object_response("test-request_route", "test-request_token", region_name=REGION)
    mock_client.write_get_object_response.assert_called_once()


def test_write_get_object_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.write_get_object_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "write_get_object_response",
    )
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to write get object response"):
        write_get_object_response("test-request_route", "test-request_token", region_name=REGION)


def test_get_object_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object
    mock_client = MagicMock()
    mock_client.get_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object("test-bucket", "test-key", version_id="test-version_id", region_name="us-east-1")
    mock_client.get_object.assert_called_once()

def test_abort_multipart_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import abort_multipart_upload
    mock_client = MagicMock()
    mock_client.abort_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    abort_multipart_upload("test-bucket", "test-key", "test-upload_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", if_match_initiated_time="test-if_match_initiated_time", region_name="us-east-1")
    mock_client.abort_multipart_upload.assert_called_once()

def test_complete_multipart_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import complete_multipart_upload
    mock_client = MagicMock()
    mock_client.complete_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    complete_multipart_upload("test-bucket", "test-key", "test-upload_id", multipart_upload=True, checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", checksum_type="test-checksum_type", mpu_object_size=1, request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", if_match="test-if_match", if_none_match="test-if_none_match", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", region_name="us-east-1")
    mock_client.complete_multipart_upload.assert_called_once()

def test_create_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import create_bucket
    mock_client = MagicMock()
    mock_client.create_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket("test-bucket", acl="test-acl", create_bucket_configuration={}, grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", object_lock_enabled_for_bucket="test-object_lock_enabled_for_bucket", object_ownership="test-object_ownership", region_name="us-east-1")
    mock_client.create_bucket.assert_called_once()

def test_create_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import create_bucket_metadata_configuration
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket_metadata_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.create_bucket_metadata_configuration.assert_called_once()

def test_create_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import create_bucket_metadata_table_configuration
    mock_client = MagicMock()
    mock_client.create_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_bucket_metadata_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.create_bucket_metadata_table_configuration.assert_called_once()

def test_create_multipart_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import create_multipart_upload
    mock_client = MagicMock()
    mock_client.create_multipart_upload.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_multipart_upload("test-bucket", "test-key", acl="test-acl", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_type="test-content_type", expires="test-expires", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write_acp="test-grant_write_acp", metadata="test-metadata", server_side_encryption="test-server_side_encryption", storage_class="test-storage_class", website_redirect_location="test-website_redirect_location", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", request_payer="test-request_payer", tagging="test-tagging", object_lock_mode="test-object_lock_mode", object_lock_retain_until_date="test-object_lock_retain_until_date", object_lock_legal_hold_status="test-object_lock_legal_hold_status", expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", checksum_type="test-checksum_type", region_name="us-east-1")
    mock_client.create_multipart_upload.assert_called_once()

def test_create_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import create_session
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    create_session("test-bucket", session_mode="test-session_mode", server_side_encryption="test-server_side_encryption", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", region_name="us-east-1")
    mock_client.create_session.assert_called_once()

def test_delete_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket
    mock_client = MagicMock()
    mock_client.delete_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket.assert_called_once()

def test_delete_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_analytics_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_analytics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_analytics_configuration.assert_called_once()

def test_delete_bucket_cors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_cors
    mock_client = MagicMock()
    mock_client.delete_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_cors("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_cors.assert_called_once()

def test_delete_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_encryption
    mock_client = MagicMock()
    mock_client.delete_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_encryption("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_encryption.assert_called_once()

def test_delete_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_intelligent_tiering_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_intelligent_tiering_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_intelligent_tiering_configuration.assert_called_once()

def test_delete_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_inventory_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_inventory_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_inventory_configuration.assert_called_once()

def test_delete_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_lifecycle
    mock_client = MagicMock()
    mock_client.delete_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_lifecycle("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_lifecycle.assert_called_once()

def test_delete_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_metadata_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metadata_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_metadata_configuration.assert_called_once()

def test_delete_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_metadata_table_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metadata_table_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_metadata_table_configuration.assert_called_once()

def test_delete_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_metrics_configuration
    mock_client = MagicMock()
    mock_client.delete_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_metrics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_metrics_configuration.assert_called_once()

def test_delete_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_ownership_controls
    mock_client = MagicMock()
    mock_client.delete_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_ownership_controls("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_ownership_controls.assert_called_once()

def test_delete_bucket_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_policy
    mock_client = MagicMock()
    mock_client.delete_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_policy("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_policy.assert_called_once()

def test_delete_bucket_replication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_replication
    mock_client = MagicMock()
    mock_client.delete_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_replication("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_replication.assert_called_once()

def test_delete_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_tagging
    mock_client = MagicMock()
    mock_client.delete_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_tagging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_tagging.assert_called_once()

def test_delete_bucket_website_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_bucket_website
    mock_client = MagicMock()
    mock_client.delete_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_bucket_website("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_bucket_website.assert_called_once()

def test_delete_object_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_object_tagging
    mock_client = MagicMock()
    mock_client.delete_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_object_tagging("test-bucket", "test-key", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_object_tagging.assert_called_once()

def test_delete_objects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_objects
    mock_client = MagicMock()
    mock_client.delete_objects.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_objects("test-bucket", True, mfa="test-mfa", request_payer="test-request_payer", bypass_governance_retention=True, expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.delete_objects.assert_called_once()

def test_delete_public_access_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import delete_public_access_block
    mock_client = MagicMock()
    mock_client.delete_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    delete_public_access_block("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.delete_public_access_block.assert_called_once()

def test_get_bucket_accelerate_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_accelerate_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_accelerate_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_accelerate_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.get_bucket_accelerate_configuration.assert_called_once()

def test_get_bucket_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_acl
    mock_client = MagicMock()
    mock_client.get_bucket_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_acl("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_acl.assert_called_once()

def test_get_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_analytics_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_analytics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_analytics_configuration.assert_called_once()

def test_get_bucket_cors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_cors
    mock_client = MagicMock()
    mock_client.get_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_cors("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_cors.assert_called_once()

def test_get_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_encryption
    mock_client = MagicMock()
    mock_client.get_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_encryption("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_encryption.assert_called_once()

def test_get_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_intelligent_tiering_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_intelligent_tiering_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_intelligent_tiering_configuration.assert_called_once()

def test_get_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_inventory_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_inventory_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_inventory_configuration.assert_called_once()

def test_get_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_lifecycle
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_lifecycle("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_lifecycle.assert_called_once()

def test_get_bucket_lifecycle_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_lifecycle_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_lifecycle_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_lifecycle_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_lifecycle_configuration.assert_called_once()

def test_get_bucket_location_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_location
    mock_client = MagicMock()
    mock_client.get_bucket_location.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_location("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_location.assert_called_once()

def test_get_bucket_logging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_logging
    mock_client = MagicMock()
    mock_client.get_bucket_logging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_logging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_logging.assert_called_once()

def test_get_bucket_metadata_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_metadata_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metadata_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_metadata_configuration.assert_called_once()

def test_get_bucket_metadata_table_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_metadata_table_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_metadata_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metadata_table_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_metadata_table_configuration.assert_called_once()

def test_get_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_metrics_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_metrics_configuration("test-bucket", "test-id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_metrics_configuration.assert_called_once()

def test_get_bucket_notification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_notification
    mock_client = MagicMock()
    mock_client.get_bucket_notification.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_notification("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_notification.assert_called_once()

def test_get_bucket_notification_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_notification_configuration
    mock_client = MagicMock()
    mock_client.get_bucket_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_notification_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_notification_configuration.assert_called_once()

def test_get_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_ownership_controls
    mock_client = MagicMock()
    mock_client.get_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_ownership_controls("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_ownership_controls.assert_called_once()

def test_get_bucket_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_policy
    mock_client = MagicMock()
    mock_client.get_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_policy("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_policy.assert_called_once()

def test_get_bucket_policy_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_policy_status
    mock_client = MagicMock()
    mock_client.get_bucket_policy_status.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_policy_status("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_policy_status.assert_called_once()

def test_get_bucket_replication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_replication
    mock_client = MagicMock()
    mock_client.get_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_replication("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_replication.assert_called_once()

def test_get_bucket_request_payment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_request_payment
    mock_client = MagicMock()
    mock_client.get_bucket_request_payment.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_request_payment("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_request_payment.assert_called_once()

def test_get_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_tagging
    mock_client = MagicMock()
    mock_client.get_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_tagging("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_tagging.assert_called_once()

def test_get_bucket_versioning_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_versioning
    mock_client = MagicMock()
    mock_client.get_bucket_versioning.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_versioning("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_versioning.assert_called_once()

def test_get_bucket_website_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_bucket_website
    mock_client = MagicMock()
    mock_client.get_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_bucket_website("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_bucket_website.assert_called_once()

def test_get_object_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_acl
    mock_client = MagicMock()
    mock_client.get_object_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_acl("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_acl.assert_called_once()

def test_get_object_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_attributes
    mock_client = MagicMock()
    mock_client.get_object_attributes.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_attributes("test-bucket", "test-key", "test-object_attributes", version_id="test-version_id", max_parts=1, part_number_marker="test-part_number_marker", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_attributes.assert_called_once()

def test_get_object_legal_hold_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_legal_hold
    mock_client = MagicMock()
    mock_client.get_object_legal_hold.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_legal_hold("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_legal_hold.assert_called_once()

def test_get_object_lock_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_lock_configuration
    mock_client = MagicMock()
    mock_client.get_object_lock_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_lock_configuration("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_lock_configuration.assert_called_once()

def test_get_object_retention_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_retention
    mock_client = MagicMock()
    mock_client.get_object_retention.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_retention("test-bucket", "test-key", version_id="test-version_id", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_retention.assert_called_once()

def test_get_object_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_tagging
    mock_client = MagicMock()
    mock_client.get_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_tagging("test-bucket", "test-key", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.get_object_tagging.assert_called_once()

def test_get_object_torrent_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_object_torrent
    mock_client = MagicMock()
    mock_client.get_object_torrent.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_object_torrent("test-bucket", "test-key", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_object_torrent.assert_called_once()

def test_get_public_access_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import get_public_access_block
    mock_client = MagicMock()
    mock_client.get_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    get_public_access_block("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.get_public_access_block.assert_called_once()

def test_head_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import head_bucket
    mock_client = MagicMock()
    mock_client.head_bucket.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    head_bucket("test-bucket", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.head_bucket.assert_called_once()

def test_head_object_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import head_object
    mock_client = MagicMock()
    mock_client.head_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    head_object("test-bucket", "test-key", if_match="test-if_match", if_modified_since="test-if_modified_since", if_none_match="test-if_none_match", if_unmodified_since="test-if_unmodified_since", range="test-range", response_cache_control="test-response_cache_control", response_content_disposition="test-response_content_disposition", response_content_encoding="test-response_content_encoding", response_content_language="test-response_content_language", response_content_type="test-response_content_type", response_expires="test-response_expires", version_id="test-version_id", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", part_number="test-part_number", expected_bucket_owner="test-expected_bucket_owner", checksum_mode="test-checksum_mode", region_name="us-east-1")
    mock_client.head_object.assert_called_once()

def test_list_bucket_analytics_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_bucket_analytics_configurations
    mock_client = MagicMock()
    mock_client.list_bucket_analytics_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_analytics_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.list_bucket_analytics_configurations.assert_called_once()

def test_list_bucket_intelligent_tiering_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_bucket_intelligent_tiering_configurations
    mock_client = MagicMock()
    mock_client.list_bucket_intelligent_tiering_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_intelligent_tiering_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.list_bucket_intelligent_tiering_configurations.assert_called_once()

def test_list_bucket_inventory_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_bucket_inventory_configurations
    mock_client = MagicMock()
    mock_client.list_bucket_inventory_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_inventory_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.list_bucket_inventory_configurations.assert_called_once()

def test_list_bucket_metrics_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_bucket_metrics_configurations
    mock_client = MagicMock()
    mock_client.list_bucket_metrics_configurations.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_bucket_metrics_configurations("test-bucket", continuation_token="test-continuation_token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.list_bucket_metrics_configurations.assert_called_once()

def test_list_buckets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_buckets
    mock_client = MagicMock()
    mock_client.list_buckets.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_buckets(max_buckets=1, continuation_token="test-continuation_token", prefix="test-prefix", bucket_region="test-bucket_region", region_name="us-east-1")
    mock_client.list_buckets.assert_called_once()

def test_list_directory_buckets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_directory_buckets
    mock_client = MagicMock()
    mock_client.list_directory_buckets.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_directory_buckets(continuation_token="test-continuation_token", max_directory_buckets=1, region_name="us-east-1")
    mock_client.list_directory_buckets.assert_called_once()

def test_list_multipart_uploads_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_multipart_uploads
    mock_client = MagicMock()
    mock_client.list_multipart_uploads.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_multipart_uploads("test-bucket", delimiter=1, encoding_type="test-encoding_type", key_marker="test-key_marker", max_uploads=1, prefix="test-prefix", upload_id_marker="test-upload_id_marker", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.list_multipart_uploads.assert_called_once()

def test_list_objects_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_objects_v2
    mock_client = MagicMock()
    mock_client.list_objects_v2.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_objects_v2("test-bucket", delimiter=1, encoding_type="test-encoding_type", max_keys=1, prefix="test-prefix", continuation_token="test-continuation_token", fetch_owner="test-fetch_owner", start_after="test-start_after", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", optional_object_attributes="test-optional_object_attributes", region_name="us-east-1")
    mock_client.list_objects_v2.assert_called_once()

def test_list_parts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import list_parts
    mock_client = MagicMock()
    mock_client.list_parts.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    list_parts("test-bucket", "test-key", "test-upload_id", max_parts=1, part_number_marker="test-part_number_marker", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", region_name="us-east-1")
    mock_client.list_parts.assert_called_once()

def test_put_bucket_accelerate_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_accelerate_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_accelerate_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_accelerate_configuration("test-bucket", {}, expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.put_bucket_accelerate_configuration.assert_called_once()

def test_put_bucket_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_acl
    mock_client = MagicMock()
    mock_client.put_bucket_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_acl("test-bucket", acl="test-acl", access_control_policy="{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_acl.assert_called_once()

def test_put_bucket_analytics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_analytics_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_analytics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_analytics_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_analytics_configuration.assert_called_once()

def test_put_bucket_cors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_cors
    mock_client = MagicMock()
    mock_client.put_bucket_cors.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_cors("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_cors.assert_called_once()

def test_put_bucket_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_encryption
    mock_client = MagicMock()
    mock_client.put_bucket_encryption.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_encryption("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_encryption.assert_called_once()

def test_put_bucket_intelligent_tiering_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_intelligent_tiering_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_intelligent_tiering_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_intelligent_tiering_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_intelligent_tiering_configuration.assert_called_once()

def test_put_bucket_inventory_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_inventory_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_inventory_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_inventory_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_inventory_configuration.assert_called_once()

def test_put_bucket_lifecycle_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_lifecycle
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_lifecycle("test-bucket", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", lifecycle_configuration={}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_lifecycle.assert_called_once()

def test_put_bucket_lifecycle_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_lifecycle_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_lifecycle_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_lifecycle_configuration("test-bucket", checksum_algorithm="test-checksum_algorithm", lifecycle_configuration={}, expected_bucket_owner="test-expected_bucket_owner", transition_default_minimum_object_size=1, region_name="us-east-1")
    mock_client.put_bucket_lifecycle_configuration.assert_called_once()

def test_put_bucket_logging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_logging
    mock_client = MagicMock()
    mock_client.put_bucket_logging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_logging("test-bucket", "test-bucket_logging_status", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_logging.assert_called_once()

def test_put_bucket_metrics_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_metrics_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_metrics_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_metrics_configuration("test-bucket", "test-id", {}, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_metrics_configuration.assert_called_once()

def test_put_bucket_notification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_notification
    mock_client = MagicMock()
    mock_client.put_bucket_notification.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_notification("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_notification.assert_called_once()

def test_put_bucket_notification_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_notification_configuration
    mock_client = MagicMock()
    mock_client.put_bucket_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_notification_configuration("test-bucket", {}, expected_bucket_owner="test-expected_bucket_owner", skip_destination_validation=True, region_name="us-east-1")
    mock_client.put_bucket_notification_configuration.assert_called_once()

def test_put_bucket_ownership_controls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_ownership_controls
    mock_client = MagicMock()
    mock_client.put_bucket_ownership_controls.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_ownership_controls("test-bucket", "test-ownership_controls", content_md5="test-content_md5", expected_bucket_owner="test-expected_bucket_owner", checksum_algorithm="test-checksum_algorithm", region_name="us-east-1")
    mock_client.put_bucket_ownership_controls.assert_called_once()

def test_put_bucket_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_policy
    mock_client = MagicMock()
    mock_client.put_bucket_policy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_policy("test-bucket", "{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", confirm_remove_self_bucket_access=True, expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_policy.assert_called_once()

def test_put_bucket_replication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_replication
    mock_client = MagicMock()
    mock_client.put_bucket_replication.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_replication("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", token="test-token", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_replication.assert_called_once()

def test_put_bucket_request_payment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_request_payment
    mock_client = MagicMock()
    mock_client.put_bucket_request_payment.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_request_payment("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_request_payment.assert_called_once()

def test_put_bucket_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_tagging
    mock_client = MagicMock()
    mock_client.put_bucket_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_tagging("test-bucket", "test-tagging", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_tagging.assert_called_once()

def test_put_bucket_versioning_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_versioning
    mock_client = MagicMock()
    mock_client.put_bucket_versioning.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_versioning("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", mfa="test-mfa", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_versioning.assert_called_once()

def test_put_bucket_website_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_bucket_website
    mock_client = MagicMock()
    mock_client.put_bucket_website.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_bucket_website("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_bucket_website.assert_called_once()

def test_put_object_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object
    mock_client = MagicMock()
    mock_client.put_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object("test-bucket", "test-key", acl="test-acl", body="test-body", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_length="test-content_length", content_md5="test-content_md5", content_type="test-content_type", checksum_algorithm="test-checksum_algorithm", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", expires="test-expires", if_match="test-if_match", if_none_match="test-if_none_match", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write_acp="test-grant_write_acp", write_offset_bytes="test-write_offset_bytes", metadata="test-metadata", server_side_encryption="test-server_side_encryption", storage_class="test-storage_class", website_redirect_location="test-website_redirect_location", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", ssekms_key_id="test-ssekms_key_id", ssekms_encryption_context={}, bucket_key_enabled="test-bucket_key_enabled", request_payer="test-request_payer", tagging="test-tagging", object_lock_mode="test-object_lock_mode", object_lock_retain_until_date="test-object_lock_retain_until_date", object_lock_legal_hold_status="test-object_lock_legal_hold_status", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_object.assert_called_once()

def test_put_object_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object_acl
    mock_client = MagicMock()
    mock_client.put_object_acl.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_acl("test-bucket", "test-key", acl="test-acl", access_control_policy="{}", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", grant_full_control="test-grant_full_control", grant_read="test-grant_read", grant_read_acp="test-grant_read_acp", grant_write="test-grant_write", grant_write_acp="test-grant_write_acp", request_payer="test-request_payer", version_id="test-version_id", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_object_acl.assert_called_once()

def test_put_object_legal_hold_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object_legal_hold
    mock_client = MagicMock()
    mock_client.put_object_legal_hold.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_legal_hold("test-bucket", "test-key", legal_hold="test-legal_hold", request_payer="test-request_payer", version_id="test-version_id", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_object_legal_hold.assert_called_once()

def test_put_object_lock_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object_lock_configuration
    mock_client = MagicMock()
    mock_client.put_object_lock_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_lock_configuration("test-bucket", object_lock_configuration={}, request_payer="test-request_payer", token="test-token", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_object_lock_configuration.assert_called_once()

def test_put_object_retention_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object_retention
    mock_client = MagicMock()
    mock_client.put_object_retention.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_retention("test-bucket", "test-key", retention="test-retention", request_payer="test-request_payer", version_id="test-version_id", bypass_governance_retention=True, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_object_retention.assert_called_once()

def test_put_object_tagging_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_object_tagging
    mock_client = MagicMock()
    mock_client.put_object_tagging.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_object_tagging("test-bucket", "test-key", "test-tagging", version_id="test-version_id", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", request_payer="test-request_payer", region_name="us-east-1")
    mock_client.put_object_tagging.assert_called_once()

def test_put_public_access_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import put_public_access_block
    mock_client = MagicMock()
    mock_client.put_public_access_block.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    put_public_access_block("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.put_public_access_block.assert_called_once()

def test_rename_object_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import rename_object
    mock_client = MagicMock()
    mock_client.rename_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    rename_object("test-bucket", "test-key", "test-rename_source", destination_if_match="test-destination_if_match", destination_if_none_match="test-destination_if_none_match", destination_if_modified_since="test-destination_if_modified_since", destination_if_unmodified_since="test-destination_if_unmodified_since", source_if_match="test-source_if_match", source_if_none_match="test-source_if_none_match", source_if_modified_since="test-source_if_modified_since", source_if_unmodified_since="test-source_if_unmodified_since", client_token="test-client_token", region_name="us-east-1")
    mock_client.rename_object.assert_called_once()

def test_restore_object_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import restore_object
    mock_client = MagicMock()
    mock_client.restore_object.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    restore_object("test-bucket", "test-key", version_id="test-version_id", restore_request="test-restore_request", request_payer="test-request_payer", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.restore_object.assert_called_once()

def test_select_object_content_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import select_object_content
    mock_client = MagicMock()
    mock_client.select_object_content.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    select_object_content("test-bucket", "test-key", "test-expression", "test-expression_type", "test-input_serialization", "test-output_serialization", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_progress="test-request_progress", scan_range="test-scan_range", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.select_object_content.assert_called_once()

def test_update_bucket_metadata_inventory_table_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import update_bucket_metadata_inventory_table_configuration
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_inventory_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    update_bucket_metadata_inventory_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.update_bucket_metadata_inventory_table_configuration.assert_called_once()

def test_update_bucket_metadata_journal_table_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import update_bucket_metadata_journal_table_configuration
    mock_client = MagicMock()
    mock_client.update_bucket_metadata_journal_table_configuration.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    update_bucket_metadata_journal_table_configuration("test-bucket", {}, content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.update_bucket_metadata_journal_table_configuration.assert_called_once()

def test_upload_part_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import upload_part
    mock_client = MagicMock()
    mock_client.upload_part.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    upload_part("test-bucket", "test-key", "test-part_number", "test-upload_id", body="test-body", content_length="test-content_length", content_md5="test-content_md5", checksum_algorithm="test-checksum_algorithm", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", region_name="us-east-1")
    mock_client.upload_part.assert_called_once()

def test_upload_part_copy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import upload_part_copy
    mock_client = MagicMock()
    mock_client.upload_part_copy.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    upload_part_copy("test-bucket", "test-copy_source", "test-key", "test-part_number", "test-upload_id", copy_source_if_match="test-copy_source_if_match", copy_source_if_modified_since="test-copy_source_if_modified_since", copy_source_if_none_match="test-copy_source_if_none_match", copy_source_if_unmodified_since="test-copy_source_if_unmodified_since", copy_source_range="test-copy_source_range", sse_customer_algorithm="test-sse_customer_algorithm", sse_customer_key="test-sse_customer_key", sse_customer_key_md5="test-sse_customer_key_md5", copy_source_sse_customer_algorithm="test-copy_source_sse_customer_algorithm", copy_source_sse_customer_key="test-copy_source_sse_customer_key", copy_source_sse_customer_key_md5="test-copy_source_sse_customer_key_md5", request_payer="test-request_payer", expected_bucket_owner="test-expected_bucket_owner", expected_source_bucket_owner="test-expected_source_bucket_owner", region_name="us-east-1")
    mock_client.upload_part_copy.assert_called_once()

def test_write_get_object_response_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.s3 import write_get_object_response
    mock_client = MagicMock()
    mock_client.write_get_object_response.return_value = {}
    monkeypatch.setattr("aws_util.s3.get_client", lambda *a, **kw: mock_client)
    write_get_object_response("test-request_route", "test-request_token", body="test-body", status_code="test-status_code", error_code="test-error_code", error_message="test-error_message", accept_ranges="test-accept_ranges", cache_control="test-cache_control", content_disposition="test-content_disposition", content_encoding="test-content_encoding", content_language="test-content_language", content_length="test-content_length", content_range="test-content_range", content_type="test-content_type", checksum_crc32="test-checksum_crc32", checksum_crc32_c="test-checksum_crc32_c", checksum_crc64_nvme="test-checksum_crc64_nvme", checksum_sha1="test-checksum_sha1", checksum_sha256="test-checksum_sha256", delete_marker=True, e_tag="test-e_tag", expires="test-expires", expiration="test-expiration", last_modified="test-last_modified", missing_meta="test-missing_meta", metadata="test-metadata", object_lock_mode="test-object_lock_mode", object_lock_legal_hold_status="test-object_lock_legal_hold_status", object_lock_retain_until_date="test-object_lock_retain_until_date", parts_count=1, replication_status="test-replication_status", request_charged="test-request_charged", restore="test-restore", server_side_encryption="test-server_side_encryption", sse_customer_algorithm="test-sse_customer_algorithm", ssekms_key_id="test-ssekms_key_id", sse_customer_key_md5="test-sse_customer_key_md5", storage_class="test-storage_class", tag_count=1, version_id="test-version_id", bucket_key_enabled="test-bucket_key_enabled", region_name="us-east-1")
    mock_client.write_get_object_response.assert_called_once()
