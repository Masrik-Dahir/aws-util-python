"""Tests for aws_util.ses module."""
from __future__ import annotations

from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.ses import (
    EmailAddress,
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

REGION = "us-east-1"
FROM = "sender@example.com"
TO = ["recipient@example.com"]


# ---------------------------------------------------------------------------
# send_email
# ---------------------------------------------------------------------------


def test_send_email_text_body(ses_client):
    result = send_email(FROM, TO, "Subject", body_text="Hello", region_name=REGION)
    assert isinstance(result, SendEmailResult)
    assert result.message_id


def test_send_email_html_body(ses_client):
    result = send_email(
        FROM, TO, "Subject", body_html="<b>Hello</b>", region_name=REGION
    )
    assert result.message_id


def test_send_email_both_bodies(ses_client):
    result = send_email(
        FROM,
        TO,
        "Subject",
        body_text="Plain",
        body_html="<b>HTML</b>",
        region_name=REGION,
    )
    assert result.message_id


def test_send_email_no_body_raises(ses_client):
    with pytest.raises(ValueError, match="At least one of body_text or body_html"):
        send_email(FROM, TO, "Subject", region_name=REGION)


def test_send_email_with_cc_bcc(ses_client):
    ses_client.verify_email_address(EmailAddress="cc@example.com")
    ses_client.verify_email_address(EmailAddress="bcc@example.com")
    result = send_email(
        FROM,
        TO,
        "Subject",
        body_text="Hello",
        cc_addresses=["cc@example.com"],
        bcc_addresses=["bcc@example.com"],
        region_name=REGION,
    )
    assert result.message_id


def test_send_email_with_reply_to(ses_client):
    result = send_email(
        FROM,
        TO,
        "Subject",
        body_text="Hello",
        reply_to_addresses=["replyto@example.com"],
        region_name=REGION,
    )
    assert result.message_id


def test_send_email_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ses as sesmod

    mock_client = MagicMock()
    mock_client.send_email.side_effect = ClientError(
        {"Error": {"Code": "MessageRejected", "Message": "rejected"}},
        "SendEmail",
    )
    monkeypatch.setattr(sesmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send email"):
        send_email(FROM, TO, "Subject", body_text="Hello", region_name=REGION)


# ---------------------------------------------------------------------------
# send_templated_email
# ---------------------------------------------------------------------------


def test_send_templated_email(ses_client):
    # moto may not support templated emails fully, but attempt it
    ses_client.create_template(
        Template={
            "TemplateName": "test-template",
            "SubjectPart": "Hello {{name}}",
            "TextPart": "Hi {{name}}",
        }
    )
    try:
        result = send_templated_email(
            FROM,
            TO,
            "test-template",
            {"name": "Alice"},
            region_name=REGION,
        )
        assert result.message_id
    except Exception:
        pytest.skip("moto doesn't support templated emails in this version")


def test_send_templated_email_with_cc_bcc(ses_client):
    ses_client.create_template(
        Template={
            "TemplateName": "cc-template",
            "SubjectPart": "Hello",
            "TextPart": "Hi",
        }
    )
    try:
        ses_client.verify_email_address(EmailAddress="cc2@example.com")
        result = send_templated_email(
            FROM,
            TO,
            "cc-template",
            {},
            cc_addresses=["cc2@example.com"],
            region_name=REGION,
        )
        assert result.message_id
    except Exception:
        pytest.skip("moto doesn't support templated emails in this version")


def test_send_templated_email_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ses as sesmod

    mock_client = MagicMock()
    mock_client.send_templated_email.side_effect = ClientError(
        {"Error": {"Code": "TemplateDoesNotExist", "Message": "not found"}},
        "SendTemplatedEmail",
    )
    monkeypatch.setattr(sesmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send templated email"):
        send_templated_email(FROM, TO, "no-template", {}, region_name=REGION)


# ---------------------------------------------------------------------------
# send_raw_email
# ---------------------------------------------------------------------------


def test_send_raw_email(ses_client):
    import email.mime.text as _mime_text
    import email.mime.multipart as _mime_multi

    msg = _mime_multi.MIMEMultipart()
    msg["Subject"] = "Test"
    msg["From"] = FROM
    msg["To"] = TO[0]
    msg.attach(_mime_text.MIMEText("hello", "plain"))

    result = send_raw_email(
        msg.as_bytes(),
        from_address=FROM,
        to_addresses=TO,
        region_name=REGION,
    )
    assert result.message_id


def test_send_raw_email_minimal(ses_client):
    import email.mime.text as _mime_text

    msg = _mime_text.MIMEText("raw body")
    msg["From"] = FROM
    msg["To"] = TO[0]
    result = send_raw_email(msg.as_bytes(), region_name=REGION)
    assert result.message_id


def test_send_raw_email_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ses as sesmod

    mock_client = MagicMock()
    mock_client.send_raw_email.side_effect = ClientError(
        {"Error": {"Code": "MessageRejected", "Message": "rejected"}},
        "SendRawEmail",
    )
    monkeypatch.setattr(sesmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send raw email"):
        send_raw_email(b"raw", region_name=REGION)


# ---------------------------------------------------------------------------
# send_with_attachment
# ---------------------------------------------------------------------------


def test_send_with_attachment(ses_client):
    attachment = {
        "filename": "test.txt",
        "data": b"attachment content",
        "mimetype": "text/plain",
    }
    result = send_with_attachment(
        FROM,
        TO,
        "Subject",
        body_text="Body",
        attachments=[attachment],
        region_name=REGION,
    )
    assert result.message_id


def test_send_with_attachment_no_mimetype(ses_client):
    attachment = {"filename": "data.bin", "data": b"binary data"}
    result = send_with_attachment(
        FROM,
        TO,
        "Subject",
        body_html="<b>Body</b>",
        attachments=[attachment],
        region_name=REGION,
    )
    assert result.message_id


def test_send_with_attachment_no_body_raises(ses_client):
    with pytest.raises(ValueError, match="At least one of body_text or body_html"):
        send_with_attachment(FROM, TO, "Subject", region_name=REGION)


def test_send_with_attachment_both_bodies(ses_client):
    result = send_with_attachment(
        FROM,
        TO,
        "Subject",
        body_text="Plain",
        body_html="<b>HTML</b>",
        region_name=REGION,
    )
    assert result.message_id


# ---------------------------------------------------------------------------
# send_bulk
# ---------------------------------------------------------------------------


def test_send_bulk(ses_client):
    messages = [
        {"to_addresses": TO, "subject": "Sub 1", "body_text": "Body 1"},
        {"to_addresses": TO, "subject": "Sub 2", "body_text": "Body 2"},
    ]
    results = send_bulk(FROM, messages, region_name=REGION)
    assert len(results) == 2
    assert all(isinstance(r, SendEmailResult) for r in results)


def test_send_bulk_with_cc_bcc(ses_client):
    ses_client.verify_email_address(EmailAddress="bulk-cc@example.com")
    messages = [
        {
            "to_addresses": TO,
            "subject": "Sub",
            "body_text": "Body",
            "cc_addresses": ["bulk-cc@example.com"],
            "reply_to_addresses": ["reply@example.com"],
        }
    ]
    results = send_bulk(FROM, messages, region_name=REGION)
    assert len(results) == 1


# ---------------------------------------------------------------------------
# verify_email_address
# ---------------------------------------------------------------------------


def test_verify_email_address(ses_client):
    verify_email_address("new@example.com", region_name=REGION)


def test_verify_email_address_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ses as sesmod

    mock_client = MagicMock()
    mock_client.verify_email_address.side_effect = ClientError(
        {"Error": {"Code": "MessageRejected", "Message": "rejected"}},
        "VerifyEmailAddress",
    )
    monkeypatch.setattr(sesmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify email address"):
        verify_email_address("bad@example.com", region_name=REGION)


# ---------------------------------------------------------------------------
# list_verified_email_addresses
# ---------------------------------------------------------------------------


def test_list_verified_email_addresses(ses_client):
    result = list_verified_email_addresses(region_name=REGION)
    assert "sender@example.com" in result
    assert "recipient@example.com" in result


def test_list_verified_email_addresses_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ses as sesmod

    mock_client = MagicMock()
    mock_client.list_verified_email_addresses.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "ListVerifiedEmailAddresses",
    )
    monkeypatch.setattr(sesmod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_verified_email_addresses failed"):
        list_verified_email_addresses(region_name=REGION)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_send_email_result_model():
    result = SendEmailResult(message_id="msg-123")
    assert result.message_id == "msg-123"


def test_email_address_model():
    addr = EmailAddress(address="test@example.com", verified=True)
    assert addr.address == "test@example.com"
    assert addr.verified is True


def test_send_templated_email_with_bcc(monkeypatch):
    """Covers bcc_addresses branch in send_templated_email (line 139)."""
    from unittest.mock import MagicMock

    mock_client = MagicMock()
    mock_client.send_templated_email.return_value = {"MessageId": "msg-bcc"}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    from aws_util.ses import send_templated_email
    result = send_templated_email(
        from_address="sender@example.com",
        to_addresses=["to@example.com"],
        template_name="my-template",
        template_data={"name": "world"},
        bcc_addresses=["bcc@example.com"],
        region_name="us-east-1",
    )
    assert result.message_id == "msg-bcc"
    call_kwargs = mock_client.send_templated_email.call_args[1]
    assert "BccAddresses" in call_kwargs["Destination"]


def test_clone_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.clone_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    clone_receipt_rule_set("test-rule_set_name", "test-original_rule_set_name", region_name=REGION)
    mock_client.clone_receipt_rule_set.assert_called_once()


def test_clone_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.clone_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "clone_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to clone receipt rule set"):
        clone_receipt_rule_set("test-rule_set_name", "test-original_rule_set_name", region_name=REGION)


def test_create_configuration_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_configuration_set({}, region_name=REGION)
    mock_client.create_configuration_set.assert_called_once()


def test_create_configuration_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create configuration set"):
        create_configuration_set({}, region_name=REGION)


def test_create_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_configuration_set_event_destination("test-configuration_set_name", {}, region_name=REGION)
    mock_client.create_configuration_set_event_destination.assert_called_once()


def test_create_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create configuration set event destination"):
        create_configuration_set_event_destination("test-configuration_set_name", {}, region_name=REGION)


def test_create_configuration_set_tracking_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_tracking_options.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_configuration_set_tracking_options("test-configuration_set_name", {}, region_name=REGION)
    mock_client.create_configuration_set_tracking_options.assert_called_once()


def test_create_configuration_set_tracking_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_tracking_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_set_tracking_options",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create configuration set tracking options"):
        create_configuration_set_tracking_options("test-configuration_set_name", {}, region_name=REGION)


def test_create_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)
    mock_client.create_custom_verification_email_template.assert_called_once()


def test_create_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom verification email template"):
        create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)


def test_create_receipt_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_filter.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_receipt_filter({}, region_name=REGION)
    mock_client.create_receipt_filter.assert_called_once()


def test_create_receipt_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_receipt_filter",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create receipt filter"):
        create_receipt_filter({}, region_name=REGION)


