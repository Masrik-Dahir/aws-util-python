from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ActivateKeySigningKeyResult",
    "AssociateVpcWithHostedZoneResult",
    "ChangeCidrCollectionResult",
    "ChangeResourceRecordSetsResult",
    "CreateCidrCollectionResult",
    "CreateHealthCheckResult",
    "CreateHostedZoneResult",
    "CreateKeySigningKeyResult",
    "CreateQueryLoggingConfigResult",
    "CreateReusableDelegationSetResult",
    "CreateTrafficPolicyInstanceResult",
    "CreateTrafficPolicyResult",
    "CreateTrafficPolicyVersionResult",
    "CreateVpcAssociationAuthorizationResult",
    "DeactivateKeySigningKeyResult",
    "DeleteHostedZoneResult",
    "DeleteKeySigningKeyResult",
    "DisableHostedZoneDnssecResult",
    "DisassociateVpcFromHostedZoneResult",
    "EnableHostedZoneDnssecResult",
    "GetAccountLimitResult",
    "GetChangeResult",
    "GetCheckerIpRangesResult",
    "GetDnssecResult",
    "GetGeoLocationResult",
    "GetHealthCheckCountResult",
    "GetHealthCheckLastFailureReasonResult",
    "GetHealthCheckResult",
    "GetHealthCheckStatusResult",
    "GetHostedZoneCountResult",
    "GetHostedZoneLimitResult",
    "GetQueryLoggingConfigResult",
    "GetReusableDelegationSetLimitResult",
    "GetReusableDelegationSetResult",
    "GetTrafficPolicyInstanceCountResult",
    "GetTrafficPolicyInstanceResult",
    "GetTrafficPolicyResult",
    "HostedZone",
    "ListCidrBlocksResult",
    "ListCidrCollectionsResult",
    "ListCidrLocationsResult",
    "ListGeoLocationsResult",
    "ListHealthChecksResult",
    "ListHostedZonesByNameResult",
    "ListHostedZonesByVpcResult",
    "ListQueryLoggingConfigsResult",
    "ListResourceRecordSetsResult",
    "ListReusableDelegationSetsResult",
    "ListTagsForResourceResult",
    "ListTagsForResourcesResult",
    "ListTrafficPoliciesResult",
    "ListTrafficPolicyInstancesByHostedZoneResult",
    "ListTrafficPolicyInstancesByPolicyResult",
    "ListTrafficPolicyInstancesResult",
    "ListTrafficPolicyVersionsResult",
    "ListVpcAssociationAuthorizationsResult",
    "ResourceRecord",
    "RunDnsAnswerResult",
    "UpdateHealthCheckResult",
    "UpdateHostedZoneCommentResult",
    "UpdateTrafficPolicyCommentResult",
    "UpdateTrafficPolicyInstanceResult",
    "activate_key_signing_key",
    "associate_vpc_with_hosted_zone",
    "bulk_upsert_records",
    "change_cidr_collection",
    "change_resource_record_sets",
    "change_tags_for_resource",
    "create_cidr_collection",
    "create_health_check",
    "create_hosted_zone",
    "create_key_signing_key",
    "create_query_logging_config",
    "create_reusable_delegation_set",
    "create_traffic_policy",
    "create_traffic_policy_instance",
    "create_traffic_policy_version",
    "create_vpc_association_authorization",
    "deactivate_key_signing_key",
    "delete_cidr_collection",
    "delete_health_check",
    "delete_hosted_zone",
    "delete_key_signing_key",
    "delete_query_logging_config",
    "delete_record",
    "delete_reusable_delegation_set",
    "delete_traffic_policy",
    "delete_traffic_policy_instance",
    "delete_vpc_association_authorization",
    "disable_hosted_zone_dnssec",
    "disassociate_vpc_from_hosted_zone",
    "enable_hosted_zone_dnssec",
    "get_account_limit",
    "get_change",
    "get_checker_ip_ranges",
    "get_dnssec",
    "get_geo_location",
    "get_health_check",
    "get_health_check_count",
    "get_health_check_last_failure_reason",
    "get_health_check_status",
    "get_hosted_zone",
    "get_hosted_zone_count",
    "get_hosted_zone_limit",
    "get_query_logging_config",
    "get_reusable_delegation_set",
    "get_reusable_delegation_set_limit",
    "get_traffic_policy",
    "get_traffic_policy_instance",
    "get_traffic_policy_instance_count",
    "list_cidr_blocks",
    "list_cidr_collections",
    "list_cidr_locations",
    "list_geo_locations",
    "list_health_checks",
    "list_hosted_zones",
    "list_hosted_zones_by_name",
    "list_hosted_zones_by_vpc",
    "list_query_logging_configs",
    "list_records",
    "list_resource_record_sets",
    "list_reusable_delegation_sets",
    "list_tags_for_resource",
    "list_tags_for_resources",
    "list_traffic_policies",
    "list_traffic_policy_instances",
    "list_traffic_policy_instances_by_hosted_zone",
    "list_traffic_policy_instances_by_policy",
    "list_traffic_policy_versions",
    "list_vpc_association_authorizations",
    "run_dns_answer",
    "update_health_check",
    "update_hosted_zone_comment",
    "update_traffic_policy_comment",
    "update_traffic_policy_instance",
    "upsert_record",
    "wait_for_change",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class HostedZone(BaseModel):
    """A Route 53 hosted zone."""

    model_config = ConfigDict(frozen=True)

    zone_id: str
    name: str
    private_zone: bool = False
    record_count: int = 0
    comment: str | None = None


class ResourceRecord(BaseModel):
    """A single Route 53 resource record set."""

    model_config = ConfigDict(frozen=True)

    name: str
    record_type: str
    ttl: int | None = None
    values: list[str] = []
    alias_dns_name: str | None = None
    alias_hosted_zone_id: str | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def list_hosted_zones(
    region_name: str | None = None,
) -> list[HostedZone]:
    """List all Route 53 hosted zones in the account.

    Args:
        region_name: AWS region override (Route 53 is global but boto3 still
            accepts a region parameter).

    Returns:
        A list of :class:`HostedZone` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    zones: list[HostedZone] = []
    try:
        paginator = client.get_paginator("list_hosted_zones")
        for page in paginator.paginate():
            for zone in page.get("HostedZones", []):
                config = zone.get("Config", {})
                zones.append(
                    HostedZone(
                        zone_id=zone["Id"].split("/")[-1],
                        name=zone["Name"],
                        private_zone=config.get("PrivateZone", False),
                        record_count=zone.get("ResourceRecordSetCount", 0),
                        comment=config.get("Comment") or None,
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_hosted_zones failed") from exc
    return zones


def get_hosted_zone(
    zone_id: str,
    region_name: str | None = None,
) -> HostedZone | None:
    """Fetch a single Route 53 hosted zone by ID.

    Args:
        zone_id: The hosted zone ID (with or without the ``/hostedzone/``
            prefix).
        region_name: AWS region override.

    Returns:
        A :class:`HostedZone`, or ``None`` if not found.
    """
    client = get_client("route53", region_name)
    try:
        resp = client.get_hosted_zone(Id=zone_id)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "NoSuchHostedZone":
            return None
        raise wrap_aws_error(exc, f"get_hosted_zone failed for {zone_id!r}") from exc
    zone = resp["HostedZone"]
    config = zone.get("Config", {})
    return HostedZone(
        zone_id=zone["Id"].split("/")[-1],
        name=zone["Name"],
        private_zone=config.get("PrivateZone", False),
        record_count=zone.get("ResourceRecordSetCount", 0),
        comment=config.get("Comment") or None,
    )


def list_records(
    zone_id: str,
    region_name: str | None = None,
) -> list[ResourceRecord]:
    """List all resource record sets in a hosted zone.

    Args:
        zone_id: The hosted zone ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`ResourceRecord` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    records: list[ResourceRecord] = []
    try:
        paginator = client.get_paginator("list_resource_record_sets")
        for page in paginator.paginate(HostedZoneId=zone_id):
            for rrs in page.get("ResourceRecordSets", []):
                alias = rrs.get("AliasTarget", {})
                values = [r["Value"] for r in rrs.get("ResourceRecords", [])]
                records.append(
                    ResourceRecord(
                        name=rrs["Name"],
                        record_type=rrs["Type"],
                        ttl=rrs.get("TTL"),
                        values=values,
                        alias_dns_name=alias.get("DNSName") or None,
                        alias_hosted_zone_id=alias.get("HostedZoneId") or None,
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_records failed for zone {zone_id!r}") from exc
    return records


def upsert_record(
    zone_id: str,
    name: str,
    record_type: str,
    values: list[str],
    ttl: int = 300,
    region_name: str | None = None,
) -> str:
    """Create or update a DNS record in a Route 53 hosted zone.

    Uses an ``UPSERT`` change action — safe to call regardless of whether the
    record already exists.

    Args:
        zone_id: The hosted zone ID.
        name: DNS record name, e.g. ``"api.example.com."`` (trailing dot is
            added automatically if absent).
        record_type: Record type: ``"A"``, ``"CNAME"``, ``"TXT"``, etc.
        values: List of record values.
        ttl: Time-to-live in seconds (default ``300``).
        region_name: AWS region override.

    Returns:
        The Change ID of the submitted change batch.

    Raises:
        RuntimeError: If the change submission fails.
    """
    client = get_client("route53", region_name)
    if not name.endswith("."):
        name += "."
    change_batch: dict[str, Any] = {
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": record_type,
                    "TTL": ttl,
                    "ResourceRecords": [{"Value": v} for v in values],
                },
            }
        ]
    }
    try:
        resp = client.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to upsert record {name!r} in zone {zone_id!r}") from exc
    return resp["ChangeInfo"]["Id"]


