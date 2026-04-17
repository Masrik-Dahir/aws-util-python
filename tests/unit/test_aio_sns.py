"""Tests for aws_util.aio.sns — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.sns import (
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


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# -- publish -----------------------------------------------------------------

async def test_publish_string(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await publish("arn:topic", "hello")
    assert isinstance(r, PublishResult)
    assert r.message_id == "m1"
    assert r.sequence_number is None


async def test_publish_dict(monkeypatch):
    mc = _mc({"MessageId": "m2", "SequenceNumber": "1"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await publish("arn:topic", {"key": "val"})
    assert r.sequence_number == "1"


async def test_publish_list(monkeypatch):
    mc = _mc({"MessageId": "m3"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    await publish("arn:topic", [1, 2])


async def test_publish_with_all_options(monkeypatch):
    mc = _mc({"MessageId": "m4"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    await publish(
        "arn:topic", "msg",
        subject="sub",
        message_group_id="grp",
        message_deduplication_id="dup",
    )
    kw = mc.call.call_args[1]
    assert kw["Subject"] == "sub"
    assert kw["MessageGroupId"] == "grp"
    assert kw["MessageDeduplicationId"] == "dup"


async def test_publish_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to publish"):
        await publish("arn:topic", "msg")


# -- publish_batch -----------------------------------------------------------

async def test_publish_batch_ok(monkeypatch):
    mc = _mc({"Successful": [{"MessageId": "m1"}, {"MessageId": "m2"}]})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await publish_batch("arn:topic", ["a", "b"])
    assert len(r) == 2


async def test_publish_batch_dict_messages(monkeypatch):
    mc = _mc({"Successful": [{"MessageId": "m1", "SequenceNumber": "1"}]})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await publish_batch("arn:topic", [{"k": "v"}])
    assert r[0].sequence_number == "1"


async def test_publish_batch_too_many():
    with pytest.raises(ValueError, match="at most 10"):
        await publish_batch("arn:topic", ["x"] * 11)


async def test_publish_batch_partial_failure(monkeypatch):
    mc = _mc({"Failed": [{"Message": "err"}], "Successful": []})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="partially failed"):
        await publish_batch("arn:topic", ["a"])


async def test_publish_batch_partial_failure_code(monkeypatch):
    mc = _mc({"Failed": [{"Code": "InternalError"}], "Successful": []})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="partially failed"):
        await publish_batch("arn:topic", ["a"])


async def test_publish_batch_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to batch-publish"):
        await publish_batch("arn:topic", ["a"])


# -- publish_fan_out ---------------------------------------------------------

async def test_publish_fan_out(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await publish_fan_out(["arn:t1", "arn:t2"], "msg", subject="s")
    assert len(r) == 2


async def test_publish_fan_out_partial_failure(monkeypatch):
    """When one or more publishes fail, AwsServiceError is raised."""
    call_count = 0

    async def fake_call(op, **kw):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"MessageId": "m1"}
        raise RuntimeError("sns boom")

    mc = AsyncMock()
    mc.call = fake_call
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="publish_fan_out failed"):
        await publish_fan_out(["arn:t1", "arn:t2"], "msg")


# -- create_topic_if_not_exists ----------------------------------------------

async def test_create_topic_standard(monkeypatch):
    mc = _mc({"TopicArn": "arn:topic"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await create_topic_if_not_exists("my-topic")
    assert r == "arn:topic"
    kw = mc.call.call_args[1]
    assert "Attributes" not in kw


async def test_create_topic_fifo(monkeypatch):
    mc = _mc({"TopicArn": "arn:topic.fifo"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    r = await create_topic_if_not_exists("my-topic", fifo=True)
    assert r == "arn:topic.fifo"
    kw = mc.call.call_args[1]
    assert kw["Name"] == "my-topic.fifo"
    assert kw["Attributes"]["FifoTopic"] == "true"


async def test_create_topic_fifo_suffix_exists(monkeypatch):
    mc = _mc({"TopicArn": "arn:t.fifo"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    await create_topic_if_not_exists("t.fifo", fifo=True)
    assert mc.call.call_args[1]["Name"] == "t.fifo"


async def test_create_topic_with_attributes(monkeypatch):
    mc = _mc({"TopicArn": "arn:t"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    await create_topic_if_not_exists("t", attributes={"KmsMasterKeyId": "k"})
    kw = mc.call.call_args[1]
    assert kw["Attributes"] == {"KmsMasterKeyId": "k"}


async def test_create_topic_fifo_with_attributes(monkeypatch):
    mc = _mc({"TopicArn": "arn:t.fifo"})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    await create_topic_if_not_exists("t", fifo=True, attributes={"X": "1"})
    kw = mc.call.call_args[1]
    assert kw["Attributes"]["FifoTopic"] == "true"
    assert kw["Attributes"]["X"] == "1"


async def test_create_topic_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to create SNS topic"):
        await create_topic_if_not_exists("t")


async def test_add_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_permission("test-topic_arn", "test-label", [], [], )
    mock_client.call.assert_called_once()


async def test_add_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_permission("test-topic_arn", "test-label", [], [], )


async def test_check_if_phone_number_is_opted_out(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await check_if_phone_number_is_opted_out("test-phone_number", )
    mock_client.call.assert_called_once()


async def test_check_if_phone_number_is_opted_out_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_if_phone_number_is_opted_out("test-phone_number", )


async def test_confirm_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await confirm_subscription("test-topic_arn", "test-token", )
    mock_client.call.assert_called_once()


async def test_confirm_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_subscription("test-topic_arn", "test-token", )


async def test_create_platform_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_platform_application("test-name", "test-platform", {}, )
    mock_client.call.assert_called_once()


async def test_create_platform_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_platform_application("test-name", "test-platform", {}, )


async def test_create_platform_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_platform_endpoint("test-platform_application_arn", "test-token", )
    mock_client.call.assert_called_once()


async def test_create_platform_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_platform_endpoint("test-platform_application_arn", "test-token", )


async def test_create_sms_sandbox_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_sms_sandbox_phone_number("test-phone_number", )
    mock_client.call.assert_called_once()


async def test_create_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_sms_sandbox_phone_number("test-phone_number", )


async def test_create_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_topic("test-name", )
    mock_client.call.assert_called_once()


async def test_create_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_topic("test-name", )


async def test_delete_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_endpoint("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_delete_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_endpoint("test-endpoint_arn", )


async def test_delete_platform_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_platform_application("test-platform_application_arn", )
    mock_client.call.assert_called_once()


async def test_delete_platform_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_platform_application("test-platform_application_arn", )


async def test_delete_sms_sandbox_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_sms_sandbox_phone_number("test-phone_number", )
    mock_client.call.assert_called_once()


async def test_delete_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_sms_sandbox_phone_number("test-phone_number", )


async def test_delete_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_topic("test-topic_arn", )
    mock_client.call.assert_called_once()


async def test_delete_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_topic("test-topic_arn", )


async def test_get_data_protection_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_protection_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_data_protection_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_protection_policy("test-resource_arn", )


async def test_get_endpoint_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_endpoint_attributes("test-endpoint_arn", )
    mock_client.call.assert_called_once()


async def test_get_endpoint_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_endpoint_attributes("test-endpoint_arn", )


async def test_get_platform_application_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_platform_application_attributes("test-platform_application_arn", )
    mock_client.call.assert_called_once()


async def test_get_platform_application_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_platform_application_attributes("test-platform_application_arn", )


async def test_get_sms_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sms_attributes()
    mock_client.call.assert_called_once()


async def test_get_sms_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sms_attributes()


async def test_get_sms_sandbox_account_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sms_sandbox_account_status()
    mock_client.call.assert_called_once()


async def test_get_sms_sandbox_account_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sms_sandbox_account_status()


async def test_get_subscription_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_subscription_attributes("test-subscription_arn", )
    mock_client.call.assert_called_once()


async def test_get_subscription_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_subscription_attributes("test-subscription_arn", )


async def test_get_topic_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_topic_attributes("test-topic_arn", )
    mock_client.call.assert_called_once()


async def test_get_topic_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_topic_attributes("test-topic_arn", )


async def test_list_endpoints_by_platform_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_endpoints_by_platform_application("test-platform_application_arn", )
    mock_client.call.assert_called_once()


async def test_list_endpoints_by_platform_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_endpoints_by_platform_application("test-platform_application_arn", )


async def test_list_origination_numbers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_origination_numbers()
    mock_client.call.assert_called_once()


async def test_list_origination_numbers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_origination_numbers()


async def test_list_phone_numbers_opted_out(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_phone_numbers_opted_out()
    mock_client.call.assert_called_once()


async def test_list_phone_numbers_opted_out_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_phone_numbers_opted_out()


async def test_list_platform_applications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_platform_applications()
    mock_client.call.assert_called_once()


async def test_list_platform_applications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_platform_applications()


async def test_list_sms_sandbox_phone_numbers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sms_sandbox_phone_numbers()
    mock_client.call.assert_called_once()


async def test_list_sms_sandbox_phone_numbers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sms_sandbox_phone_numbers()


async def test_list_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_subscriptions()
    mock_client.call.assert_called_once()


async def test_list_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_subscriptions()


async def test_list_subscriptions_by_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_subscriptions_by_topic("test-topic_arn", )
    mock_client.call.assert_called_once()


async def test_list_subscriptions_by_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_subscriptions_by_topic("test-topic_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_topics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_topics()
    mock_client.call.assert_called_once()


async def test_list_topics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_topics()


async def test_opt_in_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await opt_in_phone_number("test-phone_number", )
    mock_client.call.assert_called_once()


async def test_opt_in_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await opt_in_phone_number("test-phone_number", )


async def test_put_data_protection_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_data_protection_policy("test-resource_arn", "test-data_protection_policy", )
    mock_client.call.assert_called_once()


async def test_put_data_protection_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_data_protection_policy("test-resource_arn", "test-data_protection_policy", )


async def test_remove_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_permission("test-topic_arn", "test-label", )
    mock_client.call.assert_called_once()


async def test_remove_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_permission("test-topic_arn", "test-label", )


async def test_set_endpoint_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_endpoint_attributes("test-endpoint_arn", {}, )
    mock_client.call.assert_called_once()


async def test_set_endpoint_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_endpoint_attributes("test-endpoint_arn", {}, )


async def test_set_platform_application_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_platform_application_attributes("test-platform_application_arn", {}, )
    mock_client.call.assert_called_once()


async def test_set_platform_application_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_platform_application_attributes("test-platform_application_arn", {}, )


async def test_set_sms_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_sms_attributes({}, )
    mock_client.call.assert_called_once()


async def test_set_sms_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_sms_attributes({}, )


async def test_set_subscription_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_subscription_attributes("test-subscription_arn", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_set_subscription_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_subscription_attributes("test-subscription_arn", "test-attribute_name", )


async def test_set_topic_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_topic_attributes("test-topic_arn", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_set_topic_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_topic_attributes("test-topic_arn", "test-attribute_name", )


async def test_subscribe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await subscribe("test-topic_arn", "test-protocol", )
    mock_client.call.assert_called_once()


async def test_subscribe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await subscribe("test-topic_arn", "test-protocol", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_unsubscribe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await unsubscribe("test-subscription_arn", )
    mock_client.call.assert_called_once()


async def test_unsubscribe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unsubscribe("test-subscription_arn", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_verify_sms_sandbox_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify_sms_sandbox_phone_number("test-phone_number", "test-one_time_password", )
    mock_client.call.assert_called_once()


async def test_verify_sms_sandbox_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sns.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify_sms_sandbox_phone_number("test-phone_number", "test-one_time_password", )


@pytest.mark.asyncio
async def test_confirm_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import confirm_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await confirm_subscription("test-topic_arn", "test-token", authenticate_on_unsubscribe="test-authenticate_on_unsubscribe", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_platform_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import create_platform_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await create_platform_endpoint("test-platform_application_arn", "test-token", custom_user_data="test-custom_user_data", attributes="test-attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_sms_sandbox_phone_number_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import create_sms_sandbox_phone_number
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await create_sms_sandbox_phone_number("test-phone_number", language_code="test-language_code", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_topic_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import create_topic
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await create_topic("test-name", attributes="test-attributes", tags=[{"Key": "k", "Value": "v"}], data_protection_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_sms_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import get_sms_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await get_sms_attributes(attributes="test-attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_endpoints_by_platform_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_endpoints_by_platform_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_endpoints_by_platform_application("test-platform_application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_origination_numbers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_origination_numbers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_origination_numbers(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_phone_numbers_opted_out_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_phone_numbers_opted_out
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_phone_numbers_opted_out(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_platform_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_platform_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_platform_applications(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sms_sandbox_phone_numbers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_sms_sandbox_phone_numbers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_sms_sandbox_phone_numbers(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_subscriptions(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_subscriptions_by_topic_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_subscriptions_by_topic
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_subscriptions_by_topic("test-topic_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_topics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import list_topics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await list_topics(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_subscription_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import set_subscription_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await set_subscription_attributes("test-subscription_arn", "test-attribute_name", attribute_value="test-attribute_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_topic_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import set_topic_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await set_topic_attributes("test-topic_arn", "test-attribute_name", attribute_value="test-attribute_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_subscribe_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import subscribe
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    await subscribe("test-topic_arn", "test-protocol", endpoint="test-endpoint", attributes="test-attributes", return_subscription_arn="test-return_subscription_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_topic_if_not_exists_error(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sns import create_topic_if_not_exists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(side_effect=Exception("fail"))
    monkeypatch.setattr("aws_util.aio.sns.async_client", lambda *a, **kw: mock_client)
    import pytest as _pytest
    with _pytest.raises(RuntimeError, match="Failed to create SNS topic"):
        await create_topic_if_not_exists("test-topic", region_name="us-east-1")
