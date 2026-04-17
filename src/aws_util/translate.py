from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CreateParallelDataResult",
    "DeleteParallelDataResult",
    "DescribeTextTranslationJobResult",
    "GetParallelDataResult",
    "GetTerminologyResult",
    "ImportTerminologyResult",
    "ListParallelDataResult",
    "ListTagsForResourceResult",
    "ListTerminologiesResult",
    "ListTextTranslationJobsResult",
    "StartTextTranslationJobResult",
    "StopTextTranslationJobResult",
    "TranslateDocumentResult",
    "TranslateLanguage",
    "TranslateResult",
    "UpdateParallelDataResult",
    "create_parallel_data",
    "delete_parallel_data",
    "delete_terminology",
    "describe_text_translation_job",
    "get_parallel_data",
    "get_terminology",
    "import_terminology",
    "list_languages",
    "list_parallel_data",
    "list_tags_for_resource",
    "list_terminologies",
    "list_text_translation_jobs",
    "start_text_translation_job",
    "stop_text_translation_job",
    "tag_resource",
    "translate_batch",
    "translate_document",
    "translate_text",
    "untag_resource",
    "update_parallel_data",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TranslateResult(BaseModel):
    """The result of an Amazon Translate call."""

    model_config = ConfigDict(frozen=True)

    translated_text: str
    source_language_code: str
    target_language_code: str


class TranslateLanguage(BaseModel):
    """A language supported by Amazon Translate."""

    model_config = ConfigDict(frozen=True)

    language_code: str
    language_name: str


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def translate_text(
    text: str,
    target_language_code: str,
    source_language_code: str = "auto",
    terminology_names: list[str] | None = None,
    region_name: str | None = None,
) -> TranslateResult:
    """Translate text from one language to another.

    Args:
        text: The text to translate (up to 10,000 UTF-8 bytes).
        target_language_code: BCP-47 target language code, e.g. ``"es"``,
            ``"fr"``, ``"de"``, ``"ja"``.
        source_language_code: BCP-47 source language code, or ``"auto"``
            (default) to let Amazon Translate detect the language automatically.
        terminology_names: Optional list of custom terminology names to apply
            for domain-specific vocabulary.
        region_name: AWS region override.

    Returns:
        A :class:`TranslateResult` with the translated text and language codes.

    Raises:
        RuntimeError: If the translation fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict = {
        "Text": text,
        "SourceLanguageCode": source_language_code,
        "TargetLanguageCode": target_language_code,
    }
    if terminology_names:
        kwargs["TerminologyNames"] = terminology_names
    try:
        resp = client.translate_text(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to translate text to {target_language_code!r}") from exc
    return TranslateResult(
        translated_text=resp["TranslatedText"],
        source_language_code=resp["SourceLanguageCode"],
        target_language_code=resp["TargetLanguageCode"],
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def translate_batch(
    texts: list[str],
    target_language_code: str,
    source_language_code: str = "auto",
    terminology_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[TranslateResult]:
    """Translate a list of text strings concurrently.

    Each text is translated in a separate thread so total latency is bounded
    by the slowest individual call rather than the sum of all calls.

    Args:
        texts: List of input texts (each up to 10,000 UTF-8 bytes).
        target_language_code: BCP-47 target language code.
        source_language_code: BCP-47 source language code, or ``"auto"``
            (default) to detect automatically.
        terminology_names: Optional custom terminology names applied to each
            translation.
        region_name: AWS region override.

    Returns:
        A list of :class:`TranslateResult` objects in the same order as
        *texts*.

    Raises:
        RuntimeError: If any individual translation fails.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    if not texts:
        return []
    results: dict[int, TranslateResult] = {}
    with ThreadPoolExecutor(max_workers=min(len(texts), 10)) as pool:
        futures = {
            pool.submit(
                translate_text,
                text,
                target_language_code,
                source_language_code,
                terminology_names,
                region_name,
            ): i
            for i, text in enumerate(texts)
        }
        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    return [results[i] for i in range(len(texts))]


def list_languages(
    region_name: str | None = None,
) -> list[TranslateLanguage]:
    """List all languages supported by Amazon Translate.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`TranslateLanguage` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    languages: list[TranslateLanguage] = []
    kwargs: dict = {}
    try:
        while True:
            resp = client.list_languages(MaxResults=500, **kwargs)
            for lang in resp.get("Languages", []):
                languages.append(
                    TranslateLanguage(
                        language_code=lang["LanguageCode"],
                        language_name=lang["LanguageName"],
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_languages failed") from exc
    return languages


class CreateParallelDataResult(BaseModel):
    """Result of create_parallel_data."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    status: str | None = None