def delete_record(
    zone_id: str,
    name: str,
    record_type: str,
    values: list[str],
    ttl: int = 300,
    region_name: str | None = None,
) -> str:
    """Delete a DNS record from a Route 53 hosted zone.

    Args:
        zone_id: The hosted zone ID.
        name: DNS record name.
        record_type: Record type.
        values: Exact record values (must match the existing record).
        ttl: TTL of the existing record.
        region_name: AWS region override.

    Returns:
        The Change ID of the submitted change batch.

    Raises:
        RuntimeError: If the deletion fails.
    """
    client = get_client("route53", region_name)
    if not name.endswith("."):
        name += "."
    change_batch: dict[str, Any] = {
        "Changes": [
            {
                "Action": "DELETE",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": record_type,
                    "TTL": ttl,
                    "ResourceRecords": [{"Value": v} for v in values],
                },
            }
        ]
    }
    try:
        resp = client.change_resource_record_sets(HostedZoneId=zone_id, ChangeBatch=change_batch)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to delete record {name!r} from zone {zone_id!r}"
        ) from exc
    return resp["ChangeInfo"]["Id"]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def wait_for_change(
    change_id: str,
    timeout: float = 300.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> str:
    """Poll until a Route 53 change batch reaches ``INSYNC`` status.

    DNS changes propagate asynchronously — use this after :func:`upsert_record`
    or :func:`delete_record` when you need confirmation before proceeding.

    Args:
        change_id: Change ID returned by ``upsert_record`` / ``delete_record``
            (with or without the ``/change/`` prefix).
        timeout: Maximum seconds to wait (default ``300``).
        poll_interval: Seconds between status checks (default ``15``).
        region_name: AWS region override.

    Returns:
        The final change status (``"INSYNC"``).

    Raises:
        TimeoutError: If the change does not sync within *timeout*.
        RuntimeError: If the API call fails.
    """
    import time as _time

    client = get_client("route53", region_name)
    # Normalise ID
    if not change_id.startswith("/change/"):
        change_id = f"/change/{change_id}"

    deadline = _time.monotonic() + timeout
    while True:
        try:
            resp = client.get_change(Id=change_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"wait_for_change failed for {change_id!r}") from exc

        status = resp["ChangeInfo"]["Status"]
        if status == "INSYNC":
            return status
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Route53 change {change_id!r} did not reach INSYNC "
                f"within {timeout}s (current: {status!r})"
            )
        _time.sleep(poll_interval)


def bulk_upsert_records(
    zone_id: str,
    records: list[dict[str, Any]],
    region_name: str | None = None,
) -> str:
    """Upsert multiple DNS records in a single Route 53 change batch.

    Each record dict must contain ``"name"``, ``"record_type"``, ``"values"``,
    and optionally ``"ttl"`` (default 300).

    Args:
        zone_id: The hosted zone ID.
        records: List of record dicts.
        region_name: AWS region override.

    Returns:
        The Change ID of the submitted batch.

    Raises:
        RuntimeError: If the change submission fails.
    """
    client = get_client("route53", region_name)
    changes = []
    for rec in records:
        name = rec["name"]
        if not name.endswith("."):
            name += "."
        changes.append(
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": rec["record_type"],
                    "TTL": rec.get("ttl", 300),
                    "ResourceRecords": [{"Value": v} for v in rec["values"]],
                },
            }
        )
    try:
        resp = client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={"Changes": changes},
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"bulk_upsert_records failed for zone {zone_id!r}") from exc
    return resp["ChangeInfo"]["Id"]


class ActivateKeySigningKeyResult(BaseModel):
    """Result of activate_key_signing_key."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class AssociateVpcWithHostedZoneResult(BaseModel):
    """Result of associate_vpc_with_hosted_zone."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class ChangeCidrCollectionResult(BaseModel):
    """Result of change_cidr_collection."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None


class ChangeResourceRecordSetsResult(BaseModel):
    """Result of change_resource_record_sets."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class CreateCidrCollectionResult(BaseModel):
    """Result of create_cidr_collection."""

    model_config = ConfigDict(frozen=True)

    collection: dict[str, Any] | None = None
    location: str | None = None


class CreateHealthCheckResult(BaseModel):
    """Result of create_health_check."""

    model_config = ConfigDict(frozen=True)

    health_check: dict[str, Any] | None = None
    location: str | None = None


class CreateHostedZoneResult(BaseModel):
    """Result of create_hosted_zone."""

    model_config = ConfigDict(frozen=True)

    hosted_zone: dict[str, Any] | None = None
    change_info: dict[str, Any] | None = None
    delegation_set: dict[str, Any] | None = None
    vpc: dict[str, Any] | None = None
    location: str | None = None


class CreateKeySigningKeyResult(BaseModel):
    """Result of create_key_signing_key."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None
    key_signing_key: dict[str, Any] | None = None
    location: str | None = None


class CreateQueryLoggingConfigResult(BaseModel):
    """Result of create_query_logging_config."""

    model_config = ConfigDict(frozen=True)

    query_logging_config: dict[str, Any] | None = None
    location: str | None = None


class CreateReusableDelegationSetResult(BaseModel):
    """Result of create_reusable_delegation_set."""

    model_config = ConfigDict(frozen=True)

    delegation_set: dict[str, Any] | None = None
    location: str | None = None


class CreateTrafficPolicyResult(BaseModel):
    """Result of create_traffic_policy."""

    model_config = ConfigDict(frozen=True)

    traffic_policy: dict[str, Any] | None = None
    location: str | None = None


class CreateTrafficPolicyInstanceResult(BaseModel):
    """Result of create_traffic_policy_instance."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instance: dict[str, Any] | None = None
    location: str | None = None


class CreateTrafficPolicyVersionResult(BaseModel):
    """Result of create_traffic_policy_version."""

    model_config = ConfigDict(frozen=True)

    traffic_policy: dict[str, Any] | None = None
    location: str | None = None


class CreateVpcAssociationAuthorizationResult(BaseModel):
    """Result of create_vpc_association_authorization."""

    model_config = ConfigDict(frozen=True)

    hosted_zone_id: str | None = None
    vpc: dict[str, Any] | None = None


class DeactivateKeySigningKeyResult(BaseModel):
    """Result of deactivate_key_signing_key."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class DeleteHostedZoneResult(BaseModel):
    """Result of delete_hosted_zone."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class DeleteKeySigningKeyResult(BaseModel):
    """Result of delete_key_signing_key."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class DisableHostedZoneDnssecResult(BaseModel):
    """Result of disable_hosted_zone_dnssec."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class DisassociateVpcFromHostedZoneResult(BaseModel):
    """Result of disassociate_vpc_from_hosted_zone."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class EnableHostedZoneDnssecResult(BaseModel):
    """Result of enable_hosted_zone_dnssec."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class GetAccountLimitResult(BaseModel):
    """Result of get_account_limit."""

    model_config = ConfigDict(frozen=True)

    limit: dict[str, Any] | None = None
    count: int | None = None


