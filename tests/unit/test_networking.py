"""Tests for aws_util.networking -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.networking as mod
from aws_util.networking import VPCConnectivityResult, vpc_connectivity_manager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str, message: str = "err") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}},
        "Op",
    )


def _mock_ec2(**overrides: object) -> MagicMock:
    """Return a MagicMock that behaves like an EC2 client."""
    ec2 = MagicMock()
    for k, v in overrides.items():
        setattr(ec2, k, v)
    return ec2


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestVPCConnectivityResult:
    def test_create(self) -> None:
        r = VPCConnectivityResult(
            connectivity_type="peering",
            connection_id="pcx-123",
            status="active",
            routes_created=["rt-1 -> 10.0.0.0/16 via pcx-123"],
            security_group_rules_added=["sg-1: tcp/443 from 10.0.0.0/16"],
            dns_records_created=[],
        )
        assert r.connectivity_type == "peering"
        assert r.connection_id == "pcx-123"
        assert r.status == "active"

    def test_frozen(self) -> None:
        r = VPCConnectivityResult(
            connectivity_type="peering",
            connection_id="pcx-123",
            status="active",
            routes_created=[],
            security_group_rules_added=[],
            dns_records_created=[],
        )
        with pytest.raises(Exception):
            r.status = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# _add_routes
# ---------------------------------------------------------------------------


class TestAddRoutes:
    def test_success(self) -> None:
        ec2 = _mock_ec2()
        result = mod._add_routes(
            ec2, ["rt-1"], "10.0.0.0/16", "VpcPeeringConnectionId", "pcx-1"
        )
        assert len(result) == 1
        assert "rt-1" in result[0]
        assert "pcx-1" in result[0]

    def test_already_exists(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_route.side_effect = _client_error("RouteAlreadyExists")
        result = mod._add_routes(
            ec2, ["rt-1"], "10.0.0.0/16", "VpcPeeringConnectionId", "pcx-1"
        )
        assert "already exists" in result[0]

    def test_other_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_route.side_effect = _client_error("SomeOtherError")
        with pytest.raises(RuntimeError, match="Failed to create route"):
            mod._add_routes(
                ec2, ["rt-1"], "10.0.0.0/16", "VpcPeeringConnectionId", "pcx-1"
            )


# ---------------------------------------------------------------------------
# _add_security_group_rules
# ---------------------------------------------------------------------------


class TestAddSecurityGroupRules:
    def test_success(self) -> None:
        ec2 = _mock_ec2()
        result = mod._add_security_group_rules(
            ec2, ["sg-1"], "10.0.0.0/16", [443, 80]
        )
        assert len(result) == 2
        assert "sg-1: tcp/443" in result[0]
        assert "sg-1: tcp/80" in result[1]

    def test_duplicate(self) -> None:
        ec2 = _mock_ec2()
        ec2.authorize_security_group_ingress.side_effect = _client_error(
            "InvalidPermission.Duplicate"
        )
        result = mod._add_security_group_rules(
            ec2, ["sg-1"], "10.0.0.0/16", [443]
        )
        assert "already exists" in result[0]

    def test_other_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.authorize_security_group_ingress.side_effect = _client_error(
            "SomeOtherError"
        )
        with pytest.raises(RuntimeError, match="Failed to add SG rule"):
            mod._add_security_group_rules(
                ec2, ["sg-1"], "10.0.0.0/16", [443]
            )


# ---------------------------------------------------------------------------
# _create_dns_record
# ---------------------------------------------------------------------------


class TestCreateDnsRecord:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_r53 = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_r53)
        result = mod._create_dns_record(
            "Z123", "svc.example.com", "pcx-1", None
        )
        assert result == ["svc.example.com -> pcx-1"]
        mock_r53.change_resource_record_sets.assert_called_once()

    def test_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_r53 = MagicMock()
        mock_r53.change_resource_record_sets.side_effect = _client_error(
            "NoSuchHostedZone"
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock_r53)
        with pytest.raises(RuntimeError, match="Failed to create DNS record"):
            mod._create_dns_record("Z123", "svc.example.com", "pcx-1", None)


# ---------------------------------------------------------------------------
# _wait_for_peering
# ---------------------------------------------------------------------------


class TestWaitForPeering:
    def test_active_immediately(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "active"}}
            ]
        }
        result = mod._wait_for_peering(ec2, "pcx-1")
        assert result == "active"

    def test_terminal_state(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "failed", "Message": "boom"}}
            ]
        }
        with pytest.raises(RuntimeError, match="terminal state"):
            mod._wait_for_peering(ec2, "pcx-1")

    def test_not_found(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": []
        }
        with pytest.raises(RuntimeError, match="not found"):
            mod._wait_for_peering(ec2, "pcx-1")

    def test_describe_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_vpc_peering_connections.side_effect = _client_error(
            "AccessDenied"
        )
        with pytest.raises(RuntimeError, match="Failed to describe peering"):
            mod._wait_for_peering(ec2, "pcx-1")

    def test_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "pending-acceptance"}}
            ]
        }
        # Make time.monotonic advance past deadline
        calls = iter([0.0, 0.0, 200.0])
        monkeypatch.setattr(mod.time, "monotonic", lambda: next(calls))
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)
        with pytest.raises(TimeoutError, match="did not become active"):
            mod._wait_for_peering(ec2, "pcx-1", timeout=120.0)


# ---------------------------------------------------------------------------
# _setup_peering
# ---------------------------------------------------------------------------


class TestSetupPeering:
    def test_success_minimal(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-1"
            }
        }
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "active"}}
            ]
        }
        conn_id, status, routes, sg_rules = mod._setup_peering(
            ec2, "vpc-1", "vpc-2", [], [], "10.0.0.0/16", "10.1.0.0/16", [], []
        )
        assert conn_id == "pcx-1"
        assert status == "active"
        assert routes == []
        assert sg_rules == []

    def test_with_routes_and_sg(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-2"
            }
        }
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "active"}}
            ]
        }
        conn_id, status, routes, sg_rules = mod._setup_peering(
            ec2,
            "vpc-1",
            "vpc-2",
            ["rt-1"],
            ["rt-2"],
            "10.0.0.0/16",
            "10.1.0.0/16",
            ["sg-1"],
            [443],
        )
        assert conn_id == "pcx-2"
        assert len(routes) == 2
        assert len(sg_rules) == 2

    def test_create_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.side_effect = _client_error(
            "VpcLimitExceeded"
        )
        with pytest.raises(RuntimeError, match="Failed to create VPC peering"):
            mod._setup_peering(
                ec2, "vpc-1", "vpc-2", [], [], "", "", [], []
            )

    def test_accept_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-1"
            }
        }
        ec2.accept_vpc_peering_connection.side_effect = _client_error(
            "Forbidden"
        )
        with pytest.raises(RuntimeError, match="Failed to accept VPC peering"):
            mod._setup_peering(
                ec2, "vpc-1", "vpc-2", [], [], "", "", [], []
            )


# ---------------------------------------------------------------------------
# _get_vpc_subnets
# ---------------------------------------------------------------------------


class TestGetVpcSubnets:
    def test_success(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
                {"SubnetId": "sub-2", "AvailabilityZone": "us-east-1b"},
                {"SubnetId": "sub-3", "AvailabilityZone": "us-east-1a"},
            ]
        }
        result = mod._get_vpc_subnets(ec2, "vpc-1")
        assert result == ["sub-1", "sub-2"]

    def test_error_returns_empty(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_subnets.side_effect = _client_error("AccessDenied")
        result = mod._get_vpc_subnets(ec2, "vpc-1")
        assert result == []


# ---------------------------------------------------------------------------
# _find_existing_tgw_attachment
# ---------------------------------------------------------------------------


class TestFindExistingTgwAttachment:
    def test_success(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"TransitGatewayAttachmentId": "att-1"}
            ]
        }
        result = mod._find_existing_tgw_attachment(ec2, "tgw-1", "vpc-1")
        assert result == "att-1"

    def test_not_found(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": []
        }
        with pytest.raises(RuntimeError, match="No existing TGW attachment"):
            mod._find_existing_tgw_attachment(ec2, "tgw-1", "vpc-1")

    def test_api_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.side_effect = _client_error(
            "AccessDenied"
        )
        with pytest.raises(RuntimeError, match="Failed to find existing"):
            mod._find_existing_tgw_attachment(ec2, "tgw-1", "vpc-1")


# ---------------------------------------------------------------------------
# _describe_tgw_attachment_status
# ---------------------------------------------------------------------------


class TestDescribeTgwAttachmentStatus:
    def test_success(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"State": "available"}
            ]
        }
        result = mod._describe_tgw_attachment_status(ec2, "att-1")
        assert result == "available"

    def test_empty(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": []
        }
        result = mod._describe_tgw_attachment_status(ec2, "att-1")
        assert result == "unknown"

    def test_error_returns_unknown(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateway_vpc_attachments.side_effect = _client_error(
            "AccessDenied"
        )
        result = mod._describe_tgw_attachment_status(ec2, "att-1")
        assert result == "unknown"


# ---------------------------------------------------------------------------
# _setup_transit_gateway
# ---------------------------------------------------------------------------


class TestSetupTransitGateway:
    def _ec2_for_tgw(self) -> MagicMock:
        """Return a mock EC2 client configured for TGW tests."""
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
            ]
        }
        ec2.create_transit_gateway_vpc_attachment.side_effect = [
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-req"
                }
            },
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-acc"
                }
            },
        ]
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"State": "available"}
            ]
        }
        return ec2

    def test_success_minimal(self) -> None:
        ec2 = self._ec2_for_tgw()
        conn_id, status, routes, sg_rules = mod._setup_transit_gateway(
            ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
        )
        assert conn_id == "att-req"
        assert status == "available"
        assert routes == []
        assert sg_rules == []

    def test_with_routes_and_sg(self) -> None:
        ec2 = self._ec2_for_tgw()
        conn_id, status, routes, sg_rules = mod._setup_transit_gateway(
            ec2,
            "tgw-1",
            "vpc-1",
            "vpc-2",
            ["rt-1"],
            ["rt-2"],
            "10.0.0.0/16",
            "10.1.0.0/16",
            ["sg-1"],
            [443],
            None,
        )
        assert len(routes) == 2
        assert len(sg_rules) == 2

    def test_describe_tgw_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.side_effect = _client_error(
            "AccessDenied"
        )
        with pytest.raises(RuntimeError, match="Failed to describe transit"):
            mod._setup_transit_gateway(
                ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
            )

    def test_tgw_not_found(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": []
        }
        with pytest.raises(RuntimeError, match="not found"):
            mod._setup_transit_gateway(
                ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
            )

    def test_requestor_attach_duplicate(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
            ]
        }
        ec2.create_transit_gateway_vpc_attachment.side_effect = [
            _client_error("DuplicateTransitGatewayAttachment"),
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-acc"
                }
            },
        ]
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"TransitGatewayAttachmentId": "att-existing", "State": "available"}
            ]
        }
        conn_id, status, routes, sg_rules = mod._setup_transit_gateway(
            ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
        )
        assert conn_id == "att-existing"

    def test_acceptor_attach_duplicate(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
            ]
        }
        ec2.create_transit_gateway_vpc_attachment.side_effect = [
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-req"
                }
            },
            _client_error("DuplicateTransitGatewayAttachment"),
        ]
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"TransitGatewayAttachmentId": "att-existing", "State": "available"}
            ]
        }
        conn_id, status, routes, sg_rules = mod._setup_transit_gateway(
            ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
        )
        assert conn_id == "att-req"

    def test_requestor_attach_other_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {"Subnets": []}
        ec2.create_transit_gateway_vpc_attachment.side_effect = _client_error(
            "InvalidParameterValue"
        )
        with pytest.raises(RuntimeError, match="Failed to attach"):
            mod._setup_transit_gateway(
                ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
            )

    def test_acceptor_attach_other_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {"Subnets": []}
        ec2.create_transit_gateway_vpc_attachment.side_effect = [
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-req"
                }
            },
            _client_error("InvalidParameterValue"),
        ]
        with pytest.raises(RuntimeError, match="Failed to attach"):
            mod._setup_transit_gateway(
                ec2, "tgw-1", "vpc-1", "vpc-2", [], [], "", "", [], [], None
            )


# ---------------------------------------------------------------------------
# _setup_privatelink
# ---------------------------------------------------------------------------


class TestSetupPrivatelink:
    def _ec2_for_pl(self, svc_name: object = "com.svc") -> MagicMock:
        ec2 = _mock_ec2()
        ec2.create_vpc_endpoint_service_configuration.return_value = {
            "ServiceConfiguration": {
                "ServiceId": "svc-1",
                "ServiceName": svc_name,
            }
        }
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
            ]
        }
        ec2.create_vpc_endpoint.return_value = {
            "VpcEndpoint": {
                "VpcEndpointId": "vpce-1",
                "State": "available",
            }
        }
        return ec2

    def test_success_with_string_svc_name(self) -> None:
        ec2 = self._ec2_for_pl(svc_name="com.svc")
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
        )
        assert ep_id == "vpce-1"
        assert status == "available"
        assert routes == []
        assert sg_rules == []

    def test_with_sg_and_ports(self) -> None:
        ec2 = self._ec2_for_pl()
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", None, "vpc-1", "vpc-2",
            ["sg-1"], [443], "10.0.0.0/16", None
        )
        assert len(sg_rules) == 1

    def test_service_name_list(self) -> None:
        ec2 = self._ec2_for_pl(svc_name=["svc-a", "svc-b"])
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
        )
        assert ep_id == "vpce-1"

    def test_service_name_empty_list_with_fallback(self) -> None:
        ec2 = self._ec2_for_pl(svc_name=[])
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", "fallback-svc", "vpc-1", "vpc-2",
            [], [], "", None
        )
        assert ep_id == "vpce-1"

    def test_service_name_none_no_fallback(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_endpoint_service_configuration.return_value = {
            "ServiceConfiguration": {
                "ServiceId": "svc-1",
                "ServiceName": None,
            }
        }
        ec2.describe_subnets.return_value = {"Subnets": []}
        ec2.create_vpc_endpoint.return_value = {
            "VpcEndpoint": {
                "VpcEndpointId": "vpce-1",
                "State": "pending",
            }
        }
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
        )
        assert ep_id == "vpce-1"

    def test_no_subnets_no_sg(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_endpoint_service_configuration.return_value = {
            "ServiceConfiguration": {
                "ServiceId": "svc-1",
                "ServiceName": "com.svc",
            }
        }
        ec2.describe_subnets.return_value = {"Subnets": []}
        ec2.create_vpc_endpoint.return_value = {
            "VpcEndpoint": {
                "VpcEndpointId": "vpce-2",
                "State": "available",
            }
        }
        ep_id, status, routes, sg_rules = mod._setup_privatelink(
            ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
        )
        assert ep_id == "vpce-2"

    def test_create_svc_config_error(self) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_endpoint_service_configuration.side_effect = _client_error(
            "InvalidParameter"
        )
        with pytest.raises(RuntimeError, match="Failed to create VPC endpoint service"):
            mod._setup_privatelink(
                ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
            )

    def test_create_endpoint_error(self) -> None:
        ec2 = self._ec2_for_pl()
        ec2.create_vpc_endpoint.side_effect = _client_error("VpcEndpointFailed")
        with pytest.raises(RuntimeError, match="Failed to create VPC interface"):
            mod._setup_privatelink(
                ec2, "arn:nlb", None, "vpc-1", "vpc-2", [], [], "", None
            )


# ---------------------------------------------------------------------------
# vpc_connectivity_manager — main entry point
# ---------------------------------------------------------------------------


class TestVpcConnectivityManager:
    def test_invalid_type(self) -> None:
        with pytest.raises(ValueError, match="connectivity_type must be"):
            vpc_connectivity_manager(
                connectivity_type="invalid",
                requestor_vpc_id="vpc-1",
            )

    def test_peering_missing_acceptor(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(ValueError, match="acceptor_vpc_id is required"):
            vpc_connectivity_manager(
                connectivity_type="peering",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="",
            )

    def test_peering_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-1"
            }
        }
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "active"}}
            ]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        result = vpc_connectivity_manager(
            connectivity_type="peering",
            requestor_vpc_id="vpc-1",
            acceptor_vpc_id="vpc-2",
        )
        assert isinstance(result, VPCConnectivityResult)
        assert result.connectivity_type == "peering"
        assert result.connection_id == "pcx-1"

    def test_peering_with_dns(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-1"
            }
        }
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "active"}}
            ]
        }
        mock_r53 = MagicMock()

        def mock_get_client(service: str, *a: object, **kw: object) -> MagicMock:
            if service == "route53":
                return mock_r53
            return ec2

        monkeypatch.setattr(mod, "get_client", mock_get_client)
        result = vpc_connectivity_manager(
            connectivity_type="peering",
            requestor_vpc_id="vpc-1",
            acceptor_vpc_id="vpc-2",
            hosted_zone_id="Z123",
            dns_record_name="svc.example.com",
        )
        assert len(result.dns_records_created) == 1

    def test_transit_gateway_missing_tgw_id(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(ValueError, match="transit_gateway_id is required"):
            vpc_connectivity_manager(
                connectivity_type="transit_gateway",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="vpc-2",
            )

    def test_transit_gateway_missing_acceptor(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(ValueError, match="acceptor_vpc_id is required"):
            vpc_connectivity_manager(
                connectivity_type="transit_gateway",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="",
                transit_gateway_id="tgw-1",
            )

    def test_transit_gateway_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        ec2.describe_transit_gateways.return_value = {
            "TransitGateways": [{"TransitGatewayId": "tgw-1"}]
        }
        ec2.describe_subnets.return_value = {
            "Subnets": [
                {"SubnetId": "sub-1", "AvailabilityZone": "us-east-1a"},
            ]
        }
        ec2.create_transit_gateway_vpc_attachment.side_effect = [
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-req"
                }
            },
            {
                "TransitGatewayVpcAttachment": {
                    "TransitGatewayAttachmentId": "att-acc"
                }
            },
        ]
        ec2.describe_transit_gateway_vpc_attachments.return_value = {
            "TransitGatewayVpcAttachments": [
                {"State": "available"}
            ]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        result = vpc_connectivity_manager(
            connectivity_type="transit_gateway",
            requestor_vpc_id="vpc-1",
            acceptor_vpc_id="vpc-2",
            transit_gateway_id="tgw-1",
        )
        assert result.connectivity_type == "transit_gateway"
        assert result.connection_id == "att-req"

    def test_privatelink_missing_nlb(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(ValueError, match="nlb_arn is required"):
            vpc_connectivity_manager(
                connectivity_type="privatelink",
                requestor_vpc_id="vpc-1",
            )

    def test_privatelink_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_endpoint_service_configuration.return_value = {
            "ServiceConfiguration": {
                "ServiceId": "svc-1",
                "ServiceName": "com.svc",
            }
        }
        ec2.describe_subnets.return_value = {"Subnets": []}
        ec2.create_vpc_endpoint.return_value = {
            "VpcEndpoint": {
                "VpcEndpointId": "vpce-1",
                "State": "available",
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        result = vpc_connectivity_manager(
            connectivity_type="privatelink",
            requestor_vpc_id="vpc-1",
            nlb_arn="arn:nlb",
        )
        assert result.connectivity_type == "privatelink"
        assert result.connection_id == "vpce-1"

    def test_generic_exception_wrapped(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            mod,
            "get_client",
            lambda *a, **kw: (_ for _ in ()).throw(TypeError("boom")),
        )
        with pytest.raises(RuntimeError, match="vpc_connectivity_manager failed"):
            vpc_connectivity_manager(
                connectivity_type="peering",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="vpc-2",
            )

    def test_runtime_error_passthrough(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.side_effect = _client_error(
            "VpcLimitExceeded"
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(RuntimeError, match="Failed to create VPC peering"):
            vpc_connectivity_manager(
                connectivity_type="peering",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="vpc-2",
            )

    def test_timeout_error_passthrough(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = _mock_ec2()
        ec2.create_vpc_peering_connection.return_value = {
            "VpcPeeringConnection": {
                "VpcPeeringConnectionId": "pcx-1"
            }
        }
        ec2.describe_vpc_peering_connections.return_value = {
            "VpcPeeringConnections": [
                {"Status": {"Code": "pending-acceptance"}}
            ]
        }
        calls = iter([0.0, 0.0, 200.0])
        monkeypatch.setattr(mod.time, "monotonic", lambda: next(calls))
        monkeypatch.setattr(mod.time, "sleep", lambda _: None)
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: ec2)
        with pytest.raises(TimeoutError):
            vpc_connectivity_manager(
                connectivity_type="peering",
                requestor_vpc_id="vpc-1",
                acceptor_vpc_id="vpc-2",
            )


# ---------------------------------------------------------------------------
# vpc_lattice_service_registrar
# ---------------------------------------------------------------------------


class TestVpcLatticeServiceRegistrar:
    def _factory(self, lattice: MagicMock, r53: MagicMock) -> object:
        def _get_client(service: str, *a: object, **kw: object) -> MagicMock:
            if service == "vpc-lattice":
                return lattice
            if service == "route53":
                return r53
            return MagicMock()
        return _get_client

    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        lattice = MagicMock()
        lattice.create_target_group.return_value = {"arn": "arn:tg-1"}
        lattice.create_service.return_value = {"arn": "arn:svc-1"}
        r53 = MagicMock()
        r53.change_resource_record_sets.return_value = {
            "ChangeInfo": {"Id": "/change/C123"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        result = mod.vpc_lattice_service_registrar(
            service_network_id="sn-1",
            target_type="LAMBDA",
            target_id="arn:aws:lambda:us-east-1:123:function:my-fn",
            port=443,
            hosted_zone_id="Z123",
            domain_name="svc.example.com",
        )
        assert result.target_group_arn == "arn:tg-1"
        assert result.service_arn == "arn:svc-1"
        assert result.route53_change_id == "/change/C123"
        lattice.register_targets.assert_called_once()
        lattice.create_service_network_service_association.assert_called_once()

    def test_create_target_group_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        lattice = MagicMock()
        lattice.create_target_group.side_effect = _client_error("ValidationException")
        r53 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        with pytest.raises(RuntimeError, match="create_target_group failed"):
            mod.vpc_lattice_service_registrar(
                service_network_id="sn-1",
                target_type="IP",
                target_id="10.0.0.1",
                port=80,
                hosted_zone_id="Z1",
                domain_name="x.com",
            )

    def test_register_targets_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        lattice = MagicMock()
        lattice.create_target_group.return_value = {"arn": "arn:tg-1"}
        lattice.register_targets.side_effect = _client_error("AccessDenied")
        r53 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        with pytest.raises(RuntimeError, match="register_targets failed"):
            mod.vpc_lattice_service_registrar(
                service_network_id="sn-1",
                target_type="IP",
                target_id="10.0.0.1",
                port=80,
                hosted_zone_id="Z1",
                domain_name="x.com",
            )

    def test_service_creation_failure_is_best_effort(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        lattice = MagicMock()
        lattice.create_target_group.return_value = {"arn": "arn:tg-1"}
        lattice.create_service.side_effect = _client_error("ConflictException")
        r53 = MagicMock()
        r53.change_resource_record_sets.return_value = {
            "ChangeInfo": {"Id": "/change/C456"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        result = mod.vpc_lattice_service_registrar(
            service_network_id="sn-1",
            target_type="LAMBDA",
            target_id="arn:fn",
            port=443,
            hosted_zone_id="Z1",
            domain_name="svc.example.com",
        )
        assert result.service_arn is None
        assert result.route53_change_id == "/change/C456"

    def test_service_arn_none_skips_association(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        lattice = MagicMock()
        lattice.create_target_group.return_value = {"arn": "arn:tg-1"}
        lattice.create_service.return_value = {"arn": None}
        r53 = MagicMock()
        r53.change_resource_record_sets.return_value = {
            "ChangeInfo": {"Id": "/change/C789"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        result = mod.vpc_lattice_service_registrar(
            service_network_id="sn-1",
            target_type="LAMBDA",
            target_id="arn:fn",
            port=80,
            hosted_zone_id="Z1",
            domain_name="svc.example.com",
        )
        assert result.service_arn is None
        lattice.create_service_network_service_association.assert_not_called()

    def test_route53_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        lattice = MagicMock()
        lattice.create_target_group.return_value = {"arn": "arn:tg-1"}
        lattice.create_service.return_value = {"arn": None}
        r53 = MagicMock()
        r53.change_resource_record_sets.side_effect = _client_error("NoSuchHostedZone")
        monkeypatch.setattr(mod, "get_client", self._factory(lattice, r53))
        with pytest.raises(RuntimeError, match="route53 upsert failed"):
            mod.vpc_lattice_service_registrar(
                service_network_id="sn-1",
                target_type="IP",
                target_id="10.0.0.1",
                port=80,
                hosted_zone_id="ZBAD",
                domain_name="x.com",
            )


# ---------------------------------------------------------------------------
# transit_gateway_route_auditor
# ---------------------------------------------------------------------------


class TestTransitGatewayRouteAuditor:
    def _factory(self, ec2: MagicMock, s3: MagicMock) -> object:
        def _get_client(service: str, *a: object, **kw: object) -> MagicMock:
            if service == "ec2":
                return ec2
            if service == "s3":
                return s3
            return MagicMock()
        return _get_client

    def test_success_with_overlapping_cidrs(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.return_value = {
            "TransitGatewayRouteTables": [
                {"TransitGatewayRouteTableId": "tgw-rt-1"},
                {"TransitGatewayRouteTableId": "tgw-rt-2"},
            ]
        }
        ec2.search_transit_gateway_routes.side_effect = [
            {
                "Routes": [
                    {"DestinationCidrBlock": "10.0.0.0/16", "State": "active"},
                ]
            },
            {
                "Routes": [
                    {"DestinationCidrBlock": "10.0.0.0/24", "State": "active"},
                ]
            },
        ]
        s3 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        result = mod.transit_gateway_route_auditor(
            transit_gateway_id="tgw-1",
            bucket="audit-bucket",
            report_key="audit/report.json",
        )
        assert result.route_tables_checked == 2
        assert result.total_routes == 2
        assert len(result.overlapping_cidrs) == 1
        assert result.report_s3_key == "audit/report.json"
        s3.put_object.assert_called_once()

    def test_success_no_overlaps(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.return_value = {
            "TransitGatewayRouteTables": [
                {"TransitGatewayRouteTableId": "tgw-rt-1"},
            ]
        }
        ec2.search_transit_gateway_routes.return_value = {
            "Routes": [
                {"DestinationCidrBlock": "10.0.0.0/16", "State": "active"},
                {"DestinationCidrBlock": "172.16.0.0/12", "State": "active"},
            ]
        }
        s3 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        result = mod.transit_gateway_route_auditor("tgw-1", "b", "k")
        assert result.overlapping_cidrs == []
        assert result.total_routes == 2

    def test_describe_route_tables_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.side_effect = _client_error(
            "AccessDenied"
        )
        s3 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        with pytest.raises(RuntimeError, match="describe route tables failed"):
            mod.transit_gateway_route_auditor("tgw-1", "b", "k")

    def test_search_routes_error_continues(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.return_value = {
            "TransitGatewayRouteTables": [
                {"TransitGatewayRouteTableId": "tgw-rt-1"},
                {"TransitGatewayRouteTableId": "tgw-rt-2"},
            ]
        }
        ec2.search_transit_gateway_routes.side_effect = [
            _client_error("InvalidParameterValue"),
            {"Routes": [{"DestinationCidrBlock": "10.0.0.0/8", "State": "active"}]},
        ]
        s3 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        result = mod.transit_gateway_route_auditor("tgw-1", "b", "k")
        assert result.route_tables_checked == 2
        assert result.total_routes == 1

    def test_s3_upload_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.return_value = {
            "TransitGatewayRouteTables": []
        }
        s3 = MagicMock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        with pytest.raises(RuntimeError, match="S3 upload failed"):
            mod.transit_gateway_route_auditor("tgw-1", "b", "k")

    def test_empty_route_tables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ec2 = MagicMock()
        ec2.describe_transit_gateway_route_tables.return_value = {
            "TransitGatewayRouteTables": []
        }
        s3 = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(ec2, s3))
        result = mod.transit_gateway_route_auditor("tgw-1", "b", "k")
        assert result.route_tables_checked == 0
        assert result.total_routes == 0
        assert result.overlapping_cidrs == []


# ---------------------------------------------------------------------------
# _cidrs_overlap helper
# ---------------------------------------------------------------------------


class TestCidrsOverlap:
    def test_overlapping(self) -> None:
        assert mod._cidrs_overlap("10.0.0.0/8", "10.0.0.0/16") is True

    def test_non_overlapping(self) -> None:
        assert mod._cidrs_overlap("10.0.0.0/8", "172.16.0.0/12") is False

    def test_invalid_cidr(self) -> None:
        assert mod._cidrs_overlap("notacidr", "10.0.0.0/8") is False


# ---------------------------------------------------------------------------
# route53_health_check_manager
# ---------------------------------------------------------------------------


class TestRoute53HealthCheckManager:
    def _factory(self, r53: MagicMock, cw: MagicMock) -> object:
        def _get_client(service: str, *a: object, **kw: object) -> MagicMock:
            if service == "route53":
                return r53
            if service == "cloudwatch":
                return cw
            return MagicMock()
        return _get_client

    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time
        monkeypatch.setattr(_time, "time", lambda: 1000000.0)
        r53 = MagicMock()
        r53.create_health_check.return_value = {
            "HealthCheck": {"Id": "hc-1"}
        }
        cw = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(r53, cw))
        result = mod.route53_health_check_manager(
            endpoints=[
                {"fqdn": "api.example.com", "port": 443, "path": "/health"},
                {"fqdn": "web.example.com"},
            ],
            alarm_prefix="prod",
            sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
        )
        assert result.health_checks_created == 2
        assert result.alarms_created == 2
        assert result.health_check_ids == ["hc-1", "hc-1"]

    def test_http_endpoint(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import time as _time
        monkeypatch.setattr(_time, "time", lambda: 1000000.0)
        r53 = MagicMock()
        r53.create_health_check.return_value = {
            "HealthCheck": {"Id": "hc-http"}
        }
        cw = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(r53, cw))
        result = mod.route53_health_check_manager(
            endpoints=[{"fqdn": "app.example.com", "port": 80, "path": "/ping"}],
            alarm_prefix="test",
            sns_topic_arn="arn:sns:topic",
        )
        assert result.health_checks_created == 1

    def test_create_health_check_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import time as _time
        monkeypatch.setattr(_time, "time", lambda: 1000000.0)
        r53 = MagicMock()
        r53.create_health_check.side_effect = _client_error("InvalidInput")
        cw = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(r53, cw))
        with pytest.raises(RuntimeError, match="create_health_check failed"):
            mod.route53_health_check_manager(
                endpoints=[{"fqdn": "x.com"}],
                alarm_prefix="p",
                sns_topic_arn="arn:topic",
            )

    def test_put_metric_alarm_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import time as _time
        monkeypatch.setattr(_time, "time", lambda: 1000000.0)
        r53 = MagicMock()
        r53.create_health_check.return_value = {
            "HealthCheck": {"Id": "hc-1"}
        }
        cw = MagicMock()
        cw.put_metric_alarm.side_effect = _client_error("LimitExceeded")
        monkeypatch.setattr(mod, "get_client", self._factory(r53, cw))
        with pytest.raises(RuntimeError, match="put_metric_alarm failed"):
            mod.route53_health_check_manager(
                endpoints=[{"fqdn": "x.com"}],
                alarm_prefix="p",
                sns_topic_arn="arn:topic",
            )

    def test_empty_endpoints(self, monkeypatch: pytest.MonkeyPatch) -> None:
        r53 = MagicMock()
        cw = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(r53, cw))
        result = mod.route53_health_check_manager(
            endpoints=[],
            alarm_prefix="p",
            sns_topic_arn="arn:topic",
        )
        assert result.health_checks_created == 0
        assert result.alarms_created == 0
        assert result.health_check_ids == []


# ---------------------------------------------------------------------------
# eventbridge_cross_account_forwarder
# ---------------------------------------------------------------------------


class TestEventbridgeCrossAccountForwarder:
    def _factory(self, events: MagicMock, sts: MagicMock) -> object:
        def _get_client(service: str, *a: object, **kw: object) -> MagicMock:
            if service == "events":
                return events
            if service == "sts":
                return sts
            return MagicMock()
        return _get_client

    def test_success_with_explicit_source(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        events = MagicMock()
        events.put_rule.return_value = {"RuleArn": "arn:rule-1"}
        sts = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(events, sts))
        result = mod.eventbridge_cross_account_forwarder(
            rule_name="forward-rule",
            event_pattern={"source": ["aws.ec2"]},
            target_event_bus_arn="arn:bus:target",
            target_account_id="999999999999",
            source_account_id="111111111111",
        )
        assert result.rule_arn == "arn:rule-1"
        assert result.target_id == "forward-to-999999999999"
        assert result.source_account == "111111111111"
        sts.get_caller_identity.assert_not_called()
        events.put_targets.assert_called_once()

    def test_success_auto_detect_source(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        events = MagicMock()
        events.put_rule.return_value = {"RuleArn": "arn:rule-2"}
        sts = MagicMock()
        sts.get_caller_identity.return_value = {"Account": "222222222222"}
        monkeypatch.setattr(mod, "get_client", self._factory(events, sts))
        result = mod.eventbridge_cross_account_forwarder(
            rule_name="auto-rule",
            event_pattern={"source": ["aws.s3"]},
            target_event_bus_arn="arn:bus:t",
            target_account_id="333333333333",
        )
        assert result.source_account == "222222222222"

    def test_sts_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        events = MagicMock()
        sts = MagicMock()
        sts.get_caller_identity.side_effect = _client_error("AccessDenied")
        monkeypatch.setattr(mod, "get_client", self._factory(events, sts))
        with pytest.raises(RuntimeError, match="get_caller_identity failed"):
            mod.eventbridge_cross_account_forwarder(
                rule_name="r",
                event_pattern={},
                target_event_bus_arn="arn:bus",
                target_account_id="111",
            )

    def test_put_rule_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        events = MagicMock()
        events.put_rule.side_effect = _client_error("AccessDenied")
        sts = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(events, sts))
        with pytest.raises(RuntimeError, match="put_rule failed"):
            mod.eventbridge_cross_account_forwarder(
                rule_name="r",
                event_pattern={},
                target_event_bus_arn="arn:bus",
                target_account_id="111",
                source_account_id="222",
            )

    def test_put_targets_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        events = MagicMock()
        events.put_rule.return_value = {"RuleArn": "arn:rule"}
        events.put_targets.side_effect = _client_error("InternalException")
        sts = MagicMock()
        monkeypatch.setattr(mod, "get_client", self._factory(events, sts))
        with pytest.raises(RuntimeError, match="put_targets failed"):
            mod.eventbridge_cross_account_forwarder(
                rule_name="r",
                event_pattern={},
                target_event_bus_arn="arn:bus",
                target_account_id="111",
                source_account_id="222",
            )


# ---------------------------------------------------------------------------
# Model tests — new networking additions
# ---------------------------------------------------------------------------


class TestLatticeRegistrationResult:
    def test_create(self) -> None:
        r = mod.LatticeRegistrationResult(
            target_group_arn="arn:tg",
            service_arn="arn:svc",
            route53_change_id="/change/C1",
        )
        assert r.target_group_arn == "arn:tg"

    def test_frozen(self) -> None:
        r = mod.LatticeRegistrationResult(
            target_group_arn="arn:tg",
            service_arn=None,
            route53_change_id="/change/C1",
        )
        with pytest.raises(Exception):
            r.target_group_arn = "other"  # type: ignore[misc]


class TestTGWAuditResult:
    def test_create(self) -> None:
        r = mod.TGWAuditResult(
            route_tables_checked=2,
            total_routes=10,
            overlapping_cidrs=[],
            report_s3_key="k",
        )
        assert r.route_tables_checked == 2


class TestHealthCheckManagerResult:
    def test_create(self) -> None:
        r = mod.HealthCheckManagerResult(
            health_checks_created=3,
            alarms_created=3,
            health_check_ids=["hc-1", "hc-2", "hc-3"],
        )
        assert r.health_checks_created == 3


class TestCrossAccountForwardResult:
    def test_create(self) -> None:
        r = mod.CrossAccountForwardResult(
            rule_arn="arn:rule",
            target_id="tgt-1",
            source_account="123",
        )
        assert r.rule_arn == "arn:rule"
