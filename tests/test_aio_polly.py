"""Tests for aws_util.aio.polly module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.polly import (
    Lexicon,
    LexiconAttributes,
    LexiconDescription,
    SpeechSynthesisTask,
    SynthesisResult,
    Voice,
    describe_voices,
    get_lexicon,
    get_speech_synthesis_task,
    list_lexicons,
    list_speech_synthesis_tasks,
    put_lexicon,
    start_speech_synthesis_task,
    synthesize_speech,
    delete_lexicon,
)


# ---------------------------------------------------------------------------
# synthesize_speech
# ---------------------------------------------------------------------------


async def test_synthesize_speech_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AudioStream": b"fake-audio",
        "ContentType": "audio/mpeg",
        "RequestCharacters": 5,
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await synthesize_speech("Hello", "Joanna")
    assert isinstance(result, SynthesisResult)
    assert result.audio_stream == b"fake-audio"
    assert result.content_type == "audio/mpeg"
    assert result.request_characters == 5


async def test_synthesize_speech_with_all_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AudioStream": b"audio",
        "ContentType": "audio/ogg",
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await synthesize_speech(
        "Hello",
        "Joanna",
        output_format="ogg_vorbis",
        engine="neural",
        language_code="en-US",
        sample_rate="22050",
        speech_mark_types=["sentence"],
        text_type="ssml",
        lexicon_names=["my-lex"],
        region_name="us-west-2",
    )
    assert result.audio_stream == b"audio"
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["SampleRate"] == "22050"
    assert call_kwargs["SpeechMarkTypes"] == ["sentence"]
    assert call_kwargs["TextType"] == "ssml"
    assert call_kwargs["LexiconNames"] == ["my-lex"]


async def test_synthesize_speech_no_optional_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"AudioStream": b"data"}
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await synthesize_speech("Hi", "Matthew")
    assert result.audio_stream == b"data"
    assert result.content_type is None
    call_kwargs = mock_client.call.call_args[1]
    assert "Engine" not in call_kwargs
    assert "LanguageCode" not in call_kwargs
    assert "SampleRate" not in call_kwargs
    assert "SpeechMarkTypes" not in call_kwargs
    assert "TextType" not in call_kwargs
    assert "LexiconNames" not in call_kwargs


async def test_synthesize_speech_stream_object(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a stream-like AudioStream is read correctly."""
    import io

    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AudioStream": io.BytesIO(b"streamed-audio"),
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await synthesize_speech("Test", "Joanna")
    assert result.audio_stream == b"streamed-audio"


async def test_synthesize_speech_non_bytes_audio(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that non-bytes, non-stream AudioStream falls back to empty bytes."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AudioStream": 12345,
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await synthesize_speech("Test", "Joanna")
    assert result.audio_stream == b""


async def test_synthesize_speech_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="synthesize_speech failed"):
        await synthesize_speech("Hello", "Joanna")


# ---------------------------------------------------------------------------
# describe_voices
# ---------------------------------------------------------------------------


