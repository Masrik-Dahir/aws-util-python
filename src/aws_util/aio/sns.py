"""Native async SNS utilities — real non-blocking I/O via :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error
from aws_util.sns import (
    CheckIfPhoneNumberIsOptedOutResult,
    ConfirmSubscriptionResult,
    CreatePlatformApplicationResult,
    CreatePlatformEndpointResult,
    CreateTopicResult,
    FanOutFailure,
    GetDataProtectionPolicyResult,
    GetEndpointAttributesResult,
    GetPlatformApplicationAttributesResult,
    GetSmsAttributesResult,
    GetSmsSandboxAccountStatusResult,
    GetSubscriptionAttributesResult,
    GetTopicAttributesResult,
    ListEndpointsByPlatformApplicationResult,
    ListOriginationNumbersResult,
    ListPhoneNumbersOptedOutResult,
    ListPlatformApplicationsResult,
    ListSmsSandboxPhoneNumbersResult,
    ListSubscriptionsByTopicResult,
    ListSubscriptionsResult,
    ListTagsForResourceResult,
    ListTopicsResult,
    PublishResult,
    SubscribeResult,
)

__all__ = [
    "CheckIfPhoneNumberIsOptedOutResult",
    "ConfirmSubscriptionResult",
    "CreatePlatformApplicationResult",
    "CreatePlatformEndpointResult",
    "CreateTopicResult",
    "FanOutFailure",
    "GetDataProtectionPolicyResult",
    "GetEndpointAttributesResult",
    "GetPlatformApplicationAttributesResult",
    "GetSmsAttributesResult",
    "GetSmsSandboxAccountStatusResult",
    "GetSubscriptionAttributesResult",
    "GetTopicAttributesResult",
    "ListEndpointsByPlatformApplicationResult",
    "ListOriginationNumbersResult",
    "ListPhoneNumbersOptedOutResult",
    "ListPlatformApplicationsResult",
    "ListSmsSandboxPhoneNumbersResult",
    "ListSubscriptionsByTopicResult",
    "ListSubscriptionsResult",
    "ListTagsForResourceResult",
    "ListTopicsResult",
    "PublishResult",
    "SubscribeResult",
    "add_permission",
    "check_if_phone_number_is_opted_out",
    "confirm_subscription",
    "create_platform_application",
    "create_platform_endpoint",
    "create_sms_sandbox_phone_number",
    "create_topic",
    "create_topic_if_not_exists",
    "delete_endpoint",
    "delete_platform_application",
    "delete_sms_sandbox_phone_number",
    "delete_topic",
    "get_data_protection_policy",
    "get_endpoint_attributes",
    "get_platform_application_attributes",
    "get_sms_attributes",
    "get_sms_sandbox_account_status",
    "get_subscription_attributes",
    "get_topic_attributes",
    "list_endpoints_by_platform_application",
    "list_origination_numbers",
    "list_phone_numbers_opted_out",
    "list_platform_applications",
    "list_sms_sandbox_phone_numbers",
    "list_subscriptions",
    "list_subscriptions_by_topic",
    "list_tags_for_resource",
    "list_topics",
    "opt_in_phone_number",
    "publish",
    "publish_batch",
    "publish_fan_out",
    "put_data_protection_policy",
    "remove_permission",
    "set_endpoint_attributes",
    "set_platform_application_attributes",
    "set_sms_attributes",
    "set_subscription_attributes",
    "set_topic_attributes",
    "subscribe",
    "tag_resource",
    "unsubscribe",
    "untag_resource",
    "verify_sms_sandbox_phone_number",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def publish(
    topic_arn: str,
    message: str | dict | list,
    subject: str | None = None,
    message_group_id: str | None = None,
    message_deduplication_id: str | None = None,
    region_name: str | None = None,
) -> PublishResult:
    """Publish a single message to an SNS topic.

    Dicts and lists are serialised to JSON automatically.

    Args:
        topic_arn: ARN of the SNS topic.
        message: Message payload.  Dicts/lists are JSON-encoded.
        subject: Optional email subject used when the topic delivers to email
            subscriptions.
        message_group_id: Required for FIFO topics.
        message_deduplication_id: Deduplication ID for FIFO topics.
        region_name: AWS region override.

    Returns:
        A :class:`PublishResult` with the assigned message ID.

    Raises:
        RuntimeError: If the publish call fails.
    """
    raw_message = json.dumps(message) if isinstance(message, (dict, list)) else message
    kwargs: dict[str, Any] = {
        "TopicArn": topic_arn,
        "Message": raw_message,
    }
    if subject is not None:
        kwargs["Subject"] = subject
    if message_group_id is not None:
        kwargs["MessageGroupId"] = message_group_id
    if message_deduplication_id is not None:
        kwargs["MessageDeduplicationId"] = message_deduplication_id

    try:
        client = async_client("sns", region_name)
        resp = await client.call("Publish", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to publish to {topic_arn!r}") from exc
    return PublishResult(
        message_id=resp["MessageId"],
        sequence_number=resp.get("SequenceNumber"),
    )


async def publish_batch(
    topic_arn: str,
    messages: list[str | dict | list],
    region_name: str | None = None,
) -> list[PublishResult]:
    """Publish up to 10 messages in a single batch request.

    Args:
        topic_arn: ARN of the SNS topic.
        messages: List of message payloads (up to 10).  Dicts/lists are
            JSON-encoded.
        region_name: AWS region override.

    Returns:
        A list of :class:`PublishResult` for successfully published messages.

    Raises:
        RuntimeError: If the batch call fails or any message is rejected.
        ValueError: If more than 10 messages are supplied.
    """
    if len(messages) > 10:
        raise ValueError("publish_batch supports at most 10 messages per call")

    entries = [
        {
            "Id": str(i),
            "Message": json.dumps(m) if isinstance(m, (dict, list)) else m,
        }
        for i, m in enumerate(messages)
    ]
    try:
        client = async_client("sns", region_name)
        resp = await client.call(
            "PublishBatch",
            TopicArn=topic_arn,
            PublishBatchRequestEntries=entries,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to batch-publish to {topic_arn!r}") from exc

    if resp.get("Failed"):
        failures = [f.get("Message", f.get("Code")) for f in resp["Failed"]]
        raise AwsServiceError(f"Batch publish partially failed for {topic_arn!r}: {failures}")

    return [
        PublishResult(
            message_id=s["MessageId"],
            sequence_number=s.get("SequenceNumber"),
        )
        for s in resp.get("Successful", [])
    ]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def publish_fan_out(
    topic_arns: list[str],
    message: str | dict | list,
    subject: str | None = None,
    max_concurrency: int = 20,
    region_name: str | None = None,
) -> list[PublishResult]:
    """Publish the same message to multiple SNS topics concurrently.

    Uses ``asyncio`` with a semaphore to cap concurrency so total latency is
    bounded by the slowest topic rather than the sum of all topics.

    Args:
        topic_arns: List of SNS topic ARNs to publish to.
        message: Message payload (dicts/lists are JSON-encoded).
        subject: Optional subject for email subscriptions.
        max_concurrency: Maximum number of concurrent publish tasks
            (default ``20``).  Capped to ``len(topic_arns)``.
        region_name: AWS region override.

    Returns:
        A list of :class:`PublishResult` for **successfully** published topics,
        in the same order as the corresponding entries in *topic_arns*.

    Raises:
        AwsServiceError: If one or more publishes fail.  The exception message
            includes details about which topics failed.  Successfully published
            results are still collected before the exception is raised.
    """
    sem = asyncio.Semaphore(min(len(topic_arns), max_concurrency))
    results: dict[int, PublishResult] = {}
    failures: list[FanOutFailure] = []

    async def _publish(idx: int, arn: str) -> None:
        async with sem:
            try:
                results[idx] = await publish(arn, message, subject, region_name=region_name)
            except Exception as exc:
                failures.append(FanOutFailure(topic_arn=arn, error=str(exc)))

    await asyncio.gather(*[_publish(i, arn) for i, arn in enumerate(topic_arns)])

    if failures:
        failed_arns = [f.topic_arn for f in failures]
        raise AwsServiceError(
            f"publish_fan_out failed for {len(failures)}/{len(topic_arns)} topic(s): {failed_arns}"
        )

    return [results[i] for i in range(len(topic_arns))]


async def create_topic_if_not_exists(
    topic_name: str,
    fifo: bool = False,
    attributes: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Create an SNS topic or return the ARN of an existing one.

    ``CreateTopic`` is idempotent in SNS -- calling it with the same name
    returns the existing topic's ARN without error.

    Args:
        topic_name: Topic name.  For FIFO topics the ``.fifo`` suffix is
            appended automatically if absent.
        fifo: Create as a FIFO topic (default ``False``).
        attributes: Optional topic attributes (e.g. ``{"KmsMasterKeyId": ...}``).
        region_name: AWS region override.

    Returns:
        The ARN of the created or existing topic.

    Raises:
        RuntimeError: If topic creation fails.
    """
    name = topic_name
    if fifo and not name.endswith(".fifo"):
        name += ".fifo"
    kwargs: dict[str, Any] = {"Name": name}
    if fifo:
        attrs = {**(attributes or {}), "FifoTopic": "true"}
        kwargs["Attributes"] = attrs
    elif attributes:
        kwargs["Attributes"] = attributes
    try:
        client = async_client("sns", region_name)
        resp = await client.call("CreateTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create SNS topic {name!r}") from exc
    return resp["TopicArn"]


