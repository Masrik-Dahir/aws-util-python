"""Tests for aws_util.acm module."""
from __future__ import annotations

import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.acm as acm_mod
from aws_util.acm import (
    ACMCertificate,
    list_certificates,
    describe_certificate,
    request_certificate,
    delete_certificate,
    get_certificate_pem,
    wait_for_certificate,
    find_certificate_by_domain,
    add_tags_to_certificate,
    export_certificate,
    get_account_configuration,
    get_certificate,
    import_certificate,
    list_tags_for_certificate,
    put_account_configuration,
    remove_tags_from_certificate,
    renew_certificate,
    resend_validation_email,
    revoke_certificate,
    update_certificate_options,
)

REGION = "us-east-1"
DOMAIN = "api.example.com"


@pytest.fixture
def cert_arn():
    client = boto3.client("acm", region_name=REGION)
    resp = client.request_certificate(
        DomainName=DOMAIN,
        ValidationMethod="DNS",
    )
    return resp["CertificateArn"]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_acm_certificate_model():
    cert = ACMCertificate(
        certificate_arn="arn:aws:acm:us-east-1:123:certificate/abc",
        domain_name=DOMAIN,
        status="ISSUED",
    )
    assert cert.domain_name == DOMAIN
    assert cert.type == "AMAZON_ISSUED"
    assert cert.in_use_by == []


# ---------------------------------------------------------------------------
# list_certificates
# ---------------------------------------------------------------------------

def test_list_certificates_returns_list(cert_arn):
    result = list_certificates(region_name=REGION)
    assert isinstance(result, list)
    assert any(c.certificate_arn == cert_arn for c in result)


def test_list_certificates_with_status_filter(cert_arn):
    result = list_certificates(status_filter=["PENDING_VALIDATION"], region_name=REGION)
    assert isinstance(result, list)


