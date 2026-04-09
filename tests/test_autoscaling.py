"""Tests for aws_util.autoscaling module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError

from aws_util.autoscaling import (
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

REGION = "us-east-1"
LC_NAME = "test-lc"
ASG_NAME = "test-asg"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def launch_config():
    """Create a launch configuration for use in tests."""
    client = boto3.client("autoscaling", region_name=REGION)
    client.create_launch_configuration(
        LaunchConfigurationName=LC_NAME,
        ImageId="ami-12345678",
        InstanceType="t2.micro",
    )
    return client


@pytest.fixture
def asg(launch_config):
    """Create an ASG backed by a launch configuration."""
    client = launch_config
    client.create_auto_scaling_group(
        AutoScalingGroupName=ASG_NAME,
        LaunchConfigurationName=LC_NAME,
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        AvailabilityZones=["us-east-1a"],
    )
    return client


# ---------------------------------------------------------------------------
# Launch configuration tests
# ---------------------------------------------------------------------------


def test_create_launch_configuration():
    create_launch_configuration(
        "my-lc",
        image_id="ami-12345678",
        instance_type="t2.micro",
        region_name=REGION,
    )
    result = describe_launch_configurations(
        names=["my-lc"], region_name=REGION
    )
    assert len(result) == 1
    assert result[0].name == "my-lc"
    assert isinstance(result[0], LaunchConfigurationResult)

def test_describe_launch_configurations_all(launch_config):
    result = describe_launch_configurations(region_name=REGION)
    assert len(result) >= 1
    assert all(isinstance(lc, LaunchConfigurationResult) for lc in result)


def test_describe_launch_configurations_by_name(launch_config):
    result = describe_launch_configurations(
        names=[LC_NAME], region_name=REGION
    )
    assert len(result) == 1
    assert result[0].name == LC_NAME
    assert result[0].image_id == "ami-12345678"
    assert result[0].instance_type == "t2.micro"
    assert result[0].created_time is not None


def test_delete_launch_configuration(launch_config):
    delete_launch_configuration(LC_NAME, region_name=REGION)
    result = describe_launch_configurations(
        names=[LC_NAME], region_name=REGION
    )
    assert len(result) == 0


def test_create_launch_configuration_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.create_launch_configuration.side_effect = ClientError(
        {"Error": {"Code": "AlreadyExistsException", "Message": "exists"}},
        "CreateLaunchConfiguration",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create launch configuration"):
        create_launch_configuration(
            "bad", image_id="ami-x", instance_type="t2.micro", region_name=REGION
        )


def test_describe_launch_configurations_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.describe_launch_configurations.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribeLaunchConfigurations",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_launch_configurations failed"):
        describe_launch_configurations(region_name=REGION)


def test_delete_launch_configuration_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.delete_launch_configuration.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DeleteLaunchConfiguration",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete launch configuration"):
        delete_launch_configuration("nope", region_name=REGION)


# ---------------------------------------------------------------------------
# Auto Scaling group tests
# ---------------------------------------------------------------------------


def test_create_auto_scaling_group(launch_config):
    create_auto_scaling_group(
        "new-asg",
        launch_config_name=LC_NAME,
        min_size=0,
        max_size=2,
        desired_capacity=1,
        availability_zones=["us-east-1a"],
        tags={"env": "test"},
        region_name=REGION,
    )
    result = describe_auto_scaling_groups(
        names=["new-asg"], region_name=REGION
    )
    assert len(result) == 1
    assert result[0].name == "new-asg"
    assert result[0].tags.get("env") == "test"


def test_create_auto_scaling_group_with_vpc():
    """Test that vpc_zone_identifier and target_group_arns are passed through."""
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        create_auto_scaling_group(
            "vpc-asg",
            launch_config_name=LC_NAME,
            min_size=0,
            max_size=1,
            availability_zones=["us-east-1a"],
            vpc_zone_identifier="subnet-12345",
            target_group_arns=[
                "arn:aws:elasticloadbalancing:us-east-1:123:tg/my-tg/123"
            ],
            region_name=REGION,
        )
    call_kwargs = mock_client.create_auto_scaling_group.call_args[1]
    assert call_kwargs["VPCZoneIdentifier"] == "subnet-12345"
    assert len(call_kwargs["TargetGroupARNs"]) == 1


def test_create_auto_scaling_group_with_launch_template(launch_config):
    """Test that launch_template parameter is passed through."""
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    create_auto_scaling_group(
        "lt-asg",
        launch_template={
            "LaunchTemplateId": "lt-12345",
            "Version": "$Latest",
        },
        availability_zones=["us-east-1a"],
        region_name=REGION,
    )
    mock_client.create_auto_scaling_group.assert_called_once()
    call_kwargs = mock_client.create_auto_scaling_group.call_args[1]
    assert "LaunchTemplate" in call_kwargs
    monkeypatch.undo()


def test_describe_auto_scaling_groups_all(asg):
    result = describe_auto_scaling_groups(region_name=REGION)
    assert len(result) >= 1
    assert all(isinstance(g, AutoScalingGroupResult) for g in result)


def test_describe_auto_scaling_groups_by_name(asg):
    result = describe_auto_scaling_groups(
        names=[ASG_NAME], region_name=REGION
    )
    assert len(result) == 1
    assert result[0].name == ASG_NAME
    assert result[0].min_size == 1
    assert result[0].max_size == 3
    assert result[0].desired_capacity == 1
    assert "us-east-1a" in result[0].availability_zones
    assert result[0].arn is not None


def test_update_auto_scaling_group(asg):
    update_auto_scaling_group(
        ASG_NAME,
        min_size=0,
        max_size=5,
        desired_capacity=2,
        region_name=REGION,
    )
    result = describe_auto_scaling_groups(
        names=[ASG_NAME], region_name=REGION
    )
    assert result[0].min_size == 0
    assert result[0].max_size == 5
    assert result[0].desired_capacity == 2


def test_delete_auto_scaling_group(asg):
    delete_auto_scaling_group(
        ASG_NAME, force_delete=True, region_name=REGION
    )
    result = describe_auto_scaling_groups(
        names=[ASG_NAME], region_name=REGION
    )
    assert len(result) == 0


def test_set_desired_capacity(asg):
    set_desired_capacity(
        ASG_NAME, desired_capacity=2, region_name=REGION
    )
    result = describe_auto_scaling_groups(
        names=[ASG_NAME], region_name=REGION
    )
    assert result[0].desired_capacity == 2


def test_create_auto_scaling_group_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.create_auto_scaling_group.side_effect = ClientError(
        {"Error": {"Code": "AlreadyExistsException", "Message": "exists"}},
        "CreateAutoScalingGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create Auto Scaling group"):
        create_auto_scaling_group(
            "bad", launch_config_name="lc", region_name=REGION
        )


def test_describe_auto_scaling_groups_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribeAutoScalingGroups",
    )
    mock_client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_auto_scaling_groups failed"):
        describe_auto_scaling_groups(region_name=REGION)


def test_update_auto_scaling_group_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.update_auto_scaling_group.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "UpdateAutoScalingGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update Auto Scaling group"):
        update_auto_scaling_group("bad", min_size=0, region_name=REGION)


def test_delete_auto_scaling_group_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.delete_auto_scaling_group.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DeleteAutoScalingGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete Auto Scaling group"):
        delete_auto_scaling_group("bad", region_name=REGION)


def test_set_desired_capacity_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.set_desired_capacity.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "SetDesiredCapacity",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set desired capacity"):
        set_desired_capacity("bad", desired_capacity=99, region_name=REGION)


# ---------------------------------------------------------------------------
# Scaling policy tests
# ---------------------------------------------------------------------------


def test_put_scaling_policy_simple(asg):
    result = put_scaling_policy(
        ASG_NAME,
        "scale-out",
        policy_type="SimpleScaling",
        adjustment_type="ChangeInCapacity",
        scaling_adjustment=1,
        region_name=REGION,
    )
    assert isinstance(result, ScalingPolicyResult)
    assert result.policy_name == "scale-out"
    assert result.policy_arn is not None
    assert result.policy_type == "SimpleScaling"
    assert result.adjustment_type == "ChangeInCapacity"
    assert result.scaling_adjustment == 1


def test_put_scaling_policy_target_tracking(asg):
    result = put_scaling_policy(
        ASG_NAME,
        "tt-policy",
        policy_type="TargetTrackingScaling",
        target_tracking_config={
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "ASGAverageCPUUtilization",
            },
            "TargetValue": 50.0,
        },
        region_name=REGION,
    )
    assert isinstance(result, ScalingPolicyResult)
    assert result.policy_name == "tt-policy"
    assert result.target_tracking_config is not None


def test_describe_scaling_policies(asg):
    put_scaling_policy(
        ASG_NAME,
        "scale-out",
        policy_type="SimpleScaling",
        adjustment_type="ChangeInCapacity",
        scaling_adjustment=1,
        region_name=REGION,
    )
    result = describe_scaling_policies(ASG_NAME, region_name=REGION)
    assert len(result) >= 1
    assert all(isinstance(p, ScalingPolicyResult) for p in result)


def test_describe_scaling_policies_by_name(asg):
    put_scaling_policy(
        ASG_NAME,
        "scale-out",
        policy_type="SimpleScaling",
        adjustment_type="ChangeInCapacity",
        scaling_adjustment=1,
        region_name=REGION,
    )
    result = describe_scaling_policies(
        ASG_NAME, policy_names=["scale-out"], region_name=REGION
    )
    assert len(result) == 1
    assert result[0].policy_name == "scale-out"


def test_delete_policy(asg):
    put_scaling_policy(
        ASG_NAME,
        "to-delete",
        policy_type="SimpleScaling",
        adjustment_type="ChangeInCapacity",
        scaling_adjustment=1,
        region_name=REGION,
    )
    delete_policy(ASG_NAME, "to-delete", region_name=REGION)
    result = describe_scaling_policies(
        ASG_NAME, policy_names=["to-delete"], region_name=REGION
    )
    assert len(result) == 0


def test_put_scaling_policy_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.put_scaling_policy.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "PutScalingPolicy",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put scaling policy"):
        put_scaling_policy("asg", "pol", region_name=REGION)


def test_describe_scaling_policies_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.describe_policies.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribePolicies",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_scaling_policies failed"):
        describe_scaling_policies("asg", region_name=REGION)


def test_delete_policy_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.delete_policy.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
        "DeletePolicy",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete policy"):
        delete_policy("asg", "pol", region_name=REGION)


# ---------------------------------------------------------------------------
# Load balancer target group tests
# ---------------------------------------------------------------------------


def test_attach_load_balancer_target_groups():
    """Test attach target groups via mock (moto validates ARNs)."""
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        attach_load_balancer_target_groups(
            ASG_NAME,
            target_group_arns=["arn:tg"],
            region_name=REGION,
        )
    mock_client.attach_load_balancer_target_groups.assert_called_once()
    call_kwargs = mock_client.attach_load_balancer_target_groups.call_args[1]
    assert call_kwargs["TargetGroupARNs"] == ["arn:tg"]


def test_detach_load_balancer_target_groups():
    """Test detach target groups via mock (moto validates ARNs)."""
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        detach_load_balancer_target_groups(
            ASG_NAME,
            target_group_arns=["arn:tg"],
            region_name=REGION,
        )
    mock_client.detach_load_balancer_target_groups.assert_called_once()
    call_kwargs = mock_client.detach_load_balancer_target_groups.call_args[1]
    assert call_kwargs["TargetGroupARNs"] == ["arn:tg"]


def test_attach_load_balancer_target_groups_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.attach_load_balancer_target_groups.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "AttachLoadBalancerTargetGroups",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach target groups"):
        attach_load_balancer_target_groups(
            "asg", target_group_arns=["arn"], region_name=REGION
        )


def test_detach_load_balancer_target_groups_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.detach_load_balancer_target_groups.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DetachLoadBalancerTargetGroups",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach target groups"):
        detach_load_balancer_target_groups(
            "asg", target_group_arns=["arn"], region_name=REGION
        )


# ---------------------------------------------------------------------------
# Instance tests
# ---------------------------------------------------------------------------


def test_describe_auto_scaling_instances(asg):
    result = describe_auto_scaling_instances(region_name=REGION)
    assert isinstance(result, list)


def test_describe_auto_scaling_instances_by_id(asg):
    all_instances = describe_auto_scaling_instances(region_name=REGION)
    if all_instances:
        iid = all_instances[0]["InstanceId"]
        result = describe_auto_scaling_instances(
            instance_ids=[iid], region_name=REGION
        )
        assert len(result) >= 1


def test_describe_auto_scaling_instances_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.describe_auto_scaling_instances.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribeAutoScalingInstances",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_auto_scaling_instances failed"):
        describe_auto_scaling_instances(region_name=REGION)


def test_terminate_instance_in_auto_scaling_group(asg):
    instances = describe_auto_scaling_instances(region_name=REGION)
    if instances:
        iid = instances[0]["InstanceId"]
        result = terminate_instance_in_auto_scaling_group(
            iid, should_decrement=True, region_name=REGION
        )
        assert isinstance(result, dict)


def test_terminate_instance_in_asg_no_decrement(asg):
    """Test terminate with should_decrement=False."""
    instances = describe_auto_scaling_instances(region_name=REGION)
    if instances:
        iid = instances[0]["InstanceId"]
        result = terminate_instance_in_auto_scaling_group(
            iid, should_decrement=False, region_name=REGION
        )
        assert isinstance(result, dict)


def test_terminate_instance_in_asg_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.terminate_instance_in_auto_scaling_group.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "TerminateInstanceInAutoScalingGroup",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate instance"):
        terminate_instance_in_auto_scaling_group(
            "i-bad", region_name=REGION
        )


# ---------------------------------------------------------------------------
# Lifecycle hook tests
# ---------------------------------------------------------------------------


def test_put_lifecycle_hook(asg):
    put_lifecycle_hook(
        ASG_NAME,
        "my-hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
        heartbeat_timeout=300,
        default_result="CONTINUE",
        region_name=REGION,
    )
    hooks = describe_lifecycle_hooks(ASG_NAME, region_name=REGION)
    assert len(hooks) >= 1
    hook = [h for h in hooks if h.hook_name == "my-hook"][0]
    assert isinstance(hook, LifecycleHookResult)
    assert hook.asg_name == ASG_NAME
    assert hook.lifecycle_transition == "autoscaling:EC2_INSTANCE_LAUNCHING"
    assert hook.heartbeat_timeout == 300
    assert hook.default_result == "CONTINUE"


def test_put_lifecycle_hook_minimal(asg):
    put_lifecycle_hook(
        ASG_NAME,
        "minimal-hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_TERMINATING",
        region_name=REGION,
    )
    hooks = describe_lifecycle_hooks(
        ASG_NAME, hook_names=["minimal-hook"], region_name=REGION
    )
    assert len(hooks) == 1


def test_describe_lifecycle_hooks_by_name(asg):
    put_lifecycle_hook(
        ASG_NAME,
        "specific-hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
        region_name=REGION,
    )
    hooks = describe_lifecycle_hooks(
        ASG_NAME, hook_names=["specific-hook"], region_name=REGION
    )
    assert len(hooks) == 1
    assert hooks[0].hook_name == "specific-hook"


def test_complete_lifecycle_action(asg):
    put_lifecycle_hook(
        ASG_NAME,
        "action-hook",
        lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
        region_name=REGION,
    )
    # complete_lifecycle_action requires an instance_id or token;
    # moto may not fully support this, so we mock it.
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        complete_lifecycle_action(
            ASG_NAME,
            "action-hook",
            lifecycle_action_result="CONTINUE",
            instance_id="i-12345",
            region_name=REGION,
        )
    mock_client.complete_lifecycle_action.assert_called_once()


def test_complete_lifecycle_action_with_token():
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        complete_lifecycle_action(
            "asg",
            "hook",
            lifecycle_action_result="ABANDON",
            lifecycle_action_token="tok-123",
            region_name=REGION,
        )
    call_kwargs = mock_client.complete_lifecycle_action.call_args[1]
    assert call_kwargs["LifecycleActionToken"] == "tok-123"
    assert "InstanceId" not in call_kwargs


def test_put_lifecycle_hook_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.put_lifecycle_hook.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "PutLifecycleHook",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put lifecycle hook"):
        put_lifecycle_hook(
            "asg",
            "hook",
            lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
            region_name=REGION,
        )


def test_describe_lifecycle_hooks_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.describe_lifecycle_hooks.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribeLifecycleHooks",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_lifecycle_hooks failed"):
        describe_lifecycle_hooks("asg", region_name=REGION)


def test_complete_lifecycle_action_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.complete_lifecycle_action.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "CompleteLifecycleAction",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete lifecycle action"):
        complete_lifecycle_action(
            "asg",
            "hook",
            lifecycle_action_result="CONTINUE",
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Scaling activity tests
# ---------------------------------------------------------------------------


def test_describe_scaling_activities(asg):
    result = describe_scaling_activities(ASG_NAME, region_name=REGION)
    assert isinstance(result, list)
    # moto generates activities for ASG creation
    if result:
        assert all(isinstance(a, ScalingActivityResult) for a in result)
        assert result[0].asg_name == ASG_NAME


def test_describe_scaling_activities_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.describe_scaling_activities.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "DescribeScalingActivities",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_scaling_activities failed"):
        describe_scaling_activities("asg", region_name=REGION)


# ---------------------------------------------------------------------------
# Process suspension / resumption tests
# ---------------------------------------------------------------------------


def test_suspend_processes(asg):
    suspend_processes(
        ASG_NAME,
        scaling_processes=["Launch", "Terminate"],
        region_name=REGION,
    )
    # No error means success


def test_suspend_processes_all(asg):
    suspend_processes(ASG_NAME, region_name=REGION)


def test_resume_processes(asg):
    suspend_processes(
        ASG_NAME,
        scaling_processes=["Launch"],
        region_name=REGION,
    )
    resume_processes(
        ASG_NAME,
        scaling_processes=["Launch"],
        region_name=REGION,
    )


def test_resume_processes_all(asg):
    suspend_processes(ASG_NAME, region_name=REGION)
    resume_processes(ASG_NAME, region_name=REGION)


def test_suspend_processes_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.suspend_processes.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "SuspendProcesses",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to suspend processes"):
        suspend_processes("asg", region_name=REGION)


def test_resume_processes_error(monkeypatch):
    import aws_util.autoscaling as mod

    mock_client = MagicMock()
    mock_client.resume_processes.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "bad"}},
        "ResumeProcesses",
    )
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume processes"):
        resume_processes("asg", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_group tests
# ---------------------------------------------------------------------------


def test_wait_for_group(asg):
    result = wait_for_group(ASG_NAME, timeout=10, poll_interval=1, region_name=REGION)
    assert isinstance(result, AutoScalingGroupResult)
    assert result.name == ASG_NAME


def test_wait_for_group_not_found():
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_group(
            "nonexistent-asg",
            timeout=5,
            poll_interval=1,
            region_name=REGION,
        )


def test_wait_for_group_timeout(monkeypatch):
    import aws_util.autoscaling as mod

    # Return a group that never stabilises (instances never InService)
    monkeypatch.setattr(
        mod,
        "describe_auto_scaling_groups",
        lambda **kw: [
            AutoScalingGroupResult(
                name="timeout-asg",
                arn="arn:aws:autoscaling:us-east-1:123:autoScalingGroup:id:autoScalingGroupName/timeout-asg",
                min_size=1,
                max_size=1,
                desired_capacity=1,
                availability_zones=["us-east-1a"],
                instances=[{"InstanceId": "i-1", "LifecycleState": "Pending"}],
            )
        ],
    )
    # Use a very small timeout and patch time.sleep to not actually sleep
    monkeypatch.setattr("aws_util.autoscaling.time.sleep", lambda s: None)
    with pytest.raises(RuntimeError, match="did not stabilise"):
        wait_for_group(
            "timeout-asg",
            timeout=0.001,
            poll_interval=0.001,
            region_name=REGION,
        )


def test_wait_for_group_zero_desired(asg):
    """When desired_capacity=0 and no instances, should return immediately."""
    update_auto_scaling_group(
        ASG_NAME, desired_capacity=0, min_size=0, region_name=REGION
    )
    # Wait; moto may or may not have terminated instances, but desired=0
    # means we just need instances >= desired (0 >= 0).
    result = wait_for_group(
        ASG_NAME, timeout=10, poll_interval=1, region_name=REGION
    )
    assert result.desired_capacity == 0


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_autoscaling_group_result_model():
    model = AutoScalingGroupResult(
        name="test",
        arn="arn:aws:autoscaling:us-east-1:123:autoScalingGroup:id:autoScalingGroupName/test",
        min_size=0,
        max_size=1,
        desired_capacity=0,
        availability_zones=["us-east-1a"],
    )
    assert model.name == "test"
    assert model.launch_config_name is None
    assert model.launch_template is None
    assert model.status is None
    assert model.instances == []
    assert model.tags == {}
    assert model.extra == {}


def test_launch_configuration_result_model():
    model = LaunchConfigurationResult(
        name="lc",
        image_id="ami-123",
        instance_type="t2.micro",
        created_time="2024-01-01T00:00:00Z",
    )
    assert model.key_name is None
    assert model.security_groups == []
    assert model.extra == {}


def test_scaling_policy_result_model():
    model = ScalingPolicyResult(
        policy_name="pol",
        policy_arn="arn:policy",
        policy_type="SimpleScaling",
    )
    assert model.adjustment_type is None
    assert model.scaling_adjustment is None
    assert model.target_tracking_config is None
    assert model.extra == {}


def test_lifecycle_hook_result_model():
    model = LifecycleHookResult(
        hook_name="hook",
        asg_name="asg",
        lifecycle_transition="autoscaling:EC2_INSTANCE_LAUNCHING",
    )
    assert model.heartbeat_timeout is None
    assert model.default_result is None
    assert model.extra == {}


def test_scaling_activity_result_model():
    model = ScalingActivityResult(
        activity_id="act-123",
        asg_name="asg",
        cause="user request",
        status_code="Successful",
        start_time="2024-01-01T00:00:00Z",
    )
    assert model.description is None
    assert model.end_time is None
    assert model.extra == {}


# ---------------------------------------------------------------------------
# Parser branch coverage
# ---------------------------------------------------------------------------


def test_parse_asg_with_launch_template():
    """Exercise the LaunchTemplate branch in _parse_asg."""
    from aws_util.autoscaling import _parse_asg

    raw = {
        "AutoScalingGroupName": "lt-asg",
        "AutoScalingGroupARN": "arn:asg",
        "LaunchTemplate": {
            "LaunchTemplateId": "lt-123",
            "Version": "$Latest",
        },
        "MinSize": 1,
        "MaxSize": 3,
        "DesiredCapacity": 1,
        "AvailabilityZones": ["us-east-1a"],
        "Instances": [],
        "Tags": [{"Key": "env", "Value": "prod"}],
    }
    result = _parse_asg(raw)
    assert result.launch_template is not None
    assert result.launch_template["LaunchTemplateId"] == "lt-123"
    assert result.tags == {"env": "prod"}


def test_parse_scaling_policy_with_target_tracking():
    """Exercise the TargetTrackingConfiguration branch in _parse_scaling_policy."""
    from aws_util.autoscaling import _parse_scaling_policy

    raw = {
        "PolicyName": "tt-pol",
        "PolicyARN": "arn:pol",
        "PolicyType": "TargetTrackingScaling",
        "TargetTrackingConfiguration": {
            "PredefinedMetricSpecification": {
                "PredefinedMetricType": "ASGAverageCPUUtilization",
            },
            "TargetValue": 50.0,
        },
    }
    result = _parse_scaling_policy(raw)
    assert result.target_tracking_config is not None
    assert result.target_tracking_config["TargetValue"] == 50.0


def test_attach_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_instances.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    attach_instances("test-auto_scaling_group_name", region_name=REGION)
    mock_client.attach_instances.assert_called_once()


def test_attach_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_instances",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach instances"):
        attach_instances("test-auto_scaling_group_name", region_name=REGION)


def test_attach_load_balancers(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_load_balancers.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    attach_load_balancers("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.attach_load_balancers.assert_called_once()


def test_attach_load_balancers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_load_balancers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_load_balancers",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach load balancers"):
        attach_load_balancers("test-auto_scaling_group_name", [], region_name=REGION)


def test_attach_traffic_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_traffic_sources.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    attach_traffic_sources("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.attach_traffic_sources.assert_called_once()


def test_attach_traffic_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_traffic_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_traffic_sources",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach traffic sources"):
        attach_traffic_sources("test-auto_scaling_group_name", [], region_name=REGION)


def test_batch_delete_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    batch_delete_scheduled_action("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.batch_delete_scheduled_action.assert_called_once()


def test_batch_delete_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_scheduled_action",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete scheduled action"):
        batch_delete_scheduled_action("test-auto_scaling_group_name", [], region_name=REGION)


def test_batch_put_scheduled_update_group_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_scheduled_update_group_action.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    batch_put_scheduled_update_group_action("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.batch_put_scheduled_update_group_action.assert_called_once()


def test_batch_put_scheduled_update_group_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_scheduled_update_group_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_put_scheduled_update_group_action",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch put scheduled update group action"):
        batch_put_scheduled_update_group_action("test-auto_scaling_group_name", [], region_name=REGION)


def test_cancel_instance_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_instance_refresh.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    cancel_instance_refresh("test-auto_scaling_group_name", region_name=REGION)
    mock_client.cancel_instance_refresh.assert_called_once()


def test_cancel_instance_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_instance_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_instance_refresh",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel instance refresh"):
        cancel_instance_refresh("test-auto_scaling_group_name", region_name=REGION)


def test_create_or_update_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_or_update_tags.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    create_or_update_tags([], region_name=REGION)
    mock_client.create_or_update_tags.assert_called_once()


def test_create_or_update_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_or_update_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_or_update_tags",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create or update tags"):
        create_or_update_tags([], region_name=REGION)


def test_delete_lifecycle_hook(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lifecycle_hook.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_lifecycle_hook("test-lifecycle_hook_name", "test-auto_scaling_group_name", region_name=REGION)
    mock_client.delete_lifecycle_hook.assert_called_once()


def test_delete_lifecycle_hook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_lifecycle_hook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_lifecycle_hook",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete lifecycle hook"):
        delete_lifecycle_hook("test-lifecycle_hook_name", "test-auto_scaling_group_name", region_name=REGION)


def test_delete_notification_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", region_name=REGION)
    mock_client.delete_notification_configuration.assert_called_once()


def test_delete_notification_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_notification_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_notification_configuration",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete notification configuration"):
        delete_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", region_name=REGION)


def test_delete_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_scheduled_action("test-auto_scaling_group_name", "test-scheduled_action_name", region_name=REGION)
    mock_client.delete_scheduled_action.assert_called_once()


def test_delete_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_scheduled_action",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete scheduled action"):
        delete_scheduled_action("test-auto_scaling_group_name", "test-scheduled_action_name", region_name=REGION)


def test_delete_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_tags([], region_name=REGION)
    mock_client.delete_tags.assert_called_once()


def test_delete_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tags",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tags"):
        delete_tags([], region_name=REGION)


def test_delete_warm_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_warm_pool("test-auto_scaling_group_name", region_name=REGION)
    mock_client.delete_warm_pool.assert_called_once()


def test_delete_warm_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_warm_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_warm_pool",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete warm pool"):
        delete_warm_pool("test-auto_scaling_group_name", region_name=REGION)


def test_describe_account_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_account_limits(region_name=REGION)
    mock_client.describe_account_limits.assert_called_once()


def test_describe_account_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_limits",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account limits"):
        describe_account_limits(region_name=REGION)


def test_describe_adjustment_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_adjustment_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_adjustment_types(region_name=REGION)
    mock_client.describe_adjustment_types.assert_called_once()


def test_describe_adjustment_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_adjustment_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_adjustment_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe adjustment types"):
        describe_adjustment_types(region_name=REGION)


def test_describe_auto_scaling_notification_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_scaling_notification_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_auto_scaling_notification_types(region_name=REGION)
    mock_client.describe_auto_scaling_notification_types.assert_called_once()


def test_describe_auto_scaling_notification_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_scaling_notification_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_auto_scaling_notification_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe auto scaling notification types"):
        describe_auto_scaling_notification_types(region_name=REGION)


def test_describe_instance_refreshes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_refreshes.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_instance_refreshes("test-auto_scaling_group_name", region_name=REGION)
    mock_client.describe_instance_refreshes.assert_called_once()


def test_describe_instance_refreshes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_refreshes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_refreshes",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance refreshes"):
        describe_instance_refreshes("test-auto_scaling_group_name", region_name=REGION)


def test_describe_lifecycle_hook_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_lifecycle_hook_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_lifecycle_hook_types(region_name=REGION)
    mock_client.describe_lifecycle_hook_types.assert_called_once()


def test_describe_lifecycle_hook_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_lifecycle_hook_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_lifecycle_hook_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe lifecycle hook types"):
        describe_lifecycle_hook_types(region_name=REGION)


def test_describe_load_balancer_target_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancer_target_groups.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_load_balancer_target_groups("test-auto_scaling_group_name", region_name=REGION)
    mock_client.describe_load_balancer_target_groups.assert_called_once()


def test_describe_load_balancer_target_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancer_target_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_load_balancer_target_groups",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe load balancer target groups"):
        describe_load_balancer_target_groups("test-auto_scaling_group_name", region_name=REGION)


def test_describe_load_balancers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancers.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_load_balancers("test-auto_scaling_group_name", region_name=REGION)
    mock_client.describe_load_balancers.assert_called_once()


def test_describe_load_balancers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_load_balancers",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe load balancers"):
        describe_load_balancers("test-auto_scaling_group_name", region_name=REGION)


def test_describe_metric_collection_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_metric_collection_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_metric_collection_types(region_name=REGION)
    mock_client.describe_metric_collection_types.assert_called_once()


def test_describe_metric_collection_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_metric_collection_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_metric_collection_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe metric collection types"):
        describe_metric_collection_types(region_name=REGION)


def test_describe_notification_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_notification_configurations.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_notification_configurations(region_name=REGION)
    mock_client.describe_notification_configurations.assert_called_once()


def test_describe_notification_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_notification_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_notification_configurations",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe notification configurations"):
        describe_notification_configurations(region_name=REGION)


def test_describe_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_policies.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_policies(region_name=REGION)
    mock_client.describe_policies.assert_called_once()


def test_describe_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_policies",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe policies"):
        describe_policies(region_name=REGION)


def test_describe_scaling_process_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scaling_process_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_scaling_process_types(region_name=REGION)
    mock_client.describe_scaling_process_types.assert_called_once()


def test_describe_scaling_process_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scaling_process_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scaling_process_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scaling process types"):
        describe_scaling_process_types(region_name=REGION)


def test_describe_scheduled_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_actions(region_name=REGION)
    mock_client.describe_scheduled_actions.assert_called_once()


def test_describe_scheduled_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_actions",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scheduled actions"):
        describe_scheduled_actions(region_name=REGION)


def test_describe_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_tags(region_name=REGION)
    mock_client.describe_tags.assert_called_once()


def test_describe_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tags",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tags"):
        describe_tags(region_name=REGION)


def test_describe_termination_policy_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_termination_policy_types.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_termination_policy_types(region_name=REGION)
    mock_client.describe_termination_policy_types.assert_called_once()


def test_describe_termination_policy_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_termination_policy_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_termination_policy_types",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe termination policy types"):
        describe_termination_policy_types(region_name=REGION)


def test_describe_traffic_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_sources.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_traffic_sources("test-auto_scaling_group_name", region_name=REGION)
    mock_client.describe_traffic_sources.assert_called_once()


def test_describe_traffic_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_sources",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic sources"):
        describe_traffic_sources("test-auto_scaling_group_name", region_name=REGION)


def test_describe_warm_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_warm_pool("test-auto_scaling_group_name", region_name=REGION)
    mock_client.describe_warm_pool.assert_called_once()


def test_describe_warm_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_warm_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_warm_pool",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe warm pool"):
        describe_warm_pool("test-auto_scaling_group_name", region_name=REGION)


def test_detach_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_instances.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    detach_instances("test-auto_scaling_group_name", True, region_name=REGION)
    mock_client.detach_instances.assert_called_once()


def test_detach_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_instances",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach instances"):
        detach_instances("test-auto_scaling_group_name", True, region_name=REGION)


def test_detach_load_balancers(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_load_balancers.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    detach_load_balancers("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.detach_load_balancers.assert_called_once()


def test_detach_load_balancers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_load_balancers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_load_balancers",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach load balancers"):
        detach_load_balancers("test-auto_scaling_group_name", [], region_name=REGION)


def test_detach_traffic_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_traffic_sources.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    detach_traffic_sources("test-auto_scaling_group_name", [], region_name=REGION)
    mock_client.detach_traffic_sources.assert_called_once()


def test_detach_traffic_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_traffic_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_traffic_sources",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach traffic sources"):
        detach_traffic_sources("test-auto_scaling_group_name", [], region_name=REGION)


def test_disable_metrics_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_metrics_collection.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    disable_metrics_collection("test-auto_scaling_group_name", region_name=REGION)
    mock_client.disable_metrics_collection.assert_called_once()


def test_disable_metrics_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_metrics_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_metrics_collection",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable metrics collection"):
        disable_metrics_collection("test-auto_scaling_group_name", region_name=REGION)


def test_enable_metrics_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_metrics_collection.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    enable_metrics_collection("test-auto_scaling_group_name", "test-granularity", region_name=REGION)
    mock_client.enable_metrics_collection.assert_called_once()


def test_enable_metrics_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_metrics_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_metrics_collection",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable metrics collection"):
        enable_metrics_collection("test-auto_scaling_group_name", "test-granularity", region_name=REGION)


def test_enter_standby(monkeypatch):
    mock_client = MagicMock()
    mock_client.enter_standby.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    enter_standby("test-auto_scaling_group_name", True, region_name=REGION)
    mock_client.enter_standby.assert_called_once()


def test_enter_standby_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enter_standby.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enter_standby",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enter standby"):
        enter_standby("test-auto_scaling_group_name", True, region_name=REGION)


def test_execute_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_policy.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    execute_policy("test-policy_name", region_name=REGION)
    mock_client.execute_policy.assert_called_once()


def test_execute_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_policy",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute policy"):
        execute_policy("test-policy_name", region_name=REGION)


def test_exit_standby(monkeypatch):
    mock_client = MagicMock()
    mock_client.exit_standby.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    exit_standby("test-auto_scaling_group_name", region_name=REGION)
    mock_client.exit_standby.assert_called_once()


def test_exit_standby_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.exit_standby.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "exit_standby",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to exit standby"):
        exit_standby("test-auto_scaling_group_name", region_name=REGION)


def test_get_predictive_scaling_forecast(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_predictive_scaling_forecast.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    get_predictive_scaling_forecast("test-auto_scaling_group_name", "test-policy_name", "test-start_time", "test-end_time", region_name=REGION)
    mock_client.get_predictive_scaling_forecast.assert_called_once()


def test_get_predictive_scaling_forecast_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_predictive_scaling_forecast.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_predictive_scaling_forecast",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get predictive scaling forecast"):
        get_predictive_scaling_forecast("test-auto_scaling_group_name", "test-policy_name", "test-start_time", "test-end_time", region_name=REGION)


def test_put_notification_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_notification_configuration.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    put_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", [], region_name=REGION)
    mock_client.put_notification_configuration.assert_called_once()


def test_put_notification_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_notification_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_notification_configuration",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put notification configuration"):
        put_notification_configuration("test-auto_scaling_group_name", "test-topic_arn", [], region_name=REGION)


def test_put_scheduled_update_group_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_scheduled_update_group_action.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    put_scheduled_update_group_action("test-auto_scaling_group_name", "test-scheduled_action_name", region_name=REGION)
    mock_client.put_scheduled_update_group_action.assert_called_once()


def test_put_scheduled_update_group_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_scheduled_update_group_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_scheduled_update_group_action",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put scheduled update group action"):
        put_scheduled_update_group_action("test-auto_scaling_group_name", "test-scheduled_action_name", region_name=REGION)


def test_put_warm_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    put_warm_pool("test-auto_scaling_group_name", region_name=REGION)
    mock_client.put_warm_pool.assert_called_once()


def test_put_warm_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_warm_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_warm_pool",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put warm pool"):
        put_warm_pool("test-auto_scaling_group_name", region_name=REGION)


def test_record_lifecycle_action_heartbeat(monkeypatch):
    mock_client = MagicMock()
    mock_client.record_lifecycle_action_heartbeat.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    record_lifecycle_action_heartbeat("test-lifecycle_hook_name", "test-auto_scaling_group_name", region_name=REGION)
    mock_client.record_lifecycle_action_heartbeat.assert_called_once()


def test_record_lifecycle_action_heartbeat_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.record_lifecycle_action_heartbeat.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "record_lifecycle_action_heartbeat",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to record lifecycle action heartbeat"):
        record_lifecycle_action_heartbeat("test-lifecycle_hook_name", "test-auto_scaling_group_name", region_name=REGION)


def test_rollback_instance_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_instance_refresh.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    rollback_instance_refresh("test-auto_scaling_group_name", region_name=REGION)
    mock_client.rollback_instance_refresh.assert_called_once()


def test_rollback_instance_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_instance_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rollback_instance_refresh",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rollback instance refresh"):
        rollback_instance_refresh("test-auto_scaling_group_name", region_name=REGION)


def test_set_instance_health(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_instance_health.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    set_instance_health("test-instance_id", "test-health_status", region_name=REGION)
    mock_client.set_instance_health.assert_called_once()


def test_set_instance_health_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_instance_health.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_instance_health",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set instance health"):
        set_instance_health("test-instance_id", "test-health_status", region_name=REGION)


def test_set_instance_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_instance_protection.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    set_instance_protection([], "test-auto_scaling_group_name", True, region_name=REGION)
    mock_client.set_instance_protection.assert_called_once()


def test_set_instance_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_instance_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_instance_protection",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set instance protection"):
        set_instance_protection([], "test-auto_scaling_group_name", True, region_name=REGION)


def test_start_instance_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_instance_refresh.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    start_instance_refresh("test-auto_scaling_group_name", region_name=REGION)
    mock_client.start_instance_refresh.assert_called_once()


def test_start_instance_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_instance_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_instance_refresh",
    )
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start instance refresh"):
        start_instance_refresh("test-auto_scaling_group_name", region_name=REGION)


def test_update_auto_scaling_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import update_auto_scaling_group
    mock_client = MagicMock()
    mock_client.update_auto_scaling_group.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    update_auto_scaling_group("test-name", min_size=1, max_size=1, desired_capacity="test-desired_capacity", region_name="us-east-1")
    mock_client.update_auto_scaling_group.assert_called_once()

def test_suspend_processes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import suspend_processes
    mock_client = MagicMock()
    mock_client.suspend_processes.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    suspend_processes("test-asg_name", scaling_processes="test-scaling_processes", region_name="us-east-1")
    mock_client.suspend_processes.assert_called_once()

def test_resume_processes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import resume_processes
    mock_client = MagicMock()
    mock_client.resume_processes.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    resume_processes("test-asg_name", scaling_processes="test-scaling_processes", region_name="us-east-1")
    mock_client.resume_processes.assert_called_once()

def test_attach_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import attach_instances
    mock_client = MagicMock()
    mock_client.attach_instances.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    attach_instances(True, instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.attach_instances.assert_called_once()

def test_attach_traffic_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import attach_traffic_sources
    mock_client = MagicMock()
    mock_client.attach_traffic_sources.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    attach_traffic_sources(True, "test-traffic_sources", skip_zonal_shift_validation=True, region_name="us-east-1")
    mock_client.attach_traffic_sources.assert_called_once()

def test_cancel_instance_refresh_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import cancel_instance_refresh
    mock_client = MagicMock()
    mock_client.cancel_instance_refresh.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    cancel_instance_refresh(True, wait_for_transitioning_instances="test-wait_for_transitioning_instances", region_name="us-east-1")
    mock_client.cancel_instance_refresh.assert_called_once()

def test_delete_warm_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import delete_warm_pool
    mock_client = MagicMock()
    mock_client.delete_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    delete_warm_pool(True, force_delete=True, region_name="us-east-1")
    mock_client.delete_warm_pool.assert_called_once()

def test_describe_instance_refreshes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_instance_refreshes
    mock_client = MagicMock()
    mock_client.describe_instance_refreshes.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_instance_refreshes(True, instance_refresh_ids="test-instance_refresh_ids", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_instance_refreshes.assert_called_once()

def test_describe_load_balancer_target_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_load_balancer_target_groups
    mock_client = MagicMock()
    mock_client.describe_load_balancer_target_groups.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_load_balancer_target_groups(True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_load_balancer_target_groups.assert_called_once()

def test_describe_load_balancers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_load_balancers
    mock_client = MagicMock()
    mock_client.describe_load_balancers.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_load_balancers(True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_load_balancers.assert_called_once()

def test_describe_notification_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_notification_configurations
    mock_client = MagicMock()
    mock_client.describe_notification_configurations.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_notification_configurations(auto_scaling_group_names=True, next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_notification_configurations.assert_called_once()

def test_describe_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_policies
    mock_client = MagicMock()
    mock_client.describe_policies.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_policies(auto_scaling_group_name=True, policy_names="test-policy_names", policy_types="test-policy_types", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_policies.assert_called_once()

def test_describe_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_scheduled_actions
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_actions(auto_scaling_group_name=True, scheduled_action_names="test-scheduled_action_names", start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_scheduled_actions.assert_called_once()

def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_tags
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_tags(filters=[{}], next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_tags.assert_called_once()

def test_describe_traffic_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_traffic_sources
    mock_client = MagicMock()
    mock_client.describe_traffic_sources.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_traffic_sources(True, traffic_source_type="test-traffic_source_type", next_token="test-next_token", max_records=1, region_name="us-east-1")
    mock_client.describe_traffic_sources.assert_called_once()

def test_describe_warm_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import describe_warm_pool
    mock_client = MagicMock()
    mock_client.describe_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    describe_warm_pool(True, max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_warm_pool.assert_called_once()

def test_detach_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import detach_instances
    mock_client = MagicMock()
    mock_client.detach_instances.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    detach_instances(True, "test-should_decrement_desired_capacity", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.detach_instances.assert_called_once()

def test_disable_metrics_collection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import disable_metrics_collection
    mock_client = MagicMock()
    mock_client.disable_metrics_collection.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    disable_metrics_collection(True, metrics="test-metrics", region_name="us-east-1")
    mock_client.disable_metrics_collection.assert_called_once()

def test_enable_metrics_collection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import enable_metrics_collection
    mock_client = MagicMock()
    mock_client.enable_metrics_collection.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    enable_metrics_collection(True, "test-granularity", metrics="test-metrics", region_name="us-east-1")
    mock_client.enable_metrics_collection.assert_called_once()

def test_enter_standby_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import enter_standby
    mock_client = MagicMock()
    mock_client.enter_standby.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    enter_standby(True, "test-should_decrement_desired_capacity", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.enter_standby.assert_called_once()

def test_execute_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import execute_policy
    mock_client = MagicMock()
    mock_client.execute_policy.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    execute_policy("test-policy_name", auto_scaling_group_name=True, honor_cooldown="test-honor_cooldown", metric_value="test-metric_value", breach_threshold="test-breach_threshold", region_name="us-east-1")
    mock_client.execute_policy.assert_called_once()

def test_exit_standby_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import exit_standby
    mock_client = MagicMock()
    mock_client.exit_standby.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    exit_standby(True, instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.exit_standby.assert_called_once()

def test_put_scheduled_update_group_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import put_scheduled_update_group_action
    mock_client = MagicMock()
    mock_client.put_scheduled_update_group_action.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    put_scheduled_update_group_action(True, "test-scheduled_action_name", time="test-time", start_time="test-start_time", end_time="test-end_time", recurrence="test-recurrence", min_size=1, max_size=1, desired_capacity="test-desired_capacity", time_zone="test-time_zone", region_name="us-east-1")
    mock_client.put_scheduled_update_group_action.assert_called_once()

def test_put_warm_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import put_warm_pool
    mock_client = MagicMock()
    mock_client.put_warm_pool.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    put_warm_pool(True, max_group_prepared_capacity=1, min_size=1, pool_state="test-pool_state", instance_reuse_policy="{}", region_name="us-east-1")
    mock_client.put_warm_pool.assert_called_once()

def test_record_lifecycle_action_heartbeat_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import record_lifecycle_action_heartbeat
    mock_client = MagicMock()
    mock_client.record_lifecycle_action_heartbeat.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    record_lifecycle_action_heartbeat("test-lifecycle_hook_name", True, lifecycle_action_token="test-lifecycle_action_token", instance_id="test-instance_id", region_name="us-east-1")
    mock_client.record_lifecycle_action_heartbeat.assert_called_once()

def test_set_instance_health_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import set_instance_health
    mock_client = MagicMock()
    mock_client.set_instance_health.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    set_instance_health("test-instance_id", "test-health_status", should_respect_grace_period="test-should_respect_grace_period", region_name="us-east-1")
    mock_client.set_instance_health.assert_called_once()

def test_start_instance_refresh_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import start_instance_refresh
    mock_client = MagicMock()
    mock_client.start_instance_refresh.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    start_instance_refresh(True, strategy="test-strategy", desired_configuration={}, preferences="test-preferences", region_name="us-east-1")
    mock_client.start_instance_refresh.assert_called_once()


def test_create_launch_configuration_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import create_launch_configuration
    mock_client = MagicMock()
    mock_client.create_launch_configuration.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: mock_client)
    create_launch_configuration("test-name", image_id="ami-1", instance_type="t2.micro", security_groups=["sg-1"], region_name="us-east-1")
    mock_client.create_launch_configuration.assert_called_once()


def test_create_launch_configuration_key_name(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.autoscaling import create_launch_configuration
    m = MagicMock(); m.create_launch_configuration.return_value = {}
    monkeypatch.setattr("aws_util.autoscaling.get_client", lambda *a, **kw: m)
    create_launch_configuration("n", image_id="a", instance_type="t", key_name="k", security_groups=["s"], region_name="us-east-1")