def test_create_receipt_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_rule.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_receipt_rule("test-rule_set_name", {}, region_name=REGION)
    mock_client.create_receipt_rule.assert_called_once()


def test_create_receipt_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_receipt_rule",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create receipt rule"):
        create_receipt_rule("test-rule_set_name", {}, region_name=REGION)


def test_create_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_receipt_rule_set("test-rule_set_name", region_name=REGION)
    mock_client.create_receipt_rule_set.assert_called_once()


def test_create_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create receipt rule set"):
        create_receipt_rule_set("test-rule_set_name", region_name=REGION)


def test_create_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_template({}, region_name=REGION)
    mock_client.create_template.assert_called_once()


def test_create_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create template"):
        create_template({}, region_name=REGION)


def test_delete_configuration_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_configuration_set("test-configuration_set_name", region_name=REGION)
    mock_client.delete_configuration_set.assert_called_once()


def test_delete_configuration_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration set"):
        delete_configuration_set("test-configuration_set_name", region_name=REGION)


def test_delete_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", region_name=REGION)
    mock_client.delete_configuration_set_event_destination.assert_called_once()


def test_delete_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration set event destination"):
        delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", region_name=REGION)


def test_delete_configuration_set_tracking_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_tracking_options.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_configuration_set_tracking_options("test-configuration_set_name", region_name=REGION)
    mock_client.delete_configuration_set_tracking_options.assert_called_once()


