"""Native async networking utilities using :mod:`aws_util.aio._engine`.

Automates VPC peering, Transit Gateway attachments, and PrivateLink
endpoint creation with route table updates, security group rules,
and optional Route 53 DNS integration.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error
from aws_util.networking import (
    CrossAccountForwardResult,
    HealthCheckManagerResult,
    LatticeRegistrationResult,
    TGWAuditResult,
    VPCConnectivityResult,
    _cidrs_overlap,
)

__all__ = [
    "CrossAccountForwardResult",
    "HealthCheckManagerResult",
    "LatticeRegistrationResult",
    "TGWAuditResult",
    "VPCConnectivityResult",
    "eventbridge_cross_account_forwarder",
    "route53_health_check_manager",
    "transit_gateway_route_auditor",
    "vpc_connectivity_manager",
    "vpc_lattice_service_registrar",
]


# ---------------------------------------------------------------------------
# Internal helpers -- routing & security groups
# ---------------------------------------------------------------------------


async def _add_routes(
    client: Any,
    route_table_ids: list[str],
    destination_cidr: str,
    target_key: str,
    target_value: str,
) -> list[str]:
    """Add a route to each route table and return descriptions."""
    created: list[str] = []
    for rt_id in route_table_ids:
        kwargs: dict[str, Any] = {
            "RouteTableId": rt_id,
            "DestinationCidrBlock": destination_cidr,
            target_key: target_value,
        }
        try:
            await client.call("CreateRoute", **kwargs)
            created.append(f"{rt_id} -> {destination_cidr} via {target_value}")
        except RuntimeError as exc:
            if "RouteAlreadyExists" in str(exc):
                created.append(f"{rt_id} -> {destination_cidr} (already exists)")
            else:
                raise wrap_aws_error(exc, f"Failed to create route in {rt_id}") from exc
    return created


async def _add_security_group_rules(
    client: Any,
    security_group_ids: list[str],
    cidr: str,
    ports: list[int],
) -> list[str]:
    """Add ingress rules to each security group for *cidr* and *ports*.

    Returns a list of human-readable descriptions of rules added.
    """
    added: list[str] = []
    for sg_id in security_group_ids:
        for port in ports:
            try:
                await client.call(
                    "AuthorizeSecurityGroupIngress",
                    GroupId=sg_id,
                    IpPermissions=[
                        {
                            "IpProtocol": "tcp",
                            "FromPort": port,
                            "ToPort": port,
                            "IpRanges": [
                                {
                                    "CidrIp": cidr,
                                    "Description": ("VPC connectivity rule"),
                                }
                            ],
                        }
                    ],
                )
                added.append(f"{sg_id}: tcp/{port} from {cidr}")
            except RuntimeError as exc:
                if "InvalidPermission.Duplicate" in str(exc):
                    added.append(f"{sg_id}: tcp/{port} from {cidr} (already exists)")
                else:
                    raise wrap_aws_error(exc, f"Failed to add SG rule to {sg_id}") from exc
    return added


async def _create_dns_record(
    hosted_zone_id: str,
    record_name: str,
    target_dns: str,
    region_name: str | None,
) -> list[str]:
    """Create a Route 53 CNAME record pointing at *target_dns*."""
    r53 = async_client("route53", region_name)
    try:
        await r53.call(
            "ChangeResourceRecordSets",
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                "Comment": "VPC connectivity DNS record",
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": record_name,
                            "Type": "CNAME",
                            "TTL": 300,
                            "ResourceRecords": [
                                {"Value": target_dns},
                            ],
                        },
                    }
                ],
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to create DNS record {record_name!r}") from exc

    return [f"{record_name} -> {target_dns}"]


# ---------------------------------------------------------------------------
# Internal helpers -- peering
# ---------------------------------------------------------------------------


async def _setup_peering(
    client: Any,
    requestor_vpc_id: str,
    acceptor_vpc_id: str,
    requestor_route_table_ids: list[str],
    acceptor_route_table_ids: list[str],
    requestor_cidr: str,
    acceptor_cidr: str,
    security_group_ids: list[str],
    allowed_ports: list[int],
) -> tuple[str, str, list[str], list[str]]:
    """Create and accept a VPC peering connection.

    Returns ``(connection_id, status, routes, sg_rules)``.
    """
    # Create peering connection.
    try:
        resp = await client.call(
            "CreateVpcPeeringConnection",
            VpcId=requestor_vpc_id,
            PeerVpcId=acceptor_vpc_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to create VPC peering between {requestor_vpc_id} and {acceptor_vpc_id}"
        ) from exc

    pcx = resp["VpcPeeringConnection"]
    pcx_id: str = pcx["VpcPeeringConnectionId"]

    # Accept the peering.
    try:
        await client.call(
            "AcceptVpcPeeringConnection",
            VpcPeeringConnectionId=pcx_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to accept VPC peering {pcx_id}") from exc

    # Wait briefly for the peering to become active.
    status = await _wait_for_peering(client, pcx_id)

    # Update route tables.
    routes: list[str] = []
    if requestor_route_table_ids:
        routes.extend(
            await _add_routes(
                client,
                requestor_route_table_ids,
                acceptor_cidr,
                "VpcPeeringConnectionId",
                pcx_id,
            )
        )
    if acceptor_route_table_ids:
        routes.extend(
            await _add_routes(
                client,
                acceptor_route_table_ids,
                requestor_cidr,
                "VpcPeeringConnectionId",
                pcx_id,
            )
        )

    # Security group rules.
    sg_rules: list[str] = []
    if security_group_ids and allowed_ports:
        sg_rules.extend(
            await _add_security_group_rules(
                client,
                security_group_ids,
                acceptor_cidr,
                allowed_ports,
            )
        )
        sg_rules.extend(
            await _add_security_group_rules(
                client,
                security_group_ids,
                requestor_cidr,
                allowed_ports,
            )
        )

    return pcx_id, status, routes, sg_rules


async def _wait_for_peering(
    client: Any,
    pcx_id: str,
    timeout: float = 120.0,
    poll_interval: float = 5.0,
) -> str:
    """Wait for a peering connection to become ``active``."""
    deadline = time.monotonic() + timeout
    while True:
        try:
            resp = await client.call(
                "DescribeVpcPeeringConnections",
                VpcPeeringConnectionIds=[pcx_id],
            )
        except RuntimeError as exc:
            raise wrap_aws_error(exc, f"Failed to describe peering {pcx_id}") from exc

        pcxs = resp.get("VpcPeeringConnections", [])
        if not pcxs:
            raise AwsServiceError(f"Peering connection {pcx_id} not found")

        status_code = pcxs[0].get("Status", {}).get("Code", "unknown")
        if status_code == "active":
            return status_code
        if status_code in ("failed", "rejected", "deleted"):
            msg = pcxs[0].get("Status", {}).get("Message", "")
            raise AwsServiceError(f"Peering {pcx_id} reached terminal state {status_code!r}: {msg}")
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Peering {pcx_id} did not become active "
                f"within {timeout}s (current: {status_code!r})"
            )
        await asyncio.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Internal helpers -- transit gateway
# ---------------------------------------------------------------------------


async def _setup_transit_gateway(
    client: Any,
    transit_gateway_id: str,
    requestor_vpc_id: str,
    acceptor_vpc_id: str,
    requestor_route_table_ids: list[str],
    acceptor_route_table_ids: list[str],
    requestor_cidr: str,
    acceptor_cidr: str,
    security_group_ids: list[str],
    allowed_ports: list[int],
    region_name: str | None,
) -> tuple[str, str, list[str], list[str]]:
    """Attach VPCs to a transit gateway and configure routing.

    Returns ``(attachment_id, status, routes, sg_rules)``.
    """
    # Describe the TGW to get its route table.
    try:
        tgw_resp = await client.call(
            "DescribeTransitGateways",
            TransitGatewayIds=[transit_gateway_id],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to describe transit gateway {transit_gateway_id}"
        ) from exc

    tgws = tgw_resp.get("TransitGateways", [])
    if not tgws:
        raise AwsServiceError(f"Transit gateway {transit_gateway_id} not found")

    # Attach requestor VPC.
    req_subnet_ids = await _get_vpc_subnets(client, requestor_vpc_id)
    try:
        att_resp = await client.call(
            "CreateTransitGatewayVpcAttachment",
            TransitGatewayId=transit_gateway_id,
            VpcId=requestor_vpc_id,
            SubnetIds=req_subnet_ids[:1] if req_subnet_ids else [],
        )
        req_att_id: str = att_resp["TransitGatewayVpcAttachment"]["TransitGatewayAttachmentId"]
    except RuntimeError as exc:
        if "DuplicateTransitGatewayAttachment" in str(exc):
            req_att_id = await _find_existing_tgw_attachment(
                client, transit_gateway_id, requestor_vpc_id
            )
        else:
            raise wrap_aws_error(
                exc, f"Failed to attach {requestor_vpc_id} to TGW {transit_gateway_id}"
            ) from exc

    # Attach acceptor VPC.
    acc_subnet_ids = await _get_vpc_subnets(client, acceptor_vpc_id)
    try:
        att_resp2 = await client.call(
            "CreateTransitGatewayVpcAttachment",
            TransitGatewayId=transit_gateway_id,
            VpcId=acceptor_vpc_id,
            SubnetIds=acc_subnet_ids[:1] if acc_subnet_ids else [],
        )
        att_resp2["TransitGatewayVpcAttachment"]["TransitGatewayAttachmentId"]
    except RuntimeError as exc:
        if "DuplicateTransitGatewayAttachment" in str(exc):
            await _find_existing_tgw_attachment(client, transit_gateway_id, acceptor_vpc_id)
        else:
            raise wrap_aws_error(
                exc, f"Failed to attach {acceptor_vpc_id} to TGW {transit_gateway_id}"
            ) from exc

    # Update VPC route tables to route through TGW.
    routes: list[str] = []
    if requestor_route_table_ids:
        routes.extend(
            await _add_routes(
                client,
                requestor_route_table_ids,
                acceptor_cidr,
                "TransitGatewayId",
                transit_gateway_id,
            )
        )
    if acceptor_route_table_ids:
        routes.extend(
            await _add_routes(
                client,
                acceptor_route_table_ids,
                requestor_cidr,
                "TransitGatewayId",
                transit_gateway_id,
            )
        )

    # Security group rules.
    sg_rules: list[str] = []
    if security_group_ids and allowed_ports:
        sg_rules.extend(
            await _add_security_group_rules(
                client,
                security_group_ids,
                acceptor_cidr,
                allowed_ports,
            )
        )
        sg_rules.extend(
            await _add_security_group_rules(
                client,
                security_group_ids,
                requestor_cidr,
                allowed_ports,
            )
        )

    # Use the requestor attachment as the canonical connection ID.
    status = await _describe_tgw_attachment_status(client, req_att_id)
    return req_att_id, status, routes, sg_rules


async def _get_vpc_subnets(client: Any, vpc_id: str) -> list[str]:
    """Return subnet IDs for a VPC (one per AZ)."""
    try:
        resp = await client.call(
            "DescribeSubnets",
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}],
        )
    except RuntimeError:
        return []

    seen_azs: set[str] = set()
    subnet_ids: list[str] = []
    for s in resp.get("Subnets", []):
        az = s.get("AvailabilityZone", "")
        if az not in seen_azs:
            seen_azs.add(az)
            subnet_ids.append(s["SubnetId"])
    return subnet_ids


async def _find_existing_tgw_attachment(
    client: Any,
    tgw_id: str,
    vpc_id: str,
) -> str:
    """Find an existing TGW-VPC attachment ID."""
    try:
        resp = await client.call(
            "DescribeTransitGatewayVpcAttachments",
            Filters=[
                {
                    "Name": "transit-gateway-id",
                    "Values": [tgw_id],
                },
                {"Name": "vpc-id", "Values": [vpc_id]},
            ],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to find existing TGW attachment for VPC {vpc_id}"
        ) from exc

    attachments = resp.get("TransitGatewayVpcAttachments", [])
    if not attachments:
        raise AwsServiceError(f"No existing TGW attachment found for VPC {vpc_id} on TGW {tgw_id}")
    return attachments[0]["TransitGatewayAttachmentId"]


async def _describe_tgw_attachment_status(
    client: Any,
    attachment_id: str,
) -> str:
    """Return the state of a transit gateway attachment."""
    try:
        resp = await client.call(
            "DescribeTransitGatewayVpcAttachments",
            TransitGatewayAttachmentIds=[attachment_id],
        )
        atts = resp.get("TransitGatewayVpcAttachments", [])
        if atts:
            return atts[0].get("State", "unknown")
    except RuntimeError:
        pass
    return "unknown"


# ---------------------------------------------------------------------------
# Internal helpers -- PrivateLink
# ---------------------------------------------------------------------------


async def _setup_privatelink(
    client: Any,
    nlb_arn: str,
    service_name: str | None,
    requestor_vpc_id: str,
    acceptor_vpc_id: str,
    security_group_ids: list[str],
    allowed_ports: list[int],
    requestor_cidr: str,
    region_name: str | None,
) -> tuple[str, str, list[str], list[str]]:
    """Create a VPC endpoint service backed by an NLB and an
    interface endpoint in the consumer VPC.

    Returns ``(endpoint_id, status, routes, sg_rules)``.
    """
    # Create the VPC endpoint service in the provider VPC.
    try:
        svc_resp = await client.call(
            "CreateVpcEndpointServiceConfiguration",
            NetworkLoadBalancerArns=[nlb_arn],
            AcceptanceRequired=False,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to create VPC endpoint service for NLB {nlb_arn}"
        ) from exc

    svc_cfg = svc_resp["ServiceConfiguration"]
    svc_id: str = svc_cfg["ServiceId"]
    svc_names = svc_cfg.get("ServiceName") or service_name

    # Resolve service name for endpoint creation.
    endpoint_svc_name = (
        svc_names
        if isinstance(svc_names, str)
        else svc_names[0]
        if isinstance(svc_names, list) and svc_names
        else service_name or svc_id
    )

    # Get subnets in the consumer VPC.
    consumer_subnets = await _get_vpc_subnets(client, requestor_vpc_id)

    # Create the interface endpoint in the consumer VPC.
    ep_kwargs: dict[str, Any] = {
        "VpcEndpointType": "Interface",
        "VpcId": requestor_vpc_id,
        "ServiceName": endpoint_svc_name,
    }
    if consumer_subnets:
        ep_kwargs["SubnetIds"] = consumer_subnets
    if security_group_ids:
        ep_kwargs["SecurityGroupIds"] = security_group_ids

    try:
        ep_resp = await client.call("CreateVpcEndpoint", **ep_kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"Failed to create VPC interface endpoint in {requestor_vpc_id}"
        ) from exc

    endpoint = ep_resp["VpcEndpoint"]
    endpoint_id: str = endpoint["VpcEndpointId"]
    status = endpoint.get("State", "unknown")

    # No explicit route entries needed for PrivateLink.
    routes: list[str] = []

    # Security group rules for the consumer side.
    sg_rules: list[str] = []
    if security_group_ids and allowed_ports:
        sg_rules.extend(
            await _add_security_group_rules(
                client,
                security_group_ids,
                requestor_cidr,
                allowed_ports,
            )
        )

    return endpoint_id, status, routes, sg_rules


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def vpc_connectivity_manager(
    connectivity_type: str,
    requestor_vpc_id: str,
    acceptor_vpc_id: str = "",
    transit_gateway_id: str | None = None,
    nlb_arn: str | None = None,
    service_name: str | None = None,
    requestor_route_table_ids: list[str] | None = None,
    acceptor_route_table_ids: list[str] | None = None,
    requestor_cidr: str = "",
    acceptor_cidr: str = "",
    security_group_ids: list[str] | None = None,
    allowed_ports: list[int] | None = None,
    hosted_zone_id: str | None = None,
    dns_record_name: str | None = None,
    region_name: str | None = None,
) -> VPCConnectivityResult:
    """Automate VPC connectivity patterns (async version).

    Supports three connectivity types:

    * ``"peering"`` -- Creates a VPC peering connection, accepts it,
      updates route tables on both sides, and adds security group
      ingress rules.
    * ``"transit_gateway"`` -- Attaches both VPCs to the specified
      transit gateway, manages route table entries, and adds
      security group rules.
    * ``"privatelink"`` -- Creates a VPC endpoint service backed by
      an NLB and an interface endpoint in the consumer VPC.

    For all types, connectivity status is validated and optional
    Route 53 DNS records can be created.

    Args:
        connectivity_type: ``"peering"``, ``"transit_gateway"``,
            or ``"privatelink"``.
        requestor_vpc_id: VPC ID of the requestor (consumer for
            PrivateLink).
        acceptor_vpc_id: VPC ID of the acceptor / peer (used by
            ``peering`` and ``transit_gateway``).
        transit_gateway_id: Transit Gateway ID (required for
            ``transit_gateway``).
        nlb_arn: Network Load Balancer ARN (required for
            ``privatelink``).
        service_name: VPC endpoint service name (for
            ``privatelink``).
        requestor_route_table_ids: Route table IDs in the
            requestor VPC to update.
        acceptor_route_table_ids: Route table IDs in the acceptor
            VPC to update.
        requestor_cidr: CIDR block of the requestor VPC.
        acceptor_cidr: CIDR block of the acceptor VPC.
        security_group_ids: Security groups to update with
            ingress rules.
        allowed_ports: TCP ports to allow in security group rules.
        hosted_zone_id: Route 53 private hosted zone ID for
            optional DNS record creation.
        dns_record_name: DNS record name to create.
        region_name: AWS region override.

    Returns:
        A :class:`VPCConnectivityResult` with the connection ID,
        status, routes created, security group rules, and DNS
        records.

    Raises:
        ValueError: If *connectivity_type* is not recognised or
            required parameters are missing.
        RuntimeError: If any underlying AWS API call fails.
        TimeoutError: If a peering connection does not become
            active within the timeout.
    """
    valid_types = {"peering", "transit_gateway", "privatelink"}
    if connectivity_type not in valid_types:
        raise ValueError(
            f"connectivity_type must be one of {valid_types}, got {connectivity_type!r}"
        )

    req_rts = requestor_route_table_ids or []
    acc_rts = acceptor_route_table_ids or []
    sg_ids = security_group_ids or []
    ports = allowed_ports or []

    try:
        ec2 = async_client("ec2", region_name)

        connection_id: str
        status: str
        routes: list[str]
        sg_rules: list[str]

        if connectivity_type == "peering":
            if not acceptor_vpc_id:
                raise ValueError("acceptor_vpc_id is required for peering")
            connection_id, status, routes, sg_rules = await _setup_peering(
                ec2,
                requestor_vpc_id,
                acceptor_vpc_id,
                req_rts,
                acc_rts,
                requestor_cidr,
                acceptor_cidr,
                sg_ids,
                ports,
            )

        elif connectivity_type == "transit_gateway":
            if not transit_gateway_id:
                raise ValueError("transit_gateway_id is required for transit_gateway connectivity")
            if not acceptor_vpc_id:
                raise ValueError("acceptor_vpc_id is required for transit_gateway connectivity")
            connection_id, status, routes, sg_rules = await _setup_transit_gateway(
                ec2,
                transit_gateway_id,
                requestor_vpc_id,
                acceptor_vpc_id,
                req_rts,
                acc_rts,
                requestor_cidr,
                acceptor_cidr,
                sg_ids,
                ports,
                region_name,
            )

        else:  # privatelink
            if not nlb_arn:
                raise ValueError("nlb_arn is required for privatelink connectivity")
            connection_id, status, routes, sg_rules = await _setup_privatelink(
                ec2,
                nlb_arn,
                service_name,
                requestor_vpc_id,
                acceptor_vpc_id,
                sg_ids,
                ports,
                requestor_cidr,
                region_name,
            )

        # Optional DNS record creation.
        dns_records: list[str] = []
        if hosted_zone_id and dns_record_name:
            target_dns = connection_id
            dns_records = await _create_dns_record(
                hosted_zone_id,
                dns_record_name,
                target_dns,
                region_name,
            )

        return VPCConnectivityResult(
            connectivity_type=connectivity_type,
            connection_id=connection_id,
            status=status,
            routes_created=routes,
            security_group_rules_added=sg_rules,
            dns_records_created=dns_records,
        )

    except (RuntimeError, ValueError, TimeoutError):
        raise
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"vpc_connectivity_manager failed for {connectivity_type!r}"
        ) from exc


# ---------------------------------------------------------------------------
# New networking additions (async)
# ---------------------------------------------------------------------------


async def vpc_lattice_service_registrar(
    service_network_id: str,
    target_type: str,
    target_id: str,
    port: int,
    hosted_zone_id: str,
    domain_name: str,
    health_check_path: str = "/health",
    region_name: str | None = None,
) -> LatticeRegistrationResult:
    """Register an ECS service or Lambda as a VPC Lattice target (async).

    Args:
        service_network_id: VPC Lattice service network ID or ARN.
        target_type: Target type — ``"INSTANCE"``, ``"IP"``, ``"LAMBDA"``, or ``"ALB"``.
        target_id: ARN or ID of the target.
        port: Port for the target group.
        hosted_zone_id: Route 53 hosted zone ID for the alias record.
        domain_name: Domain name for the Route 53 alias.
        health_check_path: HTTP path for health checks (default ``"/health"``).
        region_name: AWS region override.

    Returns:
        A :class:`LatticeRegistrationResult`.

    Raises:
        RuntimeError: If any AWS API call fails.
    """

    lattice = async_client("vpc-lattice", region_name)
    r53 = async_client("route53", region_name)

    try:
        tg_resp = await lattice.call(
            "CreateTargetGroup",
            name=f"tg-{target_id.split('/')[-1].split(':')[-1][:40]}",
            type=target_type,
            config={
                "port": port,
                "protocol": "HTTPS" if port == 443 else "HTTP",
                "healthCheck": {"enabled": True, "path": health_check_path},
            },
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, "vpc_lattice_service_registrar create_target_group failed"
        ) from exc

    tg_arn: str = tg_resp["arn"]

    try:
        await lattice.call(
            "RegisterTargets",
            targetGroupIdentifier=tg_arn,
            targets=[{"id": target_id, "port": port}],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "vpc_lattice_service_registrar register_targets failed") from exc

    service_arn: str | None = None
    try:
        svc_resp = await lattice.call(
            "CreateService", name=f"svc-{domain_name.replace('.', '-')[:40]}"
        )
        service_arn = svc_resp.get("arn")
        if service_arn:
            await lattice.call(
                "CreateServiceNetworkServiceAssociation",
                serviceIdentifier=service_arn,
                serviceNetworkIdentifier=service_network_id,
            )
    except RuntimeError:
        pass

    try:
        r53_resp = await r53.call(
            "ChangeResourceRecordSets",
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": domain_name,
                            "Type": "CNAME",
                            "TTL": 60,
                            "ResourceRecords": [{"Value": domain_name}],
                        },
                    }
                ]
            },
        )
        change_id: str = r53_resp["ChangeInfo"]["Id"]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "vpc_lattice_service_registrar route53 upsert failed") from exc

    return LatticeRegistrationResult(
        target_group_arn=tg_arn,
        service_arn=service_arn,
        route53_change_id=change_id,
    )


async def transit_gateway_route_auditor(
    transit_gateway_id: str,
    bucket: str,
    report_key: str,
    region_name: str | None = None,
) -> TGWAuditResult:
    """Audit Transit Gateway route tables for overlapping CIDR blocks (async).

    Args:
        transit_gateway_id: Transit Gateway ID.
        bucket: S3 bucket for the compliance report.
        report_key: S3 key for the report JSON.
        region_name: AWS region override.

    Returns:
        A :class:`TGWAuditResult`.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    import json

    ec2 = async_client("ec2", region_name)
    s3 = async_client("s3", region_name)

    try:
        rt_resp = await ec2.call(
            "DescribeTransitGatewayRouteTables",
            Filters=[{"Name": "transit-gateway-id", "Values": [transit_gateway_id]}],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, "transit_gateway_route_auditor describe route tables failed"
        ) from exc

    route_tables = rt_resp.get("TransitGatewayRouteTables", [])
    all_routes: list[dict[str, Any]] = []

    for rt in route_tables:
        rt_id = rt["TransitGatewayRouteTableId"]
        try:
            routes_resp = await ec2.call(
                "SearchTransitGatewayRoutes",
                TransitGatewayRouteTableId=rt_id,
                Filters=[{"Name": "state", "Values": ["active", "blackhole"]}],
            )
            for route in routes_resp.get("Routes", []):
                all_routes.append({"route_table_id": rt_id, **route})
        except RuntimeError:
            continue

    overlapping: list[dict[str, Any]] = []
    cidrs = [
        (r.get("DestinationCidrBlock", ""), r["route_table_id"])
        for r in all_routes
        if r.get("DestinationCidrBlock")
    ]
    for i, (cidr_a, rt_a) in enumerate(cidrs):
        for cidr_b, rt_b in cidrs[i + 1 :]:
            if rt_a != rt_b and _cidrs_overlap(cidr_a, cidr_b):
                overlapping.append({"cidr_a": cidr_a, "rt_a": rt_a, "cidr_b": cidr_b, "rt_b": rt_b})

    report = {
        "transit_gateway_id": transit_gateway_id,
        "route_tables_checked": len(route_tables),
        "total_routes": len(all_routes),
        "overlapping_cidrs": overlapping,
        "routes": all_routes,
    }
    try:
        await s3.call(
            "PutObject",
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, default=str).encode(),
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "transit_gateway_route_auditor S3 upload failed") from exc

    return TGWAuditResult(
        route_tables_checked=len(route_tables),
        total_routes=len(all_routes),
        overlapping_cidrs=overlapping,
        report_s3_key=report_key,
    )


