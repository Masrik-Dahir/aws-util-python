"""Native async ELBv2 utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time as _time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.elbv2 import (
    AddListenerCertificatesResult,
    AddTrustStoreRevocationsResult,
    CreateTrustStoreResult,
    DescribeAccountLimitsResult,
    DescribeCapacityReservationResult,
    DescribeListenerAttributesResult,
    DescribeListenerCertificatesResult,
    DescribeLoadBalancerAttributesResult,
    DescribeSslPoliciesResult,
    DescribeTargetGroupAttributesResult,
    DescribeTrustStoreAssociationsResult,
    DescribeTrustStoreRevocationsResult,
    DescribeTrustStoresResult,
    GetResourcePolicyResult,
    GetTrustStoreCaCertificatesBundleResult,
    GetTrustStoreRevocationContentResult,
    ListenerResult,
    LoadBalancerResult,
    ModifyCapacityReservationResult,
    ModifyIpPoolsResult,
    ModifyListenerAttributesResult,
    ModifyTargetGroupAttributesResult,
    ModifyTrustStoreResult,
    RuleResult,
    SetIpAddressTypeResult,
    SetRulePrioritiesResult,
    TargetGroupResult,
    _build_tags,
    _parse_lb,
    _parse_listener,
    _parse_rule,
    _parse_tg,
)
from aws_util.exceptions import AwsNotFoundError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "AddListenerCertificatesResult",
    "AddTrustStoreRevocationsResult",
    "CreateTrustStoreResult",
    "DescribeAccountLimitsResult",
    "DescribeCapacityReservationResult",
    "DescribeListenerAttributesResult",
    "DescribeListenerCertificatesResult",
    "DescribeLoadBalancerAttributesResult",
    "DescribeSslPoliciesResult",
    "DescribeTargetGroupAttributesResult",
    "DescribeTrustStoreAssociationsResult",
    "DescribeTrustStoreRevocationsResult",
    "DescribeTrustStoresResult",
    "GetResourcePolicyResult",
    "GetTrustStoreCaCertificatesBundleResult",
    "GetTrustStoreRevocationContentResult",
    "ListenerResult",
    "LoadBalancerResult",
    "ModifyCapacityReservationResult",
    "ModifyIpPoolsResult",
    "ModifyListenerAttributesResult",
    "ModifyTargetGroupAttributesResult",
    "ModifyTrustStoreResult",
    "RuleResult",
    "SetIpAddressTypeResult",
    "SetRulePrioritiesResult",
    "TargetGroupResult",
    "add_listener_certificates",
    "add_tags",
    "add_trust_store_revocations",
    "create_listener",
    "create_load_balancer",
    "create_rule",
    "create_target_group",
    "create_trust_store",
    "delete_listener",
    "delete_load_balancer",
    "delete_rule",
    "delete_shared_trust_store_association",
    "delete_target_group",
    "delete_trust_store",
    "deregister_targets",
    "describe_account_limits",
    "describe_capacity_reservation",
    "describe_listener_attributes",
    "describe_listener_certificates",
    "describe_listeners",
    "describe_load_balancer_attributes",
    "describe_load_balancers",
    "describe_rules",
    "describe_ssl_policies",
    "describe_tags",
    "describe_target_group_attributes",
    "describe_target_groups",
    "describe_target_health",
    "describe_trust_store_associations",
    "describe_trust_store_revocations",
    "describe_trust_stores",
    "ensure_load_balancer",
    "ensure_target_group",
    "get_resource_policy",
    "get_trust_store_ca_certificates_bundle",
    "get_trust_store_revocation_content",
    "modify_capacity_reservation",
    "modify_ip_pools",
    "modify_listener",
    "modify_listener_attributes",
    "modify_load_balancer_attributes",
    "modify_rule",
    "modify_target_group",
    "modify_target_group_attributes",
    "modify_trust_store",
    "register_targets",
    "remove_listener_certificates",
    "remove_tags",
    "remove_trust_store_revocations",
    "set_ip_address_type",
    "set_rule_priorities",
    "set_security_groups",
    "set_subnets",
    "wait_for_load_balancer",
]


# ---------------------------------------------------------------------------
# Load Balancer operations
# ---------------------------------------------------------------------------


async def create_load_balancer(
    name: str,
    *,
    subnets: list[str],
    security_groups: list[str] | None = None,
    scheme: str = "internet-facing",
    type: str = "application",
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> LoadBalancerResult:
    """Create an ELBv2 load balancer.

    Args:
        name: Load balancer name.
        subnets: List of subnet IDs.
        security_groups: Security group IDs (ALB only).
        scheme: ``"internet-facing"`` or ``"internal"``.
        type: ``"application"``, ``"network"``, or ``"gateway"``.
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`LoadBalancerResult` for the new load balancer.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "Subnets": subnets,
        "Scheme": scheme,
        "Type": type,
    }
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    if tags:
        kwargs["Tags"] = _build_tags(tags)
    try:
        resp = await client.call("CreateLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_load_balancer failed for {name!r}") from exc
    lbs = resp.get("LoadBalancers", [])
    return _parse_lb(lbs[0])