def test_delete_configuration_set_tracking_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_tracking_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_set_tracking_options",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration set tracking options"):
        delete_configuration_set_tracking_options("test-configuration_set_name", region_name=REGION)


def test_delete_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_custom_verification_email_template("test-template_name", region_name=REGION)
    mock_client.delete_custom_verification_email_template.assert_called_once()


def test_delete_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom verification email template"):
        delete_custom_verification_email_template("test-template_name", region_name=REGION)


def test_delete_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_identity("test-identity", region_name=REGION)
    mock_client.delete_identity.assert_called_once()


def test_delete_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_identity",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete identity"):
        delete_identity("test-identity", region_name=REGION)


def test_delete_identity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_identity_policy("test-identity", "test-policy_name", region_name=REGION)
    mock_client.delete_identity_policy.assert_called_once()


def test_delete_identity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_identity_policy",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete identity policy"):
        delete_identity_policy("test-identity", "test-policy_name", region_name=REGION)


def test_delete_receipt_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_filter.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_receipt_filter("test-filter_name", region_name=REGION)
    mock_client.delete_receipt_filter.assert_called_once()


def test_delete_receipt_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_receipt_filter",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete receipt filter"):
        delete_receipt_filter("test-filter_name", region_name=REGION)


def test_delete_receipt_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_rule.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_receipt_rule("test-rule_set_name", "test-rule_name", region_name=REGION)
    mock_client.delete_receipt_rule.assert_called_once()


