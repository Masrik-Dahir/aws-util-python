"""Tests for aws_util.transcribe module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.transcribe as transcribe_mod
from aws_util.transcribe import (
    TranscriptionJob,
    VocabularyInfo,
    _parse_job,
    _parse_vocabulary,
    start_transcription_job,
    get_transcription_job,
    list_transcription_jobs,
    delete_transcription_job,
    create_vocabulary,
    get_vocabulary,
    list_vocabularies,
    delete_vocabulary,
    wait_for_transcription_job,
    transcribe_and_wait,
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_transcription_job_model():
    job = TranscriptionJob(
        job_name="test-job",
        job_status="COMPLETED",
        language_code="en-US",
    )
    assert job.job_name == "test-job"
    assert job.completed is True


def test_transcription_job_not_completed():
    job = TranscriptionJob(
        job_name="test-job",
        job_status="IN_PROGRESS",
    )
    assert job.completed is False


def test_transcription_job_failed():
    job = TranscriptionJob(
        job_name="test-job",
        job_status="FAILED",
        failure_reason="Bad audio",
    )
    assert job.completed is False
    assert job.failure_reason == "Bad audio"


def test_vocabulary_info_model():
    vocab = VocabularyInfo(
        vocabulary_name="my-vocab",
        language_code="en-US",
        vocabulary_state="READY",
    )
    assert vocab.vocabulary_name == "my-vocab"
    assert vocab.vocabulary_state == "READY"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def test_parse_job_full():
    raw = {
        "TranscriptionJobName": "job-1",
        "TranscriptionJobStatus": "COMPLETED",
        "LanguageCode": "en-US",
        "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
        "Transcript": {"TranscriptFileUri": "s3://bucket/output.json"},
        "FailureReason": None,
    }
    job = _parse_job(raw)
    assert job.job_name == "job-1"
    assert job.job_status == "COMPLETED"
    assert job.media_uri == "s3://bucket/audio.mp3"
    assert job.transcript_uri == "s3://bucket/output.json"


def test_parse_job_minimal():
    raw = {
        "TranscriptionJobName": "job-2",
        "TranscriptionJobStatus": "IN_PROGRESS",
    }
    job = _parse_job(raw)
    assert job.job_name == "job-2"
    assert job.media_uri is None
    assert job.transcript_uri is None
    assert job.language_code is None


def test_parse_vocabulary_full():
    raw = {
        "VocabularyName": "vocab-1",
        "LanguageCode": "en-US",
        "VocabularyState": "READY",
        "LastModifiedTime": "2024-01-01T00:00:00Z",
    }
    vocab = _parse_vocabulary(raw)
    assert vocab.vocabulary_name == "vocab-1"
    assert vocab.vocabulary_state == "READY"
    assert vocab.last_modified_time == "2024-01-01T00:00:00Z"


def test_parse_vocabulary_minimal():
    raw = {
        "VocabularyName": "vocab-2",
        "LanguageCode": "fr-FR",
    }
    vocab = _parse_vocabulary(raw)
    assert vocab.vocabulary_name == "vocab-2"
    assert vocab.vocabulary_state is None
    assert vocab.last_modified_time is None


# ---------------------------------------------------------------------------
# start_transcription_job
# ---------------------------------------------------------------------------


def test_start_transcription_job_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_transcription_job.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "IN_PROGRESS",
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
        }
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_transcription_job(
        "job-1", "s3://bucket/audio.mp3", region_name=REGION,
    )
    assert result.job_name == "job-1"
    assert result.job_status == "IN_PROGRESS"

def test_start_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "ConflictException", "Message": "Job exists"}},
        "StartTranscriptionJob",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="start_transcription_job failed"):
        start_transcription_job("job-1", "s3://bucket/audio.mp3", region_name=REGION)


# ---------------------------------------------------------------------------
# get_transcription_job
# ---------------------------------------------------------------------------


def test_get_transcription_job_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transcription_job.return_value = {
        "TranscriptionJob": {
            "TranscriptionJobName": "job-1",
            "TranscriptionJobStatus": "COMPLETED",
            "LanguageCode": "en-US",
            "Media": {"MediaFileUri": "s3://bucket/audio.mp3"},
            "Transcript": {"TranscriptFileUri": "s3://bucket/output.json"},
        }
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_transcription_job("job-1", region_name=REGION)
    assert result.job_name == "job-1"
    assert result.completed is True
    assert result.transcript_uri == "s3://bucket/output.json"


def test_get_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "Not found"}},
        "GetTranscriptionJob",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_transcription_job failed"):
        get_transcription_job("bad-job", region_name=REGION)


# ---------------------------------------------------------------------------
# list_transcription_jobs
# ---------------------------------------------------------------------------


def test_list_transcription_jobs_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_transcription_jobs.return_value = {
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
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_transcription_jobs(region_name=REGION)
    assert len(result) == 2
    assert result[0].job_name == "job-1"


def test_list_transcription_jobs_with_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_transcription_jobs.return_value = {
        "TranscriptionJobSummaries": [
            {
                "TranscriptionJobName": "job-1",
                "TranscriptionJobStatus": "COMPLETED",
            },
        ],
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_transcription_jobs(
        status="COMPLETED",
        job_name_contains="job",
        max_results=10,
        region_name=REGION,
    )
    assert len(result) == 1
    call_kwargs = mock_client.list_transcription_jobs.call_args[1]
    assert call_kwargs["Status"] == "COMPLETED"
    assert call_kwargs["JobNameContains"] == "job"
    assert call_kwargs["MaxResults"] == 10


def test_list_transcription_jobs_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_transcription_jobs.side_effect = [
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
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_transcription_jobs(region_name=REGION)
    assert len(result) == 2


def test_list_transcription_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_transcription_jobs.side_effect = ClientError(
        {"Error": {"Code": "InternalFailureException", "Message": "Internal error"}},
        "ListTranscriptionJobs",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_transcription_jobs failed"):
        list_transcription_jobs(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_transcription_job
# ---------------------------------------------------------------------------


def test_delete_transcription_job_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transcription_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_transcription_job("job-1", region_name=REGION)
    mock_client.delete_transcription_job.assert_called_once_with(
        TranscriptionJobName="job-1",
    )


def test_delete_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "Not found"}},
        "DeleteTranscriptionJob",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_transcription_job failed"):
        delete_transcription_job("bad-job", region_name=REGION)


# ---------------------------------------------------------------------------
# create_vocabulary
# ---------------------------------------------------------------------------


def test_create_vocabulary_with_phrases(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "PENDING",
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_vocabulary(
        "my-vocab", "en-US", phrases=["hello", "world"], region_name=REGION,
    )
    assert result.vocabulary_name == "my-vocab"
    assert result.vocabulary_state == "PENDING"


def test_create_vocabulary_with_file_uri(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "PENDING",
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_vocabulary(
        "my-vocab",
        "en-US",
        vocabulary_file_uri="s3://bucket/vocab.txt",
        region_name=REGION,
    )
    assert result.vocabulary_name == "my-vocab"
    call_kwargs = mock_client.create_vocabulary.call_args[1]
    assert call_kwargs["VocabularyFileUri"] == "s3://bucket/vocab.txt"


def test_create_vocabulary_no_source_raises():
    with pytest.raises(ValueError, match="Provide either phrases"):
        create_vocabulary("my-vocab", "en-US", region_name=REGION)


def test_create_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ConflictException", "Message": "Exists"}},
        "CreateVocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_vocabulary failed"):
        create_vocabulary(
            "my-vocab", "en-US", phrases=["test"], region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_vocabulary
# ---------------------------------------------------------------------------


def test_get_vocabulary_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vocabulary.return_value = {
        "VocabularyName": "my-vocab",
        "LanguageCode": "en-US",
        "VocabularyState": "READY",
        "LastModifiedTime": "2024-01-01T00:00:00Z",
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_vocabulary("my-vocab", region_name=REGION)
    assert result.vocabulary_name == "my-vocab"
    assert result.vocabulary_state == "READY"


def test_get_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "Not found"}},
        "GetVocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_vocabulary failed"):
        get_vocabulary("bad-vocab", region_name=REGION)


# ---------------------------------------------------------------------------
# list_vocabularies
# ---------------------------------------------------------------------------


def test_list_vocabularies_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabularies.return_value = {
        "Vocabularies": [
            {
                "VocabularyName": "vocab-1",
                "LanguageCode": "en-US",
                "VocabularyState": "READY",
            },
        ],
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_vocabularies(region_name=REGION)
    assert len(result) == 1
    assert result[0].vocabulary_name == "vocab-1"


def test_list_vocabularies_with_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabularies.return_value = {
        "Vocabularies": [
            {
                "VocabularyName": "vocab-1",
                "LanguageCode": "en-US",
                "VocabularyState": "READY",
            },
        ],
    }
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_vocabularies(
        state_equals="READY",
        name_contains="vocab",
        max_results=5,
        region_name=REGION,
    )
    assert len(result) == 1
    call_kwargs = mock_client.list_vocabularies.call_args[1]
    assert call_kwargs["StateEquals"] == "READY"
    assert call_kwargs["NameContains"] == "vocab"
    assert call_kwargs["MaxResults"] == 5


def test_list_vocabularies_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabularies.side_effect = [
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
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_vocabularies(region_name=REGION)
    assert len(result) == 2


def test_list_vocabularies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabularies.side_effect = ClientError(
        {"Error": {"Code": "InternalFailureException", "Message": "Error"}},
        "ListVocabularies",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_vocabularies failed"):
        list_vocabularies(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_vocabulary
# ---------------------------------------------------------------------------


def test_delete_vocabulary_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_vocabulary("my-vocab", region_name=REGION)
    mock_client.delete_vocabulary.assert_called_once_with(
        VocabularyName="my-vocab",
    )


def test_delete_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "NotFoundException", "Message": "Not found"}},
        "DeleteVocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_vocabulary failed"):
        delete_vocabulary("bad-vocab", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_transcription_job
# ---------------------------------------------------------------------------


def test_wait_for_transcription_job_already_done(monkeypatch):
    completed = TranscriptionJob(
        job_name="job-1", job_status="COMPLETED",
    )
    monkeypatch.setattr(
        transcribe_mod, "get_transcription_job",
        lambda jid, region_name=None: completed,
    )
    result = wait_for_transcription_job(
        "job-1", timeout=5.0, poll_interval=0.01, region_name=REGION,
    )
    assert result.completed


def test_wait_for_transcription_job_failed(monkeypatch):
    failed = TranscriptionJob(
        job_name="job-1", job_status="FAILED", failure_reason="Bad audio",
    )
    monkeypatch.setattr(
        transcribe_mod, "get_transcription_job",
        lambda jid, region_name=None: failed,
    )
    result = wait_for_transcription_job(
        "job-1", timeout=5.0, poll_interval=0.01, region_name=REGION,
    )
    assert result.job_status == "FAILED"


def test_wait_for_transcription_job_timeout(monkeypatch):
    in_progress = TranscriptionJob(
        job_name="job-1", job_status="IN_PROGRESS",
    )
    monkeypatch.setattr(
        transcribe_mod, "get_transcription_job",
        lambda jid, region_name=None: in_progress,
    )
    with pytest.raises(TimeoutError, match="did not finish"):
        wait_for_transcription_job(
            "job-1", timeout=0.0, poll_interval=0.0, region_name=REGION,
        )


def test_wait_for_transcription_job_polls_then_completes(monkeypatch):
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_get(jid, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return TranscriptionJob(
                job_name=jid, job_status="IN_PROGRESS",
            )
        return TranscriptionJob(
            job_name=jid, job_status="COMPLETED",
        )

    monkeypatch.setattr(transcribe_mod, "get_transcription_job", fake_get)
    result = wait_for_transcription_job(
        "job-1", timeout=10.0, poll_interval=0.001, region_name=REGION,
    )
    assert result.completed


# ---------------------------------------------------------------------------
# transcribe_and_wait
# ---------------------------------------------------------------------------


def test_transcribe_and_wait_success(monkeypatch):
    started = TranscriptionJob(
        job_name="job-1", job_status="IN_PROGRESS",
    )
    completed = TranscriptionJob(
        job_name="job-1", job_status="COMPLETED",
    )
    monkeypatch.setattr(
        transcribe_mod, "start_transcription_job",
        lambda **kw: started,
    )
    monkeypatch.setattr(
        transcribe_mod, "wait_for_transcription_job",
        lambda **kw: completed,
    )
    result = transcribe_and_wait(
        "job-1",
        "s3://bucket/audio.mp3",
        language_code="en-US",
        media_format="mp3",
        output_bucket="out-bucket",
        output_key="transcripts/job-1.json",
        settings={"ShowSpeakerLabels": True},
        poll_interval=1.0,
        timeout=60.0,
        region_name=REGION,
    )
    assert result.completed


def test_transcribe_and_wait_defaults(monkeypatch):
    started = TranscriptionJob(
        job_name="job-1", job_status="IN_PROGRESS",
    )
    completed = TranscriptionJob(
        job_name="job-1", job_status="COMPLETED",
    )
    monkeypatch.setattr(
        transcribe_mod, "start_transcription_job",
        lambda **kw: started,
    )
    monkeypatch.setattr(
        transcribe_mod, "wait_for_transcription_job",
        lambda **kw: completed,
    )
    result = transcribe_and_wait(
        "job-1",
        "s3://bucket/audio.mp3",
        region_name=REGION,
    )
    assert result.completed


def test_create_call_analytics_category(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_call_analytics_category.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    create_call_analytics_category("test-category_name", [], region_name=REGION)
    mock_client.create_call_analytics_category.assert_called_once()


def test_create_call_analytics_category_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_call_analytics_category.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_call_analytics_category",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create call analytics category"):
        create_call_analytics_category("test-category_name", [], region_name=REGION)


def test_create_language_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_language_model.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, region_name=REGION)
    mock_client.create_language_model.assert_called_once()


def test_create_language_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_language_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_language_model",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create language model"):
        create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, region_name=REGION)


def test_create_medical_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_medical_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", region_name=REGION)
    mock_client.create_medical_vocabulary.assert_called_once()


def test_create_medical_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_medical_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_medical_vocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create medical vocabulary"):
        create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", region_name=REGION)


def test_create_vocabulary_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary_filter.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", region_name=REGION)
    mock_client.create_vocabulary_filter.assert_called_once()


def test_create_vocabulary_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vocabulary_filter",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vocabulary filter"):
        create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", region_name=REGION)


def test_delete_call_analytics_category(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_call_analytics_category.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_call_analytics_category("test-category_name", region_name=REGION)
    mock_client.delete_call_analytics_category.assert_called_once()


def test_delete_call_analytics_category_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_call_analytics_category.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_call_analytics_category",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete call analytics category"):
        delete_call_analytics_category("test-category_name", region_name=REGION)


def test_delete_call_analytics_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_call_analytics_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_call_analytics_job("test-call_analytics_job_name", region_name=REGION)
    mock_client.delete_call_analytics_job.assert_called_once()


def test_delete_call_analytics_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_call_analytics_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_call_analytics_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete call analytics job"):
        delete_call_analytics_job("test-call_analytics_job_name", region_name=REGION)


def test_delete_language_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_language_model.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_language_model("test-model_name", region_name=REGION)
    mock_client.delete_language_model.assert_called_once()


def test_delete_language_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_language_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_language_model",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete language model"):
        delete_language_model("test-model_name", region_name=REGION)


def test_delete_medical_scribe_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_scribe_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_medical_scribe_job("test-medical_scribe_job_name", region_name=REGION)
    mock_client.delete_medical_scribe_job.assert_called_once()


def test_delete_medical_scribe_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_scribe_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_medical_scribe_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete medical scribe job"):
        delete_medical_scribe_job("test-medical_scribe_job_name", region_name=REGION)


def test_delete_medical_transcription_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_transcription_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_medical_transcription_job("test-medical_transcription_job_name", region_name=REGION)
    mock_client.delete_medical_transcription_job.assert_called_once()


def test_delete_medical_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_medical_transcription_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete medical transcription job"):
        delete_medical_transcription_job("test-medical_transcription_job_name", region_name=REGION)


def test_delete_medical_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_medical_vocabulary("test-vocabulary_name", region_name=REGION)
    mock_client.delete_medical_vocabulary.assert_called_once()


def test_delete_medical_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_medical_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_medical_vocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete medical vocabulary"):
        delete_medical_vocabulary("test-vocabulary_name", region_name=REGION)


def test_delete_vocabulary_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary_filter.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    delete_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)
    mock_client.delete_vocabulary_filter.assert_called_once()


def test_delete_vocabulary_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vocabulary_filter",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vocabulary filter"):
        delete_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)


def test_describe_language_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_language_model.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    describe_language_model("test-model_name", region_name=REGION)
    mock_client.describe_language_model.assert_called_once()


def test_describe_language_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_language_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_language_model",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe language model"):
        describe_language_model("test-model_name", region_name=REGION)


def test_get_call_analytics_category(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_call_analytics_category.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_call_analytics_category("test-category_name", region_name=REGION)
    mock_client.get_call_analytics_category.assert_called_once()


def test_get_call_analytics_category_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_call_analytics_category.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_call_analytics_category",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get call analytics category"):
        get_call_analytics_category("test-category_name", region_name=REGION)


def test_get_call_analytics_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_call_analytics_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_call_analytics_job("test-call_analytics_job_name", region_name=REGION)
    mock_client.get_call_analytics_job.assert_called_once()


def test_get_call_analytics_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_call_analytics_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_call_analytics_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get call analytics job"):
        get_call_analytics_job("test-call_analytics_job_name", region_name=REGION)


def test_get_medical_scribe_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_scribe_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_medical_scribe_job("test-medical_scribe_job_name", region_name=REGION)
    mock_client.get_medical_scribe_job.assert_called_once()


def test_get_medical_scribe_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_scribe_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_medical_scribe_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get medical scribe job"):
        get_medical_scribe_job("test-medical_scribe_job_name", region_name=REGION)


def test_get_medical_transcription_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_transcription_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_medical_transcription_job("test-medical_transcription_job_name", region_name=REGION)
    mock_client.get_medical_transcription_job.assert_called_once()


def test_get_medical_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_medical_transcription_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get medical transcription job"):
        get_medical_transcription_job("test-medical_transcription_job_name", region_name=REGION)


def test_get_medical_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_medical_vocabulary("test-vocabulary_name", region_name=REGION)
    mock_client.get_medical_vocabulary.assert_called_once()


def test_get_medical_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_medical_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_medical_vocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get medical vocabulary"):
        get_medical_vocabulary("test-vocabulary_name", region_name=REGION)


def test_get_vocabulary_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vocabulary_filter.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    get_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)
    mock_client.get_vocabulary_filter.assert_called_once()


def test_get_vocabulary_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vocabulary_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vocabulary_filter",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get vocabulary filter"):
        get_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)


def test_list_call_analytics_categories(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_call_analytics_categories.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_call_analytics_categories(region_name=REGION)
    mock_client.list_call_analytics_categories.assert_called_once()


def test_list_call_analytics_categories_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_call_analytics_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_call_analytics_categories",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list call analytics categories"):
        list_call_analytics_categories(region_name=REGION)


def test_list_call_analytics_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_call_analytics_jobs.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_call_analytics_jobs(region_name=REGION)
    mock_client.list_call_analytics_jobs.assert_called_once()


def test_list_call_analytics_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_call_analytics_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_call_analytics_jobs",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list call analytics jobs"):
        list_call_analytics_jobs(region_name=REGION)


def test_list_language_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_language_models.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_language_models(region_name=REGION)
    mock_client.list_language_models.assert_called_once()


def test_list_language_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_language_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_language_models",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list language models"):
        list_language_models(region_name=REGION)


def test_list_medical_scribe_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_scribe_jobs.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_medical_scribe_jobs(region_name=REGION)
    mock_client.list_medical_scribe_jobs.assert_called_once()


def test_list_medical_scribe_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_scribe_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_medical_scribe_jobs",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list medical scribe jobs"):
        list_medical_scribe_jobs(region_name=REGION)


def test_list_medical_transcription_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_transcription_jobs.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_medical_transcription_jobs(region_name=REGION)
    mock_client.list_medical_transcription_jobs.assert_called_once()


def test_list_medical_transcription_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_transcription_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_medical_transcription_jobs",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list medical transcription jobs"):
        list_medical_transcription_jobs(region_name=REGION)


def test_list_medical_vocabularies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_vocabularies.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_medical_vocabularies(region_name=REGION)
    mock_client.list_medical_vocabularies.assert_called_once()


def test_list_medical_vocabularies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_medical_vocabularies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_medical_vocabularies",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list medical vocabularies"):
        list_medical_vocabularies(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_vocabulary_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabulary_filters.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    list_vocabulary_filters(region_name=REGION)
    mock_client.list_vocabulary_filters.assert_called_once()


def test_list_vocabulary_filters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vocabulary_filters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vocabulary_filters",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vocabulary filters"):
        list_vocabulary_filters(region_name=REGION)


def test_start_call_analytics_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_call_analytics_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    start_call_analytics_job("test-call_analytics_job_name", {}, region_name=REGION)
    mock_client.start_call_analytics_job.assert_called_once()


def test_start_call_analytics_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_call_analytics_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_call_analytics_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start call analytics job"):
        start_call_analytics_job("test-call_analytics_job_name", {}, region_name=REGION)


def test_start_medical_scribe_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_medical_scribe_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    start_medical_scribe_job("test-medical_scribe_job_name", {}, "test-output_bucket_name", "test-data_access_role_arn", {}, region_name=REGION)
    mock_client.start_medical_scribe_job.assert_called_once()


def test_start_medical_scribe_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_medical_scribe_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_medical_scribe_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start medical scribe job"):
        start_medical_scribe_job("test-medical_scribe_job_name", {}, "test-output_bucket_name", "test-data_access_role_arn", {}, region_name=REGION)


def test_start_medical_transcription_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_medical_transcription_job.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", {}, "test-output_bucket_name", "test-specialty", "test-type_value", region_name=REGION)
    mock_client.start_medical_transcription_job.assert_called_once()


def test_start_medical_transcription_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_medical_transcription_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_medical_transcription_job",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start medical transcription job"):
        start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", {}, "test-output_bucket_name", "test-specialty", "test-type_value", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_call_analytics_category(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_call_analytics_category.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    update_call_analytics_category("test-category_name", [], region_name=REGION)
    mock_client.update_call_analytics_category.assert_called_once()


def test_update_call_analytics_category_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_call_analytics_category.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_call_analytics_category",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update call analytics category"):
        update_call_analytics_category("test-category_name", [], region_name=REGION)


def test_update_medical_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_medical_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    update_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", region_name=REGION)
    mock_client.update_medical_vocabulary.assert_called_once()


def test_update_medical_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_medical_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_medical_vocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update medical vocabulary"):
        update_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", region_name=REGION)


def test_update_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vocabulary.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    update_vocabulary("test-vocabulary_name", "test-language_code", region_name=REGION)
    mock_client.update_vocabulary.assert_called_once()


def test_update_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vocabulary",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vocabulary"):
        update_vocabulary("test-vocabulary_name", "test-language_code", region_name=REGION)


def test_update_vocabulary_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vocabulary_filter.return_value = {}
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    update_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)
    mock_client.update_vocabulary_filter.assert_called_once()


def test_update_vocabulary_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vocabulary_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vocabulary_filter",
    )
    monkeypatch.setattr(transcribe_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vocabulary filter"):
        update_vocabulary_filter("test-vocabulary_filter_name", region_name=REGION)


def test_list_transcription_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_transcription_jobs
    mock_client = MagicMock()
    mock_client.list_transcription_jobs.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_transcription_jobs(max_results=1, region_name="us-east-1")
    mock_client.list_transcription_jobs.assert_called_once()

def test_list_vocabularies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_vocabularies
    mock_client = MagicMock()
    mock_client.list_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_vocabularies(max_results=1, region_name="us-east-1")
    mock_client.list_vocabularies.assert_called_once()

def test_create_call_analytics_category_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import create_call_analytics_category
    mock_client = MagicMock()
    mock_client.create_call_analytics_category.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    create_call_analytics_category("test-category_name", "test-rules", tags=[{"Key": "k", "Value": "v"}], input_type="test-input_type", region_name="us-east-1")
    mock_client.create_call_analytics_category.assert_called_once()

def test_create_language_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import create_language_model
    mock_client = MagicMock()
    mock_client.create_language_model.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    create_language_model("test-language_code", "test-base_model_name", "test-model_name", {}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_language_model.assert_called_once()

def test_create_medical_vocabulary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import create_medical_vocabulary
    mock_client = MagicMock()
    mock_client.create_medical_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    create_medical_vocabulary("test-vocabulary_name", "test-language_code", "test-vocabulary_file_uri", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_medical_vocabulary.assert_called_once()

def test_create_vocabulary_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import create_vocabulary_filter
    mock_client = MagicMock()
    mock_client.create_vocabulary_filter.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    create_vocabulary_filter("test-vocabulary_filter_name", "test-language_code", words="test-words", vocabulary_filter_file_uri="test-vocabulary_filter_file_uri", tags=[{"Key": "k", "Value": "v"}], data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.create_vocabulary_filter.assert_called_once()

def test_list_call_analytics_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_call_analytics_categories
    mock_client = MagicMock()
    mock_client.list_call_analytics_categories.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_call_analytics_categories(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_call_analytics_categories.assert_called_once()

def test_list_call_analytics_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_call_analytics_jobs
    mock_client = MagicMock()
    mock_client.list_call_analytics_jobs.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_call_analytics_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_call_analytics_jobs.assert_called_once()

def test_list_language_models_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_language_models
    mock_client = MagicMock()
    mock_client.list_language_models.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_language_models(status_equals="test-status_equals", name_contains="test-name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_language_models.assert_called_once()

def test_list_medical_scribe_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_medical_scribe_jobs
    mock_client = MagicMock()
    mock_client.list_medical_scribe_jobs.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_medical_scribe_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_medical_scribe_jobs.assert_called_once()

def test_list_medical_transcription_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_medical_transcription_jobs
    mock_client = MagicMock()
    mock_client.list_medical_transcription_jobs.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_medical_transcription_jobs(status="test-status", job_name_contains="test-job_name_contains", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_medical_transcription_jobs.assert_called_once()

def test_list_medical_vocabularies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_medical_vocabularies
    mock_client = MagicMock()
    mock_client.list_medical_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_medical_vocabularies(next_token="test-next_token", max_results=1, state_equals="test-state_equals", name_contains="test-name_contains", region_name="us-east-1")
    mock_client.list_medical_vocabularies.assert_called_once()

def test_list_vocabulary_filters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import list_vocabulary_filters
    mock_client = MagicMock()
    mock_client.list_vocabulary_filters.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    list_vocabulary_filters(next_token="test-next_token", max_results=1, name_contains="test-name_contains", region_name="us-east-1")
    mock_client.list_vocabulary_filters.assert_called_once()

def test_start_call_analytics_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import start_call_analytics_job
    mock_client = MagicMock()
    mock_client.start_call_analytics_job.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    start_call_analytics_job("test-call_analytics_job_name", "test-media", output_location="test-output_location", output_encryption_kms_key_id="test-output_encryption_kms_key_id", data_access_role_arn="test-data_access_role_arn", settings={}, tags=[{"Key": "k", "Value": "v"}], channel_definitions={}, region_name="us-east-1")
    mock_client.start_call_analytics_job.assert_called_once()

def test_start_medical_scribe_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import start_medical_scribe_job
    mock_client = MagicMock()
    mock_client.start_medical_scribe_job.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    start_medical_scribe_job("test-medical_scribe_job_name", "test-media", "test-output_bucket_name", "test-data_access_role_arn", {}, output_encryption_kms_key_id="test-output_encryption_kms_key_id", kms_encryption_context={}, channel_definitions={}, tags=[{"Key": "k", "Value": "v"}], medical_scribe_context={}, region_name="us-east-1")
    mock_client.start_medical_scribe_job.assert_called_once()

def test_start_medical_transcription_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import start_medical_transcription_job
    mock_client = MagicMock()
    mock_client.start_medical_transcription_job.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    start_medical_transcription_job("test-medical_transcription_job_name", "test-language_code", "test-media", "test-output_bucket_name", "test-specialty", "test-type_value", media_sample_rate_hertz="test-media_sample_rate_hertz", media_format="test-media_format", output_key="test-output_key", output_encryption_kms_key_id="test-output_encryption_kms_key_id", kms_encryption_context={}, settings={}, content_identification_type="test-content_identification_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_medical_transcription_job.assert_called_once()

def test_update_call_analytics_category_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import update_call_analytics_category
    mock_client = MagicMock()
    mock_client.update_call_analytics_category.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    update_call_analytics_category("test-category_name", "test-rules", input_type="test-input_type", region_name="us-east-1")
    mock_client.update_call_analytics_category.assert_called_once()

def test_update_vocabulary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import update_vocabulary
    mock_client = MagicMock()
    mock_client.update_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    update_vocabulary("test-vocabulary_name", "test-language_code", phrases="test-phrases", vocabulary_file_uri="test-vocabulary_file_uri", data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.update_vocabulary.assert_called_once()

def test_update_vocabulary_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import update_vocabulary_filter
    mock_client = MagicMock()
    mock_client.update_vocabulary_filter.return_value = {}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    update_vocabulary_filter("test-vocabulary_filter_name", words="test-words", vocabulary_filter_file_uri="test-vocabulary_filter_file_uri", data_access_role_arn="test-data_access_role_arn", region_name="us-east-1")
    mock_client.update_vocabulary_filter.assert_called_once()


def test_start_transcription_job_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import start_transcription_job
    mock_client = MagicMock()
    mock_client.start_transcription_job.return_value = {"TranscriptionJob": {"TranscriptionJobName": "j", "TranscriptionJobStatus": "IN_PROGRESS"}}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: mock_client)
    start_transcription_job("job", "s3://media", "en-US", settings={"ShowSpeakerLabels": True}, region_name="us-east-1")
    mock_client.start_transcription_job.assert_called_once()


def test_start_transcription_job_all_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.transcribe import start_transcription_job
    m = MagicMock(); m.start_transcription_job.return_value = {"TranscriptionJob": {"TranscriptionJobName": "j", "TranscriptionJobStatus": "IN_PROGRESS"}}
    monkeypatch.setattr("aws_util.transcribe.get_client", lambda *a, **kw: m)
    start_transcription_job("j", "s3://m", "en-US", media_format="mp3", output_bucket="b", output_key="k", settings={}, region_name="us-east-1")
