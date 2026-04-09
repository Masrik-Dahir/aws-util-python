"""aws_util.autoscaling — EC2 Auto Scaling utilities.

Provides high-level helpers for managing Auto Scaling groups, launch
configurations, scaling policies, lifecycle hooks, and scaling activities.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "AutoScalingGroupResult",
    "BatchDeleteScheduledActionResult",
    "BatchPutScheduledUpdateGroupActionResult",
    "CancelInstanceRefreshResult",
    "DescribeAccountLimitsResult",
    "DescribeAdjustmentTypesResult",
    "DescribeAutoScalingNotificationTypesResult",
    "DescribeInstanceRefreshesResult",
    "DescribeLifecycleHookTypesResult",
    "DescribeLoadBalancerTargetGroupsResult",
    "DescribeLoadBalancersResult",
    "DescribeMetricCollectionTypesResult",
    "DescribeNotificationConfigurationsResult",
    "DescribePoliciesResult",
    "DescribeScalingProcessTypesResult",
    "DescribeScheduledActionsResult",
    "DescribeTagsResult",
    "DescribeTerminationPolicyTypesResult",
    "DescribeTrafficSourcesResult",
    "DescribeWarmPoolResult",
    "DetachInstancesResult",
    "EnterStandbyResult",
    "ExitStandbyResult",
    "GetPredictiveScalingForecastResult",
    "LaunchConfigurationResult",
    "LifecycleHookResult",
    "RollbackInstanceRefreshResult",
    "ScalingActivityResult",
    "ScalingPolicyResult",
    "StartInstanceRefreshResult",
    "attach_instances",
    "attach_load_balancer_target_groups",
    "attach_load_balancers",
    "attach_traffic_sources",
    "batch_delete_scheduled_action",
    "batch_put_scheduled_update_group_action",
    "cancel_instance_refresh",
    "complete_lifecycle_action",
    "create_auto_scaling_group",
    "create_launch_configuration",
    "create_or_update_tags",
    "delete_auto_scaling_group",
    "delete_launch_configuration",
    "delete_lifecycle_hook",
    "delete_notification_configuration",
    "delete_policy",
    "delete_scheduled_action",
    "delete_tags",
    "delete_warm_pool",
    "describe_account_limits",
    "describe_adjustment_types",
    "describe_auto_scaling_groups",
    "describe_auto_scaling_instances",
    "describe_auto_scaling_notification_types",
    "describe_instance_refreshes",
    "describe_launch_configurations",
    "describe_lifecycle_hook_types",
    "describe_lifecycle_hooks",
    "describe_load_balancer_target_groups",
    "describe_load_balancers",
    "describe_metric_collection_types",
    "describe_notification_configurations",
    "describe_policies",
    "describe_scaling_activities",
    "describe_scaling_policies",
    "describe_scaling_process_types",
    "describe_scheduled_actions",
    "describe_tags",
    "describe_termination_policy_types",
    "describe_traffic_sources",
    "describe_warm_pool",
    "detach_instances",
    "detach_load_balancer_target_groups",
    "detach_load_balancers",
    "detach_traffic_sources",
    "disable_metrics_collection",
    "enable_metrics_collection",
    "enter_standby",
    "execute_policy",
    "exit_standby",
    "get_predictive_scaling_forecast",
    "put_lifecycle_hook",
    "put_notification_configuration",
    "put_scaling_policy",
    "put_scheduled_update_group_action",
    "put_warm_pool",
    "record_lifecycle_action_heartbeat",
    "resume_processes",
    "rollback_instance_refresh",
    "set_desired_capacity",
    "set_instance_health",
    "set_instance_protection",
    "start_instance_refresh",
    "suspend_processes",
    "terminate_instance_in_auto_scaling_group",
    "update_auto_scaling_group",
    "wait_for_group",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AutoScalingGroupResult(BaseModel):
    """Metadata for an Auto Scaling group."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    launch_config_name: str | None = None
    launch_template: dict[str, Any] | None = None
    min_size: int
    max_size: int
    desired_capacity: int
    availability_zones: list[str]
    status: str | None = None
    instances: list[dict[str, Any]] = []
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class LaunchConfigurationResult(BaseModel):
    """Metadata for a launch configuration."""

    model_config = ConfigDict(frozen=True)

    name: str
    image_id: str
    instance_type: str
    key_name: str | None = None
    security_groups: list[str] = []
    created_time: str
    extra: dict[str, Any] = {}


class ScalingPolicyResult(BaseModel):
    """Metadata for a scaling policy."""

    model_config = ConfigDict(frozen=True)

    policy_name: str
    policy_arn: str
    policy_type: str
    adjustment_type: str | None = None
    scaling_adjustment: int | None = None
    target_tracking_config: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


class LifecycleHookResult(BaseModel):
    """Metadata for a lifecycle hook."""

    model_config = ConfigDict(frozen=True)

    hook_name: str
    asg_name: str
    lifecycle_transition: str
    heartbeat_timeout: int | None = None
    default_result: str | None = None
    extra: dict[str, Any] = {}


class ScalingActivityResult(BaseModel):
    """Metadata for a scaling activity."""

    model_config = ConfigDict(frozen=True)

    activity_id: str
    asg_name: str
    cause: str
    description: str | None = None
    status_code: str
    start_time: str
    end_time: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_tags(tag_list: list[dict[str, Any]]) -> dict[str, str]:
    """Convert a list of ASG tag dicts to a simple key-value mapping."""
    return {t["Key"]: t["Value"] for t in (tag_list or [])}


def _parse_asg(asg: dict[str, Any]) -> AutoScalingGroupResult:
    """Parse a raw ASG description into an :class:`AutoScalingGroupResult`."""
    lt = asg.get("LaunchTemplate")
    if lt:
        lt = dict(lt)
    return AutoScalingGroupResult(
        name=asg["AutoScalingGroupName"],
        arn=asg["AutoScalingGroupARN"],
        launch_config_name=asg.get("LaunchConfigurationName") or None,
        launch_template=lt,
        min_size=asg["MinSize"],
        max_size=asg["MaxSize"],
        desired_capacity=asg["DesiredCapacity"],
        availability_zones=asg.get("AvailabilityZones", []),
        status=asg.get("Status") or None,
        instances=[dict(i) for i in asg.get("Instances", [])],
        tags=_parse_tags(asg.get("Tags", [])),
        extra={
            k: v
            for k, v in asg.items()
            if k
            not in {
                "AutoScalingGroupName",
                "AutoScalingGroupARN",
                "LaunchConfigurationName",
                "LaunchTemplate",
                "MinSize",
                "MaxSize",
                "DesiredCapacity",
                "AvailabilityZones",
                "Status",
                "Instances",
                "Tags",
            }
        },
    )


