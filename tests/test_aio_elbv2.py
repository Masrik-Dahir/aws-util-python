"""Tests for aws_util.aio.elbv2 — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.elbv2 import (
    ListenerResult,
    LoadBalancerResult,
    RuleResult,
    TargetGroupResult,
    add_tags,
    create_listener,
    create_load_balancer,
    create_rule,
    create_target_group,
    delete_listener,
    delete_load_balancer,
    delete_rule,
    delete_target_group,
    deregister_targets,
    describe_listeners,
    describe_load_balancers,
    describe_rules,
    describe_tags,
    describe_target_groups,
    describe_target_health,
    ensure_load_balancer,
    ensure_target_group,
    modify_listener,
    modify_load_balancer_attributes,
    modify_rule,
    modify_target_group,
    register_targets,
    remove_tags,
    set_security_groups,
    set_subnets,
    wait_for_load_balancer,
    add_listener_certificates,
    add_trust_store_revocations,
    create_trust_store,
    delete_shared_trust_store_association,
    delete_trust_store,
    describe_account_limits,
    describe_capacity_reservation,
    describe_listener_attributes,
    describe_listener_certificates,
    describe_load_balancer_attributes,
    describe_ssl_policies,
    describe_target_group_attributes,
    describe_trust_store_associations,
    describe_trust_store_revocations,
    describe_trust_stores,
    get_resource_policy,
    get_trust_store_ca_certificates_bundle,
    get_trust_store_revocation_content,
    modify_capacity_reservation,
    modify_ip_pools,
    modify_listener_attributes,
    modify_target_group_attributes,
    modify_trust_store,
    remove_listener_certificates,
    remove_trust_store_revocations,
    set_ip_address_type,
    set_rule_priorities,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _lb_dict(
    arn: str = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234",
    name: str = "my-alb",
    state: str = "active",
) -> dict:
    return {
        "LoadBalancerArn": arn,
        "DNSName": "my-alb.elb.amazonaws.com",
        "LoadBalancerName": name,
        "Type": "application",
        "State": {"Code": state},
        "VpcId": "vpc-123",
        "Scheme": "internet-facing",
        "SecurityGroups": ["sg-123"],
        "AvailabilityZones": [{"ZoneName": "us-east-1a", "SubnetId": "sub-1"}],
        "CreatedTime": "2024-01-01T00:00:00Z",
        "CanonicalHostedZoneId": "Z123",
    }


def _tg_dict(
    arn: str = "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234",
    name: str = "my-tg",
) -> dict:
    return {
        "TargetGroupArn": arn,
        "TargetGroupName": name,
        "Protocol": "HTTP",
        "Port": 80,
        "VpcId": "vpc-123",
        "HealthCheckPath": "/health",
        "TargetType": "instance",
        "Matcher": {"HttpCode": "200"},
    }


def _listener_dict(
    arn: str = "arn:aws:elasticloadbalancing:us-east-1:123456789012:listener/app/my-alb/1234/5678",
    lb_arn: str = "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/my-alb/1234",
) -> dict:
    return {
        "ListenerArn": arn,
        "LoadBalancerArn": lb_arn,
        "Port": 80,
        "Protocol": "HTTP",
        "DefaultActions": [{"Type": "forward", "TargetGroupArn": "arn:tg"}],
        "SslPolicy": "ELBSecurityPolicy-2016-08",
    }


def _rule_dict(
    arn: str = "arn:aws:elasticloadbalancing:us-east-1:123456789012:listener-rule/app/my-alb/1234/5678/9012",
) -> dict:
    return {
        "RuleArn": arn,
        "Priority": "10",
        "Conditions": [{"Field": "path-pattern", "Values": ["/api/*"]}],
        "Actions": [{"Type": "forward", "TargetGroupArn": "arn:tg"}],
        "IsDefault": False,
    }


# ---------------------------------------------------------------------------
# create_load_balancer
# ---------------------------------------------------------------------------


async def test_create_load_balancer_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_load_balancer("my-alb", subnets=["sub-1", "sub-2"])
    assert isinstance(result, LoadBalancerResult)
    assert result.name == "my-alb"

async def test_create_load_balancer_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="denied"):
        await create_load_balancer("x", subnets=["s"])


async def test_create_load_balancer_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="create_load_balancer failed"):
        await create_load_balancer("x", subnets=["s"])


# ---------------------------------------------------------------------------
# describe_load_balancers
# ---------------------------------------------------------------------------


async def test_describe_load_balancers_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_load_balancers()
    assert len(result) == 1
    assert result[0].name == "my-alb"


async def test_describe_load_balancers_with_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_load_balancers(
        names=["my-alb"], arns=["arn:test"], region_name="us-east-1"
    )
    assert len(result) == 1
    kw = mock_client.call.call_args[1]
    assert "Names" in kw
    assert "LoadBalancerArns" in kw


async def test_describe_load_balancers_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"LoadBalancers": [_lb_dict(arn="arn:1", name="lb-1")], "NextMarker": "tok"},
        {"LoadBalancers": [_lb_dict(arn="arn:2", name="lb-2")]},
    ]
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_load_balancers()
    assert len(result) == 2


async def test_describe_load_balancers_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_load_balancers()
    assert result == []


async def test_describe_load_balancers_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="fail"):
        await describe_load_balancers()


async def test_describe_load_balancers_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_load_balancers failed"):
        await describe_load_balancers()


# ---------------------------------------------------------------------------
# modify_load_balancer_attributes
# ---------------------------------------------------------------------------


async def test_modify_lb_attributes_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Attributes": [{"Key": "idle_timeout.timeout_seconds", "Value": "120"}]
    }
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_load_balancer_attributes(
        "arn:lb", attributes=[{"Key": "idle_timeout.timeout_seconds", "Value": "120"}]
    )
    assert len(result) == 1


async def test_modify_lb_attributes_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await modify_load_balancer_attributes("arn:lb", attributes=[])


async def test_modify_lb_attributes_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="modify_load_balancer_attributes failed"):
        await modify_load_balancer_attributes("arn:lb", attributes=[])


# ---------------------------------------------------------------------------
# delete_load_balancer
# ---------------------------------------------------------------------------


async def test_delete_load_balancer_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await delete_load_balancer("arn:lb")
    mock_client.call.assert_awaited_once()


async def test_delete_load_balancer_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await delete_load_balancer("arn:lb")


async def test_delete_load_balancer_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="delete_load_balancer failed"):
        await delete_load_balancer("arn:lb")


# ---------------------------------------------------------------------------
# create_target_group
# ---------------------------------------------------------------------------


async def test_create_target_group_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_target_group("my-tg", vpc_id="vpc-123")
    assert isinstance(result, TargetGroupResult)
    assert result.name == "my-tg"


async def test_create_target_group_with_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_target_group(
        "my-tg", vpc_id="vpc-123", tags={"env": "test"}, region_name="us-east-1"
    )
    kw = mock_client.call.call_args[1]
    assert "Tags" in kw


async def test_create_target_group_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await create_target_group("x", vpc_id="vpc-1")


async def test_create_target_group_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="create_target_group failed"):
        await create_target_group("x", vpc_id="vpc-1")


# ---------------------------------------------------------------------------
# describe_target_groups
# ---------------------------------------------------------------------------


async def test_describe_target_groups_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_groups()
    assert len(result) == 1


async def test_describe_target_groups_with_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_groups(
        names=["tg"], arns=["arn:tg"], load_balancer_arn="arn:lb", region_name="us-east-1"
    )
    kw = mock_client.call.call_args[1]
    assert "Names" in kw
    assert "TargetGroupArns" in kw
    assert "LoadBalancerArn" in kw


async def test_describe_target_groups_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"TargetGroups": [_tg_dict(arn="arn:1", name="tg-1")], "NextMarker": "tok"},
        {"TargetGroups": [_tg_dict(arn="arn:2", name="tg-2")]},
    ]
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_groups()
    assert len(result) == 2


async def test_describe_target_groups_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_groups()
    assert result == []


async def test_describe_target_groups_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await describe_target_groups()


async def test_describe_target_groups_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_target_groups failed"):
        await describe_target_groups()


# ---------------------------------------------------------------------------
# modify_target_group
# ---------------------------------------------------------------------------


async def test_modify_target_group_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_target_group("arn:tg", health_check_path="/new")
    assert isinstance(result, TargetGroupResult)


async def test_modify_target_group_no_changes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_target_group("arn:tg")
    assert isinstance(result, TargetGroupResult)


async def test_modify_target_group_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await modify_target_group("arn:tg")


async def test_modify_target_group_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="modify_target_group failed"):
        await modify_target_group("arn:tg")


# ---------------------------------------------------------------------------
# delete_target_group
# ---------------------------------------------------------------------------


async def test_delete_target_group_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await delete_target_group("arn:tg")
    mock_client.call.assert_awaited_once()


async def test_delete_target_group_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await delete_target_group("arn:tg")


async def test_delete_target_group_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="delete_target_group failed"):
        await delete_target_group("arn:tg")


# ---------------------------------------------------------------------------
# register_targets
# ---------------------------------------------------------------------------


async def test_register_targets_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await register_targets("arn:tg", targets=[{"Id": "i-123", "Port": 80}])
    mock_client.call.assert_awaited_once()


async def test_register_targets_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await register_targets("arn:tg", targets=[{"Id": "i-1"}])


async def test_register_targets_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="register_targets failed"):
        await register_targets("arn:tg", targets=[{"Id": "i-1"}])


# ---------------------------------------------------------------------------
# deregister_targets
# ---------------------------------------------------------------------------


async def test_deregister_targets_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await deregister_targets("arn:tg", targets=[{"Id": "i-123"}])
    mock_client.call.assert_awaited_once()


async def test_deregister_targets_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await deregister_targets("arn:tg", targets=[{"Id": "i-1"}])


async def test_deregister_targets_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="deregister_targets failed"):
        await deregister_targets("arn:tg", targets=[{"Id": "i-1"}])


# ---------------------------------------------------------------------------
# describe_target_health
# ---------------------------------------------------------------------------


async def test_describe_target_health_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TargetHealthDescriptions": [
            {"Target": {"Id": "i-123", "Port": 80}, "TargetHealth": {"State": "healthy"}}
        ]
    }
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_health("arn:tg")
    assert len(result) == 1


async def test_describe_target_health_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetHealthDescriptions": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_target_health("arn:tg")
    assert result == []


async def test_describe_target_health_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await describe_target_health("arn:tg")


async def test_describe_target_health_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_target_health failed"):
        await describe_target_health("arn:tg")


# ---------------------------------------------------------------------------
# create_listener
# ---------------------------------------------------------------------------


async def test_create_listener_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_listener(
        "arn:lb", default_actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}]
    )
    assert isinstance(result, ListenerResult)
    assert result.port == 80


async def test_create_listener_with_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_listener(
        "arn:lb",
        default_actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}],
        tags={"env": "test"},
        region_name="us-east-1",
    )
    kw = mock_client.call.call_args[1]
    assert "Tags" in kw


async def test_create_listener_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await create_listener("arn:lb", default_actions=[])


async def test_create_listener_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="create_listener failed"):
        await create_listener("arn:lb", default_actions=[])


# ---------------------------------------------------------------------------
# describe_listeners
# ---------------------------------------------------------------------------


async def test_describe_listeners_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_listeners("arn:lb")
    assert len(result) == 1


async def test_describe_listeners_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Listeners": [_listener_dict(arn="arn:ln1")], "NextMarker": "tok"},
        {"Listeners": [_listener_dict(arn="arn:ln2")]},
    ]
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_listeners("arn:lb")
    assert len(result) == 2


async def test_describe_listeners_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_listeners("arn:lb")
    assert result == []


async def test_describe_listeners_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await describe_listeners("arn:lb")


async def test_describe_listeners_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_listeners failed"):
        await describe_listeners("arn:lb")


# ---------------------------------------------------------------------------
# modify_listener
# ---------------------------------------------------------------------------


async def test_modify_listener_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_listener("arn:ln", port=8080, protocol="HTTPS")
    assert isinstance(result, ListenerResult)


async def test_modify_listener_default_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_listener(
        "arn:ln",
        default_actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}],
    )
    assert isinstance(result, ListenerResult)


async def test_modify_listener_no_changes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Listeners": [_listener_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_listener("arn:ln")
    assert isinstance(result, ListenerResult)


async def test_modify_listener_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await modify_listener("arn:ln")


async def test_modify_listener_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="modify_listener failed"):
        await modify_listener("arn:ln")


# ---------------------------------------------------------------------------
# delete_listener
# ---------------------------------------------------------------------------


async def test_delete_listener_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await delete_listener("arn:ln")
    mock_client.call.assert_awaited_once()


async def test_delete_listener_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await delete_listener("arn:ln")


async def test_delete_listener_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="delete_listener failed"):
        await delete_listener("arn:ln")


# ---------------------------------------------------------------------------
# create_rule
# ---------------------------------------------------------------------------


async def test_create_rule_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": [_rule_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_rule(
        "arn:ln",
        conditions=[{"Field": "path-pattern", "Values": ["/api/*"]}],
        actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}],
        priority=10,
    )
    assert isinstance(result, RuleResult)


async def test_create_rule_with_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": [_rule_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await create_rule(
        "arn:ln",
        conditions=[],
        actions=[],
        priority=1,
        tags={"env": "test"},
        region_name="us-east-1",
    )
    kw = mock_client.call.call_args[1]
    assert "Tags" in kw


async def test_create_rule_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await create_rule("arn:ln", conditions=[], actions=[], priority=1)


async def test_create_rule_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="create_rule failed"):
        await create_rule("arn:ln", conditions=[], actions=[], priority=1)


# ---------------------------------------------------------------------------
# describe_rules
# ---------------------------------------------------------------------------


async def test_describe_rules_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": [_rule_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_rules("arn:ln")
    assert len(result) == 1


async def test_describe_rules_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Rules": [_rule_dict(arn="arn:r1")], "NextMarker": "tok"},
        {"Rules": [_rule_dict(arn="arn:r2")]},
    ]
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_rules("arn:ln")
    assert len(result) == 2


async def test_describe_rules_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_rules("arn:ln")
    assert result == []


async def test_describe_rules_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await describe_rules("arn:ln")


async def test_describe_rules_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_rules failed"):
        await describe_rules("arn:ln")


# ---------------------------------------------------------------------------
# modify_rule
# ---------------------------------------------------------------------------


async def test_modify_rule_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": [_rule_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_rule(
        "arn:rule",
        conditions=[{"Field": "path-pattern", "Values": ["/new/*"]}],
        actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}],
    )
    assert isinstance(result, RuleResult)


async def test_modify_rule_no_changes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Rules": [_rule_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await modify_rule("arn:rule")
    assert isinstance(result, RuleResult)


async def test_modify_rule_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await modify_rule("arn:rule")


async def test_modify_rule_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="modify_rule failed"):
        await modify_rule("arn:rule")


# ---------------------------------------------------------------------------
# delete_rule
# ---------------------------------------------------------------------------


async def test_delete_rule_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await delete_rule("arn:rule")
    mock_client.call.assert_awaited_once()


async def test_delete_rule_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await delete_rule("arn:rule")


async def test_delete_rule_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = IOError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="delete_rule failed"):
        await delete_rule("arn:rule")


# ---------------------------------------------------------------------------
# set_subnets
# ---------------------------------------------------------------------------


async def test_set_subnets_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "AvailabilityZones": [{"ZoneName": "us-east-1a", "SubnetId": "sub-1"}]
    }
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await set_subnets("arn:lb", subnets=["sub-1", "sub-2"])
    assert len(result) == 1


async def test_set_subnets_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await set_subnets("arn:lb", subnets=["sub-1"])


async def test_set_subnets_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="set_subnets failed"):
        await set_subnets("arn:lb", subnets=["sub-1"])


# ---------------------------------------------------------------------------
# set_security_groups
# ---------------------------------------------------------------------------


async def test_set_security_groups_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"SecurityGroupIds": ["sg-1", "sg-2"]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await set_security_groups("arn:lb", security_groups=["sg-1", "sg-2"])
    assert result == ["sg-1", "sg-2"]


async def test_set_security_groups_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await set_security_groups("arn:lb", security_groups=["sg-1"])


async def test_set_security_groups_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="set_security_groups failed"):
        await set_security_groups("arn:lb", security_groups=["sg-1"])


# ---------------------------------------------------------------------------
# add_tags
# ---------------------------------------------------------------------------


async def test_add_tags_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await add_tags(["arn:lb"], tags={"env": "prod"})
    mock_client.call.assert_awaited_once()


async def test_add_tags_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await add_tags(["arn:lb"], tags={"k": "v"})


async def test_add_tags_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="add_tags failed"):
        await add_tags(["arn:lb"], tags={"k": "v"})


# ---------------------------------------------------------------------------
# remove_tags
# ---------------------------------------------------------------------------


async def test_remove_tags_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    await remove_tags(["arn:lb"], tag_keys=["env"])
    mock_client.call.assert_awaited_once()


async def test_remove_tags_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await remove_tags(["arn:lb"], tag_keys=["k"])


async def test_remove_tags_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="remove_tags failed"):
        await remove_tags(["arn:lb"], tag_keys=["k"])


# ---------------------------------------------------------------------------
# describe_tags
# ---------------------------------------------------------------------------


async def test_describe_tags_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TagDescriptions": [
            {
                "ResourceArn": "arn:lb",
                "Tags": [{"Key": "env", "Value": "prod"}],
            }
        ]
    }
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_tags(["arn:lb"])
    assert "arn:lb" in result
    assert result["arn:lb"]["env"] == "prod"


async def test_describe_tags_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TagDescriptions": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await describe_tags(["arn:lb"])
    assert result == {}


async def test_describe_tags_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="err"):
        await describe_tags(["arn:lb"])


async def test_describe_tags_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="describe_tags failed"):
        await describe_tags(["arn:lb"])


# ---------------------------------------------------------------------------
# wait_for_load_balancer
# ---------------------------------------------------------------------------


async def test_wait_for_lb_already_active(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict(state="active")]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result = await wait_for_load_balancer("arn:lb")
    assert result.state == "active"


async def test_wait_for_lb_becomes_active(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"LoadBalancers": [_lb_dict(state="provisioning")]},
        {"LoadBalancers": [_lb_dict(state="active")]},
    ]
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with patch("aws_util.aio.elbv2.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_load_balancer("arn:lb", timeout=300, poll_interval=0.01)
    assert result.state == "active"


async def test_wait_for_lb_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": []}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_load_balancer("arn:lb")


async def test_wait_for_lb_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict(state="provisioning")]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    with patch("aws_util.aio.elbv2.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(RuntimeError, match="did not reach"):
            await wait_for_load_balancer("arn:lb", timeout=0.0, poll_interval=0.001)


# ---------------------------------------------------------------------------
# ensure_load_balancer
# ---------------------------------------------------------------------------


async def test_ensure_lb_creates_new(monkeypatch):
    call_count = 0
    mock_client = AsyncMock()

    async def mock_call(op, **kwargs):
        nonlocal call_count
        call_count += 1
        if op == "DescribeLoadBalancers":
            raise ValueError("not found")
        return {"LoadBalancers": [_lb_dict()]}

    mock_client.call = mock_call
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result, created = await ensure_load_balancer("my-alb", subnets=["sub-1"])
    assert created is True


async def test_ensure_lb_returns_existing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"LoadBalancers": [_lb_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result, created = await ensure_load_balancer("my-alb", subnets=["sub-1"])
    assert created is False
    assert result.name == "my-alb"

async def test_ensure_tg_creates_new(monkeypatch):
    mock_client = AsyncMock()

    async def mock_call(op, **kwargs):
        if op == "DescribeTargetGroups":
            raise ValueError("not found")
        return {"TargetGroups": [_tg_dict()]}

    mock_client.call = mock_call
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result, created = await ensure_target_group("my-tg", vpc_id="vpc-123")
    assert created is True


async def test_ensure_tg_returns_existing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"TargetGroups": [_tg_dict()]}
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", _mock_factory(mock_client))
    result, created = await ensure_target_group("my-tg", vpc_id="vpc-123")
    assert created is False
    assert result.name == "my-tg"

async def test_reexported_models():
    """Verify models are properly re-exported from async module."""
    assert LoadBalancerResult is not None
    assert TargetGroupResult is not None
    assert ListenerResult is not None
    assert RuleResult is not None


async def test_add_listener_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_listener_certificates("test-listener_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_listener_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_listener_certificates("test-listener_arn", [], )


async def test_add_trust_store_revocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_trust_store_revocations("test-trust_store_arn", )
    mock_client.call.assert_called_once()


async def test_add_trust_store_revocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_trust_store_revocations("test-trust_store_arn", )


async def test_create_trust_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", )
    mock_client.call.assert_called_once()


async def test_create_trust_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", )


async def test_delete_shared_trust_store_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_shared_trust_store_association("test-trust_store_arn", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_shared_trust_store_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_shared_trust_store_association("test-trust_store_arn", "test-resource_arn", )


async def test_delete_trust_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_trust_store("test-trust_store_arn", )
    mock_client.call.assert_called_once()


async def test_delete_trust_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_trust_store("test-trust_store_arn", )


async def test_describe_account_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_limits()
    mock_client.call.assert_called_once()


async def test_describe_account_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_limits()


async def test_describe_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_reservation("test-load_balancer_arn", )
    mock_client.call.assert_called_once()


async def test_describe_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_reservation("test-load_balancer_arn", )


async def test_describe_listener_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_listener_attributes("test-listener_arn", )
    mock_client.call.assert_called_once()


async def test_describe_listener_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_listener_attributes("test-listener_arn", )


async def test_describe_listener_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_listener_certificates("test-listener_arn", )
    mock_client.call.assert_called_once()


async def test_describe_listener_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_listener_certificates("test-listener_arn", )


async def test_describe_load_balancer_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_load_balancer_attributes("test-load_balancer_arn", )
    mock_client.call.assert_called_once()


async def test_describe_load_balancer_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_load_balancer_attributes("test-load_balancer_arn", )


async def test_describe_ssl_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ssl_policies()
    mock_client.call.assert_called_once()


async def test_describe_ssl_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ssl_policies()


async def test_describe_target_group_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_target_group_attributes("test-target_group_arn", )
    mock_client.call.assert_called_once()


async def test_describe_target_group_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_target_group_attributes("test-target_group_arn", )


async def test_describe_trust_store_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_trust_store_associations("test-trust_store_arn", )
    mock_client.call.assert_called_once()


async def test_describe_trust_store_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_trust_store_associations("test-trust_store_arn", )


async def test_describe_trust_store_revocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_trust_store_revocations("test-trust_store_arn", )
    mock_client.call.assert_called_once()


async def test_describe_trust_store_revocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_trust_store_revocations("test-trust_store_arn", )


async def test_describe_trust_stores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_trust_stores()
    mock_client.call.assert_called_once()


async def test_describe_trust_stores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_trust_stores()


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_get_trust_store_ca_certificates_bundle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_trust_store_ca_certificates_bundle("test-trust_store_arn", )
    mock_client.call.assert_called_once()


async def test_get_trust_store_ca_certificates_bundle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_trust_store_ca_certificates_bundle("test-trust_store_arn", )


async def test_get_trust_store_revocation_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_trust_store_revocation_content("test-trust_store_arn", 1, )
    mock_client.call.assert_called_once()


async def test_get_trust_store_revocation_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_trust_store_revocation_content("test-trust_store_arn", 1, )


async def test_modify_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_capacity_reservation("test-load_balancer_arn", )
    mock_client.call.assert_called_once()


async def test_modify_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_capacity_reservation("test-load_balancer_arn", )


async def test_modify_ip_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ip_pools("test-load_balancer_arn", )
    mock_client.call.assert_called_once()


async def test_modify_ip_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ip_pools("test-load_balancer_arn", )


async def test_modify_listener_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_listener_attributes("test-listener_arn", [], )
    mock_client.call.assert_called_once()


async def test_modify_listener_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_listener_attributes("test-listener_arn", [], )


async def test_modify_target_group_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_target_group_attributes("test-target_group_arn", [], )
    mock_client.call.assert_called_once()


async def test_modify_target_group_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_target_group_attributes("test-target_group_arn", [], )


async def test_modify_trust_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", )
    mock_client.call.assert_called_once()


async def test_modify_trust_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", )


async def test_remove_listener_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_listener_certificates("test-listener_arn", [], )
    mock_client.call.assert_called_once()


async def test_remove_listener_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_listener_certificates("test-listener_arn", [], )


async def test_remove_trust_store_revocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_trust_store_revocations("test-trust_store_arn", [], )
    mock_client.call.assert_called_once()


async def test_remove_trust_store_revocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_trust_store_revocations("test-trust_store_arn", [], )


async def test_set_ip_address_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_ip_address_type("test-load_balancer_arn", "test-ip_address_type", )
    mock_client.call.assert_called_once()


async def test_set_ip_address_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_ip_address_type("test-load_balancer_arn", "test-ip_address_type", )


async def test_set_rule_priorities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_rule_priorities([], )
    mock_client.call.assert_called_once()


async def test_set_rule_priorities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elbv2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_rule_priorities([], )


@pytest.mark.asyncio
async def test_add_trust_store_revocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import add_trust_store_revocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await add_trust_store_revocations("test-trust_store_arn", revocation_contents="test-revocation_contents", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_trust_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import create_trust_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", ca_certificates_bundle_s3_object_version="test-ca_certificates_bundle_s3_object_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_limits_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_account_limits
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_account_limits(marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_listener_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_listener_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_listener_certificates("test-listener_arn", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ssl_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_ssl_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_ssl_policies(names="test-names", marker="test-marker", page_size=1, load_balancer_type="test-load_balancer_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_trust_store_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_trust_store_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_trust_store_associations("test-trust_store_arn", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_trust_store_revocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_trust_store_revocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_trust_store_revocations("test-trust_store_arn", revocation_ids="test-revocation_ids", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_trust_stores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import describe_trust_stores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await describe_trust_stores(trust_store_arns="test-trust_store_arns", names="test-names", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import modify_capacity_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await modify_capacity_reservation("test-load_balancer_arn", minimum_load_balancer_capacity="test-minimum_load_balancer_capacity", reset_capacity_reservation="test-reset_capacity_reservation", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ip_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import modify_ip_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await modify_ip_pools("test-load_balancer_arn", ipam_pools="test-ipam_pools", remove_ipam_pools="test-remove_ipam_pools", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_trust_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import modify_trust_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: mock_client)
    await modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", ca_certificates_bundle_s3_object_version="test-ca_certificates_bundle_s3_object_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_load_balancer_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import create_load_balancer
    m = AsyncMock(); m.call = AsyncMock(return_value={"LoadBalancers": [{"LoadBalancerArn": "arn"}]})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: m)
    await create_load_balancer("lb", subnets=["sn-1"], tags={"k": "v"}, region_name="us-east-1")

@pytest.mark.asyncio
async def test_create_load_balancer_security_groups(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elbv2 import create_load_balancer
    m = AsyncMock(); m.call = AsyncMock(return_value={"LoadBalancers": [{"LoadBalancerArn": "arn"}]})
    monkeypatch.setattr("aws_util.aio.elbv2.async_client", lambda *a, **kw: m)
    await create_load_balancer("lb", subnets=["sn-1"], security_groups=["sg-1"], tags={"k": "v"}, region_name="us-east-1")
