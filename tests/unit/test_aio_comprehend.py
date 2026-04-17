

"""Tests for aws_util.aio.comprehend — native async Comprehend utilities."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.comprehend as comp_mod
from aws_util.aio.comprehend import (

    EntityResult,
    KeyPhrase,
    LanguageResult,
    PiiEntity,
    SentimentResult,
    analyze_text,
    batch_detect_sentiment,
    detect_dominant_language,
    detect_entities,
    detect_key_phrases,
    detect_pii_entities,
    detect_sentiment,
    redact_pii,
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
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.comprehend.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# detect_sentiment
# ---------------------------------------------------------------------------


async def test_detect_sentiment_success(mock_client):
    mock_client.call.return_value = {
        "Sentiment": "POSITIVE",
        "SentimentScore": {
            "Positive": 0.95,
            "Negative": 0.01,
            "Neutral": 0.03,
            "Mixed": 0.01,
        },
    }
    result = await detect_sentiment("I love it")
    assert result.sentiment == "POSITIVE"
    assert result.positive == 0.95


async def test_detect_sentiment_missing_scores(mock_client):
    mock_client.call.return_value = {"Sentiment": "NEUTRAL"}
    result = await detect_sentiment("ok")
    assert result.positive == 0.0
    assert result.negative == 0.0


async def test_detect_sentiment_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="detect_sentiment failed"):
        await detect_sentiment("text")


# ---------------------------------------------------------------------------
# detect_entities
# ---------------------------------------------------------------------------


async def test_detect_entities_success(mock_client):
    mock_client.call.return_value = {
        "Entities": [
            {
                "Text": "AWS",
                "Type": "ORGANIZATION",
                "Score": 0.99,
                "BeginOffset": 0,
                "EndOffset": 3,
            }
        ]
    }
    result = await detect_entities("AWS is great")
    assert len(result) == 1
    assert result[0].text == "AWS"
    assert result[0].entity_type == "ORGANIZATION"


async def test_detect_entities_empty(mock_client):
    mock_client.call.return_value = {"Entities": []}
    result = await detect_entities("nothing")
    assert result == []


async def test_detect_entities_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="detect_entities failed"):
        await detect_entities("text")


# ---------------------------------------------------------------------------
# detect_key_phrases
# ---------------------------------------------------------------------------


async def test_detect_key_phrases_success(mock_client):
    mock_client.call.return_value = {
        "KeyPhrases": [
            {
                "Text": "great service",
                "Score": 0.98,
                "BeginOffset": 0,
                "EndOffset": 13,
            }
        ]
    }
    result = await detect_key_phrases("great service")
    assert len(result) == 1
    assert result[0].text == "great service"


async def test_detect_key_phrases_empty(mock_client):
    mock_client.call.return_value = {"KeyPhrases": []}
    result = await detect_key_phrases("x")
    assert result == []


async def test_detect_key_phrases_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="detect_key_phrases failed"):
        await detect_key_phrases("text")


# ---------------------------------------------------------------------------
# detect_dominant_language
# ---------------------------------------------------------------------------


async def test_detect_dominant_language_success(mock_client):
    mock_client.call.return_value = {
        "Languages": [
            {"LanguageCode": "en", "Score": 0.99},
            {"LanguageCode": "fr", "Score": 0.01},
        ]
    }
    result = await detect_dominant_language("hello world")
    assert result.language_code == "en"
    assert result.score == 0.99


async def test_detect_dominant_language_no_languages(mock_client):
    mock_client.call.return_value = {"Languages": []}
    with pytest.raises(ValueError, match="could not detect any language"):
        await detect_dominant_language("???")


async def test_detect_dominant_language_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="detect_dominant_language failed"):
        await detect_dominant_language("text")


# ---------------------------------------------------------------------------
# detect_pii_entities
# ---------------------------------------------------------------------------


async def test_detect_pii_entities_success(mock_client):
    mock_client.call.return_value = {
        "Entities": [
            {
                "Type": "EMAIL_ADDRESS",
                "Score": 0.99,
                "BeginOffset": 0,
                "EndOffset": 15,
            }
        ]
    }
    result = await detect_pii_entities("alice@example.com")
    assert len(result) == 1
    assert result[0].pii_type == "EMAIL_ADDRESS"


async def test_detect_pii_entities_empty(mock_client):
    mock_client.call.return_value = {"Entities": []}
    result = await detect_pii_entities("no pii here")
    assert result == []


async def test_detect_pii_entities_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="detect_pii_entities failed"):
        await detect_pii_entities("text")


# ---------------------------------------------------------------------------
# analyze_text
# ---------------------------------------------------------------------------


async def test_analyze_text_english(monkeypatch):
    sentiment = SentimentResult(
        sentiment="POSITIVE",
        positive=0.9,
        negative=0.01,
        neutral=0.05,
        mixed=0.04,
    )
    entities = [
        EntityResult(
            text="AWS",
            entity_type="ORG",
            score=0.99,
            begin_offset=0,
            end_offset=3,
        )
    ]
    key_phrases = [
        KeyPhrase(
            text="great service", score=0.98, begin_offset=0, end_offset=13
        )
    ]
    language = LanguageResult(language_code="en", score=0.99)
    pii = [
        PiiEntity(
            pii_type="EMAIL_ADDRESS",
            score=0.99,
            begin_offset=0,
            end_offset=10,
        )
    ]

    monkeypatch.setattr(
        comp_mod,
        "detect_sentiment",
        AsyncMock(return_value=sentiment),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_entities",
        AsyncMock(return_value=entities),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_key_phrases",
        AsyncMock(return_value=key_phrases),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_dominant_language",
        AsyncMock(return_value=language),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_pii_entities",
        AsyncMock(return_value=pii),
    )

    result = await analyze_text("test text", language_code="en")
    assert result["sentiment"] == sentiment
    assert result["entities"] == entities
    assert result["key_phrases"] == key_phrases
    assert result["language"] == language
    assert result["pii_entities"] == pii


async def test_analyze_text_non_english(monkeypatch):
    """Non-English language_code => no PII detection call."""
    sentiment = SentimentResult(sentiment="NEUTRAL")
    monkeypatch.setattr(
        comp_mod,
        "detect_sentiment",
        AsyncMock(return_value=sentiment),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_entities",
        AsyncMock(return_value=[]),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_key_phrases",
        AsyncMock(return_value=[]),
    )
    monkeypatch.setattr(
        comp_mod,
        "detect_dominant_language",
        AsyncMock(
            return_value=LanguageResult(language_code="fr", score=0.99)
        ),
    )

    result = await analyze_text("bonjour", language_code="fr")
    assert result["sentiment"] == sentiment
    assert result["pii_entities"] == []


# ---------------------------------------------------------------------------
# redact_pii
# ---------------------------------------------------------------------------


async def test_redact_pii_success(monkeypatch):
    pii = [
        PiiEntity(
            pii_type="EMAIL_ADDRESS",
            score=0.99,
            begin_offset=10,
            end_offset=25,
        ),
        PiiEntity(
            pii_type="NAME",
            score=0.95,
            begin_offset=0,
            end_offset=5,
        ),
    ]
    monkeypatch.setattr(
        comp_mod,
        "detect_pii_entities",
        AsyncMock(return_value=pii),
    )
    result = await redact_pii("Alice alice@example.com hello")
    assert "[REDACTED]" in result
    # Both PII spans should be replaced
    assert result.count("[REDACTED]") == 2


async def test_redact_pii_no_entities(monkeypatch):
    monkeypatch.setattr(
        comp_mod,
        "detect_pii_entities",
        AsyncMock(return_value=[]),
    )
    result = await redact_pii("clean text")
    assert result == "clean text"


async def test_redact_pii_custom_replacement(monkeypatch):
    pii = [
        PiiEntity(
            pii_type="SSN",
            score=0.99,
            begin_offset=0,
            end_offset=11,
        )
    ]
    monkeypatch.setattr(
        comp_mod,
        "detect_pii_entities",
        AsyncMock(return_value=pii),
    )
    result = await redact_pii("123-45-6789 rest", replacement="***")
    assert result.startswith("***")


# ---------------------------------------------------------------------------
# batch_detect_sentiment
# ---------------------------------------------------------------------------


async def test_batch_detect_sentiment_success(mock_client):
    mock_client.call.return_value = {
        "ResultList": [
            {
                "Index": 0,
                "Sentiment": "POSITIVE",
                "SentimentScore": {
                    "Positive": 0.9,
                    "Negative": 0.01,
                    "Neutral": 0.05,
                    "Mixed": 0.04,
                },
            },
            {
                "Index": 1,
                "Sentiment": "NEGATIVE",
                "SentimentScore": {
                    "Positive": 0.05,
                    "Negative": 0.9,
                    "Neutral": 0.03,
                    "Mixed": 0.02,
                },
            },
        ],
        "ErrorList": [],
    }
    results = await batch_detect_sentiment(["I love it", "I hate it"])
    assert len(results) == 2
    assert results[0].sentiment == "POSITIVE"
    assert results[1].sentiment == "NEGATIVE"


async def test_batch_detect_sentiment_too_many_texts():
    with pytest.raises(ValueError, match="at most 25 texts"):
        await batch_detect_sentiment(["t"] * 26)


async def test_batch_detect_sentiment_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="batch_detect_sentiment failed"):
        await batch_detect_sentiment(["text"])


async def test_batch_detect_sentiment_with_errors(mock_client):
    mock_client.call.return_value = {
        "ResultList": [],
        "ErrorList": [{"Index": 0, "ErrorCode": "InvalidRequestException"}],
    }
    with pytest.raises(RuntimeError, match="batch_detect_sentiment had errors"):
        await batch_detect_sentiment(["text"])


async def test_batch_detect_sentiment_no_error_list(mock_client):
    """ErrorList absent (falsy) => no error raised."""
    mock_client.call.return_value = {
        "ResultList": [
            {
                "Index": 0,
                "Sentiment": "NEUTRAL",
                "SentimentScore": {
                    "Positive": 0.1,
                    "Negative": 0.1,
                    "Neutral": 0.7,
                    "Mixed": 0.1,
                },
            },
        ],
    }
    results = await batch_detect_sentiment(["ok"])
    assert len(results) == 1


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_comprehend_models_in_all():
    assert "SentimentResult" in comp_mod.__all__
    assert "EntityResult" in comp_mod.__all__
    assert "KeyPhrase" in comp_mod.__all__
    assert "LanguageResult" in comp_mod.__all__
    assert "PiiEntity" in comp_mod.__all__


async def test_batch_detect_dominant_language(mock_client):
    mock_client.call.return_value = {}
    await batch_detect_dominant_language([], )
    mock_client.call.assert_called_once()


async def test_batch_detect_dominant_language_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_detect_dominant_language([], )


async def test_batch_detect_dominant_language_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch detect dominant language"):
        await batch_detect_dominant_language([], )


async def test_batch_detect_entities(mock_client):
    mock_client.call.return_value = {}
    await batch_detect_entities([], "test-language_code", )
    mock_client.call.assert_called_once()


async def test_batch_detect_entities_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_detect_entities([], "test-language_code", )


async def test_batch_detect_entities_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch detect entities"):
        await batch_detect_entities([], "test-language_code", )


async def test_batch_detect_key_phrases(mock_client):
    mock_client.call.return_value = {}
    await batch_detect_key_phrases([], "test-language_code", )
    mock_client.call.assert_called_once()


async def test_batch_detect_key_phrases_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_detect_key_phrases([], "test-language_code", )


async def test_batch_detect_key_phrases_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch detect key phrases"):
        await batch_detect_key_phrases([], "test-language_code", )


async def test_batch_detect_syntax(mock_client):
    mock_client.call.return_value = {}
    await batch_detect_syntax([], "test-language_code", )
    mock_client.call.assert_called_once()


async def test_batch_detect_syntax_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_detect_syntax([], "test-language_code", )


async def test_batch_detect_syntax_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch detect syntax"):
        await batch_detect_syntax([], "test-language_code", )


async def test_batch_detect_targeted_sentiment(mock_client):
    mock_client.call.return_value = {}
    await batch_detect_targeted_sentiment([], "test-language_code", )
    mock_client.call.assert_called_once()


async def test_batch_detect_targeted_sentiment_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_detect_targeted_sentiment([], "test-language_code", )


async def test_batch_detect_targeted_sentiment_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch detect targeted sentiment"):
        await batch_detect_targeted_sentiment([], "test-language_code", )


async def test_classify_document(mock_client):
    mock_client.call.return_value = {}
    await classify_document("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_classify_document_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await classify_document("test-endpoint_arn", )


async def test_classify_document_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to classify document"):
        await classify_document("test-endpoint_arn", )


async def test_contains_pii_entities(mock_client):
    mock_client.call.return_value = {}
    await contains_pii_entities("test-text", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_contains_pii_entities_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await contains_pii_entities("test-text", "test-language_code", )


async def test_contains_pii_entities_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to contains pii entities"):
        await contains_pii_entities("test-text", "test-language_code", )


async def test_create_dataset(mock_client):
    mock_client.call.return_value = {}
    await create_dataset("test-flywheel_arn", "test-dataset_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_dataset_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_dataset("test-flywheel_arn", "test-dataset_name", {}, )


async def test_create_dataset_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create dataset"):
        await create_dataset("test-flywheel_arn", "test-dataset_name", {}, )


async def test_create_document_classifier(mock_client):
    mock_client.call.return_value = {}
    await create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", )
    mock_client.call.assert_called_once()


async def test_create_document_classifier_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", )


async def test_create_document_classifier_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create document classifier"):
        await create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", )


async def test_create_endpoint(mock_client):
    mock_client.call.return_value = {}
    await create_endpoint("test-endpoint_name", 1, )
    mock_client.call.assert_called_once()


async def test_create_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_endpoint("test-endpoint_name", 1, )


async def test_create_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create endpoint"):
        await create_endpoint("test-endpoint_name", 1, )


async def test_create_entity_recognizer(mock_client):
    mock_client.call.return_value = {}
    await create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", )
    mock_client.call.assert_called_once()


async def test_create_entity_recognizer_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", )


async def test_create_entity_recognizer_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create entity recognizer"):
        await create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", )


async def test_create_flywheel(mock_client):
    mock_client.call.return_value = {}
    await create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", )
    mock_client.call.assert_called_once()


async def test_create_flywheel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", )


async def test_create_flywheel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create flywheel"):
        await create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", )


async def test_delete_document_classifier(mock_client):
    mock_client.call.return_value = {}
    await delete_document_classifier("test-document_classifier_arn", )
    mock_client.call.assert_called_once()


async def test_delete_document_classifier_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_document_classifier("test-document_classifier_arn", )


async def test_delete_document_classifier_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete document classifier"):
        await delete_document_classifier("test-document_classifier_arn", )


async def test_delete_endpoint(mock_client):
    mock_client.call.return_value = {}
    await delete_endpoint("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_delete_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_endpoint("test-endpoint_arn", )


async def test_delete_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete endpoint"):
        await delete_endpoint("test-endpoint_arn", )


async def test_delete_entity_recognizer(mock_client):
    mock_client.call.return_value = {}
    await delete_entity_recognizer("test-entity_recognizer_arn", )
    mock_client.call.assert_called_once()


async def test_delete_entity_recognizer_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_entity_recognizer("test-entity_recognizer_arn", )


async def test_delete_entity_recognizer_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete entity recognizer"):
        await delete_entity_recognizer("test-entity_recognizer_arn", )


async def test_delete_flywheel(mock_client):
    mock_client.call.return_value = {}
    await delete_flywheel("test-flywheel_arn", )
    mock_client.call.assert_called_once()


async def test_delete_flywheel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_flywheel("test-flywheel_arn", )


async def test_delete_flywheel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete flywheel"):
        await delete_flywheel("test-flywheel_arn", )


async def test_delete_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        await delete_resource_policy("test-resource_arn", )


async def test_describe_dataset(mock_client):
    mock_client.call.return_value = {}
    await describe_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset("test-dataset_arn", )


async def test_describe_dataset_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        await describe_dataset("test-dataset_arn", )


async def test_describe_document_classification_job(mock_client):
    mock_client.call.return_value = {}
    await describe_document_classification_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_document_classification_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_document_classification_job("test-job_id", )


async def test_describe_document_classification_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe document classification job"):
        await describe_document_classification_job("test-job_id", )


async def test_describe_document_classifier(mock_client):
    mock_client.call.return_value = {}
    await describe_document_classifier("test-document_classifier_arn", )
    mock_client.call.assert_called_once()


async def test_describe_document_classifier_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_document_classifier("test-document_classifier_arn", )


async def test_describe_document_classifier_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe document classifier"):
        await describe_document_classifier("test-document_classifier_arn", )


async def test_describe_dominant_language_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_dominant_language_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_dominant_language_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dominant_language_detection_job("test-job_id", )


async def test_describe_dominant_language_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe dominant language detection job"):
        await describe_dominant_language_detection_job("test-job_id", )


async def test_describe_endpoint(mock_client):
    mock_client.call.return_value = {}
    await describe_endpoint("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_describe_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint("test-endpoint_arn", )


async def test_describe_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe endpoint"):
        await describe_endpoint("test-endpoint_arn", )


async def test_describe_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_entities_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_entities_detection_job("test-job_id", )


async def test_describe_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe entities detection job"):
        await describe_entities_detection_job("test-job_id", )


async def test_describe_entity_recognizer(mock_client):
    mock_client.call.return_value = {}
    await describe_entity_recognizer("test-entity_recognizer_arn", )
    mock_client.call.assert_called_once()


async def test_describe_entity_recognizer_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_entity_recognizer("test-entity_recognizer_arn", )


async def test_describe_entity_recognizer_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe entity recognizer"):
        await describe_entity_recognizer("test-entity_recognizer_arn", )


async def test_describe_events_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_events_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_events_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events_detection_job("test-job_id", )


async def test_describe_events_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe events detection job"):
        await describe_events_detection_job("test-job_id", )


async def test_describe_flywheel(mock_client):
    mock_client.call.return_value = {}
    await describe_flywheel("test-flywheel_arn", )
    mock_client.call.assert_called_once()


async def test_describe_flywheel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_flywheel("test-flywheel_arn", )


async def test_describe_flywheel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe flywheel"):
        await describe_flywheel("test-flywheel_arn", )


async def test_describe_flywheel_iteration(mock_client):
    mock_client.call.return_value = {}
    await describe_flywheel_iteration("test-flywheel_arn", "test-flywheel_iteration_id", )
    mock_client.call.assert_called_once()


async def test_describe_flywheel_iteration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_flywheel_iteration("test-flywheel_arn", "test-flywheel_iteration_id", )


async def test_describe_flywheel_iteration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe flywheel iteration"):
        await describe_flywheel_iteration("test-flywheel_arn", "test-flywheel_iteration_id", )


async def test_describe_key_phrases_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_key_phrases_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_key_phrases_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_key_phrases_detection_job("test-job_id", )


async def test_describe_key_phrases_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe key phrases detection job"):
        await describe_key_phrases_detection_job("test-job_id", )


async def test_describe_pii_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_pii_entities_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_pii_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pii_entities_detection_job("test-job_id", )


async def test_describe_pii_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe pii entities detection job"):
        await describe_pii_entities_detection_job("test-job_id", )


async def test_describe_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await describe_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_describe_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resource_policy("test-resource_arn", )


async def test_describe_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe resource policy"):
        await describe_resource_policy("test-resource_arn", )


async def test_describe_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_sentiment_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_sentiment_detection_job("test-job_id", )


async def test_describe_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe sentiment detection job"):
        await describe_sentiment_detection_job("test-job_id", )


async def test_describe_targeted_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_targeted_sentiment_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_targeted_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_targeted_sentiment_detection_job("test-job_id", )


async def test_describe_targeted_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe targeted sentiment detection job"):
        await describe_targeted_sentiment_detection_job("test-job_id", )


async def test_describe_topics_detection_job(mock_client):
    mock_client.call.return_value = {}
    await describe_topics_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_topics_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_topics_detection_job("test-job_id", )


async def test_describe_topics_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe topics detection job"):
        await describe_topics_detection_job("test-job_id", )


async def test_detect_syntax(mock_client):
    mock_client.call.return_value = {}
    await detect_syntax("test-text", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_detect_syntax_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await detect_syntax("test-text", "test-language_code", )


async def test_detect_syntax_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to detect syntax"):
        await detect_syntax("test-text", "test-language_code", )


async def test_detect_targeted_sentiment(mock_client):
    mock_client.call.return_value = {}
    await detect_targeted_sentiment("test-text", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_detect_targeted_sentiment_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await detect_targeted_sentiment("test-text", "test-language_code", )


async def test_detect_targeted_sentiment_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to detect targeted sentiment"):
        await detect_targeted_sentiment("test-text", "test-language_code", )


async def test_detect_toxic_content(mock_client):
    mock_client.call.return_value = {}
    await detect_toxic_content([], "test-language_code", )
    mock_client.call.assert_called_once()


async def test_detect_toxic_content_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await detect_toxic_content([], "test-language_code", )


async def test_detect_toxic_content_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to detect toxic content"):
        await detect_toxic_content([], "test-language_code", )


async def test_import_model(mock_client):
    mock_client.call.return_value = {}
    await import_model("test-source_model_arn", )
    mock_client.call.assert_called_once()


async def test_import_model_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await import_model("test-source_model_arn", )


async def test_import_model_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to import model"):
        await import_model("test-source_model_arn", )


async def test_list_datasets(mock_client):
    mock_client.call.return_value = {}
    await list_datasets()
    mock_client.call.assert_called_once()


async def test_list_datasets_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_datasets()


async def test_list_datasets_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list datasets"):
        await list_datasets()


async def test_list_document_classification_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_document_classification_jobs()
    mock_client.call.assert_called_once()


async def test_list_document_classification_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_document_classification_jobs()


async def test_list_document_classification_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list document classification jobs"):
        await list_document_classification_jobs()


async def test_list_document_classifier_summaries(mock_client):
    mock_client.call.return_value = {}
    await list_document_classifier_summaries()
    mock_client.call.assert_called_once()


async def test_list_document_classifier_summaries_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_document_classifier_summaries()


async def test_list_document_classifier_summaries_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list document classifier summaries"):
        await list_document_classifier_summaries()


async def test_list_document_classifiers(mock_client):
    mock_client.call.return_value = {}
    await list_document_classifiers()
    mock_client.call.assert_called_once()


async def test_list_document_classifiers_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_document_classifiers()


async def test_list_document_classifiers_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list document classifiers"):
        await list_document_classifiers()


async def test_list_dominant_language_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_dominant_language_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_dominant_language_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_dominant_language_detection_jobs()


async def test_list_dominant_language_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list dominant language detection jobs"):
        await list_dominant_language_detection_jobs()


async def test_list_endpoints(mock_client):
    mock_client.call.return_value = {}
    await list_endpoints()
    mock_client.call.assert_called_once()


async def test_list_endpoints_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_endpoints()


async def test_list_endpoints_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list endpoints"):
        await list_endpoints()


async def test_list_entities_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_entities_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_entities_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_entities_detection_jobs()


async def test_list_entities_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list entities detection jobs"):
        await list_entities_detection_jobs()


async def test_list_entity_recognizer_summaries(mock_client):
    mock_client.call.return_value = {}
    await list_entity_recognizer_summaries()
    mock_client.call.assert_called_once()


async def test_list_entity_recognizer_summaries_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_entity_recognizer_summaries()


async def test_list_entity_recognizer_summaries_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list entity recognizer summaries"):
        await list_entity_recognizer_summaries()


async def test_list_entity_recognizers(mock_client):
    mock_client.call.return_value = {}
    await list_entity_recognizers()
    mock_client.call.assert_called_once()


async def test_list_entity_recognizers_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_entity_recognizers()


async def test_list_entity_recognizers_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list entity recognizers"):
        await list_entity_recognizers()


async def test_list_events_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_events_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_events_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_events_detection_jobs()


async def test_list_events_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list events detection jobs"):
        await list_events_detection_jobs()


async def test_list_flywheel_iteration_history(mock_client):
    mock_client.call.return_value = {}
    await list_flywheel_iteration_history("test-flywheel_arn", )
    mock_client.call.assert_called_once()


async def test_list_flywheel_iteration_history_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_flywheel_iteration_history("test-flywheel_arn", )


async def test_list_flywheel_iteration_history_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list flywheel iteration history"):
        await list_flywheel_iteration_history("test-flywheel_arn", )


async def test_list_flywheels(mock_client):
    mock_client.call.return_value = {}
    await list_flywheels()
    mock_client.call.assert_called_once()


async def test_list_flywheels_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_flywheels()


async def test_list_flywheels_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list flywheels"):
        await list_flywheels()


async def test_list_key_phrases_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_key_phrases_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_key_phrases_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_key_phrases_detection_jobs()


async def test_list_key_phrases_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list key phrases detection jobs"):
        await list_key_phrases_detection_jobs()


async def test_list_pii_entities_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_pii_entities_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_pii_entities_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_pii_entities_detection_jobs()


async def test_list_pii_entities_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list pii entities detection jobs"):
        await list_pii_entities_detection_jobs()


async def test_list_sentiment_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_sentiment_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_sentiment_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_sentiment_detection_jobs()


async def test_list_sentiment_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list sentiment detection jobs"):
        await list_sentiment_detection_jobs()


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_targeted_sentiment_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_targeted_sentiment_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_targeted_sentiment_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_targeted_sentiment_detection_jobs()


async def test_list_targeted_sentiment_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list targeted sentiment detection jobs"):
        await list_targeted_sentiment_detection_jobs()


async def test_list_topics_detection_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_topics_detection_jobs()
    mock_client.call.assert_called_once()


async def test_list_topics_detection_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_topics_detection_jobs()


async def test_list_topics_detection_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list topics detection jobs"):
        await list_topics_detection_jobs()


async def test_put_resource_policy(mock_client):
    mock_client.call.return_value = {}
    await put_resource_policy("test-resource_arn", "test-resource_policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-resource_policy", )


async def test_put_resource_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        await put_resource_policy("test-resource_arn", "test-resource_policy", )


async def test_start_document_classification_job(mock_client):
    mock_client.call.return_value = {}
    await start_document_classification_job({}, {}, "test-data_access_role_arn", )
    mock_client.call.assert_called_once()


async def test_start_document_classification_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_document_classification_job({}, {}, "test-data_access_role_arn", )


async def test_start_document_classification_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start document classification job"):
        await start_document_classification_job({}, {}, "test-data_access_role_arn", )


async def test_start_dominant_language_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", )
    mock_client.call.assert_called_once()


async def test_start_dominant_language_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", )


async def test_start_dominant_language_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start dominant language detection job"):
        await start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", )


async def test_start_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_start_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start entities detection job"):
        await start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_events_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", [], )
    mock_client.call.assert_called_once()


async def test_start_events_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", [], )


async def test_start_events_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start events detection job"):
        await start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", [], )


async def test_start_flywheel_iteration(mock_client):
    mock_client.call.return_value = {}
    await start_flywheel_iteration("test-flywheel_arn", )
    mock_client.call.assert_called_once()


async def test_start_flywheel_iteration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_flywheel_iteration("test-flywheel_arn", )


async def test_start_flywheel_iteration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start flywheel iteration"):
        await start_flywheel_iteration("test-flywheel_arn", )


async def test_start_key_phrases_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_start_key_phrases_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_key_phrases_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start key phrases detection job"):
        await start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_pii_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_start_pii_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", )


async def test_start_pii_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start pii entities detection job"):
        await start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", )


async def test_start_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_start_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start sentiment detection job"):
        await start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_targeted_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_start_targeted_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_targeted_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start targeted sentiment detection job"):
        await start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", )


async def test_start_topics_detection_job(mock_client):
    mock_client.call.return_value = {}
    await start_topics_detection_job({}, {}, "test-data_access_role_arn", )
    mock_client.call.assert_called_once()


async def test_start_topics_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_topics_detection_job({}, {}, "test-data_access_role_arn", )


async def test_start_topics_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start topics detection job"):
        await start_topics_detection_job({}, {}, "test-data_access_role_arn", )


async def test_stop_dominant_language_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_dominant_language_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_dominant_language_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_dominant_language_detection_job("test-job_id", )


async def test_stop_dominant_language_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop dominant language detection job"):
        await stop_dominant_language_detection_job("test-job_id", )


async def test_stop_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_entities_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_entities_detection_job("test-job_id", )


async def test_stop_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop entities detection job"):
        await stop_entities_detection_job("test-job_id", )


async def test_stop_events_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_events_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_events_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_events_detection_job("test-job_id", )


async def test_stop_events_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop events detection job"):
        await stop_events_detection_job("test-job_id", )


async def test_stop_key_phrases_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_key_phrases_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_key_phrases_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_key_phrases_detection_job("test-job_id", )


async def test_stop_key_phrases_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop key phrases detection job"):
        await stop_key_phrases_detection_job("test-job_id", )


async def test_stop_pii_entities_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_pii_entities_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_pii_entities_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_pii_entities_detection_job("test-job_id", )


async def test_stop_pii_entities_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop pii entities detection job"):
        await stop_pii_entities_detection_job("test-job_id", )


async def test_stop_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_sentiment_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_sentiment_detection_job("test-job_id", )


async def test_stop_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop sentiment detection job"):
        await stop_sentiment_detection_job("test-job_id", )


async def test_stop_targeted_sentiment_detection_job(mock_client):
    mock_client.call.return_value = {}
    await stop_targeted_sentiment_detection_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_targeted_sentiment_detection_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_targeted_sentiment_detection_job("test-job_id", )


async def test_stop_targeted_sentiment_detection_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop targeted sentiment detection job"):
        await stop_targeted_sentiment_detection_job("test-job_id", )


async def test_stop_training_document_classifier(mock_client):
    mock_client.call.return_value = {}
    await stop_training_document_classifier("test-document_classifier_arn", )
    mock_client.call.assert_called_once()


async def test_stop_training_document_classifier_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_training_document_classifier("test-document_classifier_arn", )


async def test_stop_training_document_classifier_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop training document classifier"):
        await stop_training_document_classifier("test-document_classifier_arn", )


async def test_stop_training_entity_recognizer(mock_client):
    mock_client.call.return_value = {}
    await stop_training_entity_recognizer("test-entity_recognizer_arn", )
    mock_client.call.assert_called_once()


async def test_stop_training_entity_recognizer_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_training_entity_recognizer("test-entity_recognizer_arn", )


async def test_stop_training_entity_recognizer_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop training entity recognizer"):
        await stop_training_entity_recognizer("test-entity_recognizer_arn", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


async def test_update_endpoint(mock_client):
    mock_client.call.return_value = {}
    await update_endpoint("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_update_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_endpoint("test-endpoint_arn", )


async def test_update_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update endpoint"):
        await update_endpoint("test-endpoint_arn", )


async def test_update_flywheel(mock_client):
    mock_client.call.return_value = {}
    await update_flywheel("test-flywheel_arn", )
    mock_client.call.assert_called_once()


async def test_update_flywheel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_flywheel("test-flywheel_arn", )


async def test_update_flywheel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update flywheel"):
        await update_flywheel("test-flywheel_arn", )


@pytest.mark.asyncio
async def test_classify_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import classify_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await classify_document("test-endpoint_arn", text="test-text", bytes="test-bytes", document_reader_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import create_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await create_dataset("test-flywheel_arn", "test-dataset_name", {}, dataset_type="test-dataset_type", description="test-description", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_document_classifier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import create_document_classifier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await create_document_classifier("test-document_classifier_name", "test-data_access_role_arn", {}, "test-language_code", version_name="test-version_name", tags=[{"Key": "k", "Value": "v"}], output_data_config={}, client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, mode="test-mode", model_kms_key_id="test-model_kms_key_id", model_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import create_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await create_endpoint("test-endpoint_name", "test-desired_inference_units", model_arn="test-model_arn", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], data_access_role_arn="test-data_access_role_arn", flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_entity_recognizer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import create_entity_recognizer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await create_entity_recognizer("test-recognizer_name", "test-data_access_role_arn", {}, "test-language_code", version_name="test-version_name", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, model_kms_key_id="test-model_kms_key_id", model_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_flywheel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import create_flywheel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await create_flywheel("test-flywheel_name", "test-data_access_role_arn", "test-data_lake_s3_uri", active_model_arn="test-active_model_arn", task_config={}, model_type="test-model_type", data_security_config={}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import delete_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await delete_resource_policy("test-resource_arn", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import import_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await import_model("test-source_model_arn", model_name="test-model_name", version_name="test-version_name", model_kms_key_id="test-model_kms_key_id", data_access_role_arn="test-data_access_role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_datasets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_datasets(flywheel_arn="test-flywheel_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_document_classification_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_document_classification_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_document_classification_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_document_classifier_summaries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_document_classifier_summaries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_document_classifier_summaries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_document_classifiers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_document_classifiers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_document_classifiers(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dominant_language_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_dominant_language_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_dominant_language_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_endpoints(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_entities_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_entities_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_entities_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_entity_recognizer_summaries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_entity_recognizer_summaries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_entity_recognizer_summaries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_entity_recognizers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_entity_recognizers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_entity_recognizers(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_events_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_events_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_events_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flywheel_iteration_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_flywheel_iteration_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_flywheel_iteration_history("test-flywheel_arn", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flywheels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_flywheels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_flywheels(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_key_phrases_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_key_phrases_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_key_phrases_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_pii_entities_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_pii_entities_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_pii_entities_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sentiment_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_sentiment_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_sentiment_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_targeted_sentiment_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_targeted_sentiment_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_targeted_sentiment_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_topics_detection_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import list_topics_detection_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await list_topics_detection_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-resource_arn", "{}", policy_revision_id="test-policy_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_document_classification_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_document_classification_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_document_classification_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", document_classifier_arn="test-document_classifier_arn", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_dominant_language_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_dominant_language_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_dominant_language_detection_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_entities_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_entities_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_entities_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", entity_recognizer_arn="test-entity_recognizer_arn", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_events_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_events_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_events_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", "test-target_event_types", job_name="test-job_name", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_flywheel_iteration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_flywheel_iteration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_flywheel_iteration("test-flywheel_arn", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_key_phrases_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_key_phrases_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_key_phrases_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_pii_entities_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_pii_entities_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_pii_entities_detection_job({}, {}, "test-mode", "test-data_access_role_arn", "test-language_code", redaction_config={}, job_name="test-job_name", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_sentiment_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_sentiment_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_targeted_sentiment_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_targeted_sentiment_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_targeted_sentiment_detection_job({}, {}, "test-data_access_role_arn", "test-language_code", job_name="test-job_name", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_topics_detection_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import start_topics_detection_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await start_topics_detection_job({}, {}, "test-data_access_role_arn", job_name="test-job_name", number_of_topics="test-number_of_topics", client_request_token="test-client_request_token", volume_kms_key_id="test-volume_kms_key_id", vpc_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import update_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await update_endpoint("test-endpoint_arn", desired_model_arn="test-desired_model_arn", desired_inference_units="test-desired_inference_units", desired_data_access_role_arn="test-desired_data_access_role_arn", flywheel_arn="test-flywheel_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_flywheel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.comprehend import update_flywheel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.comprehend.async_client", lambda *a, **kw: mock_client)
    await update_flywheel("test-flywheel_arn", active_model_arn="test-active_model_arn", data_access_role_arn="test-data_access_role_arn", data_security_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()
