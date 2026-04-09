from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CreateCallAnalyticsCategoryResult",
    "CreateLanguageModelResult",
    "CreateMedicalVocabularyResult",
    "CreateVocabularyFilterResult",
    "DescribeLanguageModelResult",
    "GetCallAnalyticsCategoryResult",
    "GetCallAnalyticsJobResult",
    "GetMedicalScribeJobResult",
    "GetMedicalTranscriptionJobResult",
    "GetMedicalVocabularyResult",
    "GetVocabularyFilterResult",
    "ListCallAnalyticsCategoriesResult",
    "ListCallAnalyticsJobsResult",
    "ListLanguageModelsResult",
    "ListMedicalScribeJobsResult",
    "ListMedicalTranscriptionJobsResult",
    "ListMedicalVocabulariesResult",
    "ListTagsForResourceResult",
    "ListVocabularyFiltersResult",
    "StartCallAnalyticsJobResult",
    "StartMedicalScribeJobResult",
    "StartMedicalTranscriptionJobResult",
    "TranscriptionJob",
    "UpdateCallAnalyticsCategoryResult",
    "UpdateMedicalVocabularyResult",
    "UpdateVocabularyFilterResult",
    "UpdateVocabularyResult",
    "VocabularyInfo",
    "create_call_analytics_category",
    "create_language_model",
    "create_medical_vocabulary",
    "create_vocabulary",
    "create_vocabulary_filter",
    "delete_call_analytics_category",
    "delete_call_analytics_job",
    "delete_language_model",
    "delete_medical_scribe_job",
    "delete_medical_transcription_job",
    "delete_medical_vocabulary",
    "delete_transcription_job",
    "delete_vocabulary",
    "delete_vocabulary_filter",
    "describe_language_model",
    "get_call_analytics_category",
    "get_call_analytics_job",
    "get_medical_scribe_job",
    "get_medical_transcription_job",
    "get_medical_vocabulary",
    "get_transcription_job",
    "get_vocabulary",
    "get_vocabulary_filter",
    "list_call_analytics_categories",
    "list_call_analytics_jobs",
    "list_language_models",
    "list_medical_scribe_jobs",
    "list_medical_transcription_jobs",
    "list_medical_vocabularies",
    "list_tags_for_resource",
    "list_transcription_jobs",
    "list_vocabularies",
    "list_vocabulary_filters",
    "start_call_analytics_job",
    "start_medical_scribe_job",
    "start_medical_transcription_job",
    "start_transcription_job",
    "tag_resource",
    "transcribe_and_wait",
    "untag_resource",
    "update_call_analytics_category",
    "update_medical_vocabulary",
    "update_vocabulary",
    "update_vocabulary_filter",
    "wait_for_transcription_job",
]

_TERMINAL_STATUSES = {"COMPLETED", "FAILED"}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TranscriptionJob(BaseModel):
    """Represents an Amazon Transcribe transcription job."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    job_name: str
    job_status: str
    language_code: str | None = None
    media_uri: str | None = None
    transcript_uri: str | None = None
    failure_reason: str | None = None

    @property
    def completed(self) -> bool:
        """``True`` if the job completed successfully."""
        return self.job_status == "COMPLETED"


class VocabularyInfo(BaseModel):
    """Represents an Amazon Transcribe custom vocabulary."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    vocabulary_name: str
    language_code: str
    vocabulary_state: str | None = None
    last_modified_time: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_job(raw: dict[str, Any]) -> TranscriptionJob:
    """Convert a raw API TranscriptionJob dict to a model."""
    transcript_uri: str | None = None
    transcript = raw.get("Transcript")
    if transcript:
        transcript_uri = transcript.get("TranscriptFileUri")
    media_uri: str | None = None
    media = raw.get("Media")
    if media:
        media_uri = media.get("MediaFileUri")
    return TranscriptionJob(
        job_name=raw["TranscriptionJobName"],
        job_status=raw["TranscriptionJobStatus"],
        language_code=raw.get("LanguageCode"),
        media_uri=media_uri,
        transcript_uri=transcript_uri,
        failure_reason=raw.get("FailureReason"),
    )


def _parse_vocabulary(raw: dict[str, Any]) -> VocabularyInfo:
    """Convert a raw API vocabulary dict to a model."""
    last_mod = raw.get("LastModifiedTime")
    return VocabularyInfo(
        vocabulary_name=raw["VocabularyName"],
        language_code=raw["LanguageCode"],
        vocabulary_state=raw.get("VocabularyState"),
        last_modified_time=str(last_mod) if last_mod is not None else None,
    )


# ---------------------------------------------------------------------------
# Transcription job operations
# ---------------------------------------------------------------------------


