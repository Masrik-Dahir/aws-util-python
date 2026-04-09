"""Native async EC2 Auto Scaling utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.autoscaling import (
    AutoScalingGroupResult,
    BatchDeleteScheduledActionResult,
    BatchPutScheduledUpdateGroupActionResult,
    CancelInstanceRefreshResult,
    DescribeAccountLimitsResult,
    DescribeAdjustmentTypesResult,
    DescribeAutoScalingNotificationTypesResult,
    DescribeInstanceRefreshesResult,
    DescribeLifecycleHookTypesResult,
    DescribeLoadBalancersResult,
    DescribeLoadBalancerTargetGroupsResult,
    DescribeMetricCollectionTypesResult,
    DescribeNotificationConfigurationsResult,
    DescribePoliciesResult,
    DescribeScalingProcessTypesResult,
    DescribeScheduledActionsResult,
    DescribeTagsResult,
    DescribeTerminationPolicyTypesResult,
    DescribeTrafficSourcesResult,
    DescribeWarmPoolResult,
    DetachInstancesResult,
    EnterStandbyResult,
    ExitStandbyResult,
    GetPredictiveScalingForecastResult,
    LaunchConfigurationResult,
    LifecycleHookResult,
    RollbackInstanceRefreshResult,
    ScalingActivityResult,
    ScalingPolicyResult,
    StartInstanceRefreshResult,
    _parse_asg,
    _parse_launch_config,
    _parse_lifecycle_hook,
    _parse_scaling_activity,
    _parse_scaling_policy,
)
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
# Launch configuration operations
# ---------------------------------------------------------------------------


async def create_launch_configuration(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("CreateLaunchConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create launch configuration {name!r}") from exc


async def describe_launch_configurations(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["LaunchConfigurationNames"] = names
    try:
        resp = await client.call("DescribeLaunchConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_launch_configurations failed") from exc
    return [_parse_launch_config(lc) for lc in resp.get("LaunchConfigurations", [])]


async def delete_launch_configuration(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "DeleteLaunchConfiguration",
            LaunchConfigurationName=name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete launch configuration {name!r}") from exc


# ---------------------------------------------------------------------------
# Auto Scaling group operations
# ---------------------------------------------------------------------------


async def create_auto_scaling_group(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("CreateAutoScalingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create Auto Scaling group {name!r}") from exc


async def describe_auto_scaling_groups(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["AutoScalingGroupNames"] = names
    try:
        groups: list[AutoScalingGroupResult] = []
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("DescribeAutoScalingGroups", **kwargs)
            for asg in resp.get("AutoScalingGroups", []):
                groups.append(_parse_asg(asg))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_auto_scaling_groups failed") from exc
    return groups


async def update_auto_scaling_group(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": name}
    if min_size is not None:
        kwargs["MinSize"] = min_size
    if max_size is not None:
        kwargs["MaxSize"] = max_size
    if desired_capacity is not None:
        kwargs["DesiredCapacity"] = desired_capacity
    try:
        await client.call("UpdateAutoScalingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to update Auto Scaling group {name!r}") from exc


async def delete_auto_scaling_group(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "DeleteAutoScalingGroup",
            AutoScalingGroupName=name,
            ForceDelete=force_delete,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete Auto Scaling group {name!r}") from exc


async def set_desired_capacity(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "SetDesiredCapacity",
            AutoScalingGroupName=name,
            DesiredCapacity=desired_capacity,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to set desired capacity for {name!r}") from exc


# ---------------------------------------------------------------------------
# Scaling policy operations
# ---------------------------------------------------------------------------


async def put_scaling_policy(
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
    client = async_client("autoscaling", region_name)
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
        resp = await client.call("PutScalingPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to put scaling policy {policy_name!r}") from exc
    return ScalingPolicyResult(
        policy_name=policy_name,
        policy_arn=resp["PolicyARN"],
        policy_type=policy_type,
        adjustment_type=adjustment_type,
        scaling_adjustment=scaling_adjustment,
        target_tracking_config=target_tracking_config,
    )


async def describe_scaling_policies(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if policy_names:
        kwargs["PolicyNames"] = policy_names
    try:
        resp = await client.call("DescribePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_scaling_policies failed") from exc
    return [_parse_scaling_policy(pol) for pol in resp.get("ScalingPolicies", [])]


async def delete_policy(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "DeletePolicy",
            AutoScalingGroupName=asg_name,
            PolicyName=policy_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete policy {policy_name!r}") from exc


# ---------------------------------------------------------------------------
# Load balancer target group operations
# ---------------------------------------------------------------------------


async def attach_load_balancer_target_groups(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "AttachLoadBalancerTargetGroups",
            AutoScalingGroupName=asg_name,
            TargetGroupARNs=target_group_arns,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to attach target groups to {asg_name!r}",
        ) from exc


async def detach_load_balancer_target_groups(
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
    client = async_client("autoscaling", region_name)
    try:
        await client.call(
            "DetachLoadBalancerTargetGroups",
            AutoScalingGroupName=asg_name,
            TargetGroupARNs=target_group_arns,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to detach target groups from {asg_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


async def describe_auto_scaling_instances(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if instance_ids:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = await client.call("DescribeAutoScalingInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_auto_scaling_instances failed") from exc
    return resp.get("AutoScalingInstances", [])


async def terminate_instance_in_auto_scaling_group(
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
    client = async_client("autoscaling", region_name)
    try:
        resp = await client.call(
            "TerminateInstanceInAutoScalingGroup",
            InstanceId=instance_id,
            ShouldDecrementDesiredCapacity=should_decrement,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to terminate instance {instance_id!r} in ASG",
        ) from exc
    return resp.get("Activity", {})


# ---------------------------------------------------------------------------
# Lifecycle hook operations
# ---------------------------------------------------------------------------


async def put_lifecycle_hook(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("PutLifecycleHook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to put lifecycle hook {hook_name!r}") from exc


async def describe_lifecycle_hooks(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if hook_names:
        kwargs["LifecycleHookNames"] = hook_names
    try:
        resp = await client.call("DescribeLifecycleHooks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_lifecycle_hooks failed") from exc
    return [_parse_lifecycle_hook(hook) for hook in resp.get("LifecycleHooks", [])]


async def complete_lifecycle_action(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("CompleteLifecycleAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to complete lifecycle action for {hook_name!r}") from exc


# ---------------------------------------------------------------------------
# Scaling activity operations
# ---------------------------------------------------------------------------


async def describe_scaling_activities(
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
    client = async_client("autoscaling", region_name)
    try:
        resp = await client.call(
            "DescribeScalingActivities",
            AutoScalingGroupName=asg_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_scaling_activities failed") from exc
    return [_parse_scaling_activity(act) for act in resp.get("Activities", [])]


# ---------------------------------------------------------------------------
# Process suspension / resumption
# ---------------------------------------------------------------------------


async def suspend_processes(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if scaling_processes is not None:
        kwargs["ScalingProcesses"] = scaling_processes
    try:
        await client.call("SuspendProcesses", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to suspend processes for {asg_name!r}") from exc


async def resume_processes(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {"AutoScalingGroupName": asg_name}
    if scaling_processes is not None:
        kwargs["ScalingProcesses"] = scaling_processes
    try:
        await client.call("ResumeProcesses", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to resume processes for {asg_name!r}") from exc


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def wait_for_group(
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
        groups = await describe_auto_scaling_groups(names=[name], region_name=region_name)
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
        await asyncio.sleep(poll_interval)


async def attach_instances(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        await client.call("AttachInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach instances") from exc
    return None


async def attach_load_balancers(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["LoadBalancerNames"] = load_balancer_names
    try:
        await client.call("AttachLoadBalancers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach load balancers") from exc
    return None


async def attach_traffic_sources(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TrafficSources"] = traffic_sources
    if skip_zonal_shift_validation is not None:
        kwargs["SkipZonalShiftValidation"] = skip_zonal_shift_validation
    try:
        await client.call("AttachTrafficSources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach traffic sources") from exc
    return None


async def batch_delete_scheduled_action(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledActionNames"] = scheduled_action_names
    try:
        resp = await client.call("BatchDeleteScheduledAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete scheduled action") from exc
    return BatchDeleteScheduledActionResult(
        failed_scheduled_actions=resp.get("FailedScheduledActions"),
    )


async def batch_put_scheduled_update_group_action(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledUpdateGroupActions"] = scheduled_update_group_actions
    try:
        resp = await client.call("BatchPutScheduledUpdateGroupAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch put scheduled update group action") from exc
    return BatchPutScheduledUpdateGroupActionResult(
        failed_scheduled_update_group_actions=resp.get("FailedScheduledUpdateGroupActions"),
    )


async def cancel_instance_refresh(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if wait_for_transitioning_instances is not None:
        kwargs["WaitForTransitioningInstances"] = wait_for_transitioning_instances
    try:
        resp = await client.call("CancelInstanceRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel instance refresh") from exc
    return CancelInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )


async def create_or_update_tags(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    try:
        await client.call("CreateOrUpdateTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create or update tags") from exc
    return None


async def delete_lifecycle_hook(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LifecycleHookName"] = lifecycle_hook_name
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    try:
        await client.call("DeleteLifecycleHook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete lifecycle hook") from exc
    return None


async def delete_notification_configuration(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TopicARN"] = topic_arn
    try:
        await client.call("DeleteNotificationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete notification configuration") from exc
    return None


async def delete_scheduled_action(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ScheduledActionName"] = scheduled_action_name
    try:
        await client.call("DeleteScheduledAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduled action") from exc
    return None


async def delete_tags(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    try:
        await client.call("DeleteTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete tags") from exc
    return None


async def delete_warm_pool(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if force_delete is not None:
        kwargs["ForceDelete"] = force_delete
    try:
        await client.call("DeleteWarmPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete warm pool") from exc
    return None


async def describe_account_limits(
    region_name: str | None = None,
) -> DescribeAccountLimitsResult:
    """Describe account limits.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAccountLimits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account limits") from exc
    return DescribeAccountLimitsResult(
        max_number_of_auto_scaling_groups=resp.get("MaxNumberOfAutoScalingGroups"),
        max_number_of_launch_configurations=resp.get("MaxNumberOfLaunchConfigurations"),
        number_of_auto_scaling_groups=resp.get("NumberOfAutoScalingGroups"),
        number_of_launch_configurations=resp.get("NumberOfLaunchConfigurations"),
    )


