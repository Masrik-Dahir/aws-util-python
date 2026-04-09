"""Tests for aws_util.aio.autoscaling -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.autoscaling import (
    AutoScalingGroupResult,
    LaunchConfigurationResult,
    LifecycleHookResult,
    ScalingActivityResult,
    ScalingPolicyResult,
    attach_load_balancer_target_groups,
    complete_lifecycle_action,
    create_auto_scaling_group,
    create_launch_configuration,
    delete_auto_scaling_group,
    delete_launch_configuration,
    delete_policy,
    describe_auto_scaling_groups,
    describe_auto_scaling_instances,
    describe_launch_configurations,
    describe_lifecycle_hooks,
    describe_scaling_activities,
    describe_scaling_policies,
    detach_load_balancer_target_groups,
    put_lifecycle_hook,
    put_scaling_policy,
    resume_processes,
    set_desired_capacity,
    suspend_processes,
    terminate_instance_in_auto_scaling_group,
    update_auto_scaling_group,
    wait_for_group,
    attach_instances,
    attach_load_balancers,
    attach_traffic_sources,
    batch_delete_scheduled_action,
    batch_put_scheduled_update_group_action,
    cancel_instance_refresh,
    create_or_update_tags,
    delete_lifecycle_hook,
    delete_notification_configuration,
    delete_scheduled_action,
    delete_tags,
    delete_warm_pool,
    describe_account_limits,
    describe_adjustment_types,
    describe_auto_scaling_notification_types,
    describe_instance_refreshes,
    describe_lifecycle_hook_types,
    describe_load_balancer_target_groups,
    describe_load_balancers,
    describe_metric_collection_types,
    describe_notification_configurations,
    describe_policies,
    describe_scaling_process_types,
    describe_scheduled_actions,
    describe_tags,
    describe_termination_policy_types,
    describe_traffic_sources,
    describe_warm_pool,
    detach_instances,
    detach_load_balancers,
    detach_traffic_sources,
    disable_metrics_collection,
    enable_metrics_collection,
    enter_standby,
    execute_policy,
    exit_standby,
    get_predictive_scaling_forecast,
    put_notification_configuration,
    put_scheduled_update_group_action,
    put_warm_pool,
    record_lifecycle_action_heartbeat,
    rollback_instance_refresh,
    set_instance_health,
    set_instance_protection,
    start_instance_refresh,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# Launch configuration tests
# ---------------------------------------------------------------------------


async def test_create_launch_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await create_launch_configuration(
        "my-lc", image_id="ami-123", instance_type="t2.micro"
    )
    mock_client.call.assert_called_once()
    call_kwargs = mock_client.call.call_args
    assert call_kwargs[0][0] == "CreateLaunchConfiguration"

async def test_create_launch_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to create launch configuration"):
        await create_launch_configuration(
            "bad", image_id="ami-x", instance_type="t2.micro"
        )


async def test_describe_launch_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "LaunchConfigurations": [
            {
                "LaunchConfigurationName": "lc",
                "ImageId": "ami-123",
                "InstanceType": "t2.micro",
                "SecurityGroups": [],
                "CreatedTime": "2024-01-01T00:00:00Z",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_launch_configurations()
    assert len(result) == 1
    assert isinstance(result[0], LaunchConfigurationResult)
    assert result[0].name == "lc"


async def test_describe_launch_configurations_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LaunchConfigurations": []}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_launch_configurations(
        names=["lc"], region_name="us-east-1"
    )
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["LaunchConfigurationNames"] == ["lc"]


async def test_describe_launch_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="describe_launch_configurations failed"):
        await describe_launch_configurations()


async def test_delete_launch_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await delete_launch_configuration("lc")
    mock_client.call.assert_called_once()


async def test_delete_launch_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to delete launch configuration"):
        await delete_launch_configuration("bad")


# ---------------------------------------------------------------------------
# Auto Scaling group tests
# ---------------------------------------------------------------------------


def _asg_dict(
    name: str = "test-asg",
    arn: str = "arn:aws:autoscaling:us-east-1:123:autoScalingGroup:id:autoScalingGroupName/test-asg",
    min_size: int = 1,
    max_size: int = 3,
    desired: int = 1,
    instances: list | None = None,
    tags: list | None = None,
) -> dict:
    return {
        "AutoScalingGroupName": name,
        "AutoScalingGroupARN": arn,
        "LaunchConfigurationName": "lc",
        "MinSize": min_size,
        "MaxSize": max_size,
        "DesiredCapacity": desired,
        "AvailabilityZones": ["us-east-1a"],
        "Instances": instances or [],
        "Tags": tags or [],
    }


async def test_create_auto_scaling_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await create_auto_scaling_group(
        "asg",
        launch_config_name="lc",
        min_size=0,
        max_size=2,
        desired_capacity=1,
        availability_zones=["us-east-1a"],
        tags={"env": "test"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["AutoScalingGroupName"] == "asg"
    assert call_kwargs["LaunchConfigurationName"] == "lc"
    assert call_kwargs["DesiredCapacity"] == 1
    assert len(call_kwargs["Tags"]) == 1


async def test_create_auto_scaling_group_with_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await create_auto_scaling_group(
        "asg",
        launch_template={"LaunchTemplateId": "lt-123", "Version": "$Latest"},
        vpc_zone_identifier="subnet-123",
        target_group_arns=["arn:tg"],
        region_name="us-east-1",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "LaunchTemplate" in call_kwargs
    assert call_kwargs["VPCZoneIdentifier"] == "subnet-123"
    assert call_kwargs["TargetGroupARNs"] == ["arn:tg"]


async def test_create_auto_scaling_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to create Auto Scaling group"):
        await create_auto_scaling_group("bad", launch_config_name="lc")


async def test_describe_auto_scaling_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingGroups": [_asg_dict()],
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_auto_scaling_groups()
    assert len(result) == 1
    assert isinstance(result[0], AutoScalingGroupResult)
    assert result[0].name == "test-asg"


async def test_describe_auto_scaling_groups_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingGroups": [_asg_dict()],
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_auto_scaling_groups(
        names=["test-asg"], region_name="us-east-1"
    )
    assert len(result) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["AutoScalingGroupNames"] == ["test-asg"]


async def test_describe_auto_scaling_groups_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "AutoScalingGroups": [_asg_dict("asg-1")],
            "NextToken": "tok1",
        },
        {
            "AutoScalingGroups": [_asg_dict("asg-2")],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_auto_scaling_groups()
    assert len(result) == 2
    assert result[0].name == "asg-1"
    assert result[1].name == "asg-2"


async def test_describe_auto_scaling_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="describe_auto_scaling_groups failed"):
        await describe_auto_scaling_groups()


async def test_update_auto_scaling_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await update_auto_scaling_group(
        "asg", min_size=0, max_size=5, desired_capacity=2
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["MinSize"] == 0
    assert call_kwargs["MaxSize"] == 5
    assert call_kwargs["DesiredCapacity"] == 2


async def test_update_auto_scaling_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to update Auto Scaling group"):
        await update_auto_scaling_group("bad", min_size=0)


async def test_delete_auto_scaling_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await delete_auto_scaling_group("asg", force_delete=True)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["ForceDelete"] is True


async def test_delete_auto_scaling_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to delete Auto Scaling group"):
        await delete_auto_scaling_group("bad")


async def test_set_desired_capacity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await set_desired_capacity("asg", desired_capacity=3)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["DesiredCapacity"] == 3


async def test_set_desired_capacity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to set desired capacity"):
        await set_desired_capacity("bad", desired_capacity=99)


# ---------------------------------------------------------------------------
# Scaling policy tests
# ---------------------------------------------------------------------------


async def test_put_scaling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"PolicyARN": "arn:policy"}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await put_scaling_policy(
        "asg",
        "scale-out",
        policy_type="SimpleScaling",
        adjustment_type="ChangeInCapacity",
        scaling_adjustment=1,
    )
    assert isinstance(result, ScalingPolicyResult)
    assert result.policy_name == "scale-out"
    assert result.policy_arn == "arn:policy"


async def test_put_scaling_policy_target_tracking(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"PolicyARN": "arn:tt"}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await put_scaling_policy(
        "asg",
        "tt-policy",
        target_tracking_config={"TargetValue": 50.0},
        region_name="us-east-1",
    )
    assert result.target_tracking_config is not None


async def test_put_scaling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to put scaling policy"):
        await put_scaling_policy("asg", "pol")


async def test_describe_scaling_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ScalingPolicies": [
            {
                "PolicyName": "pol",
                "PolicyARN": "arn:pol",
                "PolicyType": "SimpleScaling",
                "AdjustmentType": "ChangeInCapacity",
                "ScalingAdjustment": 1,
                "AutoScalingGroupName": "asg",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_scaling_policies("asg")
    assert len(result) == 1
    assert isinstance(result[0], ScalingPolicyResult)


async def test_describe_scaling_policies_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"ScalingPolicies": []}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_scaling_policies(
        "asg", policy_names=["pol"], region_name="us-east-1"
    )
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["PolicyNames"] == ["pol"]


async def test_describe_scaling_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="describe_scaling_policies failed"):
        await describe_scaling_policies("asg")


async def test_delete_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await delete_policy("asg", "pol")
    mock_client.call.assert_called_once()


async def test_delete_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to delete policy"):
        await delete_policy("asg", "pol")


# ---------------------------------------------------------------------------
# Load balancer target group tests
# ---------------------------------------------------------------------------


async def test_attach_load_balancer_target_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await attach_load_balancer_target_groups(
        "asg", target_group_arns=["arn:tg"]
    )
    mock_client.call.assert_called_once()


async def test_attach_load_balancer_target_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to attach target groups"):
        await attach_load_balancer_target_groups(
            "asg", target_group_arns=["arn"]
        )


async def test_detach_load_balancer_target_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await detach_load_balancer_target_groups(
        "asg", target_group_arns=["arn:tg"]
    )
    mock_client.call.assert_called_once()


async def test_detach_load_balancer_target_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to detach target groups"):
        await detach_load_balancer_target_groups(
            "asg", target_group_arns=["arn"]
        )


# ---------------------------------------------------------------------------
# Instance tests
# ---------------------------------------------------------------------------


async def test_describe_auto_scaling_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingInstances": [
            {"InstanceId": "i-123", "AutoScalingGroupName": "asg"}
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_auto_scaling_instances()
    assert len(result) == 1
    assert result[0]["InstanceId"] == "i-123"


async def test_describe_auto_scaling_instances_with_ids(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"AutoScalingInstances": []}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_auto_scaling_instances(
        instance_ids=["i-123"], region_name="us-east-1"
    )
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["InstanceIds"] == ["i-123"]


async def test_describe_auto_scaling_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_auto_scaling_instances failed"
    ):
        await describe_auto_scaling_instances()


async def test_terminate_instance_in_auto_scaling_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Activity": {"ActivityId": "act-123", "StatusCode": "InProgress"}
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await terminate_instance_in_auto_scaling_group("i-123")
    assert result["ActivityId"] == "act-123"


async def test_terminate_instance_no_decrement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Activity": {}}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await terminate_instance_in_auto_scaling_group(
        "i-123", should_decrement=False, region_name="us-east-1"
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["ShouldDecrementDesiredCapacity"] is False


async def test_terminate_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to terminate instance"):
        await terminate_instance_in_auto_scaling_group("i-bad")


# ---------------------------------------------------------------------------
# Lifecycle hook tests
# ---------------------------------------------------------------------------


async def test_put_lifecycle_hook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await put_lifecycle_hook(
        "asg",
        "hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
        heartbeat_timeout=300,
        default_result="CONTINUE",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["HeartbeatTimeout"] == 300
    assert call_kwargs["DefaultResult"] == "CONTINUE"


async def test_put_lifecycle_hook_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await put_lifecycle_hook(
        "asg",
        "hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_TERMINATING",
        region_name="us-east-1",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "HeartbeatTimeout" not in call_kwargs
    assert "DefaultResult" not in call_kwargs


async def test_put_lifecycle_hook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to put lifecycle hook"):
        await put_lifecycle_hook(
            "asg",
            "hook",
            lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
        )


async def test_describe_lifecycle_hooks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "LifecycleHooks": [
            {
                "LifecycleHookName": "hook",
                "AutoScalingGroupName": "asg",
                "LifecycleTransition": "autoscaling:EC2_INSTANCE_LAUNCHING",
                "HeartbeatTimeout": 300,
                "DefaultResult": "CONTINUE",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_lifecycle_hooks("asg")
    assert len(result) == 1
    assert isinstance(result[0], LifecycleHookResult)
    assert result[0].hook_name == "hook"


async def test_describe_lifecycle_hooks_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LifecycleHooks": []}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_lifecycle_hooks(
        "asg", hook_names=["hook"], region_name="us-east-1"
    )
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["LifecycleHookNames"] == ["hook"]


async def test_describe_lifecycle_hooks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="describe_lifecycle_hooks failed"):
        await describe_lifecycle_hooks("asg")


async def test_complete_lifecycle_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await complete_lifecycle_action(
        "asg",
        "hook",
        lifecycle_action_result="CONTINUE",
        instance_id="i-123",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["InstanceId"] == "i-123"


async def test_complete_lifecycle_action_with_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await complete_lifecycle_action(
        "asg",
        "hook",
        lifecycle_action_result="ABANDON",
        lifecycle_action_token="tok-123",
        region_name="us-east-1",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["LifecycleActionToken"] == "tok-123"
    assert "InstanceId" not in call_kwargs


async def test_complete_lifecycle_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to complete lifecycle action"):
        await complete_lifecycle_action(
            "asg", "hook", lifecycle_action_result="CONTINUE"
        )


# ---------------------------------------------------------------------------
# Scaling activity tests
# ---------------------------------------------------------------------------


async def test_describe_scaling_activities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Activities": [
            {
                "ActivityId": "act-1",
                "AutoScalingGroupName": "asg",
                "Cause": "user",
                "StatusCode": "Successful",
                "StartTime": "2024-01-01T00:00:00Z",
                "EndTime": "2024-01-01T00:01:00Z",
                "Description": "Launching instance",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_scaling_activities("asg")
    assert len(result) == 1
    assert isinstance(result[0], ScalingActivityResult)
    assert result[0].activity_id == "act-1"
    assert result[0].end_time is not None
    assert result[0].description == "Launching instance"


async def test_describe_scaling_activities_no_end_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Activities": [
            {
                "ActivityId": "act-2",
                "AutoScalingGroupName": "asg",
                "Cause": "auto",
                "StatusCode": "InProgress",
                "StartTime": "2024-01-01T00:00:00Z",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_scaling_activities("asg", region_name="us-east-1")
    assert result[0].end_time is None


async def test_describe_scaling_activities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="describe_scaling_activities failed"):
        await describe_scaling_activities("asg")


# ---------------------------------------------------------------------------
# Process suspension / resumption tests
# ---------------------------------------------------------------------------


async def test_suspend_processes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await suspend_processes(
        "asg", scaling_processes=["Launch", "Terminate"]
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["ScalingProcesses"] == ["Launch", "Terminate"]


async def test_suspend_processes_all(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await suspend_processes("asg", region_name="us-east-1")
    call_kwargs = mock_client.call.call_args[1]
    assert "ScalingProcesses" not in call_kwargs


async def test_suspend_processes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to suspend processes"):
        await suspend_processes("asg")


async def test_resume_processes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await resume_processes("asg", scaling_processes=["Launch"])
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["ScalingProcesses"] == ["Launch"]


async def test_resume_processes_all(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    await resume_processes("asg", region_name="us-east-1")
    call_kwargs = mock_client.call.call_args[1]
    assert "ScalingProcesses" not in call_kwargs


async def test_resume_processes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="Failed to resume processes"):
        await resume_processes("asg")


# ---------------------------------------------------------------------------
# wait_for_group tests
# ---------------------------------------------------------------------------


async def test_wait_for_group_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingGroups": [
            _asg_dict(
                instances=[
                    {"InstanceId": "i-1", "LifecycleState": "InService"}
                ],
            )
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await wait_for_group("test-asg", timeout=5, poll_interval=1)
    assert isinstance(result, AutoScalingGroupResult)
    assert result.name == "test-asg"


async def test_wait_for_group_zero_desired(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingGroups": [_asg_dict(desired=0, instances=[])],
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    result = await wait_for_group("test-asg", timeout=5, poll_interval=1)
    assert result.desired_capacity == 0


async def test_wait_for_group_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"AutoScalingGroups": []}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_group("nonexistent", timeout=5, poll_interval=1)


async def test_wait_for_group_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AutoScalingGroups": [
            _asg_dict(
                instances=[
                    {"InstanceId": "i-1", "LifecycleState": "Pending"}
                ],
            )
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        _mock_factory(mock_client),
    )
    monkeypatch.setattr("aws_util.aio.autoscaling.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="did not stabilise"):
        await wait_for_group(
            "test-asg",
            timeout=0.001,
            poll_interval=0.001,
            region_name="us-east-1",
        )


# ---------------------------------------------------------------------------
# Re-export tests
# ---------------------------------------------------------------------------


def test_reexports():
    """Verify that models are re-exported from the async module."""
    from aws_util.aio import autoscaling as aio_mod

    assert aio_mod.AutoScalingGroupResult is AutoScalingGroupResult
    assert aio_mod.LaunchConfigurationResult is LaunchConfigurationResult
    assert aio_mod.ScalingPolicyResult is ScalingPolicyResult
    assert aio_mod.LifecycleHookResult is LifecycleHookResult
    assert aio_mod.ScalingActivityResult is ScalingActivityResult


async def test_attach_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_instances("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_attach_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_instances("test-auto_scaling_group_name", )


async def test_attach_load_balancers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_load_balancers("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_attach_load_balancers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_load_balancers("test-auto_scaling_group_name", [], )


async def test_attach_traffic_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_traffic_sources("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_attach_traffic_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_traffic_sources("test-auto_scaling_group_name", [], )


async def test_batch_delete_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_scheduled_action("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_scheduled_action("test-auto_scaling_group_name", [], )


async def test_batch_put_scheduled_update_group_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_put_scheduled_update_group_action("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_put_scheduled_update_group_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_put_scheduled_update_group_action("test-auto_scaling_group_name", [], )


async def test_cancel_instance_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_instance_refresh("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_cancel_instance_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_instance_refresh("test-auto_scaling_group_name", )


async def test_create_or_update_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_or_update_tags([], )
    mock_client.call.assert_called_once()


async def test_create_or_update_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_or_update_tags([], )


async def test_delete_lifecycle_hook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_lifecycle_hook("test-lifecycle_hook_name", "test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_lifecycle_hook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_lifecycle_hook("test-lifecycle_hook_name", "test-auto_scaling_group_name", )


async def test_delete_notification_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", )
    mock_client.call.assert_called_once()


async def test_delete_notification_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", )


async def test_delete_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_scheduled_action("test-auto_scaling_group_name", "test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_delete_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_scheduled_action("test-auto_scaling_group_name", "test-scheduled_action_name", )


async def test_delete_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tags([], )
    mock_client.call.assert_called_once()


async def test_delete_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tags([], )


async def test_delete_warm_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_warm_pool("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_warm_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_warm_pool("test-auto_scaling_group_name", )


async def test_describe_account_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_limits()
    mock_client.call.assert_called_once()


async def test_describe_account_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_limits()


async def test_describe_adjustment_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_adjustment_types()
    mock_client.call.assert_called_once()


async def test_describe_adjustment_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_adjustment_types()


async def test_describe_auto_scaling_notification_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_auto_scaling_notification_types()
    mock_client.call.assert_called_once()


async def test_describe_auto_scaling_notification_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_auto_scaling_notification_types()


async def test_describe_instance_refreshes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_refreshes("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_instance_refreshes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_refreshes("test-auto_scaling_group_name", )


async def test_describe_lifecycle_hook_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_lifecycle_hook_types()
    mock_client.call.assert_called_once()


async def test_describe_lifecycle_hook_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_lifecycle_hook_types()


async def test_describe_load_balancer_target_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_load_balancer_target_groups("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_load_balancer_target_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_load_balancer_target_groups("test-auto_scaling_group_name", )


async def test_describe_load_balancers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_load_balancers("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_load_balancers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_load_balancers("test-auto_scaling_group_name", )


async def test_describe_metric_collection_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_metric_collection_types()
    mock_client.call.assert_called_once()


async def test_describe_metric_collection_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_metric_collection_types()


async def test_describe_notification_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_notification_configurations()
    mock_client.call.assert_called_once()


async def test_describe_notification_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_notification_configurations()


async def test_describe_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_policies()
    mock_client.call.assert_called_once()


async def test_describe_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_policies()


async def test_describe_scaling_process_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scaling_process_types()
    mock_client.call.assert_called_once()


async def test_describe_scaling_process_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scaling_process_types()


async def test_describe_scheduled_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_actions()
    mock_client.call.assert_called_once()


async def test_describe_scheduled_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_actions()


async def test_describe_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tags()
    mock_client.call.assert_called_once()


async def test_describe_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tags()


async def test_describe_termination_policy_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_termination_policy_types()
    mock_client.call.assert_called_once()


async def test_describe_termination_policy_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_termination_policy_types()


async def test_describe_traffic_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_sources("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_traffic_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_sources("test-auto_scaling_group_name", )


async def test_describe_warm_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_warm_pool("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_warm_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_warm_pool("test-auto_scaling_group_name", )


async def test_detach_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_instances("test-auto_scaling_group_name", True, )
    mock_client.call.assert_called_once()


async def test_detach_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_instances("test-auto_scaling_group_name", True, )


async def test_detach_load_balancers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_load_balancers("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_detach_load_balancers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_load_balancers("test-auto_scaling_group_name", [], )


async def test_detach_traffic_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_traffic_sources("test-auto_scaling_group_name", [], )
    mock_client.call.assert_called_once()


async def test_detach_traffic_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_traffic_sources("test-auto_scaling_group_name", [], )


async def test_disable_metrics_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_metrics_collection("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_disable_metrics_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_metrics_collection("test-auto_scaling_group_name", )


async def test_enable_metrics_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_metrics_collection("test-auto_scaling_group_name", "test-granularity", )
    mock_client.call.assert_called_once()


async def test_enable_metrics_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_metrics_collection("test-auto_scaling_group_name", "test-granularity", )


async def test_enter_standby(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await enter_standby("test-auto_scaling_group_name", True, )
    mock_client.call.assert_called_once()


async def test_enter_standby_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enter_standby("test-auto_scaling_group_name", True, )


async def test_execute_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_policy("test-policy_name", )
    mock_client.call.assert_called_once()


async def test_execute_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_policy("test-policy_name", )


async def test_exit_standby(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await exit_standby("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_exit_standby_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await exit_standby("test-auto_scaling_group_name", )


async def test_get_predictive_scaling_forecast(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_predictive_scaling_forecast("test-auto_scaling_group_name", "test-policy_name", "test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_get_predictive_scaling_forecast_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_predictive_scaling_forecast("test-auto_scaling_group_name", "test-policy_name", "test-start_time", "test-end_time", )


async def test_put_notification_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", [], )
    mock_client.call.assert_called_once()


async def test_put_notification_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", [], )


async def test_put_scheduled_update_group_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_scheduled_update_group_action("test-auto_scaling_group_name", "test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_put_scheduled_update_group_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_scheduled_update_group_action("test-auto_scaling_group_name", "test-scheduled_action_name", )


async def test_put_warm_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_warm_pool("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_put_warm_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_warm_pool("test-auto_scaling_group_name", )


async def test_record_lifecycle_action_heartbeat(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await record_lifecycle_action_heartbeat("test-lifecycle_hook_name", "test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_record_lifecycle_action_heartbeat_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await record_lifecycle_action_heartbeat("test-lifecycle_hook_name", "test-auto_scaling_group_name", )


async def test_rollback_instance_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await rollback_instance_refresh("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_rollback_instance_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rollback_instance_refresh("test-auto_scaling_group_name", )


async def test_set_instance_health(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_instance_health("test-instance_id", "test-health_status", )
    mock_client.call.assert_called_once()


async def test_set_instance_health_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_instance_health("test-instance_id", "test-health_status", )


async def test_set_instance_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_instance_protection([], "test-auto_scaling_group_name", True, )
    mock_client.call.assert_called_once()


async def test_set_instance_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_instance_protection([], "test-auto_scaling_group_name", True, )


async def test_start_instance_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_instance_refresh("test-auto_scaling_group_name", )
    mock_client.call.assert_called_once()


async def test_start_instance_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.autoscaling.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_instance_refresh("test-auto_scaling_group_name", )


@pytest.mark.asyncio
async def test_update_auto_scaling_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import update_auto_scaling_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await update_auto_scaling_group("test-name", min_size=1, max_size=1, desired_capacity="test-desired_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_suspend_processes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import suspend_processes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await suspend_processes("test-asg_name", scaling_processes="test-scaling_processes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resume_processes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import resume_processes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await resume_processes("test-asg_name", scaling_processes="test-scaling_processes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import attach_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await attach_instances(True, instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_traffic_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import attach_traffic_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await attach_traffic_sources(True, "test-traffic_sources", skip_zonal_shift_validation=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_instance_refresh_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import cancel_instance_refresh
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await cancel_instance_refresh(True, wait_for_transitioning_instances="test-wait_for_transitioning_instances", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_warm_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import delete_warm_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await delete_warm_pool(True, force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_refreshes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_instance_refreshes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_instance_refreshes(True, instance_refresh_ids="test-instance_refresh_ids", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_load_balancer_target_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_load_balancer_target_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_load_balancer_target_groups(True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_load_balancers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_load_balancers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_load_balancers(True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_notification_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_notification_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_notification_configurations(auto_scaling_group_names=True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_policies(auto_scaling_group_name=True, policy_names="test-policy_names", policy_types="test-policy_types", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_scheduled_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_scheduled_actions(auto_scaling_group_name=True, scheduled_action_names="test-scheduled_action_names", start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_tags(filters=[{}], next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_traffic_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_traffic_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_traffic_sources(True, traffic_source_type="test-traffic_source_type", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_warm_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import describe_warm_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await describe_warm_pool(True, max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import detach_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await detach_instances(True, "test-should_decrement_desired_capacity", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_metrics_collection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import disable_metrics_collection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await disable_metrics_collection(True, metrics="test-metrics", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_metrics_collection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import enable_metrics_collection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await enable_metrics_collection(True, "test-granularity", metrics="test-metrics", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enter_standby_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import enter_standby
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await enter_standby(True, "test-should_decrement_desired_capacity", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import execute_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await execute_policy("test-policy_name", auto_scaling_group_name=True, honor_cooldown="test-honor_cooldown", metric_value="test-metric_value", breach_threshold="test-breach_threshold", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_exit_standby_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import exit_standby
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await exit_standby(True, instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_scheduled_update_group_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import put_scheduled_update_group_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await put_scheduled_update_group_action(True, "test-scheduled_action_name", time="test-time", start_time="test-start_time", end_time="test-end_time", recurrence="test-recurrence", min_size=1, max_size=1, desired_capacity="test-desired_capacity", time_zone="test-time_zone", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_warm_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import put_warm_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await put_warm_pool(True, max_group_prepared_capacity=1, min_size=1, pool_state="test-pool_state", instance_reuse_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_record_lifecycle_action_heartbeat_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import record_lifecycle_action_heartbeat
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await record_lifecycle_action_heartbeat("test-lifecycle_hook_name", True, lifecycle_action_token="test-lifecycle_action_token", instance_id="test-instance_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_instance_health_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import set_instance_health
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await set_instance_health("test-instance_id", "test-health_status", should_respect_grace_period="test-should_respect_grace_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_instance_refresh_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import start_instance_refresh
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await start_instance_refresh(True, strategy="test-strategy", desired_configuration={}, preferences="test-preferences", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_launch_configuration_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import create_launch_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: mock_client)
    await create_launch_configuration("test-name", image_id="ami-1", instance_type="t2.micro", security_groups=["sg-1"], region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_launch_configuration_key_name(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.autoscaling import create_launch_configuration
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.autoscaling.async_client", lambda *a, **kw: m)
    await create_launch_configuration("n", image_id="a", instance_type="t", key_name="k", security_groups=["s"], region_name="us-east-1")
