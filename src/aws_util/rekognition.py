from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "AssociateFacesResult",
    "BoundingBox",
    "CopyProjectVersionResult",
    "CreateDatasetResult",
    "CreateFaceLivenessSessionResult",
    "CreateProjectResult",
    "CreateProjectVersionResult",
    "CreateStreamProcessorResult",
    "DeleteFacesResult",
    "DeleteProjectResult",
    "DeleteProjectVersionResult",
    "DescribeCollectionResult",
    "DescribeDatasetResult",
    "DescribeProjectVersionsResult",
    "DescribeProjectsResult",
    "DescribeStreamProcessorResult",
    "DetectCustomLabelsResult",
    "DetectProtectiveEquipmentResult",
    "DisassociateFacesResult",
    "FaceMatch",
    "GetCelebrityInfoResult",
    "GetCelebrityRecognitionResult",
    "GetContentModerationResult",
    "GetFaceDetectionResult",
    "GetFaceLivenessSessionResultsResult",
    "GetFaceSearchResult",
    "GetLabelDetectionResult",
    "GetMediaAnalysisJobResult",
    "GetPersonTrackingResult",
    "GetSegmentDetectionResult",
    "GetTextDetectionResult",
    "IndexFacesResult",
    "ListCollectionsResult",
    "ListDatasetEntriesResult",
    "ListDatasetLabelsResult",
    "ListFacesResult",
    "ListMediaAnalysisJobsResult",
    "ListProjectPoliciesResult",
    "ListStreamProcessorsResult",
    "ListTagsForResourceResult",
    "ListUsersResult",
    "PutProjectPolicyResult",
    "RecognizeCelebritiesResult",
    "RekognitionFace",
    "RekognitionLabel",
    "RekognitionText",
    "SearchFacesByImageResult",
    "SearchFacesResult",
    "SearchUsersByImageResult",
    "SearchUsersResult",
    "StartCelebrityRecognitionResult",
    "StartContentModerationResult",
    "StartFaceDetectionResult",
    "StartFaceSearchResult",
    "StartLabelDetectionResult",
    "StartMediaAnalysisJobResult",
    "StartPersonTrackingResult",
    "StartProjectVersionResult",
    "StartSegmentDetectionResult",
    "StartStreamProcessorResult",
    "StartTextDetectionResult",
    "StopProjectVersionResult",
    "associate_faces",
    "compare_faces",
    "copy_project_version",
    "create_collection",
    "create_dataset",
    "create_face_liveness_session",
    "create_project",
    "create_project_version",
    "create_stream_processor",
    "create_user",
    "delete_collection",
    "delete_dataset",
    "delete_faces",
    "delete_project",
    "delete_project_policy",
    "delete_project_version",
    "delete_stream_processor",
    "delete_user",
    "describe_collection",
    "describe_dataset",
    "describe_project_versions",
    "describe_projects",
    "describe_stream_processor",
    "detect_custom_labels",
    "detect_faces",
    "detect_labels",
    "detect_moderation_labels",
    "detect_protective_equipment",
    "detect_text",
    "disassociate_faces",
    "distribute_dataset_entries",
    "ensure_collection",
    "get_celebrity_info",
    "get_celebrity_recognition",
    "get_content_moderation",
    "get_face_detection",
    "get_face_liveness_session_results",
    "get_face_search",
    "get_label_detection",
    "get_media_analysis_job",
    "get_person_tracking",
    "get_segment_detection",
    "get_text_detection",
    "index_face",
    "index_faces",
    "list_collections",
    "list_dataset_entries",
    "list_dataset_labels",
    "list_faces",
    "list_media_analysis_jobs",
    "list_project_policies",
    "list_stream_processors",
    "list_tags_for_resource",
    "list_users",
    "put_project_policy",
    "recognize_celebrities",
    "search_face_by_image",
    "search_faces",
    "search_faces_by_image",
    "search_users",
    "search_users_by_image",
    "start_celebrity_recognition",
    "start_content_moderation",
    "start_face_detection",
    "start_face_search",
    "start_label_detection",
    "start_media_analysis_job",
    "start_person_tracking",
    "start_project_version",
    "start_segment_detection",
    "start_stream_processor",
    "start_text_detection",
    "stop_project_version",
    "stop_stream_processor",
    "tag_resource",
    "untag_resource",
    "update_dataset_entries",
    "update_stream_processor",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class BoundingBox(BaseModel):
    """Normalised bounding box (values 0.0–1.0 relative to image dimensions)."""

    model_config = ConfigDict(frozen=True)

    width: float
    height: float
    left: float
    top: float


class RekognitionLabel(BaseModel):
    """An object/scene label detected in an image."""

    model_config = ConfigDict(frozen=True)

    name: str
    confidence: float
    parents: list[str] = []


class RekognitionFace(BaseModel):
    """A face detected in an image."""

    model_config = ConfigDict(frozen=True)

    bounding_box: BoundingBox | None = None
    confidence: float
    age_range_low: int | None = None
    age_range_high: int | None = None
    smile: bool | None = None
    eyeglasses: bool | None = None
    sunglasses: bool | None = None
    gender: str | None = None
    emotions: list[dict[str, Any]] = []


class RekognitionText(BaseModel):
    """A text block detected in an image."""

    model_config = ConfigDict(frozen=True)

    detected_text: str
    text_type: str
    confidence: float
    bounding_box: BoundingBox | None = None


class FaceMatch(BaseModel):
    """A face match result from face comparison."""

    model_config = ConfigDict(frozen=True)

    similarity: float
    bounding_box: BoundingBox | None = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _s3_image(bucket: str, key: str) -> dict:
    return {"S3Object": {"Bucket": bucket, "Name": key}}


def _bytes_image(image_bytes: bytes) -> dict:
    return {"Bytes": image_bytes}


def _bbox(bb: dict) -> BoundingBox:
    return BoundingBox(
        width=bb.get("Width", 0.0),
        height=bb.get("Height", 0.0),
        left=bb.get("Left", 0.0),
        top=bb.get("Top", 0.0),
    )


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def detect_labels(
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    max_labels: int = 20,
    min_confidence: float = 70.0,
    region_name: str | None = None,
) -> list[RekognitionLabel]:
    """Detect objects, scenes, and concepts in an image.

    Provide either *image_bytes* for an in-memory image, or *s3_bucket* /
    *s3_key* for an S3-hosted image.

    Args:
        image_bytes: Raw image bytes (JPEG or PNG).
        s3_bucket: Source S3 bucket name.
        s3_key: Source S3 object key.
        max_labels: Maximum number of labels to return.
        min_confidence: Minimum confidence threshold (0–100).
        region_name: AWS region override.

    Returns:
        A list of :class:`RekognitionLabel` objects sorted by confidence.

    Raises:
        ValueError: If neither image bytes nor S3 coordinates are provided.
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    try:
        resp = client.detect_labels(
            Image=image,
            MaxLabels=max_labels,
            MinConfidence=min_confidence,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_labels failed") from exc
    return [
        RekognitionLabel(
            name=lbl["Name"],
            confidence=lbl["Confidence"],
            parents=[p["Name"] for p in lbl.get("Parents", [])],
        )
        for lbl in resp.get("Labels", [])
    ]


def detect_faces(
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    attributes: list[str] | None = None,
    region_name: str | None = None,
) -> list[RekognitionFace]:
    """Detect faces and facial attributes in an image.

    Args:
        image_bytes: Raw image bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        attributes: Facial attributes to return.  ``["ALL"]`` returns every
            attribute.  Defaults to ``["DEFAULT"]``.
        region_name: AWS region override.

    Returns:
        A list of :class:`RekognitionFace` objects.

    Raises:
        ValueError: If neither image source is provided.
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    try:
        resp = client.detect_faces(Image=image, Attributes=attributes or ["DEFAULT"])
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_faces failed") from exc

    faces: list[RekognitionFace] = []
    for fd in resp.get("FaceDetails", []):
        bb = fd.get("BoundingBox")
        age = fd.get("AgeRange", {})
        smile = fd.get("Smile", {})
        eyeglasses = fd.get("Eyeglasses", {})
        sunglasses = fd.get("Sunglasses", {})
        gender = fd.get("Gender", {})
        faces.append(
            RekognitionFace(
                bounding_box=_bbox(bb) if bb else None,
                confidence=fd.get("Confidence", 0.0),
                age_range_low=age.get("Low"),
                age_range_high=age.get("High"),
                smile=smile.get("Value"),
                eyeglasses=eyeglasses.get("Value"),
                sunglasses=sunglasses.get("Value"),
                gender=gender.get("Value"),
                emotions=fd.get("Emotions", []),
            )
        )
    return faces