async def describe_load_balancers(
    *,
    names: list[str] | None = None,
    arns: list[str] | None = None,
    region_name: str | None = None,
) -> list[LoadBalancerResult]:
    """Describe ELBv2 load balancers.

    Args:
        names: Filter by load-balancer names.
        arns: Filter by load-balancer ARNs.
        region_name: AWS region override.

    Returns:
        A list of :class:`LoadBalancerResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["Names"] = names
    if arns:
        kwargs["LoadBalancerArns"] = arns
    results: list[LoadBalancerResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeLoadBalancers", **kwargs)
            for lb in resp.get("LoadBalancers", []):
                results.append(_parse_lb(lb))
            token = resp.get("NextMarker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_load_balancers failed") from exc
    return results


async def modify_load_balancer_attributes(
    arn: str,
    *,
    attributes: list[dict[str, str]],
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """Modify load-balancer attributes.

    Args:
        arn: Load-balancer ARN.
        attributes: List of ``{"Key": ..., "Value": ...}`` attribute dicts.
        region_name: AWS region override.

    Returns:
        The resulting list of attribute dicts from the API response.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        resp = await client.call(
            "ModifyLoadBalancerAttributes",
            LoadBalancerArn=arn,
            Attributes=attributes,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_load_balancer_attributes failed") from exc
    return resp.get("Attributes", [])


async def delete_load_balancer(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an ELBv2 load balancer.

    Args:
        arn: Load-balancer ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call("DeleteLoadBalancer", LoadBalancerArn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_load_balancer failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Target Group operations
# ---------------------------------------------------------------------------


async def create_target_group(
    name: str,
    *,
    protocol: str = "HTTP",
    port: int = 80,
    vpc_id: str,
    health_check_path: str = "/",
    target_type: str = "instance",
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> TargetGroupResult:
    """Create an ELBv2 target group.

    Args:
        name: Target group name.
        protocol: Protocol (HTTP, HTTPS, TCP, etc.).
        port: Port number.
        vpc_id: VPC ID for the target group.
        health_check_path: Health check path.
        target_type: Target type (instance, ip, lambda).
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`TargetGroupResult` for the new target group.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "Protocol": protocol,
        "Port": port,
        "VpcId": vpc_id,
        "HealthCheckPath": health_check_path,
        "TargetType": target_type,
    }
    if tags:
        kwargs["Tags"] = _build_tags(tags)
    try:
        resp = await client.call("CreateTargetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_target_group failed for {name!r}") from exc
    tgs = resp.get("TargetGroups", [])
    return _parse_tg(tgs[0])


async def describe_target_groups(
    *,
    names: list[str] | None = None,
    arns: list[str] | None = None,
    load_balancer_arn: str | None = None,
    region_name: str | None = None,
) -> list[TargetGroupResult]:
    """Describe ELBv2 target groups.

    Args:
        names: Filter by target-group names.
        arns: Filter by target-group ARNs.
        load_balancer_arn: Filter by associated load-balancer ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`TargetGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["Names"] = names
    if arns:
        kwargs["TargetGroupArns"] = arns
    if load_balancer_arn:
        kwargs["LoadBalancerArn"] = load_balancer_arn
    results: list[TargetGroupResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeTargetGroups", **kwargs)
            for tg in resp.get("TargetGroups", []):
                results.append(_parse_tg(tg))
            token = resp.get("NextMarker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_target_groups failed") from exc
    return results


async def modify_target_group(
    arn: str,
    *,
    health_check_path: str | None = None,
    region_name: str | None = None,
) -> TargetGroupResult:
    """Modify an ELBv2 target group.

    Args:
        arn: Target-group ARN.
        health_check_path: New health-check path.
        region_name: AWS region override.

    Returns:
        The updated :class:`TargetGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {"TargetGroupArn": arn}
    if health_check_path is not None:
        kwargs["HealthCheckPath"] = health_check_path
    try:
        resp = await client.call("ModifyTargetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"modify_target_group failed for {arn!r}") from exc
    tgs = resp.get("TargetGroups", [])
    return _parse_tg(tgs[0])


async def delete_target_group(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an ELBv2 target group.

    Args:
        arn: Target-group ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call("DeleteTargetGroup", TargetGroupArn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_target_group failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Target registration
# ---------------------------------------------------------------------------


async def register_targets(
    target_group_arn: str,
    *,
    targets: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Register targets with a target group.

    Args:
        target_group_arn: Target-group ARN.
        targets: List of target dicts with ``Id`` and optional ``Port``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call(
            "RegisterTargets",
            TargetGroupArn=target_group_arn,
            Targets=targets,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "register_targets failed") from exc


async def deregister_targets(
    target_group_arn: str,
    *,
    targets: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Deregister targets from a target group.

    Args:
        target_group_arn: Target-group ARN.
        targets: List of target dicts with ``Id`` and optional ``Port``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call(
            "DeregisterTargets",
            TargetGroupArn=target_group_arn,
            Targets=targets,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "deregister_targets failed") from exc


async def describe_target_health(
    target_group_arn: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Describe the health of targets in a target group.

    Args:
        target_group_arn: Target-group ARN.
        region_name: AWS region override.

    Returns:
        A list of target-health description dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        resp = await client.call(
            "DescribeTargetHealth",
            TargetGroupArn=target_group_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_target_health failed") from exc
    return resp.get("TargetHealthDescriptions", [])


# ---------------------------------------------------------------------------
# Listener operations
# ---------------------------------------------------------------------------


async def create_listener(
    load_balancer_arn: str,
    *,
    port: int = 80,
    protocol: str = "HTTP",
    default_actions: list[dict[str, Any]],
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ListenerResult:
    """Create a listener on a load balancer.

    Args:
        load_balancer_arn: The load-balancer ARN.
        port: Listener port (default 80).
        protocol: Protocol (HTTP, HTTPS, TCP, etc.).
        default_actions: Default action list for the listener.
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`ListenerResult` for the new listener.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {
        "LoadBalancerArn": load_balancer_arn,
        "Port": port,
        "Protocol": protocol,
        "DefaultActions": default_actions,
    }
    if tags:
        kwargs["Tags"] = _build_tags(tags)
    try:
        resp = await client.call("CreateListener", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_listener failed") from exc
    listeners = resp.get("Listeners", [])
    return _parse_listener(listeners[0])


async def describe_listeners(
    load_balancer_arn: str,
    *,
    region_name: str | None = None,
) -> list[ListenerResult]:
    """Describe listeners for a load balancer.

    Args:
        load_balancer_arn: The load-balancer ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`ListenerResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    results: list[ListenerResult] = []
    try:
        token: str | None = None
        while True:
            kw: dict[str, Any] = {"LoadBalancerArn": load_balancer_arn}
            if token:
                kw["Marker"] = token
            resp = await client.call("DescribeListeners", **kw)
            for ln in resp.get("Listeners", []):
                results.append(_parse_listener(ln))
            token = resp.get("NextMarker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_listeners failed") from exc
    return results


async def modify_listener(
    arn: str,
    *,
    port: int | None = None,
    protocol: str | None = None,
    default_actions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListenerResult:
    """Modify an existing listener.

    Args:
        arn: Listener ARN.
        port: New port number.
        protocol: New protocol.
        default_actions: New default actions.
        region_name: AWS region override.

    Returns:
        The updated :class:`ListenerResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {"ListenerArn": arn}
    if port is not None:
        kwargs["Port"] = port
    if protocol is not None:
        kwargs["Protocol"] = protocol
    if default_actions is not None:
        kwargs["DefaultActions"] = default_actions
    try:
        resp = await client.call("ModifyListener", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"modify_listener failed for {arn!r}") from exc
    listeners = resp.get("Listeners", [])
    return _parse_listener(listeners[0])


async def delete_listener(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a listener.

    Args:
        arn: Listener ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call("DeleteListener", ListenerArn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_listener failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Rule operations
# ---------------------------------------------------------------------------


async def create_rule(
    listener_arn: str,
    *,
    conditions: list[dict[str, Any]],
    actions: list[dict[str, Any]],
    priority: int,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> RuleResult:
    """Create a listener rule.

    Args:
        listener_arn: The listener ARN.
        conditions: Rule condition list.
        actions: Rule action list.
        priority: Integer priority (1-50000).
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`RuleResult` for the new rule.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {
        "ListenerArn": listener_arn,
        "Conditions": conditions,
        "Actions": actions,
        "Priority": priority,
    }
    if tags:
        kwargs["Tags"] = _build_tags(tags)
    try:
        resp = await client.call("CreateRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_rule failed") from exc
    rules = resp.get("Rules", [])
    return _parse_rule(rules[0])


async def describe_rules(
    listener_arn: str,
    *,
    region_name: str | None = None,
) -> list[RuleResult]:
    """Describe rules for a listener.

    Args:
        listener_arn: The listener ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`RuleResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    results: list[RuleResult] = []
    try:
        token: str | None = None
        while True:
            kw: dict[str, Any] = {"ListenerArn": listener_arn}
            if token:
                kw["Marker"] = token
            resp = await client.call("DescribeRules", **kw)
            for rule in resp.get("Rules", []):
                results.append(_parse_rule(rule))
            token = resp.get("NextMarker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_rules failed") from exc
    return results


async def modify_rule(
    arn: str,
    *,
    conditions: list[dict[str, Any]] | None = None,
    actions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> RuleResult:
    """Modify a listener rule.

    Args:
        arn: Rule ARN.
        conditions: New conditions.
        actions: New actions.
        region_name: AWS region override.

    Returns:
        The updated :class:`RuleResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {"RuleArn": arn}
    if conditions is not None:
        kwargs["Conditions"] = conditions
    if actions is not None:
        kwargs["Actions"] = actions
    try:
        resp = await client.call("ModifyRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"modify_rule failed for {arn!r}") from exc
    rules = resp.get("Rules", [])
    return _parse_rule(rules[0])


async def delete_rule(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a listener rule.

    Args:
        arn: Rule ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call("DeleteRule", RuleArn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_rule failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Subnet / security-group management
# ---------------------------------------------------------------------------


async def set_subnets(
    arn: str,
    *,
    subnets: list[str],
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Set the subnets for a load balancer.

    Args:
        arn: Load-balancer ARN.
        subnets: New subnet IDs.
        region_name: AWS region override.

    Returns:
        The resulting availability-zone list from the API response.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        resp = await client.call(
            "SetSubnets",
            LoadBalancerArn=arn,
            Subnets=subnets,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "set_subnets failed") from exc
    return resp.get("AvailabilityZones", [])


async def set_security_groups(
    arn: str,
    *,
    security_groups: list[str],
    region_name: str | None = None,
) -> list[str]:
    """Set the security groups for a load balancer.

    Args:
        arn: Load-balancer ARN.
        security_groups: New security-group IDs.
        region_name: AWS region override.

    Returns:
        The resulting list of security-group IDs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        resp = await client.call(
            "SetSecurityGroups",
            LoadBalancerArn=arn,
            SecurityGroups=security_groups,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "set_security_groups failed") from exc
    return resp.get("SecurityGroupIds", [])


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


async def add_tags(
    arns: list[str],
    *,
    tags: dict[str, str],
    region_name: str | None = None,
) -> None:
    """Add tags to one or more ELBv2 resources.

    Args:
        arns: Resource ARNs to tag.
        tags: Key-value tags to add.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call(
            "AddTags",
            ResourceArns=arns,
            Tags=_build_tags(tags),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "add_tags failed") from exc


async def remove_tags(
    arns: list[str],
    *,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags from one or more ELBv2 resources.

    Args:
        arns: Resource ARNs to untag.
        tag_keys: Tag keys to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        await client.call(
            "RemoveTags",
            ResourceArns=arns,
            TagKeys=tag_keys,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "remove_tags failed") from exc


async def describe_tags(
    arns: list[str],
    *,
    region_name: str | None = None,
) -> dict[str, dict[str, str]]:
    """Describe tags for one or more ELBv2 resources.

    Args:
        arns: Resource ARNs to describe tags for.
        region_name: AWS region override.

    Returns:
        A dict mapping each resource ARN to its ``{key: value}`` tags.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    try:
        resp = await client.call("DescribeTags", ResourceArns=arns)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_tags failed") from exc
    result: dict[str, dict[str, str]] = {}
    for desc in resp.get("TagDescriptions", []):
        arn = desc["ResourceArn"]
        result[arn] = {t["Key"]: t["Value"] for t in desc.get("Tags", [])}
    return result


# ---------------------------------------------------------------------------
# High-level utilities
# ---------------------------------------------------------------------------


async def wait_for_load_balancer(
    arn: str,
    *,
    timeout: float = 300,
    poll_interval: float = 10,
    region_name: str | None = None,
) -> LoadBalancerResult:
    """Poll until a load balancer reaches the ``active`` state.

    Args:
        arn: Load-balancer ARN.
        timeout: Maximum seconds to wait (default 300).
        poll_interval: Seconds between polls (default 10).
        region_name: AWS region override.

    Returns:
        The :class:`LoadBalancerResult` in the ``active`` state.

    Raises:
        AwsTimeoutError: If the load balancer does not become active within
            *timeout*.
        AwsNotFoundError: If the load balancer is not found.
        RuntimeError: If the API call fails.
    """
    deadline = _time.monotonic() + timeout
    while True:
        lbs = await describe_load_balancers(arns=[arn], region_name=region_name)
        if not lbs:
            raise AwsNotFoundError(f"Load balancer {arn!r} not found")
        lb = lbs[0]
        if lb.state == "active":
            return lb
        if _time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Load balancer {arn!r} did not reach 'active' state "
                f"within {timeout}s (current: {lb.state!r})"
            )
        await asyncio.sleep(poll_interval)


async def ensure_load_balancer(
    name: str,
    *,
    subnets: list[str],
    security_groups: list[str] | None = None,
    scheme: str = "internet-facing",
    type: str = "application",
    region_name: str | None = None,
) -> tuple[LoadBalancerResult, bool]:
    """Ensure a load balancer exists, creating it if necessary.

    Args:
        name: Load balancer name.
        subnets: Subnet IDs.
        security_groups: Security group IDs (ALB only).
        scheme: ``"internet-facing"`` or ``"internal"``.
        type: ``"application"``, ``"network"``, or ``"gateway"``.
        region_name: AWS region override.

    Returns:
        A tuple of ``(LoadBalancerResult, created)`` where *created* is
        ``True`` if the load balancer was newly created.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        existing = await describe_load_balancers(names=[name], region_name=region_name)
        if existing:
            return existing[0], False
    except RuntimeError:
        pass
    lb = await create_load_balancer(
        name,
        subnets=subnets,
        security_groups=security_groups,
        scheme=scheme,
        type=type,
        region_name=region_name,
    )
    return lb, True


async def ensure_target_group(
    name: str,
    *,
    protocol: str = "HTTP",
    port: int = 80,
    vpc_id: str,
    target_type: str = "instance",
    region_name: str | None = None,
) -> tuple[TargetGroupResult, bool]:
    """Ensure a target group exists, creating it if necessary.

    Args:
        name: Target group name.
        protocol: Protocol.
        port: Port.
        vpc_id: VPC ID.
        target_type: Target type.
        region_name: AWS region override.

    Returns:
        A tuple of ``(TargetGroupResult, created)`` where *created* is
        ``True`` if the target group was newly created.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        existing = await describe_target_groups(names=[name], region_name=region_name)
        if existing:
            return existing[0], False
    except RuntimeError:
        pass
    tg = await create_target_group(
        name,
        protocol=protocol,
        port=port,
        vpc_id=vpc_id,
        target_type=target_type,
        region_name=region_name,
    )
    return tg, True


async def add_listener_certificates(
    listener_arn: str,
    certificates: list[dict[str, Any]],
    region_name: str | None = None,
) -> AddListenerCertificatesResult:
    """Add listener certificates.

    Args:
        listener_arn: Listener arn.
        certificates: Certificates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ListenerArn"] = listener_arn
    kwargs["Certificates"] = certificates
    try:
        resp = await client.call("AddListenerCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add listener certificates") from exc
    return AddListenerCertificatesResult(
        certificates=resp.get("Certificates"),
    )


async def add_trust_store_revocations(
    trust_store_arn: str,
    *,
    revocation_contents: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> AddTrustStoreRevocationsResult:
    """Add trust store revocations.

    Args:
        trust_store_arn: Trust store arn.
        revocation_contents: Revocation contents.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    if revocation_contents is not None:
        kwargs["RevocationContents"] = revocation_contents
    try:
        resp = await client.call("AddTrustStoreRevocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add trust store revocations") from exc
    return AddTrustStoreRevocationsResult(
        trust_store_revocations=resp.get("TrustStoreRevocations"),
    )


async def create_trust_store(
    name: str,
    ca_certificates_bundle_s3_bucket: str,
    ca_certificates_bundle_s3_key: str,
    *,
    ca_certificates_bundle_s3_object_version: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTrustStoreResult:
    """Create trust store.

    Args:
        name: Name.
        ca_certificates_bundle_s3_bucket: Ca certificates bundle s3 bucket.
        ca_certificates_bundle_s3_key: Ca certificates bundle s3 key.
        ca_certificates_bundle_s3_object_version: Ca certificates bundle s3 object version.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["CaCertificatesBundleS3Bucket"] = ca_certificates_bundle_s3_bucket
    kwargs["CaCertificatesBundleS3Key"] = ca_certificates_bundle_s3_key
    if ca_certificates_bundle_s3_object_version is not None:
        kwargs["CaCertificatesBundleS3ObjectVersion"] = ca_certificates_bundle_s3_object_version
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateTrustStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create trust store") from exc
    return CreateTrustStoreResult(
        trust_stores=resp.get("TrustStores"),
    )


async def delete_shared_trust_store_association(
    trust_store_arn: str,
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete shared trust store association.

    Args:
        trust_store_arn: Trust store arn.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteSharedTrustStoreAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete shared trust store association") from exc
    return None


async def delete_trust_store(
    trust_store_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete trust store.

    Args:
        trust_store_arn: Trust store arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    try:
        await client.call("DeleteTrustStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete trust store") from exc
    return None


async def describe_account_limits(
    *,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> DescribeAccountLimitsResult:
    """Describe account limits.

    Args:
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("DescribeAccountLimits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account limits") from exc
    return DescribeAccountLimitsResult(
        limits=resp.get("Limits"),
        next_marker=resp.get("NextMarker"),
    )


async def describe_capacity_reservation(
    load_balancer_arn: str,
    region_name: str | None = None,
) -> DescribeCapacityReservationResult:
    """Describe capacity reservation.

    Args:
        load_balancer_arn: Load balancer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LoadBalancerArn"] = load_balancer_arn
    try:
        resp = await client.call("DescribeCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe capacity reservation") from exc
    return DescribeCapacityReservationResult(
        last_modified_time=resp.get("LastModifiedTime"),
        decrease_requests_remaining=resp.get("DecreaseRequestsRemaining"),
        minimum_load_balancer_capacity=resp.get("MinimumLoadBalancerCapacity"),
        capacity_reservation_state=resp.get("CapacityReservationState"),
    )


async def describe_listener_attributes(
    listener_arn: str,
    region_name: str | None = None,
) -> DescribeListenerAttributesResult:
    """Describe listener attributes.

    Args:
        listener_arn: Listener arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ListenerArn"] = listener_arn
    try:
        resp = await client.call("DescribeListenerAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe listener attributes") from exc
    return DescribeListenerAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def describe_listener_certificates(
    listener_arn: str,
    *,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> DescribeListenerCertificatesResult:
    """Describe listener certificates.

    Args:
        listener_arn: Listener arn.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ListenerArn"] = listener_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("DescribeListenerCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe listener certificates") from exc
    return DescribeListenerCertificatesResult(
        certificates=resp.get("Certificates"),
        next_marker=resp.get("NextMarker"),
    )


async def describe_load_balancer_attributes(
    load_balancer_arn: str,
    region_name: str | None = None,
) -> DescribeLoadBalancerAttributesResult:
    """Describe load balancer attributes.

    Args:
        load_balancer_arn: Load balancer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LoadBalancerArn"] = load_balancer_arn
    try:
        resp = await client.call("DescribeLoadBalancerAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe load balancer attributes") from exc
    return DescribeLoadBalancerAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def describe_ssl_policies(
    *,
    names: list[str] | None = None,
    marker: str | None = None,
    page_size: int | None = None,
    load_balancer_type: str | None = None,
    region_name: str | None = None,
) -> DescribeSslPoliciesResult:
    """Describe ssl policies.

    Args:
        names: Names.
        marker: Marker.
        page_size: Page size.
        load_balancer_type: Load balancer type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    if names is not None:
        kwargs["Names"] = names
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if load_balancer_type is not None:
        kwargs["LoadBalancerType"] = load_balancer_type
    try:
        resp = await client.call("DescribeSSLPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe ssl policies") from exc
    return DescribeSslPoliciesResult(
        ssl_policies=resp.get("SslPolicies"),
        next_marker=resp.get("NextMarker"),
    )


async def describe_target_group_attributes(
    target_group_arn: str,
    region_name: str | None = None,
) -> DescribeTargetGroupAttributesResult:
    """Describe target group attributes.

    Args:
        target_group_arn: Target group arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetGroupArn"] = target_group_arn
    try:
        resp = await client.call("DescribeTargetGroupAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe target group attributes") from exc
    return DescribeTargetGroupAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def describe_trust_store_associations(
    trust_store_arn: str,
    *,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> DescribeTrustStoreAssociationsResult:
    """Describe trust store associations.

    Args:
        trust_store_arn: Trust store arn.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("DescribeTrustStoreAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe trust store associations") from exc
    return DescribeTrustStoreAssociationsResult(
        trust_store_associations=resp.get("TrustStoreAssociations"),
        next_marker=resp.get("NextMarker"),
    )


async def describe_trust_store_revocations(
    trust_store_arn: str,
    *,
    revocation_ids: list[int] | None = None,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> DescribeTrustStoreRevocationsResult:
    """Describe trust store revocations.

    Args:
        trust_store_arn: Trust store arn.
        revocation_ids: Revocation ids.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    if revocation_ids is not None:
        kwargs["RevocationIds"] = revocation_ids
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("DescribeTrustStoreRevocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe trust store revocations") from exc
    return DescribeTrustStoreRevocationsResult(
        trust_store_revocations=resp.get("TrustStoreRevocations"),
        next_marker=resp.get("NextMarker"),
    )


async def describe_trust_stores(
    *,
    trust_store_arns: list[str] | None = None,
    names: list[str] | None = None,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> DescribeTrustStoresResult:
    """Describe trust stores.

    Args:
        trust_store_arns: Trust store arns.
        names: Names.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    if trust_store_arns is not None:
        kwargs["TrustStoreArns"] = trust_store_arns
    if names is not None:
        kwargs["Names"] = names
    if marker is not None:
        kwargs["Marker"] = marker
    if page_size is not None:
        kwargs["PageSize"] = page_size
    try:
        resp = await client.call("DescribeTrustStores", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe trust stores") from exc
    return DescribeTrustStoresResult(
        trust_stores=resp.get("TrustStores"),
        next_marker=resp.get("NextMarker"),
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
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy=resp.get("Policy"),
    )


async def get_trust_store_ca_certificates_bundle(
    trust_store_arn: str,
    region_name: str | None = None,
) -> GetTrustStoreCaCertificatesBundleResult:
    """Get trust store ca certificates bundle.

    Args:
        trust_store_arn: Trust store arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    try:
        resp = await client.call("GetTrustStoreCaCertificatesBundle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get trust store ca certificates bundle") from exc
    return GetTrustStoreCaCertificatesBundleResult(
        location=resp.get("Location"),
    )


async def get_trust_store_revocation_content(
    trust_store_arn: str,
    revocation_id: int,
    region_name: str | None = None,
) -> GetTrustStoreRevocationContentResult:
    """Get trust store revocation content.

    Args:
        trust_store_arn: Trust store arn.
        revocation_id: Revocation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    kwargs["RevocationId"] = revocation_id
    try:
        resp = await client.call("GetTrustStoreRevocationContent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get trust store revocation content") from exc
    return GetTrustStoreRevocationContentResult(
        location=resp.get("Location"),
    )


async def modify_capacity_reservation(
    load_balancer_arn: str,
    *,
    minimum_load_balancer_capacity: dict[str, Any] | None = None,
    reset_capacity_reservation: bool | None = None,
    region_name: str | None = None,
) -> ModifyCapacityReservationResult:
    """Modify capacity reservation.

    Args:
        load_balancer_arn: Load balancer arn.
        minimum_load_balancer_capacity: Minimum load balancer capacity.
        reset_capacity_reservation: Reset capacity reservation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LoadBalancerArn"] = load_balancer_arn
    if minimum_load_balancer_capacity is not None:
        kwargs["MinimumLoadBalancerCapacity"] = minimum_load_balancer_capacity
    if reset_capacity_reservation is not None:
        kwargs["ResetCapacityReservation"] = reset_capacity_reservation
    try:
        resp = await client.call("ModifyCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify capacity reservation") from exc
    return ModifyCapacityReservationResult(
        last_modified_time=resp.get("LastModifiedTime"),
        decrease_requests_remaining=resp.get("DecreaseRequestsRemaining"),
        minimum_load_balancer_capacity=resp.get("MinimumLoadBalancerCapacity"),
        capacity_reservation_state=resp.get("CapacityReservationState"),
    )


async def modify_ip_pools(
    load_balancer_arn: str,
    *,
    ipam_pools: dict[str, Any] | None = None,
    remove_ipam_pools: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyIpPoolsResult:
    """Modify ip pools.

    Args:
        load_balancer_arn: Load balancer arn.
        ipam_pools: Ipam pools.
        remove_ipam_pools: Remove ipam pools.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LoadBalancerArn"] = load_balancer_arn
    if ipam_pools is not None:
        kwargs["IpamPools"] = ipam_pools
    if remove_ipam_pools is not None:
        kwargs["RemoveIpamPools"] = remove_ipam_pools
    try:
        resp = await client.call("ModifyIpPools", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify ip pools") from exc
    return ModifyIpPoolsResult(
        ipam_pools=resp.get("IpamPools"),
    )


async def modify_listener_attributes(
    listener_arn: str,
    attributes: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyListenerAttributesResult:
    """Modify listener attributes.

    Args:
        listener_arn: Listener arn.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ListenerArn"] = listener_arn
    kwargs["Attributes"] = attributes
    try:
        resp = await client.call("ModifyListenerAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify listener attributes") from exc
    return ModifyListenerAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def modify_target_group_attributes(
    target_group_arn: str,
    attributes: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyTargetGroupAttributesResult:
    """Modify target group attributes.

    Args:
        target_group_arn: Target group arn.
        attributes: Attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetGroupArn"] = target_group_arn
    kwargs["Attributes"] = attributes
    try:
        resp = await client.call("ModifyTargetGroupAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify target group attributes") from exc
    return ModifyTargetGroupAttributesResult(
        attributes=resp.get("Attributes"),
    )


async def modify_trust_store(
    trust_store_arn: str,
    ca_certificates_bundle_s3_bucket: str,
    ca_certificates_bundle_s3_key: str,
    *,
    ca_certificates_bundle_s3_object_version: str | None = None,
    region_name: str | None = None,
) -> ModifyTrustStoreResult:
    """Modify trust store.

    Args:
        trust_store_arn: Trust store arn.
        ca_certificates_bundle_s3_bucket: Ca certificates bundle s3 bucket.
        ca_certificates_bundle_s3_key: Ca certificates bundle s3 key.
        ca_certificates_bundle_s3_object_version: Ca certificates bundle s3 object version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    kwargs["CaCertificatesBundleS3Bucket"] = ca_certificates_bundle_s3_bucket
    kwargs["CaCertificatesBundleS3Key"] = ca_certificates_bundle_s3_key
    if ca_certificates_bundle_s3_object_version is not None:
        kwargs["CaCertificatesBundleS3ObjectVersion"] = ca_certificates_bundle_s3_object_version
    try:
        resp = await client.call("ModifyTrustStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify trust store") from exc
    return ModifyTrustStoreResult(
        trust_stores=resp.get("TrustStores"),
    )


async def remove_listener_certificates(
    listener_arn: str,
    certificates: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Remove listener certificates.

    Args:
        listener_arn: Listener arn.
        certificates: Certificates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ListenerArn"] = listener_arn
    kwargs["Certificates"] = certificates
    try:
        await client.call("RemoveListenerCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove listener certificates") from exc
    return None


async def remove_trust_store_revocations(
    trust_store_arn: str,
    revocation_ids: list[int],
    region_name: str | None = None,
) -> None:
    """Remove trust store revocations.

    Args:
        trust_store_arn: Trust store arn.
        revocation_ids: Revocation ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustStoreArn"] = trust_store_arn
    kwargs["RevocationIds"] = revocation_ids
    try:
        await client.call("RemoveTrustStoreRevocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove trust store revocations") from exc
    return None


async def set_ip_address_type(
    load_balancer_arn: str,
    ip_address_type: str,
    region_name: str | None = None,
) -> SetIpAddressTypeResult:
    """Set ip address type.

    Args:
        load_balancer_arn: Load balancer arn.
        ip_address_type: Ip address type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LoadBalancerArn"] = load_balancer_arn
    kwargs["IpAddressType"] = ip_address_type
    try:
        resp = await client.call("SetIpAddressType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set ip address type") from exc
    return SetIpAddressTypeResult(
        ip_address_type=resp.get("IpAddressType"),
    )


async def set_rule_priorities(
    rule_priorities: list[dict[str, Any]],
    region_name: str | None = None,
) -> SetRulePrioritiesResult:
    """Set rule priorities.

    Args:
        rule_priorities: Rule priorities.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("elbv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RulePriorities"] = rule_priorities
    try:
        resp = await client.call("SetRulePriorities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set rule priorities") from exc
    return SetRulePrioritiesResult(
        rules=resp.get("Rules"),
    )
