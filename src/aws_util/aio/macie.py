"""Native async Amazon Macie utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.macie import (
    BatchGetCustomDataIdentifiersResult,
    BatchUpdateAutomatedDiscoveryAccountsResult,
    BucketInfo,
    BucketStatistics,
    ClassificationJobResult,
    CreateAllowListResult,
    CreateCustomDataIdentifierResult,
    CreateInvitationsResult,
    CreateMemberResult,
    DeclineInvitationsResult,
    DeleteInvitationsResult,
    DescribeOrganizationConfigurationResult,
    FindingResult,
    FindingsFilterResult,
    GetAdministratorAccountResult,
    GetAllowListResult,
    GetAutomatedDiscoveryConfigurationResult,
    GetClassificationExportConfigurationResult,
    GetClassificationScopeResult,
    GetCustomDataIdentifierResult,
    GetFindingsPublicationConfigurationResult,
    GetFindingStatisticsResult,
    GetInvitationsCountResult,
    GetMasterAccountResult,
    GetMemberResult,
    GetResourceProfileResult,
    GetRevealConfigurationResult,
    GetSensitiveDataOccurrencesAvailabilityResult,
    GetSensitiveDataOccurrencesResult,
    GetSensitivityInspectionTemplateResult,
    GetUsageStatisticsResult,
    GetUsageTotalsResult,
    ListAllowListsResult,
    ListAutomatedDiscoveryAccountsResult,
    ListClassificationScopesResult,
    ListCustomDataIdentifiersResult,
    ListInvitationsResult,
    ListManagedDataIdentifiersResult,
    ListMembersResult,
    ListOrganizationAdminAccountsResult,
    ListResourceProfileArtifactsResult,
    ListResourceProfileDetectionsResult,
    ListSensitivityInspectionTemplatesResult,
    ListTagsForResourceResult,
    MacieSessionResult,
    PutClassificationExportConfigurationResult,
    RunCustomDataIdentifierResult,
    SearchResourcesResult,
    UpdateAllowListResult,
    UpdateRevealConfigurationResult,
    _parse_bucket_info,
    _parse_classification_job,
    _parse_finding,
    _parse_session,
)

__all__ = [
    "BatchGetCustomDataIdentifiersResult",
    "BatchUpdateAutomatedDiscoveryAccountsResult",
    "BucketInfo",
    "BucketStatistics",
    "ClassificationJobResult",
    "CreateAllowListResult",
    "CreateCustomDataIdentifierResult",
    "CreateInvitationsResult",
    "CreateMemberResult",
    "DeclineInvitationsResult",
    "DeleteInvitationsResult",
    "DescribeOrganizationConfigurationResult",
    "FindingResult",
    "FindingsFilterResult",
    "GetAdministratorAccountResult",
    "GetAllowListResult",
    "GetAutomatedDiscoveryConfigurationResult",
    "GetClassificationExportConfigurationResult",
    "GetClassificationScopeResult",
    "GetCustomDataIdentifierResult",
    "GetFindingStatisticsResult",
    "GetFindingsPublicationConfigurationResult",
    "GetInvitationsCountResult",
    "GetMasterAccountResult",
    "GetMemberResult",
    "GetResourceProfileResult",
    "GetRevealConfigurationResult",
    "GetSensitiveDataOccurrencesAvailabilityResult",
    "GetSensitiveDataOccurrencesResult",
    "GetSensitivityInspectionTemplateResult",
    "GetUsageStatisticsResult",
    "GetUsageTotalsResult",
    "ListAllowListsResult",
    "ListAutomatedDiscoveryAccountsResult",
    "ListClassificationScopesResult",
    "ListCustomDataIdentifiersResult",
    "ListInvitationsResult",
    "ListManagedDataIdentifiersResult",
    "ListMembersResult",
    "ListOrganizationAdminAccountsResult",
    "ListResourceProfileArtifactsResult",
    "ListResourceProfileDetectionsResult",
    "ListSensitivityInspectionTemplatesResult",
    "ListTagsForResourceResult",
    "MacieSessionResult",
    "PutClassificationExportConfigurationResult",
    "RunCustomDataIdentifierResult",
    "SearchResourcesResult",
    "UpdateAllowListResult",
    "UpdateRevealConfigurationResult",
    "accept_invitation",
    "batch_get_custom_data_identifiers",
    "batch_update_automated_discovery_accounts",
    "cancel_classification_job",
    "create_allow_list",
    "create_classification_job",
    "create_custom_data_identifier",
    "create_findings_filter",
    "create_invitations",
    "create_member",
    "create_sample_findings",
    "decline_invitations",
    "delete_allow_list",
    "delete_custom_data_identifier",
    "delete_findings_filter",
    "delete_invitations",
    "delete_member",
    "describe_buckets",
    "describe_classification_job",
    "describe_organization_configuration",
    "disable_macie",
    "disable_organization_admin_account",
    "disassociate_from_administrator_account",
    "disassociate_from_master_account",
    "disassociate_member",
    "enable_macie",
    "enable_organization_admin_account",
    "get_administrator_account",
    "get_allow_list",
    "get_automated_discovery_configuration",
    "get_bucket_statistics",
    "get_classification_export_configuration",
    "get_classification_scope",
    "get_custom_data_identifier",
    "get_finding_statistics",
    "get_findings",
    "get_findings_filter",
    "get_findings_publication_configuration",
    "get_invitations_count",
    "get_macie_session",
    "get_master_account",
    "get_member",
    "get_resource_profile",
    "get_reveal_configuration",
    "get_sensitive_data_occurrences",
    "get_sensitive_data_occurrences_availability",
    "get_sensitivity_inspection_template",
    "get_usage_statistics",
    "get_usage_totals",
    "list_allow_lists",
    "list_automated_discovery_accounts",
    "list_classification_jobs",
    "list_classification_scopes",
    "list_custom_data_identifiers",
    "list_findings",
    "list_findings_filters",
    "list_invitations",
    "list_managed_data_identifiers",
    "list_members",
    "list_organization_admin_accounts",
    "list_resource_profile_artifacts",
    "list_resource_profile_detections",
    "list_sensitivity_inspection_templates",
    "list_tags_for_resource",
    "put_classification_export_configuration",
    "put_findings_publication_configuration",
    "run_custom_data_identifier",
    "search_resources",
    "tag_resource",
    "untag_resource",
    "update_allow_list",
    "update_automated_discovery_configuration",
    "update_classification_job",
    "update_classification_scope",
    "update_findings_filter",
    "update_macie_session",
    "update_member_session",
    "update_organization_configuration",
    "update_resource_profile",
    "update_resource_profile_detections",
    "update_reveal_configuration",
    "update_sensitivity_inspection_template",
]


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------


async def enable_macie(
    *,
    finding_publishing_frequency: str = "FIFTEEN_MINUTES",
    client_token: str | None = None,
    status: str = "ENABLED",
    region_name: str | None = None,
) -> None:
    """Enable Amazon Macie in the account.

    Args:
        finding_publishing_frequency: How often findings are published.
        client_token: Idempotency token.
        status: Initial status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {
        "findingPublishingFrequency": finding_publishing_frequency,
        "status": status,
    }
    if client_token:
        kwargs["clientToken"] = client_token
    try:
        await client.call("EnableMacie", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "enable_macie failed") from exc