def detect_text(
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    region_name: str | None = None,
) -> list[RekognitionText]:
    """Detect text (OCR) in an image.

    Args:
        image_bytes: Raw image bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        region_name: AWS region override.

    Returns:
        A list of :class:`RekognitionText` detections.

    Raises:
        ValueError: If neither image source is provided.
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    try:
        resp = client.detect_text(Image=image)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_text failed") from exc
    return [
        RekognitionText(
            detected_text=td["DetectedText"],
            text_type=td["Type"],
            confidence=td["Confidence"],
            bounding_box=(_bbox(td["Geometry"]["BoundingBox"]) if td.get("Geometry") else None),
        )
        for td in resp.get("TextDetections", [])
    ]


def compare_faces(
    source_bytes: bytes,
    target_bytes: bytes,
    similarity_threshold: float = 80.0,
    region_name: str | None = None,
) -> list[FaceMatch]:
    """Compare a source face against faces in a target image.

    Args:
        source_bytes: Image bytes containing the source face.
        target_bytes: Image bytes to search for matching faces.
        similarity_threshold: Minimum similarity score 0–100 (default ``80``).
        region_name: AWS region override.

    Returns:
        A list of :class:`FaceMatch` objects for faces that meet the threshold.

    Raises:
        RuntimeError: If the comparison fails.
    """
    client = get_client("rekognition", region_name)
    try:
        resp = client.compare_faces(
            SourceImage={"Bytes": source_bytes},
            TargetImage={"Bytes": target_bytes},
            SimilarityThreshold=similarity_threshold,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "compare_faces failed") from exc
    return [
        FaceMatch(
            similarity=fm["Similarity"],
            bounding_box=(
                _bbox(fm["Face"]["BoundingBox"]) if fm.get("Face", {}).get("BoundingBox") else None
            ),
        )
        for fm in resp.get("FaceMatches", [])
    ]


def detect_moderation_labels(
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    min_confidence: float = 60.0,
    region_name: str | None = None,
) -> list[RekognitionLabel]:
    """Detect unsafe or inappropriate content in an image.

    Args:
        image_bytes: Raw image bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        min_confidence: Minimum confidence threshold (default ``60``).
        region_name: AWS region override.

    Returns:
        A list of :class:`RekognitionLabel` objects for detected unsafe content.

    Raises:
        ValueError: If neither image source is provided.
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    try:
        resp = client.detect_moderation_labels(Image=image, MinConfidence=min_confidence)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_moderation_labels failed") from exc
    return [
        RekognitionLabel(
            name=lbl["Name"],
            confidence=lbl["Confidence"],
            parents=[lbl["ParentName"]] if lbl.get("ParentName") else [],
        )
        for lbl in resp.get("ModerationLabels", [])
    ]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def create_collection(
    collection_id: str,
    region_name: str | None = None,
) -> str:
    """Create a Rekognition face collection.

    Face collections are persistent stores of indexed face vectors used for
    :func:`search_face_by_image` lookups.

    Args:
        collection_id: Unique identifier for the new collection.
        region_name: AWS region override.

    Returns:
        The ARN of the created collection.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("rekognition", region_name)
    try:
        resp = client.create_collection(CollectionId=collection_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create collection {collection_id!r}") from exc
    return resp.get("CollectionArn", "")


def index_face(
    collection_id: str,
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    external_image_id: str | None = None,
    region_name: str | None = None,
) -> str:
    """Detect and index a face from an image into a Rekognition collection.

    Args:
        collection_id: Collection to index the face into.
        image_bytes: Raw image bytes.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        external_image_id: Optional label to associate with the face
            (e.g., a user ID).
        region_name: AWS region override.

    Returns:
        The Rekognition face ID assigned to the indexed face.

    Raises:
        ValueError: If neither image source is provided.
        RuntimeError: If indexing fails or no face is detected.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    kwargs: dict[str, Any] = {
        "CollectionId": collection_id,
        "Image": image,
        "MaxFaces": 1,
        "QualityFilter": "AUTO",
        "DetectionAttributes": ["DEFAULT"],
    }
    if external_image_id:
        kwargs["ExternalImageId"] = external_image_id
    try:
        resp = client.index_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"index_face failed for collection {collection_id!r}") from exc
    records = resp.get("FaceRecords", [])
    if not records:
        raise AwsServiceError("No face detected in the provided image")
    return records[0]["Face"]["FaceId"]


