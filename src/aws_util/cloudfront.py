"""aws_util.cloudfront — CloudFront distribution and invalidation utilities.

Provides helpers for managing CloudFront distributions, cache invalidations,
origin access controls, and cache policies through a simplified Pydantic-based
interface.
"""

from __future__ import annotations

import time
import uuid
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AssociateDistributionTenantWebAclResult",
    "AssociateDistributionWebAclResult",
    "CachePolicyResult",
    "CopyDistributionResult",
    "CreateAnycastIpListResult",
    "CreateCachePolicyResult",
    "CreateCloudFrontOriginAccessIdentityResult",
    "CreateConnectionGroupResult",
    "CreateContinuousDeploymentPolicyResult",
    "CreateDistributionTenantResult",
    "CreateDistributionWithTagsResult",
    "CreateFieldLevelEncryptionConfigResult",
    "CreateFieldLevelEncryptionProfileResult",
    "CreateFunctionResult",
    "CreateInvalidationForDistributionTenantResult",
    "CreateKeyGroupResult",
    "CreateKeyValueStoreResult",
    "CreateMonitoringSubscriptionResult",
    "CreateOriginRequestPolicyResult",
    "CreatePublicKeyResult",
    "CreateRealtimeLogConfigResult",
    "CreateResponseHeadersPolicyResult",
    "CreateStreamingDistributionResult",
    "CreateStreamingDistributionWithTagsResult",
    "CreateVpcOriginResult",
    "DeleteVpcOriginResult",
    "DescribeFunctionResult",
    "DescribeKeyValueStoreResult",
    "DisassociateDistributionTenantWebAclResult",
    "DisassociateDistributionWebAclResult",
    "DistributionResult",
    "GetAnycastIpListResult",
    "GetCachePolicyConfigResult",
    "GetCachePolicyResult",
    "GetCloudFrontOriginAccessIdentityConfigResult",
    "GetCloudFrontOriginAccessIdentityResult",
    "GetConnectionGroupByRoutingEndpointResult",
    "GetConnectionGroupResult",
    "GetContinuousDeploymentPolicyConfigResult",
    "GetContinuousDeploymentPolicyResult",
    "GetDistributionConfigResult",
    "GetDistributionTenantByDomainResult",
    "GetDistributionTenantResult",
    "GetFieldLevelEncryptionConfigResult",
    "GetFieldLevelEncryptionProfileConfigResult",
    "GetFieldLevelEncryptionProfileResult",
    "GetFieldLevelEncryptionResult",
    "GetFunctionResult",
    "GetInvalidationForDistributionTenantResult",
    "GetKeyGroupConfigResult",
    "GetKeyGroupResult",
    "GetManagedCertificateDetailsResult",
    "GetMonitoringSubscriptionResult",
    "GetOriginAccessControlConfigResult",
    "GetOriginRequestPolicyConfigResult",
    "GetOriginRequestPolicyResult",
    "GetPublicKeyConfigResult",
    "GetPublicKeyResult",
    "GetRealtimeLogConfigResult",
    "GetResourcePolicyResult",
    "GetResponseHeadersPolicyConfigResult",
    "GetResponseHeadersPolicyResult",
    "GetStreamingDistributionConfigResult",
    "GetStreamingDistributionResult",
    "GetVpcOriginResult",
    "InvalidationResult",
    "ListAnycastIpListsResult",
    "ListCachePoliciesResult",
    "ListCloudFrontOriginAccessIdentitiesResult",
    "ListConflictingAliasesResult",
    "ListConnectionGroupsResult",
    "ListContinuousDeploymentPoliciesResult",
    "ListDistributionTenantsByCustomizationResult",
    "ListDistributionTenantsResult",
    "ListDistributionsByAnycastIpListIdResult",
    "ListDistributionsByCachePolicyIdResult",
    "ListDistributionsByConnectionModeResult",
    "ListDistributionsByKeyGroupResult",
    "ListDistributionsByOriginRequestPolicyIdResult",
    "ListDistributionsByOwnedResourceResult",
    "ListDistributionsByRealtimeLogConfigResult",
    "ListDistributionsByResponseHeadersPolicyIdResult",
    "ListDistributionsByVpcOriginIdResult",
    "ListDistributionsByWebAclIdResult",
    "ListDomainConflictsResult",
    "ListFieldLevelEncryptionConfigsResult",
    "ListFieldLevelEncryptionProfilesResult",
    "ListFunctionsResult",
    "ListInvalidationsForDistributionTenantResult",
    "ListKeyGroupsResult",
    "ListKeyValueStoresResult",
    "ListOriginRequestPoliciesResult",
    "ListPublicKeysResult",
    "ListRealtimeLogConfigsResult",
    "ListResponseHeadersPoliciesResult",
    "ListStreamingDistributionsResult",
    "ListTagsForResourceResult",
    "ListVpcOriginsResult",
    "OriginAccessControlResult",
    "PublishFunctionResult",
    "PutResourcePolicyResult",
    "RunFunctionResult",
    "UpdateAnycastIpListResult",
    "UpdateCachePolicyResult",
    "UpdateCloudFrontOriginAccessIdentityResult",
    "UpdateConnectionGroupResult",
    "UpdateContinuousDeploymentPolicyResult",
    "UpdateDistributionTenantResult",
    "UpdateDistributionWithStagingConfigResult",
    "UpdateDomainAssociationResult",
    "UpdateFieldLevelEncryptionConfigResult",
    "UpdateFieldLevelEncryptionProfileResult",
    "UpdateFunctionResult",
    "UpdateKeyGroupResult",
    "UpdateKeyValueStoreResult",
    "UpdateOriginAccessControlResult",
    "UpdateOriginRequestPolicyResult",
    "UpdatePublicKeyResult",
    "UpdateRealtimeLogConfigResult",
    "UpdateResponseHeadersPolicyResult",
    "UpdateStreamingDistributionResult",
    "UpdateVpcOriginResult",
    "VerifyDnsConfigurationResult",
    "associate_alias",
    "associate_distribution_tenant_web_acl",
    "associate_distribution_web_acl",
    "copy_distribution",
    "create_anycast_ip_list",
    "create_cache_policy",
    "create_cloud_front_origin_access_identity",
    "create_connection_group",
    "create_continuous_deployment_policy",
    "create_distribution",
    "create_distribution_tenant",
    "create_distribution_with_tags",
    "create_field_level_encryption_config",
    "create_field_level_encryption_profile",
    "create_function",
    "create_invalidation",
    "create_invalidation_for_distribution_tenant",
    "create_key_group",
    "create_key_value_store",
    "create_monitoring_subscription",
    "create_origin_access_control",
    "create_origin_request_policy",
    "create_public_key",
    "create_realtime_log_config",
    "create_response_headers_policy",
    "create_streaming_distribution",
    "create_streaming_distribution_with_tags",
    "create_vpc_origin",
    "delete_anycast_ip_list",
    "delete_cache_policy",
    "delete_cloud_front_origin_access_identity",
    "delete_connection_group",
    "delete_continuous_deployment_policy",
    "delete_distribution",
    "delete_distribution_tenant",
    "delete_field_level_encryption_config",
    "delete_field_level_encryption_profile",
    "delete_function",
    "delete_key_group",
    "delete_key_value_store",
    "delete_monitoring_subscription",
    "delete_origin_access_control",
    "delete_origin_request_policy",
    "delete_public_key",
    "delete_realtime_log_config",
    "delete_resource_policy",
    "delete_response_headers_policy",
    "delete_streaming_distribution",
    "delete_vpc_origin",
    "describe_function",
    "describe_key_value_store",
    "disassociate_distribution_tenant_web_acl",
    "disassociate_distribution_web_acl",
    "get_anycast_ip_list",
    "get_cache_policy",
    "get_cache_policy_config",
    "get_cloud_front_origin_access_identity",
    "get_cloud_front_origin_access_identity_config",
    "get_connection_group",
    "get_connection_group_by_routing_endpoint",
    "get_continuous_deployment_policy",
    "get_continuous_deployment_policy_config",
    "get_distribution",
    "get_distribution_config",
    "get_distribution_tenant",
    "get_distribution_tenant_by_domain",
    "get_field_level_encryption",
    "get_field_level_encryption_config",
    "get_field_level_encryption_profile",
    "get_field_level_encryption_profile_config",
    "get_function",
    "get_invalidation",
    "get_invalidation_for_distribution_tenant",
    "get_key_group",
    "get_key_group_config",
    "get_managed_certificate_details",
    "get_monitoring_subscription",
    "get_origin_access_control",
    "get_origin_access_control_config",
    "get_origin_request_policy",
    "get_origin_request_policy_config",
    "get_public_key",
    "get_public_key_config",
    "get_realtime_log_config",
    "get_resource_policy",
    "get_response_headers_policy",
    "get_response_headers_policy_config",
    "get_streaming_distribution",
    "get_streaming_distribution_config",
    "get_vpc_origin",
    "invalidate_and_wait",
    "list_anycast_ip_lists",
    "list_cache_policies",
    "list_cloud_front_origin_access_identities",
    "list_conflicting_aliases",
    "list_connection_groups",
    "list_continuous_deployment_policies",
    "list_distribution_tenants",
    "list_distribution_tenants_by_customization",
    "list_distributions",
    "list_distributions_by_anycast_ip_list_id",
    "list_distributions_by_cache_policy_id",
    "list_distributions_by_connection_mode",
    "list_distributions_by_key_group",
    "list_distributions_by_origin_request_policy_id",
    "list_distributions_by_owned_resource",
    "list_distributions_by_realtime_log_config",
    "list_distributions_by_response_headers_policy_id",
    "list_distributions_by_vpc_origin_id",
    "list_distributions_by_web_acl_id",
    "list_domain_conflicts",
    "list_field_level_encryption_configs",
    "list_field_level_encryption_profiles",
    "list_functions",
    "list_invalidations",
    "list_invalidations_for_distribution_tenant",
    "list_key_groups",
    "list_key_value_stores",
    "list_origin_access_controls",
    "list_origin_request_policies",
    "list_public_keys",
    "list_realtime_log_configs",
    "list_response_headers_policies",
    "list_streaming_distributions",
    "list_tags_for_resource",
    "list_vpc_origins",
    "publish_function",
    "put_resource_policy",
    "run_function",
    "tag_resource",
    "untag_resource",
    "update_anycast_ip_list",
    "update_cache_policy",
    "update_cloud_front_origin_access_identity",
    "update_connection_group",
    "update_continuous_deployment_policy",
    "update_distribution",
    "update_distribution_tenant",
    "update_distribution_with_staging_config",
    "update_domain_association",
    "update_field_level_encryption_config",
    "update_field_level_encryption_profile",
    "update_function",
    "update_key_group",
    "update_key_value_store",
    "update_origin_access_control",
    "update_origin_request_policy",
    "update_public_key",
    "update_realtime_log_config",
    "update_response_headers_policy",
    "update_streaming_distribution",
    "update_vpc_origin",
    "verify_dns_configuration",
    "wait_for_distribution",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class DistributionResult(BaseModel):
    """A CloudFront distribution summary."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    domain_name: str
    status: str
    last_modified_time: str | None = None
    origins: list[dict[str, Any]] = []
    enabled: bool = True
    comment: str = ""
    etag: str | None = None
    extra: dict[str, Any] = {}


class InvalidationResult(BaseModel):
    """A CloudFront cache invalidation."""

    model_config = ConfigDict(frozen=True)

    id: str
    distribution_id: str
    status: str
    create_time: str | None = None
    paths: list[str] = []
    extra: dict[str, Any] = {}


class OriginAccessControlResult(BaseModel):
    """A CloudFront origin access control."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    signing_protocol: str = "sigv4"
    signing_behavior: str = "always"
    origin_type: str = "s3"
    extra: dict[str, Any] = {}


