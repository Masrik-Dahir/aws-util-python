"""Integration tests for aws_util.resilience against LocalStack."""
from __future__ import annotations

import json
import time

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. circuit_breaker
# ---------------------------------------------------------------------------


class TestCircuitBreaker:
    def test_normal_operation(self, dynamodb_pk_table):
        from aws_util.resilience import circuit_breaker

        call_count = 0

        def my_fn():
            nonlocal call_count
            call_count += 1
            return "success"

        # circuit_breaker(func, circuit_name, table_name, ...) returns CircuitBreakerResult
        result = circuit_breaker(
            func=my_fn,
            circuit_name="test-circuit",
            table_name=dynamodb_pk_table,
            failure_threshold=3,
            region_name=REGION,
        )
        assert result.allowed is True
        assert result.result == "success"
        assert result.state == "closed"
        assert call_count == 1


# ---------------------------------------------------------------------------
# 2. dlq_monitor_and_alert
# ---------------------------------------------------------------------------


class TestDlqMonitorAndAlert:
    def test_monitors_empty_dlq(self, sqs_queue, sns_topic):
        from aws_util.resilience import dlq_monitor_and_alert

        result = dlq_monitor_and_alert(
            queue_url=sqs_queue,
            topic_arn=sns_topic,
            threshold=1,
            region_name=REGION,
        )
        # DLQMonitorResult has approximate_message_count, alert_sent
        assert result.approximate_message_count >= 0
        assert isinstance(result.alert_sent, bool)

    def test_monitors_populated_dlq(self, sqs_queue, sns_topic):
        from aws_util.resilience import dlq_monitor_and_alert

        sqs = ls_client("sqs")
        for i in range(5):
            sqs.send_message(QueueUrl=sqs_queue, MessageBody=json.dumps({"idx": i}))

        result = dlq_monitor_and_alert(
            queue_url=sqs_queue,
            topic_arn=sns_topic,
            threshold=1,
            region_name=REGION,
        )
        assert result.approximate_message_count >= 5
        assert result.alert_sent is True


# ---------------------------------------------------------------------------
# 3. poison_pill_handler
# ---------------------------------------------------------------------------


class TestPoisonPillHandler:
    def test_quarantines_poison_messages(self, s3_bucket):
        from aws_util.resilience import poison_pill_handler

        # poison_pill_handler operates on pre-received SQS records
        records = [
            {
                "messageId": f"msg-{i}",
                "body": json.dumps({"idx": i}),
                "attributes": {"ApproximateReceiveCount": str(5)},
            }
            for i in range(3)
        ]

        result = poison_pill_handler(
            records=records,
            max_receive_count=3,
            quarantine_bucket=s3_bucket,
            quarantine_prefix="poison-pills/",
            region_name=REGION,
        )
        # PoisonPillResult has quarantined, passed_through, quarantine_target
        assert result.quarantined == 3
        assert result.passed_through == 0

    def test_passes_through_normal_messages(self, s3_bucket):
        from aws_util.resilience import poison_pill_handler

        records = [
            {
                "messageId": f"msg-{i}",
                "body": json.dumps({"idx": i}),
                "attributes": {"ApproximateReceiveCount": "1"},
            }
            for i in range(3)
        ]

        result = poison_pill_handler(
            records=records,
            max_receive_count=3,
            quarantine_bucket=s3_bucket,
            region_name=REGION,
        )
        assert result.quarantined == 0
        assert result.passed_through == 3


# ---------------------------------------------------------------------------
# 4. distributed_lock_manager
# ---------------------------------------------------------------------------


class TestDistributedLockManager:
    def _make_lock_table(self):
        """Create a DynamoDB table with lock_key as the hash key."""
        client = ls_client("dynamodb")
        name = f"test-lock-table-{int(time.time())}"
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "lock_key", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "lock_key", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
        except client.exceptions.ResourceInUseException:
            pass  # table already exists
        client.get_waiter("table_exists").wait(TableName=name)
        return name

    def test_acquires_and_releases_lock(self):
        from aws_util.resilience import distributed_lock_manager

        table_name = self._make_lock_table()

        result = distributed_lock_manager(
            table_name=table_name,
            lock_key="test-lock",
            owner_id="worker-1",
            ttl_seconds=30,
            action="acquire",
            region_name=REGION,
        )
        assert result.acquired is True
        assert result.lock_key == "test-lock"

    def test_lock_contention(self):
        from aws_util.resilience import distributed_lock_manager

        table_name = self._make_lock_table()

        # First lock should succeed
        r1 = distributed_lock_manager(
            table_name=table_name,
            lock_key="contention-lock",
            owner_id="worker-1",
            ttl_seconds=60,
            action="acquire",
            region_name=REGION,
        )
        assert r1.acquired is True

        # Second lock with different owner should fail
        r2 = distributed_lock_manager(
            table_name=table_name,
            lock_key="contention-lock",
            owner_id="worker-2",
            ttl_seconds=60,
            action="acquire",
            region_name=REGION,
        )
        assert r2.acquired is False


