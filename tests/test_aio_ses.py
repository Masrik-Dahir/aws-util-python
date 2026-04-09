"""Tests for aws_util.aio.ses — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.ses import (
    SendEmailResult,
    list_verified_email_addresses,
    send_bulk,
    send_email,
    send_raw_email,
    send_templated_email,
    send_with_attachment,
    verify_email_address,
    clone_receipt_rule_set,
    create_configuration_set,
    create_configuration_set_event_destination,
    create_configuration_set_tracking_options,
    create_custom_verification_email_template,
    create_receipt_filter,
    create_receipt_rule,
    create_receipt_rule_set,
    create_template,
    delete_configuration_set,
    delete_configuration_set_event_destination,
    delete_configuration_set_tracking_options,
    delete_custom_verification_email_template,
    delete_identity,
    delete_identity_policy,
    delete_receipt_filter,
    delete_receipt_rule,
    delete_receipt_rule_set,
    delete_template,
    delete_verified_email_address,
    describe_active_receipt_rule_set,
    describe_configuration_set,
    describe_receipt_rule,
    describe_receipt_rule_set,
    get_account_sending_enabled,
    get_custom_verification_email_template,
    get_identity_dkim_attributes,
    get_identity_mail_from_domain_attributes,
    get_identity_notification_attributes,
    get_identity_policies,
    get_identity_verification_attributes,
    get_send_quota,
    get_send_statistics,
    get_template,
    list_configuration_sets,
    list_custom_verification_email_templates,
    list_identities,
    list_identity_policies,
    list_receipt_filters,
    list_receipt_rule_sets,
    list_templates,
    put_configuration_set_delivery_options,
    put_identity_policy,
    reorder_receipt_rule_set,
    run_render_template,
    send_bounce,
    send_bulk_templated_email,
    send_custom_verification_email,
    set_active_receipt_rule_set,
    set_identity_dkim_enabled,
    set_identity_feedback_forwarding_enabled,
    set_identity_headers_in_notifications_enabled,
    set_identity_mail_from_domain,
    set_identity_notification_topic,
    set_receipt_rule_position,
    update_account_sending_enabled,
    update_configuration_set_event_destination,
    update_configuration_set_reputation_metrics_enabled,
    update_configuration_set_sending_enabled,
    update_configuration_set_tracking_options,
    update_custom_verification_email_template,
    update_receipt_rule,
    update_template,
    verify_domain_dkim,
    verify_domain_identity,
    verify_email_identity,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# -- send_email --------------------------------------------------------------

async def test_send_email_text(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await send_email("f@x.com", ["t@x.com"], "sub", body_text="hi")
    assert isinstance(r, SendEmailResult)
    assert r.message_id == "m1"


async def test_send_email_html(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_email("f@x.com", ["t@x.com"], "sub", body_html="<p>hi</p>")


async def test_send_email_both(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_email("f@x.com", ["t@x.com"], "sub", body_text="hi", body_html="<p>hi</p>")


async def test_send_email_cc_bcc_reply(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_email(
        "f@x.com", ["t@x.com"], "sub", body_text="hi",
        cc_addresses=["cc@x.com"],
        bcc_addresses=["bcc@x.com"],
        reply_to_addresses=["reply@x.com"],
    )
    kw = mc.call.call_args[1]
    assert kw["Destination"]["CcAddresses"] == ["cc@x.com"]
    assert kw["Destination"]["BccAddresses"] == ["bcc@x.com"]
    assert kw["ReplyToAddresses"] == ["reply@x.com"]


async def test_send_email_no_body():
    with pytest.raises(ValueError, match="body_text or body_html"):
        await send_email("f@x.com", ["t@x.com"], "sub")


async def test_send_email_error(monkeypatch):
    mc = _mc(se=RuntimeError("x"))
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to send email"):
        await send_email("f@x.com", ["t@x.com"], "sub", body_text="hi")


# -- send_templated_email ----------------------------------------------------

async def test_send_templated_email(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await send_templated_email("f@x.com", ["t@x.com"], "tmpl", {"k": "v"})
    assert r.message_id == "m1"


async def test_send_templated_email_with_cc_bcc(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_templated_email(
        "f@x.com", ["t@x.com"], "tmpl", {},
        cc_addresses=["cc@x.com"],
        bcc_addresses=["bcc@x.com"],
    )


async def test_send_templated_email_error(monkeypatch):
    mc = _mc(se=RuntimeError("x"))
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to send templated email"):
        await send_templated_email("f@x.com", ["t@x.com"], "tmpl", {})


# -- send_raw_email ----------------------------------------------------------

async def test_send_raw_email(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await send_raw_email(b"raw")
    assert r.message_id == "m1"


async def test_send_raw_email_with_from_to(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_raw_email(b"raw", from_address="f@x.com", to_addresses=["t@x.com"])
    kw = mc.call.call_args[1]
    assert kw["Source"] == "f@x.com"
    assert kw["Destinations"] == ["t@x.com"]


async def test_send_raw_email_error(monkeypatch):
    mc = _mc(se=RuntimeError("x"))
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to send raw email"):
        await send_raw_email(b"raw")


# -- send_with_attachment ----------------------------------------------------

async def test_send_with_attachment_text(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await send_with_attachment(
        "f@x.com", ["t@x.com"], "sub", body_text="hi",
        attachments=[{"filename": "f.txt", "data": b"data"}],
    )
    assert r.message_id == "m1"


async def test_send_with_attachment_html(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_with_attachment("f@x.com", ["t@x.com"], "sub", body_html="<p>hi</p>")


async def test_send_with_attachment_mimetype(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_with_attachment(
        "f@x.com", ["t@x.com"], "sub", body_text="hi",
        attachments=[{"filename": "f.txt", "data": b"data", "mimetype": "text/plain"}],
    )


async def test_send_with_attachment_no_body():
    with pytest.raises(ValueError, match="body_text or body_html"):
        await send_with_attachment("f@x.com", ["t@x.com"], "sub")


async def test_send_with_attachment_no_attachments(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await send_with_attachment("f@x.com", ["t@x.com"], "sub", body_text="hi")


# -- send_bulk ---------------------------------------------------------------

async def test_send_bulk(monkeypatch):
    mc = _mc({"MessageId": "m1"})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    msgs = [
        {"to_addresses": ["t@x.com"], "subject": "s1", "body_text": "hi"},
        {"to_addresses": ["t@x.com"], "subject": "s2", "body_html": "<p>hi</p>",
         "cc_addresses": ["cc@x.com"], "bcc_addresses": ["bcc@x.com"],
         "reply_to_addresses": ["r@x.com"]},
    ]
    r = await send_bulk("f@x.com", msgs)
    assert len(r) == 2


# -- verify_email_address ----------------------------------------------------

async def test_verify_email_address(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    await verify_email_address("e@x.com")


async def test_verify_email_address_error(monkeypatch):
    mc = _mc(se=RuntimeError("x"))
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to verify"):
        await verify_email_address("e@x.com")


# -- list_verified_email_addresses -------------------------------------------

async def test_list_verified_email_addresses(monkeypatch):
    mc = _mc({"VerifiedEmailAddresses": ["e@x.com"]})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await list_verified_email_addresses()
    assert r == ["e@x.com"]


async def test_list_verified_email_addresses_empty(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    r = await list_verified_email_addresses()
    assert r == []


async def test_list_verified_email_addresses_error(monkeypatch):
    mc = _mc(se=RuntimeError("x"))
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_verified_email_addresses failed"):
        await list_verified_email_addresses()


async def test_clone_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await clone_receipt_rule_set("test-rule_set_name", "test-original_rule_set_name", )
    mock_client.call.assert_called_once()


async def test_clone_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await clone_receipt_rule_set("test-rule_set_name", "test-original_rule_set_name", )


async def test_create_configuration_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_configuration_set({}, )
    mock_client.call.assert_called_once()


async def test_create_configuration_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_set({}, )


async def test_create_configuration_set_event_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_configuration_set_event_destination("test-configuration_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_configuration_set_event_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_set_event_destination("test-configuration_set_name", {}, )


async def test_create_configuration_set_tracking_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_configuration_set_tracking_options("test-configuration_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_configuration_set_tracking_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_set_tracking_options("test-configuration_set_name", {}, )


async def test_create_custom_verification_email_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )
    mock_client.call.assert_called_once()


async def test_create_custom_verification_email_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )


async def test_create_receipt_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_receipt_filter({}, )
    mock_client.call.assert_called_once()


async def test_create_receipt_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_receipt_filter({}, )


async def test_create_receipt_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_receipt_rule("test-rule_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_receipt_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_receipt_rule("test-rule_set_name", {}, )


async def test_create_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_receipt_rule_set("test-rule_set_name", )
    mock_client.call.assert_called_once()


async def test_create_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_receipt_rule_set("test-rule_set_name", )


async def test_create_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_template({}, )
    mock_client.call.assert_called_once()


async def test_create_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_template({}, )


async def test_delete_configuration_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_configuration_set("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_set("test-configuration_set_name", )


async def test_delete_configuration_set_event_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_set_event_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", )


async def test_delete_configuration_set_tracking_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_configuration_set_tracking_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_set_tracking_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_set_tracking_options("test-configuration_set_name", )


async def test_delete_custom_verification_email_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_verification_email_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_verification_email_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_verification_email_template("test-template_name", )


async def test_delete_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_identity("test-identity", )
    mock_client.call.assert_called_once()


async def test_delete_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_identity("test-identity", )


async def test_delete_identity_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_identity_policy("test-identity", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_identity_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_identity_policy("test-identity", "test-policy_name", )


async def test_delete_receipt_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_receipt_filter("test-filter_name", )
    mock_client.call.assert_called_once()


async def test_delete_receipt_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_receipt_filter("test-filter_name", )


async def test_delete_receipt_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_receipt_rule("test-rule_set_name", "test-rule_name", )
    mock_client.call.assert_called_once()


async def test_delete_receipt_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_receipt_rule("test-rule_set_name", "test-rule_name", )


async def test_delete_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_receipt_rule_set("test-rule_set_name", )
    mock_client.call.assert_called_once()


async def test_delete_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_receipt_rule_set("test-rule_set_name", )


async def test_delete_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_delete_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_template("test-template_name", )


async def test_delete_verified_email_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_verified_email_address("test-email_address", )
    mock_client.call.assert_called_once()


async def test_delete_verified_email_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_verified_email_address("test-email_address", )


async def test_describe_active_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_active_receipt_rule_set()
    mock_client.call.assert_called_once()


async def test_describe_active_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_active_receipt_rule_set()


async def test_describe_configuration_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_configuration_set("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_describe_configuration_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_set("test-configuration_set_name", )


async def test_describe_receipt_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_receipt_rule("test-rule_set_name", "test-rule_name", )
    mock_client.call.assert_called_once()


async def test_describe_receipt_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_receipt_rule("test-rule_set_name", "test-rule_name", )


async def test_describe_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_receipt_rule_set("test-rule_set_name", )
    mock_client.call.assert_called_once()


async def test_describe_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_receipt_rule_set("test-rule_set_name", )


async def test_get_account_sending_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_sending_enabled()
    mock_client.call.assert_called_once()


async def test_get_account_sending_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_sending_enabled()


async def test_get_custom_verification_email_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_custom_verification_email_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_get_custom_verification_email_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_verification_email_template("test-template_name", )


async def test_get_identity_dkim_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_dkim_attributes([], )
    mock_client.call.assert_called_once()


async def test_get_identity_dkim_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_dkim_attributes([], )


async def test_get_identity_mail_from_domain_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_mail_from_domain_attributes([], )
    mock_client.call.assert_called_once()


async def test_get_identity_mail_from_domain_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_mail_from_domain_attributes([], )


async def test_get_identity_notification_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_notification_attributes([], )
    mock_client.call.assert_called_once()


async def test_get_identity_notification_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_notification_attributes([], )


async def test_get_identity_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_policies("test-identity", [], )
    mock_client.call.assert_called_once()


async def test_get_identity_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_policies("test-identity", [], )


async def test_get_identity_verification_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_verification_attributes([], )
    mock_client.call.assert_called_once()


async def test_get_identity_verification_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_verification_attributes([], )


async def test_get_send_quota(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_send_quota()
    mock_client.call.assert_called_once()


async def test_get_send_quota_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_send_quota()


async def test_get_send_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_send_statistics()
    mock_client.call.assert_called_once()


async def test_get_send_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_send_statistics()


async def test_get_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_get_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_template("test-template_name", )


async def test_list_configuration_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_configuration_sets()
    mock_client.call.assert_called_once()


async def test_list_configuration_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_configuration_sets()


async def test_list_custom_verification_email_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_verification_email_templates()
    mock_client.call.assert_called_once()


async def test_list_custom_verification_email_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_verification_email_templates()


async def test_list_identities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_identities()
    mock_client.call.assert_called_once()


async def test_list_identities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_identities()


async def test_list_identity_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_identity_policies("test-identity", )
    mock_client.call.assert_called_once()


async def test_list_identity_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_identity_policies("test-identity", )


async def test_list_receipt_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_receipt_filters()
    mock_client.call.assert_called_once()


async def test_list_receipt_filters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_receipt_filters()


async def test_list_receipt_rule_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_receipt_rule_sets()
    mock_client.call.assert_called_once()


async def test_list_receipt_rule_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_receipt_rule_sets()


async def test_list_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_templates()
    mock_client.call.assert_called_once()


async def test_list_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_templates()


async def test_put_configuration_set_delivery_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_configuration_set_delivery_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_delivery_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_delivery_options("test-configuration_set_name", )


async def test_put_identity_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_identity_policy("test-identity", "test-policy_name", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_identity_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_identity_policy("test-identity", "test-policy_name", "test-policy", )


async def test_reorder_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await reorder_receipt_rule_set("test-rule_set_name", [], )
    mock_client.call.assert_called_once()


async def test_reorder_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reorder_receipt_rule_set("test-rule_set_name", [], )


async def test_run_render_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_render_template("test-template_name", "test-template_data", )
    mock_client.call.assert_called_once()


async def test_run_render_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_render_template("test-template_name", "test-template_data", )


async def test_send_bounce(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_bounce("test-original_message_id", "test-bounce_sender", [], )
    mock_client.call.assert_called_once()


async def test_send_bounce_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_bounce("test-original_message_id", "test-bounce_sender", [], )


async def test_send_bulk_templated_email(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_bulk_templated_email("test-source", "test-template", "test-default_template_data", [], )
    mock_client.call.assert_called_once()


async def test_send_bulk_templated_email_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_bulk_templated_email("test-source", "test-template", "test-default_template_data", [], )


async def test_send_custom_verification_email(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_custom_verification_email("test-email_address", "test-template_name", )
    mock_client.call.assert_called_once()


async def test_send_custom_verification_email_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_custom_verification_email("test-email_address", "test-template_name", )


async def test_set_active_receipt_rule_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_active_receipt_rule_set()
    mock_client.call.assert_called_once()


async def test_set_active_receipt_rule_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_active_receipt_rule_set()


async def test_set_identity_dkim_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_dkim_enabled("test-identity", True, )
    mock_client.call.assert_called_once()


async def test_set_identity_dkim_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_dkim_enabled("test-identity", True, )


async def test_set_identity_feedback_forwarding_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_feedback_forwarding_enabled("test-identity", True, )
    mock_client.call.assert_called_once()


async def test_set_identity_feedback_forwarding_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_feedback_forwarding_enabled("test-identity", True, )


async def test_set_identity_headers_in_notifications_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_headers_in_notifications_enabled("test-identity", "test-notification_type", True, )
    mock_client.call.assert_called_once()


async def test_set_identity_headers_in_notifications_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_headers_in_notifications_enabled("test-identity", "test-notification_type", True, )


async def test_set_identity_mail_from_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_mail_from_domain("test-identity", )
    mock_client.call.assert_called_once()


async def test_set_identity_mail_from_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_mail_from_domain("test-identity", )


async def test_set_identity_notification_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_notification_topic("test-identity", "test-notification_type", )
    mock_client.call.assert_called_once()


async def test_set_identity_notification_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_notification_topic("test-identity", "test-notification_type", )


async def test_set_receipt_rule_position(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_receipt_rule_position("test-rule_set_name", "test-rule_name", )
    mock_client.call.assert_called_once()


async def test_set_receipt_rule_position_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_receipt_rule_position("test-rule_set_name", "test-rule_name", )


async def test_update_account_sending_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_sending_enabled()
    mock_client.call.assert_called_once()


async def test_update_account_sending_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_sending_enabled()


async def test_update_configuration_set_event_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration_set_event_destination("test-configuration_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_configuration_set_event_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_set_event_destination("test-configuration_set_name", {}, )


async def test_update_configuration_set_reputation_metrics_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration_set_reputation_metrics_enabled("test-configuration_set_name", True, )
    mock_client.call.assert_called_once()


async def test_update_configuration_set_reputation_metrics_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_set_reputation_metrics_enabled("test-configuration_set_name", True, )


async def test_update_configuration_set_sending_enabled(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration_set_sending_enabled("test-configuration_set_name", True, )
    mock_client.call.assert_called_once()


async def test_update_configuration_set_sending_enabled_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_set_sending_enabled("test-configuration_set_name", True, )


async def test_update_configuration_set_tracking_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration_set_tracking_options("test-configuration_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_configuration_set_tracking_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_set_tracking_options("test-configuration_set_name", {}, )


async def test_update_custom_verification_email_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_custom_verification_email_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_update_custom_verification_email_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_verification_email_template("test-template_name", )


async def test_update_receipt_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_receipt_rule("test-rule_set_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_receipt_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_receipt_rule("test-rule_set_name", {}, )


async def test_update_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_template({}, )
    mock_client.call.assert_called_once()


async def test_update_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_template({}, )


async def test_verify_domain_dkim(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify_domain_dkim("test-domain", )
    mock_client.call.assert_called_once()


async def test_verify_domain_dkim_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify_domain_dkim("test-domain", )


async def test_verify_domain_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify_domain_identity("test-domain", )
    mock_client.call.assert_called_once()


async def test_verify_domain_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify_domain_identity("test-domain", )


async def test_verify_email_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    await verify_email_identity("test-email_address", )
    mock_client.call.assert_called_once()


async def test_verify_email_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ses.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await verify_email_identity("test-email_address", )


@pytest.mark.asyncio
async def test_create_receipt_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import create_receipt_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await create_receipt_rule("test-rule_set_name", "test-rule", after="test-after", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_configuration_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import describe_configuration_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await describe_configuration_set({}, configuration_set_attribute_names={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import list_configuration_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await list_configuration_sets(next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_verification_email_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import list_custom_verification_email_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await list_custom_verification_email_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_identities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import list_identities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await list_identities(identity_type="test-identity_type", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_receipt_rule_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import list_receipt_rule_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await list_receipt_rule_sets(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import list_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await list_templates(next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_delivery_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import put_configuration_set_delivery_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_delivery_options({}, delivery_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_bounce_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import send_bounce
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await send_bounce("test-original_message_id", "test-bounce_sender", "test-bounced_recipient_info_list", explanation="test-explanation", message_dsn="test-message_dsn", bounce_sender_arn="test-bounce_sender_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_bulk_templated_email_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import send_bulk_templated_email
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await send_bulk_templated_email("test-source", "test-template", "test-default_template_data", "test-destinations", source_arn="test-source_arn", reply_to_addresses="test-reply_to_addresses", return_path="test-return_path", return_path_arn="test-return_path_arn", configuration_set_name={}, default_tags=[{"Key": "k", "Value": "v"}], template_arn="test-template_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_custom_verification_email_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import send_custom_verification_email
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await send_custom_verification_email("test-email_address", "test-template_name", configuration_set_name={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_active_receipt_rule_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import set_active_receipt_rule_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await set_active_receipt_rule_set(rule_set_name="test-rule_set_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_identity_mail_from_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import set_identity_mail_from_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await set_identity_mail_from_domain("test-identity", mail_from_domain="test-mail_from_domain", behavior_on_mx_failure="test-behavior_on_mx_failure", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_identity_notification_topic_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import set_identity_notification_topic
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await set_identity_notification_topic("test-identity", "test-notification_type", sns_topic="test-sns_topic", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_receipt_rule_position_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import set_receipt_rule_position
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await set_receipt_rule_position("test-rule_set_name", "test-rule_name", after="test-after", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_sending_enabled_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import update_account_sending_enabled
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await update_account_sending_enabled(enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_custom_verification_email_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses import update_custom_verification_email_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses.async_client", lambda *a, **kw: mock_client)
    await update_custom_verification_email_template("test-template_name", from_email_address="test-from_email_address", template_subject="test-template_subject", template_content="test-template_content", success_redirection_url="test-success_redirection_url", failure_redirection_url="test-failure_redirection_url", region_name="us-east-1")
    mock_client.call.assert_called_once()
