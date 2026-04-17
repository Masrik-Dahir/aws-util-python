from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "BatchDetectDominantLanguageResult",
    "BatchDetectEntitiesResult",
    "BatchDetectKeyPhrasesResult",
    "BatchDetectSyntaxResult",
    "BatchDetectTargetedSentimentResult",
    "ClassifyDocumentResult",
    "ContainsPiiEntitiesResult",
    "CreateDatasetResult",
    "CreateDocumentClassifierResult",
    "CreateEndpointResult",
    "CreateEntityRecognizerResult",
    "CreateFlywheelResult",
    "DescribeDatasetResult",
    "DescribeDocumentClassificationJobResult",
    "DescribeDocumentClassifierResult",
    "DescribeDominantLanguageDetectionJobResult",
    "DescribeEndpointResult",
    "DescribeEntitiesDetectionJobResult",
    "DescribeEntityRecognizerResult",
    "DescribeEventsDetectionJobResult",
    "DescribeFlywheelIterationResult",
    "DescribeFlywheelResult",
    "DescribeKeyPhrasesDetectionJobResult",
    "DescribePiiEntitiesDetectionJobResult",
    "DescribeResourcePolicyResult",
    "DescribeSentimentDetectionJobResult",
    "DescribeTargetedSentimentDetectionJobResult",
    "DescribeTopicsDetectionJobResult",
    "DetectSyntaxResult",
    "DetectTargetedSentimentResult",
    "DetectToxicContentResult",
    "EntityResult",
    "ImportModelResult",
    "KeyPhrase",
    "LanguageResult",
    "ListDatasetsResult",
    "ListDocumentClassificationJobsResult",
    "ListDocumentClassifierSummariesResult",
    "ListDocumentClassifiersResult",
    "ListDominantLanguageDetectionJobsResult",
    "ListEndpointsResult",
    "ListEntitiesDetectionJobsResult",
    "ListEntityRecognizerSummariesResult",
    "ListEntityRecognizersResult",
    "ListEventsDetectionJobsResult",
    "ListFlywheelIterationHistoryResult",
    "ListFlywheelsResult",
    "ListKeyPhrasesDetectionJobsResult",
    "ListPiiEntitiesDetectionJobsResult",
    "ListSentimentDetectionJobsResult",
    "ListTagsForResourceResult",
    "ListTargetedSentimentDetectionJobsResult",
    "ListTopicsDetectionJobsResult",
    "PiiEntity",
    "PutResourcePolicyResult",
    "SentimentResult",
    "StartDocumentClassificationJobResult",
    "StartDominantLanguageDetectionJobResult",
    "StartEntitiesDetectionJobResult",
    "StartEventsDetectionJobResult",
    "StartFlywheelIterationResult",
    "StartKeyPhrasesDetectionJobResult",
    "StartPiiEntitiesDetectionJobResult",
    "StartSentimentDetectionJobResult",
    "StartTargetedSentimentDetectionJobResult",
    "StartTopicsDetectionJobResult",
    "StopDominantLanguageDetectionJobResult",
    "StopEntitiesDetectionJobResult",
    "StopEventsDetectionJobResult",
    "StopKeyPhrasesDetectionJobResult",
    "StopPiiEntitiesDetectionJobResult",
    "StopSentimentDetectionJobResult",
    "StopTargetedSentimentDetectionJobResult",
    "UpdateEndpointResult",
    "UpdateFlywheelResult",
    "analyze_text",
    "batch_detect_dominant_language",
    "batch_detect_entities",
    "batch_detect_key_phrases",
    "batch_detect_sentiment",
    "batch_detect_syntax",
    "batch_detect_targeted_sentiment",
    "classify_document",
    "contains_pii_entities",
    "create_dataset",
    "create_document_classifier",
    "create_endpoint",
    "create_entity_recognizer",
    "create_flywheel",
    "delete_document_classifier",
    "delete_endpoint",
    "delete_entity_recognizer",
    "delete_flywheel",
    "delete_resource_policy",
    "describe_dataset",
    "describe_document_classification_job",
    "describe_document_classifier",
    "describe_dominant_language_detection_job",
    "describe_endpoint",
    "describe_entities_detection_job",
    "describe_entity_recognizer",
    "describe_events_detection_job",
    "describe_flywheel",
    "describe_flywheel_iteration",
    "describe_key_phrases_detection_job",
    "describe_pii_entities_detection_job",
    "describe_resource_policy",
    "describe_sentiment_detection_job",
    "describe_targeted_sentiment_detection_job",
    "describe_topics_detection_job",
    "detect_dominant_language",
    "detect_entities",
    "detect_key_phrases",
    "detect_pii_entities",
    "detect_sentiment",
    "detect_syntax",
    "detect_targeted_sentiment",
    "detect_toxic_content",
    "import_model",
    "list_datasets",
    "list_document_classification_jobs",
    "list_document_classifier_summaries",
    "list_document_classifiers",
    "list_dominant_language_detection_jobs",
    "list_endpoints",
    "list_entities_detection_jobs",
    "list_entity_recognizer_summaries",
    "list_entity_recognizers",
    "list_events_detection_jobs",
    "list_flywheel_iteration_history",
    "list_flywheels",
    "list_key_phrases_detection_jobs",
    "list_pii_entities_detection_jobs",
    "list_sentiment_detection_jobs",
    "list_tags_for_resource",
    "list_targeted_sentiment_detection_jobs",
    "list_topics_detection_jobs",
    "put_resource_policy",
    "redact_pii",
    "start_document_classification_job",
    "start_dominant_language_detection_job",
    "start_entities_detection_job",
    "start_events_detection_job",
    "start_flywheel_iteration",
    "start_key_phrases_detection_job",
    "start_pii_entities_detection_job",
    "start_sentiment_detection_job",
    "start_targeted_sentiment_detection_job",
    "start_topics_detection_job",
    "stop_dominant_language_detection_job",
    "stop_entities_detection_job",
    "stop_events_detection_job",
    "stop_key_phrases_detection_job",
    "stop_pii_entities_detection_job",
    "stop_sentiment_detection_job",
    "stop_targeted_sentiment_detection_job",
    "stop_training_document_classifier",
    "stop_training_entity_recognizer",
    "tag_resource",
    "untag_resource",
    "update_endpoint",
    "update_flywheel",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class SentimentResult(BaseModel):
    """Sentiment analysis result for a piece of text."""

    model_config = ConfigDict(frozen=True)

    sentiment: str
    positive: float = 0.0
    negative: float = 0.0
    neutral: float = 0.0
    mixed: float = 0.0


class EntityResult(BaseModel):
    """A named entity detected in text."""

    model_config = ConfigDict(frozen=True)

    text: str
    entity_type: str
    score: float
    begin_offset: int
    end_offset: int


class KeyPhrase(BaseModel):
    """A key phrase detected in text."""

    model_config = ConfigDict(frozen=True)

    text: str
    score: float
    begin_offset: int
    end_offset: int


class LanguageResult(BaseModel):
    """A detected language."""

    model_config = ConfigDict(frozen=True)

    language_code: str
    score: float


