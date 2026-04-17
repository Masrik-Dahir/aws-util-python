"""Tests for aws_util.ai_ml_pipelines module."""
from __future__ import annotations

import io
import json

from unittest.mock import MagicMock
import pytest
from botocore.exceptions import ClientError

from aws_util.ai_ml_pipelines import (
    BatchTransformResult,
    BedrockChainResult,
    DocumentProcessorResult,
    EmbeddingIndexResult,
    FaceIndexResult,
    ForecastExportResult,
    FormExtractResult,
    GuardrailResult,
    ImageModerationResult,
    KBIngestResult,
    PIIRedactorResult,
    PollyAudioResult,
    RecommenderResult,
    TranscribeJobResult,
    TranslationResult,
    VideoLabelResult,
    bedrock_guardrail_enforcer,
    bedrock_knowledge_base_ingestor,
    bedrock_serverless_chain,
    comprehend_pii_redactor,
    embedding_indexer,
    forecast_inference_pipeline,
    image_moderation_pipeline,
    personalize_real_time_recommender,
    polly_audio_generator,
    rekognition_face_indexer,
    rekognition_video_label_pipeline,
    s3_document_processor,
    sagemaker_batch_transform_monitor,
    textract_form_extractor,
    transcribe_job_to_s3,
    translation_pipeline,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "op"
    )