class GetChangeResult(BaseModel):
    """Result of get_change."""

    model_config = ConfigDict(frozen=True)

    change_info: dict[str, Any] | None = None


class GetCheckerIpRangesResult(BaseModel):
    """Result of get_checker_ip_ranges."""

    model_config = ConfigDict(frozen=True)

    checker_ip_ranges: list[str] | None = None


class GetDnssecResult(BaseModel):
    """Result of get_dnssec."""

    model_config = ConfigDict(frozen=True)

    status: dict[str, Any] | None = None
    key_signing_keys: list[dict[str, Any]] | None = None


class GetGeoLocationResult(BaseModel):
    """Result of get_geo_location."""

    model_config = ConfigDict(frozen=True)

    geo_location_details: dict[str, Any] | None = None


class GetHealthCheckResult(BaseModel):
    """Result of get_health_check."""

    model_config = ConfigDict(frozen=True)

    health_check: dict[str, Any] | None = None


class GetHealthCheckCountResult(BaseModel):
    """Result of get_health_check_count."""

    model_config = ConfigDict(frozen=True)

    health_check_count: int | None = None


class GetHealthCheckLastFailureReasonResult(BaseModel):
    """Result of get_health_check_last_failure_reason."""

    model_config = ConfigDict(frozen=True)

    health_check_observations: list[dict[str, Any]] | None = None


class GetHealthCheckStatusResult(BaseModel):
    """Result of get_health_check_status."""

    model_config = ConfigDict(frozen=True)

    health_check_observations: list[dict[str, Any]] | None = None


class GetHostedZoneCountResult(BaseModel):
    """Result of get_hosted_zone_count."""

    model_config = ConfigDict(frozen=True)

    hosted_zone_count: int | None = None


class GetHostedZoneLimitResult(BaseModel):
    """Result of get_hosted_zone_limit."""

    model_config = ConfigDict(frozen=True)

    limit: dict[str, Any] | None = None
    count: int | None = None


class GetQueryLoggingConfigResult(BaseModel):
    """Result of get_query_logging_config."""

    model_config = ConfigDict(frozen=True)

    query_logging_config: dict[str, Any] | None = None


class GetReusableDelegationSetResult(BaseModel):
    """Result of get_reusable_delegation_set."""

    model_config = ConfigDict(frozen=True)

    delegation_set: dict[str, Any] | None = None


class GetReusableDelegationSetLimitResult(BaseModel):
    """Result of get_reusable_delegation_set_limit."""

    model_config = ConfigDict(frozen=True)

    limit: dict[str, Any] | None = None
    count: int | None = None


class GetTrafficPolicyResult(BaseModel):
    """Result of get_traffic_policy."""

    model_config = ConfigDict(frozen=True)

    traffic_policy: dict[str, Any] | None = None


class GetTrafficPolicyInstanceResult(BaseModel):
    """Result of get_traffic_policy_instance."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instance: dict[str, Any] | None = None


class GetTrafficPolicyInstanceCountResult(BaseModel):
    """Result of get_traffic_policy_instance_count."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instance_count: int | None = None


class ListCidrBlocksResult(BaseModel):
    """Result of list_cidr_blocks."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    cidr_blocks: list[dict[str, Any]] | None = None


class ListCidrCollectionsResult(BaseModel):
    """Result of list_cidr_collections."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    cidr_collections: list[dict[str, Any]] | None = None


class ListCidrLocationsResult(BaseModel):
    """Result of list_cidr_locations."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    cidr_locations: list[dict[str, Any]] | None = None


class ListGeoLocationsResult(BaseModel):
    """Result of list_geo_locations."""

    model_config = ConfigDict(frozen=True)

    geo_location_details_list: list[dict[str, Any]] | None = None
    is_truncated: bool | None = None
    next_continent_code: str | None = None
    next_country_code: str | None = None
    next_subdivision_code: str | None = None
    max_items: str | None = None


class ListHealthChecksResult(BaseModel):
    """Result of list_health_checks."""

    model_config = ConfigDict(frozen=True)

    health_checks: list[dict[str, Any]] | None = None
    marker: str | None = None
    is_truncated: bool | None = None
    next_marker: str | None = None
    max_items: str | None = None


class ListHostedZonesByNameResult(BaseModel):
    """Result of list_hosted_zones_by_name."""

    model_config = ConfigDict(frozen=True)

    hosted_zones: list[dict[str, Any]] | None = None
    dns_name: str | None = None
    hosted_zone_id: str | None = None
    is_truncated: bool | None = None
    next_dns_name: str | None = None
    next_hosted_zone_id: str | None = None
    max_items: str | None = None


class ListHostedZonesByVpcResult(BaseModel):
    """Result of list_hosted_zones_by_vpc."""

    model_config = ConfigDict(frozen=True)

    hosted_zone_summaries: list[dict[str, Any]] | None = None
    max_items: str | None = None
    next_token: str | None = None


class ListQueryLoggingConfigsResult(BaseModel):
    """Result of list_query_logging_configs."""

    model_config = ConfigDict(frozen=True)

    query_logging_configs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceRecordSetsResult(BaseModel):
    """Result of list_resource_record_sets."""

    model_config = ConfigDict(frozen=True)

    resource_record_sets: list[dict[str, Any]] | None = None
    is_truncated: bool | None = None
    next_record_name: str | None = None
    next_record_type: str | None = None
    next_record_identifier: str | None = None
    max_items: str | None = None


class ListReusableDelegationSetsResult(BaseModel):
    """Result of list_reusable_delegation_sets."""

    model_config = ConfigDict(frozen=True)

    delegation_sets: list[dict[str, Any]] | None = None
    marker: str | None = None
    is_truncated: bool | None = None
    next_marker: str | None = None
    max_items: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_tag_set: dict[str, Any] | None = None


class ListTagsForResourcesResult(BaseModel):
    """Result of list_tags_for_resources."""

    model_config = ConfigDict(frozen=True)

    resource_tag_sets: list[dict[str, Any]] | None = None


class ListTrafficPoliciesResult(BaseModel):
    """Result of list_traffic_policies."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_summaries: list[dict[str, Any]] | None = None
    is_truncated: bool | None = None
    traffic_policy_id_marker: str | None = None
    max_items: str | None = None


class ListTrafficPolicyInstancesResult(BaseModel):
    """Result of list_traffic_policy_instances."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instances: list[dict[str, Any]] | None = None
    hosted_zone_id_marker: str | None = None
    traffic_policy_instance_name_marker: str | None = None
    traffic_policy_instance_type_marker: str | None = None
    is_truncated: bool | None = None
    max_items: str | None = None


class ListTrafficPolicyInstancesByHostedZoneResult(BaseModel):
    """Result of list_traffic_policy_instances_by_hosted_zone."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instances: list[dict[str, Any]] | None = None
    traffic_policy_instance_name_marker: str | None = None
    traffic_policy_instance_type_marker: str | None = None
    is_truncated: bool | None = None
    max_items: str | None = None