def test_delete_receipt_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_receipt_rule",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete receipt rule"):
        delete_receipt_rule("test-rule_set_name", "test-rule_name", region_name=REGION)


def test_delete_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_receipt_rule_set("test-rule_set_name", region_name=REGION)
    mock_client.delete_receipt_rule_set.assert_called_once()


def test_delete_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete receipt rule set"):
        delete_receipt_rule_set("test-rule_set_name", region_name=REGION)


def test_delete_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_template("test-template_name", region_name=REGION)
    mock_client.delete_template.assert_called_once()


def test_delete_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete template"):
        delete_template("test-template_name", region_name=REGION)


def test_delete_verified_email_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_email_address.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    delete_verified_email_address("test-email_address", region_name=REGION)
    mock_client.delete_verified_email_address.assert_called_once()


def test_delete_verified_email_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_email_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_verified_email_address",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete verified email address"):
        delete_verified_email_address("test-email_address", region_name=REGION)


def test_describe_active_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_active_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    describe_active_receipt_rule_set(region_name=REGION)
    mock_client.describe_active_receipt_rule_set.assert_called_once()


def test_describe_active_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_active_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_active_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe active receipt rule set"):
        describe_active_receipt_rule_set(region_name=REGION)


def test_describe_configuration_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    describe_configuration_set("test-configuration_set_name", region_name=REGION)
    mock_client.describe_configuration_set.assert_called_once()


def test_describe_configuration_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe configuration set"):
        describe_configuration_set("test-configuration_set_name", region_name=REGION)


def test_describe_receipt_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_receipt_rule.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    describe_receipt_rule("test-rule_set_name", "test-rule_name", region_name=REGION)
    mock_client.describe_receipt_rule.assert_called_once()


def test_describe_receipt_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_receipt_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_receipt_rule",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe receipt rule"):
        describe_receipt_rule("test-rule_set_name", "test-rule_name", region_name=REGION)


def test_describe_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    describe_receipt_rule_set("test-rule_set_name", region_name=REGION)
    mock_client.describe_receipt_rule_set.assert_called_once()


def test_describe_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe receipt rule set"):
        describe_receipt_rule_set("test-rule_set_name", region_name=REGION)


def test_get_account_sending_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_sending_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_account_sending_enabled(region_name=REGION)
    mock_client.get_account_sending_enabled.assert_called_once()


def test_get_account_sending_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_sending_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_sending_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account sending enabled"):
        get_account_sending_enabled(region_name=REGION)


def test_get_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_custom_verification_email_template("test-template_name", region_name=REGION)
    mock_client.get_custom_verification_email_template.assert_called_once()


def test_get_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get custom verification email template"):
        get_custom_verification_email_template("test-template_name", region_name=REGION)


def test_get_identity_dkim_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_dkim_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_identity_dkim_attributes([], region_name=REGION)
    mock_client.get_identity_dkim_attributes.assert_called_once()


def test_get_identity_dkim_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_dkim_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_dkim_attributes",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity dkim attributes"):
        get_identity_dkim_attributes([], region_name=REGION)


def test_get_identity_mail_from_domain_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_mail_from_domain_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_identity_mail_from_domain_attributes([], region_name=REGION)
    mock_client.get_identity_mail_from_domain_attributes.assert_called_once()


