"""Integration tests for aws_util.contact_center_ops against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. connect_contact_event_to_dynamodb
# ---------------------------------------------------------------------------


class TestConnectContactEventToDynamodb:
    @pytest.mark.skip(reason="Connect/Kinesis CTR pipeline not available in LocalStack community")
    def test_parses_ctr_records_and_upserts_to_dynamodb(self, dynamodb_pk_table):
        from aws_util.contact_center_ops import connect_contact_event_to_dynamodb

        result = connect_contact_event_to_dynamodb(
            stream_name="connect-ctr-stream",
            table_name=dynamodb_pk_table,
            shard_iterator_type="TRIM_HORIZON",
            max_records=10,
            region_name=REGION,
        )
        assert result.records_processed >= 0
        assert result.contacts_upserted >= 0
        assert isinstance(result.shard_id, str)


# ---------------------------------------------------------------------------
# 2. connect_post_call_analyzer
# ---------------------------------------------------------------------------


class TestConnectPostCallAnalyzer:
    @pytest.mark.skip(
        reason="Transcribe/Comprehend not available in LocalStack community"
    )
    def test_transcribes_recording_and_analyzes_sentiment(
        self, s3_bucket, dynamodb_pk_table
    ):
        from aws_util.contact_center_ops import connect_post_call_analyzer

        # Upload a dummy recording
        s3 = ls_client("s3")
        s3.put_object(
            Bucket=s3_bucket,
            Key="recordings/contact-123.wav",
            Body=b"\x00" * 1024,
        )

        result = connect_post_call_analyzer(
            bucket=s3_bucket,
            recording_key="recordings/contact-123.wav",
            table_name=dynamodb_pk_table,
            language_code="en-US",
            region_name=REGION,
        )
        assert isinstance(result.transcript_text, str)
        assert result.sentiment in ("POSITIVE", "NEGATIVE", "NEUTRAL", "MIXED")
        assert isinstance(result.sentiment_scores, dict)
        assert isinstance(result.contact_id, str)


# ---------------------------------------------------------------------------
# 3. lex_escalation_to_connect
# ---------------------------------------------------------------------------


class TestLexEscalationToConnect:
    @pytest.mark.skip(reason="Lex/Connect not available in LocalStack community")
    def test_detects_escalation_intent_and_starts_outbound_contact(self):
        from aws_util.contact_center_ops import lex_escalation_to_connect

        result = lex_escalation_to_connect(
            bot_id="TESTBOTID",
            bot_alias_id="TESTALIASID",
            session_id="test-session-001",
            locale_id="en_US",
            instance_id="test-instance-id",
            contact_flow_id="test-flow-id",
            destination_phone="+15551234567",
            source_phone="+15559876543",
            escalation_intent="EscalateToAgent",
            region_name=REGION,
        )
        assert isinstance(result.escalated, bool)
        assert result.contact_id is None or isinstance(result.contact_id, str)
        assert isinstance(result.session_state, str)
