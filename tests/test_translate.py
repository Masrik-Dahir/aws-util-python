"""Tests for aws_util.translate module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.translate as translate_mod
from aws_util.translate import (
    TranslateResult,
    TranslateLanguage,
    translate_text,
    translate_batch,
    list_languages,
    create_parallel_data,
    delete_parallel_data,
    delete_terminology,
    describe_text_translation_job,
    get_parallel_data,
    get_terminology,
    import_terminology,
    list_parallel_data,
    list_tags_for_resource,
    list_terminologies,
    list_text_translation_jobs,
    start_text_translation_job,
    stop_text_translation_job,
    tag_resource,
    translate_document,
    untag_resource,
    update_parallel_data,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_translate_result_model():
    result = TranslateResult(
        translated_text="Hola",
        source_language_code="en",
        target_language_code="es",
    )
    assert result.translated_text == "Hola"


def test_translate_language_model():
    lang = TranslateLanguage(language_code="es", language_name="Spanish")
    assert lang.language_code == "es"


# ---------------------------------------------------------------------------
# translate_text
# ---------------------------------------------------------------------------

def test_translate_text_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_text.return_value = {
        "TranslatedText": "Hola mundo",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "es",
    }
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    result = translate_text("Hello world", "es", region_name=REGION)
    assert isinstance(result, TranslateResult)
    assert result.translated_text == "Hola mundo"
    assert result.source_language_code == "en"
    assert result.target_language_code == "es"


def test_translate_text_auto_detect(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_text.return_value = {
        "TranslatedText": "Bonjour",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "fr",
    }
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    result = translate_text("Hello", "fr", source_language_code="auto", region_name=REGION)
    assert result.translated_text == "Bonjour"
    call_kwargs = mock_client.translate_text.call_args[1]
    assert call_kwargs["SourceLanguageCode"] == "auto"


def test_translate_text_with_terminology(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_text.return_value = {
        "TranslatedText": "Hola",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "es",
    }
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    result = translate_text(
        "Hello", "es", terminology_names=["my-terms"], region_name=REGION
    )
    assert result.translated_text == "Hola"
    call_kwargs = mock_client.translate_text.call_args[1]
    assert call_kwargs["TerminologyNames"] == ["my-terms"]


def test_translate_text_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_text.side_effect = ClientError(
        {"Error": {"Code": "UnsupportedLanguagePairException", "Message": "unsupported pair"}},
        "TranslateText",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to translate text"):
        translate_text("Hello", "xx", region_name=REGION)


# ---------------------------------------------------------------------------
# translate_batch
# ---------------------------------------------------------------------------

def test_translate_batch_success(monkeypatch):
    def fake_translate(text, target_language_code, source_language_code="auto",
                       terminology_names=None, region_name=None):
        return TranslateResult(
            translated_text=f"Translated:{text}",
            source_language_code="en",
            target_language_code=target_language_code,
        )

    monkeypatch.setattr(translate_mod, "translate_text", fake_translate)
    texts = ["Hello", "World", "Foo"]
    results = translate_batch(texts, "fr", region_name=REGION)
    assert len(results) == 3
    assert all(isinstance(r, TranslateResult) for r in results)
    # Should preserve order
    assert results[0].translated_text == "Translated:Hello"
    assert results[1].translated_text == "Translated:World"


def test_translate_batch_empty():
    results = translate_batch([], "fr", region_name=REGION)
    assert results == []


def test_translate_batch_single(monkeypatch):
    fake_result = TranslateResult(
        translated_text="Hola", source_language_code="en", target_language_code="es"
    )
    monkeypatch.setattr(translate_mod, "translate_text", lambda *a, **kw: fake_result)
    results = translate_batch(["Hello"], "es", region_name=REGION)
    assert len(results) == 1
    assert results[0].translated_text == "Hola"


# ---------------------------------------------------------------------------
# list_languages
# ---------------------------------------------------------------------------

def test_list_languages_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_languages.return_value = {
        "Languages": [
            {"LanguageCode": "en", "LanguageName": "English"},
            {"LanguageCode": "es", "LanguageName": "Spanish"},
        ],
        "NextToken": None,
    }
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_languages(region_name=REGION)
    assert len(result) == 2
    assert all(isinstance(lang, TranslateLanguage) for lang in result)
    assert result[0].language_code == "en"


def test_list_languages_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_languages.side_effect = [
        {
            "Languages": [{"LanguageCode": "en", "LanguageName": "English"}],
            "NextToken": "token1",
        },
        {
            "Languages": [{"LanguageCode": "es", "LanguageName": "Spanish"}],
            "NextToken": None,
        },
    ]
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_languages(region_name=REGION)
    assert len(result) == 2


def test_list_languages_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_languages.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "ListLanguages"
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_languages failed"):
        list_languages(region_name=REGION)


def test_create_parallel_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_parallel_data.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    create_parallel_data("test-name", {}, "test-client_token", region_name=REGION)
    mock_client.create_parallel_data.assert_called_once()


def test_create_parallel_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_parallel_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_parallel_data",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create parallel data"):
        create_parallel_data("test-name", {}, "test-client_token", region_name=REGION)


def test_delete_parallel_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_parallel_data.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    delete_parallel_data("test-name", region_name=REGION)
    mock_client.delete_parallel_data.assert_called_once()


def test_delete_parallel_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_parallel_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_parallel_data",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete parallel data"):
        delete_parallel_data("test-name", region_name=REGION)


def test_delete_terminology(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_terminology.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    delete_terminology("test-name", region_name=REGION)
    mock_client.delete_terminology.assert_called_once()


def test_delete_terminology_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_terminology.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_terminology",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete terminology"):
        delete_terminology("test-name", region_name=REGION)


def test_describe_text_translation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_text_translation_job.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    describe_text_translation_job("test-job_id", region_name=REGION)
    mock_client.describe_text_translation_job.assert_called_once()


def test_describe_text_translation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_text_translation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_text_translation_job",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe text translation job"):
        describe_text_translation_job("test-job_id", region_name=REGION)


def test_get_parallel_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parallel_data.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    get_parallel_data("test-name", region_name=REGION)
    mock_client.get_parallel_data.assert_called_once()


def test_get_parallel_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parallel_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_parallel_data",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get parallel data"):
        get_parallel_data("test-name", region_name=REGION)


def test_get_terminology(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_terminology.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    get_terminology("test-name", region_name=REGION)
    mock_client.get_terminology.assert_called_once()


def test_get_terminology_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_terminology.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_terminology",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get terminology"):
        get_terminology("test-name", region_name=REGION)


def test_import_terminology(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_terminology.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    import_terminology("test-name", "test-merge_strategy", {}, region_name=REGION)
    mock_client.import_terminology.assert_called_once()


def test_import_terminology_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_terminology.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_terminology",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import terminology"):
        import_terminology("test-name", "test-merge_strategy", {}, region_name=REGION)


def test_list_parallel_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_parallel_data.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    list_parallel_data(region_name=REGION)
    mock_client.list_parallel_data.assert_called_once()


def test_list_parallel_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_parallel_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_parallel_data",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list parallel data"):
        list_parallel_data(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_terminologies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_terminologies.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    list_terminologies(region_name=REGION)
    mock_client.list_terminologies.assert_called_once()


def test_list_terminologies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_terminologies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_terminologies",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list terminologies"):
        list_terminologies(region_name=REGION)


def test_list_text_translation_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_text_translation_jobs.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    list_text_translation_jobs(region_name=REGION)
    mock_client.list_text_translation_jobs.assert_called_once()


def test_list_text_translation_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_text_translation_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_text_translation_jobs",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list text translation jobs"):
        list_text_translation_jobs(region_name=REGION)


def test_start_text_translation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_text_translation_job.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", [], "test-client_token", region_name=REGION)
    mock_client.start_text_translation_job.assert_called_once()


def test_start_text_translation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_text_translation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_text_translation_job",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start text translation job"):
        start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", [], "test-client_token", region_name=REGION)


def test_stop_text_translation_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_text_translation_job.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    stop_text_translation_job("test-job_id", region_name=REGION)
    mock_client.stop_text_translation_job.assert_called_once()


def test_stop_text_translation_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_text_translation_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_text_translation_job",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop text translation job"):
        stop_text_translation_job("test-job_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_translate_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_document.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    translate_document({}, "test-source_language_code", "test-target_language_code", region_name=REGION)
    mock_client.translate_document.assert_called_once()


def test_translate_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.translate_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "translate_document",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to translate document"):
        translate_document({}, "test-source_language_code", "test-target_language_code", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_parallel_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_parallel_data.return_value = {}
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    update_parallel_data("test-name", {}, "test-client_token", region_name=REGION)
    mock_client.update_parallel_data.assert_called_once()


def test_update_parallel_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_parallel_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_parallel_data",
    )
    monkeypatch.setattr(translate_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update parallel data"):
        update_parallel_data("test-name", {}, "test-client_token", region_name=REGION)


def test_create_parallel_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import create_parallel_data
    mock_client = MagicMock()
    mock_client.create_parallel_data.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    create_parallel_data("test-name", {}, "test-client_token", description="test-description", encryption_key="test-encryption_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_parallel_data.assert_called_once()

def test_get_terminology_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import get_terminology
    mock_client = MagicMock()
    mock_client.get_terminology.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    get_terminology("test-name", terminology_data_format="test-terminology_data_format", region_name="us-east-1")
    mock_client.get_terminology.assert_called_once()

def test_import_terminology_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import import_terminology
    mock_client = MagicMock()
    mock_client.import_terminology.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    import_terminology("test-name", "test-merge_strategy", "test-terminology_data", description="test-description", encryption_key="test-encryption_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_terminology.assert_called_once()

def test_list_parallel_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import list_parallel_data
    mock_client = MagicMock()
    mock_client.list_parallel_data.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    list_parallel_data(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_parallel_data.assert_called_once()

def test_list_terminologies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import list_terminologies
    mock_client = MagicMock()
    mock_client.list_terminologies.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    list_terminologies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_terminologies.assert_called_once()

def test_list_text_translation_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import list_text_translation_jobs
    mock_client = MagicMock()
    mock_client.list_text_translation_jobs.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    list_text_translation_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_text_translation_jobs.assert_called_once()

def test_start_text_translation_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import start_text_translation_job
    mock_client = MagicMock()
    mock_client.start_text_translation_job.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", "test-target_language_codes", "test-client_token", job_name="test-job_name", terminology_names="test-terminology_names", parallel_data_names="test-parallel_data_names", settings={}, region_name="us-east-1")
    mock_client.start_text_translation_job.assert_called_once()

def test_translate_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import translate_document
    mock_client = MagicMock()
    mock_client.translate_document.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    translate_document("test-document", "test-source_language_code", "test-target_language_code", terminology_names="test-terminology_names", settings={}, region_name="us-east-1")
    mock_client.translate_document.assert_called_once()

def test_update_parallel_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.translate import update_parallel_data
    mock_client = MagicMock()
    mock_client.update_parallel_data.return_value = {}
    monkeypatch.setattr("aws_util.translate.get_client", lambda *a, **kw: mock_client)
    update_parallel_data("test-name", {}, "test-client_token", description="test-description", region_name="us-east-1")
    mock_client.update_parallel_data.assert_called_once()
