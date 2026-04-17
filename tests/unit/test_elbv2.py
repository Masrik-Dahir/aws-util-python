"""Tests for aws_util.elbv2 module."""
from __future__ import annotations

from unittest.mock import MagicMock

import boto3
import pytest
from botocore.exceptions import ClientError

from aws_util.elbv2 import (
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Fixtures — VPC, subnets, security groups (required by ELBv2)
# ---------------------------------------------------------------------------


@pytest.fixture
def vpc_env():
    """Create a VPC with two subnets in different AZs and a security group."""
    ec2 = boto3.client("ec2", region_name=REGION)
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    subnet1 = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock="10.0.1.0/24", AvailabilityZone="us-east-1a"
    )
    subnet2 = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock="10.0.2.0/24", AvailabilityZone="us-east-1b"
    )
    sg = ec2.create_security_group(
        GroupName="test-sg", Description="Test SG", VpcId=vpc_id
    )
    return {
        "vpc_id": vpc_id,
        "subnet_ids": [subnet1["Subnet"]["SubnetId"], subnet2["Subnet"]["SubnetId"]],
        "sg_id": sg["GroupId"],
    }


@pytest.fixture
def lb(vpc_env):
    """Create a test ALB."""
    result = create_load_balancer(
        "test-alb",
        subnets=vpc_env["subnet_ids"],
        security_groups=[vpc_env["sg_id"]],
        scheme="internet-facing",
        type="application",
        region_name=REGION,
    )
    return result


@pytest.fixture
def tg(vpc_env):
    """Create a test target group."""
    result = create_target_group(
        "test-tg",
        protocol="HTTP",
        port=80,
        vpc_id=vpc_env["vpc_id"],
        health_check_path="/health",
        target_type="instance",
        region_name=REGION,
    )
    return result


@pytest.fixture
def listener(lb, tg):
    """Create a test listener."""
    result = create_listener(
        lb.arn,
        port=80,
        protocol="HTTP",
        default_actions=[
            {"Type": "forward", "TargetGroupArn": tg.arn}
        ],
        region_name=REGION,
    )
    return result


# ---------------------------------------------------------------------------
# Load Balancer tests
# ---------------------------------------------------------------------------


class TestCreateLoadBalancer:
    def test_basic(self, vpc_env):
        result = create_load_balancer(
            "my-alb",
            subnets=vpc_env["subnet_ids"],
            security_groups=[vpc_env["sg_id"]],
            region_name=REGION,
        )
        assert isinstance(result, LoadBalancerResult)
        assert result.name == "my-alb"
        assert result.arn

    def test_with_tags(self, vpc_env):
        result = create_load_balancer(
            "tagged-alb",
            subnets=vpc_env["subnet_ids"],
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.name == "tagged-alb"

    def test_without_security_groups(self, vpc_env):
        result = create_load_balancer(
            "no-sg-alb",
            subnets=vpc_env["subnet_ids"],
            region_name=REGION,
        )
        assert isinstance(result, LoadBalancerResult)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.create_load_balancer.side_effect = ClientError(
            {"Error": {"Code": "DuplicateLoadBalancerName", "Message": "dup"}},
            "CreateLoadBalancer",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_load_balancer failed"):
            create_load_balancer("dup", subnets=["sub-1"], region_name=REGION)


class TestDescribeLoadBalancers:
    def test_all(self, lb):
        results = describe_load_balancers(region_name=REGION)
        assert len(results) >= 1
        assert all(isinstance(r, LoadBalancerResult) for r in results)

    def test_by_name(self, lb):
        results = describe_load_balancers(names=["test-alb"], region_name=REGION)
        assert len(results) == 1
        assert results[0].name == "test-alb"

    def test_by_arn(self, lb):
        results = describe_load_balancers(arns=[lb.arn], region_name=REGION)
        assert len(results) == 1
        assert results[0].arn == lb.arn

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "DescribeLoadBalancers",
        )
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_load_balancers failed"):
            describe_load_balancers(region_name=REGION)


class TestModifyLoadBalancerAttributes:
    def test_basic(self, lb):
        result = modify_load_balancer_attributes(
            lb.arn,
            attributes=[
                {"Key": "idle_timeout.timeout_seconds", "Value": "120"}
            ],
            region_name=REGION,
        )
        assert isinstance(result, list)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.modify_load_balancer_attributes.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "ModifyLoadBalancerAttributes",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="modify_load_balancer_attributes failed"):
            modify_load_balancer_attributes(
                "arn:fake", attributes=[{"Key": "k", "Value": "v"}], region_name=REGION
            )


