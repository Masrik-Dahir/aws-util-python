"""Contact Center Operations utilities for AWS Connect, Lex, Transcribe, and Comprehend.

Provides multi-service helpers for contact center workflows:

- **connect_contact_event_to_dynamodb** — Parse Connect CTRs from Kinesis, upsert into DynamoDB.
- **connect_post_call_analyzer** — Transcribe + Comprehend sentiment analysis stored in DynamoDB.
- **lex_escalation_to_connect** — Detect Lex escalation intent and start a Connect outbound contact.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
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

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ContactEventResult(BaseModel):
    """Result of processing Connect contact trace records from Kinesis into DynamoDB."""

    model_config = ConfigDict(frozen=True)

    records_processed: int
    contacts_upserted: int
    shard_id: str


class PostCallAnalysisResult(BaseModel):
    """Result of post-call analysis: transcript + sentiment stored in DynamoDB."""

    model_config = ConfigDict(frozen=True)

    transcript_text: str
    sentiment: str
    sentiment_scores: dict[str, float]
    contact_id: str


class LexEscalationResult(BaseModel):
    """Result of Lex bot interaction with optional Connect escalation."""

    model_config = ConfigDict(frozen=True)

    escalated: bool
    contact_id: str | None
    session_state: str


# ---------------------------------------------------------------------------
# 1. connect_contact_event_to_dynamodb
# ---------------------------------------------------------------------------


def connect_contact_event_to_dynamodb(
    stream_name: str,
    table_name: str,
    shard_iterator_type: str = "LATEST",
    max_records: int = 100,
    region_name: str | None = None,
) -> ContactEventResult:
    """Parse Connect Contact Trace Records (CTRs) from Kinesis and upsert into DynamoDB.

    Reads up to *max_records* records from the first shard of *stream_name*, parses each
    record as a Connect CTR JSON payload, and writes it into *table_name* using the
    ``ContactId`` field as the partition key.

    Args:
        stream_name: Name of the Kinesis data stream carrying Connect CTRs.
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
    kinesis = get_client("kinesis", region_name)
    dynamodb = get_client("dynamodb", region_name)

    records_processed = 0
    contacts_upserted = 0

    try:
        shards_resp = kinesis.describe_stream(StreamName=stream_name)
        shards = shards_resp["StreamDescription"]["Shards"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_stream({stream_name!r})") from exc

    if not shards:
        return ContactEventResult(
            records_processed=0,
            contacts_upserted=0,
            shard_id="",
        )

    # Process the first available shard
    shard = shards[0]
    shard_id = shard["ShardId"]

    try:
        iter_resp = kinesis.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType=shard_iterator_type,
        )
        shard_iterator = iter_resp["ShardIterator"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_shard_iterator({shard_id!r})") from exc

    try:
        records_resp = kinesis.get_records(
            ShardIterator=shard_iterator,
            Limit=max_records,
        )
        raw_records = records_resp.get("Records", [])
    except ClientError as exc:
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
            dynamodb.put_item(TableName=table_name, Item=item)
            contacts_upserted += 1
        except (ClientError, json.JSONDecodeError, KeyError) as exc:
            logger.warning("Error processing CTR record: %s", exc)

    return ContactEventResult(
        records_processed=records_processed,
        contacts_upserted=contacts_upserted,
        shard_id=shard_id,
    )


# ---------------------------------------------------------------------------
# 2. connect_post_call_analyzer
# ---------------------------------------------------------------------------


def connect_post_call_analyzer(
    bucket: str,
    recording_key: str,
    table_name: str,
    language_code: str = "en-US",
    region_name: str | None = None,
) -> PostCallAnalysisResult:
    """Start a Transcribe job on a Connect call recording, run Comprehend sentiment, store in DDB.

    Workflow:
    1. Start an Amazon Transcribe transcription job targeting the S3 recording.
    2. Poll until the job completes (or fails).
    3. Read the transcript text from the output S3 location.
    4. Send the transcript to Amazon Comprehend for sentiment analysis.
    5. Persist contact_id, transcript text, sentiment, and scores in DynamoDB.

    Args:
        bucket: S3 bucket containing the Connect call recording.
        recording_key: S3 object key of the recording (e.g. ``"recordings/contact-123.wav"``).
        table_name: DynamoDB table name to store the analysis results.
        language_code: Language code for transcription (default ``"en-US"``).
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`PostCallAnalysisResult` with transcript text, sentiment, scores, and contact ID.

    Raises:
        AwsUtilError: If transcription fails or DynamoDB write fails.
    """
    transcribe = get_client("transcribe", region_name)
    comprehend = get_client("comprehend", region_name)
    s3 = get_client("s3", region_name)
    dynamodb = get_client("dynamodb", region_name)

    # Derive a contact_id from the key
    contact_id = recording_key.replace("/", "_").replace(".", "_")
    job_name = f"aws-util-{contact_id}-{int(time.time())}"
    media_uri = f"s3://{bucket}/{recording_key}"

    # Start transcription job
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            LanguageCode=language_code,
            OutputBucketName=bucket,
            OutputKey=f"transcriptions/{job_name}.json",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_transcription_job({job_name!r})") from exc

    # Poll for completion (max 20 minutes, 15s intervals)
    transcript_text = ""
    deadline = time.time() + 1200
    while time.time() < deadline:
        try:
            status_resp = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            job = status_resp["TranscriptionJob"]
            status = job["TranscriptionJobStatus"]
        except ClientError as exc:
            raise wrap_aws_error(exc, f"get_transcription_job({job_name!r})") from exc

        if status == "COMPLETED":
            break
        if status == "FAILED":
            reason = job.get("FailureReason", "unknown")
            raise wrap_aws_error(
                RuntimeError(f"Transcription job failed: {reason}"),
                f"transcription_job({job_name!r})",
            )
        logger.debug("Transcription job %s status: %s — waiting 15s", job_name, status)
        time.sleep(15)
    else:
        raise wrap_aws_error(
            TimeoutError(f"Transcription job {job_name!r} did not complete within 1200s"),
            "connect_post_call_analyzer",
        )

    # Read transcript from S3
    try:
        transcript_key = f"transcriptions/{job_name}.json"
        obj = s3.get_object(Bucket=bucket, Key=transcript_key)
        body = json.loads(obj["Body"].read())
        results = body.get("results", {})
        transcripts = results.get("transcripts", [{}])
        transcript_text = transcripts[0].get("transcript", "") if transcripts else ""
    except (ClientError, json.JSONDecodeError, KeyError) as exc:
        logger.warning("Could not read transcript from S3: %s", exc)

    # Comprehend sentiment
    sentiment = "NEUTRAL"
    sentiment_scores: dict[str, float] = {}
    if transcript_text:
        try:
            comp_resp = comprehend.detect_sentiment(
                Text=transcript_text[:5000],
                LanguageCode=language_code[:2],
            )
            sentiment = comp_resp.get("Sentiment", "NEUTRAL")
            raw_scores = comp_resp.get("SentimentScore", {})
            sentiment_scores = {k: float(v) for k, v in raw_scores.items()}
        except ClientError as exc:
            logger.warning("Comprehend sentiment detection failed: %s", exc)

    # Store in DynamoDB
    try:
        dynamodb.put_item(
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
    except ClientError as exc:
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


def lex_escalation_to_connect(
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
    """Detect if a Lex bot session requires handoff and initiate a Connect outbound contact.

    Reads the current Lex V2 session state. If the active intent name matches
    *escalation_intent*, an Amazon Connect outbound voice contact is started via
    ``start_outbound_voice_contact``.

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
    lex = get_client("lexv2-runtime", region_name)
    connect = get_client("connect", region_name)

    # Get current session state from Lex
    try:
        session_resp = lex.get_session(
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_id,
            sessionId=session_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"lex.get_session(session={session_id!r})") from exc

    session_state = session_resp.get("sessionState", {})
    active_intent = session_state.get("intent", {})
    current_intent_name = active_intent.get("name", "")
    intent_state = active_intent.get("state", "")
    session_attributes = session_resp.get("sessionAttributes", {})

    # Check if escalation intent matches
    escalated = current_intent_name == escalation_intent

    # Also check session attributes for handoff flag
    if not escalated and session_attributes.get("escalate", "").lower() in ("true", "1", "yes"):
        escalated = True

    contact_id: str | None = None

    if escalated:
        try:
            connect_resp = connect.start_outbound_voice_contact(
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
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"connect.start_outbound_voice_contact(session={session_id!r})"
            ) from exc

    return LexEscalationResult(
        escalated=escalated,
        contact_id=contact_id,
        session_state=intent_state,
    )