class DeleteParallelDataResult(BaseModel):
    """Result of delete_parallel_data."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    status: str | None = None


class DescribeTextTranslationJobResult(BaseModel):
    """Result of describe_text_translation_job."""

    model_config = ConfigDict(frozen=True)

    text_translation_job_properties: dict[str, Any] | None = None


class GetParallelDataResult(BaseModel):
    """Result of get_parallel_data."""

    model_config = ConfigDict(frozen=True)

    parallel_data_properties: dict[str, Any] | None = None
    data_location: dict[str, Any] | None = None
    auxiliary_data_location: dict[str, Any] | None = None
    latest_update_attempt_auxiliary_data_location: dict[str, Any] | None = None


class GetTerminologyResult(BaseModel):
    """Result of get_terminology."""

    model_config = ConfigDict(frozen=True)

    terminology_properties: dict[str, Any] | None = None
    terminology_data_location: dict[str, Any] | None = None
    auxiliary_data_location: dict[str, Any] | None = None


class ImportTerminologyResult(BaseModel):
    """Result of import_terminology."""

    model_config = ConfigDict(frozen=True)

    terminology_properties: dict[str, Any] | None = None
    auxiliary_data_location: dict[str, Any] | None = None


class ListParallelDataResult(BaseModel):
    """Result of list_parallel_data."""

    model_config = ConfigDict(frozen=True)

    parallel_data_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class ListTerminologiesResult(BaseModel):
    """Result of list_terminologies."""

    model_config = ConfigDict(frozen=True)

    terminology_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTextTranslationJobsResult(BaseModel):
    """Result of list_text_translation_jobs."""

    model_config = ConfigDict(frozen=True)

    text_translation_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class StartTextTranslationJobResult(BaseModel):
    """Result of start_text_translation_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopTextTranslationJobResult(BaseModel):
    """Result of stop_text_translation_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class TranslateDocumentResult(BaseModel):
    """Result of translate_document."""

    model_config = ConfigDict(frozen=True)

    translated_document: dict[str, Any] | None = None
    source_language_code: str | None = None
    target_language_code: str | None = None
    applied_terminologies: list[dict[str, Any]] | None = None
    applied_settings: dict[str, Any] | None = None


class UpdateParallelDataResult(BaseModel):
    """Result of update_parallel_data."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    status: str | None = None
    latest_update_attempt_status: str | None = None
    latest_update_attempt_at: str | None = None


def create_parallel_data(
    name: str,
    parallel_data_config: dict[str, Any],
    client_token: str,
    *,
    description: str | None = None,
    encryption_key: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateParallelDataResult:
    """Create parallel data.

    Args:
        name: Name.
        parallel_data_config: Parallel data config.
        client_token: Client token.
        description: Description.
        encryption_key: Encryption key.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ParallelDataConfig"] = parallel_data_config
    kwargs["ClientToken"] = client_token
    if description is not None:
        kwargs["Description"] = description
    if encryption_key is not None:
        kwargs["EncryptionKey"] = encryption_key
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_parallel_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create parallel data") from exc
    return CreateParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
    )


def delete_parallel_data(
    name: str,
    region_name: str | None = None,
) -> DeleteParallelDataResult:
    """Delete parallel data.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.delete_parallel_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete parallel data") from exc
    return DeleteParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
    )


