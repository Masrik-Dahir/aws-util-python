"""Native async Amazon Inspector utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.inspector import (
    AccountStatusResult,
    AssociateMemberResult,
    BatchAssociateCodeSecurityScanConfigurationResult,
    BatchDisassociateCodeSecurityScanConfigurationResult,
    BatchGetCodeSnippetResult,
    BatchGetFindingDetailsResult,
    BatchGetFreeTrialInfoResult,
    BatchGetMemberEc2DeepInspectionStatusResult,
    BatchUpdateMemberEc2DeepInspectionStatusResult,
    CancelFindingsReportResult,
    CancelSbomExportResult,
    ConfigurationResult,
    CoverageResult,
    CreateCisScanConfigurationResult,
    CreateCodeSecurityIntegrationResult,
    CreateCodeSecurityScanConfigurationResult,
    CreateFilterResult,
    DeleteCisScanConfigurationResult,
    DeleteCodeSecurityIntegrationResult,
    DeleteCodeSecurityScanConfigurationResult,
    DeleteFilterResult,
    DescribeOrganizationConfigurationResult,
    DisableDelegatedAdminAccountResult,
    DisassociateMemberResult,
    EnableDelegatedAdminAccountResult,
    FindingResult,
    GetCisScanReportResult,
    GetCisScanResultDetailsResult,
    GetClustersForImageResult,
    GetCodeSecurityIntegrationResult,
    GetCodeSecurityScanConfigurationResult,
    GetCodeSecurityScanResult,
    GetDelegatedAdminAccountResult,
    GetEc2DeepInspectionConfigurationResult,
    GetEncryptionKeyResult,
    ListAccountPermissionsResult,
    ListCisScanConfigurationsResult,
    ListCisScanResultsAggregatedByChecksResult,
    ListCisScanResultsAggregatedByTargetResourceResult,
    ListCisScansResult,
    ListCodeSecurityIntegrationsResult,
    ListCodeSecurityScanConfigurationAssociationsResult,
    ListCodeSecurityScanConfigurationsResult,
    ListCoverageStatisticsResult,
    ListDelegatedAdminAccountsResult,
    ListFiltersResult,
    ListTagsForResourceResult,
    ListUsageTotalsResult,
    MemberResult,
    ReportStatusResult,
    SbomExportResult,
    SearchVulnerabilitiesResult,
    StartCodeSecurityScanResult,
    UpdateCisScanConfigurationResult,
    UpdateCodeSecurityIntegrationResult,
    UpdateCodeSecurityScanConfigurationResult,
    UpdateEc2DeepInspectionConfigurationResult,
    UpdateFilterResult,
    UpdateOrganizationConfigurationResult,
    _parse_account_status,
    _parse_coverage,
    _parse_finding,
    _parse_member,
)

__all__ = [
    "AccountStatusResult",
    "AssociateMemberResult",
    "BatchAssociateCodeSecurityScanConfigurationResult",
    "BatchDisassociateCodeSecurityScanConfigurationResult",
    "BatchGetCodeSnippetResult",
    "BatchGetFindingDetailsResult",
    "BatchGetFreeTrialInfoResult",
    "BatchGetMemberEc2DeepInspectionStatusResult",
    "BatchUpdateMemberEc2DeepInspectionStatusResult",
    "CancelFindingsReportResult",
    "CancelSbomExportResult",
    "ConfigurationResult",
    "CoverageResult",
    "CreateCisScanConfigurationResult",
    "CreateCodeSecurityIntegrationResult",
    "CreateCodeSecurityScanConfigurationResult",
    "CreateFilterResult",
    "DeleteCisScanConfigurationResult",
    "DeleteCodeSecurityIntegrationResult",
    "DeleteCodeSecurityScanConfigurationResult",
    "DeleteFilterResult",
    "DescribeOrganizationConfigurationResult",
    "DisableDelegatedAdminAccountResult",
    "DisassociateMemberResult",
    "EnableDelegatedAdminAccountResult",
    "FindingResult",
    "GetCisScanReportResult",
    "GetCisScanResultDetailsResult",
    "GetClustersForImageResult",
    "GetCodeSecurityIntegrationResult",
    "GetCodeSecurityScanConfigurationResult",
    "GetCodeSecurityScanResult",
    "GetDelegatedAdminAccountResult",
    "GetEc2DeepInspectionConfigurationResult",
    "GetEncryptionKeyResult",
    "ListAccountPermissionsResult",
    "ListCisScanConfigurationsResult",
    "ListCisScanResultsAggregatedByChecksResult",
    "ListCisScanResultsAggregatedByTargetResourceResult",
    "ListCisScansResult",
    "ListCodeSecurityIntegrationsResult",
    "ListCodeSecurityScanConfigurationAssociationsResult",
    "ListCodeSecurityScanConfigurationsResult",
    "ListCoverageStatisticsResult",
    "ListDelegatedAdminAccountsResult",
    "ListFiltersResult",
    "ListTagsForResourceResult",
    "ListUsageTotalsResult",
    "MemberResult",
    "ReportStatusResult",
    "SbomExportResult",
    "SearchVulnerabilitiesResult",
    "StartCodeSecurityScanResult",
    "UpdateCisScanConfigurationResult",
    "UpdateCodeSecurityIntegrationResult",
    "UpdateCodeSecurityScanConfigurationResult",
    "UpdateEc2DeepInspectionConfigurationResult",
    "UpdateFilterResult",
    "UpdateOrganizationConfigurationResult",
    "associate_member",
    "batch_associate_code_security_scan_configuration",
    "batch_disassociate_code_security_scan_configuration",
    "batch_get_account_status",
    "batch_get_code_snippet",
    "batch_get_finding_details",
    "batch_get_free_trial_info",
    "batch_get_member_ec2_deep_inspection_status",
    "batch_update_member_ec2_deep_inspection_status",
    "cancel_findings_report",
    "cancel_sbom_export",
    "create_cis_scan_configuration",
    "create_code_security_integration",
    "create_code_security_scan_configuration",
    "create_filter",
    "create_findings_report",
    "create_sbom_export",
    "delete_cis_scan_configuration",
    "delete_code_security_integration",
    "delete_code_security_scan_configuration",
    "delete_filter",
    "describe_organization_configuration",
    "disable",
    "disable_delegated_admin_account",
    "disassociate_member",
    "enable",
    "enable_delegated_admin_account",
    "get_cis_scan_report",
    "get_cis_scan_result_details",
    "get_clusters_for_image",
    "get_code_security_integration",
    "get_code_security_scan",
    "get_code_security_scan_configuration",
    "get_configuration",
    "get_delegated_admin_account",
    "get_ec2_deep_inspection_configuration",
    "get_encryption_key",
    "get_findings_report_status",
    "get_member",
    "get_sbom_export",
    "list_account_permissions",
    "list_cis_scan_configurations",
    "list_cis_scan_results_aggregated_by_checks",
    "list_cis_scan_results_aggregated_by_target_resource",
    "list_cis_scans",
    "list_code_security_integrations",
    "list_code_security_scan_configuration_associations",
    "list_code_security_scan_configurations",
    "list_coverage",
    "list_coverage_statistics",
    "list_delegated_admin_accounts",
    "list_filters",
    "list_finding_aggregations",
    "list_findings",
    "list_members",
    "list_tags_for_resource",
    "list_usage_totals",
    "reset_encryption_key",
    "search_vulnerabilities",
    "send_cis_session_health",
    "send_cis_session_telemetry",
    "start_cis_session",
    "start_code_security_scan",
    "stop_cis_session",
    "tag_resource",
    "untag_resource",
    "update_cis_scan_configuration",
    "update_code_security_integration",
    "update_code_security_scan_configuration",
    "update_configuration",
    "update_ec2_deep_inspection_configuration",
    "update_encryption_key",
    "update_filter",
    "update_org_ec2_deep_inspection_configuration",
    "update_organization_configuration",
]


async def enable(
    resource_types: list[str],
    *,
    account_ids: list[str] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Enable Amazon Inspector for the specified resource types.

    Args:
        resource_types: List of resource types.
        account_ids: Account IDs to enable.
        client_token: Idempotency token.
        region_name: AWS region override.

    Returns:
        A dict with ``accounts`` and ``failedAccounts`` lists.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {"resourceTypes": resource_types}
    if account_ids:
        kwargs["accountIds"] = account_ids
    if client_token:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("Enable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "enable failed") from exc
    return {
        "accounts": resp.get("accounts", []),
        "failedAccounts": resp.get("failedAccounts", []),
    }


async def disable(
    resource_types: list[str],
    *,
    account_ids: list[str] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Disable Amazon Inspector for the specified resource types.

    Args:
        resource_types: List of resource types.
        account_ids: Account IDs to disable.
        region_name: AWS region override.

    Returns:
        A dict with ``accounts`` and ``failedAccounts`` lists.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {"resourceTypes": resource_types}
    if account_ids:
        kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("Disable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "disable failed") from exc
    return {
        "accounts": resp.get("accounts", []),
        "failedAccounts": resp.get("failedAccounts", []),
    }


async def get_configuration(
    *,
    region_name: str | None = None,
) -> ConfigurationResult:
    """Get the current Inspector configuration.

    Args:
        region_name: AWS region override.

    Returns:
        A :class:`ConfigurationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    try:
        resp = await client.call("GetConfiguration")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_configuration failed") from exc
    return ConfigurationResult(
        ecr_configuration=resp.get("ecrConfiguration", {}),
        ec2_configuration=resp.get("ec2Configuration", {}),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "ecrConfiguration",
                "ec2Configuration",
                "ResponseMetadata",
            }
        },
    )


async def update_configuration(
    *,
    ecr_configuration: dict[str, Any] | None = None,
    ec2_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update the Inspector configuration.

    Args:
        ecr_configuration: ECR scanning configuration.
        ec2_configuration: EC2 scanning configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if ecr_configuration is not None:
        kwargs["ecrConfiguration"] = ecr_configuration
    if ec2_configuration is not None:
        kwargs["ec2Configuration"] = ec2_configuration
    try:
        await client.call("UpdateConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "update_configuration failed") from exc


async def batch_get_account_status(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[AccountStatusResult]:
    """Get Inspector status for multiple accounts.

    Args:
        account_ids: List of AWS account IDs.
        region_name: AWS region override.

    Returns:
        A list of :class:`AccountStatusResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    try:
        resp = await client.call("BatchGetAccountStatus", accountIds=account_ids)
    except Exception as exc:
        raise wrap_aws_error(exc, "batch_get_account_status failed") from exc
    return [_parse_account_status(a) for a in resp.get("accounts", [])]