class PiiEntity(BaseModel):
    """A personally identifiable information (PII) entity detected in text."""

    model_config = ConfigDict(frozen=True)

    pii_type: str
    score: float
    begin_offset: int
    end_offset: int


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def detect_sentiment(
    text: str,
    language_code: str = "en",
    region_name: str | None = None,
) -> SentimentResult:
    """Detect the overall sentiment of a text string.

    Args:
        text: Input text (UTF-8, up to 5,000 bytes per call).
        language_code: BCP-47 language code, e.g. ``"en"``, ``"es"``,
            ``"fr"``.
        region_name: AWS region override.

    Returns:
        A :class:`SentimentResult` with sentiment label and confidence scores.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    try:
        resp = client.detect_sentiment(Text=text, LanguageCode=language_code)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_sentiment failed") from exc
    scores = resp.get("SentimentScore", {})
    return SentimentResult(
        sentiment=resp["Sentiment"],
        positive=scores.get("Positive", 0.0),
        negative=scores.get("Negative", 0.0),
        neutral=scores.get("Neutral", 0.0),
        mixed=scores.get("Mixed", 0.0),
    )


def detect_entities(
    text: str,
    language_code: str = "en",
    region_name: str | None = None,
) -> list[EntityResult]:
    """Detect named entities (people, places, organisations, dates, etc.) in text.

    Args:
        text: Input text (up to 5,000 bytes).
        language_code: BCP-47 language code.
        region_name: AWS region override.

    Returns:
        A list of :class:`EntityResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    try:
        resp = client.detect_entities(Text=text, LanguageCode=language_code)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_entities failed") from exc
    return [
        EntityResult(
            text=e["Text"],
            entity_type=e["Type"],
            score=e["Score"],
            begin_offset=e["BeginOffset"],
            end_offset=e["EndOffset"],
        )
        for e in resp.get("Entities", [])
    ]


def detect_key_phrases(
    text: str,
    language_code: str = "en",
    region_name: str | None = None,
) -> list[KeyPhrase]:
    """Extract key noun phrases from text.

    Args:
        text: Input text (up to 5,000 bytes).
        language_code: BCP-47 language code.
        region_name: AWS region override.

    Returns:
        A list of :class:`KeyPhrase` objects sorted by score.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    try:
        resp = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_key_phrases failed") from exc
    return [
        KeyPhrase(
            text=kp["Text"],
            score=kp["Score"],
            begin_offset=kp["BeginOffset"],
            end_offset=kp["EndOffset"],
        )
        for kp in resp.get("KeyPhrases", [])
    ]


def detect_dominant_language(
    text: str,
    region_name: str | None = None,
) -> LanguageResult:
    """Detect the dominant language of a text string.

    Args:
        text: Input text (up to 5,000 bytes).
        region_name: AWS region override.

    Returns:
        The most confident :class:`LanguageResult`.

    Raises:
        RuntimeError: If the API call fails.
        ValueError: If no language is detected.
    """
    client = get_client("comprehend", region_name)
    try:
        resp = client.detect_dominant_language(Text=text)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_dominant_language failed") from exc
    languages = [
        LanguageResult(language_code=lang["LanguageCode"], score=lang["Score"])
        for lang in resp.get("Languages", [])
    ]
    if not languages:
        raise ValueError("Comprehend could not detect any language in the text")
    return max(languages, key=lambda lang: lang.score)


def detect_pii_entities(
    text: str,
    language_code: str = "en",
    region_name: str | None = None,
) -> list[PiiEntity]:
    """Detect personally identifiable information (PII) entities in text.

    Detected types include names, addresses, SSNs, credit card numbers,
    phone numbers, email addresses, and more.

    Args:
        text: Input text (up to 5,000 bytes).
        language_code: BCP-47 language code (currently only ``"en"`` is
            supported by Comprehend).
        region_name: AWS region override.

    Returns:
        A list of :class:`PiiEntity` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    try:
        resp = client.detect_pii_entities(Text=text, LanguageCode=language_code)
    except ClientError as exc:
        raise wrap_aws_error(exc, "detect_pii_entities failed") from exc
    return [
        PiiEntity(
            pii_type=e["Type"],
            score=e["Score"],
            begin_offset=e["BeginOffset"],
            end_offset=e["EndOffset"],
        )
        for e in resp.get("Entities", [])
    ]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def analyze_text(
    text: str,
    language_code: str = "en",
    region_name: str | None = None,
) -> dict[str, Any]:
    """Run all Comprehend analyses on a text string in parallel and return results.

    Executes sentiment, entity, key phrase, and language detection concurrently
    using a thread pool, then merges the results into a single dict.

    Args:
        text: Input text (up to 5,000 bytes).
        language_code: BCP-47 language code (default ``"en"``).
        region_name: AWS region override.

    Returns:
        A dict with keys:
        - ``"sentiment"`` — :class:`SentimentResult`
        - ``"entities"`` — list of :class:`EntityResult`
        - ``"key_phrases"`` — list of :class:`KeyPhrase`
        - ``"language"`` — :class:`LanguageResult`
        - ``"pii_entities"`` — list of :class:`PiiEntity` (English only)

    Raises:
        RuntimeError: If any detection call fails.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    tasks = {
        "sentiment": lambda: detect_sentiment(text, language_code, region_name),
        "entities": lambda: detect_entities(text, language_code, region_name),
        "key_phrases": lambda: detect_key_phrases(text, language_code, region_name),
        "language": lambda: detect_dominant_language(text, region_name),
    }
    if language_code == "en":
        tasks["pii_entities"] = lambda: detect_pii_entities(text, language_code, region_name)

    results: dict[str, Any] = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {pool.submit(fn): key for key, fn in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()

    if "pii_entities" not in results:
        results["pii_entities"] = []
    return results


def redact_pii(
    text: str,
    language_code: str = "en",
    replacement: str = "[REDACTED]",
    region_name: str | None = None,
) -> str:
    """Detect and redact PII entities from text.

    Calls :func:`detect_pii_entities` and replaces each detected span with
    *replacement*, working backwards through the string to preserve offsets.

    Args:
        text: Input text (up to 5,000 bytes).
        language_code: BCP-47 language code (only ``"en"`` is supported by
            Comprehend for PII detection).
        replacement: String to substitute for each PII span (default
            ``"[REDACTED]"``).
        region_name: AWS region override.

    Returns:
        The text with all PII spans replaced by *replacement*.

    Raises:
        RuntimeError: If PII detection fails.
    """
    entities = detect_pii_entities(text, language_code, region_name)
    # Process from end to start so offsets remain valid
    entities_sorted = sorted(entities, key=lambda e: e.begin_offset, reverse=True)
    result = text
    for entity in entities_sorted:
        result = result[: entity.begin_offset] + replacement + result[entity.end_offset :]
    return result


def batch_detect_sentiment(
    texts: list[str],
    language_code: str = "en",
    region_name: str | None = None,
) -> list[SentimentResult]:
    """Detect sentiment for up to 25 text strings in one request.

    Args:
        texts: List of input texts (up to 25, each up to 5,000 bytes).
        language_code: BCP-47 language code applied to all texts.
        region_name: AWS region override.

    Returns:
        A list of :class:`SentimentResult` objects in the same order as
        *texts*.

    Raises:
        RuntimeError: If the API call fails or any item is rejected.
        ValueError: If more than 25 texts are supplied.
    """
    if len(texts) > 25:
        raise ValueError("batch_detect_sentiment supports at most 25 texts")

    client = get_client("comprehend", region_name)
    try:
        resp = client.batch_detect_sentiment(TextList=texts, LanguageCode=language_code)
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_detect_sentiment failed") from exc

    if resp.get("ErrorList"):
        errors = resp["ErrorList"]
        raise AwsServiceError(f"batch_detect_sentiment had errors: {errors}")

    results = sorted(resp.get("ResultList", []), key=lambda r: r["Index"])
    return [
        SentimentResult(
            sentiment=r["Sentiment"],
            positive=r["SentimentScore"].get("Positive", 0.0),
            negative=r["SentimentScore"].get("Negative", 0.0),
            neutral=r["SentimentScore"].get("Neutral", 0.0),
            mixed=r["SentimentScore"].get("Mixed", 0.0),
        )
        for r in results
    ]


class BatchDetectDominantLanguageResult(BaseModel):
    """Result of batch_detect_dominant_language."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None
    error_list: list[dict[str, Any]] | None = None


class BatchDetectEntitiesResult(BaseModel):
    """Result of batch_detect_entities."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None
    error_list: list[dict[str, Any]] | None = None


class BatchDetectKeyPhrasesResult(BaseModel):
    """Result of batch_detect_key_phrases."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None
    error_list: list[dict[str, Any]] | None = None


class BatchDetectSyntaxResult(BaseModel):
    """Result of batch_detect_syntax."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None
    error_list: list[dict[str, Any]] | None = None


class BatchDetectTargetedSentimentResult(BaseModel):
    """Result of batch_detect_targeted_sentiment."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None
    error_list: list[dict[str, Any]] | None = None


class ClassifyDocumentResult(BaseModel):
    """Result of classify_document."""

    model_config = ConfigDict(frozen=True)

    classes: list[dict[str, Any]] | None = None
    labels: list[dict[str, Any]] | None = None
    document_metadata: dict[str, Any] | None = None
    document_type: list[dict[str, Any]] | None = None
    errors: list[dict[str, Any]] | None = None
    warnings: list[dict[str, Any]] | None = None


class ContainsPiiEntitiesResult(BaseModel):
    """Result of contains_pii_entities."""

    model_config = ConfigDict(frozen=True)

    labels: list[dict[str, Any]] | None = None


class CreateDatasetResult(BaseModel):
    """Result of create_dataset."""

    model_config = ConfigDict(frozen=True)

    dataset_arn: str | None = None


class CreateDocumentClassifierResult(BaseModel):
    """Result of create_document_classifier."""

    model_config = ConfigDict(frozen=True)

    document_classifier_arn: str | None = None


class CreateEndpointResult(BaseModel):
    """Result of create_endpoint."""

    model_config = ConfigDict(frozen=True)

    endpoint_arn: str | None = None
    model_arn: str | None = None


class CreateEntityRecognizerResult(BaseModel):
    """Result of create_entity_recognizer."""

    model_config = ConfigDict(frozen=True)

    entity_recognizer_arn: str | None = None


class CreateFlywheelResult(BaseModel):
    """Result of create_flywheel."""

    model_config = ConfigDict(frozen=True)

    flywheel_arn: str | None = None
    active_model_arn: str | None = None


class DescribeDatasetResult(BaseModel):
    """Result of describe_dataset."""

    model_config = ConfigDict(frozen=True)

    dataset_properties: dict[str, Any] | None = None


class DescribeDocumentClassificationJobResult(BaseModel):
    """Result of describe_document_classification_job."""

    model_config = ConfigDict(frozen=True)

    document_classification_job_properties: dict[str, Any] | None = None


class DescribeDocumentClassifierResult(BaseModel):
    """Result of describe_document_classifier."""

    model_config = ConfigDict(frozen=True)

    document_classifier_properties: dict[str, Any] | None = None


class DescribeDominantLanguageDetectionJobResult(BaseModel):
    """Result of describe_dominant_language_detection_job."""

    model_config = ConfigDict(frozen=True)

    dominant_language_detection_job_properties: dict[str, Any] | None = None


class DescribeEndpointResult(BaseModel):
    """Result of describe_endpoint."""

    model_config = ConfigDict(frozen=True)

    endpoint_properties: dict[str, Any] | None = None


class DescribeEntitiesDetectionJobResult(BaseModel):
    """Result of describe_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    entities_detection_job_properties: dict[str, Any] | None = None


class DescribeEntityRecognizerResult(BaseModel):
    """Result of describe_entity_recognizer."""

    model_config = ConfigDict(frozen=True)

    entity_recognizer_properties: dict[str, Any] | None = None


class DescribeEventsDetectionJobResult(BaseModel):
    """Result of describe_events_detection_job."""

    model_config = ConfigDict(frozen=True)

    events_detection_job_properties: dict[str, Any] | None = None


class DescribeFlywheelResult(BaseModel):
    """Result of describe_flywheel."""

    model_config = ConfigDict(frozen=True)

    flywheel_properties: dict[str, Any] | None = None


class DescribeFlywheelIterationResult(BaseModel):
    """Result of describe_flywheel_iteration."""

    model_config = ConfigDict(frozen=True)

    flywheel_iteration_properties: dict[str, Any] | None = None


class DescribeKeyPhrasesDetectionJobResult(BaseModel):
    """Result of describe_key_phrases_detection_job."""

    model_config = ConfigDict(frozen=True)

    key_phrases_detection_job_properties: dict[str, Any] | None = None


class DescribePiiEntitiesDetectionJobResult(BaseModel):
    """Result of describe_pii_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    pii_entities_detection_job_properties: dict[str, Any] | None = None


class DescribeResourcePolicyResult(BaseModel):
    """Result of describe_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_policy: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    policy_revision_id: str | None = None


class DescribeSentimentDetectionJobResult(BaseModel):
    """Result of describe_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    sentiment_detection_job_properties: dict[str, Any] | None = None


class DescribeTargetedSentimentDetectionJobResult(BaseModel):
    """Result of describe_targeted_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    targeted_sentiment_detection_job_properties: dict[str, Any] | None = None


class DescribeTopicsDetectionJobResult(BaseModel):
    """Result of describe_topics_detection_job."""

    model_config = ConfigDict(frozen=True)

    topics_detection_job_properties: dict[str, Any] | None = None


class DetectSyntaxResult(BaseModel):
    """Result of detect_syntax."""

    model_config = ConfigDict(frozen=True)

    syntax_tokens: list[dict[str, Any]] | None = None


class DetectTargetedSentimentResult(BaseModel):
    """Result of detect_targeted_sentiment."""

    model_config = ConfigDict(frozen=True)

    entities: list[dict[str, Any]] | None = None


class DetectToxicContentResult(BaseModel):
    """Result of detect_toxic_content."""

    model_config = ConfigDict(frozen=True)

    result_list: list[dict[str, Any]] | None = None


class ImportModelResult(BaseModel):
    """Result of import_model."""

    model_config = ConfigDict(frozen=True)

    model_arn: str | None = None


class ListDatasetsResult(BaseModel):
    """Result of list_datasets."""

    model_config = ConfigDict(frozen=True)

    dataset_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDocumentClassificationJobsResult(BaseModel):
    """Result of list_document_classification_jobs."""

    model_config = ConfigDict(frozen=True)

    document_classification_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDocumentClassifierSummariesResult(BaseModel):
    """Result of list_document_classifier_summaries."""

    model_config = ConfigDict(frozen=True)

    document_classifier_summaries_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDocumentClassifiersResult(BaseModel):
    """Result of list_document_classifiers."""

    model_config = ConfigDict(frozen=True)

    document_classifier_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDominantLanguageDetectionJobsResult(BaseModel):
    """Result of list_dominant_language_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    dominant_language_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEndpointsResult(BaseModel):
    """Result of list_endpoints."""

    model_config = ConfigDict(frozen=True)

    endpoint_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEntitiesDetectionJobsResult(BaseModel):
    """Result of list_entities_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    entities_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEntityRecognizerSummariesResult(BaseModel):
    """Result of list_entity_recognizer_summaries."""

    model_config = ConfigDict(frozen=True)

    entity_recognizer_summaries_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEntityRecognizersResult(BaseModel):
    """Result of list_entity_recognizers."""

    model_config = ConfigDict(frozen=True)

    entity_recognizer_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEventsDetectionJobsResult(BaseModel):
    """Result of list_events_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    events_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlywheelIterationHistoryResult(BaseModel):
    """Result of list_flywheel_iteration_history."""

    model_config = ConfigDict(frozen=True)

    flywheel_iteration_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlywheelsResult(BaseModel):
    """Result of list_flywheels."""

    model_config = ConfigDict(frozen=True)

    flywheel_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListKeyPhrasesDetectionJobsResult(BaseModel):
    """Result of list_key_phrases_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    key_phrases_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPiiEntitiesDetectionJobsResult(BaseModel):
    """Result of list_pii_entities_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    pii_entities_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSentimentDetectionJobsResult(BaseModel):
    """Result of list_sentiment_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    sentiment_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    tags: list[dict[str, Any]] | None = None


class ListTargetedSentimentDetectionJobsResult(BaseModel):
    """Result of list_targeted_sentiment_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    targeted_sentiment_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTopicsDetectionJobsResult(BaseModel):
    """Result of list_topics_detection_jobs."""

    model_config = ConfigDict(frozen=True)

    topics_detection_job_properties_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    policy_revision_id: str | None = None


class StartDocumentClassificationJobResult(BaseModel):
    """Result of start_document_classification_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None
    document_classifier_arn: str | None = None


class StartDominantLanguageDetectionJobResult(BaseModel):
    """Result of start_dominant_language_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartEntitiesDetectionJobResult(BaseModel):
    """Result of start_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None
    entity_recognizer_arn: str | None = None


class StartEventsDetectionJobResult(BaseModel):
    """Result of start_events_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartFlywheelIterationResult(BaseModel):
    """Result of start_flywheel_iteration."""

    model_config = ConfigDict(frozen=True)

    flywheel_arn: str | None = None
    flywheel_iteration_id: str | None = None


class StartKeyPhrasesDetectionJobResult(BaseModel):
    """Result of start_key_phrases_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartPiiEntitiesDetectionJobResult(BaseModel):
    """Result of start_pii_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartSentimentDetectionJobResult(BaseModel):
    """Result of start_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartTargetedSentimentDetectionJobResult(BaseModel):
    """Result of start_targeted_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StartTopicsDetectionJobResult(BaseModel):
    """Result of start_topics_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_arn: str | None = None
    job_status: str | None = None


class StopDominantLanguageDetectionJobResult(BaseModel):
    """Result of stop_dominant_language_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopEntitiesDetectionJobResult(BaseModel):
    """Result of stop_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopEventsDetectionJobResult(BaseModel):
    """Result of stop_events_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopKeyPhrasesDetectionJobResult(BaseModel):
    """Result of stop_key_phrases_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopPiiEntitiesDetectionJobResult(BaseModel):
    """Result of stop_pii_entities_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopSentimentDetectionJobResult(BaseModel):
    """Result of stop_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class StopTargetedSentimentDetectionJobResult(BaseModel):
    """Result of stop_targeted_sentiment_detection_job."""

    model_config = ConfigDict(frozen=True)

    job_id: str | None = None
    job_status: str | None = None


class UpdateEndpointResult(BaseModel):
    """Result of update_endpoint."""

    model_config = ConfigDict(frozen=True)

    desired_model_arn: str | None = None


class UpdateFlywheelResult(BaseModel):
    """Result of update_flywheel."""

    model_config = ConfigDict(frozen=True)

    flywheel_properties: dict[str, Any] | None = None


def batch_detect_dominant_language(
    text_list: list[str],
    region_name: str | None = None,
) -> BatchDetectDominantLanguageResult:
    """Batch detect dominant language.

    Args:
        text_list: Text list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextList"] = text_list
    try:
        resp = client.batch_detect_dominant_language(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch detect dominant language") from exc
    return BatchDetectDominantLanguageResult(
        result_list=resp.get("ResultList"),
        error_list=resp.get("ErrorList"),
    )


def batch_detect_entities(
    text_list: list[str],
    language_code: str,
    region_name: str | None = None,
) -> BatchDetectEntitiesResult:
    """Batch detect entities.

    Args:
        text_list: Text list.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextList"] = text_list
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.batch_detect_entities(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch detect entities") from exc
    return BatchDetectEntitiesResult(
        result_list=resp.get("ResultList"),
        error_list=resp.get("ErrorList"),
    )


def batch_detect_key_phrases(
    text_list: list[str],
    language_code: str,
    region_name: str | None = None,
) -> BatchDetectKeyPhrasesResult:
    """Batch detect key phrases.

    Args:
        text_list: Text list.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextList"] = text_list
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.batch_detect_key_phrases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch detect key phrases") from exc
    return BatchDetectKeyPhrasesResult(
        result_list=resp.get("ResultList"),
        error_list=resp.get("ErrorList"),
    )


def batch_detect_syntax(
    text_list: list[str],
    language_code: str,
    region_name: str | None = None,
) -> BatchDetectSyntaxResult:
    """Batch detect syntax.

    Args:
        text_list: Text list.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextList"] = text_list
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.batch_detect_syntax(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch detect syntax") from exc
    return BatchDetectSyntaxResult(
        result_list=resp.get("ResultList"),
        error_list=resp.get("ErrorList"),
    )


def batch_detect_targeted_sentiment(
    text_list: list[str],
    language_code: str,
    region_name: str | None = None,
) -> BatchDetectTargetedSentimentResult:
    """Batch detect targeted sentiment.

    Args:
        text_list: Text list.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextList"] = text_list
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.batch_detect_targeted_sentiment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch detect targeted sentiment") from exc
    return BatchDetectTargetedSentimentResult(
        result_list=resp.get("ResultList"),
        error_list=resp.get("ErrorList"),
    )


def classify_document(
    endpoint_arn: str,
    *,
    text: str | None = None,
    bytes: bytes | None = None,
    document_reader_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ClassifyDocumentResult:
    """Classify document.

    Args:
        endpoint_arn: Endpoint arn.
        text: Text.
        bytes: Bytes.
        document_reader_config: Document reader config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    if text is not None:
        kwargs["Text"] = text
    if bytes is not None:
        kwargs["Bytes"] = bytes
    if document_reader_config is not None:
        kwargs["DocumentReaderConfig"] = document_reader_config
    try:
        resp = client.classify_document(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to classify document") from exc
    return ClassifyDocumentResult(
        classes=resp.get("Classes"),
        labels=resp.get("Labels"),
        document_metadata=resp.get("DocumentMetadata"),
        document_type=resp.get("DocumentType"),
        errors=resp.get("Errors"),
        warnings=resp.get("Warnings"),
    )


def contains_pii_entities(
    text: str,
    language_code: str,
    region_name: str | None = None,
) -> ContainsPiiEntitiesResult:
    """Contains pii entities.

    Args:
        text: Text.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Text"] = text
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.contains_pii_entities(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to contains pii entities") from exc
    return ContainsPiiEntitiesResult(
        labels=resp.get("Labels"),
    )


def create_dataset(
    flywheel_arn: str,
    dataset_name: str,
    input_data_config: dict[str, Any],
    *,
    dataset_type: str | None = None,
    description: str | None = None,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDatasetResult:
    """Create dataset.

    Args:
        flywheel_arn: Flywheel arn.
        dataset_name: Dataset name.
        input_data_config: Input data config.
        dataset_type: Dataset type.
        description: Description.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    kwargs["DatasetName"] = dataset_name
    kwargs["InputDataConfig"] = input_data_config
    if dataset_type is not None:
        kwargs["DatasetType"] = dataset_type
    if description is not None:
        kwargs["Description"] = description
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create dataset") from exc
    return CreateDatasetResult(
        dataset_arn=resp.get("DatasetArn"),
    )


def create_document_classifier(
    document_classifier_name: str,
    data_access_role_arn: str,
    input_data_config: dict[str, Any],
    language_code: str,
    *,
    version_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    output_data_config: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    mode: str | None = None,
    model_kms_key_id: str | None = None,
    model_policy: str | None = None,
    region_name: str | None = None,
) -> CreateDocumentClassifierResult:
    """Create document classifier.

    Args:
        document_classifier_name: Document classifier name.
        data_access_role_arn: Data access role arn.
        input_data_config: Input data config.
        language_code: Language code.
        version_name: Version name.
        tags: Tags.
        output_data_config: Output data config.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        mode: Mode.
        model_kms_key_id: Model kms key id.
        model_policy: Model policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentClassifierName"] = document_classifier_name
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["InputDataConfig"] = input_data_config
    kwargs["LanguageCode"] = language_code
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if tags is not None:
        kwargs["Tags"] = tags
    if output_data_config is not None:
        kwargs["OutputDataConfig"] = output_data_config
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if mode is not None:
        kwargs["Mode"] = mode
    if model_kms_key_id is not None:
        kwargs["ModelKmsKeyId"] = model_kms_key_id
    if model_policy is not None:
        kwargs["ModelPolicy"] = model_policy
    try:
        resp = client.create_document_classifier(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create document classifier") from exc
    return CreateDocumentClassifierResult(
        document_classifier_arn=resp.get("DocumentClassifierArn"),
    )


def create_endpoint(
    endpoint_name: str,
    desired_inference_units: int,
    *,
    model_arn: str | None = None,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    data_access_role_arn: str | None = None,
    flywheel_arn: str | None = None,
    region_name: str | None = None,
) -> CreateEndpointResult:
    """Create endpoint.

    Args:
        endpoint_name: Endpoint name.
        desired_inference_units: Desired inference units.
        model_arn: Model arn.
        client_request_token: Client request token.
        tags: Tags.
        data_access_role_arn: Data access role arn.
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    kwargs["DesiredInferenceUnits"] = desired_inference_units
    if model_arn is not None:
        kwargs["ModelArn"] = model_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    if flywheel_arn is not None:
        kwargs["FlywheelArn"] = flywheel_arn
    try:
        resp = client.create_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create endpoint") from exc
    return CreateEndpointResult(
        endpoint_arn=resp.get("EndpointArn"),
        model_arn=resp.get("ModelArn"),
    )


def create_entity_recognizer(
    recognizer_name: str,
    data_access_role_arn: str,
    input_data_config: dict[str, Any],
    language_code: str,
    *,
    version_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    model_kms_key_id: str | None = None,
    model_policy: str | None = None,
    region_name: str | None = None,
) -> CreateEntityRecognizerResult:
    """Create entity recognizer.

    Args:
        recognizer_name: Recognizer name.
        data_access_role_arn: Data access role arn.
        input_data_config: Input data config.
        language_code: Language code.
        version_name: Version name.
        tags: Tags.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        model_kms_key_id: Model kms key id.
        model_policy: Model policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RecognizerName"] = recognizer_name
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["InputDataConfig"] = input_data_config
    kwargs["LanguageCode"] = language_code
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if tags is not None:
        kwargs["Tags"] = tags
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if model_kms_key_id is not None:
        kwargs["ModelKmsKeyId"] = model_kms_key_id
    if model_policy is not None:
        kwargs["ModelPolicy"] = model_policy
    try:
        resp = client.create_entity_recognizer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create entity recognizer") from exc
    return CreateEntityRecognizerResult(
        entity_recognizer_arn=resp.get("EntityRecognizerArn"),
    )


def create_flywheel(
    flywheel_name: str,
    data_access_role_arn: str,
    data_lake_s3_uri: str,
    *,
    active_model_arn: str | None = None,
    task_config: dict[str, Any] | None = None,
    model_type: str | None = None,
    data_security_config: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateFlywheelResult:
    """Create flywheel.

    Args:
        flywheel_name: Flywheel name.
        data_access_role_arn: Data access role arn.
        data_lake_s3_uri: Data lake s3 uri.
        active_model_arn: Active model arn.
        task_config: Task config.
        model_type: Model type.
        data_security_config: Data security config.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelName"] = flywheel_name
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["DataLakeS3Uri"] = data_lake_s3_uri
    if active_model_arn is not None:
        kwargs["ActiveModelArn"] = active_model_arn
    if task_config is not None:
        kwargs["TaskConfig"] = task_config
    if model_type is not None:
        kwargs["ModelType"] = model_type
    if data_security_config is not None:
        kwargs["DataSecurityConfig"] = data_security_config
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_flywheel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create flywheel") from exc
    return CreateFlywheelResult(
        flywheel_arn=resp.get("FlywheelArn"),
        active_model_arn=resp.get("ActiveModelArn"),
    )


def delete_document_classifier(
    document_classifier_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete document classifier.

    Args:
        document_classifier_arn: Document classifier arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentClassifierArn"] = document_classifier_arn
    try:
        client.delete_document_classifier(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete document classifier") from exc
    return None


def delete_endpoint(
    endpoint_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    try:
        client.delete_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete endpoint") from exc
    return None


def delete_entity_recognizer(
    entity_recognizer_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete entity recognizer.

    Args:
        entity_recognizer_arn: Entity recognizer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EntityRecognizerArn"] = entity_recognizer_arn
    try:
        client.delete_entity_recognizer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete entity recognizer") from exc
    return None


def delete_flywheel(
    flywheel_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete flywheel.

    Args:
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    try:
        client.delete_flywheel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete flywheel") from exc
    return None


def delete_resource_policy(
    resource_arn: str,
    *,
    policy_revision_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        policy_revision_id: Policy revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if policy_revision_id is not None:
        kwargs["PolicyRevisionId"] = policy_revision_id
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


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
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    try:
        resp = client.describe_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset") from exc
    return DescribeDatasetResult(
        dataset_properties=resp.get("DatasetProperties"),
    )


def describe_document_classification_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeDocumentClassificationJobResult:
    """Describe document classification job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_document_classification_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe document classification job") from exc
    return DescribeDocumentClassificationJobResult(
        document_classification_job_properties=resp.get("DocumentClassificationJobProperties"),
    )


def describe_document_classifier(
    document_classifier_arn: str,
    region_name: str | None = None,
) -> DescribeDocumentClassifierResult:
    """Describe document classifier.

    Args:
        document_classifier_arn: Document classifier arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentClassifierArn"] = document_classifier_arn
    try:
        resp = client.describe_document_classifier(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe document classifier") from exc
    return DescribeDocumentClassifierResult(
        document_classifier_properties=resp.get("DocumentClassifierProperties"),
    )


def describe_dominant_language_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeDominantLanguageDetectionJobResult:
    """Describe dominant language detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_dominant_language_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe dominant language detection job") from exc
    return DescribeDominantLanguageDetectionJobResult(
        dominant_language_detection_job_properties=resp.get(
            "DominantLanguageDetectionJobProperties"
        ),
    )


def describe_endpoint(
    endpoint_arn: str,
    region_name: str | None = None,
) -> DescribeEndpointResult:
    """Describe endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    try:
        resp = client.describe_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint") from exc
    return DescribeEndpointResult(
        endpoint_properties=resp.get("EndpointProperties"),
    )


def describe_entities_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeEntitiesDetectionJobResult:
    """Describe entities detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe entities detection job") from exc
    return DescribeEntitiesDetectionJobResult(
        entities_detection_job_properties=resp.get("EntitiesDetectionJobProperties"),
    )


def describe_entity_recognizer(
    entity_recognizer_arn: str,
    region_name: str | None = None,
) -> DescribeEntityRecognizerResult:
    """Describe entity recognizer.

    Args:
        entity_recognizer_arn: Entity recognizer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EntityRecognizerArn"] = entity_recognizer_arn
    try:
        resp = client.describe_entity_recognizer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe entity recognizer") from exc
    return DescribeEntityRecognizerResult(
        entity_recognizer_properties=resp.get("EntityRecognizerProperties"),
    )


def describe_events_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeEventsDetectionJobResult:
    """Describe events detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_events_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe events detection job") from exc
    return DescribeEventsDetectionJobResult(
        events_detection_job_properties=resp.get("EventsDetectionJobProperties"),
    )


def describe_flywheel(
    flywheel_arn: str,
    region_name: str | None = None,
) -> DescribeFlywheelResult:
    """Describe flywheel.

    Args:
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    try:
        resp = client.describe_flywheel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe flywheel") from exc
    return DescribeFlywheelResult(
        flywheel_properties=resp.get("FlywheelProperties"),
    )


def describe_flywheel_iteration(
    flywheel_arn: str,
    flywheel_iteration_id: str,
    region_name: str | None = None,
) -> DescribeFlywheelIterationResult:
    """Describe flywheel iteration.

    Args:
        flywheel_arn: Flywheel arn.
        flywheel_iteration_id: Flywheel iteration id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    kwargs["FlywheelIterationId"] = flywheel_iteration_id
    try:
        resp = client.describe_flywheel_iteration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe flywheel iteration") from exc
    return DescribeFlywheelIterationResult(
        flywheel_iteration_properties=resp.get("FlywheelIterationProperties"),
    )


def describe_key_phrases_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeKeyPhrasesDetectionJobResult:
    """Describe key phrases detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_key_phrases_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe key phrases detection job") from exc
    return DescribeKeyPhrasesDetectionJobResult(
        key_phrases_detection_job_properties=resp.get("KeyPhrasesDetectionJobProperties"),
    )


def describe_pii_entities_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribePiiEntitiesDetectionJobResult:
    """Describe pii entities detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_pii_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pii entities detection job") from exc
    return DescribePiiEntitiesDetectionJobResult(
        pii_entities_detection_job_properties=resp.get("PiiEntitiesDetectionJobProperties"),
    )


def describe_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> DescribeResourcePolicyResult:
    """Describe resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.describe_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe resource policy") from exc
    return DescribeResourcePolicyResult(
        resource_policy=resp.get("ResourcePolicy"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        policy_revision_id=resp.get("PolicyRevisionId"),
    )


def describe_sentiment_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeSentimentDetectionJobResult:
    """Describe sentiment detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe sentiment detection job") from exc
    return DescribeSentimentDetectionJobResult(
        sentiment_detection_job_properties=resp.get("SentimentDetectionJobProperties"),
    )


def describe_targeted_sentiment_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeTargetedSentimentDetectionJobResult:
    """Describe targeted sentiment detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_targeted_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe targeted sentiment detection job") from exc
    return DescribeTargetedSentimentDetectionJobResult(
        targeted_sentiment_detection_job_properties=resp.get(
            "TargetedSentimentDetectionJobProperties"
        ),
    )


def describe_topics_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeTopicsDetectionJobResult:
    """Describe topics detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_topics_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe topics detection job") from exc
    return DescribeTopicsDetectionJobResult(
        topics_detection_job_properties=resp.get("TopicsDetectionJobProperties"),
    )


def detect_syntax(
    text: str,
    language_code: str,
    region_name: str | None = None,
) -> DetectSyntaxResult:
    """Detect syntax.

    Args:
        text: Text.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Text"] = text
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.detect_syntax(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect syntax") from exc
    return DetectSyntaxResult(
        syntax_tokens=resp.get("SyntaxTokens"),
    )


def detect_targeted_sentiment(
    text: str,
    language_code: str,
    region_name: str | None = None,
) -> DetectTargetedSentimentResult:
    """Detect targeted sentiment.

    Args:
        text: Text.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Text"] = text
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.detect_targeted_sentiment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect targeted sentiment") from exc
    return DetectTargetedSentimentResult(
        entities=resp.get("Entities"),
    )


def detect_toxic_content(
    text_segments: list[dict[str, Any]],
    language_code: str,
    region_name: str | None = None,
) -> DetectToxicContentResult:
    """Detect toxic content.

    Args:
        text_segments: Text segments.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TextSegments"] = text_segments
    kwargs["LanguageCode"] = language_code
    try:
        resp = client.detect_toxic_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect toxic content") from exc
    return DetectToxicContentResult(
        result_list=resp.get("ResultList"),
    )


def import_model(
    source_model_arn: str,
    *,
    model_name: str | None = None,
    version_name: str | None = None,
    model_kms_key_id: str | None = None,
    data_access_role_arn: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportModelResult:
    """Import model.

    Args:
        source_model_arn: Source model arn.
        model_name: Model name.
        version_name: Version name.
        model_kms_key_id: Model kms key id.
        data_access_role_arn: Data access role arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceModelArn"] = source_model_arn
    if model_name is not None:
        kwargs["ModelName"] = model_name
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if model_kms_key_id is not None:
        kwargs["ModelKmsKeyId"] = model_kms_key_id
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.import_model(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import model") from exc
    return ImportModelResult(
        model_arn=resp.get("ModelArn"),
    )


def list_datasets(
    *,
    flywheel_arn: str | None = None,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetsResult:
    """List datasets.

    Args:
        flywheel_arn: Flywheel arn.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if flywheel_arn is not None:
        kwargs["FlywheelArn"] = flywheel_arn
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_datasets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list datasets") from exc
    return ListDatasetsResult(
        dataset_properties_list=resp.get("DatasetPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_document_classification_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDocumentClassificationJobsResult:
    """List document classification jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_document_classification_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list document classification jobs") from exc
    return ListDocumentClassificationJobsResult(
        document_classification_job_properties_list=resp.get(
            "DocumentClassificationJobPropertiesList"
        ),
        next_token=resp.get("NextToken"),
    )


def list_document_classifier_summaries(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDocumentClassifierSummariesResult:
    """List document classifier summaries.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_document_classifier_summaries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list document classifier summaries") from exc
    return ListDocumentClassifierSummariesResult(
        document_classifier_summaries_list=resp.get("DocumentClassifierSummariesList"),
        next_token=resp.get("NextToken"),
    )


def list_document_classifiers(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDocumentClassifiersResult:
    """List document classifiers.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_document_classifiers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list document classifiers") from exc
    return ListDocumentClassifiersResult(
        document_classifier_properties_list=resp.get("DocumentClassifierPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_dominant_language_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDominantLanguageDetectionJobsResult:
    """List dominant language detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_dominant_language_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dominant language detection jobs") from exc
    return ListDominantLanguageDetectionJobsResult(
        dominant_language_detection_job_properties_list=resp.get(
            "DominantLanguageDetectionJobPropertiesList"
        ),
        next_token=resp.get("NextToken"),
    )


def list_endpoints(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEndpointsResult:
    """List endpoints.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list endpoints") from exc
    return ListEndpointsResult(
        endpoint_properties_list=resp.get("EndpointPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_entities_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEntitiesDetectionJobsResult:
    """List entities detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_entities_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list entities detection jobs") from exc
    return ListEntitiesDetectionJobsResult(
        entities_detection_job_properties_list=resp.get("EntitiesDetectionJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_entity_recognizer_summaries(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEntityRecognizerSummariesResult:
    """List entity recognizer summaries.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_entity_recognizer_summaries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list entity recognizer summaries") from exc
    return ListEntityRecognizerSummariesResult(
        entity_recognizer_summaries_list=resp.get("EntityRecognizerSummariesList"),
        next_token=resp.get("NextToken"),
    )


def list_entity_recognizers(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEntityRecognizersResult:
    """List entity recognizers.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_entity_recognizers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list entity recognizers") from exc
    return ListEntityRecognizersResult(
        entity_recognizer_properties_list=resp.get("EntityRecognizerPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_events_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEventsDetectionJobsResult:
    """List events detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_events_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list events detection jobs") from exc
    return ListEventsDetectionJobsResult(
        events_detection_job_properties_list=resp.get("EventsDetectionJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_flywheel_iteration_history(
    flywheel_arn: str,
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFlywheelIterationHistoryResult:
    """List flywheel iteration history.

    Args:
        flywheel_arn: Flywheel arn.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_flywheel_iteration_history(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flywheel iteration history") from exc
    return ListFlywheelIterationHistoryResult(
        flywheel_iteration_properties_list=resp.get("FlywheelIterationPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_flywheels(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFlywheelsResult:
    """List flywheels.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_flywheels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flywheels") from exc
    return ListFlywheelsResult(
        flywheel_summary_list=resp.get("FlywheelSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_key_phrases_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListKeyPhrasesDetectionJobsResult:
    """List key phrases detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_key_phrases_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list key phrases detection jobs") from exc
    return ListKeyPhrasesDetectionJobsResult(
        key_phrases_detection_job_properties_list=resp.get("KeyPhrasesDetectionJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def list_pii_entities_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPiiEntitiesDetectionJobsResult:
    """List pii entities detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_pii_entities_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list pii entities detection jobs") from exc
    return ListPiiEntitiesDetectionJobsResult(
        pii_entities_detection_job_properties_list=resp.get(
            "PiiEntitiesDetectionJobPropertiesList"
        ),
        next_token=resp.get("NextToken"),
    )


def list_sentiment_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSentimentDetectionJobsResult:
    """List sentiment detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_sentiment_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list sentiment detection jobs") from exc
    return ListSentimentDetectionJobsResult(
        sentiment_detection_job_properties_list=resp.get("SentimentDetectionJobPropertiesList"),
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
    client = get_client("comprehend", region_name)
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


def list_targeted_sentiment_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTargetedSentimentDetectionJobsResult:
    """List targeted sentiment detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_targeted_sentiment_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list targeted sentiment detection jobs") from exc
    return ListTargetedSentimentDetectionJobsResult(
        targeted_sentiment_detection_job_properties_list=resp.get(
            "TargetedSentimentDetectionJobPropertiesList"
        ),
        next_token=resp.get("NextToken"),
    )


def list_topics_detection_jobs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTopicsDetectionJobsResult:
    """List topics detection jobs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_topics_detection_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list topics detection jobs") from exc
    return ListTopicsDetectionJobsResult(
        topics_detection_job_properties_list=resp.get("TopicsDetectionJobPropertiesList"),
        next_token=resp.get("NextToken"),
    )


def put_resource_policy(
    resource_arn: str,
    resource_policy: str,
    *,
    policy_revision_id: str | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        resource_policy: Resource policy.
        policy_revision_id: Policy revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["ResourcePolicy"] = resource_policy
    if policy_revision_id is not None:
        kwargs["PolicyRevisionId"] = policy_revision_id
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        policy_revision_id=resp.get("PolicyRevisionId"),
    )


def start_document_classification_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    *,
    job_name: str | None = None,
    document_classifier_arn: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    flywheel_arn: str | None = None,
    region_name: str | None = None,
) -> StartDocumentClassificationJobResult:
    """Start document classification job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        job_name: Job name.
        document_classifier_arn: Document classifier arn.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    if job_name is not None:
        kwargs["JobName"] = job_name
    if document_classifier_arn is not None:
        kwargs["DocumentClassifierArn"] = document_classifier_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    if flywheel_arn is not None:
        kwargs["FlywheelArn"] = flywheel_arn
    try:
        resp = client.start_document_classification_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start document classification job") from exc
    return StartDocumentClassificationJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
        document_classifier_arn=resp.get("DocumentClassifierArn"),
    )


def start_dominant_language_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    *,
    job_name: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartDominantLanguageDetectionJobResult:
    """Start dominant language detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        job_name: Job name.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_dominant_language_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start dominant language detection job") from exc
    return StartDominantLanguageDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_entities_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    language_code: str,
    *,
    job_name: str | None = None,
    entity_recognizer_arn: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    flywheel_arn: str | None = None,
    region_name: str | None = None,
) -> StartEntitiesDetectionJobResult:
    """Start entities detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        job_name: Job name.
        entity_recognizer_arn: Entity recognizer arn.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    if job_name is not None:
        kwargs["JobName"] = job_name
    if entity_recognizer_arn is not None:
        kwargs["EntityRecognizerArn"] = entity_recognizer_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    if flywheel_arn is not None:
        kwargs["FlywheelArn"] = flywheel_arn
    try:
        resp = client.start_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start entities detection job") from exc
    return StartEntitiesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
        entity_recognizer_arn=resp.get("EntityRecognizerArn"),
    )


def start_events_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    language_code: str,
    target_event_types: list[str],
    *,
    job_name: str | None = None,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartEventsDetectionJobResult:
    """Start events detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        target_event_types: Target event types.
        job_name: Job name.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    kwargs["TargetEventTypes"] = target_event_types
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_events_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start events detection job") from exc
    return StartEventsDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_flywheel_iteration(
    flywheel_arn: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartFlywheelIterationResult:
    """Start flywheel iteration.

    Args:
        flywheel_arn: Flywheel arn.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.start_flywheel_iteration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start flywheel iteration") from exc
    return StartFlywheelIterationResult(
        flywheel_arn=resp.get("FlywheelArn"),
        flywheel_iteration_id=resp.get("FlywheelIterationId"),
    )


def start_key_phrases_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    language_code: str,
    *,
    job_name: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartKeyPhrasesDetectionJobResult:
    """Start key phrases detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        job_name: Job name.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_key_phrases_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start key phrases detection job") from exc
    return StartKeyPhrasesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_pii_entities_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    mode: str,
    data_access_role_arn: str,
    language_code: str,
    *,
    redaction_config: dict[str, Any] | None = None,
    job_name: str | None = None,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartPiiEntitiesDetectionJobResult:
    """Start pii entities detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        mode: Mode.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        redaction_config: Redaction config.
        job_name: Job name.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["Mode"] = mode
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    if redaction_config is not None:
        kwargs["RedactionConfig"] = redaction_config
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_pii_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start pii entities detection job") from exc
    return StartPiiEntitiesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_sentiment_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    language_code: str,
    *,
    job_name: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartSentimentDetectionJobResult:
    """Start sentiment detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        job_name: Job name.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start sentiment detection job") from exc
    return StartSentimentDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_targeted_sentiment_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    language_code: str,
    *,
    job_name: str | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartTargetedSentimentDetectionJobResult:
    """Start targeted sentiment detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        language_code: Language code.
        job_name: Job name.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    kwargs["LanguageCode"] = language_code
    if job_name is not None:
        kwargs["JobName"] = job_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_targeted_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start targeted sentiment detection job") from exc
    return StartTargetedSentimentDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def start_topics_detection_job(
    input_data_config: dict[str, Any],
    output_data_config: dict[str, Any],
    data_access_role_arn: str,
    *,
    job_name: str | None = None,
    number_of_topics: int | None = None,
    client_request_token: str | None = None,
    volume_kms_key_id: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartTopicsDetectionJobResult:
    """Start topics detection job.

    Args:
        input_data_config: Input data config.
        output_data_config: Output data config.
        data_access_role_arn: Data access role arn.
        job_name: Job name.
        number_of_topics: Number of topics.
        client_request_token: Client request token.
        volume_kms_key_id: Volume kms key id.
        vpc_config: Vpc config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InputDataConfig"] = input_data_config
    kwargs["OutputDataConfig"] = output_data_config
    kwargs["DataAccessRoleArn"] = data_access_role_arn
    if job_name is not None:
        kwargs["JobName"] = job_name
    if number_of_topics is not None:
        kwargs["NumberOfTopics"] = number_of_topics
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if volume_kms_key_id is not None:
        kwargs["VolumeKmsKeyId"] = volume_kms_key_id
    if vpc_config is not None:
        kwargs["VpcConfig"] = vpc_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_topics_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start topics detection job") from exc
    return StartTopicsDetectionJobResult(
        job_id=resp.get("JobId"),
        job_arn=resp.get("JobArn"),
        job_status=resp.get("JobStatus"),
    )


def stop_dominant_language_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopDominantLanguageDetectionJobResult:
    """Stop dominant language detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_dominant_language_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop dominant language detection job") from exc
    return StopDominantLanguageDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_entities_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopEntitiesDetectionJobResult:
    """Stop entities detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop entities detection job") from exc
    return StopEntitiesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_events_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopEventsDetectionJobResult:
    """Stop events detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_events_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop events detection job") from exc
    return StopEventsDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_key_phrases_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopKeyPhrasesDetectionJobResult:
    """Stop key phrases detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_key_phrases_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop key phrases detection job") from exc
    return StopKeyPhrasesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_pii_entities_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopPiiEntitiesDetectionJobResult:
    """Stop pii entities detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_pii_entities_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop pii entities detection job") from exc
    return StopPiiEntitiesDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_sentiment_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopSentimentDetectionJobResult:
    """Stop sentiment detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop sentiment detection job") from exc
    return StopSentimentDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_targeted_sentiment_detection_job(
    job_id: str,
    region_name: str | None = None,
) -> StopTargetedSentimentDetectionJobResult:
    """Stop targeted sentiment detection job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_targeted_sentiment_detection_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop targeted sentiment detection job") from exc
    return StopTargetedSentimentDetectionJobResult(
        job_id=resp.get("JobId"),
        job_status=resp.get("JobStatus"),
    )


def stop_training_document_classifier(
    document_classifier_arn: str,
    region_name: str | None = None,
) -> None:
    """Stop training document classifier.

    Args:
        document_classifier_arn: Document classifier arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentClassifierArn"] = document_classifier_arn
    try:
        client.stop_training_document_classifier(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop training document classifier") from exc
    return None


def stop_training_entity_recognizer(
    entity_recognizer_arn: str,
    region_name: str | None = None,
) -> None:
    """Stop training entity recognizer.

    Args:
        entity_recognizer_arn: Entity recognizer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EntityRecognizerArn"] = entity_recognizer_arn
    try:
        client.stop_training_entity_recognizer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop training entity recognizer") from exc
    return None


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
    client = get_client("comprehend", region_name)
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
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_endpoint(
    endpoint_arn: str,
    *,
    desired_model_arn: str | None = None,
    desired_inference_units: int | None = None,
    desired_data_access_role_arn: str | None = None,
    flywheel_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateEndpointResult:
    """Update endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        desired_model_arn: Desired model arn.
        desired_inference_units: Desired inference units.
        desired_data_access_role_arn: Desired data access role arn.
        flywheel_arn: Flywheel arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    if desired_model_arn is not None:
        kwargs["DesiredModelArn"] = desired_model_arn
    if desired_inference_units is not None:
        kwargs["DesiredInferenceUnits"] = desired_inference_units
    if desired_data_access_role_arn is not None:
        kwargs["DesiredDataAccessRoleArn"] = desired_data_access_role_arn
    if flywheel_arn is not None:
        kwargs["FlywheelArn"] = flywheel_arn
    try:
        resp = client.update_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update endpoint") from exc
    return UpdateEndpointResult(
        desired_model_arn=resp.get("DesiredModelArn"),
    )


def update_flywheel(
    flywheel_arn: str,
    *,
    active_model_arn: str | None = None,
    data_access_role_arn: str | None = None,
    data_security_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFlywheelResult:
    """Update flywheel.

    Args:
        flywheel_arn: Flywheel arn.
        active_model_arn: Active model arn.
        data_access_role_arn: Data access role arn.
        data_security_config: Data security config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("comprehend", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FlywheelArn"] = flywheel_arn
    if active_model_arn is not None:
        kwargs["ActiveModelArn"] = active_model_arn
    if data_access_role_arn is not None:
        kwargs["DataAccessRoleArn"] = data_access_role_arn
    if data_security_config is not None:
        kwargs["DataSecurityConfig"] = data_security_config
    try:
        resp = client.update_flywheel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update flywheel") from exc
    return UpdateFlywheelResult(
        flywheel_properties=resp.get("FlywheelProperties"),
    )
