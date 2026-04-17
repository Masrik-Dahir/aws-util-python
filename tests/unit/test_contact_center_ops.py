"""Tests for aws_util.contact_center_ops module."""
from __future__ import annotations

import io
import json
import time
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.contact_center_ops as mod
from aws_util.contact_center_ops import (
    ContactEventResult,
    LexEscalationResult,
    PostCallAnalysisResult,
    connect_contact_event_to_dynamodb,
    connect_post_call_analyzer,
    lex_escalation_to_connect,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_contact_event_result(self) -> None:
        r = ContactEventResult(records_processed=5, contacts_upserted=3, shard_id="shard-1")
        assert r.records_processed == 5
        assert r.contacts_upserted == 3
        assert r.shard_id == "shard-1"

    def test_post_call_analysis_result(self) -> None:
        r = PostCallAnalysisResult(
            transcript_text="Hello",
            sentiment="POSITIVE",
            sentiment_scores={"Positive": 0.95},
            contact_id="c1",
        )
        assert r.sentiment == "POSITIVE"

    def test_lex_escalation_result(self) -> None:
        r = LexEscalationResult(escalated=True, contact_id="ct-1", session_state="Fulfilled")
        assert r.escalated is True
        assert r.contact_id == "ct-1"

    def test_frozen(self) -> None:
        r = ContactEventResult(records_processed=0, contacts_upserted=0, shard_id="")
        with pytest.raises(Exception):
            r.shard_id = "x"  # type: ignore[misc]


# ==================================================================
# connect_contact_event_to_dynamodb
# ==================================================================


class TestConnectContactEventToDynamodb:
    def _build_clients(
        self,
        kinesis: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _kinesis = kinesis or _mock()
        _ddb = ddb or _mock()

        def factory(service, region_name=None):
            if service == "kinesis":
                return _kinesis
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _kinesis, _ddb

    def test_success(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {
                "Shards": [{"ShardId": "shard-001"}]
            }
        }
        kinesis.get_shard_iterator.return_value = {"ShardIterator": "iter-abc"}
        ctr_data = {
            "ContactId": "contact-123",
            "Agent": {"ARN": "arn:agent"},
            "CustomerEndpoint": {"Address": "+1234567890"},
            "InitiationTimestamp": "2026-04-15T12:00:00Z",
            "DisconnectTimestamp": "2026-04-15T12:05:00Z",
            "Channel": "VOICE",
            "Queue": {"Name": "support-queue"},
        }
        kinesis.get_records.return_value = {
            "Records": [{"Data": json.dumps(ctr_data).encode(), "SequenceNumber": "1"}]
        }
        ddb = _mock()
        factory, _, _ = self._build_clients(kinesis=kinesis, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = connect_contact_event_to_dynamodb(
            stream_name="connect-ctr-stream",
            table_name="ctr-table",
            region_name=REGION,
        )
        assert result.records_processed == 1
        assert result.contacts_upserted == 1
        assert result.shard_id == "shard-001"
        ddb.put_item.assert_called_once()

    def test_no_shards(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": []}
        }
        factory, _, _ = self._build_clients(kinesis=kinesis)
        monkeypatch.setattr(mod, "get_client", factory)

        result = connect_contact_event_to_dynamodb(
            stream_name="s", table_name="t", region_name=REGION,
        )
        assert result.records_processed == 0
        assert result.shard_id == ""

    def test_describe_stream_error(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.side_effect = _client_error("ResourceNotFoundException")
        factory, _, _ = self._build_clients(kinesis=kinesis)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            connect_contact_event_to_dynamodb(
                stream_name="s", table_name="t", region_name=REGION,
            )

    def test_get_shard_iterator_error(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": [{"ShardId": "s1"}]}
        }
        kinesis.get_shard_iterator.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(kinesis=kinesis)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            connect_contact_event_to_dynamodb(
                stream_name="s", table_name="t", region_name=REGION,
            )

    def test_get_records_error(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": [{"ShardId": "s1"}]}
        }
        kinesis.get_shard_iterator.return_value = {"ShardIterator": "iter"}
        kinesis.get_records.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(kinesis=kinesis)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            connect_contact_event_to_dynamodb(
                stream_name="s", table_name="t", region_name=REGION,
            )

    def test_malformed_record_skipped(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": [{"ShardId": "s1"}]}
        }
        kinesis.get_shard_iterator.return_value = {"ShardIterator": "iter"}
        kinesis.get_records.return_value = {
            "Records": [
                {"Data": b"not-json", "SequenceNumber": "1"},
                {"Data": json.dumps({"ContactId": "c2", "Channel": "CHAT"}).encode(), "SequenceNumber": "2"},
            ]
        }
        ddb = _mock()
        factory, _, _ = self._build_clients(kinesis=kinesis, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = connect_contact_event_to_dynamodb(
            stream_name="s", table_name="t", region_name=REGION,
        )
        assert result.records_processed == 2
        # First record fails JSON parse, second succeeds
        assert result.contacts_upserted == 1

    def test_ddb_put_error_skipped(self, monkeypatch) -> None:
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": [{"ShardId": "s1"}]}
        }
        kinesis.get_shard_iterator.return_value = {"ShardIterator": "iter"}
        kinesis.get_records.return_value = {
            "Records": [
                {"Data": json.dumps({"ContactId": "c1"}).encode(), "SequenceNumber": "1"},
            ]
        }
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(kinesis=kinesis, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = connect_contact_event_to_dynamodb(
            stream_name="s", table_name="t", region_name=REGION,
        )
        assert result.records_processed == 1
        assert result.contacts_upserted == 0

    def test_queue_not_dict(self, monkeypatch) -> None:
        """Queue field that is not a dict should yield empty QueueName."""
        kinesis = _mock()
        kinesis.describe_stream.return_value = {
            "StreamDescription": {"Shards": [{"ShardId": "s1"}]}
        }
        kinesis.get_shard_iterator.return_value = {"ShardIterator": "iter"}
        ctr = {"ContactId": "c1", "Queue": "not-a-dict"}
        kinesis.get_records.return_value = {
            "Records": [{"Data": json.dumps(ctr).encode(), "SequenceNumber": "1"}]
        }
        ddb = _mock()
        factory, _, _ = self._build_clients(kinesis=kinesis, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = connect_contact_event_to_dynamodb(
            stream_name="s", table_name="t", region_name=REGION,
        )
        assert result.contacts_upserted == 1


# ==================================================================
# connect_post_call_analyzer
# ==================================================================


class TestConnectPostCallAnalyzer:
    def _build_clients(
        self,
        transcribe: MagicMock | None = None,
        comprehend: MagicMock | None = None,
        s3: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _transcribe = transcribe or _mock()
        _comprehend = comprehend or _mock()
        _s3 = s3 or _mock()
        _ddb = ddb or _mock()

        def factory(service, region_name=None):
            if service == "transcribe":
                return _transcribe
            if service == "comprehend":
                return _comprehend
            if service == "s3":
                return _s3
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _transcribe, _comprehend, _s3, _ddb

    def test_success(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {
                "TranscriptionJobStatus": "COMPLETED",
            }
        }
        transcript_body = json.dumps({
            "results": {"transcripts": [{"transcript": "Hello how can I help?"}]}
        }).encode()
        s3 = _mock()
        s3.get_object.return_value = {"Body": io.BytesIO(transcript_body)}
        comprehend = _mock()
        comprehend.detect_sentiment.return_value = {
            "Sentiment": "POSITIVE",
            "SentimentScore": {"Positive": 0.9, "Negative": 0.05, "Neutral": 0.04, "Mixed": 0.01},
        }
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(
            transcribe=transcribe, comprehend=comprehend, s3=s3, ddb=ddb,
        )
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = connect_post_call_analyzer(
            bucket="recordings-bucket",
            recording_key="recordings/contact-123.wav",
            table_name="analysis-table",
            region_name=REGION,
        )
        assert result.transcript_text == "Hello how can I help?"
        assert result.sentiment == "POSITIVE"
        assert result.sentiment_scores["Positive"] == 0.9
        assert "contact-123" in result.contact_id
        ddb.put_item.assert_called_once()

    def test_transcription_fails(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {
                "TranscriptionJobStatus": "FAILED",
                "FailureReason": "bad audio",
            }
        }
        factory, _, _, _, _ = self._build_clients(transcribe=transcribe)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            connect_post_call_analyzer(
                bucket="b", recording_key="r/c.wav",
                table_name="t", region_name=REGION,
            )

    def test_transcription_timeout(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "IN_PROGRESS"}
        }
        factory, _, _, _, _ = self._build_clients(transcribe=transcribe)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        # Make time.time() return values that immediately exceed deadline
        call_count = [0]
        original_time = time.time

        def fake_time():
            call_count[0] += 1
            if call_count[0] <= 2:
                return original_time()
            return original_time() + 2000  # past deadline
        monkeypatch.setattr(mod.time, "time", fake_time)

        with pytest.raises(RuntimeError):
            connect_post_call_analyzer(
                bucket="b", recording_key="r/c.wav",
                table_name="t", region_name=REGION,
            )

    def test_start_transcription_error(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.start_transcription_job.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(transcribe=transcribe)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            connect_post_call_analyzer(
                bucket="b", recording_key="r/c.wav",
                table_name="t", region_name=REGION,
            )

    def test_get_transcription_job_error(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(transcribe=transcribe)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            connect_post_call_analyzer(
                bucket="b", recording_key="r/c.wav",
                table_name="t", region_name=REGION,
            )

    def test_s3_read_transcript_error(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "COMPLETED"}
        }
        s3 = _mock()
        s3.get_object.side_effect = _client_error("NoSuchKey")
        comprehend = _mock()
        comprehend.detect_sentiment.return_value = {
            "Sentiment": "NEUTRAL", "SentimentScore": {},
        }
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(
            transcribe=transcribe, s3=s3, comprehend=comprehend, ddb=ddb,
        )
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        # S3 read error is a warning, not fatal — transcript will be empty
        result = connect_post_call_analyzer(
            bucket="b", recording_key="r/c.wav",
            table_name="t", region_name=REGION,
        )
        assert result.transcript_text == ""
        # Comprehend should not be called with empty text
        assert result.sentiment == "NEUTRAL"

    def test_comprehend_error_swallowed(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "COMPLETED"}
        }
        transcript_body = json.dumps({
            "results": {"transcripts": [{"transcript": "Hello"}]}
        }).encode()
        s3 = _mock()
        s3.get_object.return_value = {"Body": io.BytesIO(transcript_body)}
        comprehend = _mock()
        comprehend.detect_sentiment.side_effect = _client_error("InternalServerError")
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(
            transcribe=transcribe, s3=s3, comprehend=comprehend, ddb=ddb,
        )
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = connect_post_call_analyzer(
            bucket="b", recording_key="r/c.wav",
            table_name="t", region_name=REGION,
        )
        # Comprehend error is warned but not fatal
        assert result.sentiment == "NEUTRAL"

    def test_ddb_write_error(self, monkeypatch) -> None:
        transcribe = _mock()
        transcribe.get_transcription_job.return_value = {
            "TranscriptionJob": {"TranscriptionJobStatus": "COMPLETED"}
        }
        s3 = _mock()
        s3.get_object.return_value = {"Body": io.BytesIO(b'{"results":{"transcripts":[{"transcript":"Hi"}]}}')}
        comprehend = _mock()
        comprehend.detect_sentiment.return_value = {"Sentiment": "NEUTRAL", "SentimentScore": {}}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(
            transcribe=transcribe, s3=s3, comprehend=comprehend, ddb=ddb,
        )
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            connect_post_call_analyzer(
                bucket="b", recording_key="r/c.wav",
                table_name="t", region_name=REGION,
            )

    def test_polling_waits_then_completes(self, monkeypatch) -> None:
        transcribe = _mock()
        # First poll: IN_PROGRESS, second: COMPLETED
        transcribe.get_transcription_job.side_effect = [
            {"TranscriptionJob": {"TranscriptionJobStatus": "IN_PROGRESS"}},
            {"TranscriptionJob": {"TranscriptionJobStatus": "COMPLETED"}},
        ]
        transcript_body = json.dumps({
            "results": {"transcripts": [{"transcript": "Test"}]}
        }).encode()
        s3 = _mock()
        s3.get_object.return_value = {"Body": io.BytesIO(transcript_body)}
        comprehend = _mock()
        comprehend.detect_sentiment.return_value = {"Sentiment": "NEUTRAL", "SentimentScore": {}}
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(
            transcribe=transcribe, s3=s3, comprehend=comprehend, ddb=ddb,
        )
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = connect_post_call_analyzer(
            bucket="b", recording_key="r/c.wav",
            table_name="t", region_name=REGION,
        )
        assert result.transcript_text == "Test"


# ==================================================================
# lex_escalation_to_connect
# ==================================================================


class TestLexEscalationToConnect:
    def _build_clients(
        self,
        lex: MagicMock | None = None,
        connect: MagicMock | None = None,
    ) -> Any:
        _lex = lex or _mock()
        _connect = connect or _mock()

        def factory(service, region_name=None):
            if service == "lexv2-runtime":
                return _lex
            if service == "connect":
                return _connect
            return _mock()
        return factory, _lex, _connect

    def test_escalation_triggered(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "Escalate", "state": "ReadyForFulfillment"},
            },
            "sessionAttributes": {},
        }
        connect = _mock()
        connect.start_outbound_voice_contact.return_value = {"ContactId": "ct-abc"}
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is True
        assert result.contact_id == "ct-abc"
        assert result.session_state == "ReadyForFulfillment"
        connect.start_outbound_voice_contact.assert_called_once()

    def test_no_escalation(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "OrderPizza", "state": "InProgress"},
            },
            "sessionAttributes": {},
        }
        connect = _mock()
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is False
        assert result.contact_id is None
        connect.start_outbound_voice_contact.assert_not_called()

    def test_escalation_via_session_attribute(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "OtherIntent", "state": "Fulfilled"},
            },
            "sessionAttributes": {"escalate": "true"},
        }
        connect = _mock()
        connect.start_outbound_voice_contact.return_value = {"ContactId": "ct-def"}
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is True

    def test_escalation_via_session_attribute_yes(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "Other", "state": "Fulfilled"},
            },
            "sessionAttributes": {"escalate": "yes"},
        }
        connect = _mock()
        connect.start_outbound_voice_contact.return_value = {"ContactId": "ct-ghi"}
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is True

    def test_escalation_via_session_attribute_1(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "Other", "state": "Fulfilled"},
            },
            "sessionAttributes": {"escalate": "1"},
        }
        connect = _mock()
        connect.start_outbound_voice_contact.return_value = {"ContactId": "ct-xyz"}
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is True

    def test_lex_session_error(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.side_effect = _client_error("ResourceNotFoundException")
        factory, _, _ = self._build_clients(lex=lex)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            lex_escalation_to_connect(
                bot_id="bot-1", bot_alias_id="alias-1",
                session_id="sess-1", locale_id="en_US",
                instance_id="inst-1", contact_flow_id="flow-1",
                destination_phone="+1234567890",
                source_phone="+0987654321",
                escalation_intent="Escalate",
                region_name=REGION,
            )

    def test_connect_start_contact_error(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "Escalate", "state": "ReadyForFulfillment"},
            },
            "sessionAttributes": {},
        }
        connect = _mock()
        connect.start_outbound_voice_contact.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(lex=lex, connect=connect)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            lex_escalation_to_connect(
                bot_id="bot-1", bot_alias_id="alias-1",
                session_id="sess-1", locale_id="en_US",
                instance_id="inst-1", contact_flow_id="flow-1",
                destination_phone="+1234567890",
                source_phone="+0987654321",
                escalation_intent="Escalate",
                region_name=REGION,
            )

    def test_no_escalate_attribute_false(self, monkeypatch) -> None:
        lex = _mock()
        lex.get_session.return_value = {
            "sessionState": {
                "intent": {"name": "Other", "state": "Fulfilled"},
            },
            "sessionAttributes": {"escalate": "false"},
        }
        factory, _, connect = self._build_clients(lex=lex)
        monkeypatch.setattr(mod, "get_client", factory)

        result = lex_escalation_to_connect(
            bot_id="bot-1", bot_alias_id="alias-1",
            session_id="sess-1", locale_id="en_US",
            instance_id="inst-1", contact_flow_id="flow-1",
            destination_phone="+1234567890",
            source_phone="+0987654321",
            escalation_intent="Escalate",
            region_name=REGION,
        )
        assert result.escalated is False
