"""Native async ACM utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
from typing import Any

from aws_util.acm import (
    ACMCertificate,
    ExportCertificateResult,
    GetAccountConfigurationResult,
    GetCertificateResult,
    ImportCertificateResult,
    ListTagsForCertificateResult,
    RevokeCertificateResult,
)
from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "ACMCertificate",
    "ExportCertificateResult",
    "GetAccountConfigurationResult",
    "GetCertificateResult",
    "ImportCertificateResult",
    "ListTagsForCertificateResult",
    "RevokeCertificateResult",
    "add_tags_to_certificate",
    "delete_certificate",
    "describe_certificate",
    "export_certificate",
    "find_certificate_by_domain",
    "get_account_configuration",
    "get_certificate",
    "get_certificate_pem",
    "import_certificate",
    "list_certificates",
    "list_tags_for_certificate",
    "put_account_configuration",
    "remove_tags_from_certificate",
    "renew_certificate",
    "request_certificate",
    "resend_validation_email",
    "revoke_certificate",
    "update_certificate_options",
    "wait_for_certificate",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def list_certificates(
    status_filter: list[str] | None = None,
    region_name: str | None = None,
) -> list[ACMCertificate]:
    """List ACM certificates in the account.

    Args:
        status_filter: Filter by certificate status, e.g.
            ``["ISSUED", "PENDING_VALIDATION"]``.  ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ACMCertificate` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    if status_filter:
        kwargs["CertificateStatuses"] = status_filter

    certs: list[ACMCertificate] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("ListCertificates", **kwargs)
            for summary in resp.get("CertificateSummaryList", []):
                certs.append(
                    ACMCertificate(
                        certificate_arn=summary["CertificateArn"],
                        domain_name=summary.get("DomainName", ""),
                        status=summary.get("Status", ""),
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_certificates failed") from exc
    return certs


async def describe_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> ACMCertificate | None:
    """Fetch detailed metadata for a single ACM certificate.

    Args:
        certificate_arn: ARN of the certificate.
        region_name: AWS region override.

    Returns:
        An :class:`ACMCertificate` with full details, or ``None`` if not
        found.

    Raises:
        RuntimeError: If the API call fails for a reason other than not
        found.
    """
    client = async_client("acm", region_name)
    try:
        resp = await client.call(
            "DescribeCertificate",
            CertificateArn=certificate_arn,
        )
    except RuntimeError as exc:
        if "ResourceNotFoundException" in str(exc):
            return None
        raise
    cert = resp["Certificate"]
    return ACMCertificate(
        certificate_arn=cert["CertificateArn"],
        domain_name=cert.get("DomainName", ""),
        status=cert.get("Status", ""),
        type=cert.get("Type", "AMAZON_ISSUED"),
        subject_alternative_names=cert.get("SubjectAlternativeNames", []),
        validation_method=(
            cert.get("DomainValidationOptions", [{}])[0].get("ValidationMethod")
            if cert.get("DomainValidationOptions")
            else None
        ),
        issued_at=cert.get("IssuedAt"),
        not_after=cert.get("NotAfter"),
        key_algorithm=cert.get("KeyAlgorithm"),
        in_use_by=cert.get("InUseBy", []),
    )


async def request_certificate(
    domain_name: str,
    validation_method: str = "DNS",
    subject_alternative_names: list[str] | None = None,
    region_name: str | None = None,
) -> str:
    """Request a new ACM certificate.

    Args:
        domain_name: Primary domain name, e.g. ``"api.example.com"``.
        validation_method: ``"DNS"`` (default) or ``"EMAIL"``.
        subject_alternative_names: Additional domain names to include.
        region_name: AWS region override.

    Returns:
        The ARN of the newly requested certificate.

    Raises:
        RuntimeError: If the request fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {
        "DomainName": domain_name,
        "ValidationMethod": validation_method,
    }
    if subject_alternative_names:
        kwargs["SubjectAlternativeNames"] = subject_alternative_names
    try:
        resp = await client.call("RequestCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to request certificate for {domain_name!r}") from exc
    return resp["CertificateArn"]


async def delete_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete an ACM certificate.

    The certificate must not be in use by any AWS service.

    Args:
        certificate_arn: ARN of the certificate to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("acm", region_name)
    try:
        await client.call(
            "DeleteCertificate",
            CertificateArn=certificate_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete certificate {certificate_arn!r}") from exc


async def get_certificate_pem(
    certificate_arn: str,
    region_name: str | None = None,
) -> str:
    """Export the PEM-encoded certificate body.

    Note: Only works for issued certificates.

    Args:
        certificate_arn: ARN of the certificate.
        region_name: AWS region override.

    Returns:
        The certificate in PEM format.

    Raises:
        RuntimeError: If the export fails.
    """
    client = async_client("acm", region_name)
    try:
        resp = await client.call("GetCertificate", CertificateArn=certificate_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to get certificate PEM for {certificate_arn!r}") from exc
    return resp["Certificate"]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def wait_for_certificate(
    certificate_arn: str,
    poll_interval: float = 15.0,
    timeout: float = 600.0,
    region_name: str | None = None,
) -> ACMCertificate:
    """Poll until an ACM certificate reaches ``ISSUED`` status.

    DNS/email validation must be completed externally before the certificate
    transitions to ISSUED.  Use this after :func:`request_certificate` when
    you need confirmation before attaching the cert to a load balancer or
    CloudFront distribution.

    Args:
        certificate_arn: ARN of the certificate to wait for.
        poll_interval: Seconds between status checks (default ``15``).
        timeout: Maximum seconds to wait (default ``600``).
        region_name: AWS region override.

    Returns:
        The :class:`ACMCertificate` once it reaches ``ISSUED``.

    Raises:
        TimeoutError: If the certificate does not reach ISSUED within
            *timeout*.
        RuntimeError: If the certificate reaches a terminal failure state
            (``FAILED``, ``VALIDATION_TIMED_OUT``, ``REVOKED``) or the
            describe call fails.
    """
    import time as _time

    _FAILED_STATUSES = {
        "FAILED",
        "VALIDATION_TIMED_OUT",
        "REVOKED",
        "INACTIVE",
    }
    deadline = _time.monotonic() + timeout
    while True:
        cert = await describe_certificate(certificate_arn, region_name=region_name)
        if cert is None:
            raise AwsServiceError(f"Certificate {certificate_arn!r} not found during wait")
        if cert.status == "ISSUED":
            return cert
        if cert.status in _FAILED_STATUSES:
            raise AwsServiceError(
                f"Certificate {certificate_arn!r} reached terminal status {cert.status!r}"
            )
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Certificate {certificate_arn!r} did not reach "
                f"ISSUED within {timeout}s "
                f"(current: {cert.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def find_certificate_by_domain(
    domain_name: str,
    status_filter: list[str] | None = None,
    region_name: str | None = None,
) -> ACMCertificate | None:
    """Find an ACM certificate by its primary domain name.

    Calls :func:`list_certificates` and then :func:`describe_certificate`
    on each matching candidate to resolve full details.

    Args:
        domain_name: Primary domain name to search for, e.g.
            ``"api.example.com"`` or ``"*.example.com"``.
        status_filter: Restrict search to these statuses (default: all).
        region_name: AWS region override.

    Returns:
        The first matching :class:`ACMCertificate`, or ``None`` if not
        found.

    Raises:
        RuntimeError: If any API call fails.
    """
    certs = await list_certificates(status_filter=status_filter, region_name=region_name)
    for cert in certs:
        if cert.domain_name == domain_name:
            return await describe_certificate(cert.certificate_arn, region_name=region_name)
    return None


async def add_tags_to_certificate(
    certificate_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags to certificate.

    Args:
        certificate_arn: Certificate arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["Tags"] = tags
    try:
        await client.call("AddTagsToCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags to certificate") from exc
    return None


async def export_certificate(
    certificate_arn: str,
    passphrase: bytes,
    region_name: str | None = None,
) -> ExportCertificateResult:
    """Export certificate.

    Args:
        certificate_arn: Certificate arn.
        passphrase: Passphrase.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["Passphrase"] = passphrase
    try:
        resp = await client.call("ExportCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to export certificate") from exc
    return ExportCertificateResult(
        certificate=resp.get("Certificate"),
        certificate_chain=resp.get("CertificateChain"),
        private_key=resp.get("PrivateKey"),
    )


async def get_account_configuration(
    region_name: str | None = None,
) -> GetAccountConfigurationResult:
    """Get account configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAccountConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account configuration") from exc
    return GetAccountConfigurationResult(
        expiry_events=resp.get("ExpiryEvents"),
    )


async def get_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> GetCertificateResult:
    """Get certificate.

    Args:
        certificate_arn: Certificate arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    try:
        resp = await client.call("GetCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get certificate") from exc
    return GetCertificateResult(
        certificate=resp.get("Certificate"),
        certificate_chain=resp.get("CertificateChain"),
    )


async def import_certificate(
    certificate: bytes,
    private_key: bytes,
    *,
    certificate_arn: str | None = None,
    certificate_chain: bytes | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportCertificateResult:
    """Import certificate.

    Args:
        certificate: Certificate.
        private_key: Private key.
        certificate_arn: Certificate arn.
        certificate_chain: Certificate chain.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Certificate"] = certificate
    kwargs["PrivateKey"] = private_key
    if certificate_arn is not None:
        kwargs["CertificateArn"] = certificate_arn
    if certificate_chain is not None:
        kwargs["CertificateChain"] = certificate_chain
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ImportCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import certificate") from exc
    return ImportCertificateResult(
        certificate_arn=resp.get("CertificateArn"),
    )


async def list_tags_for_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> ListTagsForCertificateResult:
    """List tags for certificate.

    Args:
        certificate_arn: Certificate arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    try:
        resp = await client.call("ListTagsForCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for certificate") from exc
    return ListTagsForCertificateResult(
        tags=resp.get("Tags"),
    )


async def put_account_configuration(
    idempotency_token: str,
    *,
    expiry_events: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put account configuration.

    Args:
        idempotency_token: Idempotency token.
        expiry_events: Expiry events.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdempotencyToken"] = idempotency_token
    if expiry_events is not None:
        kwargs["ExpiryEvents"] = expiry_events
    try:
        await client.call("PutAccountConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account configuration") from exc
    return None


async def remove_tags_from_certificate(
    certificate_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Remove tags from certificate.

    Args:
        certificate_arn: Certificate arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["Tags"] = tags
    try:
        await client.call("RemoveTagsFromCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from certificate") from exc
    return None


async def renew_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> None:
    """Renew certificate.

    Args:
        certificate_arn: Certificate arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    try:
        await client.call("RenewCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to renew certificate") from exc
    return None


async def resend_validation_email(
    certificate_arn: str,
    domain: str,
    validation_domain: str,
    region_name: str | None = None,
) -> None:
    """Resend validation email.

    Args:
        certificate_arn: Certificate arn.
        domain: Domain.
        validation_domain: Validation domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["Domain"] = domain
    kwargs["ValidationDomain"] = validation_domain
    try:
        await client.call("ResendValidationEmail", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resend validation email") from exc
    return None


async def revoke_certificate(
    certificate_arn: str,
    revocation_reason: str,
    region_name: str | None = None,
) -> RevokeCertificateResult:
    """Revoke certificate.

    Args:
        certificate_arn: Certificate arn.
        revocation_reason: Revocation reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["RevocationReason"] = revocation_reason
    try:
        resp = await client.call("RevokeCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to revoke certificate") from exc
    return RevokeCertificateResult(
        certificate_arn=resp.get("CertificateArn"),
    )


async def update_certificate_options(
    certificate_arn: str,
    options: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update certificate options.

    Args:
        certificate_arn: Certificate arn.
        options: Options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("acm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    kwargs["Options"] = options
    try:
        await client.call("UpdateCertificateOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update certificate options") from exc
    return None
