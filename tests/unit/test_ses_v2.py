"""Tests for aws_util.ses_v2 module — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.ses_v2 as mod
from aws_util.ses_v2 import (
    ConfigSetResult,
    ContactListResult,
    ContactResult,
    EmailIdentityResult,
    EmailTemplateResult,
    ImportJobResult,
    MessageInsightResult,
    SendEmailResult,
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


def _make_client_error(code: str = "ServiceError", msg: str = "err"):
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "Op"
    )


def _mock_client(monkeypatch, **method_returns):
    """Patch get_client to return a MagicMock with preset return values."""
    mc = MagicMock()
    for method_name, rv in method_returns.items():
        getattr(mc, method_name).return_value = rv
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mc)
    return mc


def _mock_client_error(monkeypatch, method_name: str, code: str = "X"):
    """Patch get_client so *method_name* raises ClientError."""
    mc = MagicMock()
    getattr(mc, method_name).side_effect = _make_client_error(code)
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mc)
    return mc


# -----------------------------------------------------------------------
# Model tests
# -----------------------------------------------------------------------


class TestModels:
    def test_send_email_result(self):
        r = SendEmailResult(message_id="m1")
        assert r.message_id == "m1"

    def test_email_identity_result(self):
        r = EmailIdentityResult(
            identity_name="a@b.com",
            identity_type="EMAIL_ADDRESS",
            verified_for_sending=True,
            dkim_signing_enabled=True,
            extra={"k": "v"},
        )
        assert r.identity_name == "a@b.com"
        assert r.verified_for_sending is True

    def test_config_set_result(self):
        r = ConfigSetResult(
            configuration_set_name="cs1", sending_enabled=False
        )
        assert r.configuration_set_name == "cs1"
        assert r.sending_enabled is False

    def test_email_template_result(self):
        r = EmailTemplateResult(
            template_name="t1", subject="s", text="t", html="<h>h</h>"
        )
        assert r.template_name == "t1"

    def test_contact_list_result(self):
        r = ContactListResult(
            contact_list_name="cl", description="desc"
        )
        assert r.contact_list_name == "cl"

    def test_contact_result(self):
        r = ContactResult(
            email_address="e@x.com",
            unsubscribe_all=True,
            topic_preferences=[{"t": "v"}],
        )
        assert r.email_address == "e@x.com"
        assert r.unsubscribe_all is True

    def test_import_job_result(self):
        r = ImportJobResult(
            job_id="j1", job_status="COMPLETED"
        )
        assert r.job_id == "j1"

    def test_message_insight_result(self):
        r = MessageInsightResult(
            message_id="m1",
            subject="s",
            from_email_address="f@x.com",
            insights=[{"i": 1}],
        )
        assert r.message_id == "m1"


# -----------------------------------------------------------------------
# send_email
# -----------------------------------------------------------------------


class TestSendEmail:
    def test_basic(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, send_email={"MessageId": "m1"}
        )
        r = send_email(
            "f@x.com",
            {"ToAddresses": ["t@x.com"]},
            {"Simple": {}},
            region_name=REGION,
        )
        assert isinstance(r, SendEmailResult)
        assert r.message_id == "m1"

    def test_with_config_set_and_tags(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, send_email={"MessageId": "m2"}
        )
        r = send_email(
            "f@x.com",
            {"ToAddresses": ["t@x.com"]},
            {"Simple": {}},
            configuration_set_name="cs1",
            email_tags=[{"Name": "t", "Value": "v"}],
            region_name=REGION,
        )
        assert r.message_id == "m2"
        kw = mc.send_email.call_args[1]
        assert kw["ConfigurationSetName"] == "cs1"
        assert kw["EmailTags"] == [{"Name": "t", "Value": "v"}]

    def test_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "send_email")
        with pytest.raises(RuntimeError, match="Failed to send email"):
            send_email(
                "f@x.com",
                {"ToAddresses": ["t@x.com"]},
                {"Simple": {}},
            )


# -----------------------------------------------------------------------
# send_bulk_email
# -----------------------------------------------------------------------


class TestSendBulkEmail:
    def test_basic(self, monkeypatch):
        mc = _mock_client(
            monkeypatch,
            send_bulk_email={
                "BulkEmailEntryResults": [{"Status": "SUCCESS"}]
            },
        )
        r = send_bulk_email(
            "f@x.com",
            {"Template": {"TemplateName": "t1"}},
            [{"Destination": {"ToAddresses": ["t@x.com"]}}],
            region_name=REGION,
        )
        assert len(r) == 1

    def test_with_config_set(self, monkeypatch):
        mc = _mock_client(
            monkeypatch,
            send_bulk_email={"BulkEmailEntryResults": []},
        )
        send_bulk_email(
            "f@x.com",
            {},
            [],
            configuration_set_name="cs",
        )
        kw = mc.send_bulk_email.call_args[1]
        assert kw["ConfigurationSetName"] == "cs"

    def test_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "send_bulk_email")
        with pytest.raises(
            RuntimeError, match="Failed to send bulk email"
        ):
            send_bulk_email("f@x.com", {}, [])


# -----------------------------------------------------------------------
# Email identities
# -----------------------------------------------------------------------


class TestEmailIdentities:
    def test_create(self, monkeypatch):
        _mock_client(
            monkeypatch,
            create_email_identity={
                "IdentityType": "EMAIL_ADDRESS",
                "VerifiedForSendingStatus": True,
                "DkimAttributes": {"SigningEnabled": True},
            },
        )
        r = create_email_identity(
            "a@b.com", region_name=REGION
        )
        assert isinstance(r, EmailIdentityResult)
        assert r.identity_name == "a@b.com"
        assert r.verified_for_sending is True
        assert r.dkim_signing_enabled is True

    def test_create_with_dkim_and_tags(self, monkeypatch):
        _mock_client(
            monkeypatch,
            create_email_identity={
                "IdentityType": "DOMAIN",
                "DkimAttributes": {},
            },
        )
        r = create_email_identity(
            "example.com",
            dkim_signing_attributes={"DomainSigningSelector": "sel"},
            tags=[{"Key": "k", "Value": "v"}],
        )
        assert r.identity_name == "example.com"

    def test_create_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "create_email_identity")
        with pytest.raises(
            RuntimeError, match="Failed to create email identity"
        ):
            create_email_identity("x@x.com")

    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_email_identity={
                "IdentityType": "EMAIL_ADDRESS",
                "VerifiedForSendingStatus": False,
                "DkimAttributes": {"SigningEnabled": False},
            },
        )
        r = get_email_identity("a@b.com", region_name=REGION)
        assert r.identity_name == "a@b.com"
        assert r.verified_for_sending is False

    def test_get_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "get_email_identity")
        with pytest.raises(
            RuntimeError, match="Failed to get email identity"
        ):
            get_email_identity("x@x.com")

    def test_list(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_email_identities={
                "EmailIdentities": [
                    {
                        "IdentityName": "a@b.com",
                        "IdentityType": "EMAIL_ADDRESS",
                        "SendingEnabled": True,
                    },
                ]
            },
        )
        r = list_email_identities(region_name=REGION)
        assert len(r) == 1
        assert r[0].identity_name == "a@b.com"

    def test_list_with_pagination(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_email_identities={"EmailIdentities": []},
        )
        r = list_email_identities(
            page_size=10, next_token="tok"
        )
        assert r == []

    def test_list_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "list_email_identities")
        with pytest.raises(
            RuntimeError, match="Failed to list email identities"
        ):
            list_email_identities()

    def test_delete(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, delete_email_identity={}
        )
        delete_email_identity("a@b.com", region_name=REGION)
        mc.delete_email_identity.assert_called_once()

    def test_delete_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "delete_email_identity")
        with pytest.raises(
            RuntimeError, match="Failed to delete email identity"
        ):
            delete_email_identity("x@x.com")

    def test_put_dkim(self, monkeypatch):
        mc = _mock_client(
            monkeypatch,
            put_email_identity_dkim_attributes={},
        )
        put_email_identity_dkim_attributes(
            "a@b.com", signing_enabled=False, region_name=REGION
        )
        mc.put_email_identity_dkim_attributes.assert_called_once()

    def test_put_dkim_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "put_email_identity_dkim_attributes"
        )
        with pytest.raises(
            RuntimeError, match="Failed to update DKIM"
        ):
            put_email_identity_dkim_attributes("x@x.com")


# -----------------------------------------------------------------------
# Configuration sets
# -----------------------------------------------------------------------


class TestConfigurationSets:
    def test_create(self, monkeypatch):
        _mock_client(
            monkeypatch, create_configuration_set={}
        )
        r = create_configuration_set("cs1", region_name=REGION)
        assert isinstance(r, ConfigSetResult)
        assert r.configuration_set_name == "cs1"

    def test_create_with_options(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, create_configuration_set={}
        )
        create_configuration_set(
            "cs1",
            sending_options={"SendingEnabled": True},
            tracking_options={"CustomRedirectDomain": "d.com"},
            reputation_options={"ReputationMetricsEnabled": True},
            tags=[{"Key": "k", "Value": "v"}],
        )
        kw = mc.create_configuration_set.call_args[1]
        assert "SendingOptions" in kw
        assert "TrackingOptions" in kw
        assert "ReputationOptions" in kw
        assert "Tags" in kw

    def test_create_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "create_configuration_set"
        )
        with pytest.raises(
            RuntimeError, match="Failed to create configuration set"
        ):
            create_configuration_set("cs1")

    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_configuration_set={
                "ConfigurationSetName": "cs1",
                "SendingOptions": {"SendingEnabled": False},
                "TrackingOptions": {"CustomRedirectDomain": "d"},
            },
        )
        r = get_configuration_set("cs1", region_name=REGION)
        assert r.configuration_set_name == "cs1"
        assert r.sending_enabled is False

    def test_get_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "get_configuration_set"
        )
        with pytest.raises(
            RuntimeError, match="Failed to get configuration set"
        ):
            get_configuration_set("cs1")

    def test_list(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_configuration_sets={
                "ConfigurationSets": ["cs1", "cs2"]
            },
        )
        r = list_configuration_sets(region_name=REGION)
        assert r == ["cs1", "cs2"]

    def test_list_with_pagination(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_configuration_sets={"ConfigurationSets": []},
        )
        r = list_configuration_sets(
            next_token="tok", page_size=5
        )
        assert r == []

    def test_list_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "list_configuration_sets"
        )
        with pytest.raises(
            RuntimeError, match="Failed to list configuration sets"
        ):
            list_configuration_sets()

    def test_delete(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, delete_configuration_set={}
        )
        delete_configuration_set("cs1", region_name=REGION)
        mc.delete_configuration_set.assert_called_once()

    def test_delete_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "delete_configuration_set"
        )
        with pytest.raises(
            RuntimeError,
            match="Failed to delete configuration set",
        ):
            delete_configuration_set("cs1")


# -----------------------------------------------------------------------
# Email templates
# -----------------------------------------------------------------------


class TestEmailTemplates:
    def test_create(self, monkeypatch):
        _mock_client(
            monkeypatch, create_email_template={}
        )
        r = create_email_template(
            "t1", "subj", text="txt", html="<h>", region_name=REGION
        )
        assert isinstance(r, EmailTemplateResult)
        assert r.template_name == "t1"
        assert r.subject == "subj"
        assert r.text == "txt"
        assert r.html == "<h>"

    def test_create_no_body(self, monkeypatch):
        _mock_client(
            monkeypatch, create_email_template={}
        )
        r = create_email_template("t1", "subj")
        assert r.text is None
        assert r.html is None

    def test_create_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "create_email_template"
        )
        with pytest.raises(
            RuntimeError, match="Failed to create email template"
        ):
            create_email_template("t1", "subj")

    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_email_template={
                "TemplateName": "t1",
                "TemplateContent": {
                    "Subject": "s",
                    "Text": "t",
                    "Html": "<h>",
                },
            },
        )
        r = get_email_template("t1", region_name=REGION)
        assert r.template_name == "t1"
        assert r.subject == "s"

    def test_get_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "get_email_template"
        )
        with pytest.raises(
            RuntimeError, match="Failed to get email template"
        ):
            get_email_template("t1")

    def test_list(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_email_templates={
                "TemplatesMetadata": [
                    {"TemplateName": "t1"},
                    {"TemplateName": "t2"},
                ]
            },
        )
        r = list_email_templates(region_name=REGION)
        assert r == ["t1", "t2"]

    def test_list_with_pagination(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_email_templates={"TemplatesMetadata": []},
        )
        r = list_email_templates(next_token="tok", page_size=5)
        assert r == []

    def test_list_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "list_email_templates"
        )
        with pytest.raises(
            RuntimeError, match="Failed to list email templates"
        ):
            list_email_templates()

    def test_update(self, monkeypatch):
        _mock_client(
            monkeypatch, update_email_template={}
        )
        r = update_email_template(
            "t1", "new-subj", text="new-t", html="<new>",
            region_name=REGION,
        )
        assert r.subject == "new-subj"
        assert r.text == "new-t"
        assert r.html == "<new>"

    def test_update_no_body(self, monkeypatch):
        _mock_client(
            monkeypatch, update_email_template={}
        )
        r = update_email_template("t1", "subj")
        assert r.text is None
        assert r.html is None

    def test_update_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "update_email_template"
        )
        with pytest.raises(
            RuntimeError, match="Failed to update email template"
        ):
            update_email_template("t1", "subj")

    def test_delete(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, delete_email_template={}
        )
        delete_email_template("t1", region_name=REGION)
        mc.delete_email_template.assert_called_once()

    def test_delete_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "delete_email_template"
        )
        with pytest.raises(
            RuntimeError, match="Failed to delete email template"
        ):
            delete_email_template("t1")


# -----------------------------------------------------------------------
# Contact lists
# -----------------------------------------------------------------------


class TestContactLists:
    def test_create(self, monkeypatch):
        _mock_client(
            monkeypatch, create_contact_list={}
        )
        r = create_contact_list(
            "cl1",
            description="desc",
            topics=[{"TopicName": "t"}],
            tags=[{"Key": "k", "Value": "v"}],
            region_name=REGION,
        )
        assert isinstance(r, ContactListResult)
        assert r.contact_list_name == "cl1"
        assert r.description == "desc"

    def test_create_minimal(self, monkeypatch):
        _mock_client(
            monkeypatch, create_contact_list={}
        )
        r = create_contact_list("cl1")
        assert r.contact_list_name == "cl1"

    def test_create_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "create_contact_list"
        )
        with pytest.raises(
            RuntimeError, match="Failed to create contact list"
        ):
            create_contact_list("cl1")

    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_contact_list={
                "ContactListName": "cl1",
                "Description": "d",
                "Tags": [],
            },
        )
        r = get_contact_list("cl1", region_name=REGION)
        assert r.contact_list_name == "cl1"
        assert r.description == "d"
        assert "Tags" in r.extra

    def test_get_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "get_contact_list"
        )
        with pytest.raises(
            RuntimeError, match="Failed to get contact list"
        ):
            get_contact_list("cl1")

    def test_list(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_contact_lists={
                "ContactLists": [{"ContactListName": "cl1"}]
            },
        )
        r = list_contact_lists(region_name=REGION)
        assert len(r) == 1
        assert r[0].contact_list_name == "cl1"

    def test_list_with_pagination(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_contact_lists={"ContactLists": []},
        )
        r = list_contact_lists(page_size=10, next_token="tok")
        assert r == []

    def test_list_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "list_contact_lists"
        )
        with pytest.raises(
            RuntimeError, match="Failed to list contact lists"
        ):
            list_contact_lists()


# -----------------------------------------------------------------------
# Contacts
# -----------------------------------------------------------------------


class TestContacts:
    def test_create(self, monkeypatch):
        _mock_client(monkeypatch, create_contact={})
        r = create_contact(
            "cl1",
            "e@x.com",
            topic_preferences=[{"TopicName": "t", "SubscriptionStatus": "OPT_IN"}],
            unsubscribe_all=True,
            region_name=REGION,
        )
        assert isinstance(r, ContactResult)
        assert r.email_address == "e@x.com"
        assert r.unsubscribe_all is True
        assert len(r.topic_preferences) == 1

    def test_create_minimal(self, monkeypatch):
        _mock_client(monkeypatch, create_contact={})
        r = create_contact("cl1", "e@x.com")
        assert r.topic_preferences == []

    def test_create_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "create_contact")
        with pytest.raises(
            RuntimeError, match="Failed to create contact"
        ):
            create_contact("cl1", "e@x.com")

    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_contact={
                "EmailAddress": "e@x.com",
                "UnsubscribeAll": False,
                "TopicPreferences": [],
                "CreatedTimestamp": "2024-01-01",
            },
        )
        r = get_contact("cl1", "e@x.com", region_name=REGION)
        assert r.email_address == "e@x.com"
        assert "CreatedTimestamp" in r.extra

    def test_get_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "get_contact")
        with pytest.raises(
            RuntimeError, match="Failed to get contact"
        ):
            get_contact("cl1", "e@x.com")

    def test_list(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_contacts={
                "Contacts": [
                    {
                        "EmailAddress": "e@x.com",
                        "UnsubscribeAll": False,
                        "TopicPreferences": [],
                    }
                ]
            },
        )
        r = list_contacts("cl1", region_name=REGION)
        assert len(r) == 1
        assert r[0].email_address == "e@x.com"

    def test_list_with_pagination(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_contacts={"Contacts": []},
        )
        r = list_contacts("cl1", page_size=10, next_token="tok")
        assert r == []

    def test_list_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "list_contacts")
        with pytest.raises(
            RuntimeError, match="Failed to list contacts"
        ):
            list_contacts("cl1")

    def test_update(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, update_contact={}
        )
        update_contact(
            "cl1",
            "e@x.com",
            topic_preferences=[{"TopicName": "t", "SubscriptionStatus": "OPT_OUT"}],
            unsubscribe_all=True,
            region_name=REGION,
        )
        mc.update_contact.assert_called_once()

    def test_update_minimal(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, update_contact={}
        )
        update_contact("cl1", "e@x.com")
        kw = mc.update_contact.call_args[1]
        assert "TopicPreferences" not in kw
        assert "UnsubscribeAll" not in kw

    def test_update_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "update_contact")
        with pytest.raises(
            RuntimeError, match="Failed to update contact"
        ):
            update_contact("cl1", "e@x.com")

    def test_delete(self, monkeypatch):
        mc = _mock_client(
            monkeypatch, delete_contact={}
        )
        delete_contact("cl1", "e@x.com", region_name=REGION)
        mc.delete_contact.assert_called_once()

    def test_delete_error(self, monkeypatch):
        _mock_client_error(monkeypatch, "delete_contact")
        with pytest.raises(
            RuntimeError, match="Failed to delete contact"
        ):
            delete_contact("cl1", "e@x.com")


# -----------------------------------------------------------------------
# Import / export jobs
# -----------------------------------------------------------------------


class TestImportExportJobs:
    def test_create_import_job(self, monkeypatch):
        _mock_client(
            monkeypatch,
            create_import_job={"JobId": "j1"},
        )
        r = create_import_job(
            {"SuppressionListDestination": {"SuppressionListImportAction": "PUT"}},
            {"S3Url": "s3://bucket/key", "DataFormat": "CSV"},
            region_name=REGION,
        )
        assert isinstance(r, ImportJobResult)
        assert r.job_id == "j1"

    def test_create_import_job_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "create_import_job"
        )
        with pytest.raises(
            RuntimeError, match="Failed to create import job"
        ):
            create_import_job({}, {})

    def test_get_import_job(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_import_job={
                "JobId": "j1",
                "JobStatus": "COMPLETED",
                "CreatedTimestamp": "2024-01-01",
            },
        )
        r = get_import_job("j1", region_name=REGION)
        assert r.job_id == "j1"
        assert r.job_status == "COMPLETED"
        assert "CreatedTimestamp" in r.extra

    def test_get_import_job_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "get_import_job"
        )
        with pytest.raises(
            RuntimeError, match="Failed to get import job"
        ):
            get_import_job("j1")

    def test_list_import_jobs(self, monkeypatch):
        _mock_client(
            monkeypatch,
            list_import_jobs={
                "ImportJobs": [
                    {"JobId": "j1", "JobStatus": "COMPLETED"},
                ]
            },
        )
        r = list_import_jobs(region_name=REGION)
        assert len(r) == 1
        assert r[0].job_id == "j1"

    def test_list_import_jobs_with_filters(self, monkeypatch):
        mc = _mock_client(
            monkeypatch,
            list_import_jobs={"ImportJobs": []},
        )
        list_import_jobs(
            import_destination_type="SUPPRESSION_LIST",
            next_token="tok",
            page_size=5,
        )
        kw = mc.list_import_jobs.call_args[1]
        assert kw["ImportDestinationType"] == "SUPPRESSION_LIST"
        assert kw["NextToken"] == "tok"
        assert kw["PageSize"] == 5

    def test_list_import_jobs_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "list_import_jobs"
        )
        with pytest.raises(
            RuntimeError, match="Failed to list import jobs"
        ):
            list_import_jobs()

    def test_create_export_job(self, monkeypatch):
        _mock_client(
            monkeypatch,
            create_export_job={"JobId": "ej1"},
        )
        r = create_export_job(
            {"DataFormat": "CSV"},
            {"MessageInsightsDataSource": {}},
            region_name=REGION,
        )
        assert r == "ej1"

    def test_create_export_job_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "create_export_job"
        )
        with pytest.raises(
            RuntimeError, match="Failed to create export job"
        ):
            create_export_job({}, {})


# -----------------------------------------------------------------------
# Message insights
# -----------------------------------------------------------------------


class TestMessageInsights:
    def test_get(self, monkeypatch):
        _mock_client(
            monkeypatch,
            get_message_insights={
                "MessageId": "m1",
                "Subject": "s",
                "FromEmailAddress": "f@x.com",
                "Insights": [{"Destination": "t@x.com"}],
                "Headers": [],
            },
        )
        r = get_message_insights("m1", region_name=REGION)
        assert isinstance(r, MessageInsightResult)
        assert r.message_id == "m1"
        assert r.subject == "s"
        assert r.from_email_address == "f@x.com"
        assert len(r.insights) == 1
        assert "Headers" in r.extra

    def test_get_error(self, monkeypatch):
        _mock_client_error(
            monkeypatch, "get_message_insights"
        )
        with pytest.raises(
            RuntimeError, match="Failed to get message insights"
        ):
            get_message_insights("m1")


def test_batch_get_metric_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    batch_get_metric_data([], region_name=REGION)
    mock_client.batch_get_metric_data.assert_called_once()


def test_batch_get_metric_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_metric_data",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get metric data"):
        batch_get_metric_data([], region_name=REGION)


def test_cancel_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_job.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    cancel_export_job("test-job_id", region_name=REGION)
    mock_client.cancel_export_job.assert_called_once()


def test_cancel_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_export_job",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel export job"):
        cancel_export_job("test-job_id", region_name=REGION)


def test_create_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, region_name=REGION)
    mock_client.create_configuration_set_event_destination.assert_called_once()


def test_create_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create configuration set event destination"):
        create_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, region_name=REGION)


def test_create_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)
    mock_client.create_custom_verification_email_template.assert_called_once()


def test_create_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom verification email template"):
        create_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)


def test_create_dedicated_ip_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dedicated_ip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_dedicated_ip_pool("test-pool_name", region_name=REGION)
    mock_client.create_dedicated_ip_pool.assert_called_once()


def test_create_dedicated_ip_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dedicated_ip_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dedicated_ip_pool",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dedicated ip pool"):
        create_dedicated_ip_pool("test-pool_name", region_name=REGION)


def test_create_deliverability_test_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_deliverability_test_report.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_deliverability_test_report("test-from_email_address", {}, region_name=REGION)
    mock_client.create_deliverability_test_report.assert_called_once()


def test_create_deliverability_test_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_deliverability_test_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_deliverability_test_report",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create deliverability test report"):
        create_deliverability_test_report("test-from_email_address", {}, region_name=REGION)


def test_create_email_identity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_email_identity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", region_name=REGION)
    mock_client.create_email_identity_policy.assert_called_once()


def test_create_email_identity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_email_identity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_email_identity_policy",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create email identity policy"):
        create_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", region_name=REGION)


def test_create_multi_region_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_multi_region_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_multi_region_endpoint("test-endpoint_name", {}, region_name=REGION)
    mock_client.create_multi_region_endpoint.assert_called_once()


def test_create_multi_region_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_multi_region_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_multi_region_endpoint",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create multi region endpoint"):
        create_multi_region_endpoint("test-endpoint_name", {}, region_name=REGION)


def test_create_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_tenant("test-tenant_name", region_name=REGION)
    mock_client.create_tenant.assert_called_once()


def test_create_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tenant",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tenant"):
        create_tenant("test-tenant_name", region_name=REGION)


def test_create_tenant_resource_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_tenant_resource_association("test-tenant_name", "test-resource_arn", region_name=REGION)
    mock_client.create_tenant_resource_association.assert_called_once()


def test_create_tenant_resource_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant_resource_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tenant_resource_association",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tenant resource association"):
        create_tenant_resource_association("test-tenant_name", "test-resource_arn", region_name=REGION)


def test_delete_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", region_name=REGION)
    mock_client.delete_configuration_set_event_destination.assert_called_once()


def test_delete_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration set event destination"):
        delete_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", region_name=REGION)


def test_delete_contact_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_list.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_contact_list("test-contact_list_name", region_name=REGION)
    mock_client.delete_contact_list.assert_called_once()


def test_delete_contact_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_list",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete contact list"):
        delete_contact_list("test-contact_list_name", region_name=REGION)


def test_delete_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_custom_verification_email_template("test-template_name", region_name=REGION)
    mock_client.delete_custom_verification_email_template.assert_called_once()


def test_delete_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom verification email template"):
        delete_custom_verification_email_template("test-template_name", region_name=REGION)


def test_delete_dedicated_ip_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dedicated_ip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_dedicated_ip_pool("test-pool_name", region_name=REGION)
    mock_client.delete_dedicated_ip_pool.assert_called_once()


def test_delete_dedicated_ip_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dedicated_ip_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dedicated_ip_pool",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dedicated ip pool"):
        delete_dedicated_ip_pool("test-pool_name", region_name=REGION)


def test_delete_email_identity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_email_identity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_email_identity_policy("test-email_identity", "test-policy_name", region_name=REGION)
    mock_client.delete_email_identity_policy.assert_called_once()


def test_delete_email_identity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_email_identity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_email_identity_policy",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete email identity policy"):
        delete_email_identity_policy("test-email_identity", "test-policy_name", region_name=REGION)


def test_delete_multi_region_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_multi_region_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_multi_region_endpoint("test-endpoint_name", region_name=REGION)
    mock_client.delete_multi_region_endpoint.assert_called_once()


def test_delete_multi_region_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_multi_region_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_multi_region_endpoint",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete multi region endpoint"):
        delete_multi_region_endpoint("test-endpoint_name", region_name=REGION)


def test_delete_suppressed_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_suppressed_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_suppressed_destination("test-email_address", region_name=REGION)
    mock_client.delete_suppressed_destination.assert_called_once()


def test_delete_suppressed_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_suppressed_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_suppressed_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete suppressed destination"):
        delete_suppressed_destination("test-email_address", region_name=REGION)


def test_delete_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_tenant("test-tenant_name", region_name=REGION)
    mock_client.delete_tenant.assert_called_once()


def test_delete_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tenant",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tenant"):
        delete_tenant("test-tenant_name", region_name=REGION)


def test_delete_tenant_resource_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    delete_tenant_resource_association("test-tenant_name", "test-resource_arn", region_name=REGION)
    mock_client.delete_tenant_resource_association.assert_called_once()


def test_delete_tenant_resource_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant_resource_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tenant_resource_association",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tenant resource association"):
        delete_tenant_resource_association("test-tenant_name", "test-resource_arn", region_name=REGION)


def test_get_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_account(region_name=REGION)
    mock_client.get_account.assert_called_once()


def test_get_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account"):
        get_account(region_name=REGION)


def test_get_blacklist_reports(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blacklist_reports.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_blacklist_reports([], region_name=REGION)
    mock_client.get_blacklist_reports.assert_called_once()


def test_get_blacklist_reports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blacklist_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_blacklist_reports",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get blacklist reports"):
        get_blacklist_reports([], region_name=REGION)


def test_get_configuration_set_event_destinations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_set_event_destinations.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_configuration_set_event_destinations("test-configuration_set_name", region_name=REGION)
    mock_client.get_configuration_set_event_destinations.assert_called_once()


def test_get_configuration_set_event_destinations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_set_event_destinations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_configuration_set_event_destinations",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get configuration set event destinations"):
        get_configuration_set_event_destinations("test-configuration_set_name", region_name=REGION)


def test_get_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_custom_verification_email_template("test-template_name", region_name=REGION)
    mock_client.get_custom_verification_email_template.assert_called_once()


def test_get_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get custom verification email template"):
        get_custom_verification_email_template("test-template_name", region_name=REGION)


def test_get_dedicated_ip(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ip.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_dedicated_ip("test-ip", region_name=REGION)
    mock_client.get_dedicated_ip.assert_called_once()


def test_get_dedicated_ip_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ip.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dedicated_ip",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dedicated ip"):
        get_dedicated_ip("test-ip", region_name=REGION)


def test_get_dedicated_ip_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_dedicated_ip_pool("test-pool_name", region_name=REGION)
    mock_client.get_dedicated_ip_pool.assert_called_once()


def test_get_dedicated_ip_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ip_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dedicated_ip_pool",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dedicated ip pool"):
        get_dedicated_ip_pool("test-pool_name", region_name=REGION)


def test_get_dedicated_ips(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ips.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_dedicated_ips(region_name=REGION)
    mock_client.get_dedicated_ips.assert_called_once()


def test_get_dedicated_ips_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dedicated_ips.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dedicated_ips",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dedicated ips"):
        get_dedicated_ips(region_name=REGION)


def test_get_deliverability_dashboard_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deliverability_dashboard_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_deliverability_dashboard_options(region_name=REGION)
    mock_client.get_deliverability_dashboard_options.assert_called_once()


def test_get_deliverability_dashboard_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deliverability_dashboard_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deliverability_dashboard_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get deliverability dashboard options"):
        get_deliverability_dashboard_options(region_name=REGION)


def test_get_deliverability_test_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deliverability_test_report.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_deliverability_test_report("test-report_id", region_name=REGION)
    mock_client.get_deliverability_test_report.assert_called_once()


def test_get_deliverability_test_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deliverability_test_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deliverability_test_report",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get deliverability test report"):
        get_deliverability_test_report("test-report_id", region_name=REGION)


def test_get_domain_deliverability_campaign(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_deliverability_campaign.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_domain_deliverability_campaign("test-campaign_id", region_name=REGION)
    mock_client.get_domain_deliverability_campaign.assert_called_once()


def test_get_domain_deliverability_campaign_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_deliverability_campaign.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_deliverability_campaign",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get domain deliverability campaign"):
        get_domain_deliverability_campaign("test-campaign_id", region_name=REGION)


def test_get_domain_statistics_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_statistics_report.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_domain_statistics_report("test-domain", "test-start_date", "test-end_date", region_name=REGION)
    mock_client.get_domain_statistics_report.assert_called_once()


def test_get_domain_statistics_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_statistics_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_statistics_report",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get domain statistics report"):
        get_domain_statistics_report("test-domain", "test-start_date", "test-end_date", region_name=REGION)


def test_get_email_identity_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_email_identity_policies.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_email_identity_policies("test-email_identity", region_name=REGION)
    mock_client.get_email_identity_policies.assert_called_once()


def test_get_email_identity_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_email_identity_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_email_identity_policies",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get email identity policies"):
        get_email_identity_policies("test-email_identity", region_name=REGION)


def test_get_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export_job.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_export_job("test-job_id", region_name=REGION)
    mock_client.get_export_job.assert_called_once()


def test_get_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_export_job",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get export job"):
        get_export_job("test-job_id", region_name=REGION)


def test_get_multi_region_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_multi_region_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_multi_region_endpoint("test-endpoint_name", region_name=REGION)
    mock_client.get_multi_region_endpoint.assert_called_once()


def test_get_multi_region_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_multi_region_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_multi_region_endpoint",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get multi region endpoint"):
        get_multi_region_endpoint("test-endpoint_name", region_name=REGION)


def test_get_reputation_entity(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reputation_entity.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_reputation_entity("test-reputation_entity_reference", "test-reputation_entity_type", region_name=REGION)
    mock_client.get_reputation_entity.assert_called_once()


def test_get_reputation_entity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reputation_entity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reputation_entity",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reputation entity"):
        get_reputation_entity("test-reputation_entity_reference", "test-reputation_entity_type", region_name=REGION)


def test_get_suppressed_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_suppressed_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_suppressed_destination("test-email_address", region_name=REGION)
    mock_client.get_suppressed_destination.assert_called_once()


def test_get_suppressed_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_suppressed_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_suppressed_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get suppressed destination"):
        get_suppressed_destination("test-email_address", region_name=REGION)


def test_get_tenant(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tenant.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_tenant("test-tenant_name", region_name=REGION)
    mock_client.get_tenant.assert_called_once()


def test_get_tenant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tenant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_tenant",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get tenant"):
        get_tenant("test-tenant_name", region_name=REGION)


def test_list_custom_verification_email_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_custom_verification_email_templates(region_name=REGION)
    mock_client.list_custom_verification_email_templates.assert_called_once()


def test_list_custom_verification_email_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_verification_email_templates",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list custom verification email templates"):
        list_custom_verification_email_templates(region_name=REGION)


def test_list_dedicated_ip_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dedicated_ip_pools.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_dedicated_ip_pools(region_name=REGION)
    mock_client.list_dedicated_ip_pools.assert_called_once()


def test_list_dedicated_ip_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dedicated_ip_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dedicated_ip_pools",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dedicated ip pools"):
        list_dedicated_ip_pools(region_name=REGION)


def test_list_deliverability_test_reports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_deliverability_test_reports.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_deliverability_test_reports(region_name=REGION)
    mock_client.list_deliverability_test_reports.assert_called_once()


def test_list_deliverability_test_reports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_deliverability_test_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_deliverability_test_reports",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list deliverability test reports"):
        list_deliverability_test_reports(region_name=REGION)


def test_list_domain_deliverability_campaigns(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_deliverability_campaigns.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", region_name=REGION)
    mock_client.list_domain_deliverability_campaigns.assert_called_once()


def test_list_domain_deliverability_campaigns_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_deliverability_campaigns.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_domain_deliverability_campaigns",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list domain deliverability campaigns"):
        list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", region_name=REGION)


def test_list_export_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_export_jobs(region_name=REGION)
    mock_client.list_export_jobs.assert_called_once()


def test_list_export_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_export_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_export_jobs",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list export jobs"):
        list_export_jobs(region_name=REGION)


def test_list_multi_region_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_multi_region_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_multi_region_endpoints(region_name=REGION)
    mock_client.list_multi_region_endpoints.assert_called_once()


def test_list_multi_region_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_multi_region_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_multi_region_endpoints",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list multi region endpoints"):
        list_multi_region_endpoints(region_name=REGION)


def test_list_recommendations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_recommendations(region_name=REGION)
    mock_client.list_recommendations.assert_called_once()


def test_list_recommendations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recommendations",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list recommendations"):
        list_recommendations(region_name=REGION)


def test_list_reputation_entities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reputation_entities.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_reputation_entities(region_name=REGION)
    mock_client.list_reputation_entities.assert_called_once()


def test_list_reputation_entities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reputation_entities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reputation_entities",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list reputation entities"):
        list_reputation_entities(region_name=REGION)


def test_list_resource_tenants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_tenants.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_resource_tenants("test-resource_arn", region_name=REGION)
    mock_client.list_resource_tenants.assert_called_once()


def test_list_resource_tenants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_tenants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_tenants",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource tenants"):
        list_resource_tenants("test-resource_arn", region_name=REGION)


def test_list_suppressed_destinations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_suppressed_destinations.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_suppressed_destinations(region_name=REGION)
    mock_client.list_suppressed_destinations.assert_called_once()


def test_list_suppressed_destinations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_suppressed_destinations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_suppressed_destinations",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list suppressed destinations"):
        list_suppressed_destinations(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_tenant_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tenant_resources.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_tenant_resources("test-tenant_name", region_name=REGION)
    mock_client.list_tenant_resources.assert_called_once()


def test_list_tenant_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tenant_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tenant_resources",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tenant resources"):
        list_tenant_resources("test-tenant_name", region_name=REGION)


def test_list_tenants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tenants.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_tenants(region_name=REGION)
    mock_client.list_tenants.assert_called_once()


def test_list_tenants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tenants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tenants",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tenants"):
        list_tenants(region_name=REGION)


def test_put_account_dedicated_ip_warmup_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_dedicated_ip_warmup_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_dedicated_ip_warmup_attributes(region_name=REGION)
    mock_client.put_account_dedicated_ip_warmup_attributes.assert_called_once()


def test_put_account_dedicated_ip_warmup_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_dedicated_ip_warmup_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_dedicated_ip_warmup_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account dedicated ip warmup attributes"):
        put_account_dedicated_ip_warmup_attributes(region_name=REGION)


def test_put_account_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_details.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_details("test-mail_type", "test-website_url", region_name=REGION)
    mock_client.put_account_details.assert_called_once()


def test_put_account_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_details",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account details"):
        put_account_details("test-mail_type", "test-website_url", region_name=REGION)


def test_put_account_sending_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_sending_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_sending_attributes(region_name=REGION)
    mock_client.put_account_sending_attributes.assert_called_once()


def test_put_account_sending_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_sending_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_sending_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account sending attributes"):
        put_account_sending_attributes(region_name=REGION)


def test_put_account_suppression_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_suppression_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_suppression_attributes(region_name=REGION)
    mock_client.put_account_suppression_attributes.assert_called_once()


def test_put_account_suppression_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_suppression_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_suppression_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account suppression attributes"):
        put_account_suppression_attributes(region_name=REGION)


def test_put_account_vdm_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_vdm_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_vdm_attributes({}, region_name=REGION)
    mock_client.put_account_vdm_attributes.assert_called_once()


def test_put_account_vdm_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_vdm_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_vdm_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account vdm attributes"):
        put_account_vdm_attributes({}, region_name=REGION)


def test_put_configuration_set_archiving_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_archiving_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_archiving_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_archiving_options.assert_called_once()


def test_put_configuration_set_archiving_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_archiving_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_archiving_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set archiving options"):
        put_configuration_set_archiving_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_delivery_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_delivery_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_delivery_options.assert_called_once()


def test_put_configuration_set_delivery_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_delivery_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set delivery options"):
        put_configuration_set_delivery_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_reputation_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_reputation_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_reputation_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_reputation_options.assert_called_once()


def test_put_configuration_set_reputation_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_reputation_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_reputation_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set reputation options"):
        put_configuration_set_reputation_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_sending_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_sending_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_sending_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_sending_options.assert_called_once()


def test_put_configuration_set_sending_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_sending_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_sending_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set sending options"):
        put_configuration_set_sending_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_suppression_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_suppression_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_suppression_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_suppression_options.assert_called_once()


def test_put_configuration_set_suppression_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_suppression_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_suppression_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set suppression options"):
        put_configuration_set_suppression_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_tracking_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_tracking_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_tracking_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_tracking_options.assert_called_once()


def test_put_configuration_set_tracking_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_tracking_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_tracking_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set tracking options"):
        put_configuration_set_tracking_options("test-configuration_set_name", region_name=REGION)


def test_put_configuration_set_vdm_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_vdm_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_vdm_options("test-configuration_set_name", region_name=REGION)
    mock_client.put_configuration_set_vdm_options.assert_called_once()


def test_put_configuration_set_vdm_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_set_vdm_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_set_vdm_options",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration set vdm options"):
        put_configuration_set_vdm_options("test-configuration_set_name", region_name=REGION)


def test_put_dedicated_ip_in_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_in_pool.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_dedicated_ip_in_pool("test-ip", "test-destination_pool_name", region_name=REGION)
    mock_client.put_dedicated_ip_in_pool.assert_called_once()


def test_put_dedicated_ip_in_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_in_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_dedicated_ip_in_pool",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip in pool"):
        put_dedicated_ip_in_pool("test-ip", "test-destination_pool_name", region_name=REGION)


def test_put_dedicated_ip_pool_scaling_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_pool_scaling_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_dedicated_ip_pool_scaling_attributes("test-pool_name", "test-scaling_mode", region_name=REGION)
    mock_client.put_dedicated_ip_pool_scaling_attributes.assert_called_once()


def test_put_dedicated_ip_pool_scaling_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_pool_scaling_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_dedicated_ip_pool_scaling_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip pool scaling attributes"):
        put_dedicated_ip_pool_scaling_attributes("test-pool_name", "test-scaling_mode", region_name=REGION)


def test_put_dedicated_ip_warmup_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_warmup_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_dedicated_ip_warmup_attributes("test-ip", 1, region_name=REGION)
    mock_client.put_dedicated_ip_warmup_attributes.assert_called_once()


def test_put_dedicated_ip_warmup_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_dedicated_ip_warmup_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_dedicated_ip_warmup_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put dedicated ip warmup attributes"):
        put_dedicated_ip_warmup_attributes("test-ip", 1, region_name=REGION)


def test_put_deliverability_dashboard_option(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_deliverability_dashboard_option.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_deliverability_dashboard_option(True, region_name=REGION)
    mock_client.put_deliverability_dashboard_option.assert_called_once()


def test_put_deliverability_dashboard_option_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_deliverability_dashboard_option.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_deliverability_dashboard_option",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put deliverability dashboard option"):
        put_deliverability_dashboard_option(True, region_name=REGION)


def test_put_email_identity_configuration_set_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_configuration_set_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_configuration_set_attributes("test-email_identity", region_name=REGION)
    mock_client.put_email_identity_configuration_set_attributes.assert_called_once()


def test_put_email_identity_configuration_set_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_configuration_set_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_email_identity_configuration_set_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put email identity configuration set attributes"):
        put_email_identity_configuration_set_attributes("test-email_identity", region_name=REGION)


def test_put_email_identity_dkim_signing_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_dkim_signing_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", region_name=REGION)
    mock_client.put_email_identity_dkim_signing_attributes.assert_called_once()


def test_put_email_identity_dkim_signing_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_dkim_signing_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_email_identity_dkim_signing_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put email identity dkim signing attributes"):
        put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", region_name=REGION)


def test_put_email_identity_feedback_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_feedback_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_feedback_attributes("test-email_identity", region_name=REGION)
    mock_client.put_email_identity_feedback_attributes.assert_called_once()


def test_put_email_identity_feedback_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_feedback_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_email_identity_feedback_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put email identity feedback attributes"):
        put_email_identity_feedback_attributes("test-email_identity", region_name=REGION)


def test_put_email_identity_mail_from_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_mail_from_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_mail_from_attributes("test-email_identity", region_name=REGION)
    mock_client.put_email_identity_mail_from_attributes.assert_called_once()


def test_put_email_identity_mail_from_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_email_identity_mail_from_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_email_identity_mail_from_attributes",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put email identity mail from attributes"):
        put_email_identity_mail_from_attributes("test-email_identity", region_name=REGION)


def test_put_suppressed_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_suppressed_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_suppressed_destination("test-email_address", "test-reason", region_name=REGION)
    mock_client.put_suppressed_destination.assert_called_once()


def test_put_suppressed_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_suppressed_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_suppressed_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put suppressed destination"):
        put_suppressed_destination("test-email_address", "test-reason", region_name=REGION)


def test_run_render_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_render_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    run_render_email_template("test-template_name", "test-template_data", region_name=REGION)
    mock_client.test_render_email_template.assert_called_once()


def test_run_render_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_render_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_render_email_template",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run render email template"):
        run_render_email_template("test-template_name", "test-template_data", region_name=REGION)


def test_send_custom_verification_email(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    send_custom_verification_email("test-email_address", "test-template_name", region_name=REGION)
    mock_client.send_custom_verification_email.assert_called_once()


def test_send_custom_verification_email_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_custom_verification_email",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send custom verification email"):
        send_custom_verification_email("test-email_address", "test-template_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_configuration_set_event_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_event_destination.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, region_name=REGION)
    mock_client.update_configuration_set_event_destination.assert_called_once()


def test_update_configuration_set_event_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_set_event_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_set_event_destination",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration set event destination"):
        update_configuration_set_event_destination("test-configuration_set_name", "test-event_destination_name", {}, region_name=REGION)


def test_update_contact_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_list.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_contact_list("test-contact_list_name", region_name=REGION)
    mock_client.update_contact_list.assert_called_once()


def test_update_contact_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_list",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact list"):
        update_contact_list("test-contact_list_name", region_name=REGION)


def test_update_custom_verification_email_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_verification_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)
    mock_client.update_custom_verification_email_template.assert_called_once()


def test_update_custom_verification_email_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_verification_email_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_verification_email_template",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update custom verification email template"):
        update_custom_verification_email_template("test-template_name", "test-from_email_address", "test-template_subject", "test-template_content", "test-success_redirection_url", "test-failure_redirection_url", region_name=REGION)


def test_update_email_identity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_email_identity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", region_name=REGION)
    mock_client.update_email_identity_policy.assert_called_once()


def test_update_email_identity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_email_identity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_email_identity_policy",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update email identity policy"):
        update_email_identity_policy("test-email_identity", "test-policy_name", "test-policy", region_name=REGION)


def test_update_reputation_entity_customer_managed_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_reputation_entity_customer_managed_status.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_reputation_entity_customer_managed_status("test-reputation_entity_type", "test-reputation_entity_reference", "test-sending_status", region_name=REGION)
    mock_client.update_reputation_entity_customer_managed_status.assert_called_once()


def test_update_reputation_entity_customer_managed_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_reputation_entity_customer_managed_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_reputation_entity_customer_managed_status",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update reputation entity customer managed status"):
        update_reputation_entity_customer_managed_status("test-reputation_entity_type", "test-reputation_entity_reference", "test-sending_status", region_name=REGION)


def test_update_reputation_entity_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_reputation_entity_policy.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_reputation_entity_policy("test-reputation_entity_type", "test-reputation_entity_reference", "test-reputation_entity_policy", region_name=REGION)
    mock_client.update_reputation_entity_policy.assert_called_once()


def test_update_reputation_entity_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_reputation_entity_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_reputation_entity_policy",
    )
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update reputation entity policy"):
        update_reputation_entity_policy("test-reputation_entity_type", "test-reputation_entity_reference", "test-reputation_entity_policy", region_name=REGION)


def test_send_bulk_email_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import send_bulk_email
    mock_client = MagicMock()
    mock_client.send_bulk_email.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    send_bulk_email("test-from_email_address", "test-default_content", "test-bulk_entries", configuration_set_name={}, region_name="us-east-1")
    mock_client.send_bulk_email.assert_called_once()

def test_create_email_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_email_identity
    mock_client = MagicMock()
    mock_client.create_email_identity.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_email_identity("test-identity", dkim_signing_attributes="test-dkim_signing_attributes", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_email_identity.assert_called_once()

def test_list_email_identities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_email_identities
    mock_client = MagicMock()
    mock_client.list_email_identities.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_email_identities(page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_email_identities.assert_called_once()

def test_list_configuration_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_configuration_sets
    mock_client = MagicMock()
    mock_client.list_configuration_sets.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_configuration_sets(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_configuration_sets.assert_called_once()

def test_create_email_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_email_template
    mock_client = MagicMock()
    mock_client.create_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_email_template("test-template_name", "test-subject", text="test-text", html="test-html", region_name="us-east-1")
    mock_client.create_email_template.assert_called_once()

def test_list_email_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_email_templates
    mock_client = MagicMock()
    mock_client.list_email_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_email_templates(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_email_templates.assert_called_once()

def test_update_email_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import update_email_template
    mock_client = MagicMock()
    mock_client.update_email_template.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_email_template("test-template_name", "test-subject", text="test-text", html="test-html", region_name="us-east-1")
    mock_client.update_email_template.assert_called_once()

def test_create_contact_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_contact_list
    mock_client = MagicMock()
    mock_client.create_contact_list.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_contact_list("test-contact_list_name", description="test-description", topics="test-topics", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_contact_list.assert_called_once()

def test_list_contact_lists_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_contact_lists
    mock_client = MagicMock()
    mock_client.list_contact_lists.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_contact_lists(page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_contact_lists.assert_called_once()

def test_list_contacts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_contacts
    mock_client = MagicMock()
    mock_client.list_contacts.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_contacts("test-contact_list_name", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_contacts.assert_called_once()

def test_update_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import update_contact
    mock_client = MagicMock()
    mock_client.update_contact.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_contact("test-contact_list_name", "test-email_address", topic_preferences="test-topic_preferences", unsubscribe_all="test-unsubscribe_all", region_name="us-east-1")
    mock_client.update_contact.assert_called_once()

def test_list_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_import_jobs
    mock_client = MagicMock()
    mock_client.list_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_import_jobs(import_destination_type=1, next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_import_jobs.assert_called_once()

def test_create_dedicated_ip_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_dedicated_ip_pool
    mock_client = MagicMock()
    mock_client.create_dedicated_ip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_dedicated_ip_pool("test-pool_name", tags=[{"Key": "k", "Value": "v"}], scaling_mode="test-scaling_mode", region_name="us-east-1")
    mock_client.create_dedicated_ip_pool.assert_called_once()

def test_create_deliverability_test_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_deliverability_test_report
    mock_client = MagicMock()
    mock_client.create_deliverability_test_report.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_deliverability_test_report("test-from_email_address", "test-content", report_name=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_deliverability_test_report.assert_called_once()

def test_create_multi_region_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_multi_region_endpoint
    mock_client = MagicMock()
    mock_client.create_multi_region_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_multi_region_endpoint("test-endpoint_name", "test-details", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_multi_region_endpoint.assert_called_once()

def test_create_tenant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import create_tenant
    mock_client = MagicMock()
    mock_client.create_tenant.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    create_tenant("test-tenant_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_tenant.assert_called_once()

def test_get_dedicated_ips_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import get_dedicated_ips
    mock_client = MagicMock()
    mock_client.get_dedicated_ips.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    get_dedicated_ips(pool_name="test-pool_name", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.get_dedicated_ips.assert_called_once()

def test_list_custom_verification_email_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_custom_verification_email_templates
    mock_client = MagicMock()
    mock_client.list_custom_verification_email_templates.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_custom_verification_email_templates(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_custom_verification_email_templates.assert_called_once()

def test_list_dedicated_ip_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_dedicated_ip_pools
    mock_client = MagicMock()
    mock_client.list_dedicated_ip_pools.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_dedicated_ip_pools(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_dedicated_ip_pools.assert_called_once()

def test_list_deliverability_test_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_deliverability_test_reports
    mock_client = MagicMock()
    mock_client.list_deliverability_test_reports.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_deliverability_test_reports(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_deliverability_test_reports.assert_called_once()

def test_list_domain_deliverability_campaigns_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_domain_deliverability_campaigns
    mock_client = MagicMock()
    mock_client.list_domain_deliverability_campaigns.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_domain_deliverability_campaigns("test-start_date", "test-end_date", "test-subscribed_domain", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_domain_deliverability_campaigns.assert_called_once()

def test_list_export_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_export_jobs
    mock_client = MagicMock()
    mock_client.list_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_export_jobs(next_token="test-next_token", page_size=1, export_source_type=1, job_status="test-job_status", region_name="us-east-1")
    mock_client.list_export_jobs.assert_called_once()

def test_list_multi_region_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_multi_region_endpoints
    mock_client = MagicMock()
    mock_client.list_multi_region_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_multi_region_endpoints(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_multi_region_endpoints.assert_called_once()

def test_list_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_recommendations
    mock_client = MagicMock()
    mock_client.list_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_recommendations(filter="test-filter", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_recommendations.assert_called_once()

def test_list_reputation_entities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_reputation_entities
    mock_client = MagicMock()
    mock_client.list_reputation_entities.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_reputation_entities(filter="test-filter", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_reputation_entities.assert_called_once()

def test_list_resource_tenants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_resource_tenants
    mock_client = MagicMock()
    mock_client.list_resource_tenants.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_resource_tenants("test-resource_arn", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_tenants.assert_called_once()

def test_list_suppressed_destinations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_suppressed_destinations
    mock_client = MagicMock()
    mock_client.list_suppressed_destinations.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_suppressed_destinations(reasons="test-reasons", start_date="test-start_date", end_date="test-end_date", next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_suppressed_destinations.assert_called_once()

def test_list_tenant_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_tenant_resources
    mock_client = MagicMock()
    mock_client.list_tenant_resources.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_tenant_resources("test-tenant_name", filter="test-filter", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tenant_resources.assert_called_once()

def test_list_tenants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import list_tenants
    mock_client = MagicMock()
    mock_client.list_tenants.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    list_tenants(next_token="test-next_token", page_size=1, region_name="us-east-1")
    mock_client.list_tenants.assert_called_once()

def test_put_account_dedicated_ip_warmup_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_account_dedicated_ip_warmup_attributes
    mock_client = MagicMock()
    mock_client.put_account_dedicated_ip_warmup_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_dedicated_ip_warmup_attributes(auto_warmup_enabled=True, region_name="us-east-1")
    mock_client.put_account_dedicated_ip_warmup_attributes.assert_called_once()

def test_put_account_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_account_details
    mock_client = MagicMock()
    mock_client.put_account_details.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_details("test-mail_type", "test-website_url", contact_language="test-contact_language", use_case_description=True, additional_contact_email_addresses="test-additional_contact_email_addresses", production_access_enabled="test-production_access_enabled", region_name="us-east-1")
    mock_client.put_account_details.assert_called_once()

def test_put_account_sending_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_account_sending_attributes
    mock_client = MagicMock()
    mock_client.put_account_sending_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_sending_attributes(sending_enabled="test-sending_enabled", region_name="us-east-1")
    mock_client.put_account_sending_attributes.assert_called_once()

def test_put_account_suppression_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_account_suppression_attributes
    mock_client = MagicMock()
    mock_client.put_account_suppression_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_account_suppression_attributes(suppressed_reasons="test-suppressed_reasons", region_name="us-east-1")
    mock_client.put_account_suppression_attributes.assert_called_once()

def test_put_configuration_set_archiving_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_archiving_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_archiving_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_archiving_options({}, archive_arn="test-archive_arn", region_name="us-east-1")
    mock_client.put_configuration_set_archiving_options.assert_called_once()

def test_put_configuration_set_delivery_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_delivery_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_delivery_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_delivery_options({}, tls_policy="{}", sending_pool_name="test-sending_pool_name", max_delivery_seconds=1, region_name="us-east-1")
    mock_client.put_configuration_set_delivery_options.assert_called_once()

def test_put_configuration_set_reputation_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_reputation_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_reputation_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_reputation_options({}, reputation_metrics_enabled="test-reputation_metrics_enabled", region_name="us-east-1")
    mock_client.put_configuration_set_reputation_options.assert_called_once()

def test_put_configuration_set_sending_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_sending_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_sending_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_sending_options({}, sending_enabled="test-sending_enabled", region_name="us-east-1")
    mock_client.put_configuration_set_sending_options.assert_called_once()

def test_put_configuration_set_suppression_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_suppression_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_suppression_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_suppression_options({}, suppressed_reasons="test-suppressed_reasons", region_name="us-east-1")
    mock_client.put_configuration_set_suppression_options.assert_called_once()

def test_put_configuration_set_tracking_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_tracking_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_tracking_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_tracking_options({}, custom_redirect_domain="test-custom_redirect_domain", https_policy="{}", region_name="us-east-1")
    mock_client.put_configuration_set_tracking_options.assert_called_once()

def test_put_configuration_set_vdm_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_configuration_set_vdm_options
    mock_client = MagicMock()
    mock_client.put_configuration_set_vdm_options.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_configuration_set_vdm_options({}, vdm_options={}, region_name="us-east-1")
    mock_client.put_configuration_set_vdm_options.assert_called_once()

def test_put_deliverability_dashboard_option_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_deliverability_dashboard_option
    mock_client = MagicMock()
    mock_client.put_deliverability_dashboard_option.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_deliverability_dashboard_option("test-dashboard_enabled", subscribed_domains="test-subscribed_domains", region_name="us-east-1")
    mock_client.put_deliverability_dashboard_option.assert_called_once()

def test_put_email_identity_configuration_set_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_email_identity_configuration_set_attributes
    mock_client = MagicMock()
    mock_client.put_email_identity_configuration_set_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_configuration_set_attributes("test-email_identity", configuration_set_name={}, region_name="us-east-1")
    mock_client.put_email_identity_configuration_set_attributes.assert_called_once()

def test_put_email_identity_dkim_signing_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_email_identity_dkim_signing_attributes
    mock_client = MagicMock()
    mock_client.put_email_identity_dkim_signing_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_dkim_signing_attributes("test-email_identity", "test-signing_attributes_origin", signing_attributes="test-signing_attributes", region_name="us-east-1")
    mock_client.put_email_identity_dkim_signing_attributes.assert_called_once()

def test_put_email_identity_feedback_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_email_identity_feedback_attributes
    mock_client = MagicMock()
    mock_client.put_email_identity_feedback_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_feedback_attributes("test-email_identity", email_forwarding_enabled="test-email_forwarding_enabled", region_name="us-east-1")
    mock_client.put_email_identity_feedback_attributes.assert_called_once()

def test_put_email_identity_mail_from_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import put_email_identity_mail_from_attributes
    mock_client = MagicMock()
    mock_client.put_email_identity_mail_from_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    put_email_identity_mail_from_attributes("test-email_identity", mail_from_domain="test-mail_from_domain", behavior_on_mx_failure="test-behavior_on_mx_failure", region_name="us-east-1")
    mock_client.put_email_identity_mail_from_attributes.assert_called_once()

def test_send_custom_verification_email_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import send_custom_verification_email
    mock_client = MagicMock()
    mock_client.send_custom_verification_email.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    send_custom_verification_email("test-email_address", "test-template_name", configuration_set_name={}, region_name="us-east-1")
    mock_client.send_custom_verification_email.assert_called_once()

def test_update_contact_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ses_v2 import update_contact_list
    mock_client = MagicMock()
    mock_client.update_contact_list.return_value = {}
    monkeypatch.setattr("aws_util.ses_v2.get_client", lambda *a, **kw: mock_client)
    update_contact_list("test-contact_list_name", topics="test-topics", description="test-description", region_name="us-east-1")
    mock_client.update_contact_list.assert_called_once()
