"""Integration tests for aws_util.ai_ml_pipelines against LocalStack."""
from __future__ import annotations

import json
import time

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. bedrock_serverless_chain
# ---------------------------------------------------------------------------


class TestBedrockServerlessChain:
    @pytest.mark.skip(reason="Bedrock not available in LocalStack community")
    def test_chain_stores_conversation(self, dynamodb_table):
        from aws_util.ai_ml_pipelines import bedrock_serverless_chain

        result = bedrock_serverless_chain(
            prompts=["Hello", "Follow up"],
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            conversation_id="conv-001",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert result.conversation_id == "conv-001"
        assert result.steps_completed == 2
        assert len(result.outputs) == 2


# ---------------------------------------------------------------------------
# 2. s3_document_processor
# ---------------------------------------------------------------------------


class TestS3DocumentProcessor:
    @pytest.mark.skip(reason="Textract and Comprehend not available in LocalStack community")
    def test_processes_document(self, s3_bucket, dynamodb_table):
        from aws_util.ai_ml_pipelines import s3_document_processor

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="doc.txt", Body=b"Hello world")

        result = s3_document_processor(
            bucket=s3_bucket,
            key="doc.txt",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert result.bucket == s3_bucket
        assert result.key == "doc.txt"
        assert isinstance(result.extracted_text, str)
        assert isinstance(result.sentiment, str)


# ---------------------------------------------------------------------------
# 3. image_moderation_pipeline
# ---------------------------------------------------------------------------


class TestImageModerationPipeline:
    @pytest.mark.skip(reason="Rekognition not available in LocalStack community")
    def test_moderates_image(self, s3_bucket, dynamodb_table, sns_topic):
        from aws_util.ai_ml_pipelines import image_moderation_pipeline

        s3 = ls_client("s3")
        # Create a minimal 1x1 PNG
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00"
            b"\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00"
            b"\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        s3.put_object(Bucket=s3_bucket, Key="test.png", Body=png_bytes)

        result = image_moderation_pipeline(
            bucket=s3_bucket,
            key="test.png",
            table_name=dynamodb_table,
            sns_topic_arn=sns_topic,
            confidence_threshold=75.0,
            region_name=REGION,
        )
        assert result.bucket == s3_bucket
        assert result.key == "test.png"
        assert isinstance(result.flagged, bool)


# ---------------------------------------------------------------------------
# 4. translation_pipeline
# ---------------------------------------------------------------------------


class TestTranslationPipeline:
    @pytest.mark.skip(reason="Translate not available in LocalStack community")
    def test_translates_documents(self, s3_bucket, dynamodb_table):
        from aws_util.ai_ml_pipelines import translation_pipeline

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="hello.txt", Body=b"Hello world")

        result = translation_pipeline(
            bucket=s3_bucket,
            source_keys=["hello.txt"],
            target_language="es",
            table_name=dynamodb_table,
            output_prefix="translated/",
            source_language="en",
            region_name=REGION,
        )
        assert result.translated_count == 1
        assert result.source_language == "en"
        assert result.target_language == "es"
        assert len(result.output_keys) == 1


# ---------------------------------------------------------------------------
# 5. embedding_indexer
# ---------------------------------------------------------------------------


