"""Tests for aws_util.sns module."""
from __future__ import annotations

import boto3
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.sns import (
    FanOutFailure,
    PublishResult,
    create_topic_if_not_exists,
    publish,
    publish_batch,
    publish_fan_out,
    add_permission,
    check_if_phone_number_is_opted_out,
    confirm_subscription,
    create_platform_application,
    create_platform_endpoint,
    create_sms_sandbox_phone_number,
    create_topic,
    delete_endpoint,
    delete_platform_application,
    delete_sms_sandbox_phone_number,
    delete_topic,
    get_data_protection_policy,
    get_endpoint_attributes,
    get_platform_application_attributes,
    get_sms_attributes,
    get_sms_sandbox_account_status,
    get_subscription_attributes,
    get_topic_attributes,
    list_endpoints_by_platform_application,
    list_origination_numbers,
    list_phone_numbers_opted_out,
    list_platform_applications,
    list_sms_sandbox_phone_numbers,
    list_subscriptions,
    list_subscriptions_by_topic,
    list_tags_for_resource,
    list_topics,
    opt_in_phone_number,
    put_data_protection_policy,
    remove_permission,
    set_endpoint_attributes,
    set_platform_application_attributes,
    set_sms_attributes,
    set_subscription_attributes,
    set_topic_attributes,
    subscribe,
    tag_resource,
    unsubscribe,
    untag_resource,
    verify_sms_sandbox_phone_number,
)

REGION = "us-east-1"
TOPIC_NAME = "test-topic"


@pytest.fixture
def topic(sns_client):
    _, topic_arn = sns_client
    return topic_arn


@pytest.fixture
def extra_topic():
    client = boto3.client("sns", region_name=REGION)
    resp = client.create_topic(Name="extra-topic")
    return resp["TopicArn"]


# ---------------------------------------------------------------------------
# publish
# ---------------------------------------------------------------------------


def test_publish_string_message(topic):
    result = publish(topic, "hello world", region_name=REGION)
    assert isinstance(result, PublishResult)
    assert result.message_id


def test_publish_dict_message(topic):
    result = publish(topic, {"event": "user.created", "user_id": 1}, region_name=REGION)
    assert result.message_id


def test_publish_list_message(topic):
    result = publish(topic, [1, 2, 3], region_name=REGION)
    assert result.message_id


def test_publish_with_subject(topic):
    result = publish(topic, "alert!", subject="Test Alert", region_name=REGION)
    assert result.message_id


def test_publish_runtime_error():
    with pytest.raises(RuntimeError, match="Failed to publish"):
        publish("arn:aws:sns:us-east-1:000000000000:nonexistent", "msg", region_name=REGION)


def test_publish_with_fifo_attributes():
    client = boto3.client("sns", region_name=REGION)
    resp = client.create_topic(
        Name="test-fifo.fifo",
        Attributes={"FifoTopic": "true", "ContentBasedDeduplication": "true"},
    )
    fifo_arn = resp["TopicArn"]
    result = publish(
        fifo_arn,
        "msg",
        message_group_id="grp1",
        message_deduplication_id="dedup1",
        region_name=REGION,
    )
    assert result.message_id


# ---------------------------------------------------------------------------
# publish_batch
# ---------------------------------------------------------------------------


def test_publish_batch(topic):
    results = publish_batch(topic, ["msg1", "msg2", "msg3"], region_name=REGION)
    assert len(results) == 3
    assert all(isinstance(r, PublishResult) for r in results)


def test_publish_batch_dict_messages(topic):
    results = publish_batch(topic, [{"a": 1}, {"b": 2}], region_name=REGION)
    assert len(results) == 2


def test_publish_batch_too_many():
    with pytest.raises(ValueError, match="at most 10"):
        publish_batch("arn", [f"m{i}" for i in range(11)], region_name=REGION)


def test_publish_batch_runtime_error():
    with pytest.raises(RuntimeError, match="Failed to batch-publish"):
        publish_batch(
            "arn:aws:sns:us-east-1:000000000000:nonexistent",
            ["msg"],
            region_name=REGION,
        )


