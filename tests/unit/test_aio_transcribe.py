"""Tests for aws_util.aio.transcribe module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.transcribe import (
    TranscriptionJob,
    VocabularyInfo,
    create_vocabulary,
    delete_transcription_job,
    delete_vocabulary,
    get_transcription_job,
    get_vocabulary,
    list_transcription_jobs,
    list_vocabularies,
    start_transcription_job,
    transcribe_and_wait,
    wait_for_transcription_job,
    create_call_analytics_category,
    create_language_model,
    create_medical_vocabulary,
    create_vocabulary_filter,
    delete_call_analytics_category,
    delete_call_analytics_job,
    delete_language_model,
    delete_medical_scribe_job,
    delete_medical_transcription_job,
    delete_medical_vocabulary,
    delete_vocabulary_filter,
    describe_language_model,
    get_call_analytics_category,
    get_call_analytics_job,
    get_medical_scribe_job,
    get_medical_transcription_job,
    get_medical_vocabulary,
    get_vocabulary_filter,
    list_call_analytics_categories,
    list_call_analytics_jobs,
    list_language_models,
    list_medical_scribe_jobs,
    list_medical_transcription_jobs,
    list_medical_vocabularies,
    list_tags_for_resource,
    list_vocabulary_filters,
    start_call_analytics_job,
    start_medical_scribe_job,
    start_medical_transcription_job,
    tag_resource,
    untag_resource,
    update_call_analytics_category,
    update_medical_vocabulary,
    update_vocabulary,
    update_vocabulary_filter,
)


# ---------------------------------------------------------------------------
# start_transcription_job
# ---------------------------------------------------------------------------


async def test_start_transcription_job_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "IN_PROGRESS",
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_transcription_job(
        "job-1", "s3://bucket/audio.mp3",
    )
    assert result.job_name == "job-1"
    assert result.job_status == "IN_PROGRESS"

async def test_start_transcription_job_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_transcription_job failed"):
        await start_transcription_job("job-1", "s3://bucket/audio.mp3")


# ---------------------------------------------------------------------------
# get_transcription_job
# ---------------------------------------------------------------------------


async def test_get_transcription_job_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "COMPLETED",
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
            "Transcript": {"TranscriptFileUri": "s3://bucket/output.json"},
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_transcription_job("job-1")
    assert result.completed is True
    assert result.transcript_uri == "s3://bucket/output.json"


async def test_get_transcription_job_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_transcription_job failed"):
        await get_transcription_job("bad-job")


# ---------------------------------------------------------------------------
# list_transcription_jobs
# ---------------------------------------------------------------------------


async def test_list_transcription_jobs_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJobSummaries": [
            {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
            },
            {
                "TranscriptionJobName": "job-2",
                "TranscriptionJobStatus": "FAILED",
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_transcription_jobs()
    assert len(result) == 2


async def test_list_transcription_jobs_with_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJobSummaries": [
            {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_transcription_jobs(
        status="COMPLETED",
        job_name_contains="job",
        max_results=10,
    )
    assert len(result) == 1


async def test_list_transcription_jobs_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "TranscriptionJobSummaries": [
                {"TranscriptionJobName": "job-1", "TranscriptionJobStatus": "COMPLETED"},
            ],
            "NextToken": "token1",
        },
        {
            "TranscriptionJobSummaries": [
                {"TranscriptionJobName": "job-2", "TranscriptionJobStatus": "COMPLETED"},
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_transcription_jobs()
    assert len(result) == 2


async def test_list_transcription_jobs_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_transcription_jobs failed"):
        await list_transcription_jobs()


# ---------------------------------------------------------------------------
# delete_transcription_job
# ---------------------------------------------------------------------------


async def test_delete_transcription_job_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transcription_job("job-1")
    mock_client.call.assert_called_once_with(
        "DeleteTranscriptionJob",
        TranscriptionJobName="job-1",
    )


async def test_delete_transcription_job_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_transcription_job failed"):
        await delete_transcription_job("bad-job")


# ---------------------------------------------------------------------------
# create_vocabulary
# ---------------------------------------------------------------------------


async def test_create_vocabulary_with_phrases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "PENDING",
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_vocabulary(
        "my-vocab", "en-US", phrases=["hello", "world"],
    )
    assert result.vocabulary_name == "my-vocab"
    assert result.vocabulary_state == "PENDING"


async def test_create_vocabulary_with_file_uri(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "PENDING",
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_vocabulary(
        "my-vocab", "en-US",
        vocabulary_file_uri="s3://bucket/vocab.txt",
    )
    assert result.vocabulary_name == "my-vocab"


async def test_create_vocabulary_no_source_raises() -> None:
    with pytest.raises(ValueError, match="Provide either phrases"):
        await create_vocabulary("my-vocab", "en-US")


async def test_create_vocabulary_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_vocabulary failed"):
        await create_vocabulary(
            "my-vocab", "en-US", phrases=["test"],
        )


# ---------------------------------------------------------------------------
# get_vocabulary
# ---------------------------------------------------------------------------


async def test_get_vocabulary_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "READY",
        "LastModifiedTime": "2024-01-01T00:00:00Z",
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_vocabulary("my-vocab")
    assert result.vocabulary_name == "my-vocab"
    assert result.vocabulary_state == "READY"


async def test_get_vocabulary_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_vocabulary failed"):
        await get_vocabulary("bad-vocab")


# ---------------------------------------------------------------------------
# list_vocabularies
# ---------------------------------------------------------------------------


async def test_list_vocabularies_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Vocabularies": [
            {
                "VocabularyName": "vocab-1",
                "LanguageCode": "en-US",
                "VocabularyState": "READY",
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_vocabularies()
    assert len(result) == 1
    assert result[0].vocabulary_name == "vocab-1"


async def test_list_vocabularies_with_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Vocabularies": [
            {
                "VocabularyName": "vocab-1",
                "LanguageCode": "en-US",
                "VocabularyState": "READY",
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_vocabularies(
        state_equals="READY",
        name_contains="vocab",
        max_results=5,
    )
    assert len(result) == 1


async def test_list_vocabularies_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Vocabularies": [
                {"VocabularyName": "v1", "LanguageCode": "en-US"},
            ],
            "NextToken": "tok1",
        },
        {
            "Vocabularies": [
                {"VocabularyName": "v2", "LanguageCode": "en-US"},
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_vocabularies()
    assert len(result) == 2


async def test_list_vocabularies_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_vocabularies failed"):
        await list_vocabularies()


# ---------------------------------------------------------------------------
# delete_vocabulary
# ---------------------------------------------------------------------------


async def test_delete_vocabulary_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vocabulary("my-vocab")
    mock_client.call.assert_called_once_with(
        "DeleteVocabulary", VocabularyName="my-vocab",
    )


async def test_delete_vocabulary_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_vocabulary failed"):
        await delete_vocabulary("bad-vocab")


# ---------------------------------------------------------------------------
# wait_for_transcription_job
# ---------------------------------------------------------------------------


async def test_wait_for_transcription_job_immediate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "COMPLETED",
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
            "Transcript": {"TranscriptFileUri": "s3://bucket/output.json"},
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )
    result = await wait_for_transcription_job("job-1")
    assert result.completed is True


async def test_wait_for_transcription_job_polls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "IN_PROGRESS",
            }
        },
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )
    result = await wait_for_transcription_job("job-1")
    assert result.job_status == "COMPLETED"


async def test_wait_for_transcription_job_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "FAILED",
            "FailureReason": "Bad audio",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )
    result = await wait_for_transcription_job("job-1")
    assert result.job_status == "FAILED"


async def test_wait_for_transcription_job_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import time as _time

    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "IN_PROGRESS",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )

    call_count = 0

    def fake_monotonic() -> float:
        nonlocal call_count
        call_count += 1
        if call_count <= 1:
            return 0.0
        return 1000.0

    monkeypatch.setattr(_time, "monotonic", fake_monotonic)
    with pytest.raises(TimeoutError, match="did not finish"):
        await wait_for_transcription_job("job-1", timeout=1.0)


# ---------------------------------------------------------------------------
# transcribe_and_wait
# ---------------------------------------------------------------------------


async def test_transcribe_and_wait_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    # First call: StartTranscriptionJob
    # Second call: GetTranscriptionJob (from wait) -> COMPLETED
    mock_client.call.side_effect = [
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "IN_PROGRESS",
                "LanguageCode": "en-US",
                "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
            }
        },
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
                "LanguageCode": "en-US",
                "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
                "Transcript": {"TranscriptFileUri": "s3://bucket/output.json"},
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )
    result = await transcribe_and_wait(
        "job-1",
        "s3://bucket/audio.mp3",
        media_format="mp3",
        output_bucket="out-bucket",
        output_key="transcripts/job-1.json",
        settings={"ShowSpeakerLabels": True},
        poll_interval=1.0,
        timeout=60.0,
    )
    assert result.completed


async def test_transcribe_and_wait_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "IN_PROGRESS",
                "LanguageCode": "en-US",
                "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
            }
        },
        {
            "TranscriptionJob": {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.transcribe.asyncio.sleep", AsyncMock(),
    )
    result = await transcribe_and_wait("job-1", "s3://bucket/audio.mp3")
    assert result.completed


async def test_create_call_analytics_category(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_call_analytics_category("test-category_name", [], )
    mock_client.call.assert_called_once()


async def test_create_call_analytics_category_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_call_analytics_category("test-category_name", [], )


async def test_create_language_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_language_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, )


async def test_create_medical_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", )
    mock_client.call.assert_called_once()


async def test_create_medical_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", )


async def test_create_vocabulary_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_create_vocabulary_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", )


async def test_delete_call_analytics_category(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_call_analytics_category("test-category_name", )
    mock_client.call.assert_called_once()


async def test_delete_call_analytics_category_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_call_analytics_category("test-category_name", )


async def test_delete_call_analytics_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_call_analytics_job("test-call_analytics_job_name", )
    mock_client.call.assert_called_once()


async def test_delete_call_analytics_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_call_analytics_job("test-call_analytics_job_name", )


async def test_delete_language_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_language_model("test-model_name", )
    mock_client.call.assert_called_once()


async def test_delete_language_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_language_model("test-model_name", )


async def test_delete_medical_scribe_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_medical_scribe_job("test-medical_scribe_job_name", )
    mock_client.call.assert_called_once()


async def test_delete_medical_scribe_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_medical_scribe_job("test-medical_scribe_job_name", )


async def test_delete_medical_transcription_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_medical_transcription_job("test-medical_transcription_job_name", )
    mock_client.call.assert_called_once()


async def test_delete_medical_transcription_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_medical_transcription_job("test-medical_transcription_job_name", )


async def test_delete_medical_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_medical_vocabulary("test-vocabulary_name", )
    mock_client.call.assert_called_once()


async def test_delete_medical_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_medical_vocabulary("test-vocabulary_name", )


async def test_delete_vocabulary_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vocabulary_filter("test-vocabulary_filter_name", )
    mock_client.call.assert_called_once()


async def test_delete_vocabulary_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vocabulary_filter("test-vocabulary_filter_name", )


async def test_describe_language_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_language_model("test-model_name", )
    mock_client.call.assert_called_once()


async def test_describe_language_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_language_model("test-model_name", )


async def test_get_call_analytics_category(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_call_analytics_category("test-category_name", )
    mock_client.call.assert_called_once()


async def test_get_call_analytics_category_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_call_analytics_category("test-category_name", )


async def test_get_call_analytics_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_call_analytics_job("test-call_analytics_job_name", )
    mock_client.call.assert_called_once()


async def test_get_call_analytics_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_call_analytics_job("test-call_analytics_job_name", )


async def test_get_medical_scribe_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_medical_scribe_job("test-medical_scribe_job_name", )
    mock_client.call.assert_called_once()


async def test_get_medical_scribe_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_medical_scribe_job("test-medical_scribe_job_name", )


async def test_get_medical_transcription_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_medical_transcription_job("test-medical_transcription_job_name", )
    mock_client.call.assert_called_once()


async def test_get_medical_transcription_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_medical_transcription_job("test-medical_transcription_job_name", )


async def test_get_medical_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_medical_vocabulary("test-vocabulary_name", )
    mock_client.call.assert_called_once()


async def test_get_medical_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_medical_vocabulary("test-vocabulary_name", )


async def test_get_vocabulary_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_vocabulary_filter("test-vocabulary_filter_name", )
    mock_client.call.assert_called_once()


async def test_get_vocabulary_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_vocabulary_filter("test-vocabulary_filter_name", )


async def test_list_call_analytics_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_call_analytics_categories()
    mock_client.call.assert_called_once()


async def test_list_call_analytics_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_call_analytics_categories()


async def test_list_call_analytics_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_call_analytics_jobs()
    mock_client.call.assert_called_once()


async def test_list_call_analytics_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_call_analytics_jobs()


async def test_list_language_models(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_language_models()
    mock_client.call.assert_called_once()


async def test_list_language_models_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_language_models()


async def test_list_medical_scribe_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_medical_scribe_jobs()
    mock_client.call.assert_called_once()


async def test_list_medical_scribe_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_medical_scribe_jobs()


async def test_list_medical_transcription_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_medical_transcription_jobs()
    mock_client.call.assert_called_once()


async def test_list_medical_transcription_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_medical_transcription_jobs()


async def test_list_medical_vocabularies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_medical_vocabularies()
    mock_client.call.assert_called_once()


async def test_list_medical_vocabularies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_medical_vocabularies()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_vocabulary_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vocabulary_filters()
    mock_client.call.assert_called_once()


async def test_list_vocabulary_filters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vocabulary_filters()


async def test_start_call_analytics_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_call_analytics_job("test-call_analytics_job_name", {}, )
    mock_client.call.assert_called_once()


async def test_start_call_analytics_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_call_analytics_job("test-call_analytics_job_name", {}, )


async def test_start_medical_scribe_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_medical_scribe_job("test-medical_scribe_job_name", {}, "test-output_bucket_name", "test-data_access_role_arn", {}, )
    mock_client.call.assert_called_once()


async def test_start_medical_scribe_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_medical_scribe_job("test-medical_scribe_job_name", {}, "test-output_bucket_name", "test-data_access_role_arn", {}, )


async def test_start_medical_transcription_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", {}, "test-output_bucket_name", "test-specialty", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_start_medical_transcription_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", {}, "test-output_bucket_name", "test-specialty", "test-type_value", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_call_analytics_category(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_call_analytics_category("test-category_name", [], )
    mock_client.call.assert_called_once()


async def test_update_call_analytics_category_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_call_analytics_category("test-category_name", [], )


async def test_update_medical_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", )
    mock_client.call.assert_called_once()


async def test_update_medical_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", )


async def test_update_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_vocabulary("test-vocabulary_name", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_update_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_vocabulary("test-vocabulary_name", "test-language_code", )


async def test_update_vocabulary_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_vocabulary_filter("test-vocabulary_filter_name", )
    mock_client.call.assert_called_once()


async def test_update_vocabulary_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.transcribe.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_vocabulary_filter("test-vocabulary_filter_name", )


@pytest.mark.asyncio
async def test_list_transcription_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_transcription_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_transcription_jobs(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vocabularies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_vocabularies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_vocabularies(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_call_analytics_category_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import create_call_analytics_category
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await create_call_analytics_category("test-category_name", "test-rules", tags=[{"Key": "k", "Value": "v"}], input_type="test-input_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_language_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import create_language_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_medical_vocabulary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import create_medical_vocabulary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vocabulary_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import create_vocabulary_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", words="test-words", vocabulary_filter_file_uri="test-vocabulary_filter_file_uri", tags=[{"Key": "k", "Value": "v"}], data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_call_analytics_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_call_analytics_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_call_analytics_categories(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_call_analytics_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_call_analytics_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_call_analytics_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_language_models_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_language_models
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_language_models(status_equals="test-status_equals", name_contains="test-name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_medical_scribe_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_medical_scribe_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_medical_scribe_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_medical_transcription_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_medical_transcription_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_medical_transcription_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_medical_vocabularies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_medical_vocabularies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_medical_vocabularies(next_token="test-next_token", max_results=1, state_equals="test-state_equals", name_contains="test-name_contains", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vocabulary_filters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import list_vocabulary_filters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await list_vocabulary_filters(next_token="test-next_token", max_results=1, name_contains="test-name_contains", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_call_analytics_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import start_call_analytics_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await start_call_analytics_job("test-call_analytics_job_name", "test-media", output_location="test-output_location", output_encryption_kms_key_id="test-output_encryption_kms_key_id", data_access_role_arn="test-data_access_role_arn", settings={}, tags=[{"Key": "k", "Value": "v"}], channel_definitions={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_medical_scribe_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import start_medical_scribe_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await start_medical_scribe_job("test-medical_scribe_job_name", "test-media", "test-output_bucket_name", "test-data_access_role_arn", {}, output_encryption_kms_key_id="test-output_encryption_kms_key_id", kms_encryption_context={}, channel_definitions={}, tags=[{"Key": "k", "Value": "v"}], medical_scribe_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_medical_transcription_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import start_medical_transcription_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", "test-media", "test-output_bucket_name", "test-specialty", "test-type_value", media_sample_rate_hertz="test-media_sample_rate_hertz", media_format="test-media_format", output_key="test-output_key", output_encryption_kms_key_id="test-output_encryption_kms_key_id", kms_encryption_context={}, settings={}, content_identification_type="test-content_identification_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_call_analytics_category_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import update_call_analytics_category
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await update_call_analytics_category("test-category_name", "test-rules", input_type="test-input_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_vocabulary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import update_vocabulary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await update_vocabulary("test-vocabulary_name", "test-language_code", phrases="test-phrases", vocabulary_file_uri="test-vocabulary_file_uri", data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_vocabulary_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.transcribe import update_vocabulary_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.transcribe.async_client", lambda *a, **kw: mock_client)
    await update_vocabulary_filter("test-vocabulary_filter_name", words="test-words", vocabulary_filter_file_uri="test-vocabulary_filter_file_uri", data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()
