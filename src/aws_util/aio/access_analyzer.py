"""Native async IAM Access Analyzer utilities.

Uses :mod:`aws_util.aio._engine` for true non-blocking I/O.
"""

from __future__ import annotations

from typing import Any

from aws_util.access_analyzer import (
    AnalyzerResult,
    ArchiveRuleResult,
    CheckNoPublicAccessResult,
    CreateAccessPreviewResult,
    FindingRecommendationResult,
    FindingResult,
    GetAccessPreviewResult,
    GetFindingRecommendationResult,
    GetFindingsStatisticsResult,
    GetFindingV2Result,
    GetGeneratedPolicyResult,
    ListAccessPreviewFindingsResult,
    ListAccessPreviewsResult,
    ListFindingsV2Result,
    ListPolicyGenerationsResult,
    ListTagsForResourceResult,
    PolicyValidationResult,
    StartPolicyGenerationResult,
    _parse_analyzer,
    _parse_archive_rule,
    _parse_finding,
    _parse_validation_finding,
)
from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AnalyzerResult",
    "ArchiveRuleResult",
    "CheckNoPublicAccessResult",
    "CreateAccessPreviewResult",
    "FindingRecommendationResult",
    "FindingResult",
    "GetAccessPreviewResult",
    "GetFindingRecommendationResult",
    "GetFindingV2Result",
    "GetFindingsStatisticsResult",
    "GetGeneratedPolicyResult",
    "ListAccessPreviewFindingsResult",
    "ListAccessPreviewsResult",
    "ListFindingsV2Result",
    "ListPolicyGenerationsResult",
    "ListTagsForResourceResult",
    "PolicyValidationResult",
    "StartPolicyGenerationResult",
    "apply_archive_rule",
    "cancel_policy_generation",
    "check_access_not_granted",
    "check_no_new_access",
    "check_no_public_access",
    "create_access_preview",
    "create_analyzer",
    "create_archive_rule",
    "delete_analyzer",
    "delete_archive_rule",
    "generate_finding_recommendation",
    "get_access_preview",
    "get_analyzed_resource",
    "get_analyzer",
    "get_archive_rule",
    "get_finding",
    "get_finding_recommendation",
    "get_finding_v2",
    "get_findings_statistics",
    "get_generated_policy",
    "list_access_preview_findings",
    "list_access_previews",
    "list_analyzed_resources",
    "list_analyzers",
    "list_archive_rules",
    "list_findings",
    "list_findings_v2",
    "list_policy_generations",
    "list_tags_for_resource",
    "start_policy_generation",
    "start_resource_scan",
    "tag_resource",
    "untag_resource",
    "update_analyzer",
    "update_archive_rule",
    "update_findings",
    "validate_policy",
]


# ---------------------------------------------------------------------------
# Analyzer CRUD
# ---------------------------------------------------------------------------


