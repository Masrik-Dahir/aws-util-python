"""AI/ML Serverless Pipeline utilities for multi-service orchestration.

Provides helpers for chaining AI/ML services in serverless pipelines:

- **Bedrock serverless chain** — Chain multiple Bedrock model invocations
  with DynamoDB conversation state.
- **S3 document processor** — S3 upload processing pipeline with Textract
  extraction and Comprehend analysis, results stored in DynamoDB.
- **Image moderation pipeline** — S3 image processing with Rekognition
  moderation and label detection, DynamoDB storage, and SNS alerting.
- **Translation pipeline** — Batch translate S3 documents via Translate,
  store translated text back to S3 with metadata in DynamoDB.
- **Embedding indexer** — Generate embeddings via Bedrock Titan model,
  store vectors and metadata in DynamoDB.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "BatchTransformResult",
    "BedrockChainResult",
    "DocumentProcessorResult",
    "EmbeddingIndexResult",
    "FaceIndexResult",
    "ForecastExportResult",
    "FormExtractResult",
    "GuardrailResult",
    "ImageModerationResult",
    "KBIngestResult",
    "PIIRedactorResult",
    "PollyAudioResult",
    "RecommenderResult",
    "TranscribeJobResult",
    "TranslationResult",
    "VideoLabelResult",
    "bedrock_guardrail_enforcer",
    "bedrock_knowledge_base_ingestor",
    "bedrock_serverless_chain",
    "comprehend_pii_redactor",
    "embedding_indexer",
    "forecast_inference_pipeline",
    "image_moderation_pipeline",
    "personalize_real_time_recommender",
    "polly_audio_generator",
    "rekognition_face_indexer",
    "rekognition_video_label_pipeline",
    "s3_document_processor",
    "sagemaker_batch_transform_monitor",
    "textract_form_extractor",
    "transcribe_job_to_s3",
    "translation_pipeline",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class BedrockChainResult(BaseModel):
    """Result of a chained Bedrock conversation."""

    model_config = ConfigDict(frozen=True)

    conversation_id: str
    steps_completed: int
    outputs: list[str]
    model_id: str


class DocumentProcessorResult(BaseModel):
    """Result of S3 document processing pipeline."""

    model_config = ConfigDict(frozen=True)

    bucket: str
    key: str
    extracted_text: str
    sentiment: str
    sentiment_scores: dict[str, float]
    entities: list[dict[str, Any]]


class ImageModerationResult(BaseModel):
    """Result of image moderation pipeline."""

    model_config = ConfigDict(frozen=True)

    bucket: str
    key: str
    moderation_labels: list[dict[str, Any]]
    labels: list[dict[str, Any]]
    flagged: bool
    alert_sent: bool
    message_id: str | None = None


class TranslationResult(BaseModel):
    """Result of batch translation pipeline."""

    model_config = ConfigDict(frozen=True)

    translated_count: int
    source_language: str
    target_language: str
    output_keys: list[str]


class EmbeddingIndexResult(BaseModel):
    """Result of embedding indexing pipeline."""

    model_config = ConfigDict(frozen=True)

    items_indexed: int
    model_id: str
    dimensions: int


# ---------------------------------------------------------------------------
# 1. Bedrock Serverless Chain
# ---------------------------------------------------------------------------


def bedrock_serverless_chain(
    prompts: list[str],
    model_id: str,
    conversation_id: str,
    table_name: str,
    region_name: str | None = None,
) -> BedrockChainResult:
    """Chain multiple Bedrock model invocations with DynamoDB state.

    Each prompt is sent to the Bedrock model with the previous output
    as context.  The full conversation is stored in DynamoDB.

    Args:
        prompts: List of prompt strings to process sequentially.
        model_id: Bedrock model identifier (e.g.
            ``"anthropic.claude-3-haiku-20240307-v1:0"``).
        conversation_id: Unique identifier for this conversation.
        table_name: DynamoDB table name for conversation state.
        region_name: AWS region override.

    Returns:
        A :class:`BedrockChainResult` with all outputs.

    Raises:
        RuntimeError: If Bedrock invocation or DynamoDB write fails.
    """
    bedrock = get_client("bedrock-runtime", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    outputs: list[str] = []
    context = ""

    for idx, prompt in enumerate(prompts):
        full_prompt = f"{context}\n\n{prompt}" if context else prompt

        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": full_prompt},
                ],
            }
        )

        try:
            resp = bedrock.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Bedrock invocation failed at step {idx}") from exc

        resp_body = json.loads(resp["body"].read())
        output_text = resp_body.get("content", [{}])[0].get("text", "")
        outputs.append(output_text)
        context = output_text

    # Store conversation in DynamoDB
    ts = int(time.time())
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"conversation#{conversation_id}"},
                "sk": {"S": str(ts)},
                "model_id": {"S": model_id},
                "prompts": {
                    "S": json.dumps(prompts),
                },
                "outputs": {
                    "S": json.dumps(outputs),
                },
                "steps": {"N": str(len(outputs))},
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to store conversation {conversation_id}") from exc

    return BedrockChainResult(
        conversation_id=conversation_id,
        steps_completed=len(outputs),
        outputs=outputs,
        model_id=model_id,
    )


# ---------------------------------------------------------------------------
# 2. S3 Document Processor
# ---------------------------------------------------------------------------


def s3_document_processor(
    bucket: str,
    key: str,
    table_name: str,
    region_name: str | None = None,
) -> DocumentProcessorResult:
    """Process an S3 document through Textract and Comprehend.

    Reads a document from S3, extracts text with Textract, runs
    Comprehend sentiment analysis and entity detection, and stores
    the combined results in DynamoDB.

    Args:
        bucket: S3 bucket containing the document.
        key: S3 object key of the document.
        table_name: DynamoDB table for results storage.
        region_name: AWS region override.

    Returns:
        A :class:`DocumentProcessorResult` with extraction and
        analysis results.

    Raises:
        RuntimeError: If any service call fails.
    """
    s3 = get_client("s3", region_name=region_name)
    textract = get_client("textract", region_name=region_name)
    comprehend = get_client("comprehend", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Read document from S3
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        doc_bytes = resp["Body"].read()
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to read s3://{bucket}/{key}") from exc

    # Extract text with Textract
    try:
        textract_resp = textract.detect_document_text(Document={"Bytes": doc_bytes})
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Textract extraction failed for {key}") from exc

    lines = [
        block["Text"]
        for block in textract_resp.get("Blocks", [])
        if block.get("BlockType") == "LINE" and "Text" in block
    ]
    extracted_text = "\n".join(lines)

    # Comprehend sentiment analysis
    try:
        sentiment_resp = comprehend.detect_sentiment(
            Text=extracted_text or "empty",
            LanguageCode="en",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Comprehend sentiment analysis failed") from exc

    sentiment = sentiment_resp.get("Sentiment", "UNKNOWN")
    sentiment_scores = sentiment_resp.get("SentimentScore", {})

    # Comprehend entity detection
    try:
        entity_resp = comprehend.detect_entities(
            Text=extracted_text or "empty",
            LanguageCode="en",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Comprehend entity detection failed") from exc

    entities = entity_resp.get("Entities", [])

    # Store results in DynamoDB
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"doc#{bucket}/{key}"},
                "extracted_text": {"S": extracted_text},
                "sentiment": {"S": sentiment},
                "sentiment_scores": {
                    "S": json.dumps(sentiment_scores),
                },
                "entities": {
                    "S": json.dumps(entities, default=str),
                },
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to store results for {key}") from exc

    return DocumentProcessorResult(
        bucket=bucket,
        key=key,
        extracted_text=extracted_text,
        sentiment=sentiment,
        sentiment_scores=sentiment_scores,
        entities=entities,
    )


# ---------------------------------------------------------------------------
# 3. Image Moderation Pipeline
# ---------------------------------------------------------------------------


def image_moderation_pipeline(
    bucket: str,
    key: str,
    table_name: str,
    sns_topic_arn: str | None = None,
    confidence_threshold: float = 75.0,
    region_name: str | None = None,
) -> ImageModerationResult:
    """Process an S3 image through Rekognition moderation and labelling.

    Reads an image from S3, runs Rekognition moderation-label detection
    and general label detection, stores results in DynamoDB, and sends
    an SNS alert if any moderation label exceeds the confidence
    threshold.

    Args:
        bucket: S3 bucket containing the image.
        key: S3 object key of the image.
        table_name: DynamoDB table for results storage.
        sns_topic_arn: Optional SNS topic for moderation alerts.
        confidence_threshold: Minimum confidence to flag an image
            (default 75.0).
        region_name: AWS region override.

    Returns:
        An :class:`ImageModerationResult` with labels and alert info.

    Raises:
        RuntimeError: If any service call fails.
    """
    s3 = get_client("s3", region_name=region_name)
    rek = get_client("rekognition", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Read image from S3
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = resp["Body"].read()
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to read s3://{bucket}/{key}") from exc

    # Rekognition moderation labels
    try:
        mod_resp = rek.detect_moderation_labels(
            Image={"Bytes": image_bytes},
            MinConfidence=confidence_threshold,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Rekognition moderation failed for {key}") from exc

    moderation_labels = mod_resp.get("ModerationLabels", [])

    # Rekognition general labels
    try:
        label_resp = rek.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=20,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Rekognition label detection failed for {key}") from exc

    labels = label_resp.get("Labels", [])

    flagged = len(moderation_labels) > 0

    # Store results in DynamoDB
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"image#{bucket}/{key}"},
                "moderation_labels": {
                    "S": json.dumps(moderation_labels, default=str),
                },
                "labels": {
                    "S": json.dumps(labels, default=str),
                },
                "flagged": {"BOOL": flagged},
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to store results for {key}") from exc

    # Send SNS alert if flagged
    alert_sent = False
    message_id: str | None = None
    if flagged and sns_topic_arn:
        sns = get_client("sns", region_name=region_name)
        try:
            alert_resp = sns.publish(
                TopicArn=sns_topic_arn,
                Subject="Image Moderation Alert",
                Message=json.dumps(
                    {
                        "bucket": bucket,
                        "key": key,
                        "moderation_labels": moderation_labels,
                    },
                    default=str,
                ),
            )
            alert_sent = True
            message_id = alert_resp.get("MessageId")
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to send moderation alert") from exc

    return ImageModerationResult(
        bucket=bucket,
        key=key,
        moderation_labels=moderation_labels,
        labels=labels,
        flagged=flagged,
        alert_sent=alert_sent,
        message_id=message_id,
    )


# ---------------------------------------------------------------------------
# 4. Translation Pipeline
# ---------------------------------------------------------------------------


def translation_pipeline(
    bucket: str,
    source_keys: list[str],
    target_language: str,
    table_name: str,
    output_prefix: str = "translated/",
    source_language: str = "en",
    region_name: str | None = None,
) -> TranslationResult:
    """Batch translate S3 documents and store results.

    Reads text from each S3 key, translates via AWS Translate, stores
    the translated text back to S3 under *output_prefix*, and records
    metadata in DynamoDB.

    Args:
        bucket: S3 bucket containing source documents.
        source_keys: List of S3 keys to translate.
        target_language: Target language code (e.g. ``"es"``).
        table_name: DynamoDB table for metadata storage.
        output_prefix: S3 key prefix for translated output.
        source_language: Source language code (default ``"en"``).
        region_name: AWS region override.

    Returns:
        A :class:`TranslationResult` with counts and output keys.

    Raises:
        RuntimeError: If any service call fails.
    """
    s3 = get_client("s3", region_name=region_name)
    translate = get_client("translate", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    output_keys: list[str] = []
    translated_count = 0

    for src_key in source_keys:
        # Read source text
        try:
            resp = s3.get_object(Bucket=bucket, Key=src_key)
            text = resp["Body"].read().decode("utf-8")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to read s3://{bucket}/{src_key}") from exc

        # Translate
        try:
            trans_resp = translate.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Translation failed for {src_key}") from exc

        translated_text = trans_resp.get("TranslatedText", "")
        detected_source = trans_resp.get("SourceLanguageCode", source_language)

        # Store translated text in S3
        out_key = f"{output_prefix}{target_language}/{src_key}"
        try:
            s3.put_object(
                Bucket=bucket,
                Key=out_key,
                Body=translated_text.encode("utf-8"),
                ContentType="text/plain",
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to write s3://{bucket}/{out_key}") from exc

        output_keys.append(out_key)

        # Store metadata in DynamoDB
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {
                        "S": f"translation#{src_key}",
                    },
                    "source_language": {"S": detected_source},
                    "target_language": {"S": target_language},
                    "source_key": {"S": src_key},
                    "output_key": {"S": out_key},
                    "timestamp": {
                        "N": str(int(time.time())),
                    },
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to store metadata for {src_key}") from exc

        translated_count += 1

    return TranslationResult(
        translated_count=translated_count,
        source_language=source_language,
        target_language=target_language,
        output_keys=output_keys,
    )


# ---------------------------------------------------------------------------
# 5. Embedding Indexer
# ---------------------------------------------------------------------------


def embedding_indexer(
    texts: list[str],
    model_id: str,
    table_name: str,
    region_name: str | None = None,
) -> EmbeddingIndexResult:
    """Generate embeddings via Bedrock Titan and store in DynamoDB.

    Invokes the Bedrock Titan embedding model for each text item and
    stores the resulting vectors with metadata in DynamoDB.

    Args:
        texts: List of text strings to embed.
        model_id: Bedrock embedding model identifier (e.g.
            ``"amazon.titan-embed-text-v1"``).
        table_name: DynamoDB table for vector storage.
        region_name: AWS region override.

    Returns:
        An :class:`EmbeddingIndexResult` with counts and dimensions.

    Raises:
        RuntimeError: If Bedrock invocation or DynamoDB write fails.
    """
    bedrock = get_client("bedrock-runtime", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    items_indexed = 0
    dimensions = 0

    for idx, text in enumerate(texts):
        body = json.dumps({"inputText": text})

        try:
            resp = bedrock.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Bedrock embedding failed for item {idx}") from exc

        resp_body = json.loads(resp["body"].read())
        embedding = resp_body.get("embedding", [])

        if embedding:
            dimensions = len(embedding)

        # Store in DynamoDB
        ts = int(time.time())
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": f"embedding#{ts}#{idx}"},
                    "text": {"S": text},
                    "embedding": {
                        "S": json.dumps(embedding),
                    },
                    "model_id": {"S": model_id},
                    "dimensions": {
                        "N": str(len(embedding)),
                    },
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to store embedding for item {idx}") from exc

        items_indexed += 1

    return EmbeddingIndexResult(
        items_indexed=items_indexed,
        model_id=model_id,
        dimensions=dimensions,
    )


# ---------------------------------------------------------------------------
# New Models (6-16)
# ---------------------------------------------------------------------------


class FaceIndexResult(BaseModel):
    """Result of Rekognition face indexing pipeline."""

    model_config = ConfigDict(frozen=True)

    faces_indexed: int
    face_records: list[dict[str, Any]]


class VideoLabelResult(BaseModel):
    """Result of Rekognition video label detection pipeline."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    status: str
    labels_count: int
    labels: list[dict[str, Any]]


