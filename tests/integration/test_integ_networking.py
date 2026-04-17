"""Integration tests for aws_util.networking against LocalStack."""
from __future__ import annotations

import json

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. vpc_connectivity_manager
# ---------------------------------------------------------------------------


class TestVpcConnectivityManager:
    def test_manages_peering(self):
        from aws_util.networking import vpc_connectivity_manager

        ec2 = ls_client("ec2")
        vpc1 = ec2.create_vpc(CidrBlock="10.0.0.0/16")
        vpc1_id = vpc1["Vpc"]["VpcId"]
        vpc2 = ec2.create_vpc(CidrBlock="10.1.0.0/16")
        vpc2_id = vpc2["Vpc"]["VpcId"]

        result = vpc_connectivity_manager(
            connectivity_type="peering",
            requestor_vpc_id=vpc1_id,
            acceptor_vpc_id=vpc2_id,
            requestor_cidr="10.0.0.0/16",
            acceptor_cidr="10.1.0.0/16",
            region_name=REGION,
        )
        assert result.connectivity_type == "peering"
        assert result.connection_id is not None


# ---------------------------------------------------------------------------
# 2. route53_health_check_manager
# ---------------------------------------------------------------------------


class TestRoute53HealthCheckManager:
    @pytest.mark.skip(reason="CloudWatch PutMetricAlarm returns 500 on LocalStack community")
    def test_creates_health_check(self, sns_topic):
        from aws_util.networking import route53_health_check_manager

        result = route53_health_check_manager(
            endpoints=[
                {"fqdn": "example.com", "port": 80, "path": "/health"},
            ],
            alarm_prefix="integ-test",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert result.health_checks_created >= 1
        assert isinstance(result.health_check_ids, list)


# ---------------------------------------------------------------------------
# 3. eventbridge_cross_account_forwarder
# ---------------------------------------------------------------------------


class TestEventbridgeCrossAccountForwarder:
    def test_forwards_events(self):
        from aws_util.networking import eventbridge_cross_account_forwarder

        result = eventbridge_cross_account_forwarder(
            rule_name="test-forward-rule",
            event_pattern={
                "source": ["aws.ec2"],
                "detail-type": ["EC2 Instance State-change Notification"],
            },
            target_event_bus_arn="arn:aws:events:us-east-1:123456789012:event-bus/default",
            target_account_id="123456789012",
            region_name=REGION,
        )
        assert result.rule_arn is not None
        assert result.target_id is not None


# ---------------------------------------------------------------------------
# 4. vpc_lattice_service_registrar
# ---------------------------------------------------------------------------


class TestVpcLatticeServiceRegistrar:
    @pytest.mark.skip(reason="VPC Lattice not available in LocalStack community")
    def test_registers_target(self):
        from aws_util.networking import vpc_lattice_service_registrar

        result = vpc_lattice_service_registrar(
            service_network_id="sn-0123456789abcdef0",
            target_type="LAMBDA",
            target_id="arn:aws:lambda:us-east-1:000000000000:function:my-fn",
            port=443,
            hosted_zone_id="Z1234567890",
            domain_name="svc.example.com",
            health_check_path="/health",
            region_name=REGION,
        )
        assert result.target_group_arn
        assert result.route53_change_id


# ---------------------------------------------------------------------------
# 5. transit_gateway_route_auditor
# ---------------------------------------------------------------------------


class TestTransitGatewayRouteAuditor:
    @pytest.mark.skip(reason="Transit Gateway not fully available in LocalStack community")
    def test_audits_routes(self, s3_bucket):
        from aws_util.networking import transit_gateway_route_auditor

        result = transit_gateway_route_auditor(
            transit_gateway_id="tgw-0123456789abcdef0",
            bucket=s3_bucket,
            report_key="audit/tgw-report.json",
            region_name=REGION,
        )
        assert result.route_tables_checked >= 0
        assert result.total_routes >= 0
        assert isinstance(result.overlapping_cidrs, list)
        assert result.report_s3_key == "audit/tgw-report.json"