def _parse_launch_config(
    lc: dict[str, Any],
) -> LaunchConfigurationResult:
    """Parse a raw launch configuration into a result model."""
    return LaunchConfigurationResult(
        name=lc["LaunchConfigurationName"],
        image_id=lc["ImageId"],
        instance_type=lc["InstanceType"],
        key_name=lc.get("KeyName") or None,
        security_groups=lc.get("SecurityGroups", []),
        created_time=str(lc["CreatedTime"]),
        extra={
            k: v
            for k, v in lc.items()
            if k
            not in {
                "LaunchConfigurationName",
                "ImageId",
                "InstanceType",
                "KeyName",
                "SecurityGroups",
                "CreatedTime",
            }
        },
    )


def _parse_scaling_policy(
    pol: dict[str, Any],
) -> ScalingPolicyResult:
    """Parse a raw scaling policy into a result model."""
    ttc = pol.get("TargetTrackingConfiguration")
    if ttc:
        ttc = dict(ttc)
    return ScalingPolicyResult(
        policy_name=pol["PolicyName"],
        policy_arn=pol["PolicyARN"],
        policy_type=pol["PolicyType"],
        adjustment_type=pol.get("AdjustmentType") or None,
        scaling_adjustment=pol.get("ScalingAdjustment"),
        target_tracking_config=ttc,
        extra={
            k: v
            for k, v in pol.items()
            if k
            not in {
                "PolicyName",
                "PolicyARN",
                "PolicyType",
                "AdjustmentType",
                "ScalingAdjustment",
                "TargetTrackingConfiguration",
            }
        },
    )


def _parse_lifecycle_hook(
    hook: dict[str, Any],
) -> LifecycleHookResult:
    """Parse a raw lifecycle hook into a result model."""
    return LifecycleHookResult(
        hook_name=hook["LifecycleHookName"],
        asg_name=hook["AutoScalingGroupName"],
        lifecycle_transition=hook["LifecycleTransition"],
        heartbeat_timeout=hook.get("HeartbeatTimeout"),
        default_result=hook.get("DefaultResult") or None,
        extra={
            k: v
            for k, v in hook.items()
            if k
            not in {
                "LifecycleHookName",
                "AutoScalingGroupName",
                "LifecycleTransition",
                "HeartbeatTimeout",
                "DefaultResult",
            }
        },
    )


def _parse_scaling_activity(
    act: dict[str, Any],
) -> ScalingActivityResult:
    """Parse a raw scaling activity into a result model."""
    return ScalingActivityResult(
        activity_id=act["ActivityId"],
        asg_name=act["AutoScalingGroupName"],
        cause=act.get("Cause", ""),
        description=act.get("Description") or None,
        status_code=act["StatusCode"],
        start_time=str(act["StartTime"]),
        end_time=str(act["EndTime"]) if act.get("EndTime") else None,
        extra={
            k: v
            for k, v in act.items()
            if k
            not in {
                "ActivityId",
                "AutoScalingGroupName",
                "Cause",
                "Description",
                "StatusCode",
                "StartTime",
                "EndTime",
            }
        },
    )


# ---------------------------------------------------------------------------
# Launch configuration operations
# ---------------------------------------------------------------------------


