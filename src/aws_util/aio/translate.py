"""Native async Translate utilities using the async engine."""

from __future__ import annotations

import asyncio
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.translate import (
    CreateParallelDataResult,
    DeleteParallelDataResult,
    DescribeTextTranslationJobResult,
    GetParallelDataResult,
    GetTerminologyResult,
    ImportTerminologyResult,
    ListParallelDataResult,
    ListTagsForResourceResult,
    ListTerminologiesResult,
    ListTextTranslationJobsResult,
    StartTextTranslationJobResult,
    StopTextTranslationJobResult,
    TranslateDocumentResult,
    TranslateLanguage,
    TranslateResult,
    UpdateParallelDataResult,
)

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


async def translate_text(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {
        "Text": text,
        "SourceLanguageCode": source_language_code,
        "TargetLanguageCode": target_language_code,
    }
    if terminology_names:
        kwargs["TerminologyNames"] = terminology_names
    try:
        resp = await client.call("TranslateText", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to translate text to {target_language_code!r}") from exc
    return TranslateResult(
        translated_text=resp["TranslatedText"],
        source_language_code=resp["SourceLanguageCode"],
        target_language_code=resp["TargetLanguageCode"],
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def translate_batch(
    texts: list[str],
    target_language_code: str,
    source_language_code: str = "auto",
    terminology_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[TranslateResult]:
    """Translate a list of text strings concurrently.

    Each text is translated via a separate async call so total latency is
    bounded by the slowest individual call rather than the sum of all calls.

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
    if not texts:
        return []
    coros = [
        translate_text(
            text,
            target_language_code,
            source_language_code,
            terminology_names,
            region_name,
        )
        for text in texts
    ]
    return list(await asyncio.gather(*coros))


async def list_languages(
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
    client = async_client("translate", region_name)
    languages: list[TranslateLanguage] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListLanguages", MaxResults=500, **kwargs)
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
    except Exception as exc:
        raise wrap_aws_error(exc, "list_languages failed") from exc
    return languages


async def create_parallel_data(
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
    client = async_client("translate", region_name)
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
        resp = await client.call("CreateParallelData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create parallel data") from exc
    return CreateParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
    )


async def delete_parallel_data(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteParallelData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete parallel data") from exc
    return DeleteParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
    )


async def delete_terminology(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteTerminology", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete terminology") from exc
    return None


async def describe_text_translation_job(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = await client.call("DescribeTextTranslationJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe text translation job") from exc
    return DescribeTextTranslationJobResult(
        text_translation_job_properties=resp.get("TextTranslationJobProperties"),
    )


async def get_parallel_data(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetParallelData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get parallel data") from exc
    return GetParallelDataResult(
        parallel_data_properties=resp.get("ParallelDataProperties"),
        data_location=resp.get("DataLocation"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
        latest_update_attempt_auxiliary_data_location=resp.get(
            "LatestUpdateAttemptAuxiliaryDataLocation"
        ),
    )


async def get_terminology(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if terminology_data_format is not None:
        kwargs["TerminologyDataFormat"] = terminology_data_format
    try:
        resp = await client.call("GetTerminology", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get terminology") from exc
    return GetTerminologyResult(
        terminology_properties=resp.get("TerminologyProperties"),
        terminology_data_location=resp.get("TerminologyDataLocation"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
    )


async def import_terminology(
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
    client = async_client("translate", region_name)
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
        resp = await client.call("ImportTerminology", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import terminology") from exc
    return ImportTerminologyResult(
        terminology_properties=resp.get("TerminologyProperties"),
        auxiliary_data_location=resp.get("AuxiliaryDataLocation"),
    )


async def list_parallel_data(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListParallelData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list parallel data") from exc
    return ListParallelDataResult(
        parallel_data_properties_list=resp.get("ParallelDataPropertiesList"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_terminologies(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTerminologies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list terminologies") from exc
    return ListTerminologiesResult(
        terminology_properties_list=resp.get("TerminologyPropertiesList"),
        next_token=resp.get("NextToken"),
    )


async def list_text_translation_jobs(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTextTranslationJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list text translation jobs") from exc
    return ListTextTranslationJobsResult(
        text_translation_job_properties_list=resp.get("TextTranslationJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


async def start_text_translation_job(
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
    client = async_client("translate", region_name)
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
        resp = await client.call("StartTextTranslationJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start text translation job") from exc
    return StartTextTranslationJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


async def stop_text_translation_job(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = await client.call("StopTextTranslationJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop text translation job") from exc
    return StopTextTranslationJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


async def tag_resource(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def translate_document(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Document"] = document
    kwargs["SourceLanguageCode"] = source_language_code
    kwargs["TargetLanguageCode"] = target_language_code
    if terminology_names is not None:
        kwargs["TerminologyNames"] = terminology_names
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = await client.call("TranslateDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to translate document") from exc
    return TranslateDocumentResult(
        translated_document=resp.get("TranslatedDocument"),
        source_language_code=resp.get("SourceLanguageCode"),
        target_language_code=resp.get("TargetLanguageCode"),
        applied_terminologies=resp.get("AppliedTerminologies"),
        applied_settings=resp.get("AppliedSettings"),
    )


async def untag_resource(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_parallel_data(
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
    client = async_client("translate", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ParallelDataConfig"] = parallel_data_config
    kwargs["ClientToken"] = client_token
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateParallelData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update parallel data") from exc
    return UpdateParallelDataResult(
        name=resp.get("Name"),
        status=resp.get("Status"),
        latest_update_attempt_status=resp.get("LatestUpdateAttemptStatus"),
        latest_update_attempt_at=resp.get("LatestUpdateAttemptAt"),
    )