@pytest.fixture(autouse=True)
def _aws(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", REGION)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------


def _bedrock_body(text: str) -> io.BytesIO:
    """Build a readable body mimicking Bedrock invoke_model."""
    payload = {
        "content": [{"text": text}],
    }
    return io.BytesIO(json.dumps(payload).encode())


def _embedding_body(dims: int = 3) -> io.BytesIO:
    payload = {"embedding": [0.1] * dims}
    return io.BytesIO(json.dumps(payload).encode())


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_bedrock_chain_result(self) -> None:
        r = BedrockChainResult(
            conversation_id="c1",
            steps_completed=2,
            outputs=["a", "b"],
            model_id="m",
        )
        assert r.conversation_id == "c1"
        assert r.steps_completed == 2
        assert r.outputs == ["a", "b"]
        assert r.model_id == "m"

    def test_document_processor_result(self) -> None:
        r = DocumentProcessorResult(
            bucket="b",
            key="k",
            extracted_text="hello",
            sentiment="POSITIVE",
            sentiment_scores={"Positive": 0.99},
            entities=[],
        )
        assert r.sentiment == "POSITIVE"

    def test_image_moderation_result(self) -> None:
        r = ImageModerationResult(
            bucket="b",
            key="k",
            moderation_labels=[],
            labels=[],
            flagged=False,
            alert_sent=False,
        )
        assert r.flagged is False
        assert r.message_id is None

    def test_translation_result(self) -> None:
        r = TranslationResult(
            translated_count=1,
            source_language="en",
            target_language="es",
            output_keys=["translated/es/doc.txt"],
        )
        assert r.translated_count == 1

    def test_embedding_index_result(self) -> None:
        r = EmbeddingIndexResult(
            items_indexed=5,
            model_id="titan",
            dimensions=256,
        )
        assert r.items_indexed == 5
        assert r.dimensions == 256


# ==================================================================
# 1. bedrock_serverless_chain
# ==================================================================


class TestBedrockServerlessChain:
    def test_success_single_prompt(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.return_value = {
            "body": _bedrock_body("answer1"),
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_serverless_chain(
            prompts=["hello"],
            model_id="anthropic.claude-3-haiku",
            conversation_id="conv-1",
            table_name="table",
        )
        assert result.steps_completed == 1
        assert result.outputs == ["answer1"]
        assert result.conversation_id == "conv-1"
        mock_bedrock.invoke_model.assert_called_once()
        mock_ddb.put_item.assert_called_once()

    def test_success_multiple_prompts(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.side_effect = [
            {"body": _bedrock_body("out1")},
            {"body": _bedrock_body("out2")},
        ]
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_serverless_chain(
            prompts=["p1", "p2"],
            model_id="m",
            conversation_id="c2",
            table_name="t",
        )
        assert result.steps_completed == 2
        assert result.outputs == ["out1", "out2"]

    def test_bedrock_invoke_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.side_effect = _client_error(
            "ValidationException"
        )
        mock_ddb = _mock()

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Bedrock invocation failed"
        ):
            bedrock_serverless_chain(
                prompts=["hello"],
                model_id="m",
                conversation_id="c",
                table_name="t",
            )

    def test_dynamodb_store_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.return_value = {
            "body": _bedrock_body("ok"),
        }
        mock_ddb = _mock()
        mock_ddb.put_item.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to store conversation"
        ):
            bedrock_serverless_chain(
                prompts=["hi"],
                model_id="m",
                conversation_id="c",
                table_name="t",
            )

    def test_empty_prompts(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_serverless_chain(
            prompts=[],
            model_id="m",
            conversation_id="c",
            table_name="t",
        )
        assert result.steps_completed == 0
        assert result.outputs == []
        mock_bedrock.invoke_model.assert_not_called()


# ==================================================================
# 2. s3_document_processor
# ==================================================================


class TestS3DocumentProcessor:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"hello world"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.return_value = {
            "Blocks": [
                {"BlockType": "LINE", "Text": "hello"},
                {"BlockType": "LINE", "Text": "world"},
                {"BlockType": "WORD", "Text": "ignored"},
            ],
        }
        mock_comprehend = _mock()
        mock_comprehend.detect_sentiment.return_value = {
            "Sentiment": "POSITIVE",
            "SentimentScore": {
                "Positive": 0.95,
                "Negative": 0.01,
                "Neutral": 0.03,
                "Mixed": 0.01,
            },
        }
        mock_comprehend.detect_entities.return_value = {
            "Entities": [
                {"Text": "hello", "Type": "OTHER", "Score": 0.8}
            ],
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": mock_comprehend,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = s3_document_processor(
            bucket="docs", key="doc.pdf", table_name="results"
        )
        assert result.bucket == "docs"
        assert result.key == "doc.pdf"
        assert result.extracted_text == "hello\nworld"
        assert result.sentiment == "POSITIVE"
        assert result.sentiment_scores["Positive"] == 0.95
        assert len(result.entities) == 1

    def test_s3_read_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.side_effect = _client_error(
            "NoSuchKey"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": _mock(),
                "comprehend": _mock(),
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to read"):
            s3_document_processor(
                bucket="b", key="k", table_name="t"
            )

    def test_textract_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"data"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.side_effect = (
            _client_error("InvalidParameterException")
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": _mock(),
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Textract extraction failed"
        ):
            s3_document_processor(
                bucket="b", key="k", table_name="t"
            )

    def test_comprehend_sentiment_error(
        self, monkeypatch
    ) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"data"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.return_value = {
            "Blocks": [{"BlockType": "LINE", "Text": "hi"}]
        }
        mock_comprehend = _mock()
        mock_comprehend.detect_sentiment.side_effect = (
            _client_error("TextSizeLimitExceededException")
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": mock_comprehend,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="sentiment analysis failed"
        ):
            s3_document_processor(
                bucket="b", key="k", table_name="t"
            )

    def test_comprehend_entity_error(
        self, monkeypatch
    ) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"data"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.return_value = {
            "Blocks": [{"BlockType": "LINE", "Text": "hi"}]
        }
        mock_comprehend = _mock()
        mock_comprehend.detect_sentiment.return_value = {
            "Sentiment": "NEUTRAL",
            "SentimentScore": {},
        }
        mock_comprehend.detect_entities.side_effect = (
            _client_error("InternalServerException")
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": mock_comprehend,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="entity detection failed"
        ):
            s3_document_processor(
                bucket="b", key="k", table_name="t"
            )

    def test_dynamodb_store_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"data"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.return_value = {
            "Blocks": []
        }
        mock_comprehend = _mock()
        mock_comprehend.detect_sentiment.return_value = {
            "Sentiment": "NEUTRAL",
            "SentimentScore": {},
        }
        mock_comprehend.detect_entities.return_value = {
            "Entities": []
        }
        mock_ddb = _mock()
        mock_ddb.put_item.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": mock_comprehend,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to store results"
        ):
            s3_document_processor(
                bucket="b", key="k", table_name="t"
            )

    def test_empty_blocks(self, monkeypatch) -> None:
        """No LINE blocks produces empty text; comprehend gets 'empty'."""
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"data"),
        }
        mock_textract = _mock()
        mock_textract.detect_document_text.return_value = {
            "Blocks": [{"BlockType": "WORD", "Text": "w"}]
        }
        mock_comprehend = _mock()
        mock_comprehend.detect_sentiment.return_value = {
            "Sentiment": "NEUTRAL",
            "SentimentScore": {},
        }
        mock_comprehend.detect_entities.return_value = {
            "Entities": []
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "textract": mock_textract,
                "comprehend": mock_comprehend,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = s3_document_processor(
            bucket="b", key="k", table_name="t"
        )
        assert result.extracted_text == ""
        # Comprehend called with "empty" for empty text
        call_args = (
            mock_comprehend.detect_sentiment.call_args
        )
        assert call_args.kwargs["Text"] == "empty"


# ==================================================================
# 3. image_moderation_pipeline
# ==================================================================


class TestImageModerationPipeline:
    def test_success_no_moderation(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"\x89PNG"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": []
        }
        mock_rek.detect_labels.return_value = {
            "Labels": [
                {"Name": "Dog", "Confidence": 99.5},
            ]
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = image_moderation_pipeline(
            bucket="imgs",
            key="photo.jpg",
            table_name="results",
        )
        assert result.flagged is False
        assert result.alert_sent is False
        assert result.labels[0]["Name"] == "Dog"
        assert len(result.moderation_labels) == 0

    def test_flagged_with_sns_alert(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"\x89PNG"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": [
                {
                    "Name": "Explicit",
                    "Confidence": 95.0,
                    "ParentName": "",
                }
            ]
        }
        mock_rek.detect_labels.return_value = {"Labels": []}
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}
        mock_sns = _mock()
        mock_sns.publish.return_value = {
            "MessageId": "msg-123"
        }

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": mock_ddb,
                "sns": mock_sns,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = image_moderation_pipeline(
            bucket="imgs",
            key="bad.jpg",
            table_name="results",
            sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
        )
        assert result.flagged is True
        assert result.alert_sent is True
        assert result.message_id == "msg-123"
        mock_sns.publish.assert_called_once()

    def test_flagged_no_sns_topic(self, monkeypatch) -> None:
        """Flagged but no SNS topic provided => no alert."""
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"\x89PNG"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": [
                {"Name": "Violence", "Confidence": 80.0}
            ]
        }
        mock_rek.detect_labels.return_value = {"Labels": []}
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = image_moderation_pipeline(
            bucket="imgs",
            key="bad.jpg",
            table_name="results",
        )
        assert result.flagged is True
        assert result.alert_sent is False
        assert result.message_id is None

    def test_s3_read_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.side_effect = _client_error(
            "NoSuchKey"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": _mock(),
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to read"):
            image_moderation_pipeline(
                bucket="b",
                key="k",
                table_name="t",
            )

    def test_moderation_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"img"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.side_effect = (
            _client_error("InvalidParameterException")
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Rekognition moderation failed"
        ):
            image_moderation_pipeline(
                bucket="b",
                key="k",
                table_name="t",
            )

    def test_label_detection_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"img"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": []
        }
        mock_rek.detect_labels.side_effect = _client_error(
            "ImageTooLargeException"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="label detection failed"
        ):
            image_moderation_pipeline(
                bucket="b",
                key="k",
                table_name="t",
            )

    def test_dynamodb_store_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"img"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": []
        }
        mock_rek.detect_labels.return_value = {"Labels": []}
        mock_ddb = _mock()
        mock_ddb.put_item.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to store results"
        ):
            image_moderation_pipeline(
                bucket="b",
                key="k",
                table_name="t",
            )

    def test_sns_publish_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"img"),
        }
        mock_rek = _mock()
        mock_rek.detect_moderation_labels.return_value = {
            "ModerationLabels": [
                {"Name": "Bad", "Confidence": 90.0}
            ]
        }
        mock_rek.detect_labels.return_value = {"Labels": []}
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}
        mock_sns = _mock()
        mock_sns.publish.side_effect = _client_error(
            "AuthorizationError"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "rekognition": mock_rek,
                "dynamodb": mock_ddb,
                "sns": mock_sns,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to send moderation alert"
        ):
            image_moderation_pipeline(
                bucket="b",
                key="k",
                table_name="t",
                sns_topic_arn="arn:aws:sns:us-east-1:1:topic",
            )


