from __future__ import annotations

import json
import logging
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "CancelMessageMoveTaskResult",
    "ChangeMessageVisibilityBatchResult",
    "CreateQueueResult",
    "DeleteMessageBatchResult",
    "ListDeadLetterSourceQueuesResult",
    "ListMessageMoveTasksResult",
    "ListQueueTagsResult",
    "ListQueuesResult",
    "ReceiveMessageResult",
    "SQSMessage",
    "SendMessageBatchResult",
    "SendMessageResult",
    "StartMessageMoveTaskResult",
    "add_permission",
    "cancel_message_move_task",
    "change_message_visibility",
    "change_message_visibility_batch",
    "create_queue",
    "delete_batch",
    "delete_message",
    "delete_message_batch",
    "delete_queue",
    "drain_queue",
    "get_queue_attributes",
    "get_queue_url",
    "list_dead_letter_source_queues",
    "list_message_move_tasks",
    "list_queue_tags",
    "list_queues",
    "purge_queue",
    "receive_message",
    "receive_messages",
    "remove_permission",
    "replay_dlq",
    "send_batch",
    "send_large_batch",
    "send_message",
    "send_message_batch",
    "set_queue_attributes",
    "start_message_move_task",
    "tag_queue",
    "untag_queue",
    "wait_for_message",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class SQSMessage(BaseModel):
    """A message received from an SQS queue."""

    model_config = ConfigDict(frozen=True)

    message_id: str
    receipt_handle: str
    body: str
    attributes: dict[str, str] = {}
    message_attributes: dict[str, Any] = {}

    def body_as_json(self) -> Any:
        """Parse the message body as JSON.

        Returns:
            The deserialised JSON value.

        Raises:
            ValueError: If the body is not valid JSON.
        """
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"SQS message {self.message_id!r} body is not valid JSON") from exc


class SendMessageResult(BaseModel):
    """Result of a successful ``SendMessage`` call."""

    model_config = ConfigDict(frozen=True)

    message_id: str
    sequence_number: str | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_queue_url(
    queue_name: str,
    region_name: str | None = None,
) -> str:
    """Resolve the URL for an SQS queue by name.

    Args:
        queue_name: The queue's short name (not the full URL).
        region_name: AWS region override.

    Returns:
        The full queue URL.

    Raises:
        RuntimeError: If the queue cannot be found.
    """
    client = get_client("sqs", region_name)
    try:
        resp = client.get_queue_url(QueueName=queue_name)
        return resp["QueueUrl"]
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to resolve URL for queue {queue_name!r}") from exc


