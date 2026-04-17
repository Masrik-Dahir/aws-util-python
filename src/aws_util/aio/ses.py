"""Native async SES utilities using the async engine."""

from __future__ import annotations

import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.ses import (
    DescribeActiveReceiptRuleSetResult,
    DescribeConfigurationSetResult,
    DescribeReceiptRuleResult,
    DescribeReceiptRuleSetResult,
    EmailAddress,
    GetAccountSendingEnabledResult,
    GetCustomVerificationEmailTemplateResult,
    GetIdentityDkimAttributesResult,
    GetIdentityMailFromDomainAttributesResult,
    GetIdentityNotificationAttributesResult,
    GetIdentityPoliciesResult,
    GetIdentityVerificationAttributesResult,
    GetSendQuotaResult,
    GetSendStatisticsResult,
    GetTemplateResult,
    ListConfigurationSetsResult,
    ListCustomVerificationEmailTemplatesResult,
    ListIdentitiesResult,
    ListIdentityPoliciesResult,
    ListReceiptFiltersResult,
    ListReceiptRuleSetsResult,
    ListTemplatesResult,
    RunRenderTemplateResult,
    SendBounceResult,
    SendBulkTemplatedEmailResult,
    SendCustomVerificationEmailResult,
    SendEmailResult,
    VerifyDomainDkimResult,
    VerifyDomainIdentityResult,
)

__all__ = [
    "DescribeActiveReceiptRuleSetResult",
    "DescribeConfigurationSetResult",
    "DescribeReceiptRuleResult",
    "DescribeReceiptRuleSetResult",
    "EmailAddress",
    "GetAccountSendingEnabledResult",
    "GetCustomVerificationEmailTemplateResult",
    "GetIdentityDkimAttributesResult",
    "GetIdentityMailFromDomainAttributesResult",
    "GetIdentityNotificationAttributesResult",
    "GetIdentityPoliciesResult",
    "GetIdentityVerificationAttributesResult",
    "GetSendQuotaResult",
    "GetSendStatisticsResult",
    "GetTemplateResult",
    "ListConfigurationSetsResult",
    "ListCustomVerificationEmailTemplatesResult",
    "ListIdentitiesResult",
    "ListIdentityPoliciesResult",
    "ListReceiptFiltersResult",
    "ListReceiptRuleSetsResult",
    "ListTemplatesResult",
    "RunRenderTemplateResult",
    "SendBounceResult",
    "SendBulkTemplatedEmailResult",
    "SendCustomVerificationEmailResult",
    "SendEmailResult",
    "VerifyDomainDkimResult",
    "VerifyDomainIdentityResult",
    "clone_receipt_rule_set",
    "create_configuration_set",
    "create_configuration_set_event_destination",
    "create_configuration_set_tracking_options",
    "create_custom_verification_email_template",
    "create_receipt_filter",
    "create_receipt_rule",
    "create_receipt_rule_set",
    "create_template",
    "delete_configuration_set",
    "delete_configuration_set_event_destination",
    "delete_configuration_set_tracking_options",
    "delete_custom_verification_email_template",
    "delete_identity",
    "delete_identity_policy",
    "delete_receipt_filter",
    "delete_receipt_rule",
    "delete_receipt_rule_set",
    "delete_template",
    "delete_verified_email_address",
    "describe_active_receipt_rule_set",
    "describe_configuration_set",
    "describe_receipt_rule",
    "describe_receipt_rule_set",
    "get_account_sending_enabled",
    "get_custom_verification_email_template",
    "get_identity_dkim_attributes",
    "get_identity_mail_from_domain_attributes",
    "get_identity_notification_attributes",
    "get_identity_policies",
    "get_identity_verification_attributes",
    "get_send_quota",
    "get_send_statistics",
    "get_template",
    "list_configuration_sets",
    "list_custom_verification_email_templates",
    "list_identities",
    "list_identity_policies",
    "list_receipt_filters",
    "list_receipt_rule_sets",
    "list_templates",
    "list_verified_email_addresses",
    "put_configuration_set_delivery_options",
    "put_identity_policy",
    "reorder_receipt_rule_set",
    "run_render_template",
    "send_bounce",
    "send_bulk",
    "send_bulk_templated_email",
    "send_custom_verification_email",
    "send_email",
    "send_raw_email",
    "send_templated_email",
    "send_with_attachment",
    "set_active_receipt_rule_set",
    "set_identity_dkim_enabled",
    "set_identity_feedback_forwarding_enabled",
    "set_identity_headers_in_notifications_enabled",
    "set_identity_mail_from_domain",
    "set_identity_notification_topic",
    "set_receipt_rule_position",
    "update_account_sending_enabled",
    "update_configuration_set_event_destination",
    "update_configuration_set_reputation_metrics_enabled",
    "update_configuration_set_sending_enabled",
    "update_configuration_set_tracking_options",
    "update_custom_verification_email_template",
    "update_receipt_rule",
    "update_template",
    "verify_domain_dkim",
    "verify_domain_identity",
    "verify_email_address",
    "verify_email_identity",
]