def test_list_certificates_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "ListCertificates"
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_certificates failed"):
        list_certificates(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_certificate
# ---------------------------------------------------------------------------

def test_describe_certificate_found(cert_arn):
    result = describe_certificate(cert_arn, region_name=REGION)
    assert result is not None
    assert result.certificate_arn == cert_arn
    assert result.domain_name == DOMAIN


def test_describe_certificate_not_found(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificate.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DescribeCertificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_certificate("arn:aws:acm:us-east-1:123:certificate/nonexistent", region_name=REGION)
    assert result is None


def test_describe_certificate_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificate.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "DescribeCertificate"
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_certificate failed"):
        describe_certificate("arn:bad", region_name=REGION)


# ---------------------------------------------------------------------------
# request_certificate
# ---------------------------------------------------------------------------

def test_request_certificate_success():
    arn = request_certificate(DOMAIN, region_name=REGION)
    assert "arn:aws:acm" in arn


def test_request_certificate_with_sans():
    arn = request_certificate(
        "*.example.com",
        subject_alternative_names=["example.com", "api.example.com"],
        region_name=REGION,
    )
    assert arn


def test_request_certificate_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.request_certificate.side_effect = ClientError(
        {"Error": {"Code": "InvalidDomainValidationOptionsException", "Message": "bad domain"}},
        "RequestCertificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to request certificate"):
        request_certificate("bad-domain", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_certificate
# ---------------------------------------------------------------------------

def test_delete_certificate_success(cert_arn):
    delete_certificate(cert_arn, region_name=REGION)


def test_delete_certificate_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_certificate.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DeleteCertificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete certificate"):
        delete_certificate("arn:nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# get_certificate_pem
# ---------------------------------------------------------------------------

def test_get_certificate_pem_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_certificate.side_effect = ClientError(
        {"Error": {"Code": "RequestInProgressException", "Message": "not issued yet"}},
        "GetCertificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get certificate PEM"):
        get_certificate_pem("arn:aws:acm:us-east-1:123:certificate/abc", region_name=REGION)


def test_get_certificate_pem_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_certificate.return_value = {
        "Certificate": "-----BEGIN CERTIFICATE-----\nMIIBxx...\n-----END CERTIFICATE-----"
    }
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    pem = get_certificate_pem("arn:aws:acm:us-east-1:123:certificate/abc", region_name=REGION)
    assert pem.startswith("-----BEGIN CERTIFICATE-----")


# ---------------------------------------------------------------------------
# wait_for_certificate
# ---------------------------------------------------------------------------

def test_wait_for_certificate_already_issued(monkeypatch):
    issued = ACMCertificate(
        certificate_arn="arn:...", domain_name=DOMAIN, status="ISSUED"
    )
    monkeypatch.setattr(acm_mod, "describe_certificate", lambda arn, region_name=None: issued)
    result = wait_for_certificate("arn:...", timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.status == "ISSUED"


def test_wait_for_certificate_not_found(monkeypatch):
    monkeypatch.setattr(acm_mod, "describe_certificate", lambda arn, region_name=None: None)
    with pytest.raises(RuntimeError, match="not found during wait"):
        wait_for_certificate("arn:...", timeout=5.0, poll_interval=0.01, region_name=REGION)


def test_wait_for_certificate_failed_status(monkeypatch):
    failed = ACMCertificate(
        certificate_arn="arn:...", domain_name=DOMAIN, status="FAILED"
    )
    monkeypatch.setattr(acm_mod, "describe_certificate", lambda arn, region_name=None: failed)
    with pytest.raises(RuntimeError, match="terminal status"):
        wait_for_certificate("arn:...", timeout=5.0, poll_interval=0.01, region_name=REGION)


def test_wait_for_certificate_timeout(monkeypatch):
    pending = ACMCertificate(
        certificate_arn="arn:...", domain_name=DOMAIN, status="PENDING_VALIDATION"
    )
    monkeypatch.setattr(acm_mod, "describe_certificate", lambda arn, region_name=None: pending)
    with pytest.raises(TimeoutError):
        wait_for_certificate("arn:...", timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# find_certificate_by_domain
# ---------------------------------------------------------------------------

def test_find_certificate_by_domain_found(monkeypatch):
    cert = ACMCertificate(
        certificate_arn="arn:...", domain_name=DOMAIN, status="ISSUED"
    )
    monkeypatch.setattr(acm_mod, "list_certificates", lambda **kw: [cert])
    monkeypatch.setattr(acm_mod, "describe_certificate", lambda arn, region_name=None: cert)
    result = find_certificate_by_domain(DOMAIN, region_name=REGION)
    assert result is not None
    assert result.domain_name == DOMAIN


def test_find_certificate_by_domain_not_found(monkeypatch):
    monkeypatch.setattr(acm_mod, "list_certificates", lambda **kw: [])
    result = find_certificate_by_domain("other.example.com", region_name=REGION)
    assert result is None


def test_wait_for_certificate_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_certificate (line 253)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    import aws_util.acm as acm_mod

    call_count = {"n": 0}

    def fake_describe(arn, region_name=None):
        from aws_util.acm import ACMCertificate
        call_count["n"] += 1
        if call_count["n"] < 2:
            return ACMCertificate(certificate_arn=arn, domain_name="x.example.com", status="PENDING_VALIDATION")
        return ACMCertificate(certificate_arn=arn, domain_name="x.example.com", status="ISSUED")

    monkeypatch.setattr(acm_mod, "describe_certificate", fake_describe)
    from aws_util.acm import wait_for_certificate
    result = wait_for_certificate("arn:cert:1", timeout=10.0, poll_interval=0.001, region_name="us-east-1")
    assert result.status == "ISSUED"


def test_add_tags_to_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    add_tags_to_certificate("test-certificate_arn", [], region_name=REGION)
    mock_client.add_tags_to_certificate.assert_called_once()


def test_add_tags_to_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags to certificate"):
        add_tags_to_certificate("test-certificate_arn", [], region_name=REGION)


def test_export_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    export_certificate("test-certificate_arn", "test-passphrase", region_name=REGION)
    mock_client.export_certificate.assert_called_once()


def test_export_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export certificate"):
        export_certificate("test-certificate_arn", "test-passphrase", region_name=REGION)


def test_get_account_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_configuration.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    get_account_configuration(region_name=REGION)
    mock_client.get_account_configuration.assert_called_once()


def test_get_account_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_configuration",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account configuration"):
        get_account_configuration(region_name=REGION)


def test_get_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    get_certificate("test-certificate_arn", region_name=REGION)
    mock_client.get_certificate.assert_called_once()


def test_get_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get certificate"):
        get_certificate("test-certificate_arn", region_name=REGION)


def test_import_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    import_certificate("test-certificate", "test-private_key", region_name=REGION)
    mock_client.import_certificate.assert_called_once()


def test_import_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import certificate"):
        import_certificate("test-certificate", "test-private_key", region_name=REGION)


def test_list_tags_for_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_certificate("test-certificate_arn", region_name=REGION)
    mock_client.list_tags_for_certificate.assert_called_once()


def test_list_tags_for_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for certificate"):
        list_tags_for_certificate("test-certificate_arn", region_name=REGION)


def test_put_account_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_configuration.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    put_account_configuration("test-idempotency_token", region_name=REGION)
    mock_client.put_account_configuration.assert_called_once()


def test_put_account_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_configuration",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account configuration"):
        put_account_configuration("test-idempotency_token", region_name=REGION)


def test_remove_tags_from_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    remove_tags_from_certificate("test-certificate_arn", [], region_name=REGION)
    mock_client.remove_tags_from_certificate.assert_called_once()


def test_remove_tags_from_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from certificate"):
        remove_tags_from_certificate("test-certificate_arn", [], region_name=REGION)


def test_renew_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.renew_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    renew_certificate("test-certificate_arn", region_name=REGION)
    mock_client.renew_certificate.assert_called_once()


def test_renew_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.renew_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "renew_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to renew certificate"):
        renew_certificate("test-certificate_arn", region_name=REGION)


def test_resend_validation_email(monkeypatch):
    mock_client = MagicMock()
    mock_client.resend_validation_email.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    resend_validation_email("test-certificate_arn", "test-domain", "test-validation_domain", region_name=REGION)
    mock_client.resend_validation_email.assert_called_once()


def test_resend_validation_email_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resend_validation_email.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resend_validation_email",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resend validation email"):
        resend_validation_email("test-certificate_arn", "test-domain", "test-validation_domain", region_name=REGION)


def test_revoke_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_certificate.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    revoke_certificate("test-certificate_arn", "test-revocation_reason", region_name=REGION)
    mock_client.revoke_certificate.assert_called_once()


def test_revoke_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_certificate",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke certificate"):
        revoke_certificate("test-certificate_arn", "test-revocation_reason", region_name=REGION)


def test_update_certificate_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_certificate_options.return_value = {}
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    update_certificate_options("test-certificate_arn", {}, region_name=REGION)
    mock_client.update_certificate_options.assert_called_once()


def test_update_certificate_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_certificate_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_certificate_options",
    )
    monkeypatch.setattr(acm_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update certificate options"):
        update_certificate_options("test-certificate_arn", {}, region_name=REGION)


def test_import_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.acm import import_certificate
    mock_client = MagicMock()
    mock_client.import_certificate.return_value = {}
    monkeypatch.setattr("aws_util.acm.get_client", lambda *a, **kw: mock_client)
    import_certificate("test-certificate", "test-private_key", certificate_arn="test-certificate_arn", certificate_chain="test-certificate_chain", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_certificate.assert_called_once()

def test_put_account_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.acm import put_account_configuration
    mock_client = MagicMock()
    mock_client.put_account_configuration.return_value = {}
    monkeypatch.setattr("aws_util.acm.get_client", lambda *a, **kw: mock_client)
    put_account_configuration("test-idempotency_token", expiry_events="test-expiry_events", region_name="us-east-1")
    mock_client.put_account_configuration.assert_called_once()