async def create_analyzer(
    analyzer_name: str,
    type: str = "ACCOUNT",
    *,
    archive_rules: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AnalyzerResult:
    """Create an IAM Access Analyzer analyzer.

    Args:
        analyzer_name: Name of the analyzer.
        type: Type of analyzer (``"ACCOUNT"`` or
            ``"ORGANIZATION"``).
        archive_rules: Optional list of archive rule configurations.
        tags: Optional tags to attach to the analyzer.
        region_name: AWS region override.

    Returns:
        The newly created :class:`AnalyzerResult`.

    Raises:
        RuntimeError: If analyzer creation fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {
        "analyzerName": analyzer_name,
        "type": type,
    }
    if archive_rules is not None:
        kwargs["archiveRules"] = archive_rules
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateAnalyzer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create analyzer {analyzer_name!r}") from exc
    return AnalyzerResult(
        arn=resp.get("arn", ""),
        name=analyzer_name,
        type=type,
        tags=tags or {},
    )


async def get_analyzer(
    analyzer_name: str,
    *,
    region_name: str | None = None,
) -> AnalyzerResult | None:
    """Get details for an IAM Access Analyzer analyzer.

    Args:
        analyzer_name: Name of the analyzer.
        region_name: AWS region override.

    Returns:
        An :class:`AnalyzerResult`, or ``None`` if not found.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call("GetAnalyzer", analyzerName=analyzer_name)
        return _parse_analyzer(resp.get("analyzer", {}))
    except RuntimeError as exc:
        if "ResourceNotFoundException" in str(exc):
            return None
        raise


async def list_analyzers(
    *,
    type: str | None = None,
    region_name: str | None = None,
) -> list[AnalyzerResult]:
    """List IAM Access Analyzer analyzers.

    Args:
        type: Filter by analyzer type (``"ACCOUNT"`` or
            ``"ORGANIZATION"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`AnalyzerResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    if type is not None:
        kwargs["type"] = type
    results: list[AnalyzerResult] = []
    try:
        token: str | None = None
        while True:
            call_kwargs = dict(kwargs)
            if token:
                call_kwargs["nextToken"] = token
            resp = await client.call("ListAnalyzers", **call_kwargs)
            for analyzer in resp.get("analyzers", []):
                results.append(_parse_analyzer(analyzer))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_analyzers failed") from exc
    return results


async def delete_analyzer(
    analyzer_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IAM Access Analyzer analyzer.

    Args:
        analyzer_name: Name of the analyzer to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call("DeleteAnalyzer", analyzerName=analyzer_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete analyzer {analyzer_name!r}") from exc


async def update_analyzer(
    analyzer_name: str,
    *,
    region_name: str | None = None,
) -> AnalyzerResult | None:
    """Update an IAM Access Analyzer analyzer configuration.

    Currently the Access Analyzer API does not support direct updates
    to analyzer configurations. This function fetches the current
    analyzer state to confirm it exists and returns the result.

    Args:
        analyzer_name: Name of the analyzer to update.
        region_name: AWS region override.

    Returns:
        The current :class:`AnalyzerResult`, or ``None`` if not found.

    Raises:
        RuntimeError: If the API call fails.
    """
    return await get_analyzer(analyzer_name, region_name=region_name)


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


async def get_finding(
    analyzer_arn: str,
    finding_id: str,
    *,
    region_name: str | None = None,
) -> FindingResult | None:
    """Get details for a specific Access Analyzer finding.

    Args:
        analyzer_arn: ARN of the analyzer.
        finding_id: ID of the finding.
        region_name: AWS region override.

    Returns:
        A :class:`FindingResult`, or ``None`` if not found.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call("GetFinding", analyzerArn=analyzer_arn, id=finding_id)
        return _parse_finding(resp.get("finding", {}))
    except RuntimeError as exc:
        if "ResourceNotFoundException" in str(exc):
            return None
        raise


async def list_findings(
    analyzer_arn: str,
    *,
    filter: dict[str, Any] | None = None,
    sort: dict[str, str] | None = None,
    region_name: str | None = None,
) -> list[FindingResult]:
    """List findings from an Access Analyzer analyzer.

    Args:
        analyzer_arn: ARN of the analyzer.
        filter: Optional filter criteria for findings.
        sort: Optional sort criteria.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {"analyzerArn": analyzer_arn}
    if filter is not None:
        kwargs["filter"] = filter
    if sort is not None:
        kwargs["sort"] = sort
    results: list[FindingResult] = []
    try:
        token: str | None = None
        while True:
            call_kwargs = dict(kwargs)
            if token:
                call_kwargs["nextToken"] = token
            resp = await client.call("ListFindings", **call_kwargs)
            for finding in resp.get("findings", []):
                results.append(_parse_finding(finding))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_findings failed") from exc
    return results


async def update_findings(
    analyzer_arn: str,
    finding_ids: list[str],
    status: str,
    *,
    region_name: str | None = None,
) -> None:
    """Update the status of Access Analyzer findings.

    Args:
        analyzer_arn: ARN of the analyzer.
        finding_ids: List of finding IDs to update.
        status: New status (``"ACTIVE"`` or ``"ARCHIVED"``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "UpdateFindings",
            analyzerArn=analyzer_arn,
            ids=finding_ids,
            status=status,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "update_findings failed") from exc


# ---------------------------------------------------------------------------
# Analyzed Resources
# ---------------------------------------------------------------------------


async def get_analyzed_resource(
    analyzer_arn: str,
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any] | None:
    """Get details for a resource analyzed by Access Analyzer.

    Args:
        analyzer_arn: ARN of the analyzer.
        resource_arn: ARN of the analyzed resource.
        region_name: AWS region override.

    Returns:
        A dict of resource details, or ``None`` if not found.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call(
            "GetAnalyzedResource",
            analyzerArn=analyzer_arn,
            resourceArn=resource_arn,
        )
        return resp.get("resource", {})
    except RuntimeError as exc:
        if "ResourceNotFoundException" in str(exc):
            return None
        raise


async def list_analyzed_resources(
    analyzer_arn: str,
    *,
    resource_type: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List resources analyzed by Access Analyzer.

    Args:
        analyzer_arn: ARN of the analyzer.
        resource_type: Optional resource type filter.
        region_name: AWS region override.

    Returns:
        A list of analyzed resource summary dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {"analyzerArn": analyzer_arn}
    if resource_type is not None:
        kwargs["resourceType"] = resource_type
    results: list[dict[str, Any]] = []
    try:
        token: str | None = None
        while True:
            call_kwargs = dict(kwargs)
            if token:
                call_kwargs["nextToken"] = token
            resp = await client.call("ListAnalyzedResources", **call_kwargs)
            for resource in resp.get("analyzedResources", []):
                results.append(resource)
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_analyzed_resources failed") from exc
    return results


async def start_resource_scan(
    analyzer_arn: str,
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Start a scan of a resource by Access Analyzer.

    Args:
        analyzer_arn: ARN of the analyzer.
        resource_arn: ARN of the resource to scan.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "StartResourceScan",
            analyzerArn=analyzer_arn,
            resourceArn=resource_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"start_resource_scan failed for {resource_arn!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Archive Rules
# ---------------------------------------------------------------------------


async def create_archive_rule(
    analyzer_name: str,
    rule_name: str,
    filter: dict[str, Any],
    *,
    region_name: str | None = None,
) -> None:
    """Create an archive rule for an Access Analyzer analyzer.

    Args:
        analyzer_name: Name of the analyzer.
        rule_name: Name of the archive rule.
        filter: Filter criteria for the rule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "CreateArchiveRule",
            analyzerName=analyzer_name,
            ruleName=rule_name,
            filter=filter,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create archive rule {rule_name!r}",
        ) from exc


