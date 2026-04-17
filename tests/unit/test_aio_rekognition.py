from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.rekognition import (
    BoundingBox,
    FaceMatch,
    RekognitionFace,
    RekognitionLabel,
    RekognitionText,
    _bbox,
    _resolve_image,
    compare_faces,
    create_collection,
    delete_collection,
    detect_faces,
    detect_labels,
    detect_moderation_labels,
    detect_text,
    ensure_collection,
    index_face,
    search_face_by_image,
    associate_faces,
    copy_project_version,
    create_dataset,
    create_face_liveness_session,
    create_project,
    create_project_version,
    create_stream_processor,
    create_user,
    delete_dataset,
    delete_faces,
    delete_project,
    delete_project_policy,
    delete_project_version,
    delete_stream_processor,
    delete_user,
    describe_collection,
    describe_dataset,
    describe_project_versions,
    describe_projects,
    describe_stream_processor,
    detect_custom_labels,
    detect_protective_equipment,
    disassociate_faces,
    distribute_dataset_entries,
    get_celebrity_info,
    get_celebrity_recognition,
    get_content_moderation,
    get_face_detection,
    get_face_liveness_session_results,
    get_face_search,
    get_label_detection,
    get_media_analysis_job,
    get_person_tracking,
    get_segment_detection,
    get_text_detection,
    index_faces,
    list_collections,
    list_dataset_entries,
    list_dataset_labels,
    list_faces,
    list_media_analysis_jobs,
    list_project_policies,
    list_stream_processors,
    list_tags_for_resource,
    list_users,
    put_project_policy,
    recognize_celebrities,
    search_faces,
    search_faces_by_image,
    search_users,
    search_users_by_image,
    start_celebrity_recognition,
    start_content_moderation,
    start_face_detection,
    start_face_search,
    start_label_detection,
    start_media_analysis_job,
    start_person_tracking,
    start_project_version,
    start_segment_detection,
    start_stream_processor,
    start_text_detection,
    stop_project_version,
    stop_stream_processor,
    tag_resource,
    untag_resource,
    update_dataset_entries,
    update_stream_processor,
)


# ---------------------------------------------------------------------------
# _resolve_image helper
# ---------------------------------------------------------------------------


def test_resolve_image_bytes() -> None:
    result = _resolve_image(b"img", None, None)
    assert result == {"Bytes": b"img"}


def test_resolve_image_s3() -> None:
    result = _resolve_image(None, "bucket", "key")
    assert result == {"S3Object": {"Bucket": "bucket", "Name": "key"}}


def test_resolve_image_missing() -> None:
    with pytest.raises(ValueError, match="Provide either"):
        _resolve_image(None, None, None)


def test_resolve_image_partial_s3() -> None:
    with pytest.raises(ValueError, match="Provide either"):
        _resolve_image(None, "bucket", None)


# ---------------------------------------------------------------------------
# _bbox helper
# ---------------------------------------------------------------------------


def test_bbox_full() -> None:
    bb = _bbox({"Width": 0.5, "Height": 0.6, "Left": 0.1, "Top": 0.2})
    assert isinstance(bb, BoundingBox)
    assert bb.width == 0.5
    assert bb.height == 0.6


def test_bbox_defaults() -> None:
    bb = _bbox({})
    assert bb.width == 0.0
    assert bb.height == 0.0
    assert bb.left == 0.0
    assert bb.top == 0.0


# ---------------------------------------------------------------------------
# detect_labels
# ---------------------------------------------------------------------------


