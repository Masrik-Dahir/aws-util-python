"""Tests for aws_util.aio.ses_v2 — native async SES v2 utilities."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.ses_v2 import (
    ConfigSetResult,
    ContactListResult,
    ContactResult,
    EmailIdentityResult,
    EmailTemplateResult,
    ImportJobResult,
    MessageInsightResult,
    SendEmailResult,
)

import aws_util.aio.ses_v2 as mod
from aws_util.aio.ses_v2 import (
    create_configuration_set,
    create_contact,
    create_contact_list,
    create_email_identity,
    create_email_template,
    create_export_job,
    create_import_job,
    delete_configuration_set,
    delete_contact,
    delete_email_identity,
    delete_email_template,
    get_configuration_set,
    get_contact,
    get_contact_list,
    get_email_identity,
    get_email_template,
    get_import_job,
    get_message_insights,
    list_configuration_sets,
    list_contact_lists,
    list_contacts,
    list_email_identities,
    list_email_templates,
    list_import_jobs,
    put_email_identity_dkim_attributes,
    send_bulk_email,
    send_email,
    update_contact,
    update_email_template,
    batch_get_metric_data,
    cancel_export_job,
    create_configuration_set_event_destination,
    create_custom_verification_email_template,
    create_dedicated_ip_pool,
    create_deliverability_test_report,
    create_email_identity_policy,
    create_multi_region_endpoint,
    create_tenant,
    create_tenant_resource_association,
    delete_configuration_set_event_destination,
    delete_contact_list,
    delete_custom_verification_email_template,
    delete_dedicated_ip_pool,
    delete_email_identity_policy,
    delete_multi_region_endpoint,
    delete_suppressed_destination,
    delete_tenant,
    delete_tenant_resource_association,
    get_account,
    get_blacklist_reports,
    get_configuration_set_event_destinations,
    get_custom_verification_email_template,
    get_dedicated_ip,
    get_dedicated_ip_pool,
    get_dedicated_ips,
    get_deliverability_dashboard_options,
    get_deliverability_test_report,
    get_domain_deliverability_campaign,
    get_domain_statistics_report,
    get_email_identity_policies,
    get_export_job,
    get_multi_region_endpoint,
    get_reputation_entity,
    get_suppressed_destination,
    get_tenant,
    list_custom_verification_email_templates,
    list_dedicated_ip_pools,
    list_deliverability_test_reports,
    list_domain_deliverability_campaigns,
    list_export_jobs,
    list_multi_region_endpoints,
    list_recommendations,
    list_reputation_entities,
    list_resource_tenants,
    list_suppressed_destinations,
    list_tags_for_resource,
    list_tenant_resources,
    list_tenants,
    put_account_dedicated_ip_warmup_attributes,
    put_account_details,
    put_account_sending_attributes,
    put_account_suppression_attributes,
    put_account_vdm_attributes,
    put_configuration_set_archiving_options,
    put_configuration_set_delivery_options,
    put_configuration_set_reputation_options,
    put_configuration_set_sending_options,
    put_configuration_set_suppression_options,
    put_configuration_set_tracking_options,
    put_configuration_set_vdm_options,
    put_dedicated_ip_in_pool,
    put_dedicated_ip_pool_scaling_attributes,
    put_dedicated_ip_warmup_attributes,
    put_deliverability_dashboard_option,
    put_email_identity_configuration_set_attributes,
    put_email_identity_dkim_signing_attributes,
    put_email_identity_feedback_attributes,
    put_email_identity_mail_from_attributes,
    put_suppressed_destination,
    run_render_email_template,
    send_custom_verification_email,
    tag_resource,
    untag_resource,
    update_configuration_set_event_destination,
    update_contact_list,
    update_custom_verification_email_template,
    update_email_identity_policy,
    update_reputation_entity_customer_managed_status,
    update_reputation_entity_policy,
)


REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client(monkeypatch):
    """Replace ``async_client`` so every function gets a mock client."""
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.ses_v2.async_client",
        lambda *a, **kw: client,
    )
    return client


# -----------------------------------------------------------------------
# send_email
# -----------------------------------------------------------------------


async def test_send_email_basic(mock_client):
    mock_client.call.return_value = {"MessageId": "m1"}
    r = await send_email(
        "f@x.com",
        {"ToAddresses": ["t@x.com"]},
        {"Simple": {}},
        region_name=REGION,
    )
    assert isinstance(r, SendEmailResult)
    assert r.message_id == "m1"


async def test_send_email_with_config_set_and_tags(mock_client):
    mock_client.call.return_value = {"MessageId": "m2"}
    r = await send_email(
        "f@x.com",
        {"ToAddresses": ["t@x.com"]},
        {"Simple": {}},
        configuration_set_name="cs1",
        email_tags=[{"Name": "t", "Value": "v"}],
        region_name=REGION,
    )
    assert r.message_id == "m2"


async def test_send_email_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to send email"):
        await send_email(
            "f@x.com",
            {"ToAddresses": ["t@x.com"]},
            {"Simple": {}},
        )


# -----------------------------------------------------------------------
# send_bulk_email
# -----------------------------------------------------------------------


async def test_send_bulk_email_basic(mock_client):
    mock_client.call.return_value = {
        "BulkEmailEntryResults": [{"Status": "SUCCESS"}],
    }
    r = await send_bulk_email(
        "f@x.com",
        {"Template": {"TemplateName": "t1"}},
        [{"Destination": {"ToAddresses": ["t@x.com"]}}],
        region_name=REGION,
    )
    assert len(r) == 1
    assert r[0]["Status"] == "SUCCESS"


async def test_send_bulk_email_with_config_set(mock_client):
    mock_client.call.return_value = {
        "BulkEmailEntryResults": [],
    }
    r = await send_bulk_email(
        "f@x.com",
        {},
        [],
        configuration_set_name="cs",
    )
    assert r == []


async def test_send_bulk_email_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to send bulk email"):
        await send_bulk_email("f@x.com", {}, [])


# -----------------------------------------------------------------------
# Email identities
# -----------------------------------------------------------------------


async def test_create_email_identity_success(mock_client):
    mock_client.call.return_value = {
        "IdentityType": "EMAIL_ADDRESS",
        "VerifiedForSendingStatus": True,
        "DkimAttributes": {"SigningEnabled": True},
    }
    r = await create_email_identity("a@b.com", region_name=REGION)
    assert isinstance(r, EmailIdentityResult)
    assert r.identity_name == "a@b.com"
    assert r.verified_for_sending is True
    assert r.dkim_signing_enabled is True


async def test_create_email_identity_with_dkim_and_tags(mock_client):
    mock_client.call.return_value = {
        "IdentityType": "DOMAIN",
        "DkimAttributes": {},
    }
    r = await create_email_identity(
        "example.com",
        dkim_signing_attributes={"DomainSigningSelector": "sel"},
        tags=[{"Key": "k", "Value": "v"}],
    )
    assert r.identity_name == "example.com"


async def test_create_email_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create email identity"
    ):
        await create_email_identity("x@x.com")


async def test_get_email_identity_success(mock_client):
    mock_client.call.return_value = {
        "IdentityType": "EMAIL_ADDRESS",
        "VerifiedForSendingStatus": False,
        "DkimAttributes": {"SigningEnabled": False},
    }
    r = await get_email_identity("a@b.com", region_name=REGION)
    assert r.identity_name == "a@b.com"
    assert r.verified_for_sending is False


async def test_get_email_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get email identity"
    ):
        await get_email_identity("x@x.com")


async def test_list_email_identities_success(mock_client):
    mock_client.call.return_value = {
        "EmailIdentities": [
            {
                "IdentityName": "a@b.com",
                "IdentityType": "EMAIL_ADDRESS",
                "SendingEnabled": True,
            },
        ],
    }
    r = await list_email_identities(region_name=REGION)
    assert len(r) == 1
    assert r[0].identity_name == "a@b.com"


async def test_list_email_identities_with_pagination(mock_client):
    mock_client.call.return_value = {"EmailIdentities": []}
    r = await list_email_identities(
        page_size=10, next_token="tok"
    )
    assert r == []


async def test_list_email_identities_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list email identities"
    ):
        await list_email_identities()


async def test_delete_email_identity_success(mock_client):
    mock_client.call.return_value = {}
    await delete_email_identity("a@b.com", region_name=REGION)
    mock_client.call.assert_awaited_once()


async def test_delete_email_identity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to delete email identity"
    ):
        await delete_email_identity("x@x.com")


async def test_put_dkim_attributes_success(mock_client):
    mock_client.call.return_value = {}
    await put_email_identity_dkim_attributes(
        "a@b.com", signing_enabled=False, region_name=REGION
    )
    mock_client.call.assert_awaited_once()


async def test_put_dkim_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to update DKIM"
    ):
        await put_email_identity_dkim_attributes("x@x.com")


# -----------------------------------------------------------------------
# Configuration sets
# -----------------------------------------------------------------------


async def test_create_configuration_set_success(mock_client):
    mock_client.call.return_value = {}
    r = await create_configuration_set("cs1", region_name=REGION)
    assert isinstance(r, ConfigSetResult)
    assert r.configuration_set_name == "cs1"

async def test_create_configuration_set_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create configuration set"
    ):
        await create_configuration_set("cs1")


async def test_get_configuration_set_success(mock_client):
    mock_client.call.return_value = {
        "ConfigurationSetName": "cs1",
        "SendingOptions": {"SendingEnabled": False},
        "TrackingOptions": {"CustomRedirectDomain": "d"},
    }
    r = await get_configuration_set("cs1", region_name=REGION)
    assert r.configuration_set_name == "cs1"
    assert r.sending_enabled is False


async def test_get_configuration_set_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get configuration set"
    ):
        await get_configuration_set("cs1")


async def test_list_configuration_sets_success(mock_client):
    mock_client.call.return_value = {
        "ConfigurationSets": ["cs1", "cs2"],
    }
    r = await list_configuration_sets(region_name=REGION)
    assert r == ["cs1", "cs2"]


async def test_list_configuration_sets_with_pagination(mock_client):
    mock_client.call.return_value = {"ConfigurationSets": []}
    r = await list_configuration_sets(
        next_token="tok", page_size=5
    )
    assert r == []


async def test_list_configuration_sets_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list configuration sets"
    ):
        await list_configuration_sets()


async def test_delete_configuration_set_success(mock_client):
    mock_client.call.return_value = {}
    await delete_configuration_set("cs1", region_name=REGION)
    mock_client.call.assert_awaited_once()


async def test_delete_configuration_set_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to delete configuration set"
    ):
        await delete_configuration_set("cs1")


# -----------------------------------------------------------------------
# Email templates
# -----------------------------------------------------------------------


async def test_create_email_template_success(mock_client):
    mock_client.call.return_value = {}
    r = await create_email_template(
        "t1", "subj", text="txt", html="<h>", region_name=REGION
    )
    assert isinstance(r, EmailTemplateResult)
    assert r.template_name == "t1"
    assert r.subject == "subj"
    assert r.text == "txt"
    assert r.html == "<h>"


async def test_create_email_template_no_body(mock_client):
    mock_client.call.return_value = {}
    r = await create_email_template("t1", "subj")
    assert r.text is None
    assert r.html is None


async def test_create_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create email template"
    ):
        await create_email_template("t1", "subj")


async def test_get_email_template_success(mock_client):
    mock_client.call.return_value = {
        "TemplateName": "t1",
        "TemplateContent": {
            "Subject": "s",
            "Text": "t",
            "Html": "<h>",
        },
    }
    r = await get_email_template("t1", region_name=REGION)
    assert r.template_name == "t1"
    assert r.subject == "s"


async def test_get_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get email template"
    ):
        await get_email_template("t1")


async def test_list_email_templates_success(mock_client):
    mock_client.call.return_value = {
        "TemplatesMetadata": [
            {"TemplateName": "t1"},
            {"TemplateName": "t2"},
        ],
    }
    r = await list_email_templates(region_name=REGION)
    assert r == ["t1", "t2"]


async def test_list_email_templates_with_pagination(mock_client):
    mock_client.call.return_value = {"TemplatesMetadata": []}
    r = await list_email_templates(
        next_token="tok", page_size=5
    )
    assert r == []


async def test_list_email_templates_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list email templates"
    ):
        await list_email_templates()


async def test_update_email_template_success(mock_client):
    mock_client.call.return_value = {}
    r = await update_email_template(
        "t1", "new-subj", text="new-t", html="<new>",
        region_name=REGION,
    )
    assert r.subject == "new-subj"
    assert r.text == "new-t"
    assert r.html == "<new>"


async def test_update_email_template_no_body(mock_client):
    mock_client.call.return_value = {}
    r = await update_email_template("t1", "subj")
    assert r.text is None
    assert r.html is None


async def test_update_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to update email template"
    ):
        await update_email_template("t1", "subj")


async def test_delete_email_template_success(mock_client):
    mock_client.call.return_value = {}
    await delete_email_template("t1", region_name=REGION)
    mock_client.call.assert_awaited_once()


async def test_delete_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to delete email template"
    ):
        await delete_email_template("t1")


# -----------------------------------------------------------------------
# Contact lists
# -----------------------------------------------------------------------


async def test_create_contact_list_success(mock_client):
    mock_client.call.return_value = {}
    r = await create_contact_list(
        "cl1",
        description="desc",
        topics=[{"TopicName": "t"}],
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert isinstance(r, ContactListResult)
    assert r.contact_list_name == "cl1"
    assert r.description == "desc"


async def test_create_contact_list_minimal(mock_client):
    mock_client.call.return_value = {}
    r = await create_contact_list("cl1")
    assert r.contact_list_name == "cl1"


async def test_create_contact_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create contact list"
    ):
        await create_contact_list("cl1")


async def test_get_contact_list_success(mock_client):
    mock_client.call.return_value = {
        "ContactListName": "cl1",
        "Description": "d",
        "Tags": [],
    }
    r = await get_contact_list("cl1", region_name=REGION)
    assert r.contact_list_name == "cl1"
    assert r.description == "d"
    assert "Tags" in r.extra


async def test_get_contact_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get contact list"
    ):
        await get_contact_list("cl1")


async def test_list_contact_lists_success(mock_client):
    mock_client.call.return_value = {
        "ContactLists": [{"ContactListName": "cl1"}],
    }
    r = await list_contact_lists(region_name=REGION)
    assert len(r) == 1
    assert r[0].contact_list_name == "cl1"


async def test_list_contact_lists_with_pagination(mock_client):
    mock_client.call.return_value = {"ContactLists": []}
    r = await list_contact_lists(page_size=10, next_token="tok")
    assert r == []


async def test_list_contact_lists_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list contact lists"
    ):
        await list_contact_lists()


# -----------------------------------------------------------------------
# Contacts
# -----------------------------------------------------------------------


async def test_create_contact_success(mock_client):
    mock_client.call.return_value = {}
    r = await create_contact(
        "cl1",
        "e@x.com",
        topic_preferences=[
            {"TopicName": "t", "SubscriptionStatus": "OPT_IN"},
        ],
        unsubscribe_all=True,
        region_name=REGION,
    )
    assert isinstance(r, ContactResult)
    assert r.email_address == "e@x.com"
    assert r.unsubscribe_all is True
    assert len(r.topic_preferences) == 1


async def test_create_contact_minimal(mock_client):
    mock_client.call.return_value = {}
    r = await create_contact("cl1", "e@x.com")
    assert r.topic_preferences == []


async def test_create_contact_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create contact"
    ):
        await create_contact("cl1", "e@x.com")


async def test_get_contact_success(mock_client):
    mock_client.call.return_value = {
        "EmailAddress": "e@x.com",
        "UnsubscribeAll": False,
        "TopicPreferences": [],
        "CreatedTimestamp": "2024-01-01",
    }
    r = await get_contact("cl1", "e@x.com", region_name=REGION)
    assert r.email_address == "e@x.com"
    assert "CreatedTimestamp" in r.extra


async def test_get_contact_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get contact"
    ):
        await get_contact("cl1", "e@x.com")


async def test_list_contacts_success(mock_client):
    mock_client.call.return_value = {
        "Contacts": [
            {
                "EmailAddress": "e@x.com",
                "UnsubscribeAll": False,
                "TopicPreferences": [],
            },
        ],
    }
    r = await list_contacts("cl1", region_name=REGION)
    assert len(r) == 1
    assert r[0].email_address == "e@x.com"


async def test_list_contacts_with_pagination(mock_client):
    mock_client.call.return_value = {"Contacts": []}
    r = await list_contacts("cl1", page_size=10, next_token="tok")
    assert r == []


async def test_list_contacts_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list contacts"
    ):
        await list_contacts("cl1")


async def test_update_contact_success(mock_client):
    mock_client.call.return_value = {}
    await update_contact(
        "cl1",
        "e@x.com",
        topic_preferences=[
            {"TopicName": "t", "SubscriptionStatus": "OPT_OUT"},
        ],
        unsubscribe_all=True,
        region_name=REGION,
    )
    mock_client.call.assert_awaited_once()


async def test_update_contact_minimal(mock_client):
    mock_client.call.return_value = {}
    await update_contact("cl1", "e@x.com")
    mock_client.call.assert_awaited_once()


async def test_update_contact_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to update contact"
    ):
        await update_contact("cl1", "e@x.com")


async def test_delete_contact_success(mock_client):
    mock_client.call.return_value = {}
    await delete_contact("cl1", "e@x.com", region_name=REGION)
    mock_client.call.assert_awaited_once()


async def test_delete_contact_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to delete contact"
    ):
        await delete_contact("cl1", "e@x.com")


# -----------------------------------------------------------------------
# Import / export jobs
# -----------------------------------------------------------------------


async def test_create_import_job_success(mock_client):
    mock_client.call.return_value = {"JobId": "j1"}
    r = await create_import_job(
        {
            "SuppressionListDestination": {
                "SuppressionListImportAction": "PUT",
            },
        },
        {"S3Url": "s3://bucket/key", "DataFormat": "CSV"},
        region_name=REGION,
    )
    assert isinstance(r, ImportJobResult)
    assert r.job_id == "j1"


async def test_create_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create import job"
    ):
        await create_import_job({}, {})


async def test_get_import_job_success(mock_client):
    mock_client.call.return_value = {
        "JobId": "j1",
        "JobStatus": "COMPLETED",
        "CreatedTimestamp": "2024-01-01",
    }
    r = await get_import_job("j1", region_name=REGION)
    assert r.job_id == "j1"
    assert r.job_status == "COMPLETED"
    assert "CreatedTimestamp" in r.extra


async def test_get_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get import job"
    ):
        await get_import_job("j1")


async def test_list_import_jobs_success(mock_client):
    mock_client.call.return_value = {
        "ImportJobs": [
            {"JobId": "j1", "JobStatus": "COMPLETED"},
        ],
    }
    r = await list_import_jobs(region_name=REGION)
    assert len(r) == 1
    assert r[0].job_id == "j1"


async def test_list_import_jobs_with_filters(mock_client):
    mock_client.call.return_value = {"ImportJobs": []}
    r = await list_import_jobs(
        import_destination_type="SUPPRESSION_LIST",
        next_token="tok",
        page_size=5,
    )
    assert r == []


async def test_list_import_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to list import jobs"
    ):
        await list_import_jobs()


async def test_create_export_job_success(mock_client):
    mock_client.call.return_value = {"JobId": "ej1"}
    r = await create_export_job(
        {"DataFormat": "CSV"},
        {"MessageInsightsDataSource": {}},
        region_name=REGION,
    )
    assert r == "ej1"


async def test_create_export_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to create export job"
    ):
        await create_export_job({}, {})


# -----------------------------------------------------------------------
# Message insights
# -----------------------------------------------------------------------


async def test_get_message_insights_success(mock_client):
    mock_client.call.return_value = {
        "MessageId": "m1",
        "Subject": "s",
        "FromEmailAddress": "f@x.com",
        "Insights": [{"Destination": "t@x.com"}],
        "Headers": [],
    }
    r = await get_message_insights("m1", region_name=REGION)
    assert isinstance(r, MessageInsightResult)
    assert r.message_id == "m1"
    assert r.subject == "s"
    assert r.from_email_address == "f@x.com"
    assert len(r.insights) == 1
    assert "Headers" in r.extra


async def test_get_message_insights_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(
        RuntimeError, match="Failed to get message insights"
    ):
        await get_message_insights("m1")


async def test_batch_get_metric_data(mock_client):
    mock_client.call.return_value = {}
    await batch_get_metric_data([], )
    mock_client.call.assert_called_once()


async def test_batch_get_metric_data_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_metric_data([], )


async def test_batch_get_metric_data_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get metric data"):
        await batch_get_metric_data([], )


async def test_cancel_export_job(mock_client):
    mock_client.call.return_value = {}
    await cancel_export_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_cancel_export_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_export_job("test-job_id", )


async def test_cancel_export_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to cancel export job"):
        await cancel_export_job("test-job_id", )


async def test_create_configuration_set_event_destination(mock_client):
    mock_client.call.return_value = {}
    await create_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_configuration_set_event_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )


async def test_create_configuration_set_event_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create configuration set event destination"):
        await create_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )


async def test_create_custom_verification_email_template(mock_client):
    mock_client.call.return_value = {}
    await create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )
    mock_client.call.assert_called_once()


async def test_create_custom_verification_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )


async def test_create_custom_verification_email_template_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create custom verification email template"):
        await create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )


async def test_create_dedicated_ip_pool(mock_client):
    mock_client.call.return_value = {}
    await create_dedicated_ip_pool("test-pool_name", )
    mock_client.call.assert_called_once()


async def test_create_dedicated_ip_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_dedicated_ip_pool("test-pool_name", )


async def test_create_dedicated_ip_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create dedicated ip pool"):
        await create_dedicated_ip_pool("test-pool_name", )


async def test_create_deliverability_test_report(mock_client):
    mock_client.call.return_value = {}
    await create_deliverability_test_report("test-from_email_address", {}, )
    mock_client.call.assert_called_once()


async def test_create_deliverability_test_report_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_deliverability_test_report("test-from_email_address", {}, )


async def test_create_deliverability_test_report_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create deliverability test report"):
        await create_deliverability_test_report("test-from_email_address", {}, )


async def test_create_email_identity_policy(mock_client):
    mock_client.call.return_value = {}
    await create_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )
    mock_client.call.assert_called_once()


async def test_create_email_identity_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )


async def test_create_email_identity_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create email identity policy"):
        await create_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )


async def test_create_multi_region_endpoint(mock_client):
    mock_client.call.return_value = {}
    await create_multi_region_endpoint("test-endpoint_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_multi_region_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_multi_region_endpoint("test-endpoint_name", {}, )


async def test_create_multi_region_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create multi region endpoint"):
        await create_multi_region_endpoint("test-endpoint_name", {}, )


async def test_create_tenant(mock_client):
    mock_client.call.return_value = {}
    await create_tenant("test-tenant_name", )
    mock_client.call.assert_called_once()


async def test_create_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_tenant("test-tenant_name", )


async def test_create_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create tenant"):
        await create_tenant("test-tenant_name", )


async def test_create_tenant_resource_association(mock_client):
    mock_client.call.return_value = {}
    await create_tenant_resource_association("test-tenant_name", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_create_tenant_resource_association_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_tenant_resource_association("test-tenant_name", "test-resource_arn", )


async def test_create_tenant_resource_association_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create tenant resource association"):
        await create_tenant_resource_association("test-tenant_name", "test-resource_arn", )


async def test_delete_configuration_set_event_destination(mock_client):
    mock_client.call.return_value = {}
    await delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_set_event_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", )


async def test_delete_configuration_set_event_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete configuration set event destination"):
        await delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", )


async def test_delete_contact_list(mock_client):
    mock_client.call.return_value = {}
    await delete_contact_list("test-contact_list_name", )
    mock_client.call.assert_called_once()


async def test_delete_contact_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_list("test-contact_list_name", )


async def test_delete_contact_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete contact list"):
        await delete_contact_list("test-contact_list_name", )


async def test_delete_custom_verification_email_template(mock_client):
    mock_client.call.return_value = {}
    await delete_custom_verification_email_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_verification_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_verification_email_template("test-template_name", )


async def test_delete_custom_verification_email_template_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete custom verification email template"):
        await delete_custom_verification_email_template("test-template_name", )


async def test_delete_dedicated_ip_pool(mock_client):
    mock_client.call.return_value = {}
    await delete_dedicated_ip_pool("test-pool_name", )
    mock_client.call.assert_called_once()


async def test_delete_dedicated_ip_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dedicated_ip_pool("test-pool_name", )


async def test_delete_dedicated_ip_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete dedicated ip pool"):
        await delete_dedicated_ip_pool("test-pool_name", )


async def test_delete_email_identity_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_email_identity_policy("test-email_identity", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_email_identity_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_email_identity_policy("test-email_identity", "test-policy_name", )


async def test_delete_email_identity_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete email identity policy"):
        await delete_email_identity_policy("test-email_identity", "test-policy_name", )


async def test_delete_multi_region_endpoint(mock_client):
    mock_client.call.return_value = {}
    await delete_multi_region_endpoint("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_delete_multi_region_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_multi_region_endpoint("test-endpoint_name", )


async def test_delete_multi_region_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete multi region endpoint"):
        await delete_multi_region_endpoint("test-endpoint_name", )


async def test_delete_suppressed_destination(mock_client):
    mock_client.call.return_value = {}
    await delete_suppressed_destination("test-email_address", )
    mock_client.call.assert_called_once()


async def test_delete_suppressed_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_suppressed_destination("test-email_address", )


async def test_delete_suppressed_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete suppressed destination"):
        await delete_suppressed_destination("test-email_address", )


async def test_delete_tenant(mock_client):
    mock_client.call.return_value = {}
    await delete_tenant("test-tenant_name", )
    mock_client.call.assert_called_once()


async def test_delete_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tenant("test-tenant_name", )


async def test_delete_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete tenant"):
        await delete_tenant("test-tenant_name", )


async def test_delete_tenant_resource_association(mock_client):
    mock_client.call.return_value = {}
    await delete_tenant_resource_association("test-tenant_name", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_tenant_resource_association_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tenant_resource_association("test-tenant_name", "test-resource_arn", )


async def test_delete_tenant_resource_association_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete tenant resource association"):
        await delete_tenant_resource_association("test-tenant_name", "test-resource_arn", )


async def test_get_account(mock_client):
    mock_client.call.return_value = {}
    await get_account()
    mock_client.call.assert_called_once()


async def test_get_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_account()


async def test_get_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get account"):
        await get_account()


async def test_get_blacklist_reports(mock_client):
    mock_client.call.return_value = {}
    await get_blacklist_reports([], )
    mock_client.call.assert_called_once()


async def test_get_blacklist_reports_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_blacklist_reports([], )


async def test_get_blacklist_reports_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get blacklist reports"):
        await get_blacklist_reports([], )


async def test_get_configuration_set_event_destinations(mock_client):
    mock_client.call.return_value = {}
    await get_configuration_set_event_destinations("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_get_configuration_set_event_destinations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_configuration_set_event_destinations("test-configuration_set_name", )


async def test_get_configuration_set_event_destinations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get configuration set event destinations"):
        await get_configuration_set_event_destinations("test-configuration_set_name", )


async def test_get_custom_verification_email_template(mock_client):
    mock_client.call.return_value = {}
    await get_custom_verification_email_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_get_custom_verification_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_verification_email_template("test-template_name", )


async def test_get_custom_verification_email_template_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get custom verification email template"):
        await get_custom_verification_email_template("test-template_name", )


async def test_get_dedicated_ip(mock_client):
    mock_client.call.return_value = {}
    await get_dedicated_ip("test-ip", )
    mock_client.call.assert_called_once()


async def test_get_dedicated_ip_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_dedicated_ip("test-ip", )


async def test_get_dedicated_ip_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get dedicated ip"):
        await get_dedicated_ip("test-ip", )


async def test_get_dedicated_ip_pool(mock_client):
    mock_client.call.return_value = {}
    await get_dedicated_ip_pool("test-pool_name", )
    mock_client.call.assert_called_once()


async def test_get_dedicated_ip_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_dedicated_ip_pool("test-pool_name", )


async def test_get_dedicated_ip_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get dedicated ip pool"):
        await get_dedicated_ip_pool("test-pool_name", )


async def test_get_dedicated_ips(mock_client):
    mock_client.call.return_value = {}
    await get_dedicated_ips()
    mock_client.call.assert_called_once()


async def test_get_dedicated_ips_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_dedicated_ips()


async def test_get_dedicated_ips_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get dedicated ips"):
        await get_dedicated_ips()


async def test_get_deliverability_dashboard_options(mock_client):
    mock_client.call.return_value = {}
    await get_deliverability_dashboard_options()
    mock_client.call.assert_called_once()


async def test_get_deliverability_dashboard_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_deliverability_dashboard_options()


async def test_get_deliverability_dashboard_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get deliverability dashboard options"):
        await get_deliverability_dashboard_options()


async def test_get_deliverability_test_report(mock_client):
    mock_client.call.return_value = {}
    await get_deliverability_test_report("test-report_id", )
    mock_client.call.assert_called_once()


async def test_get_deliverability_test_report_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_deliverability_test_report("test-report_id", )


async def test_get_deliverability_test_report_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get deliverability test report"):
        await get_deliverability_test_report("test-report_id", )


async def test_get_domain_deliverability_campaign(mock_client):
    mock_client.call.return_value = {}
    await get_domain_deliverability_campaign("test-campaign_id", )
    mock_client.call.assert_called_once()


async def test_get_domain_deliverability_campaign_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_domain_deliverability_campaign("test-campaign_id", )


async def test_get_domain_deliverability_campaign_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get domain deliverability campaign"):
        await get_domain_deliverability_campaign("test-campaign_id", )


async def test_get_domain_statistics_report(mock_client):
    mock_client.call.return_value = {}
    await get_domain_statistics_report("test-domain", "test-start_date", "test-end_date", )
    mock_client.call.assert_called_once()


async def test_get_domain_statistics_report_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_domain_statistics_report("test-domain", "test-start_date", "test-end_date", )


async def test_get_domain_statistics_report_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get domain statistics report"):
        await get_domain_statistics_report("test-domain", "test-start_date", "test-end_date", )


async def test_get_email_identity_policies(mock_client):
    mock_client.call.return_value = {}
    await get_email_identity_policies("test-email_identity", )
    mock_client.call.assert_called_once()


async def test_get_email_identity_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_email_identity_policies("test-email_identity", )


async def test_get_email_identity_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get email identity policies"):
        await get_email_identity_policies("test-email_identity", )


async def test_get_export_job(mock_client):
    mock_client.call.return_value = {}
    await get_export_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_export_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_export_job("test-job_id", )


async def test_get_export_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get export job"):
        await get_export_job("test-job_id", )


async def test_get_multi_region_endpoint(mock_client):
    mock_client.call.return_value = {}
    await get_multi_region_endpoint("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_get_multi_region_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_multi_region_endpoint("test-endpoint_name", )


async def test_get_multi_region_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get multi region endpoint"):
        await get_multi_region_endpoint("test-endpoint_name", )


async def test_get_reputation_entity(mock_client):
    mock_client.call.return_value = {}
    await get_reputation_entity("test-reputation_entity_reference", "test-reputation_entity_type", )
    mock_client.call.assert_called_once()


async def test_get_reputation_entity_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_reputation_entity("test-reputation_entity_reference", "test-reputation_entity_type", )


async def test_get_reputation_entity_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get reputation entity"):
        await get_reputation_entity("test-reputation_entity_reference", "test-reputation_entity_type", )


async def test_get_suppressed_destination(mock_client):
    mock_client.call.return_value = {}
    await get_suppressed_destination("test-email_address", )
    mock_client.call.assert_called_once()


async def test_get_suppressed_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_suppressed_destination("test-email_address", )


async def test_get_suppressed_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get suppressed destination"):
        await get_suppressed_destination("test-email_address", )


async def test_get_tenant(mock_client):
    mock_client.call.return_value = {}
    await get_tenant("test-tenant_name", )
    mock_client.call.assert_called_once()


async def test_get_tenant_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_tenant("test-tenant_name", )


async def test_get_tenant_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get tenant"):
        await get_tenant("test-tenant_name", )


async def test_list_custom_verification_email_templates(mock_client):
    mock_client.call.return_value = {}
    await list_custom_verification_email_templates()
    mock_client.call.assert_called_once()


async def test_list_custom_verification_email_templates_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_verification_email_templates()


async def test_list_custom_verification_email_templates_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list custom verification email templates"):
        await list_custom_verification_email_templates()


async def test_list_dedicated_ip_pools(mock_client):
    mock_client.call.return_value = {}
    await list_dedicated_ip_pools()
    mock_client.call.assert_called_once()


async def test_list_dedicated_ip_pools_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_dedicated_ip_pools()


async def test_list_dedicated_ip_pools_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list dedicated ip pools"):
        await list_dedicated_ip_pools()


async def test_list_deliverability_test_reports(mock_client):
    mock_client.call.return_value = {}
    await list_deliverability_test_reports()
    mock_client.call.assert_called_once()


async def test_list_deliverability_test_reports_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_deliverability_test_reports()


async def test_list_deliverability_test_reports_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list deliverability test reports"):
        await list_deliverability_test_reports()


async def test_list_domain_deliverability_campaigns(mock_client):
    mock_client.call.return_value = {}
    await list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", )
    mock_client.call.assert_called_once()


async def test_list_domain_deliverability_campaigns_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", )


async def test_list_domain_deliverability_campaigns_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list domain deliverability campaigns"):
        await list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", )


async def test_list_export_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_export_jobs()
    mock_client.call.assert_called_once()


async def test_list_export_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_export_jobs()


async def test_list_export_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list export jobs"):
        await list_export_jobs()


async def test_list_multi_region_endpoints(mock_client):
    mock_client.call.return_value = {}
    await list_multi_region_endpoints()
    mock_client.call.assert_called_once()


async def test_list_multi_region_endpoints_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_multi_region_endpoints()


async def test_list_multi_region_endpoints_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list multi region endpoints"):
        await list_multi_region_endpoints()


async def test_list_recommendations(mock_client):
    mock_client.call.return_value = {}
    await list_recommendations()
    mock_client.call.assert_called_once()


async def test_list_recommendations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_recommendations()


async def test_list_recommendations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list recommendations"):
        await list_recommendations()


async def test_list_reputation_entities(mock_client):
    mock_client.call.return_value = {}
    await list_reputation_entities()
    mock_client.call.assert_called_once()


async def test_list_reputation_entities_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_reputation_entities()


async def test_list_reputation_entities_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list reputation entities"):
        await list_reputation_entities()


async def test_list_resource_tenants(mock_client):
    mock_client.call.return_value = {}
    await list_resource_tenants("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_resource_tenants_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_tenants("test-resource_arn", )


async def test_list_resource_tenants_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list resource tenants"):
        await list_resource_tenants("test-resource_arn", )


async def test_list_suppressed_destinations(mock_client):
    mock_client.call.return_value = {}
    await list_suppressed_destinations()
    mock_client.call.assert_called_once()


async def test_list_suppressed_destinations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_suppressed_destinations()


async def test_list_suppressed_destinations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list suppressed destinations"):
        await list_suppressed_destinations()


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tenant_resources(mock_client):
    mock_client.call.return_value = {}
    await list_tenant_resources("test-tenant_name", )
    mock_client.call.assert_called_once()


async def test_list_tenant_resources_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tenant_resources("test-tenant_name", )


async def test_list_tenant_resources_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tenant resources"):
        await list_tenant_resources("test-tenant_name", )


async def test_list_tenants(mock_client):
    mock_client.call.return_value = {}
    await list_tenants()
    mock_client.call.assert_called_once()


async def test_list_tenants_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tenants()


async def test_list_tenants_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tenants"):
        await list_tenants()


async def test_put_account_dedicated_ip_warmup_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_account_dedicated_ip_warmup_attributes()
    mock_client.call.assert_called_once()


async def test_put_account_dedicated_ip_warmup_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_dedicated_ip_warmup_attributes()


async def test_put_account_dedicated_ip_warmup_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put account dedicated ip warmup attributes"):
        await put_account_dedicated_ip_warmup_attributes()


async def test_put_account_details(mock_client):
    mock_client.call.return_value = {}
    await put_account_details("test-mail_type", "test-website_url", )
    mock_client.call.assert_called_once()


async def test_put_account_details_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_details("test-mail_type", "test-website_url", )


async def test_put_account_details_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put account details"):
        await put_account_details("test-mail_type", "test-website_url", )


async def test_put_account_sending_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_account_sending_attributes()
    mock_client.call.assert_called_once()


async def test_put_account_sending_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_sending_attributes()


async def test_put_account_sending_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put account sending attributes"):
        await put_account_sending_attributes()


async def test_put_account_suppression_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_account_suppression_attributes()
    mock_client.call.assert_called_once()


async def test_put_account_suppression_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_suppression_attributes()


async def test_put_account_suppression_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put account suppression attributes"):
        await put_account_suppression_attributes()


async def test_put_account_vdm_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_account_vdm_attributes({}, )
    mock_client.call.assert_called_once()


async def test_put_account_vdm_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_vdm_attributes({}, )


async def test_put_account_vdm_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put account vdm attributes"):
        await put_account_vdm_attributes({}, )


async def test_put_configuration_set_archiving_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_archiving_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_archiving_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_archiving_options("test-configuration_set_name", )


async def test_put_configuration_set_archiving_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set archiving options"):
        await put_configuration_set_archiving_options("test-configuration_set_name", )


async def test_put_configuration_set_delivery_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_delivery_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_delivery_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_delivery_options("test-configuration_set_name", )


async def test_put_configuration_set_delivery_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set delivery options"):
        await put_configuration_set_delivery_options("test-configuration_set_name", )


async def test_put_configuration_set_reputation_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_reputation_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_reputation_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_reputation_options("test-configuration_set_name", )


async def test_put_configuration_set_reputation_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set reputation options"):
        await put_configuration_set_reputation_options("test-configuration_set_name", )


async def test_put_configuration_set_sending_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_sending_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_sending_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_sending_options("test-configuration_set_name", )


async def test_put_configuration_set_sending_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set sending options"):
        await put_configuration_set_sending_options("test-configuration_set_name", )


async def test_put_configuration_set_suppression_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_suppression_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_suppression_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_suppression_options("test-configuration_set_name", )


async def test_put_configuration_set_suppression_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set suppression options"):
        await put_configuration_set_suppression_options("test-configuration_set_name", )


async def test_put_configuration_set_tracking_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_tracking_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_tracking_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_tracking_options("test-configuration_set_name", )


async def test_put_configuration_set_tracking_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set tracking options"):
        await put_configuration_set_tracking_options("test-configuration_set_name", )


async def test_put_configuration_set_vdm_options(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_set_vdm_options("test-configuration_set_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_set_vdm_options_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_set_vdm_options("test-configuration_set_name", )


async def test_put_configuration_set_vdm_options_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration set vdm options"):
        await put_configuration_set_vdm_options("test-configuration_set_name", )


async def test_put_dedicated_ip_in_pool(mock_client):
    mock_client.call.return_value = {}
    await put_dedicated_ip_in_pool("test-ip", "test-destination_pool_name", )
    mock_client.call.assert_called_once()


async def test_put_dedicated_ip_in_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_dedicated_ip_in_pool("test-ip", "test-destination_pool_name", )


async def test_put_dedicated_ip_in_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip in pool"):
        await put_dedicated_ip_in_pool("test-ip", "test-destination_pool_name", )


async def test_put_dedicated_ip_pool_scaling_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_dedicated_ip_pool_scaling_attributes("test-pool_name", "test-scaling_mode", )
    mock_client.call.assert_called_once()


async def test_put_dedicated_ip_pool_scaling_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_dedicated_ip_pool_scaling_attributes("test-pool_name", "test-scaling_mode", )


async def test_put_dedicated_ip_pool_scaling_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip pool scaling attributes"):
        await put_dedicated_ip_pool_scaling_attributes("test-pool_name", "test-scaling_mode", )


async def test_put_dedicated_ip_warmup_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_dedicated_ip_warmup_attributes("test-ip", 1, )
    mock_client.call.assert_called_once()


async def test_put_dedicated_ip_warmup_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_dedicated_ip_warmup_attributes("test-ip", 1, )


async def test_put_dedicated_ip_warmup_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip warmup attributes"):
        await put_dedicated_ip_warmup_attributes("test-ip", 1, )


async def test_put_deliverability_dashboard_option(mock_client):
    mock_client.call.return_value = {}
    await put_deliverability_dashboard_option(True, )
    mock_client.call.assert_called_once()


async def test_put_deliverability_dashboard_option_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_deliverability_dashboard_option(True, )


async def test_put_deliverability_dashboard_option_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put deliverability dashboard option"):
        await put_deliverability_dashboard_option(True, )


async def test_put_email_identity_configuration_set_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_email_identity_configuration_set_attributes("test-email_identity", )
    mock_client.call.assert_called_once()


async def test_put_email_identity_configuration_set_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_email_identity_configuration_set_attributes("test-email_identity", )


async def test_put_email_identity_configuration_set_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put email identity configuration set attributes"):
        await put_email_identity_configuration_set_attributes("test-email_identity", )


async def test_put_email_identity_dkim_signing_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", )
    mock_client.call.assert_called_once()


async def test_put_email_identity_dkim_signing_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", )


async def test_put_email_identity_dkim_signing_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put email identity dkim signing attributes"):
        await put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", )


async def test_put_email_identity_feedback_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_email_identity_feedback_attributes("test-email_identity", )
    mock_client.call.assert_called_once()


async def test_put_email_identity_feedback_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_email_identity_feedback_attributes("test-email_identity", )


async def test_put_email_identity_feedback_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put email identity feedback attributes"):
        await put_email_identity_feedback_attributes("test-email_identity", )


async def test_put_email_identity_mail_from_attributes(mock_client):
    mock_client.call.return_value = {}
    await put_email_identity_mail_from_attributes("test-email_identity", )
    mock_client.call.assert_called_once()


async def test_put_email_identity_mail_from_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_email_identity_mail_from_attributes("test-email_identity", )


async def test_put_email_identity_mail_from_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put email identity mail from attributes"):
        await put_email_identity_mail_from_attributes("test-email_identity", )


async def test_put_suppressed_destination(mock_client):
    mock_client.call.return_value = {}
    await put_suppressed_destination("test-email_address", "test-reason", )
    mock_client.call.assert_called_once()


async def test_put_suppressed_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_suppressed_destination("test-email_address", "test-reason", )


async def test_put_suppressed_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put suppressed destination"):
        await put_suppressed_destination("test-email_address", "test-reason", )


async def test_run_render_email_template(mock_client):
    mock_client.call.return_value = {}
    await run_render_email_template("test-template_name", "test-template_data", )
    mock_client.call.assert_called_once()


async def test_run_render_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await run_render_email_template("test-template_name", "test-template_data", )


async def test_run_render_email_template_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to run render email template"):
        await run_render_email_template("test-template_name", "test-template_data", )


async def test_send_custom_verification_email(mock_client):
    mock_client.call.return_value = {}
    await send_custom_verification_email("test-email_address", "test-template_name", )
    mock_client.call.assert_called_once()


async def test_send_custom_verification_email_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await send_custom_verification_email("test-email_address", "test-template_name", )


async def test_send_custom_verification_email_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to send custom verification email"):
        await send_custom_verification_email("test-email_address", "test-template_name", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


async def test_update_configuration_set_event_destination(mock_client):
    mock_client.call.return_value = {}
    await update_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_configuration_set_event_destination_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )


async def test_update_configuration_set_event_destination_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update configuration set event destination"):
        await update_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, )


async def test_update_contact_list(mock_client):
    mock_client.call.return_value = {}
    await update_contact_list("test-contact_list_name", )
    mock_client.call.assert_called_once()


async def test_update_contact_list_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_list("test-contact_list_name", )


async def test_update_contact_list_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update contact list"):
        await update_contact_list("test-contact_list_name", )


async def test_update_custom_verification_email_template(mock_client):
    mock_client.call.return_value = {}
    await update_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )
    mock_client.call.assert_called_once()


async def test_update_custom_verification_email_template_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )


async def test_update_custom_verification_email_template_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update custom verification email template"):
        await update_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", )


async def test_update_email_identity_policy(mock_client):
    mock_client.call.return_value = {}
    await update_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )
    mock_client.call.assert_called_once()


async def test_update_email_identity_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )


async def test_update_email_identity_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update email identity policy"):
        await update_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", )


async def test_update_reputation_entity_customer_managed_status(mock_client):
    mock_client.call.return_value = {}
    await update_reputation_entity_customer_managed_status("test-reputation_entity_type", "test-reputation_entity_reference", "test-sending_status", )
    mock_client.call.assert_called_once()


async def test_update_reputation_entity_customer_managed_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_reputation_entity_customer_managed_status("test-reputation_entity_type", "test-reputation_entity_reference", "test-sending_status", )


async def test_update_reputation_entity_customer_managed_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update reputation entity customer managed status"):
        await update_reputation_entity_customer_managed_status("test-reputation_entity_type", "test-reputation_entity_reference", "test-sending_status", )


async def test_update_reputation_entity_policy(mock_client):
    mock_client.call.return_value = {}
    await update_reputation_entity_policy("test-reputation_entity_type", "test-reputation_entity_reference", "test-reputation_entity_policy", )
    mock_client.call.assert_called_once()


async def test_update_reputation_entity_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_reputation_entity_policy("test-reputation_entity_type", "test-reputation_entity_reference", "test-reputation_entity_policy", )


async def test_update_reputation_entity_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update reputation entity policy"):
        await update_reputation_entity_policy("test-reputation_entity_type", "test-reputation_entity_reference", "test-reputation_entity_policy", )


@pytest.mark.asyncio
async def test_send_bulk_email_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import send_bulk_email
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await send_bulk_email("test-from_email_address", "test-default_content", "test-bulk_entries", configuration_set_name={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_email_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_email_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_email_identity("test-identity", dkim_signing_attributes="test-dkim_signing_attributes", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_email_identities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_email_identities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_email_identities(page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_configuration_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_configuration_sets(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_email_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_email_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_email_template("test-template_name", "test-subject", text="test-text", html="test-html", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_email_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_email_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_email_templates(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_email_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import update_email_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await update_email_template("test-template_name", "test-subject", text="test-text", html="test-html", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_contact_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_contact_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_contact_list("test-contact_list_name", description="test-description", topics="test-topics", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contact_lists_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_contact_lists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_contact_lists(page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contacts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_contacts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_contacts("test-contact_list_name", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import update_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await update_contact("test-contact_list_name", "test-email_address", topic_preferences="test-topic_preferences", unsubscribe_all="test-unsubscribe_all", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_import_jobs(import_destination_type=1, next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dedicated_ip_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_dedicated_ip_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_dedicated_ip_pool("test-pool_name", tags=[{"Key": "k", "Value": "v"}], scaling_mode="test-scaling_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_deliverability_test_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_deliverability_test_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_deliverability_test_report("test-from_email_address", "test-content", report_name=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_multi_region_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_multi_region_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_multi_region_endpoint("test-endpoint_name", "test-details", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_tenant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_tenant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_tenant("test-tenant_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_dedicated_ips_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import get_dedicated_ips
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await get_dedicated_ips(pool_name="test-pool_name", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_verification_email_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_custom_verification_email_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_custom_verification_email_templates(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dedicated_ip_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_dedicated_ip_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_dedicated_ip_pools(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_deliverability_test_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_deliverability_test_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_deliverability_test_reports(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_domain_deliverability_campaigns_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_domain_deliverability_campaigns
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_export_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_export_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_export_jobs(next_token="test-next_token", page_size=1, export_source_type=1, job_status="test-job_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_multi_region_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_multi_region_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_multi_region_endpoints(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_recommendations(filter="test-filter", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reputation_entities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_reputation_entities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_reputation_entities(filter="test-filter", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_tenants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_resource_tenants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_resource_tenants("test-resource_arn", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_suppressed_destinations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_suppressed_destinations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_suppressed_destinations(reasons="test-reasons", start_date="test-start_date", end_date="test-end_date", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tenant_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_tenant_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_tenant_resources("test-tenant_name", filter="test-filter", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tenants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import list_tenants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await list_tenants(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_account_dedicated_ip_warmup_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_account_dedicated_ip_warmup_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_account_dedicated_ip_warmup_attributes(auto_warmup_enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_account_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_account_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_account_details("test-mail_type", "test-website_url", contact_language="test-contact_language", use_case_description=True, additional_contact_email_addresses="test-additional_contact_email_addresses", production_access_enabled="test-production_access_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_account_sending_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_account_sending_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_account_sending_attributes(sending_enabled="test-sending_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_account_suppression_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_account_suppression_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_account_suppression_attributes(suppressed_reasons="test-suppressed_reasons", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_archiving_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_archiving_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_archiving_options({}, archive_arn="test-archive_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_delivery_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_delivery_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_delivery_options({}, tls_policy="{}", sending_pool_name="test-sending_pool_name", max_delivery_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_reputation_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_reputation_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_reputation_options({}, reputation_metrics_enabled="test-reputation_metrics_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_sending_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_sending_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_sending_options({}, sending_enabled="test-sending_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_suppression_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_suppression_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_suppression_options({}, suppressed_reasons="test-suppressed_reasons", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_tracking_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_tracking_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_tracking_options({}, custom_redirect_domain="test-custom_redirect_domain", https_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_set_vdm_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_configuration_set_vdm_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_configuration_set_vdm_options({}, vdm_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_deliverability_dashboard_option_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_deliverability_dashboard_option
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_deliverability_dashboard_option("test-dashboard_enabled", subscribed_domains="test-subscribed_domains", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_email_identity_configuration_set_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_email_identity_configuration_set_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_email_identity_configuration_set_attributes("test-email_identity", configuration_set_name={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_email_identity_dkim_signing_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_email_identity_dkim_signing_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", signing_attributes="test-signing_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_email_identity_feedback_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_email_identity_feedback_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_email_identity_feedback_attributes("test-email_identity", email_forwarding_enabled="test-email_forwarding_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_email_identity_mail_from_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import put_email_identity_mail_from_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await put_email_identity_mail_from_attributes("test-email_identity", mail_from_domain="test-mail_from_domain", behavior_on_mx_failure="test-behavior_on_mx_failure", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_custom_verification_email_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import send_custom_verification_email
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await send_custom_verification_email("test-email_address", "test-template_name", configuration_set_name={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import update_contact_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await update_contact_list("test-contact_list_name", topics="test-topics", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_configuration_set_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_configuration_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: mock_client)
    await create_configuration_set("test-configuration_set_name", tags={"k": "v"}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_configuration_set_full_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ses_v2 import create_configuration_set
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ses_v2.async_client", lambda *a, **kw: m)
    await create_configuration_set("cs", sending_options={"SendingEnabled": True}, tracking_options={"CustomRedirectDomain": "d"}, reputation_options={"ReputationMetricsEnabled": True}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