async def send_email(
    from_address: str,
    to_addresses: list[str],
    subject: str,
    body_text: str | None = None,
    body_html: str | None = None,
    cc_addresses: list[str] | None = None,
    bcc_addresses: list[str] | None = None,
    reply_to_addresses: list[str] | None = None,
    charset: str = "UTF-8",
    region_name: str | None = None,
) -> SendEmailResult:
    """Send an email via Amazon SES.

    At least one of *body_text* or *body_html* must be provided.

    Args:
        from_address: Verified sender email address.
        to_addresses: List of recipient email addresses.
        subject: Email subject line.
        body_text: Plain-text body.
        body_html: HTML body.  When both are provided SES sends a multipart
            message and mail clients show the HTML version.
        cc_addresses: CC recipients.
        bcc_addresses: BCC recipients.
        reply_to_addresses: Reply-to addresses.
        charset: Character set for subject and body (default ``"UTF-8"``).
        region_name: AWS region override.

    Returns:
        A :class:`SendEmailResult` with the assigned message ID.

    Raises:
        ValueError: If neither *body_text* nor *body_html* is provided.
        RuntimeError: If the send fails.
    """
    if not body_text and not body_html:
        raise ValueError("At least one of body_text or body_html must be provided")

    client = async_client("ses", region_name)
    destination: dict[str, Any] = {"ToAddresses": to_addresses}
    if cc_addresses:
        destination["CcAddresses"] = cc_addresses
    if bcc_addresses:
        destination["BccAddresses"] = bcc_addresses

    body: dict[str, Any] = {}
    if body_text:
        body["Text"] = {"Data": body_text, "Charset": charset}
    if body_html:
        body["Html"] = {"Data": body_html, "Charset": charset}

    kwargs: dict[str, Any] = {
        "Source": from_address,
        "Destination": destination,
        "Message": {
            "Subject": {"Data": subject, "Charset": charset},
            "Body": body,
        },
    }
    if reply_to_addresses:
        kwargs["ReplyToAddresses"] = reply_to_addresses

    try:
        resp = await client.call("SendEmail", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to send email") from exc
    return SendEmailResult(message_id=resp["MessageId"])


async def send_templated_email(
    from_address: str,
    to_addresses: list[str],
    template_name: str,
    template_data: dict[str, Any],
    cc_addresses: list[str] | None = None,
    bcc_addresses: list[str] | None = None,
    region_name: str | None = None,
) -> SendEmailResult:
    """Send a templated email via Amazon SES.

    Args:
        from_address: Verified sender email address.
        to_addresses: Recipient email addresses.
        template_name: Name of the SES email template.
        template_data: Template variable substitution as a dict.
        cc_addresses: CC recipients.
        bcc_addresses: BCC recipients.
        region_name: AWS region override.

    Returns:
        A :class:`SendEmailResult` with the assigned message ID.

    Raises:
        RuntimeError: If the send fails.
    """
    client = async_client("ses", region_name)
    destination: dict[str, Any] = {"ToAddresses": to_addresses}
    if cc_addresses:
        destination["CcAddresses"] = cc_addresses
    if bcc_addresses:
        destination["BccAddresses"] = bcc_addresses

    try:
        resp = await client.call(
            "SendTemplatedEmail",
            Source=from_address,
            Destination=destination,
            Template=template_name,
            TemplateData=json.dumps(template_data),
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to send templated email with template {template_name!r}"
        ) from exc
    return SendEmailResult(message_id=resp["MessageId"])


async def send_raw_email(
    raw_message: bytes,
    from_address: str | None = None,
    to_addresses: list[str] | None = None,
    region_name: str | None = None,
) -> SendEmailResult:
    """Send a pre-formatted raw MIME email via Amazon SES.

    Use this for emails with attachments or complex multipart structures.

    Args:
        raw_message: The raw MIME message bytes.
        from_address: Sender address (overrides the ``From:`` header if set).
        to_addresses: Recipient addresses (override ``To:`` header if set).
        region_name: AWS region override.

    Returns:
        A :class:`SendEmailResult` with the assigned message ID.

    Raises:
        RuntimeError: If the send fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {"RawMessage": {"Data": raw_message}}
    if from_address:
        kwargs["Source"] = from_address
    if to_addresses:
        kwargs["Destinations"] = to_addresses
    try:
        resp = await client.call("SendRawEmail", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to send raw email") from exc
    return SendEmailResult(message_id=resp["MessageId"])


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def send_with_attachment(
    from_address: str,
    to_addresses: list[str],
    subject: str,
    body_text: str | None = None,
    body_html: str | None = None,
    attachments: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> SendEmailResult:
    """Send an email with file attachments via Amazon SES.

    Builds a multipart MIME message and sends it via :func:`send_raw_email`.
    Each attachment dict must have ``"filename"`` and ``"data"`` (bytes) keys,
    and optionally a ``"mimetype"`` key (defaults to
    ``"application/octet-stream"``).

    Args:
        from_address: Verified sender email address.
        to_addresses: Recipient email addresses.
        subject: Email subject line.
        body_text: Plain-text body.
        body_html: HTML body.
        attachments: List of attachment dicts with ``"filename"``, ``"data"``,
            and optional ``"mimetype"`` keys.
        region_name: AWS region override.

    Returns:
        A :class:`SendEmailResult` with the assigned message ID.

    Raises:
        ValueError: If neither *body_text* nor *body_html* is provided.
        RuntimeError: If the send fails.
    """
    import email.mime.application as _mime_app
    import email.mime.multipart as _mime_multi
    import email.mime.text as _mime_text

    if not body_text and not body_html:
        raise ValueError("At least one of body_text or body_html must be provided")

    msg = _mime_multi.MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = ", ".join(to_addresses)

    body_part = _mime_multi.MIMEMultipart("alternative")
    if body_text:
        body_part.attach(_mime_text.MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        body_part.attach(_mime_text.MIMEText(body_html, "html", "utf-8"))
    msg.attach(body_part)

    for att in attachments or []:
        part = _mime_app.MIMEApplication(
            att["data"],
            Name=att["filename"],
        )
        part["Content-Disposition"] = f'attachment; filename="{att["filename"]}"'
        if att.get("mimetype"):
            part.set_type(att["mimetype"])
        msg.attach(part)

    return await send_raw_email(
        raw_message=msg.as_bytes(),
        from_address=from_address,
        to_addresses=to_addresses,
        region_name=region_name,
    )


async def send_bulk(
    from_address: str,
    messages: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[SendEmailResult]:
    """Send multiple independent emails via Amazon SES.

    Each message dict must contain ``"to_addresses"`` (list[str]),
    ``"subject"`` (str), and at least one of ``"body_text"`` or
    ``"body_html"``.

    Args:
        from_address: Verified sender email address used for all messages.
        messages: List of message dicts.
        region_name: AWS region override.

    Returns:
        A list of :class:`SendEmailResult` objects in the same order as
        *messages*.

    Raises:
        RuntimeError: If any individual send fails (fails fast).
    """
    results: list[SendEmailResult] = []
    for msg in messages:
        result = await send_email(
            from_address=from_address,
            to_addresses=msg["to_addresses"],
            subject=msg["subject"],
            body_text=msg.get("body_text"),
            body_html=msg.get("body_html"),
            cc_addresses=msg.get("cc_addresses"),
            bcc_addresses=msg.get("bcc_addresses"),
            reply_to_addresses=msg.get("reply_to_addresses"),
            region_name=region_name,
        )
        results.append(result)
    return results


async def verify_email_address(
    email_address: str,
    region_name: str | None = None,
) -> None:
    """Send a verification email to an address.

    The address owner must click the link in the verification email before SES
    allows sending from it.

    Args:
        email_address: Email address to verify.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the verification request fails.
    """
    client = async_client("ses", region_name)
    try:
        await client.call("VerifyEmailAddress", EmailAddress=email_address)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to verify email address {email_address!r}") from exc


async def list_verified_email_addresses(
    region_name: str | None = None,
) -> list[str]:
    """List all verified email addresses in the SES account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of verified email address strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    try:
        resp = await client.call("ListVerifiedEmailAddresses")
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_verified_email_addresses failed") from exc
    return resp.get("VerifiedEmailAddresses", [])


async def clone_receipt_rule_set(
    rule_set_name: str,
    original_rule_set_name: str,
    region_name: str | None = None,
) -> None:
    """Clone receipt rule set.

    Args:
        rule_set_name: Rule set name.
        original_rule_set_name: Original rule set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["OriginalRuleSetName"] = original_rule_set_name
    try:
        await client.call("CloneReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to clone receipt rule set") from exc
    return None


async def create_configuration_set(
    configuration_set: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create configuration set.

    Args:
        configuration_set: Configuration set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSet"] = configuration_set
    try:
        await client.call("CreateConfigurationSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create configuration set") from exc
    return None


async def create_configuration_set_event_destination(
    configuration_set_name: str,
    event_destination: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create configuration set event destination.

    Args:
        configuration_set_name: Configuration set name.
        event_destination: Event destination.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestination"] = event_destination
    try:
        await client.call("CreateConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create configuration set event destination") from exc
    return None


async def create_configuration_set_tracking_options(
    configuration_set_name: str,
    tracking_options: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create configuration set tracking options.

    Args:
        configuration_set_name: Configuration set name.
        tracking_options: Tracking options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["TrackingOptions"] = tracking_options
    try:
        await client.call("CreateConfigurationSetTrackingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create configuration set tracking options") from exc
    return None


async def create_custom_verification_email_template(
    template_name: str,
    from_email_address: str,
    template_subject: str,
    template_content: str,
    success_redirection_url: str,
    failure_redirection_url: str,
    region_name: str | None = None,
) -> None:
    """Create custom verification email template.

    Args:
        template_name: Template name.
        from_email_address: From email address.
        template_subject: Template subject.
        template_content: Template content.
        success_redirection_url: Success redirection url.
        failure_redirection_url: Failure redirection url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    kwargs["FromEmailAddress"] = from_email_address
    kwargs["TemplateSubject"] = template_subject
    kwargs["TemplateContent"] = template_content
    kwargs["SuccessRedirectionURL"] = success_redirection_url
    kwargs["FailureRedirectionURL"] = failure_redirection_url
    try:
        await client.call("CreateCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom verification email template") from exc
    return None


async def create_receipt_filter(
    filter: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create receipt filter.

    Args:
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Filter"] = filter
    try:
        await client.call("CreateReceiptFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create receipt filter") from exc
    return None


async def create_receipt_rule(
    rule_set_name: str,
    rule: dict[str, Any],
    *,
    after: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create receipt rule.

    Args:
        rule_set_name: Rule set name.
        rule: Rule.
        after: After.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["Rule"] = rule
    if after is not None:
        kwargs["After"] = after
    try:
        await client.call("CreateReceiptRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create receipt rule") from exc
    return None


async def create_receipt_rule_set(
    rule_set_name: str,
    region_name: str | None = None,
) -> None:
    """Create receipt rule set.

    Args:
        rule_set_name: Rule set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    try:
        await client.call("CreateReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create receipt rule set") from exc
    return None


async def create_template(
    template: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create template.

    Args:
        template: Template.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Template"] = template
    try:
        await client.call("CreateTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create template") from exc
    return None


async def delete_configuration_set(
    configuration_set_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration set.

    Args:
        configuration_set_name: Configuration set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        await client.call("DeleteConfigurationSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration set") from exc
    return None


async def delete_configuration_set_event_destination(
    configuration_set_name: str,
    event_destination_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration set event destination.

    Args:
        configuration_set_name: Configuration set name.
        event_destination_name: Event destination name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestinationName"] = event_destination_name
    try:
        await client.call("DeleteConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration set event destination") from exc
    return None


async def delete_configuration_set_tracking_options(
    configuration_set_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration set tracking options.

    Args:
        configuration_set_name: Configuration set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        await client.call("DeleteConfigurationSetTrackingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration set tracking options") from exc
    return None


async def delete_custom_verification_email_template(
    template_name: str,
    region_name: str | None = None,
) -> None:
    """Delete custom verification email template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    try:
        await client.call("DeleteCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom verification email template") from exc
    return None


async def delete_identity(
    identity: str,
    region_name: str | None = None,
) -> None:
    """Delete identity.

    Args:
        identity: Identity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    try:
        await client.call("DeleteIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete identity") from exc
    return None


async def delete_identity_policy(
    identity: str,
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete identity policy.

    Args:
        identity: Identity.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["PolicyName"] = policy_name
    try:
        await client.call("DeleteIdentityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete identity policy") from exc
    return None


async def delete_receipt_filter(
    filter_name: str,
    region_name: str | None = None,
) -> None:
    """Delete receipt filter.

    Args:
        filter_name: Filter name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FilterName"] = filter_name
    try:
        await client.call("DeleteReceiptFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete receipt filter") from exc
    return None


async def delete_receipt_rule(
    rule_set_name: str,
    rule_name: str,
    region_name: str | None = None,
) -> None:
    """Delete receipt rule.

    Args:
        rule_set_name: Rule set name.
        rule_name: Rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["RuleName"] = rule_name
    try:
        await client.call("DeleteReceiptRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete receipt rule") from exc
    return None


async def delete_receipt_rule_set(
    rule_set_name: str,
    region_name: str | None = None,
) -> None:
    """Delete receipt rule set.

    Args:
        rule_set_name: Rule set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    try:
        await client.call("DeleteReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete receipt rule set") from exc
    return None


async def delete_template(
    template_name: str,
    region_name: str | None = None,
) -> None:
    """Delete template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    try:
        await client.call("DeleteTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete template") from exc
    return None


async def delete_verified_email_address(
    email_address: str,
    region_name: str | None = None,
) -> None:
    """Delete verified email address.

    Args:
        email_address: Email address.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    try:
        await client.call("DeleteVerifiedEmailAddress", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete verified email address") from exc
    return None


async def describe_active_receipt_rule_set(
    region_name: str | None = None,
) -> DescribeActiveReceiptRuleSetResult:
    """Describe active receipt rule set.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeActiveReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe active receipt rule set") from exc
    return DescribeActiveReceiptRuleSetResult(
        metadata=resp.get("Metadata"),
        rules=resp.get("Rules"),
    )


async def describe_configuration_set(
    configuration_set_name: str,
    *,
    configuration_set_attribute_names: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeConfigurationSetResult:
    """Describe configuration set.

    Args:
        configuration_set_name: Configuration set name.
        configuration_set_attribute_names: Configuration set attribute names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if configuration_set_attribute_names is not None:
        kwargs["ConfigurationSetAttributeNames"] = configuration_set_attribute_names
    try:
        resp = await client.call("DescribeConfigurationSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration set") from exc
    return DescribeConfigurationSetResult(
        configuration_set=resp.get("ConfigurationSet"),
        event_destinations=resp.get("EventDestinations"),
        tracking_options=resp.get("TrackingOptions"),
        delivery_options=resp.get("DeliveryOptions"),
        reputation_options=resp.get("ReputationOptions"),
    )


async def describe_receipt_rule(
    rule_set_name: str,
    rule_name: str,
    region_name: str | None = None,
) -> DescribeReceiptRuleResult:
    """Describe receipt rule.

    Args:
        rule_set_name: Rule set name.
        rule_name: Rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["RuleName"] = rule_name
    try:
        resp = await client.call("DescribeReceiptRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe receipt rule") from exc
    return DescribeReceiptRuleResult(
        rule=resp.get("Rule"),
    )


async def describe_receipt_rule_set(
    rule_set_name: str,
    region_name: str | None = None,
) -> DescribeReceiptRuleSetResult:
    """Describe receipt rule set.

    Args:
        rule_set_name: Rule set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    try:
        resp = await client.call("DescribeReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe receipt rule set") from exc
    return DescribeReceiptRuleSetResult(
        metadata=resp.get("Metadata"),
        rules=resp.get("Rules"),
    )


async def get_account_sending_enabled(
    region_name: str | None = None,
) -> GetAccountSendingEnabledResult:
    """Get account sending enabled.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAccountSendingEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account sending enabled") from exc
    return GetAccountSendingEnabledResult(
        enabled=resp.get("Enabled"),
    )


async def get_custom_verification_email_template(
    template_name: str,
    region_name: str | None = None,
) -> GetCustomVerificationEmailTemplateResult:
    """Get custom verification email template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    try:
        resp = await client.call("GetCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get custom verification email template") from exc
    return GetCustomVerificationEmailTemplateResult(
        template_name=resp.get("TemplateName"),
        from_email_address=resp.get("FromEmailAddress"),
        template_subject=resp.get("TemplateSubject"),
        template_content=resp.get("TemplateContent"),
        success_redirection_url=resp.get("SuccessRedirectionURL"),
        failure_redirection_url=resp.get("FailureRedirectionURL"),
    )


async def get_identity_dkim_attributes(
    identities: list[str],
    region_name: str | None = None,
) -> GetIdentityDkimAttributesResult:
    """Get identity dkim attributes.

    Args:
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identities"] = identities
    try:
        resp = await client.call("GetIdentityDkimAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity dkim attributes") from exc
    return GetIdentityDkimAttributesResult(
        dkim_attributes=resp.get("DkimAttributes"),
    )


async def get_identity_mail_from_domain_attributes(
    identities: list[str],
    region_name: str | None = None,
) -> GetIdentityMailFromDomainAttributesResult:
    """Get identity mail from domain attributes.

    Args:
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identities"] = identities
    try:
        resp = await client.call("GetIdentityMailFromDomainAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity mail from domain attributes") from exc
    return GetIdentityMailFromDomainAttributesResult(
        mail_from_domain_attributes=resp.get("MailFromDomainAttributes"),
    )


async def get_identity_notification_attributes(
    identities: list[str],
    region_name: str | None = None,
) -> GetIdentityNotificationAttributesResult:
    """Get identity notification attributes.

    Args:
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identities"] = identities
    try:
        resp = await client.call("GetIdentityNotificationAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity notification attributes") from exc
    return GetIdentityNotificationAttributesResult(
        notification_attributes=resp.get("NotificationAttributes"),
    )


async def get_identity_policies(
    identity: str,
    policy_names: list[str],
    region_name: str | None = None,
) -> GetIdentityPoliciesResult:
    """Get identity policies.

    Args:
        identity: Identity.
        policy_names: Policy names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["PolicyNames"] = policy_names
    try:
        resp = await client.call("GetIdentityPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity policies") from exc
    return GetIdentityPoliciesResult(
        policies=resp.get("Policies"),
    )


async def get_identity_verification_attributes(
    identities: list[str],
    region_name: str | None = None,
) -> GetIdentityVerificationAttributesResult:
    """Get identity verification attributes.

    Args:
        identities: Identities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identities"] = identities
    try:
        resp = await client.call("GetIdentityVerificationAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity verification attributes") from exc
    return GetIdentityVerificationAttributesResult(
        verification_attributes=resp.get("VerificationAttributes"),
    )


async def get_send_quota(
    region_name: str | None = None,
) -> GetSendQuotaResult:
    """Get send quota.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetSendQuota", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get send quota") from exc
    return GetSendQuotaResult(
        max24_hour_send=resp.get("Max24HourSend"),
        max_send_rate=resp.get("MaxSendRate"),
        sent_last24_hours=resp.get("SentLast24Hours"),
    )


async def get_send_statistics(
    region_name: str | None = None,
) -> GetSendStatisticsResult:
    """Get send statistics.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetSendStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get send statistics") from exc
    return GetSendStatisticsResult(
        send_data_points=resp.get("SendDataPoints"),
    )


async def get_template(
    template_name: str,
    region_name: str | None = None,
) -> GetTemplateResult:
    """Get template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    try:
        resp = await client.call("GetTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get template") from exc
    return GetTemplateResult(
        template=resp.get("Template"),
    )


async def list_configuration_sets(
    *,
    next_token: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListConfigurationSetsResult:
    """List configuration sets.

    Args:
        next_token: Next token.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListConfigurationSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list configuration sets") from exc
    return ListConfigurationSetsResult(
        configuration_sets=resp.get("ConfigurationSets"),
        next_token=resp.get("NextToken"),
    )


async def list_custom_verification_email_templates(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCustomVerificationEmailTemplatesResult:
    """List custom verification email templates.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListCustomVerificationEmailTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom verification email templates") from exc
    return ListCustomVerificationEmailTemplatesResult(
        custom_verification_email_templates=resp.get("CustomVerificationEmailTemplates"),
        next_token=resp.get("NextToken"),
    )


async def list_identities(
    *,
    identity_type: str | None = None,
    next_token: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListIdentitiesResult:
    """List identities.

    Args:
        identity_type: Identity type.
        next_token: Next token.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if identity_type is not None:
        kwargs["IdentityType"] = identity_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListIdentities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list identities") from exc
    return ListIdentitiesResult(
        identities=resp.get("Identities"),
        next_token=resp.get("NextToken"),
    )


async def list_identity_policies(
    identity: str,
    region_name: str | None = None,
) -> ListIdentityPoliciesResult:
    """List identity policies.

    Args:
        identity: Identity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    try:
        resp = await client.call("ListIdentityPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list identity policies") from exc
    return ListIdentityPoliciesResult(
        policy_names=resp.get("PolicyNames"),
    )


async def list_receipt_filters(
    region_name: str | None = None,
) -> ListReceiptFiltersResult:
    """List receipt filters.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("ListReceiptFilters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list receipt filters") from exc
    return ListReceiptFiltersResult(
        filters=resp.get("Filters"),
    )


async def list_receipt_rule_sets(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListReceiptRuleSetsResult:
    """List receipt rule sets.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListReceiptRuleSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list receipt rule sets") from exc
    return ListReceiptRuleSetsResult(
        rule_sets=resp.get("RuleSets"),
        next_token=resp.get("NextToken"),
    )


async def list_templates(
    *,
    next_token: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListTemplatesResult:
    """List templates.

    Args:
        next_token: Next token.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list templates") from exc
    return ListTemplatesResult(
        templates_metadata=resp.get("TemplatesMetadata"),
        next_token=resp.get("NextToken"),
    )


async def put_configuration_set_delivery_options(
    configuration_set_name: str,
    *,
    delivery_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set delivery options.

    Args:
        configuration_set_name: Configuration set name.
        delivery_options: Delivery options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if delivery_options is not None:
        kwargs["DeliveryOptions"] = delivery_options
    try:
        await client.call("PutConfigurationSetDeliveryOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set delivery options") from exc
    return None


async def put_identity_policy(
    identity: str,
    policy_name: str,
    policy: str,
    region_name: str | None = None,
) -> None:
    """Put identity policy.

    Args:
        identity: Identity.
        policy_name: Policy name.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["PolicyName"] = policy_name
    kwargs["Policy"] = policy
    try:
        await client.call("PutIdentityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put identity policy") from exc
    return None


async def reorder_receipt_rule_set(
    rule_set_name: str,
    rule_names: list[str],
    region_name: str | None = None,
) -> None:
    """Reorder receipt rule set.

    Args:
        rule_set_name: Rule set name.
        rule_names: Rule names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["RuleNames"] = rule_names
    try:
        await client.call("ReorderReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reorder receipt rule set") from exc
    return None


async def run_render_template(
    template_name: str,
    template_data: str,
    region_name: str | None = None,
) -> RunRenderTemplateResult:
    """Run render template.

    Args:
        template_name: Template name.
        template_data: Template data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    kwargs["TemplateData"] = template_data
    try:
        resp = await client.call("TestRenderTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run render template") from exc
    return RunRenderTemplateResult(
        rendered_template=resp.get("RenderedTemplate"),
    )


async def send_bounce(
    original_message_id: str,
    bounce_sender: str,
    bounced_recipient_info_list: list[dict[str, Any]],
    *,
    explanation: str | None = None,
    message_dsn: dict[str, Any] | None = None,
    bounce_sender_arn: str | None = None,
    region_name: str | None = None,
) -> SendBounceResult:
    """Send bounce.

    Args:
        original_message_id: Original message id.
        bounce_sender: Bounce sender.
        bounced_recipient_info_list: Bounced recipient info list.
        explanation: Explanation.
        message_dsn: Message dsn.
        bounce_sender_arn: Bounce sender arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginalMessageId"] = original_message_id
    kwargs["BounceSender"] = bounce_sender
    kwargs["BouncedRecipientInfoList"] = bounced_recipient_info_list
    if explanation is not None:
        kwargs["Explanation"] = explanation
    if message_dsn is not None:
        kwargs["MessageDsn"] = message_dsn
    if bounce_sender_arn is not None:
        kwargs["BounceSenderArn"] = bounce_sender_arn
    try:
        resp = await client.call("SendBounce", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send bounce") from exc
    return SendBounceResult(
        message_id=resp.get("MessageId"),
    )


async def send_bulk_templated_email(
    source: str,
    template: str,
    default_template_data: str,
    destinations: list[dict[str, Any]],
    *,
    source_arn: str | None = None,
    reply_to_addresses: list[str] | None = None,
    return_path: str | None = None,
    return_path_arn: str | None = None,
    configuration_set_name: str | None = None,
    default_tags: list[dict[str, Any]] | None = None,
    template_arn: str | None = None,
    region_name: str | None = None,
) -> SendBulkTemplatedEmailResult:
    """Send bulk templated email.

    Args:
        source: Source.
        template: Template.
        default_template_data: Default template data.
        destinations: Destinations.
        source_arn: Source arn.
        reply_to_addresses: Reply to addresses.
        return_path: Return path.
        return_path_arn: Return path arn.
        configuration_set_name: Configuration set name.
        default_tags: Default tags.
        template_arn: Template arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Source"] = source
    kwargs["Template"] = template
    kwargs["DefaultTemplateData"] = default_template_data
    kwargs["Destinations"] = destinations
    if source_arn is not None:
        kwargs["SourceArn"] = source_arn
    if reply_to_addresses is not None:
        kwargs["ReplyToAddresses"] = reply_to_addresses
    if return_path is not None:
        kwargs["ReturnPath"] = return_path
    if return_path_arn is not None:
        kwargs["ReturnPathArn"] = return_path_arn
    if configuration_set_name is not None:
        kwargs["ConfigurationSetName"] = configuration_set_name
    if default_tags is not None:
        kwargs["DefaultTags"] = default_tags
    if template_arn is not None:
        kwargs["TemplateArn"] = template_arn
    try:
        resp = await client.call("SendBulkTemplatedEmail", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send bulk templated email") from exc
    return SendBulkTemplatedEmailResult(
        status=resp.get("Status"),
    )


async def send_custom_verification_email(
    email_address: str,
    template_name: str,
    *,
    configuration_set_name: str | None = None,
    region_name: str | None = None,
) -> SendCustomVerificationEmailResult:
    """Send custom verification email.

    Args:
        email_address: Email address.
        template_name: Template name.
        configuration_set_name: Configuration set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    kwargs["TemplateName"] = template_name
    if configuration_set_name is not None:
        kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        resp = await client.call("SendCustomVerificationEmail", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send custom verification email") from exc
    return SendCustomVerificationEmailResult(
        message_id=resp.get("MessageId"),
    )


async def set_active_receipt_rule_set(
    *,
    rule_set_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set active receipt rule set.

    Args:
        rule_set_name: Rule set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if rule_set_name is not None:
        kwargs["RuleSetName"] = rule_set_name
    try:
        await client.call("SetActiveReceiptRuleSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set active receipt rule set") from exc
    return None


async def set_identity_dkim_enabled(
    identity: str,
    dkim_enabled: bool,
    region_name: str | None = None,
) -> None:
    """Set identity dkim enabled.

    Args:
        identity: Identity.
        dkim_enabled: Dkim enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["DkimEnabled"] = dkim_enabled
    try:
        await client.call("SetIdentityDkimEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set identity dkim enabled") from exc
    return None


async def set_identity_feedback_forwarding_enabled(
    identity: str,
    forwarding_enabled: bool,
    region_name: str | None = None,
) -> None:
    """Set identity feedback forwarding enabled.

    Args:
        identity: Identity.
        forwarding_enabled: Forwarding enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["ForwardingEnabled"] = forwarding_enabled
    try:
        await client.call("SetIdentityFeedbackForwardingEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set identity feedback forwarding enabled") from exc
    return None


async def set_identity_headers_in_notifications_enabled(
    identity: str,
    notification_type: str,
    enabled: bool,
    region_name: str | None = None,
) -> None:
    """Set identity headers in notifications enabled.

    Args:
        identity: Identity.
        notification_type: Notification type.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["NotificationType"] = notification_type
    kwargs["Enabled"] = enabled
    try:
        await client.call("SetIdentityHeadersInNotificationsEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to set identity headers in notifications enabled"
        ) from exc
    return None


async def set_identity_mail_from_domain(
    identity: str,
    *,
    mail_from_domain: str | None = None,
    behavior_on_mx_failure: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set identity mail from domain.

    Args:
        identity: Identity.
        mail_from_domain: Mail from domain.
        behavior_on_mx_failure: Behavior on mx failure.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    if mail_from_domain is not None:
        kwargs["MailFromDomain"] = mail_from_domain
    if behavior_on_mx_failure is not None:
        kwargs["BehaviorOnMXFailure"] = behavior_on_mx_failure
    try:
        await client.call("SetIdentityMailFromDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set identity mail from domain") from exc
    return None


async def set_identity_notification_topic(
    identity: str,
    notification_type: str,
    *,
    sns_topic: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set identity notification topic.

    Args:
        identity: Identity.
        notification_type: Notification type.
        sns_topic: Sns topic.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identity"] = identity
    kwargs["NotificationType"] = notification_type
    if sns_topic is not None:
        kwargs["SnsTopic"] = sns_topic
    try:
        await client.call("SetIdentityNotificationTopic", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set identity notification topic") from exc
    return None


async def set_receipt_rule_position(
    rule_set_name: str,
    rule_name: str,
    *,
    after: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set receipt rule position.

    Args:
        rule_set_name: Rule set name.
        rule_name: Rule name.
        after: After.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["RuleName"] = rule_name
    if after is not None:
        kwargs["After"] = after
    try:
        await client.call("SetReceiptRulePosition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set receipt rule position") from exc
    return None


async def update_account_sending_enabled(
    *,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update account sending enabled.

    Args:
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        await client.call("UpdateAccountSendingEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account sending enabled") from exc
    return None


async def update_configuration_set_event_destination(
    configuration_set_name: str,
    event_destination: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update configuration set event destination.

    Args:
        configuration_set_name: Configuration set name.
        event_destination: Event destination.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestination"] = event_destination
    try:
        await client.call("UpdateConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration set event destination") from exc
    return None


async def update_configuration_set_reputation_metrics_enabled(
    configuration_set_name: str,
    enabled: bool,
    region_name: str | None = None,
) -> None:
    """Update configuration set reputation metrics enabled.

    Args:
        configuration_set_name: Configuration set name.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["Enabled"] = enabled
    try:
        await client.call("UpdateConfigurationSetReputationMetricsEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to update configuration set reputation metrics enabled"
        ) from exc
    return None


async def update_configuration_set_sending_enabled(
    configuration_set_name: str,
    enabled: bool,
    region_name: str | None = None,
) -> None:
    """Update configuration set sending enabled.

    Args:
        configuration_set_name: Configuration set name.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["Enabled"] = enabled
    try:
        await client.call("UpdateConfigurationSetSendingEnabled", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration set sending enabled") from exc
    return None


async def update_configuration_set_tracking_options(
    configuration_set_name: str,
    tracking_options: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update configuration set tracking options.

    Args:
        configuration_set_name: Configuration set name.
        tracking_options: Tracking options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["TrackingOptions"] = tracking_options
    try:
        await client.call("UpdateConfigurationSetTrackingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration set tracking options") from exc
    return None


async def update_custom_verification_email_template(
    template_name: str,
    *,
    from_email_address: str | None = None,
    template_subject: str | None = None,
    template_content: str | None = None,
    success_redirection_url: str | None = None,
    failure_redirection_url: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update custom verification email template.

    Args:
        template_name: Template name.
        from_email_address: From email address.
        template_subject: Template subject.
        template_content: Template content.
        success_redirection_url: Success redirection url.
        failure_redirection_url: Failure redirection url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    if from_email_address is not None:
        kwargs["FromEmailAddress"] = from_email_address
    if template_subject is not None:
        kwargs["TemplateSubject"] = template_subject
    if template_content is not None:
        kwargs["TemplateContent"] = template_content
    if success_redirection_url is not None:
        kwargs["SuccessRedirectionURL"] = success_redirection_url
    if failure_redirection_url is not None:
        kwargs["FailureRedirectionURL"] = failure_redirection_url
    try:
        await client.call("UpdateCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update custom verification email template") from exc
    return None


async def update_receipt_rule(
    rule_set_name: str,
    rule: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update receipt rule.

    Args:
        rule_set_name: Rule set name.
        rule: Rule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleSetName"] = rule_set_name
    kwargs["Rule"] = rule
    try:
        await client.call("UpdateReceiptRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update receipt rule") from exc
    return None


async def update_template(
    template: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update template.

    Args:
        template: Template.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Template"] = template
    try:
        await client.call("UpdateTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update template") from exc
    return None


async def verify_domain_dkim(
    domain: str,
    region_name: str | None = None,
) -> VerifyDomainDkimResult:
    """Verify domain dkim.

    Args:
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    try:
        resp = await client.call("VerifyDomainDkim", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to verify domain dkim") from exc
    return VerifyDomainDkimResult(
        dkim_tokens=resp.get("DkimTokens"),
    )


async def verify_domain_identity(
    domain: str,
    region_name: str | None = None,
) -> VerifyDomainIdentityResult:
    """Verify domain identity.

    Args:
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    try:
        resp = await client.call("VerifyDomainIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to verify domain identity") from exc
    return VerifyDomainIdentityResult(
        verification_token=resp.get("VerificationToken"),
    )


async def verify_email_identity(
    email_address: str,
    region_name: str | None = None,
) -> None:
    """Verify email identity.

    Args:
        email_address: Email address.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ses", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    try:
        await client.call("VerifyEmailIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to verify email identity") from exc
    return None
