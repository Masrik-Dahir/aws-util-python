from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.translate import (
    TranslateLanguage,
    TranslateResult,
    list_languages,
    translate_batch,
    translate_text,
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


# ---------------------------------------------------------------------------
# translate_text
# ---------------------------------------------------------------------------


async def test_translate_text_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranslatedText": "Hola",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "es",
    }
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await translate_text("Hello", "es")
    assert isinstance(result, TranslateResult)
    assert result.translated_text == "Hola"
    assert result.source_language_code == "en"
    assert result.target_language_code == "es"


async def test_translate_text_with_terminology(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranslatedText": "Bonjour",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "fr",
    }
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await translate_text(
        "Hello",
        "fr",
        source_language_code="en",
        terminology_names=["my-terms"],
        region_name="us-west-2",
    )
    assert result.translated_text == "Bonjour"


async def test_translate_text_no_terminology(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranslatedText": "hi",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "fr",
    }
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await translate_text("hello", "fr")
    assert "TerminologyNames" not in mock_client.call.call_args[1]


async def test_translate_text_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to translate text"):
        await translate_text("Hello", "es")


# ---------------------------------------------------------------------------
# translate_batch
# ---------------------------------------------------------------------------


async def test_translate_batch_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "TranslatedText": "Hola",
            "SourceLanguageCode": "en",
            "TargetLanguageCode": "es",
        },
        {
            "TranslatedText": "Mundo",
            "SourceLanguageCode": "en",
            "TargetLanguageCode": "es",
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await translate_batch(["Hello", "World"], "es")
    assert len(result) == 2
    assert result[0].translated_text == "Hola"
    assert result[1].translated_text == "Mundo"


async def test_translate_batch_empty() -> None:
    result = await translate_batch([], "es")
    assert result == []


async def test_translate_batch_with_terminology(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranslatedText": "Bonjour",
        "SourceLanguageCode": "en",
        "TargetLanguageCode": "fr",
    }
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await translate_batch(
        ["Hello"],
        "fr",
        source_language_code="en",
        terminology_names=["terms"],
        region_name="eu-west-1",
    )
    assert len(result) == 1


# ---------------------------------------------------------------------------
# list_languages
# ---------------------------------------------------------------------------


async def test_list_languages_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Languages": [
            {"LanguageCode": "en", "LanguageName": "English"},
            {"LanguageCode": "es", "LanguageName": "Spanish"},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_languages()
    assert len(result) == 2
    assert result[0].language_code == "en"


async def test_list_languages_paginated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Languages": [{"LanguageCode": "en", "LanguageName": "English"}],
            "NextToken": "tok-1",
        },
        {
            "Languages": [{"LanguageCode": "es", "LanguageName": "Spanish"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_languages()
    assert len(result) == 2


async def test_list_languages_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_languages failed"):
        await list_languages()


async def test_create_parallel_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_parallel_data("test-name", {}, "test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_parallel_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_parallel_data("test-name", {}, "test-client_token", )


async def test_delete_parallel_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_parallel_data("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_parallel_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_parallel_data("test-name", )


async def test_delete_terminology(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_terminology("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_terminology_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_terminology("test-name", )


async def test_describe_text_translation_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_text_translation_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_text_translation_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_text_translation_job("test-job_id", )


async def test_get_parallel_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_parallel_data("test-name", )
    mock_client.call.assert_called_once()


async def test_get_parallel_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_parallel_data("test-name", )


async def test_get_terminology(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_terminology("test-name", )
    mock_client.call.assert_called_once()


async def test_get_terminology_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_terminology("test-name", )


async def test_import_terminology(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_terminology("test-name", "test-merge_strategy", {}, )
    mock_client.call.assert_called_once()


async def test_import_terminology_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_terminology("test-name", "test-merge_strategy", {}, )


async def test_list_parallel_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_parallel_data()
    mock_client.call.assert_called_once()


async def test_list_parallel_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_parallel_data()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_terminologies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_terminologies()
    mock_client.call.assert_called_once()


async def test_list_terminologies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_terminologies()


async def test_list_text_translation_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_text_translation_jobs()
    mock_client.call.assert_called_once()


async def test_list_text_translation_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_text_translation_jobs()


async def test_start_text_translation_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", [], "test-client_token", )
    mock_client.call.assert_called_once()


async def test_start_text_translation_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", [], "test-client_token", )


async def test_stop_text_translation_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_text_translation_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_text_translation_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_text_translation_job("test-job_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_translate_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await translate_document({}, "test-source_language_code", "test-target_language_code", )
    mock_client.call.assert_called_once()


async def test_translate_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await translate_document({}, "test-source_language_code", "test-target_language_code", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_parallel_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_parallel_data("test-name", {}, "test-client_token", )
    mock_client.call.assert_called_once()


async def test_update_parallel_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.translate.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_parallel_data("test-name", {}, "test-client_token", )


@pytest.mark.asyncio
async def test_create_parallel_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import create_parallel_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await create_parallel_data("test-name", {}, "test-client_token", description="test-description", encryption_key="test-encryption_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_terminology_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import get_terminology
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await get_terminology("test-name", terminology_data_format="test-terminology_data_format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_terminology_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import import_terminology
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await import_terminology("test-name", "test-merge_strategy", "test-terminology_data", description="test-description", encryption_key="test-encryption_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_parallel_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import list_parallel_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await list_parallel_data(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_terminologies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import list_terminologies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await list_terminologies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_text_translation_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import list_text_translation_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await list_text_translation_jobs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_text_translation_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import start_text_translation_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await start_text_translation_job({}, {}, "test-data_access_role_arn", "test-source_language_code", "test-target_language_codes", "test-client_token", job_name="test-job_name", terminology_names="test-terminology_names", parallel_data_names="test-parallel_data_names", settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_translate_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import translate_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await translate_document("test-document", "test-source_language_code", "test-target_language_code", terminology_names="test-terminology_names", settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_parallel_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.translate import update_parallel_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.translate.async_client", lambda *a, **kw: mock_client)
    await update_parallel_data("test-name", {}, "test-client_token", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()