async def add_permission(
    topic_arn: str,
    label: str,
    aws_account_id: list[str],
    action_name: list[str],
    region_name: str | None = None,
) -> None:
    """Add permission.

    Args:
        topic_arn: Topic arn.
        label: Label.
        aws_account_id: Aws account id.
        action_name: Action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    kwargs["Label"] = label
    kwargs["AWSAccountId"] = aws_account_id
    kwargs["ActionName"] = action_name
    try:
        await client.call("AddPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add permission") from exc
    return None


async def check_if_phone_number_is_opted_out(
    phone_number: str,
    region_name: str | None = None,
) -> CheckIfPhoneNumberIsOptedOutResult:
    """Check if phone number is opted out.

    Args:
        phone_number: Phone number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["phoneNumber"] = phone_number
    try:
        resp = await client.call("CheckIfPhoneNumberIsOptedOut", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to check if phone number is opted out") from exc
    return CheckIfPhoneNumberIsOptedOutResult(
        is_opted_out=resp.get("isOptedOut"),
    )


async def confirm_subscription(
    topic_arn: str,
    token: str,
    *,
    authenticate_on_unsubscribe: str | None = None,
    region_name: str | None = None,
) -> ConfirmSubscriptionResult:
    """Confirm subscription.

    Args:
        topic_arn: Topic arn.
        token: Token.
        authenticate_on_unsubscribe: Authenticate on unsubscribe.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    kwargs["Token"] = token
    if authenticate_on_unsubscribe is not None:
        kwargs["AuthenticateOnUnsubscribe"] = authenticate_on_unsubscribe
    try:
        resp = await client.call("ConfirmSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to confirm subscription") from exc
    return ConfirmSubscriptionResult(
        subscription_arn=resp.get("SubscriptionArn"),
    )


async def create_platform_application(
    name: str,
    platform: str,
    attributes: dict[str, Any],
    region_name: str | None = None,
) -> CreatePlatformApplicationResult:
    """Create platform application.

    Args:
        name: Name.
        platform: Platform.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Platform"] = platform
    kwargs["Attributes"] = attributes
    try:
        resp = await client.call("CreatePlatformApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create platform application") from exc
    return CreatePlatformApplicationResult(
        platform_application_arn=resp.get("PlatformApplicationArn"),
    )


async def create_platform_endpoint(
    platform_application_arn: str,
    token: str,
    *,
    custom_user_data: str | None = None,
    attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePlatformEndpointResult:
    """Create platform endpoint.

    Args:
        platform_application_arn: Platform application arn.
        token: Token.
        custom_user_data: Custom user data.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformApplicationArn"] = platform_application_arn
    kwargs["Token"] = token
    if custom_user_data is not None:
        kwargs["CustomUserData"] = custom_user_data
    if attributes is not None:
        kwargs["Attributes"] = attributes
    try:
        resp = await client.call("CreatePlatformEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create platform endpoint") from exc
    return CreatePlatformEndpointResult(
        endpoint_arn=resp.get("EndpointArn"),
    )


async def create_sms_sandbox_phone_number(
    phone_number: str,
    *,
    language_code: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create sms sandbox phone number.

    Args:
        phone_number: Phone number.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumber"] = phone_number
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    try:
        await client.call("CreateSMSSandboxPhoneNumber", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create sms sandbox phone number") from exc
    return None


async def create_topic(
    name: str,
    *,
    attributes: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    data_protection_policy: str | None = None,
    region_name: str | None = None,
) -> CreateTopicResult:
    """Create topic.

    Args:
        name: Name.
        attributes: Attributes.
        tags: Tags.
        data_protection_policy: Data protection policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if tags is not None:
        kwargs["Tags"] = tags
    if data_protection_policy is not None:
        kwargs["DataProtectionPolicy"] = data_protection_policy
    try:
        resp = await client.call("CreateTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create topic") from exc
    return CreateTopicResult(
        topic_arn=resp.get("TopicArn"),
    )


async def delete_endpoint(
    endpoint_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete endpoint.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    try:
        await client.call("DeleteEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete endpoint") from exc
    return None


async def delete_platform_application(
    platform_application_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete platform application.

    Args:
        platform_application_arn: Platform application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformApplicationArn"] = platform_application_arn
    try:
        await client.call("DeletePlatformApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete platform application") from exc
    return None


async def delete_sms_sandbox_phone_number(
    phone_number: str,
    region_name: str | None = None,
) -> None:
    """Delete sms sandbox phone number.

    Args:
        phone_number: Phone number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumber"] = phone_number
    try:
        await client.call("DeleteSMSSandboxPhoneNumber", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete sms sandbox phone number") from exc
    return None


async def delete_topic(
    topic_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete topic.

    Args:
        topic_arn: Topic arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    try:
        await client.call("DeleteTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete topic") from exc
    return None


async def get_data_protection_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetDataProtectionPolicyResult:
    """Get data protection policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetDataProtectionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data protection policy") from exc
    return GetDataProtectionPolicyResult(
        data_protection_policy=resp.get("DataProtectionPolicy"),
    )


async def get_endpoint_attributes(
    endpoint_arn: str,
    region_name: str | None = None,
) -> GetEndpointAttributesResult:
    """Get endpoint attributes.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    try:
        resp = await client.call("GetEndpointAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get endpoint attributes") from exc
    return GetEndpointAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def get_platform_application_attributes(
    platform_application_arn: str,
    region_name: str | None = None,
) -> GetPlatformApplicationAttributesResult:
    """Get platform application attributes.

    Args:
        platform_application_arn: Platform application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformApplicationArn"] = platform_application_arn
    try:
        resp = await client.call("GetPlatformApplicationAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get platform application attributes") from exc
    return GetPlatformApplicationAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def get_sms_attributes(
    *,
    attributes: list[str] | None = None,
    region_name: str | None = None,
) -> GetSmsAttributesResult:
    """Get sms attributes.

    Args:
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if attributes is not None:
        kwargs["attributes"] = attributes
    try:
        resp = await client.call("GetSMSAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sms attributes") from exc
    return GetSmsAttributesResult(
        attributes=resp.get("attributes"),
    )


async def get_sms_sandbox_account_status(
    region_name: str | None = None,
) -> GetSmsSandboxAccountStatusResult:
    """Get sms sandbox account status.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetSMSSandboxAccountStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sms sandbox account status") from exc
    return GetSmsSandboxAccountStatusResult(
        is_in_sandbox=resp.get("IsInSandbox"),
    )


async def get_subscription_attributes(
    subscription_arn: str,
    region_name: str | None = None,
) -> GetSubscriptionAttributesResult:
    """Get subscription attributes.

    Args:
        subscription_arn: Subscription arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionArn"] = subscription_arn
    try:
        resp = await client.call("GetSubscriptionAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get subscription attributes") from exc
    return GetSubscriptionAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def get_topic_attributes(
    topic_arn: str,
    region_name: str | None = None,
) -> GetTopicAttributesResult:
    """Get topic attributes.

    Args:
        topic_arn: Topic arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    try:
        resp = await client.call("GetTopicAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get topic attributes") from exc
    return GetTopicAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def list_endpoints_by_platform_application(
    platform_application_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListEndpointsByPlatformApplicationResult:
    """List endpoints by platform application.

    Args:
        platform_application_arn: Platform application arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformApplicationArn"] = platform_application_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListEndpointsByPlatformApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list endpoints by platform application") from exc
    return ListEndpointsByPlatformApplicationResult(
        endpoints=resp.get("Endpoints"),
        next_token=resp.get("NextToken"),
    )


async def list_origination_numbers(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListOriginationNumbersResult:
    """List origination numbers.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListOriginationNumbers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list origination numbers") from exc
    return ListOriginationNumbersResult(
        next_token=resp.get("NextToken"),
        phone_numbers=resp.get("PhoneNumbers"),
    )


async def list_phone_numbers_opted_out(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPhoneNumbersOptedOutResult:
    """List phone numbers opted out.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPhoneNumbersOptedOut", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list phone numbers opted out") from exc
    return ListPhoneNumbersOptedOutResult(
        phone_numbers=resp.get("phoneNumbers"),
        next_token=resp.get("nextToken"),
    )


async def list_platform_applications(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPlatformApplicationsResult:
    """List platform applications.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListPlatformApplications", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list platform applications") from exc
    return ListPlatformApplicationsResult(
        platform_applications=resp.get("PlatformApplications"),
        next_token=resp.get("NextToken"),
    )


async def list_sms_sandbox_phone_numbers(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSmsSandboxPhoneNumbersResult:
    """List sms sandbox phone numbers.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListSMSSandboxPhoneNumbers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sms sandbox phone numbers") from exc
    return ListSmsSandboxPhoneNumbersResult(
        phone_numbers=resp.get("PhoneNumbers"),
        next_token=resp.get("NextToken"),
    )


async def list_subscriptions(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSubscriptionsResult:
    """List subscriptions.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSubscriptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list subscriptions") from exc
    return ListSubscriptionsResult(
        subscriptions=resp.get("Subscriptions"),
        next_token=resp.get("NextToken"),
    )


async def list_subscriptions_by_topic(
    topic_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSubscriptionsByTopicResult:
    """List subscriptions by topic.

    Args:
        topic_arn: Topic arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSubscriptionsByTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list subscriptions by topic") from exc
    return ListSubscriptionsByTopicResult(
        subscriptions=resp.get("Subscriptions"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_topics(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTopicsResult:
    """List topics.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTopics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list topics") from exc
    return ListTopicsResult(
        topics=resp.get("Topics"),
        next_token=resp.get("NextToken"),
    )


async def opt_in_phone_number(
    phone_number: str,
    region_name: str | None = None,
) -> None:
    """Opt in phone number.

    Args:
        phone_number: Phone number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["phoneNumber"] = phone_number
    try:
        await client.call("OptInPhoneNumber", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to opt in phone number") from exc
    return None


async def put_data_protection_policy(
    resource_arn: str,
    data_protection_policy: str,
    region_name: str | None = None,
) -> None:
    """Put data protection policy.

    Args:
        resource_arn: Resource arn.
        data_protection_policy: Data protection policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["DataProtectionPolicy"] = data_protection_policy
    try:
        await client.call("PutDataProtectionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put data protection policy") from exc
    return None


async def remove_permission(
    topic_arn: str,
    label: str,
    region_name: str | None = None,
) -> None:
    """Remove permission.

    Args:
        topic_arn: Topic arn.
        label: Label.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    kwargs["Label"] = label
    try:
        await client.call("RemovePermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove permission") from exc
    return None


async def set_endpoint_attributes(
    endpoint_arn: str,
    attributes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Set endpoint attributes.

    Args:
        endpoint_arn: Endpoint arn.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    kwargs["Attributes"] = attributes
    try:
        await client.call("SetEndpointAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set endpoint attributes") from exc
    return None


async def set_platform_application_attributes(
    platform_application_arn: str,
    attributes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Set platform application attributes.

    Args:
        platform_application_arn: Platform application arn.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformApplicationArn"] = platform_application_arn
    kwargs["Attributes"] = attributes
    try:
        await client.call("SetPlatformApplicationAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set platform application attributes") from exc
    return None


async def set_sms_attributes(
    attributes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Set sms attributes.

    Args:
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["attributes"] = attributes
    try:
        await client.call("SetSMSAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set sms attributes") from exc
    return None


async def set_subscription_attributes(
    subscription_arn: str,
    attribute_name: str,
    *,
    attribute_value: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set subscription attributes.

    Args:
        subscription_arn: Subscription arn.
        attribute_name: Attribute name.
        attribute_value: Attribute value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionArn"] = subscription_arn
    kwargs["AttributeName"] = attribute_name
    if attribute_value is not None:
        kwargs["AttributeValue"] = attribute_value
    try:
        await client.call("SetSubscriptionAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set subscription attributes") from exc
    return None


async def set_topic_attributes(
    topic_arn: str,
    attribute_name: str,
    *,
    attribute_value: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set topic attributes.

    Args:
        topic_arn: Topic arn.
        attribute_name: Attribute name.
        attribute_value: Attribute value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    kwargs["AttributeName"] = attribute_name
    if attribute_value is not None:
        kwargs["AttributeValue"] = attribute_value
    try:
        await client.call("SetTopicAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set topic attributes") from exc
    return None


async def subscribe(
    topic_arn: str,
    protocol: str,
    *,
    endpoint: str | None = None,
    attributes: dict[str, Any] | None = None,
    return_subscription_arn: bool | None = None,
    region_name: str | None = None,
) -> SubscribeResult:
    """Subscribe.

    Args:
        topic_arn: Topic arn.
        protocol: Protocol.
        endpoint: Endpoint.
        attributes: Attributes.
        return_subscription_arn: Return subscription arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TopicArn"] = topic_arn
    kwargs["Protocol"] = protocol
    if endpoint is not None:
        kwargs["Endpoint"] = endpoint
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if return_subscription_arn is not None:
        kwargs["ReturnSubscriptionArn"] = return_subscription_arn
    try:
        resp = await client.call("Subscribe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to subscribe") from exc
    return SubscribeResult(
        subscription_arn=resp.get("SubscriptionArn"),
    )


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def unsubscribe(
    subscription_arn: str,
    region_name: str | None = None,
) -> None:
    """Unsubscribe.

    Args:
        subscription_arn: Subscription arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionArn"] = subscription_arn
    try:
        await client.call("Unsubscribe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to unsubscribe") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def verify_sms_sandbox_phone_number(
    phone_number: str,
    one_time_password: str,
    region_name: str | None = None,
) -> None:
    """Verify sms sandbox phone number.

    Args:
        phone_number: Phone number.
        one_time_password: One time password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sns", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumber"] = phone_number
    kwargs["OneTimePassword"] = one_time_password
    try:
        await client.call("VerifySMSSandboxPhoneNumber", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to verify sms sandbox phone number") from exc
    return None