class TestEmbeddingIndexer:
    @pytest.mark.skip(reason="Bedrock not available in LocalStack community")
    def test_indexes_embeddings(self, dynamodb_table):
        from aws_util.ai_ml_pipelines import embedding_indexer

        result = embedding_indexer(
            texts=["sample text one", "sample text two"],
            model_id="amazon.titan-embed-text-v1",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert result.items_indexed == 2
        assert result.model_id == "amazon.titan-embed-text-v1"
        assert result.dimensions > 0


# ---------------------------------------------------------------------------
# 6. rekognition_face_indexer
# ---------------------------------------------------------------------------


class TestRekognitionFaceIndexer:
    @pytest.mark.skip(reason="Rekognition not available in LocalStack community")
    def test_indexes_faces(self, s3_bucket, dynamodb_table):
        from aws_util.ai_ml_pipelines import rekognition_face_indexer

        s3 = ls_client("s3")
        png_bytes = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00"
            b"\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00"
            b"\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        s3.put_object(Bucket=s3_bucket, Key="face.png", Body=png_bytes)

        result = rekognition_face_indexer(
            collection_id="test-collection",
            bucket=s3_bucket,
            keys=["face.png"],
            table_name=dynamodb_table,
            user_ids=["user-001"],
            region_name=REGION,
        )
        assert result.faces_indexed >= 0
        assert isinstance(result.face_records, list)


# ---------------------------------------------------------------------------
# 7. rekognition_video_label_pipeline
# ---------------------------------------------------------------------------


class TestRekognitionVideoLabelPipeline:
    @pytest.mark.skip(reason="Rekognition not available in LocalStack community")
    def test_detects_video_labels(self, s3_bucket, dynamodb_table, sns_topic, iam_role):
        from aws_util.ai_ml_pipelines import rekognition_video_label_pipeline

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="video.mp4", Body=b"\x00" * 1024)

        result = rekognition_video_label_pipeline(
            bucket=s3_bucket,
            video_key="video.mp4",
            table_name=dynamodb_table,
            sns_topic_arn=sns_topic,
            role_arn=iam_role,
            min_confidence=70.0,
            region_name=REGION,
        )
        assert isinstance(result.job_id, str)
        assert result.status in ("SUCCEEDED", "FAILED")
        assert isinstance(result.labels, list)


# ---------------------------------------------------------------------------
# 8. polly_audio_generator
# ---------------------------------------------------------------------------


class TestPollyAudioGenerator:
    @pytest.mark.skip(reason="Polly not available in LocalStack community")
    def test_synthesizes_audio(self, s3_bucket):
        from aws_util.ai_ml_pipelines import polly_audio_generator

        result = polly_audio_generator(
            text="Hello world",
            bucket=s3_bucket,
            voice_id="Joanna",
            output_format="mp3",
            key_prefix="polly-audio/",
            presign_expiry=3600,
            region_name=REGION,
        )
        assert result.s3_key.startswith("polly-audio/")
        assert result.content_type == "audio/mpeg"
        assert "http" in result.presigned_url


# ---------------------------------------------------------------------------
# 9. transcribe_job_to_s3
# ---------------------------------------------------------------------------


class TestTranscribeJobToS3:
    @pytest.mark.skip(reason="Transcribe not available in LocalStack community")
    def test_transcribes_audio(self, s3_bucket):
        from aws_util.ai_ml_pipelines import transcribe_job_to_s3

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="audio.wav", Body=b"\x00" * 1024)

        job_name = f"test-job-{int(time.time())}"
        result = transcribe_job_to_s3(
            job_name=job_name,
            bucket=s3_bucket,
            audio_key="audio.wav",
            output_bucket=s3_bucket,
            output_prefix="transcripts/",
            language_code="en-US",
            region_name=REGION,
        )
        assert result.job_name == job_name
        assert result.status == "COMPLETED"
        assert isinstance(result.transcript_text, str)


# ---------------------------------------------------------------------------
# 10. comprehend_pii_redactor
# ---------------------------------------------------------------------------


class TestComprehendPiiRedactor:
    @pytest.mark.skip(reason="Comprehend not available in LocalStack community")
    def test_redacts_pii(self, s3_bucket):
        from aws_util.ai_ml_pipelines import comprehend_pii_redactor

        result = comprehend_pii_redactor(
            text="My name is John Doe and my email is john@example.com",
            bucket=s3_bucket,
            output_key="redacted/output.txt",
            replacement="[REDACTED]",
            language_code="en",
            region_name=REGION,
        )
        assert result.redacted_key == "redacted/output.txt"
        assert isinstance(result.pii_entities_found, int)
        assert isinstance(result.entity_types, list)


# ---------------------------------------------------------------------------
# 11. textract_form_extractor
# ---------------------------------------------------------------------------