class TestDeleteLoadBalancer:
    def test_basic(self, lb):
        delete_load_balancer(lb.arn, region_name=REGION)
        results = describe_load_balancers(region_name=REGION)
        assert all(r.arn != lb.arn for r in results)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.delete_load_balancer.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "DeleteLoadBalancer",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_load_balancer failed"):
            delete_load_balancer("arn:fake", region_name=REGION)


# ---------------------------------------------------------------------------
# Target Group tests
# ---------------------------------------------------------------------------


class TestCreateTargetGroup:
    def test_basic(self, vpc_env):
        result = create_target_group(
            "my-tg",
            protocol="HTTP",
            port=80,
            vpc_id=vpc_env["vpc_id"],
            region_name=REGION,
        )
        assert isinstance(result, TargetGroupResult)
        assert result.name == "my-tg"
        assert result.port == 80

    def test_with_tags(self, vpc_env):
        result = create_target_group(
            "tagged-tg",
            vpc_id=vpc_env["vpc_id"],
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.name == "tagged-tg"

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.create_target_group.side_effect = ClientError(
            {"Error": {"Code": "DuplicateTargetGroupName", "Message": "dup"}},
            "CreateTargetGroup",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_target_group failed"):
            create_target_group("dup", vpc_id="vpc-1", region_name=REGION)


class TestDescribeTargetGroups:
    def test_all(self, tg):
        results = describe_target_groups(region_name=REGION)
        assert len(results) >= 1

    def test_by_name(self, tg):
        results = describe_target_groups(names=["test-tg"], region_name=REGION)
        assert len(results) == 1
        assert results[0].name == "test-tg"

    def test_by_arn(self, tg):
        results = describe_target_groups(arns=[tg.arn], region_name=REGION)
        assert len(results) == 1

    def test_by_lb_arn(self, lb, tg, listener):
        results = describe_target_groups(
            load_balancer_arn=lb.arn, region_name=REGION
        )
        assert len(results) >= 1

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "DescribeTargetGroups",
        )
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_target_groups failed"):
            describe_target_groups(region_name=REGION)


class TestModifyTargetGroup:
    def test_health_check_path(self, tg):
        result = modify_target_group(
            tg.arn, health_check_path="/new-health", region_name=REGION
        )
        assert isinstance(result, TargetGroupResult)
        assert result.health_check_path == "/new-health"

    def test_no_changes(self, tg):
        result = modify_target_group(tg.arn, region_name=REGION)
        assert isinstance(result, TargetGroupResult)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.modify_target_group.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "ModifyTargetGroup",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="modify_target_group failed"):
            modify_target_group("arn:fake", region_name=REGION)


class TestDeleteTargetGroup:
    def test_basic(self, tg):
        delete_target_group(tg.arn, region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.delete_target_group.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "DeleteTargetGroup",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_target_group failed"):
            delete_target_group("arn:fake", region_name=REGION)


# ---------------------------------------------------------------------------
# Target registration tests
# ---------------------------------------------------------------------------


class TestRegisterTargets:
    def test_basic(self, tg):
        # Register an instance target (moto allows any ID)
        register_targets(
            tg.arn,
            targets=[{"Id": "i-12345678", "Port": 80}],
            region_name=REGION,
        )

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.register_targets.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "RegisterTargets",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="register_targets failed"):
            register_targets("arn:fake", targets=[{"Id": "i-1"}], region_name=REGION)


class TestDeregisterTargets:
    def test_basic(self, tg):
        register_targets(
            tg.arn,
            targets=[{"Id": "i-12345678", "Port": 80}],
            region_name=REGION,
        )
        deregister_targets(
            tg.arn,
            targets=[{"Id": "i-12345678", "Port": 80}],
            region_name=REGION,
        )

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.deregister_targets.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "DeregisterTargets",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="deregister_targets failed"):
            deregister_targets(
                "arn:fake", targets=[{"Id": "i-1"}], region_name=REGION
            )