def test_publish_batch_partial_failure(topic, monkeypatch):
    import aws_util.sns as snsmod

    real_get_client = snsmod.get_client

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)
        original_publish_batch = client.publish_batch

        def fake_publish_batch(**kwargs):
            resp = original_publish_batch(**kwargs)
            resp["Failed"] = [{"Id": "0", "Code": "err", "Message": "fail"}]
            resp["Successful"] = []
            return resp

        client.publish_batch = fake_publish_batch
        return client

    monkeypatch.setattr(snsmod, "get_client", patched_get_client)
    with pytest.raises(RuntimeError, match="Batch publish partially failed"):
        publish_batch(topic, ["msg1"], region_name=REGION)


# ---------------------------------------------------------------------------
# publish_fan_out
# ---------------------------------------------------------------------------


def test_publish_fan_out(topic, extra_topic):
    results = publish_fan_out(
        [topic, extra_topic],
        "broadcast message",
        region_name=REGION,
    )
    assert len(results) == 2
    assert all(isinstance(r, PublishResult) for r in results)


def test_publish_fan_out_with_subject(topic, extra_topic):
    results = publish_fan_out(
        [topic, extra_topic],
        "msg",
        subject="Alert",
        region_name=REGION,
    )
    assert len(results) == 2


def test_publish_fan_out_single_topic(topic):
    results = publish_fan_out([topic], "single", region_name=REGION)
    assert len(results) == 1


def test_publish_fan_out_failure_raises_with_details(topic):
    """When one topic fails, AwsServiceError is raised after all futures complete."""
    bad_arn = "arn:aws:sns:us-east-1:000000000000:does-not-exist"
    with pytest.raises(RuntimeError, match="publish_fan_out failed"):
        publish_fan_out(
            [topic, bad_arn],
            "broadcast",
            region_name=REGION,
        )


def test_publish_fan_out_respects_max_concurrency(topic, extra_topic):
    """max_concurrency parameter is accepted and does not break behaviour."""
    results = publish_fan_out(
        [topic, extra_topic],
        "msg",
        max_concurrency=1,
        region_name=REGION,
    )
    assert len(results) == 2


def test_fanout_failure_model():
    f = FanOutFailure(topic_arn="arn:aws:sns:us-east-1:123:t", error="boom")
    assert f.topic_arn.endswith(":t")
    assert f.error == "boom"


def test_create_topic_fifo_overrides_caller_false():
    """FifoTopic=true must win even if caller passes FifoTopic=false."""
    arn = create_topic_if_not_exists(
        "override-fifo",
        fifo=True,
        attributes={"FifoTopic": "false"},
        region_name=REGION,
    )
    assert "override-fifo.fifo" in arn


# ---------------------------------------------------------------------------
# create_topic_if_not_exists
# ---------------------------------------------------------------------------


def test_create_topic_if_not_exists_creates_new():
    arn = create_topic_if_not_exists("new-topic", region_name=REGION)
    assert "new-topic" in arn


def test_create_topic_if_not_exists_returns_existing(topic):
    # SNS CreateTopic is idempotent
    arn1 = create_topic_if_not_exists(TOPIC_NAME, region_name=REGION)
    arn2 = create_topic_if_not_exists(TOPIC_NAME, region_name=REGION)
    assert arn1 == arn2


def test_create_topic_if_not_exists_fifo():
    arn = create_topic_if_not_exists("my-fifo", fifo=True, region_name=REGION)
    assert "my-fifo.fifo" in arn


def test_create_topic_if_not_exists_fifo_already_has_suffix():
    arn = create_topic_if_not_exists("already.fifo", fifo=True, region_name=REGION)
    assert arn.endswith("already.fifo")


def test_create_topic_if_not_exists_with_attributes():
    arn = create_topic_if_not_exists(
        "attr-topic",
        attributes={"DisplayName": "My Topic"},
        region_name=REGION,
    )
    assert arn


def test_create_topic_if_not_exists_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.sns as snsmod

    mock_client = MagicMock()
    mock_client.create_topic.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "CreateTopic",
    )
    monkeypatch.setattr(snsmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create SNS topic"):
        create_topic_if_not_exists("fail-topic", region_name=REGION)


def test_add_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_permission.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    add_permission("test-topic_arn", "test-label", [], [], region_name=REGION)
    mock_client.add_permission.assert_called_once()


def test_add_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_permission",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add permission"):
        add_permission("test-topic_arn", "test-label", [], [], region_name=REGION)


