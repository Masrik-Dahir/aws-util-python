"""Native async SES v2 utilities using the async engine."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.ses_v2 import (
    BatchGetMetricDataResult,
    ConfigSetResult,
    ContactListResult,
    ContactResult,
    CreateDeliverabilityTestReportResult,
    CreateMultiRegionEndpointResult,
    CreateTenantResult,
    DeleteMultiRegionEndpointResult,
    EmailIdentityResult,
    EmailTemplateResult,
    GetAccountResult,
    GetBlacklistReportsResult,
    GetConfigurationSetEventDestinationsResult,
    GetCustomVerificationEmailTemplateResult,
    GetDedicatedIpPoolResult,
    GetDedicatedIpResult,
    GetDedicatedIpsResult,
    GetDeliverabilityDashboardOptionsResult,
    GetDeliverabilityTestReportResult,
    GetDomainDeliverabilityCampaignResult,
    GetDomainStatisticsReportResult,
    GetEmailIdentityPoliciesResult,
    GetExportJobResult,
    GetMultiRegionEndpointResult,
    GetReputationEntityResult,
    GetSuppressedDestinationResult,
    GetTenantResult,
    ImportJobResult,
    ListCustomVerificationEmailTemplatesResult,
    ListDedicatedIpPoolsResult,
    ListDeliverabilityTestReportsResult,
    ListDomainDeliverabilityCampaignsResult,
    ListExportJobsResult,
    ListMultiRegionEndpointsResult,
    ListRecommendationsResult,
    ListReputationEntitiesResult,
    ListResourceTenantsResult,
    ListSuppressedDestinationsResult,
    ListTagsForResourceResult,
    ListTenantResourcesResult,
    ListTenantsResult,
    MessageInsightResult,
    PutEmailIdentityDkimSigningAttributesResult,
    RunRenderEmailTemplateResult,
    SendCustomVerificationEmailResult,
    SendEmailResult,
)

__all__ = [
    "BatchGetMetricDataResult",
    "ConfigSetResult",
    "ContactListResult",
    "ContactResult",
    "CreateDeliverabilityTestReportResult",
    "CreateMultiRegionEndpointResult",
    "CreateTenantResult",
    "DeleteMultiRegionEndpointResult",
    "EmailIdentityResult",
    "EmailTemplateResult",
    "GetAccountResult",
    "GetBlacklistReportsResult",
    "GetConfigurationSetEventDestinationsResult",
    "GetCustomVerificationEmailTemplateResult",
    "GetDedicatedIpPoolResult",
    "GetDedicatedIpResult",
    "GetDedicatedIpsResult",
    "GetDeliverabilityDashboardOptionsResult",
    "GetDeliverabilityTestReportResult",
    "GetDomainDeliverabilityCampaignResult",
    "GetDomainStatisticsReportResult",
    "GetEmailIdentityPoliciesResult",
    "GetExportJobResult",
    "GetMultiRegionEndpointResult",
    "GetReputationEntityResult",
    "GetSuppressedDestinationResult",
    "GetTenantResult",
    "ImportJobResult",
    "ListCustomVerificationEmailTemplatesResult",
    "ListDedicatedIpPoolsResult",
    "ListDeliverabilityTestReportsResult",
    "ListDomainDeliverabilityCampaignsResult",
    "ListExportJobsResult",
    "ListMultiRegionEndpointsResult",
    "ListRecommendationsResult",
    "ListReputationEntitiesResult",
    "ListResourceTenantsResult",
    "ListSuppressedDestinationsResult",
    "ListTagsForResourceResult",
    "ListTenantResourcesResult",
    "ListTenantsResult",
    "MessageInsightResult",
    "PutEmailIdentityDkimSigningAttributesResult",
    "RunRenderEmailTemplateResult",
    "SendCustomVerificationEmailResult",
    "SendEmailResult",
    "batch_get_metric_data",
    "cancel_export_job",
    "create_configuration_set",
    "create_configuration_set_event_destination",
    "create_contact",
    "create_contact_list",
    "create_custom_verification_email_template",
    "create_dedicated_ip_pool",
    "create_deliverability_test_report",
    "create_email_identity",
    "create_email_identity_policy",
    "create_email_template",
    "create_export_job",
    "create_import_job",
    "create_multi_region_endpoint",
    "create_tenant",
    "create_tenant_resource_association",
    "delete_configuration_set",
    "delete_configuration_set_event_destination",
    "delete_contact",
    "delete_contact_list",
    "delete_custom_verification_email_template",
    "delete_dedicated_ip_pool",
    "delete_email_identity",
    "delete_email_identity_policy",
    "delete_email_template",
    "delete_multi_region_endpoint",
    "delete_suppressed_destination",
    "delete_tenant",
    "delete_tenant_resource_association",
    "get_account",
    "get_blacklist_reports",
    "get_configuration_set",
    "get_configuration_set_event_destinations",
    "get_contact",
    "get_contact_list",
    "get_custom_verification_email_template",
    "get_dedicated_ip",
    "get_dedicated_ip_pool",
    "get_dedicated_ips",
    "get_deliverability_dashboard_options",
    "get_deliverability_test_report",
    "get_domain_deliverability_campaign",
    "get_domain_statistics_report",
    "get_email_identity",
    "get_email_identity_policies",
    "get_email_template",
    "get_export_job",
    "get_import_job",
    "get_message_insights",
    "get_multi_region_endpoint",
    "get_reputation_entity",
    "get_suppressed_destination",
    "get_tenant",
    "list_configuration_sets",
    "list_contact_lists",
    "list_contacts",
    "list_custom_verification_email_templates",
    "list_dedicated_ip_pools",
    "list_deliverability_test_reports",
    "list_domain_deliverability_campaigns",
    "list_email_identities",
    "list_email_templates",
    "list_export_jobs",
    "list_import_jobs",
    "list_multi_region_endpoints",
    "list_recommendations",
    "list_reputation_entities",
    "list_resource_tenants",
    "list_suppressed_destinations",
    "list_tags_for_resource",
    "list_tenant_resources",
    "list_tenants",
    "put_account_dedicated_ip_warmup_attributes",
    "put_account_details",
    "put_account_sending_attributes",
    "put_account_suppression_attributes",
    "put_account_vdm_attributes",
    "put_configuration_set_archiving_options",
    "put_configuration_set_delivery_options",
    "put_configuration_set_reputation_options",
    "put_configuration_set_sending_options",
    "put_configuration_set_suppression_options",
    "put_configuration_set_tracking_options",
    "put_configuration_set_vdm_options",
    "put_dedicated_ip_in_pool",
    "put_dedicated_ip_pool_scaling_attributes",
    "put_dedicated_ip_warmup_attributes",
    "put_deliverability_dashboard_option",
    "put_email_identity_configuration_set_attributes",
    "put_email_identity_dkim_attributes",
    "put_email_identity_dkim_signing_attributes",
    "put_email_identity_feedback_attributes",
    "put_email_identity_mail_from_attributes",
    "put_suppressed_destination",
    "run_render_email_template",
    "send_bulk_email",
    "send_custom_verification_email",
    "send_email",
    "tag_resource",
    "untag_resource",
    "update_configuration_set_event_destination",
    "update_contact",
    "update_contact_list",
    "update_custom_verification_email_template",
    "update_email_identity_policy",
    "update_email_template",
    "update_reputation_entity_customer_managed_status",
    "update_reputation_entity_policy",
]


# ---------------------------------------------------------------------------
# Email sending
# ---------------------------------------------------------------------------


async def send_email(
    from_email_address: str,
    destination: dict[str, list[str]],
    content: dict[str, Any],
    *,
    configuration_set_name: str | None = None,
    email_tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> SendEmailResult:
    """Send an email via SES v2.

    Args:
        from_email_address: Verified sender email address.
        destination: Destination dict, e.g.
            ``{"ToAddresses": ["a@b.com"]}``.
        content: Email content dict containing ``Simple`` or ``Raw`` or
            ``Template`` key as per the SES v2 API.
        configuration_set_name: Optional configuration set name.
        email_tags: Optional message tags.
        region_name: AWS region override.

    Returns:
        A :class:`SendEmailResult` with the assigned message ID.

    Raises:
        RuntimeError: If the send fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "FromEmailAddress": from_email_address,
        "Destination": destination,
        "Content": content,
    }
    if configuration_set_name is not None:
        kwargs["ConfigurationSetName"] = configuration_set_name
    if email_tags is not None:
        kwargs["EmailTags"] = email_tags
    try:
        resp = await client.call("SendEmail", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to send email via SES v2") from exc
    return SendEmailResult(message_id=resp["MessageId"])


async def send_bulk_email(
    from_email_address: str,
    default_content: dict[str, Any],
    bulk_entries: list[dict[str, Any]],
    *,
    configuration_set_name: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Send bulk email via SES v2.

    Args:
        from_email_address: Verified sender email address.
        default_content: Default template content for the bulk operation.
        bulk_entries: List of bulk email entry dicts with ``Destination``
            and optional replacement data.
        configuration_set_name: Optional configuration set name.
        region_name: AWS region override.

    Returns:
        List of per-entry status dicts from the API response.

    Raises:
        RuntimeError: If the bulk send fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "FromEmailAddress": from_email_address,
        "DefaultContent": default_content,
        "BulkEmailEntries": bulk_entries,
    }
    if configuration_set_name is not None:
        kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        resp = await client.call("SendBulkEmail", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to send bulk email via SES v2") from exc
    return resp.get("BulkEmailEntryResults", [])


# ---------------------------------------------------------------------------
# Email identities
# ---------------------------------------------------------------------------


async def create_email_identity(
    identity: str,
    *,
    dkim_signing_attributes: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> EmailIdentityResult:
    """Create an email identity (address or domain) in SES v2.

    Args:
        identity: Email address or domain to verify.
        dkim_signing_attributes: Optional DKIM signing config.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        An :class:`EmailIdentityResult` with identity details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {"EmailIdentity": identity}
    if dkim_signing_attributes is not None:
        kwargs["DkimSigningAttributes"] = dkim_signing_attributes
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateEmailIdentity", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create email identity {identity!r}") from exc
    return EmailIdentityResult(
        identity_name=identity,
        identity_type=resp.get("IdentityType"),
        verified_for_sending=resp.get("VerifiedForSendingStatus", False),
        dkim_signing_enabled=resp.get("DkimAttributes", {}).get("SigningEnabled", False),
        extra=resp.get("DkimAttributes", {}),
    )


async def get_email_identity(
    identity: str,
    *,
    region_name: str | None = None,
) -> EmailIdentityResult:
    """Retrieve details for an email identity.

    Args:
        identity: Email address or domain.
        region_name: AWS region override.

    Returns:
        An :class:`EmailIdentityResult` with identity details.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call("GetEmailIdentity", EmailIdentity=identity)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to get email identity {identity!r}") from exc
    return EmailIdentityResult(
        identity_name=identity,
        identity_type=resp.get("IdentityType"),
        verified_for_sending=resp.get("VerifiedForSendingStatus", False),
        dkim_signing_enabled=resp.get("DkimAttributes", {}).get("SigningEnabled", False),
        extra=resp.get("DkimAttributes", {}),
    )


async def list_email_identities(
    *,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> list[EmailIdentityResult]:
    """List email identities in the SES v2 account.

    Args:
        page_size: Maximum identities to return per call.
        next_token: Pagination token from a previous call.
        region_name: AWS region override.

    Returns:
        A list of :class:`EmailIdentityResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListEmailIdentities", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to list email identities") from exc
    return [
        EmailIdentityResult(
            identity_name=item.get("IdentityName", ""),
            identity_type=item.get("IdentityType"),
            verified_for_sending=item.get("SendingEnabled", False),
        )
        for item in resp.get("EmailIdentities", [])
    ]


async def delete_email_identity(
    identity: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an email identity from SES v2.

    Args:
        identity: Email address or domain to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("sesv2", region_name)
    try:
        await client.call("DeleteEmailIdentity", EmailIdentity=identity)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete email identity {identity!r}") from exc


async def put_email_identity_dkim_attributes(
    identity: str,
    *,
    signing_enabled: bool = True,
    region_name: str | None = None,
) -> None:
    """Enable or disable DKIM signing for an email identity.

    Args:
        identity: Email address or domain.
        signing_enabled: Whether DKIM signing should be enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = async_client("sesv2", region_name)
    try:
        await client.call(
            "PutEmailIdentityDkimAttributes",
            EmailIdentity=identity,
            SigningEnabled=signing_enabled,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to update DKIM attributes for {identity!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Configuration sets
# ---------------------------------------------------------------------------


async def create_configuration_set(
    configuration_set_name: str,
    *,
    sending_options: dict[str, Any] | None = None,
    tracking_options: dict[str, Any] | None = None,
    reputation_options: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ConfigSetResult:
    """Create a configuration set in SES v2.

    Args:
        configuration_set_name: Name of the configuration set.
        sending_options: Sending option overrides.
        tracking_options: Click/open tracking overrides.
        reputation_options: Reputation metric options.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ConfigSetResult`.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "ConfigurationSetName": configuration_set_name,
    }
    if sending_options is not None:
        kwargs["SendingOptions"] = sending_options
    if tracking_options is not None:
        kwargs["TrackingOptions"] = tracking_options
    if reputation_options is not None:
        kwargs["ReputationOptions"] = reputation_options
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateConfigurationSet", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create configuration set {configuration_set_name!r}",
        ) from exc
    return ConfigSetResult(
        configuration_set_name=configuration_set_name,
    )


async def get_configuration_set(
    configuration_set_name: str,
    *,
    region_name: str | None = None,
) -> ConfigSetResult:
    """Get details of a configuration set.

    Args:
        configuration_set_name: Name of the configuration set.
        region_name: AWS region override.

    Returns:
        A :class:`ConfigSetResult`.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call(
            "GetConfigurationSet",
            ConfigurationSetName=configuration_set_name,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to get configuration set {configuration_set_name!r}",
        ) from exc
    sending = resp.get("SendingOptions", {})
    return ConfigSetResult(
        configuration_set_name=resp.get("ConfigurationSetName", configuration_set_name),
        sending_enabled=sending.get("SendingEnabled", True),
        extra=resp.get("TrackingOptions", {}),
    )


async def list_configuration_sets(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> list[str]:
    """List configuration set names in the SES v2 account.

    Args:
        next_token: Pagination token from a previous call.
        page_size: Max results per page.
        region_name: AWS region override.

    Returns:
        A list of configuration set name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListConfigurationSets", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to list configuration sets") from exc
    return resp.get("ConfigurationSets", [])


async def delete_configuration_set(
    configuration_set_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a configuration set from SES v2.

    Args:
        configuration_set_name: Name of the configuration set to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("sesv2", region_name)
    try:
        await client.call(
            "DeleteConfigurationSet",
            ConfigurationSetName=configuration_set_name,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete configuration set {configuration_set_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Email templates
# ---------------------------------------------------------------------------


async def create_email_template(
    template_name: str,
    subject: str,
    *,
    text: str | None = None,
    html: str | None = None,
    region_name: str | None = None,
) -> EmailTemplateResult:
    """Create an email template in SES v2.

    Args:
        template_name: Unique name for the template.
        subject: Subject line template.
        text: Plain-text body template.
        html: HTML body template.
        region_name: AWS region override.

    Returns:
        An :class:`EmailTemplateResult`.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    content: dict[str, str] = {"Subject": subject}
    if text is not None:
        content["Text"] = text
    if html is not None:
        content["Html"] = html
    try:
        await client.call(
            "CreateEmailTemplate",
            TemplateName=template_name,
            TemplateContent=content,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create email template {template_name!r}") from exc
    return EmailTemplateResult(
        template_name=template_name,
        subject=subject,
        text=text,
        html=html,
    )


async def get_email_template(
    template_name: str,
    *,
    region_name: str | None = None,
) -> EmailTemplateResult:
    """Retrieve an email template by name.

    Args:
        template_name: The template name.
        region_name: AWS region override.

    Returns:
        An :class:`EmailTemplateResult`.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call("GetEmailTemplate", TemplateName=template_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to get email template {template_name!r}") from exc
    content = resp.get("TemplateContent", {})
    return EmailTemplateResult(
        template_name=resp.get("TemplateName", template_name),
        subject=content.get("Subject"),
        text=content.get("Text"),
        html=content.get("Html"),
    )


async def list_email_templates(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> list[str]:
    """List email template names in the SES v2 account.

    Args:
        next_token: Pagination token.
        page_size: Max results per page.
        region_name: AWS region override.

    Returns:
        A list of template name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListEmailTemplates", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to list email templates") from exc
    return [t.get("TemplateName", "") for t in resp.get("TemplatesMetadata", [])]


async def update_email_template(
    template_name: str,
    subject: str,
    *,
    text: str | None = None,
    html: str | None = None,
    region_name: str | None = None,
) -> EmailTemplateResult:
    """Update an existing email template.

    Args:
        template_name: The template name to update.
        subject: New subject line template.
        text: New plain-text body template.
        html: New HTML body template.
        region_name: AWS region override.

    Returns:
        An :class:`EmailTemplateResult` with the updated data.

    Raises:
        RuntimeError: If the update fails.
    """
    client = async_client("sesv2", region_name)
    content: dict[str, str] = {"Subject": subject}
    if text is not None:
        content["Text"] = text
    if html is not None:
        content["Html"] = html
    try:
        await client.call(
            "UpdateEmailTemplate",
            TemplateName=template_name,
            TemplateContent=content,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to update email template {template_name!r}") from exc
    return EmailTemplateResult(
        template_name=template_name,
        subject=subject,
        text=text,
        html=html,
    )


async def delete_email_template(
    template_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an email template from SES v2.

    Args:
        template_name: The template name to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("sesv2", region_name)
    try:
        await client.call("DeleteEmailTemplate", TemplateName=template_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete email template {template_name!r}") from exc


# ---------------------------------------------------------------------------
# Contact lists & contacts
# ---------------------------------------------------------------------------


async def create_contact_list(
    contact_list_name: str,
    *,
    description: str | None = None,
    topics: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ContactListResult:
    """Create a contact list in SES v2.

    Args:
        contact_list_name: Unique contact list name.
        description: Optional description.
        topics: Optional topic preferences definitions.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ContactListResult`.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "ContactListName": contact_list_name,
    }
    if description is not None:
        kwargs["Description"] = description
    if topics is not None:
        kwargs["Topics"] = topics
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateContactList", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create contact list {contact_list_name!r}",
        ) from exc
    return ContactListResult(
        contact_list_name=contact_list_name,
        description=description,
    )


async def get_contact_list(
    contact_list_name: str,
    *,
    region_name: str | None = None,
) -> ContactListResult:
    """Get details of a contact list.

    Args:
        contact_list_name: Name of the contact list.
        region_name: AWS region override.

    Returns:
        A :class:`ContactListResult`.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call("GetContactList", ContactListName=contact_list_name)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to get contact list {contact_list_name!r}",
        ) from exc
    return ContactListResult(
        contact_list_name=resp.get("ContactListName", contact_list_name),
        description=resp.get("Description"),
        extra={k: v for k, v in resp.items() if k not in {"ContactListName", "Description"}},
    )


async def list_contact_lists(
    *,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> list[ContactListResult]:
    """List contact lists in the SES v2 account.

    Args:
        page_size: Max results per page.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A list of :class:`ContactListResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListContactLists", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to list contact lists") from exc
    return [
        ContactListResult(
            contact_list_name=item.get("ContactListName", ""),
        )
        for item in resp.get("ContactLists", [])
    ]


async def create_contact(
    contact_list_name: str,
    email_address: str,
    *,
    topic_preferences: list[dict[str, Any]] | None = None,
    unsubscribe_all: bool = False,
    region_name: str | None = None,
) -> ContactResult:
    """Add a contact to a contact list.

    Args:
        contact_list_name: Name of the contact list.
        email_address: Contact email address.
        topic_preferences: Optional topic preference overrides.
        unsubscribe_all: Whether the contact is globally unsubscribed.
        region_name: AWS region override.

    Returns:
        A :class:`ContactResult`.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "ContactListName": contact_list_name,
        "EmailAddress": email_address,
        "UnsubscribeAll": unsubscribe_all,
    }
    if topic_preferences is not None:
        kwargs["TopicPreferences"] = topic_preferences
    try:
        await client.call("CreateContact", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create contact {email_address!r} in {contact_list_name!r}",
        ) from exc
    return ContactResult(
        email_address=email_address,
        unsubscribe_all=unsubscribe_all,
        topic_preferences=topic_preferences or [],
    )


async def get_contact(
    contact_list_name: str,
    email_address: str,
    *,
    region_name: str | None = None,
) -> ContactResult:
    """Get details of a contact in a contact list.

    Args:
        contact_list_name: Name of the contact list.
        email_address: Contact email address.
        region_name: AWS region override.

    Returns:
        A :class:`ContactResult`.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call(
            "GetContact",
            ContactListName=contact_list_name,
            EmailAddress=email_address,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to get contact {email_address!r} from {contact_list_name!r}",
        ) from exc
    return ContactResult(
        email_address=resp.get("EmailAddress", email_address),
        unsubscribe_all=resp.get("UnsubscribeAll", False),
        topic_preferences=resp.get("TopicPreferences", []),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "EmailAddress",
                "UnsubscribeAll",
                "TopicPreferences",
            }
        },
    )


async def list_contacts(
    contact_list_name: str,
    *,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> list[ContactResult]:
    """List contacts in a contact list.

    Args:
        contact_list_name: Name of the contact list.
        page_size: Max results per page.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A list of :class:`ContactResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "ContactListName": contact_list_name,
    }
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListContacts", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to list contacts in {contact_list_name!r}",
        ) from exc
    return [
        ContactResult(
            email_address=item.get("EmailAddress", ""),
            unsubscribe_all=item.get("UnsubscribeAll", False),
            topic_preferences=item.get("TopicPreferences", []),
        )
        for item in resp.get("Contacts", [])
    ]


async def update_contact(
    contact_list_name: str,
    email_address: str,
    *,
    topic_preferences: list[dict[str, Any]] | None = None,
    unsubscribe_all: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update a contact's preferences.

    Args:
        contact_list_name: Name of the contact list.
        email_address: Contact email address.
        topic_preferences: New topic preferences.
        unsubscribe_all: Whether the contact is globally unsubscribed.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {
        "ContactListName": contact_list_name,
        "EmailAddress": email_address,
    }
    if topic_preferences is not None:
        kwargs["TopicPreferences"] = topic_preferences
    if unsubscribe_all is not None:
        kwargs["UnsubscribeAll"] = unsubscribe_all
    try:
        await client.call("UpdateContact", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to update contact {email_address!r} in {contact_list_name!r}",
        ) from exc


async def delete_contact(
    contact_list_name: str,
    email_address: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a contact from a contact list.

    Args:
        contact_list_name: Name of the contact list.
        email_address: Contact email address to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("sesv2", region_name)
    try:
        await client.call(
            "DeleteContact",
            ContactListName=contact_list_name,
            EmailAddress=email_address,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete contact {email_address!r} from {contact_list_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Import / export jobs
# ---------------------------------------------------------------------------


async def create_import_job(
    import_destination: dict[str, Any],
    import_data_source: dict[str, Any],
    *,
    region_name: str | None = None,
) -> ImportJobResult:
    """Create an import job in SES v2.

    Args:
        import_destination: Destination configuration dict.
        import_data_source: Data source configuration dict.
        region_name: AWS region override.

    Returns:
        An :class:`ImportJobResult` with the job ID.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call(
            "CreateImportJob",
            ImportDestination=import_destination,
            ImportDataSource=import_data_source,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to create import job") from exc
    return ImportJobResult(job_id=resp.get("JobId", ""))


async def get_import_job(
    job_id: str,
    *,
    region_name: str | None = None,
) -> ImportJobResult:
    """Get details of an import job.

    Args:
        job_id: The import job ID.
        region_name: AWS region override.

    Returns:
        An :class:`ImportJobResult`.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call("GetImportJob", JobId=job_id)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to get import job {job_id!r}") from exc
    return ImportJobResult(
        job_id=resp.get("JobId", job_id),
        job_status=resp.get("JobStatus"),
        extra={k: v for k, v in resp.items() if k not in {"JobId", "JobStatus"}},
    )


async def list_import_jobs(
    *,
    import_destination_type: str | None = None,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> list[ImportJobResult]:
    """List import jobs in the SES v2 account.

    Args:
        import_destination_type: Optional filter
            (e.g. ``"SUPPRESSION_LIST"``).
        next_token: Pagination token.
        page_size: Max results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`ImportJobResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if import_destination_type is not None:
        kwargs["ImportDestinationType"] = import_destination_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListImportJobs", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to list import jobs") from exc
    return [
        ImportJobResult(
            job_id=item.get("JobId", ""),
            job_status=item.get("JobStatus"),
        )
        for item in resp.get("ImportJobs", [])
    ]


async def create_export_job(
    export_destination: dict[str, Any],
    export_data_source: dict[str, Any],
    *,
    region_name: str | None = None,
) -> str:
    """Create an export job in SES v2.

    Args:
        export_destination: Export destination config.
        export_data_source: Data source config.
        region_name: AWS region override.

    Returns:
        The export job ID string.

    Raises:
        RuntimeError: If creation fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call(
            "CreateExportJob",
            ExportDestination=export_destination,
            ExportDataSource=export_data_source,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to create export job") from exc
    return resp.get("JobId", "")


# ---------------------------------------------------------------------------
# Message insights
# ---------------------------------------------------------------------------


async def get_message_insights(
    message_id: str,
    *,
    region_name: str | None = None,
) -> MessageInsightResult:
    """Get delivery/engagement insights for a sent message.

    Args:
        message_id: The SES message ID.
        region_name: AWS region override.

    Returns:
        A :class:`MessageInsightResult` with delivery details.

    Raises:
        RuntimeError: If the lookup fails.
    """
    client = async_client("sesv2", region_name)
    try:
        resp = await client.call("GetMessageInsights", MessageId=message_id)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to get message insights for {message_id!r}",
        ) from exc
    return MessageInsightResult(
        message_id=resp.get("MessageId", message_id),
        subject=resp.get("Subject"),
        from_email_address=resp.get("FromEmailAddress"),
        insights=resp.get("Insights", []),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "MessageId",
                "Subject",
                "FromEmailAddress",
                "Insights",
            }
        },
    )


async def batch_get_metric_data(
    queries: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetMetricDataResult:
    """Batch get metric data.

    Args:
        queries: Queries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Queries"] = queries
    try:
        resp = await client.call("BatchGetMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get metric data") from exc
    return BatchGetMetricDataResult(
        results=resp.get("Results"),
        errors=resp.get("Errors"),
    )


async def cancel_export_job(
    job_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel export job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        await client.call("CancelExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel export job") from exc
    return None


async def create_configuration_set_event_destination(
    configuration_set_name: str,
    event_destination_name: str,
    event_destination: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create configuration set event destination.

    Args:
        configuration_set_name: Configuration set name.
        event_destination_name: Event destination name.
        event_destination: Event destination.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestinationName"] = event_destination_name
    kwargs["EventDestination"] = event_destination
    try:
        await client.call("CreateConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create configuration set event destination") from exc
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
    client = async_client("sesv2", region_name)
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


async def create_dedicated_ip_pool(
    pool_name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    scaling_mode: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create dedicated ip pool.

    Args:
        pool_name: Pool name.
        tags: Tags.
        scaling_mode: Scaling mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    if tags is not None:
        kwargs["Tags"] = tags
    if scaling_mode is not None:
        kwargs["ScalingMode"] = scaling_mode
    try:
        await client.call("CreateDedicatedIpPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dedicated ip pool") from exc
    return None


async def create_deliverability_test_report(
    from_email_address: str,
    content: dict[str, Any],
    *,
    report_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDeliverabilityTestReportResult:
    """Create deliverability test report.

    Args:
        from_email_address: From email address.
        content: Content.
        report_name: Report name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FromEmailAddress"] = from_email_address
    kwargs["Content"] = content
    if report_name is not None:
        kwargs["ReportName"] = report_name
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDeliverabilityTestReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create deliverability test report") from exc
    return CreateDeliverabilityTestReportResult(
        report_id=resp.get("ReportId"),
        deliverability_test_status=resp.get("DeliverabilityTestStatus"),
    )


async def create_email_identity_policy(
    email_identity: str,
    policy_name: str,
    policy: str,
    region_name: str | None = None,
) -> None:
    """Create email identity policy.

    Args:
        email_identity: Email identity.
        policy_name: Policy name.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    kwargs["PolicyName"] = policy_name
    kwargs["Policy"] = policy
    try:
        await client.call("CreateEmailIdentityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create email identity policy") from exc
    return None


async def create_multi_region_endpoint(
    endpoint_name: str,
    details: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMultiRegionEndpointResult:
    """Create multi region endpoint.

    Args:
        endpoint_name: Endpoint name.
        details: Details.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    kwargs["Details"] = details
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateMultiRegionEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create multi region endpoint") from exc
    return CreateMultiRegionEndpointResult(
        status=resp.get("Status"),
        endpoint_id=resp.get("EndpointId"),
    )


async def create_tenant(
    tenant_name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTenantResult:
    """Create tenant.

    Args:
        tenant_name: Tenant name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create tenant") from exc
    return CreateTenantResult(
        tenant_name=resp.get("TenantName"),
        tenant_id=resp.get("TenantId"),
        tenant_arn=resp.get("TenantArn"),
        created_timestamp=resp.get("CreatedTimestamp"),
        tags=resp.get("Tags"),
        sending_status=resp.get("SendingStatus"),
    )


async def create_tenant_resource_association(
    tenant_name: str,
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Create tenant resource association.

    Args:
        tenant_name: Tenant name.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("CreateTenantResourceAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create tenant resource association") from exc
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestinationName"] = event_destination_name
    try:
        await client.call("DeleteConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration set event destination") from exc
    return None


async def delete_contact_list(
    contact_list_name: str,
    region_name: str | None = None,
) -> None:
    """Delete contact list.

    Args:
        contact_list_name: Contact list name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactListName"] = contact_list_name
    try:
        await client.call("DeleteContactList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete contact list") from exc
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    try:
        await client.call("DeleteCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom verification email template") from exc
    return None


async def delete_dedicated_ip_pool(
    pool_name: str,
    region_name: str | None = None,
) -> None:
    """Delete dedicated ip pool.

    Args:
        pool_name: Pool name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    try:
        await client.call("DeleteDedicatedIpPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dedicated ip pool") from exc
    return None


async def delete_email_identity_policy(
    email_identity: str,
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete email identity policy.

    Args:
        email_identity: Email identity.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    kwargs["PolicyName"] = policy_name
    try:
        await client.call("DeleteEmailIdentityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete email identity policy") from exc
    return None


async def delete_multi_region_endpoint(
    endpoint_name: str,
    region_name: str | None = None,
) -> DeleteMultiRegionEndpointResult:
    """Delete multi region endpoint.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    try:
        resp = await client.call("DeleteMultiRegionEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete multi region endpoint") from exc
    return DeleteMultiRegionEndpointResult(
        status=resp.get("Status"),
    )


async def delete_suppressed_destination(
    email_address: str,
    region_name: str | None = None,
) -> None:
    """Delete suppressed destination.

    Args:
        email_address: Email address.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    try:
        await client.call("DeleteSuppressedDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete suppressed destination") from exc
    return None


async def delete_tenant(
    tenant_name: str,
    region_name: str | None = None,
) -> None:
    """Delete tenant.

    Args:
        tenant_name: Tenant name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    try:
        await client.call("DeleteTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete tenant") from exc
    return None


async def delete_tenant_resource_association(
    tenant_name: str,
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete tenant resource association.

    Args:
        tenant_name: Tenant name.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteTenantResourceAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete tenant resource association") from exc
    return None


async def get_account(
    region_name: str | None = None,
) -> GetAccountResult:
    """Get account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account") from exc
    return GetAccountResult(
        dedicated_ip_auto_warmup_enabled=resp.get("DedicatedIpAutoWarmupEnabled"),
        enforcement_status=resp.get("EnforcementStatus"),
        production_access_enabled=resp.get("ProductionAccessEnabled"),
        send_quota=resp.get("SendQuota"),
        sending_enabled=resp.get("SendingEnabled"),
        suppression_attributes=resp.get("SuppressionAttributes"),
        details=resp.get("Details"),
        vdm_attributes=resp.get("VdmAttributes"),
    )


async def get_blacklist_reports(
    blacklist_item_names: list[str],
    region_name: str | None = None,
) -> GetBlacklistReportsResult:
    """Get blacklist reports.

    Args:
        blacklist_item_names: Blacklist item names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlacklistItemNames"] = blacklist_item_names
    try:
        resp = await client.call("GetBlacklistReports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get blacklist reports") from exc
    return GetBlacklistReportsResult(
        blacklist_report=resp.get("BlacklistReport"),
    )


async def get_configuration_set_event_destinations(
    configuration_set_name: str,
    region_name: str | None = None,
) -> GetConfigurationSetEventDestinationsResult:
    """Get configuration set event destinations.

    Args:
        configuration_set_name: Configuration set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        resp = await client.call("GetConfigurationSetEventDestinations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get configuration set event destinations") from exc
    return GetConfigurationSetEventDestinationsResult(
        event_destinations=resp.get("EventDestinations"),
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
    client = async_client("sesv2", region_name)
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


async def get_dedicated_ip(
    ip: str,
    region_name: str | None = None,
) -> GetDedicatedIpResult:
    """Get dedicated ip.

    Args:
        ip: Ip.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Ip"] = ip
    try:
        resp = await client.call("GetDedicatedIp", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dedicated ip") from exc
    return GetDedicatedIpResult(
        dedicated_ip=resp.get("DedicatedIp"),
    )


async def get_dedicated_ip_pool(
    pool_name: str,
    region_name: str | None = None,
) -> GetDedicatedIpPoolResult:
    """Get dedicated ip pool.

    Args:
        pool_name: Pool name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    try:
        resp = await client.call("GetDedicatedIpPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dedicated ip pool") from exc
    return GetDedicatedIpPoolResult(
        dedicated_ip_pool=resp.get("DedicatedIpPool"),
    )


async def get_dedicated_ips(
    *,
    pool_name: str | None = None,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> GetDedicatedIpsResult:
    """Get dedicated ips.

    Args:
        pool_name: Pool name.
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if pool_name is not None:
        kwargs["PoolName"] = pool_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("GetDedicatedIps", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dedicated ips") from exc
    return GetDedicatedIpsResult(
        dedicated_ips=resp.get("DedicatedIps"),
        next_token=resp.get("NextToken"),
    )


async def get_deliverability_dashboard_options(
    region_name: str | None = None,
) -> GetDeliverabilityDashboardOptionsResult:
    """Get deliverability dashboard options.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetDeliverabilityDashboardOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get deliverability dashboard options") from exc
    return GetDeliverabilityDashboardOptionsResult(
        dashboard_enabled=resp.get("DashboardEnabled"),
        subscription_expiry_date=resp.get("SubscriptionExpiryDate"),
        account_status=resp.get("AccountStatus"),
        active_subscribed_domains=resp.get("ActiveSubscribedDomains"),
        pending_expiration_subscribed_domains=resp.get("PendingExpirationSubscribedDomains"),
    )


async def get_deliverability_test_report(
    report_id: str,
    region_name: str | None = None,
) -> GetDeliverabilityTestReportResult:
    """Get deliverability test report.

    Args:
        report_id: Report id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReportId"] = report_id
    try:
        resp = await client.call("GetDeliverabilityTestReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get deliverability test report") from exc
    return GetDeliverabilityTestReportResult(
        deliverability_test_report=resp.get("DeliverabilityTestReport"),
        overall_placement=resp.get("OverallPlacement"),
        isp_placements=resp.get("IspPlacements"),
        message=resp.get("Message"),
        tags=resp.get("Tags"),
    )


async def get_domain_deliverability_campaign(
    campaign_id: str,
    region_name: str | None = None,
) -> GetDomainDeliverabilityCampaignResult:
    """Get domain deliverability campaign.

    Args:
        campaign_id: Campaign id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CampaignId"] = campaign_id
    try:
        resp = await client.call("GetDomainDeliverabilityCampaign", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain deliverability campaign") from exc
    return GetDomainDeliverabilityCampaignResult(
        domain_deliverability_campaign=resp.get("DomainDeliverabilityCampaign"),
    )


async def get_domain_statistics_report(
    domain: str,
    start_date: str,
    end_date: str,
    region_name: str | None = None,
) -> GetDomainStatisticsReportResult:
    """Get domain statistics report.

    Args:
        domain: Domain.
        start_date: Start date.
        end_date: End date.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["StartDate"] = start_date
    kwargs["EndDate"] = end_date
    try:
        resp = await client.call("GetDomainStatisticsReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain statistics report") from exc
    return GetDomainStatisticsReportResult(
        overall_volume=resp.get("OverallVolume"),
        daily_volumes=resp.get("DailyVolumes"),
    )


async def get_email_identity_policies(
    email_identity: str,
    region_name: str | None = None,
) -> GetEmailIdentityPoliciesResult:
    """Get email identity policies.

    Args:
        email_identity: Email identity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    try:
        resp = await client.call("GetEmailIdentityPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get email identity policies") from exc
    return GetEmailIdentityPoliciesResult(
        policies=resp.get("Policies"),
    )


async def get_export_job(
    job_id: str,
    region_name: str | None = None,
) -> GetExportJobResult:
    """Get export job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    try:
        resp = await client.call("GetExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get export job") from exc
    return GetExportJobResult(
        job_id=resp.get("JobId"),
        export_source_type=resp.get("ExportSourceType"),
        job_status=resp.get("JobStatus"),
        export_destination=resp.get("ExportDestination"),
        export_data_source=resp.get("ExportDataSource"),
        created_timestamp=resp.get("CreatedTimestamp"),
        completed_timestamp=resp.get("CompletedTimestamp"),
        failure_info=resp.get("FailureInfo"),
        statistics=resp.get("Statistics"),
    )


async def get_multi_region_endpoint(
    endpoint_name: str,
    region_name: str | None = None,
) -> GetMultiRegionEndpointResult:
    """Get multi region endpoint.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    try:
        resp = await client.call("GetMultiRegionEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get multi region endpoint") from exc
    return GetMultiRegionEndpointResult(
        endpoint_name=resp.get("EndpointName"),
        endpoint_id=resp.get("EndpointId"),
        routes=resp.get("Routes"),
        status=resp.get("Status"),
        created_timestamp=resp.get("CreatedTimestamp"),
        last_updated_timestamp=resp.get("LastUpdatedTimestamp"),
    )


async def get_reputation_entity(
    reputation_entity_reference: str,
    reputation_entity_type: str,
    region_name: str | None = None,
) -> GetReputationEntityResult:
    """Get reputation entity.

    Args:
        reputation_entity_reference: Reputation entity reference.
        reputation_entity_type: Reputation entity type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReputationEntityReference"] = reputation_entity_reference
    kwargs["ReputationEntityType"] = reputation_entity_type
    try:
        resp = await client.call("GetReputationEntity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get reputation entity") from exc
    return GetReputationEntityResult(
        reputation_entity=resp.get("ReputationEntity"),
    )


async def get_suppressed_destination(
    email_address: str,
    region_name: str | None = None,
) -> GetSuppressedDestinationResult:
    """Get suppressed destination.

    Args:
        email_address: Email address.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    try:
        resp = await client.call("GetSuppressedDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get suppressed destination") from exc
    return GetSuppressedDestinationResult(
        suppressed_destination=resp.get("SuppressedDestination"),
    )


async def get_tenant(
    tenant_name: str,
    region_name: str | None = None,
) -> GetTenantResult:
    """Get tenant.

    Args:
        tenant_name: Tenant name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    try:
        resp = await client.call("GetTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get tenant") from exc
    return GetTenantResult(
        tenant=resp.get("Tenant"),
    )


async def list_custom_verification_email_templates(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListCustomVerificationEmailTemplatesResult:
    """List custom verification email templates.

    Args:
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListCustomVerificationEmailTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom verification email templates") from exc
    return ListCustomVerificationEmailTemplatesResult(
        custom_verification_email_templates=resp.get("CustomVerificationEmailTemplates"),
        next_token=resp.get("NextToken"),
    )


async def list_dedicated_ip_pools(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListDedicatedIpPoolsResult:
    """List dedicated ip pools.

    Args:
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListDedicatedIpPools", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dedicated ip pools") from exc
    return ListDedicatedIpPoolsResult(
        dedicated_ip_pools=resp.get("DedicatedIpPools"),
        next_token=resp.get("NextToken"),
    )


async def list_deliverability_test_reports(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListDeliverabilityTestReportsResult:
    """List deliverability test reports.

    Args:
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListDeliverabilityTestReports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list deliverability test reports") from exc
    return ListDeliverabilityTestReportsResult(
        deliverability_test_reports=resp.get("DeliverabilityTestReports"),
        next_token=resp.get("NextToken"),
    )


async def list_domain_deliverability_campaigns(
    start_date: str,
    end_date: str,
    subscribed_domain: str,
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListDomainDeliverabilityCampaignsResult:
    """List domain deliverability campaigns.

    Args:
        start_date: Start date.
        end_date: End date.
        subscribed_domain: Subscribed domain.
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StartDate"] = start_date
    kwargs["EndDate"] = end_date
    kwargs["SubscribedDomain"] = subscribed_domain
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListDomainDeliverabilityCampaigns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list domain deliverability campaigns") from exc
    return ListDomainDeliverabilityCampaignsResult(
        domain_deliverability_campaigns=resp.get("DomainDeliverabilityCampaigns"),
        next_token=resp.get("NextToken"),
    )


async def list_export_jobs(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    export_source_type: str | None = None,
    job_status: str | None = None,
    region_name: str | None = None,
) -> ListExportJobsResult:
    """List export jobs.

    Args:
        next_token: Next token.
        page_size: Page size.
        export_source_type: Export source type.
        job_status: Job status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if export_source_type is not None:
        kwargs["ExportSourceType"] = export_source_type
    if job_status is not None:
        kwargs["JobStatus"] = job_status
    try:
        resp = await client.call("ListExportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list export jobs") from exc
    return ListExportJobsResult(
        export_jobs=resp.get("ExportJobs"),
        next_token=resp.get("NextToken"),
    )


async def list_multi_region_endpoints(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListMultiRegionEndpointsResult:
    """List multi region endpoints.

    Args:
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListMultiRegionEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list multi region endpoints") from exc
    return ListMultiRegionEndpointsResult(
        multi_region_endpoints=resp.get("MultiRegionEndpoints"),
        next_token=resp.get("NextToken"),
    )


async def list_recommendations(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListRecommendationsResult:
    """List recommendations.

    Args:
        filter: Filter.
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recommendations") from exc
    return ListRecommendationsResult(
        recommendations=resp.get("Recommendations"),
        next_token=resp.get("NextToken"),
    )


async def list_reputation_entities(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListReputationEntitiesResult:
    """List reputation entities.

    Args:
        filter: Filter.
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListReputationEntities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list reputation entities") from exc
    return ListReputationEntitiesResult(
        reputation_entities=resp.get("ReputationEntities"),
        next_token=resp.get("NextToken"),
    )


async def list_resource_tenants(
    resource_arn: str,
    *,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceTenantsResult:
    """List resource tenants.

    Args:
        resource_arn: Resource arn.
        page_size: Page size.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListResourceTenants", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list resource tenants") from exc
    return ListResourceTenantsResult(
        resource_tenants=resp.get("ResourceTenants"),
        next_token=resp.get("NextToken"),
    )


async def list_suppressed_destinations(
    *,
    reasons: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListSuppressedDestinationsResult:
    """List suppressed destinations.

    Args:
        reasons: Reasons.
        start_date: Start date.
        end_date: End date.
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if reasons is not None:
        kwargs["Reasons"] = reasons
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListSuppressedDestinations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list suppressed destinations") from exc
    return ListSuppressedDestinationsResult(
        suppressed_destination_summaries=resp.get("SuppressedDestinationSummaries"),
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_tenant_resources(
    tenant_name: str,
    *,
    filter: dict[str, Any] | None = None,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTenantResourcesResult:
    """List tenant resources.

    Args:
        tenant_name: Tenant name.
        filter: Filter.
        page_size: Page size.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TenantName"] = tenant_name
    if filter is not None:
        kwargs["Filter"] = filter
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTenantResources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tenant resources") from exc
    return ListTenantResourcesResult(
        tenant_resources=resp.get("TenantResources"),
        next_token=resp.get("NextToken"),
    )


async def list_tenants(
    *,
    next_token: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListTenantsResult:
    """List tenants.

    Args:
        next_token: Next token.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("ListTenants", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tenants") from exc
    return ListTenantsResult(
        tenants=resp.get("Tenants"),
        next_token=resp.get("NextToken"),
    )


async def put_account_dedicated_ip_warmup_attributes(
    *,
    auto_warmup_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put account dedicated ip warmup attributes.

    Args:
        auto_warmup_enabled: Auto warmup enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if auto_warmup_enabled is not None:
        kwargs["AutoWarmupEnabled"] = auto_warmup_enabled
    try:
        await client.call("PutAccountDedicatedIpWarmupAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account dedicated ip warmup attributes") from exc
    return None


async def put_account_details(
    mail_type: str,
    website_url: str,
    *,
    contact_language: str | None = None,
    use_case_description: str | None = None,
    additional_contact_email_addresses: list[str] | None = None,
    production_access_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put account details.

    Args:
        mail_type: Mail type.
        website_url: Website url.
        contact_language: Contact language.
        use_case_description: Use case description.
        additional_contact_email_addresses: Additional contact email addresses.
        production_access_enabled: Production access enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MailType"] = mail_type
    kwargs["WebsiteURL"] = website_url
    if contact_language is not None:
        kwargs["ContactLanguage"] = contact_language
    if use_case_description is not None:
        kwargs["UseCaseDescription"] = use_case_description
    if additional_contact_email_addresses is not None:
        kwargs["AdditionalContactEmailAddresses"] = additional_contact_email_addresses
    if production_access_enabled is not None:
        kwargs["ProductionAccessEnabled"] = production_access_enabled
    try:
        await client.call("PutAccountDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account details") from exc
    return None


async def put_account_sending_attributes(
    *,
    sending_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put account sending attributes.

    Args:
        sending_enabled: Sending enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if sending_enabled is not None:
        kwargs["SendingEnabled"] = sending_enabled
    try:
        await client.call("PutAccountSendingAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account sending attributes") from exc
    return None


async def put_account_suppression_attributes(
    *,
    suppressed_reasons: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Put account suppression attributes.

    Args:
        suppressed_reasons: Suppressed reasons.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    if suppressed_reasons is not None:
        kwargs["SuppressedReasons"] = suppressed_reasons
    try:
        await client.call("PutAccountSuppressionAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account suppression attributes") from exc
    return None


async def put_account_vdm_attributes(
    vdm_attributes: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put account vdm attributes.

    Args:
        vdm_attributes: Vdm attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VdmAttributes"] = vdm_attributes
    try:
        await client.call("PutAccountVdmAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account vdm attributes") from exc
    return None


async def put_configuration_set_archiving_options(
    configuration_set_name: str,
    *,
    archive_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set archiving options.

    Args:
        configuration_set_name: Configuration set name.
        archive_arn: Archive arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if archive_arn is not None:
        kwargs["ArchiveArn"] = archive_arn
    try:
        await client.call("PutConfigurationSetArchivingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set archiving options") from exc
    return None


async def put_configuration_set_delivery_options(
    configuration_set_name: str,
    *,
    tls_policy: str | None = None,
    sending_pool_name: str | None = None,
    max_delivery_seconds: int | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set delivery options.

    Args:
        configuration_set_name: Configuration set name.
        tls_policy: Tls policy.
        sending_pool_name: Sending pool name.
        max_delivery_seconds: Max delivery seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if tls_policy is not None:
        kwargs["TlsPolicy"] = tls_policy
    if sending_pool_name is not None:
        kwargs["SendingPoolName"] = sending_pool_name
    if max_delivery_seconds is not None:
        kwargs["MaxDeliverySeconds"] = max_delivery_seconds
    try:
        await client.call("PutConfigurationSetDeliveryOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set delivery options") from exc
    return None


async def put_configuration_set_reputation_options(
    configuration_set_name: str,
    *,
    reputation_metrics_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set reputation options.

    Args:
        configuration_set_name: Configuration set name.
        reputation_metrics_enabled: Reputation metrics enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if reputation_metrics_enabled is not None:
        kwargs["ReputationMetricsEnabled"] = reputation_metrics_enabled
    try:
        await client.call("PutConfigurationSetReputationOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set reputation options") from exc
    return None


async def put_configuration_set_sending_options(
    configuration_set_name: str,
    *,
    sending_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set sending options.

    Args:
        configuration_set_name: Configuration set name.
        sending_enabled: Sending enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if sending_enabled is not None:
        kwargs["SendingEnabled"] = sending_enabled
    try:
        await client.call("PutConfigurationSetSendingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set sending options") from exc
    return None


async def put_configuration_set_suppression_options(
    configuration_set_name: str,
    *,
    suppressed_reasons: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set suppression options.

    Args:
        configuration_set_name: Configuration set name.
        suppressed_reasons: Suppressed reasons.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if suppressed_reasons is not None:
        kwargs["SuppressedReasons"] = suppressed_reasons
    try:
        await client.call("PutConfigurationSetSuppressionOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set suppression options") from exc
    return None


async def put_configuration_set_tracking_options(
    configuration_set_name: str,
    *,
    custom_redirect_domain: str | None = None,
    https_policy: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set tracking options.

    Args:
        configuration_set_name: Configuration set name.
        custom_redirect_domain: Custom redirect domain.
        https_policy: Https policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if custom_redirect_domain is not None:
        kwargs["CustomRedirectDomain"] = custom_redirect_domain
    if https_policy is not None:
        kwargs["HttpsPolicy"] = https_policy
    try:
        await client.call("PutConfigurationSetTrackingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set tracking options") from exc
    return None


async def put_configuration_set_vdm_options(
    configuration_set_name: str,
    *,
    vdm_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put configuration set vdm options.

    Args:
        configuration_set_name: Configuration set name.
        vdm_options: Vdm options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    if vdm_options is not None:
        kwargs["VdmOptions"] = vdm_options
    try:
        await client.call("PutConfigurationSetVdmOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put configuration set vdm options") from exc
    return None


async def put_dedicated_ip_in_pool(
    ip: str,
    destination_pool_name: str,
    region_name: str | None = None,
) -> None:
    """Put dedicated ip in pool.

    Args:
        ip: Ip.
        destination_pool_name: Destination pool name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Ip"] = ip
    kwargs["DestinationPoolName"] = destination_pool_name
    try:
        await client.call("PutDedicatedIpInPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put dedicated ip in pool") from exc
    return None


async def put_dedicated_ip_pool_scaling_attributes(
    pool_name: str,
    scaling_mode: str,
    region_name: str | None = None,
) -> None:
    """Put dedicated ip pool scaling attributes.

    Args:
        pool_name: Pool name.
        scaling_mode: Scaling mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    kwargs["ScalingMode"] = scaling_mode
    try:
        await client.call("PutDedicatedIpPoolScalingAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put dedicated ip pool scaling attributes") from exc
    return None


async def put_dedicated_ip_warmup_attributes(
    ip: str,
    warmup_percentage: int,
    region_name: str | None = None,
) -> None:
    """Put dedicated ip warmup attributes.

    Args:
        ip: Ip.
        warmup_percentage: Warmup percentage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Ip"] = ip
    kwargs["WarmupPercentage"] = warmup_percentage
    try:
        await client.call("PutDedicatedIpWarmupAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put dedicated ip warmup attributes") from exc
    return None


async def put_deliverability_dashboard_option(
    dashboard_enabled: bool,
    *,
    subscribed_domains: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Put deliverability dashboard option.

    Args:
        dashboard_enabled: Dashboard enabled.
        subscribed_domains: Subscribed domains.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardEnabled"] = dashboard_enabled
    if subscribed_domains is not None:
        kwargs["SubscribedDomains"] = subscribed_domains
    try:
        await client.call("PutDeliverabilityDashboardOption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put deliverability dashboard option") from exc
    return None


async def put_email_identity_configuration_set_attributes(
    email_identity: str,
    *,
    configuration_set_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put email identity configuration set attributes.

    Args:
        email_identity: Email identity.
        configuration_set_name: Configuration set name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    if configuration_set_name is not None:
        kwargs["ConfigurationSetName"] = configuration_set_name
    try:
        await client.call("PutEmailIdentityConfigurationSetAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to put email identity configuration set attributes"
        ) from exc
    return None


async def put_email_identity_dkim_signing_attributes(
    email_identity: str,
    signing_attributes_origin: str,
    *,
    signing_attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutEmailIdentityDkimSigningAttributesResult:
    """Put email identity dkim signing attributes.

    Args:
        email_identity: Email identity.
        signing_attributes_origin: Signing attributes origin.
        signing_attributes: Signing attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    kwargs["SigningAttributesOrigin"] = signing_attributes_origin
    if signing_attributes is not None:
        kwargs["SigningAttributes"] = signing_attributes
    try:
        resp = await client.call("PutEmailIdentityDkimSigningAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put email identity dkim signing attributes") from exc
    return PutEmailIdentityDkimSigningAttributesResult(
        dkim_status=resp.get("DkimStatus"),
        dkim_tokens=resp.get("DkimTokens"),
    )


async def put_email_identity_feedback_attributes(
    email_identity: str,
    *,
    email_forwarding_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put email identity feedback attributes.

    Args:
        email_identity: Email identity.
        email_forwarding_enabled: Email forwarding enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    if email_forwarding_enabled is not None:
        kwargs["EmailForwardingEnabled"] = email_forwarding_enabled
    try:
        await client.call("PutEmailIdentityFeedbackAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put email identity feedback attributes") from exc
    return None


async def put_email_identity_mail_from_attributes(
    email_identity: str,
    *,
    mail_from_domain: str | None = None,
    behavior_on_mx_failure: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put email identity mail from attributes.

    Args:
        email_identity: Email identity.
        mail_from_domain: Mail from domain.
        behavior_on_mx_failure: Behavior on mx failure.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    if mail_from_domain is not None:
        kwargs["MailFromDomain"] = mail_from_domain
    if behavior_on_mx_failure is not None:
        kwargs["BehaviorOnMxFailure"] = behavior_on_mx_failure
    try:
        await client.call("PutEmailIdentityMailFromAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put email identity mail from attributes") from exc
    return None


async def put_suppressed_destination(
    email_address: str,
    reason: str,
    region_name: str | None = None,
) -> None:
    """Put suppressed destination.

    Args:
        email_address: Email address.
        reason: Reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddress"] = email_address
    kwargs["Reason"] = reason
    try:
        await client.call("PutSuppressedDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put suppressed destination") from exc
    return None


async def run_render_email_template(
    template_name: str,
    template_data: str,
    region_name: str | None = None,
) -> RunRenderEmailTemplateResult:
    """Run render email template.

    Args:
        template_name: Template name.
        template_data: Template data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    kwargs["TemplateData"] = template_data
    try:
        resp = await client.call("TestRenderEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run render email template") from exc
    return RunRenderEmailTemplateResult(
        rendered_template=resp.get("RenderedTemplate"),
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
    client = async_client("sesv2", region_name)
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_configuration_set_event_destination(
    configuration_set_name: str,
    event_destination_name: str,
    event_destination: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update configuration set event destination.

    Args:
        configuration_set_name: Configuration set name.
        event_destination_name: Event destination name.
        event_destination: Event destination.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationSetName"] = configuration_set_name
    kwargs["EventDestinationName"] = event_destination_name
    kwargs["EventDestination"] = event_destination
    try:
        await client.call("UpdateConfigurationSetEventDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration set event destination") from exc
    return None


async def update_contact_list(
    contact_list_name: str,
    *,
    topics: list[dict[str, Any]] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact list.

    Args:
        contact_list_name: Contact list name.
        topics: Topics.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactListName"] = contact_list_name
    if topics is not None:
        kwargs["Topics"] = topics
    if description is not None:
        kwargs["Description"] = description
    try:
        await client.call("UpdateContactList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update contact list") from exc
    return None


async def update_custom_verification_email_template(
    template_name: str,
    from_email_address: str,
    template_subject: str,
    template_content: str,
    success_redirection_url: str,
    failure_redirection_url: str,
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
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TemplateName"] = template_name
    kwargs["FromEmailAddress"] = from_email_address
    kwargs["TemplateSubject"] = template_subject
    kwargs["TemplateContent"] = template_content
    kwargs["SuccessRedirectionURL"] = success_redirection_url
    kwargs["FailureRedirectionURL"] = failure_redirection_url
    try:
        await client.call("UpdateCustomVerificationEmailTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update custom verification email template") from exc
    return None


async def update_email_identity_policy(
    email_identity: str,
    policy_name: str,
    policy: str,
    region_name: str | None = None,
) -> None:
    """Update email identity policy.

    Args:
        email_identity: Email identity.
        policy_name: Policy name.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailIdentity"] = email_identity
    kwargs["PolicyName"] = policy_name
    kwargs["Policy"] = policy
    try:
        await client.call("UpdateEmailIdentityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update email identity policy") from exc
    return None


async def update_reputation_entity_customer_managed_status(
    reputation_entity_type: str,
    reputation_entity_reference: str,
    sending_status: str,
    region_name: str | None = None,
) -> None:
    """Update reputation entity customer managed status.

    Args:
        reputation_entity_type: Reputation entity type.
        reputation_entity_reference: Reputation entity reference.
        sending_status: Sending status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReputationEntityType"] = reputation_entity_type
    kwargs["ReputationEntityReference"] = reputation_entity_reference
    kwargs["SendingStatus"] = sending_status
    try:
        await client.call("UpdateReputationEntityCustomerManagedStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to update reputation entity customer managed status"
        ) from exc
    return None


async def update_reputation_entity_policy(
    reputation_entity_type: str,
    reputation_entity_reference: str,
    reputation_entity_policy: str,
    region_name: str | None = None,
) -> None:
    """Update reputation entity policy.

    Args:
        reputation_entity_type: Reputation entity type.
        reputation_entity_reference: Reputation entity reference.
        reputation_entity_policy: Reputation entity policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sesv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReputationEntityType"] = reputation_entity_type
    kwargs["ReputationEntityReference"] = reputation_entity_reference
    kwargs["ReputationEntityPolicy"] = reputation_entity_policy
    try:
        await client.call("UpdateReputationEntityPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update reputation entity policy") from exc
    return None