def test_get_identity_mail_from_domain_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_mail_from_domain_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_mail_from_domain_attributes",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity mail from domain attributes"):
        get_identity_mail_from_domain_attributes([], region_name=REGION)


def test_get_identity_notification_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_notification_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_identity_notification_attributes([], region_name=REGION)
    mock_client.get_identity_notification_attributes.assert_called_once()


def test_get_identity_notification_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_notification_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_notification_attributes",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity notification attributes"):
        get_identity_notification_attributes([], region_name=REGION)


def test_get_identity_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_policies.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_identity_policies("test-identity", [], region_name=REGION)
    mock_client.get_identity_policies.assert_called_once()


def test_get_identity_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_policies",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity policies"):
        get_identity_policies("test-identity", [], region_name=REGION)


def test_get_identity_verification_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_verification_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_identity_verification_attributes([], region_name=REGION)
    mock_client.get_identity_verification_attributes.assert_called_once()


def test_get_identity_verification_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_verification_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_verification_attributes",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity verification attributes"):
        get_identity_verification_attributes([], region_name=REGION)


def test_get_send_quota(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_send_quota.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_send_quota(region_name=REGION)
    mock_client.get_send_quota.assert_called_once()


def test_get_send_quota_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_send_quota.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_send_quota",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get send quota"):
        get_send_quota(region_name=REGION)


def test_get_send_statistics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_send_statistics.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_send_statistics(region_name=REGION)
    mock_client.get_send_statistics.assert_called_once()


def test_get_send_statistics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_send_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_send_statistics",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get send statistics"):
        get_send_statistics(region_name=REGION)


def test_get_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    get_template("test-template_name", region_name=REGION)
    mock_client.get_template.assert_called_once()


def test_get_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get template"):
        get_template("test-template_name", region_name=REGION)


def test_list_configuration_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_sets.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_configuration_sets(region_name=REGION)
    mock_client.list_configuration_sets.assert_called_once()


def test_list_configuration_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_configuration_sets",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list configuration sets"):
        list_configuration_sets(region_name=REGION)


def test_list_custom_verification_email_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_custom_verification_email_templates(region_name=REGION)
    mock_client.list_custom_verification_email_templates.assert_called_once()


def test_list_custom_verification_email_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_verification_email_templates",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list custom verification email templates"):
        list_custom_verification_email_templates(region_name=REGION)


def test_list_identities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identities.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_identities(region_name=REGION)
    mock_client.list_identities.assert_called_once()


def test_list_identities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_identities",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list identities"):
        list_identities(region_name=REGION)


def test_list_identity_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_policies.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_identity_policies("test-identity", region_name=REGION)
    mock_client.list_identity_policies.assert_called_once()


def test_list_identity_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_identity_policies",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list identity policies"):
        list_identity_policies("test-identity", region_name=REGION)


def test_list_receipt_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_receipt_filters.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_receipt_filters(region_name=REGION)
    mock_client.list_receipt_filters.assert_called_once()


def test_list_receipt_filters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_receipt_filters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_receipt_filters",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list receipt filters"):
        list_receipt_filters(region_name=REGION)


def test_list_receipt_rule_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_receipt_rule_sets.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_receipt_rule_sets(region_name=REGION)
    mock_client.list_receipt_rule_sets.assert_called_once()


def test_list_receipt_rule_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_receipt_rule_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_receipt_rule_sets",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list receipt rule sets"):
        list_receipt_rule_sets(region_name=REGION)


def test_list_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_templates(region_name=REGION)
    mock_client.list_templates.assert_called_once()


def test_list_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_templates",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list templates"):
        list_templates(region_name=REGION)


def test_put_configuration_set_delivery_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_delivery_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_delivery_options.assert_called_once()


def test_put_configuration_set_delivery_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_delivery_options",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set delivery options"):
        put_configuration_set_delivery_options("test-configuration_set_name", region_name=REGION)


def test_put_identity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_identity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    put_identity_policy("test-identity", "test-policy_name", "test-policy", region_name=REGION)
    mock_client.put_identity_policy.assert_called_once()


def test_put_identity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_identity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_identity_policy",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put identity policy"):
        put_identity_policy("test-identity", "test-policy_name", "test-policy", region_name=REGION)


def test_reorder_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.reorder_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    reorder_receipt_rule_set("test-rule_set_name", [], region_name=REGION)
    mock_client.reorder_receipt_rule_set.assert_called_once()