async def test_detect_labels_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Labels": [
            {
                "Name": "Dog",
                "Confidence": 99.5,
                "Parents": [{"Name": "Animal"}],
            },
            {
                "Name": "Cat",
                "Confidence": 85.0,
                "Parents": [],
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_labels(image_bytes=b"img")
    assert len(result) == 2
    assert result[0].name == "Dog"
    assert result[0].parents == ["Animal"]


async def test_detect_labels_s3(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Labels": []}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_labels(s3_bucket="b", s3_key="k")
    assert result == []


async def test_detect_labels_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="detect_labels failed"):
        await detect_labels(image_bytes=b"img")


# ---------------------------------------------------------------------------
# detect_faces
# ---------------------------------------------------------------------------


async def test_detect_faces_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceDetails": [
            {
                "BoundingBox": {
                    "Width": 0.3,
                    "Height": 0.4,
                    "Left": 0.1,
                    "Top": 0.2,
                },
                "Confidence": 99.0,
                "AgeRange": {"Low": 20, "High": 30},
                "Smile": {"Value": True},
                "Eyeglasses": {"Value": False},
                "Sunglasses": {"Value": True},
                "Gender": {"Value": "Male"},
                "Emotions": [{"Type": "HAPPY", "Confidence": 90.0}],
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_faces(image_bytes=b"img", attributes=["ALL"])
    assert len(result) == 1
    assert result[0].bounding_box is not None
    assert result[0].confidence == 99.0
    assert result[0].age_range_low == 20
    assert result[0].smile is True
    assert result[0].gender == "Male"


async def test_detect_faces_no_bounding_box(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceDetails": [{"Confidence": 80.0}]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_faces(image_bytes=b"img")
    assert result[0].bounding_box is None
    assert result[0].age_range_low is None
    assert result[0].smile is None


async def test_detect_faces_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="detect_faces failed"):
        await detect_faces(image_bytes=b"img")


# ---------------------------------------------------------------------------
# detect_text
# ---------------------------------------------------------------------------


async def test_detect_text_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TextDetections": [
            {
                "DetectedText": "Hello",
                "Type": "LINE",
                "Confidence": 99.0,
                "Geometry": {
                    "BoundingBox": {
                        "Width": 0.5,
                        "Height": 0.1,
                        "Left": 0.1,
                        "Top": 0.2,
                    }
                },
            },
            {
                "DetectedText": "World",
                "Type": "WORD",
                "Confidence": 95.0,
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_text(image_bytes=b"img")
    assert len(result) == 2
    assert result[0].detected_text == "Hello"
    assert result[0].bounding_box is not None
    assert result[1].bounding_box is None


async def test_detect_text_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="detect_text failed"):
        await detect_text(image_bytes=b"img")


# ---------------------------------------------------------------------------
# compare_faces
# ---------------------------------------------------------------------------


async def test_compare_faces_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceMatches": [
            {
                "Similarity": 95.0,
                "Face": {
                    "BoundingBox": {
                        "Width": 0.3,
                        "Height": 0.4,
                        "Left": 0.1,
                        "Top": 0.2,
                    }
                },
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await compare_faces(b"src", b"tgt")
    assert len(result) == 1
    assert result[0].similarity == 95.0
    assert result[0].bounding_box is not None


async def test_compare_faces_no_bbox(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceMatches": [
            {"Similarity": 90.0, "Face": {}},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await compare_faces(b"src", b"tgt")
    assert result[0].bounding_box is None


async def test_compare_faces_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="compare_faces failed"):
        await compare_faces(b"src", b"tgt")


# ---------------------------------------------------------------------------
# detect_moderation_labels
# ---------------------------------------------------------------------------


async def test_detect_moderation_labels_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ModerationLabels": [
            {
                "Name": "Violence",
                "Confidence": 80.0,
                "ParentName": "Unsafe",
            },
            {
                "Name": "Safe",
                "Confidence": 95.0,
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await detect_moderation_labels(image_bytes=b"img")
    assert len(result) == 2
    assert result[0].parents == ["Unsafe"]
    assert result[1].parents == []


async def test_detect_moderation_labels_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="detect_moderation_labels failed"):
        await detect_moderation_labels(image_bytes=b"img")


# ---------------------------------------------------------------------------
# create_collection
# ---------------------------------------------------------------------------


async def test_create_collection_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "CollectionArn": "arn:aws:rekognition:us-east-1:123:collection/test"
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_collection("test")
    assert result == "arn:aws:rekognition:us-east-1:123:collection/test"


async def test_create_collection_no_arn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_collection("test")
    assert result == ""


async def test_create_collection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to create collection"):
        await create_collection("test")


# ---------------------------------------------------------------------------
# index_face
# ---------------------------------------------------------------------------


async def test_index_face_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceRecords": [{"Face": {"FaceId": "face-1"}}]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await index_face("col-1", image_bytes=b"img")
    assert result == "face-1"


async def test_index_face_with_external_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceRecords": [{"Face": {"FaceId": "face-2"}}]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await index_face(
        "col-1",
        s3_bucket="b",
        s3_key="k",
        external_image_id="user-123",
    )
    assert result == "face-2"


async def test_index_face_no_face_detected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"FaceRecords": []}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="No face detected"):
        await index_face("col-1", image_bytes=b"img")