async def get_archive_rule(
    analyzer_name: str,
    rule_name: str,
    *,
    region_name: str | None = None,
) -> ArchiveRuleResult | None:
    """Get details for an archive rule.

    Args:
        analyzer_name: Name of the analyzer.
        rule_name: Name of the archive rule.
        region_name: AWS region override.

    Returns:
        An :class:`ArchiveRuleResult`, or ``None`` if not found.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call(
            "GetArchiveRule",
            analyzerName=analyzer_name,
            ruleName=rule_name,
        )
        return _parse_archive_rule(resp.get("archiveRule", {}))
    except RuntimeError as exc:
        if "ResourceNotFoundException" in str(exc):
            return None
        raise


async def list_archive_rules(
    analyzer_name: str,
    *,
    region_name: str | None = None,
) -> list[ArchiveRuleResult]:
    """List archive rules for an analyzer.

    Args:
        analyzer_name: Name of the analyzer.
        region_name: AWS region override.

    Returns:
        A list of :class:`ArchiveRuleResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    results: list[ArchiveRuleResult] = []
    try:
        token: str | None = None
        while True:
            call_kwargs: dict[str, Any] = {
                "analyzerName": analyzer_name,
            }
            if token:
                call_kwargs["nextToken"] = token
            resp = await client.call("ListArchiveRules", **call_kwargs)
            for rule in resp.get("archiveRules", []):
                results.append(_parse_archive_rule(rule))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_archive_rules failed") from exc
    return results


async def update_archive_rule(
    analyzer_name: str,
    rule_name: str,
    filter: dict[str, Any],
    *,
    region_name: str | None = None,
) -> None:
    """Update an archive rule for an Access Analyzer analyzer.

    Args:
        analyzer_name: Name of the analyzer.
        rule_name: Name of the archive rule to update.
        filter: Updated filter criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "UpdateArchiveRule",
            analyzerName=analyzer_name,
            ruleName=rule_name,
            filter=filter,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to update archive rule {rule_name!r}",
        ) from exc


async def delete_archive_rule(
    analyzer_name: str,
    rule_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an archive rule.

    Args:
        analyzer_name: Name of the analyzer.
        rule_name: Name of the archive rule to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "DeleteArchiveRule",
            analyzerName=analyzer_name,
            ruleName=rule_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete archive rule {rule_name!r}",
        ) from exc


async def apply_archive_rule(
    analyzer_arn: str,
    rule_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Apply an archive rule retroactively to existing findings.

    Args:
        analyzer_arn: ARN of the analyzer.
        rule_name: Name of the archive rule to apply.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        await client.call(
            "ApplyArchiveRule",
            analyzerArn=analyzer_arn,
            ruleName=rule_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to apply archive rule {rule_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Policy Validation & Access Checks
# ---------------------------------------------------------------------------


async def validate_policy(
    policy_document: str,
    policy_type: str = "IDENTITY_POLICY",
    *,
    locale: str | None = None,
    validate_policy_resource_type: str | None = None,
    region_name: str | None = None,
) -> list[PolicyValidationResult]:
    """Validate an IAM policy document.

    Args:
        policy_document: JSON string of the policy document.
        policy_type: Type of policy (``"IDENTITY_POLICY"``,
            ``"RESOURCE_POLICY"``, or ``"SERVICE_CONTROL_POLICY"``).
        locale: Locale for finding descriptions.
        validate_policy_resource_type: Resource type for resource
            policy validation.
        region_name: AWS region override.

    Returns:
        A list of :class:`PolicyValidationResult` findings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {
        "policyDocument": policy_document,
        "policyType": policy_type,
    }
    if locale is not None:
        kwargs["locale"] = locale
    if validate_policy_resource_type is not None:
        kwargs["validatePolicyResourceType"] = validate_policy_resource_type
    results: list[PolicyValidationResult] = []
    try:
        token: str | None = None
        while True:
            call_kwargs = dict(kwargs)
            if token:
                call_kwargs["nextToken"] = token
            resp = await client.call("ValidatePolicy", **call_kwargs)
            for finding in resp.get("findings", []):
                results.append(_parse_validation_finding(finding))
            token = resp.get("nextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "validate_policy failed") from exc
    return results


async def check_access_not_granted(
    policy_document: str,
    access: list[dict[str, Any]],
    policy_type: str = "IDENTITY_POLICY",
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Check that a policy does not grant specified access.

    Args:
        policy_document: JSON string of the policy document.
        access: List of access descriptions to check against.
        policy_type: Type of policy to check.
        region_name: AWS region override.

    Returns:
        A dict with ``result`` (``"PASS"`` or ``"FAIL"``) and
        ``message`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call(
            "CheckAccessNotGranted",
            policyDocument=policy_document,
            access=access,
            policyType=policy_type,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "check_access_not_granted failed") from exc
    return {
        "result": resp.get("result", ""),
        "message": resp.get("message", ""),
        "reasons": resp.get("reasons", []),
    }