def start_transcription_job(
    job_name: str,
    media_uri: str,
    language_code: str = "en-US",
    media_format: str | None = None,
    output_bucket: str | None = None,
    output_key: str | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> TranscriptionJob:
    """Start a new transcription job.

    Args:
        job_name: Unique name for the transcription job.
        media_uri: S3 URI of the media file (e.g. ``s3://bucket/audio.mp3``).
        language_code: BCP-47 language code (default ``"en-US"``).
        media_format: Media format (``mp3``, ``mp4``, ``wav``, ``flac``).
            If ``None``, Transcribe auto-detects.
        output_bucket: Optional S3 bucket for the transcript output.
        output_key: Optional S3 key for the transcript output.
        settings: Optional additional job settings dict.
        region_name: AWS region override.

    Returns:
        A :class:`TranscriptionJob` with the initial job status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {
        "TranscriptionJobName": job_name,
        "LanguageCode": language_code,
        "Media": {"MediaFileUri": media_uri},
    }
    if media_format:
        kwargs["MediaFormat"] = media_format
    if output_bucket:
        kwargs["OutputBucketName"] = output_bucket
    if output_key:
        kwargs["OutputKey"] = output_key
    if settings:
        kwargs["Settings"] = settings
    try:
        resp = client.start_transcription_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_transcription_job failed for {job_name!r}") from exc
    return _parse_job(resp["TranscriptionJob"])


def get_transcription_job(
    job_name: str,
    region_name: str | None = None,
) -> TranscriptionJob:
    """Get the status and details of a transcription job.

    Args:
        job_name: Name of the transcription job.
        region_name: AWS region override.

    Returns:
        A :class:`TranscriptionJob` with current status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    try:
        resp = client.get_transcription_job(
            TranscriptionJobName=job_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_transcription_job failed for {job_name!r}") from exc
    return _parse_job(resp["TranscriptionJob"])


def list_transcription_jobs(
    status: str | None = None,
    job_name_contains: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[TranscriptionJob]:
    """List transcription jobs with optional filters.

    Args:
        status: Filter by job status (``IN_PROGRESS``, ``FAILED``,
            ``COMPLETED``, ``QUEUED``).
        job_name_contains: Filter by substring in the job name.
        max_results: Maximum number of results to return.
        region_name: AWS region override.

    Returns:
        A list of :class:`TranscriptionJob` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if status:
        kwargs["Status"] = status
    if job_name_contains:
        kwargs["JobNameContains"] = job_name_contains
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    jobs: list[TranscriptionJob] = []
    try:
        while True:
            resp = client.list_transcription_jobs(**kwargs)
            for raw in resp.get("TranscriptionJobSummaries", []):
                jobs.append(_parse_job(raw))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_transcription_jobs failed") from exc
    return jobs


def delete_transcription_job(
    job_name: str,
    region_name: str | None = None,
) -> None:
    """Delete a transcription job.

    Args:
        job_name: Name of the transcription job to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    try:
        client.delete_transcription_job(
            TranscriptionJobName=job_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_transcription_job failed for {job_name!r}") from exc


# ---------------------------------------------------------------------------
# Vocabulary operations
# ---------------------------------------------------------------------------


def create_vocabulary(
    vocabulary_name: str,
    language_code: str,
    phrases: list[str] | None = None,
    vocabulary_file_uri: str | None = None,
    region_name: str | None = None,
) -> VocabularyInfo:
    """Create a custom vocabulary for improved transcription accuracy.

    Provide either *phrases* (inline list) or *vocabulary_file_uri*
    (S3 URI to a vocabulary file), but not both.

    Args:
        vocabulary_name: Name for the vocabulary.
        language_code: BCP-47 language code (e.g. ``"en-US"``).
        phrases: List of words/phrases to include.
        vocabulary_file_uri: S3 URI to a vocabulary text file.
        region_name: AWS region override.

    Returns:
        A :class:`VocabularyInfo` with the vocabulary state.

    Raises:
        ValueError: If neither phrases nor vocabulary_file_uri is provided.
        RuntimeError: If the API call fails.
    """
    if not phrases and not vocabulary_file_uri:
        raise ValueError("Provide either phrases or vocabulary_file_uri")
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {
        "VocabularyName": vocabulary_name,
        "LanguageCode": language_code,
    }
    if phrases:
        kwargs["Phrases"] = phrases
    if vocabulary_file_uri:
        kwargs["VocabularyFileUri"] = vocabulary_file_uri
    try:
        resp = client.create_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_vocabulary failed for {vocabulary_name!r}") from exc
    return _parse_vocabulary(resp)


def get_vocabulary(
    vocabulary_name: str,
    region_name: str | None = None,
) -> VocabularyInfo:
    """Get details of a custom vocabulary.

    Args:
        vocabulary_name: Name of the vocabulary.
        region_name: AWS region override.

    Returns:
        A :class:`VocabularyInfo` with vocabulary details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    try:
        resp = client.get_vocabulary(VocabularyName=vocabulary_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_vocabulary failed for {vocabulary_name!r}") from exc
    return _parse_vocabulary(resp)


def list_vocabularies(
    state_equals: str | None = None,
    name_contains: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[VocabularyInfo]:
    """List custom vocabularies with optional filters.

    Args:
        state_equals: Filter by vocabulary state (``PENDING``, ``READY``,
            ``FAILED``).
        name_contains: Filter by substring in vocabulary name.
        max_results: Maximum number of results to return.
        region_name: AWS region override.

    Returns:
        A list of :class:`VocabularyInfo` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if state_equals:
        kwargs["StateEquals"] = state_equals
    if name_contains:
        kwargs["NameContains"] = name_contains
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    vocabs: list[VocabularyInfo] = []
    try:
        while True:
            resp = client.list_vocabularies(**kwargs)
            for raw in resp.get("Vocabularies", []):
                vocabs.append(_parse_vocabulary(raw))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_vocabularies failed") from exc
    return vocabs


def delete_vocabulary(
    vocabulary_name: str,
    region_name: str | None = None,
) -> None:
    """Delete a custom vocabulary.

    Args:
        vocabulary_name: Name of the vocabulary to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    try:
        client.delete_vocabulary(VocabularyName=vocabulary_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_vocabulary failed for {vocabulary_name!r}") from exc


# ---------------------------------------------------------------------------
# Polling / composite utilities
# ---------------------------------------------------------------------------


def wait_for_transcription_job(
    job_name: str,
    poll_interval: float = 5.0,
    timeout: float = 600.0,
    region_name: str | None = None,
) -> TranscriptionJob:
    """Poll until a transcription job reaches a terminal status.

    Args:
        job_name: Name of the transcription job to wait for.
        poll_interval: Seconds between status checks (default ``5``).
        timeout: Maximum seconds to wait (default ``600``).
        region_name: AWS region override.

    Returns:
        The final :class:`TranscriptionJob`.

    Raises:
        TimeoutError: If the job does not finish within *timeout*.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = get_transcription_job(job_name, region_name=region_name)
        if result.job_status in _TERMINAL_STATUSES:
            return result
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Transcription job {job_name!r} did not finish within {timeout}s")
        time.sleep(poll_interval)


def transcribe_and_wait(
    job_name: str,
    media_uri: str,
    language_code: str = "en-US",
    media_format: str | None = None,
    output_bucket: str | None = None,
    output_key: str | None = None,
    settings: dict[str, Any] | None = None,
    poll_interval: float = 5.0,
    timeout: float = 600.0,
    region_name: str | None = None,
) -> TranscriptionJob:
    """Start a transcription job and wait for it to complete.

    This is a convenience wrapper that calls
    :func:`start_transcription_job` followed by
    :func:`wait_for_transcription_job`.

    Args:
        job_name: Unique name for the transcription job.
        media_uri: S3 URI of the media file.
        language_code: BCP-47 language code (default ``"en-US"``).
        media_format: Media format (``mp3``, ``mp4``, ``wav``, ``flac``).
        output_bucket: Optional S3 bucket for the transcript output.
        output_key: Optional S3 key for the transcript output.
        settings: Optional additional job settings dict.
        poll_interval: Seconds between status checks (default ``5``).
        timeout: Maximum seconds to wait (default ``600``).
        region_name: AWS region override.

    Returns:
        The final :class:`TranscriptionJob`.

    Raises:
        RuntimeError: If starting the job fails.
        TimeoutError: If the job does not finish within *timeout*.
    """
    start_transcription_job(
        job_name=job_name,
        media_uri=media_uri,
        language_code=language_code,
        media_format=media_format,
        output_bucket=output_bucket,
        output_key=output_key,
        settings=settings,
        region_name=region_name,
    )
    return wait_for_transcription_job(
        job_name=job_name,
        poll_interval=poll_interval,
        timeout=timeout,
        region_name=region_name,
    )


class CreateCallAnalyticsCategoryResult(BaseModel):
    """Result of create_call_analytics_category."""

    model_config = ConfigDict(frozen=True)

    category_properties: dict[str, Any] | None = None


class CreateLanguageModelResult(BaseModel):
    """Result of create_language_model."""

    model_config = ConfigDict(frozen=True)

    language_code: str | None = None
    base_model_name: str | None = None
    model_name: str | None = None
    input_data_config: dict[str, Any] | None = None
    model_status: str | None = None


class CreateMedicalVocabularyResult(BaseModel):
    """Result of create_medical_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_name: str | None = None
    language_code: str | None = None
    vocabulary_state: str | None = None
    last_modified_time: str | None = None
    failure_reason: str | None = None


class CreateVocabularyFilterResult(BaseModel):
    """Result of create_vocabulary_filter."""

    model_config = ConfigDict(frozen=True)

    vocabulary_filter_name: str | None = None
    language_code: str | None = None
    last_modified_time: str | None = None


class DescribeLanguageModelResult(BaseModel):
    """Result of describe_language_model."""

    model_config = ConfigDict(frozen=True)

    language_model: dict[str, Any] | None = None


class GetCallAnalyticsCategoryResult(BaseModel):
    """Result of get_call_analytics_category."""

    model_config = ConfigDict(frozen=True)

    category_properties: dict[str, Any] | None = None


class GetCallAnalyticsJobResult(BaseModel):
    """Result of get_call_analytics_job."""

    model_config = ConfigDict(frozen=True)

    call_analytics_job: dict[str, Any] | None = None


class GetMedicalScribeJobResult(BaseModel):
    """Result of get_medical_scribe_job."""

    model_config = ConfigDict(frozen=True)

    medical_scribe_job: dict[str, Any] | None = None


class GetMedicalTranscriptionJobResult(BaseModel):
    """Result of get_medical_transcription_job."""

    model_config = ConfigDict(frozen=True)

    medical_transcription_job: dict[str, Any] | None = None


class GetMedicalVocabularyResult(BaseModel):
    """Result of get_medical_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_name: str | None = None
    language_code: str | None = None
    vocabulary_state: str | None = None
    last_modified_time: str | None = None
    failure_reason: str | None = None
    download_uri: str | None = None


class GetVocabularyFilterResult(BaseModel):
    """Result of get_vocabulary_filter."""

    model_config = ConfigDict(frozen=True)

    vocabulary_filter_name: str | None = None
    language_code: str | None = None
    last_modified_time: str | None = None
    download_uri: str | None = None


class ListCallAnalyticsCategoriesResult(BaseModel):
    """Result of list_call_analytics_categories."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    categories: list[dict[str, Any]] | None = None


class ListCallAnalyticsJobsResult(BaseModel):
    """Result of list_call_analytics_jobs."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    next_token: str | None = None
    call_analytics_job_summaries: list[dict[str, Any]] | None = None


class ListLanguageModelsResult(BaseModel):
    """Result of list_language_models."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    models: list[dict[str, Any]] | None = None


class ListMedicalScribeJobsResult(BaseModel):
    """Result of list_medical_scribe_jobs."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    next_token: str | None = None
    medical_scribe_job_summaries: list[dict[str, Any]] | None = None


class ListMedicalTranscriptionJobsResult(BaseModel):
    """Result of list_medical_transcription_jobs."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    next_token: str | None = None
    medical_transcription_job_summaries: list[dict[str, Any]] | None = None


class ListMedicalVocabulariesResult(BaseModel):
    """Result of list_medical_vocabularies."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    next_token: str | None = None
    vocabularies: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    tags: list[dict[str, Any]] | None = None


class ListVocabularyFiltersResult(BaseModel):
    """Result of list_vocabulary_filters."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    vocabulary_filters: list[dict[str, Any]] | None = None


class StartCallAnalyticsJobResult(BaseModel):
    """Result of start_call_analytics_job."""

    model_config = ConfigDict(frozen=True)

    call_analytics_job: dict[str, Any] | None = None


class StartMedicalScribeJobResult(BaseModel):
    """Result of start_medical_scribe_job."""

    model_config = ConfigDict(frozen=True)

    medical_scribe_job: dict[str, Any] | None = None


class StartMedicalTranscriptionJobResult(BaseModel):
    """Result of start_medical_transcription_job."""

    model_config = ConfigDict(frozen=True)

    medical_transcription_job: dict[str, Any] | None = None


class UpdateCallAnalyticsCategoryResult(BaseModel):
    """Result of update_call_analytics_category."""

    model_config = ConfigDict(frozen=True)

    category_properties: dict[str, Any] | None = None


class UpdateMedicalVocabularyResult(BaseModel):
    """Result of update_medical_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_name: str | None = None
    language_code: str | None = None
    last_modified_time: str | None = None
    vocabulary_state: str | None = None


class UpdateVocabularyResult(BaseModel):
    """Result of update_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_name: str | None = None
    language_code: str | None = None
    last_modified_time: str | None = None
    vocabulary_state: str | None = None


class UpdateVocabularyFilterResult(BaseModel):
    """Result of update_vocabulary_filter."""

    model_config = ConfigDict(frozen=True)

    vocabulary_filter_name: str | None = None
    language_code: str | None = None
    last_modified_time: str | None = None


def create_call_analytics_category(
    category_name: str,
    rules: list[dict[str, Any]],
    *,
    tags: list[dict[str, Any]] | None = None,
    input_type: str | None = None,
    region_name: str | None = None,
) -> CreateCallAnalyticsCategoryResult:
    """Create call analytics category.

    Args:
        category_name: Category name.
        rules: Rules.
        tags: Tags.
        input_type: Input type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CategoryName"] = category_name
    kwargs["Rules"] = rules
    if tags is not None:
        kwargs["Tags"] = tags
    if input_type is not None:
        kwargs["InputType"] = input_type
    try:
        resp = client.create_call_analytics_category(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create call analytics category") from exc
    return CreateCallAnalyticsCategoryResult(
        category_properties=resp.get("CategoryProperties"),
    )


def create_language_model(
    language_code: str,
    base_model_name: str,
    model_name: str,
    input_data_config: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateLanguageModelResult:
    """Create language model.

    Args:
        language_code: Language code.
        base_model_name: Base model name.
        model_name: Model name.
        input_data_config: Input data config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LanguageCode"] = language_code
    kwargs["BaseModelName"] = base_model_name
    kwargs["ModelName"] = model_name
    kwargs["InputDataConfig"] = input_data_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_language_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create language model") from exc
    return CreateLanguageModelResult(
        language_code=resp.get("LanguageCode"),
        base_model_name=resp.get("BaseModelName"),
        model_name=resp.get("ModelName"),
        input_data_config=resp.get("InputDataConfig"),
        model_status=resp.get("ModelStatus"),
    )


def create_medical_vocabulary(
    vocabulary_name: str,
    language_code: str,
    vocabulary_file_uri: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMedicalVocabularyResult:
    """Create medical vocabulary.

    Args:
        vocabulary_name: Vocabulary name.
        language_code: Language code.
        vocabulary_file_uri: Vocabulary file uri.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyName"] = vocabulary_name
    kwargs["LanguageCode"] = language_code
    kwargs["VocabularyFileUri"] = vocabulary_file_uri
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_medical_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create medical vocabulary") from exc
    return CreateMedicalVocabularyResult(
        vocabulary_name=resp.get("VocabularyName"),
        language_code=resp.get("LanguageCode"),
        vocabulary_state=resp.get("VocabularyState"),
        last_modified_time=resp.get("LastModifiedTime"),
        failure_reason=resp.get("FailureReason"),
    )


def create_vocabulary_filter(
    vocabulary_filter_name: str,
    language_code: str,
    *,
    words: list[str] | None = None,
    vocabulary_filter_file_uri: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    data_access_role_arn: str | None = None,
    region_name: str | None = None,
) -> CreateVocabularyFilterResult:
    """Create vocabulary filter.

    Args:
        vocabulary_filter_name: Vocabulary filter name.
        language_code: Language code.
        words: Words.
        vocabulary_filter_file_uri: Vocabulary filter file uri.
        tags: Tags.
        data_access_role_arn: Data access role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyFilterName"] = vocabulary_filter_name
    kwargs["LanguageCode"] = language_code
    if words is not None:
        kwargs["Words"] = words
    if vocabulary_filter_file_uri is not None:
        kwargs["VocabularyFilterFileUri"] = vocabulary_filter_file_uri
    if tags is not None:
        kwargs["Tags"] = tags
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    try:
        resp = client.create_vocabulary_filter(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vocabulary filter") from exc
    return CreateVocabularyFilterResult(
        vocabulary_filter_name=resp.get("VocabularyFilterName"),
        language_code=resp.get("LanguageCode"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def delete_call_analytics_category(
    category_name: str,
    region_name: str | None = None,
) -> None:
    """Delete call analytics category.

    Args:
        category_name: Category name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CategoryName"] = category_name
    try:
        client.delete_call_analytics_category(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete call analytics category") from exc
    return None


def delete_call_analytics_job(
    call_analytics_job_name: str,
    region_name: str | None = None,
) -> None:
    """Delete call analytics job.

    Args:
        call_analytics_job_name: Call analytics job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallAnalyticsJobName"] = call_analytics_job_name
    try:
        client.delete_call_analytics_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete call analytics job") from exc
    return None


def delete_language_model(
    model_name: str,
    region_name: str | None = None,
) -> None:
    """Delete language model.

    Args:
        model_name: Model name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ModelName"] = model_name
    try:
        client.delete_language_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete language model") from exc
    return None


def delete_medical_scribe_job(
    medical_scribe_job_name: str,
    region_name: str | None = None,
) -> None:
    """Delete medical scribe job.

    Args:
        medical_scribe_job_name: Medical scribe job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalScribeJobName"] = medical_scribe_job_name
    try:
        client.delete_medical_scribe_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete medical scribe job") from exc
    return None


def delete_medical_transcription_job(
    medical_transcription_job_name: str,
    region_name: str | None = None,
) -> None:
    """Delete medical transcription job.

    Args:
        medical_transcription_job_name: Medical transcription job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalTranscriptionJobName"] = medical_transcription_job_name
    try:
        client.delete_medical_transcription_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete medical transcription job") from exc
    return None


def delete_medical_vocabulary(
    vocabulary_name: str,
    region_name: str | None = None,
) -> None:
    """Delete medical vocabulary.

    Args:
        vocabulary_name: Vocabulary name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyName"] = vocabulary_name
    try:
        client.delete_medical_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete medical vocabulary") from exc
    return None


def delete_vocabulary_filter(
    vocabulary_filter_name: str,
    region_name: str | None = None,
) -> None:
    """Delete vocabulary filter.

    Args:
        vocabulary_filter_name: Vocabulary filter name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyFilterName"] = vocabulary_filter_name
    try:
        client.delete_vocabulary_filter(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vocabulary filter") from exc
    return None


def describe_language_model(
    model_name: str,
    region_name: str | None = None,
) -> DescribeLanguageModelResult:
    """Describe language model.

    Args:
        model_name: Model name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ModelName"] = model_name
    try:
        resp = client.describe_language_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe language model") from exc
    return DescribeLanguageModelResult(
        language_model=resp.get("LanguageModel"),
    )


def get_call_analytics_category(
    category_name: str,
    region_name: str | None = None,
) -> GetCallAnalyticsCategoryResult:
    """Get call analytics category.

    Args:
        category_name: Category name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CategoryName"] = category_name
    try:
        resp = client.get_call_analytics_category(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get call analytics category") from exc
    return GetCallAnalyticsCategoryResult(
        category_properties=resp.get("CategoryProperties"),
    )


def get_call_analytics_job(
    call_analytics_job_name: str,
    region_name: str | None = None,
) -> GetCallAnalyticsJobResult:
    """Get call analytics job.

    Args:
        call_analytics_job_name: Call analytics job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallAnalyticsJobName"] = call_analytics_job_name
    try:
        resp = client.get_call_analytics_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get call analytics job") from exc
    return GetCallAnalyticsJobResult(
        call_analytics_job=resp.get("CallAnalyticsJob"),
    )


def get_medical_scribe_job(
    medical_scribe_job_name: str,
    region_name: str | None = None,
) -> GetMedicalScribeJobResult:
    """Get medical scribe job.

    Args:
        medical_scribe_job_name: Medical scribe job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalScribeJobName"] = medical_scribe_job_name
    try:
        resp = client.get_medical_scribe_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get medical scribe job") from exc
    return GetMedicalScribeJobResult(
        medical_scribe_job=resp.get("MedicalScribeJob"),
    )


def get_medical_transcription_job(
    medical_transcription_job_name: str,
    region_name: str | None = None,
) -> GetMedicalTranscriptionJobResult:
    """Get medical transcription job.

    Args:
        medical_transcription_job_name: Medical transcription job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalTranscriptionJobName"] = medical_transcription_job_name
    try:
        resp = client.get_medical_transcription_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get medical transcription job") from exc
    return GetMedicalTranscriptionJobResult(
        medical_transcription_job=resp.get("MedicalTranscriptionJob"),
    )


def get_medical_vocabulary(
    vocabulary_name: str,
    region_name: str | None = None,
) -> GetMedicalVocabularyResult:
    """Get medical vocabulary.

    Args:
        vocabulary_name: Vocabulary name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyName"] = vocabulary_name
    try:
        resp = client.get_medical_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get medical vocabulary") from exc
    return GetMedicalVocabularyResult(
        vocabulary_name=resp.get("VocabularyName"),
        language_code=resp.get("LanguageCode"),
        vocabulary_state=resp.get("VocabularyState"),
        last_modified_time=resp.get("LastModifiedTime"),
        failure_reason=resp.get("FailureReason"),
        download_uri=resp.get("DownloadUri"),
    )


def get_vocabulary_filter(
    vocabulary_filter_name: str,
    region_name: str | None = None,
) -> GetVocabularyFilterResult:
    """Get vocabulary filter.

    Args:
        vocabulary_filter_name: Vocabulary filter name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyFilterName"] = vocabulary_filter_name
    try:
        resp = client.get_vocabulary_filter(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get vocabulary filter") from exc
    return GetVocabularyFilterResult(
        vocabulary_filter_name=resp.get("VocabularyFilterName"),
        language_code=resp.get("LanguageCode"),
        last_modified_time=resp.get("LastModifiedTime"),
        download_uri=resp.get("DownloadUri"),
    )


def list_call_analytics_categories(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCallAnalyticsCategoriesResult:
    """List call analytics categories.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_call_analytics_categories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list call analytics categories") from exc
    return ListCallAnalyticsCategoriesResult(
        next_token=resp.get("NextToken"),
        categories=resp.get("Categories"),
    )


def list_call_analytics_jobs(
    *,
    status: str | None = None,
    job_name_contains: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCallAnalyticsJobsResult:
    """List call analytics jobs.

    Args:
        status: Status.
        job_name_contains: Job name contains.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    if job_name_contains is not None:
        kwargs["JobNameContains"] = job_name_contains
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_call_analytics_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list call analytics jobs") from exc
    return ListCallAnalyticsJobsResult(
        status=resp.get("Status"),
        next_token=resp.get("NextToken"),
        call_analytics_job_summaries=resp.get("CallAnalyticsJobSummaries"),
    )


def list_language_models(
    *,
    status_equals: str | None = None,
    name_contains: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListLanguageModelsResult:
    """List language models.

    Args:
        status_equals: Status equals.
        name_contains: Name contains.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if status_equals is not None:
        kwargs["StatusEquals"] = status_equals
    if name_contains is not None:
        kwargs["NameContains"] = name_contains
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_language_models(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list language models") from exc
    return ListLanguageModelsResult(
        next_token=resp.get("NextToken"),
        models=resp.get("Models"),
    )


def list_medical_scribe_jobs(
    *,
    status: str | None = None,
    job_name_contains: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMedicalScribeJobsResult:
    """List medical scribe jobs.

    Args:
        status: Status.
        job_name_contains: Job name contains.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    if job_name_contains is not None:
        kwargs["JobNameContains"] = job_name_contains
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_medical_scribe_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list medical scribe jobs") from exc
    return ListMedicalScribeJobsResult(
        status=resp.get("Status"),
        next_token=resp.get("NextToken"),
        medical_scribe_job_summaries=resp.get("MedicalScribeJobSummaries"),
    )


def list_medical_transcription_jobs(
    *,
    status: str | None = None,
    job_name_contains: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMedicalTranscriptionJobsResult:
    """List medical transcription jobs.

    Args:
        status: Status.
        job_name_contains: Job name contains.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    if job_name_contains is not None:
        kwargs["JobNameContains"] = job_name_contains
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_medical_transcription_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list medical transcription jobs") from exc
    return ListMedicalTranscriptionJobsResult(
        status=resp.get("Status"),
        next_token=resp.get("NextToken"),
        medical_transcription_job_summaries=resp.get("MedicalTranscriptionJobSummaries"),
    )


def list_medical_vocabularies(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    state_equals: str | None = None,
    name_contains: str | None = None,
    region_name: str | None = None,
) -> ListMedicalVocabulariesResult:
    """List medical vocabularies.

    Args:
        next_token: Next token.
        max_results: Max results.
        state_equals: State equals.
        name_contains: Name contains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if state_equals is not None:
        kwargs["StateEquals"] = state_equals
    if name_contains is not None:
        kwargs["NameContains"] = name_contains
    try:
        resp = client.list_medical_vocabularies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list medical vocabularies") from exc
    return ListMedicalVocabulariesResult(
        status=resp.get("Status"),
        next_token=resp.get("NextToken"),
        vocabularies=resp.get("Vocabularies"),
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
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_arn=resp.get("ResourceArn"),
        tags=resp.get("Tags"),
    )


def list_vocabulary_filters(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    name_contains: str | None = None,
    region_name: str | None = None,
) -> ListVocabularyFiltersResult:
    """List vocabulary filters.

    Args:
        next_token: Next token.
        max_results: Max results.
        name_contains: Name contains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if name_contains is not None:
        kwargs["NameContains"] = name_contains
    try:
        resp = client.list_vocabulary_filters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list vocabulary filters") from exc
    return ListVocabularyFiltersResult(
        next_token=resp.get("NextToken"),
        vocabulary_filters=resp.get("VocabularyFilters"),
    )


def start_call_analytics_job(
    call_analytics_job_name: str,
    media: dict[str, Any],
    *,
    output_location: str | None = None,
    output_encryption_kms_key_id: str | None = None,
    data_access_role_arn: str | None = None,
    settings: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    channel_definitions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartCallAnalyticsJobResult:
    """Start call analytics job.

    Args:
        call_analytics_job_name: Call analytics job name.
        media: Media.
        output_location: Output location.
        output_encryption_kms_key_id: Output encryption kms key id.
        data_access_role_arn: Data access role arn.
        settings: Settings.
        tags: Tags.
        channel_definitions: Channel definitions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallAnalyticsJobName"] = call_analytics_job_name
    kwargs["Media"] = media
    if output_location is not None:
        kwargs["OutputLocation"] = output_location
    if output_encryption_kms_key_id is not None:
        kwargs["OutputEncryptionKMSKeyId"] = output_encryption_kms_key_id
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    if settings is not None:
        kwargs["Settings"] = settings
    if tags is not None:
        kwargs["Tags"] = tags
    if channel_definitions is not None:
        kwargs["ChannelDefinitions"] = channel_definitions
    try:
        resp = client.start_call_analytics_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start call analytics job") from exc
    return StartCallAnalyticsJobResult(
        call_analytics_job=resp.get("CallAnalyticsJob"),
    )


def start_medical_scribe_job(
    medical_scribe_job_name: str,
    media: dict[str, Any],
    output_bucket_name: str,
    data_access_role_arn: str,
    settings: dict[str, Any],
    *,
    output_encryption_kms_key_id: str | None = None,
    kms_encryption_context: dict[str, Any] | None = None,
    channel_definitions: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    medical_scribe_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartMedicalScribeJobResult:
    """Start medical scribe job.

    Args:
        medical_scribe_job_name: Medical scribe job name.
        media: Media.
        output_bucket_name: Output bucket name.
        data_access_role_arn: Data access role arn.
        settings: Settings.
        output_encryption_kms_key_id: Output encryption kms key id.
        kms_encryption_context: Kms encryption context.
        channel_definitions: Channel definitions.
        tags: Tags.
        medical_scribe_context: Medical scribe context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalScribeJobName"] = medical_scribe_job_name
    kwargs["Media"] = media
    kwargs["OutputBucketName"] = output_bucket_name
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["Settings"] = settings
    if output_encryption_kms_key_id is not None:
        kwargs["OutputEncryptionKMSKeyId"] = output_encryption_kms_key_id
    if kms_encryption_context is not None:
        kwargs["KMSEncryptionContext"] = kms_encryption_context
    if channel_definitions is not None:
        kwargs["ChannelDefinitions"] = channel_definitions
    if tags is not None:
        kwargs["Tags"] = tags
    if medical_scribe_context is not None:
        kwargs["MedicalScribeContext"] = medical_scribe_context
    try:
        resp = client.start_medical_scribe_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start medical scribe job") from exc
    return StartMedicalScribeJobResult(
        medical_scribe_job=resp.get("MedicalScribeJob"),
    )


def start_medical_transcription_job(
    medical_transcription_job_name: str,
    language_code: str,
    media: dict[str, Any],
    output_bucket_name: str,
    specialty: str,
    type_value: str,
    *,
    media_sample_rate_hertz: int | None = None,
    media_format: str | None = None,
    output_key: str | None = None,
    output_encryption_kms_key_id: str | None = None,
    kms_encryption_context: dict[str, Any] | None = None,
    settings: dict[str, Any] | None = None,
    content_identification_type: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartMedicalTranscriptionJobResult:
    """Start medical transcription job.

    Args:
        medical_transcription_job_name: Medical transcription job name.
        language_code: Language code.
        media: Media.
        output_bucket_name: Output bucket name.
        specialty: Specialty.
        type_value: Type value.
        media_sample_rate_hertz: Media sample rate hertz.
        media_format: Media format.
        output_key: Output key.
        output_encryption_kms_key_id: Output encryption kms key id.
        kms_encryption_context: Kms encryption context.
        settings: Settings.
        content_identification_type: Content identification type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MedicalTranscriptionJobName"] = medical_transcription_job_name
    kwargs["LanguageCode"] = language_code
    kwargs["Media"] = media
    kwargs["OutputBucketName"] = output_bucket_name
    kwargs["Specialty"] = specialty
    kwargs["Type"] = type_value
    if media_sample_rate_hertz is not None:
        kwargs["MediaSampleRateHertz"] = media_sample_rate_hertz
    if media_format is not None:
        kwargs["MediaFormat"] = media_format
    if output_key is not None:
        kwargs["OutputKey"] = output_key
    if output_encryption_kms_key_id is not None:
        kwargs["OutputEncryptionKMSKeyId"] = output_encryption_kms_key_id
    if kms_encryption_context is not None:
        kwargs["KMSEncryptionContext"] = kms_encryption_context
    if settings is not None:
        kwargs["Settings"] = settings
    if content_identification_type is not None:
        kwargs["ContentIdentificationType"] = content_identification_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_medical_transcription_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start medical transcription job") from exc
    return StartMedicalTranscriptionJobResult(
        medical_transcription_job=resp.get("MedicalTranscriptionJob"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
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
    client = get_client("transcribe", region_name)
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
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_call_analytics_category(
    category_name: str,
    rules: list[dict[str, Any]],
    *,
    input_type: str | None = None,
    region_name: str | None = None,
) -> UpdateCallAnalyticsCategoryResult:
    """Update call analytics category.

    Args:
        category_name: Category name.
        rules: Rules.
        input_type: Input type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CategoryName"] = category_name
    kwargs["Rules"] = rules
    if input_type is not None:
        kwargs["InputType"] = input_type
    try:
        resp = client.update_call_analytics_category(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update call analytics category") from exc
    return UpdateCallAnalyticsCategoryResult(
        category_properties=resp.get("CategoryProperties"),
    )


def update_medical_vocabulary(
    vocabulary_name: str,
    language_code: str,
    vocabulary_file_uri: str,
    region_name: str | None = None,
) -> UpdateMedicalVocabularyResult:
    """Update medical vocabulary.

    Args:
        vocabulary_name: Vocabulary name.
        language_code: Language code.
        vocabulary_file_uri: Vocabulary file uri.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyName"] = vocabulary_name
    kwargs["LanguageCode"] = language_code
    kwargs["VocabularyFileUri"] = vocabulary_file_uri
    try:
        resp = client.update_medical_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update medical vocabulary") from exc
    return UpdateMedicalVocabularyResult(
        vocabulary_name=resp.get("VocabularyName"),
        language_code=resp.get("LanguageCode"),
        last_modified_time=resp.get("LastModifiedTime"),
        vocabulary_state=resp.get("VocabularyState"),
    )


def update_vocabulary(
    vocabulary_name: str,
    language_code: str,
    *,
    phrases: list[str] | None = None,
    vocabulary_file_uri: str | None = None,
    data_access_role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateVocabularyResult:
    """Update vocabulary.

    Args:
        vocabulary_name: Vocabulary name.
        language_code: Language code.
        phrases: Phrases.
        vocabulary_file_uri: Vocabulary file uri.
        data_access_role_arn: Data access role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyName"] = vocabulary_name
    kwargs["LanguageCode"] = language_code
    if phrases is not None:
        kwargs["Phrases"] = phrases
    if vocabulary_file_uri is not None:
        kwargs["VocabularyFileUri"] = vocabulary_file_uri
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    try:
        resp = client.update_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update vocabulary") from exc
    return UpdateVocabularyResult(
        vocabulary_name=resp.get("VocabularyName"),
        language_code=resp.get("LanguageCode"),
        last_modified_time=resp.get("LastModifiedTime"),
        vocabulary_state=resp.get("VocabularyState"),
    )


def update_vocabulary_filter(
    vocabulary_filter_name: str,
    *,
    words: list[str] | None = None,
    vocabulary_filter_file_uri: str | None = None,
    data_access_role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateVocabularyFilterResult:
    """Update vocabulary filter.

    Args:
        vocabulary_filter_name: Vocabulary filter name.
        words: Words.
        vocabulary_filter_file_uri: Vocabulary filter file uri.
        data_access_role_arn: Data access role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("transcribe", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VocabularyFilterName"] = vocabulary_filter_name
    if words is not None:
        kwargs["Words"] = words
    if vocabulary_filter_file_uri is not None:
        kwargs["VocabularyFilterFileUri"] = vocabulary_filter_file_uri
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    try:
        resp = client.update_vocabulary_filter(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update vocabulary filter") from exc
    return UpdateVocabularyFilterResult(
        vocabulary_filter_name=resp.get("VocabularyFilterName"),
        language_code=resp.get("LanguageCode"),
        last_modified_time=resp.get("LastModifiedTime"),
    )
