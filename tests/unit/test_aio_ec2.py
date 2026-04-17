"""Tests for aws_util.aio.ec2 — 100 % line coverage."""
from __future__ import annotations

import base64
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.ec2 import (
    EC2Image,
    EC2Instance,
    SecurityGroup,
    create_image,
    describe_images,
    describe_instances,
    describe_security_groups,
    get_instance,
    get_instance_console_output,
    get_instances_by_tag,
    get_latest_ami,
    reboot_instances,
    start_instances,
    stop_instances,
    terminate_instances,
    wait_for_instance_state,
    accept_address_transfer,
    accept_capacity_reservation_billing_ownership,
    accept_reserved_instances_exchange_quote,
    accept_transit_gateway_multicast_domain_associations,
    accept_transit_gateway_peering_attachment,
    accept_transit_gateway_vpc_attachment,
    accept_vpc_endpoint_connections,
    accept_vpc_peering_connection,
    advertise_byoip_cidr,
    allocate_address,
    allocate_hosts,
    allocate_ipam_pool_cidr,
    apply_security_groups_to_client_vpn_target_network,
    assign_ipv6_addresses,
    assign_private_ip_addresses,
    assign_private_nat_gateway_address,
    associate_address,
    associate_capacity_reservation_billing_owner,
    associate_client_vpn_target_network,
    associate_dhcp_options,
    associate_enclave_certificate_iam_role,
    associate_iam_instance_profile,
    associate_instance_event_window,
    associate_ipam_byoasn,
    associate_ipam_resource_discovery,
    associate_nat_gateway_address,
    associate_route_server,
    associate_route_table,
    associate_security_group_vpc,
    associate_subnet_cidr_block,
    associate_transit_gateway_multicast_domain,
    associate_transit_gateway_policy_table,
    associate_transit_gateway_route_table,
    associate_trunk_interface,
    associate_vpc_cidr_block,
    attach_classic_link_vpc,
    attach_internet_gateway,
    attach_network_interface,
    attach_verified_access_trust_provider,
    attach_volume,
    attach_vpn_gateway,
    authorize_client_vpn_ingress,
    authorize_security_group_egress,
    authorize_security_group_ingress,
    bundle_instance,
    cancel_bundle_task,
    cancel_capacity_reservation,
    cancel_capacity_reservation_fleets,
    cancel_conversion_task,
    cancel_declarative_policies_report,
    cancel_export_task,
    cancel_image_launch_permission,
    cancel_import_task,
    cancel_reserved_instances_listing,
    cancel_spot_fleet_requests,
    cancel_spot_instance_requests,
    confirm_product_instance,
    copy_fpga_image,
    copy_image,
    copy_snapshot,
    copy_volumes,
    create_capacity_manager_data_export,
    create_capacity_reservation,
    create_capacity_reservation_by_splitting,
    create_capacity_reservation_fleet,
    create_carrier_gateway,
    create_client_vpn_endpoint,
    create_client_vpn_route,
    create_coip_cidr,
    create_coip_pool,
    create_customer_gateway,
    create_default_subnet,
    create_default_vpc,
    create_delegate_mac_volume_ownership_task,
    create_dhcp_options,
    create_egress_only_internet_gateway,
    create_fleet,
    create_flow_logs,
    create_fpga_image,
    create_image_usage_report,
    create_instance_connect_endpoint,
    create_instance_event_window,
    create_instance_export_task,
    create_internet_gateway,
    create_ipam,
    create_ipam_external_resource_verification_token,
    create_ipam_pool,
    create_ipam_prefix_list_resolver,
    create_ipam_prefix_list_resolver_target,
    create_ipam_resource_discovery,
    create_ipam_scope,
    create_key_pair,
    create_launch_template,
    create_launch_template_version,
    create_local_gateway_route,
    create_local_gateway_route_table,
    create_local_gateway_route_table_virtual_interface_group_association,
    create_local_gateway_route_table_vpc_association,
    create_local_gateway_virtual_interface,
    create_local_gateway_virtual_interface_group,
    create_mac_system_integrity_protection_modification_task,
    create_managed_prefix_list,
    create_nat_gateway,
    create_network_acl,
    create_network_acl_entry,
    create_network_insights_access_scope,
    create_network_insights_path,
    create_network_interface,
    create_network_interface_permission,
    create_placement_group,
    create_public_ipv4_pool,
    create_replace_root_volume_task,
    create_reserved_instances_listing,
    create_restore_image_task,
    create_route,
    create_route_server,
    create_route_server_endpoint,
    create_route_server_peer,
    create_route_table,
    create_security_group,
    create_snapshot,
    create_snapshots,
    create_spot_datafeed_subscription,
    create_store_image_task,
    create_subnet,
    create_subnet_cidr_reservation,
    create_tags,
    create_traffic_mirror_filter,
    create_traffic_mirror_filter_rule,
    create_traffic_mirror_session,
    create_traffic_mirror_target,
    create_transit_gateway,
    create_transit_gateway_connect,
    create_transit_gateway_connect_peer,
    create_transit_gateway_multicast_domain,
    create_transit_gateway_peering_attachment,
    create_transit_gateway_policy_table,
    create_transit_gateway_prefix_list_reference,
    create_transit_gateway_route,
    create_transit_gateway_route_table,
    create_transit_gateway_route_table_announcement,
    create_transit_gateway_vpc_attachment,
    create_verified_access_endpoint,
    create_verified_access_group,
    create_verified_access_instance,
    create_verified_access_trust_provider,
    create_volume,
    create_vpc,
    create_vpc_block_public_access_exclusion,
    create_vpc_endpoint,
    create_vpc_endpoint_connection_notification,
    create_vpc_endpoint_service_configuration,
    create_vpc_peering_connection,
    create_vpn_connection,
    create_vpn_connection_route,
    create_vpn_gateway,
    delete_capacity_manager_data_export,
    delete_carrier_gateway,
    delete_client_vpn_endpoint,
    delete_client_vpn_route,
    delete_coip_cidr,
    delete_coip_pool,
    delete_customer_gateway,
    delete_dhcp_options,
    delete_egress_only_internet_gateway,
    delete_fleets,
    delete_flow_logs,
    delete_fpga_image,
    delete_image_usage_report,
    delete_instance_connect_endpoint,
    delete_instance_event_window,
    delete_internet_gateway,
    delete_ipam,
    delete_ipam_external_resource_verification_token,
    delete_ipam_pool,
    delete_ipam_prefix_list_resolver,
    delete_ipam_prefix_list_resolver_target,
    delete_ipam_resource_discovery,
    delete_ipam_scope,
    delete_key_pair,
    delete_launch_template,
    delete_launch_template_versions,
    delete_local_gateway_route,
    delete_local_gateway_route_table,
    delete_local_gateway_route_table_virtual_interface_group_association,
    delete_local_gateway_route_table_vpc_association,
    delete_local_gateway_virtual_interface,
    delete_local_gateway_virtual_interface_group,
    delete_managed_prefix_list,
    delete_nat_gateway,
    delete_network_acl,
    delete_network_acl_entry,
    delete_network_insights_access_scope,
    delete_network_insights_access_scope_analysis,
    delete_network_insights_analysis,
    delete_network_insights_path,
    delete_network_interface,
    delete_network_interface_permission,
    delete_placement_group,
    delete_public_ipv4_pool,
    delete_queued_reserved_instances,
    delete_route,
    delete_route_server,
    delete_route_server_endpoint,
    delete_route_server_peer,
    delete_route_table,
    delete_security_group,
    delete_snapshot,
    delete_spot_datafeed_subscription,
    delete_subnet,
    delete_subnet_cidr_reservation,
    delete_tags,
    delete_traffic_mirror_filter,
    delete_traffic_mirror_filter_rule,
    delete_traffic_mirror_session,
    delete_traffic_mirror_target,
    delete_transit_gateway,
    delete_transit_gateway_connect,
    delete_transit_gateway_connect_peer,
    delete_transit_gateway_multicast_domain,
    delete_transit_gateway_peering_attachment,
    delete_transit_gateway_policy_table,
    delete_transit_gateway_prefix_list_reference,
    delete_transit_gateway_route,
    delete_transit_gateway_route_table,
    delete_transit_gateway_route_table_announcement,
    delete_transit_gateway_vpc_attachment,
    delete_verified_access_endpoint,
    delete_verified_access_group,
    delete_verified_access_instance,
    delete_verified_access_trust_provider,
    delete_volume,
    delete_vpc,
    delete_vpc_block_public_access_exclusion,
    delete_vpc_endpoint_connection_notifications,
    delete_vpc_endpoint_service_configurations,
    delete_vpc_endpoints,
    delete_vpc_peering_connection,
    delete_vpn_connection,
    delete_vpn_connection_route,
    delete_vpn_gateway,
    deprovision_byoip_cidr,
    deprovision_ipam_byoasn,
    deprovision_ipam_pool_cidr,
    deprovision_public_ipv4_pool_cidr,
    deregister_image,
    deregister_instance_event_notification_attributes,
    deregister_transit_gateway_multicast_group_members,
    deregister_transit_gateway_multicast_group_sources,
    describe_account_attributes,
    describe_address_transfers,
    describe_addresses,
    describe_addresses_attribute,
    describe_aggregate_id_format,
    describe_availability_zones,
    describe_aws_network_performance_metric_subscriptions,
    describe_bundle_tasks,
    describe_byoip_cidrs,
    describe_capacity_block_extension_history,
    describe_capacity_block_extension_offerings,
    describe_capacity_block_offerings,
    describe_capacity_block_status,
    describe_capacity_blocks,
    describe_capacity_manager_data_exports,
    describe_capacity_reservation_billing_requests,
    describe_capacity_reservation_fleets,
    describe_capacity_reservation_topology,
    describe_capacity_reservations,
    describe_carrier_gateways,
    describe_classic_link_instances,
    describe_client_vpn_authorization_rules,
    describe_client_vpn_connections,
    describe_client_vpn_endpoints,
    describe_client_vpn_routes,
    describe_client_vpn_target_networks,
    describe_coip_pools,
    describe_conversion_tasks,
    describe_customer_gateways,
    describe_declarative_policies_reports,
    describe_dhcp_options,
    describe_egress_only_internet_gateways,
    describe_elastic_gpus,
    describe_export_image_tasks,
    describe_export_tasks,
    describe_fast_launch_images,
    describe_fast_snapshot_restores,
    describe_fleet_history,
    describe_fleet_instances,
    describe_fleets,
    describe_flow_logs,
    describe_fpga_image_attribute,
    describe_fpga_images,
    describe_host_reservation_offerings,
    describe_host_reservations,
    describe_hosts,
    describe_iam_instance_profile_associations,
    describe_id_format,
    describe_identity_id_format,
    describe_image_attribute,
    describe_image_references,
    describe_image_usage_report_entries,
    describe_image_usage_reports,
    describe_import_image_tasks,
    describe_import_snapshot_tasks,
    describe_instance_attribute,
    describe_instance_connect_endpoints,
    describe_instance_credit_specifications,
    describe_instance_event_notification_attributes,
    describe_instance_event_windows,
    describe_instance_image_metadata,
    describe_instance_status,
    describe_instance_topology,
    describe_instance_type_offerings,
    describe_instance_types,
    describe_internet_gateways,
    describe_ipam_byoasn,
    describe_ipam_external_resource_verification_tokens,
    describe_ipam_pools,
    describe_ipam_prefix_list_resolver_targets,
    describe_ipam_prefix_list_resolvers,
    describe_ipam_resource_discoveries,
    describe_ipam_resource_discovery_associations,
    describe_ipam_scopes,
    describe_ipams,
    describe_ipv6_pools,
    describe_key_pairs,
    describe_launch_template_versions,
    describe_launch_templates,
    describe_local_gateway_route_table_virtual_interface_group_associations,
    describe_local_gateway_route_table_vpc_associations,
    describe_local_gateway_route_tables,
    describe_local_gateway_virtual_interface_groups,
    describe_local_gateway_virtual_interfaces,
    describe_local_gateways,
    describe_locked_snapshots,
    describe_mac_hosts,
    describe_mac_modification_tasks,
    describe_managed_prefix_lists,
    describe_moving_addresses,
    describe_nat_gateways,
    describe_network_acls,
    describe_network_insights_access_scope_analyses,
    describe_network_insights_access_scopes,
    describe_network_insights_analyses,
    describe_network_insights_paths,
    describe_network_interface_attribute,
    describe_network_interface_permissions,
    describe_network_interfaces,
    describe_outpost_lags,
    describe_placement_groups,
    describe_prefix_lists,
    describe_principal_id_format,
    describe_public_ipv4_pools,
    describe_regions,
    describe_replace_root_volume_tasks,
    describe_reserved_instances,
    describe_reserved_instances_listings,
    describe_reserved_instances_modifications,
    describe_reserved_instances_offerings,
    describe_route_server_endpoints,
    describe_route_server_peers,
    describe_route_servers,
    describe_route_tables,
    describe_scheduled_instance_availability,
    describe_scheduled_instances,
    describe_security_group_references,
    describe_security_group_rules,
    describe_security_group_vpc_associations,
    describe_service_link_virtual_interfaces,
    describe_snapshot_attribute,
    describe_snapshot_tier_status,
    describe_snapshots,
    describe_spot_datafeed_subscription,
    describe_spot_fleet_instances,
    describe_spot_fleet_request_history,
    describe_spot_fleet_requests,
    describe_spot_instance_requests,
    describe_spot_price_history,
    describe_stale_security_groups,
    describe_store_image_tasks,
    describe_subnets,
    describe_tags,
    describe_traffic_mirror_filter_rules,
    describe_traffic_mirror_filters,
    describe_traffic_mirror_sessions,
    describe_traffic_mirror_targets,
    describe_transit_gateway_attachments,
    describe_transit_gateway_connect_peers,
    describe_transit_gateway_connects,
    describe_transit_gateway_multicast_domains,
    describe_transit_gateway_peering_attachments,
    describe_transit_gateway_policy_tables,
    describe_transit_gateway_route_table_announcements,
    describe_transit_gateway_route_tables,
    describe_transit_gateway_vpc_attachments,
    describe_transit_gateways,
    describe_trunk_interface_associations,
    describe_verified_access_endpoints,
    describe_verified_access_groups,
    describe_verified_access_instance_logging_configurations,
    describe_verified_access_instances,
    describe_verified_access_trust_providers,
    describe_volume_attribute,
    describe_volume_status,
    describe_volumes,
    describe_volumes_modifications,
    describe_vpc_attribute,
    describe_vpc_block_public_access_exclusions,
    describe_vpc_block_public_access_options,
    describe_vpc_classic_link,
    describe_vpc_classic_link_dns_support,
    describe_vpc_endpoint_associations,
    describe_vpc_endpoint_connection_notifications,
    describe_vpc_endpoint_connections,
    describe_vpc_endpoint_service_configurations,
    describe_vpc_endpoint_service_permissions,
    describe_vpc_endpoint_services,
    describe_vpc_endpoints,
    describe_vpc_peering_connections,
    describe_vpcs,
    describe_vpn_connections,
    describe_vpn_gateways,
    detach_classic_link_vpc,
    detach_internet_gateway,
    detach_network_interface,
    detach_verified_access_trust_provider,
    detach_volume,
    detach_vpn_gateway,
    disable_address_transfer,
    disable_allowed_images_settings,
    disable_aws_network_performance_metric_subscription,
    disable_capacity_manager,
    disable_ebs_encryption_by_default,
    disable_fast_launch,
    disable_fast_snapshot_restores,
    disable_image,
    disable_image_block_public_access,
    disable_image_deprecation,
    disable_image_deregistration_protection,
    disable_ipam_organization_admin_account,
    disable_route_server_propagation,
    disable_serial_console_access,
    disable_snapshot_block_public_access,
    disable_transit_gateway_route_table_propagation,
    disable_vgw_route_propagation,
    disable_vpc_classic_link,
    disable_vpc_classic_link_dns_support,
    disassociate_address,
    disassociate_capacity_reservation_billing_owner,
    disassociate_client_vpn_target_network,
    disassociate_enclave_certificate_iam_role,
    disassociate_iam_instance_profile,
    disassociate_instance_event_window,
    disassociate_ipam_byoasn,
    disassociate_ipam_resource_discovery,
    disassociate_nat_gateway_address,
    disassociate_route_server,
    disassociate_route_table,
    disassociate_security_group_vpc,
    disassociate_subnet_cidr_block,
    disassociate_transit_gateway_multicast_domain,
    disassociate_transit_gateway_policy_table,
    disassociate_transit_gateway_route_table,
    disassociate_trunk_interface,
    disassociate_vpc_cidr_block,
    enable_address_transfer,
    enable_allowed_images_settings,
    enable_aws_network_performance_metric_subscription,
    enable_capacity_manager,
    enable_ebs_encryption_by_default,
    enable_fast_launch,
    enable_fast_snapshot_restores,
    enable_image,
    enable_image_block_public_access,
    enable_image_deprecation,
    enable_image_deregistration_protection,
    enable_ipam_organization_admin_account,
    enable_reachability_analyzer_organization_sharing,
    enable_route_server_propagation,
    enable_serial_console_access,
    enable_snapshot_block_public_access,
    enable_transit_gateway_route_table_propagation,
    enable_vgw_route_propagation,
    enable_volume_io,
    enable_vpc_classic_link,
    enable_vpc_classic_link_dns_support,
    export_client_vpn_client_certificate_revocation_list,
    export_client_vpn_client_configuration,
    export_image,
    export_transit_gateway_routes,
    export_verified_access_instance_client_configuration,
    get_active_vpn_tunnel_status,
    get_allowed_images_settings,
    get_associated_enclave_certificate_iam_roles,
    get_associated_ipv6_pool_cidrs,
    get_aws_network_performance_data,
    get_capacity_manager_attributes,
    get_capacity_manager_metric_data,
    get_capacity_manager_metric_dimensions,
    get_capacity_reservation_usage,
    get_coip_pool_usage,
    get_console_output,
    get_console_screenshot,
    get_declarative_policies_report_summary,
    get_default_credit_specification,
    get_ebs_default_kms_key_id,
    get_ebs_encryption_by_default,
    get_flow_logs_integration_template,
    get_groups_for_capacity_reservation,
    get_host_reservation_purchase_preview,
    get_image_ancestry,
    get_image_block_public_access_state,
    get_instance_metadata_defaults,
    get_instance_tpm_ek_pub,
    get_instance_types_from_instance_requirements,
    get_instance_uefi_data,
    get_ipam_address_history,
    get_ipam_discovered_accounts,
    get_ipam_discovered_public_addresses,
    get_ipam_discovered_resource_cidrs,
    get_ipam_pool_allocations,
    get_ipam_pool_cidrs,
    get_ipam_prefix_list_resolver_rules,
    get_ipam_prefix_list_resolver_version_entries,
    get_ipam_prefix_list_resolver_versions,
    get_ipam_resource_cidrs,
    get_launch_template_data,
    get_managed_prefix_list_associations,
    get_managed_prefix_list_entries,
    get_network_insights_access_scope_analysis_findings,
    get_network_insights_access_scope_content,
    get_password_data,
    get_reserved_instances_exchange_quote,
    get_route_server_associations,
    get_route_server_propagations,
    get_route_server_routing_database,
    get_security_groups_for_vpc,
    get_serial_console_access_status,
    get_snapshot_block_public_access_state,
    get_spot_placement_scores,
    get_subnet_cidr_reservations,
    get_transit_gateway_attachment_propagations,
    get_transit_gateway_multicast_domain_associations,
    get_transit_gateway_policy_table_associations,
    get_transit_gateway_policy_table_entries,
    get_transit_gateway_prefix_list_references,
    get_transit_gateway_route_table_associations,
    get_transit_gateway_route_table_propagations,
    get_verified_access_endpoint_policy,
    get_verified_access_endpoint_targets,
    get_verified_access_group_policy,
    get_vpn_connection_device_sample_configuration,
    get_vpn_connection_device_types,
    get_vpn_tunnel_replacement_status,
    import_client_vpn_client_certificate_revocation_list,
    import_image,
    import_instance,
    import_key_pair,
    import_snapshot,
    import_volume,
    list_images_in_recycle_bin,
    list_snapshots_in_recycle_bin,
    lock_snapshot,
    modify_address_attribute,
    modify_availability_zone_group,
    modify_capacity_reservation,
    modify_capacity_reservation_fleet,
    modify_client_vpn_endpoint,
    modify_default_credit_specification,
    modify_ebs_default_kms_key_id,
    modify_fleet,
    modify_fpga_image_attribute,
    modify_hosts,
    modify_id_format,
    modify_identity_id_format,
    modify_image_attribute,
    modify_instance_attribute,
    modify_instance_capacity_reservation_attributes,
    modify_instance_connect_endpoint,
    modify_instance_cpu_options,
    modify_instance_credit_specification,
    modify_instance_event_start_time,
    modify_instance_event_window,
    modify_instance_maintenance_options,
    modify_instance_metadata_defaults,
    modify_instance_metadata_options,
    modify_instance_network_performance_options,
    modify_instance_placement,
    modify_ipam,
    modify_ipam_pool,
    modify_ipam_prefix_list_resolver,
    modify_ipam_prefix_list_resolver_target,
    modify_ipam_resource_cidr,
    modify_ipam_resource_discovery,
    modify_ipam_scope,
    modify_launch_template,
    modify_local_gateway_route,
    modify_managed_prefix_list,
    modify_network_interface_attribute,
    modify_private_dns_name_options,
    modify_public_ip_dns_name_options,
    modify_reserved_instances,
    modify_route_server,
    modify_security_group_rules,
    modify_snapshot_attribute,
    modify_snapshot_tier,
    modify_spot_fleet_request,
    modify_subnet_attribute,
    modify_traffic_mirror_filter_network_services,
    modify_traffic_mirror_filter_rule,
    modify_traffic_mirror_session,
    modify_transit_gateway,
    modify_transit_gateway_prefix_list_reference,
    modify_transit_gateway_vpc_attachment,
    modify_verified_access_endpoint,
    modify_verified_access_endpoint_policy,
    modify_verified_access_group,
    modify_verified_access_group_policy,
    modify_verified_access_instance,
    modify_verified_access_instance_logging_configuration,
    modify_verified_access_trust_provider,
    modify_volume,
    modify_volume_attribute,
    modify_vpc_attribute,
    modify_vpc_block_public_access_exclusion,
    modify_vpc_block_public_access_options,
    modify_vpc_endpoint,
    modify_vpc_endpoint_connection_notification,
    modify_vpc_endpoint_service_configuration,
    modify_vpc_endpoint_service_payer_responsibility,
    modify_vpc_endpoint_service_permissions,
    modify_vpc_peering_connection_options,
    modify_vpc_tenancy,
    modify_vpn_connection,
    modify_vpn_connection_options,
    modify_vpn_tunnel_certificate,
    modify_vpn_tunnel_options,
    monitor_instances,
    move_address_to_vpc,
    move_byoip_cidr_to_ipam,
    move_capacity_reservation_instances,
    provision_byoip_cidr,
    provision_ipam_byoasn,
    provision_ipam_pool_cidr,
    provision_public_ipv4_pool_cidr,
    purchase_capacity_block,
    purchase_capacity_block_extension,
    purchase_host_reservation,
    purchase_reserved_instances_offering,
    purchase_scheduled_instances,
    register_image,
    register_instance_event_notification_attributes,
    register_transit_gateway_multicast_group_members,
    register_transit_gateway_multicast_group_sources,
    reject_capacity_reservation_billing_ownership,
    reject_transit_gateway_multicast_domain_associations,
    reject_transit_gateway_peering_attachment,
    reject_transit_gateway_vpc_attachment,
    reject_vpc_endpoint_connections,
    reject_vpc_peering_connection,
    release_address,
    release_hosts,
    release_ipam_pool_allocation,
    replace_iam_instance_profile_association,
    replace_image_criteria_in_allowed_images_settings,
    replace_network_acl_association,
    replace_network_acl_entry,
    replace_route,
    replace_route_table_association,
    replace_transit_gateway_route,
    replace_vpn_tunnel,
    report_instance_status,
    request_spot_fleet,
    request_spot_instances,
    reset_address_attribute,
    reset_ebs_default_kms_key_id,
    reset_fpga_image_attribute,
    reset_image_attribute,
    reset_instance_attribute,
    reset_network_interface_attribute,
    reset_snapshot_attribute,
    restore_address_to_classic,
    restore_image_from_recycle_bin,
    restore_managed_prefix_list_version,
    restore_snapshot_from_recycle_bin,
    restore_snapshot_tier,
    revoke_client_vpn_ingress,
    revoke_security_group_egress,
    revoke_security_group_ingress,
    run_instances,
    run_scheduled_instances,
    search_local_gateway_routes,
    search_transit_gateway_multicast_groups,
    search_transit_gateway_routes,
    send_diagnostic_interrupt,
    start_declarative_policies_report,
    start_network_insights_access_scope_analysis,
    start_network_insights_analysis,
    start_vpc_endpoint_service_private_dns_verification,
    terminate_client_vpn_connections,
    unassign_ipv6_addresses,
    unassign_private_ip_addresses,
    unassign_private_nat_gateway_address,
    unlock_snapshot,
    unmonitor_instances,
    update_capacity_manager_organizations_access,
    update_security_group_rule_descriptions_egress,
    update_security_group_rule_descriptions_ingress,
    withdraw_byoip_cidr,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _instance_dict(
    instance_id: str = "i-12345",
    state: str = "running",
    instance_type: str = "t3.micro",
) -> dict:
    return {
        "InstanceId": instance_id,
        "InstanceType": instance_type,
        "State": {"Name": state},
        "PublicIpAddress": "1.2.3.4",
        "PrivateIpAddress": "10.0.0.1",
        "PublicDnsName": "ec2.example.com",
        "ImageId": "ami-abc123",
        "Tags": [{"Key": "Name", "Value": "test"}],
    }


# ---------------------------------------------------------------------------
# describe_instances
# ---------------------------------------------------------------------------


async def test_describe_instances_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [
            {"Instances": [_instance_dict()]}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_instances()
    assert len(result) == 1
    assert result[0].instance_id == "i-12345"
    assert result[0].state == "running"


async def test_describe_instances_with_ids_and_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [{"Instances": [_instance_dict()]}],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_instances(
        instance_ids=["i-12345"],
        filters=[{"Name": "instance-state-name", "Values": ["running"]}],
        region_name="us-east-1",
    )
    assert len(result) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["InstanceIds"] == ["i-12345"]
    assert "Filters" in call_kwargs


async def test_describe_instances_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Reservations": [{"Instances": [_instance_dict("i-1")]}],
            "NextToken": "tok1",
        },
        {
            "Reservations": [{"Instances": [_instance_dict("i-2")]}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_instances()
    assert len(result) == 2
    assert result[0].instance_id == "i-1"
    assert result[1].instance_id == "i-2"


async def test_describe_instances_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Reservations": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_instances()
    assert result == []


async def test_describe_instances_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api error")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api error"):
        await describe_instances()


async def test_describe_instances_generic_exception(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("unexpected")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_instances failed"):
        await describe_instances()


# ---------------------------------------------------------------------------
# get_instance
# ---------------------------------------------------------------------------


async def test_get_instance_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [{"Instances": [_instance_dict()]}],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instance("i-12345")
    assert result is not None
    assert result.instance_id == "i-12345"


async def test_get_instance_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Reservations": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instance("i-noexist")
    assert result is None


# ---------------------------------------------------------------------------
# start_instances
# ---------------------------------------------------------------------------


async def test_start_instances_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    await start_instances(["i-123"])
    mock_client.call.assert_awaited_once_with(
        "StartInstances", InstanceIds=["i-123"]
    )


async def test_start_instances_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="denied"):
        await start_instances(["i-123"])


async def test_start_instances_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to start instances"):
        await start_instances(["i-123"])


# ---------------------------------------------------------------------------
# stop_instances
# ---------------------------------------------------------------------------


async def test_stop_instances_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    await stop_instances(["i-123"], force=True)
    mock_client.call.assert_awaited_once_with(
        "StopInstances", InstanceIds=["i-123"], Force=True
    )


async def test_stop_instances_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("oops")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="oops"):
        await stop_instances(["i-123"])


async def test_stop_instances_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("wrong")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to stop instances"):
        await stop_instances(["i-123"])


# ---------------------------------------------------------------------------
# reboot_instances
# ---------------------------------------------------------------------------


async def test_reboot_instances_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    await reboot_instances(["i-123"])
    mock_client.call.assert_awaited_once()


async def test_reboot_instances_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("no")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="no"):
        await reboot_instances(["i-123"])