class ListTrafficPolicyInstancesByPolicyResult(BaseModel):
    """Result of list_traffic_policy_instances_by_policy."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instances: list[dict[str, Any]] | None = None
    hosted_zone_id_marker: str | None = None
    traffic_policy_instance_name_marker: str | None = None
    traffic_policy_instance_type_marker: str | None = None
    is_truncated: bool | None = None
    max_items: str | None = None


class ListTrafficPolicyVersionsResult(BaseModel):
    """Result of list_traffic_policy_versions."""

    model_config = ConfigDict(frozen=True)

    traffic_policies: list[dict[str, Any]] | None = None
    is_truncated: bool | None = None
    traffic_policy_version_marker: str | None = None
    max_items: str | None = None


class ListVpcAssociationAuthorizationsResult(BaseModel):
    """Result of list_vpc_association_authorizations."""

    model_config = ConfigDict(frozen=True)

    hosted_zone_id: str | None = None
    next_token: str | None = None
    vp_cs: list[dict[str, Any]] | None = None


class RunDnsAnswerResult(BaseModel):
    """Result of run_dns_answer."""

    model_config = ConfigDict(frozen=True)

    nameserver: str | None = None
    record_name: str | None = None
    record_type: str | None = None
    record_data: list[str] | None = None
    response_code: str | None = None
    protocol: str | None = None


class UpdateHealthCheckResult(BaseModel):
    """Result of update_health_check."""

    model_config = ConfigDict(frozen=True)

    health_check: dict[str, Any] | None = None


class UpdateHostedZoneCommentResult(BaseModel):
    """Result of update_hosted_zone_comment."""

    model_config = ConfigDict(frozen=True)

    hosted_zone: dict[str, Any] | None = None


class UpdateTrafficPolicyCommentResult(BaseModel):
    """Result of update_traffic_policy_comment."""

    model_config = ConfigDict(frozen=True)

    traffic_policy: dict[str, Any] | None = None


class UpdateTrafficPolicyInstanceResult(BaseModel):
    """Result of update_traffic_policy_instance."""

    model_config = ConfigDict(frozen=True)

    traffic_policy_instance: dict[str, Any] | None = None


def activate_key_signing_key(
    hosted_zone_id: str,
    name: str,
    region_name: str | None = None,
) -> ActivateKeySigningKeyResult:
    """Activate key signing key.

    Args:
        hosted_zone_id: Hosted zone id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["Name"] = name
    try:
        resp = client.activate_key_signing_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to activate key signing key") from exc
    return ActivateKeySigningKeyResult(
        change_info=resp.get("ChangeInfo"),
    )


def associate_vpc_with_hosted_zone(
    hosted_zone_id: str,
    vpc: dict[str, Any],
    *,
    comment: str | None = None,
    region_name: str | None = None,
) -> AssociateVpcWithHostedZoneResult:
    """Associate vpc with hosted zone.

    Args:
        hosted_zone_id: Hosted zone id.
        vpc: Vpc.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["VPC"] = vpc
    if comment is not None:
        kwargs["Comment"] = comment
    try:
        resp = client.associate_vpc_with_hosted_zone(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate vpc with hosted zone") from exc
    return AssociateVpcWithHostedZoneResult(
        change_info=resp.get("ChangeInfo"),
    )


def change_cidr_collection(
    id: str,
    changes: list[dict[str, Any]],
    *,
    collection_version: int | None = None,
    region_name: str | None = None,
) -> ChangeCidrCollectionResult:
    """Change cidr collection.

    Args:
        id: Id.
        changes: Changes.
        collection_version: Collection version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Changes"] = changes
    if collection_version is not None:
        kwargs["CollectionVersion"] = collection_version
    try:
        resp = client.change_cidr_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change cidr collection") from exc
    return ChangeCidrCollectionResult(
        id=resp.get("Id"),
    )


def change_resource_record_sets(
    hosted_zone_id: str,
    change_batch: dict[str, Any],
    region_name: str | None = None,
) -> ChangeResourceRecordSetsResult:
    """Change resource record sets.

    Args:
        hosted_zone_id: Hosted zone id.
        change_batch: Change batch.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["ChangeBatch"] = change_batch
    try:
        resp = client.change_resource_record_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change resource record sets") from exc
    return ChangeResourceRecordSetsResult(
        change_info=resp.get("ChangeInfo"),
    )


def change_tags_for_resource(
    resource_type: str,
    resource_id: str,
    *,
    add_tags: list[dict[str, Any]] | None = None,
    remove_tag_keys: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Change tags for resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        add_tags: Add tags.
        remove_tag_keys: Remove tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    if add_tags is not None:
        kwargs["AddTags"] = add_tags
    if remove_tag_keys is not None:
        kwargs["RemoveTagKeys"] = remove_tag_keys
    try:
        client.change_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change tags for resource") from exc
    return None


def create_cidr_collection(
    name: str,
    caller_reference: str,
    region_name: str | None = None,
) -> CreateCidrCollectionResult:
    """Create cidr collection.

    Args:
        name: Name.
        caller_reference: Caller reference.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["CallerReference"] = caller_reference
    try:
        resp = client.create_cidr_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cidr collection") from exc
    return CreateCidrCollectionResult(
        collection=resp.get("Collection"),
        location=resp.get("Location"),
    )