async def check_no_new_access(
    new_policy_document: str,
    existing_policy_document: str,
    policy_type: str = "IDENTITY_POLICY",
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Check that a new policy does not grant new access.

    Args:
        new_policy_document: JSON string of the new policy.
        existing_policy_document: JSON string of the existing policy.
        policy_type: Type of policy to check.
        region_name: AWS region override.

    Returns:
        A dict with ``result`` (``"PASS"`` or ``"FAIL"``) and
        ``message`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call(
            "CheckNoNewAccess",
            newPolicyDocument=new_policy_document,
            existingPolicyDocument=existing_policy_document,
            policyType=policy_type,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "check_no_new_access failed") from exc
    return {
        "result": resp.get("result", ""),
        "message": resp.get("message", ""),
        "reasons": resp.get("reasons", []),
    }


async def generate_finding_recommendation(
    analyzer_arn: str,
    finding_id: str,
    *,
    region_name: str | None = None,
) -> FindingRecommendationResult:
    """Generate a recommendation for resolving a finding.

    Args:
        analyzer_arn: ARN of the analyzer.
        finding_id: ID of the finding.
        region_name: AWS region override.

    Returns:
        A :class:`FindingRecommendationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    try:
        resp = await client.call(
            "GetFindingRecommendation",
            analyzerArn=analyzer_arn,
            id=finding_id,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"generate_finding_recommendation failed for {finding_id!r}",
        ) from exc
    return FindingRecommendationResult(
        recommendation_type=resp.get("recommendationType", ""),
        recommended_steps=resp.get("recommendedSteps", []),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "recommendationType",
                "recommendedSteps",
                "ResponseMetadata",
            }
        },
    )