def delete_terminology(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete terminology.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_terminology(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete terminology") from exc
    return None


def describe_text_translation_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeTextTranslationJobResult:
    """Describe text translation job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_text_translation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe text translation job") from exc
    return DescribeTextTranslationJobResult(
        text_translation_job_properties=resp.get("TextTranslationJobProperties"),
    )


def get_parallel_data(
    name: str,
    region_name: str | None = None,
) -> GetParallelDataResult:
    """Get parallel data.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.get_parallel_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get parallel data") from exc
    return GetParallelDataResult(
        parallel_data_properties=resp.get("ParallelDataProperties"),
        data_location=resp.get("DataLocation"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
        latest_update_attempt_auxiliary_data_location=resp.get(
            "LatestUpdateAttemptAuxiliaryDataLocation"
        ),
    )


def get_terminology(
    name: str,
    *,
    terminology_data_format: str | None = None,
    region_name: str | None = None,
) -> GetTerminologyResult:
    """Get terminology.

    Args:
        name: Name.
        terminology_data_format: Terminology data format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if terminology_data_format is not None:
        kwargs["TerminologyDataFormat"] = terminology_data_format
    try:
        resp = client.get_terminology(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get terminology") from exc
    return GetTerminologyResult(
        terminology_properties=resp.get("TerminologyProperties"),
        terminology_data_location=resp.get("TerminologyDataLocation"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
    )


def import_terminology(
    name: str,
    merge_strategy: str,
    terminology_data: dict[str, Any],
    *,
    description: str | None = None,
    encryption_key: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportTerminologyResult:
    """Import terminology.

    Args:
        name: Name.
        merge_strategy: Merge strategy.
        terminology_data: Terminology data.
        description: Description.
        encryption_key: Encryption key.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["MergeStrategy"] = merge_strategy
    kwargs["TerminologyData"] = terminology_data
    if description is not None:
        kwargs["Description"] = description
    if encryption_key is not None:
        kwargs["EncryptionKey"] = encryption_key
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.import_terminology(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import terminology") from exc
    return ImportTerminologyResult(
        terminology_properties=resp.get("TerminologyProperties"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
    )


def list_parallel_data(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListParallelDataResult:
    """List parallel data.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_parallel_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list parallel data") from exc
    return ListParallelDataResult(
        parallel_data_properties_list=resp.get("ParallelDataPropertiesList"),
        next_token=resp.get("NextToken"),
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
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_terminologies(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTerminologiesResult:
    """List terminologies.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_terminologies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list terminologies") from exc
    return ListTerminologiesResult(
        terminology_properties_list=resp.get("TerminologyPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_text_translation_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTextTranslationJobsResult:
    """List text translation jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_text_translation_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list text translation jobs") from exc
    return ListTextTranslationJobsResult(
        text_translation_job_properties_list=resp.get("TextTranslationJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def start_text_translation_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    source_language_code: str,
    target_language_codes: list[str],
    client_token: str,
    *,
    job_name: str | None = None,
    terminology_names: list[str] | None = None,
    parallel_data_names: list[str] | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartTextTranslationJobResult:
    """Start text translation job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        source_language_code: Source language code.
        target_language_codes: Target language codes.
        client_token: Client token.
        job_name: Job name.
        terminology_names: Terminology names.
        parallel_data_names: Parallel data names.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["SourceLanguageCode"] = source_language_code
    kwargs["TargetLanguageCodes"] = target_language_codes
    kwargs["ClientToken"] = client_token
    if job_name is not None:
        kwargs["JobName"] = job_name
    if terminology_names is not None:
        kwargs["TerminologyNames"] = terminology_names
    if parallel_data_names is not None:
        kwargs["ParallelDataNames"] = parallel_data_names
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = client.start_text_translation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start text translation job") from exc
    return StartTextTranslationJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_text_translation_job(
    job_id: str,
    region_name: str | None = None,
) -> StopTextTranslationJobResult:
    """Stop text translation job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_text_translation_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop text translation job") from exc
    return StopTextTranslationJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
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
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def translate_document(
    document: dict[str, Any],
    source_language_code: str,
    target_language_code: str,
    *,
    terminology_names: list[str] | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> TranslateDocumentResult:
    """Translate document.

    Args:
        document: Document.
        source_language_code: Source language code.
        target_language_code: Target language code.
        terminology_names: Terminology names.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Document"] = document
    kwargs["SourceLanguageCode"] = source_language_code
    kwargs["TargetLanguageCode"] = target_language_code
    if terminology_names is not None:
        kwargs["TerminologyNames"] = terminology_names
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = client.translate_document(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to translate document") from exc
    return TranslateDocumentResult(
        translated_document=resp.get("TranslatedDocument"),
        source_language_code=resp.get("SourceLanguageCode"),
        target_language_code=resp.get("TargetLanguageCode"),
        applied_terminologies=resp.get("AppliedTerminologies"),
        applied_settings=resp.get("AppliedSettings"),
    )


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
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_parallel_data(
    name: str,
    parallel_data_config: dict[str, Any],
    client_token: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateParallelDataResult:
    """Update parallel data.

    Args:
        name: Name.
        parallel_data_config: Parallel data config.
        client_token: Client token.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ParallelDataConfig"] = parallel_data_config
    kwargs["ClientToken"] = client_token
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_parallel_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update parallel data") from exc
    return UpdateParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
        latest_update_attempt_status=resp.get("LatestUpdateAttemptStatus"),
        latest_update_attempt_at=resp.get("LatestUpdateAttemptAt"),
    )
