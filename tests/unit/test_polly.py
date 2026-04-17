"""Tests for aws_util.polly module."""
from __future__ import annotations

import io
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.polly as polly_mod
from aws_util.polly import (
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_synthesis_result_model():
    result = SynthesisResult(
        audio_stream=b"audio-data",
        content_type="audio/mpeg",
        request_characters=5,
    )
    assert result.audio_stream == b"audio-data"
    assert result.content_type == "audio/mpeg"
    assert result.request_characters == 5


def test_voice_model():
    voice = Voice(
        voice_id="Joanna",
        name="Joanna",
        gender="Female",
        language_code="en-US",
        language_name="US English",
        supported_engines=["neural", "standard"],
    )
    assert voice.voice_id == "Joanna"
    assert voice.gender == "Female"
    assert voice.supported_engines == ["neural", "standard"]


def test_voice_model_defaults():
    voice = Voice(voice_id="Matthew")
    assert voice.name is None
    assert voice.supported_engines == []


def test_speech_synthesis_task_model():
    task = SpeechSynthesisTask(
        task_id="task-123",
        task_status="completed",
        output_uri="s3://bucket/output.mp3",
        voice_id="Joanna",
    )
    assert task.task_id == "task-123"
    assert task.task_status == "completed"


def test_speech_synthesis_task_defaults():
    task = SpeechSynthesisTask()
    assert task.task_id is None
    assert task.speech_mark_types == []


def test_lexicon_attributes_model():
    attrs = LexiconAttributes(
        alphabet="ipa",
        language_code="en-US",
        lexemes_count=10,
        size=500,
    )
    assert attrs.alphabet == "ipa"
    assert attrs.lexemes_count == 10


def test_lexicon_model():
    lex = Lexicon(name="my-lexicon", content="<lexicon>...</lexicon>")
    assert lex.name == "my-lexicon"
    assert lex.content == "<lexicon>...</lexicon>"


def test_lexicon_description_model():
    desc = LexiconDescription(
        name="my-lexicon",
        attributes=LexiconAttributes(alphabet="ipa"),
    )
    assert desc.name == "my-lexicon"
    assert desc.attributes is not None
    assert desc.attributes.alphabet == "ipa"


def test_lexicon_description_defaults():
    desc = LexiconDescription()
    assert desc.name is None
    assert desc.attributes is None


# ---------------------------------------------------------------------------
# synthesize_speech
# ---------------------------------------------------------------------------


def test_synthesize_speech_success(monkeypatch):
    mock_client = MagicMock()
    audio_stream = io.BytesIO(b"fake-mp3-audio")
    mock_client.synthesize_speech.return_value = {
        "AudioStream": audio_stream,
        "ContentType": "audio/mpeg",
        "RequestCharacters": 11,
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    result = synthesize_speech("Hello world", "Joanna", region_name=REGION)
    assert isinstance(result, SynthesisResult)
    assert result.audio_stream == b"fake-mp3-audio"
    assert result.content_type == "audio/mpeg"
    assert result.request_characters == 11


def test_synthesize_speech_with_all_options(monkeypatch):
    mock_client = MagicMock()
    audio_stream = io.BytesIO(b"audio")
    mock_client.synthesize_speech.return_value = {
        "AudioStream": audio_stream,
        "ContentType": "audio/mpeg",
        "RequestCharacters": 5,
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    result = synthesize_speech(
        "Hello",
        "Joanna",
        output_format="ogg_vorbis",
        engine="neural",
        language_code="en-US",
        sample_rate="22050",
        speech_mark_types=["sentence"],
        text_type="ssml",
        lexicon_names=["my-lex"],
        region_name=REGION,
    )
    assert result.audio_stream == b"audio"
    call_kwargs = mock_client.synthesize_speech.call_args[1]
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["SampleRate"] == "22050"
    assert call_kwargs["SpeechMarkTypes"] == ["sentence"]
    assert call_kwargs["TextType"] == "ssml"
    assert call_kwargs["LexiconNames"] == ["my-lex"]
    assert call_kwargs["OutputFormat"] == "ogg_vorbis"


def test_synthesize_speech_minimal_options(monkeypatch):
    mock_client = MagicMock()
    audio_stream = io.BytesIO(b"data")
    mock_client.synthesize_speech.return_value = {
        "AudioStream": audio_stream,
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    result = synthesize_speech("Hi", "Matthew", region_name=REGION)
    assert result.audio_stream == b"data"
    assert result.content_type is None
    assert result.request_characters is None
    call_kwargs = mock_client.synthesize_speech.call_args[1]
    assert "Engine" not in call_kwargs
    assert "LanguageCode" not in call_kwargs
    assert "SampleRate" not in call_kwargs
    assert "SpeechMarkTypes" not in call_kwargs
    assert "TextType" not in call_kwargs
    assert "LexiconNames" not in call_kwargs


def test_synthesize_speech_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.synthesize_speech.side_effect = ClientError(
        {"Error": {"Code": "InvalidParameterException", "Message": "bad param"}},
        "SynthesizeSpeech",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="synthesize_speech failed"):
        synthesize_speech("Hello", "BadVoice", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_voices
# ---------------------------------------------------------------------------


def test_describe_voices_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_voices.return_value = {
        "Voices": [
            {
                "Id": "Joanna",
                "Name": "Joanna",
                "Gender": "Female",
                "LanguageCode": "en-US",
                "LanguageName": "US English",
                "SupportedEngines": ["neural", "standard"],
            },
            {
                "Id": "Matthew",
                "Name": "Matthew",
                "Gender": "Male",
                "LanguageCode": "en-US",
                "LanguageName": "US English",
                "SupportedEngines": ["neural"],
            },
        ],
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    voices = describe_voices(region_name=REGION)
    assert len(voices) == 2
    assert voices[0].voice_id == "Joanna"
    assert voices[1].voice_id == "Matthew"


def test_describe_voices_with_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_voices.return_value = {
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
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    voices = describe_voices(
        language_code="en-US",
        engine="neural",
        include_additional_language_codes=True,
        region_name=REGION,
    )
    assert len(voices) == 1
    call_kwargs = mock_client.describe_voices.call_args[1]
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["IncludeAdditionalLanguageCodes"] is True


def test_describe_voices_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_voices.side_effect = [
        {
            "Voices": [{"Id": "Joanna", "Name": "Joanna"}],
            "NextToken": "token-1",
        },
        {
            "Voices": [{"Id": "Matthew", "Name": "Matthew"}],
        },
    ]
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    voices = describe_voices(region_name=REGION)
    assert len(voices) == 2


def test_describe_voices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_voices.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}},
        "DescribeVoices",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_voices failed"):
        describe_voices(region_name=REGION)


# ---------------------------------------------------------------------------
# list_speech_synthesis_tasks
# ---------------------------------------------------------------------------


def test_list_speech_synthesis_tasks_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_speech_synthesis_tasks.return_value = {
        "SynthesisTasks": [
            {"TaskId": "t-1", "TaskStatus": "completed", "VoiceId": "Joanna"},
            {"TaskId": "t-2", "TaskStatus": "inProgress", "VoiceId": "Matthew"},
        ],
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = list_speech_synthesis_tasks(region_name=REGION)
    assert len(tasks) == 2
    assert tasks[0].task_id == "t-1"
    assert tasks[1].task_status == "inProgress"


def test_list_speech_synthesis_tasks_with_status_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_speech_synthesis_tasks.return_value = {
        "SynthesisTasks": [
            {"TaskId": "t-1", "TaskStatus": "completed"},
        ],
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = list_speech_synthesis_tasks(status="completed", region_name=REGION)
    assert len(tasks) == 1
    call_kwargs = mock_client.list_speech_synthesis_tasks.call_args[1]
    assert call_kwargs["Status"] == "completed"


def test_list_speech_synthesis_tasks_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_speech_synthesis_tasks.side_effect = [
        {
            "SynthesisTasks": [{"TaskId": "t-1", "TaskStatus": "completed"}],
            "NextToken": "tok-1",
        },
        {
            "SynthesisTasks": [{"TaskId": "t-2", "TaskStatus": "completed"}],
        },
    ]
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = list_speech_synthesis_tasks(region_name=REGION)
    assert len(tasks) == 2


def test_list_speech_synthesis_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_speech_synthesis_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceFailure", "Message": "error"}},
        "ListSpeechSynthesisTasks",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_speech_synthesis_tasks failed"):
        list_speech_synthesis_tasks(region_name=REGION)


# ---------------------------------------------------------------------------
# get_speech_synthesis_task
# ---------------------------------------------------------------------------


def test_get_speech_synthesis_task_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_speech_synthesis_task.return_value = {
        "SynthesisTask": {
            "TaskId": "t-1",
            "TaskStatus": "completed",
            "OutputUri": "s3://bucket/output.mp3",
            "OutputFormat": "mp3",
            "VoiceId": "Joanna",
            "Engine": "neural",
            "SampleRate": "22050",
            "SpeechMarkTypes": ["sentence"],
            "RequestCharacters": 100,
            "TextType": "text",
            "LanguageCode": "en-US",
            "TaskStatusReason": None,
        },
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    task = get_speech_synthesis_task("t-1", region_name=REGION)
    assert isinstance(task, SpeechSynthesisTask)
    assert task.task_id == "t-1"
    assert task.task_status == "completed"
    assert task.output_uri == "s3://bucket/output.mp3"
    assert task.engine == "neural"


def test_get_speech_synthesis_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_speech_synthesis_task.side_effect = ClientError(
        {"Error": {"Code": "TaskNotFoundException", "Message": "not found"}},
        "GetSpeechSynthesisTask",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_speech_synthesis_task failed"):
        get_speech_synthesis_task("bad-id", region_name=REGION)


# ---------------------------------------------------------------------------
# start_speech_synthesis_task
# ---------------------------------------------------------------------------


def test_start_speech_synthesis_task_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_speech_synthesis_task.return_value = {
        "SynthesisTask": {
            "TaskId": "t-new",
            "TaskStatus": "scheduled",
            "OutputUri": "s3://bucket/prefix/output.mp3",
            "VoiceId": "Joanna",
            "OutputFormat": "mp3",
        },
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    task = start_speech_synthesis_task(
        text="Hello",
        voice_id="Joanna",
        output_format="mp3",
        output_s3_bucket_name="bucket",
        region_name=REGION,
    )
    assert task.task_id == "t-new"
    assert task.task_status == "scheduled"


def test_start_speech_synthesis_task_all_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_speech_synthesis_task.return_value = {
        "SynthesisTask": {
            "TaskId": "t-all",
            "TaskStatus": "scheduled",
        },
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    task = start_speech_synthesis_task(
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
        sns_topic_arn="arn:aws:sns:us-east-1:123456789012:topic",
        region_name=REGION,
    )
    assert task.task_id == "t-all"
    call_kwargs = mock_client.start_speech_synthesis_task.call_args[1]
    assert call_kwargs["OutputS3KeyPrefix"] == "prefix/"
    assert call_kwargs["Engine"] == "neural"
    assert call_kwargs["LanguageCode"] == "en-US"
    assert call_kwargs["SampleRate"] == "22050"
    assert call_kwargs["TextType"] == "ssml"
    assert call_kwargs["LexiconNames"] == ["lex1"]
    assert call_kwargs["SnsTopicArn"] == "arn:aws:sns:us-east-1:123456789012:topic"


def test_start_speech_synthesis_task_minimal(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_speech_synthesis_task.return_value = {
        "SynthesisTask": {"TaskId": "t-min", "TaskStatus": "scheduled"},
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    task = start_speech_synthesis_task(
        text="Hi",
        voice_id="Matthew",
        output_format="mp3",
        output_s3_bucket_name="bucket",
        region_name=REGION,
    )
    assert task.task_id == "t-min"
    call_kwargs = mock_client.start_speech_synthesis_task.call_args[1]
    assert "OutputS3KeyPrefix" not in call_kwargs
    assert "Engine" not in call_kwargs
    assert "LanguageCode" not in call_kwargs
    assert "SampleRate" not in call_kwargs
    assert "TextType" not in call_kwargs
    assert "LexiconNames" not in call_kwargs
    assert "SnsTopicArn" not in call_kwargs


def test_start_speech_synthesis_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_speech_synthesis_task.side_effect = ClientError(
        {"Error": {"Code": "InvalidS3BucketException", "Message": "bad bucket"}},
        "StartSpeechSynthesisTask",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="start_speech_synthesis_task failed"):
        start_speech_synthesis_task(
            text="Hello",
            voice_id="Joanna",
            output_format="mp3",
            output_s3_bucket_name="bad-bucket",
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_lexicon
# ---------------------------------------------------------------------------


def test_get_lexicon_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lexicon.return_value = {
        "Lexicon": {
            "Name": "my-lex",
            "Content": "<lexicon>data</lexicon>",
        },
        "LexiconAttributes": {
            "Alphabet": "ipa",
            "LanguageCode": "en-US",
            "LexiconArn": "arn:aws:polly:us-east-1:123456789012:lexicon/my-lex",
            "LexemesCount": 5,
            "Size": 200,
        },
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    lexicon, attributes = get_lexicon("my-lex", region_name=REGION)
    assert isinstance(lexicon, Lexicon)
    assert lexicon.name == "my-lex"
    assert lexicon.content == "<lexicon>data</lexicon>"
    assert isinstance(attributes, LexiconAttributes)
    assert attributes.alphabet == "ipa"
    assert attributes.lexemes_count == 5


def test_get_lexicon_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_lexicon.side_effect = ClientError(
        {"Error": {"Code": "LexiconNotFoundException", "Message": "not found"}},
        "GetLexicon",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_lexicon failed"):
        get_lexicon("missing", region_name=REGION)


# ---------------------------------------------------------------------------
# put_lexicon
# ---------------------------------------------------------------------------


def test_put_lexicon_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_lexicon.return_value = {}
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    put_lexicon("my-lex", "<lexicon>data</lexicon>", region_name=REGION)
    mock_client.put_lexicon.assert_called_once_with(
        Name="my-lex", Content="<lexicon>data</lexicon>"
    )


def test_put_lexicon_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_lexicon.side_effect = ClientError(
        {"Error": {"Code": "InvalidLexiconException", "Message": "bad content"}},
        "PutLexicon",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="put_lexicon failed"):
        put_lexicon("bad-lex", "bad-content", region_name=REGION)


# ---------------------------------------------------------------------------
# list_lexicons
# ---------------------------------------------------------------------------


def test_list_lexicons_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lexicons.return_value = {
        "Lexicons": [
            {
                "Name": "lex-1",
                "Attributes": {
                    "Alphabet": "ipa",
                    "LanguageCode": "en-US",
                    "LexemesCount": 3,
                    "Size": 100,
                },
            },
            {
                "Name": "lex-2",
                "Attributes": {
                    "Alphabet": "x-sampa",
                    "LanguageCode": "fr-FR",
                },
            },
        ],
    }
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    descriptions = list_lexicons(region_name=REGION)
    assert len(descriptions) == 2
    assert descriptions[0].name == "lex-1"
    assert descriptions[0].attributes is not None
    assert descriptions[0].attributes.alphabet == "ipa"
    assert descriptions[1].name == "lex-2"


def test_list_lexicons_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lexicons.side_effect = [
        {
            "Lexicons": [{"Name": "lex-1", "Attributes": {}}],
            "NextToken": "tok-1",
        },
        {
            "Lexicons": [{"Name": "lex-2", "Attributes": {}}],
        },
    ]
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    descriptions = list_lexicons(region_name=REGION)
    assert len(descriptions) == 2


def test_list_lexicons_empty(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lexicons.return_value = {"Lexicons": []}
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    descriptions = list_lexicons(region_name=REGION)
    assert descriptions == []


def test_list_lexicons_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lexicons.side_effect = ClientError(
        {"Error": {"Code": "ServiceFailure", "Message": "error"}},
        "ListLexicons",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_lexicons failed"):
        list_lexicons(region_name=REGION)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def test_parse_task():
    from aws_util.polly import _parse_task

    data = {
        "TaskId": "t-1",
        "TaskStatus": "completed",
        "TaskStatusReason": "done",
        "OutputUri": "s3://bucket/out.mp3",
        "OutputFormat": "mp3",
        "TextType": "text",
        "VoiceId": "Joanna",
        "LanguageCode": "en-US",
        "Engine": "neural",
        "SampleRate": "22050",
        "SpeechMarkTypes": ["word"],
        "RequestCharacters": 50,
    }
    task = _parse_task(data)
    assert task.task_id == "t-1"
    assert task.task_status_reason == "done"
    assert task.speech_mark_types == ["word"]
    assert task.request_characters == 50


def test_parse_task_empty():
    from aws_util.polly import _parse_task

    task = _parse_task({})
    assert task.task_id is None
    assert task.speech_mark_types == []


def test_parse_lexicon_attributes():
    from aws_util.polly import _parse_lexicon_attributes

    data = {
        "Alphabet": "ipa",
        "LanguageCode": "en-US",
        "LastModified": "2024-01-01",
        "LexiconArn": "arn:aws:polly:us-east-1:123:lexicon/x",
        "LexemesCount": 10,
        "Size": 300,
    }
    attrs = _parse_lexicon_attributes(data)
    assert attrs.alphabet == "ipa"
    assert attrs.last_modified == "2024-01-01"
    assert attrs.lexicon_arn == "arn:aws:polly:us-east-1:123:lexicon/x"


def test_parse_lexicon_attributes_empty():
    from aws_util.polly import _parse_lexicon_attributes

    attrs = _parse_lexicon_attributes({})
    assert attrs.alphabet is None
    assert attrs.lexemes_count is None


def test_delete_lexicon(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lexicon.return_value = {}
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    delete_lexicon("test-name", region_name=REGION)
    mock_client.delete_lexicon.assert_called_once()


def test_delete_lexicon_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lexicon.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_lexicon",
    )
    monkeypatch.setattr(polly_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete lexicon"):
        delete_lexicon("test-name", region_name=REGION)