async def cancel_policy_generation(
    job_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel policy generation.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    try:
        await client.call("CancelPolicyGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel policy generation") from exc
    return None


async def check_no_public_access(
    policy_document: str,
    resource_type: str,
    region_name: str | None = None,
) -> CheckNoPublicAccessResult:
    """Check no public access.

    Args:
        policy_document: Policy document.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyDocument"] = policy_document
    kwargs["resourceType"] = resource_type
    try:
        resp = await client.call("CheckNoPublicAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to check no public access") from exc
    return CheckNoPublicAccessResult(
        result=resp.get("result"),
        message=resp.get("message"),
        reasons=resp.get("reasons"),
    )


async def create_access_preview(
    analyzer_arn: str,
    configurations: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateAccessPreviewResult:
    """Create access preview.

    Args:
        analyzer_arn: Analyzer arn.
        configurations: Configurations.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    kwargs["configurations"] = configurations
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("CreateAccessPreview", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create access preview") from exc
    return CreateAccessPreviewResult(
        id=resp.get("id"),
    )


async def get_access_preview(
    access_preview_id: str,
    analyzer_arn: str,
    region_name: str | None = None,
) -> GetAccessPreviewResult:
    """Get access preview.

    Args:
        access_preview_id: Access preview id.
        analyzer_arn: Analyzer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPreviewId"] = access_preview_id
    kwargs["analyzerArn"] = analyzer_arn
    try:
        resp = await client.call("GetAccessPreview", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get access preview") from exc
    return GetAccessPreviewResult(
        access_preview=resp.get("accessPreview"),
    )


async def get_finding_recommendation(
    analyzer_arn: str,
    id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetFindingRecommendationResult:
    """Get finding recommendation.

    Args:
        analyzer_arn: Analyzer arn.
        id: Id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    kwargs["id"] = id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("GetFindingRecommendation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding recommendation") from exc
    return GetFindingRecommendationResult(
        started_at=resp.get("startedAt"),
        completed_at=resp.get("completedAt"),
        next_token=resp.get("nextToken"),
        error=resp.get("error"),
        resource_arn=resp.get("resourceArn"),
        recommended_steps=resp.get("recommendedSteps"),
        recommendation_type=resp.get("recommendationType"),
        status=resp.get("status"),
    )


async def get_finding_v2(
    analyzer_arn: str,
    id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetFindingV2Result:
    """Get finding v2.

    Args:
        analyzer_arn: Analyzer arn.
        id: Id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    kwargs["id"] = id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("GetFindingV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding v2") from exc
    return GetFindingV2Result(
        analyzed_at=resp.get("analyzedAt"),
        created_at=resp.get("createdAt"),
        error=resp.get("error"),
        id=resp.get("id"),
        next_token=resp.get("nextToken"),
        resource=resp.get("resource"),
        resource_type=resp.get("resourceType"),
        resource_owner_account=resp.get("resourceOwnerAccount"),
        status=resp.get("status"),
        updated_at=resp.get("updatedAt"),
        finding_details=resp.get("findingDetails"),
        finding_type=resp.get("findingType"),
    )


async def get_findings_statistics(
    analyzer_arn: str,
    region_name: str | None = None,
) -> GetFindingsStatisticsResult:
    """Get findings statistics.

    Args:
        analyzer_arn: Analyzer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    try:
        resp = await client.call("GetFindingsStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get findings statistics") from exc
    return GetFindingsStatisticsResult(
        findings_statistics=resp.get("findingsStatistics"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


async def get_generated_policy(
    job_id: str,
    *,
    include_resource_placeholders: bool | None = None,
    include_service_level_template: bool | None = None,
    region_name: str | None = None,
) -> GetGeneratedPolicyResult:
    """Get generated policy.

    Args:
        job_id: Job id.
        include_resource_placeholders: Include resource placeholders.
        include_service_level_template: Include service level template.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if include_resource_placeholders is not None:
        kwargs["includeResourcePlaceholders"] = include_resource_placeholders
    if include_service_level_template is not None:
        kwargs["includeServiceLevelTemplate"] = include_service_level_template
    try:
        resp = await client.call("GetGeneratedPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get generated policy") from exc
    return GetGeneratedPolicyResult(
        job_details=resp.get("jobDetails"),
        generated_policy_result=resp.get("generatedPolicyResult"),
    )


async def list_access_preview_findings(
    access_preview_id: str,
    analyzer_arn: str,
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccessPreviewFindingsResult:
    """List access preview findings.

    Args:
        access_preview_id: Access preview id.
        analyzer_arn: Analyzer arn.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPreviewId"] = access_preview_id
    kwargs["analyzerArn"] = analyzer_arn
    if filter is not None:
        kwargs["filter"] = filter
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAccessPreviewFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access preview findings") from exc
    return ListAccessPreviewFindingsResult(
        findings=resp.get("findings"),
        next_token=resp.get("nextToken"),
    )


async def list_access_previews(
    analyzer_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccessPreviewsResult:
    """List access previews.

    Args:
        analyzer_arn: Analyzer arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAccessPreviews", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access previews") from exc
    return ListAccessPreviewsResult(
        access_previews=resp.get("accessPreviews"),
        next_token=resp.get("nextToken"),
    )


async def list_findings_v2(
    analyzer_arn: str,
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListFindingsV2Result:
    """List findings v2.

    Args:
        analyzer_arn: Analyzer arn.
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        sort: Sort.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["analyzerArn"] = analyzer_arn
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort is not None:
        kwargs["sort"] = sort
    try:
        resp = await client.call("ListFindingsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list findings v2") from exc
    return ListFindingsV2Result(
        findings=resp.get("findings"),
        next_token=resp.get("nextToken"),
    )


async def list_policy_generations(
    *,
    principal_arn: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPolicyGenerationsResult:
    """List policy generations.

    Args:
        principal_arn: Principal arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    if principal_arn is not None:
        kwargs["principalArn"] = principal_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPolicyGenerations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policy generations") from exc
    return ListPolicyGenerationsResult(
        policy_generations=resp.get("policyGenerations"),
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
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def start_policy_generation(
    policy_generation_details: dict[str, Any],
    *,
    cloud_trail_details: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartPolicyGenerationResult:
    """Start policy generation.

    Args:
        policy_generation_details: Policy generation details.
        cloud_trail_details: Cloud trail details.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyGenerationDetails"] = policy_generation_details
    if cloud_trail_details is not None:
        kwargs["cloudTrailDetails"] = cloud_trail_details
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("StartPolicyGeneration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start policy generation") from exc
    return StartPolicyGenerationResult(
        job_id=resp.get("jobId"),
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
    client = async_client("accessanalyzer", region_name)
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
    client = async_client("accessanalyzer", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
