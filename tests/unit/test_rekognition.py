"""Tests for aws_util.rekognition module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.rekognition as rek_mod
from aws_util.rekognition import (
    BoundingBox,
    RekognitionLabel,
    RekognitionFace,
    RekognitionText,
    FaceMatch,
    detect_labels,
    detect_faces,
    detect_text,
    compare_faces,
    detect_moderation_labels,
    create_collection,
    index_face,
    search_face_by_image,
    delete_collection,
    ensure_collection,
    _resolve_image,
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

REGION = "us-east-1"
FAKE_IMAGE = b"\xff\xd8\xff\xe0" + b"\x00" * 100  # fake JPEG header


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def test_resolve_image_bytes():
    result = _resolve_image(FAKE_IMAGE, None, None)
    assert result == {"Bytes": FAKE_IMAGE}


def test_resolve_image_s3():
    result = _resolve_image(None, "my-bucket", "my-key")
    assert result == {"S3Object": {"Bucket": "my-bucket", "Name": "my-key"}}


def test_resolve_image_no_source_raises():
    with pytest.raises(ValueError, match="Provide either image_bytes"):
        _resolve_image(None, None, None)


def test_resolve_image_s3_missing_key_raises():
    with pytest.raises(ValueError):
        _resolve_image(None, "my-bucket", None)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_bounding_box_model():
    bb = BoundingBox(width=0.5, height=0.3, left=0.1, top=0.2)
    assert bb.width == 0.5


def _encode_unused_placeholder():
    pass  # _encode is not exported from rekognition module


def test_rekognition_label_model():
    lbl = RekognitionLabel(name="Car", confidence=99.5, parents=["Vehicle"])
    assert lbl.name == "Car"
    assert lbl.parents == ["Vehicle"]


def test_rekognition_face_model():
    face = RekognitionFace(confidence=99.0)
    assert face.gender is None


def test_rekognition_text_model():
    txt = RekognitionText(
        detected_text="Hello",
        text_type="LINE",
        confidence=95.0,
    )
    assert txt.detected_text == "Hello"


def test_face_match_model():
    fm = FaceMatch(similarity=92.5)
    assert fm.similarity == 92.5


# ---------------------------------------------------------------------------
# detect_labels
# ---------------------------------------------------------------------------

def test_detect_labels_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_labels.return_value = {
        "Labels": [
            {"Name": "Cat", "Confidence": 99.0, "Parents": []},
            {"Name": "Animal", "Confidence": 97.0, "Parents": []},
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_labels(image_bytes=FAKE_IMAGE, region_name=REGION)
    assert len(result) == 2
    assert all(isinstance(lbl, RekognitionLabel) for lbl in result)
    assert result[0].name == "Cat"


def test_detect_labels_s3(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_labels.return_value = {"Labels": []}
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_labels(s3_bucket="my-bucket", s3_key="img.jpg", region_name=REGION)
    assert result == []


def test_detect_labels_no_source_raises(monkeypatch):
    mock_client = MagicMock()
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(ValueError):
        detect_labels(region_name=REGION)


def test_detect_labels_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_labels.side_effect = ClientError(
        {"Error": {"Code": "InvalidImageException", "Message": "bad image"}}, "DetectLabels"
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_labels failed"):
        detect_labels(image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_faces
# ---------------------------------------------------------------------------

def test_detect_faces_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_faces.return_value = {
        "FaceDetails": [
            {
                "BoundingBox": {"Width": 0.5, "Height": 0.5, "Left": 0.1, "Top": 0.1},
                "Confidence": 99.9,
                "AgeRange": {"Low": 25, "High": 35},
                "Smile": {"Value": True},
                "Eyeglasses": {"Value": False},
                "Sunglasses": {"Value": False},
                "Gender": {"Value": "Male"},
                "Emotions": [],
            }
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_faces(image_bytes=FAKE_IMAGE, region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], RekognitionFace)
    assert result[0].gender == "Male"
    assert result[0].smile is True


def test_detect_faces_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_faces.side_effect = ClientError(
        {"Error": {"Code": "InvalidImageException", "Message": "bad image"}}, "DetectFaces"
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_faces failed"):
        detect_faces(image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_text
# ---------------------------------------------------------------------------

def test_detect_text_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_text.return_value = {
        "TextDetections": [
            {
                "DetectedText": "HELLO",
                "Type": "LINE",
                "Confidence": 99.5,
                "Geometry": {
                    "BoundingBox": {"Width": 0.5, "Height": 0.1, "Left": 0.0, "Top": 0.0}
                },
            }
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_text(image_bytes=FAKE_IMAGE, region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], RekognitionText)
    assert result[0].detected_text == "HELLO"


def test_detect_text_no_geometry(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_text.return_value = {
        "TextDetections": [
            {"DetectedText": "WORLD", "Type": "WORD", "Confidence": 90.0}
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_text(image_bytes=FAKE_IMAGE, region_name=REGION)
    assert result[0].bounding_box is None


def test_detect_text_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_text.side_effect = ClientError(
        {"Error": {"Code": "InvalidImageException", "Message": "bad image"}}, "DetectText"
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_text failed"):
        detect_text(image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# compare_faces
# ---------------------------------------------------------------------------

def test_compare_faces_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.compare_faces.return_value = {
        "FaceMatches": [
            {
                "Similarity": 95.0,
                "Face": {"BoundingBox": {"Width": 0.5, "Height": 0.5, "Left": 0.1, "Top": 0.1}},
            }
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = compare_faces(FAKE_IMAGE, FAKE_IMAGE, region_name=REGION)
    assert len(result) == 1
    assert result[0].similarity == 95.0


def test_compare_faces_no_match(monkeypatch):
    mock_client = MagicMock()
    mock_client.compare_faces.return_value = {"FaceMatches": []}
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = compare_faces(FAKE_IMAGE, FAKE_IMAGE, region_name=REGION)
    assert result == []


def test_compare_faces_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.compare_faces.side_effect = ClientError(
        {"Error": {"Code": "InvalidImageException", "Message": "bad image"}}, "CompareFaces"
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="compare_faces failed"):
        compare_faces(FAKE_IMAGE, FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_moderation_labels
# ---------------------------------------------------------------------------

def test_detect_moderation_labels_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_moderation_labels.return_value = {
        "ModerationLabels": [
            {"Name": "Suggestive", "Confidence": 75.0, "ParentName": "Explicit Nudity"},
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_moderation_labels(image_bytes=FAKE_IMAGE, region_name=REGION)
    assert len(result) == 1
    assert result[0].name == "Suggestive"
    assert result[0].parents == ["Explicit Nudity"]


def test_detect_moderation_labels_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_moderation_labels.side_effect = ClientError(
        {"Error": {"Code": "InvalidImageException", "Message": "bad image"}},
        "DetectModerationLabels",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_moderation_labels failed"):
        detect_moderation_labels(image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# create_collection / delete_collection
# ---------------------------------------------------------------------------

def test_create_collection_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_collection.return_value = {
        "CollectionArn": "arn:aws:rekognition:us-east-1:123:collection/test-coll"
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    arn = create_collection("test-coll", region_name=REGION)
    assert "test-coll" in arn


def test_create_collection_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_collection.side_effect = ClientError(
        {"Error": {"Code": "ResourceAlreadyExistsException", "Message": "exists"}},
        "CreateCollection",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create collection"):
        create_collection("existing-coll", region_name=REGION)


def test_delete_collection_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_collection.return_value = {"StatusCode": 200}
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    delete_collection("test-coll", region_name=REGION)
    mock_client.delete_collection.assert_called_once()


def test_delete_collection_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_collection.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DeleteCollection",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete collection"):
        delete_collection("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# index_face
# ---------------------------------------------------------------------------

def test_index_face_no_face_detected(monkeypatch):
    mock_client = MagicMock()
    mock_client.index_faces.return_value = {"FaceRecords": []}
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="No face detected"):
        index_face("test-coll", image_bytes=FAKE_IMAGE, region_name=REGION)


def test_index_face_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.index_faces.return_value = {
        "FaceRecords": [{"Face": {"FaceId": "face-abc-123"}}]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    face_id = index_face(
        "test-coll",
        image_bytes=FAKE_IMAGE,
        external_image_id="user123",
        region_name=REGION,
    )
    assert face_id == "face-abc-123"


def test_index_face_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.index_faces.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "collection not found"}},
        "IndexFaces",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="index_face failed"):
        index_face("nonexistent-coll", image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# search_face_by_image
# ---------------------------------------------------------------------------

def test_search_face_by_image_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces_by_image.return_value = {
        "FaceMatches": [
            {
                "Similarity": 98.0,
                "Face": {"FaceId": "face-123", "ExternalImageId": "user1", "Confidence": 99.0},
            }
        ]
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = search_face_by_image("test-coll", image_bytes=FAKE_IMAGE, region_name=REGION)
    assert len(result) == 1
    assert result[0]["face_id"] == "face-123"
    assert result[0]["similarity"] == 98.0


def test_search_face_by_image_no_match(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces_by_image.return_value = {"FaceMatches": []}
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    result = search_face_by_image("test-coll", image_bytes=FAKE_IMAGE, region_name=REGION)
    assert result == []


def test_search_face_by_image_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces_by_image.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "SearchFacesByImage",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="search_face_by_image failed"):
        search_face_by_image("nonexistent", image_bytes=FAKE_IMAGE, region_name=REGION)


# ---------------------------------------------------------------------------
# ensure_collection
# ---------------------------------------------------------------------------

def test_ensure_collection_existing(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_collection.return_value = {
        "CollectionARN": "arn:aws:rekognition:us-east-1:123:collection/test-coll"
    }
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    arn, created = ensure_collection("test-coll", region_name=REGION)
    assert created is False
    assert "test-coll" in arn


def test_ensure_collection_creates_new(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_collection.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DescribeCollection",
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    monkeypatch.setattr(
        rek_mod,
        "create_collection",
        lambda cid, region_name=None: "arn:aws:rekognition:us-east-1:123:collection/new-coll",
    )
    arn, created = ensure_collection("new-coll", region_name=REGION)
    assert created is True


def test_ensure_collection_other_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_collection.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "DescribeCollection"
    )
    monkeypatch.setattr(rek_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="ensure_collection failed"):
        ensure_collection("any-coll", region_name=REGION)


def test_associate_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    associate_faces("test-collection_id", "test-user_id", [], region_name=REGION)
    mock_client.associate_faces.assert_called_once()


def test_associate_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate faces"):
        associate_faces("test-collection_id", "test-user_id", [], region_name=REGION)


def test_copy_project_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, region_name=REGION)
    mock_client.copy_project_version.assert_called_once()


def test_copy_project_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_project_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_project_version",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy project version"):
        copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, region_name=REGION)


def test_create_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_dataset("test-dataset_type", "test-project_arn", region_name=REGION)
    mock_client.create_dataset.assert_called_once()


def test_create_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dataset",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dataset"):
        create_dataset("test-dataset_type", "test-project_arn", region_name=REGION)


def test_create_face_liveness_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_face_liveness_session.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_face_liveness_session(region_name=REGION)
    mock_client.create_face_liveness_session.assert_called_once()


def test_create_face_liveness_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_face_liveness_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_face_liveness_session",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create face liveness session"):
        create_face_liveness_session(region_name=REGION)


def test_create_project(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_project.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_project("test-project_name", region_name=REGION)
    mock_client.create_project.assert_called_once()


def test_create_project_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_project",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create project"):
        create_project("test-project_name", region_name=REGION)


def test_create_project_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_project_version("test-project_arn", "test-version_name", {}, region_name=REGION)
    mock_client.create_project_version.assert_called_once()


def test_create_project_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_project_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_project_version",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create project version"):
        create_project_version("test-project_arn", "test-version_name", {}, region_name=REGION)


def test_create_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_stream_processor({}, {}, "test-name", {}, "test-role_arn", region_name=REGION)
    mock_client.create_stream_processor.assert_called_once()


def test_create_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stream processor"):
        create_stream_processor({}, {}, "test-name", {}, "test-role_arn", region_name=REGION)


def test_create_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_user("test-collection_id", "test-user_id", region_name=REGION)
    mock_client.create_user.assert_called_once()


def test_create_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user"):
        create_user("test-collection_id", "test-user_id", region_name=REGION)


def test_delete_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_dataset("test-dataset_arn", region_name=REGION)
    mock_client.delete_dataset.assert_called_once()


def test_delete_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset"):
        delete_dataset("test-dataset_arn", region_name=REGION)


def test_delete_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_faces("test-collection_id", [], region_name=REGION)
    mock_client.delete_faces.assert_called_once()


def test_delete_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete faces"):
        delete_faces("test-collection_id", [], region_name=REGION)


def test_delete_project(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_project("test-project_arn", region_name=REGION)
    mock_client.delete_project.assert_called_once()


def test_delete_project_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_project",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete project"):
        delete_project("test-project_arn", region_name=REGION)


def test_delete_project_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project_policy.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_project_policy("test-project_arn", "test-policy_name", region_name=REGION)
    mock_client.delete_project_policy.assert_called_once()


def test_delete_project_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_project_policy",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete project policy"):
        delete_project_policy("test-project_arn", "test-policy_name", region_name=REGION)


def test_delete_project_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_project_version("test-project_version_arn", region_name=REGION)
    mock_client.delete_project_version.assert_called_once()


def test_delete_project_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_project_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_project_version",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete project version"):
        delete_project_version("test-project_version_arn", region_name=REGION)


def test_delete_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_stream_processor("test-name", region_name=REGION)
    mock_client.delete_stream_processor.assert_called_once()


def test_delete_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stream processor"):
        delete_stream_processor("test-name", region_name=REGION)


def test_delete_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_user("test-collection_id", "test-user_id", region_name=REGION)
    mock_client.delete_user.assert_called_once()


def test_delete_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        delete_user("test-collection_id", "test-user_id", region_name=REGION)


def test_describe_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_collection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_collection("test-collection_id", region_name=REGION)
    mock_client.describe_collection.assert_called_once()


def test_describe_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_collection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe collection"):
        describe_collection("test-collection_id", region_name=REGION)


def test_describe_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_dataset("test-dataset_arn", region_name=REGION)
    mock_client.describe_dataset.assert_called_once()


def test_describe_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        describe_dataset("test-dataset_arn", region_name=REGION)


def test_describe_project_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_project_versions.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_project_versions("test-project_arn", region_name=REGION)
    mock_client.describe_project_versions.assert_called_once()


def test_describe_project_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_project_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_project_versions",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe project versions"):
        describe_project_versions("test-project_arn", region_name=REGION)


def test_describe_projects(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_projects.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_projects(region_name=REGION)
    mock_client.describe_projects.assert_called_once()


def test_describe_projects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_projects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_projects",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe projects"):
        describe_projects(region_name=REGION)


def test_describe_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_stream_processor("test-name", region_name=REGION)
    mock_client.describe_stream_processor.assert_called_once()


def test_describe_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stream processor"):
        describe_stream_processor("test-name", region_name=REGION)


def test_detect_custom_labels(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_custom_labels.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    detect_custom_labels("test-project_version_arn", {}, region_name=REGION)
    mock_client.detect_custom_labels.assert_called_once()


def test_detect_custom_labels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_custom_labels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_custom_labels",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect custom labels"):
        detect_custom_labels("test-project_version_arn", {}, region_name=REGION)


def test_detect_protective_equipment(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_protective_equipment.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    detect_protective_equipment({}, region_name=REGION)
    mock_client.detect_protective_equipment.assert_called_once()


def test_detect_protective_equipment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_protective_equipment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_protective_equipment",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect protective equipment"):
        detect_protective_equipment({}, region_name=REGION)


def test_disassociate_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    disassociate_faces("test-collection_id", "test-user_id", [], region_name=REGION)
    mock_client.disassociate_faces.assert_called_once()


def test_disassociate_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate faces"):
        disassociate_faces("test-collection_id", "test-user_id", [], region_name=REGION)


def test_distribute_dataset_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.distribute_dataset_entries.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    distribute_dataset_entries([], region_name=REGION)
    mock_client.distribute_dataset_entries.assert_called_once()


def test_distribute_dataset_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.distribute_dataset_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "distribute_dataset_entries",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to distribute dataset entries"):
        distribute_dataset_entries([], region_name=REGION)


def test_get_celebrity_info(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_celebrity_info.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_celebrity_info("test-id", region_name=REGION)
    mock_client.get_celebrity_info.assert_called_once()


def test_get_celebrity_info_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_celebrity_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_celebrity_info",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get celebrity info"):
        get_celebrity_info("test-id", region_name=REGION)


def test_get_celebrity_recognition(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_celebrity_recognition.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_celebrity_recognition("test-job_id", region_name=REGION)
    mock_client.get_celebrity_recognition.assert_called_once()


def test_get_celebrity_recognition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_celebrity_recognition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_celebrity_recognition",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get celebrity recognition"):
        get_celebrity_recognition("test-job_id", region_name=REGION)


def test_get_content_moderation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_content_moderation.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_content_moderation("test-job_id", region_name=REGION)
    mock_client.get_content_moderation.assert_called_once()


def test_get_content_moderation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_content_moderation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_content_moderation",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get content moderation"):
        get_content_moderation("test-job_id", region_name=REGION)


def test_get_face_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_face_detection("test-job_id", region_name=REGION)
    mock_client.get_face_detection.assert_called_once()


def test_get_face_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_face_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get face detection"):
        get_face_detection("test-job_id", region_name=REGION)


def test_get_face_liveness_session_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_liveness_session_results.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_face_liveness_session_results("test-session_id", region_name=REGION)
    mock_client.get_face_liveness_session_results.assert_called_once()


def test_get_face_liveness_session_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_liveness_session_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_face_liveness_session_results",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get face liveness session results"):
        get_face_liveness_session_results("test-session_id", region_name=REGION)


def test_get_face_search(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_search.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_face_search("test-job_id", region_name=REGION)
    mock_client.get_face_search.assert_called_once()


def test_get_face_search_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_face_search.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_face_search",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get face search"):
        get_face_search("test-job_id", region_name=REGION)


def test_get_label_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_label_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_label_detection("test-job_id", region_name=REGION)
    mock_client.get_label_detection.assert_called_once()


def test_get_label_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_label_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_label_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get label detection"):
        get_label_detection("test-job_id", region_name=REGION)


def test_get_media_analysis_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_media_analysis_job.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_media_analysis_job("test-job_id", region_name=REGION)
    mock_client.get_media_analysis_job.assert_called_once()


def test_get_media_analysis_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_media_analysis_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_media_analysis_job",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get media analysis job"):
        get_media_analysis_job("test-job_id", region_name=REGION)


def test_get_person_tracking(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_person_tracking.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_person_tracking("test-job_id", region_name=REGION)
    mock_client.get_person_tracking.assert_called_once()


def test_get_person_tracking_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_person_tracking.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_person_tracking",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get person tracking"):
        get_person_tracking("test-job_id", region_name=REGION)


def test_get_segment_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_segment_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_segment_detection("test-job_id", region_name=REGION)
    mock_client.get_segment_detection.assert_called_once()


def test_get_segment_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_segment_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_segment_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get segment detection"):
        get_segment_detection("test-job_id", region_name=REGION)


def test_get_text_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_text_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_text_detection("test-job_id", region_name=REGION)
    mock_client.get_text_detection.assert_called_once()


def test_get_text_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_text_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_text_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get text detection"):
        get_text_detection("test-job_id", region_name=REGION)


def test_index_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.index_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    index_faces("test-collection_id", {}, region_name=REGION)
    mock_client.index_faces.assert_called_once()


def test_index_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.index_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "index_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to index faces"):
        index_faces("test-collection_id", {}, region_name=REGION)


def test_list_collections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_collections.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_collections(region_name=REGION)
    mock_client.list_collections.assert_called_once()


def test_list_collections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_collections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_collections",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list collections"):
        list_collections(region_name=REGION)


def test_list_dataset_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_entries.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_dataset_entries("test-dataset_arn", region_name=REGION)
    mock_client.list_dataset_entries.assert_called_once()


def test_list_dataset_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_entries",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset entries"):
        list_dataset_entries("test-dataset_arn", region_name=REGION)


def test_list_dataset_labels(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_labels.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_dataset_labels("test-dataset_arn", region_name=REGION)
    mock_client.list_dataset_labels.assert_called_once()


def test_list_dataset_labels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_labels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_labels",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset labels"):
        list_dataset_labels("test-dataset_arn", region_name=REGION)


def test_list_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_faces("test-collection_id", region_name=REGION)
    mock_client.list_faces.assert_called_once()


def test_list_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list faces"):
        list_faces("test-collection_id", region_name=REGION)


def test_list_media_analysis_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_media_analysis_jobs.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_media_analysis_jobs(region_name=REGION)
    mock_client.list_media_analysis_jobs.assert_called_once()


def test_list_media_analysis_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_media_analysis_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_media_analysis_jobs",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list media analysis jobs"):
        list_media_analysis_jobs(region_name=REGION)


def test_list_project_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_project_policies.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_project_policies("test-project_arn", region_name=REGION)
    mock_client.list_project_policies.assert_called_once()


def test_list_project_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_project_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_project_policies",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list project policies"):
        list_project_policies("test-project_arn", region_name=REGION)


def test_list_stream_processors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stream_processors.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_stream_processors(region_name=REGION)
    mock_client.list_stream_processors.assert_called_once()


def test_list_stream_processors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stream_processors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stream_processors",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stream processors"):
        list_stream_processors(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_users.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_users("test-collection_id", region_name=REGION)
    mock_client.list_users.assert_called_once()


def test_list_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_users",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list users"):
        list_users("test-collection_id", region_name=REGION)


def test_put_project_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_project_policy.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", region_name=REGION)
    mock_client.put_project_policy.assert_called_once()


def test_put_project_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_project_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_project_policy",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put project policy"):
        put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", region_name=REGION)


def test_recognize_celebrities(monkeypatch):
    mock_client = MagicMock()
    mock_client.recognize_celebrities.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    recognize_celebrities({}, region_name=REGION)
    mock_client.recognize_celebrities.assert_called_once()


def test_recognize_celebrities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.recognize_celebrities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "recognize_celebrities",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to recognize celebrities"):
        recognize_celebrities({}, region_name=REGION)


def test_search_faces(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_faces("test-collection_id", "test-face_id", region_name=REGION)
    mock_client.search_faces.assert_called_once()


def test_search_faces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_faces",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search faces"):
        search_faces("test-collection_id", "test-face_id", region_name=REGION)


def test_search_faces_by_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces_by_image.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_faces_by_image("test-collection_id", {}, region_name=REGION)
    mock_client.search_faces_by_image.assert_called_once()


def test_search_faces_by_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_faces_by_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_faces_by_image",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search faces by image"):
        search_faces_by_image("test-collection_id", {}, region_name=REGION)


def test_search_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_users("test-collection_id", region_name=REGION)
    mock_client.search_users.assert_called_once()


def test_search_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_users",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search users"):
        search_users("test-collection_id", region_name=REGION)


def test_search_users_by_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users_by_image.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_users_by_image("test-collection_id", {}, region_name=REGION)
    mock_client.search_users_by_image.assert_called_once()


def test_search_users_by_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users_by_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_users_by_image",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search users by image"):
        search_users_by_image("test-collection_id", {}, region_name=REGION)


def test_start_celebrity_recognition(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_celebrity_recognition.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_celebrity_recognition({}, region_name=REGION)
    mock_client.start_celebrity_recognition.assert_called_once()


def test_start_celebrity_recognition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_celebrity_recognition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_celebrity_recognition",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start celebrity recognition"):
        start_celebrity_recognition({}, region_name=REGION)


def test_start_content_moderation(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_content_moderation.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_content_moderation({}, region_name=REGION)
    mock_client.start_content_moderation.assert_called_once()


def test_start_content_moderation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_content_moderation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_content_moderation",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start content moderation"):
        start_content_moderation({}, region_name=REGION)


def test_start_face_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_face_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_face_detection({}, region_name=REGION)
    mock_client.start_face_detection.assert_called_once()


def test_start_face_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_face_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_face_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start face detection"):
        start_face_detection({}, region_name=REGION)


def test_start_face_search(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_face_search.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_face_search({}, "test-collection_id", region_name=REGION)
    mock_client.start_face_search.assert_called_once()


def test_start_face_search_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_face_search.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_face_search",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start face search"):
        start_face_search({}, "test-collection_id", region_name=REGION)


def test_start_label_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_label_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_label_detection({}, region_name=REGION)
    mock_client.start_label_detection.assert_called_once()


def test_start_label_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_label_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_label_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start label detection"):
        start_label_detection({}, region_name=REGION)


def test_start_media_analysis_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_media_analysis_job.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_media_analysis_job({}, {}, {}, region_name=REGION)
    mock_client.start_media_analysis_job.assert_called_once()


def test_start_media_analysis_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_media_analysis_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_media_analysis_job",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start media analysis job"):
        start_media_analysis_job({}, {}, {}, region_name=REGION)


def test_start_person_tracking(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_person_tracking.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_person_tracking({}, region_name=REGION)
    mock_client.start_person_tracking.assert_called_once()


def test_start_person_tracking_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_person_tracking.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_person_tracking",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start person tracking"):
        start_person_tracking({}, region_name=REGION)


def test_start_project_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_project_version("test-project_version_arn", 1, region_name=REGION)
    mock_client.start_project_version.assert_called_once()


def test_start_project_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_project_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_project_version",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start project version"):
        start_project_version("test-project_version_arn", 1, region_name=REGION)


def test_start_segment_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_segment_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_segment_detection({}, [], region_name=REGION)
    mock_client.start_segment_detection.assert_called_once()


def test_start_segment_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_segment_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_segment_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start segment detection"):
        start_segment_detection({}, [], region_name=REGION)


def test_start_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_stream_processor("test-name", region_name=REGION)
    mock_client.start_stream_processor.assert_called_once()


def test_start_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start stream processor"):
        start_stream_processor("test-name", region_name=REGION)


def test_start_text_detection(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_text_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_text_detection({}, region_name=REGION)
    mock_client.start_text_detection.assert_called_once()


def test_start_text_detection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_text_detection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_text_detection",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start text detection"):
        start_text_detection({}, region_name=REGION)


def test_stop_project_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    stop_project_version("test-project_version_arn", region_name=REGION)
    mock_client.stop_project_version.assert_called_once()


def test_stop_project_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_project_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_project_version",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop project version"):
        stop_project_version("test-project_version_arn", region_name=REGION)


def test_stop_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    stop_stream_processor("test-name", region_name=REGION)
    mock_client.stop_stream_processor.assert_called_once()


def test_stop_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop stream processor"):
        stop_stream_processor("test-name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_dataset_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset_entries.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    update_dataset_entries("test-dataset_arn", {}, region_name=REGION)
    mock_client.update_dataset_entries.assert_called_once()


def test_update_dataset_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dataset_entries",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dataset entries"):
        update_dataset_entries("test-dataset_arn", {}, region_name=REGION)


def test_update_stream_processor(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    update_stream_processor("test-name", region_name=REGION)
    mock_client.update_stream_processor.assert_called_once()


def test_update_stream_processor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_processor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stream_processor",
    )
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stream processor"):
        update_stream_processor("test-name", region_name=REGION)


def test_associate_faces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import associate_faces
    mock_client = MagicMock()
    mock_client.associate_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    associate_faces("test-collection_id", "test-user_id", "test-face_ids", user_match_threshold="test-user_match_threshold", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.associate_faces.assert_called_once()

def test_copy_project_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import copy_project_version
    mock_client = MagicMock()
    mock_client.copy_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    copy_project_version("test-source_project_arn", "test-source_project_version_arn", "test-destination_project_arn", "test-version_name", {}, tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.copy_project_version.assert_called_once()

def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_dataset
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_dataset("test-dataset_type", "test-project_arn", dataset_source="test-dataset_source", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dataset.assert_called_once()

def test_create_face_liveness_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_face_liveness_session
    mock_client = MagicMock()
    mock_client.create_face_liveness_session.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_face_liveness_session(kms_key_id="test-kms_key_id", settings={}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_face_liveness_session.assert_called_once()

def test_create_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_project
    mock_client = MagicMock()
    mock_client.create_project.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_project("test-project_name", feature="test-feature", auto_update=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_project.assert_called_once()

def test_create_project_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_project_version
    mock_client = MagicMock()
    mock_client.create_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_project_version("test-project_arn", "test-version_name", {}, training_data="test-training_data", testing_data="test-testing_data", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", version_description="test-version_description", feature_config={}, region_name="us-east-1")
    mock_client.create_project_version.assert_called_once()

def test_create_stream_processor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_stream_processor
    mock_client = MagicMock()
    mock_client.create_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_stream_processor("test-input", "test-output", "test-name", {}, "test-role_arn", tags=[{"Key": "k", "Value": "v"}], notification_channel="test-notification_channel", kms_key_id="test-kms_key_id", regions_of_interest="test-regions_of_interest", data_sharing_preference="test-data_sharing_preference", region_name="us-east-1")
    mock_client.create_stream_processor.assert_called_once()

def test_create_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import create_user
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    create_user("test-collection_id", "test-user_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_user.assert_called_once()

def test_delete_project_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import delete_project_policy
    mock_client = MagicMock()
    mock_client.delete_project_policy.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_project_policy("test-project_arn", "test-policy_name", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.delete_project_policy.assert_called_once()

def test_delete_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import delete_user
    mock_client = MagicMock()
    mock_client.delete_user.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    delete_user("test-collection_id", "test-user_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.delete_user.assert_called_once()

def test_describe_project_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import describe_project_versions
    mock_client = MagicMock()
    mock_client.describe_project_versions.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_project_versions("test-project_arn", version_names="test-version_names", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_project_versions.assert_called_once()

def test_describe_projects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import describe_projects
    mock_client = MagicMock()
    mock_client.describe_projects.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    describe_projects(next_token="test-next_token", max_results=1, project_names="test-project_names", features="test-features", region_name="us-east-1")
    mock_client.describe_projects.assert_called_once()

def test_detect_custom_labels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import detect_custom_labels
    mock_client = MagicMock()
    mock_client.detect_custom_labels.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    detect_custom_labels("test-project_version_arn", "test-image", max_results=1, min_confidence="test-min_confidence", region_name="us-east-1")
    mock_client.detect_custom_labels.assert_called_once()

def test_detect_protective_equipment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import detect_protective_equipment
    mock_client = MagicMock()
    mock_client.detect_protective_equipment.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    detect_protective_equipment("test-image", summarization_attributes="test-summarization_attributes", region_name="us-east-1")
    mock_client.detect_protective_equipment.assert_called_once()

def test_disassociate_faces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import disassociate_faces
    mock_client = MagicMock()
    mock_client.disassociate_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    disassociate_faces("test-collection_id", "test-user_id", "test-face_ids", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.disassociate_faces.assert_called_once()

def test_get_celebrity_recognition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_celebrity_recognition
    mock_client = MagicMock()
    mock_client.get_celebrity_recognition.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_celebrity_recognition("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.get_celebrity_recognition.assert_called_once()

def test_get_content_moderation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_content_moderation
    mock_client = MagicMock()
    mock_client.get_content_moderation.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_content_moderation("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", aggregate_by="test-aggregate_by", region_name="us-east-1")
    mock_client.get_content_moderation.assert_called_once()

def test_get_face_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_face_detection
    mock_client = MagicMock()
    mock_client.get_face_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_face_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_face_detection.assert_called_once()

def test_get_face_search_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_face_search
    mock_client = MagicMock()
    mock_client.get_face_search.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_face_search("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.get_face_search.assert_called_once()

def test_get_label_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_label_detection
    mock_client = MagicMock()
    mock_client.get_label_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_label_detection("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", aggregate_by="test-aggregate_by", region_name="us-east-1")
    mock_client.get_label_detection.assert_called_once()

def test_get_person_tracking_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_person_tracking
    mock_client = MagicMock()
    mock_client.get_person_tracking.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_person_tracking("test-job_id", max_results=1, next_token="test-next_token", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.get_person_tracking.assert_called_once()

def test_get_segment_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_segment_detection
    mock_client = MagicMock()
    mock_client.get_segment_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_segment_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_segment_detection.assert_called_once()

def test_get_text_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import get_text_detection
    mock_client = MagicMock()
    mock_client.get_text_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    get_text_detection("test-job_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_text_detection.assert_called_once()

def test_index_faces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import index_faces
    mock_client = MagicMock()
    mock_client.index_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    index_faces("test-collection_id", "test-image", external_image_id="test-external_image_id", detection_attributes="test-detection_attributes", max_faces=1, quality_filter=[{}], region_name="us-east-1")
    mock_client.index_faces.assert_called_once()

def test_list_collections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_collections
    mock_client = MagicMock()
    mock_client.list_collections.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_collections(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_collections.assert_called_once()

def test_list_dataset_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_dataset_entries
    mock_client = MagicMock()
    mock_client.list_dataset_entries.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_dataset_entries("test-dataset_arn", contains_labels="test-contains_labels", labeled="test-labeled", source_ref_contains="test-source_ref_contains", has_errors="test-has_errors", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dataset_entries.assert_called_once()

def test_list_dataset_labels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_dataset_labels
    mock_client = MagicMock()
    mock_client.list_dataset_labels.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_dataset_labels("test-dataset_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dataset_labels.assert_called_once()

def test_list_faces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_faces
    mock_client = MagicMock()
    mock_client.list_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_faces("test-collection_id", next_token="test-next_token", max_results=1, user_id="test-user_id", face_ids="test-face_ids", region_name="us-east-1")
    mock_client.list_faces.assert_called_once()

def test_list_media_analysis_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_media_analysis_jobs
    mock_client = MagicMock()
    mock_client.list_media_analysis_jobs.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_media_analysis_jobs(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_media_analysis_jobs.assert_called_once()

def test_list_project_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_project_policies
    mock_client = MagicMock()
    mock_client.list_project_policies.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_project_policies("test-project_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_project_policies.assert_called_once()

def test_list_stream_processors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_stream_processors
    mock_client = MagicMock()
    mock_client.list_stream_processors.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_stream_processors(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_stream_processors.assert_called_once()

def test_list_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import list_users
    mock_client = MagicMock()
    mock_client.list_users.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    list_users("test-collection_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_users.assert_called_once()

def test_put_project_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import put_project_policy
    mock_client = MagicMock()
    mock_client.put_project_policy.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    put_project_policy("test-project_arn", "test-policy_name", "test-policy_document", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.put_project_policy.assert_called_once()

def test_search_faces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import search_faces
    mock_client = MagicMock()
    mock_client.search_faces.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_faces("test-collection_id", "test-face_id", max_faces=1, face_match_threshold="test-face_match_threshold", region_name="us-east-1")
    mock_client.search_faces.assert_called_once()

def test_search_faces_by_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import search_faces_by_image
    mock_client = MagicMock()
    mock_client.search_faces_by_image.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_faces_by_image("test-collection_id", "test-image", max_faces=1, face_match_threshold="test-face_match_threshold", quality_filter=[{}], region_name="us-east-1")
    mock_client.search_faces_by_image.assert_called_once()

def test_search_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import search_users
    mock_client = MagicMock()
    mock_client.search_users.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_users("test-collection_id", user_id="test-user_id", face_id="test-face_id", user_match_threshold="test-user_match_threshold", max_users=1, region_name="us-east-1")
    mock_client.search_users.assert_called_once()

def test_search_users_by_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import search_users_by_image
    mock_client = MagicMock()
    mock_client.search_users_by_image.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    search_users_by_image("test-collection_id", "test-image", user_match_threshold="test-user_match_threshold", max_users=1, quality_filter=[{}], region_name="us-east-1")
    mock_client.search_users_by_image.assert_called_once()

def test_start_celebrity_recognition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_celebrity_recognition
    mock_client = MagicMock()
    mock_client.start_celebrity_recognition.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_celebrity_recognition("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.start_celebrity_recognition.assert_called_once()

def test_start_content_moderation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_content_moderation
    mock_client = MagicMock()
    mock_client.start_content_moderation.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_content_moderation("test-video", min_confidence="test-min_confidence", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.start_content_moderation.assert_called_once()

def test_start_face_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_face_detection
    mock_client = MagicMock()
    mock_client.start_face_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_face_detection("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", face_attributes="test-face_attributes", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.start_face_detection.assert_called_once()

def test_start_face_search_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_face_search
    mock_client = MagicMock()
    mock_client.start_face_search.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_face_search("test-video", "test-collection_id", client_request_token="test-client_request_token", face_match_threshold="test-face_match_threshold", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.start_face_search.assert_called_once()

def test_start_label_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_label_detection
    mock_client = MagicMock()
    mock_client.start_label_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_label_detection("test-video", client_request_token="test-client_request_token", min_confidence="test-min_confidence", notification_channel="test-notification_channel", job_tag="test-job_tag", features="test-features", settings={}, region_name="us-east-1")
    mock_client.start_label_detection.assert_called_once()

def test_start_media_analysis_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_media_analysis_job
    mock_client = MagicMock()
    mock_client.start_media_analysis_job.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_media_analysis_job({}, "test-input", {}, client_request_token="test-client_request_token", job_name="test-job_name", kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.start_media_analysis_job.assert_called_once()

def test_start_person_tracking_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_person_tracking
    mock_client = MagicMock()
    mock_client.start_person_tracking.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_person_tracking("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", region_name="us-east-1")
    mock_client.start_person_tracking.assert_called_once()

def test_start_project_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_project_version
    mock_client = MagicMock()
    mock_client.start_project_version.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_project_version("test-project_version_arn", "test-min_inference_units", max_inference_units=1, region_name="us-east-1")
    mock_client.start_project_version.assert_called_once()

def test_start_segment_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_segment_detection
    mock_client = MagicMock()
    mock_client.start_segment_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_segment_detection("test-video", "test-segment_types", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", filters=[{}], region_name="us-east-1")
    mock_client.start_segment_detection.assert_called_once()

def test_start_stream_processor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_stream_processor
    mock_client = MagicMock()
    mock_client.start_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_stream_processor("test-name", start_selector="test-start_selector", stop_selector="test-stop_selector", region_name="us-east-1")
    mock_client.start_stream_processor.assert_called_once()

def test_start_text_detection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import start_text_detection
    mock_client = MagicMock()
    mock_client.start_text_detection.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    start_text_detection("test-video", client_request_token="test-client_request_token", notification_channel="test-notification_channel", job_tag="test-job_tag", filters=[{}], region_name="us-east-1")
    mock_client.start_text_detection.assert_called_once()

def test_update_stream_processor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rekognition import update_stream_processor
    mock_client = MagicMock()
    mock_client.update_stream_processor.return_value = {}
    monkeypatch.setattr("aws_util.rekognition.get_client", lambda *a, **kw: mock_client)
    update_stream_processor("test-name", settings_for_update={}, regions_of_interest_for_update="test-regions_of_interest_for_update", data_sharing_preference_for_update="test-data_sharing_preference_for_update", parameters_to_delete="test-parameters_to_delete", region_name="us-east-1")
    mock_client.update_stream_processor.assert_called_once()