class TestDescribeTargetHealth:
    def test_basic(self, tg):
        result = describe_target_health(tg.arn, region_name=REGION)
        assert isinstance(result, list)

    def test_with_targets(self, tg):
        register_targets(
            tg.arn,
            targets=[{"Id": "i-12345678", "Port": 80}],
            region_name=REGION,
        )
        result = describe_target_health(tg.arn, region_name=REGION)
        assert isinstance(result, list)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.describe_target_health.side_effect = ClientError(
            {"Error": {"Code": "TargetGroupNotFound", "Message": "nope"}},
            "DescribeTargetHealth",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_target_health failed"):
            describe_target_health("arn:fake", region_name=REGION)


# ---------------------------------------------------------------------------
# Listener tests
# ---------------------------------------------------------------------------


class TestCreateListener:
    def test_basic(self, lb, tg):
        result = create_listener(
            lb.arn,
            port=80,
            protocol="HTTP",
            default_actions=[
                {"Type": "forward", "TargetGroupArn": tg.arn}
            ],
            region_name=REGION,
        )
        assert isinstance(result, ListenerResult)
        assert result.port == 80

    def test_with_tags(self, lb, tg):
        result = create_listener(
            lb.arn,
            port=8080,
            protocol="HTTP",
            default_actions=[
                {"Type": "forward", "TargetGroupArn": tg.arn}
            ],
            tags={"env": "test"},
            region_name=REGION,
        )
        assert isinstance(result, ListenerResult)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.create_listener.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "CreateListener",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_listener failed"):
            create_listener(
                "arn:fake",
                default_actions=[{"Type": "forward", "TargetGroupArn": "arn:tg"}],
                region_name=REGION,
            )


class TestDescribeListeners:
    def test_basic(self, lb, listener):
        results = describe_listeners(lb.arn, region_name=REGION)
        assert len(results) >= 1
        assert all(isinstance(r, ListenerResult) for r in results)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "DescribeListeners",
        )
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_listeners failed"):
            describe_listeners("arn:fake", region_name=REGION)


class TestModifyListener:
    def test_port(self, listener, lb, tg):
        result = modify_listener(
            listener.arn,
            port=8080,
            region_name=REGION,
        )
        assert isinstance(result, ListenerResult)

    def test_protocol(self, listener, lb, tg):
        result = modify_listener(
            listener.arn,
            protocol="HTTP",
            region_name=REGION,
        )
        assert isinstance(result, ListenerResult)

    def test_default_actions(self, listener, lb, tg):
        result = modify_listener(
            listener.arn,
            default_actions=[
                {"Type": "forward", "TargetGroupArn": tg.arn}
            ],
            region_name=REGION,
        )
        assert isinstance(result, ListenerResult)

    def test_no_changes(self, listener):
        result = modify_listener(listener.arn, region_name=REGION)
        assert isinstance(result, ListenerResult)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.modify_listener.side_effect = ClientError(
            {"Error": {"Code": "ListenerNotFound", "Message": "nope"}},
            "ModifyListener",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="modify_listener failed"):
            modify_listener("arn:fake", region_name=REGION)