async def test_describe_voices_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Voices": [
            {
                "Id": "Joanna",
                "Name": "Joanna",
                "Gender": "Female",
                "LanguageCode": "en-US",
                "LanguageName": "US English",
                "SupportedEngines": ["neural"],
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    voices = await describe_voices()
    assert len(voices) == 1
    assert isinstance(voices[0], Voice)
    assert voices[0].voice_id == "Joanna"


async def test_describe_voices_with_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Voices": [{"Id": "Joanna"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_voices(
        language_code="en-US",
        engine="neural",
        include_additional_language_codes=True,
        region_name="eu-west-1",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["IncludeAdditionalLanguageCodes"] is True


async def test_describe_voices_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Voices": [{"Id": "Joanna"}],
            "NextToken": "tok-1",
        },
        {
            "Voices": [{"Id": "Matthew"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    voices = await describe_voices()
    assert len(voices) == 2


async def test_describe_voices_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_voices failed"):
        await describe_voices()


# ---------------------------------------------------------------------------
# list_speech_synthesis_tasks
# ---------------------------------------------------------------------------


async def test_list_speech_synthesis_tasks_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTasks": [
            {"TaskId": "t-1", "TaskStatus": "completed"},
            {"TaskId": "t-2", "TaskStatus": "inProgress"},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    tasks = await list_speech_synthesis_tasks()
    assert len(tasks) == 2
    assert tasks[0].task_id == "t-1"


async def test_list_speech_synthesis_tasks_with_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTasks": [{"TaskId": "t-1", "TaskStatus": "completed"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    tasks = await list_speech_synthesis_tasks(status="completed")
    assert len(tasks) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Status"] == "completed"


async def test_list_speech_synthesis_tasks_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "SynthesisTasks": [{"TaskId": "t-1", "TaskStatus": "completed"}],
            "NextToken": "tok-1",
        },
        {
            "SynthesisTasks": [{"TaskId": "t-2", "TaskStatus": "completed"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    tasks = await list_speech_synthesis_tasks()
    assert len(tasks) == 2


async def test_list_speech_synthesis_tasks_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_speech_synthesis_tasks failed"):
        await list_speech_synthesis_tasks()


# ---------------------------------------------------------------------------
# get_speech_synthesis_task
# ---------------------------------------------------------------------------


async def test_get_speech_synthesis_task_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTask": {
            "TaskId": "t-1",
            "TaskStatus": "completed",
            "OutputUri": "s3://bucket/out.mp3",
            "VoiceId": "Joanna",
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    task = await get_speech_synthesis_task("t-1")
    assert isinstance(task, SpeechSynthesisTask)
    assert task.task_id == "t-1"
    assert task.task_status == "completed"


async def test_get_speech_synthesis_task_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_speech_synthesis_task failed"):
        await get_speech_synthesis_task("bad-id")


# ---------------------------------------------------------------------------
# start_speech_synthesis_task
# ---------------------------------------------------------------------------


async def test_start_speech_synthesis_task_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTask": {
            "TaskId": "t-new",
            "TaskStatus": "scheduled",
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    task = await start_speech_synthesis_task(
        text="Hello",
        voice_id="Joanna",
        output_format="mp3",
        output_s3_bucket_name="bucket",
    )
    assert task.task_id == "t-new"
    assert task.task_status == "scheduled"


async def test_start_speech_synthesis_task_all_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTask": {"TaskId": "t-all", "TaskStatus": "scheduled"},
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_speech_synthesis_task(
        text="Hello",
        voice_id="Joanna",
        output_format="mp3",
        output_s3_bucket_name="bucket",
        output_s3_key_prefix="prefix/",
        engine="neural",
        language_code="en-US",
        sample_rate="22050",
        text_type="ssml",
        lexicon_names=["lex1"],
        sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
        region_name="us-west-2",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["OutputS3KeyPrefix"] == "prefix/"
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["SampleRate"] == "22050"
    assert call_kwargs["TextType"] == "ssml"
    assert call_kwargs["LexiconNames"] == ["lex1"]
    assert call_kwargs["SnsTopicArn"] == "arn:aws:sns:us-east-1:123:topic"


async def test_start_speech_synthesis_task_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SynthesisTask": {"TaskId": "t-min", "TaskStatus": "scheduled"},
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_speech_synthesis_task(
        text="Hi",
        voice_id="Matthew",
        output_format="mp3",
        output_s3_bucket_name="bucket",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "OutputS3KeyPrefix" not in call_kwargs
    assert "Engine" not in call_kwargs
    assert "LanguageCode" not in call_kwargs
    assert "SampleRate" not in call_kwargs
    assert "TextType" not in call_kwargs
    assert "LexiconNames" not in call_kwargs
    assert "SnsTopicArn" not in call_kwargs


async def test_start_speech_synthesis_task_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_speech_synthesis_task failed"):
        await start_speech_synthesis_task(
            text="Hello",
            voice_id="Joanna",
            output_format="mp3",
            output_s3_bucket_name="bucket",
        )


# ---------------------------------------------------------------------------
# get_lexicon
# ---------------------------------------------------------------------------


async def test_get_lexicon_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Lexicon": {
            "Name": "my-lex",
            "Content": "<lexicon>data</lexicon>",
        },
        "LexiconAttributes": {
            "Alphabet": "ipa",
            "LanguageCode": "en-US",
            "LexiconArn": "arn:aws:polly:us-east-1:123:lexicon/my-lex",
            "LexemesCount": 5,
            "Size": 200,
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    lexicon, attributes = await get_lexicon("my-lex")
    assert isinstance(lexicon, Lexicon)
    assert lexicon.name == "my-lex"
    assert isinstance(attributes, LexiconAttributes)
    assert attributes.alphabet == "ipa"


async def test_get_lexicon_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_lexicon failed"):
        await get_lexicon("missing")


# ---------------------------------------------------------------------------
# put_lexicon
# ---------------------------------------------------------------------------


async def test_put_lexicon_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_lexicon("my-lex", "<lexicon>data</lexicon>")
    mock_client.call.assert_called_once_with(
        "PutLexicon", Name="my-lex", Content="<lexicon>data</lexicon>"
    )


async def test_put_lexicon_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="put_lexicon failed"):
        await put_lexicon("bad-lex", "bad-content")


# ---------------------------------------------------------------------------
# list_lexicons
# ---------------------------------------------------------------------------


async def test_list_lexicons_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Lexicons": [
            {
                "Name": "lex-1",
                "Attributes": {
                    "Alphabet": "ipa",
                    "LanguageCode": "en-US",
                    "LexemesCount": 3,
                },
            },
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    descriptions = await list_lexicons()
    assert len(descriptions) == 1
    assert isinstance(descriptions[0], LexiconDescription)
    assert descriptions[0].name == "lex-1"


async def test_list_lexicons_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Lexicons": [{"Name": "lex-1", "Attributes": {}}],
            "NextToken": "tok-1",
        },
        {
            "Lexicons": [{"Name": "lex-2", "Attributes": {}}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    descriptions = await list_lexicons()
    assert len(descriptions) == 2


async def test_list_lexicons_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Lexicons": []}
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    descriptions = await list_lexicons()
    assert descriptions == []


async def test_list_lexicons_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_lexicons failed"):
        await list_lexicons()


# ---------------------------------------------------------------------------
# Re-exported models
# ---------------------------------------------------------------------------


def test_reexported_models() -> None:
    """Ensure all models are re-exported from the async module."""
    assert SynthesisResult is not None
    assert Voice is not None
    assert SpeechSynthesisTask is not None
    assert Lexicon is not None
    assert LexiconAttributes is not None
    assert LexiconDescription is not None


async def test_delete_lexicon(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_lexicon("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_lexicon_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.polly.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_lexicon("test-name", )
