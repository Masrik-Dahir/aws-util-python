"""Native async Contact Center Operations — real non-blocking I/O via :mod:`aws_util.aio._engine`.

Async counterpart to :mod:`aws_util.contact_center_ops`.  All models are re-exported
from the sync module.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.contact_center_ops import (
    ContactEventResult,
    LexEscalationResult,
    PostCallAnalysisResult,
)
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "ContactEventResult",
    "LexEscalationResult",
    "PostCallAnalysisResult",
    "connect_contact_event_to_dynamodb",
    "connect_post_call_analyzer",
    "lex_escalation_to_connect",
]

_TRANSCRIBE_POLL_INTERVAL = 15.0
_TRANSCRIBE_MAX_WAIT = 1200.0


# ---------------------------------------------------------------------------
# 1. connect_contact_event_to_dynamodb
# ---------------------------------------------------------------------------


async def connect_contact_event_to_dynamodb(
    stream_name: str,
    table_name: str,
    shard_iterator_type: str = "LATEST",
    max_records: int = 100,
    region_name: str | None = None,
) -> ContactEventResult:
    """Parse Connect CTRs from Kinesis and upsert into DynamoDB (async).

    Args:
        stream_name: Kinesis data stream name carrying Connect CTRs.
        table_name: DynamoDB table name to upsert records into.
        shard_iterator_type: Shard iterator type — ``"LATEST"`` or ``"TRIM_HORIZON"``
            (default ``"LATEST"``).
        max_records: Maximum number of Kinesis records to fetch (default 100).
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`ContactEventResult` with counts and the shard ID that was read.

    Raises:
        AwsUtilError: If the Kinesis stream or DynamoDB table cannot be accessed.
    """
    kinesis = async_client("kinesis", region_name)
    dynamodb = async_client("dynamodb", region_name)

    records_processed = 0
    contacts_upserted = 0

    try:
        shards_resp = await kinesis.call("DescribeStream", StreamName=stream_name)
        shards = shards_resp["StreamDescription"]["Shards"]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"describe_stream({stream_name!r})") from exc

    if not shards:
        return ContactEventResult(
            records_processed=0,
            contacts_upserted=0,
            shard_id="",
        )

    shard = shards[0]
    shard_id = shard["ShardId"]

    try:
        iter_resp = await kinesis.call(
            "GetShardIterator",
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType=shard_iterator_type,
        )
        shard_iterator = iter_resp["ShardIterator"]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_shard_iterator({shard_id!r})") from exc

    try:
        records_resp = await kinesis.call(
            "GetRecords",
            ShardIterator=shard_iterator,
            Limit=max_records,
        )
        raw_records = records_resp.get("Records", [])
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_records(shard={shard_id!r})") from exc

    for raw in raw_records:
        records_processed += 1
        try:
            data = json.loads(raw["Data"])
            contact_id = data.get("ContactId", raw.get("SequenceNumber", "unknown"))
            item: dict[str, Any] = {
                "ContactId": {"S": contact_id},
                "AgentId": {"S": data.get("Agent", {}).get("ARN", "")},
                "CustomerEndpoint": {"S": str(data.get("CustomerEndpoint", {}).get("Address", ""))},
                "InitiationTimestamp": {"S": str(data.get("InitiationTimestamp", ""))},
                "DisconnectTimestamp": {"S": str(data.get("DisconnectTimestamp", ""))},
                "Channel": {"S": data.get("Channel", "")},
                "QueueName": {
                    "S": data.get("Queue", {}).get("Name", "")
                    if isinstance(data.get("Queue"), dict)
                    else ""
                },
                "RawPayload": {"S": json.dumps(data)},
                "IngestedAt": {"N": str(int(time.time()))},
            }
            await dynamodb.call("PutItem", TableName=table_name, Item=item)
            contacts_upserted += 1
        except (RuntimeError, json.JSONDecodeError, KeyError) as exc:
            logger.warning("Error processing CTR record: %s", exc)

    return ContactEventResult(
        records_processed=records_processed,
        contacts_upserted=contacts_upserted,
        shard_id=shard_id,
    )


# ---------------------------------------------------------------------------
# 2. connect_post_call_analyzer
# ---------------------------------------------------------------------------


async def connect_post_call_analyzer(
    bucket: str,
    recording_key: str,
    table_name: str,
    language_code: str = "en-US",
    region_name: str | None = None,
) -> PostCallAnalysisResult:
    """Transcribe a Connect recording, run Comprehend sentiment, store in DynamoDB (async).

    Args:
        bucket: S3 bucket containing the Connect call recording.
        recording_key: S3 object key of the recording.
        table_name: DynamoDB table name to store the analysis results.
        language_code: Language code for transcription (default ``"en-US"``).
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`PostCallAnalysisResult` with transcript text, sentiment, scores, and contact ID.

    Raises:
        AwsUtilError: If transcription fails or DynamoDB write fails.
    """
    transcribe = async_client("transcribe", region_name)
    comprehend = async_client("comprehend", region_name)
    s3 = async_client("s3", region_name)
    dynamodb = async_client("dynamodb", region_name)

    contact_id = recording_key.replace("/", "_").replace(".", "_")
    job_name = f"aws-util-{contact_id}-{int(time.time())}"
    media_uri = f"s3://{bucket}/{recording_key}"

    # Start transcription job
    try:
        await transcribe.call(
            "StartTranscriptionJob",
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            LanguageCode=language_code,
            OutputBucketName=bucket,
            OutputKey=f"transcriptions/{job_name}.json",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"start_transcription_job({job_name!r})") from exc

    # Poll for completion
    transcript_text = ""
    deadline = time.monotonic() + _TRANSCRIBE_MAX_WAIT
    while True:
        try:
            status_resp = await transcribe.call(
                "GetTranscriptionJob", TranscriptionJobName=job_name
            )
            job = status_resp["TranscriptionJob"]
            status = job["TranscriptionJobStatus"]
        except RuntimeError as exc:
            raise wrap_aws_error(exc, f"get_transcription_job({job_name!r})") from exc

        if status == "COMPLETED":
            break
        if status == "FAILED":
            reason = job.get("FailureReason", "unknown")
            raise wrap_aws_error(
                RuntimeError(f"Transcription job failed: {reason}"),
                f"transcription_job({job_name!r})",
            )
        if time.monotonic() + _TRANSCRIBE_POLL_INTERVAL > deadline:
            raise wrap_aws_error(
                TimeoutError(f"Transcription job {job_name!r} timed out"),
                "connect_post_call_analyzer",
            )
        logger.debug(
            "Transcription job %s status: %s — waiting %.0fs",
            job_name,
            status,
            _TRANSCRIBE_POLL_INTERVAL,
        )
        await asyncio.sleep(_TRANSCRIBE_POLL_INTERVAL)

    # Read transcript from S3
    try:
        transcript_key = f"transcriptions/{job_name}.json"
        obj = await s3.call("GetObject", Bucket=bucket, Key=transcript_key)
        raw_bytes: bytes = obj["Body"]
        body = json.loads(raw_bytes if isinstance(raw_bytes, (bytes, str)) else b"")
        results = body.get("results", {})
        transcripts = results.get("transcripts", [{}])
        transcript_text = transcripts[0].get("transcript", "") if transcripts else ""
    except (RuntimeError, json.JSONDecodeError) as exc:
        logger.warning("Could not read transcript from S3: %s", exc)

    # Comprehend sentiment
    sentiment = "NEUTRAL"
    sentiment_scores: dict[str, float] = {}
    if transcript_text:
        try:
            comp_resp = await comprehend.call(
                "DetectSentiment",
                Text=transcript_text[:5000],
                LanguageCode=language_code[:2],
            )
            sentiment = comp_resp.get("Sentiment", "NEUTRAL")
            raw_scores = comp_resp.get("SentimentScore", {})
            sentiment_scores = {k: float(v) for k, v in raw_scores.items()}
        except RuntimeError as exc:
            logger.warning("Comprehend sentiment detection failed: %s", exc)

    # Store in DynamoDB
    try:
        await dynamodb.call(
            "PutItem",
            TableName=table_name,
            Item={
                "ContactId": {"S": contact_id},
                "TranscriptText": {"S": transcript_text},
                "Sentiment": {"S": sentiment},
                "SentimentScores": {"S": json.dumps(sentiment_scores)},
                "LanguageCode": {"S": language_code},
                "JobName": {"S": job_name},
                "RecordingUri": {"S": media_uri},
                "AnalyzedAt": {"N": str(int(time.time()))},
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"put_item into {table_name!r}") from exc

    return PostCallAnalysisResult(
        transcript_text=transcript_text,
        sentiment=sentiment,
        sentiment_scores=sentiment_scores,
        contact_id=contact_id,
    )


# ---------------------------------------------------------------------------
# 3. lex_escalation_to_connect
# ---------------------------------------------------------------------------


async def lex_escalation_to_connect(
    bot_id: str,
    bot_alias_id: str,
    session_id: str,
    locale_id: str,
    instance_id: str,
    contact_flow_id: str,
    destination_phone: str,
    source_phone: str,
    escalation_intent: str,
    region_name: str | None = None,
) -> LexEscalationResult:
    """Detect if a Lex bot session requires handoff and initiate a Connect outbound contact (async).

    Args:
        bot_id: Lex V2 bot identifier.
        bot_alias_id: Lex V2 bot alias identifier.
        session_id: Unique session identifier for the Lex conversation.
        locale_id: Lex locale identifier (e.g. ``"en_US"``).
        instance_id: Amazon Connect instance identifier.
        contact_flow_id: Connect contact flow to invoke on escalation.
        destination_phone: Destination phone number to call (E.164 format).
        source_phone: Caller ID phone number (E.164 format).
        escalation_intent: Intent name that triggers escalation to a live agent.
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`LexEscalationResult` with escalation flag, optional contact ID, and session state.

    Raises:
        AwsUtilError: If Lex session cannot be read or Connect contact fails to start.
    """
    lex = async_client("lexv2-runtime", region_name)
    connect = async_client("connect", region_name)

    try:
        session_resp = await lex.call(
            "GetSession",
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_id,
            sessionId=session_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"lex.get_session(session={session_id!r})") from exc

    session_state = session_resp.get("sessionState", {})
    active_intent = session_state.get("intent", {})
    current_intent_name = active_intent.get("name", "")
    intent_state = active_intent.get("state", "")
    session_attributes = session_resp.get("sessionAttributes", {})

    escalated = current_intent_name == escalation_intent
    if not escalated and session_attributes.get("escalate", "").lower() in ("true", "1", "yes"):
        escalated = True

    contact_id: str | None = None

    if escalated:
        try:
            connect_resp = await connect.call(
                "StartOutboundVoiceContact",
                DestinationPhoneNumber=destination_phone,
                ContactFlowId=contact_flow_id,
                InstanceId=instance_id,
                SourcePhoneNumber=source_phone,
                Attributes={
                    "LexSessionId": session_id,
                    "EscalationIntent": escalation_intent,
                    "CurrentIntent": current_intent_name,
                },
            )
            contact_id = connect_resp.get("ContactId")
            logger.info(
                "Escalated Lex session %s to Connect contact %s (intent=%s)",
                session_id,
                contact_id,
                current_intent_name,
            )
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"connect.start_outbound_voice_contact(session={session_id!r})"
            ) from exc

    return LexEscalationResult(
        escalated=escalated,
        contact_id=contact_id,
        session_state=intent_state,
    )