def test_reorder_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reorder_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reorder_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reorder receipt rule set"):
        reorder_receipt_rule_set("test-rule_set_name", [], region_name=REGION)


def test_run_render_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_render_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    run_render_template("test-template_name", "test-template_data", region_name=REGION)
    mock_client.test_render_template.assert_called_once()


def test_run_render_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_render_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_render_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run render template"):
        run_render_template("test-template_name", "test-template_data", region_name=REGION)


def test_send_bounce(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_bounce.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_bounce("test-original_message_id", "test-bounce_sender", [], region_name=REGION)
    mock_client.send_bounce.assert_called_once()


def test_send_bounce_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_bounce.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_bounce",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send bounce"):
        send_bounce("test-original_message_id", "test-bounce_sender", [], region_name=REGION)


def test_send_bulk_templated_email(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_bulk_templated_email.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_bulk_templated_email("test-source", "test-template", "test-default_template_data", [], region_name=REGION)
    mock_client.send_bulk_templated_email.assert_called_once()


def test_send_bulk_templated_email_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_bulk_templated_email.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_bulk_templated_email",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send bulk templated email"):
        send_bulk_templated_email("test-source", "test-template", "test-default_template_data", [], region_name=REGION)


def test_send_custom_verification_email(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_custom_verification_email("test-email_address", "test-template_name", region_name=REGION)
    mock_client.send_custom_verification_email.assert_called_once()


def test_send_custom_verification_email_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_custom_verification_email",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send custom verification email"):
        send_custom_verification_email("test-email_address", "test-template_name", region_name=REGION)


def test_set_active_receipt_rule_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_active_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_active_receipt_rule_set(region_name=REGION)
    mock_client.set_active_receipt_rule_set.assert_called_once()


def test_set_active_receipt_rule_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_active_receipt_rule_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_active_receipt_rule_set",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set active receipt rule set"):
        set_active_receipt_rule_set(region_name=REGION)


def test_set_identity_dkim_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_dkim_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_dkim_enabled("test-identity", True, region_name=REGION)
    mock_client.set_identity_dkim_enabled.assert_called_once()


def test_set_identity_dkim_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_dkim_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_dkim_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set identity dkim enabled"):
        set_identity_dkim_enabled("test-identity", True, region_name=REGION)


def test_set_identity_feedback_forwarding_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_feedback_forwarding_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_feedback_forwarding_enabled("test-identity", True, region_name=REGION)
    mock_client.set_identity_feedback_forwarding_enabled.assert_called_once()


def test_set_identity_feedback_forwarding_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_feedback_forwarding_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_feedback_forwarding_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set identity feedback forwarding enabled"):
        set_identity_feedback_forwarding_enabled("test-identity", True, region_name=REGION)


def test_set_identity_headers_in_notifications_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_headers_in_notifications_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_headers_in_notifications_enabled("test-identity", "test-notification_type", True, region_name=REGION)
    mock_client.set_identity_headers_in_notifications_enabled.assert_called_once()


def test_set_identity_headers_in_notifications_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_headers_in_notifications_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_headers_in_notifications_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set identity headers in notifications enabled"):
        set_identity_headers_in_notifications_enabled("test-identity", "test-notification_type", True, region_name=REGION)


def test_set_identity_mail_from_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_mail_from_domain.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_mail_from_domain("test-identity", region_name=REGION)
    mock_client.set_identity_mail_from_domain.assert_called_once()


def test_set_identity_mail_from_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_mail_from_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_mail_from_domain",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set identity mail from domain"):
        set_identity_mail_from_domain("test-identity", region_name=REGION)


def test_set_identity_notification_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_notification_topic.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_notification_topic("test-identity", "test-notification_type", region_name=REGION)
    mock_client.set_identity_notification_topic.assert_called_once()


def test_set_identity_notification_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_identity_notification_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_notification_topic",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set identity notification topic"):
        set_identity_notification_topic("test-identity", "test-notification_type", region_name=REGION)


def test_set_receipt_rule_position(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_receipt_rule_position.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_receipt_rule_position("test-rule_set_name", "test-rule_name", region_name=REGION)
    mock_client.set_receipt_rule_position.assert_called_once()


def test_set_receipt_rule_position_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_receipt_rule_position.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_receipt_rule_position",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set receipt rule position"):
        set_receipt_rule_position("test-rule_set_name", "test-rule_name", region_name=REGION)