async def describe_adjustment_types(
    region_name: str | None = None,
) -> DescribeAdjustmentTypesResult:
    """Describe adjustment types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAdjustmentTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe adjustment types") from exc
    return DescribeAdjustmentTypesResult(
        adjustment_types=resp.get("AdjustmentTypes"),
    )


async def describe_auto_scaling_notification_types(
    region_name: str | None = None,
) -> DescribeAutoScalingNotificationTypesResult:
    """Describe auto scaling notification types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAutoScalingNotificationTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe auto scaling notification types") from exc
    return DescribeAutoScalingNotificationTypesResult(
        auto_scaling_notification_types=resp.get("AutoScalingNotificationTypes"),
    )


async def describe_instance_refreshes(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_refresh_ids is not None:
        kwargs["InstanceRefreshIds"] = instance_refresh_ids
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeInstanceRefreshes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance refreshes") from exc
    return DescribeInstanceRefreshesResult(
        instance_refreshes=resp.get("InstanceRefreshes"),
        next_token=resp.get("NextToken"),
    )


async def describe_lifecycle_hook_types(
    region_name: str | None = None,
) -> DescribeLifecycleHookTypesResult:
    """Describe lifecycle hook types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeLifecycleHookTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe lifecycle hook types") from exc
    return DescribeLifecycleHookTypesResult(
        lifecycle_hook_types=resp.get("LifecycleHookTypes"),
    )


async def describe_load_balancer_target_groups(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeLoadBalancerTargetGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe load balancer target groups") from exc
    return DescribeLoadBalancerTargetGroupsResult(
        load_balancer_target_groups=resp.get("LoadBalancerTargetGroups"),
        next_token=resp.get("NextToken"),
    )


async def describe_load_balancers(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeLoadBalancers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe load balancers") from exc
    return DescribeLoadBalancersResult(
        load_balancers=resp.get("LoadBalancers"),
        next_token=resp.get("NextToken"),
    )


async def describe_metric_collection_types(
    region_name: str | None = None,
) -> DescribeMetricCollectionTypesResult:
    """Describe metric collection types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeMetricCollectionTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metric collection types") from exc
    return DescribeMetricCollectionTypesResult(
        metrics=resp.get("Metrics"),
        granularities=resp.get("Granularities"),
    )


async def describe_notification_configurations(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if auto_scaling_group_names is not None:
        kwargs["AutoScalingGroupNames"] = auto_scaling_group_names
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeNotificationConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe notification configurations") from exc
    return DescribeNotificationConfigurationsResult(
        notification_configurations=resp.get("NotificationConfigurations"),
        next_token=resp.get("NextToken"),
    )


async def describe_policies(
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
    client = async_client("autoscaling", region_name)
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
        resp = await client.call("DescribePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe policies") from exc
    return DescribePoliciesResult(
        scaling_policies=resp.get("ScalingPolicies"),
        next_token=resp.get("NextToken"),
    )


async def describe_scaling_process_types(
    region_name: str | None = None,
) -> DescribeScalingProcessTypesResult:
    """Describe scaling process types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeScalingProcessTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe scaling process types") from exc
    return DescribeScalingProcessTypesResult(
        processes=resp.get("Processes"),
    )


async def describe_scheduled_actions(
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
    client = async_client("autoscaling", region_name)
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
        resp = await client.call("DescribeScheduledActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduled actions") from exc
    return DescribeScheduledActionsResult(
        scheduled_update_group_actions=resp.get("ScheduledUpdateGroupActions"),
        next_token=resp.get("NextToken"),
    )


async def describe_tags(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe tags") from exc
    return DescribeTagsResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


async def describe_termination_policy_types(
    region_name: str | None = None,
) -> DescribeTerminationPolicyTypesResult:
    """Describe termination policy types.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeTerminationPolicyTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe termination policy types") from exc
    return DescribeTerminationPolicyTypesResult(
        termination_policy_types=resp.get("TerminationPolicyTypes"),
    )


async def describe_traffic_sources(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if traffic_source_type is not None:
        kwargs["TrafficSourceType"] = traffic_source_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeTrafficSources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe traffic sources") from exc
    return DescribeTrafficSourcesResult(
        traffic_sources=resp.get("TrafficSources"),
        next_token=resp.get("NextToken"),
    )


async def describe_warm_pool(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeWarmPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe warm pool") from exc
    return DescribeWarmPoolResult(
        warm_pool_configuration=resp.get("WarmPoolConfiguration"),
        instances=resp.get("Instances"),
        next_token=resp.get("NextToken"),
    )


async def detach_instances(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ShouldDecrementDesiredCapacity"] = should_decrement_desired_capacity
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = await client.call("DetachInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach instances") from exc
    return DetachInstancesResult(
        activities=resp.get("Activities"),
    )


async def detach_load_balancers(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["LoadBalancerNames"] = load_balancer_names
    try:
        await client.call("DetachLoadBalancers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach load balancers") from exc
    return None


async def detach_traffic_sources(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TrafficSources"] = traffic_sources
    try:
        await client.call("DetachTrafficSources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach traffic sources") from exc
    return None


async def disable_metrics_collection(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if metrics is not None:
        kwargs["Metrics"] = metrics
    try:
        await client.call("DisableMetricsCollection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable metrics collection") from exc
    return None


async def enable_metrics_collection(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["Granularity"] = granularity
    if metrics is not None:
        kwargs["Metrics"] = metrics
    try:
        await client.call("EnableMetricsCollection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable metrics collection") from exc
    return None


async def enter_standby(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ShouldDecrementDesiredCapacity"] = should_decrement_desired_capacity
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = await client.call("EnterStandby", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enter standby") from exc
    return EnterStandbyResult(
        activities=resp.get("Activities"),
    )


async def execute_policy(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("ExecutePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to execute policy") from exc
    return None


async def exit_standby(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        resp = await client.call("ExitStandby", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to exit standby") from exc
    return ExitStandbyResult(
        activities=resp.get("Activities"),
    )


async def get_predictive_scaling_forecast(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["PolicyName"] = policy_name
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    try:
        resp = await client.call("GetPredictiveScalingForecast", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get predictive scaling forecast") from exc
    return GetPredictiveScalingForecastResult(
        load_forecast=resp.get("LoadForecast"),
        capacity_forecast=resp.get("CapacityForecast"),
        update_time=resp.get("UpdateTime"),
    )


async def put_notification_configuration(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["TopicARN"] = topic_arn
    kwargs["NotificationTypes"] = notification_types
    try:
        await client.call("PutNotificationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put notification configuration") from exc
    return None


async def put_scheduled_update_group_action(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("PutScheduledUpdateGroupAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put scheduled update group action") from exc
    return None


async def put_warm_pool(
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
    client = async_client("autoscaling", region_name)
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
        await client.call("PutWarmPool", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put warm pool") from exc
    return None


async def record_lifecycle_action_heartbeat(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["LifecycleHookName"] = lifecycle_hook_name
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if lifecycle_action_token is not None:
        kwargs["LifecycleActionToken"] = lifecycle_action_token
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    try:
        await client.call("RecordLifecycleActionHeartbeat", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to record lifecycle action heartbeat") from exc
    return None


async def rollback_instance_refresh(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    try:
        resp = await client.call("RollbackInstanceRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to rollback instance refresh") from exc
    return RollbackInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )


async def set_instance_health(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HealthStatus"] = health_status
    if should_respect_grace_period is not None:
        kwargs["ShouldRespectGracePeriod"] = should_respect_grace_period
    try:
        await client.call("SetInstanceHealth", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set instance health") from exc
    return None


async def set_instance_protection(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceIds"] = instance_ids
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    kwargs["ProtectedFromScaleIn"] = protected_from_scale_in
    try:
        await client.call("SetInstanceProtection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set instance protection") from exc
    return None


async def start_instance_refresh(
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
    client = async_client("autoscaling", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingGroupName"] = auto_scaling_group_name
    if strategy is not None:
        kwargs["Strategy"] = strategy
    if desired_configuration is not None:
        kwargs["DesiredConfiguration"] = desired_configuration
    if preferences is not None:
        kwargs["Preferences"] = preferences
    try:
        resp = await client.call("StartInstanceRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start instance refresh") from exc
    return StartInstanceRefreshResult(
        instance_refresh_id=resp.get("InstanceRefreshId"),
    )
