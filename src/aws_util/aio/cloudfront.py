"""Native async CloudFront utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.cloudfront import (
    AssociateDistributionTenantWebAclResult,
    AssociateDistributionWebAclResult,
    CachePolicyResult,
    CopyDistributionResult,
    CreateAnycastIpListResult,
    CreateCachePolicyResult,
    CreateCloudFrontOriginAccessIdentityResult,
    CreateConnectionGroupResult,
    CreateContinuousDeploymentPolicyResult,
    CreateDistributionTenantResult,
    CreateDistributionWithTagsResult,
    CreateFieldLevelEncryptionConfigResult,
    CreateFieldLevelEncryptionProfileResult,
    CreateFunctionResult,
    CreateInvalidationForDistributionTenantResult,
    CreateKeyGroupResult,
    CreateKeyValueStoreResult,
    CreateMonitoringSubscriptionResult,
    CreateOriginRequestPolicyResult,
    CreatePublicKeyResult,
    CreateRealtimeLogConfigResult,
    CreateResponseHeadersPolicyResult,
    CreateStreamingDistributionResult,
    CreateStreamingDistributionWithTagsResult,
    CreateVpcOriginResult,
    DeleteVpcOriginResult,
    DescribeFunctionResult,
    DescribeKeyValueStoreResult,
    DisassociateDistributionTenantWebAclResult,
    DisassociateDistributionWebAclResult,
    DistributionResult,
    GetAnycastIpListResult,
    GetCachePolicyConfigResult,
    GetCachePolicyResult,
    GetCloudFrontOriginAccessIdentityConfigResult,
    GetCloudFrontOriginAccessIdentityResult,
    GetConnectionGroupByRoutingEndpointResult,
    GetConnectionGroupResult,
    GetContinuousDeploymentPolicyConfigResult,
    GetContinuousDeploymentPolicyResult,
    GetDistributionConfigResult,
    GetDistributionTenantByDomainResult,
    GetDistributionTenantResult,
    GetFieldLevelEncryptionConfigResult,
    GetFieldLevelEncryptionProfileConfigResult,
    GetFieldLevelEncryptionProfileResult,
    GetFieldLevelEncryptionResult,
    GetFunctionResult,
    GetInvalidationForDistributionTenantResult,
    GetKeyGroupConfigResult,
    GetKeyGroupResult,
    GetManagedCertificateDetailsResult,
    GetMonitoringSubscriptionResult,
    GetOriginAccessControlConfigResult,
    GetOriginRequestPolicyConfigResult,
    GetOriginRequestPolicyResult,
    GetPublicKeyConfigResult,
    GetPublicKeyResult,
    GetRealtimeLogConfigResult,
    GetResourcePolicyResult,
    GetResponseHeadersPolicyConfigResult,
    GetResponseHeadersPolicyResult,
    GetStreamingDistributionConfigResult,
    GetStreamingDistributionResult,
    GetVpcOriginResult,
    InvalidationResult,
    ListAnycastIpListsResult,
    ListCachePoliciesResult,
    ListCloudFrontOriginAccessIdentitiesResult,
    ListConflictingAliasesResult,
    ListConnectionGroupsResult,
    ListContinuousDeploymentPoliciesResult,
    ListDistributionsByAnycastIpListIdResult,
    ListDistributionsByCachePolicyIdResult,
    ListDistributionsByConnectionModeResult,
    ListDistributionsByKeyGroupResult,
    ListDistributionsByOriginRequestPolicyIdResult,
    ListDistributionsByOwnedResourceResult,
    ListDistributionsByRealtimeLogConfigResult,
    ListDistributionsByResponseHeadersPolicyIdResult,
    ListDistributionsByVpcOriginIdResult,
    ListDistributionsByWebAclIdResult,
    ListDistributionTenantsByCustomizationResult,
    ListDistributionTenantsResult,
    ListDomainConflictsResult,
    ListFieldLevelEncryptionConfigsResult,
    ListFieldLevelEncryptionProfilesResult,
    ListFunctionsResult,
    ListInvalidationsForDistributionTenantResult,
    ListKeyGroupsResult,
    ListKeyValueStoresResult,
    ListOriginRequestPoliciesResult,
    ListPublicKeysResult,
    ListRealtimeLogConfigsResult,
    ListResponseHeadersPoliciesResult,
    ListStreamingDistributionsResult,
    ListTagsForResourceResult,
    ListVpcOriginsResult,
    OriginAccessControlResult,
    PublishFunctionResult,
    PutResourcePolicyResult,
    RunFunctionResult,
    UpdateAnycastIpListResult,
    UpdateCachePolicyResult,
    UpdateCloudFrontOriginAccessIdentityResult,
    UpdateConnectionGroupResult,
    UpdateContinuousDeploymentPolicyResult,
    UpdateDistributionTenantResult,
    UpdateDistributionWithStagingConfigResult,
    UpdateDomainAssociationResult,
    UpdateFieldLevelEncryptionConfigResult,
    UpdateFieldLevelEncryptionProfileResult,
    UpdateFunctionResult,
    UpdateKeyGroupResult,
    UpdateKeyValueStoreResult,
    UpdateOriginAccessControlResult,
    UpdateOriginRequestPolicyResult,
    UpdatePublicKeyResult,
    UpdateRealtimeLogConfigResult,
    UpdateResponseHeadersPolicyResult,
    UpdateStreamingDistributionResult,
    UpdateVpcOriginResult,
    VerifyDnsConfigurationResult,
)
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


async def create_distribution(
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
        origins: List of origin configuration dicts.
        default_cache_behavior: Default cache behavior configuration.
        comment: Human-readable comment for the distribution.
        enabled: Whether the distribution is enabled.
        caller_reference: Unique reference string. Defaults to a UUID.
        region_name: AWS region override.

    Returns:
        A :class:`DistributionResult` describing the new distribution.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudfront", region_name)
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
        resp = await client.call(
            "CreateDistribution",
            DistributionConfig=distribution_config,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "create_distribution failed") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


async def get_distribution(
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
    client = async_client("cloudfront", region_name)
    try:
        resp = await client.call("GetDistribution", Id=distribution_id)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_distribution failed for {distribution_id!r}") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


async def list_distributions(
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
    client = async_client("cloudfront", region_name)
    results: list[DistributionResult] = []
    try:
        marker: str | None = None
        while True:
            kwargs: dict[str, Any] = {}
            if marker:
                kwargs["Marker"] = marker
            resp = await client.call("ListDistributions", **kwargs)
            dist_list = resp.get("DistributionList", {})
            for dist in dist_list.get("Items", []):
                results.append(_parse_distribution(dist))
            if not dist_list.get("IsTruncated", False):
                break
            marker = dist_list.get("NextMarker")
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_distributions failed") from exc
    return results


async def update_distribution(
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
        if_match: The ETag for optimistic concurrency control.
        region_name: AWS region override.

    Returns:
        A :class:`DistributionResult` with the updated state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudfront", region_name)
    try:
        resp = await client.call(
            "UpdateDistribution",
            DistributionConfig=distribution_config,
            Id=distribution_id,
            IfMatch=if_match,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_distribution failed for {distribution_id!r}") from exc

    dist = resp.get("Distribution", {})
    etag = resp.get("ETag")
    return _parse_distribution(dist, etag=etag)


async def delete_distribution(
    distribution_id: str,
    *,
    if_match: str,
    region_name: str | None = None,
) -> None:
    """Delete a CloudFront distribution.

    Args:
        distribution_id: The distribution ID.
        if_match: The ETag for optimistic concurrency.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudfront", region_name)
    try:
        await client.call("DeleteDistribution", Id=distribution_id, IfMatch=if_match)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_distribution failed for {distribution_id!r}") from exc