async def test_reboot_instances_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("disk")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to reboot"):
        await reboot_instances(["i-123"])


# ---------------------------------------------------------------------------
# terminate_instances
# ---------------------------------------------------------------------------


async def test_terminate_instances_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    await terminate_instances(["i-123"])
    mock_client.call.assert_awaited_once()


async def test_terminate_instances_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("nope")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="nope"):
        await terminate_instances(["i-123"])


async def test_terminate_instances_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = IOError("io")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to terminate"):
        await terminate_instances(["i-123"])


# ---------------------------------------------------------------------------
# create_image
# ---------------------------------------------------------------------------


async def test_create_image_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"ImageId": "ami-new123"}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await create_image("i-123", "my-image", description="desc")
    assert result == "ami-new123"


async def test_create_image_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_image("i-123", "img")


async def test_create_image_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("val")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="Failed to create image"):
        await create_image("i-123", "img")


# ---------------------------------------------------------------------------
# describe_images
# ---------------------------------------------------------------------------


async def test_describe_images_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Images": [
            {
                "ImageId": "ami-1",
                "Name": "test-ami",
                "State": "available",
                "CreationDate": "2024-01-01",
                "Description": "A test AMI",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_images(
        image_ids=["ami-1"],
        owners=["self"],
        filters=[{"Name": "state", "Values": ["available"]}],
    )
    assert len(result) == 1
    assert result[0].image_id == "ami-1"
    assert result[0].description == "A test AMI"


async def test_describe_images_no_params(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Images": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_images()
    assert result == []


async def test_describe_images_empty_description(monkeypatch):
    """Description of '' should become None."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Images": [
            {
                "ImageId": "ami-2",
                "Name": "n",
                "State": "available",
                "Description": "",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_images()
    assert result[0].description is None


async def test_describe_images_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_images()


async def test_describe_images_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("type")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_images failed"):
        await describe_images()


# ---------------------------------------------------------------------------
# describe_security_groups
# ---------------------------------------------------------------------------


async def test_describe_security_groups_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-1",
                "GroupName": "default",
                "Description": "Default SG",
                "VpcId": "vpc-123",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_security_groups(
        group_ids=["sg-1"],
        filters=[{"Name": "group-name", "Values": ["default"]}],
    )
    assert len(result) == 1
    assert result[0].group_id == "sg-1"
    assert result[0].vpc_id == "vpc-123"


async def test_describe_security_groups_no_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-2",
                "GroupName": "no-vpc",
                "Description": "No VPC",
                "VpcId": "",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await describe_security_groups()
    assert result[0].vpc_id is None


async def test_describe_security_groups_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="denied"):
        await describe_security_groups()


async def test_describe_security_groups_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_security_groups failed"):
        await describe_security_groups()


# ---------------------------------------------------------------------------
# wait_for_instance_state
# ---------------------------------------------------------------------------


async def test_wait_for_instance_state_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [
            {"Instances": [_instance_dict(state="running")]}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_instance_state("i-12345", "running")
    assert result.state == "running"


async def test_wait_for_instance_state_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Reservations": [
                {"Instances": [_instance_dict(state="pending")]}
            ],
        },
        {
            "Reservations": [
                {"Instances": [_instance_dict(state="running")]}
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ec2.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_instance_state(
            "i-12345", "running", timeout=300, poll_interval=0.01
        )
    assert result.state == "running"


async def test_wait_for_instance_state_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Reservations": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_instance_state("i-gone", "running")


async def test_wait_for_instance_state_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [
            {"Instances": [_instance_dict(state="pending")]}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ec2.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(TimeoutError, match="did not reach state"):
            await wait_for_instance_state(
                "i-12345", "running", timeout=0.0, poll_interval=0.001
            )


# ---------------------------------------------------------------------------
# get_instances_by_tag
# ---------------------------------------------------------------------------


async def test_get_instances_by_tag(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Reservations": [
            {"Instances": [_instance_dict()]}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instances_by_tag("env", "prod")
    assert len(result) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Filters"] == [
        {"Name": "tag:env", "Values": ["prod"]}
    ]


async def test_get_instances_by_tag_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Reservations": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instances_by_tag(
        "Name", "test", region_name="us-west-2"
    )
    assert result == []


# ---------------------------------------------------------------------------
# get_latest_ami
# ---------------------------------------------------------------------------


async def test_get_latest_ami_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Images": [
            {
                "ImageId": "ami-old",
                "Name": "app-v1",
                "State": "available",
                "CreationDate": "2023-01-01",
            },
            {
                "ImageId": "ami-new",
                "Name": "app-v2",
                "State": "available",
                "CreationDate": "2024-01-01",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_ami("app-*")
    assert result is not None
    assert result.image_id == "ami-new"


async def test_get_latest_ami_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Images": []}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_ami("no-match-*")
    assert result is None


async def test_get_latest_ami_custom_owners(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Images": [
            {
                "ImageId": "ami-1",
                "Name": "test",
                "State": "available",
                "CreationDate": "2024-06-01",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_ami(
        "test*", owners=["amazon"], region_name="eu-west-1"
    )
    assert result is not None


async def test_get_latest_ami_none_creation_date(monkeypatch):
    """AMIs without creation_date should sort by empty string."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Images": [
            {
                "ImageId": "ami-no-date",
                "Name": "nd",
                "State": "available",
            },
            {
                "ImageId": "ami-with-date",
                "Name": "wd",
                "State": "available",
                "CreationDate": "2024-01-01",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_latest_ami("*")
    assert result is not None
    assert result.image_id == "ami-with-date"


# ---------------------------------------------------------------------------
# get_instance_console_output
# ---------------------------------------------------------------------------


async def test_get_instance_console_output_success(monkeypatch):
    encoded = base64.b64encode(b"boot log output").decode()
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Output": encoded}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instance_console_output("i-123")
    assert result == "boot log output"


async def test_get_instance_console_output_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Output": ""}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instance_console_output("i-123")
    assert result == ""


async def test_get_instance_console_output_missing_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    result = await get_instance_console_output("i-123")
    assert result == ""


async def test_get_instance_console_output_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_instance_console_output("i-123")


async def test_get_instance_console_output_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="get_console_output failed"):
        await get_instance_console_output("i-123")


async def test_accept_address_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_address_transfer("test-address", )
    mock_client.call.assert_called_once()


async def test_accept_address_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_address_transfer("test-address", )


async def test_accept_capacity_reservation_billing_ownership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_capacity_reservation_billing_ownership("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_accept_capacity_reservation_billing_ownership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_capacity_reservation_billing_ownership("test-capacity_reservation_id", )


async def test_accept_reserved_instances_exchange_quote(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_reserved_instances_exchange_quote([], )
    mock_client.call.assert_called_once()


async def test_accept_reserved_instances_exchange_quote_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_reserved_instances_exchange_quote([], )


async def test_accept_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_transit_gateway_multicast_domain_associations()
    mock_client.call.assert_called_once()


async def test_accept_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_transit_gateway_multicast_domain_associations()


async def test_accept_transit_gateway_peering_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_accept_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )


async def test_accept_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_accept_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )


async def test_accept_vpc_endpoint_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_vpc_endpoint_connections("test-service_id", [], )
    mock_client.call.assert_called_once()


async def test_accept_vpc_endpoint_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_vpc_endpoint_connections("test-service_id", [], )


async def test_accept_vpc_peering_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_vpc_peering_connection("test-vpc_peering_connection_id", )
    mock_client.call.assert_called_once()


async def test_accept_vpc_peering_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_vpc_peering_connection("test-vpc_peering_connection_id", )


async def test_advertise_byoip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await advertise_byoip_cidr("test-cidr", )
    mock_client.call.assert_called_once()


async def test_advertise_byoip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await advertise_byoip_cidr("test-cidr", )


async def test_allocate_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await allocate_address()
    mock_client.call.assert_called_once()


async def test_allocate_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await allocate_address()


async def test_allocate_hosts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await allocate_hosts()
    mock_client.call.assert_called_once()


async def test_allocate_hosts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await allocate_hosts()


async def test_allocate_ipam_pool_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await allocate_ipam_pool_cidr("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_allocate_ipam_pool_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await allocate_ipam_pool_cidr("test-ipam_pool_id", )


async def test_apply_security_groups_to_client_vpn_target_network(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_security_groups_to_client_vpn_target_network("test-client_vpn_endpoint_id", "test-vpc_id", [], )
    mock_client.call.assert_called_once()


async def test_apply_security_groups_to_client_vpn_target_network_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_security_groups_to_client_vpn_target_network("test-client_vpn_endpoint_id", "test-vpc_id", [], )


async def test_assign_ipv6_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await assign_ipv6_addresses("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_assign_ipv6_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await assign_ipv6_addresses("test-network_interface_id", )


async def test_assign_private_ip_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await assign_private_ip_addresses("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_assign_private_ip_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await assign_private_ip_addresses("test-network_interface_id", )


async def test_assign_private_nat_gateway_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await assign_private_nat_gateway_address("test-nat_gateway_id", )
    mock_client.call.assert_called_once()


async def test_assign_private_nat_gateway_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await assign_private_nat_gateway_address("test-nat_gateway_id", )


async def test_associate_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_address()
    mock_client.call.assert_called_once()


async def test_associate_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_address()


async def test_associate_capacity_reservation_billing_owner(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", )
    mock_client.call.assert_called_once()


async def test_associate_capacity_reservation_billing_owner_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", )


async def test_associate_client_vpn_target_network(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_associate_client_vpn_target_network_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", )


async def test_associate_dhcp_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_dhcp_options("test-dhcp_options_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_associate_dhcp_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_dhcp_options("test-dhcp_options_id", "test-vpc_id", )


async def test_associate_enclave_certificate_iam_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_associate_enclave_certificate_iam_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", )


async def test_associate_iam_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_iam_instance_profile({}, "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_associate_iam_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_iam_instance_profile({}, "test-instance_id", )


async def test_associate_instance_event_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_instance_event_window("test-instance_event_window_id", {}, )
    mock_client.call.assert_called_once()


async def test_associate_instance_event_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_instance_event_window("test-instance_event_window_id", {}, )


async def test_associate_ipam_byoasn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_ipam_byoasn("test-asn", "test-cidr", )
    mock_client.call.assert_called_once()


async def test_associate_ipam_byoasn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_ipam_byoasn("test-asn", "test-cidr", )


async def test_associate_ipam_resource_discovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", )
    mock_client.call.assert_called_once()


async def test_associate_ipam_resource_discovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", )


async def test_associate_nat_gateway_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_nat_gateway_address("test-nat_gateway_id", [], )
    mock_client.call.assert_called_once()


async def test_associate_nat_gateway_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_nat_gateway_address("test-nat_gateway_id", [], )


async def test_associate_route_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_route_server("test-route_server_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_associate_route_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_route_server("test-route_server_id", "test-vpc_id", )


async def test_associate_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_route_table("test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_associate_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_route_table("test-route_table_id", )


async def test_associate_security_group_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_security_group_vpc("test-group_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_associate_security_group_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_security_group_vpc("test-group_id", "test-vpc_id", )


async def test_associate_subnet_cidr_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_subnet_cidr_block("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_associate_subnet_cidr_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_subnet_cidr_block("test-subnet_id", )


async def test_associate_transit_gateway_multicast_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], )
    mock_client.call.assert_called_once()


async def test_associate_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], )


async def test_associate_transit_gateway_policy_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_associate_transit_gateway_policy_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", )


async def test_associate_transit_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_associate_transit_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", )


async def test_associate_trunk_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", )
    mock_client.call.assert_called_once()


async def test_associate_trunk_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", )


async def test_associate_vpc_cidr_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_vpc_cidr_block("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_associate_vpc_cidr_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_vpc_cidr_block("test-vpc_id", )


async def test_attach_classic_link_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_classic_link_vpc("test-instance_id", "test-vpc_id", [], )
    mock_client.call.assert_called_once()


async def test_attach_classic_link_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_classic_link_vpc("test-instance_id", "test-vpc_id", [], )


async def test_attach_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_internet_gateway("test-internet_gateway_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_attach_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_internet_gateway("test-internet_gateway_id", "test-vpc_id", )


async def test_attach_network_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_network_interface("test-network_interface_id", "test-instance_id", 1, )
    mock_client.call.assert_called_once()


async def test_attach_network_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_network_interface("test-network_interface_id", "test-instance_id", 1, )


async def test_attach_verified_access_trust_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", )
    mock_client.call.assert_called_once()


async def test_attach_verified_access_trust_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", )


async def test_attach_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_volume("test-device", "test-instance_id", "test-volume_id", )
    mock_client.call.assert_called_once()


async def test_attach_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_volume("test-device", "test-instance_id", "test-volume_id", )


async def test_attach_vpn_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", )
    mock_client.call.assert_called_once()


async def test_attach_vpn_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", )


async def test_authorize_client_vpn_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", )
    mock_client.call.assert_called_once()


async def test_authorize_client_vpn_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", )


async def test_authorize_security_group_egress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_security_group_egress("test-group_id", )
    mock_client.call.assert_called_once()


async def test_authorize_security_group_egress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_security_group_egress("test-group_id", )


async def test_authorize_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_security_group_ingress()
    mock_client.call.assert_called_once()


async def test_authorize_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_security_group_ingress()


async def test_bundle_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await bundle_instance("test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_bundle_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await bundle_instance("test-instance_id", {}, )


async def test_cancel_bundle_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_bundle_task("test-bundle_id", )
    mock_client.call.assert_called_once()


async def test_cancel_bundle_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_bundle_task("test-bundle_id", )


async def test_cancel_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_capacity_reservation("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_cancel_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_capacity_reservation("test-capacity_reservation_id", )


async def test_cancel_capacity_reservation_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_capacity_reservation_fleets([], )
    mock_client.call.assert_called_once()


async def test_cancel_capacity_reservation_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_capacity_reservation_fleets([], )


async def test_cancel_conversion_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_conversion_task("test-conversion_task_id", )
    mock_client.call.assert_called_once()


async def test_cancel_conversion_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_conversion_task("test-conversion_task_id", )


async def test_cancel_declarative_policies_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_declarative_policies_report("test-report_id", )
    mock_client.call.assert_called_once()


async def test_cancel_declarative_policies_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_declarative_policies_report("test-report_id", )


async def test_cancel_export_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_export_task("test-export_task_id", )
    mock_client.call.assert_called_once()


async def test_cancel_export_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_export_task("test-export_task_id", )


async def test_cancel_image_launch_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_image_launch_permission("test-image_id", )
    mock_client.call.assert_called_once()


async def test_cancel_image_launch_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_image_launch_permission("test-image_id", )


async def test_cancel_import_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_import_task()
    mock_client.call.assert_called_once()


async def test_cancel_import_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_import_task()


async def test_cancel_reserved_instances_listing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_reserved_instances_listing("test-reserved_instances_listing_id", )
    mock_client.call.assert_called_once()


async def test_cancel_reserved_instances_listing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_reserved_instances_listing("test-reserved_instances_listing_id", )


async def test_cancel_spot_fleet_requests(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_spot_fleet_requests([], True, )
    mock_client.call.assert_called_once()


async def test_cancel_spot_fleet_requests_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_spot_fleet_requests([], True, )


async def test_cancel_spot_instance_requests(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_spot_instance_requests([], )
    mock_client.call.assert_called_once()


async def test_cancel_spot_instance_requests_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_spot_instance_requests([], )


async def test_confirm_product_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await confirm_product_instance("test-instance_id", "test-product_code", )
    mock_client.call.assert_called_once()


async def test_confirm_product_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_product_instance("test-instance_id", "test-product_code", )


async def test_copy_fpga_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_fpga_image("test-source_fpga_image_id", "test-source_region", )
    mock_client.call.assert_called_once()


async def test_copy_fpga_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_fpga_image("test-source_fpga_image_id", "test-source_region", )


async def test_copy_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_image("test-name", "test-source_image_id", "test-source_region", )
    mock_client.call.assert_called_once()


async def test_copy_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_image("test-name", "test-source_image_id", "test-source_region", )


async def test_copy_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_snapshot("test-source_region", "test-source_snapshot_id", )
    mock_client.call.assert_called_once()


async def test_copy_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_snapshot("test-source_region", "test-source_snapshot_id", )


async def test_copy_volumes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_volumes("test-source_volume_id", )
    mock_client.call.assert_called_once()


async def test_copy_volumes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_volumes("test-source_volume_id", )


async def test_create_capacity_manager_data_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", )
    mock_client.call.assert_called_once()


async def test_create_capacity_manager_data_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", )


async def test_create_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_capacity_reservation("test-instance_type", "test-instance_platform", 1, )
    mock_client.call.assert_called_once()


async def test_create_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_reservation("test-instance_type", "test-instance_platform", 1, )


async def test_create_capacity_reservation_by_splitting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, )
    mock_client.call.assert_called_once()


async def test_create_capacity_reservation_by_splitting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, )


async def test_create_capacity_reservation_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_capacity_reservation_fleet([], 1, )
    mock_client.call.assert_called_once()


async def test_create_capacity_reservation_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_reservation_fleet([], 1, )


async def test_create_carrier_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_carrier_gateway("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_carrier_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_carrier_gateway("test-vpc_id", )


async def test_create_client_vpn_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_client_vpn_endpoint("test-server_certificate_arn", [], {}, )
    mock_client.call.assert_called_once()


async def test_create_client_vpn_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_client_vpn_endpoint("test-server_certificate_arn", [], {}, )


async def test_create_client_vpn_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", )
    mock_client.call.assert_called_once()


async def test_create_client_vpn_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", )


async def test_create_coip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_coip_cidr("test-cidr", "test-coip_pool_id", )
    mock_client.call.assert_called_once()


async def test_create_coip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_coip_cidr("test-cidr", "test-coip_pool_id", )


async def test_create_coip_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_coip_pool("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_create_coip_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_coip_pool("test-local_gateway_route_table_id", )


async def test_create_customer_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_customer_gateway("test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_customer_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_customer_gateway("test-type_value", )


async def test_create_default_subnet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_default_subnet()
    mock_client.call.assert_called_once()


async def test_create_default_subnet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_default_subnet()


async def test_create_default_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_default_vpc()
    mock_client.call.assert_called_once()


async def test_create_default_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_default_vpc()


async def test_create_delegate_mac_volume_ownership_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", )
    mock_client.call.assert_called_once()


async def test_create_delegate_mac_volume_ownership_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", )


async def test_create_dhcp_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dhcp_options([], )
    mock_client.call.assert_called_once()


async def test_create_dhcp_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dhcp_options([], )


async def test_create_egress_only_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_egress_only_internet_gateway("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_egress_only_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_egress_only_internet_gateway("test-vpc_id", )


async def test_create_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_fleet([], {}, )
    mock_client.call.assert_called_once()


async def test_create_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_fleet([], {}, )


async def test_create_flow_logs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_flow_logs([], "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_create_flow_logs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_flow_logs([], "test-resource_type", )


async def test_create_fpga_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_fpga_image({}, )
    mock_client.call.assert_called_once()


async def test_create_fpga_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_fpga_image({}, )


async def test_create_image_usage_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_image_usage_report("test-image_id", [], )
    mock_client.call.assert_called_once()


async def test_create_image_usage_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_image_usage_report("test-image_id", [], )


async def test_create_instance_connect_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_connect_endpoint("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_create_instance_connect_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_connect_endpoint("test-subnet_id", )


async def test_create_instance_event_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_event_window()
    mock_client.call.assert_called_once()


async def test_create_instance_event_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_event_window()


async def test_create_instance_export_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_export_task("test-instance_id", "test-target_environment", {}, )
    mock_client.call.assert_called_once()


async def test_create_instance_export_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_export_task("test-instance_id", "test-target_environment", {}, )


async def test_create_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_internet_gateway()
    mock_client.call.assert_called_once()


async def test_create_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_internet_gateway()


async def test_create_ipam(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam()
    mock_client.call.assert_called_once()


async def test_create_ipam_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam()


async def test_create_ipam_external_resource_verification_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_external_resource_verification_token("test-ipam_id", )
    mock_client.call.assert_called_once()


async def test_create_ipam_external_resource_verification_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_external_resource_verification_token("test-ipam_id", )


async def test_create_ipam_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_pool("test-ipam_scope_id", "test-address_family", )
    mock_client.call.assert_called_once()


async def test_create_ipam_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_pool("test-ipam_scope_id", "test-address_family", )


async def test_create_ipam_prefix_list_resolver(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", )
    mock_client.call.assert_called_once()


async def test_create_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", )


async def test_create_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", True, )
    mock_client.call.assert_called_once()


async def test_create_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", True, )


async def test_create_ipam_resource_discovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_resource_discovery()
    mock_client.call.assert_called_once()


async def test_create_ipam_resource_discovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_resource_discovery()


async def test_create_ipam_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ipam_scope("test-ipam_id", )
    mock_client.call.assert_called_once()


async def test_create_ipam_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ipam_scope("test-ipam_id", )


async def test_create_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_key_pair("test-key_name", )
    mock_client.call.assert_called_once()


async def test_create_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_key_pair("test-key_name", )


async def test_create_launch_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_launch_template("test-launch_template_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_launch_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_launch_template("test-launch_template_name", {}, )


async def test_create_launch_template_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_launch_template_version({}, )
    mock_client.call.assert_called_once()


async def test_create_launch_template_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_launch_template_version({}, )


async def test_create_local_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_route("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_route("test-local_gateway_route_table_id", )


async def test_create_local_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_route_table("test-local_gateway_id", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_route_table("test-local_gateway_id", )


async def test_create_local_gateway_route_table_virtual_interface_group_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_route_table_virtual_interface_group_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", )


async def test_create_local_gateway_route_table_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_route_table_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", )


async def test_create_local_gateway_virtual_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", 1, "test-local_address", "test-peer_address", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_virtual_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", 1, "test-local_address", "test-peer_address", )


async def test_create_local_gateway_virtual_interface_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_local_gateway_virtual_interface_group("test-local_gateway_id", )
    mock_client.call.assert_called_once()


async def test_create_local_gateway_virtual_interface_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_local_gateway_virtual_interface_group("test-local_gateway_id", )


async def test_create_mac_system_integrity_protection_modification_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", )
    mock_client.call.assert_called_once()


async def test_create_mac_system_integrity_protection_modification_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", )


async def test_create_managed_prefix_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", )
    mock_client.call.assert_called_once()


async def test_create_managed_prefix_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", )


async def test_create_nat_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_nat_gateway("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_create_nat_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_nat_gateway("test-subnet_id", )


async def test_create_network_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_acl("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_network_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_acl("test-vpc_id", )


async def test_create_network_acl_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, )
    mock_client.call.assert_called_once()


async def test_create_network_acl_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, )


async def test_create_network_insights_access_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_insights_access_scope("test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_network_insights_access_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_insights_access_scope("test-client_token", )


async def test_create_network_insights_path(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_insights_path("test-source", "test-protocol", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_network_insights_path_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_insights_path("test-source", "test-protocol", "test-client_token", )


async def test_create_network_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_interface("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_create_network_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_interface("test-subnet_id", )


async def test_create_network_interface_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_network_interface_permission("test-network_interface_id", "test-permission", )
    mock_client.call.assert_called_once()


async def test_create_network_interface_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_network_interface_permission("test-network_interface_id", "test-permission", )


async def test_create_placement_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_placement_group()
    mock_client.call.assert_called_once()


async def test_create_placement_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_placement_group()


async def test_create_public_ipv4_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_public_ipv4_pool()
    mock_client.call.assert_called_once()


async def test_create_public_ipv4_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_public_ipv4_pool()


async def test_create_replace_root_volume_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_replace_root_volume_task("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_create_replace_root_volume_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_replace_root_volume_task("test-instance_id", )


async def test_create_reserved_instances_listing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_reserved_instances_listing("test-reserved_instances_id", 1, [], "test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_reserved_instances_listing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_reserved_instances_listing("test-reserved_instances_id", 1, [], "test-client_token", )


async def test_create_restore_image_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_restore_image_task("test-bucket", "test-object_key", )
    mock_client.call.assert_called_once()


async def test_create_restore_image_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_restore_image_task("test-bucket", "test-object_key", )


async def test_create_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_route("test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_create_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_route("test-route_table_id", )


async def test_create_route_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_route_server(1, )
    mock_client.call.assert_called_once()


async def test_create_route_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_route_server(1, )


async def test_create_route_server_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_route_server_endpoint("test-route_server_id", "test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_create_route_server_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_route_server_endpoint("test-route_server_id", "test-subnet_id", )


async def test_create_route_server_peer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, )
    mock_client.call.assert_called_once()


async def test_create_route_server_peer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, )


async def test_create_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_route_table("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_route_table("test-vpc_id", )


async def test_create_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_security_group("test-description", "test-group_name", )
    mock_client.call.assert_called_once()


async def test_create_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_security_group("test-description", "test-group_name", )


async def test_create_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot("test-volume_id", )


async def test_create_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshots({}, )
    mock_client.call.assert_called_once()


async def test_create_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshots({}, )


async def test_create_spot_datafeed_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_spot_datafeed_subscription("test-bucket", )
    mock_client.call.assert_called_once()


async def test_create_spot_datafeed_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_spot_datafeed_subscription("test-bucket", )


async def test_create_store_image_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_store_image_task("test-image_id", "test-bucket", )
    mock_client.call.assert_called_once()


async def test_create_store_image_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_store_image_task("test-image_id", "test-bucket", )


async def test_create_subnet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_subnet("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_subnet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_subnet("test-vpc_id", )


async def test_create_subnet_cidr_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", )
    mock_client.call.assert_called_once()


async def test_create_subnet_cidr_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", )


async def test_create_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tags([], [], )
    mock_client.call.assert_called_once()


async def test_create_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tags([], [], )


async def test_create_traffic_mirror_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_mirror_filter()
    mock_client.call.assert_called_once()


async def test_create_traffic_mirror_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_mirror_filter()


async def test_create_traffic_mirror_filter_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", 1, "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", )
    mock_client.call.assert_called_once()


async def test_create_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", 1, "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", )


async def test_create_traffic_mirror_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", 1, )
    mock_client.call.assert_called_once()


async def test_create_traffic_mirror_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", 1, )


async def test_create_traffic_mirror_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_mirror_target()
    mock_client.call.assert_called_once()


async def test_create_traffic_mirror_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_mirror_target()


async def test_create_transit_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway()
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway()


async def test_create_transit_gateway_connect(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_connect("test-transport_transit_gateway_attachment_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_connect_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_connect("test-transport_transit_gateway_attachment_id", {}, )


async def test_create_transit_gateway_connect_peer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", [], )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_connect_peer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", [], )


async def test_create_transit_gateway_multicast_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_multicast_domain("test-transit_gateway_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_multicast_domain("test-transit_gateway_id", )


async def test_create_transit_gateway_peering_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", "test-peer_account_id", "test-peer_region", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", "test-peer_account_id", "test-peer_region", )


async def test_create_transit_gateway_policy_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_policy_table("test-transit_gateway_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_policy_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_policy_table("test-transit_gateway_id", )


async def test_create_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )


async def test_create_transit_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", )


async def test_create_transit_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_route_table("test-transit_gateway_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_route_table("test-transit_gateway_id", )


async def test_create_transit_gateway_route_table_announcement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_route_table_announcement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", )


async def test_create_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", [], )
    mock_client.call.assert_called_once()


async def test_create_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", [], )


async def test_create_verified_access_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", )
    mock_client.call.assert_called_once()


async def test_create_verified_access_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", )


async def test_create_verified_access_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_verified_access_group("test-verified_access_instance_id", )
    mock_client.call.assert_called_once()


async def test_create_verified_access_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_verified_access_group("test-verified_access_instance_id", )


async def test_create_verified_access_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_verified_access_instance()
    mock_client.call.assert_called_once()


async def test_create_verified_access_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_verified_access_instance()


async def test_create_verified_access_trust_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", )
    mock_client.call.assert_called_once()


async def test_create_verified_access_trust_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", )


async def test_create_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_volume()
    mock_client.call.assert_called_once()


async def test_create_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_volume()


async def test_create_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc()
    mock_client.call.assert_called_once()


async def test_create_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc()


async def test_create_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", )
    mock_client.call.assert_called_once()


async def test_create_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", )


async def test_create_vpc_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_endpoint("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_vpc_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_endpoint("test-vpc_id", )


async def test_create_vpc_endpoint_connection_notification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_endpoint_connection_notification("test-connection_notification_arn", [], )
    mock_client.call.assert_called_once()


async def test_create_vpc_endpoint_connection_notification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_endpoint_connection_notification("test-connection_notification_arn", [], )


async def test_create_vpc_endpoint_service_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_endpoint_service_configuration()
    mock_client.call.assert_called_once()


async def test_create_vpc_endpoint_service_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_endpoint_service_configuration()


async def test_create_vpc_peering_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_peering_connection("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_create_vpc_peering_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_peering_connection("test-vpc_id", )


async def test_create_vpn_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpn_connection("test-customer_gateway_id", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_vpn_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpn_connection("test-customer_gateway_id", "test-type_value", )


async def test_create_vpn_connection_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", )
    mock_client.call.assert_called_once()


async def test_create_vpn_connection_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", )


async def test_create_vpn_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpn_gateway("test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_vpn_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpn_gateway("test-type_value", )


async def test_delete_capacity_manager_data_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_capacity_manager_data_export("test-capacity_manager_data_export_id", )
    mock_client.call.assert_called_once()


async def test_delete_capacity_manager_data_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_capacity_manager_data_export("test-capacity_manager_data_export_id", )


async def test_delete_carrier_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_carrier_gateway("test-carrier_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_carrier_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_carrier_gateway("test-carrier_gateway_id", )


async def test_delete_client_vpn_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_client_vpn_endpoint("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_delete_client_vpn_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_client_vpn_endpoint("test-client_vpn_endpoint_id", )


async def test_delete_client_vpn_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", )
    mock_client.call.assert_called_once()


async def test_delete_client_vpn_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", )


async def test_delete_coip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_coip_cidr("test-cidr", "test-coip_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_coip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_coip_cidr("test-cidr", "test-coip_pool_id", )


async def test_delete_coip_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_coip_pool("test-coip_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_coip_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_coip_pool("test-coip_pool_id", )


async def test_delete_customer_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_customer_gateway("test-customer_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_customer_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_customer_gateway("test-customer_gateway_id", )


async def test_delete_dhcp_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dhcp_options("test-dhcp_options_id", )
    mock_client.call.assert_called_once()


async def test_delete_dhcp_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dhcp_options("test-dhcp_options_id", )


async def test_delete_egress_only_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_egress_only_internet_gateway("test-egress_only_internet_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_egress_only_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_egress_only_internet_gateway("test-egress_only_internet_gateway_id", )


async def test_delete_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fleets([], True, )
    mock_client.call.assert_called_once()


async def test_delete_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fleets([], True, )


async def test_delete_flow_logs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_flow_logs([], )
    mock_client.call.assert_called_once()


async def test_delete_flow_logs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_flow_logs([], )


async def test_delete_fpga_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fpga_image("test-fpga_image_id", )
    mock_client.call.assert_called_once()


async def test_delete_fpga_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fpga_image("test-fpga_image_id", )


async def test_delete_image_usage_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_image_usage_report("test-report_id", )
    mock_client.call.assert_called_once()


async def test_delete_image_usage_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_image_usage_report("test-report_id", )


async def test_delete_instance_connect_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_instance_connect_endpoint("test-instance_connect_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_delete_instance_connect_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_instance_connect_endpoint("test-instance_connect_endpoint_id", )


async def test_delete_instance_event_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_instance_event_window("test-instance_event_window_id", )
    mock_client.call.assert_called_once()


async def test_delete_instance_event_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_instance_event_window("test-instance_event_window_id", )


async def test_delete_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_internet_gateway("test-internet_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_internet_gateway("test-internet_gateway_id", )


async def test_delete_ipam(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam("test-ipam_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam("test-ipam_id", )


async def test_delete_ipam_external_resource_verification_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_external_resource_verification_token("test-ipam_external_resource_verification_token_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_external_resource_verification_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_external_resource_verification_token("test-ipam_external_resource_verification_token_id", )


async def test_delete_ipam_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_pool("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_pool("test-ipam_pool_id", )


async def test_delete_ipam_prefix_list_resolver(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", )


async def test_delete_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", )


async def test_delete_ipam_resource_discovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_resource_discovery("test-ipam_resource_discovery_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_resource_discovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_resource_discovery("test-ipam_resource_discovery_id", )


async def test_delete_ipam_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ipam_scope("test-ipam_scope_id", )
    mock_client.call.assert_called_once()


async def test_delete_ipam_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ipam_scope("test-ipam_scope_id", )


async def test_delete_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_key_pair()
    mock_client.call.assert_called_once()


async def test_delete_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_key_pair()


async def test_delete_launch_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_launch_template()
    mock_client.call.assert_called_once()


async def test_delete_launch_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_launch_template()


async def test_delete_launch_template_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_launch_template_versions([], )
    mock_client.call.assert_called_once()


async def test_delete_launch_template_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_launch_template_versions([], )


async def test_delete_local_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_route("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_route("test-local_gateway_route_table_id", )


async def test_delete_local_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_route_table("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_route_table("test-local_gateway_route_table_id", )


async def test_delete_local_gateway_route_table_virtual_interface_group_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_virtual_interface_group_association_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_route_table_virtual_interface_group_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_virtual_interface_group_association_id", )


async def test_delete_local_gateway_route_table_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_route_table_vpc_association("test-local_gateway_route_table_vpc_association_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_route_table_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_route_table_vpc_association("test-local_gateway_route_table_vpc_association_id", )


async def test_delete_local_gateway_virtual_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_virtual_interface("test-local_gateway_virtual_interface_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_virtual_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_virtual_interface("test-local_gateway_virtual_interface_id", )


async def test_delete_local_gateway_virtual_interface_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_local_gateway_virtual_interface_group("test-local_gateway_virtual_interface_group_id", )
    mock_client.call.assert_called_once()


async def test_delete_local_gateway_virtual_interface_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_local_gateway_virtual_interface_group("test-local_gateway_virtual_interface_group_id", )


async def test_delete_managed_prefix_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_managed_prefix_list("test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_delete_managed_prefix_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_managed_prefix_list("test-prefix_list_id", )


async def test_delete_nat_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_nat_gateway("test-nat_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_nat_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_nat_gateway("test-nat_gateway_id", )


async def test_delete_network_acl(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_acl("test-network_acl_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_acl_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_acl("test-network_acl_id", )


async def test_delete_network_acl_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_acl_entry("test-network_acl_id", 1, True, )
    mock_client.call.assert_called_once()


async def test_delete_network_acl_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_acl_entry("test-network_acl_id", 1, True, )


async def test_delete_network_insights_access_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_insights_access_scope("test-network_insights_access_scope_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_insights_access_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_insights_access_scope("test-network_insights_access_scope_id", )


async def test_delete_network_insights_access_scope_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_insights_access_scope_analysis("test-network_insights_access_scope_analysis_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_insights_access_scope_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_insights_access_scope_analysis("test-network_insights_access_scope_analysis_id", )


async def test_delete_network_insights_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_insights_analysis("test-network_insights_analysis_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_insights_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_insights_analysis("test-network_insights_analysis_id", )


async def test_delete_network_insights_path(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_insights_path("test-network_insights_path_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_insights_path_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_insights_path("test-network_insights_path_id", )


async def test_delete_network_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_interface("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_interface("test-network_interface_id", )


async def test_delete_network_interface_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_network_interface_permission("test-network_interface_permission_id", )
    mock_client.call.assert_called_once()


async def test_delete_network_interface_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_network_interface_permission("test-network_interface_permission_id", )


async def test_delete_placement_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_placement_group("test-group_name", )
    mock_client.call.assert_called_once()


async def test_delete_placement_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_placement_group("test-group_name", )


async def test_delete_public_ipv4_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_public_ipv4_pool("test-pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_public_ipv4_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_public_ipv4_pool("test-pool_id", )


async def test_delete_queued_reserved_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_queued_reserved_instances([], )
    mock_client.call.assert_called_once()


async def test_delete_queued_reserved_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_queued_reserved_instances([], )


async def test_delete_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_route("test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_route("test-route_table_id", )


async def test_delete_route_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_route_server("test-route_server_id", )
    mock_client.call.assert_called_once()


async def test_delete_route_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_route_server("test-route_server_id", )


async def test_delete_route_server_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_route_server_endpoint("test-route_server_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_delete_route_server_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_route_server_endpoint("test-route_server_endpoint_id", )


async def test_delete_route_server_peer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_route_server_peer("test-route_server_peer_id", )
    mock_client.call.assert_called_once()


async def test_delete_route_server_peer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_route_server_peer("test-route_server_peer_id", )


async def test_delete_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_route_table("test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_route_table("test-route_table_id", )


async def test_delete_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_security_group()
    mock_client.call.assert_called_once()


async def test_delete_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_security_group()


async def test_delete_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot("test-snapshot_id", )


async def test_delete_spot_datafeed_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_spot_datafeed_subscription()
    mock_client.call.assert_called_once()


async def test_delete_spot_datafeed_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_spot_datafeed_subscription()


async def test_delete_subnet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_subnet("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_delete_subnet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_subnet("test-subnet_id", )


async def test_delete_subnet_cidr_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_subnet_cidr_reservation("test-subnet_cidr_reservation_id", )
    mock_client.call.assert_called_once()


async def test_delete_subnet_cidr_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_subnet_cidr_reservation("test-subnet_cidr_reservation_id", )


async def test_delete_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tags([], )
    mock_client.call.assert_called_once()


async def test_delete_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tags([], )


async def test_delete_traffic_mirror_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_mirror_filter("test-traffic_mirror_filter_id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_mirror_filter_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_mirror_filter("test-traffic_mirror_filter_id", )


async def test_delete_traffic_mirror_filter_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", )


async def test_delete_traffic_mirror_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_mirror_session("test-traffic_mirror_session_id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_mirror_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_mirror_session("test-traffic_mirror_session_id", )


async def test_delete_traffic_mirror_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_mirror_target("test-traffic_mirror_target_id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_mirror_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_mirror_target("test-traffic_mirror_target_id", )


async def test_delete_transit_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway("test-transit_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway("test-transit_gateway_id", )


async def test_delete_transit_gateway_connect(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_connect("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_connect_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_connect("test-transit_gateway_attachment_id", )


async def test_delete_transit_gateway_connect_peer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_connect_peer("test-transit_gateway_connect_peer_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_connect_peer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_connect_peer("test-transit_gateway_connect_peer_id", )


async def test_delete_transit_gateway_multicast_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", )


async def test_delete_transit_gateway_peering_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )


async def test_delete_transit_gateway_policy_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_policy_table("test-transit_gateway_policy_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_policy_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_policy_table("test-transit_gateway_policy_table_id", )


async def test_delete_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )


async def test_delete_transit_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_route("test-transit_gateway_route_table_id", "test-destination_cidr_block", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_route("test-transit_gateway_route_table_id", "test-destination_cidr_block", )


async def test_delete_transit_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_route_table("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_route_table("test-transit_gateway_route_table_id", )


async def test_delete_transit_gateway_route_table_announcement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_route_table_announcement("test-transit_gateway_route_table_announcement_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_route_table_announcement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_route_table_announcement("test-transit_gateway_route_table_announcement_id", )


async def test_delete_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_delete_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )


async def test_delete_verified_access_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_verified_access_endpoint("test-verified_access_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_delete_verified_access_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_verified_access_endpoint("test-verified_access_endpoint_id", )


async def test_delete_verified_access_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_verified_access_group("test-verified_access_group_id", )
    mock_client.call.assert_called_once()


async def test_delete_verified_access_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_verified_access_group("test-verified_access_group_id", )


async def test_delete_verified_access_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_verified_access_instance("test-verified_access_instance_id", )
    mock_client.call.assert_called_once()


async def test_delete_verified_access_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_verified_access_instance("test-verified_access_instance_id", )


async def test_delete_verified_access_trust_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_verified_access_trust_provider("test-verified_access_trust_provider_id", )
    mock_client.call.assert_called_once()


async def test_delete_verified_access_trust_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_verified_access_trust_provider("test-verified_access_trust_provider_id", )


async def test_delete_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_volume("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_delete_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_volume("test-volume_id", )


async def test_delete_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc("test-vpc_id", )


async def test_delete_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_block_public_access_exclusion("test-exclusion_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_block_public_access_exclusion("test-exclusion_id", )


async def test_delete_vpc_endpoint_connection_notifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_endpoint_connection_notifications([], )
    mock_client.call.assert_called_once()


async def test_delete_vpc_endpoint_connection_notifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_endpoint_connection_notifications([], )


async def test_delete_vpc_endpoint_service_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_endpoint_service_configurations([], )
    mock_client.call.assert_called_once()


async def test_delete_vpc_endpoint_service_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_endpoint_service_configurations([], )


async def test_delete_vpc_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_endpoints([], )
    mock_client.call.assert_called_once()


async def test_delete_vpc_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_endpoints([], )


async def test_delete_vpc_peering_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_peering_connection("test-vpc_peering_connection_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_peering_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_peering_connection("test-vpc_peering_connection_id", )


async def test_delete_vpn_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpn_connection("test-vpn_connection_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpn_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpn_connection("test-vpn_connection_id", )


async def test_delete_vpn_connection_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpn_connection_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", )


async def test_delete_vpn_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpn_gateway("test-vpn_gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpn_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpn_gateway("test-vpn_gateway_id", )


async def test_deprovision_byoip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deprovision_byoip_cidr("test-cidr", )
    mock_client.call.assert_called_once()


async def test_deprovision_byoip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deprovision_byoip_cidr("test-cidr", )


async def test_deprovision_ipam_byoasn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deprovision_ipam_byoasn("test-ipam_id", "test-asn", )
    mock_client.call.assert_called_once()


async def test_deprovision_ipam_byoasn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deprovision_ipam_byoasn("test-ipam_id", "test-asn", )


async def test_deprovision_ipam_pool_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deprovision_ipam_pool_cidr("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_deprovision_ipam_pool_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deprovision_ipam_pool_cidr("test-ipam_pool_id", )


async def test_deprovision_public_ipv4_pool_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deprovision_public_ipv4_pool_cidr("test-pool_id", "test-cidr", )
    mock_client.call.assert_called_once()


async def test_deprovision_public_ipv4_pool_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deprovision_public_ipv4_pool_cidr("test-pool_id", "test-cidr", )


async def test_deregister_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_image("test-image_id", )
    mock_client.call.assert_called_once()


async def test_deregister_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_image("test-image_id", )


async def test_deregister_instance_event_notification_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_instance_event_notification_attributes({}, )
    mock_client.call.assert_called_once()


async def test_deregister_instance_event_notification_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_instance_event_notification_attributes({}, )


async def test_deregister_transit_gateway_multicast_group_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_transit_gateway_multicast_group_members()
    mock_client.call.assert_called_once()


async def test_deregister_transit_gateway_multicast_group_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_transit_gateway_multicast_group_members()


async def test_deregister_transit_gateway_multicast_group_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_transit_gateway_multicast_group_sources()
    mock_client.call.assert_called_once()


async def test_deregister_transit_gateway_multicast_group_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_transit_gateway_multicast_group_sources()


async def test_describe_account_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_attributes()
    mock_client.call.assert_called_once()


async def test_describe_account_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_attributes()


async def test_describe_address_transfers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_address_transfers()
    mock_client.call.assert_called_once()


async def test_describe_address_transfers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_address_transfers()


async def test_describe_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_addresses()
    mock_client.call.assert_called_once()


async def test_describe_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_addresses()


async def test_describe_addresses_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_addresses_attribute()
    mock_client.call.assert_called_once()


async def test_describe_addresses_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_addresses_attribute()


async def test_describe_aggregate_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_aggregate_id_format()
    mock_client.call.assert_called_once()


async def test_describe_aggregate_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_aggregate_id_format()


async def test_describe_availability_zones(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_availability_zones()
    mock_client.call.assert_called_once()


async def test_describe_availability_zones_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_availability_zones()


async def test_describe_aws_network_performance_metric_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_aws_network_performance_metric_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_aws_network_performance_metric_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_aws_network_performance_metric_subscriptions()


async def test_describe_bundle_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bundle_tasks()
    mock_client.call.assert_called_once()


async def test_describe_bundle_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bundle_tasks()


async def test_describe_byoip_cidrs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_byoip_cidrs(1, )
    mock_client.call.assert_called_once()


async def test_describe_byoip_cidrs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_byoip_cidrs(1, )


async def test_describe_capacity_block_extension_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_block_extension_history()
    mock_client.call.assert_called_once()


async def test_describe_capacity_block_extension_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_block_extension_history()


async def test_describe_capacity_block_extension_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_describe_capacity_block_extension_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", )


async def test_describe_capacity_block_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_block_offerings(1, )
    mock_client.call.assert_called_once()


async def test_describe_capacity_block_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_block_offerings(1, )


async def test_describe_capacity_block_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_block_status()
    mock_client.call.assert_called_once()


async def test_describe_capacity_block_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_block_status()


async def test_describe_capacity_blocks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_blocks()
    mock_client.call.assert_called_once()


async def test_describe_capacity_blocks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_blocks()


async def test_describe_capacity_manager_data_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_manager_data_exports()
    mock_client.call.assert_called_once()


async def test_describe_capacity_manager_data_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_manager_data_exports()


async def test_describe_capacity_reservation_billing_requests(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_reservation_billing_requests("test-role", )
    mock_client.call.assert_called_once()


async def test_describe_capacity_reservation_billing_requests_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_reservation_billing_requests("test-role", )


async def test_describe_capacity_reservation_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_reservation_fleets()
    mock_client.call.assert_called_once()


async def test_describe_capacity_reservation_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_reservation_fleets()


async def test_describe_capacity_reservation_topology(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_reservation_topology()
    mock_client.call.assert_called_once()


async def test_describe_capacity_reservation_topology_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_reservation_topology()


async def test_describe_capacity_reservations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_reservations()
    mock_client.call.assert_called_once()


async def test_describe_capacity_reservations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_reservations()


async def test_describe_carrier_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_carrier_gateways()
    mock_client.call.assert_called_once()


async def test_describe_carrier_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_carrier_gateways()


async def test_describe_classic_link_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_classic_link_instances()
    mock_client.call.assert_called_once()


async def test_describe_classic_link_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_classic_link_instances()


async def test_describe_client_vpn_authorization_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_describe_client_vpn_authorization_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", )


async def test_describe_client_vpn_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_client_vpn_connections("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_describe_client_vpn_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_client_vpn_connections("test-client_vpn_endpoint_id", )


async def test_describe_client_vpn_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_client_vpn_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_client_vpn_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_client_vpn_endpoints()


async def test_describe_client_vpn_routes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_client_vpn_routes("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_describe_client_vpn_routes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_client_vpn_routes("test-client_vpn_endpoint_id", )


async def test_describe_client_vpn_target_networks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_client_vpn_target_networks("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_describe_client_vpn_target_networks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_client_vpn_target_networks("test-client_vpn_endpoint_id", )


async def test_describe_coip_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_coip_pools()
    mock_client.call.assert_called_once()


async def test_describe_coip_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_coip_pools()


async def test_describe_conversion_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_conversion_tasks()
    mock_client.call.assert_called_once()


async def test_describe_conversion_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_conversion_tasks()


async def test_describe_customer_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_customer_gateways()
    mock_client.call.assert_called_once()


async def test_describe_customer_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_customer_gateways()


async def test_describe_declarative_policies_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_declarative_policies_reports()
    mock_client.call.assert_called_once()


async def test_describe_declarative_policies_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_declarative_policies_reports()


async def test_describe_dhcp_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dhcp_options()
    mock_client.call.assert_called_once()


async def test_describe_dhcp_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dhcp_options()


async def test_describe_egress_only_internet_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_egress_only_internet_gateways()
    mock_client.call.assert_called_once()


async def test_describe_egress_only_internet_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_egress_only_internet_gateways()


async def test_describe_elastic_gpus(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_elastic_gpus()
    mock_client.call.assert_called_once()


async def test_describe_elastic_gpus_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_elastic_gpus()


async def test_describe_export_image_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_export_image_tasks()
    mock_client.call.assert_called_once()


async def test_describe_export_image_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_export_image_tasks()


async def test_describe_export_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_export_tasks()
    mock_client.call.assert_called_once()


async def test_describe_export_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_export_tasks()


async def test_describe_fast_launch_images(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fast_launch_images()
    mock_client.call.assert_called_once()


async def test_describe_fast_launch_images_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fast_launch_images()


async def test_describe_fast_snapshot_restores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fast_snapshot_restores()
    mock_client.call.assert_called_once()


async def test_describe_fast_snapshot_restores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fast_snapshot_restores()


async def test_describe_fleet_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_history("test-fleet_id", "test-start_time", )
    mock_client.call.assert_called_once()


async def test_describe_fleet_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_history("test-fleet_id", "test-start_time", )


async def test_describe_fleet_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_instances("test-fleet_id", )
    mock_client.call.assert_called_once()


async def test_describe_fleet_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_instances("test-fleet_id", )


async def test_describe_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleets()
    mock_client.call.assert_called_once()


async def test_describe_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleets()


async def test_describe_flow_logs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_flow_logs()
    mock_client.call.assert_called_once()


async def test_describe_flow_logs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_flow_logs()


async def test_describe_fpga_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fpga_image_attribute("test-fpga_image_id", "test-attribute", )
    mock_client.call.assert_called_once()


async def test_describe_fpga_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fpga_image_attribute("test-fpga_image_id", "test-attribute", )


async def test_describe_fpga_images(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fpga_images()
    mock_client.call.assert_called_once()


async def test_describe_fpga_images_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fpga_images()


async def test_describe_host_reservation_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_host_reservation_offerings()
    mock_client.call.assert_called_once()


async def test_describe_host_reservation_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_host_reservation_offerings()


async def test_describe_host_reservations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_host_reservations()
    mock_client.call.assert_called_once()


async def test_describe_host_reservations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_host_reservations()


async def test_describe_hosts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_hosts()
    mock_client.call.assert_called_once()


async def test_describe_hosts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_hosts()


async def test_describe_iam_instance_profile_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_iam_instance_profile_associations()
    mock_client.call.assert_called_once()


async def test_describe_iam_instance_profile_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_iam_instance_profile_associations()


async def test_describe_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_id_format()
    mock_client.call.assert_called_once()


async def test_describe_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_id_format()


async def test_describe_identity_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_identity_id_format("test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_describe_identity_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_identity_id_format("test-principal_arn", )


async def test_describe_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_attribute("test-attribute", "test-image_id", )
    mock_client.call.assert_called_once()


async def test_describe_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_attribute("test-attribute", "test-image_id", )


async def test_describe_image_references(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_references([], )
    mock_client.call.assert_called_once()


async def test_describe_image_references_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_references([], )


async def test_describe_image_usage_report_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_usage_report_entries()
    mock_client.call.assert_called_once()


async def test_describe_image_usage_report_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_usage_report_entries()


async def test_describe_image_usage_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_image_usage_reports()
    mock_client.call.assert_called_once()


async def test_describe_image_usage_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_image_usage_reports()


async def test_describe_import_image_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_import_image_tasks()
    mock_client.call.assert_called_once()


async def test_describe_import_image_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_import_image_tasks()


async def test_describe_import_snapshot_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_import_snapshot_tasks()
    mock_client.call.assert_called_once()


async def test_describe_import_snapshot_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_import_snapshot_tasks()


async def test_describe_instance_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_attribute("test-instance_id", "test-attribute", )
    mock_client.call.assert_called_once()


async def test_describe_instance_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_attribute("test-instance_id", "test-attribute", )


async def test_describe_instance_connect_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_connect_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_instance_connect_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_connect_endpoints()


async def test_describe_instance_credit_specifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_credit_specifications()
    mock_client.call.assert_called_once()


async def test_describe_instance_credit_specifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_credit_specifications()


async def test_describe_instance_event_notification_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_event_notification_attributes()
    mock_client.call.assert_called_once()


async def test_describe_instance_event_notification_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_event_notification_attributes()


async def test_describe_instance_event_windows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_event_windows()
    mock_client.call.assert_called_once()


async def test_describe_instance_event_windows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_event_windows()


async def test_describe_instance_image_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_image_metadata()
    mock_client.call.assert_called_once()


async def test_describe_instance_image_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_image_metadata()


async def test_describe_instance_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_status()
    mock_client.call.assert_called_once()


async def test_describe_instance_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_status()


async def test_describe_instance_topology(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_topology()
    mock_client.call.assert_called_once()


async def test_describe_instance_topology_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_topology()


async def test_describe_instance_type_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_type_offerings()
    mock_client.call.assert_called_once()


async def test_describe_instance_type_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_type_offerings()


async def test_describe_instance_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_types()
    mock_client.call.assert_called_once()


async def test_describe_instance_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_types()


async def test_describe_internet_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_internet_gateways()
    mock_client.call.assert_called_once()


async def test_describe_internet_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_internet_gateways()


async def test_describe_ipam_byoasn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_byoasn()
    mock_client.call.assert_called_once()


async def test_describe_ipam_byoasn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_byoasn()


async def test_describe_ipam_external_resource_verification_tokens(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_external_resource_verification_tokens()
    mock_client.call.assert_called_once()


async def test_describe_ipam_external_resource_verification_tokens_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_external_resource_verification_tokens()


async def test_describe_ipam_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_pools()
    mock_client.call.assert_called_once()


async def test_describe_ipam_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_pools()


async def test_describe_ipam_prefix_list_resolver_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_prefix_list_resolver_targets()
    mock_client.call.assert_called_once()


async def test_describe_ipam_prefix_list_resolver_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_prefix_list_resolver_targets()


async def test_describe_ipam_prefix_list_resolvers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_prefix_list_resolvers()
    mock_client.call.assert_called_once()


async def test_describe_ipam_prefix_list_resolvers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_prefix_list_resolvers()


async def test_describe_ipam_resource_discoveries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_resource_discoveries()
    mock_client.call.assert_called_once()


async def test_describe_ipam_resource_discoveries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_resource_discoveries()


async def test_describe_ipam_resource_discovery_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_resource_discovery_associations()
    mock_client.call.assert_called_once()


async def test_describe_ipam_resource_discovery_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_resource_discovery_associations()


async def test_describe_ipam_scopes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipam_scopes()
    mock_client.call.assert_called_once()


async def test_describe_ipam_scopes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipam_scopes()


async def test_describe_ipams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipams()
    mock_client.call.assert_called_once()


async def test_describe_ipams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipams()


async def test_describe_ipv6_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ipv6_pools()
    mock_client.call.assert_called_once()


async def test_describe_ipv6_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ipv6_pools()


async def test_describe_key_pairs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_key_pairs()
    mock_client.call.assert_called_once()


async def test_describe_key_pairs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_key_pairs()


async def test_describe_launch_template_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_launch_template_versions()
    mock_client.call.assert_called_once()


async def test_describe_launch_template_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_launch_template_versions()


async def test_describe_launch_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_launch_templates()
    mock_client.call.assert_called_once()


async def test_describe_launch_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_launch_templates()


async def test_describe_local_gateway_route_table_virtual_interface_group_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateway_route_table_virtual_interface_group_associations()
    mock_client.call.assert_called_once()


async def test_describe_local_gateway_route_table_virtual_interface_group_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateway_route_table_virtual_interface_group_associations()


async def test_describe_local_gateway_route_table_vpc_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateway_route_table_vpc_associations()
    mock_client.call.assert_called_once()


async def test_describe_local_gateway_route_table_vpc_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateway_route_table_vpc_associations()


async def test_describe_local_gateway_route_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateway_route_tables()
    mock_client.call.assert_called_once()


async def test_describe_local_gateway_route_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateway_route_tables()


async def test_describe_local_gateway_virtual_interface_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateway_virtual_interface_groups()
    mock_client.call.assert_called_once()


async def test_describe_local_gateway_virtual_interface_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateway_virtual_interface_groups()


async def test_describe_local_gateway_virtual_interfaces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateway_virtual_interfaces()
    mock_client.call.assert_called_once()


async def test_describe_local_gateway_virtual_interfaces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateway_virtual_interfaces()


async def test_describe_local_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_local_gateways()
    mock_client.call.assert_called_once()


async def test_describe_local_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_local_gateways()


async def test_describe_locked_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_locked_snapshots()
    mock_client.call.assert_called_once()


async def test_describe_locked_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_locked_snapshots()


async def test_describe_mac_hosts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_mac_hosts()
    mock_client.call.assert_called_once()


async def test_describe_mac_hosts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_mac_hosts()


async def test_describe_mac_modification_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_mac_modification_tasks()
    mock_client.call.assert_called_once()


async def test_describe_mac_modification_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_mac_modification_tasks()


async def test_describe_managed_prefix_lists(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_managed_prefix_lists()
    mock_client.call.assert_called_once()


async def test_describe_managed_prefix_lists_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_managed_prefix_lists()


async def test_describe_moving_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_moving_addresses()
    mock_client.call.assert_called_once()


async def test_describe_moving_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_moving_addresses()


async def test_describe_nat_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_nat_gateways()
    mock_client.call.assert_called_once()


async def test_describe_nat_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_nat_gateways()


async def test_describe_network_acls(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_acls()
    mock_client.call.assert_called_once()


async def test_describe_network_acls_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_acls()


async def test_describe_network_insights_access_scope_analyses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_insights_access_scope_analyses()
    mock_client.call.assert_called_once()


async def test_describe_network_insights_access_scope_analyses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_insights_access_scope_analyses()


async def test_describe_network_insights_access_scopes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_insights_access_scopes()
    mock_client.call.assert_called_once()


async def test_describe_network_insights_access_scopes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_insights_access_scopes()


async def test_describe_network_insights_analyses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_insights_analyses()
    mock_client.call.assert_called_once()


async def test_describe_network_insights_analyses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_insights_analyses()


async def test_describe_network_insights_paths(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_insights_paths()
    mock_client.call.assert_called_once()


async def test_describe_network_insights_paths_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_insights_paths()


async def test_describe_network_interface_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_interface_attribute("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_describe_network_interface_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_interface_attribute("test-network_interface_id", )


async def test_describe_network_interface_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_interface_permissions()
    mock_client.call.assert_called_once()


async def test_describe_network_interface_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_interface_permissions()


async def test_describe_network_interfaces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_network_interfaces()
    mock_client.call.assert_called_once()


async def test_describe_network_interfaces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_network_interfaces()


async def test_describe_outpost_lags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_outpost_lags()
    mock_client.call.assert_called_once()


async def test_describe_outpost_lags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_outpost_lags()


async def test_describe_placement_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_placement_groups()
    mock_client.call.assert_called_once()


async def test_describe_placement_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_placement_groups()


async def test_describe_prefix_lists(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_prefix_lists()
    mock_client.call.assert_called_once()


async def test_describe_prefix_lists_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_prefix_lists()


async def test_describe_principal_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_principal_id_format()
    mock_client.call.assert_called_once()


async def test_describe_principal_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_principal_id_format()


async def test_describe_public_ipv4_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_public_ipv4_pools()
    mock_client.call.assert_called_once()


async def test_describe_public_ipv4_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_public_ipv4_pools()


async def test_describe_regions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_regions()
    mock_client.call.assert_called_once()


async def test_describe_regions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_regions()


async def test_describe_replace_root_volume_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replace_root_volume_tasks()
    mock_client.call.assert_called_once()


async def test_describe_replace_root_volume_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replace_root_volume_tasks()


async def test_describe_reserved_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_instances()
    mock_client.call.assert_called_once()


async def test_describe_reserved_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_instances()


async def test_describe_reserved_instances_listings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_instances_listings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_instances_listings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_instances_listings()


async def test_describe_reserved_instances_modifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_instances_modifications()
    mock_client.call.assert_called_once()


async def test_describe_reserved_instances_modifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_instances_modifications()


async def test_describe_reserved_instances_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_instances_offerings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_instances_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_instances_offerings()


async def test_describe_route_server_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_route_server_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_route_server_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_route_server_endpoints()


async def test_describe_route_server_peers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_route_server_peers()
    mock_client.call.assert_called_once()


async def test_describe_route_server_peers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_route_server_peers()


async def test_describe_route_servers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_route_servers()
    mock_client.call.assert_called_once()


async def test_describe_route_servers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_route_servers()


async def test_describe_route_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_route_tables()
    mock_client.call.assert_called_once()


async def test_describe_route_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_route_tables()


async def test_describe_scheduled_instance_availability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_instance_availability({}, {}, )
    mock_client.call.assert_called_once()


async def test_describe_scheduled_instance_availability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_instance_availability({}, {}, )


async def test_describe_scheduled_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_instances()
    mock_client.call.assert_called_once()


async def test_describe_scheduled_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_instances()


async def test_describe_security_group_references(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_group_references([], )
    mock_client.call.assert_called_once()


async def test_describe_security_group_references_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_group_references([], )


async def test_describe_security_group_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_group_rules()
    mock_client.call.assert_called_once()


async def test_describe_security_group_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_group_rules()


async def test_describe_security_group_vpc_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_group_vpc_associations()
    mock_client.call.assert_called_once()


async def test_describe_security_group_vpc_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_group_vpc_associations()


async def test_describe_service_link_virtual_interfaces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_link_virtual_interfaces()
    mock_client.call.assert_called_once()


async def test_describe_service_link_virtual_interfaces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_link_virtual_interfaces()


async def test_describe_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshot_attribute("test-attribute", "test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_describe_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshot_attribute("test-attribute", "test-snapshot_id", )


async def test_describe_snapshot_tier_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshot_tier_status()
    mock_client.call.assert_called_once()


async def test_describe_snapshot_tier_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshot_tier_status()


async def test_describe_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshots()
    mock_client.call.assert_called_once()


async def test_describe_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshots()


async def test_describe_spot_datafeed_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_datafeed_subscription()
    mock_client.call.assert_called_once()


async def test_describe_spot_datafeed_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_datafeed_subscription()


async def test_describe_spot_fleet_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_fleet_instances("test-spot_fleet_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_spot_fleet_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_fleet_instances("test-spot_fleet_request_id", )


async def test_describe_spot_fleet_request_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", )
    mock_client.call.assert_called_once()


async def test_describe_spot_fleet_request_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", )


async def test_describe_spot_fleet_requests(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_fleet_requests()
    mock_client.call.assert_called_once()


async def test_describe_spot_fleet_requests_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_fleet_requests()


async def test_describe_spot_instance_requests(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_instance_requests()
    mock_client.call.assert_called_once()


async def test_describe_spot_instance_requests_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_instance_requests()


async def test_describe_spot_price_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_spot_price_history()
    mock_client.call.assert_called_once()


async def test_describe_spot_price_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_spot_price_history()


async def test_describe_stale_security_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stale_security_groups("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_describe_stale_security_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stale_security_groups("test-vpc_id", )


async def test_describe_store_image_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_store_image_tasks()
    mock_client.call.assert_called_once()


async def test_describe_store_image_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_store_image_tasks()


async def test_describe_subnets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_subnets()
    mock_client.call.assert_called_once()


async def test_describe_subnets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_subnets()


async def test_describe_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tags()
    mock_client.call.assert_called_once()


async def test_describe_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tags()


async def test_describe_traffic_mirror_filter_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_mirror_filter_rules()
    mock_client.call.assert_called_once()


async def test_describe_traffic_mirror_filter_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_mirror_filter_rules()


async def test_describe_traffic_mirror_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_mirror_filters()
    mock_client.call.assert_called_once()


async def test_describe_traffic_mirror_filters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_mirror_filters()


async def test_describe_traffic_mirror_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_mirror_sessions()
    mock_client.call.assert_called_once()


async def test_describe_traffic_mirror_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_mirror_sessions()


async def test_describe_traffic_mirror_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_mirror_targets()
    mock_client.call.assert_called_once()


async def test_describe_traffic_mirror_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_mirror_targets()


async def test_describe_transit_gateway_attachments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_attachments()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_attachments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_attachments()


async def test_describe_transit_gateway_connect_peers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_connect_peers()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_connect_peers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_connect_peers()


async def test_describe_transit_gateway_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_connects()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_connects()


async def test_describe_transit_gateway_multicast_domains(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_multicast_domains()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_multicast_domains_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_multicast_domains()


async def test_describe_transit_gateway_peering_attachments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_peering_attachments()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_peering_attachments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_peering_attachments()


async def test_describe_transit_gateway_policy_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_policy_tables()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_policy_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_policy_tables()


async def test_describe_transit_gateway_route_table_announcements(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_route_table_announcements()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_route_table_announcements_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_route_table_announcements()


async def test_describe_transit_gateway_route_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_route_tables()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_route_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_route_tables()


async def test_describe_transit_gateway_vpc_attachments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateway_vpc_attachments()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateway_vpc_attachments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateway_vpc_attachments()


async def test_describe_transit_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_transit_gateways()
    mock_client.call.assert_called_once()


async def test_describe_transit_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_transit_gateways()


async def test_describe_trunk_interface_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_trunk_interface_associations()
    mock_client.call.assert_called_once()


async def test_describe_trunk_interface_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_trunk_interface_associations()


async def test_describe_verified_access_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_verified_access_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_verified_access_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_verified_access_endpoints()


async def test_describe_verified_access_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_verified_access_groups()
    mock_client.call.assert_called_once()


async def test_describe_verified_access_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_verified_access_groups()


async def test_describe_verified_access_instance_logging_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_verified_access_instance_logging_configurations()
    mock_client.call.assert_called_once()


async def test_describe_verified_access_instance_logging_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_verified_access_instance_logging_configurations()


async def test_describe_verified_access_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_verified_access_instances()
    mock_client.call.assert_called_once()


async def test_describe_verified_access_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_verified_access_instances()


async def test_describe_verified_access_trust_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_verified_access_trust_providers()
    mock_client.call.assert_called_once()


async def test_describe_verified_access_trust_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_verified_access_trust_providers()


async def test_describe_volume_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_volume_attribute("test-attribute", "test-volume_id", )
    mock_client.call.assert_called_once()


async def test_describe_volume_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_volume_attribute("test-attribute", "test-volume_id", )


async def test_describe_volume_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_volume_status()
    mock_client.call.assert_called_once()


async def test_describe_volume_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_volume_status()


async def test_describe_volumes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_volumes()
    mock_client.call.assert_called_once()


async def test_describe_volumes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_volumes()


async def test_describe_volumes_modifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_volumes_modifications()
    mock_client.call.assert_called_once()


async def test_describe_volumes_modifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_volumes_modifications()


async def test_describe_vpc_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_attribute("test-attribute", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_attribute("test-attribute", "test-vpc_id", )


async def test_describe_vpc_block_public_access_exclusions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_block_public_access_exclusions()
    mock_client.call.assert_called_once()


async def test_describe_vpc_block_public_access_exclusions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_block_public_access_exclusions()


async def test_describe_vpc_block_public_access_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_block_public_access_options()
    mock_client.call.assert_called_once()


async def test_describe_vpc_block_public_access_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_block_public_access_options()


async def test_describe_vpc_classic_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_classic_link()
    mock_client.call.assert_called_once()


async def test_describe_vpc_classic_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_classic_link()


async def test_describe_vpc_classic_link_dns_support(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_classic_link_dns_support()
    mock_client.call.assert_called_once()


async def test_describe_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_classic_link_dns_support()


async def test_describe_vpc_endpoint_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_associations()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_associations()


async def test_describe_vpc_endpoint_connection_notifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_connection_notifications()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_connection_notifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_connection_notifications()


async def test_describe_vpc_endpoint_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_connections()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_connections()


async def test_describe_vpc_endpoint_service_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_service_configurations()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_service_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_service_configurations()


async def test_describe_vpc_endpoint_service_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_service_permissions("test-service_id", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_service_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_service_permissions("test-service_id", )


async def test_describe_vpc_endpoint_services(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoint_services()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoint_services_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoint_services()


async def test_describe_vpc_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_vpc_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_endpoints()


async def test_describe_vpc_peering_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_peering_connections()
    mock_client.call.assert_called_once()


async def test_describe_vpc_peering_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_peering_connections()


async def test_describe_vpcs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpcs()
    mock_client.call.assert_called_once()


async def test_describe_vpcs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpcs()


async def test_describe_vpn_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpn_connections()
    mock_client.call.assert_called_once()


async def test_describe_vpn_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpn_connections()


async def test_describe_vpn_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpn_gateways()
    mock_client.call.assert_called_once()


async def test_describe_vpn_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpn_gateways()


async def test_detach_classic_link_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_classic_link_vpc("test-instance_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_detach_classic_link_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_classic_link_vpc("test-instance_id", "test-vpc_id", )


async def test_detach_internet_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_internet_gateway("test-internet_gateway_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_detach_internet_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_internet_gateway("test-internet_gateway_id", "test-vpc_id", )


async def test_detach_network_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_network_interface("test-attachment_id", )
    mock_client.call.assert_called_once()


async def test_detach_network_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_network_interface("test-attachment_id", )


async def test_detach_verified_access_trust_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", )
    mock_client.call.assert_called_once()


async def test_detach_verified_access_trust_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", )


async def test_detach_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_volume("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_detach_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_volume("test-volume_id", )


async def test_detach_vpn_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", )
    mock_client.call.assert_called_once()


async def test_detach_vpn_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", )


async def test_disable_address_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_address_transfer("test-allocation_id", )
    mock_client.call.assert_called_once()


async def test_disable_address_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_address_transfer("test-allocation_id", )


async def test_disable_allowed_images_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_allowed_images_settings()
    mock_client.call.assert_called_once()


async def test_disable_allowed_images_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_allowed_images_settings()


async def test_disable_aws_network_performance_metric_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_aws_network_performance_metric_subscription()
    mock_client.call.assert_called_once()


async def test_disable_aws_network_performance_metric_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_aws_network_performance_metric_subscription()


async def test_disable_capacity_manager(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_capacity_manager()
    mock_client.call.assert_called_once()


async def test_disable_capacity_manager_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_capacity_manager()


async def test_disable_ebs_encryption_by_default(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_ebs_encryption_by_default()
    mock_client.call.assert_called_once()


async def test_disable_ebs_encryption_by_default_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_ebs_encryption_by_default()


async def test_disable_fast_launch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_fast_launch("test-image_id", )
    mock_client.call.assert_called_once()


async def test_disable_fast_launch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_fast_launch("test-image_id", )


async def test_disable_fast_snapshot_restores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_fast_snapshot_restores([], )
    mock_client.call.assert_called_once()


async def test_disable_fast_snapshot_restores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_fast_snapshot_restores([], )


async def test_disable_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_image("test-image_id", )
    mock_client.call.assert_called_once()


async def test_disable_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_image("test-image_id", )


async def test_disable_image_block_public_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_image_block_public_access()
    mock_client.call.assert_called_once()


async def test_disable_image_block_public_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_image_block_public_access()


async def test_disable_image_deprecation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_image_deprecation("test-image_id", )
    mock_client.call.assert_called_once()


async def test_disable_image_deprecation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_image_deprecation("test-image_id", )


async def test_disable_image_deregistration_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_image_deregistration_protection("test-image_id", )
    mock_client.call.assert_called_once()


async def test_disable_image_deregistration_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_image_deregistration_protection("test-image_id", )


async def test_disable_ipam_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_ipam_organization_admin_account("test-delegated_admin_account_id", )
    mock_client.call.assert_called_once()


async def test_disable_ipam_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_ipam_organization_admin_account("test-delegated_admin_account_id", )


async def test_disable_route_server_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_route_server_propagation("test-route_server_id", "test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_disable_route_server_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_route_server_propagation("test-route_server_id", "test-route_table_id", )


async def test_disable_serial_console_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_serial_console_access()
    mock_client.call.assert_called_once()


async def test_disable_serial_console_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_serial_console_access()


async def test_disable_snapshot_block_public_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_snapshot_block_public_access()
    mock_client.call.assert_called_once()


async def test_disable_snapshot_block_public_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_snapshot_block_public_access()


async def test_disable_transit_gateway_route_table_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_disable_transit_gateway_route_table_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", )


async def test_disable_vgw_route_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_vgw_route_propagation("test-gateway_id", "test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_disable_vgw_route_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_vgw_route_propagation("test-gateway_id", "test-route_table_id", )


async def test_disable_vpc_classic_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_vpc_classic_link("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_disable_vpc_classic_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_vpc_classic_link("test-vpc_id", )


async def test_disable_vpc_classic_link_dns_support(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_vpc_classic_link_dns_support()
    mock_client.call.assert_called_once()


async def test_disable_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_vpc_classic_link_dns_support()


async def test_disassociate_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_address()
    mock_client.call.assert_called_once()


async def test_disassociate_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_address()


async def test_disassociate_capacity_reservation_billing_owner(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_capacity_reservation_billing_owner_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", )


async def test_disassociate_client_vpn_target_network(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_client_vpn_target_network_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-association_id", )


async def test_disassociate_enclave_certificate_iam_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_enclave_certificate_iam_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", )


async def test_disassociate_iam_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_iam_instance_profile("test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_iam_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_iam_instance_profile("test-association_id", )


async def test_disassociate_instance_event_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_instance_event_window("test-instance_event_window_id", {}, )
    mock_client.call.assert_called_once()


async def test_disassociate_instance_event_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_instance_event_window("test-instance_event_window_id", {}, )


async def test_disassociate_ipam_byoasn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_ipam_byoasn("test-asn", "test-cidr", )
    mock_client.call.assert_called_once()


async def test_disassociate_ipam_byoasn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_ipam_byoasn("test-asn", "test-cidr", )


async def test_disassociate_ipam_resource_discovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_ipam_resource_discovery("test-ipam_resource_discovery_association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_ipam_resource_discovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_ipam_resource_discovery("test-ipam_resource_discovery_association_id", )


async def test_disassociate_nat_gateway_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_nat_gateway_address("test-nat_gateway_id", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_nat_gateway_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_nat_gateway_address("test-nat_gateway_id", [], )


async def test_disassociate_route_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_route_server("test-route_server_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_route_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_route_server("test-route_server_id", "test-vpc_id", )


async def test_disassociate_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_route_table("test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_route_table("test-association_id", )


async def test_disassociate_security_group_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_security_group_vpc("test-group_id", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_security_group_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_security_group_vpc("test-group_id", "test-vpc_id", )


async def test_disassociate_subnet_cidr_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_subnet_cidr_block("test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_subnet_cidr_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_subnet_cidr_block("test-association_id", )


async def test_disassociate_transit_gateway_multicast_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], )


async def test_disassociate_transit_gateway_policy_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_transit_gateway_policy_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", )


async def test_disassociate_transit_gateway_route_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_transit_gateway_route_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", )


async def test_disassociate_trunk_interface(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_trunk_interface("test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_trunk_interface_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_trunk_interface("test-association_id", )


async def test_disassociate_vpc_cidr_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_vpc_cidr_block("test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_vpc_cidr_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_vpc_cidr_block("test-association_id", )


async def test_enable_address_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_address_transfer("test-allocation_id", "test-transfer_account_id", )
    mock_client.call.assert_called_once()


async def test_enable_address_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_address_transfer("test-allocation_id", "test-transfer_account_id", )


async def test_enable_allowed_images_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_allowed_images_settings("test-allowed_images_settings_state", )
    mock_client.call.assert_called_once()


async def test_enable_allowed_images_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_allowed_images_settings("test-allowed_images_settings_state", )


async def test_enable_aws_network_performance_metric_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_aws_network_performance_metric_subscription()
    mock_client.call.assert_called_once()


async def test_enable_aws_network_performance_metric_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_aws_network_performance_metric_subscription()


async def test_enable_capacity_manager(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_capacity_manager()
    mock_client.call.assert_called_once()


async def test_enable_capacity_manager_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_capacity_manager()


async def test_enable_ebs_encryption_by_default(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_ebs_encryption_by_default()
    mock_client.call.assert_called_once()


async def test_enable_ebs_encryption_by_default_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_ebs_encryption_by_default()


async def test_enable_fast_launch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_fast_launch("test-image_id", )
    mock_client.call.assert_called_once()


async def test_enable_fast_launch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_fast_launch("test-image_id", )


async def test_enable_fast_snapshot_restores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_fast_snapshot_restores([], )
    mock_client.call.assert_called_once()


async def test_enable_fast_snapshot_restores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_fast_snapshot_restores([], )


async def test_enable_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_image("test-image_id", )
    mock_client.call.assert_called_once()


async def test_enable_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_image("test-image_id", )


async def test_enable_image_block_public_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_image_block_public_access("test-image_block_public_access_state", )
    mock_client.call.assert_called_once()


async def test_enable_image_block_public_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_image_block_public_access("test-image_block_public_access_state", )


async def test_enable_image_deprecation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_image_deprecation("test-image_id", "test-deprecate_at", )
    mock_client.call.assert_called_once()


async def test_enable_image_deprecation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_image_deprecation("test-image_id", "test-deprecate_at", )


async def test_enable_image_deregistration_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_image_deregistration_protection("test-image_id", )
    mock_client.call.assert_called_once()


async def test_enable_image_deregistration_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_image_deregistration_protection("test-image_id", )


async def test_enable_ipam_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_ipam_organization_admin_account("test-delegated_admin_account_id", )
    mock_client.call.assert_called_once()


async def test_enable_ipam_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_ipam_organization_admin_account("test-delegated_admin_account_id", )


async def test_enable_reachability_analyzer_organization_sharing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_reachability_analyzer_organization_sharing()
    mock_client.call.assert_called_once()


async def test_enable_reachability_analyzer_organization_sharing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_reachability_analyzer_organization_sharing()


async def test_enable_route_server_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_route_server_propagation("test-route_server_id", "test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_enable_route_server_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_route_server_propagation("test-route_server_id", "test-route_table_id", )


async def test_enable_serial_console_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_serial_console_access()
    mock_client.call.assert_called_once()


async def test_enable_serial_console_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_serial_console_access()


async def test_enable_snapshot_block_public_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_snapshot_block_public_access("test-state", )
    mock_client.call.assert_called_once()


async def test_enable_snapshot_block_public_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_snapshot_block_public_access("test-state", )


async def test_enable_transit_gateway_route_table_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_enable_transit_gateway_route_table_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", )


async def test_enable_vgw_route_propagation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_vgw_route_propagation("test-gateway_id", "test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_enable_vgw_route_propagation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_vgw_route_propagation("test-gateway_id", "test-route_table_id", )


async def test_enable_volume_io(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_volume_io("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_enable_volume_io_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_volume_io("test-volume_id", )


async def test_enable_vpc_classic_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_vpc_classic_link("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_enable_vpc_classic_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_vpc_classic_link("test-vpc_id", )


async def test_enable_vpc_classic_link_dns_support(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_vpc_classic_link_dns_support()
    mock_client.call.assert_called_once()


async def test_enable_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_vpc_classic_link_dns_support()


async def test_export_client_vpn_client_certificate_revocation_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_export_client_vpn_client_certificate_revocation_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", )


async def test_export_client_vpn_client_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_client_vpn_client_configuration("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_export_client_vpn_client_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_client_vpn_client_configuration("test-client_vpn_endpoint_id", )


async def test_export_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_image("test-disk_image_format", "test-image_id", {}, )
    mock_client.call.assert_called_once()


async def test_export_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_image("test-disk_image_format", "test-image_id", {}, )


async def test_export_transit_gateway_routes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", )
    mock_client.call.assert_called_once()


async def test_export_transit_gateway_routes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", )


async def test_export_verified_access_instance_client_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_verified_access_instance_client_configuration("test-verified_access_instance_id", )
    mock_client.call.assert_called_once()


async def test_export_verified_access_instance_client_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_verified_access_instance_client_configuration("test-verified_access_instance_id", )


async def test_get_active_vpn_tunnel_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_active_vpn_tunnel_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )
    mock_client.call.assert_called_once()


async def test_get_active_vpn_tunnel_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_active_vpn_tunnel_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )


async def test_get_allowed_images_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_allowed_images_settings()
    mock_client.call.assert_called_once()


async def test_get_allowed_images_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_allowed_images_settings()


async def test_get_associated_enclave_certificate_iam_roles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_associated_enclave_certificate_iam_roles("test-certificate_arn", )
    mock_client.call.assert_called_once()


async def test_get_associated_enclave_certificate_iam_roles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_associated_enclave_certificate_iam_roles("test-certificate_arn", )


async def test_get_associated_ipv6_pool_cidrs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_associated_ipv6_pool_cidrs("test-pool_id", )
    mock_client.call.assert_called_once()


async def test_get_associated_ipv6_pool_cidrs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_associated_ipv6_pool_cidrs("test-pool_id", )


async def test_get_aws_network_performance_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_aws_network_performance_data()
    mock_client.call.assert_called_once()


async def test_get_aws_network_performance_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_aws_network_performance_data()


async def test_get_capacity_manager_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_capacity_manager_attributes()
    mock_client.call.assert_called_once()


async def test_get_capacity_manager_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_manager_attributes()


async def test_get_capacity_manager_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_capacity_manager_metric_data([], "test-start_time", "test-end_time", 1, )
    mock_client.call.assert_called_once()


async def test_get_capacity_manager_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_manager_metric_data([], "test-start_time", "test-end_time", 1, )


async def test_get_capacity_manager_metric_dimensions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_capacity_manager_metric_dimensions([], "test-start_time", "test-end_time", [], )
    mock_client.call.assert_called_once()


async def test_get_capacity_manager_metric_dimensions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_manager_metric_dimensions([], "test-start_time", "test-end_time", [], )


async def test_get_capacity_reservation_usage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_capacity_reservation_usage("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_get_capacity_reservation_usage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_reservation_usage("test-capacity_reservation_id", )


async def test_get_coip_pool_usage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_coip_pool_usage("test-pool_id", )
    mock_client.call.assert_called_once()


async def test_get_coip_pool_usage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_coip_pool_usage("test-pool_id", )


async def test_get_console_output(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_console_output("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_console_output_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_console_output("test-instance_id", )


async def test_get_console_screenshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_console_screenshot("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_console_screenshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_console_screenshot("test-instance_id", )


async def test_get_declarative_policies_report_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_declarative_policies_report_summary("test-report_id", )
    mock_client.call.assert_called_once()


async def test_get_declarative_policies_report_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_declarative_policies_report_summary("test-report_id", )


async def test_get_default_credit_specification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_default_credit_specification("test-instance_family", )
    mock_client.call.assert_called_once()


async def test_get_default_credit_specification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_default_credit_specification("test-instance_family", )


async def test_get_ebs_default_kms_key_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ebs_default_kms_key_id()
    mock_client.call.assert_called_once()


async def test_get_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ebs_default_kms_key_id()


async def test_get_ebs_encryption_by_default(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ebs_encryption_by_default()
    mock_client.call.assert_called_once()


async def test_get_ebs_encryption_by_default_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ebs_encryption_by_default()


async def test_get_flow_logs_integration_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_logs_integration_template("test-flow_log_id", "test-config_delivery_s3_destination_arn", {}, )
    mock_client.call.assert_called_once()


async def test_get_flow_logs_integration_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_logs_integration_template("test-flow_log_id", "test-config_delivery_s3_destination_arn", {}, )


async def test_get_groups_for_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_groups_for_capacity_reservation("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_get_groups_for_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_groups_for_capacity_reservation("test-capacity_reservation_id", )


async def test_get_host_reservation_purchase_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_host_reservation_purchase_preview([], "test-offering_id", )
    mock_client.call.assert_called_once()


async def test_get_host_reservation_purchase_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_host_reservation_purchase_preview([], "test-offering_id", )


async def test_get_image_ancestry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_image_ancestry("test-image_id", )
    mock_client.call.assert_called_once()


async def test_get_image_ancestry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_image_ancestry("test-image_id", )


async def test_get_image_block_public_access_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_image_block_public_access_state()
    mock_client.call.assert_called_once()


async def test_get_image_block_public_access_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_image_block_public_access_state()


async def test_get_instance_metadata_defaults(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_metadata_defaults()
    mock_client.call.assert_called_once()


async def test_get_instance_metadata_defaults_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_metadata_defaults()


async def test_get_instance_tpm_ek_pub(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_tpm_ek_pub("test-instance_id", "test-key_type", "test-key_format", )
    mock_client.call.assert_called_once()


async def test_get_instance_tpm_ek_pub_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_tpm_ek_pub("test-instance_id", "test-key_type", "test-key_format", )


async def test_get_instance_types_from_instance_requirements(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_types_from_instance_requirements([], [], {}, )
    mock_client.call.assert_called_once()


async def test_get_instance_types_from_instance_requirements_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_types_from_instance_requirements([], [], {}, )


async def test_get_instance_uefi_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_uefi_data("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_instance_uefi_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_uefi_data("test-instance_id", )


async def test_get_ipam_address_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_address_history("test-cidr", "test-ipam_scope_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_address_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_address_history("test-cidr", "test-ipam_scope_id", )


async def test_get_ipam_discovered_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", )
    mock_client.call.assert_called_once()


async def test_get_ipam_discovered_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", )


async def test_get_ipam_discovered_public_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", )
    mock_client.call.assert_called_once()


async def test_get_ipam_discovered_public_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", )


async def test_get_ipam_discovered_resource_cidrs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", )
    mock_client.call.assert_called_once()


async def test_get_ipam_discovered_resource_cidrs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", )


async def test_get_ipam_pool_allocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_pool_allocations("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_pool_allocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_pool_allocations("test-ipam_pool_id", )


async def test_get_ipam_pool_cidrs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_pool_cidrs("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_pool_cidrs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_pool_cidrs("test-ipam_pool_id", )


async def test_get_ipam_prefix_list_resolver_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_prefix_list_resolver_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", )


async def test_get_ipam_prefix_list_resolver_version_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", 1, )
    mock_client.call.assert_called_once()


async def test_get_ipam_prefix_list_resolver_version_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", 1, )


async def test_get_ipam_prefix_list_resolver_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_prefix_list_resolver_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", )


async def test_get_ipam_resource_cidrs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ipam_resource_cidrs("test-ipam_scope_id", )
    mock_client.call.assert_called_once()


async def test_get_ipam_resource_cidrs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ipam_resource_cidrs("test-ipam_scope_id", )


async def test_get_launch_template_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_launch_template_data("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_launch_template_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_launch_template_data("test-instance_id", )


async def test_get_managed_prefix_list_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_managed_prefix_list_associations("test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_get_managed_prefix_list_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_managed_prefix_list_associations("test-prefix_list_id", )


async def test_get_managed_prefix_list_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_managed_prefix_list_entries("test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_get_managed_prefix_list_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_managed_prefix_list_entries("test-prefix_list_id", )


async def test_get_network_insights_access_scope_analysis_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", )
    mock_client.call.assert_called_once()


async def test_get_network_insights_access_scope_analysis_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", )


async def test_get_network_insights_access_scope_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_network_insights_access_scope_content("test-network_insights_access_scope_id", )
    mock_client.call.assert_called_once()


async def test_get_network_insights_access_scope_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_network_insights_access_scope_content("test-network_insights_access_scope_id", )


async def test_get_password_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_password_data("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_password_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_password_data("test-instance_id", )


async def test_get_reserved_instances_exchange_quote(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reserved_instances_exchange_quote([], )
    mock_client.call.assert_called_once()


async def test_get_reserved_instances_exchange_quote_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reserved_instances_exchange_quote([], )


async def test_get_route_server_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_route_server_associations("test-route_server_id", )
    mock_client.call.assert_called_once()


async def test_get_route_server_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_route_server_associations("test-route_server_id", )


async def test_get_route_server_propagations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_route_server_propagations("test-route_server_id", )
    mock_client.call.assert_called_once()


async def test_get_route_server_propagations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_route_server_propagations("test-route_server_id", )


async def test_get_route_server_routing_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_route_server_routing_database("test-route_server_id", )
    mock_client.call.assert_called_once()


async def test_get_route_server_routing_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_route_server_routing_database("test-route_server_id", )


async def test_get_security_groups_for_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_security_groups_for_vpc("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_get_security_groups_for_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_security_groups_for_vpc("test-vpc_id", )


async def test_get_serial_console_access_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_serial_console_access_status()
    mock_client.call.assert_called_once()


async def test_get_serial_console_access_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_serial_console_access_status()


async def test_get_snapshot_block_public_access_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_snapshot_block_public_access_state()
    mock_client.call.assert_called_once()


async def test_get_snapshot_block_public_access_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_snapshot_block_public_access_state()


async def test_get_spot_placement_scores(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_spot_placement_scores(1, )
    mock_client.call.assert_called_once()


async def test_get_spot_placement_scores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_spot_placement_scores(1, )


async def test_get_subnet_cidr_reservations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_subnet_cidr_reservations("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_get_subnet_cidr_reservations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_subnet_cidr_reservations("test-subnet_id", )


async def test_get_transit_gateway_attachment_propagations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_attachment_propagations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", )


async def test_get_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", )


async def test_get_transit_gateway_policy_table_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_policy_table_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", )


async def test_get_transit_gateway_policy_table_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_policy_table_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", )


async def test_get_transit_gateway_prefix_list_references(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_prefix_list_references_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", )


async def test_get_transit_gateway_route_table_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_route_table_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", )


async def test_get_transit_gateway_route_table_propagations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_get_transit_gateway_route_table_propagations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", )


async def test_get_verified_access_endpoint_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_verified_access_endpoint_policy("test-verified_access_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_get_verified_access_endpoint_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_verified_access_endpoint_policy("test-verified_access_endpoint_id", )


async def test_get_verified_access_endpoint_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_verified_access_endpoint_targets("test-verified_access_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_get_verified_access_endpoint_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_verified_access_endpoint_targets("test-verified_access_endpoint_id", )


async def test_get_verified_access_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_verified_access_group_policy("test-verified_access_group_id", )
    mock_client.call.assert_called_once()


async def test_get_verified_access_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_verified_access_group_policy("test-verified_access_group_id", )


async def test_get_vpn_connection_device_sample_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", )
    mock_client.call.assert_called_once()


async def test_get_vpn_connection_device_sample_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", )


async def test_get_vpn_connection_device_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_vpn_connection_device_types()
    mock_client.call.assert_called_once()


async def test_get_vpn_connection_device_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_vpn_connection_device_types()


async def test_get_vpn_tunnel_replacement_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_vpn_tunnel_replacement_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )
    mock_client.call.assert_called_once()


async def test_get_vpn_tunnel_replacement_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_vpn_tunnel_replacement_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )


async def test_import_client_vpn_client_certificate_revocation_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", "test-certificate_revocation_list", )
    mock_client.call.assert_called_once()


async def test_import_client_vpn_client_certificate_revocation_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", "test-certificate_revocation_list", )


async def test_import_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_image()
    mock_client.call.assert_called_once()


async def test_import_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_image()


async def test_import_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_instance("test-platform", )
    mock_client.call.assert_called_once()


async def test_import_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_instance("test-platform", )


async def test_import_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_key_pair("test-key_name", "test-public_key_material", )
    mock_client.call.assert_called_once()


async def test_import_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_key_pair("test-key_name", "test-public_key_material", )


async def test_import_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_snapshot()
    mock_client.call.assert_called_once()


async def test_import_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_snapshot()


async def test_import_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_volume({}, {}, )
    mock_client.call.assert_called_once()


async def test_import_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_volume({}, {}, )


async def test_list_images_in_recycle_bin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_images_in_recycle_bin()
    mock_client.call.assert_called_once()


async def test_list_images_in_recycle_bin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_images_in_recycle_bin()


async def test_list_snapshots_in_recycle_bin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_snapshots_in_recycle_bin()
    mock_client.call.assert_called_once()


async def test_list_snapshots_in_recycle_bin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_snapshots_in_recycle_bin()


async def test_lock_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await lock_snapshot("test-snapshot_id", "test-lock_mode", )
    mock_client.call.assert_called_once()


async def test_lock_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await lock_snapshot("test-snapshot_id", "test-lock_mode", )


async def test_modify_address_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_address_attribute("test-allocation_id", )
    mock_client.call.assert_called_once()


async def test_modify_address_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_address_attribute("test-allocation_id", )


async def test_modify_availability_zone_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_availability_zone_group("test-group_name", "test-opt_in_status", )
    mock_client.call.assert_called_once()


async def test_modify_availability_zone_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_availability_zone_group("test-group_name", "test-opt_in_status", )


async def test_modify_capacity_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_capacity_reservation("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_modify_capacity_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_capacity_reservation("test-capacity_reservation_id", )


async def test_modify_capacity_reservation_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", )
    mock_client.call.assert_called_once()


async def test_modify_capacity_reservation_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", )


async def test_modify_client_vpn_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_client_vpn_endpoint("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_modify_client_vpn_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_client_vpn_endpoint("test-client_vpn_endpoint_id", )


async def test_modify_default_credit_specification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_default_credit_specification("test-instance_family", "test-cpu_credits", )
    mock_client.call.assert_called_once()


async def test_modify_default_credit_specification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_default_credit_specification("test-instance_family", "test-cpu_credits", )


async def test_modify_ebs_default_kms_key_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ebs_default_kms_key_id("test-kms_key_id", )
    mock_client.call.assert_called_once()


async def test_modify_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ebs_default_kms_key_id("test-kms_key_id", )


async def test_modify_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_fleet("test-fleet_id", )
    mock_client.call.assert_called_once()


async def test_modify_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_fleet("test-fleet_id", )


async def test_modify_fpga_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_fpga_image_attribute("test-fpga_image_id", )
    mock_client.call.assert_called_once()


async def test_modify_fpga_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_fpga_image_attribute("test-fpga_image_id", )


async def test_modify_hosts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_hosts([], )
    mock_client.call.assert_called_once()


async def test_modify_hosts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_hosts([], )


async def test_modify_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_id_format("test-resource", True, )
    mock_client.call.assert_called_once()


async def test_modify_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_id_format("test-resource", True, )


async def test_modify_identity_id_format(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_identity_id_format("test-resource", True, "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_modify_identity_id_format_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_identity_id_format("test-resource", True, "test-principal_arn", )


async def test_modify_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_image_attribute("test-image_id", )
    mock_client.call.assert_called_once()


async def test_modify_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_image_attribute("test-image_id", )


async def test_modify_instance_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_attribute("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_attribute("test-instance_id", )


async def test_modify_instance_capacity_reservation_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_capacity_reservation_attributes("test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_modify_instance_capacity_reservation_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_capacity_reservation_attributes("test-instance_id", {}, )


async def test_modify_instance_connect_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_connect_endpoint("test-instance_connect_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_connect_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_connect_endpoint("test-instance_connect_endpoint_id", )


async def test_modify_instance_cpu_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_cpu_options("test-instance_id", 1, 1, )
    mock_client.call.assert_called_once()


async def test_modify_instance_cpu_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_cpu_options("test-instance_id", 1, 1, )


async def test_modify_instance_credit_specification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_credit_specification([], )
    mock_client.call.assert_called_once()


async def test_modify_instance_credit_specification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_credit_specification([], )


async def test_modify_instance_event_start_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_event_start_time("test-instance_id", "test-instance_event_id", "test-not_before", )
    mock_client.call.assert_called_once()


async def test_modify_instance_event_start_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_event_start_time("test-instance_id", "test-instance_event_id", "test-not_before", )


async def test_modify_instance_event_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_event_window("test-instance_event_window_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_event_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_event_window("test-instance_event_window_id", )


async def test_modify_instance_maintenance_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_maintenance_options("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_maintenance_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_maintenance_options("test-instance_id", )


async def test_modify_instance_metadata_defaults(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_metadata_defaults()
    mock_client.call.assert_called_once()


async def test_modify_instance_metadata_defaults_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_metadata_defaults()


async def test_modify_instance_metadata_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_metadata_options("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_metadata_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_metadata_options("test-instance_id", )


async def test_modify_instance_network_performance_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_network_performance_options("test-instance_id", "test-bandwidth_weighting", )
    mock_client.call.assert_called_once()


async def test_modify_instance_network_performance_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_network_performance_options("test-instance_id", "test-bandwidth_weighting", )


async def test_modify_instance_placement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_placement("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_instance_placement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_placement("test-instance_id", )


async def test_modify_ipam(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam("test-ipam_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam("test-ipam_id", )


async def test_modify_ipam_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_pool("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_pool("test-ipam_pool_id", )


async def test_modify_ipam_prefix_list_resolver(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", )


async def test_modify_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", )


async def test_modify_ipam_resource_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", True, )
    mock_client.call.assert_called_once()


async def test_modify_ipam_resource_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", True, )


async def test_modify_ipam_resource_discovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_resource_discovery("test-ipam_resource_discovery_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_resource_discovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_resource_discovery("test-ipam_resource_discovery_id", )


async def test_modify_ipam_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_ipam_scope("test-ipam_scope_id", )
    mock_client.call.assert_called_once()


async def test_modify_ipam_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_ipam_scope("test-ipam_scope_id", )


async def test_modify_launch_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_launch_template()
    mock_client.call.assert_called_once()


async def test_modify_launch_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_launch_template()


async def test_modify_local_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_local_gateway_route("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_modify_local_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_local_gateway_route("test-local_gateway_route_table_id", )


async def test_modify_managed_prefix_list(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_managed_prefix_list("test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_modify_managed_prefix_list_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_managed_prefix_list("test-prefix_list_id", )


async def test_modify_network_interface_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_network_interface_attribute("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_modify_network_interface_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_network_interface_attribute("test-network_interface_id", )


async def test_modify_private_dns_name_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_private_dns_name_options("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_private_dns_name_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_private_dns_name_options("test-instance_id", )


async def test_modify_public_ip_dns_name_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_public_ip_dns_name_options("test-network_interface_id", "test-hostname_type", )
    mock_client.call.assert_called_once()


async def test_modify_public_ip_dns_name_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_public_ip_dns_name_options("test-network_interface_id", "test-hostname_type", )


async def test_modify_reserved_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_reserved_instances([], [], )
    mock_client.call.assert_called_once()


async def test_modify_reserved_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_reserved_instances([], [], )


async def test_modify_route_server(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_route_server("test-route_server_id", )
    mock_client.call.assert_called_once()


async def test_modify_route_server_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_route_server("test-route_server_id", )


async def test_modify_security_group_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_security_group_rules("test-group_id", [], )
    mock_client.call.assert_called_once()


async def test_modify_security_group_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_security_group_rules("test-group_id", [], )


async def test_modify_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_snapshot_attribute("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_modify_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_snapshot_attribute("test-snapshot_id", )


async def test_modify_snapshot_tier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_snapshot_tier("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_modify_snapshot_tier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_snapshot_tier("test-snapshot_id", )


async def test_modify_spot_fleet_request(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_spot_fleet_request("test-spot_fleet_request_id", )
    mock_client.call.assert_called_once()


async def test_modify_spot_fleet_request_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_spot_fleet_request("test-spot_fleet_request_id", )


async def test_modify_subnet_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_subnet_attribute("test-subnet_id", )
    mock_client.call.assert_called_once()


async def test_modify_subnet_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_subnet_attribute("test-subnet_id", )


async def test_modify_traffic_mirror_filter_network_services(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", )
    mock_client.call.assert_called_once()


async def test_modify_traffic_mirror_filter_network_services_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", )


async def test_modify_traffic_mirror_filter_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", )
    mock_client.call.assert_called_once()


async def test_modify_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", )


async def test_modify_traffic_mirror_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_traffic_mirror_session("test-traffic_mirror_session_id", )
    mock_client.call.assert_called_once()


async def test_modify_traffic_mirror_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_traffic_mirror_session("test-traffic_mirror_session_id", )


async def test_modify_transit_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_transit_gateway("test-transit_gateway_id", )
    mock_client.call.assert_called_once()


async def test_modify_transit_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_transit_gateway("test-transit_gateway_id", )


async def test_modify_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )
    mock_client.call.assert_called_once()


async def test_modify_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", )


async def test_modify_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_modify_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )


async def test_modify_verified_access_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_endpoint("test-verified_access_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_endpoint("test-verified_access_endpoint_id", )


async def test_modify_verified_access_endpoint_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_endpoint_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", )


async def test_modify_verified_access_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_group("test-verified_access_group_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_group("test-verified_access_group_id", )


async def test_modify_verified_access_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_group_policy("test-verified_access_group_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_group_policy("test-verified_access_group_id", )


async def test_modify_verified_access_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_instance("test-verified_access_instance_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_instance("test-verified_access_instance_id", )


async def test_modify_verified_access_instance_logging_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_instance_logging_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", {}, )


async def test_modify_verified_access_trust_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_verified_access_trust_provider("test-verified_access_trust_provider_id", )
    mock_client.call.assert_called_once()


async def test_modify_verified_access_trust_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_verified_access_trust_provider("test-verified_access_trust_provider_id", )


async def test_modify_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_volume("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_modify_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_volume("test-volume_id", )


async def test_modify_volume_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_volume_attribute("test-volume_id", )
    mock_client.call.assert_called_once()


async def test_modify_volume_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_volume_attribute("test-volume_id", )


async def test_modify_vpc_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_attribute("test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_attribute("test-vpc_id", )


async def test_modify_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_block_public_access_exclusion("test-exclusion_id", "test-internet_gateway_exclusion_mode", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_block_public_access_exclusion("test-exclusion_id", "test-internet_gateway_exclusion_mode", )


async def test_modify_vpc_block_public_access_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_block_public_access_options("test-internet_gateway_block_mode", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_block_public_access_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_block_public_access_options("test-internet_gateway_block_mode", )


async def test_modify_vpc_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_endpoint("test-vpc_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_endpoint("test-vpc_endpoint_id", )


async def test_modify_vpc_endpoint_connection_notification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_endpoint_connection_notification("test-connection_notification_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_endpoint_connection_notification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_endpoint_connection_notification("test-connection_notification_id", )


async def test_modify_vpc_endpoint_service_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_endpoint_service_configuration("test-service_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_endpoint_service_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_endpoint_service_configuration("test-service_id", )


async def test_modify_vpc_endpoint_service_payer_responsibility(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_endpoint_service_payer_responsibility("test-service_id", "test-payer_responsibility", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_endpoint_service_payer_responsibility_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_endpoint_service_payer_responsibility("test-service_id", "test-payer_responsibility", )


async def test_modify_vpc_endpoint_service_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_endpoint_service_permissions("test-service_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_endpoint_service_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_endpoint_service_permissions("test-service_id", )


async def test_modify_vpc_peering_connection_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_peering_connection_options("test-vpc_peering_connection_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_peering_connection_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_peering_connection_options("test-vpc_peering_connection_id", )


async def test_modify_vpc_tenancy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpc_tenancy("test-vpc_id", "test-instance_tenancy", )
    mock_client.call.assert_called_once()


async def test_modify_vpc_tenancy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpc_tenancy("test-vpc_id", "test-instance_tenancy", )


async def test_modify_vpn_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpn_connection("test-vpn_connection_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpn_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpn_connection("test-vpn_connection_id", )


async def test_modify_vpn_connection_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpn_connection_options("test-vpn_connection_id", )
    mock_client.call.assert_called_once()


async def test_modify_vpn_connection_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpn_connection_options("test-vpn_connection_id", )


async def test_modify_vpn_tunnel_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpn_tunnel_certificate("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )
    mock_client.call.assert_called_once()


async def test_modify_vpn_tunnel_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpn_tunnel_certificate("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )


async def test_modify_vpn_tunnel_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, )
    mock_client.call.assert_called_once()


async def test_modify_vpn_tunnel_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, )


async def test_monitor_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await monitor_instances([], )
    mock_client.call.assert_called_once()


async def test_monitor_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await monitor_instances([], )


async def test_move_address_to_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await move_address_to_vpc("test-public_ip", )
    mock_client.call.assert_called_once()


async def test_move_address_to_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await move_address_to_vpc("test-public_ip", )


async def test_move_byoip_cidr_to_ipam(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await move_byoip_cidr_to_ipam("test-cidr", "test-ipam_pool_id", "test-ipam_pool_owner", )
    mock_client.call.assert_called_once()


async def test_move_byoip_cidr_to_ipam_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await move_byoip_cidr_to_ipam("test-cidr", "test-ipam_pool_id", "test-ipam_pool_owner", )


async def test_move_capacity_reservation_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, )
    mock_client.call.assert_called_once()


async def test_move_capacity_reservation_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, )


async def test_provision_byoip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await provision_byoip_cidr("test-cidr", )
    mock_client.call.assert_called_once()


async def test_provision_byoip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await provision_byoip_cidr("test-cidr", )


async def test_provision_ipam_byoasn(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await provision_ipam_byoasn("test-ipam_id", "test-asn", {}, )
    mock_client.call.assert_called_once()


async def test_provision_ipam_byoasn_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await provision_ipam_byoasn("test-ipam_id", "test-asn", {}, )


async def test_provision_ipam_pool_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await provision_ipam_pool_cidr("test-ipam_pool_id", )
    mock_client.call.assert_called_once()


async def test_provision_ipam_pool_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await provision_ipam_pool_cidr("test-ipam_pool_id", )


async def test_provision_public_ipv4_pool_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", 1, )
    mock_client.call.assert_called_once()


async def test_provision_public_ipv4_pool_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", 1, )


async def test_purchase_capacity_block(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", )
    mock_client.call.assert_called_once()


async def test_purchase_capacity_block_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", )


async def test_purchase_capacity_block_extension(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_capacity_block_extension("test-capacity_block_extension_offering_id", "test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_purchase_capacity_block_extension_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_capacity_block_extension("test-capacity_block_extension_offering_id", "test-capacity_reservation_id", )


async def test_purchase_host_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_host_reservation([], "test-offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_host_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_host_reservation([], "test-offering_id", )


async def test_purchase_reserved_instances_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_reserved_instances_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", )


async def test_purchase_scheduled_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_scheduled_instances([], )
    mock_client.call.assert_called_once()


async def test_purchase_scheduled_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_scheduled_instances([], )


async def test_register_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_image("test-name", )
    mock_client.call.assert_called_once()


async def test_register_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_image("test-name", )


async def test_register_instance_event_notification_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_instance_event_notification_attributes({}, )
    mock_client.call.assert_called_once()


async def test_register_instance_event_notification_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_instance_event_notification_attributes({}, )


async def test_register_transit_gateway_multicast_group_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", [], )
    mock_client.call.assert_called_once()


async def test_register_transit_gateway_multicast_group_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", [], )


async def test_register_transit_gateway_multicast_group_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", [], )
    mock_client.call.assert_called_once()


async def test_register_transit_gateway_multicast_group_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", [], )


async def test_reject_capacity_reservation_billing_ownership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_capacity_reservation_billing_ownership("test-capacity_reservation_id", )
    mock_client.call.assert_called_once()


async def test_reject_capacity_reservation_billing_ownership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_capacity_reservation_billing_ownership("test-capacity_reservation_id", )


async def test_reject_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_transit_gateway_multicast_domain_associations()
    mock_client.call.assert_called_once()


async def test_reject_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_transit_gateway_multicast_domain_associations()


async def test_reject_transit_gateway_peering_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_reject_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", )


async def test_reject_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )
    mock_client.call.assert_called_once()


async def test_reject_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", )


async def test_reject_vpc_endpoint_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_vpc_endpoint_connections("test-service_id", [], )
    mock_client.call.assert_called_once()


async def test_reject_vpc_endpoint_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_vpc_endpoint_connections("test-service_id", [], )


async def test_reject_vpc_peering_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_vpc_peering_connection("test-vpc_peering_connection_id", )
    mock_client.call.assert_called_once()


async def test_reject_vpc_peering_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_vpc_peering_connection("test-vpc_peering_connection_id", )


async def test_release_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await release_address()
    mock_client.call.assert_called_once()


async def test_release_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await release_address()


async def test_release_hosts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await release_hosts([], )
    mock_client.call.assert_called_once()


async def test_release_hosts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await release_hosts([], )


async def test_release_ipam_pool_allocation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await release_ipam_pool_allocation("test-ipam_pool_id", "test-cidr", "test-ipam_pool_allocation_id", )
    mock_client.call.assert_called_once()


async def test_release_ipam_pool_allocation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await release_ipam_pool_allocation("test-ipam_pool_id", "test-cidr", "test-ipam_pool_allocation_id", )


async def test_replace_iam_instance_profile_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_iam_instance_profile_association({}, "test-association_id", )
    mock_client.call.assert_called_once()


async def test_replace_iam_instance_profile_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_iam_instance_profile_association({}, "test-association_id", )


async def test_replace_image_criteria_in_allowed_images_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_image_criteria_in_allowed_images_settings()
    mock_client.call.assert_called_once()


async def test_replace_image_criteria_in_allowed_images_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_image_criteria_in_allowed_images_settings()


async def test_replace_network_acl_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_network_acl_association("test-association_id", "test-network_acl_id", )
    mock_client.call.assert_called_once()


async def test_replace_network_acl_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_network_acl_association("test-association_id", "test-network_acl_id", )


async def test_replace_network_acl_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, )
    mock_client.call.assert_called_once()


async def test_replace_network_acl_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, )


async def test_replace_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_route("test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_replace_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_route("test-route_table_id", )


async def test_replace_route_table_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_route_table_association("test-association_id", "test-route_table_id", )
    mock_client.call.assert_called_once()


async def test_replace_route_table_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_route_table_association("test-association_id", "test-route_table_id", )


async def test_replace_transit_gateway_route(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_replace_transit_gateway_route_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", )


async def test_replace_vpn_tunnel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )
    mock_client.call.assert_called_once()


async def test_replace_vpn_tunnel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", )


async def test_report_instance_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await report_instance_status([], "test-status", [], )
    mock_client.call.assert_called_once()


async def test_report_instance_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await report_instance_status([], "test-status", [], )


async def test_request_spot_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await request_spot_fleet({}, )
    mock_client.call.assert_called_once()


async def test_request_spot_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await request_spot_fleet({}, )


async def test_request_spot_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await request_spot_instances()
    mock_client.call.assert_called_once()


async def test_request_spot_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await request_spot_instances()


async def test_reset_address_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_address_attribute("test-allocation_id", "test-attribute", )
    mock_client.call.assert_called_once()


async def test_reset_address_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_address_attribute("test-allocation_id", "test-attribute", )


async def test_reset_ebs_default_kms_key_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_ebs_default_kms_key_id()
    mock_client.call.assert_called_once()


async def test_reset_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_ebs_default_kms_key_id()


async def test_reset_fpga_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_fpga_image_attribute("test-fpga_image_id", )
    mock_client.call.assert_called_once()


async def test_reset_fpga_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_fpga_image_attribute("test-fpga_image_id", )


async def test_reset_image_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_image_attribute("test-attribute", "test-image_id", )
    mock_client.call.assert_called_once()


async def test_reset_image_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_image_attribute("test-attribute", "test-image_id", )


async def test_reset_instance_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_instance_attribute("test-instance_id", "test-attribute", )
    mock_client.call.assert_called_once()


async def test_reset_instance_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_instance_attribute("test-instance_id", "test-attribute", )


async def test_reset_network_interface_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_network_interface_attribute("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_reset_network_interface_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_network_interface_attribute("test-network_interface_id", )


async def test_reset_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_snapshot_attribute("test-attribute", "test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_reset_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_snapshot_attribute("test-attribute", "test-snapshot_id", )


async def test_restore_address_to_classic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_address_to_classic("test-public_ip", )
    mock_client.call.assert_called_once()


async def test_restore_address_to_classic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_address_to_classic("test-public_ip", )


async def test_restore_image_from_recycle_bin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_image_from_recycle_bin("test-image_id", )
    mock_client.call.assert_called_once()


async def test_restore_image_from_recycle_bin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_image_from_recycle_bin("test-image_id", )


async def test_restore_managed_prefix_list_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_managed_prefix_list_version("test-prefix_list_id", 1, 1, )
    mock_client.call.assert_called_once()


async def test_restore_managed_prefix_list_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_managed_prefix_list_version("test-prefix_list_id", 1, 1, )


async def test_restore_snapshot_from_recycle_bin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_snapshot_from_recycle_bin("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_restore_snapshot_from_recycle_bin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_snapshot_from_recycle_bin("test-snapshot_id", )


async def test_restore_snapshot_tier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_snapshot_tier("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_restore_snapshot_tier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_snapshot_tier("test-snapshot_id", )


async def test_revoke_client_vpn_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", )
    mock_client.call.assert_called_once()


async def test_revoke_client_vpn_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", )


async def test_revoke_security_group_egress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_security_group_egress("test-group_id", )
    mock_client.call.assert_called_once()


async def test_revoke_security_group_egress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_security_group_egress("test-group_id", )


async def test_revoke_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_security_group_ingress()
    mock_client.call.assert_called_once()


async def test_revoke_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_security_group_ingress()


async def test_run_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_instances(1, 1, )
    mock_client.call.assert_called_once()


async def test_run_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_instances(1, 1, )


async def test_run_scheduled_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_scheduled_instances({}, "test-scheduled_instance_id", )
    mock_client.call.assert_called_once()


async def test_run_scheduled_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_scheduled_instances({}, "test-scheduled_instance_id", )


async def test_search_local_gateway_routes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_local_gateway_routes("test-local_gateway_route_table_id", )
    mock_client.call.assert_called_once()


async def test_search_local_gateway_routes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_local_gateway_routes("test-local_gateway_route_table_id", )


async def test_search_transit_gateway_multicast_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", )
    mock_client.call.assert_called_once()


async def test_search_transit_gateway_multicast_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", )


async def test_search_transit_gateway_routes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_transit_gateway_routes("test-transit_gateway_route_table_id", [], )
    mock_client.call.assert_called_once()


async def test_search_transit_gateway_routes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_transit_gateway_routes("test-transit_gateway_route_table_id", [], )


async def test_send_diagnostic_interrupt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_diagnostic_interrupt("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_send_diagnostic_interrupt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_diagnostic_interrupt("test-instance_id", )


async def test_start_declarative_policies_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_declarative_policies_report("test-s3_bucket", "test-target_id", )
    mock_client.call.assert_called_once()


async def test_start_declarative_policies_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_declarative_policies_report("test-s3_bucket", "test-target_id", )


async def test_start_network_insights_access_scope_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_start_network_insights_access_scope_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", )


async def test_start_network_insights_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_network_insights_analysis("test-network_insights_path_id", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_start_network_insights_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_network_insights_analysis("test-network_insights_path_id", "test-client_token", )


async def test_start_vpc_endpoint_service_private_dns_verification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_vpc_endpoint_service_private_dns_verification("test-service_id", )
    mock_client.call.assert_called_once()


async def test_start_vpc_endpoint_service_private_dns_verification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_vpc_endpoint_service_private_dns_verification("test-service_id", )


async def test_terminate_client_vpn_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await terminate_client_vpn_connections("test-client_vpn_endpoint_id", )
    mock_client.call.assert_called_once()


async def test_terminate_client_vpn_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await terminate_client_vpn_connections("test-client_vpn_endpoint_id", )


async def test_unassign_ipv6_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await unassign_ipv6_addresses("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_unassign_ipv6_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unassign_ipv6_addresses("test-network_interface_id", )


async def test_unassign_private_ip_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await unassign_private_ip_addresses("test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_unassign_private_ip_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unassign_private_ip_addresses("test-network_interface_id", )


async def test_unassign_private_nat_gateway_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await unassign_private_nat_gateway_address("test-nat_gateway_id", [], )
    mock_client.call.assert_called_once()


async def test_unassign_private_nat_gateway_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unassign_private_nat_gateway_address("test-nat_gateway_id", [], )


async def test_unlock_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await unlock_snapshot("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_unlock_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unlock_snapshot("test-snapshot_id", )


async def test_unmonitor_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await unmonitor_instances([], )
    mock_client.call.assert_called_once()


async def test_unmonitor_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unmonitor_instances([], )


async def test_update_capacity_manager_organizations_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_capacity_manager_organizations_access(True, )
    mock_client.call.assert_called_once()


async def test_update_capacity_manager_organizations_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_capacity_manager_organizations_access(True, )


async def test_update_security_group_rule_descriptions_egress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_security_group_rule_descriptions_egress()
    mock_client.call.assert_called_once()


async def test_update_security_group_rule_descriptions_egress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_group_rule_descriptions_egress()


async def test_update_security_group_rule_descriptions_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_security_group_rule_descriptions_ingress()
    mock_client.call.assert_called_once()


async def test_update_security_group_rule_descriptions_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_group_rule_descriptions_ingress()


async def test_withdraw_byoip_cidr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    await withdraw_byoip_cidr("test-cidr", )
    mock_client.call.assert_called_once()


async def test_withdraw_byoip_cidr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ec2.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await withdraw_byoip_cidr("test-cidr", )


@pytest.mark.asyncio
async def test_accept_address_transfer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import accept_address_transfer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await accept_address_transfer("test-address", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_accept_reserved_instances_exchange_quote_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import accept_reserved_instances_exchange_quote
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await accept_reserved_instances_exchange_quote("test-reserved_instance_ids", target_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_accept_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import accept_transit_gateway_multicast_domain_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await accept_transit_gateway_multicast_domain_associations(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_advertise_byoip_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import advertise_byoip_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await advertise_byoip_cidr("test-cidr", asn="test-asn", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_allocate_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import allocate_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await allocate_address(domain="test-domain", address="test-address", public_ipv4_pool="test-public_ipv4_pool", network_border_group="test-network_border_group", customer_owned_ipv4_pool="test-customer_owned_ipv4_pool", tag_specifications={}, ipam_pool_id="test-ipam_pool_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_allocate_hosts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import allocate_hosts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await allocate_hosts(instance_family="test-instance_family", tag_specifications={}, host_recovery="test-host_recovery", outpost_arn="test-outpost_arn", host_maintenance="test-host_maintenance", asset_ids="test-asset_ids", availability_zone_id="test-availability_zone_id", auto_placement=True, client_token="test-client_token", instance_type="test-instance_type", quantity="test-quantity", availability_zone="test-availability_zone", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_allocate_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import allocate_ipam_pool_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await allocate_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", netmask_length="test-netmask_length", client_token="test-client_token", description="test-description", preview_next_cidr="test-preview_next_cidr", allowed_cidrs=True, disallowed_cidrs="test-disallowed_cidrs", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_assign_ipv6_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import assign_ipv6_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await assign_ipv6_addresses("test-network_interface_id", ipv6_prefix_count=1, ipv6_prefixes="test-ipv6_prefixes", ipv6_addresses="test-ipv6_addresses", ipv6_address_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_assign_private_ip_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import assign_private_ip_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await assign_private_ip_addresses("test-network_interface_id", ipv4_prefixes="test-ipv4_prefixes", ipv4_prefix_count=1, private_ip_addresses="test-private_ip_addresses", secondary_private_ip_address_count=1, allow_reassignment=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_assign_private_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import assign_private_nat_gateway_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await assign_private_nat_gateway_address("test-nat_gateway_id", private_ip_addresses="test-private_ip_addresses", private_ip_address_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_address(allocation_id="test-allocation_id", instance_id="test-instance_id", public_ip="test-public_ip", network_interface_id="test-network_interface_id", private_ip_address="test-private_ip_address", allow_reassociation=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_client_vpn_target_network_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_client_vpn_target_network
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_ipam_resource_discovery
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_nat_gateway_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_nat_gateway_address("test-nat_gateway_id", "test-allocation_ids", private_ip_addresses="test-private_ip_addresses", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_route_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_route_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_route_table("test-route_table_id", gateway_id="test-gateway_id", public_ipv4_pool="test-public_ipv4_pool", subnet_id="test-subnet_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_subnet_cidr_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_subnet_cidr_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_subnet_cidr_block("test-subnet_id", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", ipv6_cidr_block="test-ipv6_cidr_block", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_trunk_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_trunk_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", vlan_id="test-vlan_id", gre_key="test-gre_key", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_vpc_cidr_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import associate_vpc_cidr_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await associate_vpc_cidr_block("test-vpc_id", cidr_block="test-cidr_block", ipv6_cidr_block_network_border_group="test-ipv6_cidr_block_network_border_group", ipv6_pool="test-ipv6_pool", ipv6_cidr_block="test-ipv6_cidr_block", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", amazon_provided_ipv6_cidr_block="test-amazon_provided_ipv6_cidr_block", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_network_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import attach_network_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await attach_network_interface("test-network_interface_id", "test-instance_id", "test-device_index", network_card_index="test-network_card_index", ena_srd_specification={}, ena_queue_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import attach_verified_access_trust_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_client_vpn_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import authorize_client_vpn_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", access_group_id="test-access_group_id", authorize_all_groups="test-authorize_all_groups", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_security_group_egress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import authorize_security_group_egress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await authorize_security_group_egress("test-group_id", tag_specifications={}, source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", ip_protocol="test-ip_protocol", from_port=1, to_port=1, cidr_ip="test-cidr_ip", ip_permissions="test-ip_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import authorize_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await authorize_security_group_ingress(cidr_ip="test-cidr_ip", from_port=1, group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", ip_protocol="test-ip_protocol", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", to_port=1, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_conversion_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import cancel_conversion_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await cancel_conversion_task("test-conversion_task_id", reason_message="test-reason_message", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_import_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import cancel_import_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await cancel_import_task(cancel_reason="test-cancel_reason", import_task_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_fpga_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import copy_fpga_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await copy_fpga_image("test-source_fpga_image_id", "test-source_region", description="test-description", name="test-name", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import copy_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await copy_image("test-name", "test-source_image_id", "test-source_region", client_token="test-client_token", description="test-description", encrypted=True, kms_key_id="test-kms_key_id", destination_outpost_arn="test-destination_outpost_arn", copy_image_tags=[{"Key": "k", "Value": "v"}], tag_specifications={}, snapshot_copy_completion_duration_minutes=1, destination_availability_zone="test-destination_availability_zone", destination_availability_zone_id="test-destination_availability_zone_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import copy_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await copy_snapshot("test-source_region", "test-source_snapshot_id", description="test-description", destination_outpost_arn="test-destination_outpost_arn", destination_region="test-destination_region", encrypted=True, kms_key_id="test-kms_key_id", presigned_url="test-presigned_url", tag_specifications={}, completion_duration_minutes=1, destination_availability_zone="test-destination_availability_zone", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_volumes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import copy_volumes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await copy_volumes("test-source_volume_id", iops="test-iops", size=1, volume_type="test-volume_type", tag_specifications={}, multi_attach_enabled=True, throughput="test-throughput", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_capacity_manager_data_export_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_capacity_manager_data_export
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", s3_bucket_prefix="test-s3_bucket_prefix", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_capacity_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_capacity_reservation("test-instance_type", "test-instance_platform", 1, client_token="test-client_token", availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", tenancy="test-tenancy", ebs_optimized="test-ebs_optimized", ephemeral_storage="test-ephemeral_storage", end_date="test-end_date", end_date_type="test-end_date_type", instance_match_criteria="test-instance_match_criteria", tag_specifications={}, outpost_arn="test-outpost_arn", placement_group_arn="test-placement_group_arn", start_date="test-start_date", commitment_duration=1, delivery_preference="test-delivery_preference", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_capacity_reservation_by_splitting_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_capacity_reservation_by_splitting
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_capacity_reservation_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_capacity_reservation_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_capacity_reservation_fleet({}, "test-total_target_capacity", allocation_strategy="test-allocation_strategy", client_token="test-client_token", tenancy="test-tenancy", end_date="test-end_date", instance_match_criteria="test-instance_match_criteria", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_carrier_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_carrier_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_carrier_gateway("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_client_vpn_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_client_vpn_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_client_vpn_endpoint("test-server_certificate_arn", {}, {}, client_cidr_block="test-client_cidr_block", dns_servers="test-dns_servers", transport_protocol=1, vpn_port=1, description="test-description", split_tunnel="test-split_tunnel", client_token="test-client_token", tag_specifications={}, security_group_ids="test-security_group_ids", vpc_id="test-vpc_id", self_service_portal=1, client_connect_options={}, session_timeout_hours=1, client_login_banner_options={}, client_route_enforcement_options={}, disconnect_on_session_timeout=1, endpoint_ip_address_type="test-endpoint_ip_address_type", traffic_ip_address_type="test-traffic_ip_address_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_client_vpn_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_client_vpn_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_coip_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_coip_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_coip_pool("test-local_gateway_route_table_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_customer_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_customer_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_customer_gateway("test-type_value", bgp_asn="test-bgp_asn", public_ip="test-public_ip", certificate_arn="test-certificate_arn", tag_specifications={}, device_name="test-device_name", ip_address="test-ip_address", bgp_asn_extended="test-bgp_asn_extended", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_default_subnet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_default_subnet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_default_subnet(availability_zone="test-availability_zone", ipv6_native="test-ipv6_native", availability_zone_id="test-availability_zone_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_delegate_mac_volume_ownership_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_delegate_mac_volume_ownership_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dhcp_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_dhcp_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_dhcp_options({}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_egress_only_internet_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_egress_only_internet_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_egress_only_internet_gateway("test-vpc_id", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_fleet({}, {}, client_token="test-client_token", spot_options={}, on_demand_options={}, excess_capacity_termination_policy="{}", terminate_instances_with_expiration="test-terminate_instances_with_expiration", type_value="test-type_value", valid_from="test-valid_from", valid_until="test-valid_until", replace_unhealthy_instances="test-replace_unhealthy_instances", tag_specifications={}, context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_flow_logs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_flow_logs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_flow_logs("test-resource_ids", "test-resource_type", client_token="test-client_token", deliver_logs_permission_arn="test-deliver_logs_permission_arn", deliver_cross_account_role=1, log_group_name="test-log_group_name", traffic_type="test-traffic_type", log_destination_type="test-log_destination_type", log_destination="test-log_destination", log_format="test-log_format", tag_specifications={}, max_aggregation_interval=1, destination_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_fpga_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_fpga_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_fpga_image("test-input_storage_location", logs_storage_location="test-logs_storage_location", description="test-description", name="test-name", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_image_usage_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_image_usage_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_image_usage_report("test-image_id", "test-resource_types", account_ids=1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instance_connect_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_instance_connect_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_instance_connect_endpoint("test-subnet_id", security_group_ids="test-security_group_ids", preserve_client_ip="test-preserve_client_ip", client_token="test-client_token", tag_specifications={}, ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instance_event_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_instance_event_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_instance_event_window(name="test-name", time_ranges="test-time_ranges", cron_expression="test-cron_expression", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instance_export_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_instance_export_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_instance_export_task("test-instance_id", "test-target_environment", 1, tag_specifications={}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_internet_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_internet_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_internet_gateway(tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam(description="test-description", operating_regions="test-operating_regions", tag_specifications={}, client_token="test-client_token", tier="test-tier", enable_private_gua=True, metered_account=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_external_resource_verification_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_external_resource_verification_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_external_resource_verification_token("test-ipam_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_pool("test-ipam_scope_id", "test-address_family", locale="test-locale", source_ipam_pool_id="test-source_ipam_pool_id", description="test-description", auto_import=True, publicly_advertisable="test-publicly_advertisable", allocation_min_netmask_length="test-allocation_min_netmask_length", allocation_max_netmask_length=1, allocation_default_netmask_length="test-allocation_default_netmask_length", allocation_resource_tags=[{"Key": "k", "Value": "v"}], tag_specifications={}, client_token="test-client_token", aws_service="test-aws_service", public_ip_source="test-public_ip_source", source_resource="test-source_resource", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_prefix_list_resolver_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_prefix_list_resolver
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", description="test-description", rules="test-rules", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_prefix_list_resolver_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_prefix_list_resolver_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", "test-track_latest_version", desired_version="test-desired_version", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_resource_discovery
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_resource_discovery(description="test-description", operating_regions="test-operating_regions", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ipam_scope_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_ipam_scope
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_ipam_scope("test-ipam_id", description="test-description", tag_specifications={}, client_token="test-client_token", external_authority_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_key_pair("test-key_name", key_type="test-key_type", tag_specifications={}, key_format="test-key_format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_launch_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_launch_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_launch_template("test-launch_template_name", "test-launch_template_data", client_token="test-client_token", version_description="test-version_description", operator="test-operator", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_launch_template_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_launch_template_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_launch_template_version("test-launch_template_data", client_token="test-client_token", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", source_version="test-source_version", version_description="test-version_description", resolve_alias="test-resolve_alias", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", local_gateway_virtual_interface_group_id="test-local_gateway_virtual_interface_group_id", network_interface_id="test-network_interface_id", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_route_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_route_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_route_table("test-local_gateway_id", mode="test-mode", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_route_table_virtual_interface_group_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_route_table_virtual_interface_group_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_route_table_vpc_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_route_table_vpc_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_virtual_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_virtual_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", "test-vlan", "test-local_address", "test-peer_address", peer_bgp_asn="test-peer_bgp_asn", tag_specifications={}, peer_bgp_asn_extended="test-peer_bgp_asn_extended", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_local_gateway_virtual_interface_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_local_gateway_virtual_interface_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_local_gateway_virtual_interface_group("test-local_gateway_id", local_bgp_asn="test-local_bgp_asn", local_bgp_asn_extended="test-local_bgp_asn_extended", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_mac_system_integrity_protection_modification_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_mac_system_integrity_protection_modification_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", client_token="test-client_token", mac_credentials="test-mac_credentials", mac_system_integrity_protection_configuration={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_managed_prefix_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_managed_prefix_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", entries="test-entries", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_nat_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_nat_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_nat_gateway("test-subnet_id", allocation_id="test-allocation_id", client_token="test-client_token", tag_specifications={}, connectivity_type="test-connectivity_type", private_ip_address="test-private_ip_address", secondary_allocation_ids="test-secondary_allocation_ids", secondary_private_ip_addresses="test-secondary_private_ip_addresses", secondary_private_ip_address_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_acl_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_acl
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_acl("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_acl_entry_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_acl_entry
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_acl_entry("test-network_acl_id", "test-rule_number", "test-protocol", "test-rule_action", "test-egress", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", icmp_type_code="test-icmp_type_code", port_range=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_insights_access_scope_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_insights_access_scope
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_insights_access_scope("test-client_token", match_paths="test-match_paths", exclude_paths="test-exclude_paths", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_insights_path_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_insights_path
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_insights_path("test-source", "test-protocol", "test-client_token", source_ip="test-source_ip", destination_ip="test-destination_ip", destination="test-destination", destination_port=1, tag_specifications={}, filter_at_source="test-filter_at_source", filter_at_destination="test-filter_at_destination", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_interface("test-subnet_id", ipv4_prefixes="test-ipv4_prefixes", ipv4_prefix_count=1, ipv6_prefixes="test-ipv6_prefixes", ipv6_prefix_count=1, interface_type="test-interface_type", tag_specifications={}, client_token="test-client_token", enable_primary_ipv6=True, connection_tracking_specification={}, operator="test-operator", description="test-description", private_ip_address="test-private_ip_address", groups="test-groups", private_ip_addresses="test-private_ip_addresses", secondary_private_ip_address_count=1, ipv6_addresses="test-ipv6_addresses", ipv6_address_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_network_interface_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_network_interface_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_network_interface_permission("test-network_interface_id", "test-permission", aws_account_id=1, aws_service="test-aws_service", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_placement_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_placement_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_placement_group(partition_count=1, tag_specifications={}, spread_level="test-spread_level", group_name="test-group_name", strategy="test-strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_public_ipv4_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_public_ipv4_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_public_ipv4_pool(tag_specifications={}, network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_replace_root_volume_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_replace_root_volume_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_replace_root_volume_task("test-instance_id", snapshot_id="test-snapshot_id", client_token="test-client_token", tag_specifications={}, image_id="test-image_id", delete_replaced_root_volume=True, volume_initialization_rate="test-volume_initialization_rate", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_restore_image_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_restore_image_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_restore_image_task("test-bucket", "test-object_key", name="test-name", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", vpc_endpoint_id="test-vpc_endpoint_id", transit_gateway_id="test-transit_gateway_id", local_gateway_id="test-local_gateway_id", carrier_gateway_id="test-carrier_gateway_id", core_network_arn="test-core_network_arn", odb_network_arn="test-odb_network_arn", destination_cidr_block="test-destination_cidr_block", gateway_id="test-gateway_id", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", egress_only_internet_gateway_id="test-egress_only_internet_gateway_id", instance_id="test-instance_id", network_interface_id="test-network_interface_id", vpc_peering_connection_id="test-vpc_peering_connection_id", nat_gateway_id="test-nat_gateway_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_route_server_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_route_server
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_route_server("test-amazon_side_asn", client_token="test-client_token", persist_routes="test-persist_routes", persist_routes_duration=1, sns_notifications_enabled="test-sns_notifications_enabled", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_route_server_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_route_server_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_route_server_endpoint("test-route_server_id", "test-subnet_id", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_route_server_peer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_route_server_peer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_route_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_route_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_route_table("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_security_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_security_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_security_group("test-description", "test-group_name", vpc_id="test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_snapshot("test-volume_id", description="test-description", outpost_arn="test-outpost_arn", tag_specifications={}, location="test-location", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_snapshots({}, description="test-description", outpost_arn="test-outpost_arn", tag_specifications={}, copy_tags_from_source=[{"Key": "k", "Value": "v"}], location="test-location", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_spot_datafeed_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_spot_datafeed_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_spot_datafeed_subscription("test-bucket", prefix="test-prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_store_image_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_store_image_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_store_image_task("test-image_id", "test-bucket", s3_object_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_subnet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_subnet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_subnet("test-vpc_id", tag_specifications={}, availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", outpost_arn="test-outpost_arn", ipv6_native="test-ipv6_native", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_subnet_cidr_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_subnet_cidr_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", description="test-description", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_mirror_filter_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_traffic_mirror_filter
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_traffic_mirror_filter(description="test-description", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_mirror_filter_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_traffic_mirror_filter_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", "test-rule_number", "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", destination_port_range=1, source_port_range=1, protocol="test-protocol", description="test-description", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_mirror_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_traffic_mirror_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", "test-session_number", packet_length="test-packet_length", virtual_network_id="test-virtual_network_id", description="test-description", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_mirror_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_traffic_mirror_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_traffic_mirror_target(network_interface_id="test-network_interface_id", network_load_balancer_arn="test-network_load_balancer_arn", description="test-description", tag_specifications={}, client_token="test-client_token", gateway_load_balancer_endpoint_id="test-gateway_load_balancer_endpoint_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway(description="test-description", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_connect_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_connect
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_connect(1, {}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_connect_peer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_connect_peer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", "test-inside_cidr_blocks", transit_gateway_address="test-transit_gateway_address", bgp_options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_multicast_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_multicast_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_multicast_domain("test-transit_gateway_id", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_peering_attachment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_peering_attachment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", 1, "test-peer_region", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_policy_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_policy_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_policy_table("test-transit_gateway_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_prefix_list_reference_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_prefix_list_reference
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_route_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_route_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_route_table("test-transit_gateway_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_route_table_announcement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_route_table_announcement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_transit_gateway_vpc_attachment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_transit_gateway_vpc_attachment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", "test-subnet_ids", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_verified_access_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", domain_certificate_arn="test-domain_certificate_arn", application_domain="test-application_domain", endpoint_domain_prefix="test-endpoint_domain_prefix", security_group_ids="test-security_group_ids", load_balancer_options={}, network_interface_options={}, description="test-description", policy_document="test-policy_document", tag_specifications={}, client_token="test-client_token", sse_specification={}, rds_options={}, cidr_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_verified_access_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_verified_access_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_verified_access_group("test-verified_access_instance_id", description="test-description", policy_document="test-policy_document", tag_specifications={}, client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_verified_access_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_verified_access_instance(description="test-description", tag_specifications={}, client_token="test-client_token", fips_enabled="test-fips_enabled", cidr_endpoints_custom_sub_domain="test-cidr_endpoints_custom_sub_domain", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_verified_access_trust_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", user_trust_provider_type="test-user_trust_provider_type", device_trust_provider_type="test-device_trust_provider_type", oidc_options={}, device_options={}, description="test-description", tag_specifications={}, client_token="test-client_token", sse_specification={}, native_application_oidc_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_volume(availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", encrypted=True, iops="test-iops", kms_key_id="test-kms_key_id", outpost_arn="test-outpost_arn", size=1, snapshot_id="test-snapshot_id", volume_type="test-volume_type", tag_specifications={}, multi_attach_enabled=True, throughput="test-throughput", client_token="test-client_token", volume_initialization_rate="test-volume_initialization_rate", operator="test-operator", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc(cidr_block="test-cidr_block", ipv6_pool="test-ipv6_pool", ipv6_cidr_block="test-ipv6_cidr_block", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", ipv6_cidr_block_network_border_group="test-ipv6_cidr_block_network_border_group", tag_specifications={}, instance_tenancy="test-instance_tenancy", amazon_provided_ipv6_cidr_block="test-amazon_provided_ipv6_cidr_block", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_block_public_access_exclusion_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc_block_public_access_exclusion
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", subnet_id="test-subnet_id", vpc_id="test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc_endpoint("test-vpc_id", vpc_endpoint_type="test-vpc_endpoint_type", service_name="test-service_name", policy_document="test-policy_document", route_table_ids="test-route_table_ids", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", ip_address_type="test-ip_address_type", dns_options={}, client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", tag_specifications={}, subnet_configurations={}, service_network_arn="test-service_network_arn", resource_configuration_arn={}, service_region="test-service_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_endpoint_connection_notification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc_endpoint_connection_notification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc_endpoint_connection_notification("test-connection_notification_arn", "test-connection_events", service_id="test-service_id", vpc_endpoint_id="test-vpc_endpoint_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_endpoint_service_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc_endpoint_service_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc_endpoint_service_configuration(acceptance_required="test-acceptance_required", private_dns_name="test-private_dns_name", network_load_balancer_arns="test-network_load_balancer_arns", gateway_load_balancer_arns="test-gateway_load_balancer_arns", supported_ip_address_types=1, supported_regions=1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_peering_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpc_peering_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpc_peering_connection("test-vpc_id", peer_region="test-peer_region", tag_specifications={}, peer_vpc_id="test-peer_vpc_id", peer_owner_id="test-peer_owner_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpn_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpn_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpn_connection("test-customer_gateway_id", "test-type_value", vpn_gateway_id="test-vpn_gateway_id", transit_gateway_id="test-transit_gateway_id", tag_specifications={}, pre_shared_key_storage="test-pre_shared_key_storage", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpn_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import create_vpn_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await create_vpn_gateway("test-type_value", availability_zone="test-availability_zone", tag_specifications={}, amazon_side_asn="test-amazon_side_asn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_client_vpn_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_client_vpn_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", target_vpc_subnet_id="test-target_vpc_subnet_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_instance_event_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_instance_event_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_instance_event_window("test-instance_event_window_id", force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_ipam_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_ipam
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_ipam("test-ipam_id", cascade="test-cascade", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_ipam_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_ipam_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_ipam_pool("test-ipam_pool_id", cascade="test-cascade", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_key_pair(key_name="test-key_name", key_pair_id="test-key_pair_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_launch_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_launch_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_launch_template(launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_launch_template_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_launch_template_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_launch_template_versions("test-versions", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_local_gateway_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_network_interface_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_network_interface_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_network_interface_permission("test-network_interface_permission_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_public_ipv4_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_public_ipv4_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_public_ipv4_pool("test-pool_id", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", destination_cidr_block="test-destination_cidr_block", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_security_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_security_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_security_group(group_id="test-group_id", group_name="test-group_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_tags("test-resources", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_verified_access_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_verified_access_endpoint("test-verified_access_endpoint_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_verified_access_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_verified_access_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_verified_access_group("test-verified_access_group_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_verified_access_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_verified_access_instance("test-verified_access_instance_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import delete_verified_access_trust_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await delete_verified_access_trust_provider("test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deprovision_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import deprovision_ipam_pool_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await deprovision_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import deregister_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await deregister_image("test-image_id", delete_associated_snapshots=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_transit_gateway_multicast_group_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import deregister_transit_gateway_multicast_group_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await deregister_transit_gateway_multicast_group_members(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", group_ip_address="test-group_ip_address", network_interface_ids="test-network_interface_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_transit_gateway_multicast_group_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import deregister_transit_gateway_multicast_group_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await deregister_transit_gateway_multicast_group_sources(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", group_ip_address="test-group_ip_address", network_interface_ids="test-network_interface_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_account_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_account_attributes(attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_address_transfers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_address_transfers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_address_transfers(allocation_ids="test-allocation_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_addresses(public_ips="test-public_ips", filters=[{}], allocation_ids="test-allocation_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_addresses_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_addresses_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_addresses_attribute(allocation_ids="test-allocation_ids", attribute="test-attribute", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_availability_zones_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_availability_zones
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_availability_zones(zone_names="test-zone_names", zone_ids="test-zone_ids", all_availability_zones="test-all_availability_zones", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_aws_network_performance_metric_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_aws_network_performance_metric_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_aws_network_performance_metric_subscriptions(max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_bundle_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_bundle_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_bundle_tasks(bundle_ids="test-bundle_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_byoip_cidrs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_byoip_cidrs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_byoip_cidrs(1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_block_extension_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_block_extension_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_block_extension_history(capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_block_extension_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_block_extension_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_block_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_block_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_block_offerings(1, instance_type="test-instance_type", instance_count=1, start_date_range="test-start_date_range", end_date_range="test-end_date_range", next_token="test-next_token", max_results=1, ultraserver_type="test-ultraserver_type", ultraserver_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_block_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_block_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_block_status(capacity_block_ids="test-capacity_block_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_blocks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_blocks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_blocks(capacity_block_ids="test-capacity_block_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_manager_data_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_manager_data_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_manager_data_exports(capacity_manager_data_export_ids=1, max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_reservation_billing_requests_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_reservation_billing_requests
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_reservation_billing_requests("test-role", capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_reservation_fleets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_reservation_fleets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_reservation_fleets(capacity_reservation_fleet_ids="test-capacity_reservation_fleet_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_reservation_topology_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_reservation_topology
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_reservation_topology(next_token="test-next_token", max_results=1, capacity_reservation_ids="test-capacity_reservation_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_reservations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_capacity_reservations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_reservations(capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_carrier_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_carrier_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_carrier_gateways(carrier_gateway_ids="test-carrier_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_classic_link_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_classic_link_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_classic_link_instances(instance_ids="test-instance_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_client_vpn_authorization_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_client_vpn_authorization_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_client_vpn_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_client_vpn_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_client_vpn_connections("test-client_vpn_endpoint_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_client_vpn_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_client_vpn_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_client_vpn_endpoints(client_vpn_endpoint_ids="test-client_vpn_endpoint_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_client_vpn_routes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_client_vpn_routes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_client_vpn_routes("test-client_vpn_endpoint_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_client_vpn_target_networks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_client_vpn_target_networks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_client_vpn_target_networks("test-client_vpn_endpoint_id", association_ids="test-association_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_coip_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_coip_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_coip_pools(pool_ids="test-pool_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_conversion_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_conversion_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_conversion_tasks(conversion_task_ids="test-conversion_task_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_customer_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_customer_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_customer_gateways(customer_gateway_ids="test-customer_gateway_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_declarative_policies_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_declarative_policies_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_declarative_policies_reports(next_token="test-next_token", max_results=1, report_ids=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_dhcp_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_dhcp_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_dhcp_options(dhcp_options_ids={}, next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_egress_only_internet_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_egress_only_internet_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_egress_only_internet_gateways(egress_only_internet_gateway_ids="test-egress_only_internet_gateway_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_elastic_gpus_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_elastic_gpus
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_elastic_gpus(elastic_gpu_ids="test-elastic_gpu_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_export_image_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_export_image_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_export_image_tasks(filters=[{}], export_image_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_export_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_export_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_export_tasks(filters=[{}], export_task_ids=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fast_launch_images_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fast_launch_images
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fast_launch_images(image_ids="test-image_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fast_snapshot_restores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fast_snapshot_restores(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fleet_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_history("test-fleet_id", "test-start_time", event_type="test-event_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleet_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fleet_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fleet_instances("test-fleet_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fleets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fleets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fleets(max_results=1, next_token="test-next_token", fleet_ids="test-fleet_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_flow_logs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_flow_logs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_flow_logs(filter="test-filter", flow_log_ids="test-flow_log_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_fpga_images_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_fpga_images
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_fpga_images(fpga_image_ids="test-fpga_image_ids", owners="test-owners", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_host_reservation_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_host_reservation_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_host_reservation_offerings(filter="test-filter", max_duration=1, max_results=1, min_duration=1, next_token="test-next_token", offering_id="test-offering_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_host_reservations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_host_reservations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_host_reservations(filter="test-filter", host_reservation_id_set="test-host_reservation_id_set", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_hosts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_hosts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_hosts(host_ids="test-host_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_iam_instance_profile_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_iam_instance_profile_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_iam_instance_profile_associations(association_ids="test-association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_id_format_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_id_format
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_id_format(resource="test-resource", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_identity_id_format_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_identity_id_format
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_identity_id_format("test-principal_arn", resource="test-resource", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_image_references_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_image_references
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_image_references("test-image_ids", include_all_resource_types=True, resource_types="test-resource_types", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_image_usage_report_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_image_usage_report_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_image_usage_report_entries(image_ids="test-image_ids", report_ids=1, next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_image_usage_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_image_usage_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_image_usage_reports(image_ids="test-image_ids", report_ids=1, next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_import_image_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_import_image_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_import_image_tasks(filters=[{}], import_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_import_snapshot_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_import_snapshot_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_import_snapshot_tasks(filters=[{}], import_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_connect_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_connect_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_connect_endpoints(max_results=1, next_token="test-next_token", filters=[{}], instance_connect_endpoint_ids="test-instance_connect_endpoint_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_credit_specifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_credit_specifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_credit_specifications(filters=[{}], instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_event_windows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_event_windows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_event_windows(instance_event_window_ids="test-instance_event_window_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_image_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_image_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_image_metadata(filters=[{}], instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_status(instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", filters=[{}], include_all_instances=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_topology_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_topology
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_topology(next_token="test-next_token", max_results=1, instance_ids="test-instance_ids", group_names="test-group_names", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_type_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_type_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_type_offerings(location_type="test-location_type", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_instance_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_instance_types(instance_types="test-instance_types", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_internet_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_internet_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_internet_gateways(next_token="test-next_token", max_results=1, internet_gateway_ids="test-internet_gateway_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_byoasn_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_byoasn
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_byoasn(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_external_resource_verification_tokens_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_external_resource_verification_tokens
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_external_resource_verification_tokens(filters=[{}], next_token="test-next_token", max_results=1, ipam_external_resource_verification_token_ids="test-ipam_external_resource_verification_token_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_pools(filters=[{}], max_results=1, next_token="test-next_token", ipam_pool_ids="test-ipam_pool_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_prefix_list_resolver_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_prefix_list_resolver_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_prefix_list_resolver_targets(filters=[{}], max_results=1, next_token="test-next_token", ipam_prefix_list_resolver_target_ids="test-ipam_prefix_list_resolver_target_ids", ipam_prefix_list_resolver_id="test-ipam_prefix_list_resolver_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_prefix_list_resolvers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_prefix_list_resolvers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_prefix_list_resolvers(filters=[{}], max_results=1, next_token="test-next_token", ipam_prefix_list_resolver_ids="test-ipam_prefix_list_resolver_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_resource_discoveries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_resource_discoveries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_resource_discoveries(ipam_resource_discovery_ids="test-ipam_resource_discovery_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_resource_discovery_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_resource_discovery_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_resource_discovery_associations(ipam_resource_discovery_association_ids="test-ipam_resource_discovery_association_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipam_scopes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipam_scopes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipam_scopes(filters=[{}], max_results=1, next_token="test-next_token", ipam_scope_ids="test-ipam_scope_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipams_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipams
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipams(filters=[{}], max_results=1, next_token="test-next_token", ipam_ids="test-ipam_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ipv6_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_ipv6_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_ipv6_pools(pool_ids="test-pool_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_key_pairs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_key_pairs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_key_pairs(key_names="test-key_names", key_pair_ids="test-key_pair_ids", include_public_key=True, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_launch_template_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_launch_template_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_launch_template_versions(launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", versions="test-versions", min_version="test-min_version", max_version=1, next_token="test-next_token", max_results=1, filters=[{}], resolve_alias="test-resolve_alias", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_launch_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_launch_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_launch_templates(launch_template_ids="test-launch_template_ids", launch_template_names="test-launch_template_names", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateway_route_table_virtual_interface_group_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateway_route_table_virtual_interface_group_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateway_route_table_virtual_interface_group_associations(local_gateway_route_table_virtual_interface_group_association_ids="test-local_gateway_route_table_virtual_interface_group_association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateway_route_table_vpc_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateway_route_table_vpc_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateway_route_table_vpc_associations(local_gateway_route_table_vpc_association_ids="test-local_gateway_route_table_vpc_association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateway_route_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateway_route_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateway_route_tables(local_gateway_route_table_ids="test-local_gateway_route_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateway_virtual_interface_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateway_virtual_interface_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateway_virtual_interface_groups(local_gateway_virtual_interface_group_ids="test-local_gateway_virtual_interface_group_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateway_virtual_interfaces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateway_virtual_interfaces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateway_virtual_interfaces(local_gateway_virtual_interface_ids="test-local_gateway_virtual_interface_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_local_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_local_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_local_gateways(local_gateway_ids="test-local_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_locked_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_locked_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_locked_snapshots(filters=[{}], max_results=1, next_token="test-next_token", snapshot_ids="test-snapshot_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_mac_hosts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_mac_hosts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_mac_hosts(filters=[{}], host_ids="test-host_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_mac_modification_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_mac_modification_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_mac_modification_tasks(filters=[{}], mac_modification_task_ids="test-mac_modification_task_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_managed_prefix_lists_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_managed_prefix_lists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_managed_prefix_lists(filters=[{}], max_results=1, next_token="test-next_token", prefix_list_ids="test-prefix_list_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_moving_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_moving_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_moving_addresses(public_ips="test-public_ips", next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_nat_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_nat_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_nat_gateways(filter="test-filter", max_results=1, nat_gateway_ids="test-nat_gateway_ids", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_acls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_acls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_acls(next_token="test-next_token", max_results=1, network_acl_ids="test-network_acl_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_insights_access_scope_analyses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_insights_access_scope_analyses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_insights_access_scope_analyses(network_insights_access_scope_analysis_ids="test-network_insights_access_scope_analysis_ids", network_insights_access_scope_id="test-network_insights_access_scope_id", analysis_start_time_begin="test-analysis_start_time_begin", analysis_start_time_end="test-analysis_start_time_end", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_insights_access_scopes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_insights_access_scopes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_insights_access_scopes(network_insights_access_scope_ids="test-network_insights_access_scope_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_insights_analyses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_insights_analyses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_insights_analyses(network_insights_analysis_ids="test-network_insights_analysis_ids", network_insights_path_id="test-network_insights_path_id", analysis_start_time="test-analysis_start_time", analysis_end_time="test-analysis_end_time", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_insights_paths_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_insights_paths
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_insights_paths(network_insights_path_ids="test-network_insights_path_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_interface_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_interface_attribute("test-network_interface_id", attribute="test-attribute", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_interface_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_interface_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_interface_permissions(network_interface_permission_ids="test-network_interface_permission_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_network_interfaces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_network_interfaces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_network_interfaces(next_token="test-next_token", max_results=1, network_interface_ids="test-network_interface_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_outpost_lags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_outpost_lags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_outpost_lags(outpost_lag_ids="test-outpost_lag_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_placement_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_placement_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_placement_groups(group_ids="test-group_ids", group_names="test-group_names", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_prefix_lists_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_prefix_lists
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_prefix_lists(filters=[{}], max_results=1, next_token="test-next_token", prefix_list_ids="test-prefix_list_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_principal_id_format_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_principal_id_format
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_principal_id_format(resources="test-resources", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_public_ipv4_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_public_ipv4_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_public_ipv4_pools(pool_ids="test-pool_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_regions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_regions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_regions(region_names="test-region_names", all_regions="test-all_regions", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replace_root_volume_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_replace_root_volume_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_replace_root_volume_tasks(replace_root_volume_task_ids="test-replace_root_volume_task_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_reserved_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_instances(offering_class="test-offering_class", reserved_instances_ids="test-reserved_instances_ids", filters=[{}], offering_type="test-offering_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_instances_listings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_reserved_instances_listings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_instances_listings(reserved_instances_id="test-reserved_instances_id", reserved_instances_listing_id="test-reserved_instances_listing_id", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_instances_modifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_reserved_instances_modifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_instances_modifications(reserved_instances_modification_ids="test-reserved_instances_modification_ids", next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_instances_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_reserved_instances_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_instances_offerings(availability_zone="test-availability_zone", include_marketplace=True, instance_type="test-instance_type", max_duration=1, max_instance_count=1, min_duration=1, offering_class="test-offering_class", product_description="test-product_description", reserved_instances_offering_ids="test-reserved_instances_offering_ids", availability_zone_id="test-availability_zone_id", filters=[{}], instance_tenancy="test-instance_tenancy", offering_type="test-offering_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_route_server_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_route_server_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_route_server_endpoints(route_server_endpoint_ids="test-route_server_endpoint_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_route_server_peers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_route_server_peers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_route_server_peers(route_server_peer_ids="test-route_server_peer_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_route_servers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_route_servers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_route_servers(route_server_ids="test-route_server_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_route_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_route_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_route_tables(next_token="test-next_token", max_results=1, route_table_ids="test-route_table_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_scheduled_instance_availability_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_scheduled_instance_availability
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_scheduled_instance_availability("test-first_slot_start_time_range", "test-recurrence", filters=[{}], max_results=1, max_slot_duration_in_hours=1, min_slot_duration_in_hours=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_scheduled_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_scheduled_instances(filters=[{}], max_results=1, next_token="test-next_token", scheduled_instance_ids="test-scheduled_instance_ids", slot_start_time_range="test-slot_start_time_range", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_security_group_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_security_group_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_security_group_rules(filters=[{}], security_group_rule_ids="test-security_group_rule_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_security_group_vpc_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_security_group_vpc_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_security_group_vpc_associations(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_service_link_virtual_interfaces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_service_link_virtual_interfaces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_service_link_virtual_interfaces(service_link_virtual_interface_ids="test-service_link_virtual_interface_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshot_tier_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_snapshot_tier_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_snapshot_tier_status(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_snapshots(max_results=1, next_token="test-next_token", owner_ids="test-owner_ids", restorable_by_user_ids="test-restorable_by_user_ids", snapshot_ids="test-snapshot_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_spot_fleet_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_spot_fleet_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_spot_fleet_instances("test-spot_fleet_request_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_spot_fleet_request_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_spot_fleet_request_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", event_type="test-event_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_spot_fleet_requests_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_spot_fleet_requests
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_spot_fleet_requests(spot_fleet_request_ids="test-spot_fleet_request_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_spot_instance_requests_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_spot_instance_requests
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_spot_instance_requests(next_token="test-next_token", max_results=1, spot_instance_request_ids="test-spot_instance_request_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_spot_price_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_spot_price_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_spot_price_history(availability_zone_id="test-availability_zone_id", start_time="test-start_time", end_time="test-end_time", instance_types="test-instance_types", product_descriptions="test-product_descriptions", filters=[{}], availability_zone="test-availability_zone", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stale_security_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_stale_security_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_stale_security_groups("test-vpc_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_store_image_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_store_image_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_store_image_tasks(image_ids="test-image_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_subnets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_subnets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_subnets(filters=[{}], subnet_ids="test-subnet_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_tags(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_traffic_mirror_filter_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_traffic_mirror_filter_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_traffic_mirror_filter_rules(traffic_mirror_filter_rule_ids="test-traffic_mirror_filter_rule_ids", traffic_mirror_filter_id="test-traffic_mirror_filter_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_traffic_mirror_filters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_traffic_mirror_filters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_traffic_mirror_filters(traffic_mirror_filter_ids="test-traffic_mirror_filter_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_traffic_mirror_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_traffic_mirror_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_traffic_mirror_sessions(traffic_mirror_session_ids="test-traffic_mirror_session_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_traffic_mirror_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_traffic_mirror_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_traffic_mirror_targets(traffic_mirror_target_ids="test-traffic_mirror_target_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_attachments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_attachments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_connect_peers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_connect_peers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_connect_peers(transit_gateway_connect_peer_ids="test-transit_gateway_connect_peer_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_connects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_connects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_connects(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_multicast_domains_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_multicast_domains
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_multicast_domains(transit_gateway_multicast_domain_ids="test-transit_gateway_multicast_domain_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_peering_attachments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_peering_attachments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_peering_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_policy_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_policy_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_policy_tables(transit_gateway_policy_table_ids="test-transit_gateway_policy_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_route_table_announcements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_route_table_announcements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_route_table_announcements(transit_gateway_route_table_announcement_ids="test-transit_gateway_route_table_announcement_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_route_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_route_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_route_tables(transit_gateway_route_table_ids="test-transit_gateway_route_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateway_vpc_attachments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateway_vpc_attachments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateway_vpc_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_transit_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_transit_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_transit_gateways(transit_gateway_ids="test-transit_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_trunk_interface_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_trunk_interface_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_trunk_interface_associations(association_ids="test-association_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_verified_access_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_verified_access_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_verified_access_endpoints(verified_access_endpoint_ids="test-verified_access_endpoint_ids", verified_access_instance_id="test-verified_access_instance_id", verified_access_group_id="test-verified_access_group_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_verified_access_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_verified_access_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_verified_access_groups(verified_access_group_ids="test-verified_access_group_ids", verified_access_instance_id="test-verified_access_instance_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_verified_access_instance_logging_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_verified_access_instance_logging_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_verified_access_instance_logging_configurations(verified_access_instance_ids="test-verified_access_instance_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_verified_access_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_verified_access_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_verified_access_instances(verified_access_instance_ids="test-verified_access_instance_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_verified_access_trust_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_verified_access_trust_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_verified_access_trust_providers(verified_access_trust_provider_ids="test-verified_access_trust_provider_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_volume_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_volume_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_volume_status(max_results=1, next_token="test-next_token", volume_ids="test-volume_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_volumes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_volumes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_volumes(volume_ids="test-volume_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_volumes_modifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_volumes_modifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_volumes_modifications(volume_ids="test-volume_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_block_public_access_exclusions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_block_public_access_exclusions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_block_public_access_exclusions(filters=[{}], exclusion_ids="test-exclusion_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_classic_link_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_classic_link
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_classic_link(vpc_ids="test-vpc_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_classic_link_dns_support
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_classic_link_dns_support(vpc_ids="test-vpc_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_associations(vpc_endpoint_ids="test-vpc_endpoint_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_connection_notifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_connection_notifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_connection_notifications(connection_notification_id="test-connection_notification_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_connections(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_service_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_service_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_service_configurations(service_ids="test-service_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_service_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_service_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_service_permissions("test-service_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoint_services_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoint_services
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoint_services(service_names="test-service_names", filters=[{}], max_results=1, next_token="test-next_token", service_regions="test-service_regions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_endpoints(vpc_endpoint_ids="test-vpc_endpoint_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpc_peering_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpc_peering_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpc_peering_connections(next_token="test-next_token", max_results=1, vpc_peering_connection_ids="test-vpc_peering_connection_ids", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpcs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpcs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpcs(filters=[{}], vpc_ids="test-vpc_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpn_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpn_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpn_connections(filters=[{}], vpn_connection_ids="test-vpn_connection_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vpn_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import describe_vpn_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await describe_vpn_gateways(filters=[{}], vpn_gateway_ids="test-vpn_gateway_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_network_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import detach_network_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await detach_network_interface("test-attachment_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import detach_verified_access_trust_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import detach_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await detach_volume("test-volume_id", device="test-device", force=True, instance_id="test-instance_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_aws_network_performance_metric_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_aws_network_performance_metric_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_aws_network_performance_metric_subscription(source="test-source", destination="test-destination", metric="test-metric", statistic="test-statistic", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_capacity_manager_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_capacity_manager
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_capacity_manager(client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_fast_launch_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_fast_launch
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_fast_launch("test-image_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_fast_snapshot_restores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_fast_snapshot_restores("test-source_snapshot_ids", availability_zones="test-availability_zones", availability_zone_ids="test-availability_zone_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_transit_gateway_route_table_propagation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_transit_gateway_route_table_propagation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", transit_gateway_route_table_announcement_id="test-transit_gateway_route_table_announcement_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disable_vpc_classic_link_dns_support
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disable_vpc_classic_link_dns_support(vpc_id="test-vpc_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disassociate_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disassociate_address(association_id="test-association_id", public_ip="test-public_ip", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disassociate_nat_gateway_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disassociate_nat_gateway_address("test-nat_gateway_id", "test-association_ids", max_drain_duration_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_trunk_interface_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import disassociate_trunk_interface
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await disassociate_trunk_interface("test-association_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_aws_network_performance_metric_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_aws_network_performance_metric_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_aws_network_performance_metric_subscription(source="test-source", destination="test-destination", metric="test-metric", statistic="test-statistic", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_capacity_manager_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_capacity_manager
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_capacity_manager(organizations_access="test-organizations_access", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_fast_launch_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_fast_launch
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_fast_launch("test-image_id", resource_type="test-resource_type", snapshot_configuration={}, launch_template="test-launch_template", max_parallel_launches=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_fast_snapshot_restores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_fast_snapshot_restores("test-source_snapshot_ids", availability_zones="test-availability_zones", availability_zone_ids="test-availability_zone_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_image_deregistration_protection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_image_deregistration_protection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_image_deregistration_protection("test-image_id", with_cooldown="test-with_cooldown", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_transit_gateway_route_table_propagation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_transit_gateway_route_table_propagation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", transit_gateway_route_table_announcement_id="test-transit_gateway_route_table_announcement_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import enable_vpc_classic_link_dns_support
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await enable_vpc_classic_link_dns_support(vpc_id="test-vpc_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_export_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import export_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await export_image("test-disk_image_format", "test-image_id", 1, client_token="test-client_token", description="test-description", role_name="test-role_name", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_export_transit_gateway_routes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import export_transit_gateway_routes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_associated_ipv6_pool_cidrs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_associated_ipv6_pool_cidrs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_associated_ipv6_pool_cidrs("test-pool_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_aws_network_performance_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_aws_network_performance_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_aws_network_performance_data(data_queries="test-data_queries", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_capacity_manager_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_capacity_manager_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_capacity_manager_metric_data("test-metric_names", "test-start_time", "test-end_time", "test-period", group_by="test-group_by", filter_by="test-filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_capacity_manager_metric_dimensions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_capacity_manager_metric_dimensions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_capacity_manager_metric_dimensions("test-group_by", "test-start_time", "test-end_time", "test-metric_names", filter_by="test-filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_capacity_reservation_usage_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_capacity_reservation_usage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_capacity_reservation_usage("test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_coip_pool_usage_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_coip_pool_usage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_coip_pool_usage("test-pool_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_console_output_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_console_output
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_console_output("test-instance_id", latest="test-latest", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_console_screenshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_console_screenshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_console_screenshot("test-instance_id", wake_up="test-wake_up", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_groups_for_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_groups_for_capacity_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_groups_for_capacity_reservation("test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_instance_types_from_instance_requirements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_instance_types_from_instance_requirements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_instance_types_from_instance_requirements("test-architecture_types", "test-virtualization_types", "test-instance_requirements", max_results=1, next_token="test-next_token", context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_address_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_address_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_address_history("test-cidr", "test-ipam_scope_id", vpc_id="test-vpc_id", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_discovered_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_discovered_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_discovered_public_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_discovered_public_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_discovered_resource_cidrs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_discovered_resource_cidrs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_pool_allocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_pool_allocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_pool_allocations("test-ipam_pool_id", ipam_pool_allocation_id="test-ipam_pool_allocation_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_pool_cidrs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_pool_cidrs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_pool_cidrs("test-ipam_pool_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_prefix_list_resolver_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_prefix_list_resolver_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_prefix_list_resolver_version_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_prefix_list_resolver_version_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", "test-ipam_prefix_list_resolver_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_prefix_list_resolver_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_prefix_list_resolver_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", ipam_prefix_list_resolver_versions="test-ipam_prefix_list_resolver_versions", max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ipam_resource_cidrs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_ipam_resource_cidrs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_ipam_resource_cidrs("test-ipam_scope_id", filters=[{}], max_results=1, next_token="test-next_token", ipam_pool_id="test-ipam_pool_id", resource_id="test-resource_id", resource_type="test-resource_type", resource_tag="test-resource_tag", resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_managed_prefix_list_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_managed_prefix_list_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_managed_prefix_list_associations("test-prefix_list_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_managed_prefix_list_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_managed_prefix_list_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_managed_prefix_list_entries("test-prefix_list_id", target_version="test-target_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_network_insights_access_scope_analysis_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_network_insights_access_scope_analysis_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_reserved_instances_exchange_quote_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_reserved_instances_exchange_quote
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_reserved_instances_exchange_quote("test-reserved_instance_ids", target_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_route_server_propagations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_route_server_propagations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_route_server_propagations("test-route_server_id", route_table_id="test-route_table_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_route_server_routing_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_route_server_routing_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_route_server_routing_database("test-route_server_id", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_security_groups_for_vpc_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_security_groups_for_vpc
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_security_groups_for_vpc("test-vpc_id", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_spot_placement_scores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_spot_placement_scores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_spot_placement_scores("test-target_capacity", instance_types="test-instance_types", target_capacity_unit_type="test-target_capacity_unit_type", single_availability_zone="test-single_availability_zone", region_names="test-region_names", instance_requirements_with_metadata="test-instance_requirements_with_metadata", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_subnet_cidr_reservations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_subnet_cidr_reservations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_subnet_cidr_reservations("test-subnet_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_attachment_propagations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_attachment_propagations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_multicast_domain_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_policy_table_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_policy_table_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_policy_table_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_policy_table_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_prefix_list_references_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_prefix_list_references
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_route_table_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_route_table_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_transit_gateway_route_table_propagations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_transit_gateway_route_table_propagations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_verified_access_endpoint_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_verified_access_endpoint_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_verified_access_endpoint_targets("test-verified_access_endpoint_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_vpn_connection_device_sample_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_vpn_connection_device_sample_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", internet_key_exchange_version="test-internet_key_exchange_version", sample_type="test-sample_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_vpn_connection_device_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import get_vpn_connection_device_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await get_vpn_connection_device_types(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import import_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await import_image(architecture="test-architecture", client_data="test-client_data", client_token="test-client_token", description="test-description", disk_containers="test-disk_containers", encrypted=True, hypervisor="test-hypervisor", kms_key_id="test-kms_key_id", license_type="test-license_type", platform="test-platform", role_name="test-role_name", license_specifications={}, tag_specifications={}, usage_operation="test-usage_operation", boot_mode="test-boot_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import import_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await import_instance("test-platform", description="test-description", launch_specification={}, disk_images="test-disk_images", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import import_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await import_key_pair("test-key_name", "test-public_key_material", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import import_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await import_snapshot(client_data="test-client_data", client_token="test-client_token", description="test-description", disk_container="test-disk_container", encrypted=True, kms_key_id="test-kms_key_id", role_name="test-role_name", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import import_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await import_volume("test-image", "test-volume", availability_zone_id="test-availability_zone_id", availability_zone="test-availability_zone", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_images_in_recycle_bin_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import list_images_in_recycle_bin
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await list_images_in_recycle_bin(image_ids="test-image_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_snapshots_in_recycle_bin_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import list_snapshots_in_recycle_bin
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await list_snapshots_in_recycle_bin(max_results=1, next_token="test-next_token", snapshot_ids="test-snapshot_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_lock_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import lock_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await lock_snapshot("test-snapshot_id", "test-lock_mode", cool_off_period="test-cool_off_period", lock_duration=1, expiration_date="test-expiration_date", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_address_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_address_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_address_attribute("test-allocation_id", domain_name="test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_capacity_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_capacity_reservation("test-capacity_reservation_id", instance_count=1, end_date="test-end_date", end_date_type="test-end_date_type", accept="test-accept", additional_info="test-additional_info", instance_match_criteria="test-instance_match_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_capacity_reservation_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_capacity_reservation_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", total_target_capacity="test-total_target_capacity", end_date="test-end_date", remove_end_date="test-remove_end_date", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_client_vpn_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_client_vpn_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_client_vpn_endpoint("test-client_vpn_endpoint_id", server_certificate_arn="test-server_certificate_arn", connection_log_options={}, dns_servers="test-dns_servers", vpn_port=1, description="test-description", split_tunnel="test-split_tunnel", security_group_ids="test-security_group_ids", vpc_id="test-vpc_id", self_service_portal=1, client_connect_options={}, session_timeout_hours=1, client_login_banner_options={}, client_route_enforcement_options={}, disconnect_on_session_timeout=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_fleet("test-fleet_id", excess_capacity_termination_policy="{}", launch_template_configs={}, target_capacity_specification={}, context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_fpga_image_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_fpga_image_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_fpga_image_attribute("test-fpga_image_id", attribute="test-attribute", operation_type="test-operation_type", user_ids="test-user_ids", user_groups="test-user_groups", product_codes="test-product_codes", load_permission="test-load_permission", description="test-description", name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_hosts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_hosts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_hosts("test-host_ids", host_recovery="test-host_recovery", instance_type="test-instance_type", instance_family="test-instance_family", host_maintenance="test-host_maintenance", auto_placement=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_image_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_image_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_image_attribute("test-image_id", attribute="test-attribute", description="test-description", launch_permission="test-launch_permission", operation_type="test-operation_type", product_codes="test-product_codes", user_groups="test-user_groups", user_ids="test-user_ids", value="test-value", organization_arns="test-organization_arns", organizational_unit_arns="test-organizational_unit_arns", imds_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_attribute("test-instance_id", source_dest_check="test-source_dest_check", disable_api_stop=True, attribute="test-attribute", value="test-value", block_device_mappings={}, disable_api_termination=True, instance_type="test-instance_type", kernel="test-kernel", ramdisk="test-ramdisk", user_data="test-user_data", instance_initiated_shutdown_behavior="test-instance_initiated_shutdown_behavior", groups="test-groups", ebs_optimized="test-ebs_optimized", sriov_net_support=1, ena_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_connect_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_connect_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_connect_endpoint("test-instance_connect_endpoint_id", ip_address_type="test-ip_address_type", security_group_ids="test-security_group_ids", preserve_client_ip="test-preserve_client_ip", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_credit_specification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_credit_specification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_credit_specification({}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_event_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_event_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_event_window("test-instance_event_window_id", name="test-name", time_ranges="test-time_ranges", cron_expression="test-cron_expression", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_maintenance_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_maintenance_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_maintenance_options("test-instance_id", auto_recovery=True, reboot_migration="test-reboot_migration", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_metadata_defaults_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_metadata_defaults
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_metadata_defaults(http_tokens="test-http_tokens", http_put_response_hop_limit=1, http_endpoint="test-http_endpoint", instance_metadata_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_metadata_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_metadata_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_metadata_options("test-instance_id", http_tokens="test-http_tokens", http_put_response_hop_limit=1, http_endpoint="test-http_endpoint", http_protocol_ipv6="test-http_protocol_ipv6", instance_metadata_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_instance_placement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_instance_placement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_instance_placement("test-instance_id", group_name="test-group_name", partition_number="test-partition_number", host_resource_group_arn="test-host_resource_group_arn", group_id="test-group_id", tenancy="test-tenancy", affinity="test-affinity", host_id="test-host_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam("test-ipam_id", description="test-description", add_operating_regions="test-add_operating_regions", remove_operating_regions="test-remove_operating_regions", tier="test-tier", enable_private_gua=True, metered_account=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_pool("test-ipam_pool_id", description="test-description", auto_import=True, allocation_min_netmask_length="test-allocation_min_netmask_length", allocation_max_netmask_length=1, allocation_default_netmask_length="test-allocation_default_netmask_length", clear_allocation_default_netmask_length="test-clear_allocation_default_netmask_length", add_allocation_resource_tags=[{"Key": "k", "Value": "v"}], remove_allocation_resource_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_prefix_list_resolver_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_prefix_list_resolver
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", description="test-description", rules="test-rules", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_prefix_list_resolver_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_prefix_list_resolver_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", desired_version="test-desired_version", track_latest_version="test-track_latest_version", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_resource_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_resource_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", "test-monitored", destination_ipam_scope_id="test-destination_ipam_scope_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_resource_discovery
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_resource_discovery("test-ipam_resource_discovery_id", description="test-description", add_operating_regions="test-add_operating_regions", remove_operating_regions="test-remove_operating_regions", add_organizational_unit_exclusions="test-add_organizational_unit_exclusions", remove_organizational_unit_exclusions="test-remove_organizational_unit_exclusions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_ipam_scope_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_ipam_scope
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_ipam_scope("test-ipam_scope_id", description="test-description", external_authority_configuration={}, remove_external_authority_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_launch_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_launch_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_launch_template(client_token="test-client_token", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", default_version="test-default_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_local_gateway_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", local_gateway_virtual_interface_group_id="test-local_gateway_virtual_interface_group_id", network_interface_id="test-network_interface_id", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_managed_prefix_list_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_managed_prefix_list
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_managed_prefix_list("test-prefix_list_id", current_version="test-current_version", prefix_list_name="test-prefix_list_name", add_entries="test-add_entries", remove_entries="test-remove_entries", max_entries=1, ipam_prefix_list_resolver_sync_enabled="test-ipam_prefix_list_resolver_sync_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_network_interface_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_network_interface_attribute("test-network_interface_id", ena_srd_specification={}, enable_primary_ipv6=True, connection_tracking_specification={}, associate_public_ip_address="test-associate_public_ip_address", associated_subnet_ids="test-associated_subnet_ids", description="test-description", source_dest_check="test-source_dest_check", groups="test-groups", attachment="test-attachment", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_private_dns_name_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_private_dns_name_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_private_dns_name_options("test-instance_id", private_dns_hostname_type="test-private_dns_hostname_type", enable_resource_name_dns_a_record=True, enable_resource_name_dns_aaaa_record=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_reserved_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_reserved_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_reserved_instances("test-reserved_instances_ids", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_route_server_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_route_server
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_route_server("test-route_server_id", persist_routes="test-persist_routes", persist_routes_duration=1, sns_notifications_enabled="test-sns_notifications_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_snapshot_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_snapshot_attribute("test-snapshot_id", attribute="test-attribute", create_volume_permission="test-create_volume_permission", group_names="test-group_names", operation_type="test-operation_type", user_ids="test-user_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_snapshot_tier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_snapshot_tier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_snapshot_tier("test-snapshot_id", storage_tier="test-storage_tier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_spot_fleet_request_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_spot_fleet_request
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_spot_fleet_request("test-spot_fleet_request_id", launch_template_configs={}, on_demand_target_capacity="test-on_demand_target_capacity", context={}, target_capacity="test-target_capacity", excess_capacity_termination_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_subnet_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_subnet_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_subnet_attribute("test-subnet_id", assign_ipv6_address_on_creation="test-assign_ipv6_address_on_creation", map_public_ip_on_launch="test-map_public_ip_on_launch", map_customer_owned_ip_on_launch="test-map_customer_owned_ip_on_launch", customer_owned_ipv4_pool="test-customer_owned_ipv4_pool", enable_dns64=True, private_dns_hostname_type_on_launch="test-private_dns_hostname_type_on_launch", enable_resource_name_dns_a_record_on_launch=True, enable_resource_name_dns_aaaa_record_on_launch=True, enable_lni_at_device_index=True, disable_lni_at_device_index=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_traffic_mirror_filter_network_services_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_traffic_mirror_filter_network_services
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", add_network_services="test-add_network_services", remove_network_services="test-remove_network_services", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_traffic_mirror_filter_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_traffic_mirror_filter_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", traffic_direction="test-traffic_direction", rule_number="test-rule_number", rule_action="test-rule_action", destination_port_range=1, source_port_range=1, protocol="test-protocol", destination_cidr_block="test-destination_cidr_block", source_cidr_block="test-source_cidr_block", description="test-description", remove_fields="test-remove_fields", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_traffic_mirror_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_traffic_mirror_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_traffic_mirror_session("test-traffic_mirror_session_id", traffic_mirror_target_id="test-traffic_mirror_target_id", traffic_mirror_filter_id="test-traffic_mirror_filter_id", packet_length="test-packet_length", session_number="test-session_number", virtual_network_id="test-virtual_network_id", description="test-description", remove_fields="test-remove_fields", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_transit_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_transit_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_transit_gateway("test-transit_gateway_id", description="test-description", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_transit_gateway_prefix_list_reference_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_transit_gateway_prefix_list_reference
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_transit_gateway_vpc_attachment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_transit_gateway_vpc_attachment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", add_subnet_ids="test-add_subnet_ids", remove_subnet_ids="test-remove_subnet_ids", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_endpoint("test-verified_access_endpoint_id", verified_access_group_id="test-verified_access_group_id", load_balancer_options={}, network_interface_options={}, description="test-description", client_token="test-client_token", rds_options={}, cidr_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_endpoint_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_endpoint_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", policy_enabled="test-policy_enabled", policy_document="test-policy_document", client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_group("test-verified_access_group_id", verified_access_instance_id="test-verified_access_instance_id", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_group_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_group_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_group_policy("test-verified_access_group_id", policy_enabled="test-policy_enabled", policy_document="test-policy_document", client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_instance("test-verified_access_instance_id", description="test-description", client_token="test-client_token", cidr_endpoints_custom_sub_domain="test-cidr_endpoints_custom_sub_domain", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_instance_logging_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_instance_logging_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", "test-access_logs", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_verified_access_trust_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_verified_access_trust_provider("test-verified_access_trust_provider_id", oidc_options={}, device_options={}, description="test-description", client_token="test-client_token", sse_specification={}, native_application_oidc_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_volume("test-volume_id", size=1, volume_type="test-volume_type", iops="test-iops", throughput="test-throughput", multi_attach_enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_volume_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_volume_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_volume_attribute("test-volume_id", auto_enable_io=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_attribute("test-vpc_id", enable_dns_hostnames=True, enable_dns_support=True, enable_network_address_usage_metrics=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_endpoint("test-vpc_endpoint_id", reset_policy="{}", policy_document="test-policy_document", add_route_table_ids="test-add_route_table_ids", remove_route_table_ids="test-remove_route_table_ids", add_subnet_ids="test-add_subnet_ids", remove_subnet_ids="test-remove_subnet_ids", add_security_group_ids="test-add_security_group_ids", remove_security_group_ids="test-remove_security_group_ids", ip_address_type="test-ip_address_type", dns_options={}, private_dns_enabled="test-private_dns_enabled", subnet_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_endpoint_connection_notification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_endpoint_connection_notification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_endpoint_connection_notification("test-connection_notification_id", connection_notification_arn="test-connection_notification_arn", connection_events="test-connection_events", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_endpoint_service_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_endpoint_service_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_endpoint_service_configuration("test-service_id", private_dns_name="test-private_dns_name", remove_private_dns_name="test-remove_private_dns_name", acceptance_required="test-acceptance_required", add_network_load_balancer_arns="test-add_network_load_balancer_arns", remove_network_load_balancer_arns="test-remove_network_load_balancer_arns", add_gateway_load_balancer_arns="test-add_gateway_load_balancer_arns", remove_gateway_load_balancer_arns="test-remove_gateway_load_balancer_arns", add_supported_ip_address_types=1, remove_supported_ip_address_types=1, add_supported_regions=1, remove_supported_regions=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_endpoint_service_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_endpoint_service_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_endpoint_service_permissions("test-service_id", add_allowed_principals="test-add_allowed_principals", remove_allowed_principals="test-remove_allowed_principals", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpc_peering_connection_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpc_peering_connection_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpc_peering_connection_options("test-vpc_peering_connection_id", accepter_peering_connection_options={}, requester_peering_connection_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpn_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpn_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpn_connection("test-vpn_connection_id", transit_gateway_id="test-transit_gateway_id", customer_gateway_id="test-customer_gateway_id", vpn_gateway_id="test-vpn_gateway_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpn_connection_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpn_connection_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpn_connection_options("test-vpn_connection_id", local_ipv4_network_cidr="test-local_ipv4_network_cidr", remote_ipv4_network_cidr="test-remote_ipv4_network_cidr", local_ipv6_network_cidr="test-local_ipv6_network_cidr", remote_ipv6_network_cidr="test-remote_ipv6_network_cidr", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_vpn_tunnel_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import modify_vpn_tunnel_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, skip_tunnel_replacement=True, pre_shared_key_storage="test-pre_shared_key_storage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_move_capacity_reservation_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import move_capacity_reservation_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_provision_byoip_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import provision_byoip_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await provision_byoip_cidr("test-cidr", cidr_authorization_context={}, publicly_advertisable="test-publicly_advertisable", description="test-description", pool_tag_specifications={}, multi_region=True, network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_provision_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import provision_ipam_pool_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await provision_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", cidr_authorization_context={}, netmask_length="test-netmask_length", client_token="test-client_token", verification_method="test-verification_method", ipam_external_resource_verification_token_id="test-ipam_external_resource_verification_token_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_provision_public_ipv4_pool_cidr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import provision_public_ipv4_pool_cidr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", "test-netmask_length", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_capacity_block_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import purchase_capacity_block
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_host_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import purchase_host_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await purchase_host_reservation("test-host_id_set", "test-offering_id", client_token="test-client_token", currency_code="test-currency_code", limit_price=1, tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_reserved_instances_offering_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import purchase_reserved_instances_offering
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", purchase_time="test-purchase_time", limit_price=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import purchase_scheduled_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await purchase_scheduled_instances("test-purchase_requests", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import register_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await register_image("test-name", image_location="test-image_location", billing_products="test-billing_products", boot_mode="test-boot_mode", tpm_support=1, uefi_data="test-uefi_data", imds_support=1, tag_specifications={}, description="test-description", architecture="test-architecture", kernel_id="test-kernel_id", ramdisk_id="test-ramdisk_id", root_device_name="test-root_device_name", block_device_mappings={}, virtualization_type="test-virtualization_type", sriov_net_support=1, ena_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_transit_gateway_multicast_group_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import register_transit_gateway_multicast_group_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", "test-network_interface_ids", group_ip_address="test-group_ip_address", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_transit_gateway_multicast_group_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import register_transit_gateway_multicast_group_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", "test-network_interface_ids", group_ip_address="test-group_ip_address", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reject_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import reject_transit_gateway_multicast_domain_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await reject_transit_gateway_multicast_domain_associations(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_release_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import release_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await release_address(allocation_id="test-allocation_id", public_ip="test-public_ip", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replace_image_criteria_in_allowed_images_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import replace_image_criteria_in_allowed_images_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await replace_image_criteria_in_allowed_images_settings(image_criteria="test-image_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replace_network_acl_entry_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import replace_network_acl_entry
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await replace_network_acl_entry("test-network_acl_id", "test-rule_number", "test-protocol", "test-rule_action", "test-egress", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", icmp_type_code="test-icmp_type_code", port_range=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replace_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import replace_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await replace_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", vpc_endpoint_id="test-vpc_endpoint_id", local_target="test-local_target", transit_gateway_id="test-transit_gateway_id", local_gateway_id="test-local_gateway_id", carrier_gateway_id="test-carrier_gateway_id", core_network_arn="test-core_network_arn", odb_network_arn="test-odb_network_arn", destination_cidr_block="test-destination_cidr_block", gateway_id="test-gateway_id", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", egress_only_internet_gateway_id="test-egress_only_internet_gateway_id", instance_id="test-instance_id", network_interface_id="test-network_interface_id", vpc_peering_connection_id="test-vpc_peering_connection_id", nat_gateway_id="test-nat_gateway_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replace_transit_gateway_route_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import replace_transit_gateway_route
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replace_vpn_tunnel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import replace_vpn_tunnel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", apply_pending_maintenance=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_report_instance_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import report_instance_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await report_instance_status("test-instances", "test-status", "test-reason_codes", start_time="test-start_time", end_time="test-end_time", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_request_spot_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import request_spot_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await request_spot_instances(launch_specification={}, tag_specifications={}, instance_interruption_behavior="test-instance_interruption_behavior", spot_price="test-spot_price", client_token="test-client_token", instance_count=1, type_value="test-type_value", valid_from="test-valid_from", valid_until="test-valid_until", launch_group="test-launch_group", availability_zone_group="test-availability_zone_group", block_duration_minutes=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_fpga_image_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import reset_fpga_image_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await reset_fpga_image_attribute("test-fpga_image_id", attribute="test-attribute", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import reset_network_interface_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await reset_network_interface_attribute("test-network_interface_id", source_dest_check="test-source_dest_check", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_snapshot_tier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import restore_snapshot_tier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await restore_snapshot_tier("test-snapshot_id", temporary_restore_days="test-temporary_restore_days", permanent_restore="test-permanent_restore", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_client_vpn_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import revoke_client_vpn_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", access_group_id="test-access_group_id", revoke_all_groups="test-revoke_all_groups", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_security_group_egress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import revoke_security_group_egress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await revoke_security_group_egress("test-group_id", security_group_rule_ids="test-security_group_rule_ids", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", ip_protocol="test-ip_protocol", from_port=1, to_port=1, cidr_ip="test-cidr_ip", ip_permissions="test-ip_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import revoke_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await revoke_security_group_ingress(cidr_ip="test-cidr_ip", from_port=1, group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", ip_protocol="test-ip_protocol", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", to_port=1, security_group_rule_ids="test-security_group_rule_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import run_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await run_instances(1, 1, block_device_mappings={}, image_id="test-image_id", instance_type="test-instance_type", ipv6_address_count=1, ipv6_addresses="test-ipv6_addresses", kernel_id="test-kernel_id", key_name="test-key_name", monitoring="test-monitoring", placement="test-placement", ramdisk_id="test-ramdisk_id", security_group_ids="test-security_group_ids", security_groups="test-security_groups", subnet_id="test-subnet_id", user_data="test-user_data", elastic_gpu_specification={}, elastic_inference_accelerators="test-elastic_inference_accelerators", tag_specifications={}, launch_template="test-launch_template", instance_market_options={}, credit_specification={}, cpu_options={}, capacity_reservation_specification={}, hibernation_options={}, license_specifications={}, metadata_options={}, enclave_options={}, private_dns_name_options={}, maintenance_options={}, disable_api_stop=True, enable_primary_ipv6=True, network_performance_options={}, operator="test-operator", disable_api_termination=True, instance_initiated_shutdown_behavior="test-instance_initiated_shutdown_behavior", private_ip_address="test-private_ip_address", client_token="test-client_token", additional_info="test-additional_info", network_interfaces="test-network_interfaces", iam_instance_profile="test-iam_instance_profile", ebs_optimized="test-ebs_optimized", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import run_scheduled_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await run_scheduled_instances({}, "test-scheduled_instance_id", client_token="test-client_token", instance_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_local_gateway_routes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import search_local_gateway_routes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await search_local_gateway_routes("test-local_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_transit_gateway_multicast_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import search_transit_gateway_multicast_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_transit_gateway_routes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import search_transit_gateway_routes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await search_transit_gateway_routes("test-transit_gateway_route_table_id", [{}], max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_declarative_policies_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import start_declarative_policies_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await start_declarative_policies_report("test-s3_bucket", "test-target_id", s3_prefix="test-s3_prefix", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_network_insights_access_scope_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import start_network_insights_access_scope_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_network_insights_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import start_network_insights_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await start_network_insights_analysis("test-network_insights_path_id", "test-client_token", additional_accounts=1, filter_in_arns="test-filter_in_arns", filter_out_arns="test-filter_out_arns", tag_specifications={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_terminate_client_vpn_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import terminate_client_vpn_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await terminate_client_vpn_connections("test-client_vpn_endpoint_id", connection_id="test-connection_id", username="test-username", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_unassign_ipv6_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import unassign_ipv6_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await unassign_ipv6_addresses("test-network_interface_id", ipv6_prefixes="test-ipv6_prefixes", ipv6_addresses="test-ipv6_addresses", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_unassign_private_ip_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import unassign_private_ip_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await unassign_private_ip_addresses("test-network_interface_id", ipv4_prefixes="test-ipv4_prefixes", private_ip_addresses="test-private_ip_addresses", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_unassign_private_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import unassign_private_nat_gateway_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await unassign_private_nat_gateway_address("test-nat_gateway_id", "test-private_ip_addresses", max_drain_duration_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_capacity_manager_organizations_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import update_capacity_manager_organizations_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await update_capacity_manager_organizations_access("test-organizations_access", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_group_rule_descriptions_egress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import update_security_group_rule_descriptions_egress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await update_security_group_rule_descriptions_egress(group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", security_group_rule_descriptions="test-security_group_rule_descriptions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_group_rule_descriptions_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ec2 import update_security_group_rule_descriptions_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ec2.async_client", lambda *a, **kw: mock_client)
    await update_security_group_rule_descriptions_ingress(group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", security_group_rule_descriptions="test-security_group_rule_descriptions", region_name="us-east-1")
    mock_client.call.assert_called_once()