def test_check_if_phone_number_is_opted_out(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_if_phone_number_is_opted_out.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    check_if_phone_number_is_opted_out("test-phone_number", region_name=REGION)
    mock_client.check_if_phone_number_is_opted_out.assert_called_once()


def test_check_if_phone_number_is_opted_out_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_if_phone_number_is_opted_out.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "check_if_phone_number_is_opted_out",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to check if phone number is opted out"):
        check_if_phone_number_is_opted_out("test-phone_number", region_name=REGION)


def test_confirm_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_subscription.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    confirm_subscription("test-topic_arn", "test-token", region_name=REGION)
    mock_client.confirm_subscription.assert_called_once()


def test_confirm_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_subscription",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to confirm subscription"):
        confirm_subscription("test-topic_arn", "test-token", region_name=REGION)


def test_create_platform_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_platform_application.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_platform_application("test-name", "test-platform", {}, region_name=REGION)
    mock_client.create_platform_application.assert_called_once()


def test_create_platform_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_platform_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_platform_application",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create platform application"):
        create_platform_application("test-name", "test-platform", {}, region_name=REGION)


def test_create_platform_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_platform_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_platform_endpoint("test-platform_application_arn", "test-token", region_name=REGION)
    mock_client.create_platform_endpoint.assert_called_once()


def test_create_platform_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_platform_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_platform_endpoint",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create platform endpoint"):
        create_platform_endpoint("test-platform_application_arn", "test-token", region_name=REGION)


def test_create_sms_sandbox_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_sms_sandbox_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_sms_sandbox_phone_number("test-phone_number", region_name=REGION)
    mock_client.create_sms_sandbox_phone_number.assert_called_once()


def test_create_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_sms_sandbox_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_sms_sandbox_phone_number",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create sms sandbox phone number"):
        create_sms_sandbox_phone_number("test-phone_number", region_name=REGION)


def test_create_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_topic("test-name", region_name=REGION)
    mock_client.create_topic.assert_called_once()


def test_create_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_topic",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create topic"):
        create_topic("test-name", region_name=REGION)


def test_delete_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    delete_endpoint("test-endpoint_arn", region_name=REGION)
    mock_client.delete_endpoint.assert_called_once()


def test_delete_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_endpoint",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete endpoint"):
        delete_endpoint("test-endpoint_arn", region_name=REGION)


def test_delete_platform_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_platform_application.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    delete_platform_application("test-platform_application_arn", region_name=REGION)
    mock_client.delete_platform_application.assert_called_once()


def test_delete_platform_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_platform_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_platform_application",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete platform application"):
        delete_platform_application("test-platform_application_arn", region_name=REGION)


def test_delete_sms_sandbox_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_sms_sandbox_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    delete_sms_sandbox_phone_number("test-phone_number", region_name=REGION)
    mock_client.delete_sms_sandbox_phone_number.assert_called_once()


def test_delete_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_sms_sandbox_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_sms_sandbox_phone_number",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete sms sandbox phone number"):
        delete_sms_sandbox_phone_number("test-phone_number", region_name=REGION)


def test_delete_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    delete_topic("test-topic_arn", region_name=REGION)
    mock_client.delete_topic.assert_called_once()


def test_delete_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_topic",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete topic"):
        delete_topic("test-topic_arn", region_name=REGION)


def test_get_data_protection_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_protection_policy.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_data_protection_policy("test-resource_arn", region_name=REGION)
    mock_client.get_data_protection_policy.assert_called_once()


def test_get_data_protection_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_protection_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_protection_policy",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data protection policy"):
        get_data_protection_policy("test-resource_arn", region_name=REGION)


def test_get_endpoint_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_endpoint_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_endpoint_attributes("test-endpoint_arn", region_name=REGION)
    mock_client.get_endpoint_attributes.assert_called_once()


def test_get_endpoint_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_endpoint_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_endpoint_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get endpoint attributes"):
        get_endpoint_attributes("test-endpoint_arn", region_name=REGION)


