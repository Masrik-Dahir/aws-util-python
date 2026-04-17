"""Native async Amazon Polly utilities using the async engine."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.polly import (
    Lexicon,
    LexiconAttributes,
    LexiconDescription,
    SpeechSynthesisTask,
    SynthesisResult,
    Voice,
    _parse_lexicon_attributes,
    _parse_task,
)

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


async def synthesize_speech(
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
    client = async_client("polly", region_name)
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
        resp = await client.call("SynthesizeSpeech", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "synthesize_speech failed") from exc
    audio_data = resp.get("AudioStream", b"")
    if hasattr(audio_data, "read"):
        audio_data = audio_data.read()
    return SynthesisResult(
        audio_stream=audio_data if isinstance(audio_data, bytes) else b"",
        content_type=resp.get("ContentType"),
        request_characters=resp.get("RequestCharacters"),
    )


async def describe_voices(
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
    client = async_client("polly", region_name)
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
            resp = await client.call("DescribeVoices", **kwargs)
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
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_voices failed") from exc
    return voices


async def list_speech_synthesis_tasks(
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
    client = async_client("polly", region_name)
    tasks: list[SpeechSynthesisTask] = []
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    try:
        while True:
            resp = await client.call("ListSpeechSynthesisTasks", **kwargs)
            for t in resp.get("SynthesisTasks", []):
                tasks.append(_parse_task(t))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_speech_synthesis_tasks failed") from exc
    return tasks


async def get_speech_synthesis_task(
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
    client = async_client("polly", region_name)
    try:
        resp = await client.call("GetSpeechSynthesisTask", TaskId=task_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_speech_synthesis_task failed for task {task_id!r}") from exc
    return _parse_task(resp["SynthesisTask"])


async def start_speech_synthesis_task(
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
    client = async_client("polly", region_name)
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
        resp = await client.call("StartSpeechSynthesisTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "start_speech_synthesis_task failed") from exc
    return _parse_task(resp["SynthesisTask"])


async def get_lexicon(
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
    client = async_client("polly", region_name)
    try:
        resp = await client.call("GetLexicon", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_lexicon failed for {name!r}") from exc
    lex_data = resp.get("Lexicon", {})
    attr_data = resp.get("LexiconAttributes", {})
    lexicon = Lexicon(
        name=lex_data.get("Name"),
        content=lex_data.get("Content"),
    )
    attributes = _parse_lexicon_attributes(attr_data)
    return lexicon, attributes


async def put_lexicon(
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
    client = async_client("polly", region_name)
    try:
        await client.call("PutLexicon", Name=name, Content=content)
    except Exception as exc:
        raise wrap_aws_error(exc, f"put_lexicon failed for {name!r}") from exc


async def list_lexicons(
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
    client = async_client("polly", region_name)
    descriptions: list[LexiconDescription] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListLexicons", **kwargs)
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
    except Exception as exc:
        raise wrap_aws_error(exc, "list_lexicons failed") from exc
    return descriptions


async def delete_lexicon(
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
    client = async_client("polly", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteLexicon", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete lexicon") from exc
    return None