async def disable_macie(
    *,
    region_name: str | None = None,
) -> None:
    """Disable Amazon Macie in the account.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        await client.call("DisableMacie")
    except Exception as exc:
        raise wrap_aws_error(exc, "disable_macie failed") from exc


async def get_macie_session(
    *,
    region_name: str | None = None,
) -> MacieSessionResult:
    """Get the current Macie session status.

    Args:
        region_name: AWS region override.

    Returns:
        A :class:`MacieSessionResult` with session metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        resp = await client.call("GetMacieSession")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_macie_session failed") from exc
    return _parse_session(resp)


async def update_macie_session(
    *,
    finding_publishing_frequency: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update the Macie session configuration.

    Args:
        finding_publishing_frequency: New publishing frequency.
        status: New status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if finding_publishing_frequency is not None:
        kwargs["findingPublishingFrequency"] = finding_publishing_frequency
    if status is not None:
        kwargs["status"] = status
    try:
        await client.call("UpdateMacieSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "update_macie_session failed") from exc


# ---------------------------------------------------------------------------
# Classification jobs
# ---------------------------------------------------------------------------


async def create_classification_job(
    name: str,
    job_type: str,
    *,
    s3_job_definition: dict[str, Any],
    client_token: str | None = None,
    description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClassificationJobResult:
    """Create a Macie classification job.

    Args:
        name: Display name for the job.
        job_type: ``ONE_TIME`` or ``SCHEDULED``.
        s3_job_definition: S3 bucket/object scope definition.
        client_token: Idempotency token.
        description: Optional description.
        tags: Optional tags.
        region_name: AWS region override.

    Returns:
        A :class:`ClassificationJobResult` with the new job details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "jobType": job_type,
        "s3JobDefinition": s3_job_definition,
    }
    if client_token:
        kwargs["clientToken"] = client_token
    if description:
        kwargs["description"] = description
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateClassificationJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_classification_job failed for {name!r}") from exc
    return ClassificationJobResult(
        job_id=resp.get("jobId", ""),
        job_status=resp.get("jobArn", ""),
        extra={k: v for k, v in resp.items() if k not in {"jobId", "jobArn", "ResponseMetadata"}},
    )


async def describe_classification_job(
    job_id: str,
    *,
    region_name: str | None = None,
) -> ClassificationJobResult:
    """Describe a Macie classification job.

    Args:
        job_id: The job identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ClassificationJobResult` with job details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        resp = await client.call("DescribeClassificationJob", jobId=job_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_classification_job failed for {job_id!r}",
        ) from exc
    return _parse_classification_job(resp)


async def list_classification_jobs(
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[ClassificationJobResult]:
    """List Macie classification jobs.

    Args:
        filter_criteria: Filter criteria dict.
        sort_criteria: Sort criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClassificationJobResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_criteria:
        kwargs["filterCriteria"] = filter_criteria
    if sort_criteria:
        kwargs["sortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[ClassificationJobResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListClassificationJobs", **kwargs)
            for item in resp.get("items", []):
                results.append(_parse_classification_job(item))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_classification_jobs failed") from exc
    return results


async def update_classification_job(
    job_id: str,
    *,
    job_status: str,
    region_name: str | None = None,
) -> None:
    """Update a Macie classification job status.

    Args:
        job_id: The job identifier.
        job_status: New status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        await client.call(
            "UpdateClassificationJob",
            jobId=job_id,
            jobStatus=job_status,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_classification_job failed for {job_id!r}",
        ) from exc


async def cancel_classification_job(
    job_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Cancel a Macie classification job.

    Args:
        job_id: The job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        await client.call(
            "UpdateClassificationJob",
            jobId=job_id,
            jobStatus="CANCELLED",
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"cancel_classification_job failed for {job_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


async def list_findings(
    *,
    finding_criteria: dict[str, Any] | None = None,
    sort_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[str]:
    """List Macie finding IDs.

    Args:
        finding_criteria: Filter criteria dict.
        sort_criteria: Sort criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of finding ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if finding_criteria:
        kwargs["findingCriteria"] = finding_criteria
    if sort_criteria:
        kwargs["sortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    ids: list[str] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListFindings", **kwargs)
            ids.extend(resp.get("findingIds", []))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_findings failed") from exc
    return ids


async def get_findings(
    finding_ids: list[str],
    *,
    sort_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[FindingResult]:
    """Get details for specific Macie findings.

    Args:
        finding_ids: List of finding IDs.
        sort_criteria: Sort criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {"findingIds": finding_ids}
    if sort_criteria:
        kwargs["sortCriteria"] = sort_criteria
    try:
        resp = await client.call("GetFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_findings failed") from exc
    return [_parse_finding(f) for f in resp.get("findings", [])]


# ---------------------------------------------------------------------------
# Findings filters
# ---------------------------------------------------------------------------


async def list_findings_filters(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[FindingsFilterResult]:
    """List Macie findings filters.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingsFilterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[FindingsFilterResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("ListFindingsFilters", **kwargs)
            for item in resp.get("findingsFilterListItems", []):
                results.append(
                    FindingsFilterResult(
                        filter_id=item.get("id", ""),
                        name=item.get("name", ""),
                        action=item.get("action", ""),
                        arn=item.get("arn", ""),
                        extra={
                            k: v
                            for k, v in item.items()
                            if k not in {"id", "name", "action", "arn"}
                        },
                    )
                )
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_findings_filters failed") from exc
    return results


async def create_findings_filter(
    name: str,
    action: str,
    *,
    finding_criteria: dict[str, Any],
    description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> FindingsFilterResult:
    """Create a Macie findings filter.

    Args:
        name: Display name for the filter.
        action: ``ARCHIVE`` or ``NOOP``.
        finding_criteria: Filter criteria dict.
        description: Optional description.
        client_token: Idempotency token.
        tags: Optional tags.
        region_name: AWS region override.

    Returns:
        A :class:`FindingsFilterResult` with the new filter details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "action": action,
        "findingCriteria": finding_criteria,
    }
    if description:
        kwargs["description"] = description
    if client_token:
        kwargs["clientToken"] = client_token
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateFindingsFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_findings_filter failed for {name!r}") from exc
    return FindingsFilterResult(
        filter_id=resp.get("id", ""),
        arn=resp.get("arn", ""),
        extra={k: v for k, v in resp.items() if k not in {"id", "arn", "ResponseMetadata"}},
    )


async def get_findings_filter(
    filter_id: str,
    *,
    region_name: str | None = None,
) -> FindingsFilterResult:
    """Get a Macie findings filter.

    Args:
        filter_id: The filter identifier.
        region_name: AWS region override.

    Returns:
        A :class:`FindingsFilterResult` with filter details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        resp = await client.call("GetFindingsFilter", id=filter_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_findings_filter failed for {filter_id!r}",
        ) from exc
    return FindingsFilterResult(
        filter_id=resp.get("id", ""),
        name=resp.get("name", ""),
        action=resp.get("action", ""),
        arn=resp.get("arn", ""),
        extra={
            k: v
            for k, v in resp.items()
            if k not in {"id", "name", "action", "arn", "ResponseMetadata"}
        },
    )


async def update_findings_filter(
    filter_id: str,
    *,
    name: str | None = None,
    action: str | None = None,
    finding_criteria: dict[str, Any] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> FindingsFilterResult:
    """Update a Macie findings filter.

    Args:
        filter_id: The filter identifier.
        name: New display name.
        action: New action.
        finding_criteria: New filter criteria dict.
        description: New description.
        region_name: AWS region override.

    Returns:
        A :class:`FindingsFilterResult` with updated filter details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {"id": filter_id}
    if name is not None:
        kwargs["name"] = name
    if action is not None:
        kwargs["action"] = action
    if finding_criteria is not None:
        kwargs["findingCriteria"] = finding_criteria
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("UpdateFindingsFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_findings_filter failed for {filter_id!r}",
        ) from exc
    return FindingsFilterResult(
        filter_id=resp.get("id", ""),
        arn=resp.get("arn", ""),
        extra={k: v for k, v in resp.items() if k not in {"id", "arn", "ResponseMetadata"}},
    )


async def delete_findings_filter(
    filter_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Macie findings filter.

    Args:
        filter_id: The filter identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    try:
        await client.call("DeleteFindingsFilter", id=filter_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"delete_findings_filter failed for {filter_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# S3 bucket analysis
# ---------------------------------------------------------------------------


async def describe_buckets(
    *,
    criteria: dict[str, Any] | None = None,
    sort_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[BucketInfo]:
    """Describe S3 buckets monitored by Macie.

    Args:
        criteria: Filter criteria dict.
        sort_criteria: Sort criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`BucketInfo` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if criteria:
        kwargs["criteria"] = criteria
    if sort_criteria:
        kwargs["sortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    results: list[BucketInfo] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["nextToken"] = token
            resp = await client.call("DescribeBuckets", **kwargs)
            for b in resp.get("buckets", []):
                results.append(_parse_bucket_info(b))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_buckets failed") from exc
    return results


async def get_bucket_statistics(
    *,
    account_id: str | None = None,
    region_name: str | None = None,
) -> BucketStatistics:
    """Get aggregated S3 bucket statistics from Macie.

    Args:
        account_id: Optional account ID to filter by.
        region_name: AWS region override.

    Returns:
        A :class:`BucketStatistics` with aggregate statistics.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if account_id:
        kwargs["accountId"] = account_id
    try:
        resp = await client.call("GetBucketStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_bucket_statistics failed") from exc
    return BucketStatistics(
        buckets_count=resp.get("bucketsCount", 0),
        classifiable_object_count=resp.get("classifiableObjectCount", 0),
        classifiable_size_in_bytes=resp.get("classifiableSizeInBytes", 0),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "bucketsCount",
                "classifiableObjectCount",
                "classifiableSizeInBytes",
                "ResponseMetadata",
            }
        },
    )


async def accept_invitation(
    invitation_id: str,
    *,
    administrator_account_id: str | None = None,
    master_account: str | None = None,
    region_name: str | None = None,
) -> None:
    """Accept invitation.

    Args:
        invitation_id: Invitation id.
        administrator_account_id: Administrator account id.
        master_account: Master account.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["invitationId"] = invitation_id
    if administrator_account_id is not None:
        kwargs["administratorAccountId"] = administrator_account_id
    if master_account is not None:
        kwargs["masterAccount"] = master_account
    try:
        await client.call("AcceptInvitation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to accept invitation") from exc
    return None


async def batch_get_custom_data_identifiers(
    *,
    ids: list[str] | None = None,
    region_name: str | None = None,
) -> BatchGetCustomDataIdentifiersResult:
    """Batch get custom data identifiers.

    Args:
        ids: Ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if ids is not None:
        kwargs["ids"] = ids
    try:
        resp = await client.call("BatchGetCustomDataIdentifiers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get custom data identifiers") from exc
    return BatchGetCustomDataIdentifiersResult(
        custom_data_identifiers=resp.get("customDataIdentifiers"),
        not_found_identifier_ids=resp.get("notFoundIdentifierIds"),
    )


async def batch_update_automated_discovery_accounts(
    *,
    accounts: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> BatchUpdateAutomatedDiscoveryAccountsResult:
    """Batch update automated discovery accounts.

    Args:
        accounts: Accounts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if accounts is not None:
        kwargs["accounts"] = accounts
    try:
        resp = await client.call("BatchUpdateAutomatedDiscoveryAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update automated discovery accounts") from exc
    return BatchUpdateAutomatedDiscoveryAccountsResult(
        errors=resp.get("errors"),
    )


async def create_allow_list(
    client_token: str,
    criteria: dict[str, Any],
    name: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAllowListResult:
    """Create allow list.

    Args:
        client_token: Client token.
        criteria: Criteria.
        name: Name.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientToken"] = client_token
    kwargs["criteria"] = criteria
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateAllowList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create allow list") from exc
    return CreateAllowListResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
    )


async def create_custom_data_identifier(
    name: str,
    regex: str,
    *,
    client_token: str | None = None,
    description: str | None = None,
    ignore_words: list[str] | None = None,
    keywords: list[str] | None = None,
    maximum_match_distance: int | None = None,
    severity_levels: list[dict[str, Any]] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCustomDataIdentifierResult:
    """Create custom data identifier.

    Args:
        name: Name.
        regex: Regex.
        client_token: Client token.
        description: Description.
        ignore_words: Ignore words.
        keywords: Keywords.
        maximum_match_distance: Maximum match distance.
        severity_levels: Severity levels.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["regex"] = regex
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if description is not None:
        kwargs["description"] = description
    if ignore_words is not None:
        kwargs["ignoreWords"] = ignore_words
    if keywords is not None:
        kwargs["keywords"] = keywords
    if maximum_match_distance is not None:
        kwargs["maximumMatchDistance"] = maximum_match_distance
    if severity_levels is not None:
        kwargs["severityLevels"] = severity_levels
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCustomDataIdentifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom data identifier") from exc
    return CreateCustomDataIdentifierResult(
        custom_data_identifier_id=resp.get("customDataIdentifierId"),
    )


async def create_invitations(
    account_ids: list[str],
    *,
    disable_email_notification: bool | None = None,
    message: str | None = None,
    region_name: str | None = None,
) -> CreateInvitationsResult:
    """Create invitations.

    Args:
        account_ids: Account ids.
        disable_email_notification: Disable email notification.
        message: Message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountIds"] = account_ids
    if disable_email_notification is not None:
        kwargs["disableEmailNotification"] = disable_email_notification
    if message is not None:
        kwargs["message"] = message
    try:
        resp = await client.call("CreateInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create invitations") from exc
    return CreateInvitationsResult(
        unprocessed_accounts=resp.get("unprocessedAccounts"),
    )


async def create_member(
    account: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateMemberResult:
    """Create member.

    Args:
        account: Account.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["account"] = account
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create member") from exc
    return CreateMemberResult(
        arn=resp.get("arn"),
    )


async def create_sample_findings(
    *,
    finding_types: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Create sample findings.

    Args:
        finding_types: Finding types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if finding_types is not None:
        kwargs["findingTypes"] = finding_types
    try:
        await client.call("CreateSampleFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create sample findings") from exc
    return None


async def decline_invitations(
    account_ids: list[str],
    region_name: str | None = None,
) -> DeclineInvitationsResult:
    """Decline invitations.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("DeclineInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to decline invitations") from exc
    return DeclineInvitationsResult(
        unprocessed_accounts=resp.get("unprocessedAccounts"),
    )


async def delete_allow_list(
    id: str,
    *,
    ignore_job_checks: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete allow list.

    Args:
        id: Id.
        ignore_job_checks: Ignore job checks.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    if ignore_job_checks is not None:
        kwargs["ignoreJobChecks"] = ignore_job_checks
    try:
        await client.call("DeleteAllowList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete allow list") from exc
    return None


async def delete_custom_data_identifier(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete custom data identifier.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        await client.call("DeleteCustomDataIdentifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom data identifier") from exc
    return None


async def delete_invitations(
    account_ids: list[str],
    region_name: str | None = None,
) -> DeleteInvitationsResult:
    """Delete invitations.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accountIds"] = account_ids
    try:
        resp = await client.call("DeleteInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete invitations") from exc
    return DeleteInvitationsResult(
        unprocessed_accounts=resp.get("unprocessedAccounts"),
    )


async def delete_member(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete member.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        await client.call("DeleteMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete member") from exc
    return None


async def describe_organization_configuration(
    region_name: str | None = None,
) -> DescribeOrganizationConfigurationResult:
    """Describe organization configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("autoEnable"),
        max_account_limit_reached=resp.get("maxAccountLimitReached"),
    )


async def disable_organization_admin_account(
    admin_account_id: str,
    region_name: str | None = None,
) -> None:
    """Disable organization admin account.

    Args:
        admin_account_id: Admin account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["adminAccountId"] = admin_account_id
    try:
        await client.call("DisableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable organization admin account") from exc
    return None


async def disassociate_from_administrator_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from administrator account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisassociateFromAdministratorAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from administrator account") from exc
    return None


async def disassociate_from_master_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisassociateFromMasterAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from master account") from exc
    return None


async def disassociate_member(
    id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate member.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        await client.call("DisassociateMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate member") from exc
    return None


async def enable_organization_admin_account(
    admin_account_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Enable organization admin account.

    Args:
        admin_account_id: Admin account id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["adminAccountId"] = admin_account_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("EnableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable organization admin account") from exc
    return None


async def get_administrator_account(
    region_name: str | None = None,
) -> GetAdministratorAccountResult:
    """Get administrator account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAdministratorAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get administrator account") from exc
    return GetAdministratorAccountResult(
        administrator=resp.get("administrator"),
    )


async def get_allow_list(
    id: str,
    region_name: str | None = None,
) -> GetAllowListResult:
    """Get allow list.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetAllowList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get allow list") from exc
    return GetAllowListResult(
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
        criteria=resp.get("criteria"),
        description=resp.get("description"),
        id=resp.get("id"),
        name=resp.get("name"),
        status=resp.get("status"),
        tags=resp.get("tags"),
        updated_at=resp.get("updatedAt"),
    )


async def get_automated_discovery_configuration(
    region_name: str | None = None,
) -> GetAutomatedDiscoveryConfigurationResult:
    """Get automated discovery configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAutomatedDiscoveryConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get automated discovery configuration") from exc
    return GetAutomatedDiscoveryConfigurationResult(
        auto_enable_organization_members=resp.get("autoEnableOrganizationMembers"),
        classification_scope_id=resp.get("classificationScopeId"),
        disabled_at=resp.get("disabledAt"),
        first_enabled_at=resp.get("firstEnabledAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
        sensitivity_inspection_template_id=resp.get("sensitivityInspectionTemplateId"),
        status=resp.get("status"),
    )


async def get_classification_export_configuration(
    region_name: str | None = None,
) -> GetClassificationExportConfigurationResult:
    """Get classification export configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetClassificationExportConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get classification export configuration") from exc
    return GetClassificationExportConfigurationResult(
        configuration=resp.get("configuration"),
    )


async def get_classification_scope(
    id: str,
    region_name: str | None = None,
) -> GetClassificationScopeResult:
    """Get classification scope.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetClassificationScope", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get classification scope") from exc
    return GetClassificationScopeResult(
        id=resp.get("id"),
        name=resp.get("name"),
        s3=resp.get("s3"),
    )


async def get_custom_data_identifier(
    id: str,
    region_name: str | None = None,
) -> GetCustomDataIdentifierResult:
    """Get custom data identifier.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetCustomDataIdentifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get custom data identifier") from exc
    return GetCustomDataIdentifierResult(
        arn=resp.get("arn"),
        created_at=resp.get("createdAt"),
        deleted=resp.get("deleted"),
        description=resp.get("description"),
        id=resp.get("id"),
        ignore_words=resp.get("ignoreWords"),
        keywords=resp.get("keywords"),
        maximum_match_distance=resp.get("maximumMatchDistance"),
        name=resp.get("name"),
        regex=resp.get("regex"),
        severity_levels=resp.get("severityLevels"),
        tags=resp.get("tags"),
    )


async def get_finding_statistics(
    group_by: str,
    *,
    finding_criteria: dict[str, Any] | None = None,
    size: int | None = None,
    sort_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetFindingStatisticsResult:
    """Get finding statistics.

    Args:
        group_by: Group by.
        finding_criteria: Finding criteria.
        size: Size.
        sort_criteria: Sort criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["groupBy"] = group_by
    if finding_criteria is not None:
        kwargs["findingCriteria"] = finding_criteria
    if size is not None:
        kwargs["size"] = size
    if sort_criteria is not None:
        kwargs["sortCriteria"] = sort_criteria
    try:
        resp = await client.call("GetFindingStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding statistics") from exc
    return GetFindingStatisticsResult(
        counts_by_group=resp.get("countsByGroup"),
    )


async def get_findings_publication_configuration(
    region_name: str | None = None,
) -> GetFindingsPublicationConfigurationResult:
    """Get findings publication configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetFindingsPublicationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get findings publication configuration") from exc
    return GetFindingsPublicationConfigurationResult(
        security_hub_configuration=resp.get("securityHubConfiguration"),
    )


async def get_invitations_count(
    region_name: str | None = None,
) -> GetInvitationsCountResult:
    """Get invitations count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetInvitationsCount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get invitations count") from exc
    return GetInvitationsCountResult(
        invitations_count=resp.get("invitationsCount"),
    )


async def get_master_account(
    region_name: str | None = None,
) -> GetMasterAccountResult:
    """Get master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetMasterAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get master account") from exc
    return GetMasterAccountResult(
        master=resp.get("master"),
    )


async def get_member(
    id: str,
    region_name: str | None = None,
) -> GetMemberResult:
    """Get member.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get member") from exc
    return GetMemberResult(
        account_id=resp.get("accountId"),
        administrator_account_id=resp.get("administratorAccountId"),
        arn=resp.get("arn"),
        email=resp.get("email"),
        invited_at=resp.get("invitedAt"),
        master_account_id=resp.get("masterAccountId"),
        relationship_status=resp.get("relationshipStatus"),
        tags=resp.get("tags"),
        updated_at=resp.get("updatedAt"),
    )


async def get_resource_profile(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourceProfileResult:
    """Get resource profile.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource profile") from exc
    return GetResourceProfileResult(
        profile_updated_at=resp.get("profileUpdatedAt"),
        sensitivity_score=resp.get("sensitivityScore"),
        sensitivity_score_overridden=resp.get("sensitivityScoreOverridden"),
        statistics=resp.get("statistics"),
    )


async def get_reveal_configuration(
    region_name: str | None = None,
) -> GetRevealConfigurationResult:
    """Get reveal configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetRevealConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get reveal configuration") from exc
    return GetRevealConfigurationResult(
        configuration=resp.get("configuration"),
        retrieval_configuration=resp.get("retrievalConfiguration"),
    )


async def get_sensitive_data_occurrences(
    finding_id: str,
    region_name: str | None = None,
) -> GetSensitiveDataOccurrencesResult:
    """Get sensitive data occurrences.

    Args:
        finding_id: Finding id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingId"] = finding_id
    try:
        resp = await client.call("GetSensitiveDataOccurrences", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sensitive data occurrences") from exc
    return GetSensitiveDataOccurrencesResult(
        error=resp.get("error"),
        sensitive_data_occurrences=resp.get("sensitiveDataOccurrences"),
        status=resp.get("status"),
    )


async def get_sensitive_data_occurrences_availability(
    finding_id: str,
    region_name: str | None = None,
) -> GetSensitiveDataOccurrencesAvailabilityResult:
    """Get sensitive data occurrences availability.

    Args:
        finding_id: Finding id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingId"] = finding_id
    try:
        resp = await client.call("GetSensitiveDataOccurrencesAvailability", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sensitive data occurrences availability") from exc
    return GetSensitiveDataOccurrencesAvailabilityResult(
        code=resp.get("code"),
        reasons=resp.get("reasons"),
    )


async def get_sensitivity_inspection_template(
    id: str,
    region_name: str | None = None,
) -> GetSensitivityInspectionTemplateResult:
    """Get sensitivity inspection template.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetSensitivityInspectionTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sensitivity inspection template") from exc
    return GetSensitivityInspectionTemplateResult(
        description=resp.get("description"),
        excludes=resp.get("excludes"),
        includes=resp.get("includes"),
        name=resp.get("name"),
        sensitivity_inspection_template_id=resp.get("sensitivityInspectionTemplateId"),
    )


async def get_usage_statistics(
    *,
    filter_by: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_by: dict[str, Any] | None = None,
    time_range: str | None = None,
    region_name: str | None = None,
) -> GetUsageStatisticsResult:
    """Get usage statistics.

    Args:
        filter_by: Filter by.
        max_results: Max results.
        next_token: Next token.
        sort_by: Sort by.
        time_range: Time range.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if filter_by is not None:
        kwargs["filterBy"] = filter_by
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if time_range is not None:
        kwargs["timeRange"] = time_range
    try:
        resp = await client.call("GetUsageStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage statistics") from exc
    return GetUsageStatisticsResult(
        next_token=resp.get("nextToken"),
        records=resp.get("records"),
        time_range=resp.get("timeRange"),
    )


async def get_usage_totals(
    *,
    time_range: str | None = None,
    region_name: str | None = None,
) -> GetUsageTotalsResult:
    """Get usage totals.

    Args:
        time_range: Time range.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if time_range is not None:
        kwargs["timeRange"] = time_range
    try:
        resp = await client.call("GetUsageTotals", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage totals") from exc
    return GetUsageTotalsResult(
        time_range=resp.get("timeRange"),
        usage_totals=resp.get("usageTotals"),
    )


async def list_allow_lists(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAllowListsResult:
    """List allow lists.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAllowLists", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list allow lists") from exc
    return ListAllowListsResult(
        allow_lists=resp.get("allowLists"),
        next_token=resp.get("nextToken"),
    )


async def list_automated_discovery_accounts(
    *,
    account_ids: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAutomatedDiscoveryAccountsResult:
    """List automated discovery accounts.

    Args:
        account_ids: Account ids.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if account_ids is not None:
        kwargs["accountIds"] = account_ids
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAutomatedDiscoveryAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list automated discovery accounts") from exc
    return ListAutomatedDiscoveryAccountsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


async def list_classification_scopes(
    *,
    name: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClassificationScopesResult:
    """List classification scopes.

    Args:
        name: Name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["name"] = name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListClassificationScopes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list classification scopes") from exc
    return ListClassificationScopesResult(
        classification_scopes=resp.get("classificationScopes"),
        next_token=resp.get("nextToken"),
    )


async def list_custom_data_identifiers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCustomDataIdentifiersResult:
    """List custom data identifiers.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListCustomDataIdentifiers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom data identifiers") from exc
    return ListCustomDataIdentifiersResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


async def list_invitations(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListInvitationsResult:
    """List invitations.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list invitations") from exc
    return ListInvitationsResult(
        invitations=resp.get("invitations"),
        next_token=resp.get("nextToken"),
    )


async def list_managed_data_identifiers(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListManagedDataIdentifiersResult:
    """List managed data identifiers.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListManagedDataIdentifiers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list managed data identifiers") from exc
    return ListManagedDataIdentifiersResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


async def list_members(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    only_associated: str | None = None,
    region_name: str | None = None,
) -> ListMembersResult:
    """List members.

    Args:
        max_results: Max results.
        next_token: Next token.
        only_associated: Only associated.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if only_associated is not None:
        kwargs["onlyAssociated"] = only_associated
    try:
        resp = await client.call("ListMembers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list members") from exc
    return ListMembersResult(
        members=resp.get("members"),
        next_token=resp.get("nextToken"),
    )


async def list_organization_admin_accounts(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListOrganizationAdminAccountsResult:
    """List organization admin accounts.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListOrganizationAdminAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list organization admin accounts") from exc
    return ListOrganizationAdminAccountsResult(
        admin_accounts=resp.get("adminAccounts"),
        next_token=resp.get("nextToken"),
    )


async def list_resource_profile_artifacts(
    resource_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceProfileArtifactsResult:
    """List resource profile artifacts.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListResourceProfileArtifacts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list resource profile artifacts") from exc
    return ListResourceProfileArtifactsResult(
        artifacts=resp.get("artifacts"),
        next_token=resp.get("nextToken"),
    )


async def list_resource_profile_detections(
    resource_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceProfileDetectionsResult:
    """List resource profile detections.

    Args:
        resource_arn: Resource arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListResourceProfileDetections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list resource profile detections") from exc
    return ListResourceProfileDetectionsResult(
        detections=resp.get("detections"),
        next_token=resp.get("nextToken"),
    )


async def list_sensitivity_inspection_templates(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSensitivityInspectionTemplatesResult:
    """List sensitivity inspection templates.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSensitivityInspectionTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sensitivity inspection templates") from exc
    return ListSensitivityInspectionTemplatesResult(
        next_token=resp.get("nextToken"),
        sensitivity_inspection_templates=resp.get("sensitivityInspectionTemplates"),
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
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def put_classification_export_configuration(
    configuration: dict[str, Any],
    region_name: str | None = None,
) -> PutClassificationExportConfigurationResult:
    """Put classification export configuration.

    Args:
        configuration: Configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["configuration"] = configuration
    try:
        resp = await client.call("PutClassificationExportConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put classification export configuration") from exc
    return PutClassificationExportConfigurationResult(
        configuration=resp.get("configuration"),
    )


async def put_findings_publication_configuration(
    *,
    client_token: str | None = None,
    security_hub_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put findings publication configuration.

    Args:
        client_token: Client token.
        security_hub_configuration: Security hub configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if security_hub_configuration is not None:
        kwargs["securityHubConfiguration"] = security_hub_configuration
    try:
        await client.call("PutFindingsPublicationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put findings publication configuration") from exc
    return None


async def run_custom_data_identifier(
    regex: str,
    sample_text: str,
    *,
    ignore_words: list[str] | None = None,
    keywords: list[str] | None = None,
    maximum_match_distance: int | None = None,
    region_name: str | None = None,
) -> RunCustomDataIdentifierResult:
    """Run custom data identifier.

    Args:
        regex: Regex.
        sample_text: Sample text.
        ignore_words: Ignore words.
        keywords: Keywords.
        maximum_match_distance: Maximum match distance.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["regex"] = regex
    kwargs["sampleText"] = sample_text
    if ignore_words is not None:
        kwargs["ignoreWords"] = ignore_words
    if keywords is not None:
        kwargs["keywords"] = keywords
    if maximum_match_distance is not None:
        kwargs["maximumMatchDistance"] = maximum_match_distance
    try:
        resp = await client.call("TestCustomDataIdentifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run custom data identifier") from exc
    return RunCustomDataIdentifierResult(
        match_count=resp.get("matchCount"),
    )


async def search_resources(
    *,
    bucket_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchResourcesResult:
    """Search resources.

    Args:
        bucket_criteria: Bucket criteria.
        max_results: Max results.
        next_token: Next token.
        sort_criteria: Sort criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    if bucket_criteria is not None:
        kwargs["bucketCriteria"] = bucket_criteria
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_criteria is not None:
        kwargs["sortCriteria"] = sort_criteria
    try:
        resp = await client.call("SearchResources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search resources") from exc
    return SearchResourcesResult(
        matching_resources=resp.get("matchingResources"),
        next_token=resp.get("nextToken"),
    )


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
    client = async_client("macie2", region_name)
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
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_allow_list(
    criteria: dict[str, Any],
    id: str,
    name: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateAllowListResult:
    """Update allow list.

    Args:
        criteria: Criteria.
        id: Id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["criteria"] = criteria
    kwargs["id"] = id
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("UpdateAllowList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update allow list") from exc
    return UpdateAllowListResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
    )


async def update_automated_discovery_configuration(
    status: str,
    *,
    auto_enable_organization_members: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update automated discovery configuration.

    Args:
        status: Status.
        auto_enable_organization_members: Auto enable organization members.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["status"] = status
    if auto_enable_organization_members is not None:
        kwargs["autoEnableOrganizationMembers"] = auto_enable_organization_members
    try:
        await client.call("UpdateAutomatedDiscoveryConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update automated discovery configuration") from exc
    return None


async def update_classification_scope(
    id: str,
    *,
    s3: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update classification scope.

    Args:
        id: Id.
        s3: S3.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    if s3 is not None:
        kwargs["s3"] = s3
    try:
        await client.call("UpdateClassificationScope", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update classification scope") from exc
    return None


async def update_member_session(
    id: str,
    status: str,
    region_name: str | None = None,
) -> None:
    """Update member session.

    Args:
        id: Id.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    kwargs["status"] = status
    try:
        await client.call("UpdateMemberSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update member session") from exc
    return None


async def update_organization_configuration(
    auto_enable: bool,
    region_name: str | None = None,
) -> None:
    """Update organization configuration.

    Args:
        auto_enable: Auto enable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["autoEnable"] = auto_enable
    try:
        await client.call("UpdateOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return None


async def update_resource_profile(
    resource_arn: str,
    *,
    sensitivity_score_override: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update resource profile.

    Args:
        resource_arn: Resource arn.
        sensitivity_score_override: Sensitivity score override.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if sensitivity_score_override is not None:
        kwargs["sensitivityScoreOverride"] = sensitivity_score_override
    try:
        await client.call("UpdateResourceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update resource profile") from exc
    return None


async def update_resource_profile_detections(
    resource_arn: str,
    *,
    suppress_data_identifiers: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Update resource profile detections.

    Args:
        resource_arn: Resource arn.
        suppress_data_identifiers: Suppress data identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if suppress_data_identifiers is not None:
        kwargs["suppressDataIdentifiers"] = suppress_data_identifiers
    try:
        await client.call("UpdateResourceProfileDetections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update resource profile detections") from exc
    return None


async def update_reveal_configuration(
    configuration: dict[str, Any],
    *,
    retrieval_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateRevealConfigurationResult:
    """Update reveal configuration.

    Args:
        configuration: Configuration.
        retrieval_configuration: Retrieval configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["configuration"] = configuration
    if retrieval_configuration is not None:
        kwargs["retrievalConfiguration"] = retrieval_configuration
    try:
        resp = await client.call("UpdateRevealConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update reveal configuration") from exc
    return UpdateRevealConfigurationResult(
        configuration=resp.get("configuration"),
        retrieval_configuration=resp.get("retrievalConfiguration"),
    )


async def update_sensitivity_inspection_template(
    id: str,
    *,
    description: str | None = None,
    excludes: dict[str, Any] | None = None,
    includes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update sensitivity inspection template.

    Args:
        id: Id.
        description: Description.
        excludes: Excludes.
        includes: Includes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("macie2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    if description is not None:
        kwargs["description"] = description
    if excludes is not None:
        kwargs["excludes"] = excludes
    if includes is not None:
        kwargs["includes"] = includes
    try:
        await client.call("UpdateSensitivityInspectionTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update sensitivity inspection template") from exc
    return None