async def list_findings(
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[FindingResult]:
    """List Inspector findings.

    Args:
        filter_criteria: Filter criteria dict.
        sort_criteria: Sort criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria:
        kwargs["filterCriteria"] = filter_criteria
    if sort_criteria:
        kwargs["sortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[FindingResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListFindings", **kwargs)
            for f in resp.get("findings", []):
                results.append(_parse_finding(f))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_findings failed") from exc
    return results


async def list_finding_aggregations(
    aggregation_type: str,
    *,
    aggregation_request: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List finding aggregations.

    Args:
        aggregation_type: Type of aggregation.
        aggregation_request: Optional aggregation request dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of aggregation response dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {"aggregationType": aggregation_type}
    if aggregation_request:
        kwargs["aggregationRequest"] = aggregation_request
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[dict[str, Any]] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListFindingAggregations", **kwargs)
            results.extend(resp.get("responses", []))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_finding_aggregations failed") from exc
    return results


async def get_findings_report_status(
    report_id: str,
    *,
    region_name: str | None = None,
) -> ReportStatusResult:
    """Get the status of a findings report.

    Args:
        report_id: The report identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ReportStatusResult` with report status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    try:
        resp = await client.call("GetFindingsReportStatus", reportId=report_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_findings_report_status failed for {report_id!r}",
        ) from exc
    return ReportStatusResult(
        report_id=resp.get("reportId", ""),
        status=resp.get("status", ""),
        error_code=resp.get("errorCode", ""),
        error_message=resp.get("errorMessage", ""),
        destination=resp.get("destination", {}),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "reportId",
                "status",
                "errorCode",
                "errorMessage",
                "destination",
                "ResponseMetadata",
            }
        },
    )


async def create_findings_report(
    *,
    report_format: str,
    s3_destination: dict[str, Any],
    filter_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a findings report.

    Args:
        report_format: ``CSV`` or ``JSON``.
        s3_destination: S3 destination dict.
        filter_criteria: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        The report ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {
        "reportFormat": report_format,
        "s3Destination": s3_destination,
    }
    if filter_criteria:
        kwargs["filterCriteria"] = filter_criteria
    try:
        resp = await client.call("CreateFindingsReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_findings_report failed") from exc
    return resp.get("reportId", "")


async def get_sbom_export(
    report_id: str,
    *,
    region_name: str | None = None,
) -> SbomExportResult:
    """Get the status of an SBOM export.

    Args:
        report_id: The export identifier.
        region_name: AWS region override.

    Returns:
        A :class:`SbomExportResult` with export status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    try:
        resp = await client.call("GetSbomExport", reportId=report_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_sbom_export failed for {report_id!r}") from exc
    return SbomExportResult(
        report_id=resp.get("reportId", ""),
        status=resp.get("status", ""),
        error_code=resp.get("errorCode", ""),
        error_message=resp.get("errorMessage", ""),
        s3_destination=resp.get("s3Destination", {}),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "reportId",
                "status",
                "errorCode",
                "errorMessage",
                "s3Destination",
                "ResponseMetadata",
            }
        },
    )


async def create_sbom_export(
    *,
    report_format: str,
    s3_destination: dict[str, Any],
    resource_filter_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Create an SBOM export.

    Args:
        report_format: ``CYCLONEDX_1_4`` or ``SPDX_2_3``.
        s3_destination: S3 destination dict.
        resource_filter_criteria: Optional filter criteria.
        region_name: AWS region override.

    Returns:
        The export report ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {
        "reportFormat": report_format,
        "s3Destination": s3_destination,
    }
    if resource_filter_criteria:
        kwargs["resourceFilterCriteria"] = resource_filter_criteria
    try:
        resp = await client.call("CreateSbomExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_sbom_export failed") from exc
    return resp.get("reportId", "")


async def list_coverage(
    *,
    filter_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[CoverageResult]:
    """List Inspector coverage for resources.

    Args:
        filter_criteria: Filter criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`CoverageResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria:
        kwargs["filterCriteria"] = filter_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[CoverageResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListCoverage", **kwargs)
            for c in resp.get("coveredResources", []):
                results.append(_parse_coverage(c))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_coverage failed") from exc
    return results


async def list_members(
    *,
    only_associated: bool = True,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[MemberResult]:
    """List Inspector member accounts.

    Args:
        only_associated: If ``True``, only return associated members.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {"onlyAssociated": only_associated}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[MemberResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListMembers", **kwargs)
            for m in resp.get("members", []):
                results.append(_parse_member(m))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_members failed") from exc
    return results


async def get_member(
    account_id: str,
    *,
    region_name: str | None = None,
) -> MemberResult:
    """Get details for a specific member account.

    Args:
        account_id: AWS account ID.
        region_name: AWS region override.

    Returns:
        A :class:`MemberResult` with member details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    try:
        resp = await client.call("GetMember", accountId=account_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_member failed for {account_id!r}") from exc
    return _parse_member(resp.get("member", {}))


async def associate_member(
    account_id: str,
    region_name: str | None = None,
) -> AssociateMemberResult:
    """Associate member.

    Args:
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountId"] = account_id
    try:
        resp = await client.call("AssociateMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate member") from exc
    return AssociateMemberResult(
        account_id=resp.get("accountId"),
    )


async def batch_associate_code_security_scan_configuration(
    associate_configuration_requests: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchAssociateCodeSecurityScanConfigurationResult:
    """Batch associate code security scan configuration.

    Args:
        associate_configuration_requests: Associate configuration requests.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["associateConfigurationRequests"] = associate_configuration_requests
    try:
        resp = await client.call("BatchAssociateCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch associate code security scan configuration"
        ) from exc
    return BatchAssociateCodeSecurityScanConfigurationResult(
        failed_associations=resp.get("failedAssociations"),
        successful_associations=resp.get("successfulAssociations"),
    )


async def batch_disassociate_code_security_scan_configuration(
    disassociate_configuration_requests: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchDisassociateCodeSecurityScanConfigurationResult:
    """Batch disassociate code security scan configuration.

    Args:
        disassociate_configuration_requests: Disassociate configuration requests.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["disassociateConfigurationRequests"] = disassociate_configuration_requests
    try:
        resp = await client.call("BatchDisassociateCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch disassociate code security scan configuration"
        ) from exc
    return BatchDisassociateCodeSecurityScanConfigurationResult(
        failed_associations=resp.get("failedAssociations"),
        successful_associations=resp.get("successfulAssociations"),
    )


async def batch_get_code_snippet(
    finding_arns: list[str],
    region_name: str | None = None,
) -> BatchGetCodeSnippetResult:
    """Batch get code snippet.

    Args:
        finding_arns: Finding arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingArns"] = finding_arns
    try:
        resp = await client.call("BatchGetCodeSnippet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get code snippet") from exc
    return BatchGetCodeSnippetResult(
        code_snippet_results=resp.get("codeSnippetResults"),
        errors=resp.get("errors"),
    )


async def batch_get_finding_details(
    finding_arns: list[str],
    region_name: str | None = None,
) -> BatchGetFindingDetailsResult:
    """Batch get finding details.

    Args:
        finding_arns: Finding arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingArns"] = finding_arns
    try:
        resp = await client.call("BatchGetFindingDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get finding details") from exc
    return BatchGetFindingDetailsResult(
        finding_details=resp.get("findingDetails"),
        errors=resp.get("errors"),
    )


async def batch_get_free_trial_info(
    account_ids: list[str],
    region_name: str | None = None,
) -> BatchGetFreeTrialInfoResult:
    """Batch get free trial info.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("BatchGetFreeTrialInfo", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get free trial info") from exc
    return BatchGetFreeTrialInfoResult(
        accounts=resp.get("accounts"),
        failed_accounts=resp.get("failedAccounts"),
    )


async def batch_get_member_ec2_deep_inspection_status(
    *,
    account_ids: list[str] | None = None,
    region_name: str | None = None,
) -> BatchGetMemberEc2DeepInspectionStatusResult:
    """Batch get member ec2 deep inspection status.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if account_ids is not None:
        kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("BatchGetMemberEc2DeepInspectionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get member ec2 deep inspection status") from exc
    return BatchGetMemberEc2DeepInspectionStatusResult(
        account_ids=resp.get("accountIds"),
        failed_account_ids=resp.get("failedAccountIds"),
    )


async def batch_update_member_ec2_deep_inspection_status(
    account_ids: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchUpdateMemberEc2DeepInspectionStatusResult:
    """Batch update member ec2 deep inspection status.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("BatchUpdateMemberEc2DeepInspectionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch update member ec2 deep inspection status"
        ) from exc
    return BatchUpdateMemberEc2DeepInspectionStatusResult(
        account_ids=resp.get("accountIds"),
        failed_account_ids=resp.get("failedAccountIds"),
    )


async def cancel_findings_report(
    report_id: str,
    region_name: str | None = None,
) -> CancelFindingsReportResult:
    """Cancel findings report.

    Args:
        report_id: Report id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportId"] = report_id
    try:
        resp = await client.call("CancelFindingsReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel findings report") from exc
    return CancelFindingsReportResult(
        report_id=resp.get("reportId"),
    )


async def cancel_sbom_export(
    report_id: str,
    region_name: str | None = None,
) -> CancelSbomExportResult:
    """Cancel sbom export.

    Args:
        report_id: Report id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportId"] = report_id
    try:
        resp = await client.call("CancelSbomExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel sbom export") from exc
    return CancelSbomExportResult(
        report_id=resp.get("reportId"),
    )


async def create_cis_scan_configuration(
    scan_name: str,
    security_level: str,
    schedule: dict[str, Any],
    targets: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCisScanConfigurationResult:
    """Create cis scan configuration.

    Args:
        scan_name: Scan name.
        security_level: Security level.
        schedule: Schedule.
        targets: Targets.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanName"] = scan_name
    kwargs["securityLevel"] = security_level
    kwargs["schedule"] = schedule
    kwargs["targets"] = targets
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCisScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cis scan configuration") from exc
    return CreateCisScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def create_code_security_integration(
    name: str,
    type_value: str,
    *,
    details: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCodeSecurityIntegrationResult:
    """Create code security integration.

    Args:
        name: Name.
        type_value: Type value.
        details: Details.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["type"] = type_value
    if details is not None:
        kwargs["details"] = details
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCodeSecurityIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create code security integration") from exc
    return CreateCodeSecurityIntegrationResult(
        integration_arn=resp.get("integrationArn"),
        status=resp.get("status"),
        authorization_url=resp.get("authorizationUrl"),
    )


async def create_code_security_scan_configuration(
    name: str,
    level: str,
    configuration: dict[str, Any],
    *,
    scope_settings: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCodeSecurityScanConfigurationResult:
    """Create code security scan configuration.

    Args:
        name: Name.
        level: Level.
        configuration: Configuration.
        scope_settings: Scope settings.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["level"] = level
    kwargs["configuration"] = configuration
    if scope_settings is not None:
        kwargs["scopeSettings"] = scope_settings
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create code security scan configuration") from exc
    return CreateCodeSecurityScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def create_filter(
    action: str,
    filter_criteria: dict[str, Any],
    name: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    reason: str | None = None,
    region_name: str | None = None,
) -> CreateFilterResult:
    """Create filter.

    Args:
        action: Action.
        filter_criteria: Filter criteria.
        name: Name.
        description: Description.
        tags: Tags.
        reason: Reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["action"] = action
    kwargs["filterCriteria"] = filter_criteria
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    if reason is not None:
        kwargs["reason"] = reason
    try:
        resp = await client.call("CreateFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create filter") from exc
    return CreateFilterResult(
        arn=resp.get("arn"),
    )


async def delete_cis_scan_configuration(
    scan_configuration_arn: str,
    region_name: str | None = None,
) -> DeleteCisScanConfigurationResult:
    """Delete cis scan configuration.

    Args:
        scan_configuration_arn: Scan configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    try:
        resp = await client.call("DeleteCisScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cis scan configuration") from exc
    return DeleteCisScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def delete_code_security_integration(
    integration_arn: str,
    region_name: str | None = None,
) -> DeleteCodeSecurityIntegrationResult:
    """Delete code security integration.

    Args:
        integration_arn: Integration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["integrationArn"] = integration_arn
    try:
        resp = await client.call("DeleteCodeSecurityIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete code security integration") from exc
    return DeleteCodeSecurityIntegrationResult(
        integration_arn=resp.get("integrationArn"),
    )


async def delete_code_security_scan_configuration(
    scan_configuration_arn: str,
    region_name: str | None = None,
) -> DeleteCodeSecurityScanConfigurationResult:
    """Delete code security scan configuration.

    Args:
        scan_configuration_arn: Scan configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    try:
        resp = await client.call("DeleteCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete code security scan configuration") from exc
    return DeleteCodeSecurityScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def delete_filter(
    arn: str,
    region_name: str | None = None,
) -> DeleteFilterResult:
    """Delete filter.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = await client.call("DeleteFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete filter") from exc
    return DeleteFilterResult(
        arn=resp.get("arn"),
    )


async def describe_organization_configuration(
    region_name: str | None = None,
) -> DescribeOrganizationConfigurationResult:
    """Describe organization configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("autoEnable"),
        max_account_limit_reached=resp.get("maxAccountLimitReached"),
    )


async def disable_delegated_admin_account(
    delegated_admin_account_id: str,
    region_name: str | None = None,
) -> DisableDelegatedAdminAccountResult:
    """Disable delegated admin account.

    Args:
        delegated_admin_account_id: Delegated admin account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["delegatedAdminAccountId"] = delegated_admin_account_id
    try:
        resp = await client.call("DisableDelegatedAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable delegated admin account") from exc
    return DisableDelegatedAdminAccountResult(
        delegated_admin_account_id=resp.get("delegatedAdminAccountId"),
    )


async def disassociate_member(
    account_id: str,
    region_name: str | None = None,
) -> DisassociateMemberResult:
    """Disassociate member.

    Args:
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountId"] = account_id
    try:
        resp = await client.call("DisassociateMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate member") from exc
    return DisassociateMemberResult(
        account_id=resp.get("accountId"),
    )


async def enable_delegated_admin_account(
    delegated_admin_account_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> EnableDelegatedAdminAccountResult:
    """Enable delegated admin account.

    Args:
        delegated_admin_account_id: Delegated admin account id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["delegatedAdminAccountId"] = delegated_admin_account_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("EnableDelegatedAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable delegated admin account") from exc
    return EnableDelegatedAdminAccountResult(
        delegated_admin_account_id=resp.get("delegatedAdminAccountId"),
    )


async def get_cis_scan_report(
    scan_arn: str,
    *,
    target_accounts: list[str] | None = None,
    report_format: str | None = None,
    region_name: str | None = None,
) -> GetCisScanReportResult:
    """Get cis scan report.

    Args:
        scan_arn: Scan arn.
        target_accounts: Target accounts.
        report_format: Report format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanArn"] = scan_arn
    if target_accounts is not None:
        kwargs["targetAccounts"] = target_accounts
    if report_format is not None:
        kwargs["reportFormat"] = report_format
    try:
        resp = await client.call("GetCisScanReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cis scan report") from exc
    return GetCisScanReportResult(
        url=resp.get("url"),
        status=resp.get("status"),
    )


async def get_cis_scan_result_details(
    scan_arn: str,
    target_resource_id: str,
    account_id: str,
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetCisScanResultDetailsResult:
    """Get cis scan result details.

    Args:
        scan_arn: Scan arn.
        target_resource_id: Target resource id.
        account_id: Account id.
        filter_criteria: Filter criteria.
        sort_by: Sort by.
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanArn"] = scan_arn
    kwargs["targetResourceId"] = target_resource_id
    kwargs["accountId"] = account_id
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("GetCisScanResultDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cis scan result details") from exc
    return GetCisScanResultDetailsResult(
        scan_result_details=resp.get("scanResultDetails"),
        next_token=resp.get("nextToken"),
    )


async def get_clusters_for_image(
    filter: dict[str, Any],
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetClustersForImageResult:
    """Get clusters for image.

    Args:
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("GetClustersForImage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get clusters for image") from exc
    return GetClustersForImageResult(
        cluster=resp.get("cluster"),
        next_token=resp.get("nextToken"),
    )


async def get_code_security_integration(
    integration_arn: str,
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetCodeSecurityIntegrationResult:
    """Get code security integration.

    Args:
        integration_arn: Integration arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["integrationArn"] = integration_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("GetCodeSecurityIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get code security integration") from exc
    return GetCodeSecurityIntegrationResult(
        integration_arn=resp.get("integrationArn"),
        name=resp.get("name"),
        type_value=resp.get("type"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        created_on=resp.get("createdOn"),
        last_update_on=resp.get("lastUpdateOn"),
        tags=resp.get("tags"),
        authorization_url=resp.get("authorizationUrl"),
    )


async def get_code_security_scan(
    resource: dict[str, Any],
    scan_id: str,
    region_name: str | None = None,
) -> GetCodeSecurityScanResult:
    """Get code security scan.

    Args:
        resource: Resource.
        scan_id: Scan id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resource"] = resource
    kwargs["scanId"] = scan_id
    try:
        resp = await client.call("GetCodeSecurityScan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get code security scan") from exc
    return GetCodeSecurityScanResult(
        scan_id=resp.get("scanId"),
        resource=resp.get("resource"),
        account_id=resp.get("accountId"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        created_at=resp.get("createdAt"),
        updated_at=resp.get("updatedAt"),
        last_commit_id=resp.get("lastCommitId"),
    )


async def get_code_security_scan_configuration(
    scan_configuration_arn: str,
    region_name: str | None = None,
) -> GetCodeSecurityScanConfigurationResult:
    """Get code security scan configuration.

    Args:
        scan_configuration_arn: Scan configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    try:
        resp = await client.call("GetCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get code security scan configuration") from exc
    return GetCodeSecurityScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
        name=resp.get("name"),
        configuration=resp.get("configuration"),
        level=resp.get("level"),
        scope_settings=resp.get("scopeSettings"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
        tags=resp.get("tags"),
    )


async def get_delegated_admin_account(
    region_name: str | None = None,
) -> GetDelegatedAdminAccountResult:
    """Get delegated admin account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetDelegatedAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get delegated admin account") from exc
    return GetDelegatedAdminAccountResult(
        delegated_admin=resp.get("delegatedAdmin"),
    )


async def get_ec2_deep_inspection_configuration(
    region_name: str | None = None,
) -> GetEc2DeepInspectionConfigurationResult:
    """Get ec2 deep inspection configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetEc2DeepInspectionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ec2 deep inspection configuration") from exc
    return GetEc2DeepInspectionConfigurationResult(
        package_paths=resp.get("packagePaths"),
        org_package_paths=resp.get("orgPackagePaths"),
        status=resp.get("status"),
        error_message=resp.get("errorMessage"),
    )


async def get_encryption_key(
    scan_type: str,
    resource_type: str,
    region_name: str | None = None,
) -> GetEncryptionKeyResult:
    """Get encryption key.

    Args:
        scan_type: Scan type.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanType"] = scan_type
    kwargs["resourceType"] = resource_type
    try:
        resp = await client.call("GetEncryptionKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get encryption key") from exc
    return GetEncryptionKeyResult(
        kms_key_id=resp.get("kmsKeyId"),
    )


async def list_account_permissions(
    *,
    service: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAccountPermissionsResult:
    """List account permissions.

    Args:
        service: Service.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if service is not None:
        kwargs["service"] = service
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAccountPermissions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account permissions") from exc
    return ListAccountPermissionsResult(
        permissions=resp.get("permissions"),
        next_token=resp.get("nextToken"),
    )


async def list_cis_scan_configurations(
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCisScanConfigurationsResult:
    """List cis scan configurations.

    Args:
        filter_criteria: Filter criteria.
        sort_by: Sort by.
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCisScanConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cis scan configurations") from exc
    return ListCisScanConfigurationsResult(
        scan_configurations=resp.get("scanConfigurations"),
        next_token=resp.get("nextToken"),
    )


async def list_cis_scan_results_aggregated_by_checks(
    scan_arn: str,
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCisScanResultsAggregatedByChecksResult:
    """List cis scan results aggregated by checks.

    Args:
        scan_arn: Scan arn.
        filter_criteria: Filter criteria.
        sort_by: Sort by.
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanArn"] = scan_arn
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCisScanResultsAggregatedByChecks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cis scan results aggregated by checks") from exc
    return ListCisScanResultsAggregatedByChecksResult(
        check_aggregations=resp.get("checkAggregations"),
        next_token=resp.get("nextToken"),
    )


async def list_cis_scan_results_aggregated_by_target_resource(
    scan_arn: str,
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCisScanResultsAggregatedByTargetResourceResult:
    """List cis scan results aggregated by target resource.

    Args:
        scan_arn: Scan arn.
        filter_criteria: Filter criteria.
        sort_by: Sort by.
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanArn"] = scan_arn
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCisScanResultsAggregatedByTargetResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list cis scan results aggregated by target resource"
        ) from exc
    return ListCisScanResultsAggregatedByTargetResourceResult(
        target_resource_aggregations=resp.get("targetResourceAggregations"),
        next_token=resp.get("nextToken"),
    )


async def list_cis_scans(
    *,
    filter_criteria: dict[str, Any] | None = None,
    detail_level: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCisScansResult:
    """List cis scans.

    Args:
        filter_criteria: Filter criteria.
        detail_level: Detail level.
        sort_by: Sort by.
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if detail_level is not None:
        kwargs["detailLevel"] = detail_level
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCisScans", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cis scans") from exc
    return ListCisScansResult(
        scans=resp.get("scans"),
        next_token=resp.get("nextToken"),
    )


async def list_code_security_integrations(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCodeSecurityIntegrationsResult:
    """List code security integrations.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCodeSecurityIntegrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list code security integrations") from exc
    return ListCodeSecurityIntegrationsResult(
        integrations=resp.get("integrations"),
        next_token=resp.get("nextToken"),
    )


async def list_code_security_scan_configuration_associations(
    scan_configuration_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCodeSecurityScanConfigurationAssociationsResult:
    """List code security scan configuration associations.

    Args:
        scan_configuration_arn: Scan configuration arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCodeSecurityScanConfigurationAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list code security scan configuration associations"
        ) from exc
    return ListCodeSecurityScanConfigurationAssociationsResult(
        associations=resp.get("associations"),
        next_token=resp.get("nextToken"),
    )


async def list_code_security_scan_configurations(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCodeSecurityScanConfigurationsResult:
    """List code security scan configurations.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCodeSecurityScanConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list code security scan configurations") from exc
    return ListCodeSecurityScanConfigurationsResult(
        configurations=resp.get("configurations"),
        next_token=resp.get("nextToken"),
    )


async def list_coverage_statistics(
    *,
    filter_criteria: dict[str, Any] | None = None,
    group_by: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCoverageStatisticsResult:
    """List coverage statistics.

    Args:
        filter_criteria: Filter criteria.
        group_by: Group by.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if group_by is not None:
        kwargs["groupBy"] = group_by
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListCoverageStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list coverage statistics") from exc
    return ListCoverageStatisticsResult(
        counts_by_group=resp.get("countsByGroup"),
        total_counts=resp.get("totalCounts"),
        next_token=resp.get("nextToken"),
    )


async def list_delegated_admin_accounts(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDelegatedAdminAccountsResult:
    """List delegated admin accounts.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListDelegatedAdminAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list delegated admin accounts") from exc
    return ListDelegatedAdminAccountsResult(
        delegated_admin_accounts=resp.get("delegatedAdminAccounts"),
        next_token=resp.get("nextToken"),
    )


async def list_filters(
    *,
    arns: list[str] | None = None,
    action: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFiltersResult:
    """List filters.

    Args:
        arns: Arns.
        action: Action.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if arns is not None:
        kwargs["arns"] = arns
    if action is not None:
        kwargs["action"] = action
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListFilters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list filters") from exc
    return ListFiltersResult(
        filters=resp.get("filters"),
        next_token=resp.get("nextToken"),
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
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def list_usage_totals(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    account_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ListUsageTotalsResult:
    """List usage totals.

    Args:
        max_results: Max results.
        next_token: Next token.
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if account_ids is not None:
        kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("ListUsageTotals", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list usage totals") from exc
    return ListUsageTotalsResult(
        next_token=resp.get("nextToken"),
        totals=resp.get("totals"),
    )


async def reset_encryption_key(
    scan_type: str,
    resource_type: str,
    region_name: str | None = None,
) -> None:
    """Reset encryption key.

    Args:
        scan_type: Scan type.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanType"] = scan_type
    kwargs["resourceType"] = resource_type
    try:
        await client.call("ResetEncryptionKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset encryption key") from exc
    return None


async def search_vulnerabilities(
    filter_criteria: dict[str, Any],
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SearchVulnerabilitiesResult:
    """Search vulnerabilities.

    Args:
        filter_criteria: Filter criteria.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["filterCriteria"] = filter_criteria
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("SearchVulnerabilities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search vulnerabilities") from exc
    return SearchVulnerabilitiesResult(
        vulnerabilities=resp.get("vulnerabilities"),
        next_token=resp.get("nextToken"),
    )


async def send_cis_session_health(
    scan_job_id: str,
    session_token: str,
    region_name: str | None = None,
) -> None:
    """Send cis session health.

    Args:
        scan_job_id: Scan job id.
        session_token: Session token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanJobId"] = scan_job_id
    kwargs["sessionToken"] = session_token
    try:
        await client.call("SendCisSessionHealth", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send cis session health") from exc
    return None


async def send_cis_session_telemetry(
    scan_job_id: str,
    session_token: str,
    messages: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Send cis session telemetry.

    Args:
        scan_job_id: Scan job id.
        session_token: Session token.
        messages: Messages.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanJobId"] = scan_job_id
    kwargs["sessionToken"] = session_token
    kwargs["messages"] = messages
    try:
        await client.call("SendCisSessionTelemetry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send cis session telemetry") from exc
    return None


async def start_cis_session(
    scan_job_id: str,
    message: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Start cis session.

    Args:
        scan_job_id: Scan job id.
        message: Message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanJobId"] = scan_job_id
    kwargs["message"] = message
    try:
        await client.call("StartCisSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start cis session") from exc
    return None


async def start_code_security_scan(
    resource: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartCodeSecurityScanResult:
    """Start code security scan.

    Args:
        resource: Resource.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resource"] = resource
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("StartCodeSecurityScan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start code security scan") from exc
    return StartCodeSecurityScanResult(
        scan_id=resp.get("scanId"),
        status=resp.get("status"),
    )


async def stop_cis_session(
    scan_job_id: str,
    session_token: str,
    message: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Stop cis session.

    Args:
        scan_job_id: Scan job id.
        session_token: Session token.
        message: Message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanJobId"] = scan_job_id
    kwargs["sessionToken"] = session_token
    kwargs["message"] = message
    try:
        await client.call("StopCisSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop cis session") from exc
    return None


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
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
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
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
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_cis_scan_configuration(
    scan_configuration_arn: str,
    *,
    scan_name: str | None = None,
    security_level: str | None = None,
    schedule: dict[str, Any] | None = None,
    targets: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateCisScanConfigurationResult:
    """Update cis scan configuration.

    Args:
        scan_configuration_arn: Scan configuration arn.
        scan_name: Scan name.
        security_level: Security level.
        schedule: Schedule.
        targets: Targets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    if scan_name is not None:
        kwargs["scanName"] = scan_name
    if security_level is not None:
        kwargs["securityLevel"] = security_level
    if schedule is not None:
        kwargs["schedule"] = schedule
    if targets is not None:
        kwargs["targets"] = targets
    try:
        resp = await client.call("UpdateCisScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cis scan configuration") from exc
    return UpdateCisScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def update_code_security_integration(
    integration_arn: str,
    details: dict[str, Any],
    region_name: str | None = None,
) -> UpdateCodeSecurityIntegrationResult:
    """Update code security integration.

    Args:
        integration_arn: Integration arn.
        details: Details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["integrationArn"] = integration_arn
    kwargs["details"] = details
    try:
        resp = await client.call("UpdateCodeSecurityIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update code security integration") from exc
    return UpdateCodeSecurityIntegrationResult(
        integration_arn=resp.get("integrationArn"),
        status=resp.get("status"),
    )


async def update_code_security_scan_configuration(
    scan_configuration_arn: str,
    configuration: dict[str, Any],
    region_name: str | None = None,
) -> UpdateCodeSecurityScanConfigurationResult:
    """Update code security scan configuration.

    Args:
        scan_configuration_arn: Scan configuration arn.
        configuration: Configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scanConfigurationArn"] = scan_configuration_arn
    kwargs["configuration"] = configuration
    try:
        resp = await client.call("UpdateCodeSecurityScanConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update code security scan configuration") from exc
    return UpdateCodeSecurityScanConfigurationResult(
        scan_configuration_arn=resp.get("scanConfigurationArn"),
    )


async def update_ec2_deep_inspection_configuration(
    *,
    activate_deep_inspection: bool | None = None,
    package_paths: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateEc2DeepInspectionConfigurationResult:
    """Update ec2 deep inspection configuration.

    Args:
        activate_deep_inspection: Activate deep inspection.
        package_paths: Package paths.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    if activate_deep_inspection is not None:
        kwargs["activateDeepInspection"] = activate_deep_inspection
    if package_paths is not None:
        kwargs["packagePaths"] = package_paths
    try:
        resp = await client.call("UpdateEc2DeepInspectionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ec2 deep inspection configuration") from exc
    return UpdateEc2DeepInspectionConfigurationResult(
        package_paths=resp.get("packagePaths"),
        org_package_paths=resp.get("orgPackagePaths"),
        status=resp.get("status"),
        error_message=resp.get("errorMessage"),
    )


async def update_encryption_key(
    kms_key_id: str,
    scan_type: str,
    resource_type: str,
    region_name: str | None = None,
) -> None:
    """Update encryption key.

    Args:
        kms_key_id: Kms key id.
        scan_type: Scan type.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["kmsKeyId"] = kms_key_id
    kwargs["scanType"] = scan_type
    kwargs["resourceType"] = resource_type
    try:
        await client.call("UpdateEncryptionKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update encryption key") from exc
    return None


async def update_filter(
    filter_arn: str,
    *,
    action: str | None = None,
    description: str | None = None,
    filter_criteria: dict[str, Any] | None = None,
    name: str | None = None,
    reason: str | None = None,
    region_name: str | None = None,
) -> UpdateFilterResult:
    """Update filter.

    Args:
        filter_arn: Filter arn.
        action: Action.
        description: Description.
        filter_criteria: Filter criteria.
        name: Name.
        reason: Reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["filterArn"] = filter_arn
    if action is not None:
        kwargs["action"] = action
    if description is not None:
        kwargs["description"] = description
    if filter_criteria is not None:
        kwargs["filterCriteria"] = filter_criteria
    if name is not None:
        kwargs["name"] = name
    if reason is not None:
        kwargs["reason"] = reason
    try:
        resp = await client.call("UpdateFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update filter") from exc
    return UpdateFilterResult(
        arn=resp.get("arn"),
    )


async def update_org_ec2_deep_inspection_configuration(
    org_package_paths: list[str],
    region_name: str | None = None,
) -> None:
    """Update org ec2 deep inspection configuration.

    Args:
        org_package_paths: Org package paths.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["orgPackagePaths"] = org_package_paths
    try:
        await client.call("UpdateOrgEc2DeepInspectionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update org ec2 deep inspection configuration") from exc
    return None


async def update_organization_configuration(
    auto_enable: dict[str, Any],
    region_name: str | None = None,
) -> UpdateOrganizationConfigurationResult:
    """Update organization configuration.

    Args:
        auto_enable: Auto enable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("inspector2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["autoEnable"] = auto_enable
    try:
        resp = await client.call("UpdateOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return UpdateOrganizationConfigurationResult(
        auto_enable=resp.get("autoEnable"),
    )