# ==================================================================
# 4. translation_pipeline
# ==================================================================


class TestTranslationPipeline:
    def test_success_single_key(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"Hello world"),
        }
        mock_s3.put_object.return_value = {}
        mock_translate = _mock()
        mock_translate.translate_text.return_value = {
            "TranslatedText": "Hola mundo",
            "SourceLanguageCode": "en",
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = translation_pipeline(
            bucket="docs",
            source_keys=["doc.txt"],
            target_language="es",
            table_name="meta",
        )
        assert result.translated_count == 1
        assert result.target_language == "es"
        assert result.source_language == "en"
        assert len(result.output_keys) == 1
        assert "translated/es/doc.txt" in result.output_keys[0]

    def test_success_multiple_keys(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.side_effect = [
            {"Body": io.BytesIO(b"one")},
            {"Body": io.BytesIO(b"two")},
        ]
        mock_s3.put_object.return_value = {}
        mock_translate = _mock()
        mock_translate.translate_text.side_effect = [
            {
                "TranslatedText": "uno",
                "SourceLanguageCode": "en",
            },
            {
                "TranslatedText": "dos",
                "SourceLanguageCode": "en",
            },
        ]
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = translation_pipeline(
            bucket="docs",
            source_keys=["a.txt", "b.txt"],
            target_language="es",
            table_name="meta",
        )
        assert result.translated_count == 2
        assert len(result.output_keys) == 2

    def test_s3_read_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.side_effect = _client_error(
            "NoSuchKey"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": _mock(),
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to read"):
            translation_pipeline(
                bucket="b",
                source_keys=["k"],
                target_language="es",
                table_name="t",
            )

    def test_translate_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"text"),
        }
        mock_translate = _mock()
        mock_translate.translate_text.side_effect = (
            _client_error("UnsupportedLanguagePairException")
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Translation failed"
        ):
            translation_pipeline(
                bucket="b",
                source_keys=["k"],
                target_language="xx",
                table_name="t",
            )

    def test_s3_write_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"text"),
        }
        mock_s3.put_object.side_effect = _client_error(
            "AccessDenied"
        )
        mock_translate = _mock()
        mock_translate.translate_text.return_value = {
            "TranslatedText": "translated",
            "SourceLanguageCode": "en",
        }

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to write"
        ):
            translation_pipeline(
                bucket="b",
                source_keys=["k"],
                target_language="es",
                table_name="t",
            )

    def test_dynamodb_metadata_error(
        self, monkeypatch
    ) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_s3.get_object.return_value = {
            "Body": io.BytesIO(b"text"),
        }
        mock_s3.put_object.return_value = {}
        mock_translate = _mock()
        mock_translate.translate_text.return_value = {
            "TranslatedText": "translated",
            "SourceLanguageCode": "en",
        }
        mock_ddb = _mock()
        mock_ddb.put_item.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to store metadata"
        ):
            translation_pipeline(
                bucket="b",
                source_keys=["k"],
                target_language="es",
                table_name="t",
            )

    def test_empty_keys(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = _mock()
        mock_translate = _mock()
        mock_ddb = _mock()

        def factory(svc, region_name=None):
            return {
                "s3": mock_s3,
                "translate": mock_translate,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = translation_pipeline(
            bucket="b",
            source_keys=[],
            target_language="es",
            table_name="t",
        )
        assert result.translated_count == 0
        assert result.output_keys == []


# ==================================================================
# 5. embedding_indexer
# ==================================================================


class TestEmbeddingIndexer:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.side_effect = [
            {"body": _embedding_body(dims=4)},
            {"body": _embedding_body(dims=4)},
        ]
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = embedding_indexer(
            texts=["hello", "world"],
            model_id="amazon.titan-embed-text-v1",
            table_name="vectors",
        )
        assert result.items_indexed == 2
        assert result.dimensions == 4
        assert result.model_id == "amazon.titan-embed-text-v1"
        assert mock_ddb.put_item.call_count == 2

    def test_bedrock_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.side_effect = _client_error(
            "ValidationException"
        )

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": _mock(),
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Bedrock embedding failed"
        ):
            embedding_indexer(
                texts=["hi"],
                model_id="m",
                table_name="t",
            )

    def test_dynamodb_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_bedrock.invoke_model.return_value = {
            "body": _embedding_body(dims=2),
        }
        mock_ddb = _mock()
        mock_ddb.put_item.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(
            RuntimeError, match="Failed to store embedding"
        ):
            embedding_indexer(
                texts=["hi"],
                model_id="m",
                table_name="t",
            )

    def test_empty_texts(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_bedrock = _mock()
        mock_ddb = _mock()

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = embedding_indexer(
            texts=[],
            model_id="m",
            table_name="t",
        )
        assert result.items_indexed == 0
        assert result.dimensions == 0
        mock_bedrock.invoke_model.assert_not_called()

    def test_empty_embedding_response(
        self, monkeypatch
    ) -> None:
        """When Bedrock returns empty embedding list."""
        import aws_util.ai_ml_pipelines as mod

        empty_body = io.BytesIO(
            json.dumps({"embedding": []}).encode()
        )
        mock_bedrock = _mock()
        mock_bedrock.invoke_model.return_value = {
            "body": empty_body,
        }
        mock_ddb = _mock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {
                "bedrock-runtime": mock_bedrock,
                "dynamodb": mock_ddb,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = embedding_indexer(
            texts=["hi"],
            model_id="m",
            table_name="t",
        )
        assert result.items_indexed == 1
        assert result.dimensions == 0


# ==================================================================
# 6. rekognition_face_indexer
# ==================================================================


class TestRekognitionFaceIndexer:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.return_value = {}
        mock_rek.index_faces.return_value = {
            "FaceRecords": [
                {"Face": {"FaceId": "face-1"}},
                {"Face": {"FaceId": "face-2"}},
            ],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = rekognition_face_indexer(
            collection_id="col1",
            bucket="imgs",
            keys=["a.jpg"],
            table_name="faces",
            user_ids=["u1"],
        )
        assert result.faces_indexed == 2
        assert len(result.face_records) == 2
        mock_rek.create_collection.assert_called_once()
        assert mock_ddb.put_item.call_count == 2

    def test_collection_already_exists(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.side_effect = _client_error(
            "ResourceAlreadyExistsException"
        )
        mock_rek.index_faces.return_value = {
            "FaceRecords": [{"Face": {"FaceId": "f1"}}],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = rekognition_face_indexer(
            collection_id="col1",
            bucket="b",
            keys=["x.jpg"],
            table_name="t",
            user_ids=["u1"],
        )
        assert result.faces_indexed == 1

    def test_create_collection_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.side_effect = _client_error("AccessDeniedException")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to create collection"):
            rekognition_face_indexer(
                collection_id="c", bucket="b", keys=["k"], table_name="t", user_ids=["u"]
            )

    def test_index_faces_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.return_value = {}
        mock_rek.index_faces.side_effect = _client_error("InvalidParameterException")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Rekognition index_faces failed"):
            rekognition_face_indexer(
                collection_id="c", bucket="b", keys=["k"], table_name="t", user_ids=["u"]
            )

    def test_ddb_put_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.return_value = {}
        mock_rek.index_faces.return_value = {
            "FaceRecords": [{"Face": {"FaceId": "f1"}}],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.side_effect = _client_error("ResourceNotFoundException")

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to store face mapping"):
            rekognition_face_indexer(
                collection_id="c", bucket="b", keys=["k"], table_name="t", user_ids=["u"]
            )

    def test_empty_face_id_skipped(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.create_collection.return_value = {}
        mock_rek.index_faces.return_value = {
            "FaceRecords": [{"Face": {"FaceId": ""}}, {"Face": {"FaceId": "f1"}}],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = rekognition_face_indexer(
            collection_id="c", bucket="b", keys=["k"], table_name="t", user_ids=["u"]
        )
        assert result.faces_indexed == 2
        # Only 1 put_item since empty FaceId is skipped
        assert mock_ddb.put_item.call_count == 1


# ==================================================================
# 7. rekognition_video_label_pipeline
# ==================================================================


class TestRekognitionVideoLabelPipeline:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.start_label_detection.return_value = {"JobId": "job-1"}
        mock_rek.get_label_detection.return_value = {
            "JobStatus": "SUCCEEDED",
            "Labels": [{"Label": {"Name": "Car"}, "Timestamp": 0}],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        result = rekognition_video_label_pipeline(
            bucket="vids",
            video_key="clip.mp4",
            table_name="labels",
            sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
            role_arn="arn:aws:iam::123:role/rek",
        )
        assert result.job_id == "job-1"
        assert result.status == "SUCCEEDED"
        assert result.labels_count == 1

    def test_start_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.start_label_detection.side_effect = _client_error("AccessDeniedException")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to start label detection"):
            rekognition_video_label_pipeline(
                bucket="b", video_key="v", table_name="t",
                sns_topic_arn="arn", role_arn="arn",
            )

    def test_poll_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.start_label_detection.return_value = {"JobId": "j1"}
        mock_rek.get_label_detection.side_effect = _client_error("InternalError")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to poll label detection"):
            rekognition_video_label_pipeline(
                bucket="b", video_key="v", table_name="t",
                sns_topic_arn="arn", role_arn="arn",
            )

    def test_job_failed(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.start_label_detection.return_value = {"JobId": "j1"}
        mock_rek.get_label_detection.return_value = {
            "JobStatus": "FAILED",
            "StatusMessage": "bad video",
            "Labels": [],
        }
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="failed: bad video"):
            rekognition_video_label_pipeline(
                bucket="b", video_key="v", table_name="t",
                sns_topic_arn="arn", role_arn="arn",
            )

    def test_ddb_store_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_rek = MagicMock()
        mock_rek.start_label_detection.return_value = {"JobId": "j1"}
        mock_rek.get_label_detection.return_value = {
            "JobStatus": "SUCCEEDED",
            "Labels": [{"Label": {"Name": "X"}}],
        }
        mock_ddb = MagicMock()
        mock_ddb.put_item.side_effect = _client_error("ResourceNotFoundException")

        def factory(svc, region_name=None):
            return {"rekognition": mock_rek, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to store label"):
            rekognition_video_label_pipeline(
                bucket="b", video_key="v", table_name="t",
                sns_topic_arn="arn", role_arn="arn",
            )


# ==================================================================
# 8. polly_audio_generator
# ==================================================================


class TestPollyAudioGenerator:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_polly = MagicMock()
        mock_polly.synthesize_speech.return_value = {
            "AudioStream": io.BytesIO(b"audio-data"),
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_s3.generate_presigned_url.return_value = "https://presigned.url"

        def factory(svc, region_name=None):
            return {"polly": mock_polly, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = polly_audio_generator(
            text="Hello world",
            bucket="audio-bucket",
        )
        assert result.presigned_url == "https://presigned.url"
        assert result.content_type == "audio/mpeg"
        assert "polly-audio/" in result.s3_key

    def test_polly_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_polly = MagicMock()
        mock_polly.synthesize_speech.side_effect = _client_error("ValidationException")
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"polly": mock_polly, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Polly synthesize_speech failed"):
            polly_audio_generator(text="hi", bucket="b")

    def test_s3_upload_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_polly = MagicMock()
        mock_polly.synthesize_speech.return_value = {
            "AudioStream": io.BytesIO(b"data"),
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = _client_error("AccessDenied")

        def factory(svc, region_name=None):
            return {"polly": mock_polly, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to upload audio"):
            polly_audio_generator(text="hi", bucket="b")

    def test_presign_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_polly = MagicMock()
        mock_polly.synthesize_speech.return_value = {
            "AudioStream": io.BytesIO(b"data"),
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_s3.generate_presigned_url.side_effect = _client_error("InternalError")

        def factory(svc, region_name=None):
            return {"polly": mock_polly, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to generate pre-signed URL"):
            polly_audio_generator(text="hi", bucket="b")


# ==================================================================
# 9. transcribe_job_to_s3
# ==================================================================


class TestTranscribeJobToS3:
    def test_success(self, monkeypatch) -> None:
        import urllib.request

        import aws_util.ai_ml_pipelines as mod

        mock_transcribe = MagicMock()
        mock_transcribe.start_transcription_job.return_value = {}
        mock_transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {
                "TranscriptionJobStatus": "COMPLETED",
                "Transcript": {"TranscriptFileUri": "https://example.com/transcript.json"},
            },
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"transcribe": mock_transcribe, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        transcript_json = {
            "results": {"transcripts": [{"transcript": "hello world"}]}
        }
        fake_response = io.BytesIO(json.dumps(transcript_json).encode())
        fake_response.read = fake_response.read
        monkeypatch.setattr(
            urllib.request, "urlopen",
            lambda url: fake_response,
        )

        result = transcribe_job_to_s3(
            job_name="job1",
            bucket="audio",
            audio_key="audio.mp3",
            output_bucket="out",
            output_prefix="transcripts/",
        )
        assert result.job_name == "job1"
        assert result.status == "COMPLETED"
        assert result.transcript_text == "hello world"
        assert "transcripts/" in result.transcript_key

    def test_start_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_transcribe = MagicMock()
        mock_transcribe.start_transcription_job.side_effect = _client_error("LimitExceededException")
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"transcribe": mock_transcribe, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to start transcription"):
            transcribe_job_to_s3(
                job_name="j", bucket="b", audio_key="a",
                output_bucket="o", output_prefix="p",
            )

    def test_poll_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_transcribe = MagicMock()
        mock_transcribe.start_transcription_job.return_value = {}
        mock_transcribe.get_transcription_job.side_effect = _client_error("InternalFailureException")
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"transcribe": mock_transcribe, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to poll transcription"):
            transcribe_job_to_s3(
                job_name="j", bucket="b", audio_key="a",
                output_bucket="o", output_prefix="p",
            )

    def test_job_failed(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_transcribe = MagicMock()
        mock_transcribe.start_transcription_job.return_value = {}
        mock_transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {
                "TranscriptionJobStatus": "FAILED",
                "FailureReason": "bad audio",
            },
        }
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"transcribe": mock_transcribe, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="failed: bad audio"):
            transcribe_job_to_s3(
                job_name="j", bucket="b", audio_key="a",
                output_bucket="o", output_prefix="p",
            )


# ==================================================================
# 10. comprehend_pii_redactor
# ==================================================================


class TestComprehendPIIRedactor:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_comprehend = MagicMock()
        mock_comprehend.detect_pii_entities.return_value = {
            "Entities": [
                {"Type": "EMAIL_ADDRESS", "BeginOffset": 10, "EndOffset": 25},
                {"Type": "NAME", "BeginOffset": 0, "EndOffset": 5},
            ],
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"comprehend": mock_comprehend, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = comprehend_pii_redactor(
            text="Hello user@example.com here",
            bucket="pii",
            output_key="redacted.txt",
        )
        assert result.pii_entities_found == 2
        assert len(result.entity_types) > 0
        assert result.redacted_key == "redacted.txt"

    def test_no_pii(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_comprehend = MagicMock()
        mock_comprehend.detect_pii_entities.return_value = {"Entities": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"comprehend": mock_comprehend, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = comprehend_pii_redactor(
            text="No PII here", bucket="b", output_key="out.txt",
        )
        assert result.pii_entities_found == 0
        assert result.entity_types == []

    def test_comprehend_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_comprehend = MagicMock()
        mock_comprehend.detect_pii_entities.side_effect = _client_error("TextSizeLimitExceededException")
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"comprehend": mock_comprehend, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Comprehend detect_pii_entities failed"):
            comprehend_pii_redactor(text="x", bucket="b", output_key="k")

    def test_s3_upload_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_comprehend = MagicMock()
        mock_comprehend.detect_pii_entities.return_value = {"Entities": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = _client_error("AccessDenied")

        def factory(svc, region_name=None):
            return {"comprehend": mock_comprehend, "s3": mock_s3}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to write redacted text"):
            comprehend_pii_redactor(text="x", bucket="b", output_key="k")


# ==================================================================
# 11. textract_form_extractor
# ==================================================================


class TestTextractFormExtractor:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        blocks = [
            {"Id": "1", "BlockType": "KEY_VALUE_SET", "EntityTypes": ["KEY"],
             "Relationships": [
                 {"Type": "CHILD", "Ids": ["3"]},
                 {"Type": "VALUE", "Ids": ["2"]},
             ], "Page": 1},
            {"Id": "2", "BlockType": "KEY_VALUE_SET", "EntityTypes": ["VALUE"],
             "Relationships": [
                 {"Type": "CHILD", "Ids": ["4"]},
             ], "Page": 1},
            {"Id": "3", "BlockType": "WORD", "Text": "Name", "Page": 1},
            {"Id": "4", "BlockType": "WORD", "Text": "Alice", "Page": 1},
        ]
        mock_textract = MagicMock()
        mock_textract.analyze_document.return_value = {"Blocks": blocks}
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"textract": mock_textract, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = textract_form_extractor(
            bucket="docs", key="form.pdf", table_name="forms",
        )
        assert result.page_count == 1
        assert len(result.key_value_pairs) == 1
        assert result.key_value_pairs[0]["key"] == "Name"
        assert result.key_value_pairs[0]["value"] == "Alice"
        assert result.items_stored == 1

    def test_textract_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_textract = MagicMock()
        mock_textract.analyze_document.side_effect = _client_error("InvalidParameterException")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"textract": mock_textract, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Textract analyze_document failed"):
            textract_form_extractor(bucket="b", key="k", table_name="t")

    def test_ddb_store_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        blocks = [
            {"Id": "1", "BlockType": "KEY_VALUE_SET", "EntityTypes": ["KEY"],
             "Relationships": [
                 {"Type": "CHILD", "Ids": ["3"]},
                 {"Type": "VALUE", "Ids": ["2"]},
             ], "Page": 1},
            {"Id": "2", "BlockType": "KEY_VALUE_SET", "EntityTypes": ["VALUE"],
             "Relationships": [{"Type": "CHILD", "Ids": ["4"]}], "Page": 1},
            {"Id": "3", "BlockType": "WORD", "Text": "K", "Page": 1},
            {"Id": "4", "BlockType": "WORD", "Text": "V", "Page": 1},
        ]
        mock_textract = MagicMock()
        mock_textract.analyze_document.return_value = {"Blocks": blocks}
        mock_ddb = MagicMock()
        mock_ddb.put_item.side_effect = _client_error("ResourceNotFoundException")

        def factory(svc, region_name=None):
            return {"textract": mock_textract, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to store form pair"):
            textract_form_extractor(bucket="b", key="k", table_name="t")


# ==================================================================
# 12. bedrock_knowledge_base_ingestor
# ==================================================================


class TestBedrockKnowledgeBaseIngestor:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {}
        mock_ba = MagicMock()
        mock_ba.start_ingestion_job.return_value = {
            "ingestionJob": {"ingestionJobId": "ing-1"},
        }
        mock_ba.get_ingestion_job.return_value = {
            "ingestionJob": {"status": "COMPLETE"},
        }

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "bedrock-agent": mock_ba}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        result = bedrock_knowledge_base_ingestor(
            knowledge_base_id="kb-1",
            data_source_id="ds-1",
            bucket="docs",
            document_keys=["a.pdf", "b.pdf"],
        )
        assert result.ingestion_job_id == "ing-1"
        assert result.status == "COMPLETE"
        assert result.documents_uploaded == 2

    def test_s3_verify_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = MagicMock()
        mock_s3.head_object.side_effect = _client_error("NoSuchKey")
        mock_ba = MagicMock()

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "bedrock-agent": mock_ba}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="not found"):
            bedrock_knowledge_base_ingestor(
                knowledge_base_id="kb", data_source_id="ds",
                bucket="b", document_keys=["missing.pdf"],
            )

    def test_start_ingestion_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {}
        mock_ba = MagicMock()
        mock_ba.start_ingestion_job.side_effect = _client_error("ValidationException")

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "bedrock-agent": mock_ba}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to start Bedrock ingestion"):
            bedrock_knowledge_base_ingestor(
                knowledge_base_id="kb", data_source_id="ds",
                bucket="b", document_keys=["d.pdf"],
            )

    def test_poll_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {}
        mock_ba = MagicMock()
        mock_ba.start_ingestion_job.return_value = {
            "ingestionJob": {"ingestionJobId": "ing-1"},
        }
        mock_ba.get_ingestion_job.side_effect = _client_error("InternalError")

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "bedrock-agent": mock_ba}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to poll ingestion"):
            bedrock_knowledge_base_ingestor(
                knowledge_base_id="kb", data_source_id="ds",
                bucket="b", document_keys=["d.pdf"],
            )

    def test_job_failed(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {}
        mock_ba = MagicMock()
        mock_ba.start_ingestion_job.return_value = {
            "ingestionJob": {"ingestionJobId": "ing-1"},
        }
        mock_ba.get_ingestion_job.return_value = {
            "ingestionJob": {"status": "FAILED"},
        }

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "bedrock-agent": mock_ba}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="ingestion job .* failed"):
            bedrock_knowledge_base_ingestor(
                knowledge_base_id="kb", data_source_id="ds",
                bucket="b", document_keys=["d.pdf"],
            )


# ==================================================================
# 13. bedrock_guardrail_enforcer
# ==================================================================


class TestBedrockGuardrailEnforcer:
    def test_no_violations(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_br = MagicMock()
        mock_br.apply_guardrail.return_value = {
            "action": "ALLOWED",
            "outputs": [],
            "assessments": [],
        }
        mock_logs = MagicMock()

        def factory(svc, region_name=None):
            return {"bedrock-runtime": mock_br, "logs": mock_logs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_guardrail_enforcer(
            guardrail_id="g1", guardrail_version="1",
            text="hello", source="INPUT",
            log_group_name="/guardrails",
        )
        assert result.action == "ALLOWED"
        assert result.violations == []
        assert result.logged is False

    def test_with_violations(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_br = MagicMock()
        mock_br.apply_guardrail.return_value = {
            "action": "BLOCKED",
            "outputs": [],
            "assessments": [
                {"topicPolicy": {"topics": [{"action": "BLOCKED", "name": "violence"}]}}
            ],
        }
        mock_logs = MagicMock()
        mock_logs.create_log_stream.return_value = {}
        mock_logs.put_log_events.return_value = {}

        def factory(svc, region_name=None):
            return {"bedrock-runtime": mock_br, "logs": mock_logs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_guardrail_enforcer(
            guardrail_id="g1", guardrail_version="1",
            text="bad text", source="INPUT",
            log_group_name="/guardrails",
        )
        assert result.action == "BLOCKED"
        assert len(result.violations) == 1
        assert result.logged is True

    def test_apply_guardrail_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_br = MagicMock()
        mock_br.apply_guardrail.side_effect = _client_error("ValidationException")
        mock_logs = MagicMock()

        def factory(svc, region_name=None):
            return {"bedrock-runtime": mock_br, "logs": mock_logs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to apply guardrail"):
            bedrock_guardrail_enforcer(
                guardrail_id="g1", guardrail_version="1",
                text="t", source="INPUT", log_group_name="/lg",
            )

    def test_log_stream_already_exists(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_br = MagicMock()
        mock_br.apply_guardrail.return_value = {
            "action": "BLOCKED",
            "outputs": [],
            "assessments": [
                {"topicPolicy": {"topics": [{"action": "BLOCKED", "name": "x"}]}}
            ],
        }
        mock_logs = MagicMock()
        mock_logs.create_log_stream.side_effect = _client_error("ResourceAlreadyExistsException")
        mock_logs.put_log_events.return_value = {}

        def factory(svc, region_name=None):
            return {"bedrock-runtime": mock_br, "logs": mock_logs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = bedrock_guardrail_enforcer(
            guardrail_id="g1", guardrail_version="1",
            text="t", source="INPUT", log_group_name="/lg",
        )
        assert result.logged is True

    def test_put_log_events_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_br = MagicMock()
        mock_br.apply_guardrail.return_value = {
            "action": "BLOCKED",
            "outputs": [],
            "assessments": [
                {"topicPolicy": {"topics": [{"action": "BLOCKED", "name": "x"}]}}
            ],
        }
        mock_logs = MagicMock()
        mock_logs.create_log_stream.return_value = {}
        mock_logs.put_log_events.side_effect = _client_error("InternalError")

        def factory(svc, region_name=None):
            return {"bedrock-runtime": mock_br, "logs": mock_logs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to put CloudWatch log events"):
            bedrock_guardrail_enforcer(
                guardrail_id="g1", guardrail_version="1",
                text="t", source="INPUT", log_group_name="/lg",
            )


# ==================================================================
# 14. personalize_real_time_recommender
# ==================================================================


class TestPersonalizeRealTimeRecommender:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_pe = MagicMock()
        mock_pe.put_events.return_value = {}
        mock_pr = MagicMock()
        mock_pr.get_recommendations.return_value = {
            "itemList": [{"itemId": "i1"}, {"itemId": "i2"}],
        }

        def factory(svc, region_name=None):
            return {
                "personalize-events": mock_pe,
                "personalize-runtime": mock_pr,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        result = personalize_real_time_recommender(
            tracking_id="trk",
            campaign_arn="arn:campaign",
            user_id="u1",
            item_id="item-1",
            event_type="click",
            session_id="sess-1",
        )
        assert result.event_recorded is True
        assert len(result.recommendations) == 2

    def test_put_events_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_pe = MagicMock()
        mock_pe.put_events.side_effect = _client_error("InvalidInputException")
        mock_pr = MagicMock()

        def factory(svc, region_name=None):
            return {
                "personalize-events": mock_pe,
                "personalize-runtime": mock_pr,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to record Personalize event"):
            personalize_real_time_recommender(
                tracking_id="t", campaign_arn="a", user_id="u",
                item_id="i", event_type="e", session_id="s",
            )

    def test_get_recommendations_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_pe = MagicMock()
        mock_pe.put_events.return_value = {}
        mock_pr = MagicMock()
        mock_pr.get_recommendations.side_effect = _client_error("ResourceNotFoundException")

        def factory(svc, region_name=None):
            return {
                "personalize-events": mock_pe,
                "personalize-runtime": mock_pr,
            }[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to get recommendations"):
            personalize_real_time_recommender(
                tracking_id="t", campaign_arn="a", user_id="u",
                item_id="i", event_type="e", session_id="s",
            )


# ==================================================================
# 15. forecast_inference_pipeline
# ==================================================================


class TestForecastInferencePipeline:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_forecast = MagicMock()
        mock_forecast.create_forecast_export_job.return_value = {
            "ForecastExportJobArn": "arn:forecast-export",
        }
        mock_forecast.describe_forecast_export_job.return_value = {
            "Status": "ACTIVE",
        }
        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {
            "Contents": [{"Key": "prefix/data.csv"}],
        }
        csv_content = "item_id,date,p10\nA,2024-01-01,100\n"
        body_mock = MagicMock()
        body_mock.read.return_value = csv_content.encode()
        mock_s3.get_object.return_value = {"Body": body_mock}
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"forecast": mock_forecast, "s3": mock_s3, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)
        monkeypatch.setattr(mod.time, "time", lambda: 1000000)

        result = forecast_inference_pipeline(
            forecast_arn="arn:forecast",
            s3_path="s3://bucket/prefix/",
            iam_role_arn="arn:role",
            table_name="preds",
        )
        assert result.export_job_arn == "arn:forecast-export"
        assert result.status == "ACTIVE"
        assert result.predictions_loaded == 1

    def test_create_export_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_forecast = MagicMock()
        mock_forecast.create_forecast_export_job.side_effect = _client_error("ResourceNotFoundException")
        mock_s3 = MagicMock()
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"forecast": mock_forecast, "s3": mock_s3, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "time", lambda: 1000000)

        with pytest.raises(RuntimeError, match="Failed to create Forecast export"):
            forecast_inference_pipeline(
                forecast_arn="a", s3_path="s3://b/p/", iam_role_arn="r", table_name="t",
            )

    def test_export_failed(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_forecast = MagicMock()
        mock_forecast.create_forecast_export_job.return_value = {
            "ForecastExportJobArn": "arn:job",
        }
        mock_forecast.describe_forecast_export_job.return_value = {
            "Status": "CREATE_FAILED",
        }
        mock_s3 = MagicMock()
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"forecast": mock_forecast, "s3": mock_s3, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)
        monkeypatch.setattr(mod.time, "time", lambda: 1000000)

        with pytest.raises(RuntimeError, match="Forecast export job .* failed"):
            forecast_inference_pipeline(
                forecast_arn="a", s3_path="s3://b/p/", iam_role_arn="r", table_name="t",
            )

    def test_poll_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_forecast = MagicMock()
        mock_forecast.create_forecast_export_job.return_value = {
            "ForecastExportJobArn": "arn:job",
        }
        mock_forecast.describe_forecast_export_job.side_effect = _client_error("InternalError")
        mock_s3 = MagicMock()
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"forecast": mock_forecast, "s3": mock_s3, "dynamodb": mock_ddb}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)
        monkeypatch.setattr(mod.time, "time", lambda: 1000000)

        with pytest.raises(RuntimeError, match="Failed to poll export job"):
            forecast_inference_pipeline(
                forecast_arn="a", s3_path="s3://b/p/", iam_role_arn="r", table_name="t",
            )


# ==================================================================
# 16. sagemaker_batch_transform_monitor
# ==================================================================


class TestSagemakerBatchTransformMonitor:
    def test_success(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_sm = MagicMock()
        mock_sm.create_transform_job.return_value = {}
        mock_sm.describe_transform_job.return_value = {
            "TransformJobStatus": "Completed",
        }
        mock_sqs = MagicMock()
        mock_sqs.send_message.return_value = {"MessageId": "msg-1"}

        def factory(svc, region_name=None):
            return {"sagemaker": mock_sm, "sqs": mock_sqs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        result = sagemaker_batch_transform_monitor(
            job_name="job1",
            model_name="model1",
            input_s3_uri="s3://in/data",
            output_s3_uri="s3://out/data",
            instance_type="ml.m5.xlarge",
            instance_count=1,
            queue_url="https://sqs.url/q",
        )
        assert result.job_name == "job1"
        assert result.status == "Completed"
        assert result.message_id == "msg-1"

    def test_create_job_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_sm = MagicMock()
        mock_sm.create_transform_job.side_effect = _client_error("ValidationException")
        mock_sqs = MagicMock()

        def factory(svc, region_name=None):
            return {"sagemaker": mock_sm, "sqs": mock_sqs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError, match="Failed to create SageMaker transform"):
            sagemaker_batch_transform_monitor(
                job_name="j", model_name="m", input_s3_uri="s3://i",
                output_s3_uri="s3://o", instance_type="ml.m5.xlarge",
                instance_count=1, queue_url="https://q",
            )

    def test_poll_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_sm = MagicMock()
        mock_sm.create_transform_job.return_value = {}
        mock_sm.describe_transform_job.side_effect = _client_error("InternalError")
        mock_sqs = MagicMock()

        def factory(svc, region_name=None):
            return {"sagemaker": mock_sm, "sqs": mock_sqs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to poll transform job"):
            sagemaker_batch_transform_monitor(
                job_name="j", model_name="m", input_s3_uri="s3://i",
                output_s3_uri="s3://o", instance_type="ml.m5.xlarge",
                instance_count=1, queue_url="https://q",
            )

    def test_sqs_error(self, monkeypatch) -> None:
        import aws_util.ai_ml_pipelines as mod

        mock_sm = MagicMock()
        mock_sm.create_transform_job.return_value = {}
        mock_sm.describe_transform_job.return_value = {
            "TransformJobStatus": "Completed",
        }
        mock_sqs = MagicMock()
        mock_sqs.send_message.side_effect = _client_error("QueueDoesNotExist")

        def factory(svc, region_name=None):
            return {"sagemaker": mock_sm, "sqs": mock_sqs}[svc]

        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)

        with pytest.raises(RuntimeError, match="Failed to send SQS message"):
            sagemaker_batch_transform_monitor(
                job_name="j", model_name="m", input_s3_uri="s3://i",
                output_s3_uri="s3://o", instance_type="ml.m5.xlarge",
                instance_count=1, queue_url="https://q",
            )


# ==================================================================
# Helpers (must be after all test classes to avoid conftest issues)
# ==================================================================

from unittest.mock import MagicMock  # noqa: E402


def _mock() -> MagicMock:
    return MagicMock()