async def route53_health_check_manager(
    endpoints: list[dict[str, Any]],
    alarm_prefix: str,
    sns_topic_arn: str,
    region_name: str | None = None,
) -> HealthCheckManagerResult:
    """Create Route 53 health checks and CloudWatch alarms for endpoints (async).

    Args:
        endpoints: List of endpoint dicts with ``fqdn``, ``port``, ``path``.
        alarm_prefix: Prefix for CloudWatch alarm names.
        sns_topic_arn: SNS topic ARN for alarm notifications.
        region_name: AWS region override.

    Returns:
        A :class:`HealthCheckManagerResult`.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    import time

    r53 = async_client("route53", region_name)
    cw = async_client("cloudwatch", region_name)

    health_check_ids: list[str] = []
    alarms_created = 0

    for ep in endpoints:
        fqdn: str = ep["fqdn"]
        port: int = int(ep.get("port", 443))
        path: str = ep.get("path", "/")
        protocol = "HTTPS" if port == 443 else "HTTP"

        try:
            hc_resp = await r53.call(
                "CreateHealthCheck",
                CallerReference=f"{fqdn}-{port}-{int(time.time())}",
                HealthCheckConfig={
                    "FullyQualifiedDomainName": fqdn,
                    "Port": port,
                    "Type": protocol,
                    "ResourcePath": path,
                    "RequestInterval": 30,
                    "FailureThreshold": 3,
                },
            )
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"route53_health_check_manager create_health_check failed for {fqdn}"
            ) from exc

        hc_id: str = hc_resp["HealthCheck"]["Id"]
        health_check_ids.append(hc_id)

        alarm_name = f"{alarm_prefix}-{fqdn.replace('.', '-')}-{port}"
        try:
            await cw.call(
                "PutMetricAlarm",
                AlarmName=alarm_name,
                Namespace="AWS/Route53",
                MetricName="HealthCheckStatus",
                Dimensions=[{"Name": "HealthCheckId", "Value": hc_id}],
                Statistic="Minimum",
                Period=60,
                EvaluationPeriods=1,
                Threshold=1.0,
                ComparisonOperator="LessThanThreshold",
                TreatMissingData="breaching",
                AlarmActions=[sns_topic_arn],
            )
            alarms_created += 1
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, f"route53_health_check_manager put_metric_alarm failed for {fqdn}"
            ) from exc

    return HealthCheckManagerResult(
        health_checks_created=len(health_check_ids),
        alarms_created=alarms_created,
        health_check_ids=health_check_ids,
    )


async def eventbridge_cross_account_forwarder(
    rule_name: str,
    event_pattern: dict[str, Any],
    target_event_bus_arn: str,
    target_account_id: str,
    source_account_id: str | None = None,
    region_name: str | None = None,
) -> CrossAccountForwardResult:
    """Create an EventBridge rule to forward events to a target account bus (async).

    Args:
        rule_name: Name for the EventBridge rule.
        event_pattern: Event pattern dict for the rule.
        target_event_bus_arn: ARN of the target account event bus.
        target_account_id: AWS account ID of the target.
        source_account_id: Source account ID (auto-detected via STS if omitted).
        region_name: AWS region override.

    Returns:
        A :class:`CrossAccountForwardResult`.

    Raises:
        RuntimeError: If any AWS API call fails.
    """
    import json

    events_client = async_client("events", region_name)
    sts = async_client("sts", region_name)

    if not source_account_id:
        try:
            identity = await sts.call("GetCallerIdentity")
            source_account_id = identity["Account"]
        except RuntimeError as exc:
            raise wrap_aws_error(
                exc, "eventbridge_cross_account_forwarder get_caller_identity failed"
            ) from exc

    try:
        rule_resp = await events_client.call(
            "PutRule",
            Name=rule_name,
            EventPattern=json.dumps(event_pattern),
            State="ENABLED",
            Description=f"Forward events to account {target_account_id}",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"eventbridge_cross_account_forwarder put_rule failed for {rule_name!r}"
        ) from exc

    rule_arn: str = rule_resp["RuleArn"]
    target_id = f"forward-to-{target_account_id}"

    try:
        await events_client.call(
            "PutTargets",
            Rule=rule_name,
            Targets=[{"Id": target_id, "Arn": target_event_bus_arn}],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "eventbridge_cross_account_forwarder put_targets failed") from exc

    return CrossAccountForwardResult(
        rule_arn=rule_arn,
        target_id=target_id,
        source_account=source_account_id,
    )
