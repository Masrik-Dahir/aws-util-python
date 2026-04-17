"""Integration tests for aws_util.lambda_middleware against LocalStack."""
from __future__ import annotations

import json
import time

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. idempotent_handler
# ---------------------------------------------------------------------------


class TestIdempotentHandler:
    def _make_idempotency_table(self):
        """Create a DynamoDB table with idempotency_key as the hash key."""
        client = ls_client("dynamodb")
        name = f"test-idemp-table-{int(time.time())}"
        client.create_table(
            TableName=name,
            KeySchema=[{"AttributeName": "idempotency_key", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "idempotency_key", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        client.get_waiter("table_exists").wait(TableName=name)
        return name

    def test_idempotent_call(self):
        from aws_util.lambda_middleware import idempotent_handler

        table_name = self._make_idempotency_table()
        call_count = 0

        # idempotent_handler is a decorator factory: idempotent_handler(table_name, ...) -> decorator
        @idempotent_handler(table_name=table_name, region_name=REGION)
        def my_handler(event, context):
            nonlocal call_count
            call_count += 1
            return {"statusCode": 200, "body": "ok"}

        event = {"key": "test-event-1"}
        context = type("Ctx", (), {"function_name": "test", "aws_request_id": "req-1"})()

        result1 = my_handler(event, context)
        assert result1["statusCode"] == 200
        assert call_count == 1

        # Second call with same event should return cached result
        result2 = my_handler(event, context)
        assert result2["statusCode"] == 200


# ---------------------------------------------------------------------------
# 2. evaluate_feature_flag
# ---------------------------------------------------------------------------


class TestEvaluateFeatureFlag:
    def test_feature_flag(self, ssm_client):
        from aws_util.lambda_middleware import evaluate_feature_flag

        # evaluate_feature_flag reads from SSM Parameter Store, not DynamoDB
        ssm_client.put_parameter(
            Name="/feature-flags/dark-mode",
            Value="true",
            Type="String",
            Overwrite=True,
        )

        result = evaluate_feature_flag(
            flag_name="dark-mode",
            ssm_prefix="/feature-flags/",
            region_name=REGION,
        )
        # FeatureFlagResult has name, enabled, value
        assert result.name == "dark-mode"
        assert result.enabled is True
        assert result.value == "true"

    def test_flag_not_found(self):
        from aws_util.lambda_middleware import evaluate_feature_flag

        result = evaluate_feature_flag(
            flag_name="nonexistent-flag",
            ssm_prefix="/feature-flags/",
            region_name=REGION,
        )
        assert result.enabled is False
        assert result.value == ""


# ---------------------------------------------------------------------------
# 3. Parse event functions (pure compute -- no AWS needed)
# ---------------------------------------------------------------------------


class TestParseEvents:
    def test_parse_sqs_event(self):
        from aws_util.lambda_middleware import parse_sqs_event

        raw = {
            "Records": [
                {
                    "messageId": "msg-1",
                    "receiptHandle": "handle",
                    "body": json.dumps({"data": "test"}),
                    "attributes": {},
                    "messageAttributes": {},
                    "md5OfBody": "abc",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:123:queue",
                    "awsRegion": "us-east-1",
                }
            ]
        }
        result = parse_sqs_event(raw)
        # SQSEvent uses capital Records, SQSRecord uses camelCase messageId
        assert len(result.Records) == 1
        assert result.Records[0].messageId == "msg-1"

    def test_parse_sns_event(self):
        from aws_util.lambda_middleware import parse_sns_event

        raw = {
            "Records": [
                {
                    "EventVersion": "1.0",
                    "EventSubscriptionArn": "arn:aws:sns:us-east-1:123:topic:sub",
                    "EventSource": "aws:sns",
                    "Sns": {
                        "Type": "Notification",
                        "MessageId": "msg-1",
                        "TopicArn": "arn:aws:sns:us-east-1:123:topic",
                        "Subject": "Test",
                        "Message": json.dumps({"key": "value"}),
                        "Timestamp": "2024-01-01T00:00:00.000Z",
                        "SignatureVersion": "1",
                        "Signature": "sig",
                        "SigningCertUrl": "https://example.com/cert",
                        "UnsubscribeUrl": "https://example.com/unsub",
                        "MessageAttributes": {},
                    },
                }
            ]
        }
        result = parse_sns_event(raw)
        # SNSEvent uses capital Records
        assert len(result.Records) == 1

    def test_parse_api_gateway_event(self):
        from aws_util.lambda_middleware import parse_api_gateway_event

        raw = {
            "httpMethod": "GET",
            "path": "/test",
            "headers": {"Content-Type": "application/json"},
            "queryStringParameters": {"q": "hello"},
            "pathParameters": None,
            "body": None,
            "isBase64Encoded": False,
            "requestContext": {"stage": "prod"},
            "resource": "/test",
            "stageVariables": None,
            "multiValueHeaders": {},
            "multiValueQueryStringParameters": {},
        }
        result = parse_api_gateway_event(raw)
        # APIGatewayEvent uses camelCase httpMethod
        assert result.httpMethod == "GET"
        assert result.path == "/test"

    def test_parse_eventbridge_event(self):
        from aws_util.lambda_middleware import parse_eventbridge_event

        raw = {
            "version": "0",
            "id": "event-1",
            "detail-type": "EC2 Instance State-change Notification",
            "source": "aws.ec2",
            "account": "123456789012",
            "time": "2024-01-01T00:00:00Z",
            "region": "us-east-1",
            "resources": [],
            "detail": {"instance-id": "i-1234"},
        }
        result = parse_eventbridge_event(raw)
        assert result.source == "aws.ec2"
        assert result.detail["instance-id"] == "i-1234"


# ---------------------------------------------------------------------------
# 4. batch_processor
# ---------------------------------------------------------------------------


class TestBatchProcessor:
    def test_processes_batch(self):
        from aws_util.lambda_middleware import batch_processor

        records = [
            {"messageId": f"msg-{i}", "body": json.dumps({"idx": i})}
            for i in range(5)
        ]

        def process_record(record):
            return {"processed": True}

        # batch_processor(handler, records) -- positional args
        result = batch_processor(
            handler=process_record,
            records=records,
        )
        # BatchProcessingResult has successful (list), failed (list), batch_item_failures
        assert len(result.successful) == 5
        assert len(result.failed) == 0

    def test_partial_failure(self):
        from aws_util.lambda_middleware import batch_processor

        records = [
            {"messageId": f"msg-{i}", "body": json.dumps({"idx": i})}
            for i in range(5)
        ]

        def process_record(record):
            body = json.loads(record["body"])
            if body["idx"] == 2:
                raise ValueError("Intentional failure")
            return {"processed": True}

        result = batch_processor(
            handler=process_record,
            records=records,
        )
        assert len(result.successful) == 4
        assert len(result.failed) == 1


# ---------------------------------------------------------------------------
# 5. lambda_response helper
# ---------------------------------------------------------------------------


class TestLambdaResponse:
    def test_json_response(self):
        from aws_util.lambda_middleware import lambda_response

        resp = lambda_response(
            status_code=200,
            body={"message": "ok"},
        )
        assert resp["statusCode"] == 200
        assert json.loads(resp["body"])["message"] == "ok"
        assert "application/json" in resp["headers"]["Content-Type"]

    def test_cors_preflight(self):
        from aws_util.lambda_middleware import cors_preflight

        resp = cors_preflight()
        # cors_preflight returns statusCode 204
        assert resp["statusCode"] == 204
        assert "Access-Control-Allow-Origin" in resp["headers"]