class TestTextractFormExtractor:
    @pytest.mark.skip(reason="Textract not available in LocalStack community")
    def test_extracts_form_data(self, s3_bucket, dynamodb_table):
        from aws_util.ai_ml_pipelines import textract_form_extractor

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="form.pdf", Body=b"%PDF-1.4 fake pdf content")

        result = textract_form_extractor(
            bucket=s3_bucket,
            key="form.pdf",
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert isinstance(result.page_count, int)
        assert isinstance(result.key_value_pairs, list)
        assert isinstance(result.items_stored, int)


# ---------------------------------------------------------------------------
# 12. bedrock_knowledge_base_ingestor
# ---------------------------------------------------------------------------


class TestBedrockKnowledgeBaseIngestor:
    @pytest.mark.skip(reason="Bedrock not available in LocalStack community")
    def test_ingests_documents(self, s3_bucket):
        from aws_util.ai_ml_pipelines import bedrock_knowledge_base_ingestor

        s3 = ls_client("s3")
        s3.put_object(Bucket=s3_bucket, Key="doc1.txt", Body=b"Document one content")
        s3.put_object(Bucket=s3_bucket, Key="doc2.txt", Body=b"Document two content")

        result = bedrock_knowledge_base_ingestor(
            knowledge_base_id="kb-test-001",
            data_source_id="ds-test-001",
            bucket=s3_bucket,
            document_keys=["doc1.txt", "doc2.txt"],
            region_name=REGION,
        )
        assert isinstance(result.ingestion_job_id, str)
        assert result.documents_uploaded == 2
        assert result.status in ("COMPLETE", "FAILED")


# ---------------------------------------------------------------------------
# 13. bedrock_guardrail_enforcer
# ---------------------------------------------------------------------------


class TestBedrockGuardrailEnforcer:
    @pytest.mark.skip(reason="Bedrock not available in LocalStack community")
    def test_enforces_guardrail(self, logs_group):
        from aws_util.ai_ml_pipelines import bedrock_guardrail_enforcer

        result = bedrock_guardrail_enforcer(
            guardrail_id="gr-test-001",
            guardrail_version="1",
            text="This is some text to check against the guardrail",
            source="INPUT",
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert result.action in ("ALLOWED", "BLOCKED", "NONE")
        assert isinstance(result.violations, list)
        assert isinstance(result.logged, bool)


# ---------------------------------------------------------------------------
# 14. personalize_real_time_recommender
# ---------------------------------------------------------------------------


class TestPersonalizeRealTimeRecommender:
    @pytest.mark.skip(reason="Personalize not available in LocalStack community")
    def test_recommends_items(self):
        from aws_util.ai_ml_pipelines import personalize_real_time_recommender

        result = personalize_real_time_recommender(
            tracking_id="tracking-test-001",
            campaign_arn="arn:aws:personalize:us-east-1:000000000000:campaign/test-campaign",
            user_id="user-001",
            item_id="item-001",
            event_type="click",
            session_id="session-001",
            num_results=5,
            region_name=REGION,
        )
        assert result.event_recorded is True
        assert isinstance(result.recommendations, list)


# ---------------------------------------------------------------------------
# 15. forecast_inference_pipeline
# ---------------------------------------------------------------------------


class TestForecastInferencePipeline:
    @pytest.mark.skip(reason="Forecast not available in LocalStack community")
    def test_exports_forecast(self, dynamodb_table, s3_bucket, iam_role):
        from aws_util.ai_ml_pipelines import forecast_inference_pipeline

        result = forecast_inference_pipeline(
            forecast_arn="arn:aws:forecast:us-east-1:000000000000:forecast/test-forecast",
            s3_path=f"s3://{s3_bucket}/forecast-output/",
            iam_role_arn=iam_role,
            table_name=dynamodb_table,
            region_name=REGION,
        )
        assert isinstance(result.export_job_arn, str)
        assert result.status in ("ACTIVE", "CREATE_FAILED")
        assert isinstance(result.predictions_loaded, int)


# ---------------------------------------------------------------------------
# 16. sagemaker_batch_transform_monitor
# ---------------------------------------------------------------------------


class TestSagemakerBatchTransformMonitor:
    @pytest.mark.skip(reason="SageMaker not available in LocalStack community")
    def test_monitors_transform_job(self, s3_bucket, sqs_queue):
        from aws_util.ai_ml_pipelines import sagemaker_batch_transform_monitor

        job_name = f"test-transform-{int(time.time())}"
        result = sagemaker_batch_transform_monitor(
            job_name=job_name,
            model_name="test-model",
            input_s3_uri=f"s3://{s3_bucket}/input/",
            output_s3_uri=f"s3://{s3_bucket}/output/",
            instance_type="ml.m5.xlarge",
            instance_count=1,
            queue_url=sqs_queue,
            content_type="text/csv",
            region_name=REGION,
        )
        assert result.job_name == job_name
        assert result.status in ("Completed", "Failed")
        assert isinstance(result.output_s3_uri, str)