async def test_index_face_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="index_face failed"):
        await index_face("col-1", image_bytes=b"img")


# ---------------------------------------------------------------------------
# search_face_by_image
# ---------------------------------------------------------------------------


async def test_search_face_by_image_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FaceMatches": [
            {
                "Face": {
                    "FaceId": "face-1",
                    "ExternalImageId": "user-1",
                    "Confidence": 99.0,
                },
                "Similarity": 95.0,
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await search_face_by_image("col-1", image_bytes=b"img")
    assert len(result) == 1
    assert result[0]["face_id"] == "face-1"
    assert result[0]["external_image_id"] == "user-1"
    assert result[0]["similarity"] == 95.0


async def test_search_face_by_image_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"FaceMatches": []}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await search_face_by_image("col-1", image_bytes=b"img")
    assert result == []


async def test_search_face_by_image_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="search_face_by_image failed"):
        await search_face_by_image("col-1", image_bytes=b"img")


# ---------------------------------------------------------------------------
# delete_collection
# ---------------------------------------------------------------------------


async def test_delete_collection_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_collection("col-1")


async def test_delete_collection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to delete collection"):
        await delete_collection("col-1")


# ---------------------------------------------------------------------------
# ensure_collection
# ---------------------------------------------------------------------------


async def test_ensure_collection_exists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "CollectionARN": "arn:aws:rekognition:us-east-1:123:collection/test"
    }
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    arn, created = await ensure_collection("test")
    assert arn == "arn:aws:rekognition:us-east-1:123:collection/test"
    assert created is False


async def test_ensure_collection_creates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    # First call (DescribeCollection) raises ResourceNotFoundException
    # Second call (CreateCollection) succeeds
    mock_client.call.side_effect = [
        RuntimeError("ResourceNotFoundException"),
        {"CollectionArn": "arn:aws:rekognition:us-east-1:123:collection/new"},
    ]
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    arn, created = await ensure_collection("new")
    assert created is True
    assert "new" in arn


async def test_ensure_collection_other_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDeniedException")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="ensure_collection failed"):
        await ensure_collection("test")


async def test_associate_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_faces("test-collection_id", "test-user_id", [], )
    mock_client.call.assert_called_once()


async def test_associate_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_faces("test-collection_id", "test-user_id", [], )


async def test_copy_project_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, )
    mock_client.call.assert_called_once()


async def test_copy_project_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, )


async def test_create_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dataset("test-dataset_type", "test-project_arn", )
    mock_client.call.assert_called_once()


async def test_create_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dataset("test-dataset_type", "test-project_arn", )


async def test_create_face_liveness_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_face_liveness_session()
    mock_client.call.assert_called_once()


async def test_create_face_liveness_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_face_liveness_session()


async def test_create_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_project("test-project_name", )
    mock_client.call.assert_called_once()


async def test_create_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_project("test-project_name", )