def test_get_platform_application_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_platform_application_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_platform_application_attributes("test-platform_application_arn", region_name=REGION)
    mock_client.get_platform_application_attributes.assert_called_once()


def test_get_platform_application_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_platform_application_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_platform_application_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get platform application attributes"):
        get_platform_application_attributes("test-platform_application_arn", region_name=REGION)


def test_get_sms_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sms_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_sms_attributes(region_name=REGION)
    mock_client.get_sms_attributes.assert_called_once()


def test_get_sms_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sms_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sms_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get sms attributes"):
        get_sms_attributes(region_name=REGION)


def test_get_sms_sandbox_account_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sms_sandbox_account_status.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_sms_sandbox_account_status(region_name=REGION)
    mock_client.get_sms_sandbox_account_status.assert_called_once()


def test_get_sms_sandbox_account_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sms_sandbox_account_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sms_sandbox_account_status",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get sms sandbox account status"):
        get_sms_sandbox_account_status(region_name=REGION)


def test_get_subscription_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_subscription_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_subscription_attributes("test-subscription_arn", region_name=REGION)
    mock_client.get_subscription_attributes.assert_called_once()


def test_get_subscription_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_subscription_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_subscription_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get subscription attributes"):
        get_subscription_attributes("test-subscription_arn", region_name=REGION)


def test_get_topic_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_topic_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_topic_attributes("test-topic_arn", region_name=REGION)
    mock_client.get_topic_attributes.assert_called_once()


def test_get_topic_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_topic_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_topic_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get topic attributes"):
        get_topic_attributes("test-topic_arn", region_name=REGION)


def test_list_endpoints_by_platform_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints_by_platform_application.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_endpoints_by_platform_application("test-platform_application_arn", region_name=REGION)
    mock_client.list_endpoints_by_platform_application.assert_called_once()


def test_list_endpoints_by_platform_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints_by_platform_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_endpoints_by_platform_application",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list endpoints by platform application"):
        list_endpoints_by_platform_application("test-platform_application_arn", region_name=REGION)


def test_list_origination_numbers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_origination_numbers.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_origination_numbers(region_name=REGION)
    mock_client.list_origination_numbers.assert_called_once()


def test_list_origination_numbers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_origination_numbers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_origination_numbers",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list origination numbers"):
        list_origination_numbers(region_name=REGION)


def test_list_phone_numbers_opted_out(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers_opted_out.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers_opted_out(region_name=REGION)
    mock_client.list_phone_numbers_opted_out.assert_called_once()


def test_list_phone_numbers_opted_out_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers_opted_out.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_phone_numbers_opted_out",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list phone numbers opted out"):
        list_phone_numbers_opted_out(region_name=REGION)


def test_list_platform_applications(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_platform_applications.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_platform_applications(region_name=REGION)
    mock_client.list_platform_applications.assert_called_once()


def test_list_platform_applications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_platform_applications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_platform_applications",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list platform applications"):
        list_platform_applications(region_name=REGION)


def test_list_sms_sandbox_phone_numbers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sms_sandbox_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_sms_sandbox_phone_numbers(region_name=REGION)
    mock_client.list_sms_sandbox_phone_numbers.assert_called_once()


def test_list_sms_sandbox_phone_numbers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sms_sandbox_phone_numbers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sms_sandbox_phone_numbers",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list sms sandbox phone numbers"):
        list_sms_sandbox_phone_numbers(region_name=REGION)


def test_list_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_subscriptions(region_name=REGION)
    mock_client.list_subscriptions.assert_called_once()


def test_list_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_subscriptions",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list subscriptions"):
        list_subscriptions(region_name=REGION)


def test_list_subscriptions_by_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_subscriptions_by_topic.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_subscriptions_by_topic("test-topic_arn", region_name=REGION)
    mock_client.list_subscriptions_by_topic.assert_called_once()


def test_list_subscriptions_by_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_subscriptions_by_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_subscriptions_by_topic",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list subscriptions by topic"):
        list_subscriptions_by_topic("test-topic_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_topics(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_topics(region_name=REGION)
    mock_client.list_topics.assert_called_once()


def test_list_topics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topics",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list topics"):
        list_topics(region_name=REGION)