class PollyAudioResult(BaseModel):
    """Result of Polly audio synthesis pipeline."""

    model_config = ConfigDict(frozen=True)

    s3_key: str
    presigned_url: str
    content_type: str


class TranscribeJobResult(BaseModel):
    """Result of Transcribe job pipeline."""

    model_config = ConfigDict(frozen=True)

    job_name: str
    status: str
    transcript_key: str
    transcript_text: str


class PIIRedactorResult(BaseModel):
    """Result of Comprehend PII redaction pipeline."""

    model_config = ConfigDict(frozen=True)

    pii_entities_found: int
    entity_types: list[str]
    redacted_key: str


class FormExtractResult(BaseModel):
    """Result of Textract form extraction pipeline."""

    model_config = ConfigDict(frozen=True)

    page_count: int
    key_value_pairs: list[dict[str, Any]]
    items_stored: int


class KBIngestResult(BaseModel):
    """Result of Bedrock knowledge base ingestion pipeline."""

    model_config = ConfigDict(frozen=True)

    ingestion_job_id: str
    status: str
    documents_uploaded: int


class GuardrailResult(BaseModel):
    """Result of Bedrock guardrail enforcement."""

    model_config = ConfigDict(frozen=True)

    action: str
    violations: list[dict[str, Any]]
    logged: bool