def test_update_account_sending_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_sending_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_account_sending_enabled(region_name=REGION)
    mock_client.update_account_sending_enabled.assert_called_once()


def test_update_account_sending_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_sending_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_sending_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account sending enabled"):
        update_account_sending_enabled(region_name=REGION)


def test_update_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_configuration_set_event_destination("test-configuration_set_name", {}, region_name=REGION)
    mock_client.update_configuration_set_event_destination.assert_called_once()


def test_update_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration set event destination"):
        update_configuration_set_event_destination("test-configuration_set_name", {}, region_name=REGION)


def test_update_configuration_set_reputation_metrics_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_reputation_metrics_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_configuration_set_reputation_metrics_enabled("test-configuration_set_name", True, region_name=REGION)
    mock_client.update_configuration_set_reputation_metrics_enabled.assert_called_once()


def test_update_configuration_set_reputation_metrics_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_reputation_metrics_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_set_reputation_metrics_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration set reputation metrics enabled"):
        update_configuration_set_reputation_metrics_enabled("test-configuration_set_name", True, region_name=REGION)


def test_update_configuration_set_sending_enabled(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_sending_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_configuration_set_sending_enabled("test-configuration_set_name", True, region_name=REGION)
    mock_client.update_configuration_set_sending_enabled.assert_called_once()


def test_update_configuration_set_sending_enabled_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_sending_enabled.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_set_sending_enabled",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration set sending enabled"):
        update_configuration_set_sending_enabled("test-configuration_set_name", True, region_name=REGION)


def test_update_configuration_set_tracking_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_tracking_options.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_configuration_set_tracking_options("test-configuration_set_name", {}, region_name=REGION)
    mock_client.update_configuration_set_tracking_options.assert_called_once()


def test_update_configuration_set_tracking_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_tracking_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_set_tracking_options",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration set tracking options"):
        update_configuration_set_tracking_options("test-configuration_set_name", {}, region_name=REGION)


def test_update_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_custom_verification_email_template("test-template_name", region_name=REGION)
    mock_client.update_custom_verification_email_template.assert_called_once()


def test_update_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update custom verification email template"):
        update_custom_verification_email_template("test-template_name", region_name=REGION)


def test_update_receipt_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_receipt_rule.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_receipt_rule("test-rule_set_name", {}, region_name=REGION)
    mock_client.update_receipt_rule.assert_called_once()


def test_update_receipt_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_receipt_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_receipt_rule",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update receipt rule"):
        update_receipt_rule("test-rule_set_name", {}, region_name=REGION)


def test_update_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_template({}, region_name=REGION)
    mock_client.update_template.assert_called_once()


def test_update_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_template",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update template"):
        update_template({}, region_name=REGION)


def test_verify_domain_dkim(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_domain_dkim.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    verify_domain_dkim("test-domain", region_name=REGION)
    mock_client.verify_domain_dkim.assert_called_once()


def test_verify_domain_dkim_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_domain_dkim.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_domain_dkim",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify domain dkim"):
        verify_domain_dkim("test-domain", region_name=REGION)


def test_verify_domain_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_domain_identity.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    verify_domain_identity("test-domain", region_name=REGION)
    mock_client.verify_domain_identity.assert_called_once()


def test_verify_domain_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_domain_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_domain_identity",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify domain identity"):
        verify_domain_identity("test-domain", region_name=REGION)


def test_verify_email_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_email_identity.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    verify_email_identity("test-email_address", region_name=REGION)
    mock_client.verify_email_identity.assert_called_once()


def test_verify_email_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_email_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_email_identity",
    )
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify email identity"):
        verify_email_identity("test-email_address", region_name=REGION)


def test_create_receipt_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import create_receipt_rule
    mock_client = MagicMock()
    mock_client.create_receipt_rule.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    create_receipt_rule("test-rule_set_name", "test-rule", after="test-after", region_name="us-east-1")
    mock_client.create_receipt_rule.assert_called_once()

def test_describe_configuration_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import describe_configuration_set
    mock_client = MagicMock()
    mock_client.describe_configuration_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    describe_configuration_set({}, configuration_set_attribute_names={}, region_name="us-east-1")
    mock_client.describe_configuration_set.assert_called_once()