class CachePolicyResult(BaseModel):
    """A CloudFront cache policy."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    comment: str = ""
    min_ttl: int = 0
    max_ttl: int = 31536000
    default_ttl: int = 86400
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_distribution(
    dist: dict[str, Any],
    etag: str | None = None,
) -> DistributionResult:
    """Build a DistributionResult from an AWS response dict."""
    config = dist.get("DistributionConfig", dist)
    origins_data = config.get("Origins", dist.get("Origins", {}))
    if isinstance(origins_data, dict):
        origin_items = origins_data.get("Items", [])
    else:
        origin_items = origins_data

    last_mod = dist.get("LastModifiedTime")
    if last_mod is not None:
        last_mod = str(last_mod)

    return DistributionResult(
        id=dist.get("Id", ""),
        arn=dist.get("ARN", ""),
        domain_name=dist.get("DomainName", ""),
        status=dist.get("Status", ""),
        last_modified_time=last_mod,
        origins=origin_items,
        enabled=config.get("Enabled", True),
        comment=config.get("Comment", ""),
        etag=etag,
        extra={},
    )


def _parse_invalidation(
    inv: dict[str, Any],
    distribution_id: str,
) -> InvalidationResult:
    """Build an InvalidationResult from an AWS response dict."""
    batch = inv.get("InvalidationBatch", {})
    paths_obj = batch.get("Paths", {})
    path_items = paths_obj.get("Items", [])
    create_time = inv.get("CreateTime")
    if create_time is not None:
        create_time = str(create_time)

    return InvalidationResult(
        id=inv.get("Id", ""),
        distribution_id=distribution_id,
        status=inv.get("Status", ""),
        create_time=create_time,
        paths=path_items,
        extra={},
    )


# ---------------------------------------------------------------------------
# Distribution functions
# ---------------------------------------------------------------------------


def create_distribution(
    *,
    origins: list[dict[str, Any]],
    default_cache_behavior: dict[str, Any],
    comment: str = "",
    enabled: bool = True,
    caller_reference: str | None = None,
    region_name: str | None = None,
) -> DistributionResult:
    """Create a new CloudFront distribution.

    Args:
        origins: List of origin configuration dicts. Each must include
            ``DomainName``, ``Id``, and optionally ``S3OriginConfig``.
        default_cache_behavior: Default cache behavior configuration with
            ``TargetOriginId``, ``ViewerProtocolPolicy``, etc.
        comment: Human-readable comment for the distribution.
        enabled: Whether the distribution is enabled.
        caller_reference: Unique reference string. Defaults to a UUID.
        region_name: AWS region override.

    Returns:
        A :class:`DistributionResult` describing the new distribution.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    ref = caller_reference or str(uuid.uuid4())

    distribution_config: dict[str, Any] = {
        "CallerReference": ref,
        "Comment": comment,
        "Enabled": enabled,
        "Origins": {
            "Quantity": len(origins),
            "Items": origins,
        },
        "DefaultCacheBehavior": default_cache_behavior,
    }

    try:
        resp = client.create_distribution(
            DistributionConfig=distribution_config,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_distribution failed") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


def get_distribution(
    distribution_id: str,
    *,
    region_name: str | None = None,
) -> DistributionResult:
    """Fetch a CloudFront distribution by ID.

    Args:
        distribution_id: The distribution ID.
        region_name: AWS region override.

    Returns:
        A :class:`DistributionResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        resp = client.get_distribution(Id=distribution_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_distribution failed for {distribution_id!r}") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


def list_distributions(
    *,
    region_name: str | None = None,
) -> list[DistributionResult]:
    """List all CloudFront distributions in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`DistributionResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    results: list[DistributionResult] = []
    try:
        paginator = client.get_paginator("list_distributions")
        for page in paginator.paginate():
            dist_list = page.get("DistributionList", {})
            for dist in dist_list.get("Items", []):
                results.append(_parse_distribution(dist))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_distributions failed") from exc
    return results


def update_distribution(
    distribution_id: str,
    *,
    distribution_config: dict[str, Any],
    if_match: str,
    region_name: str | None = None,
) -> DistributionResult:
    """Update an existing CloudFront distribution.

    Args:
        distribution_id: The distribution ID.
        distribution_config: Full distribution configuration dict.
        if_match: The ETag of the current distribution (for optimistic
            concurrency control).
        region_name: AWS region override.

    Returns:
        A :class:`DistributionResult` with the updated state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        resp = client.update_distribution(
            DistributionConfig=distribution_config,
            Id=distribution_id,
            IfMatch=if_match,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_distribution failed for {distribution_id!r}") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


def delete_distribution(
    distribution_id: str,
    *,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete a CloudFront distribution.

    The distribution must be disabled before deletion.

    Args:
        distribution_id: The distribution ID.
        if_match: The ETag of the current distribution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        client.delete_distribution(Id=distribution_id, IfMatch=if_match)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_distribution failed for {distribution_id!r}") from exc


# ---------------------------------------------------------------------------
# Invalidation functions
# ---------------------------------------------------------------------------


def create_invalidation(
    distribution_id: str,
    *,
    paths: list[str],
    caller_reference: str | None = None,
    region_name: str | None = None,
) -> InvalidationResult:
    """Create a cache invalidation for a CloudFront distribution.

    Args:
        distribution_id: The distribution ID.
        paths: List of URL paths to invalidate (e.g. ``["/*"]``).
        caller_reference: Unique reference. Defaults to a UUID.
        region_name: AWS region override.

    Returns:
        An :class:`InvalidationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    ref = caller_reference or str(uuid.uuid4())

    try:
        resp = client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                "Paths": {
                    "Quantity": len(paths),
                    "Items": paths,
                },
                "CallerReference": ref,
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_invalidation failed for {distribution_id!r}") from exc

    inv = resp.get("Invalidation", {})
    return _parse_invalidation(inv, distribution_id)


def get_invalidation(
    distribution_id: str,
    invalidation_id: str,
    *,
    region_name: str | None = None,
) -> InvalidationResult:
    """Fetch a specific invalidation.

    Args:
        distribution_id: The distribution ID.
        invalidation_id: The invalidation ID.
        region_name: AWS region override.

    Returns:
        An :class:`InvalidationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        resp = client.get_invalidation(
            DistributionId=distribution_id,
            Id=invalidation_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_invalidation failed for {distribution_id!r}/{invalidation_id!r}",
        ) from exc

    inv = resp.get("Invalidation", {})
    return _parse_invalidation(inv, distribution_id)


def list_invalidations(
    distribution_id: str,
    *,
    region_name: str | None = None,
) -> list[InvalidationResult]:
    """List all invalidations for a CloudFront distribution.

    Args:
        distribution_id: The distribution ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`InvalidationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    results: list[InvalidationResult] = []
    try:
        paginator = client.get_paginator("list_invalidations")
        for page in paginator.paginate(DistributionId=distribution_id):
            inv_list = page.get("InvalidationList", {})
            for inv in inv_list.get("Items", []):
                create_time = inv.get("CreateTime")
                if create_time is not None:
                    create_time = str(create_time)
                results.append(
                    InvalidationResult(
                        id=inv.get("Id", ""),
                        distribution_id=distribution_id,
                        status=inv.get("Status", ""),
                        create_time=create_time,
                        paths=[],
                        extra={},
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_invalidations failed for {distribution_id!r}") from exc
    return results


# ---------------------------------------------------------------------------
# Origin Access Control functions
# ---------------------------------------------------------------------------


def create_origin_access_control(
    name: str,
    *,
    signing_protocol: str = "sigv4",
    signing_behavior: str = "always",
    origin_type: str = "s3",
    description: str = "",
    region_name: str | None = None,
) -> OriginAccessControlResult:
    """Create a CloudFront origin access control (OAC).

    Args:
        name: A unique name for the OAC.
        signing_protocol: Signing protocol (default ``"sigv4"``).
        signing_behavior: Signing behavior (default ``"always"``).
        origin_type: Origin type (default ``"s3"``).
        description: Human-readable description.
        region_name: AWS region override.

    Returns:
        An :class:`OriginAccessControlResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        resp = client.create_origin_access_control(
            OriginAccessControlConfig={
                "Name": name,
                "Description": description,
                "SigningProtocol": signing_protocol,
                "SigningBehavior": signing_behavior,
                "OriginAccessControlOriginType": origin_type,
            },
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_origin_access_control failed") from exc

    oac = resp.get("OriginAccessControl", {})
    config = oac.get("OriginAccessControlConfig", {})
    return OriginAccessControlResult(
        id=oac.get("Id", ""),
        name=config.get("Name", name),
        signing_protocol=config.get("SigningProtocol", signing_protocol),
        signing_behavior=config.get("SigningBehavior", signing_behavior),
        origin_type=config.get("OriginAccessControlOriginType", origin_type),
        extra={},
    )


def get_origin_access_control(
    oac_id: str,
    *,
    region_name: str | None = None,
) -> OriginAccessControlResult:
    """Fetch an origin access control by ID.

    Args:
        oac_id: The OAC ID.
        region_name: AWS region override.

    Returns:
        An :class:`OriginAccessControlResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        resp = client.get_origin_access_control(Id=oac_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_origin_access_control failed for {oac_id!r}") from exc

    oac = resp.get("OriginAccessControl", {})
    config = oac.get("OriginAccessControlConfig", {})
    return OriginAccessControlResult(
        id=oac.get("Id", ""),
        name=config.get("Name", ""),
        signing_protocol=config.get("SigningProtocol", "sigv4"),
        signing_behavior=config.get("SigningBehavior", "always"),
        origin_type=config.get("OriginAccessControlOriginType", "s3"),
        extra={},
    )


def list_origin_access_controls(
    *,
    region_name: str | None = None,
) -> list[OriginAccessControlResult]:
    """List all origin access controls.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`OriginAccessControlResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    results: list[OriginAccessControlResult] = []
    try:
        resp = client.list_origin_access_controls()
        oac_list = resp.get("OriginAccessControlList", {})
        for item in oac_list.get("Items", []):
            results.append(
                OriginAccessControlResult(
                    id=item.get("Id", ""),
                    name=item.get("Name", ""),
                    signing_protocol=item.get("SigningProtocol", "sigv4"),
                    signing_behavior=item.get("SigningBehavior", "always"),
                    origin_type=item.get("OriginAccessControlOriginType", "s3"),
                    extra={},
                )
            )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_origin_access_controls failed") from exc
    return results


def delete_origin_access_control(
    oac_id: str,
    *,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete an origin access control.

    Args:
        oac_id: The OAC ID.
        if_match: The ETag for optimistic concurrency.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    try:
        client.delete_origin_access_control(Id=oac_id, IfMatch=if_match)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_origin_access_control failed for {oac_id!r}") from exc


# ---------------------------------------------------------------------------
# Polling / wait utilities
# ---------------------------------------------------------------------------


def wait_for_distribution(
    distribution_id: str,
    *,
    target_status: str = "Deployed",
    timeout: float = 600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> DistributionResult:
    """Poll until a distribution reaches the target status.

    Args:
        distribution_id: The distribution ID.
        target_status: Status to wait for (default ``"Deployed"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`DistributionResult` once *target_status* is reached.

    Raises:
        AwsTimeoutError: If *timeout* is exceeded.
        RuntimeError: If an API call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = get_distribution(distribution_id, region_name=region_name)
        if result.status == target_status:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Distribution {distribution_id!r} did not reach "
                f"{target_status!r} within {timeout}s "
                f"(current: {result.status!r})"
            )
        time.sleep(poll_interval)


def invalidate_and_wait(
    distribution_id: str,
    *,
    paths: list[str],
    timeout: float = 300,
    poll_interval: float = 10,
    region_name: str | None = None,
) -> InvalidationResult:
    """Create a cache invalidation and poll until it completes.

    Args:
        distribution_id: The distribution ID.
        paths: URL paths to invalidate.
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`InvalidationResult` once status is ``"Completed"``.

    Raises:
        AwsTimeoutError: If *timeout* is exceeded.
        RuntimeError: If an API call fails.
    """
    inv = create_invalidation(distribution_id, paths=paths, region_name=region_name)
    deadline = time.monotonic() + timeout
    while True:
        current = get_invalidation(distribution_id, inv.id, region_name=region_name)
        if current.status.upper() == "COMPLETED":
            return current
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Invalidation {inv.id!r} did not complete within "
                f"{timeout}s (current: {current.status!r})"
            )
        time.sleep(poll_interval)


class AssociateDistributionTenantWebAclResult(BaseModel):
    """Result of associate_distribution_tenant_web_acl."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    web_acl_arn: str | None = None
    e_tag: str | None = None


class AssociateDistributionWebAclResult(BaseModel):
    """Result of associate_distribution_web_acl."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    web_acl_arn: str | None = None
    e_tag: str | None = None


class CopyDistributionResult(BaseModel):
    """Result of copy_distribution."""

    model_config = ConfigDict(frozen=True)

    distribution: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateAnycastIpListResult(BaseModel):
    """Result of create_anycast_ip_list."""

    model_config = ConfigDict(frozen=True)

    anycast_ip_list: dict[str, Any] | None = None
    e_tag: str | None = None


class CreateCachePolicyResult(BaseModel):
    """Result of create_cache_policy."""

    model_config = ConfigDict(frozen=True)

    cache_policy: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateCloudFrontOriginAccessIdentityResult(BaseModel):
    """Result of create_cloud_front_origin_access_identity."""

    model_config = ConfigDict(frozen=True)

    cloud_front_origin_access_identity: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateConnectionGroupResult(BaseModel):
    """Result of create_connection_group."""

    model_config = ConfigDict(frozen=True)

    connection_group: dict[str, Any] | None = None
    e_tag: str | None = None


class CreateContinuousDeploymentPolicyResult(BaseModel):
    """Result of create_continuous_deployment_policy."""

    model_config = ConfigDict(frozen=True)

    continuous_deployment_policy: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateDistributionTenantResult(BaseModel):
    """Result of create_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    distribution_tenant: dict[str, Any] | None = None
    e_tag: str | None = None


class CreateDistributionWithTagsResult(BaseModel):
    """Result of create_distribution_with_tags."""

    model_config = ConfigDict(frozen=True)

    distribution: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateFieldLevelEncryptionConfigResult(BaseModel):
    """Result of create_field_level_encryption_config."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateFieldLevelEncryptionProfileResult(BaseModel):
    """Result of create_field_level_encryption_profile."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_profile: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateFunctionResult(BaseModel):
    """Result of create_function."""

    model_config = ConfigDict(frozen=True)

    function_summary: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateInvalidationForDistributionTenantResult(BaseModel):
    """Result of create_invalidation_for_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    location: str | None = None
    invalidation: dict[str, Any] | None = None


class CreateKeyGroupResult(BaseModel):
    """Result of create_key_group."""

    model_config = ConfigDict(frozen=True)

    key_group: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateKeyValueStoreResult(BaseModel):
    """Result of create_key_value_store."""

    model_config = ConfigDict(frozen=True)

    key_value_store: dict[str, Any] | None = None
    e_tag: str | None = None
    location: str | None = None


class CreateMonitoringSubscriptionResult(BaseModel):
    """Result of create_monitoring_subscription."""

    model_config = ConfigDict(frozen=True)

    monitoring_subscription: dict[str, Any] | None = None


class CreateOriginRequestPolicyResult(BaseModel):
    """Result of create_origin_request_policy."""

    model_config = ConfigDict(frozen=True)

    origin_request_policy: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreatePublicKeyResult(BaseModel):
    """Result of create_public_key."""

    model_config = ConfigDict(frozen=True)

    public_key: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateRealtimeLogConfigResult(BaseModel):
    """Result of create_realtime_log_config."""

    model_config = ConfigDict(frozen=True)

    realtime_log_config: dict[str, Any] | None = None


class CreateResponseHeadersPolicyResult(BaseModel):
    """Result of create_response_headers_policy."""

    model_config = ConfigDict(frozen=True)

    response_headers_policy: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateStreamingDistributionResult(BaseModel):
    """Result of create_streaming_distribution."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateStreamingDistributionWithTagsResult(BaseModel):
    """Result of create_streaming_distribution_with_tags."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class CreateVpcOriginResult(BaseModel):
    """Result of create_vpc_origin."""

    model_config = ConfigDict(frozen=True)

    vpc_origin: dict[str, Any] | None = None
    location: str | None = None
    e_tag: str | None = None


class DeleteVpcOriginResult(BaseModel):
    """Result of delete_vpc_origin."""

    model_config = ConfigDict(frozen=True)

    vpc_origin: dict[str, Any] | None = None
    e_tag: str | None = None


class DescribeFunctionResult(BaseModel):
    """Result of describe_function."""

    model_config = ConfigDict(frozen=True)

    function_summary: dict[str, Any] | None = None
    e_tag: str | None = None


class DescribeKeyValueStoreResult(BaseModel):
    """Result of describe_key_value_store."""

    model_config = ConfigDict(frozen=True)

    key_value_store: dict[str, Any] | None = None
    e_tag: str | None = None


class DisassociateDistributionTenantWebAclResult(BaseModel):
    """Result of disassociate_distribution_tenant_web_acl."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    e_tag: str | None = None


class DisassociateDistributionWebAclResult(BaseModel):
    """Result of disassociate_distribution_web_acl."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    e_tag: str | None = None


class GetAnycastIpListResult(BaseModel):
    """Result of get_anycast_ip_list."""

    model_config = ConfigDict(frozen=True)

    anycast_ip_list: dict[str, Any] | None = None
    e_tag: str | None = None


class GetCachePolicyResult(BaseModel):
    """Result of get_cache_policy."""

    model_config = ConfigDict(frozen=True)

    cache_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class GetCachePolicyConfigResult(BaseModel):
    """Result of get_cache_policy_config."""

    model_config = ConfigDict(frozen=True)

    cache_policy_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetCloudFrontOriginAccessIdentityResult(BaseModel):
    """Result of get_cloud_front_origin_access_identity."""

    model_config = ConfigDict(frozen=True)

    cloud_front_origin_access_identity: dict[str, Any] | None = None
    e_tag: str | None = None


class GetCloudFrontOriginAccessIdentityConfigResult(BaseModel):
    """Result of get_cloud_front_origin_access_identity_config."""

    model_config = ConfigDict(frozen=True)

    cloud_front_origin_access_identity_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetConnectionGroupResult(BaseModel):
    """Result of get_connection_group."""

    model_config = ConfigDict(frozen=True)

    connection_group: dict[str, Any] | None = None
    e_tag: str | None = None


class GetConnectionGroupByRoutingEndpointResult(BaseModel):
    """Result of get_connection_group_by_routing_endpoint."""

    model_config = ConfigDict(frozen=True)

    connection_group: dict[str, Any] | None = None
    e_tag: str | None = None


class GetContinuousDeploymentPolicyResult(BaseModel):
    """Result of get_continuous_deployment_policy."""

    model_config = ConfigDict(frozen=True)

    continuous_deployment_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class GetContinuousDeploymentPolicyConfigResult(BaseModel):
    """Result of get_continuous_deployment_policy_config."""

    model_config = ConfigDict(frozen=True)

    continuous_deployment_policy_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetDistributionConfigResult(BaseModel):
    """Result of get_distribution_config."""

    model_config = ConfigDict(frozen=True)

    distribution_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetDistributionTenantResult(BaseModel):
    """Result of get_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    distribution_tenant: dict[str, Any] | None = None
    e_tag: str | None = None


class GetDistributionTenantByDomainResult(BaseModel):
    """Result of get_distribution_tenant_by_domain."""

    model_config = ConfigDict(frozen=True)

    distribution_tenant: dict[str, Any] | None = None
    e_tag: str | None = None


class GetFieldLevelEncryptionResult(BaseModel):
    """Result of get_field_level_encryption."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption: dict[str, Any] | None = None
    e_tag: str | None = None


class GetFieldLevelEncryptionConfigResult(BaseModel):
    """Result of get_field_level_encryption_config."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetFieldLevelEncryptionProfileResult(BaseModel):
    """Result of get_field_level_encryption_profile."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_profile: dict[str, Any] | None = None
    e_tag: str | None = None


class GetFieldLevelEncryptionProfileConfigResult(BaseModel):
    """Result of get_field_level_encryption_profile_config."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_profile_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetFunctionResult(BaseModel):
    """Result of get_function."""

    model_config = ConfigDict(frozen=True)

    function_code: bytes | None = None
    e_tag: str | None = None
    content_type: str | None = None


class GetInvalidationForDistributionTenantResult(BaseModel):
    """Result of get_invalidation_for_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    invalidation: dict[str, Any] | None = None


class GetKeyGroupResult(BaseModel):
    """Result of get_key_group."""

    model_config = ConfigDict(frozen=True)

    key_group: dict[str, Any] | None = None
    e_tag: str | None = None


class GetKeyGroupConfigResult(BaseModel):
    """Result of get_key_group_config."""

    model_config = ConfigDict(frozen=True)

    key_group_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetManagedCertificateDetailsResult(BaseModel):
    """Result of get_managed_certificate_details."""

    model_config = ConfigDict(frozen=True)

    managed_certificate_details: dict[str, Any] | None = None


class GetMonitoringSubscriptionResult(BaseModel):
    """Result of get_monitoring_subscription."""

    model_config = ConfigDict(frozen=True)

    monitoring_subscription: dict[str, Any] | None = None


class GetOriginAccessControlConfigResult(BaseModel):
    """Result of get_origin_access_control_config."""

    model_config = ConfigDict(frozen=True)

    origin_access_control_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetOriginRequestPolicyResult(BaseModel):
    """Result of get_origin_request_policy."""

    model_config = ConfigDict(frozen=True)

    origin_request_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class GetOriginRequestPolicyConfigResult(BaseModel):
    """Result of get_origin_request_policy_config."""

    model_config = ConfigDict(frozen=True)

    origin_request_policy_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetPublicKeyResult(BaseModel):
    """Result of get_public_key."""

    model_config = ConfigDict(frozen=True)

    public_key: dict[str, Any] | None = None
    e_tag: str | None = None


class GetPublicKeyConfigResult(BaseModel):
    """Result of get_public_key_config."""

    model_config = ConfigDict(frozen=True)

    public_key_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetRealtimeLogConfigResult(BaseModel):
    """Result of get_realtime_log_config."""

    model_config = ConfigDict(frozen=True)

    realtime_log_config: dict[str, Any] | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    policy_document: str | None = None


class GetResponseHeadersPolicyResult(BaseModel):
    """Result of get_response_headers_policy."""

    model_config = ConfigDict(frozen=True)

    response_headers_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class GetResponseHeadersPolicyConfigResult(BaseModel):
    """Result of get_response_headers_policy_config."""

    model_config = ConfigDict(frozen=True)

    response_headers_policy_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetStreamingDistributionResult(BaseModel):
    """Result of get_streaming_distribution."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution: dict[str, Any] | None = None
    e_tag: str | None = None


class GetStreamingDistributionConfigResult(BaseModel):
    """Result of get_streaming_distribution_config."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution_config: dict[str, Any] | None = None
    e_tag: str | None = None


class GetVpcOriginResult(BaseModel):
    """Result of get_vpc_origin."""

    model_config = ConfigDict(frozen=True)

    vpc_origin: dict[str, Any] | None = None
    e_tag: str | None = None


class ListAnycastIpListsResult(BaseModel):
    """Result of list_anycast_ip_lists."""

    model_config = ConfigDict(frozen=True)

    anycast_ip_lists: dict[str, Any] | None = None


class ListCachePoliciesResult(BaseModel):
    """Result of list_cache_policies."""

    model_config = ConfigDict(frozen=True)

    cache_policy_list: dict[str, Any] | None = None


class ListCloudFrontOriginAccessIdentitiesResult(BaseModel):
    """Result of list_cloud_front_origin_access_identities."""

    model_config = ConfigDict(frozen=True)

    cloud_front_origin_access_identity_list: dict[str, Any] | None = None


class ListConflictingAliasesResult(BaseModel):
    """Result of list_conflicting_aliases."""

    model_config = ConfigDict(frozen=True)

    conflicting_aliases_list: dict[str, Any] | None = None


class ListConnectionGroupsResult(BaseModel):
    """Result of list_connection_groups."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    connection_groups: list[dict[str, Any]] | None = None


class ListContinuousDeploymentPoliciesResult(BaseModel):
    """Result of list_continuous_deployment_policies."""

    model_config = ConfigDict(frozen=True)

    continuous_deployment_policy_list: dict[str, Any] | None = None


class ListDistributionTenantsResult(BaseModel):
    """Result of list_distribution_tenants."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    distribution_tenant_list: list[dict[str, Any]] | None = None


class ListDistributionTenantsByCustomizationResult(BaseModel):
    """Result of list_distribution_tenants_by_customization."""

    model_config = ConfigDict(frozen=True)

    next_marker: str | None = None
    distribution_tenant_list: list[dict[str, Any]] | None = None


class ListDistributionsByAnycastIpListIdResult(BaseModel):
    """Result of list_distributions_by_anycast_ip_list_id."""

    model_config = ConfigDict(frozen=True)

    distribution_list: dict[str, Any] | None = None


class ListDistributionsByCachePolicyIdResult(BaseModel):
    """Result of list_distributions_by_cache_policy_id."""

    model_config = ConfigDict(frozen=True)

    distribution_id_list: dict[str, Any] | None = None


class ListDistributionsByConnectionModeResult(BaseModel):
    """Result of list_distributions_by_connection_mode."""

    model_config = ConfigDict(frozen=True)

    distribution_list: dict[str, Any] | None = None


class ListDistributionsByKeyGroupResult(BaseModel):
    """Result of list_distributions_by_key_group."""

    model_config = ConfigDict(frozen=True)

    distribution_id_list: dict[str, Any] | None = None


class ListDistributionsByOriginRequestPolicyIdResult(BaseModel):
    """Result of list_distributions_by_origin_request_policy_id."""

    model_config = ConfigDict(frozen=True)

    distribution_id_list: dict[str, Any] | None = None


class ListDistributionsByOwnedResourceResult(BaseModel):
    """Result of list_distributions_by_owned_resource."""

    model_config = ConfigDict(frozen=True)

    distribution_list: dict[str, Any] | None = None


class ListDistributionsByRealtimeLogConfigResult(BaseModel):
    """Result of list_distributions_by_realtime_log_config."""

    model_config = ConfigDict(frozen=True)

    distribution_list: dict[str, Any] | None = None


class ListDistributionsByResponseHeadersPolicyIdResult(BaseModel):
    """Result of list_distributions_by_response_headers_policy_id."""

    model_config = ConfigDict(frozen=True)

    distribution_id_list: dict[str, Any] | None = None


class ListDistributionsByVpcOriginIdResult(BaseModel):
    """Result of list_distributions_by_vpc_origin_id."""

    model_config = ConfigDict(frozen=True)

    distribution_id_list: dict[str, Any] | None = None


class ListDistributionsByWebAclIdResult(BaseModel):
    """Result of list_distributions_by_web_acl_id."""

    model_config = ConfigDict(frozen=True)

    distribution_list: dict[str, Any] | None = None


class ListDomainConflictsResult(BaseModel):
    """Result of list_domain_conflicts."""

    model_config = ConfigDict(frozen=True)

    domain_conflicts: list[dict[str, Any]] | None = None
    next_marker: str | None = None


class ListFieldLevelEncryptionConfigsResult(BaseModel):
    """Result of list_field_level_encryption_configs."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_list: dict[str, Any] | None = None


class ListFieldLevelEncryptionProfilesResult(BaseModel):
    """Result of list_field_level_encryption_profiles."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_profile_list: dict[str, Any] | None = None


class ListFunctionsResult(BaseModel):
    """Result of list_functions."""

    model_config = ConfigDict(frozen=True)

    function_list: dict[str, Any] | None = None


class ListInvalidationsForDistributionTenantResult(BaseModel):
    """Result of list_invalidations_for_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    invalidation_list: dict[str, Any] | None = None


class ListKeyGroupsResult(BaseModel):
    """Result of list_key_groups."""

    model_config = ConfigDict(frozen=True)

    key_group_list: dict[str, Any] | None = None


class ListKeyValueStoresResult(BaseModel):
    """Result of list_key_value_stores."""

    model_config = ConfigDict(frozen=True)

    key_value_store_list: dict[str, Any] | None = None


class ListOriginRequestPoliciesResult(BaseModel):
    """Result of list_origin_request_policies."""

    model_config = ConfigDict(frozen=True)

    origin_request_policy_list: dict[str, Any] | None = None


class ListPublicKeysResult(BaseModel):
    """Result of list_public_keys."""

    model_config = ConfigDict(frozen=True)

    public_key_list: dict[str, Any] | None = None


class ListRealtimeLogConfigsResult(BaseModel):
    """Result of list_realtime_log_configs."""

    model_config = ConfigDict(frozen=True)

    realtime_log_configs: dict[str, Any] | None = None


class ListResponseHeadersPoliciesResult(BaseModel):
    """Result of list_response_headers_policies."""

    model_config = ConfigDict(frozen=True)

    response_headers_policy_list: dict[str, Any] | None = None


class ListStreamingDistributionsResult(BaseModel):
    """Result of list_streaming_distributions."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution_list: dict[str, Any] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListVpcOriginsResult(BaseModel):
    """Result of list_vpc_origins."""

    model_config = ConfigDict(frozen=True)

    vpc_origin_list: dict[str, Any] | None = None


class PublishFunctionResult(BaseModel):
    """Result of publish_function."""

    model_config = ConfigDict(frozen=True)

    function_summary: dict[str, Any] | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None


class RunFunctionResult(BaseModel):
    """Result of run_function."""

    model_config = ConfigDict(frozen=True)

    run_result: dict[str, Any] | None = None


class UpdateAnycastIpListResult(BaseModel):
    """Result of update_anycast_ip_list."""

    model_config = ConfigDict(frozen=True)

    anycast_ip_list: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateCachePolicyResult(BaseModel):
    """Result of update_cache_policy."""

    model_config = ConfigDict(frozen=True)

    cache_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateCloudFrontOriginAccessIdentityResult(BaseModel):
    """Result of update_cloud_front_origin_access_identity."""

    model_config = ConfigDict(frozen=True)

    cloud_front_origin_access_identity: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateConnectionGroupResult(BaseModel):
    """Result of update_connection_group."""

    model_config = ConfigDict(frozen=True)

    connection_group: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateContinuousDeploymentPolicyResult(BaseModel):
    """Result of update_continuous_deployment_policy."""

    model_config = ConfigDict(frozen=True)

    continuous_deployment_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateDistributionTenantResult(BaseModel):
    """Result of update_distribution_tenant."""

    model_config = ConfigDict(frozen=True)

    distribution_tenant: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateDistributionWithStagingConfigResult(BaseModel):
    """Result of update_distribution_with_staging_config."""

    model_config = ConfigDict(frozen=True)

    distribution: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateDomainAssociationResult(BaseModel):
    """Result of update_domain_association."""

    model_config = ConfigDict(frozen=True)

    domain: str | None = None
    resource_id: str | None = None
    e_tag: str | None = None


class UpdateFieldLevelEncryptionConfigResult(BaseModel):
    """Result of update_field_level_encryption_config."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateFieldLevelEncryptionProfileResult(BaseModel):
    """Result of update_field_level_encryption_profile."""

    model_config = ConfigDict(frozen=True)

    field_level_encryption_profile: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateFunctionResult(BaseModel):
    """Result of update_function."""

    model_config = ConfigDict(frozen=True)

    function_summary: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateKeyGroupResult(BaseModel):
    """Result of update_key_group."""

    model_config = ConfigDict(frozen=True)

    key_group: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateKeyValueStoreResult(BaseModel):
    """Result of update_key_value_store."""

    model_config = ConfigDict(frozen=True)

    key_value_store: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateOriginAccessControlResult(BaseModel):
    """Result of update_origin_access_control."""

    model_config = ConfigDict(frozen=True)

    origin_access_control: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateOriginRequestPolicyResult(BaseModel):
    """Result of update_origin_request_policy."""

    model_config = ConfigDict(frozen=True)

    origin_request_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdatePublicKeyResult(BaseModel):
    """Result of update_public_key."""

    model_config = ConfigDict(frozen=True)

    public_key: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateRealtimeLogConfigResult(BaseModel):
    """Result of update_realtime_log_config."""

    model_config = ConfigDict(frozen=True)

    realtime_log_config: dict[str, Any] | None = None


class UpdateResponseHeadersPolicyResult(BaseModel):
    """Result of update_response_headers_policy."""

    model_config = ConfigDict(frozen=True)

    response_headers_policy: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateStreamingDistributionResult(BaseModel):
    """Result of update_streaming_distribution."""

    model_config = ConfigDict(frozen=True)

    streaming_distribution: dict[str, Any] | None = None
    e_tag: str | None = None


class UpdateVpcOriginResult(BaseModel):
    """Result of update_vpc_origin."""

    model_config = ConfigDict(frozen=True)

    vpc_origin: dict[str, Any] | None = None
    e_tag: str | None = None


class VerifyDnsConfigurationResult(BaseModel):
    """Result of verify_dns_configuration."""

    model_config = ConfigDict(frozen=True)

    dns_configuration_list: list[dict[str, Any]] | None = None


def associate_alias(
    target_distribution_id: str,
    alias: str,
    region_name: str | None = None,
) -> None:
    """Associate alias.

    Args:
        target_distribution_id: Target distribution id.
        alias: Alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetDistributionId"] = target_distribution_id
    kwargs["Alias"] = alias
    try:
        client.associate_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate alias") from exc
    return None


def associate_distribution_tenant_web_acl(
    id: str,
    web_acl_arn: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> AssociateDistributionTenantWebAclResult:
    """Associate distribution tenant web acl.

    Args:
        id: Id.
        web_acl_arn: Web acl arn.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["WebACLArn"] = web_acl_arn
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.associate_distribution_tenant_web_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate distribution tenant web acl") from exc
    return AssociateDistributionTenantWebAclResult(
        id=resp.get("Id"),
        web_acl_arn=resp.get("WebACLArn"),
        e_tag=resp.get("ETag"),
    )


def associate_distribution_web_acl(
    id: str,
    web_acl_arn: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> AssociateDistributionWebAclResult:
    """Associate distribution web acl.

    Args:
        id: Id.
        web_acl_arn: Web acl arn.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["WebACLArn"] = web_acl_arn
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.associate_distribution_web_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate distribution web acl") from exc
    return AssociateDistributionWebAclResult(
        id=resp.get("Id"),
        web_acl_arn=resp.get("WebACLArn"),
        e_tag=resp.get("ETag"),
    )


def copy_distribution(
    primary_distribution_id: str,
    caller_reference: str,
    *,
    staging: bool | None = None,
    if_match: str | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> CopyDistributionResult:
    """Copy distribution.

    Args:
        primary_distribution_id: Primary distribution id.
        caller_reference: Caller reference.
        staging: Staging.
        if_match: If match.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PrimaryDistributionId"] = primary_distribution_id
    kwargs["CallerReference"] = caller_reference
    if staging is not None:
        kwargs["Staging"] = staging
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = client.copy_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy distribution") from exc
    return CopyDistributionResult(
        distribution=resp.get("Distribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_anycast_ip_list(
    name: str,
    ip_count: int,
    *,
    tags: dict[str, Any] | None = None,
    ip_address_type: str | None = None,
    region_name: str | None = None,
) -> CreateAnycastIpListResult:
    """Create anycast ip list.

    Args:
        name: Name.
        ip_count: Ip count.
        tags: Tags.
        ip_address_type: Ip address type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IpCount"] = ip_count
    if tags is not None:
        kwargs["Tags"] = tags
    if ip_address_type is not None:
        kwargs["IpAddressType"] = ip_address_type
    try:
        resp = client.create_anycast_ip_list(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create anycast ip list") from exc
    return CreateAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


def create_cache_policy(
    cache_policy_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateCachePolicyResult:
    """Create cache policy.

    Args:
        cache_policy_config: Cache policy config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyConfig"] = cache_policy_config
    try:
        resp = client.create_cache_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cache policy") from exc
    return CreateCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_cloud_front_origin_access_identity(
    cloud_front_origin_access_identity_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateCloudFrontOriginAccessIdentityResult:
    """Create cloud front origin access identity.

    Args:
        cloud_front_origin_access_identity_config: Cloud front origin access identity config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CloudFrontOriginAccessIdentityConfig"] = cloud_front_origin_access_identity_config
    try:
        resp = client.create_cloud_front_origin_access_identity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cloud front origin access identity") from exc
    return CreateCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_connection_group(
    name: str,
    *,
    ipv6_enabled: bool | None = None,
    tags: dict[str, Any] | None = None,
    anycast_ip_list_id: str | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateConnectionGroupResult:
    """Create connection group.

    Args:
        name: Name.
        ipv6_enabled: Ipv6 enabled.
        tags: Tags.
        anycast_ip_list_id: Anycast ip list id.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if ipv6_enabled is not None:
        kwargs["Ipv6Enabled"] = ipv6_enabled
    if tags is not None:
        kwargs["Tags"] = tags
    if anycast_ip_list_id is not None:
        kwargs["AnycastIpListId"] = anycast_ip_list_id
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = client.create_connection_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create connection group") from exc
    return CreateConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


def create_continuous_deployment_policy(
    continuous_deployment_policy_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateContinuousDeploymentPolicyResult:
    """Create continuous deployment policy.

    Args:
        continuous_deployment_policy_config: Continuous deployment policy config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContinuousDeploymentPolicyConfig"] = continuous_deployment_policy_config
    try:
        resp = client.create_continuous_deployment_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create continuous deployment policy") from exc
    return CreateContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_distribution_tenant(
    distribution_id: str,
    name: str,
    domains: list[dict[str, Any]],
    *,
    tags: dict[str, Any] | None = None,
    customizations: dict[str, Any] | None = None,
    parameters: list[dict[str, Any]] | None = None,
    connection_group_id: str | None = None,
    managed_certificate_request: dict[str, Any] | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateDistributionTenantResult:
    """Create distribution tenant.

    Args:
        distribution_id: Distribution id.
        name: Name.
        domains: Domains.
        tags: Tags.
        customizations: Customizations.
        parameters: Parameters.
        connection_group_id: Connection group id.
        managed_certificate_request: Managed certificate request.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    kwargs["Name"] = name
    kwargs["Domains"] = domains
    if tags is not None:
        kwargs["Tags"] = tags
    if customizations is not None:
        kwargs["Customizations"] = customizations
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if connection_group_id is not None:
        kwargs["ConnectionGroupId"] = connection_group_id
    if managed_certificate_request is not None:
        kwargs["ManagedCertificateRequest"] = managed_certificate_request
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = client.create_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create distribution tenant") from exc
    return CreateDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


def create_distribution_with_tags(
    distribution_config_with_tags: dict[str, Any],
    region_name: str | None = None,
) -> CreateDistributionWithTagsResult:
    """Create distribution with tags.

    Args:
        distribution_config_with_tags: Distribution config with tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionConfigWithTags"] = distribution_config_with_tags
    try:
        resp = client.create_distribution_with_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create distribution with tags") from exc
    return CreateDistributionWithTagsResult(
        distribution=resp.get("Distribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_field_level_encryption_config(
    field_level_encryption_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateFieldLevelEncryptionConfigResult:
    """Create field level encryption config.

    Args:
        field_level_encryption_config: Field level encryption config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionConfig"] = field_level_encryption_config
    try:
        resp = client.create_field_level_encryption_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create field level encryption config") from exc
    return CreateFieldLevelEncryptionConfigResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_field_level_encryption_profile(
    field_level_encryption_profile_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateFieldLevelEncryptionProfileResult:
    """Create field level encryption profile.

    Args:
        field_level_encryption_profile_config: Field level encryption profile config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionProfileConfig"] = field_level_encryption_profile_config
    try:
        resp = client.create_field_level_encryption_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create field level encryption profile") from exc
    return CreateFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_function(
    name: str,
    function_config: dict[str, Any],
    function_code: bytes,
    region_name: str | None = None,
) -> CreateFunctionResult:
    """Create function.

    Args:
        name: Name.
        function_config: Function config.
        function_code: Function code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["FunctionConfig"] = function_config
    kwargs["FunctionCode"] = function_code
    try:
        resp = client.create_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create function") from exc
    return CreateFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_invalidation_for_distribution_tenant(
    id: str,
    invalidation_batch: dict[str, Any],
    region_name: str | None = None,
) -> CreateInvalidationForDistributionTenantResult:
    """Create invalidation for distribution tenant.

    Args:
        id: Id.
        invalidation_batch: Invalidation batch.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["InvalidationBatch"] = invalidation_batch
    try:
        resp = client.create_invalidation_for_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create invalidation for distribution tenant") from exc
    return CreateInvalidationForDistributionTenantResult(
        location=resp.get("Location"),
        invalidation=resp.get("Invalidation"),
    )


def create_key_group(
    key_group_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateKeyGroupResult:
    """Create key group.

    Args:
        key_group_config: Key group config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupConfig"] = key_group_config
    try:
        resp = client.create_key_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create key group") from exc
    return CreateKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_key_value_store(
    name: str,
    *,
    comment: str | None = None,
    import_source: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateKeyValueStoreResult:
    """Create key value store.

    Args:
        name: Name.
        comment: Comment.
        import_source: Import source.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if comment is not None:
        kwargs["Comment"] = comment
    if import_source is not None:
        kwargs["ImportSource"] = import_source
    try:
        resp = client.create_key_value_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create key value store") from exc
    return CreateKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
        location=resp.get("Location"),
    )


def create_monitoring_subscription(
    distribution_id: str,
    monitoring_subscription: dict[str, Any],
    region_name: str | None = None,
) -> CreateMonitoringSubscriptionResult:
    """Create monitoring subscription.

    Args:
        distribution_id: Distribution id.
        monitoring_subscription: Monitoring subscription.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    kwargs["MonitoringSubscription"] = monitoring_subscription
    try:
        resp = client.create_monitoring_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create monitoring subscription") from exc
    return CreateMonitoringSubscriptionResult(
        monitoring_subscription=resp.get("MonitoringSubscription"),
    )


def create_origin_request_policy(
    origin_request_policy_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateOriginRequestPolicyResult:
    """Create origin request policy.

    Args:
        origin_request_policy_config: Origin request policy config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyConfig"] = origin_request_policy_config
    try:
        resp = client.create_origin_request_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create origin request policy") from exc
    return CreateOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_public_key(
    public_key_config: dict[str, Any],
    region_name: str | None = None,
) -> CreatePublicKeyResult:
    """Create public key.

    Args:
        public_key_config: Public key config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PublicKeyConfig"] = public_key_config
    try:
        resp = client.create_public_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create public key") from exc
    return CreatePublicKeyResult(
        public_key=resp.get("PublicKey"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_realtime_log_config(
    end_points: list[dict[str, Any]],
    fields: list[str],
    name: str,
    sampling_rate: int,
    region_name: str | None = None,
) -> CreateRealtimeLogConfigResult:
    """Create realtime log config.

    Args:
        end_points: End points.
        fields: Fields.
        name: Name.
        sampling_rate: Sampling rate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndPoints"] = end_points
    kwargs["Fields"] = fields
    kwargs["Name"] = name
    kwargs["SamplingRate"] = sampling_rate
    try:
        resp = client.create_realtime_log_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create realtime log config") from exc
    return CreateRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


def create_response_headers_policy(
    response_headers_policy_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateResponseHeadersPolicyResult:
    """Create response headers policy.

    Args:
        response_headers_policy_config: Response headers policy config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyConfig"] = response_headers_policy_config
    try:
        resp = client.create_response_headers_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create response headers policy") from exc
    return CreateResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_streaming_distribution(
    streaming_distribution_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateStreamingDistributionResult:
    """Create streaming distribution.

    Args:
        streaming_distribution_config: Streaming distribution config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfig"] = streaming_distribution_config
    try:
        resp = client.create_streaming_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create streaming distribution") from exc
    return CreateStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_streaming_distribution_with_tags(
    streaming_distribution_config_with_tags: dict[str, Any],
    region_name: str | None = None,
) -> CreateStreamingDistributionWithTagsResult:
    """Create streaming distribution with tags.

    Args:
        streaming_distribution_config_with_tags: Streaming distribution config with tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfigWithTags"] = streaming_distribution_config_with_tags
    try:
        resp = client.create_streaming_distribution_with_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create streaming distribution with tags") from exc
    return CreateStreamingDistributionWithTagsResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def create_vpc_origin(
    vpc_origin_endpoint_config: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateVpcOriginResult:
    """Create vpc origin.

    Args:
        vpc_origin_endpoint_config: Vpc origin endpoint config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginEndpointConfig"] = vpc_origin_endpoint_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_vpc_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vpc origin") from exc
    return CreateVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


def delete_anycast_ip_list(
    id: str,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete anycast ip list.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        client.delete_anycast_ip_list(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete anycast ip list") from exc
    return None


def delete_cache_policy(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete cache policy.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_cache_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cache policy") from exc
    return None


def delete_cloud_front_origin_access_identity(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete cloud front origin access identity.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_cloud_front_origin_access_identity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cloud front origin access identity") from exc
    return None


def delete_connection_group(
    id: str,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete connection group.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        client.delete_connection_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connection group") from exc
    return None


def delete_continuous_deployment_policy(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete continuous deployment policy.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_continuous_deployment_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete continuous deployment policy") from exc
    return None


def delete_distribution_tenant(
    id: str,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete distribution tenant.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        client.delete_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete distribution tenant") from exc
    return None


def delete_field_level_encryption_config(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete field level encryption config.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_field_level_encryption_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete field level encryption config") from exc
    return None


def delete_field_level_encryption_profile(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete field level encryption profile.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_field_level_encryption_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete field level encryption profile") from exc
    return None


def delete_function(
    name: str,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete function.

    Args:
        name: Name.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        client.delete_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete function") from exc
    return None


def delete_key_group(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete key group.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_key_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete key group") from exc
    return None


def delete_key_value_store(
    name: str,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete key value store.

    Args:
        name: Name.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        client.delete_key_value_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete key value store") from exc
    return None


def delete_monitoring_subscription(
    distribution_id: str,
    region_name: str | None = None,
) -> None:
    """Delete monitoring subscription.

    Args:
        distribution_id: Distribution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    try:
        client.delete_monitoring_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete monitoring subscription") from exc
    return None


def delete_origin_request_policy(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete origin request policy.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_origin_request_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete origin request policy") from exc
    return None


def delete_public_key(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete public key.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_public_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete public key") from exc
    return None


def delete_realtime_log_config(
    *,
    name: str | None = None,
    arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete realtime log config.

    Args:
        name: Name.
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if arn is not None:
        kwargs["ARN"] = arn
    try:
        client.delete_realtime_log_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete realtime log config") from exc
    return None


def delete_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def delete_response_headers_policy(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete response headers policy.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_response_headers_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete response headers policy") from exc
    return None


def delete_streaming_distribution(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete streaming distribution.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        client.delete_streaming_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete streaming distribution") from exc
    return None


def delete_vpc_origin(
    id: str,
    if_match: str,
    region_name: str | None = None,
) -> DeleteVpcOriginResult:
    """Delete vpc origin.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        resp = client.delete_vpc_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc origin") from exc
    return DeleteVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


def describe_function(
    name: str,
    *,
    stage: str | None = None,
    region_name: str | None = None,
) -> DescribeFunctionResult:
    """Describe function.

    Args:
        name: Name.
        stage: Stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = client.describe_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe function") from exc
    return DescribeFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        e_tag=resp.get("ETag"),
    )


def describe_key_value_store(
    name: str,
    region_name: str | None = None,
) -> DescribeKeyValueStoreResult:
    """Describe key value store.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_key_value_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe key value store") from exc
    return DescribeKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
    )


def disassociate_distribution_tenant_web_acl(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> DisassociateDistributionTenantWebAclResult:
    """Disassociate distribution tenant web acl.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.disassociate_distribution_tenant_web_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate distribution tenant web acl") from exc
    return DisassociateDistributionTenantWebAclResult(
        id=resp.get("Id"),
        e_tag=resp.get("ETag"),
    )


def disassociate_distribution_web_acl(
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> DisassociateDistributionWebAclResult:
    """Disassociate distribution web acl.

    Args:
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.disassociate_distribution_web_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate distribution web acl") from exc
    return DisassociateDistributionWebAclResult(
        id=resp.get("Id"),
        e_tag=resp.get("ETag"),
    )


def get_anycast_ip_list(
    id: str,
    region_name: str | None = None,
) -> GetAnycastIpListResult:
    """Get anycast ip list.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_anycast_ip_list(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get anycast ip list") from exc
    return GetAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


def get_cache_policy(
    id: str,
    region_name: str | None = None,
) -> GetCachePolicyResult:
    """Get cache policy.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_cache_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get cache policy") from exc
    return GetCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        e_tag=resp.get("ETag"),
    )


def get_cache_policy_config(
    id: str,
    region_name: str | None = None,
) -> GetCachePolicyConfigResult:
    """Get cache policy config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_cache_policy_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get cache policy config") from exc
    return GetCachePolicyConfigResult(
        cache_policy_config=resp.get("CachePolicyConfig"),
        e_tag=resp.get("ETag"),
    )


def get_cloud_front_origin_access_identity(
    id: str,
    region_name: str | None = None,
) -> GetCloudFrontOriginAccessIdentityResult:
    """Get cloud front origin access identity.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_cloud_front_origin_access_identity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get cloud front origin access identity") from exc
    return GetCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        e_tag=resp.get("ETag"),
    )


def get_cloud_front_origin_access_identity_config(
    id: str,
    region_name: str | None = None,
) -> GetCloudFrontOriginAccessIdentityConfigResult:
    """Get cloud front origin access identity config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_cloud_front_origin_access_identity_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get cloud front origin access identity config"
        ) from exc
    return GetCloudFrontOriginAccessIdentityConfigResult(
        cloud_front_origin_access_identity_config=resp.get("CloudFrontOriginAccessIdentityConfig"),
        e_tag=resp.get("ETag"),
    )


def get_connection_group(
    identifier: str,
    region_name: str | None = None,
) -> GetConnectionGroupResult:
    """Get connection group.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = client.get_connection_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get connection group") from exc
    return GetConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


def get_connection_group_by_routing_endpoint(
    routing_endpoint: str,
    region_name: str | None = None,
) -> GetConnectionGroupByRoutingEndpointResult:
    """Get connection group by routing endpoint.

    Args:
        routing_endpoint: Routing endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoutingEndpoint"] = routing_endpoint
    try:
        resp = client.get_connection_group_by_routing_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get connection group by routing endpoint") from exc
    return GetConnectionGroupByRoutingEndpointResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


def get_continuous_deployment_policy(
    id: str,
    region_name: str | None = None,
) -> GetContinuousDeploymentPolicyResult:
    """Get continuous deployment policy.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_continuous_deployment_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get continuous deployment policy") from exc
    return GetContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        e_tag=resp.get("ETag"),
    )


def get_continuous_deployment_policy_config(
    id: str,
    region_name: str | None = None,
) -> GetContinuousDeploymentPolicyConfigResult:
    """Get continuous deployment policy config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_continuous_deployment_policy_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get continuous deployment policy config") from exc
    return GetContinuousDeploymentPolicyConfigResult(
        continuous_deployment_policy_config=resp.get("ContinuousDeploymentPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


def get_distribution_config(
    id: str,
    region_name: str | None = None,
) -> GetDistributionConfigResult:
    """Get distribution config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_distribution_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get distribution config") from exc
    return GetDistributionConfigResult(
        distribution_config=resp.get("DistributionConfig"),
        e_tag=resp.get("ETag"),
    )


def get_distribution_tenant(
    identifier: str,
    region_name: str | None = None,
) -> GetDistributionTenantResult:
    """Get distribution tenant.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = client.get_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get distribution tenant") from exc
    return GetDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


def get_distribution_tenant_by_domain(
    domain: str,
    region_name: str | None = None,
) -> GetDistributionTenantByDomainResult:
    """Get distribution tenant by domain.

    Args:
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    try:
        resp = client.get_distribution_tenant_by_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get distribution tenant by domain") from exc
    return GetDistributionTenantByDomainResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


def get_field_level_encryption(
    id: str,
    region_name: str | None = None,
) -> GetFieldLevelEncryptionResult:
    """Get field level encryption.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_field_level_encryption(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption") from exc
    return GetFieldLevelEncryptionResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        e_tag=resp.get("ETag"),
    )


def get_field_level_encryption_config(
    id: str,
    region_name: str | None = None,
) -> GetFieldLevelEncryptionConfigResult:
    """Get field level encryption config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_field_level_encryption_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption config") from exc
    return GetFieldLevelEncryptionConfigResult(
        field_level_encryption_config=resp.get("FieldLevelEncryptionConfig"),
        e_tag=resp.get("ETag"),
    )


def get_field_level_encryption_profile(
    id: str,
    region_name: str | None = None,
) -> GetFieldLevelEncryptionProfileResult:
    """Get field level encryption profile.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_field_level_encryption_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption profile") from exc
    return GetFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        e_tag=resp.get("ETag"),
    )


def get_field_level_encryption_profile_config(
    id: str,
    region_name: str | None = None,
) -> GetFieldLevelEncryptionProfileConfigResult:
    """Get field level encryption profile config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_field_level_encryption_profile_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption profile config") from exc
    return GetFieldLevelEncryptionProfileConfigResult(
        field_level_encryption_profile_config=resp.get("FieldLevelEncryptionProfileConfig"),
        e_tag=resp.get("ETag"),
    )


def get_function(
    name: str,
    *,
    stage: str | None = None,
    region_name: str | None = None,
) -> GetFunctionResult:
    """Get function.

    Args:
        name: Name.
        stage: Stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = client.get_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get function") from exc
    return GetFunctionResult(
        function_code=resp.get("FunctionCode"),
        e_tag=resp.get("ETag"),
        content_type=resp.get("ContentType"),
    )


def get_invalidation_for_distribution_tenant(
    distribution_tenant_id: str,
    id: str,
    region_name: str | None = None,
) -> GetInvalidationForDistributionTenantResult:
    """Get invalidation for distribution tenant.

    Args:
        distribution_tenant_id: Distribution tenant id.
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionTenantId"] = distribution_tenant_id
    kwargs["Id"] = id
    try:
        resp = client.get_invalidation_for_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get invalidation for distribution tenant") from exc
    return GetInvalidationForDistributionTenantResult(
        invalidation=resp.get("Invalidation"),
    )


def get_key_group(
    id: str,
    region_name: str | None = None,
) -> GetKeyGroupResult:
    """Get key group.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_key_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get key group") from exc
    return GetKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        e_tag=resp.get("ETag"),
    )


def get_key_group_config(
    id: str,
    region_name: str | None = None,
) -> GetKeyGroupConfigResult:
    """Get key group config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_key_group_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get key group config") from exc
    return GetKeyGroupConfigResult(
        key_group_config=resp.get("KeyGroupConfig"),
        e_tag=resp.get("ETag"),
    )


def get_managed_certificate_details(
    identifier: str,
    region_name: str | None = None,
) -> GetManagedCertificateDetailsResult:
    """Get managed certificate details.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = client.get_managed_certificate_details(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get managed certificate details") from exc
    return GetManagedCertificateDetailsResult(
        managed_certificate_details=resp.get("ManagedCertificateDetails"),
    )


def get_monitoring_subscription(
    distribution_id: str,
    region_name: str | None = None,
) -> GetMonitoringSubscriptionResult:
    """Get monitoring subscription.

    Args:
        distribution_id: Distribution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    try:
        resp = client.get_monitoring_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get monitoring subscription") from exc
    return GetMonitoringSubscriptionResult(
        monitoring_subscription=resp.get("MonitoringSubscription"),
    )


def get_origin_access_control_config(
    id: str,
    region_name: str | None = None,
) -> GetOriginAccessControlConfigResult:
    """Get origin access control config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_origin_access_control_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get origin access control config") from exc
    return GetOriginAccessControlConfigResult(
        origin_access_control_config=resp.get("OriginAccessControlConfig"),
        e_tag=resp.get("ETag"),
    )


def get_origin_request_policy(
    id: str,
    region_name: str | None = None,
) -> GetOriginRequestPolicyResult:
    """Get origin request policy.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_origin_request_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get origin request policy") from exc
    return GetOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        e_tag=resp.get("ETag"),
    )


def get_origin_request_policy_config(
    id: str,
    region_name: str | None = None,
) -> GetOriginRequestPolicyConfigResult:
    """Get origin request policy config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_origin_request_policy_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get origin request policy config") from exc
    return GetOriginRequestPolicyConfigResult(
        origin_request_policy_config=resp.get("OriginRequestPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


def get_public_key(
    id: str,
    region_name: str | None = None,
) -> GetPublicKeyResult:
    """Get public key.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_public_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get public key") from exc
    return GetPublicKeyResult(
        public_key=resp.get("PublicKey"),
        e_tag=resp.get("ETag"),
    )


def get_public_key_config(
    id: str,
    region_name: str | None = None,
) -> GetPublicKeyConfigResult:
    """Get public key config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_public_key_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get public key config") from exc
    return GetPublicKeyConfigResult(
        public_key_config=resp.get("PublicKeyConfig"),
        e_tag=resp.get("ETag"),
    )


def get_realtime_log_config(
    *,
    name: str | None = None,
    arn: str | None = None,
    region_name: str | None = None,
) -> GetRealtimeLogConfigResult:
    """Get realtime log config.

    Args:
        name: Name.
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if arn is not None:
        kwargs["ARN"] = arn
    try:
        resp = client.get_realtime_log_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get realtime log config") from exc
    return GetRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        policy_document=resp.get("PolicyDocument"),
    )


def get_response_headers_policy(
    id: str,
    region_name: str | None = None,
) -> GetResponseHeadersPolicyResult:
    """Get response headers policy.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_response_headers_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get response headers policy") from exc
    return GetResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        e_tag=resp.get("ETag"),
    )


def get_response_headers_policy_config(
    id: str,
    region_name: str | None = None,
) -> GetResponseHeadersPolicyConfigResult:
    """Get response headers policy config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_response_headers_policy_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get response headers policy config") from exc
    return GetResponseHeadersPolicyConfigResult(
        response_headers_policy_config=resp.get("ResponseHeadersPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


def get_streaming_distribution(
    id: str,
    region_name: str | None = None,
) -> GetStreamingDistributionResult:
    """Get streaming distribution.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_streaming_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get streaming distribution") from exc
    return GetStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        e_tag=resp.get("ETag"),
    )


def get_streaming_distribution_config(
    id: str,
    region_name: str | None = None,
) -> GetStreamingDistributionConfigResult:
    """Get streaming distribution config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_streaming_distribution_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get streaming distribution config") from exc
    return GetStreamingDistributionConfigResult(
        streaming_distribution_config=resp.get("StreamingDistributionConfig"),
        e_tag=resp.get("ETag"),
    )


def get_vpc_origin(
    id: str,
    region_name: str | None = None,
) -> GetVpcOriginResult:
    """Get vpc origin.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_vpc_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get vpc origin") from exc
    return GetVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


def list_anycast_ip_lists(
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAnycastIpListsResult:
    """List anycast ip lists.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_anycast_ip_lists(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list anycast ip lists") from exc
    return ListAnycastIpListsResult(
        anycast_ip_lists=resp.get("AnycastIpLists"),
    )


def list_cache_policies(
    *,
    type_value: str | None = None,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListCachePoliciesResult:
    """List cache policies.

    Args:
        type_value: Type value.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_cache_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cache policies") from exc
    return ListCachePoliciesResult(
        cache_policy_list=resp.get("CachePolicyList"),
    )


def list_cloud_front_origin_access_identities(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListCloudFrontOriginAccessIdentitiesResult:
    """List cloud front origin access identities.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_cloud_front_origin_access_identities(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cloud front origin access identities") from exc
    return ListCloudFrontOriginAccessIdentitiesResult(
        cloud_front_origin_access_identity_list=resp.get("CloudFrontOriginAccessIdentityList"),
    )


def list_conflicting_aliases(
    distribution_id: str,
    alias: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListConflictingAliasesResult:
    """List conflicting aliases.

    Args:
        distribution_id: Distribution id.
        alias: Alias.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    kwargs["Alias"] = alias
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_conflicting_aliases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list conflicting aliases") from exc
    return ListConflictingAliasesResult(
        conflicting_aliases_list=resp.get("ConflictingAliasesList"),
    )


def list_connection_groups(
    *,
    association_filter: dict[str, Any] | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListConnectionGroupsResult:
    """List connection groups.

    Args:
        association_filter: Association filter.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if association_filter is not None:
        kwargs["AssociationFilter"] = association_filter
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_connection_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list connection groups") from exc
    return ListConnectionGroupsResult(
        next_marker=resp.get("NextMarker"),
        connection_groups=resp.get("ConnectionGroups"),
    )


def list_continuous_deployment_policies(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListContinuousDeploymentPoliciesResult:
    """List continuous deployment policies.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_continuous_deployment_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list continuous deployment policies") from exc
    return ListContinuousDeploymentPoliciesResult(
        continuous_deployment_policy_list=resp.get("ContinuousDeploymentPolicyList"),
    )


def list_distribution_tenants(
    *,
    association_filter: dict[str, Any] | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListDistributionTenantsResult:
    """List distribution tenants.

    Args:
        association_filter: Association filter.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if association_filter is not None:
        kwargs["AssociationFilter"] = association_filter
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distribution_tenants(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distribution tenants") from exc
    return ListDistributionTenantsResult(
        next_marker=resp.get("NextMarker"),
        distribution_tenant_list=resp.get("DistributionTenantList"),
    )


def list_distribution_tenants_by_customization(
    *,
    web_acl_arn: str | None = None,
    certificate_arn: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListDistributionTenantsByCustomizationResult:
    """List distribution tenants by customization.

    Args:
        web_acl_arn: Web acl arn.
        certificate_arn: Certificate arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if web_acl_arn is not None:
        kwargs["WebACLArn"] = web_acl_arn
    if certificate_arn is not None:
        kwargs["CertificateArn"] = certificate_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distribution_tenants_by_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distribution tenants by customization") from exc
    return ListDistributionTenantsByCustomizationResult(
        next_marker=resp.get("NextMarker"),
        distribution_tenant_list=resp.get("DistributionTenantList"),
    )


def list_distributions_by_anycast_ip_list_id(
    anycast_ip_list_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByAnycastIpListIdResult:
    """List distributions by anycast ip list id.

    Args:
        anycast_ip_list_id: Anycast ip list id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AnycastIpListId"] = anycast_ip_list_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_anycast_ip_list_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by anycast ip list id") from exc
    return ListDistributionsByAnycastIpListIdResult(
        distribution_list=resp.get("DistributionList"),
    )


def list_distributions_by_cache_policy_id(
    cache_policy_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByCachePolicyIdResult:
    """List distributions by cache policy id.

    Args:
        cache_policy_id: Cache policy id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyId"] = cache_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_cache_policy_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by cache policy id") from exc
    return ListDistributionsByCachePolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


def list_distributions_by_connection_mode(
    connection_mode: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListDistributionsByConnectionModeResult:
    """List distributions by connection mode.

    Args:
        connection_mode: Connection mode.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionMode"] = connection_mode
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_connection_mode(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by connection mode") from exc
    return ListDistributionsByConnectionModeResult(
        distribution_list=resp.get("DistributionList"),
    )


def list_distributions_by_key_group(
    key_group_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByKeyGroupResult:
    """List distributions by key group.

    Args:
        key_group_id: Key group id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupId"] = key_group_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_key_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by key group") from exc
    return ListDistributionsByKeyGroupResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


def list_distributions_by_origin_request_policy_id(
    origin_request_policy_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByOriginRequestPolicyIdResult:
    """List distributions by origin request policy id.

    Args:
        origin_request_policy_id: Origin request policy id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyId"] = origin_request_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_origin_request_policy_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list distributions by origin request policy id"
        ) from exc
    return ListDistributionsByOriginRequestPolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


def list_distributions_by_owned_resource(
    resource_arn: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByOwnedResourceResult:
    """List distributions by owned resource.

    Args:
        resource_arn: Resource arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_owned_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by owned resource") from exc
    return ListDistributionsByOwnedResourceResult(
        distribution_list=resp.get("DistributionList"),
    )


def list_distributions_by_realtime_log_config(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    realtime_log_config_name: str | None = None,
    realtime_log_config_arn: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByRealtimeLogConfigResult:
    """List distributions by realtime log config.

    Args:
        marker: Marker.
        max_items: Max items.
        realtime_log_config_name: Realtime log config name.
        realtime_log_config_arn: Realtime log config arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if realtime_log_config_name is not None:
        kwargs["RealtimeLogConfigName"] = realtime_log_config_name
    if realtime_log_config_arn is not None:
        kwargs["RealtimeLogConfigArn"] = realtime_log_config_arn
    try:
        resp = client.list_distributions_by_realtime_log_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by realtime log config") from exc
    return ListDistributionsByRealtimeLogConfigResult(
        distribution_list=resp.get("DistributionList"),
    )


def list_distributions_by_response_headers_policy_id(
    response_headers_policy_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByResponseHeadersPolicyIdResult:
    """List distributions by response headers policy id.

    Args:
        response_headers_policy_id: Response headers policy id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyId"] = response_headers_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_response_headers_policy_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list distributions by response headers policy id"
        ) from exc
    return ListDistributionsByResponseHeadersPolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


def list_distributions_by_vpc_origin_id(
    vpc_origin_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByVpcOriginIdResult:
    """List distributions by vpc origin id.

    Args:
        vpc_origin_id: Vpc origin id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginId"] = vpc_origin_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_vpc_origin_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by vpc origin id") from exc
    return ListDistributionsByVpcOriginIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


def list_distributions_by_web_acl_id(
    web_acl_id: str,
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListDistributionsByWebAclIdResult:
    """List distributions by web acl id.

    Args:
        web_acl_id: Web acl id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebACLId"] = web_acl_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_distributions_by_web_acl_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by web acl id") from exc
    return ListDistributionsByWebAclIdResult(
        distribution_list=resp.get("DistributionList"),
    )


def list_domain_conflicts(
    domain: str,
    domain_control_validation_resource: dict[str, Any],
    *,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListDomainConflictsResult:
    """List domain conflicts.

    Args:
        domain: Domain.
        domain_control_validation_resource: Domain control validation resource.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["DomainControlValidationResource"] = domain_control_validation_resource
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_domain_conflicts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list domain conflicts") from exc
    return ListDomainConflictsResult(
        domain_conflicts=resp.get("DomainConflicts"),
        next_marker=resp.get("NextMarker"),
    )


def list_field_level_encryption_configs(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListFieldLevelEncryptionConfigsResult:
    """List field level encryption configs.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_field_level_encryption_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list field level encryption configs") from exc
    return ListFieldLevelEncryptionConfigsResult(
        field_level_encryption_list=resp.get("FieldLevelEncryptionList"),
    )


def list_field_level_encryption_profiles(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListFieldLevelEncryptionProfilesResult:
    """List field level encryption profiles.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_field_level_encryption_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list field level encryption profiles") from exc
    return ListFieldLevelEncryptionProfilesResult(
        field_level_encryption_profile_list=resp.get("FieldLevelEncryptionProfileList"),
    )


def list_functions(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    stage: str | None = None,
    region_name: str | None = None,
) -> ListFunctionsResult:
    """List functions.

    Args:
        marker: Marker.
        max_items: Max items.
        stage: Stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = client.list_functions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list functions") from exc
    return ListFunctionsResult(
        function_list=resp.get("FunctionList"),
    )


def list_invalidations_for_distribution_tenant(
    id: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListInvalidationsForDistributionTenantResult:
    """List invalidations for distribution tenant.

    Args:
        id: Id.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_invalidations_for_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list invalidations for distribution tenant") from exc
    return ListInvalidationsForDistributionTenantResult(
        invalidation_list=resp.get("InvalidationList"),
    )


def list_key_groups(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListKeyGroupsResult:
    """List key groups.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_key_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list key groups") from exc
    return ListKeyGroupsResult(
        key_group_list=resp.get("KeyGroupList"),
    )


def list_key_value_stores(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> ListKeyValueStoresResult:
    """List key value stores.

    Args:
        marker: Marker.
        max_items: Max items.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = client.list_key_value_stores(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list key value stores") from exc
    return ListKeyValueStoresResult(
        key_value_store_list=resp.get("KeyValueStoreList"),
    )


def list_origin_request_policies(
    *,
    type_value: str | None = None,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListOriginRequestPoliciesResult:
    """List origin request policies.

    Args:
        type_value: Type value.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_origin_request_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list origin request policies") from exc
    return ListOriginRequestPoliciesResult(
        origin_request_policy_list=resp.get("OriginRequestPolicyList"),
    )


def list_public_keys(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListPublicKeysResult:
    """List public keys.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_public_keys(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list public keys") from exc
    return ListPublicKeysResult(
        public_key_list=resp.get("PublicKeyList"),
    )


def list_realtime_log_configs(
    *,
    max_items: str | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListRealtimeLogConfigsResult:
    """List realtime log configs.

    Args:
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_realtime_log_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list realtime log configs") from exc
    return ListRealtimeLogConfigsResult(
        realtime_log_configs=resp.get("RealtimeLogConfigs"),
    )


def list_response_headers_policies(
    *,
    type_value: str | None = None,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListResponseHeadersPoliciesResult:
    """List response headers policies.

    Args:
        type_value: Type value.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_response_headers_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list response headers policies") from exc
    return ListResponseHeadersPoliciesResult(
        response_headers_policy_list=resp.get("ResponseHeadersPolicyList"),
    )


def list_streaming_distributions(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListStreamingDistributionsResult:
    """List streaming distributions.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_streaming_distributions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list streaming distributions") from exc
    return ListStreamingDistributionsResult(
        streaming_distribution_list=resp.get("StreamingDistributionList"),
    )


def list_tags_for_resource(
    resource: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource: Resource.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_vpc_origins(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListVpcOriginsResult:
    """List vpc origins.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_vpc_origins(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list vpc origins") from exc
    return ListVpcOriginsResult(
        vpc_origin_list=resp.get("VpcOriginList"),
    )


def publish_function(
    name: str,
    if_match: str,
    region_name: str | None = None,
) -> PublishFunctionResult:
    """Publish function.

    Args:
        name: Name.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        resp = client.publish_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish function") from exc
    return PublishFunctionResult(
        function_summary=resp.get("FunctionSummary"),
    )


def put_resource_policy(
    resource_arn: str,
    policy_document: str,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy_document: Policy document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["PolicyDocument"] = policy_document
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
    )


def run_function(
    name: str,
    if_match: str,
    event_object: bytes,
    *,
    stage: str | None = None,
    region_name: str | None = None,
) -> RunFunctionResult:
    """Run function.

    Args:
        name: Name.
        if_match: If match.
        event_object: Event object.
        stage: Stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    kwargs["EventObject"] = event_object
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = client.test_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run function") from exc
    return RunFunctionResult(
        run_result=resp.get("TestResult"),
    )


def tag_resource(
    resource: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource: Resource.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource: str,
    tag_keys: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource: Resource.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_anycast_ip_list(
    id: str,
    if_match: str,
    *,
    ip_address_type: str | None = None,
    region_name: str | None = None,
) -> UpdateAnycastIpListResult:
    """Update anycast ip list.

    Args:
        id: Id.
        if_match: If match.
        ip_address_type: Ip address type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    if ip_address_type is not None:
        kwargs["IpAddressType"] = ip_address_type
    try:
        resp = client.update_anycast_ip_list(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update anycast ip list") from exc
    return UpdateAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


def update_cache_policy(
    cache_policy_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateCachePolicyResult:
    """Update cache policy.

    Args:
        cache_policy_config: Cache policy config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyConfig"] = cache_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_cache_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update cache policy") from exc
    return UpdateCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        e_tag=resp.get("ETag"),
    )


def update_cloud_front_origin_access_identity(
    cloud_front_origin_access_identity_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateCloudFrontOriginAccessIdentityResult:
    """Update cloud front origin access identity.

    Args:
        cloud_front_origin_access_identity_config: Cloud front origin access identity config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CloudFrontOriginAccessIdentityConfig"] = cloud_front_origin_access_identity_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_cloud_front_origin_access_identity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update cloud front origin access identity") from exc
    return UpdateCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        e_tag=resp.get("ETag"),
    )


def update_connection_group(
    id: str,
    if_match: str,
    *,
    ipv6_enabled: bool | None = None,
    anycast_ip_list_id: str | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateConnectionGroupResult:
    """Update connection group.

    Args:
        id: Id.
        if_match: If match.
        ipv6_enabled: Ipv6 enabled.
        anycast_ip_list_id: Anycast ip list id.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    if ipv6_enabled is not None:
        kwargs["Ipv6Enabled"] = ipv6_enabled
    if anycast_ip_list_id is not None:
        kwargs["AnycastIpListId"] = anycast_ip_list_id
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = client.update_connection_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update connection group") from exc
    return UpdateConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


def update_continuous_deployment_policy(
    continuous_deployment_policy_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateContinuousDeploymentPolicyResult:
    """Update continuous deployment policy.

    Args:
        continuous_deployment_policy_config: Continuous deployment policy config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContinuousDeploymentPolicyConfig"] = continuous_deployment_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_continuous_deployment_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update continuous deployment policy") from exc
    return UpdateContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        e_tag=resp.get("ETag"),
    )


def update_distribution_tenant(
    id: str,
    if_match: str,
    *,
    distribution_id: str | None = None,
    domains: list[dict[str, Any]] | None = None,
    customizations: dict[str, Any] | None = None,
    parameters: list[dict[str, Any]] | None = None,
    connection_group_id: str | None = None,
    managed_certificate_request: dict[str, Any] | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateDistributionTenantResult:
    """Update distribution tenant.

    Args:
        id: Id.
        if_match: If match.
        distribution_id: Distribution id.
        domains: Domains.
        customizations: Customizations.
        parameters: Parameters.
        connection_group_id: Connection group id.
        managed_certificate_request: Managed certificate request.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    if distribution_id is not None:
        kwargs["DistributionId"] = distribution_id
    if domains is not None:
        kwargs["Domains"] = domains
    if customizations is not None:
        kwargs["Customizations"] = customizations
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if connection_group_id is not None:
        kwargs["ConnectionGroupId"] = connection_group_id
    if managed_certificate_request is not None:
        kwargs["ManagedCertificateRequest"] = managed_certificate_request
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = client.update_distribution_tenant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update distribution tenant") from exc
    return UpdateDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


def update_distribution_with_staging_config(
    id: str,
    *,
    staging_distribution_id: str | None = None,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateDistributionWithStagingConfigResult:
    """Update distribution with staging config.

    Args:
        id: Id.
        staging_distribution_id: Staging distribution id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if staging_distribution_id is not None:
        kwargs["StagingDistributionId"] = staging_distribution_id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_distribution_with_staging_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update distribution with staging config") from exc
    return UpdateDistributionWithStagingConfigResult(
        distribution=resp.get("Distribution"),
        e_tag=resp.get("ETag"),
    )


def update_domain_association(
    domain: str,
    target_resource: dict[str, Any],
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateDomainAssociationResult:
    """Update domain association.

    Args:
        domain: Domain.
        target_resource: Target resource.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["TargetResource"] = target_resource
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_domain_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update domain association") from exc
    return UpdateDomainAssociationResult(
        domain=resp.get("Domain"),
        resource_id=resp.get("ResourceId"),
        e_tag=resp.get("ETag"),
    )


def update_field_level_encryption_config(
    field_level_encryption_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateFieldLevelEncryptionConfigResult:
    """Update field level encryption config.

    Args:
        field_level_encryption_config: Field level encryption config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionConfig"] = field_level_encryption_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_field_level_encryption_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update field level encryption config") from exc
    return UpdateFieldLevelEncryptionConfigResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        e_tag=resp.get("ETag"),
    )


def update_field_level_encryption_profile(
    field_level_encryption_profile_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateFieldLevelEncryptionProfileResult:
    """Update field level encryption profile.

    Args:
        field_level_encryption_profile_config: Field level encryption profile config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionProfileConfig"] = field_level_encryption_profile_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_field_level_encryption_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update field level encryption profile") from exc
    return UpdateFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        e_tag=resp.get("ETag"),
    )


def update_function(
    name: str,
    if_match: str,
    function_config: dict[str, Any],
    function_code: bytes,
    region_name: str | None = None,
) -> UpdateFunctionResult:
    """Update function.

    Args:
        name: Name.
        if_match: If match.
        function_config: Function config.
        function_code: Function code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    kwargs["FunctionConfig"] = function_config
    kwargs["FunctionCode"] = function_code
    try:
        resp = client.update_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update function") from exc
    return UpdateFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        e_tag=resp.get("ETag"),
    )


def update_key_group(
    key_group_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateKeyGroupResult:
    """Update key group.

    Args:
        key_group_config: Key group config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupConfig"] = key_group_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_key_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update key group") from exc
    return UpdateKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        e_tag=resp.get("ETag"),
    )


def update_key_value_store(
    name: str,
    comment: str,
    if_match: str,
    region_name: str | None = None,
) -> UpdateKeyValueStoreResult:
    """Update key value store.

    Args:
        name: Name.
        comment: Comment.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Comment"] = comment
    kwargs["IfMatch"] = if_match
    try:
        resp = client.update_key_value_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update key value store") from exc
    return UpdateKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
    )


def update_origin_access_control(
    origin_access_control_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateOriginAccessControlResult:
    """Update origin access control.

    Args:
        origin_access_control_config: Origin access control config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginAccessControlConfig"] = origin_access_control_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_origin_access_control(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update origin access control") from exc
    return UpdateOriginAccessControlResult(
        origin_access_control=resp.get("OriginAccessControl"),
        e_tag=resp.get("ETag"),
    )


def update_origin_request_policy(
    origin_request_policy_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateOriginRequestPolicyResult:
    """Update origin request policy.

    Args:
        origin_request_policy_config: Origin request policy config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyConfig"] = origin_request_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_origin_request_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update origin request policy") from exc
    return UpdateOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        e_tag=resp.get("ETag"),
    )


def update_public_key(
    public_key_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdatePublicKeyResult:
    """Update public key.

    Args:
        public_key_config: Public key config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PublicKeyConfig"] = public_key_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_public_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update public key") from exc
    return UpdatePublicKeyResult(
        public_key=resp.get("PublicKey"),
        e_tag=resp.get("ETag"),
    )


def update_realtime_log_config(
    *,
    end_points: list[dict[str, Any]] | None = None,
    fields: list[str] | None = None,
    name: str | None = None,
    arn: str | None = None,
    sampling_rate: int | None = None,
    region_name: str | None = None,
) -> UpdateRealtimeLogConfigResult:
    """Update realtime log config.

    Args:
        end_points: End points.
        fields: Fields.
        name: Name.
        arn: Arn.
        sampling_rate: Sampling rate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if end_points is not None:
        kwargs["EndPoints"] = end_points
    if fields is not None:
        kwargs["Fields"] = fields
    if name is not None:
        kwargs["Name"] = name
    if arn is not None:
        kwargs["ARN"] = arn
    if sampling_rate is not None:
        kwargs["SamplingRate"] = sampling_rate
    try:
        resp = client.update_realtime_log_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update realtime log config") from exc
    return UpdateRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


def update_response_headers_policy(
    response_headers_policy_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateResponseHeadersPolicyResult:
    """Update response headers policy.

    Args:
        response_headers_policy_config: Response headers policy config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyConfig"] = response_headers_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_response_headers_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update response headers policy") from exc
    return UpdateResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        e_tag=resp.get("ETag"),
    )


def update_streaming_distribution(
    streaming_distribution_config: dict[str, Any],
    id: str,
    *,
    if_match: str | None = None,
    region_name: str | None = None,
) -> UpdateStreamingDistributionResult:
    """Update streaming distribution.

    Args:
        streaming_distribution_config: Streaming distribution config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfig"] = streaming_distribution_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = client.update_streaming_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update streaming distribution") from exc
    return UpdateStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        e_tag=resp.get("ETag"),
    )


def update_vpc_origin(
    vpc_origin_endpoint_config: dict[str, Any],
    id: str,
    if_match: str,
    region_name: str | None = None,
) -> UpdateVpcOriginResult:
    """Update vpc origin.

    Args:
        vpc_origin_endpoint_config: Vpc origin endpoint config.
        id: Id.
        if_match: If match.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginEndpointConfig"] = vpc_origin_endpoint_config
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        resp = client.update_vpc_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update vpc origin") from exc
    return UpdateVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


def verify_dns_configuration(
    identifier: str,
    *,
    domain: str | None = None,
    region_name: str | None = None,
) -> VerifyDnsConfigurationResult:
    """Verify dns configuration.

    Args:
        identifier: Identifier.
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    if domain is not None:
        kwargs["Domain"] = domain
    try:
        resp = client.verify_dns_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to verify dns configuration") from exc
    return VerifyDnsConfigurationResult(
        dns_configuration_list=resp.get("DnsConfigurationList"),
    )