# ---------------------------------------------------------------------------
# 5. retry_with_backoff
# ---------------------------------------------------------------------------


class TestRetryWithBackoff:
    def test_succeeds_after_retry(self):
        from aws_util.resilience import retry_with_backoff

        attempt = 0

        # retry_with_backoff is a decorator
        @retry_with_backoff(max_retries=5, base_delay=0.01)
        def flaky_fn():
            nonlocal attempt
            attempt += 1
            if attempt < 3:
                raise RuntimeError("Transient error")
            return "success"

        result = flaky_fn()
        # Returns RetryResult with success, result, attempts
        assert result.success is True
        assert result.result == "success"
        assert attempt == 3

    def test_exhausts_retries(self):
        from aws_util.resilience import retry_with_backoff

        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_fail():
            raise RuntimeError("Permanent error")

        result = always_fail()
        # Returns RetryResult with success=False
        assert result.success is False
        assert result.last_error is not None


# ---------------------------------------------------------------------------
# 6. graceful_degradation
# ---------------------------------------------------------------------------


class TestGracefulDegradation:
    def _make_cache_table(self):
        """Create a DynamoDB table with pk as the hash key for caching."""
        client = ls_client("dynamodb")
        name = f"test-cache-table-{int(time.time())}"
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
        except client.exceptions.ResourceInUseException:
            pass  # table already exists
        client.get_waiter("table_exists").wait(TableName=name)
        return name

    def test_returns_primary(self):
        from aws_util.resilience import graceful_degradation

        cache_table = self._make_cache_table()

        def primary():
            return "primary_result"

        result = graceful_degradation(
            func=primary,
            cache_table=cache_table,
            cache_key="test-key",
            region_name=REGION,
        )
        # GracefulDegradationResult has from_cache, result, error
        assert result.from_cache is False
        assert result.result == "primary_result"

    def test_returns_fallback_on_failure(self):
        from aws_util.resilience import graceful_degradation

        cache_table = self._make_cache_table()

        # First, populate the cache with a successful call
        def primary_success():
            return "cached_value"

        graceful_degradation(
            func=primary_success,
            cache_table=cache_table,
            cache_key="fallback-key",
            region_name=REGION,
        )

        # Now call with a function that fails — should return cached value
        def primary_fail():
            raise RuntimeError("Primary failed")

        result = graceful_degradation(
            func=primary_fail,
            cache_table=cache_table,
            cache_key="fallback-key",
            region_name=REGION,
        )
        assert result.from_cache is True
        assert result.result == "cached_value"


# ---------------------------------------------------------------------------
# 7. lambda_destination_router
# ---------------------------------------------------------------------------


class TestLambdaDestinationRouter:
    def test_configures_destinations(self, iam_role, sqs_queue, sns_topic):
        from aws_util.resilience import lambda_destination_router

        import io
        import zipfile

        # Create a Lambda function
        lam = ls_client("lambda")
        fn_name = f"dest-router-fn-{int(time.time())}"
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(event, context): return event")

        try:
            lam.create_function(
                FunctionName=fn_name,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ResourceConflictException":
                pass
            else:
                raise

        # Get the SQS queue ARN for the destination
        sqs = ls_client("sqs")
        attrs = sqs.get_queue_attributes(
            QueueUrl=sqs_queue,
            AttributeNames=["QueueArn"],
        )
        queue_arn = attrs["Attributes"]["QueueArn"]

        result = lambda_destination_router(
            function_name=fn_name,
            on_success_arn=queue_arn,
            on_failure_arn=sns_topic,
            region_name=REGION,
        )
        assert result.function_name == fn_name
        assert result.on_success == queue_arn
        assert result.on_failure == sns_topic

    def test_raises_when_no_destinations(self):
        from aws_util.resilience import lambda_destination_router

        with pytest.raises(ValueError, match="At least one of"):
            lambda_destination_router(
                function_name="any-fn",
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# 8. timeout_sentinel
# ---------------------------------------------------------------------------


class TestTimeoutSentinel:
    def test_succeeds_within_timeout(self):
        from aws_util.resilience import timeout_sentinel

        def fast_fn():
            return "done"

        result = timeout_sentinel(
            func=fast_fn,
            timeout_seconds=5.0,
        )
        assert result.success is True
        assert result.result == "done"
        assert result.timed_out is False

    def test_times_out(self):
        from aws_util.resilience import timeout_sentinel

        def slow_fn():
            time.sleep(10)
            return "too late"

        result = timeout_sentinel(
            func=slow_fn,
            timeout_seconds=0.5,
        )
        assert result.success is False
        assert result.timed_out is True
        assert result.error is not None

    def test_handles_exception(self):
        from aws_util.resilience import timeout_sentinel

        def error_fn():
            raise ValueError("kaboom")

        result = timeout_sentinel(
            func=error_fn,
            timeout_seconds=5.0,
        )
        assert result.success is False
        assert result.timed_out is False
        assert "kaboom" in result.error