def create_launch_configuration(
    name: str,
    *,
    image_id: str,
    instance_type: str,
    key_name: str | None = None,
    security_groups: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Create a launch configuration.

    Args:
        name: Launch configuration name.
        image_id: AMI ID.
        instance_type: EC2 instance type.
        key_name: Optional SSH key pair name.
        security_groups: Optional list of security group IDs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {
        "LaunchConfigurationName": name,
        "ImageId": image_id,
        "InstanceType": instance_type,
    }
    if key_name is not None:
        kwargs["KeyName"] = key_name
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    try:
        client.create_launch_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create launch configuration {name!r}") from exc


def describe_launch_configurations(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[LaunchConfigurationResult]:
    """Describe one or more launch configurations.

    Args:
        names: Specific launch configuration names to describe.
        region_name: AWS region override.

    Returns:
        A list of :class:`LaunchConfigurationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["LaunchConfigurationNames"] = names
    try:
        resp = client.describe_launch_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_launch_configurations failed") from exc
    return [_parse_launch_config(lc) for lc in resp.get("LaunchConfigurations", [])]


def delete_launch_configuration(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a launch configuration.

    Args:
        name: Launch configuration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.delete_launch_configuration(LaunchConfigurationName=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete launch configuration {name!r}") from exc


# ---------------------------------------------------------------------------
# Auto Scaling group operations
# ---------------------------------------------------------------------------


def create_auto_scaling_group(
    name: str,
    *,
    launch_config_name: str | None = None,
    launch_template: dict[str, Any] | None = None,
    min_size: int = 0,
    max_size: int = 1,
    desired_capacity: int | None = None,
    availability_zones: list[str] | None = None,
    vpc_zone_identifier: str | None = None,
    target_group_arns: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> None:
    """Create an Auto Scaling group.

    Args:
        name: Auto Scaling group name.
        launch_config_name: Launch configuration name (mutually exclusive
            with *launch_template*).
        launch_template: Launch template specification dict.
        min_size: Minimum group size.
        max_size: Maximum group size.
        desired_capacity: Desired number of instances.
        availability_zones: AZs for the group.
        vpc_zone_identifier: Comma-separated subnet IDs.
        target_group_arns: ALB/NLB target group ARNs.
        tags: Key-value tags to apply to the group and instances.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingGroupName": name,
        "MinSize": min_size,
        "MaxSize": max_size,
    }
    if launch_config_name is not None:
        kwargs["LaunchConfigurationName"] = launch_config_name
    if launch_template is not None:
        kwargs["LaunchTemplate"] = launch_template
    if desired_capacity is not None:
        kwargs["DesiredCapacity"] = desired_capacity
    if availability_zones is not None:
        kwargs["AvailabilityZones"] = availability_zones
    if vpc_zone_identifier is not None:
        kwargs["VPCZoneIdentifier"] = vpc_zone_identifier
    if target_group_arns is not None:
        kwargs["TargetGroupARNs"] = target_group_arns
    if tags is not None:
        kwargs["Tags"] = [
            {
                "Key": k,
                "Value": v,
                "PropagateAtLaunch": True,
            }
            for k, v in tags.items()
        ]
    try:
        client.create_auto_scaling_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create Auto Scaling group {name!r}") from exc


def describe_auto_scaling_groups(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[AutoScalingGroupResult]:
    """Describe one or more Auto Scaling groups.

    Args:
        names: Specific group names to describe.  ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`AutoScalingGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["AutoScalingGroupNames"] = names
    try:
        groups: list[AutoScalingGroupResult] = []
        paginator = client.get_paginator("describe_auto_scaling_groups")
        for page in paginator.paginate(**kwargs):
            for asg in page.get("AutoScalingGroups", []):
                groups.append(_parse_asg(asg))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_auto_scaling_groups failed") from exc
    return groups


def update_auto_scaling_group(
    name: str,
    *,
    min_size: int | None = None,
    max_size: int | None = None,
    desired_capacity: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update an Auto Scaling group's size parameters.

    Args:
        name: Auto Scaling group name.
        min_size: New minimum group size.
        max_size: New maximum group size.
        desired_capacity: New desired capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": name}
    if min_size is not None:
        kwargs["MinSize"] = min_size
    if max_size is not None:
        kwargs["MaxSize"] = max_size
    if desired_capacity is not None:
        kwargs["DesiredCapacity"] = desired_capacity
    try:
        client.update_auto_scaling_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update Auto Scaling group {name!r}") from exc


def delete_auto_scaling_group(
    name: str,
    *,
    force_delete: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete an Auto Scaling group.

    Args:
        name: Auto Scaling group name.
        force_delete: If ``True``, terminate all instances before deleting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.delete_auto_scaling_group(
            AutoScalingGroupName=name,
            ForceDelete=force_delete,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete Auto Scaling group {name!r}") from exc


def set_desired_capacity(
    name: str,
    *,
    desired_capacity: int,
    region_name: str | None = None,
) -> None:
    """Set the desired capacity for an Auto Scaling group.

    Args:
        name: Auto Scaling group name.
        desired_capacity: The new desired number of instances.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.set_desired_capacity(
            AutoScalingGroupName=name,
            DesiredCapacity=desired_capacity,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to set desired capacity for {name!r}") from exc


# ---------------------------------------------------------------------------
# Scaling policy operations
# ---------------------------------------------------------------------------


def put_scaling_policy(
    asg_name: str,
    policy_name: str,
    *,
    policy_type: str = "TargetTrackingScaling",
    target_tracking_config: dict[str, Any] | None = None,
    adjustment_type: str | None = None,
    scaling_adjustment: int | None = None,
    region_name: str | None = None,
) -> ScalingPolicyResult:
    """Create or update a scaling policy.

    Args:
        asg_name: Auto Scaling group name.
        policy_name: Scaling policy name.
        policy_type: Policy type (default ``"TargetTrackingScaling"``).
        target_tracking_config: Target tracking configuration dict.
        adjustment_type: Adjustment type for simple/step policies.
        scaling_adjustment: Scaling adjustment value.
        region_name: AWS region override.

    Returns:
        A :class:`ScalingPolicyResult` with the policy ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingGroupName": asg_name,
        "PolicyName": policy_name,
        "PolicyType": policy_type,
    }
    if target_tracking_config is not None:
        kwargs["TargetTrackingConfiguration"] = target_tracking_config
    if adjustment_type is not None:
        kwargs["AdjustmentType"] = adjustment_type
    if scaling_adjustment is not None:
        kwargs["ScalingAdjustment"] = scaling_adjustment
    try:
        resp = client.put_scaling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to put scaling policy {policy_name!r}") from exc
    policy_arn = resp.get("PolicyARN", "")
    return ScalingPolicyResult(
        policy_name=policy_name,
        policy_arn=policy_arn,
        policy_type=policy_type,
        adjustment_type=adjustment_type,
        scaling_adjustment=scaling_adjustment,
        target_tracking_config=target_tracking_config,
    )


def describe_scaling_policies(
    asg_name: str,
    *,
    policy_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[ScalingPolicyResult]:
    """Describe scaling policies for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        policy_names: Specific policy names to describe.
        region_name: AWS region override.

    Returns:
        A list of :class:`ScalingPolicyResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if policy_names:
        kwargs["PolicyNames"] = policy_names
    try:
        resp = client.describe_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_scaling_policies failed") from exc
    return [_parse_scaling_policy(pol) for pol in resp.get("ScalingPolicies", [])]


def delete_policy(
    asg_name: str,
    policy_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a scaling policy.

    Args:
        asg_name: Auto Scaling group name.
        policy_name: Scaling policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.delete_policy(
            AutoScalingGroupName=asg_name,
            PolicyName=policy_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete policy {policy_name!r}") from exc


# ---------------------------------------------------------------------------
# Load balancer target group operations
# ---------------------------------------------------------------------------


def attach_load_balancer_target_groups(
    asg_name: str,
    *,
    target_group_arns: list[str],
    region_name: str | None = None,
) -> None:
    """Attach ALB/NLB target groups to an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        target_group_arns: Target group ARNs to attach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.attach_load_balancer_target_groups(
            AutoScalingGroupName=asg_name,
            TargetGroupARNs=target_group_arns,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to attach target groups to {asg_name!r}",
        ) from exc


def detach_load_balancer_target_groups(
    asg_name: str,
    *,
    target_group_arns: list[str],
    region_name: str | None = None,
) -> None:
    """Detach ALB/NLB target groups from an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        target_group_arns: Target group ARNs to detach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        client.detach_load_balancer_target_groups(
            AutoScalingGroupName=asg_name,
            TargetGroupARNs=target_group_arns,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to detach target groups from {asg_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


def describe_auto_scaling_instances(
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Describe Auto Scaling instances.

    Args:
        instance_ids: Specific instance IDs to describe.
        region_name: AWS region override.

    Returns:
        A list of instance description dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if instance_ids:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = client.describe_auto_scaling_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_auto_scaling_instances failed") from exc
    return resp.get("AutoScalingInstances", [])


def terminate_instance_in_auto_scaling_group(
    instance_id: str,
    *,
    should_decrement: bool = True,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Terminate an instance in an Auto Scaling group.

    Args:
        instance_id: EC2 instance ID.
        should_decrement: Whether to decrement the desired capacity.
        region_name: AWS region override.

    Returns:
        The termination activity dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        resp = client.terminate_instance_in_auto_scaling_group(
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=should_decrement,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to terminate instance {instance_id!r} in ASG",
        ) from exc
    return resp.get("Activity", {})


# ---------------------------------------------------------------------------
# Lifecycle hook operations
# ---------------------------------------------------------------------------


def put_lifecycle_hook(
    asg_name: str,
    hook_name: str,
    *,
    lifecycle_transition: str,
    heartbeat_timeout: int | None = None,
    default_result: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create or update a lifecycle hook on an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        hook_name: Lifecycle hook name.
        lifecycle_transition: The instance state transition, e.g.
            ``"autoscaling:EC2_INSTANCE_LAUNCHING"``.
        heartbeat_timeout: Seconds before the hook times out.
        default_result: Default action (``"CONTINUE"`` or ``"ABANDON"``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingGroupName": asg_name,
        "LifecycleHookName": hook_name,
        "LifecycleTransition": lifecycle_transition,
    }
    if heartbeat_timeout is not None:
        kwargs["HeartbeatTimeout"] = heartbeat_timeout
    if default_result is not None:
        kwargs["DefaultResult"] = default_result
    try:
        client.put_lifecycle_hook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to put lifecycle hook {hook_name!r}") from exc


def describe_lifecycle_hooks(
    asg_name: str,
    *,
    hook_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[LifecycleHookResult]:
    """Describe lifecycle hooks for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        hook_names: Specific hook names to describe.
        region_name: AWS region override.

    Returns:
        A list of :class:`LifecycleHookResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if hook_names:
        kwargs["LifecycleHookNames"] = hook_names
    try:
        resp = client.describe_lifecycle_hooks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_lifecycle_hooks failed") from exc
    return [_parse_lifecycle_hook(hook) for hook in resp.get("LifecycleHooks", [])]


def complete_lifecycle_action(
    asg_name: str,
    hook_name: str,
    *,
    lifecycle_action_result: str,
    instance_id: str | None = None,
    lifecycle_action_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Complete a lifecycle action for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        hook_name: Lifecycle hook name.
        lifecycle_action_result: ``"CONTINUE"`` or ``"ABANDON"``.
        instance_id: The EC2 instance ID.
        lifecycle_action_token: Lifecycle action token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingGroupName": asg_name,
        "LifecycleHookName": hook_name,
        "LifecycleActionResult": lifecycle_action_result,
    }
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if lifecycle_action_token is not None:
        kwargs["LifecycleActionToken"] = lifecycle_action_token
    try:
        client.complete_lifecycle_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to complete lifecycle action for {hook_name!r}") from exc


# ---------------------------------------------------------------------------
# Scaling activity operations
# ---------------------------------------------------------------------------


def describe_scaling_activities(
    asg_name: str,
    *,
    region_name: str | None = None,
) -> list[ScalingActivityResult]:
    """Describe scaling activities for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        region_name: AWS region override.

    Returns:
        A list of :class:`ScalingActivityResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    try:
        resp = client.describe_scaling_activities(
            AutoScalingGroupName=asg_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_scaling_activities failed") from exc
    return [_parse_scaling_activity(act) for act in resp.get("Activities", [])]


# ---------------------------------------------------------------------------
# Process suspension / resumption
# ---------------------------------------------------------------------------


def suspend_processes(
    asg_name: str,
    *,
    scaling_processes: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Suspend scaling processes for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        scaling_processes: Specific processes to suspend (e.g.
            ``["Launch", "Terminate"]``).  ``None`` suspends all.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if scaling_processes is not None:
        kwargs["ScalingProcesses"] = scaling_processes
    try:
        client.suspend_processes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to suspend processes for {asg_name!r}") from exc


def resume_processes(
    asg_name: str,
    *,
    scaling_processes: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Resume scaling processes for an Auto Scaling group.

    Args:
        asg_name: Auto Scaling group name.
        scaling_processes: Specific processes to resume.  ``None`` resumes all.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if scaling_processes is not None:
        kwargs["ScalingProcesses"] = scaling_processes
    try:
        client.resume_processes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to resume processes for {asg_name!r}") from exc


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


def wait_for_group(
    name: str,
    *,
    timeout: float = 300,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> AutoScalingGroupResult:
    """Poll until all instances in an Auto Scaling group are ``InService``.

    Args:
        name: Auto Scaling group name.
        timeout: Maximum seconds to wait (default ``300``).
        poll_interval: Seconds between polls (default ``15``).
        region_name: AWS region override.

    Returns:
        The :class:`AutoScalingGroupResult` once all instances are InService.

    Raises:
        AwsTimeoutError: If the group does not stabilise within *timeout*.
        RuntimeError: If the group is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        groups = describe_auto_scaling_groups(names=[name], region_name=region_name)
        if not groups:
            raise AwsServiceError(f"Auto Scaling group {name!r} not found")
        group = groups[0]
        if (
            group.desired_capacity == 0
            or all(inst.get("LifecycleState") == "InService" for inst in group.instances)
        ) and len(group.instances) >= group.desired_capacity:
            return group
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Auto Scaling group {name!r} did not stabilise within {timeout}s"
            )
        time.sleep(poll_interval)


class BatchDeleteScheduledActionResult(BaseModel):
    """Result of batch_delete_scheduled_action."""

    model_config = ConfigDict(frozen=True)

    failed_scheduled_actions: list[dict[str, Any]] | None = None


class BatchPutScheduledUpdateGroupActionResult(BaseModel):
    """Result of batch_put_scheduled_update_group_action."""

    model_config = ConfigDict(frozen=True)

    failed_scheduled_update_group_actions: list[dict[str, Any]] | None = None


class CancelInstanceRefreshResult(BaseModel):
    """Result of cancel_instance_refresh."""

    model_config = ConfigDict(frozen=True)

    instance_refresh_id: str | None = None


class DescribeAccountLimitsResult(BaseModel):
    """Result of describe_account_limits."""

    model_config = ConfigDict(frozen=True)

    max_number_of_auto_scaling_groups: int | None = None
    max_number_of_launch_configurations: int | None = None
    number_of_auto_scaling_groups: int | None = None
    number_of_launch_configurations: int | None = None


class DescribeAdjustmentTypesResult(BaseModel):
    """Result of describe_adjustment_types."""

    model_config = ConfigDict(frozen=True)

    adjustment_types: list[dict[str, Any]] | None = None


class DescribeAutoScalingNotificationTypesResult(BaseModel):
    """Result of describe_auto_scaling_notification_types."""

    model_config = ConfigDict(frozen=True)

    auto_scaling_notification_types: list[str] | None = None


class DescribeInstanceRefreshesResult(BaseModel):
    """Result of describe_instance_refreshes."""

    model_config = ConfigDict(frozen=True)

    instance_refreshes: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeLifecycleHookTypesResult(BaseModel):
    """Result of describe_lifecycle_hook_types."""

    model_config = ConfigDict(frozen=True)

    lifecycle_hook_types: list[str] | None = None


class DescribeLoadBalancerTargetGroupsResult(BaseModel):
    """Result of describe_load_balancer_target_groups."""

    model_config = ConfigDict(frozen=True)

    load_balancer_target_groups: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeLoadBalancersResult(BaseModel):
    """Result of describe_load_balancers."""

    model_config = ConfigDict(frozen=True)

    load_balancers: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeMetricCollectionTypesResult(BaseModel):
    """Result of describe_metric_collection_types."""

    model_config = ConfigDict(frozen=True)

    metrics: list[dict[str, Any]] | None = None
    granularities: list[dict[str, Any]] | None = None


class DescribeNotificationConfigurationsResult(BaseModel):
    """Result of describe_notification_configurations."""

    model_config = ConfigDict(frozen=True)

    notification_configurations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribePoliciesResult(BaseModel):
    """Result of describe_policies."""

    model_config = ConfigDict(frozen=True)

    scaling_policies: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeScalingProcessTypesResult(BaseModel):
    """Result of describe_scaling_process_types."""

    model_config = ConfigDict(frozen=True)

    processes: list[dict[str, Any]] | None = None


class DescribeScheduledActionsResult(BaseModel):
    """Result of describe_scheduled_actions."""

    model_config = ConfigDict(frozen=True)

    scheduled_update_group_actions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeTagsResult(BaseModel):
    """Result of describe_tags."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeTerminationPolicyTypesResult(BaseModel):
    """Result of describe_termination_policy_types."""

    model_config = ConfigDict(frozen=True)

    termination_policy_types: list[str] | None = None


class DescribeTrafficSourcesResult(BaseModel):
    """Result of describe_traffic_sources."""

    model_config = ConfigDict(frozen=True)

    traffic_sources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeWarmPoolResult(BaseModel):
    """Result of describe_warm_pool."""

    model_config = ConfigDict(frozen=True)

    warm_pool_configuration: dict[str, Any] | None = None
    instances: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DetachInstancesResult(BaseModel):
    """Result of detach_instances."""

    model_config = ConfigDict(frozen=True)

    activities: list[dict[str, Any]] | None = None


class EnterStandbyResult(BaseModel):
    """Result of enter_standby."""

    model_config = ConfigDict(frozen=True)

    activities: list[dict[str, Any]] | None = None


class ExitStandbyResult(BaseModel):
    """Result of exit_standby."""

    model_config = ConfigDict(frozen=True)

    activities: list[dict[str, Any]] | None = None


class GetPredictiveScalingForecastResult(BaseModel):
    """Result of get_predictive_scaling_forecast."""

    model_config = ConfigDict(frozen=True)

    load_forecast: list[dict[str, Any]] | None = None
    capacity_forecast: dict[str, Any] | None = None
    update_time: str | None = None


class RollbackInstanceRefreshResult(BaseModel):
    """Result of rollback_instance_refresh."""

    model_config = ConfigDict(frozen=True)

    instance_refresh_id: str | None = None


class StartInstanceRefreshResult(BaseModel):
    """Result of start_instance_refresh."""

    model_config = ConfigDict(frozen=True)

    instance_refresh_id: str | None = None


def attach_instances(
    auto_scaling_group_name: str,
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Attach instances.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        client.attach_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to attach instances") from exc
    return None


def attach_load_balancers(
    auto_scaling_group_name: str,
    load_balancer_names: list[str],
    region_name: str | None = None,
) -> None:
    """Attach load balancers.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        load_balancer_names: Load balancer names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["LoadBalancerNames"] = load_balancer_names
    try:
        client.attach_load_balancers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to attach load balancers") from exc
    return None


def attach_traffic_sources(
    auto_scaling_group_name: str,
    traffic_sources: list[dict[str, Any]],
    *,
    skip_zonal_shift_validation: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Attach traffic sources.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        traffic_sources: Traffic sources.
        skip_zonal_shift_validation: Skip zonal shift validation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TrafficSources"] = traffic_sources
    if skip_zonal_shift_validation is not None:
        kwargs["SkipZonalShiftValidation"] = skip_zonal_shift_validation
    try:
        client.attach_traffic_sources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to attach traffic sources") from exc
    return None


def batch_delete_scheduled_action(
    auto_scaling_group_name: str,
    scheduled_action_names: list[str],
    region_name: str | None = None,
) -> BatchDeleteScheduledActionResult:
    """Batch delete scheduled action.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        scheduled_action_names: Scheduled action names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledActionNames"] = scheduled_action_names
    try:
        resp = client.batch_delete_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete scheduled action") from exc
    return BatchDeleteScheduledActionResult(
        failed_scheduled_actions=resp.get("FailedScheduledActions"),
    )


def batch_put_scheduled_update_group_action(
    auto_scaling_group_name: str,
    scheduled_update_group_actions: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchPutScheduledUpdateGroupActionResult:
    """Batch put scheduled update group action.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        scheduled_update_group_actions: Scheduled update group actions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledUpdateGroupActions"] = scheduled_update_group_actions
    try:
        resp = client.batch_put_scheduled_update_group_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch put scheduled update group action") from exc
    return BatchPutScheduledUpdateGroupActionResult(
        failed_scheduled_update_group_actions=resp.get("FailedScheduledUpdateGroupActions"),
    )


def cancel_instance_refresh(
    auto_scaling_group_name: str,
    *,
    wait_for_transitioning_instances: bool | None = None,
    region_name: str | None = None,
) -> CancelInstanceRefreshResult:
    """Cancel instance refresh.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        wait_for_transitioning_instances: Wait for transitioning instances.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if wait_for_transitioning_instances is not None:
        kwargs["WaitForTransitioningInstances"] = wait_for_transitioning_instances
    try:
        resp = client.cancel_instance_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel instance refresh") from exc
    return CancelInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )


def create_or_update_tags(
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Create or update tags.

    Args:
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    try:
        client.create_or_update_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create or update tags") from exc
    return None


def delete_lifecycle_hook(
    lifecycle_hook_name: str,
    auto_scaling_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete lifecycle hook.

    Args:
        lifecycle_hook_name: Lifecycle hook name.
        auto_scaling_group_name: Auto scaling group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LifecycleHookName"] = lifecycle_hook_name
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    try:
        client.delete_lifecycle_hook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete lifecycle hook") from exc
    return None


def delete_notification_configuration(
    auto_scaling_group_name: str,
    topic_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete notification configuration.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        topic_arn: Topic arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TopicARN"] = topic_arn
    try:
        client.delete_notification_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete notification configuration") from exc
    return None


def delete_scheduled_action(
    auto_scaling_group_name: str,
    scheduled_action_name: str,
    region_name: str | None = None,
) -> None:
    """Delete scheduled action.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        scheduled_action_name: Scheduled action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledActionName"] = scheduled_action_name
    try:
        client.delete_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduled action") from exc
    return None


def delete_tags(
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Delete tags.

    Args:
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    try:
        client.delete_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete tags") from exc
    return None


def delete_warm_pool(
    auto_scaling_group_name: str,
    *,
    force_delete: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete warm pool.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        force_delete: Force delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if force_delete is not None:
        kwargs["ForceDelete"] = force_delete
    try:
        client.delete_warm_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete warm pool") from exc
    return None


def describe_account_limits(
    region_name: str | None = None,
) -> DescribeAccountLimitsResult:
    """Describe account limits.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_account_limits(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account limits") from exc
    return DescribeAccountLimitsResult(
        max_number_of_auto_scaling_groups=resp.get("MaxNumberOfAutoScalingGroups"),
        max_number_of_launch_configurations=resp.get("MaxNumberOfLaunchConfigurations"),
        number_of_auto_scaling_groups=resp.get("NumberOfAutoScalingGroups"),
        number_of_launch_configurations=resp.get("NumberOfLaunchConfigurations"),
    )


def describe_adjustment_types(
    region_name: str | None = None,
) -> DescribeAdjustmentTypesResult:
    """Describe adjustment types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_adjustment_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe adjustment types") from exc
    return DescribeAdjustmentTypesResult(
        adjustment_types=resp.get("AdjustmentTypes"),
    )


def describe_auto_scaling_notification_types(
    region_name: str | None = None,
) -> DescribeAutoScalingNotificationTypesResult:
    """Describe auto scaling notification types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_auto_scaling_notification_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe auto scaling notification types") from exc
    return DescribeAutoScalingNotificationTypesResult(
        auto_scaling_notification_types=resp.get("AutoScalingNotificationTypes"),
    )


def describe_instance_refreshes(
    auto_scaling_group_name: str,
    *,
    instance_refresh_ids: list[str] | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeInstanceRefreshesResult:
    """Describe instance refreshes.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        instance_refresh_ids: Instance refresh ids.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_refresh_ids is not None:
        kwargs["InstanceRefreshIds"] = instance_refresh_ids
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_instance_refreshes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe instance refreshes") from exc
    return DescribeInstanceRefreshesResult(
        instance_refreshes=resp.get("InstanceRefreshes"),
        next_token=resp.get("NextToken"),
    )


def describe_lifecycle_hook_types(
    region_name: str | None = None,
) -> DescribeLifecycleHookTypesResult:
    """Describe lifecycle hook types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_lifecycle_hook_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe lifecycle hook types") from exc
    return DescribeLifecycleHookTypesResult(
        lifecycle_hook_types=resp.get("LifecycleHookTypes"),
    )


def describe_load_balancer_target_groups(
    auto_scaling_group_name: str,
    *,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeLoadBalancerTargetGroupsResult:
    """Describe load balancer target groups.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_load_balancer_target_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe load balancer target groups") from exc
    return DescribeLoadBalancerTargetGroupsResult(
        load_balancer_target_groups=resp.get("LoadBalancerTargetGroups"),
        next_token=resp.get("NextToken"),
    )


def describe_load_balancers(
    auto_scaling_group_name: str,
    *,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeLoadBalancersResult:
    """Describe load balancers.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_load_balancers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe load balancers") from exc
    return DescribeLoadBalancersResult(
        load_balancers=resp.get("LoadBalancers"),
        next_token=resp.get("NextToken"),
    )


def describe_metric_collection_types(
    region_name: str | None = None,
) -> DescribeMetricCollectionTypesResult:
    """Describe metric collection types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_metric_collection_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe metric collection types") from exc
    return DescribeMetricCollectionTypesResult(
        metrics=resp.get("Metrics"),
        granularities=resp.get("Granularities"),
    )


def describe_notification_configurations(
    *,
    auto_scaling_group_names: list[str] | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeNotificationConfigurationsResult:
    """Describe notification configurations.

    Args:
        auto_scaling_group_names: Auto scaling group names.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if auto_scaling_group_names is not None:
        kwargs["AutoScalingGroupNames"] = auto_scaling_group_names
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_notification_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe notification configurations") from exc
    return DescribeNotificationConfigurationsResult(
        notification_configurations=resp.get("NotificationConfigurations"),
        next_token=resp.get("NextToken"),
    )


def describe_policies(
    *,
    auto_scaling_group_name: str | None = None,
    policy_names: list[str] | None = None,
    policy_types: list[str] | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribePoliciesResult:
    """Describe policies.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        policy_names: Policy names.
        policy_types: Policy types.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if auto_scaling_group_name is not None:
        kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if policy_names is not None:
        kwargs["PolicyNames"] = policy_names
    if policy_types is not None:
        kwargs["PolicyTypes"] = policy_types
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe policies") from exc
    return DescribePoliciesResult(
        scaling_policies=resp.get("ScalingPolicies"),
        next_token=resp.get("NextToken"),
    )


def describe_scaling_process_types(
    region_name: str | None = None,
) -> DescribeScalingProcessTypesResult:
    """Describe scaling process types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_scaling_process_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe scaling process types") from exc
    return DescribeScalingProcessTypesResult(
        processes=resp.get("Processes"),
    )


def describe_scheduled_actions(
    *,
    auto_scaling_group_name: str | None = None,
    scheduled_action_names: list[str] | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeScheduledActionsResult:
    """Describe scheduled actions.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        scheduled_action_names: Scheduled action names.
        start_time: Start time.
        end_time: End time.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if auto_scaling_group_name is not None:
        kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if scheduled_action_names is not None:
        kwargs["ScheduledActionNames"] = scheduled_action_names
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_scheduled_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduled actions") from exc
    return DescribeScheduledActionsResult(
        scheduled_update_group_actions=resp.get("ScheduledUpdateGroupActions"),
        next_token=resp.get("NextToken"),
    )


def describe_tags(
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeTagsResult:
    """Describe tags.

    Args:
        filters: Filters.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe tags") from exc
    return DescribeTagsResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def describe_termination_policy_types(
    region_name: str | None = None,
) -> DescribeTerminationPolicyTypesResult:
    """Describe termination policy types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_termination_policy_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe termination policy types") from exc
    return DescribeTerminationPolicyTypesResult(
        termination_policy_types=resp.get("TerminationPolicyTypes"),
    )


def describe_traffic_sources(
    auto_scaling_group_name: str,
    *,
    traffic_source_type: str | None = None,
    next_token: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeTrafficSourcesResult:
    """Describe traffic sources.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        traffic_source_type: Traffic source type.
        next_token: Next token.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if traffic_source_type is not None:
        kwargs["TrafficSourceType"] = traffic_source_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_traffic_sources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe traffic sources") from exc
    return DescribeTrafficSourcesResult(
        traffic_sources=resp.get("TrafficSources"),
        next_token=resp.get("NextToken"),
    )


def describe_warm_pool(
    auto_scaling_group_name: str,
    *,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeWarmPoolResult:
    """Describe warm pool.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_warm_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe warm pool") from exc
    return DescribeWarmPoolResult(
        warm_pool_configuration=resp.get("WarmPoolConfiguration"),
        instances=resp.get("Instances"),
        next_token=resp.get("NextToken"),
    )


def detach_instances(
    auto_scaling_group_name: str,
    should_decrement_desired_capacity: bool,
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> DetachInstancesResult:
    """Detach instances.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        should_decrement_desired_capacity: Should decrement desired capacity.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ShouldDecrementDesiredCapacity"] = should_decrement_desired_capacity
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = client.detach_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detach instances") from exc
    return DetachInstancesResult(
        activities=resp.get("Activities"),
    )


def detach_load_balancers(
    auto_scaling_group_name: str,
    load_balancer_names: list[str],
    region_name: str | None = None,
) -> None:
    """Detach load balancers.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        load_balancer_names: Load balancer names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["LoadBalancerNames"] = load_balancer_names
    try:
        client.detach_load_balancers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detach load balancers") from exc
    return None


def detach_traffic_sources(
    auto_scaling_group_name: str,
    traffic_sources: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Detach traffic sources.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        traffic_sources: Traffic sources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TrafficSources"] = traffic_sources
    try:
        client.detach_traffic_sources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detach traffic sources") from exc
    return None


def disable_metrics_collection(
    auto_scaling_group_name: str,
    *,
    metrics: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Disable metrics collection.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        metrics: Metrics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if metrics is not None:
        kwargs["Metrics"] = metrics
    try:
        client.disable_metrics_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable metrics collection") from exc
    return None


def enable_metrics_collection(
    auto_scaling_group_name: str,
    granularity: str,
    *,
    metrics: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Enable metrics collection.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        granularity: Granularity.
        metrics: Metrics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["Granularity"] = granularity
    if metrics is not None:
        kwargs["Metrics"] = metrics
    try:
        client.enable_metrics_collection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable metrics collection") from exc
    return None


def enter_standby(
    auto_scaling_group_name: str,
    should_decrement_desired_capacity: bool,
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> EnterStandbyResult:
    """Enter standby.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        should_decrement_desired_capacity: Should decrement desired capacity.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ShouldDecrementDesiredCapacity"] = should_decrement_desired_capacity
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = client.enter_standby(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enter standby") from exc
    return EnterStandbyResult(
        activities=resp.get("Activities"),
    )


def execute_policy(
    policy_name: str,
    *,
    auto_scaling_group_name: str | None = None,
    honor_cooldown: bool | None = None,
    metric_value: float | None = None,
    breach_threshold: float | None = None,
    region_name: str | None = None,
) -> None:
    """Execute policy.

    Args:
        policy_name: Policy name.
        auto_scaling_group_name: Auto scaling group name.
        honor_cooldown: Honor cooldown.
        metric_value: Metric value.
        breach_threshold: Breach threshold.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyName"] = policy_name
    if auto_scaling_group_name is not None:
        kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if honor_cooldown is not None:
        kwargs["HonorCooldown"] = honor_cooldown
    if metric_value is not None:
        kwargs["MetricValue"] = metric_value
    if breach_threshold is not None:
        kwargs["BreachThreshold"] = breach_threshold
    try:
        client.execute_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute policy") from exc
    return None


def exit_standby(
    auto_scaling_group_name: str,
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ExitStandbyResult:
    """Exit standby.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = client.exit_standby(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to exit standby") from exc
    return ExitStandbyResult(
        activities=resp.get("Activities"),
    )


def get_predictive_scaling_forecast(
    auto_scaling_group_name: str,
    policy_name: str,
    start_time: str,
    end_time: str,
    region_name: str | None = None,
) -> GetPredictiveScalingForecastResult:
    """Get predictive scaling forecast.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        policy_name: Policy name.
        start_time: Start time.
        end_time: End time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["PolicyName"] = policy_name
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    try:
        resp = client.get_predictive_scaling_forecast(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get predictive scaling forecast") from exc
    return GetPredictiveScalingForecastResult(
        load_forecast=resp.get("LoadForecast"),
        capacity_forecast=resp.get("CapacityForecast"),
        update_time=resp.get("UpdateTime"),
    )


def put_notification_configuration(
    auto_scaling_group_name: str,
    topic_arn: str,
    notification_types: list[str],
    region_name: str | None = None,
) -> None:
    """Put notification configuration.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        topic_arn: Topic arn.
        notification_types: Notification types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TopicARN"] = topic_arn
    kwargs["NotificationTypes"] = notification_types
    try:
        client.put_notification_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put notification configuration") from exc
    return None


def put_scheduled_update_group_action(
    auto_scaling_group_name: str,
    scheduled_action_name: str,
    *,
    time: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    recurrence: str | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
    desired_capacity: int | None = None,
    time_zone: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put scheduled update group action.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        scheduled_action_name: Scheduled action name.
        time: Time.
        start_time: Start time.
        end_time: End time.
        recurrence: Recurrence.
        min_size: Min size.
        max_size: Max size.
        desired_capacity: Desired capacity.
        time_zone: Time zone.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledActionName"] = scheduled_action_name
    if time is not None:
        kwargs["Time"] = time
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if recurrence is not None:
        kwargs["Recurrence"] = recurrence
    if min_size is not None:
        kwargs["MinSize"] = min_size
    if max_size is not None:
        kwargs["MaxSize"] = max_size
    if desired_capacity is not None:
        kwargs["DesiredCapacity"] = desired_capacity
    if time_zone is not None:
        kwargs["TimeZone"] = time_zone
    try:
        client.put_scheduled_update_group_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put scheduled update group action") from exc
    return None


def put_warm_pool(
    auto_scaling_group_name: str,
    *,
    max_group_prepared_capacity: int | None = None,
    min_size: int | None = None,
    pool_state: str | None = None,
    instance_reuse_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put warm pool.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        max_group_prepared_capacity: Max group prepared capacity.
        min_size: Min size.
        pool_state: Pool state.
        instance_reuse_policy: Instance reuse policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if max_group_prepared_capacity is not None:
        kwargs["MaxGroupPreparedCapacity"] = max_group_prepared_capacity
    if min_size is not None:
        kwargs["MinSize"] = min_size
    if pool_state is not None:
        kwargs["PoolState"] = pool_state
    if instance_reuse_policy is not None:
        kwargs["InstanceReusePolicy"] = instance_reuse_policy
    try:
        client.put_warm_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put warm pool") from exc
    return None


def record_lifecycle_action_heartbeat(
    lifecycle_hook_name: str,
    auto_scaling_group_name: str,
    *,
    lifecycle_action_token: str | None = None,
    instance_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Record lifecycle action heartbeat.

    Args:
        lifecycle_hook_name: Lifecycle hook name.
        auto_scaling_group_name: Auto scaling group name.
        lifecycle_action_token: Lifecycle action token.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LifecycleHookName"] = lifecycle_hook_name
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if lifecycle_action_token is not None:
        kwargs["LifecycleActionToken"] = lifecycle_action_token
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    try:
        client.record_lifecycle_action_heartbeat(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to record lifecycle action heartbeat") from exc
    return None


def rollback_instance_refresh(
    auto_scaling_group_name: str,
    region_name: str | None = None,
) -> RollbackInstanceRefreshResult:
    """Rollback instance refresh.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    try:
        resp = client.rollback_instance_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rollback instance refresh") from exc
    return RollbackInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )


def set_instance_health(
    instance_id: str,
    health_status: str,
    *,
    should_respect_grace_period: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Set instance health.

    Args:
        instance_id: Instance id.
        health_status: Health status.
        should_respect_grace_period: Should respect grace period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HealthStatus"] = health_status
    if should_respect_grace_period is not None:
        kwargs["ShouldRespectGracePeriod"] = should_respect_grace_period
    try:
        client.set_instance_health(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set instance health") from exc
    return None


def set_instance_protection(
    instance_ids: list[str],
    auto_scaling_group_name: str,
    protected_from_scale_in: bool,
    region_name: str | None = None,
) -> None:
    """Set instance protection.

    Args:
        instance_ids: Instance ids.
        auto_scaling_group_name: Auto scaling group name.
        protected_from_scale_in: Protected from scale in.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceIds"] = instance_ids
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ProtectedFromScaleIn"] = protected_from_scale_in
    try:
        client.set_instance_protection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set instance protection") from exc
    return None


def start_instance_refresh(
    auto_scaling_group_name: str,
    *,
    strategy: str | None = None,
    desired_configuration: dict[str, Any] | None = None,
    preferences: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartInstanceRefreshResult:
    """Start instance refresh.

    Args:
        auto_scaling_group_name: Auto scaling group name.
        strategy: Strategy.
        desired_configuration: Desired configuration.
        preferences: Preferences.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if strategy is not None:
        kwargs["Strategy"] = strategy
    if desired_configuration is not None:
        kwargs["DesiredConfiguration"] = desired_configuration
    if preferences is not None:
        kwargs["Preferences"] = preferences
    try:
        resp = client.start_instance_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start instance refresh") from exc
    return StartInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )
