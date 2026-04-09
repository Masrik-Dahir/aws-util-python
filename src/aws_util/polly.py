"""aws_util.polly --- Amazon Polly text-to-speech utilities.

Provides high-level helpers for synthesizing speech, managing voices,
handling asynchronous speech synthesis tasks, and managing pronunciation
lexicons.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "Lexicon",
    "LexiconAttributes",
    "LexiconDescription",
    "SpeechSynthesisTask",
    "SynthesisResult",
    "Voice",
    "delete_lexicon",
    "describe_voices",
    "get_lexicon",
    "get_speech_synthesis_task",
    "list_lexicons",
    "list_speech_synthesis_tasks",
    "put_lexicon",
    "start_speech_synthesis_task",
    "synthesize_speech",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class SynthesisResult(BaseModel):
    """The result of a synchronous speech synthesis call."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    audio_stream: bytes
    content_type: str | None = None
    request_characters: int | None = None


class Voice(BaseModel):
    """A voice available in Amazon Polly."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    voice_id: str
    name: str | None = None
    gender: str | None = None
    language_code: str | None = None
    language_name: str | None = None
    supported_engines: list[str] = []


class SpeechSynthesisTask(BaseModel):
    """Metadata for an asynchronous speech synthesis task."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    task_id: str | None = None
    task_status: str | None = None
    task_status_reason: str | None = None
    output_uri: str | None = None
    output_format: str | None = None
    text_type: str | None = None
    voice_id: str | None = None
    language_code: str | None = None
    engine: str | None = None
    sample_rate: str | None = None
    speech_mark_types: list[str] = []
    request_characters: int | None = None


class LexiconAttributes(BaseModel):
    """Attributes describing a pronunciation lexicon."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    alphabet: str | None = None
    language_code: str | None = None
    last_modified: Any = None
    lexicon_arn: str | None = None
    lexemes_count: int | None = None
    size: int | None = None


class Lexicon(BaseModel):
    """A pronunciation lexicon with its content."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str | None = None
    content: str | None = None


class LexiconDescription(BaseModel):
    """Summary description of a pronunciation lexicon."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str | None = None
    attributes: LexiconAttributes | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def synthesize_speech(
    text: str,
    voice_id: str,
    output_format: str = "mp3",
    engine: str | None = None,
    language_code: str | None = None,
    sample_rate: str | None = None,
    speech_mark_types: list[str] | None = None,
    text_type: str | None = None,
    lexicon_names: list[str] | None = None,
    region_name: str | None = None,
) -> SynthesisResult:
    """Synthesize speech from text and return raw audio bytes.

    Args:
        text: The input text to synthesize (plain text or SSML depending
            on *text_type*).
        voice_id: Polly voice ID, e.g. ``"Joanna"``, ``"Matthew"``.
        output_format: Audio format: ``"mp3"``, ``"ogg_vorbis"``, or
            ``"pcm"``.  Defaults to ``"mp3"``.
        engine: Speech engine: ``"standard"`` or ``"neural"``.
        language_code: BCP-47 language code for bilingual voices.
        sample_rate: Audio sample rate in Hz (e.g. ``"22050"``).
        speech_mark_types: List of speech mark types to include.
        text_type: ``"text"`` or ``"ssml"``.
        lexicon_names: Pronunciation lexicons to apply.
        region_name: AWS region override.

    Returns:
        A :class:`SynthesisResult` containing the audio bytes, content
        type, and character count.

    Raises:
        RuntimeError: If the synthesis call fails.
    """
    client = get_client("polly", region_name)
    kwargs: dict[str, Any] = {
        "Text": text,
        "VoiceId": voice_id,
        "OutputFormat": output_format,
    }
    if engine is not None:
        kwargs["Engine"] = engine
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    if sample_rate is not None:
        kwargs["SampleRate"] = sample_rate
    if speech_mark_types is not None:
        kwargs["SpeechMarkTypes"] = speech_mark_types
    if text_type is not None:
        kwargs["TextType"] = text_type
    if lexicon_names is not None:
        kwargs["LexiconNames"] = lexicon_names
    try:
        resp = client.synthesize_speech(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "synthesize_speech failed") from exc
    audio_bytes = resp["AudioStream"].read()
    return SynthesisResult(
        audio_stream=audio_bytes,
        content_type=resp.get("ContentType"),
        request_characters=resp.get("RequestCharacters"),
    )


def describe_voices(
    language_code: str | None = None,
    engine: str | None = None,
    include_additional_language_codes: bool = False,
    region_name: str | None = None,
) -> list[Voice]:
    """List available Polly voices, optionally filtered by language or engine.

    Args:
        language_code: Filter voices by BCP-47 language code.
        engine: Filter by engine type (``"standard"`` or ``"neural"``).
        include_additional_language_codes: Whether to include additional
            language codes each voice supports.
        region_name: AWS region override.

    Returns:
        A list of :class:`Voice` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    voices: list[Voice] = []
    kwargs: dict[str, Any] = {
        "IncludeAdditionalLanguageCodes": include_additional_language_codes,
    }
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    if engine is not None:
        kwargs["Engine"] = engine
    try:
        while True:
            resp = client.describe_voices(**kwargs)
            for v in resp.get("Voices", []):
                voices.append(
                    Voice(
                        voice_id=v["Id"],
                        name=v.get("Name"),
                        gender=v.get("Gender"),
                        language_code=v.get("LanguageCode"),
                        language_name=v.get("LanguageName"),
                        supported_engines=v.get("SupportedEngines", []),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_voices failed") from exc
    return voices


def list_speech_synthesis_tasks(
    status: str | None = None,
    region_name: str | None = None,
) -> list[SpeechSynthesisTask]:
    """List asynchronous speech synthesis tasks.

    Args:
        status: Filter by task status (e.g. ``"completed"``,
            ``"inProgress"``, ``"scheduled"``, ``"failed"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`SpeechSynthesisTask` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    tasks: list[SpeechSynthesisTask] = []
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    try:
        while True:
            resp = client.list_speech_synthesis_tasks(**kwargs)
            for t in resp.get("SynthesisTasks", []):
                tasks.append(_parse_task(t))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_speech_synthesis_tasks failed") from exc
    return tasks


def get_speech_synthesis_task(
    task_id: str,
    region_name: str | None = None,
) -> SpeechSynthesisTask:
    """Get details of an asynchronous speech synthesis task.

    Args:
        task_id: The task identifier returned by
            :func:`start_speech_synthesis_task`.
        region_name: AWS region override.

    Returns:
        A :class:`SpeechSynthesisTask` with current task status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    try:
        resp = client.get_speech_synthesis_task(TaskId=task_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_speech_synthesis_task failed for task {task_id!r}") from exc
    return _parse_task(resp["SynthesisTask"])


def start_speech_synthesis_task(
    text: str,
    voice_id: str,
    output_format: str,
    output_s3_bucket_name: str,
    output_s3_key_prefix: str | None = None,
    engine: str | None = None,
    language_code: str | None = None,
    sample_rate: str | None = None,
    text_type: str | None = None,
    lexicon_names: list[str] | None = None,
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> SpeechSynthesisTask:
    """Start an asynchronous speech synthesis task.

    The synthesized audio is saved to the specified S3 bucket.

    Args:
        text: Input text to synthesize.
        voice_id: Polly voice ID.
        output_format: Audio format (``"mp3"``, ``"ogg_vorbis"``, or
            ``"pcm"``).
        output_s3_bucket_name: S3 bucket for output audio.
        output_s3_key_prefix: Optional S3 key prefix for output.
        engine: Speech engine (``"standard"`` or ``"neural"``).
        language_code: BCP-47 language code.
        sample_rate: Audio sample rate in Hz.
        text_type: ``"text"`` or ``"ssml"``.
        lexicon_names: Pronunciation lexicons to apply.
        sns_topic_arn: SNS topic ARN for task completion notifications.
        region_name: AWS region override.

    Returns:
        A :class:`SpeechSynthesisTask` with the new task details.

    Raises:
        RuntimeError: If the task submission fails.
    """
    client = get_client("polly", region_name)
    kwargs: dict[str, Any] = {
        "Text": text,
        "VoiceId": voice_id,
        "OutputFormat": output_format,
        "OutputS3BucketName": output_s3_bucket_name,
    }
    if output_s3_key_prefix is not None:
        kwargs["OutputS3KeyPrefix"] = output_s3_key_prefix
    if engine is not None:
        kwargs["Engine"] = engine
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    if sample_rate is not None:
        kwargs["SampleRate"] = sample_rate
    if text_type is not None:
        kwargs["TextType"] = text_type
    if lexicon_names is not None:
        kwargs["LexiconNames"] = lexicon_names
    if sns_topic_arn is not None:
        kwargs["SnsTopicArn"] = sns_topic_arn
    try:
        resp = client.start_speech_synthesis_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_speech_synthesis_task failed") from exc
    return _parse_task(resp["SynthesisTask"])


def get_lexicon(
    name: str,
    region_name: str | None = None,
) -> tuple[Lexicon, LexiconAttributes]:
    """Retrieve a pronunciation lexicon by name.

    Args:
        name: Name of the lexicon.
        region_name: AWS region override.

    Returns:
        A tuple of (:class:`Lexicon`, :class:`LexiconAttributes`).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    try:
        resp = client.get_lexicon(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_lexicon failed for {name!r}") from exc
    lex_data = resp.get("Lexicon", {})
    attr_data = resp.get("LexiconAttributes", {})
    lexicon = Lexicon(
        name=lex_data.get("Name"),
        content=lex_data.get("Content"),
    )
    attributes = _parse_lexicon_attributes(attr_data)
    return lexicon, attributes


def put_lexicon(
    name: str,
    content: str,
    region_name: str | None = None,
) -> None:
    """Create or update a pronunciation lexicon.

    Args:
        name: Name of the lexicon.
        content: The PLS (Pronunciation Lexicon Specification) XML content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    try:
        client.put_lexicon(Name=name, Content=content)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"put_lexicon failed for {name!r}") from exc


def list_lexicons(
    region_name: str | None = None,
) -> list[LexiconDescription]:
    """List all pronunciation lexicons in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`LexiconDescription` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    descriptions: list[LexiconDescription] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_lexicons(**kwargs)
            for lex in resp.get("Lexicons", []):
                attr_data = lex.get("Attributes", {})
                descriptions.append(
                    LexiconDescription(
                        name=lex.get("Name"),
                        attributes=_parse_lexicon_attributes(attr_data),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_lexicons failed") from exc
    return descriptions


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_task(data: dict[str, Any]) -> SpeechSynthesisTask:
    """Convert a raw API task dict to a :class:`SpeechSynthesisTask`."""
    return SpeechSynthesisTask(
        task_id=data.get("TaskId"),
        task_status=data.get("TaskStatus"),
        task_status_reason=data.get("TaskStatusReason"),
        output_uri=data.get("OutputUri"),
        output_format=data.get("OutputFormat"),
        text_type=data.get("TextType"),
        voice_id=data.get("VoiceId"),
        language_code=data.get("LanguageCode"),
        engine=data.get("Engine"),
        sample_rate=data.get("SampleRate"),
        speech_mark_types=data.get("SpeechMarkTypes", []),
        request_characters=data.get("RequestCharacters"),
    )


def _parse_lexicon_attributes(data: dict[str, Any]) -> LexiconAttributes:
    """Convert a raw API attributes dict to a :class:`LexiconAttributes`."""
    return LexiconAttributes(
        alphabet=data.get("Alphabet"),
        language_code=data.get("LanguageCode"),
        last_modified=data.get("LastModified"),
        lexicon_arn=data.get("LexiconArn"),
        lexemes_count=data.get("LexemesCount"),
        size=data.get("Size"),
    )


def delete_lexicon(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete lexicon.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("polly", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_lexicon(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete lexicon") from exc
    return None