# ---------------------------------------------------------------------------
# Invalidation functions
# ---------------------------------------------------------------------------


async def create_invalidation(
    distribution_id: str,
    *,
    paths: list[str],
    caller_reference: str | None = None,
    region_name: str | None = None,
) -> InvalidationResult:
    """Create a cache invalidation for a CloudFront distribution.

    Args:
        distribution_id: The distribution ID.
        paths: List of URL paths to invalidate.
        caller_reference: Unique reference. Defaults to a UUID.
        region_name: AWS region override.

    Returns:
        An :class:`InvalidationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudfront", region_name)
    ref = caller_reference or str(uuid.uuid4())

    try:
        resp = await client.call(
            "CreateInvalidation",
            DistributionId=distribution_id,
            InvalidationBatch={
                "Paths": {
                    "Quantity": len(paths),
                    "Items": paths,
                },
                "CallerReference": ref,
            },
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_invalidation failed for {distribution_id!r}") from exc

    inv = resp.get("Invalidation", {})
    return _parse_invalidation(inv, distribution_id)


async def get_invalidation(
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
    client = async_client("cloudfront", region_name)
    try:
        resp = await client.call(
            "GetInvalidation",
            DistributionId=distribution_id,
            Id=invalidation_id,
        )
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_invalidation failed for {distribution_id!r}/{invalidation_id!r}",
        ) from exc

    inv = resp.get("Invalidation", {})
    return _parse_invalidation(inv, distribution_id)


async def list_invalidations(
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
    client = async_client("cloudfront", region_name)
    results: list[InvalidationResult] = []
    try:
        marker: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "DistributionId": distribution_id,
            }
            if marker:
                kwargs["Marker"] = marker
            resp = await client.call("ListInvalidations", **kwargs)
            inv_list = resp.get("InvalidationList", {})
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
            if not inv_list.get("IsTruncated", False):
                break
            marker = inv_list.get("NextMarker")
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"list_invalidations failed for {distribution_id!r}") from exc
    return results


# ---------------------------------------------------------------------------
# Origin Access Control functions
# ---------------------------------------------------------------------------


async def create_origin_access_control(
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
    client = async_client("cloudfront", region_name)
    try:
        resp = await client.call(
            "CreateOriginAccessControl",
            OriginAccessControlConfig={
                "Name": name,
                "Description": description,
                "SigningProtocol": signing_protocol,
                "SigningBehavior": signing_behavior,
                "OriginAccessControlOriginType": origin_type,
            },
        )
    except RuntimeError:
        raise
    except Exception as exc:
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


async def get_origin_access_control(
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
    client = async_client("cloudfront", region_name)
    try:
        resp = await client.call("GetOriginAccessControl", Id=oac_id)
    except RuntimeError:
        raise
    except Exception as exc:
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


async def list_origin_access_controls(
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
    client = async_client("cloudfront", region_name)
    results: list[OriginAccessControlResult] = []
    try:
        resp = await client.call("ListOriginAccessControls")
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
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_origin_access_controls failed") from exc
    return results


async def delete_origin_access_control(
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
    client = async_client("cloudfront", region_name)
    try:
        await client.call("DeleteOriginAccessControl", Id=oac_id, IfMatch=if_match)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_origin_access_control failed for {oac_id!r}") from exc


# ---------------------------------------------------------------------------
# Polling / wait utilities
# ---------------------------------------------------------------------------


async def wait_for_distribution(
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
        result = await get_distribution(distribution_id, region_name=region_name)
        if result.status == target_status:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Distribution {distribution_id!r} did not reach "
                f"{target_status!r} within {timeout}s "
                f"(current: {result.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def invalidate_and_wait(
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
    inv = await create_invalidation(distribution_id, paths=paths, region_name=region_name)
    deadline = time.monotonic() + timeout
    while True:
        current = await get_invalidation(distribution_id, inv.id, region_name=region_name)
        if current.status.upper() == "COMPLETED":
            return current
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Invalidation {inv.id!r} did not complete within "
                f"{timeout}s (current: {current.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def associate_alias(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetDistributionId"] = target_distribution_id
    kwargs["Alias"] = alias
    try:
        await client.call("AssociateAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate alias") from exc
    return None


async def associate_distribution_tenant_web_acl(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["WebACLArn"] = web_acl_arn
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("AssociateDistributionTenantWebACL", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate distribution tenant web acl") from exc
    return AssociateDistributionTenantWebAclResult(
        id=resp.get("Id"),
        web_acl_arn=resp.get("WebACLArn"),
        e_tag=resp.get("ETag"),
    )


async def associate_distribution_web_acl(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["WebACLArn"] = web_acl_arn
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("AssociateDistributionWebACL", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate distribution web acl") from exc
    return AssociateDistributionWebAclResult(
        id=resp.get("Id"),
        web_acl_arn=resp.get("WebACLArn"),
        e_tag=resp.get("ETag"),
    )


async def copy_distribution(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("CopyDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy distribution") from exc
    return CopyDistributionResult(
        distribution=resp.get("Distribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_anycast_ip_list(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IpCount"] = ip_count
    if tags is not None:
        kwargs["Tags"] = tags
    if ip_address_type is not None:
        kwargs["IpAddressType"] = ip_address_type
    try:
        resp = await client.call("CreateAnycastIpList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create anycast ip list") from exc
    return CreateAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


async def create_cache_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyConfig"] = cache_policy_config
    try:
        resp = await client.call("CreateCachePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cache policy") from exc
    return CreateCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_cloud_front_origin_access_identity(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CloudFrontOriginAccessIdentityConfig"] = cloud_front_origin_access_identity_config
    try:
        resp = await client.call("CreateCloudFrontOriginAccessIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cloud front origin access identity") from exc
    return CreateCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_connection_group(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("CreateConnectionGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create connection group") from exc
    return CreateConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


async def create_continuous_deployment_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContinuousDeploymentPolicyConfig"] = continuous_deployment_policy_config
    try:
        resp = await client.call("CreateContinuousDeploymentPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create continuous deployment policy") from exc
    return CreateContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("CreateDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create distribution tenant") from exc
    return CreateDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


async def create_distribution_with_tags(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionConfigWithTags"] = distribution_config_with_tags
    try:
        resp = await client.call("CreateDistributionWithTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create distribution with tags") from exc
    return CreateDistributionWithTagsResult(
        distribution=resp.get("Distribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_field_level_encryption_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionConfig"] = field_level_encryption_config
    try:
        resp = await client.call("CreateFieldLevelEncryptionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create field level encryption config") from exc
    return CreateFieldLevelEncryptionConfigResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_field_level_encryption_profile(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionProfileConfig"] = field_level_encryption_profile_config
    try:
        resp = await client.call("CreateFieldLevelEncryptionProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create field level encryption profile") from exc
    return CreateFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["FunctionConfig"] = function_config
    kwargs["FunctionCode"] = function_code
    try:
        resp = await client.call("CreateFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create function") from exc
    return CreateFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_invalidation_for_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["InvalidationBatch"] = invalidation_batch
    try:
        resp = await client.call("CreateInvalidationForDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create invalidation for distribution tenant") from exc
    return CreateInvalidationForDistributionTenantResult(
        location=resp.get("Location"),
        invalidation=resp.get("Invalidation"),
    )


async def create_key_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupConfig"] = key_group_config
    try:
        resp = await client.call("CreateKeyGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create key group") from exc
    return CreateKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_key_value_store(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if comment is not None:
        kwargs["Comment"] = comment
    if import_source is not None:
        kwargs["ImportSource"] = import_source
    try:
        resp = await client.call("CreateKeyValueStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create key value store") from exc
    return CreateKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
        location=resp.get("Location"),
    )


async def create_monitoring_subscription(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    kwargs["MonitoringSubscription"] = monitoring_subscription
    try:
        resp = await client.call("CreateMonitoringSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create monitoring subscription") from exc
    return CreateMonitoringSubscriptionResult(
        monitoring_subscription=resp.get("MonitoringSubscription"),
    )


async def create_origin_request_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyConfig"] = origin_request_policy_config
    try:
        resp = await client.call("CreateOriginRequestPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create origin request policy") from exc
    return CreateOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_public_key(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PublicKeyConfig"] = public_key_config
    try:
        resp = await client.call("CreatePublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create public key") from exc
    return CreatePublicKeyResult(
        public_key=resp.get("PublicKey"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_realtime_log_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndPoints"] = end_points
    kwargs["Fields"] = fields
    kwargs["Name"] = name
    kwargs["SamplingRate"] = sampling_rate
    try:
        resp = await client.call("CreateRealtimeLogConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create realtime log config") from exc
    return CreateRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


async def create_response_headers_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyConfig"] = response_headers_policy_config
    try:
        resp = await client.call("CreateResponseHeadersPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create response headers policy") from exc
    return CreateResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_streaming_distribution(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfig"] = streaming_distribution_config
    try:
        resp = await client.call("CreateStreamingDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create streaming distribution") from exc
    return CreateStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_streaming_distribution_with_tags(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfigWithTags"] = streaming_distribution_config_with_tags
    try:
        resp = await client.call("CreateStreamingDistributionWithTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create streaming distribution with tags") from exc
    return CreateStreamingDistributionWithTagsResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def create_vpc_origin(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginEndpointConfig"] = vpc_origin_endpoint_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVpcOrigin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc origin") from exc
    return CreateVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        location=resp.get("Location"),
        e_tag=resp.get("ETag"),
    )


async def delete_anycast_ip_list(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteAnycastIpList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete anycast ip list") from exc
    return None


async def delete_cache_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteCachePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cache policy") from exc
    return None


async def delete_cloud_front_origin_access_identity(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteCloudFrontOriginAccessIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cloud front origin access identity") from exc
    return None


async def delete_connection_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteConnectionGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete connection group") from exc
    return None


async def delete_continuous_deployment_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteContinuousDeploymentPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete continuous deployment policy") from exc
    return None


async def delete_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete distribution tenant") from exc
    return None


async def delete_field_level_encryption_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteFieldLevelEncryptionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete field level encryption config") from exc
    return None


async def delete_field_level_encryption_profile(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteFieldLevelEncryptionProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete field level encryption profile") from exc
    return None


async def delete_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete function") from exc
    return None


async def delete_key_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteKeyGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete key group") from exc
    return None


async def delete_key_value_store(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteKeyValueStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete key value store") from exc
    return None


async def delete_monitoring_subscription(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    try:
        await client.call("DeleteMonitoringSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete monitoring subscription") from exc
    return None


async def delete_origin_request_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteOriginRequestPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete origin request policy") from exc
    return None


async def delete_public_key(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeletePublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete public key") from exc
    return None


async def delete_realtime_log_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if arn is not None:
        kwargs["ARN"] = arn
    try:
        await client.call("DeleteRealtimeLogConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete realtime log config") from exc
    return None


async def delete_resource_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def delete_response_headers_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteResponseHeadersPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete response headers policy") from exc
    return None


async def delete_streaming_distribution(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        await client.call("DeleteStreamingDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete streaming distribution") from exc
    return None


async def delete_vpc_origin(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("DeleteVpcOrigin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc origin") from exc
    return DeleteVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


async def describe_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = await client.call("DescribeFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe function") from exc
    return DescribeFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        e_tag=resp.get("ETag"),
    )


async def describe_key_value_store(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DescribeKeyValueStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe key value store") from exc
    return DescribeKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
    )


async def disassociate_distribution_tenant_web_acl(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("DisassociateDistributionTenantWebACL", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate distribution tenant web acl") from exc
    return DisassociateDistributionTenantWebAclResult(
        id=resp.get("Id"),
        e_tag=resp.get("ETag"),
    )


async def disassociate_distribution_web_acl(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("DisassociateDistributionWebACL", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate distribution web acl") from exc
    return DisassociateDistributionWebAclResult(
        id=resp.get("Id"),
        e_tag=resp.get("ETag"),
    )


async def get_anycast_ip_list(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetAnycastIpList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get anycast ip list") from exc
    return GetAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


async def get_cache_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetCachePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cache policy") from exc
    return GetCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        e_tag=resp.get("ETag"),
    )


async def get_cache_policy_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetCachePolicyConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cache policy config") from exc
    return GetCachePolicyConfigResult(
        cache_policy_config=resp.get("CachePolicyConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_cloud_front_origin_access_identity(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetCloudFrontOriginAccessIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cloud front origin access identity") from exc
    return GetCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        e_tag=resp.get("ETag"),
    )


async def get_cloud_front_origin_access_identity_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetCloudFrontOriginAccessIdentityConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to get cloud front origin access identity config"
        ) from exc
    return GetCloudFrontOriginAccessIdentityConfigResult(
        cloud_front_origin_access_identity_config=resp.get("CloudFrontOriginAccessIdentityConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_connection_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = await client.call("GetConnectionGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connection group") from exc
    return GetConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


async def get_connection_group_by_routing_endpoint(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoutingEndpoint"] = routing_endpoint
    try:
        resp = await client.call("GetConnectionGroupByRoutingEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connection group by routing endpoint") from exc
    return GetConnectionGroupByRoutingEndpointResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


async def get_continuous_deployment_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetContinuousDeploymentPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get continuous deployment policy") from exc
    return GetContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        e_tag=resp.get("ETag"),
    )


async def get_continuous_deployment_policy_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetContinuousDeploymentPolicyConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get continuous deployment policy config") from exc
    return GetContinuousDeploymentPolicyConfigResult(
        continuous_deployment_policy_config=resp.get("ContinuousDeploymentPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_distribution_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetDistributionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution config") from exc
    return GetDistributionConfigResult(
        distribution_config=resp.get("DistributionConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = await client.call("GetDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution tenant") from exc
    return GetDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


async def get_distribution_tenant_by_domain(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    try:
        resp = await client.call("GetDistributionTenantByDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution tenant by domain") from exc
    return GetDistributionTenantByDomainResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


async def get_field_level_encryption(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetFieldLevelEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption") from exc
    return GetFieldLevelEncryptionResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        e_tag=resp.get("ETag"),
    )


async def get_field_level_encryption_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetFieldLevelEncryptionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption config") from exc
    return GetFieldLevelEncryptionConfigResult(
        field_level_encryption_config=resp.get("FieldLevelEncryptionConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_field_level_encryption_profile(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetFieldLevelEncryptionProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption profile") from exc
    return GetFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        e_tag=resp.get("ETag"),
    )


async def get_field_level_encryption_profile_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetFieldLevelEncryptionProfileConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get field level encryption profile config") from exc
    return GetFieldLevelEncryptionProfileConfigResult(
        field_level_encryption_profile_config=resp.get("FieldLevelEncryptionProfileConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = await client.call("GetFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get function") from exc
    return GetFunctionResult(
        function_code=resp.get("FunctionCode"),
        e_tag=resp.get("ETag"),
        content_type=resp.get("ContentType"),
    )


async def get_invalidation_for_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionTenantId"] = distribution_tenant_id
    kwargs["Id"] = id
    try:
        resp = await client.call("GetInvalidationForDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get invalidation for distribution tenant") from exc
    return GetInvalidationForDistributionTenantResult(
        invalidation=resp.get("Invalidation"),
    )


async def get_key_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetKeyGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get key group") from exc
    return GetKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        e_tag=resp.get("ETag"),
    )


async def get_key_group_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetKeyGroupConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get key group config") from exc
    return GetKeyGroupConfigResult(
        key_group_config=resp.get("KeyGroupConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_managed_certificate_details(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = await client.call("GetManagedCertificateDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get managed certificate details") from exc
    return GetManagedCertificateDetailsResult(
        managed_certificate_details=resp.get("ManagedCertificateDetails"),
    )


async def get_monitoring_subscription(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    try:
        resp = await client.call("GetMonitoringSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get monitoring subscription") from exc
    return GetMonitoringSubscriptionResult(
        monitoring_subscription=resp.get("MonitoringSubscription"),
    )


async def get_origin_access_control_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetOriginAccessControlConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get origin access control config") from exc
    return GetOriginAccessControlConfigResult(
        origin_access_control_config=resp.get("OriginAccessControlConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_origin_request_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetOriginRequestPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get origin request policy") from exc
    return GetOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        e_tag=resp.get("ETag"),
    )


async def get_origin_request_policy_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetOriginRequestPolicyConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get origin request policy config") from exc
    return GetOriginRequestPolicyConfigResult(
        origin_request_policy_config=resp.get("OriginRequestPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_public_key(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetPublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get public key") from exc
    return GetPublicKeyResult(
        public_key=resp.get("PublicKey"),
        e_tag=resp.get("ETag"),
    )


async def get_public_key_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetPublicKeyConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get public key config") from exc
    return GetPublicKeyConfigResult(
        public_key_config=resp.get("PublicKeyConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_realtime_log_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if arn is not None:
        kwargs["ARN"] = arn
    try:
        resp = await client.call("GetRealtimeLogConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get realtime log config") from exc
    return GetRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


async def get_resource_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        policy_document=resp.get("PolicyDocument"),
    )


async def get_response_headers_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetResponseHeadersPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get response headers policy") from exc
    return GetResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        e_tag=resp.get("ETag"),
    )


async def get_response_headers_policy_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetResponseHeadersPolicyConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get response headers policy config") from exc
    return GetResponseHeadersPolicyConfigResult(
        response_headers_policy_config=resp.get("ResponseHeadersPolicyConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_streaming_distribution(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetStreamingDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get streaming distribution") from exc
    return GetStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        e_tag=resp.get("ETag"),
    )


async def get_streaming_distribution_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetStreamingDistributionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get streaming distribution config") from exc
    return GetStreamingDistributionConfigResult(
        streaming_distribution_config=resp.get("StreamingDistributionConfig"),
        e_tag=resp.get("ETag"),
    )


async def get_vpc_origin(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetVpcOrigin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get vpc origin") from exc
    return GetVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


async def list_anycast_ip_lists(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAnycastIpLists", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list anycast ip lists") from exc
    return ListAnycastIpListsResult(
        anycast_ip_lists=resp.get("AnycastIpLists"),
    )


async def list_cache_policies(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListCachePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cache policies") from exc
    return ListCachePoliciesResult(
        cache_policy_list=resp.get("CachePolicyList"),
    )


async def list_cloud_front_origin_access_identities(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListCloudFrontOriginAccessIdentities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cloud front origin access identities") from exc
    return ListCloudFrontOriginAccessIdentitiesResult(
        cloud_front_origin_access_identity_list=resp.get("CloudFrontOriginAccessIdentityList"),
    )


async def list_conflicting_aliases(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DistributionId"] = distribution_id
    kwargs["Alias"] = alias
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListConflictingAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list conflicting aliases") from exc
    return ListConflictingAliasesResult(
        conflicting_aliases_list=resp.get("ConflictingAliasesList"),
    )


async def list_connection_groups(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if association_filter is not None:
        kwargs["AssociationFilter"] = association_filter
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListConnectionGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list connection groups") from exc
    return ListConnectionGroupsResult(
        next_marker=resp.get("NextMarker"),
        connection_groups=resp.get("ConnectionGroups"),
    )


async def list_continuous_deployment_policies(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListContinuousDeploymentPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list continuous deployment policies") from exc
    return ListContinuousDeploymentPoliciesResult(
        continuous_deployment_policy_list=resp.get("ContinuousDeploymentPolicyList"),
    )


async def list_distribution_tenants(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if association_filter is not None:
        kwargs["AssociationFilter"] = association_filter
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionTenants", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distribution tenants") from exc
    return ListDistributionTenantsResult(
        next_marker=resp.get("NextMarker"),
        distribution_tenant_list=resp.get("DistributionTenantList"),
    )


async def list_distribution_tenants_by_customization(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("ListDistributionTenantsByCustomization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distribution tenants by customization") from exc
    return ListDistributionTenantsByCustomizationResult(
        next_marker=resp.get("NextMarker"),
        distribution_tenant_list=resp.get("DistributionTenantList"),
    )


async def list_distributions_by_anycast_ip_list_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AnycastIpListId"] = anycast_ip_list_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByAnycastIpListId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by anycast ip list id") from exc
    return ListDistributionsByAnycastIpListIdResult(
        distribution_list=resp.get("DistributionList"),
    )


async def list_distributions_by_cache_policy_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyId"] = cache_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByCachePolicyId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by cache policy id") from exc
    return ListDistributionsByCachePolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


async def list_distributions_by_connection_mode(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionMode"] = connection_mode
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByConnectionMode", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by connection mode") from exc
    return ListDistributionsByConnectionModeResult(
        distribution_list=resp.get("DistributionList"),
    )


async def list_distributions_by_key_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupId"] = key_group_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByKeyGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by key group") from exc
    return ListDistributionsByKeyGroupResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


async def list_distributions_by_origin_request_policy_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyId"] = origin_request_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByOriginRequestPolicyId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list distributions by origin request policy id"
        ) from exc
    return ListDistributionsByOriginRequestPolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


async def list_distributions_by_owned_resource(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByOwnedResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by owned resource") from exc
    return ListDistributionsByOwnedResourceResult(
        distribution_list=resp.get("DistributionList"),
    )


async def list_distributions_by_realtime_log_config(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("ListDistributionsByRealtimeLogConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by realtime log config") from exc
    return ListDistributionsByRealtimeLogConfigResult(
        distribution_list=resp.get("DistributionList"),
    )


async def list_distributions_by_response_headers_policy_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyId"] = response_headers_policy_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByResponseHeadersPolicyId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list distributions by response headers policy id"
        ) from exc
    return ListDistributionsByResponseHeadersPolicyIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


async def list_distributions_by_vpc_origin_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginId"] = vpc_origin_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByVpcOriginId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by vpc origin id") from exc
    return ListDistributionsByVpcOriginIdResult(
        distribution_id_list=resp.get("DistributionIdList"),
    )


async def list_distributions_by_web_acl_id(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WebACLId"] = web_acl_id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListDistributionsByWebACLId", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list distributions by web acl id") from exc
    return ListDistributionsByWebAclIdResult(
        distribution_list=resp.get("DistributionList"),
    )


async def list_domain_conflicts(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["DomainControlValidationResource"] = domain_control_validation_resource
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("ListDomainConflicts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list domain conflicts") from exc
    return ListDomainConflictsResult(
        domain_conflicts=resp.get("DomainConflicts"),
        next_marker=resp.get("NextMarker"),
    )


async def list_field_level_encryption_configs(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListFieldLevelEncryptionConfigs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list field level encryption configs") from exc
    return ListFieldLevelEncryptionConfigsResult(
        field_level_encryption_list=resp.get("FieldLevelEncryptionList"),
    )


async def list_field_level_encryption_profiles(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListFieldLevelEncryptionProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list field level encryption profiles") from exc
    return ListFieldLevelEncryptionProfilesResult(
        field_level_encryption_profile_list=resp.get("FieldLevelEncryptionProfileList"),
    )


async def list_functions(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = await client.call("ListFunctions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list functions") from exc
    return ListFunctionsResult(
        function_list=resp.get("FunctionList"),
    )


async def list_invalidations_for_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListInvalidationsForDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list invalidations for distribution tenant") from exc
    return ListInvalidationsForDistributionTenantResult(
        invalidation_list=resp.get("InvalidationList"),
    )


async def list_key_groups(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListKeyGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list key groups") from exc
    return ListKeyGroupsResult(
        key_group_list=resp.get("KeyGroupList"),
    )


async def list_key_value_stores(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = await client.call("ListKeyValueStores", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list key value stores") from exc
    return ListKeyValueStoresResult(
        key_value_store_list=resp.get("KeyValueStoreList"),
    )


async def list_origin_request_policies(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListOriginRequestPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list origin request policies") from exc
    return ListOriginRequestPoliciesResult(
        origin_request_policy_list=resp.get("OriginRequestPolicyList"),
    )


async def list_public_keys(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListPublicKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list public keys") from exc
    return ListPublicKeysResult(
        public_key_list=resp.get("PublicKeyList"),
    )


async def list_realtime_log_configs(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("ListRealtimeLogConfigs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list realtime log configs") from exc
    return ListRealtimeLogConfigsResult(
        realtime_log_configs=resp.get("RealtimeLogConfigs"),
    )


async def list_response_headers_policies(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListResponseHeadersPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list response headers policies") from exc
    return ListResponseHeadersPoliciesResult(
        response_headers_policy_list=resp.get("ResponseHeadersPolicyList"),
    )


async def list_streaming_distributions(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListStreamingDistributions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list streaming distributions") from exc
    return ListStreamingDistributionsResult(
        streaming_distribution_list=resp.get("StreamingDistributionList"),
    )


async def list_tags_for_resource(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_vpc_origins(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListVpcOrigins", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list vpc origins") from exc
    return ListVpcOriginsResult(
        vpc_origin_list=resp.get("VpcOriginList"),
    )


async def publish_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("PublishFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to publish function") from exc
    return PublishFunctionResult(
        function_summary=resp.get("FunctionSummary"),
    )


async def put_resource_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["PolicyDocument"] = policy_document
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
    )


async def run_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    kwargs["EventObject"] = event_object
    if stage is not None:
        kwargs["Stage"] = stage
    try:
        resp = await client.call("TestFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run function") from exc
    return RunFunctionResult(
        run_result=resp.get("TestResult"),
    )


async def tag_resource(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Resource"] = resource
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_anycast_ip_list(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    if ip_address_type is not None:
        kwargs["IpAddressType"] = ip_address_type
    try:
        resp = await client.call("UpdateAnycastIpList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update anycast ip list") from exc
    return UpdateAnycastIpListResult(
        anycast_ip_list=resp.get("AnycastIpList"),
        e_tag=resp.get("ETag"),
    )


async def update_cache_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CachePolicyConfig"] = cache_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateCachePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cache policy") from exc
    return UpdateCachePolicyResult(
        cache_policy=resp.get("CachePolicy"),
        e_tag=resp.get("ETag"),
    )


async def update_cloud_front_origin_access_identity(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CloudFrontOriginAccessIdentityConfig"] = cloud_front_origin_access_identity_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateCloudFrontOriginAccessIdentity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cloud front origin access identity") from exc
    return UpdateCloudFrontOriginAccessIdentityResult(
        cloud_front_origin_access_identity=resp.get("CloudFrontOriginAccessIdentity"),
        e_tag=resp.get("ETag"),
    )


async def update_connection_group(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("UpdateConnectionGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update connection group") from exc
    return UpdateConnectionGroupResult(
        connection_group=resp.get("ConnectionGroup"),
        e_tag=resp.get("ETag"),
    )


async def update_continuous_deployment_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContinuousDeploymentPolicyConfig"] = continuous_deployment_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateContinuousDeploymentPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update continuous deployment policy") from exc
    return UpdateContinuousDeploymentPolicyResult(
        continuous_deployment_policy=resp.get("ContinuousDeploymentPolicy"),
        e_tag=resp.get("ETag"),
    )


async def update_distribution_tenant(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("UpdateDistributionTenant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update distribution tenant") from exc
    return UpdateDistributionTenantResult(
        distribution_tenant=resp.get("DistributionTenant"),
        e_tag=resp.get("ETag"),
    )


async def update_distribution_with_staging_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if staging_distribution_id is not None:
        kwargs["StagingDistributionId"] = staging_distribution_id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateDistributionWithStagingConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update distribution with staging config") from exc
    return UpdateDistributionWithStagingConfigResult(
        distribution=resp.get("Distribution"),
        e_tag=resp.get("ETag"),
    )


async def update_domain_association(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["TargetResource"] = target_resource
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateDomainAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update domain association") from exc
    return UpdateDomainAssociationResult(
        domain=resp.get("Domain"),
        resource_id=resp.get("ResourceId"),
        e_tag=resp.get("ETag"),
    )


async def update_field_level_encryption_config(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionConfig"] = field_level_encryption_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateFieldLevelEncryptionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update field level encryption config") from exc
    return UpdateFieldLevelEncryptionConfigResult(
        field_level_encryption=resp.get("FieldLevelEncryption"),
        e_tag=resp.get("ETag"),
    )


async def update_field_level_encryption_profile(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FieldLevelEncryptionProfileConfig"] = field_level_encryption_profile_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateFieldLevelEncryptionProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update field level encryption profile") from exc
    return UpdateFieldLevelEncryptionProfileResult(
        field_level_encryption_profile=resp.get("FieldLevelEncryptionProfile"),
        e_tag=resp.get("ETag"),
    )


async def update_function(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["IfMatch"] = if_match
    kwargs["FunctionConfig"] = function_config
    kwargs["FunctionCode"] = function_code
    try:
        resp = await client.call("UpdateFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update function") from exc
    return UpdateFunctionResult(
        function_summary=resp.get("FunctionSummary"),
        e_tag=resp.get("ETag"),
    )


async def update_key_group(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KeyGroupConfig"] = key_group_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateKeyGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update key group") from exc
    return UpdateKeyGroupResult(
        key_group=resp.get("KeyGroup"),
        e_tag=resp.get("ETag"),
    )


async def update_key_value_store(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Comment"] = comment
    kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateKeyValueStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update key value store") from exc
    return UpdateKeyValueStoreResult(
        key_value_store=resp.get("KeyValueStore"),
        e_tag=resp.get("ETag"),
    )


async def update_origin_access_control(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginAccessControlConfig"] = origin_access_control_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateOriginAccessControl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update origin access control") from exc
    return UpdateOriginAccessControlResult(
        origin_access_control=resp.get("OriginAccessControl"),
        e_tag=resp.get("ETag"),
    )


async def update_origin_request_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OriginRequestPolicyConfig"] = origin_request_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateOriginRequestPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update origin request policy") from exc
    return UpdateOriginRequestPolicyResult(
        origin_request_policy=resp.get("OriginRequestPolicy"),
        e_tag=resp.get("ETag"),
    )


async def update_public_key(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PublicKeyConfig"] = public_key_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdatePublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update public key") from exc
    return UpdatePublicKeyResult(
        public_key=resp.get("PublicKey"),
        e_tag=resp.get("ETag"),
    )


async def update_realtime_log_config(
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
    client = async_client("cloudfront", region_name)
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
        resp = await client.call("UpdateRealtimeLogConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update realtime log config") from exc
    return UpdateRealtimeLogConfigResult(
        realtime_log_config=resp.get("RealtimeLogConfig"),
    )


async def update_response_headers_policy(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResponseHeadersPolicyConfig"] = response_headers_policy_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateResponseHeadersPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update response headers policy") from exc
    return UpdateResponseHeadersPolicyResult(
        response_headers_policy=resp.get("ResponseHeadersPolicy"),
        e_tag=resp.get("ETag"),
    )


async def update_streaming_distribution(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamingDistributionConfig"] = streaming_distribution_config
    kwargs["Id"] = id
    if if_match is not None:
        kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateStreamingDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update streaming distribution") from exc
    return UpdateStreamingDistributionResult(
        streaming_distribution=resp.get("StreamingDistribution"),
        e_tag=resp.get("ETag"),
    )


async def update_vpc_origin(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcOriginEndpointConfig"] = vpc_origin_endpoint_config
    kwargs["Id"] = id
    kwargs["IfMatch"] = if_match
    try:
        resp = await client.call("UpdateVpcOrigin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update vpc origin") from exc
    return UpdateVpcOriginResult(
        vpc_origin=resp.get("VpcOrigin"),
        e_tag=resp.get("ETag"),
    )


async def verify_dns_configuration(
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
    client = async_client("cloudfront", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    if domain is not None:
        kwargs["Domain"] = domain
    try:
        resp = await client.call("VerifyDnsConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to verify dns configuration") from exc
    return VerifyDnsConfigurationResult(
        dns_configuration_list=resp.get("DnsConfigurationList"),
    )
