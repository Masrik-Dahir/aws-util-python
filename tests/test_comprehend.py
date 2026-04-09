"""Tests for aws_util.comprehend module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.comprehend as comprehend_mod
from aws_util.comprehend import (
    SentimentResult,
    EntityResult,
    KeyPhrase,
    LanguageResult,
    PiiEntity,
    detect_sentiment,
    detect_entities,
    detect_key_phrases,
    detect_dominant_language,
    detect_pii_entities,
    analyze_text,
    redact_pii,
    batch_detect_sentiment,
    batch_detect_dominant_language,
    batch_detect_entities,
    batch_detect_key_phrases,
    batch_detect_syntax,
    batch_detect_targeted_sentiment,
    classify_document,
    contains_pii_entities,
    create_dataset,
    create_document_classifier,
    create_endpoint,
    create_entity_recognizer,
    create_flywheel,
    delete_document_classifier,
    delete_endpoint,
    delete_entity_recognizer,
    delete_flywheel,
    delete_resource_policy,
    describe_dataset,
    describe_document_classification_job,
    describe_document_classifier,
    describe_dominant_language_detection_job,
    describe_endpoint,
    describe_entities_detection_job,
    describe_entity_recognizer,
    describe_events_detection_job,
    describe_flywheel,
    describe_flywheel_iteration,
    describe_key_phrases_detection_job,
    describe_pii_entities_detection_job,
    describe_resource_policy,
    describe_sentiment_detection_job,
    describe_targeted_sentiment_detection_job,
    describe_topics_detection_job,
    detect_syntax,
    detect_targeted_sentiment,
    detect_toxic_content,
    import_model,
    list_datasets,
    list_document_classification_jobs,
    list_document_classifier_summaries,
    list_document_classifiers,
    list_dominant_language_detection_jobs,
    list_endpoints,
    list_entities_detection_jobs,
    list_entity_recognizer_summaries,
    list_entity_recognizers,
    list_events_detection_jobs,
    list_flywheel_iteration_history,
    list_flywheels,
    list_key_phrases_detection_jobs,
    list_pii_entities_detection_jobs,
    list_sentiment_detection_jobs,
    list_tags_for_resource,
    list_targeted_sentiment_detection_jobs,
    list_topics_detection_jobs,
    put_resource_policy,
    start_document_classification_job,
    start_dominant_language_detection_job,
    start_entities_detection_job,
    start_events_detection_job,
    start_flywheel_iteration,
    start_key_phrases_detection_job,
    start_pii_entities_detection_job,
    start_sentiment_detection_job,
    start_targeted_sentiment_detection_job,
    start_topics_detection_job,
    stop_dominant_language_detection_job,
    stop_entities_detection_job,
    stop_events_detection_job,
    stop_key_phrases_detection_job,
    stop_pii_entities_detection_job,
    stop_sentiment_detection_job,
    stop_targeted_sentiment_detection_job,
    stop_training_document_classifier,
    stop_training_entity_recognizer,
    tag_resource,
    untag_resource,
    update_endpoint,
    update_flywheel,
)

REGION = "us-east-1"
TEXT = "I love AWS. Jeff Bezos founded Amazon in Seattle."


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_sentiment_result_model():
    result = SentimentResult(sentiment="POSITIVE", positive=0.95)
    assert result.sentiment == "POSITIVE"
    assert result.negative == 0.0


def test_entity_result_model():
    ent = EntityResult(
        text="Jeff Bezos", entity_type="PERSON", score=0.99, begin_offset=10, end_offset=20
    )
    assert ent.entity_type == "PERSON"


def test_key_phrase_model():
    kp = KeyPhrase(text="AWS", score=0.95, begin_offset=5, end_offset=8)
    assert kp.text == "AWS"


def test_language_result_model():
    lang = LanguageResult(language_code="en", score=0.99)
    assert lang.language_code == "en"


def test_pii_entity_model():
    pii = PiiEntity(pii_type="EMAIL", score=0.99, begin_offset=0, end_offset=20)
    assert pii.pii_type == "EMAIL"


# ---------------------------------------------------------------------------
# detect_sentiment
# ---------------------------------------------------------------------------

def test_detect_sentiment_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_sentiment.return_value = {
        "Sentiment": "POSITIVE",
        "SentimentScore": {"Positive": 0.95, "Negative": 0.02, "Neutral": 0.02, "Mixed": 0.01},
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_sentiment(TEXT, region_name=REGION)
    assert isinstance(result, SentimentResult)
    assert result.sentiment == "POSITIVE"
    assert result.positive == 0.95


def test_detect_sentiment_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_sentiment.side_effect = ClientError(
        {"Error": {"Code": "TextSizeLimitExceededException", "Message": "too large"}},
        "DetectSentiment",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_sentiment failed"):
        detect_sentiment("x" * 10000, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_entities
# ---------------------------------------------------------------------------

def test_detect_entities_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_entities.return_value = {
        "Entities": [
            {"Text": "Jeff Bezos", "Type": "PERSON", "Score": 0.99, "BeginOffset": 10, "EndOffset": 20},
            {"Text": "Amazon", "Type": "ORGANIZATION", "Score": 0.98, "BeginOffset": 30, "EndOffset": 36},
        ]
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_entities(TEXT, region_name=REGION)
    assert len(result) == 2
    assert all(isinstance(e, EntityResult) for e in result)
    assert result[0].text == "Jeff Bezos"


def test_detect_entities_empty(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_entities.return_value = {"Entities": []}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_entities("blah", region_name=REGION)
    assert result == []


def test_detect_entities_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_entities.side_effect = ClientError(
        {"Error": {"Code": "UnsupportedLanguageException", "Message": "unsupported"}},
        "DetectEntities",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_entities failed"):
        detect_entities(TEXT, language_code="xx", region_name=REGION)


# ---------------------------------------------------------------------------
# detect_key_phrases
# ---------------------------------------------------------------------------

def test_detect_key_phrases_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_key_phrases.return_value = {
        "KeyPhrases": [
            {"Text": "AWS", "Score": 0.95, "BeginOffset": 7, "EndOffset": 10},
        ]
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_key_phrases(TEXT, region_name=REGION)
    assert len(result) == 1
    assert result[0].text == "AWS"


def test_detect_key_phrases_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_key_phrases.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "bad request"}},
        "DetectKeyPhrases",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_key_phrases failed"):
        detect_key_phrases(TEXT, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_dominant_language
# ---------------------------------------------------------------------------

def test_detect_dominant_language_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_dominant_language.return_value = {
        "Languages": [
            {"LanguageCode": "en", "Score": 0.99},
            {"LanguageCode": "es", "Score": 0.01},
        ]
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_dominant_language(TEXT, region_name=REGION)
    assert isinstance(result, LanguageResult)
    assert result.language_code == "en"


def test_detect_dominant_language_no_language(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_dominant_language.return_value = {"Languages": []}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(ValueError, match="could not detect any language"):
        detect_dominant_language("", region_name=REGION)


def test_detect_dominant_language_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_dominant_language.side_effect = ClientError(
        {"Error": {"Code": "InternalServerException", "Message": "error"}},
        "DetectDominantLanguage",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_dominant_language failed"):
        detect_dominant_language(TEXT, region_name=REGION)


# ---------------------------------------------------------------------------
# detect_pii_entities
# ---------------------------------------------------------------------------

def test_detect_pii_entities_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_pii_entities.return_value = {
        "Entities": [
            {"Type": "EMAIL", "Score": 0.99, "BeginOffset": 0, "EndOffset": 20},
        ]
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_pii_entities("test@example.com", region_name=REGION)
    assert len(result) == 1
    assert result[0].pii_type == "EMAIL"


def test_detect_pii_entities_empty(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_pii_entities.return_value = {"Entities": []}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = detect_pii_entities("no pii here", region_name=REGION)
    assert result == []


def test_detect_pii_entities_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_pii_entities.side_effect = ClientError(
        {"Error": {"Code": "TextSizeLimitExceededException", "Message": "too large"}},
        "DetectPiiEntities",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="detect_pii_entities failed"):
        detect_pii_entities("x" * 10000, region_name=REGION)


# ---------------------------------------------------------------------------
# analyze_text
# ---------------------------------------------------------------------------

def test_analyze_text_english(monkeypatch):
    def fake_sentiment(text, lang="en", region_name=None):
        return SentimentResult(sentiment="POSITIVE")

    def fake_entities(text, lang="en", region_name=None):
        return []

    def fake_key_phrases(text, lang="en", region_name=None):
        return []

    def fake_language(text, region_name=None):
        return LanguageResult(language_code="en", score=0.99)

    def fake_pii(text, lang="en", region_name=None):
        return []

    monkeypatch.setattr(comprehend_mod, "detect_sentiment", fake_sentiment)
    monkeypatch.setattr(comprehend_mod, "detect_entities", fake_entities)
    monkeypatch.setattr(comprehend_mod, "detect_key_phrases", fake_key_phrases)
    monkeypatch.setattr(comprehend_mod, "detect_dominant_language", fake_language)
    monkeypatch.setattr(comprehend_mod, "detect_pii_entities", fake_pii)

    result = analyze_text(TEXT, region_name=REGION)
    assert "sentiment" in result
    assert "entities" in result
    assert "key_phrases" in result
    assert "language" in result
    assert "pii_entities" in result


def test_analyze_text_non_english(monkeypatch):
    def fake_sentiment(text, lang="es", region_name=None):
        return SentimentResult(sentiment="NEUTRAL")

    def fake_entities(text, lang="es", region_name=None):
        return []

    def fake_key_phrases(text, lang="es", region_name=None):
        return []

    def fake_language(text, region_name=None):
        return LanguageResult(language_code="es", score=0.98)

    monkeypatch.setattr(comprehend_mod, "detect_sentiment", fake_sentiment)
    monkeypatch.setattr(comprehend_mod, "detect_entities", fake_entities)
    monkeypatch.setattr(comprehend_mod, "detect_key_phrases", fake_key_phrases)
    monkeypatch.setattr(comprehend_mod, "detect_dominant_language", fake_language)

    result = analyze_text("Hola mundo", language_code="es", region_name=REGION)
    # For non-English, pii_entities should be empty list
    assert result["pii_entities"] == []


# ---------------------------------------------------------------------------
# redact_pii
# ---------------------------------------------------------------------------

def test_redact_pii_success(monkeypatch):
    monkeypatch.setattr(
        comprehend_mod,
        "detect_pii_entities",
        lambda text, lang="en", region_name=None: [
            PiiEntity(pii_type="EMAIL", score=0.99, begin_offset=6, end_offset=22)
        ],
    )
    result = redact_pii("Email: user@example.com here", region_name=REGION)
    assert "[REDACTED]" in result
    assert "user@example.com" not in result


def test_redact_pii_no_entities(monkeypatch):
    monkeypatch.setattr(
        comprehend_mod,
        "detect_pii_entities",
        lambda text, lang="en", region_name=None: [],
    )
    text = "No PII here"
    result = redact_pii(text, region_name=REGION)
    assert result == text


def test_redact_pii_custom_replacement(monkeypatch):
    monkeypatch.setattr(
        comprehend_mod,
        "detect_pii_entities",
        lambda text, lang="en", region_name=None: [
            PiiEntity(pii_type="EMAIL", score=0.99, begin_offset=0, end_offset=16)
        ],
    )
    result = redact_pii("user@example.com", replacement="***", region_name=REGION)
    assert result == "***"


# ---------------------------------------------------------------------------
# batch_detect_sentiment
# ---------------------------------------------------------------------------

def test_batch_detect_sentiment_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_sentiment.return_value = {
        "ResultList": [
            {
                "Index": 0,
                "Sentiment": "POSITIVE",
                "SentimentScore": {"Positive": 0.9, "Negative": 0.05, "Neutral": 0.03, "Mixed": 0.02},
            },
            {
                "Index": 1,
                "Sentiment": "NEGATIVE",
                "SentimentScore": {"Positive": 0.1, "Negative": 0.85, "Neutral": 0.03, "Mixed": 0.02},
            },
        ],
        "ErrorList": [],
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    result = batch_detect_sentiment(["Great!", "Terrible!"], region_name=REGION)
    assert len(result) == 2
    assert result[0].sentiment == "POSITIVE"
    assert result[1].sentiment == "NEGATIVE"


def test_batch_detect_sentiment_too_many_raises():
    with pytest.raises(ValueError, match="at most 25"):
        batch_detect_sentiment(["text"] * 26, region_name=REGION)


def test_batch_detect_sentiment_with_errors(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_sentiment.return_value = {
        "ResultList": [],
        "ErrorList": [{"Index": 0, "ErrorCode": "INTERNAL_SERVER_ERROR", "ErrorMessage": "error"}],
    }
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="had errors"):
        batch_detect_sentiment(["text"], region_name=REGION)


def test_batch_detect_sentiment_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_sentiment.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "bad request"}},
        "BatchDetectSentiment",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="batch_detect_sentiment failed"):
        batch_detect_sentiment(["text"], region_name=REGION)


def test_batch_detect_dominant_language(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_dominant_language.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    batch_detect_dominant_language([], region_name=REGION)
    mock_client.batch_detect_dominant_language.assert_called_once()


def test_batch_detect_dominant_language_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_dominant_language.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_detect_dominant_language",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch detect dominant language"):
        batch_detect_dominant_language([], region_name=REGION)


def test_batch_detect_entities(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_entities.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    batch_detect_entities([], "test-language_code", region_name=REGION)
    mock_client.batch_detect_entities.assert_called_once()


def test_batch_detect_entities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_entities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_detect_entities",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch detect entities"):
        batch_detect_entities([], "test-language_code", region_name=REGION)


def test_batch_detect_key_phrases(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_key_phrases.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    batch_detect_key_phrases([], "test-language_code", region_name=REGION)
    mock_client.batch_detect_key_phrases.assert_called_once()


def test_batch_detect_key_phrases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_key_phrases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_detect_key_phrases",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch detect key phrases"):
        batch_detect_key_phrases([], "test-language_code", region_name=REGION)


def test_batch_detect_syntax(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_syntax.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    batch_detect_syntax([], "test-language_code", region_name=REGION)
    mock_client.batch_detect_syntax.assert_called_once()


def test_batch_detect_syntax_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_syntax.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_detect_syntax",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch detect syntax"):
        batch_detect_syntax([], "test-language_code", region_name=REGION)


def test_batch_detect_targeted_sentiment(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_targeted_sentiment.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    batch_detect_targeted_sentiment([], "test-language_code", region_name=REGION)
    mock_client.batch_detect_targeted_sentiment.assert_called_once()


def test_batch_detect_targeted_sentiment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_detect_targeted_sentiment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_detect_targeted_sentiment",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch detect targeted sentiment"):
        batch_detect_targeted_sentiment([], "test-language_code", region_name=REGION)


def test_classify_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.classify_document.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    classify_document("test-endpoint_arn", region_name=REGION)
    mock_client.classify_document.assert_called_once()


def test_classify_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.classify_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "classify_document",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to classify document"):
        classify_document("test-endpoint_arn", region_name=REGION)


def test_contains_pii_entities(monkeypatch):
    mock_client = MagicMock()
    mock_client.contains_pii_entities.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    contains_pii_entities("test-text", "test-language_code", region_name=REGION)
    mock_client.contains_pii_entities.assert_called_once()


def test_contains_pii_entities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.contains_pii_entities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "contains_pii_entities",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to contains pii entities"):
        contains_pii_entities("test-text", "test-language_code", region_name=REGION)


def test_create_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    create_dataset("test-flywheel_arn", "test-dataset_name", {}, region_name=REGION)
    mock_client.create_dataset.assert_called_once()


def test_create_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dataset",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dataset"):
        create_dataset("test-flywheel_arn", "test-dataset_name", {}, region_name=REGION)


def test_create_document_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_document_classifier.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", region_name=REGION)
    mock_client.create_document_classifier.assert_called_once()


def test_create_document_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_document_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_document_classifier",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create document classifier"):
        create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", region_name=REGION)


def test_create_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    create_endpoint("test-endpoint_name", 1, region_name=REGION)
    mock_client.create_endpoint.assert_called_once()


def test_create_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_endpoint",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create endpoint"):
        create_endpoint("test-endpoint_name", 1, region_name=REGION)


def test_create_entity_recognizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_entity_recognizer.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", region_name=REGION)
    mock_client.create_entity_recognizer.assert_called_once()


def test_create_entity_recognizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_entity_recognizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_entity_recognizer",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create entity recognizer"):
        create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", region_name=REGION)


def test_create_flywheel(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flywheel.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", region_name=REGION)
    mock_client.create_flywheel.assert_called_once()


def test_create_flywheel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flywheel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_flywheel",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create flywheel"):
        create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", region_name=REGION)


def test_delete_document_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_document_classifier.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    delete_document_classifier("test-document_classifier_arn", region_name=REGION)
    mock_client.delete_document_classifier.assert_called_once()


def test_delete_document_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_document_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_document_classifier",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete document classifier"):
        delete_document_classifier("test-document_classifier_arn", region_name=REGION)


def test_delete_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    delete_endpoint("test-endpoint_arn", region_name=REGION)
    mock_client.delete_endpoint.assert_called_once()


def test_delete_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_endpoint",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete endpoint"):
        delete_endpoint("test-endpoint_arn", region_name=REGION)


def test_delete_entity_recognizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_entity_recognizer.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    delete_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)
    mock_client.delete_entity_recognizer.assert_called_once()


def test_delete_entity_recognizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_entity_recognizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_entity_recognizer",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete entity recognizer"):
        delete_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)


def test_delete_flywheel(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flywheel.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    delete_flywheel("test-flywheel_arn", region_name=REGION)
    mock_client.delete_flywheel.assert_called_once()


def test_delete_flywheel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flywheel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_flywheel",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete flywheel"):
        delete_flywheel("test-flywheel_arn", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_describe_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_dataset("test-dataset_arn", region_name=REGION)
    mock_client.describe_dataset.assert_called_once()


def test_describe_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        describe_dataset("test-dataset_arn", region_name=REGION)


def test_describe_document_classification_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_classification_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_document_classification_job("test-job_id", region_name=REGION)
    mock_client.describe_document_classification_job.assert_called_once()


def test_describe_document_classification_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_classification_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_document_classification_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe document classification job"):
        describe_document_classification_job("test-job_id", region_name=REGION)


def test_describe_document_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_classifier.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_document_classifier("test-document_classifier_arn", region_name=REGION)
    mock_client.describe_document_classifier.assert_called_once()


def test_describe_document_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_document_classifier",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe document classifier"):
        describe_document_classifier("test-document_classifier_arn", region_name=REGION)


def test_describe_dominant_language_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dominant_language_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_dominant_language_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_dominant_language_detection_job.assert_called_once()


def test_describe_dominant_language_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dominant_language_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dominant_language_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dominant language detection job"):
        describe_dominant_language_detection_job("test-job_id", region_name=REGION)


def test_describe_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_endpoint("test-endpoint_arn", region_name=REGION)
    mock_client.describe_endpoint.assert_called_once()


def test_describe_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoint"):
        describe_endpoint("test-endpoint_arn", region_name=REGION)


def test_describe_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_entities_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_entities_detection_job.assert_called_once()


def test_describe_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe entities detection job"):
        describe_entities_detection_job("test-job_id", region_name=REGION)


def test_describe_entity_recognizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entity_recognizer.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)
    mock_client.describe_entity_recognizer.assert_called_once()


def test_describe_entity_recognizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entity_recognizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_entity_recognizer",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe entity recognizer"):
        describe_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)


def test_describe_events_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_events_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_events_detection_job.assert_called_once()


def test_describe_events_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe events detection job"):
        describe_events_detection_job("test-job_id", region_name=REGION)


def test_describe_flywheel(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flywheel.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_flywheel("test-flywheel_arn", region_name=REGION)
    mock_client.describe_flywheel.assert_called_once()


def test_describe_flywheel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flywheel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_flywheel",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe flywheel"):
        describe_flywheel("test-flywheel_arn", region_name=REGION)


def test_describe_flywheel_iteration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flywheel_iteration.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_flywheel_iteration("test-flywheel_arn", "test-flywheel_iteration_id", region_name=REGION)
    mock_client.describe_flywheel_iteration.assert_called_once()


def test_describe_flywheel_iteration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flywheel_iteration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_flywheel_iteration",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe flywheel iteration"):
        describe_flywheel_iteration("test-flywheel_arn", "test-flywheel_iteration_id", region_name=REGION)


def test_describe_key_phrases_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_phrases_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_key_phrases_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_key_phrases_detection_job.assert_called_once()


def test_describe_key_phrases_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_phrases_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_key_phrases_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe key phrases detection job"):
        describe_key_phrases_detection_job("test-job_id", region_name=REGION)


def test_describe_pii_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pii_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_pii_entities_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_pii_entities_detection_job.assert_called_once()


def test_describe_pii_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pii_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pii_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe pii entities detection job"):
        describe_pii_entities_detection_job("test-job_id", region_name=REGION)


def test_describe_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_policy.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.describe_resource_policy.assert_called_once()


def test_describe_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resource_policy",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe resource policy"):
        describe_resource_policy("test-resource_arn", region_name=REGION)


def test_describe_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_sentiment_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_sentiment_detection_job.assert_called_once()


def test_describe_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe sentiment detection job"):
        describe_sentiment_detection_job("test-job_id", region_name=REGION)


def test_describe_targeted_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_targeted_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_targeted_sentiment_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_targeted_sentiment_detection_job.assert_called_once()


def test_describe_targeted_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_targeted_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_targeted_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe targeted sentiment detection job"):
        describe_targeted_sentiment_detection_job("test-job_id", region_name=REGION)


def test_describe_topics_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topics_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    describe_topics_detection_job("test-job_id", region_name=REGION)
    mock_client.describe_topics_detection_job.assert_called_once()


def test_describe_topics_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topics_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_topics_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe topics detection job"):
        describe_topics_detection_job("test-job_id", region_name=REGION)


def test_detect_syntax(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_syntax.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    detect_syntax("test-text", "test-language_code", region_name=REGION)
    mock_client.detect_syntax.assert_called_once()


def test_detect_syntax_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_syntax.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_syntax",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect syntax"):
        detect_syntax("test-text", "test-language_code", region_name=REGION)


def test_detect_targeted_sentiment(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_targeted_sentiment.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    detect_targeted_sentiment("test-text", "test-language_code", region_name=REGION)
    mock_client.detect_targeted_sentiment.assert_called_once()


def test_detect_targeted_sentiment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_targeted_sentiment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_targeted_sentiment",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect targeted sentiment"):
        detect_targeted_sentiment("test-text", "test-language_code", region_name=REGION)


def test_detect_toxic_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_toxic_content.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    detect_toxic_content([], "test-language_code", region_name=REGION)
    mock_client.detect_toxic_content.assert_called_once()


def test_detect_toxic_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_toxic_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_toxic_content",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect toxic content"):
        detect_toxic_content([], "test-language_code", region_name=REGION)


def test_import_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_model.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    import_model("test-source_model_arn", region_name=REGION)
    mock_client.import_model.assert_called_once()


def test_import_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_model",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import model"):
        import_model("test-source_model_arn", region_name=REGION)


def test_list_datasets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_datasets.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_datasets(region_name=REGION)
    mock_client.list_datasets.assert_called_once()


def test_list_datasets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_datasets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_datasets",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list datasets"):
        list_datasets(region_name=REGION)


def test_list_document_classification_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classification_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_document_classification_jobs(region_name=REGION)
    mock_client.list_document_classification_jobs.assert_called_once()


def test_list_document_classification_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classification_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_document_classification_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list document classification jobs"):
        list_document_classification_jobs(region_name=REGION)


def test_list_document_classifier_summaries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classifier_summaries.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_document_classifier_summaries(region_name=REGION)
    mock_client.list_document_classifier_summaries.assert_called_once()


def test_list_document_classifier_summaries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classifier_summaries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_document_classifier_summaries",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list document classifier summaries"):
        list_document_classifier_summaries(region_name=REGION)


def test_list_document_classifiers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classifiers.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_document_classifiers(region_name=REGION)
    mock_client.list_document_classifiers.assert_called_once()


def test_list_document_classifiers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_classifiers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_document_classifiers",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list document classifiers"):
        list_document_classifiers(region_name=REGION)


def test_list_dominant_language_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dominant_language_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_dominant_language_detection_jobs(region_name=REGION)
    mock_client.list_dominant_language_detection_jobs.assert_called_once()


def test_list_dominant_language_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dominant_language_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dominant_language_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dominant language detection jobs"):
        list_dominant_language_detection_jobs(region_name=REGION)


def test_list_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_endpoints(region_name=REGION)
    mock_client.list_endpoints.assert_called_once()


def test_list_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_endpoints",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list endpoints"):
        list_endpoints(region_name=REGION)


def test_list_entities_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_entities_detection_jobs(region_name=REGION)
    mock_client.list_entities_detection_jobs.assert_called_once()


def test_list_entities_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_entities_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list entities detection jobs"):
        list_entities_detection_jobs(region_name=REGION)


def test_list_entity_recognizer_summaries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entity_recognizer_summaries.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_entity_recognizer_summaries(region_name=REGION)
    mock_client.list_entity_recognizer_summaries.assert_called_once()


def test_list_entity_recognizer_summaries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entity_recognizer_summaries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_entity_recognizer_summaries",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list entity recognizer summaries"):
        list_entity_recognizer_summaries(region_name=REGION)


def test_list_entity_recognizers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entity_recognizers.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_entity_recognizers(region_name=REGION)
    mock_client.list_entity_recognizers.assert_called_once()


def test_list_entity_recognizers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entity_recognizers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_entity_recognizers",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list entity recognizers"):
        list_entity_recognizers(region_name=REGION)


def test_list_events_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_events_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_events_detection_jobs(region_name=REGION)
    mock_client.list_events_detection_jobs.assert_called_once()


def test_list_events_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_events_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_events_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list events detection jobs"):
        list_events_detection_jobs(region_name=REGION)


def test_list_flywheel_iteration_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flywheel_iteration_history.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_flywheel_iteration_history("test-flywheel_arn", region_name=REGION)
    mock_client.list_flywheel_iteration_history.assert_called_once()


def test_list_flywheel_iteration_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flywheel_iteration_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flywheel_iteration_history",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flywheel iteration history"):
        list_flywheel_iteration_history("test-flywheel_arn", region_name=REGION)


def test_list_flywheels(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flywheels.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_flywheels(region_name=REGION)
    mock_client.list_flywheels.assert_called_once()


def test_list_flywheels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flywheels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flywheels",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flywheels"):
        list_flywheels(region_name=REGION)


def test_list_key_phrases_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_phrases_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_key_phrases_detection_jobs(region_name=REGION)
    mock_client.list_key_phrases_detection_jobs.assert_called_once()


def test_list_key_phrases_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_key_phrases_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_key_phrases_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list key phrases detection jobs"):
        list_key_phrases_detection_jobs(region_name=REGION)


def test_list_pii_entities_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_pii_entities_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_pii_entities_detection_jobs(region_name=REGION)
    mock_client.list_pii_entities_detection_jobs.assert_called_once()


def test_list_pii_entities_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_pii_entities_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_pii_entities_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list pii entities detection jobs"):
        list_pii_entities_detection_jobs(region_name=REGION)


def test_list_sentiment_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sentiment_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_sentiment_detection_jobs(region_name=REGION)
    mock_client.list_sentiment_detection_jobs.assert_called_once()


def test_list_sentiment_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sentiment_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sentiment_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list sentiment detection jobs"):
        list_sentiment_detection_jobs(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_targeted_sentiment_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targeted_sentiment_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_targeted_sentiment_detection_jobs(region_name=REGION)
    mock_client.list_targeted_sentiment_detection_jobs.assert_called_once()


def test_list_targeted_sentiment_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targeted_sentiment_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_targeted_sentiment_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list targeted sentiment detection jobs"):
        list_targeted_sentiment_detection_jobs(region_name=REGION)


def test_list_topics_detection_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics_detection_jobs.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    list_topics_detection_jobs(region_name=REGION)
    mock_client.list_topics_detection_jobs.assert_called_once()


def test_list_topics_detection_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics_detection_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topics_detection_jobs",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list topics detection jobs"):
        list_topics_detection_jobs(region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-resource_policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-resource_policy", region_name=REGION)


def test_start_document_classification_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_document_classification_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_document_classification_job({}, {}, "test-data_access_role_arn", region_name=REGION)
    mock_client.start_document_classification_job.assert_called_once()


def test_start_document_classification_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_document_classification_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_document_classification_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start document classification job"):
        start_document_classification_job({}, {}, "test-data_access_role_arn", region_name=REGION)


def test_start_dominant_language_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dominant_language_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", region_name=REGION)
    mock_client.start_dominant_language_detection_job.assert_called_once()


def test_start_dominant_language_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dominant_language_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_dominant_language_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start dominant language detection job"):
        start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", region_name=REGION)


def test_start_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)
    mock_client.start_entities_detection_job.assert_called_once()


def test_start_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start entities detection job"):
        start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)


def test_start_events_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_events_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", [], region_name=REGION)
    mock_client.start_events_detection_job.assert_called_once()


def test_start_events_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_events_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_events_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start events detection job"):
        start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", [], region_name=REGION)


def test_start_flywheel_iteration(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_flywheel_iteration.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_flywheel_iteration("test-flywheel_arn", region_name=REGION)
    mock_client.start_flywheel_iteration.assert_called_once()


def test_start_flywheel_iteration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_flywheel_iteration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_flywheel_iteration",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start flywheel iteration"):
        start_flywheel_iteration("test-flywheel_arn", region_name=REGION)


def test_start_key_phrases_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_key_phrases_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)
    mock_client.start_key_phrases_detection_job.assert_called_once()


def test_start_key_phrases_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_key_phrases_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_key_phrases_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start key phrases detection job"):
        start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)


def test_start_pii_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_pii_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", region_name=REGION)
    mock_client.start_pii_entities_detection_job.assert_called_once()


def test_start_pii_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_pii_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_pii_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start pii entities detection job"):
        start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", region_name=REGION)


def test_start_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)
    mock_client.start_sentiment_detection_job.assert_called_once()


def test_start_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start sentiment detection job"):
        start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)


def test_start_targeted_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_targeted_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)
    mock_client.start_targeted_sentiment_detection_job.assert_called_once()


def test_start_targeted_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_targeted_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_targeted_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start targeted sentiment detection job"):
        start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", region_name=REGION)


def test_start_topics_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_topics_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    start_topics_detection_job({}, {}, "test-data_access_role_arn", region_name=REGION)
    mock_client.start_topics_detection_job.assert_called_once()


def test_start_topics_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_topics_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_topics_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start topics detection job"):
        start_topics_detection_job({}, {}, "test-data_access_role_arn", region_name=REGION)


def test_stop_dominant_language_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_dominant_language_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_dominant_language_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_dominant_language_detection_job.assert_called_once()


def test_stop_dominant_language_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_dominant_language_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_dominant_language_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop dominant language detection job"):
        stop_dominant_language_detection_job("test-job_id", region_name=REGION)


def test_stop_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_entities_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_entities_detection_job.assert_called_once()


def test_stop_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop entities detection job"):
        stop_entities_detection_job("test-job_id", region_name=REGION)


def test_stop_events_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_events_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_events_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_events_detection_job.assert_called_once()


def test_stop_events_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_events_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_events_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop events detection job"):
        stop_events_detection_job("test-job_id", region_name=REGION)


def test_stop_key_phrases_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_key_phrases_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_key_phrases_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_key_phrases_detection_job.assert_called_once()


def test_stop_key_phrases_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_key_phrases_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_key_phrases_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop key phrases detection job"):
        stop_key_phrases_detection_job("test-job_id", region_name=REGION)


def test_stop_pii_entities_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_pii_entities_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_pii_entities_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_pii_entities_detection_job.assert_called_once()


def test_stop_pii_entities_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_pii_entities_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_pii_entities_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop pii entities detection job"):
        stop_pii_entities_detection_job("test-job_id", region_name=REGION)


def test_stop_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_sentiment_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_sentiment_detection_job.assert_called_once()


def test_stop_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop sentiment detection job"):
        stop_sentiment_detection_job("test-job_id", region_name=REGION)


def test_stop_targeted_sentiment_detection_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_targeted_sentiment_detection_job.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_targeted_sentiment_detection_job("test-job_id", region_name=REGION)
    mock_client.stop_targeted_sentiment_detection_job.assert_called_once()


def test_stop_targeted_sentiment_detection_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_targeted_sentiment_detection_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_targeted_sentiment_detection_job",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop targeted sentiment detection job"):
        stop_targeted_sentiment_detection_job("test-job_id", region_name=REGION)


def test_stop_training_document_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_training_document_classifier.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_training_document_classifier("test-document_classifier_arn", region_name=REGION)
    mock_client.stop_training_document_classifier.assert_called_once()


def test_stop_training_document_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_training_document_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_training_document_classifier",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop training document classifier"):
        stop_training_document_classifier("test-document_classifier_arn", region_name=REGION)


def test_stop_training_entity_recognizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_training_entity_recognizer.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    stop_training_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)
    mock_client.stop_training_entity_recognizer.assert_called_once()


def test_stop_training_entity_recognizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_training_entity_recognizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_training_entity_recognizer",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop training entity recognizer"):
        stop_training_entity_recognizer("test-entity_recognizer_arn", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    update_endpoint("test-endpoint_arn", region_name=REGION)
    mock_client.update_endpoint.assert_called_once()


def test_update_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_endpoint",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update endpoint"):
        update_endpoint("test-endpoint_arn", region_name=REGION)


def test_update_flywheel(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flywheel.return_value = {}
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    update_flywheel("test-flywheel_arn", region_name=REGION)
    mock_client.update_flywheel.assert_called_once()


def test_update_flywheel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flywheel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_flywheel",
    )
    monkeypatch.setattr(comprehend_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update flywheel"):
        update_flywheel("test-flywheel_arn", region_name=REGION)


def test_classify_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import classify_document
    mock_client = MagicMock()
    mock_client.classify_document.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    classify_document("test-endpoint_arn", text="test-text", bytes="test-bytes", document_reader_config={}, region_name="us-east-1")
    mock_client.classify_document.assert_called_once()

def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import create_dataset
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    create_dataset("test-flywheel_arn", "test-dataset_name", {}, dataset_type="test-dataset_type", description="test-description", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dataset.assert_called_once()

def test_create_document_classifier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import create_document_classifier
    mock_client = MagicMock()
    mock_client.create_document_classifier.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", version_name="test-version_name", tags=[{"Key": "k", "Value": "v"}], output_data_config={}, client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, mode="test-mode", model_kms_key_id="test-model_kms_key_id", model_policy="{}", region_name="us-east-1")
    mock_client.create_document_classifier.assert_called_once()

def test_create_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import create_endpoint
    mock_client = MagicMock()
    mock_client.create_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    create_endpoint("test-endpoint_name", "test-desired_inference_units", model_arn="test-model_arn", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], data_access_role_arn="test-data_access_role_arn", flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.create_endpoint.assert_called_once()

def test_create_entity_recognizer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import create_entity_recognizer
    mock_client = MagicMock()
    mock_client.create_entity_recognizer.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", version_name="test-version_name", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, model_kms_key_id="test-model_kms_key_id", model_policy="{}", region_name="us-east-1")
    mock_client.create_entity_recognizer.assert_called_once()

def test_create_flywheel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import create_flywheel
    mock_client = MagicMock()
    mock_client.create_flywheel.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", active_model_arn="test-active_model_arn", task_config={}, model_type="test-model_type", data_security_config={}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_flywheel.assert_called_once()

def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import delete_resource_policy
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.delete_resource_policy.assert_called_once()

def test_import_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import import_model
    mock_client = MagicMock()
    mock_client.import_model.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    import_model("test-source_model_arn", model_name="test-model_name", version_name="test-version_name", model_kms_key_id="test-model_kms_key_id", data_access_role_arn="test-data_access_role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_model.assert_called_once()

def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_datasets
    mock_client = MagicMock()
    mock_client.list_datasets.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_datasets(flywheel_arn="test-flywheel_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_datasets.assert_called_once()

def test_list_document_classification_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_document_classification_jobs
    mock_client = MagicMock()
    mock_client.list_document_classification_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_document_classification_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_document_classification_jobs.assert_called_once()

def test_list_document_classifier_summaries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_document_classifier_summaries
    mock_client = MagicMock()
    mock_client.list_document_classifier_summaries.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_document_classifier_summaries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_document_classifier_summaries.assert_called_once()

def test_list_document_classifiers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_document_classifiers
    mock_client = MagicMock()
    mock_client.list_document_classifiers.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_document_classifiers(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_document_classifiers.assert_called_once()

def test_list_dominant_language_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_dominant_language_detection_jobs
    mock_client = MagicMock()
    mock_client.list_dominant_language_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_dominant_language_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dominant_language_detection_jobs.assert_called_once()

def test_list_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_endpoints
    mock_client = MagicMock()
    mock_client.list_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_endpoints(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_endpoints.assert_called_once()

def test_list_entities_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_entities_detection_jobs
    mock_client = MagicMock()
    mock_client.list_entities_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_entities_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_entities_detection_jobs.assert_called_once()

def test_list_entity_recognizer_summaries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_entity_recognizer_summaries
    mock_client = MagicMock()
    mock_client.list_entity_recognizer_summaries.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_entity_recognizer_summaries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_entity_recognizer_summaries.assert_called_once()

def test_list_entity_recognizers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_entity_recognizers
    mock_client = MagicMock()
    mock_client.list_entity_recognizers.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_entity_recognizers(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_entity_recognizers.assert_called_once()

def test_list_events_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_events_detection_jobs
    mock_client = MagicMock()
    mock_client.list_events_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_events_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_events_detection_jobs.assert_called_once()

def test_list_flywheel_iteration_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_flywheel_iteration_history
    mock_client = MagicMock()
    mock_client.list_flywheel_iteration_history.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_flywheel_iteration_history("test-flywheel_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_flywheel_iteration_history.assert_called_once()

def test_list_flywheels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_flywheels
    mock_client = MagicMock()
    mock_client.list_flywheels.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_flywheels(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_flywheels.assert_called_once()

def test_list_key_phrases_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_key_phrases_detection_jobs
    mock_client = MagicMock()
    mock_client.list_key_phrases_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_key_phrases_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_key_phrases_detection_jobs.assert_called_once()

def test_list_pii_entities_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_pii_entities_detection_jobs
    mock_client = MagicMock()
    mock_client.list_pii_entities_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_pii_entities_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_pii_entities_detection_jobs.assert_called_once()

def test_list_sentiment_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_sentiment_detection_jobs
    mock_client = MagicMock()
    mock_client.list_sentiment_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_sentiment_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_sentiment_detection_jobs.assert_called_once()

def test_list_targeted_sentiment_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_targeted_sentiment_detection_jobs
    mock_client = MagicMock()
    mock_client.list_targeted_sentiment_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_targeted_sentiment_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_targeted_sentiment_detection_jobs.assert_called_once()

def test_list_topics_detection_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import list_topics_detection_jobs
    mock_client = MagicMock()
    mock_client.list_topics_detection_jobs.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    list_topics_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_topics_detection_jobs.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "{}", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_start_document_classification_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_document_classification_job
    mock_client = MagicMock()
    mock_client.start_document_classification_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_document_classification_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", document_classifier_arn="test-document_classifier_arn", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.start_document_classification_job.assert_called_once()

def test_start_dominant_language_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_dominant_language_detection_job
    mock_client = MagicMock()
    mock_client.start_dominant_language_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_dominant_language_detection_job.assert_called_once()

def test_start_entities_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_entities_detection_job
    mock_client = MagicMock()
    mock_client.start_entities_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", entity_recognizer_arn="test-entity_recognizer_arn", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.start_entities_detection_job.assert_called_once()

def test_start_events_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_events_detection_job
    mock_client = MagicMock()
    mock_client.start_events_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", "test-target_event_types", job_name="test-job_name", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_events_detection_job.assert_called_once()

def test_start_flywheel_iteration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_flywheel_iteration
    mock_client = MagicMock()
    mock_client.start_flywheel_iteration.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_flywheel_iteration("test-flywheel_arn", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_flywheel_iteration.assert_called_once()

def test_start_key_phrases_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_key_phrases_detection_job
    mock_client = MagicMock()
    mock_client.start_key_phrases_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_key_phrases_detection_job.assert_called_once()

def test_start_pii_entities_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_pii_entities_detection_job
    mock_client = MagicMock()
    mock_client.start_pii_entities_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", redaction_config={}, job_name="test-job_name", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_pii_entities_detection_job.assert_called_once()

def test_start_sentiment_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_sentiment_detection_job
    mock_client = MagicMock()
    mock_client.start_sentiment_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_sentiment_detection_job.assert_called_once()

def test_start_targeted_sentiment_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_targeted_sentiment_detection_job
    mock_client = MagicMock()
    mock_client.start_targeted_sentiment_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_targeted_sentiment_detection_job.assert_called_once()

def test_start_topics_detection_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import start_topics_detection_job
    mock_client = MagicMock()
    mock_client.start_topics_detection_job.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    start_topics_detection_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", number_of_topics="test-number_of_topics", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_topics_detection_job.assert_called_once()

def test_update_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import update_endpoint
    mock_client = MagicMock()
    mock_client.update_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    update_endpoint("test-endpoint_arn", desired_model_arn="test-desired_model_arn", desired_inference_units="test-desired_inference_units", desired_data_access_role_arn="test-desired_data_access_role_arn", flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.update_endpoint.assert_called_once()

def test_update_flywheel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.comprehend import update_flywheel
    mock_client = MagicMock()
    mock_client.update_flywheel.return_value = {}
    monkeypatch.setattr("aws_util.comprehend.get_client", lambda *a, **kw: mock_client)
    update_flywheel("test-flywheel_arn", active_model_arn="test-active_model_arn", data_access_role_arn="test-data_access_role_arn", data_security_config={}, region_name="us-east-1")
    mock_client.update_flywheel.assert_called_once()