def test_opt_in_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.opt_in_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    opt_in_phone_number("test-phone_number", region_name=REGION)
    mock_client.opt_in_phone_number.assert_called_once()


def test_opt_in_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.opt_in_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "opt_in_phone_number",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to opt in phone number"):
        opt_in_phone_number("test-phone_number", region_name=REGION)


def test_put_data_protection_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_protection_policy.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    put_data_protection_policy("test-resource_arn", "test-data_protection_policy", region_name=REGION)
    mock_client.put_data_protection_policy.assert_called_once()


def test_put_data_protection_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_protection_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_data_protection_policy",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put data protection policy"):
        put_data_protection_policy("test-resource_arn", "test-data_protection_policy", region_name=REGION)


def test_remove_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    remove_permission("test-topic_arn", "test-label", region_name=REGION)
    mock_client.remove_permission.assert_called_once()


def test_remove_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_permission",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove permission"):
        remove_permission("test-topic_arn", "test-label", region_name=REGION)


def test_set_endpoint_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_endpoint_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_endpoint_attributes("test-endpoint_arn", {}, region_name=REGION)
    mock_client.set_endpoint_attributes.assert_called_once()


def test_set_endpoint_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_endpoint_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_endpoint_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set endpoint attributes"):
        set_endpoint_attributes("test-endpoint_arn", {}, region_name=REGION)


def test_set_platform_application_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_platform_application_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_platform_application_attributes("test-platform_application_arn", {}, region_name=REGION)
    mock_client.set_platform_application_attributes.assert_called_once()


def test_set_platform_application_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_platform_application_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_platform_application_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set platform application attributes"):
        set_platform_application_attributes("test-platform_application_arn", {}, region_name=REGION)


def test_set_sms_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_sms_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_sms_attributes({}, region_name=REGION)
    mock_client.set_sms_attributes.assert_called_once()


def test_set_sms_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_sms_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_sms_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set sms attributes"):
        set_sms_attributes({}, region_name=REGION)


def test_set_subscription_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_subscription_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_subscription_attributes("test-subscription_arn", "test-attribute_name", region_name=REGION)
    mock_client.set_subscription_attributes.assert_called_once()


def test_set_subscription_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_subscription_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_subscription_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set subscription attributes"):
        set_subscription_attributes("test-subscription_arn", "test-attribute_name", region_name=REGION)


def test_set_topic_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_topic_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_topic_attributes("test-topic_arn", "test-attribute_name", region_name=REGION)
    mock_client.set_topic_attributes.assert_called_once()


def test_set_topic_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_topic_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_topic_attributes",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set topic attributes"):
        set_topic_attributes("test-topic_arn", "test-attribute_name", region_name=REGION)


def test_subscribe(monkeypatch):
    mock_client = MagicMock()
    mock_client.subscribe.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    subscribe("test-topic_arn", "test-protocol", region_name=REGION)
    mock_client.subscribe.assert_called_once()


def test_subscribe_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.subscribe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "subscribe",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to subscribe"):
        subscribe("test-topic_arn", "test-protocol", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_unsubscribe(monkeypatch):
    mock_client = MagicMock()
    mock_client.unsubscribe.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    unsubscribe("test-subscription_arn", region_name=REGION)
    mock_client.unsubscribe.assert_called_once()


def test_unsubscribe_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unsubscribe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unsubscribe",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unsubscribe"):
        unsubscribe("test-subscription_arn", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_verify_sms_sandbox_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_sms_sandbox_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    verify_sms_sandbox_phone_number("test-phone_number", "test-one_time_password", region_name=REGION)
    mock_client.verify_sms_sandbox_phone_number.assert_called_once()


def test_verify_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_sms_sandbox_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_sms_sandbox_phone_number",
    )
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify sms sandbox phone number"):
        verify_sms_sandbox_phone_number("test-phone_number", "test-one_time_password", region_name=REGION)