class TestDeleteListener:
    def test_basic(self, listener, lb):
        delete_listener(listener.arn, region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.delete_listener.side_effect = ClientError(
            {"Error": {"Code": "ListenerNotFound", "Message": "nope"}},
            "DeleteListener",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_listener failed"):
            delete_listener("arn:fake", region_name=REGION)


# ---------------------------------------------------------------------------
# Rule tests
# ---------------------------------------------------------------------------


class TestCreateRule:
    def test_basic(self, listener, tg):
        result = create_rule(
            listener.arn,
            conditions=[
                {
                    "Field": "path-pattern",
                    "Values": ["/api/*"],
                }
            ],
            actions=[
                {"Type": "forward", "TargetGroupArn": tg.arn}
            ],
            priority=10,
            region_name=REGION,
        )
        assert isinstance(result, RuleResult)
        assert result.arn

    def test_with_tags(self, listener, tg):
        result = create_rule(
            listener.arn,
            conditions=[
                {
                    "Field": "path-pattern",
                    "Values": ["/web/*"],
                }
            ],
            actions=[
                {"Type": "forward", "TargetGroupArn": tg.arn}
            ],
            priority=20,
            tags={"env": "test"},
            region_name=REGION,
        )
        assert isinstance(result, RuleResult)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.create_rule.side_effect = ClientError(
            {"Error": {"Code": "ListenerNotFound", "Message": "nope"}},
            "CreateRule",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_rule failed"):
            create_rule(
                "arn:fake",
                conditions=[],
                actions=[],
                priority=1,
                region_name=REGION,
            )


class TestDescribeRules:
    def test_basic(self, listener, tg):
        create_rule(
            listener.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/api/*"]}],
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            priority=10,
            region_name=REGION,
        )
        results = describe_rules(listener.arn, region_name=REGION)
        assert len(results) >= 1
        assert all(isinstance(r, RuleResult) for r in results)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "ListenerNotFound", "Message": "nope"}},
            "DescribeRules",
        )
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_rules failed"):
            describe_rules("arn:fake", region_name=REGION)


class TestModifyRule:
    def test_conditions(self, listener, tg):
        rule = create_rule(
            listener.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/api/*"]}],
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            priority=10,
            region_name=REGION,
        )
        result = modify_rule(
            rule.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/v2/*"]}],
            region_name=REGION,
        )
        assert isinstance(result, RuleResult)

    def test_actions(self, listener, tg):
        rule = create_rule(
            listener.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/old/*"]}],
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            priority=11,
            region_name=REGION,
        )
        result = modify_rule(
            rule.arn,
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            region_name=REGION,
        )
        assert isinstance(result, RuleResult)

    def test_no_changes_raises_validation(self, listener, tg):
        """modify_rule with no conditions/actions raises a validation error."""
        rule = create_rule(
            listener.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/noop/*"]}],
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            priority=12,
            region_name=REGION,
        )
        with pytest.raises(RuntimeError, match="modify_rule failed"):
            modify_rule(rule.arn, region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.modify_rule.side_effect = ClientError(
            {"Error": {"Code": "RuleNotFound", "Message": "nope"}},
            "ModifyRule",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="modify_rule failed"):
            modify_rule("arn:fake", region_name=REGION)


class TestDeleteRule:
    def test_basic(self, listener, tg):
        rule = create_rule(
            listener.arn,
            conditions=[{"Field": "path-pattern", "Values": ["/del/*"]}],
            actions=[{"Type": "forward", "TargetGroupArn": tg.arn}],
            priority=13,
            region_name=REGION,
        )
        delete_rule(rule.arn, region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.delete_rule.side_effect = ClientError(
            {"Error": {"Code": "RuleNotFound", "Message": "nope"}},
            "DeleteRule",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_rule failed"):
            delete_rule("arn:fake", region_name=REGION)


# ---------------------------------------------------------------------------
# Subnet / security group tests
# ---------------------------------------------------------------------------


class TestSetSubnets:
    def test_basic(self, lb, vpc_env):
        result = set_subnets(
            lb.arn, subnets=vpc_env["subnet_ids"], region_name=REGION
        )
        assert isinstance(result, list)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.set_subnets.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "SetSubnets",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="set_subnets failed"):
            set_subnets("arn:fake", subnets=["s-1"], region_name=REGION)


class TestSetSecurityGroups:
    def test_basic(self, lb, vpc_env):
        result = set_security_groups(
            lb.arn, security_groups=[vpc_env["sg_id"]], region_name=REGION
        )
        assert isinstance(result, list)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.set_security_groups.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "SetSecurityGroups",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="set_security_groups failed"):
            set_security_groups(
                "arn:fake", security_groups=["sg-1"], region_name=REGION
            )


# ---------------------------------------------------------------------------
# Tag tests
# ---------------------------------------------------------------------------


class TestAddTags:
    def test_basic(self, lb):
        add_tags([lb.arn], tags={"env": "prod"}, region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.add_tags.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "AddTags",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="add_tags failed"):
            add_tags(["arn:fake"], tags={"k": "v"}, region_name=REGION)


class TestRemoveTags:
    def test_basic(self, lb):
        add_tags([lb.arn], tags={"env": "prod"}, region_name=REGION)
        remove_tags([lb.arn], tag_keys=["env"], region_name=REGION)

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.remove_tags.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "RemoveTags",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="remove_tags failed"):
            remove_tags(["arn:fake"], tag_keys=["k"], region_name=REGION)


class TestDescribeTags:
    def test_basic(self, lb):
        add_tags([lb.arn], tags={"env": "prod", "team": "devops"}, region_name=REGION)
        result = describe_tags([lb.arn], region_name=REGION)
        assert lb.arn in result
        assert result[lb.arn]["env"] == "prod"
        assert result[lb.arn]["team"] == "devops"

    def test_error(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_client.describe_tags.side_effect = ClientError(
            {"Error": {"Code": "LoadBalancerNotFound", "Message": "nope"}},
            "DescribeTags",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_tags failed"):
            describe_tags(["arn:fake"], region_name=REGION)


# ---------------------------------------------------------------------------
# High-level utility tests
# ---------------------------------------------------------------------------


class TestWaitForLoadBalancer:
    def test_already_active(self, lb):
        # moto creates LBs in provisioning state typically, but may
        # return active. Either way we exercise the code path.
        # We use monkeypatch to control the state to ensure 'active' path
        result = wait_for_load_balancer(lb.arn, timeout=5, poll_interval=0.1, region_name=REGION)
        assert isinstance(result, LoadBalancerResult)

    def test_timeout(self, monkeypatch):
        import aws_util.elbv2 as mod

        # Make describe always return provisioning state
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {
                "LoadBalancers": [
                    {
                        "LoadBalancerArn": "arn:test",
                        "DNSName": "test.elb.amazonaws.com",
                        "LoadBalancerName": "test",
                        "Type": "application",
                        "State": {"Code": "provisioning"},
                        "VpcId": "vpc-1",
                        "Scheme": "internet-facing",
                    }
                ]
            }
        ]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="did not reach"):
            wait_for_load_balancer(
                "arn:test", timeout=0.0, poll_interval=0.01, region_name=REGION
            )

    def test_not_found(self, monkeypatch):
        import aws_util.elbv2 as mod

        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"LoadBalancers": []}]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="not found"):
            wait_for_load_balancer("arn:fake", region_name=REGION)

    def test_becomes_active(self, monkeypatch):
        import aws_util.elbv2 as mod

        call_count = 0

        def _make_paginator(*args, **kwargs):
            paginator = MagicMock()

            nonlocal call_count
            call_count += 1
            if call_count == 1:
                state = "provisioning"
            else:
                state = "active"
            paginator.paginate.return_value = [
                {
                    "LoadBalancers": [
                        {
                            "LoadBalancerArn": "arn:test",
                            "DNSName": "test.elb.amazonaws.com",
                            "LoadBalancerName": "test",
                            "Type": "application",
                            "State": {"Code": state},
                        }
                    ]
                }
            ]
            return paginator

        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = _make_paginator
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_client)
        monkeypatch.setattr(mod._time, "sleep", lambda x: None)
        result = wait_for_load_balancer(
            "arn:test", timeout=60, poll_interval=0.01, region_name=REGION
        )
        assert result.state == "active"


class TestEnsureLoadBalancer:
    def test_creates_new(self, vpc_env):
        result, created = ensure_load_balancer(
            "ensure-alb",
            subnets=vpc_env["subnet_ids"],
            security_groups=[vpc_env["sg_id"]],
            region_name=REGION,
        )
        assert created is True
        assert result.name == "ensure-alb"

    def test_returns_existing(self, lb, vpc_env):
        result, created = ensure_load_balancer(
            "test-alb",
            subnets=vpc_env["subnet_ids"],
            region_name=REGION,
        )
        assert created is False
        assert result.arn == lb.arn

    def test_describe_error_fallback_to_create(self, monkeypatch, vpc_env):
        """When describe raises RuntimeError, falls through to create."""
        import aws_util.elbv2 as mod

        original_describe = mod.describe_load_balancers
        original_create = mod.create_load_balancer

        first_call = True

        def patched_describe(**kwargs):
            nonlocal first_call
            if first_call:
                first_call = False
                raise RuntimeError("simulated error")
            return original_describe(**kwargs)

        monkeypatch.setattr(mod, "describe_load_balancers", patched_describe)
        result, created = ensure_load_balancer(
            "fallback-alb",
            subnets=vpc_env["subnet_ids"],
            security_groups=[vpc_env["sg_id"]],
            region_name=REGION,
        )
        assert created is True


class TestEnsureTargetGroup:
    def test_creates_new(self, vpc_env):
        result, created = ensure_target_group(
            "ensure-tg",
            vpc_id=vpc_env["vpc_id"],
            region_name=REGION,
        )
        assert created is True
        assert result.name == "ensure-tg"

    def test_returns_existing(self, tg, vpc_env):
        result, created = ensure_target_group(
            "test-tg",
            vpc_id=vpc_env["vpc_id"],
            region_name=REGION,
        )
        assert created is False
        assert result.arn == tg.arn

    def test_describe_error_fallback_to_create(self, monkeypatch, vpc_env):
        """When describe raises RuntimeError, falls through to create."""
        import aws_util.elbv2 as mod

        first_call = True

        def patched_describe(**kwargs):
            nonlocal first_call
            if first_call:
                first_call = False
                raise RuntimeError("simulated error")
            return mod.describe_target_groups(**kwargs)

        monkeypatch.setattr(mod, "describe_target_groups", patched_describe)
        result, created = ensure_target_group(
            "fallback-tg",
            vpc_id=vpc_env["vpc_id"],
            region_name=REGION,
        )
        assert created is True


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_load_balancer_result_frozen(self):
        lb = LoadBalancerResult(
            arn="arn:test", dns_name="test.elb", name="test", type="application", state="active"
        )
        with pytest.raises(Exception):
            lb.name = "changed"

    def test_target_group_result_frozen(self):
        tg = TargetGroupResult(arn="arn:tg", name="test")
        with pytest.raises(Exception):
            tg.name = "changed"

    def test_listener_result_frozen(self):
        ln = ListenerResult(arn="arn:ln", load_balancer_arn="arn:lb")
        with pytest.raises(Exception):
            ln.port = 9999

    def test_rule_result_frozen(self):
        rule = RuleResult(arn="arn:rule")
        with pytest.raises(Exception):
            rule.priority = "999"

    def test_load_balancer_result_defaults(self):
        lb = LoadBalancerResult(
            arn="arn:test", dns_name="d", name="n", type="application", state="active"
        )
        assert lb.vpc_id is None
        assert lb.scheme is None
        assert lb.security_groups == []
        assert lb.availability_zones == []
        assert lb.created_time is None
        assert lb.extra == {}

    def test_target_group_result_defaults(self):
        tg = TargetGroupResult(arn="arn:tg", name="tg")
        assert tg.protocol is None
        assert tg.port is None
        assert tg.vpc_id is None
        assert tg.health_check_path is None
        assert tg.target_type is None
        assert tg.extra == {}

    def test_listener_result_defaults(self):
        ln = ListenerResult(arn="arn:ln", load_balancer_arn="arn:lb")
        assert ln.port is None
        assert ln.protocol is None
        assert ln.default_actions == []
        assert ln.extra == {}

    def test_rule_result_defaults(self):
        rule = RuleResult(arn="arn:rule")
        assert rule.priority is None
        assert rule.conditions == []
        assert rule.actions == []
        assert rule.is_default is False
        assert rule.extra == {}


def test_add_listener_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_listener_certificates.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    add_listener_certificates("test-listener_arn", [], region_name=REGION)
    mock_client.add_listener_certificates.assert_called_once()


def test_add_listener_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_listener_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_listener_certificates",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add listener certificates"):
        add_listener_certificates("test-listener_arn", [], region_name=REGION)


def test_add_trust_store_revocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_trust_store_revocations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    add_trust_store_revocations("test-trust_store_arn", region_name=REGION)
    mock_client.add_trust_store_revocations.assert_called_once()


def test_add_trust_store_revocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_trust_store_revocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_trust_store_revocations",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add trust store revocations"):
        add_trust_store_revocations("test-trust_store_arn", region_name=REGION)


def test_create_trust_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trust_store.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", region_name=REGION)
    mock_client.create_trust_store.assert_called_once()


def test_create_trust_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trust_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_trust_store",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create trust store"):
        create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", region_name=REGION)


def test_delete_shared_trust_store_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_shared_trust_store_association.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    delete_shared_trust_store_association("test-trust_store_arn", "test-resource_arn", region_name=REGION)
    mock_client.delete_shared_trust_store_association.assert_called_once()


def test_delete_shared_trust_store_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_shared_trust_store_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_shared_trust_store_association",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete shared trust store association"):
        delete_shared_trust_store_association("test-trust_store_arn", "test-resource_arn", region_name=REGION)


def test_delete_trust_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trust_store.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    delete_trust_store("test-trust_store_arn", region_name=REGION)
    mock_client.delete_trust_store.assert_called_once()


def test_delete_trust_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trust_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_trust_store",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete trust store"):
        delete_trust_store("test-trust_store_arn", region_name=REGION)


def test_describe_account_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_account_limits(region_name=REGION)
    mock_client.describe_account_limits.assert_called_once()


def test_describe_account_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_limits",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account limits"):
        describe_account_limits(region_name=REGION)


def test_describe_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation("test-load_balancer_arn", region_name=REGION)
    mock_client.describe_capacity_reservation.assert_called_once()


def test_describe_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity reservation"):
        describe_capacity_reservation("test-load_balancer_arn", region_name=REGION)


def test_describe_listener_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_listener_attributes.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_listener_attributes("test-listener_arn", region_name=REGION)
    mock_client.describe_listener_attributes.assert_called_once()


def test_describe_listener_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_listener_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_listener_attributes",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe listener attributes"):
        describe_listener_attributes("test-listener_arn", region_name=REGION)


def test_describe_listener_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_listener_certificates.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_listener_certificates("test-listener_arn", region_name=REGION)
    mock_client.describe_listener_certificates.assert_called_once()


def test_describe_listener_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_listener_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_listener_certificates",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe listener certificates"):
        describe_listener_certificates("test-listener_arn", region_name=REGION)


def test_describe_load_balancer_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancer_attributes.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_load_balancer_attributes("test-load_balancer_arn", region_name=REGION)
    mock_client.describe_load_balancer_attributes.assert_called_once()


def test_describe_load_balancer_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_load_balancer_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_load_balancer_attributes",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe load balancer attributes"):
        describe_load_balancer_attributes("test-load_balancer_arn", region_name=REGION)


def test_describe_ssl_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ssl_policies.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_ssl_policies(region_name=REGION)
    mock_client.describe_ssl_policies.assert_called_once()


def test_describe_ssl_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ssl_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ssl_policies",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ssl policies"):
        describe_ssl_policies(region_name=REGION)


def test_describe_target_group_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_target_group_attributes.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_target_group_attributes("test-target_group_arn", region_name=REGION)
    mock_client.describe_target_group_attributes.assert_called_once()


def test_describe_target_group_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_target_group_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_target_group_attributes",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe target group attributes"):
        describe_target_group_attributes("test-target_group_arn", region_name=REGION)


def test_describe_trust_store_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_store_associations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_store_associations("test-trust_store_arn", region_name=REGION)
    mock_client.describe_trust_store_associations.assert_called_once()


def test_describe_trust_store_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_store_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_trust_store_associations",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe trust store associations"):
        describe_trust_store_associations("test-trust_store_arn", region_name=REGION)


def test_describe_trust_store_revocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_store_revocations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_store_revocations("test-trust_store_arn", region_name=REGION)
    mock_client.describe_trust_store_revocations.assert_called_once()


def test_describe_trust_store_revocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_store_revocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_trust_store_revocations",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe trust store revocations"):
        describe_trust_store_revocations("test-trust_store_arn", region_name=REGION)


def test_describe_trust_stores(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_stores.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_stores(region_name=REGION)
    mock_client.describe_trust_stores.assert_called_once()


def test_describe_trust_stores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trust_stores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_trust_stores",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe trust stores"):
        describe_trust_stores(region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_get_trust_store_ca_certificates_bundle(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trust_store_ca_certificates_bundle.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    get_trust_store_ca_certificates_bundle("test-trust_store_arn", region_name=REGION)
    mock_client.get_trust_store_ca_certificates_bundle.assert_called_once()


def test_get_trust_store_ca_certificates_bundle_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trust_store_ca_certificates_bundle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_trust_store_ca_certificates_bundle",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get trust store ca certificates bundle"):
        get_trust_store_ca_certificates_bundle("test-trust_store_arn", region_name=REGION)


def test_get_trust_store_revocation_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trust_store_revocation_content.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    get_trust_store_revocation_content("test-trust_store_arn", 1, region_name=REGION)
    mock_client.get_trust_store_revocation_content.assert_called_once()


def test_get_trust_store_revocation_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trust_store_revocation_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_trust_store_revocation_content",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get trust store revocation content"):
        get_trust_store_revocation_content("test-trust_store_arn", 1, region_name=REGION)


def test_modify_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation("test-load_balancer_arn", region_name=REGION)
    mock_client.modify_capacity_reservation.assert_called_once()


def test_modify_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify capacity reservation"):
        modify_capacity_reservation("test-load_balancer_arn", region_name=REGION)


def test_modify_ip_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ip_pools.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_ip_pools("test-load_balancer_arn", region_name=REGION)
    mock_client.modify_ip_pools.assert_called_once()


def test_modify_ip_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ip_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ip_pools",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ip pools"):
        modify_ip_pools("test-load_balancer_arn", region_name=REGION)


def test_modify_listener_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_listener_attributes.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_listener_attributes("test-listener_arn", [], region_name=REGION)
    mock_client.modify_listener_attributes.assert_called_once()


def test_modify_listener_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_listener_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_listener_attributes",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify listener attributes"):
        modify_listener_attributes("test-listener_arn", [], region_name=REGION)


def test_modify_target_group_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_target_group_attributes.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_target_group_attributes("test-target_group_arn", [], region_name=REGION)
    mock_client.modify_target_group_attributes.assert_called_once()


def test_modify_target_group_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_target_group_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_target_group_attributes",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify target group attributes"):
        modify_target_group_attributes("test-target_group_arn", [], region_name=REGION)


def test_modify_trust_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_trust_store.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", region_name=REGION)
    mock_client.modify_trust_store.assert_called_once()


def test_modify_trust_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_trust_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_trust_store",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify trust store"):
        modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", region_name=REGION)


def test_remove_listener_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_listener_certificates.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    remove_listener_certificates("test-listener_arn", [], region_name=REGION)
    mock_client.remove_listener_certificates.assert_called_once()


def test_remove_listener_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_listener_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_listener_certificates",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove listener certificates"):
        remove_listener_certificates("test-listener_arn", [], region_name=REGION)


def test_remove_trust_store_revocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_trust_store_revocations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    remove_trust_store_revocations("test-trust_store_arn", [], region_name=REGION)
    mock_client.remove_trust_store_revocations.assert_called_once()


def test_remove_trust_store_revocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_trust_store_revocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_trust_store_revocations",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove trust store revocations"):
        remove_trust_store_revocations("test-trust_store_arn", [], region_name=REGION)


def test_set_ip_address_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_ip_address_type.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    set_ip_address_type("test-load_balancer_arn", "test-ip_address_type", region_name=REGION)
    mock_client.set_ip_address_type.assert_called_once()


def test_set_ip_address_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_ip_address_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_ip_address_type",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set ip address type"):
        set_ip_address_type("test-load_balancer_arn", "test-ip_address_type", region_name=REGION)


def test_set_rule_priorities(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_rule_priorities.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    set_rule_priorities([], region_name=REGION)
    mock_client.set_rule_priorities.assert_called_once()


def test_set_rule_priorities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_rule_priorities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_rule_priorities",
    )
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set rule priorities"):
        set_rule_priorities([], region_name=REGION)


def test_add_trust_store_revocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import add_trust_store_revocations
    mock_client = MagicMock()
    mock_client.add_trust_store_revocations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    add_trust_store_revocations("test-trust_store_arn", revocation_contents="test-revocation_contents", region_name="us-east-1")
    mock_client.add_trust_store_revocations.assert_called_once()

def test_create_trust_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import create_trust_store
    mock_client = MagicMock()
    mock_client.create_trust_store.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    create_trust_store("test-name", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", ca_certificates_bundle_s3_object_version="test-ca_certificates_bundle_s3_object_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_trust_store.assert_called_once()

def test_describe_account_limits_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_account_limits
    mock_client = MagicMock()
    mock_client.describe_account_limits.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_account_limits(marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.describe_account_limits.assert_called_once()

def test_describe_listener_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_listener_certificates
    mock_client = MagicMock()
    mock_client.describe_listener_certificates.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_listener_certificates("test-listener_arn", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.describe_listener_certificates.assert_called_once()

def test_describe_ssl_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_ssl_policies
    mock_client = MagicMock()
    mock_client.describe_ssl_policies.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_ssl_policies(names="test-names", marker="test-marker", page_size=1, load_balancer_type="test-load_balancer_type", region_name="us-east-1")
    mock_client.describe_ssl_policies.assert_called_once()

def test_describe_trust_store_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_trust_store_associations
    mock_client = MagicMock()
    mock_client.describe_trust_store_associations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_store_associations("test-trust_store_arn", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.describe_trust_store_associations.assert_called_once()

def test_describe_trust_store_revocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_trust_store_revocations
    mock_client = MagicMock()
    mock_client.describe_trust_store_revocations.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_store_revocations("test-trust_store_arn", revocation_ids="test-revocation_ids", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.describe_trust_store_revocations.assert_called_once()

def test_describe_trust_stores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import describe_trust_stores
    mock_client = MagicMock()
    mock_client.describe_trust_stores.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    describe_trust_stores(trust_store_arns="test-trust_store_arns", names="test-names", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.describe_trust_stores.assert_called_once()

def test_modify_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import modify_capacity_reservation
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation("test-load_balancer_arn", minimum_load_balancer_capacity="test-minimum_load_balancer_capacity", reset_capacity_reservation="test-reset_capacity_reservation", region_name="us-east-1")
    mock_client.modify_capacity_reservation.assert_called_once()

def test_modify_ip_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import modify_ip_pools
    mock_client = MagicMock()
    mock_client.modify_ip_pools.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_ip_pools("test-load_balancer_arn", ipam_pools="test-ipam_pools", remove_ipam_pools="test-remove_ipam_pools", region_name="us-east-1")
    mock_client.modify_ip_pools.assert_called_once()

def test_modify_trust_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elbv2 import modify_trust_store
    mock_client = MagicMock()
    mock_client.modify_trust_store.return_value = {}
    monkeypatch.setattr("aws_util.elbv2.get_client", lambda *a, **kw: mock_client)
    modify_trust_store("test-trust_store_arn", "test-ca_certificates_bundle_s3_bucket", "test-ca_certificates_bundle_s3_key", ca_certificates_bundle_s3_object_version="test-ca_certificates_bundle_s3_object_version", region_name="us-east-1")
    mock_client.modify_trust_store.assert_called_once()