async def test_create_project_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_project_version("test-project_arn", "test-version_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_project_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_project_version("test-project_arn", "test-version_name", {}, )


async def test_create_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stream_processor({}, {}, "test-name", {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stream_processor({}, {}, "test-name", {}, "test-role_arn", )


async def test_create_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user("test-collection_id", "test-user_id", )
    mock_client.call.assert_called_once()


async def test_create_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user("test-collection_id", "test-user_id", )


async def test_delete_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset("test-dataset_arn", )


async def test_delete_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_faces("test-collection_id", [], )
    mock_client.call.assert_called_once()


async def test_delete_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_faces("test-collection_id", [], )


async def test_delete_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_project("test-project_arn", )
    mock_client.call.assert_called_once()


async def test_delete_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_project("test-project_arn", )


async def test_delete_project_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_project_policy("test-project_arn", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_project_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_project_policy("test-project_arn", "test-policy_name", )


async def test_delete_project_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_project_version("test-project_version_arn", )
    mock_client.call.assert_called_once()


async def test_delete_project_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_project_version("test-project_version_arn", )


async def test_delete_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stream_processor("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stream_processor("test-name", )


async def test_delete_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user("test-collection_id", "test-user_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user("test-collection_id", "test-user_id", )


async def test_describe_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_collection("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_describe_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_collection("test-collection_id", )


async def test_describe_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset("test-dataset_arn", )


async def test_describe_project_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_project_versions("test-project_arn", )
    mock_client.call.assert_called_once()


async def test_describe_project_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_project_versions("test-project_arn", )


async def test_describe_projects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_projects()
    mock_client.call.assert_called_once()


async def test_describe_projects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_projects()


async def test_describe_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stream_processor("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stream_processor("test-name", )


async def test_detect_custom_labels(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await detect_custom_labels("test-project_version_arn", {}, )
    mock_client.call.assert_called_once()


async def test_detect_custom_labels_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detect_custom_labels("test-project_version_arn", {}, )


async def test_detect_protective_equipment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await detect_protective_equipment({}, )
    mock_client.call.assert_called_once()


async def test_detect_protective_equipment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detect_protective_equipment({}, )


async def test_disassociate_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_faces("test-collection_id", "test-user_id", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_faces("test-collection_id", "test-user_id", [], )


async def test_distribute_dataset_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await distribute_dataset_entries([], )
    mock_client.call.assert_called_once()


async def test_distribute_dataset_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await distribute_dataset_entries([], )


async def test_get_celebrity_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_celebrity_info("test-id", )
    mock_client.call.assert_called_once()


async def test_get_celebrity_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_celebrity_info("test-id", )


async def test_get_celebrity_recognition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_celebrity_recognition("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_celebrity_recognition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_celebrity_recognition("test-job_id", )


async def test_get_content_moderation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_content_moderation("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_content_moderation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_content_moderation("test-job_id", )


async def test_get_face_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_face_detection("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_face_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_face_detection("test-job_id", )


async def test_get_face_liveness_session_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_face_liveness_session_results("test-session_id", )
    mock_client.call.assert_called_once()


async def test_get_face_liveness_session_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_face_liveness_session_results("test-session_id", )


async def test_get_face_search(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_face_search("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_face_search_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_face_search("test-job_id", )


async def test_get_label_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_label_detection("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_label_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_label_detection("test-job_id", )


async def test_get_media_analysis_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_media_analysis_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_media_analysis_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_media_analysis_job("test-job_id", )


async def test_get_person_tracking(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_person_tracking("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_person_tracking_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_person_tracking("test-job_id", )


async def test_get_segment_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_segment_detection("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_segment_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_segment_detection("test-job_id", )


async def test_get_text_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_text_detection("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_text_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_text_detection("test-job_id", )


async def test_index_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await index_faces("test-collection_id", {}, )
    mock_client.call.assert_called_once()


async def test_index_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await index_faces("test-collection_id", {}, )


async def test_list_collections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_collections()
    mock_client.call.assert_called_once()


async def test_list_collections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_collections()


async def test_list_dataset_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_entries("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_list_dataset_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_entries("test-dataset_arn", )


async def test_list_dataset_labels(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_labels("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_list_dataset_labels_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_labels("test-dataset_arn", )


async def test_list_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_faces("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_list_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_faces("test-collection_id", )


async def test_list_media_analysis_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_media_analysis_jobs()
    mock_client.call.assert_called_once()


async def test_list_media_analysis_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_media_analysis_jobs()


async def test_list_project_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_project_policies("test-project_arn", )
    mock_client.call.assert_called_once()


async def test_list_project_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_project_policies("test-project_arn", )


async def test_list_stream_processors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stream_processors()
    mock_client.call.assert_called_once()


async def test_list_stream_processors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stream_processors()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_users("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_list_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_users("test-collection_id", )


async def test_put_project_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_project_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", )


async def test_recognize_celebrities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await recognize_celebrities({}, )
    mock_client.call.assert_called_once()


async def test_recognize_celebrities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await recognize_celebrities({}, )


async def test_search_faces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_faces("test-collection_id", "test-face_id", )
    mock_client.call.assert_called_once()


async def test_search_faces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_faces("test-collection_id", "test-face_id", )


async def test_search_faces_by_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_faces_by_image("test-collection_id", {}, )
    mock_client.call.assert_called_once()


async def test_search_faces_by_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_faces_by_image("test-collection_id", {}, )


async def test_search_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_users("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_search_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_users("test-collection_id", )


async def test_search_users_by_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_users_by_image("test-collection_id", {}, )
    mock_client.call.assert_called_once()


async def test_search_users_by_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_users_by_image("test-collection_id", {}, )


async def test_start_celebrity_recognition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_celebrity_recognition({}, )
    mock_client.call.assert_called_once()


async def test_start_celebrity_recognition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_celebrity_recognition({}, )


async def test_start_content_moderation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_content_moderation({}, )
    mock_client.call.assert_called_once()


async def test_start_content_moderation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_content_moderation({}, )


async def test_start_face_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_face_detection({}, )
    mock_client.call.assert_called_once()


async def test_start_face_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_face_detection({}, )


async def test_start_face_search(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_face_search({}, "test-collection_id", )
    mock_client.call.assert_called_once()


async def test_start_face_search_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_face_search({}, "test-collection_id", )


async def test_start_label_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_label_detection({}, )
    mock_client.call.assert_called_once()


async def test_start_label_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_label_detection({}, )


async def test_start_media_analysis_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_media_analysis_job({}, {}, {}, )
    mock_client.call.assert_called_once()


async def test_start_media_analysis_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_media_analysis_job({}, {}, {}, )


async def test_start_person_tracking(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_person_tracking({}, )
    mock_client.call.assert_called_once()


async def test_start_person_tracking_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_person_tracking({}, )


async def test_start_project_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_project_version("test-project_version_arn", 1, )
    mock_client.call.assert_called_once()


async def test_start_project_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_project_version("test-project_version_arn", 1, )


async def test_start_segment_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_segment_detection({}, [], )
    mock_client.call.assert_called_once()


async def test_start_segment_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_segment_detection({}, [], )


async def test_start_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_stream_processor("test-name", )
    mock_client.call.assert_called_once()


async def test_start_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_stream_processor("test-name", )


async def test_start_text_detection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_text_detection({}, )
    mock_client.call.assert_called_once()


async def test_start_text_detection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_text_detection({}, )


async def test_stop_project_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_project_version("test-project_version_arn", )
    mock_client.call.assert_called_once()


async def test_stop_project_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_project_version("test-project_version_arn", )


async def test_stop_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_stream_processor("test-name", )
    mock_client.call.assert_called_once()


async def test_stop_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_stream_processor("test-name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_dataset_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dataset_entries("test-dataset_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_dataset_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dataset_entries("test-dataset_arn", {}, )


async def test_update_stream_processor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stream_processor("test-name", )
    mock_client.call.assert_called_once()


async def test_update_stream_processor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rekognition.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stream_processor("test-name", )


@pytest.mark.asyncio
async def test_associate_faces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import associate_faces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await associate_faces("test-collection_id", "test-user_id", "test-face_ids", user_match_threshold="test-user_match_threshold", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_project_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import copy_project_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_dataset("test-dataset_type", "test-project_arn", dataset_source="test-dataset_source", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_face_liveness_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_face_liveness_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_face_liveness_session(kms_key_id="test-kms_key_id", settings={}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_project("test-project_name", feature="test-feature", auto_update=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_project_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_project_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_project_version("test-project_arn", "test-version_name", {}, training_data="test-training_data", testing_data="test-testing_data", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", version_description="test-version_description", feature_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stream_processor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_stream_processor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_stream_processor("test-input", "test-output", "test-name", {}, "test-role_arn", tags=[{"Key": "k", "Value": "v"}], notification_channel="test-notification_channel", kms_key_id="test-kms_key_id", regions_of_interest="test-regions_of_interest", data_sharing_preference="test-data_sharing_preference", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import create_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await create_user("test-collection_id", "test-user_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_project_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import delete_project_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await delete_project_policy("test-project_arn", "test-policy_name", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import delete_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await delete_user("test-collection_id", "test-user_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_project_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import describe_project_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await describe_project_versions("test-project_arn", version_names="test-version_names", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_projects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import describe_projects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await describe_projects(next_token="test-next_token", max_results=1, project_names="test-project_names", features="test-features", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detect_custom_labels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import detect_custom_labels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await detect_custom_labels("test-project_version_arn", "test-image", max_results=1, min_confidence="test-min_confidence", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detect_protective_equipment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import detect_protective_equipment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await detect_protective_equipment("test-image", summarization_attributes="test-summarization_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_faces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import disassociate_faces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await disassociate_faces("test-collection_id", "test-user_id", "test-face_ids", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_celebrity_recognition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_celebrity_recognition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_celebrity_recognition("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_content_moderation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_content_moderation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_content_moderation("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", aggregate_by="test-aggregate_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_face_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_face_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_face_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_face_search_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_face_search
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_face_search("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_label_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_label_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_label_detection("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", aggregate_by="test-aggregate_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_person_tracking_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_person_tracking
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_person_tracking("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_segment_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_segment_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_segment_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_text_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import get_text_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await get_text_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_index_faces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import index_faces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await index_faces("test-collection_id", "test-image", external_image_id="test-external_image_id", detection_attributes="test-detection_attributes", max_faces=1, quality_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_collections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_collections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_collections(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_dataset_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_dataset_entries("test-dataset_arn", contains_labels="test-contains_labels", labeled="test-labeled", source_ref_contains="test-source_ref_contains", has_errors="test-has_errors", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_labels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_dataset_labels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_dataset_labels("test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_faces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_faces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_faces("test-collection_id", next_token="test-next_token", max_results=1, user_id="test-user_id", face_ids="test-face_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_media_analysis_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_media_analysis_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_media_analysis_jobs(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_project_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_project_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_project_policies("test-project_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stream_processors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_stream_processors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_stream_processors(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import list_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await list_users("test-collection_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_project_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import put_project_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_faces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import search_faces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await search_faces("test-collection_id", "test-face_id", max_faces=1, face_match_threshold="test-face_match_threshold", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_faces_by_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import search_faces_by_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await search_faces_by_image("test-collection_id", "test-image", max_faces=1, face_match_threshold="test-face_match_threshold", quality_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import search_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await search_users("test-collection_id", user_id="test-user_id", face_id="test-face_id", user_match_threshold="test-user_match_threshold", max_users=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_users_by_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import search_users_by_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await search_users_by_image("test-collection_id", "test-image", user_match_threshold="test-user_match_threshold", max_users=1, quality_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_celebrity_recognition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_celebrity_recognition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_celebrity_recognition("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_content_moderation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_content_moderation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_content_moderation("test-video", min_confidence="test-min_confidence", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_face_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_face_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_face_detection("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", face_attributes="test-face_attributes", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_face_search_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_face_search
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_face_search("test-video", "test-collection_id", client_request_token="test-client_request_token", face_match_threshold="test-face_match_threshold", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_label_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_label_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_label_detection("test-video", client_request_token="test-client_request_token", min_confidence="test-min_confidence", notification_channel="test-notification_channel", job_tag="test-job_tag", features="test-features", settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_media_analysis_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_media_analysis_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_media_analysis_job({}, "test-input", {}, client_request_token="test-client_request_token", job_name="test-job_name", kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_person_tracking_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_person_tracking
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_person_tracking("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_project_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_project_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_project_version("test-project_version_arn", "test-min_inference_units", max_inference_units=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_segment_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_segment_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_segment_detection("test-video", "test-segment_types", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_stream_processor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_stream_processor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_stream_processor("test-name", start_selector="test-start_selector", stop_selector="test-stop_selector", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_text_detection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import start_text_detection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await start_text_detection("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stream_processor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rekognition import update_stream_processor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rekognition.async_client", lambda *a, **kw: mock_client)
    await update_stream_processor("test-name", settings_for_update={}, regions_of_interest_for_update="test-regions_of_interest_for_update", data_sharing_preference_for_update="test-data_sharing_preference_for_update", parameters_to_delete="test-parameters_to_delete", region_name="us-east-1")
    mock_client.call.assert_called_once()