def search_face_by_image(
    collection_id: str,
    image_bytes: bytes | None = None,
    s3_bucket: str | None = None,
    s3_key: str | None = None,
    max_faces: int = 5,
    face_match_threshold: float = 80.0,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Search a Rekognition collection for faces matching the face in an image.

    Args:
        collection_id: Collection to search.
        image_bytes: Raw image bytes containing a query face.
        s3_bucket: Source S3 bucket.
        s3_key: Source S3 key.
        max_faces: Maximum number of matching faces to return (default 5).
        face_match_threshold: Minimum similarity score 0–100 (default 80).
        region_name: AWS region override.

    Returns:
        A list of match dicts with ``face_id``, ``external_image_id``,
        ``similarity``, and ``confidence`` keys.

    Raises:
        ValueError: If neither image source is provided.
        RuntimeError: If the search fails.
    """
    client = get_client("rekognition", region_name)
    image = _resolve_image(image_bytes, s3_bucket, s3_key)
    try:
        resp = client.search_faces_by_image(
            CollectionId=collection_id,
            Image=image,
            MaxFaces=max_faces,
            FaceMatchThreshold=face_match_threshold,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"search_face_by_image failed for collection {collection_id!r}"
        ) from exc
    return [
        {
            "face_id": m["Face"]["FaceId"],
            "external_image_id": m["Face"].get("ExternalImageId"),
            "similarity": m["Similarity"],
            "confidence": m["Face"].get("Confidence"),
        }
        for m in resp.get("FaceMatches", [])
    ]


def delete_collection(
    collection_id: str,
    region_name: str | None = None,
) -> None:
    """Delete a Rekognition face collection and all indexed faces.

    Args:
        collection_id: Collection to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = get_client("rekognition", region_name)
    try:
        client.delete_collection(CollectionId=collection_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete collection {collection_id!r}") from exc


def ensure_collection(
    collection_id: str,
    region_name: str | None = None,
) -> tuple[str, bool]:
    """Get or create a Rekognition face collection (idempotent).

    If the collection already exists its ARN is returned unchanged.  If it
    does not exist it is created.

    Args:
        collection_id: Unique identifier for the collection.
        region_name: AWS region override.

    Returns:
        A ``(collection_arn, created)`` tuple where *created* is ``True`` if
        the collection was just created.

    Raises:
        RuntimeError: If the describe or create call fails.
    """
    client = get_client("rekognition", region_name)
    try:
        resp = client.describe_collection(CollectionId=collection_id)
        return resp["CollectionARN"], False
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceNotFoundException":
            raise wrap_aws_error(exc, f"ensure_collection failed for {collection_id!r}") from exc

    arn = create_collection(collection_id, region_name=region_name)
    return arn, True


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _resolve_image(
    image_bytes: bytes | None,
    s3_bucket: str | None,
    s3_key: str | None,
) -> dict:
    if image_bytes is not None:
        return _bytes_image(image_bytes)
    if s3_bucket and s3_key:
        return _s3_image(s3_bucket, s3_key)
    raise ValueError("Provide either image_bytes or both s3_bucket and s3_key")


class AssociateFacesResult(BaseModel):
    """Result of associate_faces."""

    model_config = ConfigDict(frozen=True)

    associated_faces: list[dict[str, Any]] | None = None
    unsuccessful_face_associations: list[dict[str, Any]] | None = None
    user_status: str | None = None


class CopyProjectVersionResult(BaseModel):
    """Result of copy_project_version."""

    model_config = ConfigDict(frozen=True)

    project_version_arn: str | None = None


class CreateDatasetResult(BaseModel):
    """Result of create_dataset."""

    model_config = ConfigDict(frozen=True)

    dataset_arn: str | None = None


class CreateFaceLivenessSessionResult(BaseModel):
    """Result of create_face_liveness_session."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None


class CreateProjectResult(BaseModel):
    """Result of create_project."""

    model_config = ConfigDict(frozen=True)

    project_arn: str | None = None


class CreateProjectVersionResult(BaseModel):
    """Result of create_project_version."""

    model_config = ConfigDict(frozen=True)

    project_version_arn: str | None = None


class CreateStreamProcessorResult(BaseModel):
    """Result of create_stream_processor."""

    model_config = ConfigDict(frozen=True)

    stream_processor_arn: str | None = None


class DeleteFacesResult(BaseModel):
    """Result of delete_faces."""

    model_config = ConfigDict(frozen=True)

    deleted_faces: list[str] | None = None
    unsuccessful_face_deletions: list[dict[str, Any]] | None = None


class DeleteProjectResult(BaseModel):
    """Result of delete_project."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class DeleteProjectVersionResult(BaseModel):
    """Result of delete_project_version."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class DescribeCollectionResult(BaseModel):
    """Result of describe_collection."""

    model_config = ConfigDict(frozen=True)

    face_count: int | None = None
    face_model_version: str | None = None
    collection_arn: str | None = None
    creation_timestamp: str | None = None
    user_count: int | None = None


class DescribeDatasetResult(BaseModel):
    """Result of describe_dataset."""

    model_config = ConfigDict(frozen=True)

    dataset_description: dict[str, Any] | None = None


class DescribeProjectVersionsResult(BaseModel):
    """Result of describe_project_versions."""

    model_config = ConfigDict(frozen=True)

    project_version_descriptions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeProjectsResult(BaseModel):
    """Result of describe_projects."""

    model_config = ConfigDict(frozen=True)

    project_descriptions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeStreamProcessorResult(BaseModel):
    """Result of describe_stream_processor."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    stream_processor_arn: str | None = None
    status: str | None = None
    status_message: str | None = None
    creation_timestamp: str | None = None
    last_update_timestamp: str | None = None
    input: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    role_arn: str | None = None
    settings: dict[str, Any] | None = None
    notification_channel: dict[str, Any] | None = None
    kms_key_id: str | None = None
    regions_of_interest: list[dict[str, Any]] | None = None
    data_sharing_preference: dict[str, Any] | None = None


class DetectCustomLabelsResult(BaseModel):
    """Result of detect_custom_labels."""

    model_config = ConfigDict(frozen=True)

    custom_labels: list[dict[str, Any]] | None = None


class DetectProtectiveEquipmentResult(BaseModel):
    """Result of detect_protective_equipment."""

    model_config = ConfigDict(frozen=True)

    protective_equipment_model_version: str | None = None
    persons: list[dict[str, Any]] | None = None
    summary: dict[str, Any] | None = None


class DisassociateFacesResult(BaseModel):
    """Result of disassociate_faces."""

    model_config = ConfigDict(frozen=True)

    disassociated_faces: list[dict[str, Any]] | None = None
    unsuccessful_face_disassociations: list[dict[str, Any]] | None = None
    user_status: str | None = None


class GetCelebrityInfoResult(BaseModel):
    """Result of get_celebrity_info."""

    model_config = ConfigDict(frozen=True)

    urls: list[str] | None = None
    name: str | None = None
    known_gender: dict[str, Any] | None = None


class GetCelebrityRecognitionResult(BaseModel):
    """Result of get_celebrity_recognition."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    next_token: str | None = None
    celebrities: list[dict[str, Any]] | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class GetContentModerationResult(BaseModel):
    """Result of get_content_moderation."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    moderation_labels: list[dict[str, Any]] | None = None
    next_token: str | None = None
    moderation_model_version: str | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None
    get_request_metadata: dict[str, Any] | None = None


class GetFaceDetectionResult(BaseModel):
    """Result of get_face_detection."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    next_token: str | None = None
    faces: list[dict[str, Any]] | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class GetFaceLivenessSessionResultsResult(BaseModel):
    """Result of get_face_liveness_session_results."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None
    status: str | None = None
    confidence: float | None = None
    reference_image: dict[str, Any] | None = None
    audit_images: list[dict[str, Any]] | None = None
    challenge: dict[str, Any] | None = None


class GetFaceSearchResult(BaseModel):
    """Result of get_face_search."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    next_token: str | None = None
    video_metadata: dict[str, Any] | None = None
    persons: list[dict[str, Any]] | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class GetLabelDetectionResult(BaseModel):
    """Result of get_label_detection."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    next_token: str | None = None
    labels: list[dict[str, Any]] | None = None
    label_model_version: str | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None
    get_request_metadata: dict[str, Any] | None = None


class GetMediaAnalysisJobResult(BaseModel):
    """Result of get_media_analysis_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_name: str | None = None
    operations_config: dict[str, Any] | None = None
    status: str | None = None
    failure_details: dict[str, Any] | None = None
    creation_timestamp: str | None = None
    completion_timestamp: str | None = None
    input: dict[str, Any] | None = None
    output_config: dict[str, Any] | None = None
    kms_key_id: str | None = None
    results: dict[str, Any] | None = None
    manifest_summary: dict[str, Any] | None = None


class GetPersonTrackingResult(BaseModel):
    """Result of get_person_tracking."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    next_token: str | None = None
    persons: list[dict[str, Any]] | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class GetSegmentDetectionResult(BaseModel):
    """Result of get_segment_detection."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: list[dict[str, Any]] | None = None
    audio_metadata: list[dict[str, Any]] | None = None
    next_token: str | None = None
    segments: list[dict[str, Any]] | None = None
    selected_segment_types: list[dict[str, Any]] | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class GetTextDetectionResult(BaseModel):
    """Result of get_text_detection."""

    model_config = ConfigDict(frozen=True)

    job_status: str | None = None
    status_message: str | None = None
    video_metadata: dict[str, Any] | None = None
    text_detections: list[dict[str, Any]] | None = None
    next_token: str | None = None
    text_model_version: str | None = None
    job_id: str | None = None
    video: dict[str, Any] | None = None
    job_tag: str | None = None


class IndexFacesResult(BaseModel):
    """Result of index_faces."""

    model_config = ConfigDict(frozen=True)

    face_records: list[dict[str, Any]] | None = None
    orientation_correction: str | None = None
    face_model_version: str | None = None
    unindexed_faces: list[dict[str, Any]] | None = None


class ListCollectionsResult(BaseModel):
    """Result of list_collections."""

    model_config = ConfigDict(frozen=True)

    collection_ids: list[str] | None = None
    next_token: str | None = None
    face_model_versions: list[str] | None = None


class ListDatasetEntriesResult(BaseModel):
    """Result of list_dataset_entries."""

    model_config = ConfigDict(frozen=True)

    dataset_entries: list[str] | None = None
    next_token: str | None = None


class ListDatasetLabelsResult(BaseModel):
    """Result of list_dataset_labels."""

    model_config = ConfigDict(frozen=True)

    dataset_label_descriptions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFacesResult(BaseModel):
    """Result of list_faces."""

    model_config = ConfigDict(frozen=True)

    faces: list[dict[str, Any]] | None = None
    next_token: str | None = None
    face_model_version: str | None = None


class ListMediaAnalysisJobsResult(BaseModel):
    """Result of list_media_analysis_jobs."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    media_analysis_jobs: list[dict[str, Any]] | None = None


class ListProjectPoliciesResult(BaseModel):
    """Result of list_project_policies."""

    model_config = ConfigDict(frozen=True)

    project_policies: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStreamProcessorsResult(BaseModel):
    """Result of list_stream_processors."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    stream_processors: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListUsersResult(BaseModel):
    """Result of list_users."""

    model_config = ConfigDict(frozen=True)

    users: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutProjectPolicyResult(BaseModel):
    """Result of put_project_policy."""

    model_config = ConfigDict(frozen=True)

    policy_revision_id: str | None = None


class RecognizeCelebritiesResult(BaseModel):
    """Result of recognize_celebrities."""

    model_config = ConfigDict(frozen=True)

    celebrity_faces: list[dict[str, Any]] | None = None
    unrecognized_faces: list[dict[str, Any]] | None = None
    orientation_correction: str | None = None


class SearchFacesResult(BaseModel):
    """Result of search_faces."""

    model_config = ConfigDict(frozen=True)

    searched_face_id: str | None = None
    face_matches: list[dict[str, Any]] | None = None
    face_model_version: str | None = None


class SearchFacesByImageResult(BaseModel):
    """Result of search_faces_by_image."""

    model_config = ConfigDict(frozen=True)

    searched_face_bounding_box: dict[str, Any] | None = None
    searched_face_confidence: float | None = None
    face_matches: list[dict[str, Any]] | None = None
    face_model_version: str | None = None


class SearchUsersResult(BaseModel):
    """Result of search_users."""

    model_config = ConfigDict(frozen=True)

    user_matches: list[dict[str, Any]] | None = None
    face_model_version: str | None = None
    searched_face: dict[str, Any] | None = None
    searched_user: dict[str, Any] | None = None


class SearchUsersByImageResult(BaseModel):
    """Result of search_users_by_image."""

    model_config = ConfigDict(frozen=True)

    user_matches: list[dict[str, Any]] | None = None
    face_model_version: str | None = None
    searched_face: dict[str, Any] | None = None
    unsearched_faces: list[dict[str, Any]] | None = None


class StartCelebrityRecognitionResult(BaseModel):
    """Result of start_celebrity_recognition."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartContentModerationResult(BaseModel):
    """Result of start_content_moderation."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartFaceDetectionResult(BaseModel):
    """Result of start_face_detection."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartFaceSearchResult(BaseModel):
    """Result of start_face_search."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartLabelDetectionResult(BaseModel):
    """Result of start_label_detection."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartMediaAnalysisJobResult(BaseModel):
    """Result of start_media_analysis_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartPersonTrackingResult(BaseModel):
    """Result of start_person_tracking."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartProjectVersionResult(BaseModel):
    """Result of start_project_version."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class StartSegmentDetectionResult(BaseModel):
    """Result of start_segment_detection."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StartStreamProcessorResult(BaseModel):
    """Result of start_stream_processor."""

    model_config = ConfigDict(frozen=True)

    session_id: str | None = None


class StartTextDetectionResult(BaseModel):
    """Result of start_text_detection."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None


class StopProjectVersionResult(BaseModel):
    """Result of stop_project_version."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


def associate_faces(
    collection_id: str,
    user_id: str,
    face_ids: list[str],
    *,
    user_match_threshold: float | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> AssociateFacesResult:
    """Associate faces.

    Args:
        collection_id: Collection id.
        user_id: User id.
        face_ids: Face ids.
        user_match_threshold: User match threshold.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["UserId"] = user_id
    kwargs["FaceIds"] = face_ids
    if user_match_threshold is not None:
        kwargs["UserMatchThreshold"] = user_match_threshold
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.associate_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate faces") from exc
    return AssociateFacesResult(
        associated_faces=resp.get("AssociatedFaces"),
        unsuccessful_face_associations=resp.get("UnsuccessfulFaceAssociations"),
        user_status=resp.get("UserStatus"),
    )


def copy_project_version(
    source_project_arn: str,
    source_project_version_arn: str,
    destination_project_arn: str,
    version_name: str,
    output_config: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> CopyProjectVersionResult:
    """Copy project version.

    Args:
        source_project_arn: Source project arn.
        source_project_version_arn: Source project version arn.
        destination_project_arn: Destination project arn.
        version_name: Version name.
        output_config: Output config.
        tags: Tags.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceProjectArn"] = source_project_arn
    kwargs["SourceProjectVersionArn"] = source_project_version_arn
    kwargs["DestinationProjectArn"] = destination_project_arn
    kwargs["VersionName"] = version_name
    kwargs["OutputConfig"] = output_config
    if tags is not None:
        kwargs["Tags"] = tags
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    try:
        resp = client.copy_project_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy project version") from exc
    return CopyProjectVersionResult(
        project_version_arn=resp.get("ProjectVersionArn"),
    )


def create_dataset(
    dataset_type: str,
    project_arn: str,
    *,
    dataset_source: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDatasetResult:
    """Create dataset.

    Args:
        dataset_type: Dataset type.
        project_arn: Project arn.
        dataset_source: Dataset source.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetType"] = dataset_type
    kwargs["ProjectArn"] = project_arn
    if dataset_source is not None:
        kwargs["DatasetSource"] = dataset_source
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create dataset") from exc
    return CreateDatasetResult(
        dataset_arn=resp.get("DatasetArn"),
    )


def create_face_liveness_session(
    *,
    kms_key_id: str | None = None,
    settings: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateFaceLivenessSessionResult:
    """Create face liveness session.

    Args:
        kms_key_id: Kms key id.
        settings: Settings.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if settings is not None:
        kwargs["Settings"] = settings
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.create_face_liveness_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create face liveness session") from exc
    return CreateFaceLivenessSessionResult(
        session_id=resp.get("SessionId"),
    )


def create_project(
    project_name: str,
    *,
    feature: str | None = None,
    auto_update: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateProjectResult:
    """Create project.

    Args:
        project_name: Project name.
        feature: Feature.
        auto_update: Auto update.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectName"] = project_name
    if feature is not None:
        kwargs["Feature"] = feature
    if auto_update is not None:
        kwargs["AutoUpdate"] = auto_update
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create project") from exc
    return CreateProjectResult(
        project_arn=resp.get("ProjectArn"),
    )


def create_project_version(
    project_arn: str,
    version_name: str,
    output_config: dict[str, Any],
    *,
    training_data: dict[str, Any] | None = None,
    testing_data: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    version_description: str | None = None,
    feature_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateProjectVersionResult:
    """Create project version.

    Args:
        project_arn: Project arn.
        version_name: Version name.
        output_config: Output config.
        training_data: Training data.
        testing_data: Testing data.
        tags: Tags.
        kms_key_id: Kms key id.
        version_description: Version description.
        feature_config: Feature config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    kwargs["VersionName"] = version_name
    kwargs["OutputConfig"] = output_config
    if training_data is not None:
        kwargs["TrainingData"] = training_data
    if testing_data is not None:
        kwargs["TestingData"] = testing_data
    if tags is not None:
        kwargs["Tags"] = tags
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if feature_config is not None:
        kwargs["FeatureConfig"] = feature_config
    try:
        resp = client.create_project_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create project version") from exc
    return CreateProjectVersionResult(
        project_version_arn=resp.get("ProjectVersionArn"),
    )


def create_stream_processor(
    input: dict[str, Any],
    output: dict[str, Any],
    name: str,
    settings: dict[str, Any],
    role_arn: str,
    *,
    tags: dict[str, Any] | None = None,
    notification_channel: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    regions_of_interest: list[dict[str, Any]] | None = None,
    data_sharing_preference: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateStreamProcessorResult:
    """Create stream processor.

    Args:
        input: Input.
        output: Output.
        name: Name.
        settings: Settings.
        role_arn: Role arn.
        tags: Tags.
        notification_channel: Notification channel.
        kms_key_id: Kms key id.
        regions_of_interest: Regions of interest.
        data_sharing_preference: Data sharing preference.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Input"] = input
    kwargs["Output"] = output
    kwargs["Name"] = name
    kwargs["Settings"] = settings
    kwargs["RoleArn"] = role_arn
    if tags is not None:
        kwargs["Tags"] = tags
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if regions_of_interest is not None:
        kwargs["RegionsOfInterest"] = regions_of_interest
    if data_sharing_preference is not None:
        kwargs["DataSharingPreference"] = data_sharing_preference
    try:
        resp = client.create_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create stream processor") from exc
    return CreateStreamProcessorResult(
        stream_processor_arn=resp.get("StreamProcessorArn"),
    )


def create_user(
    collection_id: str,
    user_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create user.

    Args:
        collection_id: Collection id.
        user_id: User id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["UserId"] = user_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        client.create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user") from exc
    return None


def delete_dataset(
    dataset_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset.

    Args:
        dataset_arn: Dataset arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    try:
        client.delete_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset") from exc
    return None


def delete_faces(
    collection_id: str,
    face_ids: list[str],
    region_name: str | None = None,
) -> DeleteFacesResult:
    """Delete faces.

    Args:
        collection_id: Collection id.
        face_ids: Face ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["FaceIds"] = face_ids
    try:
        resp = client.delete_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete faces") from exc
    return DeleteFacesResult(
        deleted_faces=resp.get("DeletedFaces"),
        unsuccessful_face_deletions=resp.get("UnsuccessfulFaceDeletions"),
    )


def delete_project(
    project_arn: str,
    region_name: str | None = None,
) -> DeleteProjectResult:
    """Delete project.

    Args:
        project_arn: Project arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    try:
        resp = client.delete_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete project") from exc
    return DeleteProjectResult(
        status=resp.get("Status"),
    )


def delete_project_policy(
    project_arn: str,
    policy_name: str,
    *,
    policy_revision_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete project policy.

    Args:
        project_arn: Project arn.
        policy_name: Policy name.
        policy_revision_id: Policy revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    kwargs["PolicyName"] = policy_name
    if policy_revision_id is not None:
        kwargs["PolicyRevisionId"] = policy_revision_id
    try:
        client.delete_project_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete project policy") from exc
    return None


def delete_project_version(
    project_version_arn: str,
    region_name: str | None = None,
) -> DeleteProjectVersionResult:
    """Delete project version.

    Args:
        project_version_arn: Project version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectVersionArn"] = project_version_arn
    try:
        resp = client.delete_project_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete project version") from exc
    return DeleteProjectVersionResult(
        status=resp.get("Status"),
    )


def delete_stream_processor(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete stream processor.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete stream processor") from exc
    return None


def delete_user(
    collection_id: str,
    user_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete user.

    Args:
        collection_id: Collection id.
        user_id: User id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["UserId"] = user_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        client.delete_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user") from exc
    return None


def describe_collection(
    collection_id: str,
    region_name: str | None = None,
) -> DescribeCollectionResult:
    """Describe collection.

    Args:
        collection_id: Collection id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    try:
        resp = client.describe_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe collection") from exc
    return DescribeCollectionResult(
        face_count=resp.get("FaceCount"),
        face_model_version=resp.get("FaceModelVersion"),
        collection_arn=resp.get("CollectionARN"),
        creation_timestamp=resp.get("CreationTimestamp"),
        user_count=resp.get("UserCount"),
    )


def describe_dataset(
    dataset_arn: str,
    region_name: str | None = None,
) -> DescribeDatasetResult:
    """Describe dataset.

    Args:
        dataset_arn: Dataset arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    try:
        resp = client.describe_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset") from exc
    return DescribeDatasetResult(
        dataset_description=resp.get("DatasetDescription"),
    )


def describe_project_versions(
    project_arn: str,
    *,
    version_names: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeProjectVersionsResult:
    """Describe project versions.

    Args:
        project_arn: Project arn.
        version_names: Version names.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    if version_names is not None:
        kwargs["VersionNames"] = version_names
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_project_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe project versions") from exc
    return DescribeProjectVersionsResult(
        project_version_descriptions=resp.get("ProjectVersionDescriptions"),
        next_token=resp.get("NextToken"),
    )


def describe_projects(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    project_names: list[str] | None = None,
    features: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeProjectsResult:
    """Describe projects.

    Args:
        next_token: Next token.
        max_results: Max results.
        project_names: Project names.
        features: Features.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if project_names is not None:
        kwargs["ProjectNames"] = project_names
    if features is not None:
        kwargs["Features"] = features
    try:
        resp = client.describe_projects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe projects") from exc
    return DescribeProjectsResult(
        project_descriptions=resp.get("ProjectDescriptions"),
        next_token=resp.get("NextToken"),
    )


def describe_stream_processor(
    name: str,
    region_name: str | None = None,
) -> DescribeStreamProcessorResult:
    """Describe stream processor.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stream processor") from exc
    return DescribeStreamProcessorResult(
        name=resp.get("Name"),
        stream_processor_arn=resp.get("StreamProcessorArn"),
        status=resp.get("Status"),
        status_message=resp.get("StatusMessage"),
        creation_timestamp=resp.get("CreationTimestamp"),
        last_update_timestamp=resp.get("LastUpdateTimestamp"),
        input=resp.get("Input"),
        output=resp.get("Output"),
        role_arn=resp.get("RoleArn"),
        settings=resp.get("Settings"),
        notification_channel=resp.get("NotificationChannel"),
        kms_key_id=resp.get("KmsKeyId"),
        regions_of_interest=resp.get("RegionsOfInterest"),
        data_sharing_preference=resp.get("DataSharingPreference"),
    )


def detect_custom_labels(
    project_version_arn: str,
    image: dict[str, Any],
    *,
    max_results: int | None = None,
    min_confidence: float | None = None,
    region_name: str | None = None,
) -> DetectCustomLabelsResult:
    """Detect custom labels.

    Args:
        project_version_arn: Project version arn.
        image: Image.
        max_results: Max results.
        min_confidence: Min confidence.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectVersionArn"] = project_version_arn
    kwargs["Image"] = image
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if min_confidence is not None:
        kwargs["MinConfidence"] = min_confidence
    try:
        resp = client.detect_custom_labels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect custom labels") from exc
    return DetectCustomLabelsResult(
        custom_labels=resp.get("CustomLabels"),
    )


def detect_protective_equipment(
    image: dict[str, Any],
    *,
    summarization_attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> DetectProtectiveEquipmentResult:
    """Detect protective equipment.

    Args:
        image: Image.
        summarization_attributes: Summarization attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Image"] = image
    if summarization_attributes is not None:
        kwargs["SummarizationAttributes"] = summarization_attributes
    try:
        resp = client.detect_protective_equipment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect protective equipment") from exc
    return DetectProtectiveEquipmentResult(
        protective_equipment_model_version=resp.get("ProtectiveEquipmentModelVersion"),
        persons=resp.get("Persons"),
        summary=resp.get("Summary"),
    )


def disassociate_faces(
    collection_id: str,
    user_id: str,
    face_ids: list[str],
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DisassociateFacesResult:
    """Disassociate faces.

    Args:
        collection_id: Collection id.
        user_id: User id.
        face_ids: Face ids.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["UserId"] = user_id
    kwargs["FaceIds"] = face_ids
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.disassociate_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate faces") from exc
    return DisassociateFacesResult(
        disassociated_faces=resp.get("DisassociatedFaces"),
        unsuccessful_face_disassociations=resp.get("UnsuccessfulFaceDisassociations"),
        user_status=resp.get("UserStatus"),
    )


def distribute_dataset_entries(
    datasets: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Distribute dataset entries.

    Args:
        datasets: Datasets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Datasets"] = datasets
    try:
        client.distribute_dataset_entries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to distribute dataset entries") from exc
    return None


def get_celebrity_info(
    id: str,
    region_name: str | None = None,
) -> GetCelebrityInfoResult:
    """Get celebrity info.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_celebrity_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get celebrity info") from exc
    return GetCelebrityInfoResult(
        urls=resp.get("Urls"),
        name=resp.get("Name"),
        known_gender=resp.get("KnownGender"),
    )


def get_celebrity_recognition(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    region_name: str | None = None,
) -> GetCelebrityRecognitionResult:
    """Get celebrity recognition.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    try:
        resp = client.get_celebrity_recognition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get celebrity recognition") from exc
    return GetCelebrityRecognitionResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        next_token=resp.get("NextToken"),
        celebrities=resp.get("Celebrities"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def get_content_moderation(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    aggregate_by: str | None = None,
    region_name: str | None = None,
) -> GetContentModerationResult:
    """Get content moderation.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        aggregate_by: Aggregate by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    if aggregate_by is not None:
        kwargs["AggregateBy"] = aggregate_by
    try:
        resp = client.get_content_moderation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get content moderation") from exc
    return GetContentModerationResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        moderation_labels=resp.get("ModerationLabels"),
        next_token=resp.get("NextToken"),
        moderation_model_version=resp.get("ModerationModelVersion"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
        get_request_metadata=resp.get("GetRequestMetadata"),
    )


def get_face_detection(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetFaceDetectionResult:
    """Get face detection.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_face_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get face detection") from exc
    return GetFaceDetectionResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        next_token=resp.get("NextToken"),
        faces=resp.get("Faces"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def get_face_liveness_session_results(
    session_id: str,
    region_name: str | None = None,
) -> GetFaceLivenessSessionResultsResult:
    """Get face liveness session results.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = client.get_face_liveness_session_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get face liveness session results") from exc
    return GetFaceLivenessSessionResultsResult(
        session_id=resp.get("SessionId"),
        status=resp.get("Status"),
        confidence=resp.get("Confidence"),
        reference_image=resp.get("ReferenceImage"),
        audit_images=resp.get("AuditImages"),
        challenge=resp.get("Challenge"),
    )


def get_face_search(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    region_name: str | None = None,
) -> GetFaceSearchResult:
    """Get face search.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    try:
        resp = client.get_face_search(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get face search") from exc
    return GetFaceSearchResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        next_token=resp.get("NextToken"),
        video_metadata=resp.get("VideoMetadata"),
        persons=resp.get("Persons"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def get_label_detection(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    aggregate_by: str | None = None,
    region_name: str | None = None,
) -> GetLabelDetectionResult:
    """Get label detection.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        aggregate_by: Aggregate by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    if aggregate_by is not None:
        kwargs["AggregateBy"] = aggregate_by
    try:
        resp = client.get_label_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get label detection") from exc
    return GetLabelDetectionResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        next_token=resp.get("NextToken"),
        labels=resp.get("Labels"),
        label_model_version=resp.get("LabelModelVersion"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
        get_request_metadata=resp.get("GetRequestMetadata"),
    )


def get_media_analysis_job(
    job_id: str,
    region_name: str | None = None,
) -> GetMediaAnalysisJobResult:
    """Get media analysis job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.get_media_analysis_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get media analysis job") from exc
    return GetMediaAnalysisJobResult(
        job_id=resp.get("JobId"),
        job_name=resp.get("JobName"),
        operations_config=resp.get("OperationsConfig"),
        status=resp.get("Status"),
        failure_details=resp.get("FailureDetails"),
        creation_timestamp=resp.get("CreationTimestamp"),
        completion_timestamp=resp.get("CompletionTimestamp"),
        input=resp.get("Input"),
        output_config=resp.get("OutputConfig"),
        kms_key_id=resp.get("KmsKeyId"),
        results=resp.get("Results"),
        manifest_summary=resp.get("ManifestSummary"),
    )


def get_person_tracking(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: str | None = None,
    region_name: str | None = None,
) -> GetPersonTrackingResult:
    """Get person tracking.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    try:
        resp = client.get_person_tracking(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get person tracking") from exc
    return GetPersonTrackingResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        next_token=resp.get("NextToken"),
        persons=resp.get("Persons"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def get_segment_detection(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetSegmentDetectionResult:
    """Get segment detection.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_segment_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get segment detection") from exc
    return GetSegmentDetectionResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        audio_metadata=resp.get("AudioMetadata"),
        next_token=resp.get("NextToken"),
        segments=resp.get("Segments"),
        selected_segment_types=resp.get("SelectedSegmentTypes"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def get_text_detection(
    job_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetTextDetectionResult:
    """Get text detection.

    Args:
        job_id: Job id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_text_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get text detection") from exc
    return GetTextDetectionResult(
        job_status=resp.get("JobStatus"),
        status_message=resp.get("StatusMessage"),
        video_metadata=resp.get("VideoMetadata"),
        text_detections=resp.get("TextDetections"),
        next_token=resp.get("NextToken"),
        text_model_version=resp.get("TextModelVersion"),
        job_id=resp.get("JobId"),
        video=resp.get("Video"),
        job_tag=resp.get("JobTag"),
    )


def index_faces(
    collection_id: str,
    image: dict[str, Any],
    *,
    external_image_id: str | None = None,
    detection_attributes: list[str] | None = None,
    max_faces: int | None = None,
    quality_filter: str | None = None,
    region_name: str | None = None,
) -> IndexFacesResult:
    """Index faces.

    Args:
        collection_id: Collection id.
        image: Image.
        external_image_id: External image id.
        detection_attributes: Detection attributes.
        max_faces: Max faces.
        quality_filter: Quality filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["Image"] = image
    if external_image_id is not None:
        kwargs["ExternalImageId"] = external_image_id
    if detection_attributes is not None:
        kwargs["DetectionAttributes"] = detection_attributes
    if max_faces is not None:
        kwargs["MaxFaces"] = max_faces
    if quality_filter is not None:
        kwargs["QualityFilter"] = quality_filter
    try:
        resp = client.index_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to index faces") from exc
    return IndexFacesResult(
        face_records=resp.get("FaceRecords"),
        orientation_correction=resp.get("OrientationCorrection"),
        face_model_version=resp.get("FaceModelVersion"),
        unindexed_faces=resp.get("UnindexedFaces"),
    )


def list_collections(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCollectionsResult:
    """List collections.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_collections(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list collections") from exc
    return ListCollectionsResult(
        collection_ids=resp.get("CollectionIds"),
        next_token=resp.get("NextToken"),
        face_model_versions=resp.get("FaceModelVersions"),
    )


def list_dataset_entries(
    dataset_arn: str,
    *,
    contains_labels: list[str] | None = None,
    labeled: bool | None = None,
    source_ref_contains: str | None = None,
    has_errors: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetEntriesResult:
    """List dataset entries.

    Args:
        dataset_arn: Dataset arn.
        contains_labels: Contains labels.
        labeled: Labeled.
        source_ref_contains: Source ref contains.
        has_errors: Has errors.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    if contains_labels is not None:
        kwargs["ContainsLabels"] = contains_labels
    if labeled is not None:
        kwargs["Labeled"] = labeled
    if source_ref_contains is not None:
        kwargs["SourceRefContains"] = source_ref_contains
    if has_errors is not None:
        kwargs["HasErrors"] = has_errors
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_dataset_entries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dataset entries") from exc
    return ListDatasetEntriesResult(
        dataset_entries=resp.get("DatasetEntries"),
        next_token=resp.get("NextToken"),
    )


def list_dataset_labels(
    dataset_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetLabelsResult:
    """List dataset labels.

    Args:
        dataset_arn: Dataset arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_dataset_labels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dataset labels") from exc
    return ListDatasetLabelsResult(
        dataset_label_descriptions=resp.get("DatasetLabelDescriptions"),
        next_token=resp.get("NextToken"),
    )


def list_faces(
    collection_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    user_id: str | None = None,
    face_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ListFacesResult:
    """List faces.

    Args:
        collection_id: Collection id.
        next_token: Next token.
        max_results: Max results.
        user_id: User id.
        face_ids: Face ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if user_id is not None:
        kwargs["UserId"] = user_id
    if face_ids is not None:
        kwargs["FaceIds"] = face_ids
    try:
        resp = client.list_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list faces") from exc
    return ListFacesResult(
        faces=resp.get("Faces"),
        next_token=resp.get("NextToken"),
        face_model_version=resp.get("FaceModelVersion"),
    )


def list_media_analysis_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMediaAnalysisJobsResult:
    """List media analysis jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_media_analysis_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list media analysis jobs") from exc
    return ListMediaAnalysisJobsResult(
        next_token=resp.get("NextToken"),
        media_analysis_jobs=resp.get("MediaAnalysisJobs"),
    )


def list_project_policies(
    project_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListProjectPoliciesResult:
    """List project policies.

    Args:
        project_arn: Project arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_project_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list project policies") from exc
    return ListProjectPoliciesResult(
        project_policies=resp.get("ProjectPolicies"),
        next_token=resp.get("NextToken"),
    )


def list_stream_processors(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStreamProcessorsResult:
    """List stream processors.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_stream_processors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stream processors") from exc
    return ListStreamProcessorsResult(
        next_token=resp.get("NextToken"),
        stream_processors=resp.get("StreamProcessors"),
    )


def list_tags_for_resource(
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
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_users(
    collection_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListUsersResult:
    """List users.

    Args:
        collection_id: Collection id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list users") from exc
    return ListUsersResult(
        users=resp.get("Users"),
        next_token=resp.get("NextToken"),
    )


def put_project_policy(
    project_arn: str,
    policy_name: str,
    policy_document: str,
    *,
    policy_revision_id: str | None = None,
    region_name: str | None = None,
) -> PutProjectPolicyResult:
    """Put project policy.

    Args:
        project_arn: Project arn.
        policy_name: Policy name.
        policy_document: Policy document.
        policy_revision_id: Policy revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectArn"] = project_arn
    kwargs["PolicyName"] = policy_name
    kwargs["PolicyDocument"] = policy_document
    if policy_revision_id is not None:
        kwargs["PolicyRevisionId"] = policy_revision_id
    try:
        resp = client.put_project_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put project policy") from exc
    return PutProjectPolicyResult(
        policy_revision_id=resp.get("PolicyRevisionId"),
    )


def recognize_celebrities(
    image: dict[str, Any],
    region_name: str | None = None,
) -> RecognizeCelebritiesResult:
    """Recognize celebrities.

    Args:
        image: Image.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Image"] = image
    try:
        resp = client.recognize_celebrities(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to recognize celebrities") from exc
    return RecognizeCelebritiesResult(
        celebrity_faces=resp.get("CelebrityFaces"),
        unrecognized_faces=resp.get("UnrecognizedFaces"),
        orientation_correction=resp.get("OrientationCorrection"),
    )


def search_faces(
    collection_id: str,
    face_id: str,
    *,
    max_faces: int | None = None,
    face_match_threshold: float | None = None,
    region_name: str | None = None,
) -> SearchFacesResult:
    """Search faces.

    Args:
        collection_id: Collection id.
        face_id: Face id.
        max_faces: Max faces.
        face_match_threshold: Face match threshold.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["FaceId"] = face_id
    if max_faces is not None:
        kwargs["MaxFaces"] = max_faces
    if face_match_threshold is not None:
        kwargs["FaceMatchThreshold"] = face_match_threshold
    try:
        resp = client.search_faces(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search faces") from exc
    return SearchFacesResult(
        searched_face_id=resp.get("SearchedFaceId"),
        face_matches=resp.get("FaceMatches"),
        face_model_version=resp.get("FaceModelVersion"),
    )


def search_faces_by_image(
    collection_id: str,
    image: dict[str, Any],
    *,
    max_faces: int | None = None,
    face_match_threshold: float | None = None,
    quality_filter: str | None = None,
    region_name: str | None = None,
) -> SearchFacesByImageResult:
    """Search faces by image.

    Args:
        collection_id: Collection id.
        image: Image.
        max_faces: Max faces.
        face_match_threshold: Face match threshold.
        quality_filter: Quality filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["Image"] = image
    if max_faces is not None:
        kwargs["MaxFaces"] = max_faces
    if face_match_threshold is not None:
        kwargs["FaceMatchThreshold"] = face_match_threshold
    if quality_filter is not None:
        kwargs["QualityFilter"] = quality_filter
    try:
        resp = client.search_faces_by_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search faces by image") from exc
    return SearchFacesByImageResult(
        searched_face_bounding_box=resp.get("SearchedFaceBoundingBox"),
        searched_face_confidence=resp.get("SearchedFaceConfidence"),
        face_matches=resp.get("FaceMatches"),
        face_model_version=resp.get("FaceModelVersion"),
    )


def search_users(
    collection_id: str,
    *,
    user_id: str | None = None,
    face_id: str | None = None,
    user_match_threshold: float | None = None,
    max_users: int | None = None,
    region_name: str | None = None,
) -> SearchUsersResult:
    """Search users.

    Args:
        collection_id: Collection id.
        user_id: User id.
        face_id: Face id.
        user_match_threshold: User match threshold.
        max_users: Max users.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    if user_id is not None:
        kwargs["UserId"] = user_id
    if face_id is not None:
        kwargs["FaceId"] = face_id
    if user_match_threshold is not None:
        kwargs["UserMatchThreshold"] = user_match_threshold
    if max_users is not None:
        kwargs["MaxUsers"] = max_users
    try:
        resp = client.search_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search users") from exc
    return SearchUsersResult(
        user_matches=resp.get("UserMatches"),
        face_model_version=resp.get("FaceModelVersion"),
        searched_face=resp.get("SearchedFace"),
        searched_user=resp.get("SearchedUser"),
    )


def search_users_by_image(
    collection_id: str,
    image: dict[str, Any],
    *,
    user_match_threshold: float | None = None,
    max_users: int | None = None,
    quality_filter: str | None = None,
    region_name: str | None = None,
) -> SearchUsersByImageResult:
    """Search users by image.

    Args:
        collection_id: Collection id.
        image: Image.
        user_match_threshold: User match threshold.
        max_users: Max users.
        quality_filter: Quality filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    kwargs["Image"] = image
    if user_match_threshold is not None:
        kwargs["UserMatchThreshold"] = user_match_threshold
    if max_users is not None:
        kwargs["MaxUsers"] = max_users
    if quality_filter is not None:
        kwargs["QualityFilter"] = quality_filter
    try:
        resp = client.search_users_by_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search users by image") from exc
    return SearchUsersByImageResult(
        user_matches=resp.get("UserMatches"),
        face_model_version=resp.get("FaceModelVersion"),
        searched_face=resp.get("SearchedFace"),
        unsearched_faces=resp.get("UnsearchedFaces"),
    )


def start_celebrity_recognition(
    video: dict[str, Any],
    *,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    region_name: str | None = None,
) -> StartCelebrityRecognitionResult:
    """Start celebrity recognition.

    Args:
        video: Video.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        job_tag: Job tag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    try:
        resp = client.start_celebrity_recognition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start celebrity recognition") from exc
    return StartCelebrityRecognitionResult(
        job_id=resp.get("JobId"),
    )


def start_content_moderation(
    video: dict[str, Any],
    *,
    min_confidence: float | None = None,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    region_name: str | None = None,
) -> StartContentModerationResult:
    """Start content moderation.

    Args:
        video: Video.
        min_confidence: Min confidence.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        job_tag: Job tag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if min_confidence is not None:
        kwargs["MinConfidence"] = min_confidence
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    try:
        resp = client.start_content_moderation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start content moderation") from exc
    return StartContentModerationResult(
        job_id=resp.get("JobId"),
    )


def start_face_detection(
    video: dict[str, Any],
    *,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    face_attributes: str | None = None,
    job_tag: str | None = None,
    region_name: str | None = None,
) -> StartFaceDetectionResult:
    """Start face detection.

    Args:
        video: Video.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        face_attributes: Face attributes.
        job_tag: Job tag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if face_attributes is not None:
        kwargs["FaceAttributes"] = face_attributes
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    try:
        resp = client.start_face_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start face detection") from exc
    return StartFaceDetectionResult(
        job_id=resp.get("JobId"),
    )


def start_face_search(
    video: dict[str, Any],
    collection_id: str,
    *,
    client_request_token: str | None = None,
    face_match_threshold: float | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    region_name: str | None = None,
) -> StartFaceSearchResult:
    """Start face search.

    Args:
        video: Video.
        collection_id: Collection id.
        client_request_token: Client request token.
        face_match_threshold: Face match threshold.
        notification_channel: Notification channel.
        job_tag: Job tag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    kwargs["CollectionId"] = collection_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if face_match_threshold is not None:
        kwargs["FaceMatchThreshold"] = face_match_threshold
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    try:
        resp = client.start_face_search(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start face search") from exc
    return StartFaceSearchResult(
        job_id=resp.get("JobId"),
    )


def start_label_detection(
    video: dict[str, Any],
    *,
    client_request_token: str | None = None,
    min_confidence: float | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    features: list[str] | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartLabelDetectionResult:
    """Start label detection.

    Args:
        video: Video.
        client_request_token: Client request token.
        min_confidence: Min confidence.
        notification_channel: Notification channel.
        job_tag: Job tag.
        features: Features.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if min_confidence is not None:
        kwargs["MinConfidence"] = min_confidence
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if features is not None:
        kwargs["Features"] = features
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = client.start_label_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start label detection") from exc
    return StartLabelDetectionResult(
        job_id=resp.get("JobId"),
    )


def start_media_analysis_job(
    operations_config: dict[str, Any],
    input: dict[str, Any],
    output_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    job_name: str | None = None,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> StartMediaAnalysisJobResult:
    """Start media analysis job.

    Args:
        operations_config: Operations config.
        input: Input.
        output_config: Output config.
        client_request_token: Client request token.
        job_name: Job name.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OperationsConfig"] = operations_config
    kwargs["Input"] = input
    kwargs["OutputConfig"] = output_config
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if job_name is not None:
        kwargs["JobName"] = job_name
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    try:
        resp = client.start_media_analysis_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start media analysis job") from exc
    return StartMediaAnalysisJobResult(
        job_id=resp.get("JobId"),
    )


def start_person_tracking(
    video: dict[str, Any],
    *,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    region_name: str | None = None,
) -> StartPersonTrackingResult:
    """Start person tracking.

    Args:
        video: Video.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        job_tag: Job tag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    try:
        resp = client.start_person_tracking(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start person tracking") from exc
    return StartPersonTrackingResult(
        job_id=resp.get("JobId"),
    )


def start_project_version(
    project_version_arn: str,
    min_inference_units: int,
    *,
    max_inference_units: int | None = None,
    region_name: str | None = None,
) -> StartProjectVersionResult:
    """Start project version.

    Args:
        project_version_arn: Project version arn.
        min_inference_units: Min inference units.
        max_inference_units: Max inference units.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectVersionArn"] = project_version_arn
    kwargs["MinInferenceUnits"] = min_inference_units
    if max_inference_units is not None:
        kwargs["MaxInferenceUnits"] = max_inference_units
    try:
        resp = client.start_project_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start project version") from exc
    return StartProjectVersionResult(
        status=resp.get("Status"),
    )


def start_segment_detection(
    video: dict[str, Any],
    segment_types: list[str],
    *,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartSegmentDetectionResult:
    """Start segment detection.

    Args:
        video: Video.
        segment_types: Segment types.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        job_tag: Job tag.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    kwargs["SegmentTypes"] = segment_types
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.start_segment_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start segment detection") from exc
    return StartSegmentDetectionResult(
        job_id=resp.get("JobId"),
    )


def start_stream_processor(
    name: str,
    *,
    start_selector: dict[str, Any] | None = None,
    stop_selector: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartStreamProcessorResult:
    """Start stream processor.

    Args:
        name: Name.
        start_selector: Start selector.
        stop_selector: Stop selector.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if start_selector is not None:
        kwargs["StartSelector"] = start_selector
    if stop_selector is not None:
        kwargs["StopSelector"] = stop_selector
    try:
        resp = client.start_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start stream processor") from exc
    return StartStreamProcessorResult(
        session_id=resp.get("SessionId"),
    )


def start_text_detection(
    video: dict[str, Any],
    *,
    client_request_token: str | None = None,
    notification_channel: dict[str, Any] | None = None,
    job_tag: str | None = None,
    filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartTextDetectionResult:
    """Start text detection.

    Args:
        video: Video.
        client_request_token: Client request token.
        notification_channel: Notification channel.
        job_tag: Job tag.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Video"] = video
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if notification_channel is not None:
        kwargs["NotificationChannel"] = notification_channel
    if job_tag is not None:
        kwargs["JobTag"] = job_tag
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.start_text_detection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start text detection") from exc
    return StartTextDetectionResult(
        job_id=resp.get("JobId"),
    )


def stop_project_version(
    project_version_arn: str,
    region_name: str | None = None,
) -> StopProjectVersionResult:
    """Stop project version.

    Args:
        project_version_arn: Project version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProjectVersionArn"] = project_version_arn
    try:
        resp = client.stop_project_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop project version") from exc
    return StopProjectVersionResult(
        status=resp.get("Status"),
    )


def stop_stream_processor(
    name: str,
    region_name: str | None = None,
) -> None:
    """Stop stream processor.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.stop_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop stream processor") from exc
    return None


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_dataset_entries(
    dataset_arn: str,
    changes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update dataset entries.

    Args:
        dataset_arn: Dataset arn.
        changes: Changes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    kwargs["Changes"] = changes
    try:
        client.update_dataset_entries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update dataset entries") from exc
    return None


def update_stream_processor(
    name: str,
    *,
    settings_for_update: dict[str, Any] | None = None,
    regions_of_interest_for_update: list[dict[str, Any]] | None = None,
    data_sharing_preference_for_update: dict[str, Any] | None = None,
    parameters_to_delete: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Update stream processor.

    Args:
        name: Name.
        settings_for_update: Settings for update.
        regions_of_interest_for_update: Regions of interest for update.
        data_sharing_preference_for_update: Data sharing preference for update.
        parameters_to_delete: Parameters to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rekognition", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if settings_for_update is not None:
        kwargs["SettingsForUpdate"] = settings_for_update
    if regions_of_interest_for_update is not None:
        kwargs["RegionsOfInterestForUpdate"] = regions_of_interest_for_update
    if data_sharing_preference_for_update is not None:
        kwargs["DataSharingPreferenceForUpdate"] = data_sharing_preference_for_update
    if parameters_to_delete is not None:
        kwargs["ParametersToDelete"] = parameters_to_delete
    try:
        client.update_stream_processor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update stream processor") from exc
    return None