def test_list_configuration_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import list_configuration_sets
    mock_client = MagicMock()
    mock_client.list_configuration_sets.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_configuration_sets(next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.list_configuration_sets.assert_called_once()

def test_list_custom_verification_email_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import list_custom_verification_email_templates
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_custom_verification_email_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_custom_verification_email_templates.assert_called_once()

def test_list_identities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import list_identities
    mock_client = MagicMock()
    mock_client.list_identities.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_identities(identity_type="test-identity_type", next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.list_identities.assert_called_once()

def test_list_receipt_rule_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import list_receipt_rule_sets
    mock_client = MagicMock()
    mock_client.list_receipt_rule_sets.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_receipt_rule_sets(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_receipt_rule_sets.assert_called_once()

def test_list_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import list_templates
    mock_client = MagicMock()
    mock_client.list_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    list_templates(next_token="test-next_token", max_items=1, region_name="us-east-1")
    mock_client.list_templates.assert_called_once()

def test_put_configuration_set_delivery_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import put_configuration_set_delivery_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_delivery_options({}, delivery_options={}, region_name="us-east-1")
    mock_client.put_configuration_set_delivery_options.assert_called_once()

def test_send_bounce_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import send_bounce
    mock_client = MagicMock()
    mock_client.send_bounce.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_bounce("test-original_message_id", "test-bounce_sender", "test-bounced_recipient_info_list", explanation="test-explanation", message_dsn="test-message_dsn", bounce_sender_arn="test-bounce_sender_arn", region_name="us-east-1")
    mock_client.send_bounce.assert_called_once()

def test_send_bulk_templated_email_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import send_bulk_templated_email
    mock_client = MagicMock()
    mock_client.send_bulk_templated_email.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_bulk_templated_email("test-source", "test-template", "test-default_template_data", "test-destinations", source_arn="test-source_arn", reply_to_addresses="test-reply_to_addresses", return_path="test-return_path", return_path_arn="test-return_path_arn", configuration_set_name={}, default_tags=[{"Key": "k", "Value": "v"}], template_arn="test-template_arn", region_name="us-east-1")
    mock_client.send_bulk_templated_email.assert_called_once()

def test_send_custom_verification_email_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import send_custom_verification_email
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    send_custom_verification_email("test-email_address", "test-template_name", configuration_set_name={}, region_name="us-east-1")
    mock_client.send_custom_verification_email.assert_called_once()

def test_set_active_receipt_rule_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import set_active_receipt_rule_set
    mock_client = MagicMock()
    mock_client.set_active_receipt_rule_set.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_active_receipt_rule_set(rule_set_name="test-rule_set_name", region_name="us-east-1")
    mock_client.set_active_receipt_rule_set.assert_called_once()

def test_set_identity_mail_from_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import set_identity_mail_from_domain
    mock_client = MagicMock()
    mock_client.set_identity_mail_from_domain.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_mail_from_domain("test-identity", mail_from_domain="test-mail_from_domain", behavior_on_mx_failure="test-behavior_on_mx_failure", region_name="us-east-1")
    mock_client.set_identity_mail_from_domain.assert_called_once()

def test_set_identity_notification_topic_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import set_identity_notification_topic
    mock_client = MagicMock()
    mock_client.set_identity_notification_topic.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_identity_notification_topic("test-identity", "test-notification_type", sns_topic="test-sns_topic", region_name="us-east-1")
    mock_client.set_identity_notification_topic.assert_called_once()

def test_set_receipt_rule_position_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import set_receipt_rule_position
    mock_client = MagicMock()
    mock_client.set_receipt_rule_position.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    set_receipt_rule_position("test-rule_set_name", "test-rule_name", after="test-after", region_name="us-east-1")
    mock_client.set_receipt_rule_position.assert_called_once()

def test_update_account_sending_enabled_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import update_account_sending_enabled
    mock_client = MagicMock()
    mock_client.update_account_sending_enabled.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_account_sending_enabled(enabled=True, region_name="us-east-1")
    mock_client.update_account_sending_enabled.assert_called_once()

def test_update_custom_verification_email_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses import update_custom_verification_email_template
    mock_client = MagicMock()
    mock_client.update_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses.get_client", lambda *a, **kw: mock_client)
    update_custom_verification_email_template("test-template_name", from_email_address="test-from_email_address", template_subject="test-template_subject", template_content="test-template_content", success_redirection_url="test-success_redirection_url", failure_redirection_url="test-failure_redirection_url", region_name="us-east-1")
    mock_client.update_custom_verification_email_template.assert_called_once()