class RecommenderResult(BaseModel):
    """Result of Personalize real-time recommendation pipeline."""

    model_config = ConfigDict(frozen=True)

    event_recorded: bool
    recommendations: list[dict[str, Any]]


class ForecastExportResult(BaseModel):
    """Result of Forecast inference export pipeline."""

    model_config = ConfigDict(frozen=True)

    export_job_arn: str
    status: str
    predictions_loaded: int


class BatchTransformResult(BaseModel):
    """Result of SageMaker batch transform monitor pipeline."""

    model_config = ConfigDict(frozen=True)

    job_name: str
    status: str
    output_s3_uri: str
    message_id: str | None = None


# ---------------------------------------------------------------------------
# 6. Rekognition Face Indexer
# ---------------------------------------------------------------------------


def rekognition_face_indexer(
    collection_id: str,
    bucket: str,
    keys: list[str],
    table_name: str,
    user_ids: list[str],
    region_name: str | None = None,
) -> FaceIndexResult:
    """Index faces from S3 images into a Rekognition collection.

    For each image key, calls Rekognition ``index_faces`` and stores the
    returned face IDs mapped to the corresponding user ID in DynamoDB.
    The Rekognition collection is created if it does not already exist.

    Args:
        collection_id: Rekognition collection identifier.
        bucket: S3 bucket containing the images.
        keys: List of S3 object keys (one image per key).
        table_name: DynamoDB table for face-ID to user-ID mapping.
        user_ids: User identifiers parallel to *keys*.
        region_name: AWS region override.

    Returns:
        A :class:`FaceIndexResult` with total faces indexed and raw records.

    Raises:
        RuntimeError: If any Rekognition, S3, or DynamoDB call fails.
    """
    rek = get_client("rekognition", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Create collection if it does not exist
    try:
        rek.create_collection(CollectionId=collection_id)
        logger.info("Created Rekognition collection %s", collection_id)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
            raise wrap_aws_error(exc, f"Failed to create collection {collection_id}") from exc

    all_face_records: list[dict[str, Any]] = []
    total_indexed = 0

    for key, user_id in zip(keys, user_ids, strict=False):
        try:
            resp = rek.index_faces(
                CollectionId=collection_id,
                Image={"S3Object": {"Bucket": bucket, "Name": key}},
                ExternalImageId=user_id,
                DetectionAttributes=["DEFAULT"],
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Rekognition index_faces failed for {key}") from exc

        face_records = resp.get("FaceRecords", [])
        all_face_records.extend(face_records)

        # Store face-ID -> user-ID mapping in DynamoDB
        for record in face_records:
            face_id = record.get("Face", {}).get("FaceId", "")
            if not face_id:
                continue
            try:
                ddb.put_item(
                    TableName=table_name,
                    Item={
                        "pk": {"S": f"face#{face_id}"},
                        "user_id": {"S": user_id},
                        "collection_id": {"S": collection_id},
                        "s3_key": {"S": key},
                        "timestamp": {"N": str(int(time.time()))},
                    },
                )
            except ClientError as exc:
                raise wrap_aws_error(exc, f"Failed to store face mapping for {face_id}") from exc

        total_indexed += len(face_records)

    return FaceIndexResult(
        faces_indexed=total_indexed,
        face_records=all_face_records,
    )


# ---------------------------------------------------------------------------
# 7. Rekognition Video Label Pipeline
# ---------------------------------------------------------------------------


def rekognition_video_label_pipeline(
    bucket: str,
    video_key: str,
    table_name: str,
    sns_topic_arn: str,
    role_arn: str,
    min_confidence: float = 70.0,
    region_name: str | None = None,
) -> VideoLabelResult:
    """Start Rekognition video label detection, poll, and store results.

    Starts an asynchronous Rekognition label detection job on an S3
    video object, polls ``get_label_detection`` until the job reaches
    ``SUCCEEDED`` or ``FAILED``, then writes all labels to DynamoDB.

    Args:
        bucket: S3 bucket containing the video.
        video_key: S3 object key of the video file.
        table_name: DynamoDB table for label storage.
        sns_topic_arn: SNS topic ARN for Rekognition job notifications.
        role_arn: IAM role ARN that Rekognition assumes to publish to SNS.
        min_confidence: Minimum label confidence to return (default 70.0).
        region_name: AWS region override.

    Returns:
        A :class:`VideoLabelResult` with job metadata and labels.

    Raises:
        RuntimeError: If Rekognition or DynamoDB calls fail, or the job fails.
    """
    rek = get_client("rekognition", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Start label detection
    try:
        start_resp = rek.start_label_detection(
            Video={"S3Object": {"Bucket": bucket, "Name": video_key}},
            MinConfidence=min_confidence,
            NotificationChannel={
                "SNSTopicArn": sns_topic_arn,
                "RoleArn": role_arn,
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start label detection for {video_key}") from exc

    job_id = start_resp["JobId"]
    logger.info("Started Rekognition label detection job %s", job_id)

    # Poll until terminal state
    status = "IN_PROGRESS"
    labels: list[dict[str, Any]] = []
    while status == "IN_PROGRESS":
        time.sleep(5)
        try:
            poll_resp = rek.get_label_detection(JobId=job_id, SortBy="TIMESTAMP")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll label detection job {job_id}") from exc

        status = poll_resp.get("JobStatus", "IN_PROGRESS")
        labels = poll_resp.get("Labels", [])

    if status == "FAILED":
        status_message = poll_resp.get("StatusMessage", "unknown error")
        raise RuntimeError(f"Rekognition video label job {job_id} failed: {status_message}")

    # Store labels in DynamoDB
    ts = int(time.time())
    for idx, label_item in enumerate(labels):
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": f"video-label#{job_id}"},
                    "sk": {"S": f"{idx:06d}"},
                    "job_id": {"S": job_id},
                    "video_key": {"S": video_key},
                    "label": {"S": json.dumps(label_item, default=str)},
                    "timestamp": {"N": str(ts)},
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to store label {idx} for job {job_id}") from exc

    return VideoLabelResult(
        job_id=job_id,
        status=status,
        labels_count=len(labels),
        labels=labels,
    )


# ---------------------------------------------------------------------------
# 8. Polly Audio Generator
# ---------------------------------------------------------------------------


def polly_audio_generator(
    text: str,
    bucket: str,
    voice_id: str = "Joanna",
    output_format: str = "mp3",
    key_prefix: str = "polly-audio/",
    presign_expiry: int = 3600,
    region_name: str | None = None,
) -> PollyAudioResult:
    """Synthesize text with Polly, upload to S3, and return a pre-signed URL.

    Calls Polly ``synthesize_speech``, writes the audio stream to S3
    under *key_prefix*, then generates a pre-signed URL for the object.

    Args:
        text: The text to synthesize.
        bucket: S3 bucket for audio storage.
        voice_id: Polly voice identifier (default ``"Joanna"``).
        output_format: Audio format (default ``"mp3"``).
        key_prefix: S3 key prefix for the output audio file.
        presign_expiry: Pre-signed URL expiry in seconds (default 3600).
        region_name: AWS region override.

    Returns:
        A :class:`PollyAudioResult` with S3 key, pre-signed URL, and
        content type.

    Raises:
        RuntimeError: If Polly or S3 calls fail.
    """
    polly = get_client("polly", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    content_type_map = {"mp3": "audio/mpeg", "ogg_vorbis": "audio/ogg", "pcm": "audio/pcm"}
    content_type = content_type_map.get(output_format, "audio/mpeg")

    # Synthesize speech
    try:
        polly_resp = polly.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            OutputFormat=output_format,
            Engine="standard",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Polly synthesize_speech failed") from exc

    audio_stream = polly_resp["AudioStream"].read()

    # Upload to S3
    ts = int(time.time())
    s3_key = f"{key_prefix}{voice_id}_{ts}.{output_format}"
    try:
        s3.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=audio_stream,
            ContentType=content_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to upload audio to s3://{bucket}/{s3_key}") from exc

    # Generate pre-signed URL
    try:
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": s3_key},
            ExpiresIn=presign_expiry,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to generate pre-signed URL for {s3_key}") from exc

    return PollyAudioResult(
        s3_key=s3_key,
        presigned_url=presigned_url,
        content_type=content_type,
    )


# ---------------------------------------------------------------------------
# 9. Transcribe Job to S3
# ---------------------------------------------------------------------------


def transcribe_job_to_s3(
    job_name: str,
    bucket: str,
    audio_key: str,
    output_bucket: str,
    output_prefix: str,
    language_code: str = "en-US",
    region_name: str | None = None,
) -> TranscribeJobResult:
    """Start a Transcribe job, poll to completion, and copy transcript to S3.

    Starts an AWS Transcribe job for the given S3 audio object, polls
    ``get_transcription_job`` until the job reaches ``COMPLETED`` or
    ``FAILED``, reads the transcript JSON from the Transcribe-provided
    URI, then copies the transcript text to *output_bucket* under
    *output_prefix*.

    Args:
        job_name: Unique name for the Transcribe job.
        bucket: S3 bucket containing the audio file.
        audio_key: S3 object key of the audio file.
        output_bucket: S3 bucket for the copied transcript.
        output_prefix: S3 key prefix for the transcript output.
        language_code: BCP-47 language code (default ``"en-US"``).
        region_name: AWS region override.

    Returns:
        A :class:`TranscribeJobResult` with job metadata and transcript.

    Raises:
        RuntimeError: If Transcribe or S3 calls fail, or the job fails.
    """
    import urllib.request

    transcribe = get_client("transcribe", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    media_uri = f"s3://{bucket}/{audio_key}"

    # Start transcription job
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            LanguageCode=language_code,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start transcription job {job_name}") from exc

    logger.info("Started Transcribe job %s", job_name)

    # Poll until terminal state
    status = "IN_PROGRESS"
    job_detail: dict[str, Any] = {}
    while status in ("IN_PROGRESS", "QUEUED"):
        time.sleep(10)
        try:
            poll_resp = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll transcription job {job_name}") from exc

        job_detail = poll_resp.get("TranscriptionJob", {})
        status = job_detail.get("TranscriptionJobStatus", "IN_PROGRESS")

    if status == "FAILED":
        reason = job_detail.get("FailureReason", "unknown")
        raise RuntimeError(f"Transcribe job {job_name} failed: {reason}")

    # Read transcript from TranscriptFileUri
    transcript_uri = job_detail.get("Transcript", {}).get("TranscriptFileUri", "")
    try:
        with urllib.request.urlopen(transcript_uri) as response:
            transcript_json = json.loads(response.read())
    except Exception as exc:
        raise RuntimeError(f"Failed to read transcript from {transcript_uri}: {exc}") from exc

    transcript_text = (
        transcript_json.get("results", {}).get("transcripts", [{}])[0].get("transcript", "")
    )

    # Copy transcript to output S3 location
    transcript_key = f"{output_prefix}{job_name}/transcript.json"
    try:
        s3.put_object(
            Bucket=output_bucket,
            Key=transcript_key,
            Body=json.dumps(transcript_json).encode("utf-8"),
            ContentType="application/json",
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to write transcript to s3://{output_bucket}/{transcript_key}"
        ) from exc

    return TranscribeJobResult(
        job_name=job_name,
        status=status,
        transcript_key=transcript_key,
        transcript_text=transcript_text,
    )


# ---------------------------------------------------------------------------
# 10. Comprehend PII Redactor
# ---------------------------------------------------------------------------


def comprehend_pii_redactor(
    text: str,
    bucket: str,
    output_key: str,
    replacement: str = "[REDACTED]",
    language_code: str = "en",
    region_name: str | None = None,
) -> PIIRedactorResult:
    """Detect PII in text with Comprehend, redact, and store in S3.

    Calls Comprehend ``detect_pii_entities`` on the input text, replaces
    each detected entity span with *replacement*, then uploads the
    sanitized text to S3 at *output_key*.

    Args:
        text: Input text to redact.
        bucket: S3 bucket for redacted output.
        output_key: S3 object key for the sanitized text.
        replacement: String to substitute for each PII span (default
            ``"[REDACTED]"``).
        language_code: Language code for Comprehend (default ``"en"``).
        region_name: AWS region override.

    Returns:
        A :class:`PIIRedactorResult` with entity count, types, and S3 key.

    Raises:
        RuntimeError: If Comprehend or S3 calls fail.
    """
    comprehend = get_client("comprehend", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    # Detect PII entities
    try:
        pii_resp = comprehend.detect_pii_entities(
            Text=text,
            LanguageCode=language_code,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Comprehend detect_pii_entities failed") from exc

    entities = pii_resp.get("Entities", [])

    # Redact entities by replacing spans in reverse order to preserve offsets
    redacted = text
    sorted_entities = sorted(entities, key=lambda e: e.get("BeginOffset", 0), reverse=True)
    for entity in sorted_entities:
        begin = entity.get("BeginOffset", 0)
        end = entity.get("EndOffset", 0)
        redacted = redacted[:begin] + replacement + redacted[end:]

    entity_types = list({e.get("Type", "") for e in entities})

    # Store redacted text in S3
    try:
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=redacted.encode("utf-8"),
            ContentType="text/plain",
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to write redacted text to s3://{bucket}/{output_key}"
        ) from exc

    return PIIRedactorResult(
        pii_entities_found=len(entities),
        entity_types=entity_types,
        redacted_key=output_key,
    )


# ---------------------------------------------------------------------------
# 11. Textract Form Extractor
# ---------------------------------------------------------------------------


def textract_form_extractor(
    bucket: str,
    key: str,
    table_name: str,
    region_name: str | None = None,
) -> FormExtractResult:
    """Run Textract AnalyzeDocument on an S3 PDF and extract form pairs.

    Calls Textract ``analyze_document`` with ``FeatureTypes=["FORMS"]``,
    parses KEY_VALUE_SET blocks to build key-value pairs, and stores
    each pair as an item in DynamoDB.

    Args:
        bucket: S3 bucket containing the PDF.
        key: S3 object key of the PDF document.
        table_name: DynamoDB table for key-value pair storage.
        region_name: AWS region override.

    Returns:
        A :class:`FormExtractResult` with page count, pairs, and items stored.

    Raises:
        RuntimeError: If Textract or DynamoDB calls fail.
    """
    textract = get_client("textract", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Analyze document
    try:
        resp = textract.analyze_document(
            Document={"S3Object": {"Bucket": bucket, "Name": key}},
            FeatureTypes=["FORMS"],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Textract analyze_document failed for {key}") from exc

    blocks = resp.get("Blocks", [])
    page_count = max((b.get("Page", 1) for b in blocks), default=1)

    # Index blocks by ID
    block_map: dict[str, dict[str, Any]] = {b["Id"]: b for b in blocks}

    def get_text_for_block(block: dict[str, Any]) -> str:
        """Recursively collect WORD text for a KEY or VALUE block."""
        text_parts: list[str] = []
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "CHILD":
                for child_id in rel.get("Ids", []):
                    child = block_map.get(child_id, {})
                    if child.get("BlockType") == "WORD":
                        text_parts.append(child.get("Text", ""))
        return " ".join(text_parts)

    key_value_pairs: list[dict[str, Any]] = []
    for block in blocks:
        if block.get("BlockType") != "KEY_VALUE_SET":
            continue
        if "KEY" not in block.get("EntityTypes", []):
            continue

        key_text = get_text_for_block(block)
        value_text = ""
        for rel in block.get("Relationships", []):
            if rel.get("Type") == "VALUE":
                for val_id in rel.get("Ids", []):
                    val_block = block_map.get(val_id, {})
                    value_text = get_text_for_block(val_block)

        key_value_pairs.append({"key": key_text, "value": value_text})

    # Store pairs in DynamoDB
    items_stored = 0
    ts = int(time.time())
    for idx, pair in enumerate(key_value_pairs):
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": f"form#{bucket}/{key}"},
                    "sk": {"S": f"{idx:06d}"},
                    "form_key": {"S": pair["key"]},
                    "form_value": {"S": pair["value"]},
                    "s3_key": {"S": key},
                    "timestamp": {"N": str(ts)},
                },
            )
            items_stored += 1
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to store form pair {idx} for {key}") from exc

    return FormExtractResult(
        page_count=page_count,
        key_value_pairs=key_value_pairs,
        items_stored=items_stored,
    )


# ---------------------------------------------------------------------------
# 12. Bedrock Knowledge Base Ingestor
# ---------------------------------------------------------------------------


def bedrock_knowledge_base_ingestor(
    knowledge_base_id: str,
    data_source_id: str,
    bucket: str,
    document_keys: list[str],
    region_name: str | None = None,
) -> KBIngestResult:
    """Upload documents to S3 and trigger a Bedrock knowledge base ingestion.

    Verifies that all S3 objects exist, starts a Bedrock Agent ingestion
    job for the given knowledge base and data source, and polls
    ``get_ingestion_job`` until the job reaches ``COMPLETE`` or ``FAILED``.

    Args:
        knowledge_base_id: Bedrock knowledge base identifier.
        data_source_id: Bedrock data source identifier within the KB.
        bucket: S3 bucket containing the documents.
        document_keys: List of S3 object keys to ingest.
        region_name: AWS region override.

    Returns:
        A :class:`KBIngestResult` with job ID, status, and document count.

    Raises:
        RuntimeError: If S3 verification or Bedrock Agent calls fail.
    """
    s3 = get_client("s3", region_name=region_name)
    bedrock_agent = get_client("bedrock-agent", region_name=region_name)

    # Verify all S3 objects exist
    for doc_key in document_keys:
        try:
            s3.head_object(Bucket=bucket, Key=doc_key)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"S3 object s3://{bucket}/{doc_key} not found") from exc

    # Start ingestion job
    try:
        start_resp = bedrock_agent.start_ingestion_job(
            knowledgeBaseId=knowledge_base_id,
            dataSourceId=data_source_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start Bedrock ingestion job") from exc

    ingestion_job = start_resp.get("ingestionJob", {})
    job_id = ingestion_job.get("ingestionJobId", "")
    logger.info("Started Bedrock ingestion job %s", job_id)

    # Poll until terminal state
    status = "STARTING"
    while status in ("STARTING", "IN_PROGRESS"):
        time.sleep(10)
        try:
            poll_resp = bedrock_agent.get_ingestion_job(
                knowledgeBaseId=knowledge_base_id,
                dataSourceId=data_source_id,
                ingestionJobId=job_id,
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll ingestion job {job_id}") from exc

        status = poll_resp.get("ingestionJob", {}).get("status", "IN_PROGRESS")

    if status == "FAILED":
        raise RuntimeError(f"Bedrock ingestion job {job_id} failed")

    return KBIngestResult(
        ingestion_job_id=job_id,
        status=status,
        documents_uploaded=len(document_keys),
    )


# ---------------------------------------------------------------------------
# 13. Bedrock Guardrail Enforcer
# ---------------------------------------------------------------------------


def bedrock_guardrail_enforcer(
    guardrail_id: str,
    guardrail_version: str,
    text: str,
    source: str,
    log_group_name: str,
    region_name: str | None = None,
) -> GuardrailResult:
    """Apply a Bedrock Guardrail to text and log violations to CloudWatch.

    Calls Bedrock Runtime ``apply_guardrail`` for the given text and
    source (``"INPUT"`` or ``"OUTPUT"``).  If any violations are found,
    puts a log event to the specified CloudWatch Logs log group.

    Args:
        guardrail_id: Bedrock Guardrail identifier.
        guardrail_version: Guardrail version string.
        text: Text to evaluate against the guardrail.
        source: Either ``"INPUT"`` or ``"OUTPUT"``.
        log_group_name: CloudWatch Logs log group for violation events.
        region_name: AWS region override.

    Returns:
        A :class:`GuardrailResult` with action, violations, and log status.

    Raises:
        RuntimeError: If Bedrock Runtime or CloudWatch Logs calls fail.
    """
    bedrock_runtime = get_client("bedrock-runtime", region_name=region_name)
    logs = get_client("logs", region_name=region_name)

    # Apply guardrail
    try:
        guardrail_resp = bedrock_runtime.apply_guardrail(
            guardrailIdentifier=guardrail_id,
            guardrailVersion=guardrail_version,
            source=source,
            content=[{"text": {"text": text}}],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to apply guardrail {guardrail_id}") from exc

    action = guardrail_resp.get("action", "ALLOWED")
    guardrail_resp.get("outputs", [])
    assessments = guardrail_resp.get("assessments", [])

    violations: list[dict[str, Any]] = []
    for assessment in assessments:
        for policy_type, policy_data in assessment.items():
            if isinstance(policy_data, dict) and policy_data.get("topics"):
                for topic in policy_data["topics"]:
                    if topic.get("action") == "BLOCKED":
                        violations.append({"policy": policy_type, "detail": topic})

    # Log violations to CloudWatch if present
    logged = False
    if violations:
        log_stream_name = f"guardrail-violations/{guardrail_id}"
        ts_ms = int(time.time() * 1000)

        # Ensure log stream exists
        try:
            logs.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise wrap_aws_error(exc, "Failed to create CloudWatch log stream") from exc

        try:
            logs.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[
                    {
                        "timestamp": ts_ms,
                        "message": json.dumps(
                            {
                                "guardrail_id": guardrail_id,
                                "action": action,
                                "source": source,
                                "violations": violations,
                            },
                            default=str,
                        ),
                    }
                ],
            )
            logged = True
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to put CloudWatch log events") from exc

    return GuardrailResult(
        action=action,
        violations=violations,
        logged=logged,
    )


# ---------------------------------------------------------------------------
# 14. Personalize Real-Time Recommender
# ---------------------------------------------------------------------------


def personalize_real_time_recommender(
    tracking_id: str,
    campaign_arn: str,
    user_id: str,
    item_id: str,
    event_type: str,
    session_id: str,
    num_results: int = 10,
    region_name: str | None = None,
) -> RecommenderResult:
    """Record a user event and retrieve real-time recommendations.

    Records the interaction event to the Personalize event tracker via
    ``put_events``, then calls ``get_recommendations`` on the given
    campaign to return personalised item recommendations.

    Args:
        tracking_id: Personalize event tracker ID.
        campaign_arn: ARN of the Personalize campaign.
        user_id: User identifier.
        item_id: Item interacted with.
        event_type: Type of event (e.g. ``"click"``, ``"purchase"``).
        session_id: Session identifier for the event.
        num_results: Number of recommendations to return (default 10).
        region_name: AWS region override.

    Returns:
        A :class:`RecommenderResult` with event status and recommendations.

    Raises:
        RuntimeError: If Personalize service calls fail.
    """
    personalize_events = get_client("personalize-events", region_name=region_name)
    personalize_runtime = get_client("personalize-runtime", region_name=region_name)

    # Record event
    event_recorded = False
    try:
        personalize_events.put_events(
            trackingId=tracking_id,
            userId=user_id,
            sessionId=session_id,
            eventList=[
                {
                    "eventType": event_type,
                    "itemId": item_id,
                    "sentAt": time.time(),
                }
            ],
        )
        event_recorded = True
        logger.info("Recorded Personalize event for user %s item %s", user_id, item_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to record Personalize event for user {user_id}") from exc

    # Get recommendations
    try:
        rec_resp = personalize_runtime.get_recommendations(
            campaignArn=campaign_arn,
            userId=user_id,
            numResults=num_results,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to get recommendations for user {user_id}") from exc

    recommendations = rec_resp.get("itemList", [])

    return RecommenderResult(
        event_recorded=event_recorded,
        recommendations=recommendations,
    )


# ---------------------------------------------------------------------------
# 15. Forecast Inference Pipeline
# ---------------------------------------------------------------------------


def forecast_inference_pipeline(
    forecast_arn: str,
    s3_path: str,
    iam_role_arn: str,
    table_name: str,
    region_name: str | None = None,
) -> ForecastExportResult:
    """Export a Forecast dataset, poll for completion, load into DynamoDB.

    Creates a Forecast export job targeting the given S3 path, polls
    ``describe_forecast_export_job`` until the job reaches ``ACTIVE`` or
    ``CREATE_FAILED``, reads the resulting CSV(s) from S3, and writes
    each prediction row into DynamoDB.

    Args:
        forecast_arn: ARN of the Forecast to export.
        s3_path: S3 destination path (``"s3://bucket/prefix/"``).
        iam_role_arn: IAM role ARN for Forecast to write to S3.
        table_name: DynamoDB table for predictions.
        region_name: AWS region override.

    Returns:
        A :class:`ForecastExportResult` with job ARN, status, and count.

    Raises:
        RuntimeError: If Forecast, S3, or DynamoDB calls fail.
    """
    import csv
    import io

    forecast = get_client("forecast", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Parse S3 path
    s3_path_stripped = s3_path.rstrip("/")
    if s3_path_stripped.startswith("s3://"):
        s3_path_stripped = s3_path_stripped[5:]
    parts = s3_path_stripped.split("/", 1)
    export_bucket = parts[0]
    export_prefix = parts[1] if len(parts) > 1 else ""

    # Create export job
    job_name = f"forecast-export-{int(time.time())}"
    try:
        export_resp = forecast.create_forecast_export_job(
            ForecastExportJobName=job_name,
            ForecastArn=forecast_arn,
            Destination={
                "S3Config": {
                    "Path": s3_path,
                    "RoleArn": iam_role_arn,
                }
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create Forecast export job") from exc

    export_job_arn = export_resp.get("ForecastExportJobArn", "")
    logger.info("Started Forecast export job %s", export_job_arn)

    # Poll until terminal
    status = "CREATE_PENDING"
    while status in ("CREATE_PENDING", "CREATE_IN_PROGRESS"):
        time.sleep(15)
        try:
            desc_resp = forecast.describe_forecast_export_job(ForecastExportJobArn=export_job_arn)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll export job {export_job_arn}") from exc

        status = desc_resp.get("Status", "CREATE_IN_PROGRESS")

    if status == "CREATE_FAILED":
        raise RuntimeError(f"Forecast export job {export_job_arn} failed")

    # List and read CSV files from S3
    predictions_loaded = 0
    ts = int(time.time())
    try:
        list_resp = s3.list_objects_v2(Bucket=export_bucket, Prefix=export_prefix)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to list export objects in {s3_path}") from exc

    for obj in list_resp.get("Contents", []):
        obj_key = obj["Key"]
        if not obj_key.endswith(".csv"):
            continue

        try:
            csv_resp = s3.get_object(Bucket=export_bucket, Key=obj_key)
            csv_content = csv_resp["Body"].read().decode("utf-8")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to read CSV {obj_key}") from exc

        reader = csv.DictReader(io.StringIO(csv_content))
        for row_idx, row in enumerate(reader):
            try:
                ddb.put_item(
                    TableName=table_name,
                    Item={
                        "pk": {"S": f"forecast#{export_job_arn}"},
                        "sk": {"S": f"{obj_key}#{row_idx:08d}"},
                        "data": {"S": json.dumps(row)},
                        "timestamp": {"N": str(ts)},
                    },
                )
                predictions_loaded += 1
            except ClientError as exc:
                raise wrap_aws_error(
                    exc, f"Failed to store prediction row {row_idx} from {obj_key}"
                ) from exc

    return ForecastExportResult(
        export_job_arn=export_job_arn,
        status=status,
        predictions_loaded=predictions_loaded,
    )


# ---------------------------------------------------------------------------
# 16. SageMaker Batch Transform Monitor
# ---------------------------------------------------------------------------


def sagemaker_batch_transform_monitor(
    job_name: str,
    model_name: str,
    input_s3_uri: str,
    output_s3_uri: str,
    instance_type: str,
    instance_count: int,
    queue_url: str,
    content_type: str = "text/csv",
    region_name: str | None = None,
) -> BatchTransformResult:
    """Start a SageMaker batch transform job, poll, and notify via SQS.

    Creates a SageMaker transform job with the given model and data
    locations, polls ``describe_transform_job`` until the job reaches
    ``Completed`` or ``Failed``, then sends the output S3 URI to the
    specified SQS queue.

    Args:
        job_name: Unique name for the transform job.
        model_name: Name of the SageMaker model to use.
        input_s3_uri: S3 URI for transform input data.
        output_s3_uri: S3 URI for transform output.
        instance_type: ML instance type (e.g. ``"ml.m5.xlarge"``).
        instance_count: Number of instances for the transform job.
        queue_url: SQS queue URL to send the completion message.
        content_type: MIME type of the input data (default ``"text/csv"``).
        region_name: AWS region override.

    Returns:
        A :class:`BatchTransformResult` with job status and SQS message ID.

    Raises:
        RuntimeError: If SageMaker or SQS calls fail.
    """
    sm = get_client("sagemaker", region_name=region_name)
    sqs = get_client("sqs", region_name=region_name)

    # Create transform job
    try:
        sm.create_transform_job(
            TransformJobName=job_name,
            ModelName=model_name,
            TransformInput={
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": input_s3_uri,
                    }
                },
                "ContentType": content_type,
                "SplitType": "Line",
            },
            TransformOutput={
                "S3OutputPath": output_s3_uri,
            },
            TransformResources={
                "InstanceType": instance_type,
                "InstanceCount": instance_count,
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create SageMaker transform job {job_name}") from exc

    logger.info("Started SageMaker batch transform job %s", job_name)

    # Poll until terminal state
    status = "InProgress"
    while status in ("InProgress", "Stopping"):
        time.sleep(15)
        try:
            desc_resp = sm.describe_transform_job(TransformJobName=job_name)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to poll transform job {job_name}") from exc

        status = desc_resp.get("TransformJobStatus", "InProgress")

    # Send SQS notification
    message_id: str | None = None
    try:
        sqs_resp = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(
                {
                    "job_name": job_name,
                    "status": status,
                    "output_s3_uri": output_s3_uri,
                },
                default=str,
            ),
        )
        message_id = sqs_resp.get("MessageId")
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to send SQS message for job {job_name}") from exc

    return BatchTransformResult(
        job_name=job_name,
        status=status,
        output_s3_uri=output_s3_uri,
        message_id=message_id,
    )