def test_confirm_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import confirm_subscription
    mock_client = MagicMock()
    mock_client.confirm_subscription.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    confirm_subscription("test-topic_arn", "test-token", authenticate_on_unsubscribe="test-authenticate_on_unsubscribe", region_name="us-east-1")
    mock_client.confirm_subscription.assert_called_once()

def test_create_platform_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import create_platform_endpoint
    mock_client = MagicMock()
    mock_client.create_platform_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_platform_endpoint("test-platform_application_arn", "test-token", custom_user_data="test-custom_user_data", attributes="test-attributes", region_name="us-east-1")
    mock_client.create_platform_endpoint.assert_called_once()

def test_create_sms_sandbox_phone_number_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import create_sms_sandbox_phone_number
    mock_client = MagicMock()
    mock_client.create_sms_sandbox_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_sms_sandbox_phone_number("test-phone_number", language_code="test-language_code", region_name="us-east-1")
    mock_client.create_sms_sandbox_phone_number.assert_called_once()

def test_create_topic_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import create_topic
    mock_client = MagicMock()
    mock_client.create_topic.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    create_topic("test-name", attributes="test-attributes", tags=[{"Key": "k", "Value": "v"}], data_protection_policy="{}", region_name="us-east-1")
    mock_client.create_topic.assert_called_once()

def test_get_sms_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import get_sms_attributes
    mock_client = MagicMock()
    mock_client.get_sms_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    get_sms_attributes(attributes="test-attributes", region_name="us-east-1")
    mock_client.get_sms_attributes.assert_called_once()

def test_list_endpoints_by_platform_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_endpoints_by_platform_application
    mock_client = MagicMock()
    mock_client.list_endpoints_by_platform_application.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_endpoints_by_platform_application("test-platform_application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_endpoints_by_platform_application.assert_called_once()

def test_list_origination_numbers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_origination_numbers
    mock_client = MagicMock()
    mock_client.list_origination_numbers.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_origination_numbers(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_origination_numbers.assert_called_once()

def test_list_phone_numbers_opted_out_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_phone_numbers_opted_out
    mock_client = MagicMock()
    mock_client.list_phone_numbers_opted_out.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers_opted_out(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_phone_numbers_opted_out.assert_called_once()

def test_list_platform_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_platform_applications
    mock_client = MagicMock()
    mock_client.list_platform_applications.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_platform_applications(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_platform_applications.assert_called_once()

def test_list_sms_sandbox_phone_numbers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_sms_sandbox_phone_numbers
    mock_client = MagicMock()
    mock_client.list_sms_sandbox_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_sms_sandbox_phone_numbers(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_sms_sandbox_phone_numbers.assert_called_once()

def test_list_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_subscriptions
    mock_client = MagicMock()
    mock_client.list_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_subscriptions(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_subscriptions.assert_called_once()

def test_list_subscriptions_by_topic_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_subscriptions_by_topic
    mock_client = MagicMock()
    mock_client.list_subscriptions_by_topic.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_subscriptions_by_topic("test-topic_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_subscriptions_by_topic.assert_called_once()

def test_list_topics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import list_topics
    mock_client = MagicMock()
    mock_client.list_topics.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    list_topics(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_topics.assert_called_once()

def test_set_subscription_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import set_subscription_attributes
    mock_client = MagicMock()
    mock_client.set_subscription_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_subscription_attributes("test-subscription_arn", "test-attribute_name", attribute_value="test-attribute_value", region_name="us-east-1")
    mock_client.set_subscription_attributes.assert_called_once()

def test_set_topic_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import set_topic_attributes
    mock_client = MagicMock()
    mock_client.set_topic_attributes.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    set_topic_attributes("test-topic_arn", "test-attribute_name", attribute_value="test-attribute_value", region_name="us-east-1")
    mock_client.set_topic_attributes.assert_called_once()

def test_subscribe_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sns import subscribe
    mock_client = MagicMock()
    mock_client.subscribe.return_value = {}
    monkeypatch.setattr("aws_util.sns.get_client", lambda *a, **kw: mock_client)
    subscribe("test-topic_arn", "test-protocol", endpoint="test-endpoint", attributes="test-attributes", return_subscription_arn="test-return_subscription_arn", region_name="us-east-1")
    mock_client.subscribe.assert_called_once()