def send_message(
    queue_url: str,
    body: str | dict | list,
    delay_seconds: int = 0,
    message_group_id: str | None = None,
    message_deduplication_id: str | None = None,
    region_name: str | None = None,
) -> SendMessageResult:
    """Send a single message to an SQS queue.

    Dicts and lists are serialised to JSON automatically.

    Args:
        queue_url: Full SQS queue URL.
        body: Message body.  Dicts/lists are JSON-encoded.
        delay_seconds: Delay before the message becomes visible (0–900 s).
        message_group_id: Required for FIFO queues.
        message_deduplication_id: Deduplication ID for FIFO queues.
        region_name: AWS region override.

    Returns:
        A :class:`SendMessageResult` with the assigned message ID.

    Raises:
        RuntimeError: If the send fails.
    """
    client = get_client("sqs", region_name)
    raw_body = json.dumps(body) if isinstance(body, (dict, list)) else body
    kwargs: dict[str, Any] = {
        "QueueUrl": queue_url,
        "MessageBody": raw_body,
        "DelaySeconds": delay_seconds,
    }
    if message_group_id is not None:
        kwargs["MessageGroupId"] = message_group_id
    if message_deduplication_id is not None:
        kwargs["MessageDeduplicationId"] = message_deduplication_id

    try:
        resp = client.send_message(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to send message to {queue_url!r}") from exc
    return SendMessageResult(
        message_id=resp["MessageId"],
        sequence_number=resp.get("SequenceNumber"),
    )


def send_batch(
    queue_url: str,
    messages: list[str | dict | list],
    region_name: str | None = None,
) -> list[SendMessageResult]:
    """Send up to 10 messages in a single batch request.

    Args:
        queue_url: Full SQS queue URL.
        messages: List of message bodies (up to 10).  Dicts/lists are
            JSON-encoded.
        region_name: AWS region override.

    Returns:
        A list of :class:`SendMessageResult` for successfully sent messages.

    Raises:
        RuntimeError: If the batch call fails or any message is rejected.
        ValueError: If more than 10 messages are supplied.
    """
    if len(messages) > 10:
        raise ValueError("send_batch supports at most 10 messages per call")

    client = get_client("sqs", region_name)
    entries = [
        {
            "Id": str(i),
            "MessageBody": json.dumps(m) if isinstance(m, (dict, list)) else m,
        }
        for i, m in enumerate(messages)
    ]
    try:
        resp = client.send_message_batch(QueueUrl=queue_url, Entries=entries)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to send message batch to {queue_url!r}") from exc

    if resp.get("Failed"):
        failures = [f["Message"] for f in resp["Failed"]]
        raise AwsServiceError(f"Batch send partially failed for {queue_url!r}: {failures}")

    return [
        SendMessageResult(
            message_id=s["MessageId"],
            sequence_number=s.get("SequenceNumber"),
        )
        for s in resp.get("Successful", [])
    ]


def receive_messages(
    queue_url: str,
    max_number: int = 1,
    wait_seconds: int = 0,
    visibility_timeout: int = 30,
    region_name: str | None = None,
) -> list[SQSMessage]:
    """Receive up to *max_number* messages from a queue.

    Args:
        queue_url: Full SQS queue URL.
        max_number: Maximum messages to retrieve (1–10).
        wait_seconds: Long-poll duration in seconds (0 = short poll).
            Setting this to 20 is recommended for cost efficiency.
        visibility_timeout: Seconds the message stays invisible after receipt.
        region_name: AWS region override.

    Returns:
        A list of :class:`SQSMessage` instances (may be empty).

    Raises:
        RuntimeError: If the receive call fails.
    """
    client = get_client("sqs", region_name)
    try:
        resp = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_seconds,
            VisibilityTimeout=visibility_timeout,
            AttributeNames=["All"],
            MessageAttributeNames=["All"],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to receive messages from {queue_url!r}") from exc

    return [
        SQSMessage(
            message_id=m["MessageId"],
            receipt_handle=m["ReceiptHandle"],
            body=m["Body"],
            attributes=m.get("Attributes", {}),
            message_attributes=m.get("MessageAttributes", {}),
        )
        for m in resp.get("Messages", [])
    ]


def delete_message(
    queue_url: str,
    receipt_handle: str,
    region_name: str | None = None,
) -> None:
    """Delete (acknowledge) a single message from a queue.

    Args:
        queue_url: Full SQS queue URL.
        receipt_handle: The ``ReceiptHandle`` returned when the message was
            received.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    client = get_client("sqs", region_name)
    try:
        client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete message from {queue_url!r}") from exc


def delete_batch(
    queue_url: str,
    receipt_handles: list[str],
    region_name: str | None = None,
) -> None:
    """Delete up to 10 messages in a single batch request.

    Args:
        queue_url: Full SQS queue URL.
        receipt_handles: List of ``ReceiptHandle`` values (up to 10).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the batch delete fails or any deletion is rejected.
        ValueError: If more than 10 handles are supplied.
    """
    if len(receipt_handles) > 10:
        raise ValueError("delete_batch supports at most 10 handles per call")

    client = get_client("sqs", region_name)
    entries = [{"Id": str(i), "ReceiptHandle": rh} for i, rh in enumerate(receipt_handles)]
    try:
        resp = client.delete_message_batch(QueueUrl=queue_url, Entries=entries)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete message batch from {queue_url!r}") from exc

    if resp.get("Failed"):
        failures = [f["Message"] for f in resp["Failed"]]
        raise AwsServiceError(f"Batch delete partially failed for {queue_url!r}: {failures}")


def purge_queue(
    queue_url: str,
    region_name: str | None = None,
) -> None:
    """Delete all messages in a queue.

    This is irreversible.  SQS enforces a 60-second cooldown between purges.

    Args:
        queue_url: Full SQS queue URL.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the purge fails.
    """
    client = get_client("sqs", region_name)
    try:
        client.purge_queue(QueueUrl=queue_url)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to purge queue {queue_url!r}") from exc


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def drain_queue(
    queue_url: str,
    handler: Any,
    batch_size: int = 10,
    max_messages: int | None = None,
    visibility_timeout: int = 60,
    wait_seconds: int = 5,
    region_name: str | None = None,
) -> int:
    """Continuously receive and process messages until the queue is empty.

    Calls ``handler(message)`` for each :class:`SQSMessage`.  Deletes the
    message automatically if the handler returns without raising.  If the
    handler raises, the message becomes visible again after *visibility_timeout*
    seconds.

    Args:
        queue_url: Full SQS queue URL.
        handler: Callable that accepts a single :class:`SQSMessage`.
        batch_size: Number of messages to receive per poll (1–10).
        max_messages: Stop after processing this many messages.  ``None``
            drains the queue completely.
        visibility_timeout: Seconds the message stays invisible while being
            processed.
        wait_seconds: Long-poll duration per receive call.
        region_name: AWS region override.

    Returns:
        Total number of messages successfully processed.

    Raises:
        RuntimeError: If a receive or delete call fails.
    """
    processed = 0
    consecutive_empty = 0

    while True:
        if max_messages is not None and processed >= max_messages:
            break

        remaining = (
            min(batch_size, max_messages - processed) if max_messages is not None else batch_size
        )
        messages = receive_messages(
            queue_url,
            max_number=remaining,
            wait_seconds=wait_seconds,
            visibility_timeout=visibility_timeout,
            region_name=region_name,
        )

        if not messages:
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
            continue

        consecutive_empty = 0
        for msg in messages:
            try:
                handler(msg)
                delete_message(queue_url, msg.receipt_handle, region_name=region_name)
                processed += 1
            except Exception:
                logger.exception(
                    "drain_queue handler failed for message %s",
                    msg.message_id,
                )

    return processed


def replay_dlq(
    dlq_url: str,
    target_url: str,
    max_messages: int | None = None,
    region_name: str | None = None,
) -> int:
    """Move messages from a dead-letter queue back to a target queue.

    Useful for replaying failed messages after fixing the underlying issue.

    Args:
        dlq_url: Full URL of the dead-letter queue.
        target_url: Full URL of the destination queue.
        max_messages: Maximum messages to replay.  ``None`` replays all.
        region_name: AWS region override.

    Returns:
        Number of messages successfully moved.

    Raises:
        RuntimeError: If any receive, send, or delete call fails.
    """

    def _replay(msg: SQSMessage) -> None:
        kwargs: dict[str, Any] = {
            "QueueUrl": target_url,
            "MessageBody": msg.body,
        }
        if msg.message_attributes:
            kwargs["MessageAttributes"] = msg.message_attributes
        client = get_client("sqs", region_name)
        try:
            client.send_message(**kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to replay message to {target_url!r}") from exc

    return drain_queue(
        dlq_url,
        handler=_replay,
        max_messages=max_messages,
        region_name=region_name,
    )


def send_large_batch(
    queue_url: str,
    messages: list[str | dict | list],
    region_name: str | None = None,
) -> int:
    """Send any number of messages to an SQS queue, automatically chunking into
    batches of 10.

    Args:
        queue_url: Full SQS queue URL.
        messages: Message bodies of any length.  Dicts/lists are JSON-encoded.
        region_name: AWS region override.

    Returns:
        Total number of messages sent.

    Raises:
        RuntimeError: If any batch fails.
    """
    total_sent = 0
    for i in range(0, len(messages), 10):
        chunk = messages[i : i + 10]
        send_batch(queue_url, chunk, region_name=region_name)
        total_sent += len(chunk)
    return total_sent


def wait_for_message(
    queue_url: str,
    predicate: Any | None = None,
    timeout: float = 60.0,
    poll_interval: float = 2.0,
    visibility_timeout: int = 30,
    delete_on_match: bool = True,
    region_name: str | None = None,
) -> SQSMessage | None:
    """Poll a queue until a message matching *predicate* arrives or *timeout* expires.

    .. note::

        Messages that are received but do **not** match *predicate* are
        neither deleted nor explicitly returned to the queue.  They remain
        invisible for the duration of *visibility_timeout* and only become
        available to other consumers once that period expires.  This can
        delay processing of those messages by other consumers.

    Args:
        queue_url: Full SQS queue URL.
        predicate: Optional callable ``(SQSMessage) -> bool``.  If ``None``,
            the first message received is returned.
        timeout: Maximum seconds to wait (default ``60``).
        poll_interval: Seconds between receive calls (default ``2``).
        visibility_timeout: Seconds the message stays invisible after receipt.
        delete_on_match: If ``True`` (default), delete the matching message
            automatically.
        region_name: AWS region override.

    Returns:
        The first matching :class:`SQSMessage`, or ``None`` if *timeout*
        expires without a match.

    Raises:
        RuntimeError: If a receive or delete call fails.
    """
    import time as _time

    deadline = _time.monotonic() + timeout
    while _time.monotonic() < deadline:
        messages = receive_messages(
            queue_url,
            max_number=10,
            wait_seconds=min(int(poll_interval), 20),
            visibility_timeout=visibility_timeout,
            region_name=region_name,
        )
        for msg in messages:
            if predicate is None or predicate(msg):
                if delete_on_match:
                    delete_message(queue_url, msg.receipt_handle, region_name=region_name)
                return msg
        _time.sleep(max(0, poll_interval - 1))
    return None


def get_queue_attributes(
    queue_url: str,
    attributes: list[str] | None = None,
    region_name: str | None = None,
) -> dict[str, str]:
    """Fetch queue attributes such as message count and ARN.

    Args:
        queue_url: Full SQS queue URL.
        attributes: List of attribute names to retrieve.  Defaults to
            ``["All"]``.  Common values: ``"ApproximateNumberOfMessages"``,
            ``"QueueArn"``, ``"VisibilityTimeout"``.
        region_name: AWS region override.

    Returns:
        A dict of attribute name → value strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    try:
        resp = client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=attributes or ["All"],
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_queue_attributes failed for {queue_url!r}") from exc
    return resp.get("Attributes", {})


class CancelMessageMoveTaskResult(BaseModel):
    """Result of cancel_message_move_task."""

    model_config = ConfigDict(frozen=True)

    approximate_number_of_messages_moved: int | None = None


class ChangeMessageVisibilityBatchResult(BaseModel):
    """Result of change_message_visibility_batch."""

    model_config = ConfigDict(frozen=True)

    successful: list[dict[str, Any]] | None = None
    failed: list[dict[str, Any]] | None = None


class CreateQueueResult(BaseModel):
    """Result of create_queue."""

    model_config = ConfigDict(frozen=True)

    queue_url: str | None = None


class DeleteMessageBatchResult(BaseModel):
    """Result of delete_message_batch."""

    model_config = ConfigDict(frozen=True)

    successful: list[dict[str, Any]] | None = None
    failed: list[dict[str, Any]] | None = None


class ListDeadLetterSourceQueuesResult(BaseModel):
    """Result of list_dead_letter_source_queues."""

    model_config = ConfigDict(frozen=True)

    queue_urls: list[str] | None = None
    next_token: str | None = None


class ListMessageMoveTasksResult(BaseModel):
    """Result of list_message_move_tasks."""

    model_config = ConfigDict(frozen=True)

    results: list[dict[str, Any]] | None = None


class ListQueueTagsResult(BaseModel):
    """Result of list_queue_tags."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListQueuesResult(BaseModel):
    """Result of list_queues."""

    model_config = ConfigDict(frozen=True)

    queue_urls: list[str] | None = None
    next_token: str | None = None


class ReceiveMessageResult(BaseModel):
    """Result of receive_message."""

    model_config = ConfigDict(frozen=True)

    messages: list[dict[str, Any]] | None = None


class SendMessageBatchResult(BaseModel):
    """Result of send_message_batch."""

    model_config = ConfigDict(frozen=True)

    successful: list[dict[str, Any]] | None = None
    failed: list[dict[str, Any]] | None = None


class StartMessageMoveTaskResult(BaseModel):
    """Result of start_message_move_task."""

    model_config = ConfigDict(frozen=True)

    task_handle: str | None = None


def add_permission(
    queue_url: str,
    label: str,
    aws_account_ids: list[str],
    actions: list[str],
    region_name: str | None = None,
) -> None:
    """Add permission.

    Args:
        queue_url: Queue url.
        label: Label.
        aws_account_ids: Aws account ids.
        actions: Actions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Label"] = label
    kwargs["AWSAccountIds"] = aws_account_ids
    kwargs["Actions"] = actions
    try:
        client.add_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add permission") from exc
    return None


def cancel_message_move_task(
    task_handle: str,
    region_name: str | None = None,
) -> CancelMessageMoveTaskResult:
    """Cancel message move task.

    Args:
        task_handle: Task handle.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskHandle"] = task_handle
    try:
        resp = client.cancel_message_move_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel message move task") from exc
    return CancelMessageMoveTaskResult(
        approximate_number_of_messages_moved=resp.get("ApproximateNumberOfMessagesMoved"),
    )


def change_message_visibility(
    queue_url: str,
    receipt_handle: str,
    visibility_timeout: int,
    region_name: str | None = None,
) -> None:
    """Change message visibility.

    Args:
        queue_url: Queue url.
        receipt_handle: Receipt handle.
        visibility_timeout: Visibility timeout.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["ReceiptHandle"] = receipt_handle
    kwargs["VisibilityTimeout"] = visibility_timeout
    try:
        client.change_message_visibility(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change message visibility") from exc
    return None


def change_message_visibility_batch(
    queue_url: str,
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> ChangeMessageVisibilityBatchResult:
    """Change message visibility batch.

    Args:
        queue_url: Queue url.
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Entries"] = entries
    try:
        resp = client.change_message_visibility_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change message visibility batch") from exc
    return ChangeMessageVisibilityBatchResult(
        successful=resp.get("Successful"),
        failed=resp.get("Failed"),
    )


def create_queue(
    queue_name: str,
    *,
    attributes: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateQueueResult:
    """Create queue.

    Args:
        queue_name: Queue name.
        attributes: Attributes.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueName"] = queue_name
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create queue") from exc
    return CreateQueueResult(
        queue_url=resp.get("QueueUrl"),
    )


def delete_message_batch(
    queue_url: str,
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> DeleteMessageBatchResult:
    """Delete message batch.

    Args:
        queue_url: Queue url.
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Entries"] = entries
    try:
        resp = client.delete_message_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete message batch") from exc
    return DeleteMessageBatchResult(
        successful=resp.get("Successful"),
        failed=resp.get("Failed"),
    )


def delete_queue(
    queue_url: str,
    region_name: str | None = None,
) -> None:
    """Delete queue.

    Args:
        queue_url: Queue url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    try:
        client.delete_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete queue") from exc
    return None


def list_dead_letter_source_queues(
    queue_url: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDeadLetterSourceQueuesResult:
    """List dead letter source queues.

    Args:
        queue_url: Queue url.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_dead_letter_source_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dead letter source queues") from exc
    return ListDeadLetterSourceQueuesResult(
        queue_urls=resp.get("queueUrls"),
        next_token=resp.get("NextToken"),
    )


def list_message_move_tasks(
    source_arn: str,
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMessageMoveTasksResult:
    """List message move tasks.

    Args:
        source_arn: Source arn.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceArn"] = source_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_message_move_tasks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list message move tasks") from exc
    return ListMessageMoveTasksResult(
        results=resp.get("Results"),
    )


def list_queue_tags(
    queue_url: str,
    region_name: str | None = None,
) -> ListQueueTagsResult:
    """List queue tags.

    Args:
        queue_url: Queue url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    try:
        resp = client.list_queue_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list queue tags") from exc
    return ListQueueTagsResult(
        tags=resp.get("Tags"),
    )


def list_queues(
    *,
    queue_name_prefix: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListQueuesResult:
    """List queues.

    Args:
        queue_name_prefix: Queue name prefix.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    if queue_name_prefix is not None:
        kwargs["QueueNamePrefix"] = queue_name_prefix
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list queues") from exc
    return ListQueuesResult(
        queue_urls=resp.get("QueueUrls"),
        next_token=resp.get("NextToken"),
    )


def receive_message(
    queue_url: str,
    *,
    attribute_names: list[str] | None = None,
    message_system_attribute_names: list[str] | None = None,
    message_attribute_names: list[str] | None = None,
    max_number_of_messages: int | None = None,
    visibility_timeout: int | None = None,
    wait_time_seconds: int | None = None,
    receive_request_attempt_id: str | None = None,
    region_name: str | None = None,
) -> ReceiveMessageResult:
    """Receive message.

    Args:
        queue_url: Queue url.
        attribute_names: Attribute names.
        message_system_attribute_names: Message system attribute names.
        message_attribute_names: Message attribute names.
        max_number_of_messages: Max number of messages.
        visibility_timeout: Visibility timeout.
        wait_time_seconds: Wait time seconds.
        receive_request_attempt_id: Receive request attempt id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    if attribute_names is not None:
        kwargs["AttributeNames"] = attribute_names
    if message_system_attribute_names is not None:
        kwargs["MessageSystemAttributeNames"] = message_system_attribute_names
    if message_attribute_names is not None:
        kwargs["MessageAttributeNames"] = message_attribute_names
    if max_number_of_messages is not None:
        kwargs["MaxNumberOfMessages"] = max_number_of_messages
    if visibility_timeout is not None:
        kwargs["VisibilityTimeout"] = visibility_timeout
    if wait_time_seconds is not None:
        kwargs["WaitTimeSeconds"] = wait_time_seconds
    if receive_request_attempt_id is not None:
        kwargs["ReceiveRequestAttemptId"] = receive_request_attempt_id
    try:
        resp = client.receive_message(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to receive message") from exc
    return ReceiveMessageResult(
        messages=resp.get("Messages"),
    )


def remove_permission(
    queue_url: str,
    label: str,
    region_name: str | None = None,
) -> None:
    """Remove permission.

    Args:
        queue_url: Queue url.
        label: Label.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Label"] = label
    try:
        client.remove_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove permission") from exc
    return None


def send_message_batch(
    queue_url: str,
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> SendMessageBatchResult:
    """Send message batch.

    Args:
        queue_url: Queue url.
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Entries"] = entries
    try:
        resp = client.send_message_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send message batch") from exc
    return SendMessageBatchResult(
        successful=resp.get("Successful"),
        failed=resp.get("Failed"),
    )


def set_queue_attributes(
    queue_url: str,
    attributes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Set queue attributes.

    Args:
        queue_url: Queue url.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Attributes"] = attributes
    try:
        client.set_queue_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set queue attributes") from exc
    return None


def start_message_move_task(
    source_arn: str,
    *,
    destination_arn: str | None = None,
    max_number_of_messages_per_second: int | None = None,
    region_name: str | None = None,
) -> StartMessageMoveTaskResult:
    """Start message move task.

    Args:
        source_arn: Source arn.
        destination_arn: Destination arn.
        max_number_of_messages_per_second: Max number of messages per second.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceArn"] = source_arn
    if destination_arn is not None:
        kwargs["DestinationArn"] = destination_arn
    if max_number_of_messages_per_second is not None:
        kwargs["MaxNumberOfMessagesPerSecond"] = max_number_of_messages_per_second
    try:
        resp = client.start_message_move_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start message move task") from exc
    return StartMessageMoveTaskResult(
        task_handle=resp.get("TaskHandle"),
    )


def tag_queue(
    queue_url: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag queue.

    Args:
        queue_url: Queue url.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["Tags"] = tags
    try:
        client.tag_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag queue") from exc
    return None


def untag_queue(
    queue_url: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag queue.

    Args:
        queue_url: Queue url.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sqs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueueUrl"] = queue_url
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag queue") from exc
    return None