def create_health_check(
    caller_reference: str,
    health_check_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateHealthCheckResult:
    """Create health check.

    Args:
        caller_reference: Caller reference.
        health_check_config: Health check config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallerReference"] = caller_reference
    kwargs["HealthCheckConfig"] = health_check_config
    try:
        resp = client.create_health_check(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create health check") from exc
    return CreateHealthCheckResult(
        health_check=resp.get("HealthCheck"),
        location=resp.get("Location"),
    )


def create_hosted_zone(
    name: str,
    caller_reference: str,
    *,
    vpc: dict[str, Any] | None = None,
    hosted_zone_config: dict[str, Any] | None = None,
    delegation_set_id: str | None = None,
    region_name: str | None = None,
) -> CreateHostedZoneResult:
    """Create hosted zone.

    Args:
        name: Name.
        caller_reference: Caller reference.
        vpc: Vpc.
        hosted_zone_config: Hosted zone config.
        delegation_set_id: Delegation set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["CallerReference"] = caller_reference
    if vpc is not None:
        kwargs["VPC"] = vpc
    if hosted_zone_config is not None:
        kwargs["HostedZoneConfig"] = hosted_zone_config
    if delegation_set_id is not None:
        kwargs["DelegationSetId"] = delegation_set_id
    try:
        resp = client.create_hosted_zone(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create hosted zone") from exc
    return CreateHostedZoneResult(
        hosted_zone=resp.get("HostedZone"),
        change_info=resp.get("ChangeInfo"),
        delegation_set=resp.get("DelegationSet"),
        vpc=resp.get("VPC"),
        location=resp.get("Location"),
    )


def create_key_signing_key(
    caller_reference: str,
    hosted_zone_id: str,
    key_management_service_arn: str,
    name: str,
    status: str,
    region_name: str | None = None,
) -> CreateKeySigningKeyResult:
    """Create key signing key.

    Args:
        caller_reference: Caller reference.
        hosted_zone_id: Hosted zone id.
        key_management_service_arn: Key management service arn.
        name: Name.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallerReference"] = caller_reference
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["KeyManagementServiceArn"] = key_management_service_arn
    kwargs["Name"] = name
    kwargs["Status"] = status
    try:
        resp = client.create_key_signing_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create key signing key") from exc
    return CreateKeySigningKeyResult(
        change_info=resp.get("ChangeInfo"),
        key_signing_key=resp.get("KeySigningKey"),
        location=resp.get("Location"),
    )


def create_query_logging_config(
    hosted_zone_id: str,
    cloud_watch_logs_log_group_arn: str,
    region_name: str | None = None,
) -> CreateQueryLoggingConfigResult:
    """Create query logging config.

    Args:
        hosted_zone_id: Hosted zone id.
        cloud_watch_logs_log_group_arn: Cloud watch logs log group arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["CloudWatchLogsLogGroupArn"] = cloud_watch_logs_log_group_arn
    try:
        resp = client.create_query_logging_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create query logging config") from exc
    return CreateQueryLoggingConfigResult(
        query_logging_config=resp.get("QueryLoggingConfig"),
        location=resp.get("Location"),
    )


def create_reusable_delegation_set(
    caller_reference: str,
    *,
    hosted_zone_id: str | None = None,
    region_name: str | None = None,
) -> CreateReusableDelegationSetResult:
    """Create reusable delegation set.

    Args:
        caller_reference: Caller reference.
        hosted_zone_id: Hosted zone id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CallerReference"] = caller_reference
    if hosted_zone_id is not None:
        kwargs["HostedZoneId"] = hosted_zone_id
    try:
        resp = client.create_reusable_delegation_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create reusable delegation set") from exc
    return CreateReusableDelegationSetResult(
        delegation_set=resp.get("DelegationSet"),
        location=resp.get("Location"),
    )


def create_traffic_policy(
    name: str,
    document: str,
    *,
    comment: str | None = None,
    region_name: str | None = None,
) -> CreateTrafficPolicyResult:
    """Create traffic policy.

    Args:
        name: Name.
        document: Document.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Document"] = document
    if comment is not None:
        kwargs["Comment"] = comment
    try:
        resp = client.create_traffic_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create traffic policy") from exc
    return CreateTrafficPolicyResult(
        traffic_policy=resp.get("TrafficPolicy"),
        location=resp.get("Location"),
    )


def create_traffic_policy_instance(
    hosted_zone_id: str,
    name: str,
    ttl: int,
    traffic_policy_id: str,
    traffic_policy_version: int,
    region_name: str | None = None,
) -> CreateTrafficPolicyInstanceResult:
    """Create traffic policy instance.

    Args:
        hosted_zone_id: Hosted zone id.
        name: Name.
        ttl: Ttl.
        traffic_policy_id: Traffic policy id.
        traffic_policy_version: Traffic policy version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["Name"] = name
    kwargs["TTL"] = ttl
    kwargs["TrafficPolicyId"] = traffic_policy_id
    kwargs["TrafficPolicyVersion"] = traffic_policy_version
    try:
        resp = client.create_traffic_policy_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create traffic policy instance") from exc
    return CreateTrafficPolicyInstanceResult(
        traffic_policy_instance=resp.get("TrafficPolicyInstance"),
        location=resp.get("Location"),
    )


def create_traffic_policy_version(
    id: str,
    document: str,
    *,
    comment: str | None = None,
    region_name: str | None = None,
) -> CreateTrafficPolicyVersionResult:
    """Create traffic policy version.

    Args:
        id: Id.
        document: Document.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Document"] = document
    if comment is not None:
        kwargs["Comment"] = comment
    try:
        resp = client.create_traffic_policy_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create traffic policy version") from exc
    return CreateTrafficPolicyVersionResult(
        traffic_policy=resp.get("TrafficPolicy"),
        location=resp.get("Location"),
    )


def create_vpc_association_authorization(
    hosted_zone_id: str,
    vpc: dict[str, Any],
    region_name: str | None = None,
) -> CreateVpcAssociationAuthorizationResult:
    """Create vpc association authorization.

    Args:
        hosted_zone_id: Hosted zone id.
        vpc: Vpc.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["VPC"] = vpc
    try:
        resp = client.create_vpc_association_authorization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vpc association authorization") from exc
    return CreateVpcAssociationAuthorizationResult(
        hosted_zone_id=resp.get("HostedZoneId"),
        vpc=resp.get("VPC"),
    )


def deactivate_key_signing_key(
    hosted_zone_id: str,
    name: str,
    region_name: str | None = None,
) -> DeactivateKeySigningKeyResult:
    """Deactivate key signing key.

    Args:
        hosted_zone_id: Hosted zone id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["Name"] = name
    try:
        resp = client.deactivate_key_signing_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deactivate key signing key") from exc
    return DeactivateKeySigningKeyResult(
        change_info=resp.get("ChangeInfo"),
    )


def delete_cidr_collection(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete cidr collection.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        client.delete_cidr_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cidr collection") from exc
    return None


def delete_health_check(
    health_check_id: str,
    region_name: str | None = None,
) -> None:
    """Delete health check.

    Args:
        health_check_id: Health check id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HealthCheckId"] = health_check_id
    try:
        client.delete_health_check(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete health check") from exc
    return None


def delete_hosted_zone(
    id: str,
    region_name: str | None = None,
) -> DeleteHostedZoneResult:
    """Delete hosted zone.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.delete_hosted_zone(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete hosted zone") from exc
    return DeleteHostedZoneResult(
        change_info=resp.get("ChangeInfo"),
    )


def delete_key_signing_key(
    hosted_zone_id: str,
    name: str,
    region_name: str | None = None,
) -> DeleteKeySigningKeyResult:
    """Delete key signing key.

    Args:
        hosted_zone_id: Hosted zone id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["Name"] = name
    try:
        resp = client.delete_key_signing_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete key signing key") from exc
    return DeleteKeySigningKeyResult(
        change_info=resp.get("ChangeInfo"),
    )


def delete_query_logging_config(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete query logging config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        client.delete_query_logging_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete query logging config") from exc
    return None


def delete_reusable_delegation_set(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete reusable delegation set.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        client.delete_reusable_delegation_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete reusable delegation set") from exc
    return None


def delete_traffic_policy(
    id: str,
    version: int,
    region_name: str | None = None,
) -> None:
    """Delete traffic policy.

    Args:
        id: Id.
        version: Version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Version"] = version
    try:
        client.delete_traffic_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete traffic policy") from exc
    return None


def delete_traffic_policy_instance(
    id: str,
    region_name: str | None = None,
) -> None:
    """Delete traffic policy instance.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        client.delete_traffic_policy_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete traffic policy instance") from exc
    return None


def delete_vpc_association_authorization(
    hosted_zone_id: str,
    vpc: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Delete vpc association authorization.

    Args:
        hosted_zone_id: Hosted zone id.
        vpc: Vpc.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["VPC"] = vpc
    try:
        client.delete_vpc_association_authorization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc association authorization") from exc
    return None


def disable_hosted_zone_dnssec(
    hosted_zone_id: str,
    region_name: str | None = None,
) -> DisableHostedZoneDnssecResult:
    """Disable hosted zone dnssec.

    Args:
        hosted_zone_id: Hosted zone id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    try:
        resp = client.disable_hosted_zone_dnssec(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable hosted zone dnssec") from exc
    return DisableHostedZoneDnssecResult(
        change_info=resp.get("ChangeInfo"),
    )


def disassociate_vpc_from_hosted_zone(
    hosted_zone_id: str,
    vpc: dict[str, Any],
    *,
    comment: str | None = None,
    region_name: str | None = None,
) -> DisassociateVpcFromHostedZoneResult:
    """Disassociate vpc from hosted zone.

    Args:
        hosted_zone_id: Hosted zone id.
        vpc: Vpc.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["VPC"] = vpc
    if comment is not None:
        kwargs["Comment"] = comment
    try:
        resp = client.disassociate_vpc_from_hosted_zone(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate vpc from hosted zone") from exc
    return DisassociateVpcFromHostedZoneResult(
        change_info=resp.get("ChangeInfo"),
    )


def enable_hosted_zone_dnssec(
    hosted_zone_id: str,
    region_name: str | None = None,
) -> EnableHostedZoneDnssecResult:
    """Enable hosted zone dnssec.

    Args:
        hosted_zone_id: Hosted zone id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    try:
        resp = client.enable_hosted_zone_dnssec(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable hosted zone dnssec") from exc
    return EnableHostedZoneDnssecResult(
        change_info=resp.get("ChangeInfo"),
    )


def get_account_limit(
    type_value: str,
    region_name: str | None = None,
) -> GetAccountLimitResult:
    """Get account limit.

    Args:
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Type"] = type_value
    try:
        resp = client.get_account_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get account limit") from exc
    return GetAccountLimitResult(
        limit=resp.get("Limit"),
        count=resp.get("Count"),
    )


def get_change(
    id: str,
    region_name: str | None = None,
) -> GetChangeResult:
    """Get change.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_change(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get change") from exc
    return GetChangeResult(
        change_info=resp.get("ChangeInfo"),
    )


def get_checker_ip_ranges(
    region_name: str | None = None,
) -> GetCheckerIpRangesResult:
    """Get checker ip ranges.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_checker_ip_ranges(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get checker ip ranges") from exc
    return GetCheckerIpRangesResult(
        checker_ip_ranges=resp.get("CheckerIpRanges"),
    )


def get_dnssec(
    hosted_zone_id: str,
    region_name: str | None = None,
) -> GetDnssecResult:
    """Get dnssec.

    Args:
        hosted_zone_id: Hosted zone id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    try:
        resp = client.get_dnssec(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get dnssec") from exc
    return GetDnssecResult(
        status=resp.get("Status"),
        key_signing_keys=resp.get("KeySigningKeys"),
    )


def get_geo_location(
    *,
    continent_code: str | None = None,
    country_code: str | None = None,
    subdivision_code: str | None = None,
    region_name: str | None = None,
) -> GetGeoLocationResult:
    """Get geo location.

    Args:
        continent_code: Continent code.
        country_code: Country code.
        subdivision_code: Subdivision code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if continent_code is not None:
        kwargs["ContinentCode"] = continent_code
    if country_code is not None:
        kwargs["CountryCode"] = country_code
    if subdivision_code is not None:
        kwargs["SubdivisionCode"] = subdivision_code
    try:
        resp = client.get_geo_location(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get geo location") from exc
    return GetGeoLocationResult(
        geo_location_details=resp.get("GeoLocationDetails"),
    )


def get_health_check(
    health_check_id: str,
    region_name: str | None = None,
) -> GetHealthCheckResult:
    """Get health check.

    Args:
        health_check_id: Health check id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HealthCheckId"] = health_check_id
    try:
        resp = client.get_health_check(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get health check") from exc
    return GetHealthCheckResult(
        health_check=resp.get("HealthCheck"),
    )


def get_health_check_count(
    region_name: str | None = None,
) -> GetHealthCheckCountResult:
    """Get health check count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_health_check_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get health check count") from exc
    return GetHealthCheckCountResult(
        health_check_count=resp.get("HealthCheckCount"),
    )


def get_health_check_last_failure_reason(
    health_check_id: str,
    region_name: str | None = None,
) -> GetHealthCheckLastFailureReasonResult:
    """Get health check last failure reason.

    Args:
        health_check_id: Health check id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HealthCheckId"] = health_check_id
    try:
        resp = client.get_health_check_last_failure_reason(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get health check last failure reason") from exc
    return GetHealthCheckLastFailureReasonResult(
        health_check_observations=resp.get("HealthCheckObservations"),
    )


def get_health_check_status(
    health_check_id: str,
    region_name: str | None = None,
) -> GetHealthCheckStatusResult:
    """Get health check status.

    Args:
        health_check_id: Health check id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HealthCheckId"] = health_check_id
    try:
        resp = client.get_health_check_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get health check status") from exc
    return GetHealthCheckStatusResult(
        health_check_observations=resp.get("HealthCheckObservations"),
    )


def get_hosted_zone_count(
    region_name: str | None = None,
) -> GetHostedZoneCountResult:
    """Get hosted zone count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_hosted_zone_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get hosted zone count") from exc
    return GetHostedZoneCountResult(
        hosted_zone_count=resp.get("HostedZoneCount"),
    )


def get_hosted_zone_limit(
    type_value: str,
    hosted_zone_id: str,
    region_name: str | None = None,
) -> GetHostedZoneLimitResult:
    """Get hosted zone limit.

    Args:
        type_value: Type value.
        hosted_zone_id: Hosted zone id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Type"] = type_value
    kwargs["HostedZoneId"] = hosted_zone_id
    try:
        resp = client.get_hosted_zone_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get hosted zone limit") from exc
    return GetHostedZoneLimitResult(
        limit=resp.get("Limit"),
        count=resp.get("Count"),
    )


def get_query_logging_config(
    id: str,
    region_name: str | None = None,
) -> GetQueryLoggingConfigResult:
    """Get query logging config.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_query_logging_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get query logging config") from exc
    return GetQueryLoggingConfigResult(
        query_logging_config=resp.get("QueryLoggingConfig"),
    )


def get_reusable_delegation_set(
    id: str,
    region_name: str | None = None,
) -> GetReusableDelegationSetResult:
    """Get reusable delegation set.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_reusable_delegation_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get reusable delegation set") from exc
    return GetReusableDelegationSetResult(
        delegation_set=resp.get("DelegationSet"),
    )


def get_reusable_delegation_set_limit(
    type_value: str,
    delegation_set_id: str,
    region_name: str | None = None,
) -> GetReusableDelegationSetLimitResult:
    """Get reusable delegation set limit.

    Args:
        type_value: Type value.
        delegation_set_id: Delegation set id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Type"] = type_value
    kwargs["DelegationSetId"] = delegation_set_id
    try:
        resp = client.get_reusable_delegation_set_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get reusable delegation set limit") from exc
    return GetReusableDelegationSetLimitResult(
        limit=resp.get("Limit"),
        count=resp.get("Count"),
    )


def get_traffic_policy(
    id: str,
    version: int,
    region_name: str | None = None,
) -> GetTrafficPolicyResult:
    """Get traffic policy.

    Args:
        id: Id.
        version: Version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Version"] = version
    try:
        resp = client.get_traffic_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get traffic policy") from exc
    return GetTrafficPolicyResult(
        traffic_policy=resp.get("TrafficPolicy"),
    )


def get_traffic_policy_instance(
    id: str,
    region_name: str | None = None,
) -> GetTrafficPolicyInstanceResult:
    """Get traffic policy instance.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_traffic_policy_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get traffic policy instance") from exc
    return GetTrafficPolicyInstanceResult(
        traffic_policy_instance=resp.get("TrafficPolicyInstance"),
    )


def get_traffic_policy_instance_count(
    region_name: str | None = None,
) -> GetTrafficPolicyInstanceCountResult:
    """Get traffic policy instance count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_traffic_policy_instance_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get traffic policy instance count") from exc
    return GetTrafficPolicyInstanceCountResult(
        traffic_policy_instance_count=resp.get("TrafficPolicyInstanceCount"),
    )


def list_cidr_blocks(
    collection_id: str,
    *,
    location_name: str | None = None,
    next_token: str | None = None,
    max_results: str | None = None,
    region_name: str | None = None,
) -> ListCidrBlocksResult:
    """List cidr blocks.

    Args:
        collection_id: Collection id.
        location_name: Location name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    if location_name is not None:
        kwargs["LocationName"] = location_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_cidr_blocks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cidr blocks") from exc
    return ListCidrBlocksResult(
        next_token=resp.get("NextToken"),
        cidr_blocks=resp.get("CidrBlocks"),
    )


def list_cidr_collections(
    *,
    next_token: str | None = None,
    max_results: str | None = None,
    region_name: str | None = None,
) -> ListCidrCollectionsResult:
    """List cidr collections.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_cidr_collections(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cidr collections") from exc
    return ListCidrCollectionsResult(
        next_token=resp.get("NextToken"),
        cidr_collections=resp.get("CidrCollections"),
    )


def list_cidr_locations(
    collection_id: str,
    *,
    next_token: str | None = None,
    max_results: str | None = None,
    region_name: str | None = None,
) -> ListCidrLocationsResult:
    """List cidr locations.

    Args:
        collection_id: Collection id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectionId"] = collection_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_cidr_locations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cidr locations") from exc
    return ListCidrLocationsResult(
        next_token=resp.get("NextToken"),
        cidr_locations=resp.get("CidrLocations"),
    )


def list_geo_locations(
    *,
    start_continent_code: str | None = None,
    start_country_code: str | None = None,
    start_subdivision_code: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListGeoLocationsResult:
    """List geo locations.

    Args:
        start_continent_code: Start continent code.
        start_country_code: Start country code.
        start_subdivision_code: Start subdivision code.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if start_continent_code is not None:
        kwargs["StartContinentCode"] = start_continent_code
    if start_country_code is not None:
        kwargs["StartCountryCode"] = start_country_code
    if start_subdivision_code is not None:
        kwargs["StartSubdivisionCode"] = start_subdivision_code
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_geo_locations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list geo locations") from exc
    return ListGeoLocationsResult(
        geo_location_details_list=resp.get("GeoLocationDetailsList"),
        is_truncated=resp.get("IsTruncated"),
        next_continent_code=resp.get("NextContinentCode"),
        next_country_code=resp.get("NextCountryCode"),
        next_subdivision_code=resp.get("NextSubdivisionCode"),
        max_items=resp.get("MaxItems"),
    )


def list_health_checks(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListHealthChecksResult:
    """List health checks.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_health_checks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list health checks") from exc
    return ListHealthChecksResult(
        health_checks=resp.get("HealthChecks"),
        marker=resp.get("Marker"),
        is_truncated=resp.get("IsTruncated"),
        next_marker=resp.get("NextMarker"),
        max_items=resp.get("MaxItems"),
    )


def list_hosted_zones_by_name(
    *,
    dns_name: str | None = None,
    hosted_zone_id: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListHostedZonesByNameResult:
    """List hosted zones by name.

    Args:
        dns_name: Dns name.
        hosted_zone_id: Hosted zone id.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if dns_name is not None:
        kwargs["DNSName"] = dns_name
    if hosted_zone_id is not None:
        kwargs["HostedZoneId"] = hosted_zone_id
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_hosted_zones_by_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list hosted zones by name") from exc
    return ListHostedZonesByNameResult(
        hosted_zones=resp.get("HostedZones"),
        dns_name=resp.get("DNSName"),
        hosted_zone_id=resp.get("HostedZoneId"),
        is_truncated=resp.get("IsTruncated"),
        next_dns_name=resp.get("NextDNSName"),
        next_hosted_zone_id=resp.get("NextHostedZoneId"),
        max_items=resp.get("MaxItems"),
    )


def list_hosted_zones_by_vpc(
    vpc_id: str,
    vpc_region: str,
    *,
    max_items: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListHostedZonesByVpcResult:
    """List hosted zones by vpc.

    Args:
        vpc_id: Vpc id.
        vpc_region: Vpc region.
        max_items: Max items.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VPCId"] = vpc_id
    kwargs["VPCRegion"] = vpc_region
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_hosted_zones_by_vpc(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list hosted zones by vpc") from exc
    return ListHostedZonesByVpcResult(
        hosted_zone_summaries=resp.get("HostedZoneSummaries"),
        max_items=resp.get("MaxItems"),
        next_token=resp.get("NextToken"),
    )


def list_query_logging_configs(
    *,
    hosted_zone_id: str | None = None,
    next_token: str | None = None,
    max_results: str | None = None,
    region_name: str | None = None,
) -> ListQueryLoggingConfigsResult:
    """List query logging configs.

    Args:
        hosted_zone_id: Hosted zone id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if hosted_zone_id is not None:
        kwargs["HostedZoneId"] = hosted_zone_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_query_logging_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list query logging configs") from exc
    return ListQueryLoggingConfigsResult(
        query_logging_configs=resp.get("QueryLoggingConfigs"),
        next_token=resp.get("NextToken"),
    )


def list_resource_record_sets(
    hosted_zone_id: str,
    *,
    start_record_name: str | None = None,
    start_record_type: str | None = None,
    start_record_identifier: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListResourceRecordSetsResult:
    """List resource record sets.

    Args:
        hosted_zone_id: Hosted zone id.
        start_record_name: Start record name.
        start_record_type: Start record type.
        start_record_identifier: Start record identifier.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    if start_record_name is not None:
        kwargs["StartRecordName"] = start_record_name
    if start_record_type is not None:
        kwargs["StartRecordType"] = start_record_type
    if start_record_identifier is not None:
        kwargs["StartRecordIdentifier"] = start_record_identifier
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_resource_record_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource record sets") from exc
    return ListResourceRecordSetsResult(
        resource_record_sets=resp.get("ResourceRecordSets"),
        is_truncated=resp.get("IsTruncated"),
        next_record_name=resp.get("NextRecordName"),
        next_record_type=resp.get("NextRecordType"),
        next_record_identifier=resp.get("NextRecordIdentifier"),
        max_items=resp.get("MaxItems"),
    )


def list_reusable_delegation_sets(
    *,
    marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListReusableDelegationSetsResult:
    """List reusable delegation sets.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_reusable_delegation_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list reusable delegation sets") from exc
    return ListReusableDelegationSetsResult(
        delegation_sets=resp.get("DelegationSets"),
        marker=resp.get("Marker"),
        is_truncated=resp.get("IsTruncated"),
        next_marker=resp.get("NextMarker"),
        max_items=resp.get("MaxItems"),
    )


def list_tags_for_resource(
    resource_type: str,
    resource_id: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_tag_set=resp.get("ResourceTagSet"),
    )


def list_tags_for_resources(
    resource_type: str,
    resource_ids: list[str],
    region_name: str | None = None,
) -> ListTagsForResourcesResult:
    """List tags for resources.

    Args:
        resource_type: Resource type.
        resource_ids: Resource ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceIds"] = resource_ids
    try:
        resp = client.list_tags_for_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resources") from exc
    return ListTagsForResourcesResult(
        resource_tag_sets=resp.get("ResourceTagSets"),
    )


def list_traffic_policies(
    *,
    traffic_policy_id_marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListTrafficPoliciesResult:
    """List traffic policies.

    Args:
        traffic_policy_id_marker: Traffic policy id marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if traffic_policy_id_marker is not None:
        kwargs["TrafficPolicyIdMarker"] = traffic_policy_id_marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_traffic_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic policies") from exc
    return ListTrafficPoliciesResult(
        traffic_policy_summaries=resp.get("TrafficPolicySummaries"),
        is_truncated=resp.get("IsTruncated"),
        traffic_policy_id_marker=resp.get("TrafficPolicyIdMarker"),
        max_items=resp.get("MaxItems"),
    )


def list_traffic_policy_instances(
    *,
    hosted_zone_id_marker: str | None = None,
    traffic_policy_instance_name_marker: str | None = None,
    traffic_policy_instance_type_marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListTrafficPolicyInstancesResult:
    """List traffic policy instances.

    Args:
        hosted_zone_id_marker: Hosted zone id marker.
        traffic_policy_instance_name_marker: Traffic policy instance name marker.
        traffic_policy_instance_type_marker: Traffic policy instance type marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    if hosted_zone_id_marker is not None:
        kwargs["HostedZoneIdMarker"] = hosted_zone_id_marker
    if traffic_policy_instance_name_marker is not None:
        kwargs["TrafficPolicyInstanceNameMarker"] = traffic_policy_instance_name_marker
    if traffic_policy_instance_type_marker is not None:
        kwargs["TrafficPolicyInstanceTypeMarker"] = traffic_policy_instance_type_marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_traffic_policy_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic policy instances") from exc
    return ListTrafficPolicyInstancesResult(
        traffic_policy_instances=resp.get("TrafficPolicyInstances"),
        hosted_zone_id_marker=resp.get("HostedZoneIdMarker"),
        traffic_policy_instance_name_marker=resp.get("TrafficPolicyInstanceNameMarker"),
        traffic_policy_instance_type_marker=resp.get("TrafficPolicyInstanceTypeMarker"),
        is_truncated=resp.get("IsTruncated"),
        max_items=resp.get("MaxItems"),
    )


def list_traffic_policy_instances_by_hosted_zone(
    hosted_zone_id: str,
    *,
    traffic_policy_instance_name_marker: str | None = None,
    traffic_policy_instance_type_marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListTrafficPolicyInstancesByHostedZoneResult:
    """List traffic policy instances by hosted zone.

    Args:
        hosted_zone_id: Hosted zone id.
        traffic_policy_instance_name_marker: Traffic policy instance name marker.
        traffic_policy_instance_type_marker: Traffic policy instance type marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    if traffic_policy_instance_name_marker is not None:
        kwargs["TrafficPolicyInstanceNameMarker"] = traffic_policy_instance_name_marker
    if traffic_policy_instance_type_marker is not None:
        kwargs["TrafficPolicyInstanceTypeMarker"] = traffic_policy_instance_type_marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_traffic_policy_instances_by_hosted_zone(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic policy instances by hosted zone") from exc
    return ListTrafficPolicyInstancesByHostedZoneResult(
        traffic_policy_instances=resp.get("TrafficPolicyInstances"),
        traffic_policy_instance_name_marker=resp.get("TrafficPolicyInstanceNameMarker"),
        traffic_policy_instance_type_marker=resp.get("TrafficPolicyInstanceTypeMarker"),
        is_truncated=resp.get("IsTruncated"),
        max_items=resp.get("MaxItems"),
    )


def list_traffic_policy_instances_by_policy(
    traffic_policy_id: str,
    traffic_policy_version: int,
    *,
    hosted_zone_id_marker: str | None = None,
    traffic_policy_instance_name_marker: str | None = None,
    traffic_policy_instance_type_marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListTrafficPolicyInstancesByPolicyResult:
    """List traffic policy instances by policy.

    Args:
        traffic_policy_id: Traffic policy id.
        traffic_policy_version: Traffic policy version.
        hosted_zone_id_marker: Hosted zone id marker.
        traffic_policy_instance_name_marker: Traffic policy instance name marker.
        traffic_policy_instance_type_marker: Traffic policy instance type marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficPolicyId"] = traffic_policy_id
    kwargs["TrafficPolicyVersion"] = traffic_policy_version
    if hosted_zone_id_marker is not None:
        kwargs["HostedZoneIdMarker"] = hosted_zone_id_marker
    if traffic_policy_instance_name_marker is not None:
        kwargs["TrafficPolicyInstanceNameMarker"] = traffic_policy_instance_name_marker
    if traffic_policy_instance_type_marker is not None:
        kwargs["TrafficPolicyInstanceTypeMarker"] = traffic_policy_instance_type_marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_traffic_policy_instances_by_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic policy instances by policy") from exc
    return ListTrafficPolicyInstancesByPolicyResult(
        traffic_policy_instances=resp.get("TrafficPolicyInstances"),
        hosted_zone_id_marker=resp.get("HostedZoneIdMarker"),
        traffic_policy_instance_name_marker=resp.get("TrafficPolicyInstanceNameMarker"),
        traffic_policy_instance_type_marker=resp.get("TrafficPolicyInstanceTypeMarker"),
        is_truncated=resp.get("IsTruncated"),
        max_items=resp.get("MaxItems"),
    )


def list_traffic_policy_versions(
    id: str,
    *,
    traffic_policy_version_marker: str | None = None,
    max_items: str | None = None,
    region_name: str | None = None,
) -> ListTrafficPolicyVersionsResult:
    """List traffic policy versions.

    Args:
        id: Id.
        traffic_policy_version_marker: Traffic policy version marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if traffic_policy_version_marker is not None:
        kwargs["TrafficPolicyVersionMarker"] = traffic_policy_version_marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.list_traffic_policy_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic policy versions") from exc
    return ListTrafficPolicyVersionsResult(
        traffic_policies=resp.get("TrafficPolicies"),
        is_truncated=resp.get("IsTruncated"),
        traffic_policy_version_marker=resp.get("TrafficPolicyVersionMarker"),
        max_items=resp.get("MaxItems"),
    )


def list_vpc_association_authorizations(
    hosted_zone_id: str,
    *,
    next_token: str | None = None,
    max_results: str | None = None,
    region_name: str | None = None,
) -> ListVpcAssociationAuthorizationsResult:
    """List vpc association authorizations.

    Args:
        hosted_zone_id: Hosted zone id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_vpc_association_authorizations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list vpc association authorizations") from exc
    return ListVpcAssociationAuthorizationsResult(
        hosted_zone_id=resp.get("HostedZoneId"),
        next_token=resp.get("NextToken"),
        vp_cs=resp.get("VPCs"),
    )


def run_dns_answer(
    hosted_zone_id: str,
    record_name: str,
    record_type: str,
    *,
    resolver_ip: str | None = None,
    edns0_client_subnet_ip: str | None = None,
    edns0_client_subnet_mask: str | None = None,
    region_name: str | None = None,
) -> RunDnsAnswerResult:
    """Run dns answer.

    Args:
        hosted_zone_id: Hosted zone id.
        record_name: Record name.
        record_type: Record type.
        resolver_ip: Resolver ip.
        edns0_client_subnet_ip: Edns0 client subnet ip.
        edns0_client_subnet_mask: Edns0 client subnet mask.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HostedZoneId"] = hosted_zone_id
    kwargs["RecordName"] = record_name
    kwargs["RecordType"] = record_type
    if resolver_ip is not None:
        kwargs["ResolverIP"] = resolver_ip
    if edns0_client_subnet_ip is not None:
        kwargs["EDNS0ClientSubnetIP"] = edns0_client_subnet_ip
    if edns0_client_subnet_mask is not None:
        kwargs["EDNS0ClientSubnetMask"] = edns0_client_subnet_mask
    try:
        resp = client.test_dns_answer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run dns answer") from exc
    return RunDnsAnswerResult(
        nameserver=resp.get("Nameserver"),
        record_name=resp.get("RecordName"),
        record_type=resp.get("RecordType"),
        record_data=resp.get("RecordData"),
        response_code=resp.get("ResponseCode"),
        protocol=resp.get("Protocol"),
    )


def update_health_check(
    health_check_id: str,
    *,
    health_check_version: int | None = None,
    ip_address: str | None = None,
    port: int | None = None,
    resource_path: str | None = None,
    fully_qualified_domain_name: str | None = None,
    search_string: str | None = None,
    failure_threshold: int | None = None,
    inverted: bool | None = None,
    disabled: bool | None = None,
    health_threshold: int | None = None,
    child_health_checks: list[str] | None = None,
    enable_sni: bool | None = None,
    regions: list[str] | None = None,
    alarm_identifier: dict[str, Any] | None = None,
    insufficient_data_health_status: str | None = None,
    reset_elements: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateHealthCheckResult:
    """Update health check.

    Args:
        health_check_id: Health check id.
        health_check_version: Health check version.
        ip_address: Ip address.
        port: Port.
        resource_path: Resource path.
        fully_qualified_domain_name: Fully qualified domain name.
        search_string: Search string.
        failure_threshold: Failure threshold.
        inverted: Inverted.
        disabled: Disabled.
        health_threshold: Health threshold.
        child_health_checks: Child health checks.
        enable_sni: Enable sni.
        regions: Regions.
        alarm_identifier: Alarm identifier.
        insufficient_data_health_status: Insufficient data health status.
        reset_elements: Reset elements.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HealthCheckId"] = health_check_id
    if health_check_version is not None:
        kwargs["HealthCheckVersion"] = health_check_version
    if ip_address is not None:
        kwargs["IPAddress"] = ip_address
    if port is not None:
        kwargs["Port"] = port
    if resource_path is not None:
        kwargs["ResourcePath"] = resource_path
    if fully_qualified_domain_name is not None:
        kwargs["FullyQualifiedDomainName"] = fully_qualified_domain_name
    if search_string is not None:
        kwargs["SearchString"] = search_string
    if failure_threshold is not None:
        kwargs["FailureThreshold"] = failure_threshold
    if inverted is not None:
        kwargs["Inverted"] = inverted
    if disabled is not None:
        kwargs["Disabled"] = disabled
    if health_threshold is not None:
        kwargs["HealthThreshold"] = health_threshold
    if child_health_checks is not None:
        kwargs["ChildHealthChecks"] = child_health_checks
    if enable_sni is not None:
        kwargs["EnableSNI"] = enable_sni
    if regions is not None:
        kwargs["Regions"] = regions
    if alarm_identifier is not None:
        kwargs["AlarmIdentifier"] = alarm_identifier
    if insufficient_data_health_status is not None:
        kwargs["InsufficientDataHealthStatus"] = insufficient_data_health_status
    if reset_elements is not None:
        kwargs["ResetElements"] = reset_elements
    try:
        resp = client.update_health_check(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update health check") from exc
    return UpdateHealthCheckResult(
        health_check=resp.get("HealthCheck"),
    )


def update_hosted_zone_comment(
    id: str,
    *,
    comment: str | None = None,
    region_name: str | None = None,
) -> UpdateHostedZoneCommentResult:
    """Update hosted zone comment.

    Args:
        id: Id.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if comment is not None:
        kwargs["Comment"] = comment
    try:
        resp = client.update_hosted_zone_comment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update hosted zone comment") from exc
    return UpdateHostedZoneCommentResult(
        hosted_zone=resp.get("HostedZone"),
    )


def update_traffic_policy_comment(
    id: str,
    version: int,
    comment: str,
    region_name: str | None = None,
) -> UpdateTrafficPolicyCommentResult:
    """Update traffic policy comment.

    Args:
        id: Id.
        version: Version.
        comment: Comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Version"] = version
    kwargs["Comment"] = comment
    try:
        resp = client.update_traffic_policy_comment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update traffic policy comment") from exc
    return UpdateTrafficPolicyCommentResult(
        traffic_policy=resp.get("TrafficPolicy"),
    )


def update_traffic_policy_instance(
    id: str,
    ttl: int,
    traffic_policy_id: str,
    traffic_policy_version: int,
    region_name: str | None = None,
) -> UpdateTrafficPolicyInstanceResult:
    """Update traffic policy instance.

    Args:
        id: Id.
        ttl: Ttl.
        traffic_policy_id: Traffic policy id.
        traffic_policy_version: Traffic policy version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("route53", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["TTL"] = ttl
    kwargs["TrafficPolicyId"] = traffic_policy_id
    kwargs["TrafficPolicyVersion"] = traffic_policy_version
    try:
        resp = client.update_traffic_policy_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update traffic policy instance") from exc
    return UpdateTrafficPolicyInstanceResult(
        traffic_policy_instance=resp.get("TrafficPolicyInstance"),
    )
