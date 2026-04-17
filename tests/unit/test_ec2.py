"""Tests for aws_util.ec2 module."""
from __future__ import annotations


from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.ec2 import (
    EC2Image,
    EC2Instance,
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

REGION = "us-east-1"


@pytest.fixture
def instance_id(ec2_client):
    _, iid = ec2_client
    return iid


@pytest.fixture
def ec2(ec2_client):
    client, _ = ec2_client
    return client


# ---------------------------------------------------------------------------
# describe_instances
# ---------------------------------------------------------------------------


def test_describe_instances_all(ec2_client):
    result = describe_instances(region_name=REGION)
    assert len(result) >= 1
    assert all(isinstance(i, EC2Instance) for i in result)


def test_describe_instances_by_id(ec2_client):
    client, instance_id = ec2_client
    result = describe_instances([instance_id], region_name=REGION)
    assert len(result) == 1
    assert result[0].instance_id == instance_id


def test_describe_instances_with_filter(ec2_client):
    result = describe_instances(
        filters=[{"Name": "instance-state-name", "Values": ["running", "pending"]}],
        region_name=REGION,
    )
    assert isinstance(result, list)


def test_describe_instances_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "InvalidParameterValue", "Message": "invalid"}},
        "DescribeInstances",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_instances failed"):
        describe_instances(region_name=REGION)


# ---------------------------------------------------------------------------
# get_instance
# ---------------------------------------------------------------------------


def test_get_instance_existing(ec2_client):
    client, instance_id = ec2_client
    result = get_instance(instance_id, region_name=REGION)
    assert result is not None
    assert result.instance_id == instance_id


def test_get_instance_nonexistent():
    # moto raises InvalidInstanceID.NotFound which propagates as RuntimeError
    with pytest.raises(RuntimeError, match="describe_instances failed"):
        get_instance("i-00000000000000000", region_name=REGION)


# ---------------------------------------------------------------------------
# start_instances / stop_instances / reboot_instances / terminate_instances
# ---------------------------------------------------------------------------


def test_stop_instances(ec2_client):
    client, instance_id = ec2_client
    stop_instances([instance_id], region_name=REGION)
    # Just verify no exception


def test_stop_instances_force(ec2_client):
    client, instance_id = ec2_client
    stop_instances([instance_id], force=True, region_name=REGION)


def test_start_instances(ec2_client):
    client, instance_id = ec2_client
    stop_instances([instance_id], region_name=REGION)
    start_instances([instance_id], region_name=REGION)


def test_reboot_instances(ec2_client):
    client, instance_id = ec2_client
    reboot_instances([instance_id], region_name=REGION)


def test_terminate_instances(ec2_client):
    client, instance_id = ec2_client
    terminate_instances([instance_id], region_name=REGION)


def test_stop_instances_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.stop_instances.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "StopInstances",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop instances"):
        stop_instances(["i-nonexistent"], region_name=REGION)


def test_start_instances_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.start_instances.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "StartInstances",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start instances"):
        start_instances(["i-nonexistent"], region_name=REGION)


def test_reboot_instances_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.reboot_instances.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "RebootInstances",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reboot instances"):
        reboot_instances(["i-nonexistent"], region_name=REGION)


def test_terminate_instances_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.terminate_instances.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "TerminateInstances",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate instances"):
        terminate_instances(["i-nonexistent"], region_name=REGION)


# ---------------------------------------------------------------------------
# create_image
# ---------------------------------------------------------------------------


def test_create_image(ec2_client):
    client, instance_id = ec2_client
    image_id = create_image(instance_id, "test-ami", region_name=REGION)
    assert image_id.startswith("ami-")


def test_create_image_with_description(ec2_client):
    client, instance_id = ec2_client
    image_id = create_image(
        instance_id,
        "desc-ami",
        description="Test description",
        no_reboot=False,
        region_name=REGION,
    )
    assert image_id.startswith("ami-")


def test_create_image_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.create_image.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "CreateImage",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create image"):
        create_image("i-nonexistent", "ami-name", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_images
# ---------------------------------------------------------------------------


def test_describe_images_all(ec2_client):
    result = describe_images(region_name=REGION)
    assert isinstance(result, list)


def test_describe_images_with_ids(ec2_client):
    client, instance_id = ec2_client
    image_id = create_image(instance_id, "test-img", region_name=REGION)
    result = describe_images(image_ids=[image_id], region_name=REGION)
    assert any(img.image_id == image_id for img in result)


def test_describe_images_with_owners(ec2_client):
    result = describe_images(owners=["self"], region_name=REGION)
    assert isinstance(result, list)


def test_describe_images_with_filters(ec2_client):
    result = describe_images(
        filters=[{"Name": "state", "Values": ["available"]}],
        region_name=REGION,
    )
    assert isinstance(result, list)


def test_describe_images_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.describe_images.side_effect = ClientError(
        {"Error": {"Code": "InvalidAMIID.NotFound", "Message": "not found"}},
        "DescribeImages",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_images failed"):
        describe_images(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_security_groups
# ---------------------------------------------------------------------------


def test_describe_security_groups(ec2_client):
    result = describe_security_groups(region_name=REGION)
    assert isinstance(result, list)
    assert len(result) >= 1  # default security group


def test_describe_security_groups_with_filter(ec2_client):
    result = describe_security_groups(
        filters=[{"Name": "group-name", "Values": ["default"]}],
        region_name=REGION,
    )
    assert isinstance(result, list)


def test_describe_security_groups_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.describe_security_groups.side_effect = ClientError(
        {"Error": {"Code": "InvalidGroup.NotFound", "Message": "not found"}},
        "DescribeSecurityGroups",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_security_groups failed"):
        describe_security_groups(region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_instance_state
# ---------------------------------------------------------------------------


def test_wait_for_instance_state_already_in_state(ec2_client):
    client, instance_id = ec2_client
    # Instance starts in 'running' or 'pending' state
    result = wait_for_instance_state(
        instance_id,
        "running",
        timeout=30.0,
        poll_interval=0.01,
        region_name=REGION,
    )
    assert isinstance(result, EC2Instance)


def test_wait_for_instance_state_timeout(ec2_client):
    client, instance_id = ec2_client
    with pytest.raises(TimeoutError, match="did not reach state"):
        wait_for_instance_state(
            instance_id,
            "nonexistent-state",
            timeout=0.1,
            poll_interval=0.05,
            region_name=REGION,
        )


def test_wait_for_instance_state_not_found():
    with pytest.raises(RuntimeError, match="describe_instances failed|not found"):
        wait_for_instance_state(
            "i-00000000000000000",
            "running",
            timeout=0.5,
            poll_interval=0.1,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_instances_by_tag
# ---------------------------------------------------------------------------


def test_get_instances_by_tag(ec2_client):
    client, instance_id = ec2_client
    client.create_tags(
        Resources=[instance_id],
        Tags=[{"Key": "Environment", "Value": "test"}],
    )
    result = get_instances_by_tag("Environment", "test", region_name=REGION)
    assert any(i.instance_id == instance_id for i in result)


def test_get_instances_by_tag_no_match():
    result = get_instances_by_tag("NoSuchKey", "NoSuchValue", region_name=REGION)
    assert result == []


# ---------------------------------------------------------------------------
# get_latest_ami
# ---------------------------------------------------------------------------


def test_get_latest_ami_no_match():
    result = get_latest_ami("nonexistent-ami-*", region_name=REGION)
    assert result is None


def test_get_latest_ami_with_match(ec2_client):
    client, instance_id = ec2_client
    create_image(instance_id, "my-app-v1", region_name=REGION)
    result = get_latest_ami("my-app-*", owners=["self"], region_name=REGION)
    # May return None or an image depending on moto's AMI filtering
    assert result is None or isinstance(result, EC2Image)


# ---------------------------------------------------------------------------
# get_instance_console_output
# ---------------------------------------------------------------------------


def test_get_instance_console_output(ec2_client, monkeypatch):
    """Test console output retrieval; moto may return invalid base64 so we mock it."""
    import base64
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    client, instance_id = ec2_client
    mock_client = MagicMock()
    mock_client.get_console_output.return_value = {
        "Output": base64.b64encode(b"console output").decode()
    }
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    output = get_instance_console_output(instance_id, region_name=REGION)
    assert isinstance(output, str)
    assert "console output" in output


def test_get_instance_console_output_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.get_console_output.side_effect = ClientError(
        {"Error": {"Code": "InvalidInstanceID.NotFound", "Message": "not found"}},
        "GetConsoleOutput",
    )
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_console_output failed"):
        get_instance_console_output("i-nonexistent", region_name=REGION)


def test_describe_security_groups_with_group_ids(monkeypatch):
    """Covers GroupIds kwarg branch in describe_security_groups (line 321)."""
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.describe_security_groups.return_value = {"SecurityGroups": []}
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_security_groups(group_ids=["sg-12345"], region_name=REGION)
    assert result == []
    call_kwargs = mock_client.describe_security_groups.call_args[1]
    assert call_kwargs.get("GroupIds") == ["sg-12345"]


def test_wait_for_instance_state_instance_not_found(monkeypatch):
    """Covers 'instance not found' RuntimeError in wait_for_instance_state (line 375)."""
    import aws_util.ec2 as ec2mod
    monkeypatch.setattr(ec2mod, "get_instance", lambda *a, **kw: None)
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_instance_state(
            "i-nonexistent", "running", timeout=5.0, poll_interval=0.01, region_name=REGION
        )


def test_wait_for_instance_state_polls_then_times_out(monkeypatch):
    """Covers the sleep branch (line 383) by letting the loop iterate before timeout."""
    import aws_util.ec2 as ec2mod

    fake = EC2Instance(
        instance_id="i-abc",
        instance_type="t2.micro",
        state="pending",
        launch_time="2024-01-01T00:00:00Z",
        private_ip=None,
        public_ip=None,
        vpc_id=None,
        subnet_id=None,
        tags={},
    )
    monkeypatch.setattr(ec2mod, "get_instance", lambda *a, **kw: fake)
    with pytest.raises(TimeoutError, match="did not reach state"):
        wait_for_instance_state(
            "i-abc",
            "running",
            timeout=0.15,
            poll_interval=0.01,
            region_name=REGION,
        )


def test_get_console_output_empty(monkeypatch):
    """Covers empty console output return '' branch (line 465)."""
    from unittest.mock import MagicMock
    import aws_util.ec2 as ec2mod

    mock_client = MagicMock()
    mock_client.get_console_output.return_value = {"Output": ""}
    monkeypatch.setattr(ec2mod, "get_client", lambda *a, **kw: mock_client)
    from aws_util.ec2 import get_instance_console_output
    result = get_instance_console_output("i-12345", region_name=REGION)
    assert result == ""


def test_accept_address_transfer(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_address_transfer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_address_transfer("test-address", region_name=REGION)
    mock_client.accept_address_transfer.assert_called_once()


def test_accept_address_transfer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_address_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_address_transfer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept address transfer"):
        accept_address_transfer("test-address", region_name=REGION)


def test_accept_capacity_reservation_billing_ownership(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_capacity_reservation_billing_ownership.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_capacity_reservation_billing_ownership("test-capacity_reservation_id", region_name=REGION)
    mock_client.accept_capacity_reservation_billing_ownership.assert_called_once()


def test_accept_capacity_reservation_billing_ownership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_capacity_reservation_billing_ownership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_capacity_reservation_billing_ownership",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept capacity reservation billing ownership"):
        accept_capacity_reservation_billing_ownership("test-capacity_reservation_id", region_name=REGION)


def test_accept_reserved_instances_exchange_quote(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_reserved_instances_exchange_quote.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_reserved_instances_exchange_quote([], region_name=REGION)
    mock_client.accept_reserved_instances_exchange_quote.assert_called_once()


def test_accept_reserved_instances_exchange_quote_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_reserved_instances_exchange_quote.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_reserved_instances_exchange_quote",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept reserved instances exchange quote"):
        accept_reserved_instances_exchange_quote([], region_name=REGION)


def test_accept_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_transit_gateway_multicast_domain_associations(region_name=REGION)
    mock_client.accept_transit_gateway_multicast_domain_associations.assert_called_once()


def test_accept_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_multicast_domain_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_transit_gateway_multicast_domain_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept transit gateway multicast domain associations"):
        accept_transit_gateway_multicast_domain_associations(region_name=REGION)


def test_accept_transit_gateway_peering_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_peering_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.accept_transit_gateway_peering_attachment.assert_called_once()


def test_accept_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_peering_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_transit_gateway_peering_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept transit gateway peering attachment"):
        accept_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_accept_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.accept_transit_gateway_vpc_attachment.assert_called_once()


def test_accept_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_vpc_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_transit_gateway_vpc_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept transit gateway vpc attachment"):
        accept_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_accept_vpc_endpoint_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_vpc_endpoint_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_vpc_endpoint_connections("test-service_id", [], region_name=REGION)
    mock_client.accept_vpc_endpoint_connections.assert_called_once()


def test_accept_vpc_endpoint_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_vpc_endpoint_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_vpc_endpoint_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept vpc endpoint connections"):
        accept_vpc_endpoint_connections("test-service_id", [], region_name=REGION)


def test_accept_vpc_peering_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_vpc_peering_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)
    mock_client.accept_vpc_peering_connection.assert_called_once()


def test_accept_vpc_peering_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_vpc_peering_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_vpc_peering_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept vpc peering connection"):
        accept_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)


def test_advertise_byoip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.advertise_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    advertise_byoip_cidr("test-cidr", region_name=REGION)
    mock_client.advertise_byoip_cidr.assert_called_once()


def test_advertise_byoip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.advertise_byoip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "advertise_byoip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to advertise byoip cidr"):
        advertise_byoip_cidr("test-cidr", region_name=REGION)


def test_allocate_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_address(region_name=REGION)
    mock_client.allocate_address.assert_called_once()


def test_allocate_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "allocate_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to allocate address"):
        allocate_address(region_name=REGION)


def test_allocate_hosts(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_hosts(region_name=REGION)
    mock_client.allocate_hosts.assert_called_once()


def test_allocate_hosts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_hosts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "allocate_hosts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to allocate hosts"):
        allocate_hosts(region_name=REGION)


def test_allocate_ipam_pool_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)
    mock_client.allocate_ipam_pool_cidr.assert_called_once()


def test_allocate_ipam_pool_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.allocate_ipam_pool_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "allocate_ipam_pool_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to allocate ipam pool cidr"):
        allocate_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)


def test_apply_security_groups_to_client_vpn_target_network(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_security_groups_to_client_vpn_target_network.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    apply_security_groups_to_client_vpn_target_network("test-client_vpn_endpoint_id", "test-vpc_id", [], region_name=REGION)
    mock_client.apply_security_groups_to_client_vpn_target_network.assert_called_once()


def test_apply_security_groups_to_client_vpn_target_network_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_security_groups_to_client_vpn_target_network.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_security_groups_to_client_vpn_target_network",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to apply security groups to client vpn target network"):
        apply_security_groups_to_client_vpn_target_network("test-client_vpn_endpoint_id", "test-vpc_id", [], region_name=REGION)


def test_assign_ipv6_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_ipv6_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_ipv6_addresses("test-network_interface_id", region_name=REGION)
    mock_client.assign_ipv6_addresses.assert_called_once()


def test_assign_ipv6_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_ipv6_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assign_ipv6_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assign ipv6 addresses"):
        assign_ipv6_addresses("test-network_interface_id", region_name=REGION)


def test_assign_private_ip_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_private_ip_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_private_ip_addresses("test-network_interface_id", region_name=REGION)
    mock_client.assign_private_ip_addresses.assert_called_once()


def test_assign_private_ip_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_private_ip_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assign_private_ip_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assign private ip addresses"):
        assign_private_ip_addresses("test-network_interface_id", region_name=REGION)


def test_assign_private_nat_gateway_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_private_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_private_nat_gateway_address("test-nat_gateway_id", region_name=REGION)
    mock_client.assign_private_nat_gateway_address.assert_called_once()


def test_assign_private_nat_gateway_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_private_nat_gateway_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assign_private_nat_gateway_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assign private nat gateway address"):
        assign_private_nat_gateway_address("test-nat_gateway_id", region_name=REGION)


def test_associate_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_address(region_name=REGION)
    mock_client.associate_address.assert_called_once()


def test_associate_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate address"):
        associate_address(region_name=REGION)


def test_associate_capacity_reservation_billing_owner(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_capacity_reservation_billing_owner.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", region_name=REGION)
    mock_client.associate_capacity_reservation_billing_owner.assert_called_once()


def test_associate_capacity_reservation_billing_owner_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_capacity_reservation_billing_owner.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_capacity_reservation_billing_owner",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate capacity reservation billing owner"):
        associate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", region_name=REGION)


def test_associate_client_vpn_target_network(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_client_vpn_target_network.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", region_name=REGION)
    mock_client.associate_client_vpn_target_network.assert_called_once()


def test_associate_client_vpn_target_network_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_client_vpn_target_network.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_client_vpn_target_network",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate client vpn target network"):
        associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", region_name=REGION)


def test_associate_dhcp_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_dhcp_options("test-dhcp_options_id", "test-vpc_id", region_name=REGION)
    mock_client.associate_dhcp_options.assert_called_once()


def test_associate_dhcp_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_dhcp_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_dhcp_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate dhcp options"):
        associate_dhcp_options("test-dhcp_options_id", "test-vpc_id", region_name=REGION)


def test_associate_enclave_certificate_iam_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_enclave_certificate_iam_role.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", region_name=REGION)
    mock_client.associate_enclave_certificate_iam_role.assert_called_once()


def test_associate_enclave_certificate_iam_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_enclave_certificate_iam_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_enclave_certificate_iam_role",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate enclave certificate iam role"):
        associate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", region_name=REGION)


def test_associate_iam_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_iam_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_iam_instance_profile({}, "test-instance_id", region_name=REGION)
    mock_client.associate_iam_instance_profile.assert_called_once()


def test_associate_iam_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_iam_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_iam_instance_profile",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate iam instance profile"):
        associate_iam_instance_profile({}, "test-instance_id", region_name=REGION)


def test_associate_instance_event_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_instance_event_window("test-instance_event_window_id", {}, region_name=REGION)
    mock_client.associate_instance_event_window.assert_called_once()


def test_associate_instance_event_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_instance_event_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_instance_event_window",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate instance event window"):
        associate_instance_event_window("test-instance_event_window_id", {}, region_name=REGION)


def test_associate_ipam_byoasn(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_ipam_byoasn("test-asn", "test-cidr", region_name=REGION)
    mock_client.associate_ipam_byoasn.assert_called_once()


def test_associate_ipam_byoasn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ipam_byoasn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_ipam_byoasn",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate ipam byoasn"):
        associate_ipam_byoasn("test-asn", "test-cidr", region_name=REGION)


def test_associate_ipam_resource_discovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", region_name=REGION)
    mock_client.associate_ipam_resource_discovery.assert_called_once()


def test_associate_ipam_resource_discovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ipam_resource_discovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_ipam_resource_discovery",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate ipam resource discovery"):
        associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", region_name=REGION)


def test_associate_nat_gateway_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)
    mock_client.associate_nat_gateway_address.assert_called_once()


def test_associate_nat_gateway_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_nat_gateway_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_nat_gateway_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate nat gateway address"):
        associate_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)


def test_associate_route_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_route_server("test-route_server_id", "test-vpc_id", region_name=REGION)
    mock_client.associate_route_server.assert_called_once()


def test_associate_route_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_route_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_route_server",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate route server"):
        associate_route_server("test-route_server_id", "test-vpc_id", region_name=REGION)


def test_associate_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_route_table("test-route_table_id", region_name=REGION)
    mock_client.associate_route_table.assert_called_once()


def test_associate_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate route table"):
        associate_route_table("test-route_table_id", region_name=REGION)


def test_associate_security_group_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_security_group_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_security_group_vpc("test-group_id", "test-vpc_id", region_name=REGION)
    mock_client.associate_security_group_vpc.assert_called_once()


def test_associate_security_group_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_security_group_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_security_group_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate security group vpc"):
        associate_security_group_vpc("test-group_id", "test-vpc_id", region_name=REGION)


def test_associate_subnet_cidr_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_subnet_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_subnet_cidr_block("test-subnet_id", region_name=REGION)
    mock_client.associate_subnet_cidr_block.assert_called_once()


def test_associate_subnet_cidr_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_subnet_cidr_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_subnet_cidr_block",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate subnet cidr block"):
        associate_subnet_cidr_block("test-subnet_id", region_name=REGION)


def test_associate_transit_gateway_multicast_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_multicast_domain.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], region_name=REGION)
    mock_client.associate_transit_gateway_multicast_domain.assert_called_once()


def test_associate_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_multicast_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_transit_gateway_multicast_domain",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate transit gateway multicast domain"):
        associate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], region_name=REGION)


def test_associate_transit_gateway_policy_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_policy_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.associate_transit_gateway_policy_table.assert_called_once()


def test_associate_transit_gateway_policy_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_policy_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_transit_gateway_policy_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate transit gateway policy table"):
        associate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", region_name=REGION)


def test_associate_transit_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.associate_transit_gateway_route_table.assert_called_once()


def test_associate_transit_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_transit_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_transit_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate transit gateway route table"):
        associate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", region_name=REGION)


def test_associate_trunk_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_trunk_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", region_name=REGION)
    mock_client.associate_trunk_interface.assert_called_once()


def test_associate_trunk_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_trunk_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_trunk_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate trunk interface"):
        associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", region_name=REGION)


def test_associate_vpc_cidr_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_vpc_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_vpc_cidr_block("test-vpc_id", region_name=REGION)
    mock_client.associate_vpc_cidr_block.assert_called_once()


def test_associate_vpc_cidr_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_vpc_cidr_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_vpc_cidr_block",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate vpc cidr block"):
        associate_vpc_cidr_block("test-vpc_id", region_name=REGION)


def test_attach_classic_link_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_classic_link_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_classic_link_vpc("test-instance_id", "test-vpc_id", [], region_name=REGION)
    mock_client.attach_classic_link_vpc.assert_called_once()


def test_attach_classic_link_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_classic_link_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_classic_link_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach classic link vpc"):
        attach_classic_link_vpc("test-instance_id", "test-vpc_id", [], region_name=REGION)


def test_attach_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_internet_gateway("test-internet_gateway_id", "test-vpc_id", region_name=REGION)
    mock_client.attach_internet_gateway.assert_called_once()


def test_attach_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach internet gateway"):
        attach_internet_gateway("test-internet_gateway_id", "test-vpc_id", region_name=REGION)


def test_attach_network_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_network_interface("test-network_interface_id", "test-instance_id", 1, region_name=REGION)
    mock_client.attach_network_interface.assert_called_once()


def test_attach_network_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_network_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_network_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach network interface"):
        attach_network_interface("test-network_interface_id", "test-instance_id", 1, region_name=REGION)


def test_attach_verified_access_trust_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", region_name=REGION)
    mock_client.attach_verified_access_trust_provider.assert_called_once()


def test_attach_verified_access_trust_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_verified_access_trust_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_verified_access_trust_provider",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach verified access trust provider"):
        attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", region_name=REGION)


def test_attach_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_volume("test-device", "test-instance_id", "test-volume_id", region_name=REGION)
    mock_client.attach_volume.assert_called_once()


def test_attach_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach volume"):
        attach_volume("test-device", "test-instance_id", "test-volume_id", region_name=REGION)


def test_attach_vpn_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_vpn_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", region_name=REGION)
    mock_client.attach_vpn_gateway.assert_called_once()


def test_attach_vpn_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_vpn_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_vpn_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach vpn gateway"):
        attach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", region_name=REGION)


def test_authorize_client_vpn_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_client_vpn_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", region_name=REGION)
    mock_client.authorize_client_vpn_ingress.assert_called_once()


def test_authorize_client_vpn_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_client_vpn_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_client_vpn_ingress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize client vpn ingress"):
        authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", region_name=REGION)


def test_authorize_security_group_egress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_security_group_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_security_group_egress("test-group_id", region_name=REGION)
    mock_client.authorize_security_group_egress.assert_called_once()


def test_authorize_security_group_egress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_security_group_egress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_security_group_egress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize security group egress"):
        authorize_security_group_egress("test-group_id", region_name=REGION)


def test_authorize_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_security_group_ingress(region_name=REGION)
    mock_client.authorize_security_group_ingress.assert_called_once()


def test_authorize_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize security group ingress"):
        authorize_security_group_ingress(region_name=REGION)


def test_bundle_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.bundle_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    bundle_instance("test-instance_id", {}, region_name=REGION)
    mock_client.bundle_instance.assert_called_once()


def test_bundle_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.bundle_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "bundle_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to bundle instance"):
        bundle_instance("test-instance_id", {}, region_name=REGION)


def test_cancel_bundle_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_bundle_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_bundle_task("test-bundle_id", region_name=REGION)
    mock_client.cancel_bundle_task.assert_called_once()


def test_cancel_bundle_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_bundle_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_bundle_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel bundle task"):
        cancel_bundle_task("test-bundle_id", region_name=REGION)


def test_cancel_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_capacity_reservation("test-capacity_reservation_id", region_name=REGION)
    mock_client.cancel_capacity_reservation.assert_called_once()


def test_cancel_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel capacity reservation"):
        cancel_capacity_reservation("test-capacity_reservation_id", region_name=REGION)


def test_cancel_capacity_reservation_fleets(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_capacity_reservation_fleets([], region_name=REGION)
    mock_client.cancel_capacity_reservation_fleets.assert_called_once()


def test_cancel_capacity_reservation_fleets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_capacity_reservation_fleets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel capacity reservation fleets"):
        cancel_capacity_reservation_fleets([], region_name=REGION)


def test_cancel_conversion_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_conversion_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_conversion_task("test-conversion_task_id", region_name=REGION)
    mock_client.cancel_conversion_task.assert_called_once()


def test_cancel_conversion_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_conversion_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_conversion_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel conversion task"):
        cancel_conversion_task("test-conversion_task_id", region_name=REGION)


def test_cancel_declarative_policies_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_declarative_policies_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_declarative_policies_report("test-report_id", region_name=REGION)
    mock_client.cancel_declarative_policies_report.assert_called_once()


def test_cancel_declarative_policies_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_declarative_policies_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_declarative_policies_report",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel declarative policies report"):
        cancel_declarative_policies_report("test-report_id", region_name=REGION)


def test_cancel_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_export_task("test-export_task_id", region_name=REGION)
    mock_client.cancel_export_task.assert_called_once()


def test_cancel_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_export_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel export task"):
        cancel_export_task("test-export_task_id", region_name=REGION)


def test_cancel_image_launch_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_image_launch_permission.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_image_launch_permission("test-image_id", region_name=REGION)
    mock_client.cancel_image_launch_permission.assert_called_once()


def test_cancel_image_launch_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_image_launch_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_image_launch_permission",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel image launch permission"):
        cancel_image_launch_permission("test-image_id", region_name=REGION)


def test_cancel_import_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_import_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_import_task(region_name=REGION)
    mock_client.cancel_import_task.assert_called_once()


def test_cancel_import_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_import_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_import_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel import task"):
        cancel_import_task(region_name=REGION)


def test_cancel_reserved_instances_listing(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_reserved_instances_listing.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_reserved_instances_listing("test-reserved_instances_listing_id", region_name=REGION)
    mock_client.cancel_reserved_instances_listing.assert_called_once()


def test_cancel_reserved_instances_listing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_reserved_instances_listing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_reserved_instances_listing",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel reserved instances listing"):
        cancel_reserved_instances_listing("test-reserved_instances_listing_id", region_name=REGION)


def test_cancel_spot_fleet_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_spot_fleet_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_spot_fleet_requests([], True, region_name=REGION)
    mock_client.cancel_spot_fleet_requests.assert_called_once()


def test_cancel_spot_fleet_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_spot_fleet_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_spot_fleet_requests",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel spot fleet requests"):
        cancel_spot_fleet_requests([], True, region_name=REGION)


def test_cancel_spot_instance_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_spot_instance_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_spot_instance_requests([], region_name=REGION)
    mock_client.cancel_spot_instance_requests.assert_called_once()


def test_cancel_spot_instance_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_spot_instance_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_spot_instance_requests",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel spot instance requests"):
        cancel_spot_instance_requests([], region_name=REGION)


def test_confirm_product_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_product_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    confirm_product_instance("test-instance_id", "test-product_code", region_name=REGION)
    mock_client.confirm_product_instance.assert_called_once()


def test_confirm_product_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_product_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_product_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to confirm product instance"):
        confirm_product_instance("test-instance_id", "test-product_code", region_name=REGION)


def test_copy_fpga_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_fpga_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_fpga_image("test-source_fpga_image_id", "test-source_region", region_name=REGION)
    mock_client.copy_fpga_image.assert_called_once()


def test_copy_fpga_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_fpga_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_fpga_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy fpga image"):
        copy_fpga_image("test-source_fpga_image_id", "test-source_region", region_name=REGION)


def test_copy_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_image("test-name", "test-source_image_id", "test-source_region", region_name=REGION)
    mock_client.copy_image.assert_called_once()


def test_copy_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy image"):
        copy_image("test-name", "test-source_image_id", "test-source_region", region_name=REGION)


def test_copy_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_snapshot("test-source_region", "test-source_snapshot_id", region_name=REGION)
    mock_client.copy_snapshot.assert_called_once()


def test_copy_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy snapshot"):
        copy_snapshot("test-source_region", "test-source_snapshot_id", region_name=REGION)


def test_copy_volumes(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_volumes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_volumes("test-source_volume_id", region_name=REGION)
    mock_client.copy_volumes.assert_called_once()


def test_copy_volumes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_volumes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_volumes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy volumes"):
        copy_volumes("test-source_volume_id", region_name=REGION)


def test_create_capacity_manager_data_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_manager_data_export.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", region_name=REGION)
    mock_client.create_capacity_manager_data_export.assert_called_once()


def test_create_capacity_manager_data_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_manager_data_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_manager_data_export",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity manager data export"):
        create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", region_name=REGION)


def test_create_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation("test-instance_type", "test-instance_platform", 1, region_name=REGION)
    mock_client.create_capacity_reservation.assert_called_once()


def test_create_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity reservation"):
        create_capacity_reservation("test-instance_type", "test-instance_platform", 1, region_name=REGION)


def test_create_capacity_reservation_by_splitting(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_by_splitting.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, region_name=REGION)
    mock_client.create_capacity_reservation_by_splitting.assert_called_once()


def test_create_capacity_reservation_by_splitting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_by_splitting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_reservation_by_splitting",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity reservation by splitting"):
        create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, region_name=REGION)


def test_create_capacity_reservation_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation_fleet([], 1, region_name=REGION)
    mock_client.create_capacity_reservation_fleet.assert_called_once()


def test_create_capacity_reservation_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_reservation_fleet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity reservation fleet"):
        create_capacity_reservation_fleet([], 1, region_name=REGION)


def test_create_carrier_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_carrier_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_carrier_gateway("test-vpc_id", region_name=REGION)
    mock_client.create_carrier_gateway.assert_called_once()


def test_create_carrier_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_carrier_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_carrier_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create carrier gateway"):
        create_carrier_gateway("test-vpc_id", region_name=REGION)


def test_create_client_vpn_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_client_vpn_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_client_vpn_endpoint("test-server_certificate_arn", [], {}, region_name=REGION)
    mock_client.create_client_vpn_endpoint.assert_called_once()


def test_create_client_vpn_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_client_vpn_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_client_vpn_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create client vpn endpoint"):
        create_client_vpn_endpoint("test-server_certificate_arn", [], {}, region_name=REGION)


def test_create_client_vpn_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_client_vpn_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", region_name=REGION)
    mock_client.create_client_vpn_route.assert_called_once()


def test_create_client_vpn_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_client_vpn_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_client_vpn_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create client vpn route"):
        create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", region_name=REGION)


def test_create_coip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_coip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_coip_cidr("test-cidr", "test-coip_pool_id", region_name=REGION)
    mock_client.create_coip_cidr.assert_called_once()


def test_create_coip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_coip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_coip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create coip cidr"):
        create_coip_cidr("test-cidr", "test-coip_pool_id", region_name=REGION)


def test_create_coip_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_coip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_coip_pool("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.create_coip_pool.assert_called_once()


def test_create_coip_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_coip_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_coip_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create coip pool"):
        create_coip_pool("test-local_gateway_route_table_id", region_name=REGION)


def test_create_customer_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_customer_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_customer_gateway("test-type_value", region_name=REGION)
    mock_client.create_customer_gateway.assert_called_once()


def test_create_customer_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_customer_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_customer_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create customer gateway"):
        create_customer_gateway("test-type_value", region_name=REGION)


def test_create_default_subnet(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_default_subnet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_default_subnet(region_name=REGION)
    mock_client.create_default_subnet.assert_called_once()


def test_create_default_subnet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_default_subnet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_default_subnet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create default subnet"):
        create_default_subnet(region_name=REGION)


def test_create_default_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_default_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_default_vpc(region_name=REGION)
    mock_client.create_default_vpc.assert_called_once()


def test_create_default_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_default_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_default_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create default vpc"):
        create_default_vpc(region_name=REGION)


def test_create_delegate_mac_volume_ownership_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delegate_mac_volume_ownership_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", region_name=REGION)
    mock_client.create_delegate_mac_volume_ownership_task.assert_called_once()


def test_create_delegate_mac_volume_ownership_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delegate_mac_volume_ownership_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_delegate_mac_volume_ownership_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create delegate mac volume ownership task"):
        create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", region_name=REGION)


def test_create_dhcp_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_dhcp_options([], region_name=REGION)
    mock_client.create_dhcp_options.assert_called_once()


def test_create_dhcp_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dhcp_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dhcp_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dhcp options"):
        create_dhcp_options([], region_name=REGION)


def test_create_egress_only_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_egress_only_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_egress_only_internet_gateway("test-vpc_id", region_name=REGION)
    mock_client.create_egress_only_internet_gateway.assert_called_once()


def test_create_egress_only_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_egress_only_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_egress_only_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create egress only internet gateway"):
        create_egress_only_internet_gateway("test-vpc_id", region_name=REGION)


def test_create_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_fleet([], {}, region_name=REGION)
    mock_client.create_fleet.assert_called_once()


def test_create_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_fleet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create fleet"):
        create_fleet([], {}, region_name=REGION)


def test_create_flow_logs(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_logs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_flow_logs([], "test-resource_type", region_name=REGION)
    mock_client.create_flow_logs.assert_called_once()


def test_create_flow_logs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_flow_logs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_flow_logs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create flow logs"):
        create_flow_logs([], "test-resource_type", region_name=REGION)


def test_create_fpga_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_fpga_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_fpga_image({}, region_name=REGION)
    mock_client.create_fpga_image.assert_called_once()


def test_create_fpga_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_fpga_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_fpga_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create fpga image"):
        create_fpga_image({}, region_name=REGION)


def test_create_image_usage_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_image_usage_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_image_usage_report("test-image_id", [], region_name=REGION)
    mock_client.create_image_usage_report.assert_called_once()


def test_create_image_usage_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_image_usage_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_image_usage_report",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create image usage report"):
        create_image_usage_report("test-image_id", [], region_name=REGION)


def test_create_instance_connect_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_connect_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_connect_endpoint("test-subnet_id", region_name=REGION)
    mock_client.create_instance_connect_endpoint.assert_called_once()


def test_create_instance_connect_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_connect_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_connect_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create instance connect endpoint"):
        create_instance_connect_endpoint("test-subnet_id", region_name=REGION)


def test_create_instance_event_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_event_window(region_name=REGION)
    mock_client.create_instance_event_window.assert_called_once()


def test_create_instance_event_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_event_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_event_window",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create instance event window"):
        create_instance_event_window(region_name=REGION)


def test_create_instance_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_export_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_export_task("test-instance_id", "test-target_environment", {}, region_name=REGION)
    mock_client.create_instance_export_task.assert_called_once()


def test_create_instance_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_export_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create instance export task"):
        create_instance_export_task("test-instance_id", "test-target_environment", {}, region_name=REGION)


def test_create_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_internet_gateway(region_name=REGION)
    mock_client.create_internet_gateway.assert_called_once()


def test_create_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create internet gateway"):
        create_internet_gateway(region_name=REGION)


def test_create_ipam(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam(region_name=REGION)
    mock_client.create_ipam.assert_called_once()


def test_create_ipam_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam"):
        create_ipam(region_name=REGION)


def test_create_ipam_external_resource_verification_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_external_resource_verification_token.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_external_resource_verification_token("test-ipam_id", region_name=REGION)
    mock_client.create_ipam_external_resource_verification_token.assert_called_once()


def test_create_ipam_external_resource_verification_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_external_resource_verification_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_external_resource_verification_token",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam external resource verification token"):
        create_ipam_external_resource_verification_token("test-ipam_id", region_name=REGION)


def test_create_ipam_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_pool("test-ipam_scope_id", "test-address_family", region_name=REGION)
    mock_client.create_ipam_pool.assert_called_once()


def test_create_ipam_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam pool"):
        create_ipam_pool("test-ipam_scope_id", "test-address_family", region_name=REGION)


def test_create_ipam_prefix_list_resolver(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", region_name=REGION)
    mock_client.create_ipam_prefix_list_resolver.assert_called_once()


def test_create_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_prefix_list_resolver",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam prefix list resolver"):
        create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", region_name=REGION)


def test_create_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", True, region_name=REGION)
    mock_client.create_ipam_prefix_list_resolver_target.assert_called_once()


def test_create_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_prefix_list_resolver_target",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam prefix list resolver target"):
        create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", True, region_name=REGION)


def test_create_ipam_resource_discovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_resource_discovery(region_name=REGION)
    mock_client.create_ipam_resource_discovery.assert_called_once()


def test_create_ipam_resource_discovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_resource_discovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_resource_discovery",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam resource discovery"):
        create_ipam_resource_discovery(region_name=REGION)


def test_create_ipam_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_scope("test-ipam_id", region_name=REGION)
    mock_client.create_ipam_scope.assert_called_once()


def test_create_ipam_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ipam_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ipam_scope",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ipam scope"):
        create_ipam_scope("test-ipam_id", region_name=REGION)


def test_create_key_pair(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_key_pair("test-key_name", region_name=REGION)
    mock_client.create_key_pair.assert_called_once()


def test_create_key_pair_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key_pair",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create key pair"):
        create_key_pair("test-key_name", region_name=REGION)


def test_create_launch_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_launch_template("test-launch_template_name", {}, region_name=REGION)
    mock_client.create_launch_template.assert_called_once()


def test_create_launch_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_launch_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_launch_template",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create launch template"):
        create_launch_template("test-launch_template_name", {}, region_name=REGION)


def test_create_launch_template_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_launch_template_version.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_launch_template_version({}, region_name=REGION)
    mock_client.create_launch_template_version.assert_called_once()


def test_create_launch_template_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_launch_template_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_launch_template_version",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create launch template version"):
        create_launch_template_version({}, region_name=REGION)


def test_create_local_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.create_local_gateway_route.assert_called_once()


def test_create_local_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway route"):
        create_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)


def test_create_local_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table("test-local_gateway_id", region_name=REGION)
    mock_client.create_local_gateway_route_table.assert_called_once()


def test_create_local_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway route table"):
        create_local_gateway_route_table("test-local_gateway_id", region_name=REGION)


def test_create_local_gateway_route_table_virtual_interface_group_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_virtual_interface_group_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", region_name=REGION)
    mock_client.create_local_gateway_route_table_virtual_interface_group_association.assert_called_once()


def test_create_local_gateway_route_table_virtual_interface_group_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_virtual_interface_group_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_route_table_virtual_interface_group_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway route table virtual interface group association"):
        create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", region_name=REGION)


def test_create_local_gateway_route_table_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", region_name=REGION)
    mock_client.create_local_gateway_route_table_vpc_association.assert_called_once()


def test_create_local_gateway_route_table_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_route_table_vpc_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway route table vpc association"):
        create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", region_name=REGION)


def test_create_local_gateway_virtual_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", 1, "test-local_address", "test-peer_address", region_name=REGION)
    mock_client.create_local_gateway_virtual_interface.assert_called_once()


def test_create_local_gateway_virtual_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_virtual_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway virtual interface"):
        create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", 1, "test-local_address", "test-peer_address", region_name=REGION)


def test_create_local_gateway_virtual_interface_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_virtual_interface_group("test-local_gateway_id", region_name=REGION)
    mock_client.create_local_gateway_virtual_interface_group.assert_called_once()


def test_create_local_gateway_virtual_interface_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_local_gateway_virtual_interface_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create local gateway virtual interface group"):
        create_local_gateway_virtual_interface_group("test-local_gateway_id", region_name=REGION)


def test_create_mac_system_integrity_protection_modification_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_mac_system_integrity_protection_modification_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", region_name=REGION)
    mock_client.create_mac_system_integrity_protection_modification_task.assert_called_once()


def test_create_mac_system_integrity_protection_modification_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_mac_system_integrity_protection_modification_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_mac_system_integrity_protection_modification_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create mac system integrity protection modification task"):
        create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", region_name=REGION)


def test_create_managed_prefix_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_managed_prefix_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", region_name=REGION)
    mock_client.create_managed_prefix_list.assert_called_once()


def test_create_managed_prefix_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_managed_prefix_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_managed_prefix_list",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create managed prefix list"):
        create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", region_name=REGION)


def test_create_nat_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_nat_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_nat_gateway("test-subnet_id", region_name=REGION)
    mock_client.create_nat_gateway.assert_called_once()


def test_create_nat_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_nat_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_nat_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create nat gateway"):
        create_nat_gateway("test-subnet_id", region_name=REGION)


def test_create_network_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_acl.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_acl("test-vpc_id", region_name=REGION)
    mock_client.create_network_acl.assert_called_once()


def test_create_network_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_acl",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network acl"):
        create_network_acl("test-vpc_id", region_name=REGION)


def test_create_network_acl_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_acl_entry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, region_name=REGION)
    mock_client.create_network_acl_entry.assert_called_once()


def test_create_network_acl_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_acl_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_acl_entry",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network acl entry"):
        create_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, region_name=REGION)


def test_create_network_insights_access_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_insights_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_insights_access_scope("test-client_token", region_name=REGION)
    mock_client.create_network_insights_access_scope.assert_called_once()


def test_create_network_insights_access_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_insights_access_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_insights_access_scope",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network insights access scope"):
        create_network_insights_access_scope("test-client_token", region_name=REGION)


def test_create_network_insights_path(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_insights_path.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_insights_path("test-source", "test-protocol", "test-client_token", region_name=REGION)
    mock_client.create_network_insights_path.assert_called_once()


def test_create_network_insights_path_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_insights_path.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_insights_path",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network insights path"):
        create_network_insights_path("test-source", "test-protocol", "test-client_token", region_name=REGION)


def test_create_network_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_interface("test-subnet_id", region_name=REGION)
    mock_client.create_network_interface.assert_called_once()


def test_create_network_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network interface"):
        create_network_interface("test-subnet_id", region_name=REGION)


def test_create_network_interface_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_interface_permission.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_interface_permission("test-network_interface_id", "test-permission", region_name=REGION)
    mock_client.create_network_interface_permission.assert_called_once()


def test_create_network_interface_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_network_interface_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_network_interface_permission",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create network interface permission"):
        create_network_interface_permission("test-network_interface_id", "test-permission", region_name=REGION)


def test_create_placement_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_placement_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_placement_group(region_name=REGION)
    mock_client.create_placement_group.assert_called_once()


def test_create_placement_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_placement_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_placement_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create placement group"):
        create_placement_group(region_name=REGION)


def test_create_public_ipv4_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_public_ipv4_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_public_ipv4_pool(region_name=REGION)
    mock_client.create_public_ipv4_pool.assert_called_once()


def test_create_public_ipv4_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_public_ipv4_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_public_ipv4_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create public ipv4 pool"):
        create_public_ipv4_pool(region_name=REGION)


def test_create_replace_root_volume_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replace_root_volume_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_replace_root_volume_task("test-instance_id", region_name=REGION)
    mock_client.create_replace_root_volume_task.assert_called_once()


def test_create_replace_root_volume_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replace_root_volume_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_replace_root_volume_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create replace root volume task"):
        create_replace_root_volume_task("test-instance_id", region_name=REGION)


def test_create_reserved_instances_listing(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reserved_instances_listing.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_reserved_instances_listing("test-reserved_instances_id", 1, [], "test-client_token", region_name=REGION)
    mock_client.create_reserved_instances_listing.assert_called_once()


def test_create_reserved_instances_listing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reserved_instances_listing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_reserved_instances_listing",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create reserved instances listing"):
        create_reserved_instances_listing("test-reserved_instances_id", 1, [], "test-client_token", region_name=REGION)


def test_create_restore_image_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_restore_image_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_restore_image_task("test-bucket", "test-object_key", region_name=REGION)
    mock_client.create_restore_image_task.assert_called_once()


def test_create_restore_image_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_restore_image_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_restore_image_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create restore image task"):
        create_restore_image_task("test-bucket", "test-object_key", region_name=REGION)


def test_create_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route("test-route_table_id", region_name=REGION)
    mock_client.create_route.assert_called_once()


def test_create_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create route"):
        create_route("test-route_table_id", region_name=REGION)


def test_create_route_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server(1, region_name=REGION)
    mock_client.create_route_server.assert_called_once()


def test_create_route_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_route_server",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create route server"):
        create_route_server(1, region_name=REGION)


def test_create_route_server_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server_endpoint("test-route_server_id", "test-subnet_id", region_name=REGION)
    mock_client.create_route_server_endpoint.assert_called_once()


def test_create_route_server_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_route_server_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create route server endpoint"):
        create_route_server_endpoint("test-route_server_id", "test-subnet_id", region_name=REGION)


def test_create_route_server_peer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, region_name=REGION)
    mock_client.create_route_server_peer.assert_called_once()


def test_create_route_server_peer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_server_peer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_route_server_peer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create route server peer"):
        create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, region_name=REGION)


def test_create_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_table("test-vpc_id", region_name=REGION)
    mock_client.create_route_table.assert_called_once()


def test_create_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create route table"):
        create_route_table("test-vpc_id", region_name=REGION)


def test_create_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_security_group("test-description", "test-group_name", region_name=REGION)
    mock_client.create_security_group.assert_called_once()


def test_create_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_security_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create security group"):
        create_security_group("test-description", "test-group_name", region_name=REGION)


def test_create_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-volume_id", region_name=REGION)
    mock_client.create_snapshot.assert_called_once()


def test_create_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        create_snapshot("test-volume_id", region_name=REGION)


def test_create_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_snapshots({}, region_name=REGION)
    mock_client.create_snapshots.assert_called_once()


def test_create_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshots",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshots"):
        create_snapshots({}, region_name=REGION)


def test_create_spot_datafeed_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_spot_datafeed_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_spot_datafeed_subscription("test-bucket", region_name=REGION)
    mock_client.create_spot_datafeed_subscription.assert_called_once()


def test_create_spot_datafeed_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_spot_datafeed_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_spot_datafeed_subscription",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create spot datafeed subscription"):
        create_spot_datafeed_subscription("test-bucket", region_name=REGION)


def test_create_store_image_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_store_image_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_store_image_task("test-image_id", "test-bucket", region_name=REGION)
    mock_client.create_store_image_task.assert_called_once()


def test_create_store_image_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_store_image_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_store_image_task",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create store image task"):
        create_store_image_task("test-image_id", "test-bucket", region_name=REGION)


def test_create_subnet(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_subnet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_subnet("test-vpc_id", region_name=REGION)
    mock_client.create_subnet.assert_called_once()


def test_create_subnet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_subnet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_subnet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create subnet"):
        create_subnet("test-vpc_id", region_name=REGION)


def test_create_subnet_cidr_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_subnet_cidr_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", region_name=REGION)
    mock_client.create_subnet_cidr_reservation.assert_called_once()


def test_create_subnet_cidr_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_subnet_cidr_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_subnet_cidr_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create subnet cidr reservation"):
        create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", region_name=REGION)


def test_create_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_tags([], [], region_name=REGION)
    mock_client.create_tags.assert_called_once()


def test_create_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tags",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tags"):
        create_tags([], [], region_name=REGION)


def test_create_traffic_mirror_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_filter(region_name=REGION)
    mock_client.create_traffic_mirror_filter.assert_called_once()


def test_create_traffic_mirror_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_mirror_filter",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic mirror filter"):
        create_traffic_mirror_filter(region_name=REGION)


def test_create_traffic_mirror_filter_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter_rule.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", 1, "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", region_name=REGION)
    mock_client.create_traffic_mirror_filter_rule.assert_called_once()


def test_create_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_mirror_filter_rule",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic mirror filter rule"):
        create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", 1, "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", region_name=REGION)


def test_create_traffic_mirror_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_session.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", 1, region_name=REGION)
    mock_client.create_traffic_mirror_session.assert_called_once()


def test_create_traffic_mirror_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_mirror_session",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic mirror session"):
        create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", 1, region_name=REGION)


def test_create_traffic_mirror_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_target(region_name=REGION)
    mock_client.create_traffic_mirror_target.assert_called_once()


def test_create_traffic_mirror_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_mirror_target",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic mirror target"):
        create_traffic_mirror_target(region_name=REGION)


def test_create_transit_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway(region_name=REGION)
    mock_client.create_transit_gateway.assert_called_once()


def test_create_transit_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway"):
        create_transit_gateway(region_name=REGION)


def test_create_transit_gateway_connect(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_connect("test-transport_transit_gateway_attachment_id", {}, region_name=REGION)
    mock_client.create_transit_gateway_connect.assert_called_once()


def test_create_transit_gateway_connect_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_connect",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway connect"):
        create_transit_gateway_connect("test-transport_transit_gateway_attachment_id", {}, region_name=REGION)


def test_create_transit_gateway_connect_peer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", [], region_name=REGION)
    mock_client.create_transit_gateway_connect_peer.assert_called_once()


def test_create_transit_gateway_connect_peer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect_peer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_connect_peer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway connect peer"):
        create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", [], region_name=REGION)


def test_create_transit_gateway_multicast_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_multicast_domain.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_multicast_domain("test-transit_gateway_id", region_name=REGION)
    mock_client.create_transit_gateway_multicast_domain.assert_called_once()


def test_create_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_multicast_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_multicast_domain",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway multicast domain"):
        create_transit_gateway_multicast_domain("test-transit_gateway_id", region_name=REGION)


def test_create_transit_gateway_peering_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_peering_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", "test-peer_account_id", "test-peer_region", region_name=REGION)
    mock_client.create_transit_gateway_peering_attachment.assert_called_once()


def test_create_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_peering_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_peering_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway peering attachment"):
        create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", "test-peer_account_id", "test-peer_region", region_name=REGION)


def test_create_transit_gateway_policy_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_policy_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_policy_table("test-transit_gateway_id", region_name=REGION)
    mock_client.create_transit_gateway_policy_table.assert_called_once()


def test_create_transit_gateway_policy_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_policy_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_policy_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway policy table"):
        create_transit_gateway_policy_table("test-transit_gateway_id", region_name=REGION)


def test_create_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_prefix_list_reference.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)
    mock_client.create_transit_gateway_prefix_list_reference.assert_called_once()


def test_create_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_prefix_list_reference.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_prefix_list_reference",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway prefix list reference"):
        create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)


def test_create_transit_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.create_transit_gateway_route.assert_called_once()


def test_create_transit_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway route"):
        create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", region_name=REGION)


def test_create_transit_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route_table("test-transit_gateway_id", region_name=REGION)
    mock_client.create_transit_gateway_route_table.assert_called_once()


def test_create_transit_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway route table"):
        create_transit_gateway_route_table("test-transit_gateway_id", region_name=REGION)


def test_create_transit_gateway_route_table_announcement(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table_announcement.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", region_name=REGION)
    mock_client.create_transit_gateway_route_table_announcement.assert_called_once()


def test_create_transit_gateway_route_table_announcement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table_announcement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_route_table_announcement",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway route table announcement"):
        create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", region_name=REGION)


def test_create_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", [], region_name=REGION)
    mock_client.create_transit_gateway_vpc_attachment.assert_called_once()


def test_create_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_transit_gateway_vpc_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_transit_gateway_vpc_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create transit gateway vpc attachment"):
        create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", [], region_name=REGION)


def test_create_verified_access_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", region_name=REGION)
    mock_client.create_verified_access_endpoint.assert_called_once()


def test_create_verified_access_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_verified_access_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create verified access endpoint"):
        create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", region_name=REGION)


def test_create_verified_access_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_group("test-verified_access_instance_id", region_name=REGION)
    mock_client.create_verified_access_group.assert_called_once()


def test_create_verified_access_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_verified_access_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create verified access group"):
        create_verified_access_group("test-verified_access_instance_id", region_name=REGION)


def test_create_verified_access_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_instance(region_name=REGION)
    mock_client.create_verified_access_instance.assert_called_once()


def test_create_verified_access_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_verified_access_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create verified access instance"):
        create_verified_access_instance(region_name=REGION)


def test_create_verified_access_trust_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", region_name=REGION)
    mock_client.create_verified_access_trust_provider.assert_called_once()


def test_create_verified_access_trust_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_verified_access_trust_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_verified_access_trust_provider",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create verified access trust provider"):
        create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", region_name=REGION)


def test_create_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_volume(region_name=REGION)
    mock_client.create_volume.assert_called_once()


def test_create_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create volume"):
        create_volume(region_name=REGION)


def test_create_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc(region_name=REGION)
    mock_client.create_vpc.assert_called_once()


def test_create_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc"):
        create_vpc(region_name=REGION)


def test_create_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_block_public_access_exclusion.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", region_name=REGION)
    mock_client.create_vpc_block_public_access_exclusion.assert_called_once()


def test_create_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_block_public_access_exclusion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_block_public_access_exclusion",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc block public access exclusion"):
        create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", region_name=REGION)


def test_create_vpc_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint("test-vpc_id", region_name=REGION)
    mock_client.create_vpc_endpoint.assert_called_once()


def test_create_vpc_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc endpoint"):
        create_vpc_endpoint("test-vpc_id", region_name=REGION)


def test_create_vpc_endpoint_connection_notification(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_connection_notification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint_connection_notification("test-connection_notification_arn", [], region_name=REGION)
    mock_client.create_vpc_endpoint_connection_notification.assert_called_once()


def test_create_vpc_endpoint_connection_notification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_connection_notification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_endpoint_connection_notification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc endpoint connection notification"):
        create_vpc_endpoint_connection_notification("test-connection_notification_arn", [], region_name=REGION)


def test_create_vpc_endpoint_service_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_service_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint_service_configuration(region_name=REGION)
    mock_client.create_vpc_endpoint_service_configuration.assert_called_once()


def test_create_vpc_endpoint_service_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_service_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_endpoint_service_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc endpoint service configuration"):
        create_vpc_endpoint_service_configuration(region_name=REGION)


def test_create_vpc_peering_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_peering_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_peering_connection("test-vpc_id", region_name=REGION)
    mock_client.create_vpc_peering_connection.assert_called_once()


def test_create_vpc_peering_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_peering_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_peering_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc peering connection"):
        create_vpc_peering_connection("test-vpc_id", region_name=REGION)


def test_create_vpn_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpn_connection("test-customer_gateway_id", "test-type_value", region_name=REGION)
    mock_client.create_vpn_connection.assert_called_once()


def test_create_vpn_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpn_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpn connection"):
        create_vpn_connection("test-customer_gateway_id", "test-type_value", region_name=REGION)


def test_create_vpn_connection_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_connection_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", region_name=REGION)
    mock_client.create_vpn_connection_route.assert_called_once()


def test_create_vpn_connection_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_connection_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpn_connection_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpn connection route"):
        create_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", region_name=REGION)


def test_create_vpn_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpn_gateway("test-type_value", region_name=REGION)
    mock_client.create_vpn_gateway.assert_called_once()


def test_create_vpn_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpn_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpn_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpn gateway"):
        create_vpn_gateway("test-type_value", region_name=REGION)


def test_delete_capacity_manager_data_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_manager_data_export.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_capacity_manager_data_export("test-capacity_manager_data_export_id", region_name=REGION)
    mock_client.delete_capacity_manager_data_export.assert_called_once()


def test_delete_capacity_manager_data_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_manager_data_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_capacity_manager_data_export",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete capacity manager data export"):
        delete_capacity_manager_data_export("test-capacity_manager_data_export_id", region_name=REGION)


def test_delete_carrier_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_carrier_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_carrier_gateway("test-carrier_gateway_id", region_name=REGION)
    mock_client.delete_carrier_gateway.assert_called_once()


def test_delete_carrier_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_carrier_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_carrier_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete carrier gateway"):
        delete_carrier_gateway("test-carrier_gateway_id", region_name=REGION)


def test_delete_client_vpn_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_vpn_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_client_vpn_endpoint("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.delete_client_vpn_endpoint.assert_called_once()


def test_delete_client_vpn_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_vpn_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_client_vpn_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete client vpn endpoint"):
        delete_client_vpn_endpoint("test-client_vpn_endpoint_id", region_name=REGION)


def test_delete_client_vpn_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_vpn_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", region_name=REGION)
    mock_client.delete_client_vpn_route.assert_called_once()


def test_delete_client_vpn_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_vpn_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_client_vpn_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete client vpn route"):
        delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", region_name=REGION)


def test_delete_coip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_coip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_coip_cidr("test-cidr", "test-coip_pool_id", region_name=REGION)
    mock_client.delete_coip_cidr.assert_called_once()


def test_delete_coip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_coip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_coip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete coip cidr"):
        delete_coip_cidr("test-cidr", "test-coip_pool_id", region_name=REGION)


def test_delete_coip_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_coip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_coip_pool("test-coip_pool_id", region_name=REGION)
    mock_client.delete_coip_pool.assert_called_once()


def test_delete_coip_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_coip_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_coip_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete coip pool"):
        delete_coip_pool("test-coip_pool_id", region_name=REGION)


def test_delete_customer_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_customer_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_customer_gateway("test-customer_gateway_id", region_name=REGION)
    mock_client.delete_customer_gateway.assert_called_once()


def test_delete_customer_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_customer_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_customer_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete customer gateway"):
        delete_customer_gateway("test-customer_gateway_id", region_name=REGION)


def test_delete_dhcp_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_dhcp_options("test-dhcp_options_id", region_name=REGION)
    mock_client.delete_dhcp_options.assert_called_once()


def test_delete_dhcp_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dhcp_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dhcp_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dhcp options"):
        delete_dhcp_options("test-dhcp_options_id", region_name=REGION)


def test_delete_egress_only_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_egress_only_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_egress_only_internet_gateway("test-egress_only_internet_gateway_id", region_name=REGION)
    mock_client.delete_egress_only_internet_gateway.assert_called_once()


def test_delete_egress_only_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_egress_only_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_egress_only_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete egress only internet gateway"):
        delete_egress_only_internet_gateway("test-egress_only_internet_gateway_id", region_name=REGION)


def test_delete_fleets(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_fleets([], True, region_name=REGION)
    mock_client.delete_fleets.assert_called_once()


def test_delete_fleets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fleets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete fleets"):
        delete_fleets([], True, region_name=REGION)


def test_delete_flow_logs(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_logs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_flow_logs([], region_name=REGION)
    mock_client.delete_flow_logs.assert_called_once()


def test_delete_flow_logs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_flow_logs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_flow_logs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete flow logs"):
        delete_flow_logs([], region_name=REGION)


def test_delete_fpga_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_fpga_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_fpga_image("test-fpga_image_id", region_name=REGION)
    mock_client.delete_fpga_image.assert_called_once()


def test_delete_fpga_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_fpga_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fpga_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete fpga image"):
        delete_fpga_image("test-fpga_image_id", region_name=REGION)


def test_delete_image_usage_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_image_usage_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_image_usage_report("test-report_id", region_name=REGION)
    mock_client.delete_image_usage_report.assert_called_once()


def test_delete_image_usage_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_image_usage_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_image_usage_report",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete image usage report"):
        delete_image_usage_report("test-report_id", region_name=REGION)


def test_delete_instance_connect_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_connect_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_instance_connect_endpoint("test-instance_connect_endpoint_id", region_name=REGION)
    mock_client.delete_instance_connect_endpoint.assert_called_once()


def test_delete_instance_connect_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_connect_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_instance_connect_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete instance connect endpoint"):
        delete_instance_connect_endpoint("test-instance_connect_endpoint_id", region_name=REGION)


def test_delete_instance_event_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_instance_event_window("test-instance_event_window_id", region_name=REGION)
    mock_client.delete_instance_event_window.assert_called_once()


def test_delete_instance_event_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_event_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_instance_event_window",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete instance event window"):
        delete_instance_event_window("test-instance_event_window_id", region_name=REGION)


def test_delete_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_internet_gateway("test-internet_gateway_id", region_name=REGION)
    mock_client.delete_internet_gateway.assert_called_once()


def test_delete_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete internet gateway"):
        delete_internet_gateway("test-internet_gateway_id", region_name=REGION)


def test_delete_ipam(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam("test-ipam_id", region_name=REGION)
    mock_client.delete_ipam.assert_called_once()


def test_delete_ipam_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam"):
        delete_ipam("test-ipam_id", region_name=REGION)


def test_delete_ipam_external_resource_verification_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_external_resource_verification_token.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_external_resource_verification_token("test-ipam_external_resource_verification_token_id", region_name=REGION)
    mock_client.delete_ipam_external_resource_verification_token.assert_called_once()


def test_delete_ipam_external_resource_verification_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_external_resource_verification_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_external_resource_verification_token",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam external resource verification token"):
        delete_ipam_external_resource_verification_token("test-ipam_external_resource_verification_token_id", region_name=REGION)


def test_delete_ipam_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_pool("test-ipam_pool_id", region_name=REGION)
    mock_client.delete_ipam_pool.assert_called_once()


def test_delete_ipam_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam pool"):
        delete_ipam_pool("test-ipam_pool_id", region_name=REGION)


def test_delete_ipam_prefix_list_resolver(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_prefix_list_resolver.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", region_name=REGION)
    mock_client.delete_ipam_prefix_list_resolver.assert_called_once()


def test_delete_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_prefix_list_resolver.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_prefix_list_resolver",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam prefix list resolver"):
        delete_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", region_name=REGION)


def test_delete_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_prefix_list_resolver_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", region_name=REGION)
    mock_client.delete_ipam_prefix_list_resolver_target.assert_called_once()


def test_delete_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_prefix_list_resolver_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_prefix_list_resolver_target",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam prefix list resolver target"):
        delete_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", region_name=REGION)


def test_delete_ipam_resource_discovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_resource_discovery("test-ipam_resource_discovery_id", region_name=REGION)
    mock_client.delete_ipam_resource_discovery.assert_called_once()


def test_delete_ipam_resource_discovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_resource_discovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_resource_discovery",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam resource discovery"):
        delete_ipam_resource_discovery("test-ipam_resource_discovery_id", region_name=REGION)


def test_delete_ipam_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_scope("test-ipam_scope_id", region_name=REGION)
    mock_client.delete_ipam_scope.assert_called_once()


def test_delete_ipam_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ipam_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ipam_scope",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ipam scope"):
        delete_ipam_scope("test-ipam_scope_id", region_name=REGION)


def test_delete_key_pair(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_key_pair(region_name=REGION)
    mock_client.delete_key_pair.assert_called_once()


def test_delete_key_pair_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_key_pair",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete key pair"):
        delete_key_pair(region_name=REGION)


def test_delete_launch_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_launch_template(region_name=REGION)
    mock_client.delete_launch_template.assert_called_once()


def test_delete_launch_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_launch_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_launch_template",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete launch template"):
        delete_launch_template(region_name=REGION)


def test_delete_launch_template_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_launch_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_launch_template_versions([], region_name=REGION)
    mock_client.delete_launch_template_versions.assert_called_once()


def test_delete_launch_template_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_launch_template_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_launch_template_versions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete launch template versions"):
        delete_launch_template_versions([], region_name=REGION)


def test_delete_local_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.delete_local_gateway_route.assert_called_once()


def test_delete_local_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway route"):
        delete_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)


def test_delete_local_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_route_table("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.delete_local_gateway_route_table.assert_called_once()


def test_delete_local_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway route table"):
        delete_local_gateway_route_table("test-local_gateway_route_table_id", region_name=REGION)


def test_delete_local_gateway_route_table_virtual_interface_group_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table_virtual_interface_group_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_virtual_interface_group_association_id", region_name=REGION)
    mock_client.delete_local_gateway_route_table_virtual_interface_group_association.assert_called_once()


def test_delete_local_gateway_route_table_virtual_interface_group_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table_virtual_interface_group_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_route_table_virtual_interface_group_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway route table virtual interface group association"):
        delete_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_virtual_interface_group_association_id", region_name=REGION)


def test_delete_local_gateway_route_table_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_route_table_vpc_association("test-local_gateway_route_table_vpc_association_id", region_name=REGION)
    mock_client.delete_local_gateway_route_table_vpc_association.assert_called_once()


def test_delete_local_gateway_route_table_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route_table_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_route_table_vpc_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway route table vpc association"):
        delete_local_gateway_route_table_vpc_association("test-local_gateway_route_table_vpc_association_id", region_name=REGION)


def test_delete_local_gateway_virtual_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_virtual_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_virtual_interface("test-local_gateway_virtual_interface_id", region_name=REGION)
    mock_client.delete_local_gateway_virtual_interface.assert_called_once()


def test_delete_local_gateway_virtual_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_virtual_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_virtual_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway virtual interface"):
        delete_local_gateway_virtual_interface("test-local_gateway_virtual_interface_id", region_name=REGION)


def test_delete_local_gateway_virtual_interface_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_virtual_interface_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_virtual_interface_group("test-local_gateway_virtual_interface_group_id", region_name=REGION)
    mock_client.delete_local_gateway_virtual_interface_group.assert_called_once()


def test_delete_local_gateway_virtual_interface_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_local_gateway_virtual_interface_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_local_gateway_virtual_interface_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete local gateway virtual interface group"):
        delete_local_gateway_virtual_interface_group("test-local_gateway_virtual_interface_group_id", region_name=REGION)


def test_delete_managed_prefix_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_managed_prefix_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_managed_prefix_list("test-prefix_list_id", region_name=REGION)
    mock_client.delete_managed_prefix_list.assert_called_once()


def test_delete_managed_prefix_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_managed_prefix_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_managed_prefix_list",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete managed prefix list"):
        delete_managed_prefix_list("test-prefix_list_id", region_name=REGION)


def test_delete_nat_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_nat_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_nat_gateway("test-nat_gateway_id", region_name=REGION)
    mock_client.delete_nat_gateway.assert_called_once()


def test_delete_nat_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_nat_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_nat_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete nat gateway"):
        delete_nat_gateway("test-nat_gateway_id", region_name=REGION)


def test_delete_network_acl(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_acl.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_acl("test-network_acl_id", region_name=REGION)
    mock_client.delete_network_acl.assert_called_once()


def test_delete_network_acl_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_acl.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_acl",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network acl"):
        delete_network_acl("test-network_acl_id", region_name=REGION)


def test_delete_network_acl_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_acl_entry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_acl_entry("test-network_acl_id", 1, True, region_name=REGION)
    mock_client.delete_network_acl_entry.assert_called_once()


def test_delete_network_acl_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_acl_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_acl_entry",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network acl entry"):
        delete_network_acl_entry("test-network_acl_id", 1, True, region_name=REGION)


def test_delete_network_insights_access_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_insights_access_scope("test-network_insights_access_scope_id", region_name=REGION)
    mock_client.delete_network_insights_access_scope.assert_called_once()


def test_delete_network_insights_access_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_access_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_insights_access_scope",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network insights access scope"):
        delete_network_insights_access_scope("test-network_insights_access_scope_id", region_name=REGION)


def test_delete_network_insights_access_scope_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_access_scope_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_insights_access_scope_analysis("test-network_insights_access_scope_analysis_id", region_name=REGION)
    mock_client.delete_network_insights_access_scope_analysis.assert_called_once()


def test_delete_network_insights_access_scope_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_access_scope_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_insights_access_scope_analysis",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network insights access scope analysis"):
        delete_network_insights_access_scope_analysis("test-network_insights_access_scope_analysis_id", region_name=REGION)


def test_delete_network_insights_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_insights_analysis("test-network_insights_analysis_id", region_name=REGION)
    mock_client.delete_network_insights_analysis.assert_called_once()


def test_delete_network_insights_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_insights_analysis",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network insights analysis"):
        delete_network_insights_analysis("test-network_insights_analysis_id", region_name=REGION)


def test_delete_network_insights_path(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_path.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_insights_path("test-network_insights_path_id", region_name=REGION)
    mock_client.delete_network_insights_path.assert_called_once()


def test_delete_network_insights_path_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_insights_path.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_insights_path",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network insights path"):
        delete_network_insights_path("test-network_insights_path_id", region_name=REGION)


def test_delete_network_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_interface("test-network_interface_id", region_name=REGION)
    mock_client.delete_network_interface.assert_called_once()


def test_delete_network_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network interface"):
        delete_network_interface("test-network_interface_id", region_name=REGION)


def test_delete_network_interface_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_interface_permission.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_interface_permission("test-network_interface_permission_id", region_name=REGION)
    mock_client.delete_network_interface_permission.assert_called_once()


def test_delete_network_interface_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_network_interface_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_network_interface_permission",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete network interface permission"):
        delete_network_interface_permission("test-network_interface_permission_id", region_name=REGION)


def test_delete_placement_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_placement_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_placement_group("test-group_name", region_name=REGION)
    mock_client.delete_placement_group.assert_called_once()


def test_delete_placement_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_placement_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_placement_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete placement group"):
        delete_placement_group("test-group_name", region_name=REGION)


def test_delete_public_ipv4_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_ipv4_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_public_ipv4_pool("test-pool_id", region_name=REGION)
    mock_client.delete_public_ipv4_pool.assert_called_once()


def test_delete_public_ipv4_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_public_ipv4_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_public_ipv4_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete public ipv4 pool"):
        delete_public_ipv4_pool("test-pool_id", region_name=REGION)


def test_delete_queued_reserved_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_queued_reserved_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_queued_reserved_instances([], region_name=REGION)
    mock_client.delete_queued_reserved_instances.assert_called_once()


def test_delete_queued_reserved_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_queued_reserved_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_queued_reserved_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete queued reserved instances"):
        delete_queued_reserved_instances([], region_name=REGION)


def test_delete_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route("test-route_table_id", region_name=REGION)
    mock_client.delete_route.assert_called_once()


def test_delete_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete route"):
        delete_route("test-route_table_id", region_name=REGION)


def test_delete_route_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route_server("test-route_server_id", region_name=REGION)
    mock_client.delete_route_server.assert_called_once()


def test_delete_route_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_route_server",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete route server"):
        delete_route_server("test-route_server_id", region_name=REGION)


def test_delete_route_server_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route_server_endpoint("test-route_server_endpoint_id", region_name=REGION)
    mock_client.delete_route_server_endpoint.assert_called_once()


def test_delete_route_server_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_route_server_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete route server endpoint"):
        delete_route_server_endpoint("test-route_server_endpoint_id", region_name=REGION)


def test_delete_route_server_peer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route_server_peer("test-route_server_peer_id", region_name=REGION)
    mock_client.delete_route_server_peer.assert_called_once()


def test_delete_route_server_peer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_server_peer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_route_server_peer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete route server peer"):
        delete_route_server_peer("test-route_server_peer_id", region_name=REGION)


def test_delete_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route_table("test-route_table_id", region_name=REGION)
    mock_client.delete_route_table.assert_called_once()


def test_delete_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete route table"):
        delete_route_table("test-route_table_id", region_name=REGION)


def test_delete_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_security_group(region_name=REGION)
    mock_client.delete_security_group.assert_called_once()


def test_delete_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_security_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete security group"):
        delete_security_group(region_name=REGION)


def test_delete_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_snapshot("test-snapshot_id", region_name=REGION)
    mock_client.delete_snapshot.assert_called_once()


def test_delete_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        delete_snapshot("test-snapshot_id", region_name=REGION)


def test_delete_spot_datafeed_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_spot_datafeed_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_spot_datafeed_subscription(region_name=REGION)
    mock_client.delete_spot_datafeed_subscription.assert_called_once()


def test_delete_spot_datafeed_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_spot_datafeed_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_spot_datafeed_subscription",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete spot datafeed subscription"):
        delete_spot_datafeed_subscription(region_name=REGION)


def test_delete_subnet(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_subnet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_subnet("test-subnet_id", region_name=REGION)
    mock_client.delete_subnet.assert_called_once()


def test_delete_subnet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_subnet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_subnet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete subnet"):
        delete_subnet("test-subnet_id", region_name=REGION)


def test_delete_subnet_cidr_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_subnet_cidr_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_subnet_cidr_reservation("test-subnet_cidr_reservation_id", region_name=REGION)
    mock_client.delete_subnet_cidr_reservation.assert_called_once()


def test_delete_subnet_cidr_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_subnet_cidr_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_subnet_cidr_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete subnet cidr reservation"):
        delete_subnet_cidr_reservation("test-subnet_cidr_reservation_id", region_name=REGION)


def test_delete_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_tags([], region_name=REGION)
    mock_client.delete_tags.assert_called_once()


def test_delete_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tags",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tags"):
        delete_tags([], region_name=REGION)


def test_delete_traffic_mirror_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_filter.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_traffic_mirror_filter("test-traffic_mirror_filter_id", region_name=REGION)
    mock_client.delete_traffic_mirror_filter.assert_called_once()


def test_delete_traffic_mirror_filter_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_filter.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_mirror_filter",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic mirror filter"):
        delete_traffic_mirror_filter("test-traffic_mirror_filter_id", region_name=REGION)


def test_delete_traffic_mirror_filter_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_filter_rule.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", region_name=REGION)
    mock_client.delete_traffic_mirror_filter_rule.assert_called_once()


def test_delete_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_filter_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_mirror_filter_rule",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic mirror filter rule"):
        delete_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", region_name=REGION)


def test_delete_traffic_mirror_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_session.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_traffic_mirror_session("test-traffic_mirror_session_id", region_name=REGION)
    mock_client.delete_traffic_mirror_session.assert_called_once()


def test_delete_traffic_mirror_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_mirror_session",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic mirror session"):
        delete_traffic_mirror_session("test-traffic_mirror_session_id", region_name=REGION)


def test_delete_traffic_mirror_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_traffic_mirror_target("test-traffic_mirror_target_id", region_name=REGION)
    mock_client.delete_traffic_mirror_target.assert_called_once()


def test_delete_traffic_mirror_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_mirror_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_mirror_target",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic mirror target"):
        delete_traffic_mirror_target("test-traffic_mirror_target_id", region_name=REGION)


def test_delete_transit_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway("test-transit_gateway_id", region_name=REGION)
    mock_client.delete_transit_gateway.assert_called_once()


def test_delete_transit_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway"):
        delete_transit_gateway("test-transit_gateway_id", region_name=REGION)


def test_delete_transit_gateway_connect(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_connect.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_connect("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.delete_transit_gateway_connect.assert_called_once()


def test_delete_transit_gateway_connect_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_connect.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_connect",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway connect"):
        delete_transit_gateway_connect("test-transit_gateway_attachment_id", region_name=REGION)


def test_delete_transit_gateway_connect_peer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_connect_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_connect_peer("test-transit_gateway_connect_peer_id", region_name=REGION)
    mock_client.delete_transit_gateway_connect_peer.assert_called_once()


def test_delete_transit_gateway_connect_peer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_connect_peer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_connect_peer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway connect peer"):
        delete_transit_gateway_connect_peer("test-transit_gateway_connect_peer_id", region_name=REGION)


def test_delete_transit_gateway_multicast_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_multicast_domain.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", region_name=REGION)
    mock_client.delete_transit_gateway_multicast_domain.assert_called_once()


def test_delete_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_multicast_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_multicast_domain",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway multicast domain"):
        delete_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", region_name=REGION)


def test_delete_transit_gateway_peering_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_peering_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.delete_transit_gateway_peering_attachment.assert_called_once()


def test_delete_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_peering_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_peering_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway peering attachment"):
        delete_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_delete_transit_gateway_policy_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_policy_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_policy_table("test-transit_gateway_policy_table_id", region_name=REGION)
    mock_client.delete_transit_gateway_policy_table.assert_called_once()


def test_delete_transit_gateway_policy_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_policy_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_policy_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway policy table"):
        delete_transit_gateway_policy_table("test-transit_gateway_policy_table_id", region_name=REGION)


def test_delete_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_prefix_list_reference.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)
    mock_client.delete_transit_gateway_prefix_list_reference.assert_called_once()


def test_delete_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_prefix_list_reference.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_prefix_list_reference",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway prefix list reference"):
        delete_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)


def test_delete_transit_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_route("test-transit_gateway_route_table_id", "test-destination_cidr_block", region_name=REGION)
    mock_client.delete_transit_gateway_route.assert_called_once()


def test_delete_transit_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway route"):
        delete_transit_gateway_route("test-transit_gateway_route_table_id", "test-destination_cidr_block", region_name=REGION)


def test_delete_transit_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_route_table("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.delete_transit_gateway_route_table.assert_called_once()


def test_delete_transit_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway route table"):
        delete_transit_gateway_route_table("test-transit_gateway_route_table_id", region_name=REGION)


def test_delete_transit_gateway_route_table_announcement(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route_table_announcement.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_route_table_announcement("test-transit_gateway_route_table_announcement_id", region_name=REGION)
    mock_client.delete_transit_gateway_route_table_announcement.assert_called_once()


def test_delete_transit_gateway_route_table_announcement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_route_table_announcement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_route_table_announcement",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway route table announcement"):
        delete_transit_gateway_route_table_announcement("test-transit_gateway_route_table_announcement_id", region_name=REGION)


def test_delete_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.delete_transit_gateway_vpc_attachment.assert_called_once()


def test_delete_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_transit_gateway_vpc_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_transit_gateway_vpc_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete transit gateway vpc attachment"):
        delete_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_delete_verified_access_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_endpoint("test-verified_access_endpoint_id", region_name=REGION)
    mock_client.delete_verified_access_endpoint.assert_called_once()


def test_delete_verified_access_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_verified_access_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete verified access endpoint"):
        delete_verified_access_endpoint("test-verified_access_endpoint_id", region_name=REGION)


def test_delete_verified_access_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_group("test-verified_access_group_id", region_name=REGION)
    mock_client.delete_verified_access_group.assert_called_once()


def test_delete_verified_access_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_verified_access_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete verified access group"):
        delete_verified_access_group("test-verified_access_group_id", region_name=REGION)


def test_delete_verified_access_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_instance("test-verified_access_instance_id", region_name=REGION)
    mock_client.delete_verified_access_instance.assert_called_once()


def test_delete_verified_access_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_verified_access_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete verified access instance"):
        delete_verified_access_instance("test-verified_access_instance_id", region_name=REGION)


def test_delete_verified_access_trust_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_trust_provider("test-verified_access_trust_provider_id", region_name=REGION)
    mock_client.delete_verified_access_trust_provider.assert_called_once()


def test_delete_verified_access_trust_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_verified_access_trust_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_verified_access_trust_provider",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete verified access trust provider"):
        delete_verified_access_trust_provider("test-verified_access_trust_provider_id", region_name=REGION)


def test_delete_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_volume("test-volume_id", region_name=REGION)
    mock_client.delete_volume.assert_called_once()


def test_delete_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete volume"):
        delete_volume("test-volume_id", region_name=REGION)


def test_delete_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc("test-vpc_id", region_name=REGION)
    mock_client.delete_vpc.assert_called_once()


def test_delete_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc"):
        delete_vpc("test-vpc_id", region_name=REGION)


def test_delete_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_block_public_access_exclusion.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc_block_public_access_exclusion("test-exclusion_id", region_name=REGION)
    mock_client.delete_vpc_block_public_access_exclusion.assert_called_once()


def test_delete_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_block_public_access_exclusion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_block_public_access_exclusion",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc block public access exclusion"):
        delete_vpc_block_public_access_exclusion("test-exclusion_id", region_name=REGION)


def test_delete_vpc_endpoint_connection_notifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoint_connection_notifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc_endpoint_connection_notifications([], region_name=REGION)
    mock_client.delete_vpc_endpoint_connection_notifications.assert_called_once()


def test_delete_vpc_endpoint_connection_notifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoint_connection_notifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_endpoint_connection_notifications",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc endpoint connection notifications"):
        delete_vpc_endpoint_connection_notifications([], region_name=REGION)


def test_delete_vpc_endpoint_service_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoint_service_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc_endpoint_service_configurations([], region_name=REGION)
    mock_client.delete_vpc_endpoint_service_configurations.assert_called_once()


def test_delete_vpc_endpoint_service_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoint_service_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_endpoint_service_configurations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc endpoint service configurations"):
        delete_vpc_endpoint_service_configurations([], region_name=REGION)


def test_delete_vpc_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc_endpoints([], region_name=REGION)
    mock_client.delete_vpc_endpoints.assert_called_once()


def test_delete_vpc_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc endpoints"):
        delete_vpc_endpoints([], region_name=REGION)


def test_delete_vpc_peering_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_peering_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)
    mock_client.delete_vpc_peering_connection.assert_called_once()


def test_delete_vpc_peering_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_peering_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_peering_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc peering connection"):
        delete_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)


def test_delete_vpn_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpn_connection("test-vpn_connection_id", region_name=REGION)
    mock_client.delete_vpn_connection.assert_called_once()


def test_delete_vpn_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpn_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpn connection"):
        delete_vpn_connection("test-vpn_connection_id", region_name=REGION)


def test_delete_vpn_connection_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_connection_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", region_name=REGION)
    mock_client.delete_vpn_connection_route.assert_called_once()


def test_delete_vpn_connection_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_connection_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpn_connection_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpn connection route"):
        delete_vpn_connection_route("test-destination_cidr_block", "test-vpn_connection_id", region_name=REGION)


def test_delete_vpn_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_vpn_gateway("test-vpn_gateway_id", region_name=REGION)
    mock_client.delete_vpn_gateway.assert_called_once()


def test_delete_vpn_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpn_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpn_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpn gateway"):
        delete_vpn_gateway("test-vpn_gateway_id", region_name=REGION)


def test_deprovision_byoip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deprovision_byoip_cidr("test-cidr", region_name=REGION)
    mock_client.deprovision_byoip_cidr.assert_called_once()


def test_deprovision_byoip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_byoip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deprovision_byoip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deprovision byoip cidr"):
        deprovision_byoip_cidr("test-cidr", region_name=REGION)


def test_deprovision_ipam_byoasn(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deprovision_ipam_byoasn("test-ipam_id", "test-asn", region_name=REGION)
    mock_client.deprovision_ipam_byoasn.assert_called_once()


def test_deprovision_ipam_byoasn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_ipam_byoasn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deprovision_ipam_byoasn",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deprovision ipam byoasn"):
        deprovision_ipam_byoasn("test-ipam_id", "test-asn", region_name=REGION)


def test_deprovision_ipam_pool_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deprovision_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)
    mock_client.deprovision_ipam_pool_cidr.assert_called_once()


def test_deprovision_ipam_pool_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_ipam_pool_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deprovision_ipam_pool_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deprovision ipam pool cidr"):
        deprovision_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)


def test_deprovision_public_ipv4_pool_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_public_ipv4_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deprovision_public_ipv4_pool_cidr("test-pool_id", "test-cidr", region_name=REGION)
    mock_client.deprovision_public_ipv4_pool_cidr.assert_called_once()


def test_deprovision_public_ipv4_pool_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deprovision_public_ipv4_pool_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deprovision_public_ipv4_pool_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deprovision public ipv4 pool cidr"):
        deprovision_public_ipv4_pool_cidr("test-pool_id", "test-cidr", region_name=REGION)


def test_deregister_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_image("test-image_id", region_name=REGION)
    mock_client.deregister_image.assert_called_once()


def test_deregister_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister image"):
        deregister_image("test-image_id", region_name=REGION)


def test_deregister_instance_event_notification_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_instance_event_notification_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_instance_event_notification_attributes({}, region_name=REGION)
    mock_client.deregister_instance_event_notification_attributes.assert_called_once()


def test_deregister_instance_event_notification_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_instance_event_notification_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_instance_event_notification_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister instance event notification attributes"):
        deregister_instance_event_notification_attributes({}, region_name=REGION)


def test_deregister_transit_gateway_multicast_group_members(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_members.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_transit_gateway_multicast_group_members(region_name=REGION)
    mock_client.deregister_transit_gateway_multicast_group_members.assert_called_once()


def test_deregister_transit_gateway_multicast_group_members_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_members.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_transit_gateway_multicast_group_members",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister transit gateway multicast group members"):
        deregister_transit_gateway_multicast_group_members(region_name=REGION)


def test_deregister_transit_gateway_multicast_group_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_sources.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_transit_gateway_multicast_group_sources(region_name=REGION)
    mock_client.deregister_transit_gateway_multicast_group_sources.assert_called_once()


def test_deregister_transit_gateway_multicast_group_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_transit_gateway_multicast_group_sources",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister transit gateway multicast group sources"):
        deregister_transit_gateway_multicast_group_sources(region_name=REGION)


def test_describe_account_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_account_attributes(region_name=REGION)
    mock_client.describe_account_attributes.assert_called_once()


def test_describe_account_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account attributes"):
        describe_account_attributes(region_name=REGION)


def test_describe_address_transfers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_address_transfers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_address_transfers(region_name=REGION)
    mock_client.describe_address_transfers.assert_called_once()


def test_describe_address_transfers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_address_transfers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_address_transfers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe address transfers"):
        describe_address_transfers(region_name=REGION)


def test_describe_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_addresses(region_name=REGION)
    mock_client.describe_addresses.assert_called_once()


def test_describe_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe addresses"):
        describe_addresses(region_name=REGION)


def test_describe_addresses_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addresses_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_addresses_attribute(region_name=REGION)
    mock_client.describe_addresses_attribute.assert_called_once()


def test_describe_addresses_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addresses_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_addresses_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe addresses attribute"):
        describe_addresses_attribute(region_name=REGION)


def test_describe_aggregate_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_aggregate_id_format(region_name=REGION)
    mock_client.describe_aggregate_id_format.assert_called_once()


def test_describe_aggregate_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_aggregate_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe aggregate id format"):
        describe_aggregate_id_format(region_name=REGION)


def test_describe_availability_zones(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_availability_zones.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_availability_zones(region_name=REGION)
    mock_client.describe_availability_zones.assert_called_once()


def test_describe_availability_zones_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_availability_zones.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_availability_zones",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe availability zones"):
        describe_availability_zones(region_name=REGION)


def test_describe_aws_network_performance_metric_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aws_network_performance_metric_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_aws_network_performance_metric_subscriptions(region_name=REGION)
    mock_client.describe_aws_network_performance_metric_subscriptions.assert_called_once()


def test_describe_aws_network_performance_metric_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aws_network_performance_metric_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_aws_network_performance_metric_subscriptions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe aws network performance metric subscriptions"):
        describe_aws_network_performance_metric_subscriptions(region_name=REGION)


def test_describe_bundle_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bundle_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_bundle_tasks(region_name=REGION)
    mock_client.describe_bundle_tasks.assert_called_once()


def test_describe_bundle_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bundle_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bundle_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe bundle tasks"):
        describe_bundle_tasks(region_name=REGION)


def test_describe_byoip_cidrs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_byoip_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_byoip_cidrs(1, region_name=REGION)
    mock_client.describe_byoip_cidrs.assert_called_once()


def test_describe_byoip_cidrs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_byoip_cidrs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_byoip_cidrs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe byoip cidrs"):
        describe_byoip_cidrs(1, region_name=REGION)


def test_describe_capacity_block_extension_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_extension_history(region_name=REGION)
    mock_client.describe_capacity_block_extension_history.assert_called_once()


def test_describe_capacity_block_extension_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_block_extension_history",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity block extension history"):
        describe_capacity_block_extension_history(region_name=REGION)


def test_describe_capacity_block_extension_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", region_name=REGION)
    mock_client.describe_capacity_block_extension_offerings.assert_called_once()


def test_describe_capacity_block_extension_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_block_extension_offerings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity block extension offerings"):
        describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", region_name=REGION)


def test_describe_capacity_block_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_offerings(1, region_name=REGION)
    mock_client.describe_capacity_block_offerings.assert_called_once()


def test_describe_capacity_block_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_block_offerings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity block offerings"):
        describe_capacity_block_offerings(1, region_name=REGION)


def test_describe_capacity_block_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_status(region_name=REGION)
    mock_client.describe_capacity_block_status.assert_called_once()


def test_describe_capacity_block_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_block_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_block_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity block status"):
        describe_capacity_block_status(region_name=REGION)


def test_describe_capacity_blocks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_blocks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_blocks(region_name=REGION)
    mock_client.describe_capacity_blocks.assert_called_once()


def test_describe_capacity_blocks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_blocks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_blocks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity blocks"):
        describe_capacity_blocks(region_name=REGION)


def test_describe_capacity_manager_data_exports(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_manager_data_exports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_manager_data_exports(region_name=REGION)
    mock_client.describe_capacity_manager_data_exports.assert_called_once()


def test_describe_capacity_manager_data_exports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_manager_data_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_manager_data_exports",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity manager data exports"):
        describe_capacity_manager_data_exports(region_name=REGION)


def test_describe_capacity_reservation_billing_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_billing_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_billing_requests("test-role", region_name=REGION)
    mock_client.describe_capacity_reservation_billing_requests.assert_called_once()


def test_describe_capacity_reservation_billing_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_billing_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_reservation_billing_requests",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity reservation billing requests"):
        describe_capacity_reservation_billing_requests("test-role", region_name=REGION)


def test_describe_capacity_reservation_fleets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_fleets(region_name=REGION)
    mock_client.describe_capacity_reservation_fleets.assert_called_once()


def test_describe_capacity_reservation_fleets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_reservation_fleets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity reservation fleets"):
        describe_capacity_reservation_fleets(region_name=REGION)


def test_describe_capacity_reservation_topology(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_topology.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_topology(region_name=REGION)
    mock_client.describe_capacity_reservation_topology.assert_called_once()


def test_describe_capacity_reservation_topology_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_topology.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_reservation_topology",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity reservation topology"):
        describe_capacity_reservation_topology(region_name=REGION)


def test_describe_capacity_reservations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservations(region_name=REGION)
    mock_client.describe_capacity_reservations.assert_called_once()


def test_describe_capacity_reservations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_reservations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_reservations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity reservations"):
        describe_capacity_reservations(region_name=REGION)


def test_describe_carrier_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_carrier_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_carrier_gateways(region_name=REGION)
    mock_client.describe_carrier_gateways.assert_called_once()


def test_describe_carrier_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_carrier_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_carrier_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe carrier gateways"):
        describe_carrier_gateways(region_name=REGION)


def test_describe_classic_link_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_classic_link_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_classic_link_instances(region_name=REGION)
    mock_client.describe_classic_link_instances.assert_called_once()


def test_describe_classic_link_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_classic_link_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_classic_link_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe classic link instances"):
        describe_classic_link_instances(region_name=REGION)


def test_describe_client_vpn_authorization_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_authorization_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.describe_client_vpn_authorization_rules.assert_called_once()


def test_describe_client_vpn_authorization_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_authorization_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_client_vpn_authorization_rules",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe client vpn authorization rules"):
        describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", region_name=REGION)


def test_describe_client_vpn_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_connections("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.describe_client_vpn_connections.assert_called_once()


def test_describe_client_vpn_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_client_vpn_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe client vpn connections"):
        describe_client_vpn_connections("test-client_vpn_endpoint_id", region_name=REGION)


def test_describe_client_vpn_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_endpoints(region_name=REGION)
    mock_client.describe_client_vpn_endpoints.assert_called_once()


def test_describe_client_vpn_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_client_vpn_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe client vpn endpoints"):
        describe_client_vpn_endpoints(region_name=REGION)


def test_describe_client_vpn_routes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_routes("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.describe_client_vpn_routes.assert_called_once()


def test_describe_client_vpn_routes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_routes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_client_vpn_routes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe client vpn routes"):
        describe_client_vpn_routes("test-client_vpn_endpoint_id", region_name=REGION)


def test_describe_client_vpn_target_networks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_target_networks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_target_networks("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.describe_client_vpn_target_networks.assert_called_once()


def test_describe_client_vpn_target_networks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_client_vpn_target_networks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_client_vpn_target_networks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe client vpn target networks"):
        describe_client_vpn_target_networks("test-client_vpn_endpoint_id", region_name=REGION)


def test_describe_coip_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_coip_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_coip_pools(region_name=REGION)
    mock_client.describe_coip_pools.assert_called_once()


def test_describe_coip_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_coip_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_coip_pools",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe coip pools"):
        describe_coip_pools(region_name=REGION)


def test_describe_conversion_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conversion_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_conversion_tasks(region_name=REGION)
    mock_client.describe_conversion_tasks.assert_called_once()


def test_describe_conversion_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conversion_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_conversion_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe conversion tasks"):
        describe_conversion_tasks(region_name=REGION)


def test_describe_customer_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_customer_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_customer_gateways(region_name=REGION)
    mock_client.describe_customer_gateways.assert_called_once()


def test_describe_customer_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_customer_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_customer_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe customer gateways"):
        describe_customer_gateways(region_name=REGION)


def test_describe_declarative_policies_reports(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_declarative_policies_reports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_declarative_policies_reports(region_name=REGION)
    mock_client.describe_declarative_policies_reports.assert_called_once()


def test_describe_declarative_policies_reports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_declarative_policies_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_declarative_policies_reports",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe declarative policies reports"):
        describe_declarative_policies_reports(region_name=REGION)


def test_describe_dhcp_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_dhcp_options(region_name=REGION)
    mock_client.describe_dhcp_options.assert_called_once()


def test_describe_dhcp_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dhcp_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dhcp_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dhcp options"):
        describe_dhcp_options(region_name=REGION)


def test_describe_egress_only_internet_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_egress_only_internet_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_egress_only_internet_gateways(region_name=REGION)
    mock_client.describe_egress_only_internet_gateways.assert_called_once()


def test_describe_egress_only_internet_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_egress_only_internet_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_egress_only_internet_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe egress only internet gateways"):
        describe_egress_only_internet_gateways(region_name=REGION)


def test_describe_elastic_gpus(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_elastic_gpus.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_elastic_gpus(region_name=REGION)
    mock_client.describe_elastic_gpus.assert_called_once()


def test_describe_elastic_gpus_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_elastic_gpus.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_elastic_gpus",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe elastic gpus"):
        describe_elastic_gpus(region_name=REGION)


def test_describe_export_image_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_export_image_tasks(region_name=REGION)
    mock_client.describe_export_image_tasks.assert_called_once()


def test_describe_export_image_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_image_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_export_image_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe export image tasks"):
        describe_export_image_tasks(region_name=REGION)


def test_describe_export_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_export_tasks(region_name=REGION)
    mock_client.describe_export_tasks.assert_called_once()


def test_describe_export_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_export_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe export tasks"):
        describe_export_tasks(region_name=REGION)


def test_describe_fast_launch_images(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fast_launch_images.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fast_launch_images(region_name=REGION)
    mock_client.describe_fast_launch_images.assert_called_once()


def test_describe_fast_launch_images_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fast_launch_images.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fast_launch_images",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fast launch images"):
        describe_fast_launch_images(region_name=REGION)


def test_describe_fast_snapshot_restores(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fast_snapshot_restores(region_name=REGION)
    mock_client.describe_fast_snapshot_restores.assert_called_once()


def test_describe_fast_snapshot_restores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fast_snapshot_restores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fast_snapshot_restores",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fast snapshot restores"):
        describe_fast_snapshot_restores(region_name=REGION)


def test_describe_fleet_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleet_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleet_history("test-fleet_id", "test-start_time", region_name=REGION)
    mock_client.describe_fleet_history.assert_called_once()


def test_describe_fleet_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleet_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_history",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fleet history"):
        describe_fleet_history("test-fleet_id", "test-start_time", region_name=REGION)


def test_describe_fleet_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleet_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleet_instances("test-fleet_id", region_name=REGION)
    mock_client.describe_fleet_instances.assert_called_once()


def test_describe_fleet_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleet_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fleet instances"):
        describe_fleet_instances("test-fleet_id", region_name=REGION)


def test_describe_fleets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleets(region_name=REGION)
    mock_client.describe_fleets.assert_called_once()


def test_describe_fleets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fleets"):
        describe_fleets(region_name=REGION)


def test_describe_flow_logs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flow_logs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_flow_logs(region_name=REGION)
    mock_client.describe_flow_logs.assert_called_once()


def test_describe_flow_logs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_flow_logs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_flow_logs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe flow logs"):
        describe_flow_logs(region_name=REGION)


def test_describe_fpga_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fpga_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fpga_image_attribute("test-fpga_image_id", "test-attribute", region_name=REGION)
    mock_client.describe_fpga_image_attribute.assert_called_once()


def test_describe_fpga_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fpga_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fpga_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fpga image attribute"):
        describe_fpga_image_attribute("test-fpga_image_id", "test-attribute", region_name=REGION)


def test_describe_fpga_images(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fpga_images.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fpga_images(region_name=REGION)
    mock_client.describe_fpga_images.assert_called_once()


def test_describe_fpga_images_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_fpga_images.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fpga_images",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe fpga images"):
        describe_fpga_images(region_name=REGION)


def test_describe_host_reservation_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_reservation_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_host_reservation_offerings(region_name=REGION)
    mock_client.describe_host_reservation_offerings.assert_called_once()


def test_describe_host_reservation_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_reservation_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_host_reservation_offerings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe host reservation offerings"):
        describe_host_reservation_offerings(region_name=REGION)


def test_describe_host_reservations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_host_reservations(region_name=REGION)
    mock_client.describe_host_reservations.assert_called_once()


def test_describe_host_reservations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_host_reservations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_host_reservations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe host reservations"):
        describe_host_reservations(region_name=REGION)


def test_describe_hosts(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_hosts(region_name=REGION)
    mock_client.describe_hosts.assert_called_once()


def test_describe_hosts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hosts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_hosts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe hosts"):
        describe_hosts(region_name=REGION)


def test_describe_iam_instance_profile_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_iam_instance_profile_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_iam_instance_profile_associations(region_name=REGION)
    mock_client.describe_iam_instance_profile_associations.assert_called_once()


def test_describe_iam_instance_profile_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_iam_instance_profile_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_iam_instance_profile_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe iam instance profile associations"):
        describe_iam_instance_profile_associations(region_name=REGION)


def test_describe_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_id_format(region_name=REGION)
    mock_client.describe_id_format.assert_called_once()


def test_describe_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe id format"):
        describe_id_format(region_name=REGION)


def test_describe_identity_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_identity_id_format("test-principal_arn", region_name=REGION)
    mock_client.describe_identity_id_format.assert_called_once()


def test_describe_identity_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_identity_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe identity id format"):
        describe_identity_id_format("test-principal_arn", region_name=REGION)


def test_describe_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_attribute("test-attribute", "test-image_id", region_name=REGION)
    mock_client.describe_image_attribute.assert_called_once()


def test_describe_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image attribute"):
        describe_image_attribute("test-attribute", "test-image_id", region_name=REGION)


def test_describe_image_references(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_references.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_references([], region_name=REGION)
    mock_client.describe_image_references.assert_called_once()


def test_describe_image_references_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_references.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_references",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image references"):
        describe_image_references([], region_name=REGION)


def test_describe_image_usage_report_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_usage_report_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_usage_report_entries(region_name=REGION)
    mock_client.describe_image_usage_report_entries.assert_called_once()


def test_describe_image_usage_report_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_usage_report_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_usage_report_entries",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image usage report entries"):
        describe_image_usage_report_entries(region_name=REGION)


def test_describe_image_usage_reports(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_usage_reports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_usage_reports(region_name=REGION)
    mock_client.describe_image_usage_reports.assert_called_once()


def test_describe_image_usage_reports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_image_usage_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_image_usage_reports",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe image usage reports"):
        describe_image_usage_reports(region_name=REGION)


def test_describe_import_image_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_import_image_tasks(region_name=REGION)
    mock_client.describe_import_image_tasks.assert_called_once()


def test_describe_import_image_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import_image_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_import_image_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe import image tasks"):
        describe_import_image_tasks(region_name=REGION)


def test_describe_import_snapshot_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import_snapshot_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_import_snapshot_tasks(region_name=REGION)
    mock_client.describe_import_snapshot_tasks.assert_called_once()


def test_describe_import_snapshot_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_import_snapshot_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_import_snapshot_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe import snapshot tasks"):
        describe_import_snapshot_tasks(region_name=REGION)


def test_describe_instance_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_attribute("test-instance_id", "test-attribute", region_name=REGION)
    mock_client.describe_instance_attribute.assert_called_once()


def test_describe_instance_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance attribute"):
        describe_instance_attribute("test-instance_id", "test-attribute", region_name=REGION)


def test_describe_instance_connect_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_connect_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_connect_endpoints(region_name=REGION)
    mock_client.describe_instance_connect_endpoints.assert_called_once()


def test_describe_instance_connect_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_connect_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_connect_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance connect endpoints"):
        describe_instance_connect_endpoints(region_name=REGION)


def test_describe_instance_credit_specifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_credit_specifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_credit_specifications(region_name=REGION)
    mock_client.describe_instance_credit_specifications.assert_called_once()


def test_describe_instance_credit_specifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_credit_specifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_credit_specifications",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance credit specifications"):
        describe_instance_credit_specifications(region_name=REGION)


def test_describe_instance_event_notification_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_event_notification_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_event_notification_attributes(region_name=REGION)
    mock_client.describe_instance_event_notification_attributes.assert_called_once()


def test_describe_instance_event_notification_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_event_notification_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_event_notification_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance event notification attributes"):
        describe_instance_event_notification_attributes(region_name=REGION)


def test_describe_instance_event_windows(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_event_windows.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_event_windows(region_name=REGION)
    mock_client.describe_instance_event_windows.assert_called_once()


def test_describe_instance_event_windows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_event_windows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_event_windows",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance event windows"):
        describe_instance_event_windows(region_name=REGION)


def test_describe_instance_image_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_image_metadata.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_image_metadata(region_name=REGION)
    mock_client.describe_instance_image_metadata.assert_called_once()


def test_describe_instance_image_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_image_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_image_metadata",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance image metadata"):
        describe_instance_image_metadata(region_name=REGION)


def test_describe_instance_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_status(region_name=REGION)
    mock_client.describe_instance_status.assert_called_once()


def test_describe_instance_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance status"):
        describe_instance_status(region_name=REGION)


def test_describe_instance_topology(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_topology.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_topology(region_name=REGION)
    mock_client.describe_instance_topology.assert_called_once()


def test_describe_instance_topology_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_topology.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_topology",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance topology"):
        describe_instance_topology(region_name=REGION)


def test_describe_instance_type_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_type_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_type_offerings(region_name=REGION)
    mock_client.describe_instance_type_offerings.assert_called_once()


def test_describe_instance_type_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_type_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_type_offerings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance type offerings"):
        describe_instance_type_offerings(region_name=REGION)


def test_describe_instance_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_types.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_types(region_name=REGION)
    mock_client.describe_instance_types.assert_called_once()


def test_describe_instance_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_types",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance types"):
        describe_instance_types(region_name=REGION)


def test_describe_internet_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_internet_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_internet_gateways(region_name=REGION)
    mock_client.describe_internet_gateways.assert_called_once()


def test_describe_internet_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_internet_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_internet_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe internet gateways"):
        describe_internet_gateways(region_name=REGION)


def test_describe_ipam_byoasn(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_byoasn(region_name=REGION)
    mock_client.describe_ipam_byoasn.assert_called_once()


def test_describe_ipam_byoasn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_byoasn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_byoasn",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam byoasn"):
        describe_ipam_byoasn(region_name=REGION)


def test_describe_ipam_external_resource_verification_tokens(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_external_resource_verification_tokens.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_external_resource_verification_tokens(region_name=REGION)
    mock_client.describe_ipam_external_resource_verification_tokens.assert_called_once()


def test_describe_ipam_external_resource_verification_tokens_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_external_resource_verification_tokens.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_external_resource_verification_tokens",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam external resource verification tokens"):
        describe_ipam_external_resource_verification_tokens(region_name=REGION)


def test_describe_ipam_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_pools(region_name=REGION)
    mock_client.describe_ipam_pools.assert_called_once()


def test_describe_ipam_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_pools",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam pools"):
        describe_ipam_pools(region_name=REGION)


def test_describe_ipam_prefix_list_resolver_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolver_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_prefix_list_resolver_targets(region_name=REGION)
    mock_client.describe_ipam_prefix_list_resolver_targets.assert_called_once()


def test_describe_ipam_prefix_list_resolver_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolver_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_prefix_list_resolver_targets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam prefix list resolver targets"):
        describe_ipam_prefix_list_resolver_targets(region_name=REGION)


def test_describe_ipam_prefix_list_resolvers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolvers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_prefix_list_resolvers(region_name=REGION)
    mock_client.describe_ipam_prefix_list_resolvers.assert_called_once()


def test_describe_ipam_prefix_list_resolvers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolvers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_prefix_list_resolvers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam prefix list resolvers"):
        describe_ipam_prefix_list_resolvers(region_name=REGION)


def test_describe_ipam_resource_discoveries(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discoveries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_resource_discoveries(region_name=REGION)
    mock_client.describe_ipam_resource_discoveries.assert_called_once()


def test_describe_ipam_resource_discoveries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discoveries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_resource_discoveries",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam resource discoveries"):
        describe_ipam_resource_discoveries(region_name=REGION)


def test_describe_ipam_resource_discovery_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discovery_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_resource_discovery_associations(region_name=REGION)
    mock_client.describe_ipam_resource_discovery_associations.assert_called_once()


def test_describe_ipam_resource_discovery_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discovery_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_resource_discovery_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam resource discovery associations"):
        describe_ipam_resource_discovery_associations(region_name=REGION)


def test_describe_ipam_scopes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_scopes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_scopes(region_name=REGION)
    mock_client.describe_ipam_scopes.assert_called_once()


def test_describe_ipam_scopes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipam_scopes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipam_scopes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipam scopes"):
        describe_ipam_scopes(region_name=REGION)


def test_describe_ipams(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipams.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipams(region_name=REGION)
    mock_client.describe_ipams.assert_called_once()


def test_describe_ipams_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipams.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipams",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipams"):
        describe_ipams(region_name=REGION)


def test_describe_ipv6_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipv6_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipv6_pools(region_name=REGION)
    mock_client.describe_ipv6_pools.assert_called_once()


def test_describe_ipv6_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ipv6_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ipv6_pools",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ipv6 pools"):
        describe_ipv6_pools(region_name=REGION)


def test_describe_key_pairs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_pairs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_key_pairs(region_name=REGION)
    mock_client.describe_key_pairs.assert_called_once()


def test_describe_key_pairs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_pairs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_key_pairs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe key pairs"):
        describe_key_pairs(region_name=REGION)


def test_describe_launch_template_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_launch_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_launch_template_versions(region_name=REGION)
    mock_client.describe_launch_template_versions.assert_called_once()


def test_describe_launch_template_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_launch_template_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_launch_template_versions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe launch template versions"):
        describe_launch_template_versions(region_name=REGION)


def test_describe_launch_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_launch_templates.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_launch_templates(region_name=REGION)
    mock_client.describe_launch_templates.assert_called_once()


def test_describe_launch_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_launch_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_launch_templates",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe launch templates"):
        describe_launch_templates(region_name=REGION)


def test_describe_local_gateway_route_table_virtual_interface_group_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_virtual_interface_group_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_table_virtual_interface_group_associations(region_name=REGION)
    mock_client.describe_local_gateway_route_table_virtual_interface_group_associations.assert_called_once()


def test_describe_local_gateway_route_table_virtual_interface_group_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_virtual_interface_group_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateway_route_table_virtual_interface_group_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateway route table virtual interface group associations"):
        describe_local_gateway_route_table_virtual_interface_group_associations(region_name=REGION)


def test_describe_local_gateway_route_table_vpc_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_table_vpc_associations(region_name=REGION)
    mock_client.describe_local_gateway_route_table_vpc_associations.assert_called_once()


def test_describe_local_gateway_route_table_vpc_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_vpc_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateway_route_table_vpc_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateway route table vpc associations"):
        describe_local_gateway_route_table_vpc_associations(region_name=REGION)


def test_describe_local_gateway_route_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_tables(region_name=REGION)
    mock_client.describe_local_gateway_route_tables.assert_called_once()


def test_describe_local_gateway_route_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateway_route_tables",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateway route tables"):
        describe_local_gateway_route_tables(region_name=REGION)


def test_describe_local_gateway_virtual_interface_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interface_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_virtual_interface_groups(region_name=REGION)
    mock_client.describe_local_gateway_virtual_interface_groups.assert_called_once()


def test_describe_local_gateway_virtual_interface_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interface_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateway_virtual_interface_groups",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateway virtual interface groups"):
        describe_local_gateway_virtual_interface_groups(region_name=REGION)


def test_describe_local_gateway_virtual_interfaces(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_virtual_interfaces(region_name=REGION)
    mock_client.describe_local_gateway_virtual_interfaces.assert_called_once()


def test_describe_local_gateway_virtual_interfaces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interfaces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateway_virtual_interfaces",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateway virtual interfaces"):
        describe_local_gateway_virtual_interfaces(region_name=REGION)


def test_describe_local_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateways(region_name=REGION)
    mock_client.describe_local_gateways.assert_called_once()


def test_describe_local_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_local_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_local_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe local gateways"):
        describe_local_gateways(region_name=REGION)


def test_describe_locked_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_locked_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_locked_snapshots(region_name=REGION)
    mock_client.describe_locked_snapshots.assert_called_once()


def test_describe_locked_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_locked_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_locked_snapshots",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe locked snapshots"):
        describe_locked_snapshots(region_name=REGION)


def test_describe_mac_hosts(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_mac_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_mac_hosts(region_name=REGION)
    mock_client.describe_mac_hosts.assert_called_once()


def test_describe_mac_hosts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_mac_hosts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_mac_hosts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe mac hosts"):
        describe_mac_hosts(region_name=REGION)


def test_describe_mac_modification_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_mac_modification_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_mac_modification_tasks(region_name=REGION)
    mock_client.describe_mac_modification_tasks.assert_called_once()


def test_describe_mac_modification_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_mac_modification_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_mac_modification_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe mac modification tasks"):
        describe_mac_modification_tasks(region_name=REGION)


def test_describe_managed_prefix_lists(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_prefix_lists.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_managed_prefix_lists(region_name=REGION)
    mock_client.describe_managed_prefix_lists.assert_called_once()


def test_describe_managed_prefix_lists_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_prefix_lists.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_managed_prefix_lists",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe managed prefix lists"):
        describe_managed_prefix_lists(region_name=REGION)


def test_describe_moving_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_moving_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_moving_addresses(region_name=REGION)
    mock_client.describe_moving_addresses.assert_called_once()


def test_describe_moving_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_moving_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_moving_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe moving addresses"):
        describe_moving_addresses(region_name=REGION)


def test_describe_nat_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_nat_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_nat_gateways(region_name=REGION)
    mock_client.describe_nat_gateways.assert_called_once()


def test_describe_nat_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_nat_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_nat_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe nat gateways"):
        describe_nat_gateways(region_name=REGION)


def test_describe_network_acls(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_acls.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_acls(region_name=REGION)
    mock_client.describe_network_acls.assert_called_once()


def test_describe_network_acls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_acls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_acls",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network acls"):
        describe_network_acls(region_name=REGION)


def test_describe_network_insights_access_scope_analyses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scope_analyses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_access_scope_analyses(region_name=REGION)
    mock_client.describe_network_insights_access_scope_analyses.assert_called_once()


def test_describe_network_insights_access_scope_analyses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scope_analyses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_insights_access_scope_analyses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network insights access scope analyses"):
        describe_network_insights_access_scope_analyses(region_name=REGION)


def test_describe_network_insights_access_scopes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scopes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_access_scopes(region_name=REGION)
    mock_client.describe_network_insights_access_scopes.assert_called_once()


def test_describe_network_insights_access_scopes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scopes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_insights_access_scopes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network insights access scopes"):
        describe_network_insights_access_scopes(region_name=REGION)


def test_describe_network_insights_analyses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_analyses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_analyses(region_name=REGION)
    mock_client.describe_network_insights_analyses.assert_called_once()


def test_describe_network_insights_analyses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_analyses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_insights_analyses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network insights analyses"):
        describe_network_insights_analyses(region_name=REGION)


def test_describe_network_insights_paths(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_paths.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_paths(region_name=REGION)
    mock_client.describe_network_insights_paths.assert_called_once()


def test_describe_network_insights_paths_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_insights_paths.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_insights_paths",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network insights paths"):
        describe_network_insights_paths(region_name=REGION)


def test_describe_network_interface_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interface_attribute("test-network_interface_id", region_name=REGION)
    mock_client.describe_network_interface_attribute.assert_called_once()


def test_describe_network_interface_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interface_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_interface_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network interface attribute"):
        describe_network_interface_attribute("test-network_interface_id", region_name=REGION)


def test_describe_network_interface_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interface_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interface_permissions(region_name=REGION)
    mock_client.describe_network_interface_permissions.assert_called_once()


def test_describe_network_interface_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interface_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_interface_permissions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network interface permissions"):
        describe_network_interface_permissions(region_name=REGION)


def test_describe_network_interfaces(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interfaces(region_name=REGION)
    mock_client.describe_network_interfaces.assert_called_once()


def test_describe_network_interfaces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_network_interfaces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_network_interfaces",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe network interfaces"):
        describe_network_interfaces(region_name=REGION)


def test_describe_outpost_lags(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_outpost_lags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_outpost_lags(region_name=REGION)
    mock_client.describe_outpost_lags.assert_called_once()


def test_describe_outpost_lags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_outpost_lags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_outpost_lags",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe outpost lags"):
        describe_outpost_lags(region_name=REGION)


def test_describe_placement_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_placement_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_placement_groups(region_name=REGION)
    mock_client.describe_placement_groups.assert_called_once()


def test_describe_placement_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_placement_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_placement_groups",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe placement groups"):
        describe_placement_groups(region_name=REGION)


def test_describe_prefix_lists(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_prefix_lists.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_prefix_lists(region_name=REGION)
    mock_client.describe_prefix_lists.assert_called_once()


def test_describe_prefix_lists_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_prefix_lists.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_prefix_lists",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe prefix lists"):
        describe_prefix_lists(region_name=REGION)


def test_describe_principal_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_principal_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_principal_id_format(region_name=REGION)
    mock_client.describe_principal_id_format.assert_called_once()


def test_describe_principal_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_principal_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_principal_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe principal id format"):
        describe_principal_id_format(region_name=REGION)


def test_describe_public_ipv4_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_public_ipv4_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_public_ipv4_pools(region_name=REGION)
    mock_client.describe_public_ipv4_pools.assert_called_once()


def test_describe_public_ipv4_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_public_ipv4_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_public_ipv4_pools",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe public ipv4 pools"):
        describe_public_ipv4_pools(region_name=REGION)


def test_describe_regions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_regions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_regions(region_name=REGION)
    mock_client.describe_regions.assert_called_once()


def test_describe_regions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_regions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_regions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe regions"):
        describe_regions(region_name=REGION)


def test_describe_replace_root_volume_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replace_root_volume_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_replace_root_volume_tasks(region_name=REGION)
    mock_client.describe_replace_root_volume_tasks.assert_called_once()


def test_describe_replace_root_volume_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replace_root_volume_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replace_root_volume_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe replace root volume tasks"):
        describe_replace_root_volume_tasks(region_name=REGION)


def test_describe_reserved_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances(region_name=REGION)
    mock_client.describe_reserved_instances.assert_called_once()


def test_describe_reserved_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved instances"):
        describe_reserved_instances(region_name=REGION)


def test_describe_reserved_instances_listings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_listings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_listings(region_name=REGION)
    mock_client.describe_reserved_instances_listings.assert_called_once()


def test_describe_reserved_instances_listings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_listings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_instances_listings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved instances listings"):
        describe_reserved_instances_listings(region_name=REGION)


def test_describe_reserved_instances_modifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_modifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_modifications(region_name=REGION)
    mock_client.describe_reserved_instances_modifications.assert_called_once()


def test_describe_reserved_instances_modifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_modifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_instances_modifications",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved instances modifications"):
        describe_reserved_instances_modifications(region_name=REGION)


def test_describe_reserved_instances_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_offerings(region_name=REGION)
    mock_client.describe_reserved_instances_offerings.assert_called_once()


def test_describe_reserved_instances_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_instances_offerings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved instances offerings"):
        describe_reserved_instances_offerings(region_name=REGION)


def test_describe_route_server_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_server_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_server_endpoints(region_name=REGION)
    mock_client.describe_route_server_endpoints.assert_called_once()


def test_describe_route_server_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_server_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_route_server_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe route server endpoints"):
        describe_route_server_endpoints(region_name=REGION)


def test_describe_route_server_peers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_server_peers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_server_peers(region_name=REGION)
    mock_client.describe_route_server_peers.assert_called_once()


def test_describe_route_server_peers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_server_peers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_route_server_peers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe route server peers"):
        describe_route_server_peers(region_name=REGION)


def test_describe_route_servers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_servers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_servers(region_name=REGION)
    mock_client.describe_route_servers.assert_called_once()


def test_describe_route_servers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_servers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_route_servers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe route servers"):
        describe_route_servers(region_name=REGION)


def test_describe_route_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_tables(region_name=REGION)
    mock_client.describe_route_tables.assert_called_once()


def test_describe_route_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_route_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_route_tables",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe route tables"):
        describe_route_tables(region_name=REGION)


def test_describe_scheduled_instance_availability(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_instance_availability.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_instance_availability({}, {}, region_name=REGION)
    mock_client.describe_scheduled_instance_availability.assert_called_once()


def test_describe_scheduled_instance_availability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_instance_availability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_instance_availability",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scheduled instance availability"):
        describe_scheduled_instance_availability({}, {}, region_name=REGION)


def test_describe_scheduled_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_instances(region_name=REGION)
    mock_client.describe_scheduled_instances.assert_called_once()


def test_describe_scheduled_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scheduled instances"):
        describe_scheduled_instances(region_name=REGION)


def test_describe_security_group_references(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_references.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_security_group_references([], region_name=REGION)
    mock_client.describe_security_group_references.assert_called_once()


def test_describe_security_group_references_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_references.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_group_references",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security group references"):
        describe_security_group_references([], region_name=REGION)


def test_describe_security_group_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_security_group_rules(region_name=REGION)
    mock_client.describe_security_group_rules.assert_called_once()


def test_describe_security_group_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_group_rules",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security group rules"):
        describe_security_group_rules(region_name=REGION)


def test_describe_security_group_vpc_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_security_group_vpc_associations(region_name=REGION)
    mock_client.describe_security_group_vpc_associations.assert_called_once()


def test_describe_security_group_vpc_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_group_vpc_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_group_vpc_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security group vpc associations"):
        describe_security_group_vpc_associations(region_name=REGION)


def test_describe_service_link_virtual_interfaces(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_link_virtual_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_service_link_virtual_interfaces(region_name=REGION)
    mock_client.describe_service_link_virtual_interfaces.assert_called_once()


def test_describe_service_link_virtual_interfaces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_link_virtual_interfaces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_link_virtual_interfaces",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service link virtual interfaces"):
        describe_service_link_virtual_interfaces(region_name=REGION)


def test_describe_snapshot_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_attribute("test-attribute", "test-snapshot_id", region_name=REGION)
    mock_client.describe_snapshot_attribute.assert_called_once()


def test_describe_snapshot_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshot_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshot attribute"):
        describe_snapshot_attribute("test-attribute", "test-snapshot_id", region_name=REGION)


def test_describe_snapshot_tier_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_tier_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_tier_status(region_name=REGION)
    mock_client.describe_snapshot_tier_status.assert_called_once()


def test_describe_snapshot_tier_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_tier_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshot_tier_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshot tier status"):
        describe_snapshot_tier_status(region_name=REGION)


def test_describe_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_snapshots(region_name=REGION)
    mock_client.describe_snapshots.assert_called_once()


def test_describe_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshots",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshots"):
        describe_snapshots(region_name=REGION)


def test_describe_spot_datafeed_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_datafeed_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_datafeed_subscription(region_name=REGION)
    mock_client.describe_spot_datafeed_subscription.assert_called_once()


def test_describe_spot_datafeed_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_datafeed_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_datafeed_subscription",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot datafeed subscription"):
        describe_spot_datafeed_subscription(region_name=REGION)


def test_describe_spot_fleet_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_instances("test-spot_fleet_request_id", region_name=REGION)
    mock_client.describe_spot_fleet_instances.assert_called_once()


def test_describe_spot_fleet_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_fleet_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot fleet instances"):
        describe_spot_fleet_instances("test-spot_fleet_request_id", region_name=REGION)


def test_describe_spot_fleet_request_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_request_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", region_name=REGION)
    mock_client.describe_spot_fleet_request_history.assert_called_once()


def test_describe_spot_fleet_request_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_request_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_fleet_request_history",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot fleet request history"):
        describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", region_name=REGION)


def test_describe_spot_fleet_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_requests(region_name=REGION)
    mock_client.describe_spot_fleet_requests.assert_called_once()


def test_describe_spot_fleet_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_fleet_requests",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot fleet requests"):
        describe_spot_fleet_requests(region_name=REGION)


def test_describe_spot_instance_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_instance_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_instance_requests(region_name=REGION)
    mock_client.describe_spot_instance_requests.assert_called_once()


def test_describe_spot_instance_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_instance_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_instance_requests",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot instance requests"):
        describe_spot_instance_requests(region_name=REGION)


def test_describe_spot_price_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_price_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_price_history(region_name=REGION)
    mock_client.describe_spot_price_history.assert_called_once()


def test_describe_spot_price_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_spot_price_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_spot_price_history",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe spot price history"):
        describe_spot_price_history(region_name=REGION)


def test_describe_stale_security_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stale_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_stale_security_groups("test-vpc_id", region_name=REGION)
    mock_client.describe_stale_security_groups.assert_called_once()


def test_describe_stale_security_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stale_security_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stale_security_groups",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stale security groups"):
        describe_stale_security_groups("test-vpc_id", region_name=REGION)


def test_describe_store_image_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_store_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_store_image_tasks(region_name=REGION)
    mock_client.describe_store_image_tasks.assert_called_once()


def test_describe_store_image_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_store_image_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_store_image_tasks",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe store image tasks"):
        describe_store_image_tasks(region_name=REGION)


def test_describe_subnets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_subnets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_subnets(region_name=REGION)
    mock_client.describe_subnets.assert_called_once()


def test_describe_subnets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_subnets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_subnets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe subnets"):
        describe_subnets(region_name=REGION)


def test_describe_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_tags(region_name=REGION)
    mock_client.describe_tags.assert_called_once()


def test_describe_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tags",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tags"):
        describe_tags(region_name=REGION)


def test_describe_traffic_mirror_filter_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filter_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_filter_rules(region_name=REGION)
    mock_client.describe_traffic_mirror_filter_rules.assert_called_once()


def test_describe_traffic_mirror_filter_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filter_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_mirror_filter_rules",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic mirror filter rules"):
        describe_traffic_mirror_filter_rules(region_name=REGION)


def test_describe_traffic_mirror_filters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filters.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_filters(region_name=REGION)
    mock_client.describe_traffic_mirror_filters.assert_called_once()


def test_describe_traffic_mirror_filters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_mirror_filters",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic mirror filters"):
        describe_traffic_mirror_filters(region_name=REGION)


def test_describe_traffic_mirror_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_sessions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_sessions(region_name=REGION)
    mock_client.describe_traffic_mirror_sessions.assert_called_once()


def test_describe_traffic_mirror_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_mirror_sessions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic mirror sessions"):
        describe_traffic_mirror_sessions(region_name=REGION)


def test_describe_traffic_mirror_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_targets(region_name=REGION)
    mock_client.describe_traffic_mirror_targets.assert_called_once()


def test_describe_traffic_mirror_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_mirror_targets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic mirror targets"):
        describe_traffic_mirror_targets(region_name=REGION)


def test_describe_transit_gateway_attachments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_attachments(region_name=REGION)
    mock_client.describe_transit_gateway_attachments.assert_called_once()


def test_describe_transit_gateway_attachments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_attachments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_attachments",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway attachments"):
        describe_transit_gateway_attachments(region_name=REGION)


def test_describe_transit_gateway_connect_peers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connect_peers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_connect_peers(region_name=REGION)
    mock_client.describe_transit_gateway_connect_peers.assert_called_once()


def test_describe_transit_gateway_connect_peers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connect_peers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_connect_peers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway connect peers"):
        describe_transit_gateway_connect_peers(region_name=REGION)


def test_describe_transit_gateway_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connects.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_connects(region_name=REGION)
    mock_client.describe_transit_gateway_connects.assert_called_once()


def test_describe_transit_gateway_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_connects",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway connects"):
        describe_transit_gateway_connects(region_name=REGION)


def test_describe_transit_gateway_multicast_domains(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_multicast_domains.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_multicast_domains(region_name=REGION)
    mock_client.describe_transit_gateway_multicast_domains.assert_called_once()


def test_describe_transit_gateway_multicast_domains_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_multicast_domains.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_multicast_domains",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway multicast domains"):
        describe_transit_gateway_multicast_domains(region_name=REGION)


def test_describe_transit_gateway_peering_attachments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_peering_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_peering_attachments(region_name=REGION)
    mock_client.describe_transit_gateway_peering_attachments.assert_called_once()


def test_describe_transit_gateway_peering_attachments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_peering_attachments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_peering_attachments",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway peering attachments"):
        describe_transit_gateway_peering_attachments(region_name=REGION)


def test_describe_transit_gateway_policy_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_policy_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_policy_tables(region_name=REGION)
    mock_client.describe_transit_gateway_policy_tables.assert_called_once()


def test_describe_transit_gateway_policy_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_policy_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_policy_tables",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway policy tables"):
        describe_transit_gateway_policy_tables(region_name=REGION)


def test_describe_transit_gateway_route_table_announcements(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_table_announcements.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_route_table_announcements(region_name=REGION)
    mock_client.describe_transit_gateway_route_table_announcements.assert_called_once()


def test_describe_transit_gateway_route_table_announcements_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_table_announcements.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_route_table_announcements",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway route table announcements"):
        describe_transit_gateway_route_table_announcements(region_name=REGION)


def test_describe_transit_gateway_route_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_route_tables(region_name=REGION)
    mock_client.describe_transit_gateway_route_tables.assert_called_once()


def test_describe_transit_gateway_route_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_route_tables",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway route tables"):
        describe_transit_gateway_route_tables(region_name=REGION)


def test_describe_transit_gateway_vpc_attachments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_vpc_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_vpc_attachments(region_name=REGION)
    mock_client.describe_transit_gateway_vpc_attachments.assert_called_once()


def test_describe_transit_gateway_vpc_attachments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_vpc_attachments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateway_vpc_attachments",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateway vpc attachments"):
        describe_transit_gateway_vpc_attachments(region_name=REGION)


def test_describe_transit_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateways(region_name=REGION)
    mock_client.describe_transit_gateways.assert_called_once()


def test_describe_transit_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_transit_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_transit_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe transit gateways"):
        describe_transit_gateways(region_name=REGION)


def test_describe_trunk_interface_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trunk_interface_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_trunk_interface_associations(region_name=REGION)
    mock_client.describe_trunk_interface_associations.assert_called_once()


def test_describe_trunk_interface_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trunk_interface_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_trunk_interface_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe trunk interface associations"):
        describe_trunk_interface_associations(region_name=REGION)


def test_describe_verified_access_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_endpoints(region_name=REGION)
    mock_client.describe_verified_access_endpoints.assert_called_once()


def test_describe_verified_access_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_verified_access_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe verified access endpoints"):
        describe_verified_access_endpoints(region_name=REGION)


def test_describe_verified_access_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_groups(region_name=REGION)
    mock_client.describe_verified_access_groups.assert_called_once()


def test_describe_verified_access_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_verified_access_groups",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe verified access groups"):
        describe_verified_access_groups(region_name=REGION)


def test_describe_verified_access_instance_logging_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_instance_logging_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_instance_logging_configurations(region_name=REGION)
    mock_client.describe_verified_access_instance_logging_configurations.assert_called_once()


def test_describe_verified_access_instance_logging_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_instance_logging_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_verified_access_instance_logging_configurations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe verified access instance logging configurations"):
        describe_verified_access_instance_logging_configurations(region_name=REGION)


def test_describe_verified_access_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_instances(region_name=REGION)
    mock_client.describe_verified_access_instances.assert_called_once()


def test_describe_verified_access_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_verified_access_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe verified access instances"):
        describe_verified_access_instances(region_name=REGION)


def test_describe_verified_access_trust_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_trust_providers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_trust_providers(region_name=REGION)
    mock_client.describe_verified_access_trust_providers.assert_called_once()


def test_describe_verified_access_trust_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_verified_access_trust_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_verified_access_trust_providers",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe verified access trust providers"):
        describe_verified_access_trust_providers(region_name=REGION)


def test_describe_volume_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volume_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volume_attribute("test-attribute", "test-volume_id", region_name=REGION)
    mock_client.describe_volume_attribute.assert_called_once()


def test_describe_volume_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volume_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_volume_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe volume attribute"):
        describe_volume_attribute("test-attribute", "test-volume_id", region_name=REGION)


def test_describe_volume_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volume_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volume_status(region_name=REGION)
    mock_client.describe_volume_status.assert_called_once()


def test_describe_volume_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volume_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_volume_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe volume status"):
        describe_volume_status(region_name=REGION)


def test_describe_volumes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volumes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volumes(region_name=REGION)
    mock_client.describe_volumes.assert_called_once()


def test_describe_volumes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volumes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_volumes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe volumes"):
        describe_volumes(region_name=REGION)


def test_describe_volumes_modifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volumes_modifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volumes_modifications(region_name=REGION)
    mock_client.describe_volumes_modifications.assert_called_once()


def test_describe_volumes_modifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_volumes_modifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_volumes_modifications",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe volumes modifications"):
        describe_volumes_modifications(region_name=REGION)


def test_describe_vpc_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_attribute("test-attribute", "test-vpc_id", region_name=REGION)
    mock_client.describe_vpc_attribute.assert_called_once()


def test_describe_vpc_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc attribute"):
        describe_vpc_attribute("test-attribute", "test-vpc_id", region_name=REGION)


def test_describe_vpc_block_public_access_exclusions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_block_public_access_exclusions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_block_public_access_exclusions(region_name=REGION)
    mock_client.describe_vpc_block_public_access_exclusions.assert_called_once()


def test_describe_vpc_block_public_access_exclusions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_block_public_access_exclusions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_block_public_access_exclusions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc block public access exclusions"):
        describe_vpc_block_public_access_exclusions(region_name=REGION)


def test_describe_vpc_block_public_access_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_block_public_access_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_block_public_access_options(region_name=REGION)
    mock_client.describe_vpc_block_public_access_options.assert_called_once()


def test_describe_vpc_block_public_access_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_block_public_access_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_block_public_access_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc block public access options"):
        describe_vpc_block_public_access_options(region_name=REGION)


def test_describe_vpc_classic_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_classic_link(region_name=REGION)
    mock_client.describe_vpc_classic_link.assert_called_once()


def test_describe_vpc_classic_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_classic_link",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc classic link"):
        describe_vpc_classic_link(region_name=REGION)


def test_describe_vpc_classic_link_dns_support(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_classic_link_dns_support(region_name=REGION)
    mock_client.describe_vpc_classic_link_dns_support.assert_called_once()


def test_describe_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link_dns_support.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_classic_link_dns_support",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc classic link dns support"):
        describe_vpc_classic_link_dns_support(region_name=REGION)


def test_describe_vpc_endpoint_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_associations(region_name=REGION)
    mock_client.describe_vpc_endpoint_associations.assert_called_once()


def test_describe_vpc_endpoint_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint associations"):
        describe_vpc_endpoint_associations(region_name=REGION)


def test_describe_vpc_endpoint_connection_notifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connection_notifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_connection_notifications(region_name=REGION)
    mock_client.describe_vpc_endpoint_connection_notifications.assert_called_once()


def test_describe_vpc_endpoint_connection_notifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connection_notifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_connection_notifications",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint connection notifications"):
        describe_vpc_endpoint_connection_notifications(region_name=REGION)


def test_describe_vpc_endpoint_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_connections(region_name=REGION)
    mock_client.describe_vpc_endpoint_connections.assert_called_once()


def test_describe_vpc_endpoint_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint connections"):
        describe_vpc_endpoint_connections(region_name=REGION)


def test_describe_vpc_endpoint_service_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_service_configurations(region_name=REGION)
    mock_client.describe_vpc_endpoint_service_configurations.assert_called_once()


def test_describe_vpc_endpoint_service_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_service_configurations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint service configurations"):
        describe_vpc_endpoint_service_configurations(region_name=REGION)


def test_describe_vpc_endpoint_service_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_service_permissions("test-service_id", region_name=REGION)
    mock_client.describe_vpc_endpoint_service_permissions.assert_called_once()


def test_describe_vpc_endpoint_service_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_service_permissions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint service permissions"):
        describe_vpc_endpoint_service_permissions("test-service_id", region_name=REGION)


def test_describe_vpc_endpoint_services(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_services.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_services(region_name=REGION)
    mock_client.describe_vpc_endpoint_services.assert_called_once()


def test_describe_vpc_endpoint_services_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_services.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoint_services",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoint services"):
        describe_vpc_endpoint_services(region_name=REGION)


def test_describe_vpc_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoints(region_name=REGION)
    mock_client.describe_vpc_endpoints.assert_called_once()


def test_describe_vpc_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_endpoints",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc endpoints"):
        describe_vpc_endpoints(region_name=REGION)


def test_describe_vpc_peering_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_peering_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_peering_connections(region_name=REGION)
    mock_client.describe_vpc_peering_connections.assert_called_once()


def test_describe_vpc_peering_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_peering_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_peering_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc peering connections"):
        describe_vpc_peering_connections(region_name=REGION)


def test_describe_vpcs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpcs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpcs(region_name=REGION)
    mock_client.describe_vpcs.assert_called_once()


def test_describe_vpcs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpcs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpcs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpcs"):
        describe_vpcs(region_name=REGION)


def test_describe_vpn_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpn_connections(region_name=REGION)
    mock_client.describe_vpn_connections.assert_called_once()


def test_describe_vpn_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpn_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpn_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpn connections"):
        describe_vpn_connections(region_name=REGION)


def test_describe_vpn_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpn_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpn_gateways(region_name=REGION)
    mock_client.describe_vpn_gateways.assert_called_once()


def test_describe_vpn_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpn_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpn_gateways",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpn gateways"):
        describe_vpn_gateways(region_name=REGION)


def test_detach_classic_link_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_classic_link_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_classic_link_vpc("test-instance_id", "test-vpc_id", region_name=REGION)
    mock_client.detach_classic_link_vpc.assert_called_once()


def test_detach_classic_link_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_classic_link_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_classic_link_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach classic link vpc"):
        detach_classic_link_vpc("test-instance_id", "test-vpc_id", region_name=REGION)


def test_detach_internet_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_internet_gateway("test-internet_gateway_id", "test-vpc_id", region_name=REGION)
    mock_client.detach_internet_gateway.assert_called_once()


def test_detach_internet_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_internet_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_internet_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach internet gateway"):
        detach_internet_gateway("test-internet_gateway_id", "test-vpc_id", region_name=REGION)


def test_detach_network_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_network_interface("test-attachment_id", region_name=REGION)
    mock_client.detach_network_interface.assert_called_once()


def test_detach_network_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_network_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_network_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach network interface"):
        detach_network_interface("test-attachment_id", region_name=REGION)


def test_detach_verified_access_trust_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", region_name=REGION)
    mock_client.detach_verified_access_trust_provider.assert_called_once()


def test_detach_verified_access_trust_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_verified_access_trust_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_verified_access_trust_provider",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach verified access trust provider"):
        detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", region_name=REGION)


def test_detach_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_volume("test-volume_id", region_name=REGION)
    mock_client.detach_volume.assert_called_once()


def test_detach_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach volume"):
        detach_volume("test-volume_id", region_name=REGION)


def test_detach_vpn_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_vpn_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", region_name=REGION)
    mock_client.detach_vpn_gateway.assert_called_once()


def test_detach_vpn_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_vpn_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_vpn_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach vpn gateway"):
        detach_vpn_gateway("test-vpc_id", "test-vpn_gateway_id", region_name=REGION)


def test_disable_address_transfer(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_address_transfer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_address_transfer("test-allocation_id", region_name=REGION)
    mock_client.disable_address_transfer.assert_called_once()


def test_disable_address_transfer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_address_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_address_transfer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable address transfer"):
        disable_address_transfer("test-allocation_id", region_name=REGION)


def test_disable_allowed_images_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_allowed_images_settings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_allowed_images_settings(region_name=REGION)
    mock_client.disable_allowed_images_settings.assert_called_once()


def test_disable_allowed_images_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_allowed_images_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_allowed_images_settings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable allowed images settings"):
        disable_allowed_images_settings(region_name=REGION)


def test_disable_aws_network_performance_metric_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_aws_network_performance_metric_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_aws_network_performance_metric_subscription(region_name=REGION)
    mock_client.disable_aws_network_performance_metric_subscription.assert_called_once()


def test_disable_aws_network_performance_metric_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_aws_network_performance_metric_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_aws_network_performance_metric_subscription",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable aws network performance metric subscription"):
        disable_aws_network_performance_metric_subscription(region_name=REGION)


def test_disable_capacity_manager(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_capacity_manager.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_capacity_manager(region_name=REGION)
    mock_client.disable_capacity_manager.assert_called_once()


def test_disable_capacity_manager_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_capacity_manager.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_capacity_manager",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable capacity manager"):
        disable_capacity_manager(region_name=REGION)


def test_disable_ebs_encryption_by_default(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_ebs_encryption_by_default.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_ebs_encryption_by_default(region_name=REGION)
    mock_client.disable_ebs_encryption_by_default.assert_called_once()


def test_disable_ebs_encryption_by_default_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_ebs_encryption_by_default.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_ebs_encryption_by_default",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable ebs encryption by default"):
        disable_ebs_encryption_by_default(region_name=REGION)


def test_disable_fast_launch(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_fast_launch.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_fast_launch("test-image_id", region_name=REGION)
    mock_client.disable_fast_launch.assert_called_once()


def test_disable_fast_launch_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_fast_launch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_fast_launch",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable fast launch"):
        disable_fast_launch("test-image_id", region_name=REGION)


def test_disable_fast_snapshot_restores(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_fast_snapshot_restores([], region_name=REGION)
    mock_client.disable_fast_snapshot_restores.assert_called_once()


def test_disable_fast_snapshot_restores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_fast_snapshot_restores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_fast_snapshot_restores",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable fast snapshot restores"):
        disable_fast_snapshot_restores([], region_name=REGION)


def test_disable_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_image("test-image_id", region_name=REGION)
    mock_client.disable_image.assert_called_once()


def test_disable_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable image"):
        disable_image("test-image_id", region_name=REGION)


def test_disable_image_block_public_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_block_public_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_image_block_public_access(region_name=REGION)
    mock_client.disable_image_block_public_access.assert_called_once()


def test_disable_image_block_public_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_block_public_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_image_block_public_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable image block public access"):
        disable_image_block_public_access(region_name=REGION)


def test_disable_image_deprecation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_deprecation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_image_deprecation("test-image_id", region_name=REGION)
    mock_client.disable_image_deprecation.assert_called_once()


def test_disable_image_deprecation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_deprecation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_image_deprecation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable image deprecation"):
        disable_image_deprecation("test-image_id", region_name=REGION)


def test_disable_image_deregistration_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_deregistration_protection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_image_deregistration_protection("test-image_id", region_name=REGION)
    mock_client.disable_image_deregistration_protection.assert_called_once()


def test_disable_image_deregistration_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_image_deregistration_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_image_deregistration_protection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable image deregistration protection"):
        disable_image_deregistration_protection("test-image_id", region_name=REGION)


def test_disable_ipam_organization_admin_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_ipam_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_ipam_organization_admin_account("test-delegated_admin_account_id", region_name=REGION)
    mock_client.disable_ipam_organization_admin_account.assert_called_once()


def test_disable_ipam_organization_admin_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_ipam_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_ipam_organization_admin_account",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable ipam organization admin account"):
        disable_ipam_organization_admin_account("test-delegated_admin_account_id", region_name=REGION)


def test_disable_route_server_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_route_server_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_route_server_propagation("test-route_server_id", "test-route_table_id", region_name=REGION)
    mock_client.disable_route_server_propagation.assert_called_once()


def test_disable_route_server_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_route_server_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_route_server_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable route server propagation"):
        disable_route_server_propagation("test-route_server_id", "test-route_table_id", region_name=REGION)


def test_disable_serial_console_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_serial_console_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_serial_console_access(region_name=REGION)
    mock_client.disable_serial_console_access.assert_called_once()


def test_disable_serial_console_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_serial_console_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_serial_console_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable serial console access"):
        disable_serial_console_access(region_name=REGION)


def test_disable_snapshot_block_public_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_snapshot_block_public_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_snapshot_block_public_access(region_name=REGION)
    mock_client.disable_snapshot_block_public_access.assert_called_once()


def test_disable_snapshot_block_public_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_snapshot_block_public_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_snapshot_block_public_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable snapshot block public access"):
        disable_snapshot_block_public_access(region_name=REGION)


def test_disable_transit_gateway_route_table_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_transit_gateway_route_table_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.disable_transit_gateway_route_table_propagation.assert_called_once()


def test_disable_transit_gateway_route_table_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_transit_gateway_route_table_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_transit_gateway_route_table_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable transit gateway route table propagation"):
        disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", region_name=REGION)


def test_disable_vgw_route_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vgw_route_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_vgw_route_propagation("test-gateway_id", "test-route_table_id", region_name=REGION)
    mock_client.disable_vgw_route_propagation.assert_called_once()


def test_disable_vgw_route_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vgw_route_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_vgw_route_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable vgw route propagation"):
        disable_vgw_route_propagation("test-gateway_id", "test-route_table_id", region_name=REGION)


def test_disable_vpc_classic_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vpc_classic_link.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_vpc_classic_link("test-vpc_id", region_name=REGION)
    mock_client.disable_vpc_classic_link.assert_called_once()


def test_disable_vpc_classic_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vpc_classic_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_vpc_classic_link",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable vpc classic link"):
        disable_vpc_classic_link("test-vpc_id", region_name=REGION)


def test_disable_vpc_classic_link_dns_support(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_vpc_classic_link_dns_support(region_name=REGION)
    mock_client.disable_vpc_classic_link_dns_support.assert_called_once()


def test_disable_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_vpc_classic_link_dns_support.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_vpc_classic_link_dns_support",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable vpc classic link dns support"):
        disable_vpc_classic_link_dns_support(region_name=REGION)


def test_disassociate_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_address(region_name=REGION)
    mock_client.disassociate_address.assert_called_once()


def test_disassociate_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate address"):
        disassociate_address(region_name=REGION)


def test_disassociate_capacity_reservation_billing_owner(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_capacity_reservation_billing_owner.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", region_name=REGION)
    mock_client.disassociate_capacity_reservation_billing_owner.assert_called_once()


def test_disassociate_capacity_reservation_billing_owner_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_capacity_reservation_billing_owner.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_capacity_reservation_billing_owner",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate capacity reservation billing owner"):
        disassociate_capacity_reservation_billing_owner("test-capacity_reservation_id", "test-unused_reservation_billing_owner_id", region_name=REGION)


def test_disassociate_client_vpn_target_network(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_client_vpn_target_network.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-association_id", region_name=REGION)
    mock_client.disassociate_client_vpn_target_network.assert_called_once()


def test_disassociate_client_vpn_target_network_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_client_vpn_target_network.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_client_vpn_target_network",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate client vpn target network"):
        disassociate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-association_id", region_name=REGION)


def test_disassociate_enclave_certificate_iam_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_enclave_certificate_iam_role.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", region_name=REGION)
    mock_client.disassociate_enclave_certificate_iam_role.assert_called_once()


def test_disassociate_enclave_certificate_iam_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_enclave_certificate_iam_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_enclave_certificate_iam_role",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate enclave certificate iam role"):
        disassociate_enclave_certificate_iam_role("test-certificate_arn", "test-role_arn", region_name=REGION)


def test_disassociate_iam_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_iam_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_iam_instance_profile("test-association_id", region_name=REGION)
    mock_client.disassociate_iam_instance_profile.assert_called_once()


def test_disassociate_iam_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_iam_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_iam_instance_profile",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate iam instance profile"):
        disassociate_iam_instance_profile("test-association_id", region_name=REGION)


def test_disassociate_instance_event_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_instance_event_window("test-instance_event_window_id", {}, region_name=REGION)
    mock_client.disassociate_instance_event_window.assert_called_once()


def test_disassociate_instance_event_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_instance_event_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_instance_event_window",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate instance event window"):
        disassociate_instance_event_window("test-instance_event_window_id", {}, region_name=REGION)


def test_disassociate_ipam_byoasn(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_ipam_byoasn("test-asn", "test-cidr", region_name=REGION)
    mock_client.disassociate_ipam_byoasn.assert_called_once()


def test_disassociate_ipam_byoasn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ipam_byoasn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_ipam_byoasn",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate ipam byoasn"):
        disassociate_ipam_byoasn("test-asn", "test-cidr", region_name=REGION)


def test_disassociate_ipam_resource_discovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_ipam_resource_discovery("test-ipam_resource_discovery_association_id", region_name=REGION)
    mock_client.disassociate_ipam_resource_discovery.assert_called_once()


def test_disassociate_ipam_resource_discovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ipam_resource_discovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_ipam_resource_discovery",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate ipam resource discovery"):
        disassociate_ipam_resource_discovery("test-ipam_resource_discovery_association_id", region_name=REGION)


def test_disassociate_nat_gateway_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)
    mock_client.disassociate_nat_gateway_address.assert_called_once()


def test_disassociate_nat_gateway_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_nat_gateway_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_nat_gateway_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate nat gateway address"):
        disassociate_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)


def test_disassociate_route_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_route_server("test-route_server_id", "test-vpc_id", region_name=REGION)
    mock_client.disassociate_route_server.assert_called_once()


def test_disassociate_route_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_route_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_route_server",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate route server"):
        disassociate_route_server("test-route_server_id", "test-vpc_id", region_name=REGION)


def test_disassociate_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_route_table("test-association_id", region_name=REGION)
    mock_client.disassociate_route_table.assert_called_once()


def test_disassociate_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate route table"):
        disassociate_route_table("test-association_id", region_name=REGION)


def test_disassociate_security_group_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_security_group_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_security_group_vpc("test-group_id", "test-vpc_id", region_name=REGION)
    mock_client.disassociate_security_group_vpc.assert_called_once()


def test_disassociate_security_group_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_security_group_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_security_group_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate security group vpc"):
        disassociate_security_group_vpc("test-group_id", "test-vpc_id", region_name=REGION)


def test_disassociate_subnet_cidr_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_subnet_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_subnet_cidr_block("test-association_id", region_name=REGION)
    mock_client.disassociate_subnet_cidr_block.assert_called_once()


def test_disassociate_subnet_cidr_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_subnet_cidr_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_subnet_cidr_block",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate subnet cidr block"):
        disassociate_subnet_cidr_block("test-association_id", region_name=REGION)


def test_disassociate_transit_gateway_multicast_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_multicast_domain.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], region_name=REGION)
    mock_client.disassociate_transit_gateway_multicast_domain.assert_called_once()


def test_disassociate_transit_gateway_multicast_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_multicast_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_transit_gateway_multicast_domain",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate transit gateway multicast domain"):
        disassociate_transit_gateway_multicast_domain("test-transit_gateway_multicast_domain_id", "test-transit_gateway_attachment_id", [], region_name=REGION)


def test_disassociate_transit_gateway_policy_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_policy_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.disassociate_transit_gateway_policy_table.assert_called_once()


def test_disassociate_transit_gateway_policy_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_policy_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_transit_gateway_policy_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate transit gateway policy table"):
        disassociate_transit_gateway_policy_table("test-transit_gateway_policy_table_id", "test-transit_gateway_attachment_id", region_name=REGION)


def test_disassociate_transit_gateway_route_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.disassociate_transit_gateway_route_table.assert_called_once()


def test_disassociate_transit_gateway_route_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_transit_gateway_route_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_transit_gateway_route_table",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate transit gateway route table"):
        disassociate_transit_gateway_route_table("test-transit_gateway_route_table_id", "test-transit_gateway_attachment_id", region_name=REGION)


def test_disassociate_trunk_interface(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_trunk_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_trunk_interface("test-association_id", region_name=REGION)
    mock_client.disassociate_trunk_interface.assert_called_once()


def test_disassociate_trunk_interface_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_trunk_interface.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_trunk_interface",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate trunk interface"):
        disassociate_trunk_interface("test-association_id", region_name=REGION)


def test_disassociate_vpc_cidr_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_vpc_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_vpc_cidr_block("test-association_id", region_name=REGION)
    mock_client.disassociate_vpc_cidr_block.assert_called_once()


def test_disassociate_vpc_cidr_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_vpc_cidr_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_vpc_cidr_block",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate vpc cidr block"):
        disassociate_vpc_cidr_block("test-association_id", region_name=REGION)


def test_enable_address_transfer(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_address_transfer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_address_transfer("test-allocation_id", "test-transfer_account_id", region_name=REGION)
    mock_client.enable_address_transfer.assert_called_once()


def test_enable_address_transfer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_address_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_address_transfer",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable address transfer"):
        enable_address_transfer("test-allocation_id", "test-transfer_account_id", region_name=REGION)


def test_enable_allowed_images_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_allowed_images_settings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_allowed_images_settings("test-allowed_images_settings_state", region_name=REGION)
    mock_client.enable_allowed_images_settings.assert_called_once()


def test_enable_allowed_images_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_allowed_images_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_allowed_images_settings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable allowed images settings"):
        enable_allowed_images_settings("test-allowed_images_settings_state", region_name=REGION)


def test_enable_aws_network_performance_metric_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_aws_network_performance_metric_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_aws_network_performance_metric_subscription(region_name=REGION)
    mock_client.enable_aws_network_performance_metric_subscription.assert_called_once()


def test_enable_aws_network_performance_metric_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_aws_network_performance_metric_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_aws_network_performance_metric_subscription",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable aws network performance metric subscription"):
        enable_aws_network_performance_metric_subscription(region_name=REGION)


def test_enable_capacity_manager(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_capacity_manager.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_capacity_manager(region_name=REGION)
    mock_client.enable_capacity_manager.assert_called_once()


def test_enable_capacity_manager_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_capacity_manager.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_capacity_manager",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable capacity manager"):
        enable_capacity_manager(region_name=REGION)


def test_enable_ebs_encryption_by_default(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_ebs_encryption_by_default.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_ebs_encryption_by_default(region_name=REGION)
    mock_client.enable_ebs_encryption_by_default.assert_called_once()


def test_enable_ebs_encryption_by_default_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_ebs_encryption_by_default.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_ebs_encryption_by_default",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable ebs encryption by default"):
        enable_ebs_encryption_by_default(region_name=REGION)


def test_enable_fast_launch(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_fast_launch.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_fast_launch("test-image_id", region_name=REGION)
    mock_client.enable_fast_launch.assert_called_once()


def test_enable_fast_launch_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_fast_launch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_fast_launch",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable fast launch"):
        enable_fast_launch("test-image_id", region_name=REGION)


def test_enable_fast_snapshot_restores(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_fast_snapshot_restores([], region_name=REGION)
    mock_client.enable_fast_snapshot_restores.assert_called_once()


def test_enable_fast_snapshot_restores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_fast_snapshot_restores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_fast_snapshot_restores",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable fast snapshot restores"):
        enable_fast_snapshot_restores([], region_name=REGION)


def test_enable_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_image("test-image_id", region_name=REGION)
    mock_client.enable_image.assert_called_once()


def test_enable_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable image"):
        enable_image("test-image_id", region_name=REGION)


def test_enable_image_block_public_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_block_public_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_image_block_public_access("test-image_block_public_access_state", region_name=REGION)
    mock_client.enable_image_block_public_access.assert_called_once()


def test_enable_image_block_public_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_block_public_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_image_block_public_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable image block public access"):
        enable_image_block_public_access("test-image_block_public_access_state", region_name=REGION)


def test_enable_image_deprecation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_deprecation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_image_deprecation("test-image_id", "test-deprecate_at", region_name=REGION)
    mock_client.enable_image_deprecation.assert_called_once()


def test_enable_image_deprecation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_deprecation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_image_deprecation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable image deprecation"):
        enable_image_deprecation("test-image_id", "test-deprecate_at", region_name=REGION)


def test_enable_image_deregistration_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_deregistration_protection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_image_deregistration_protection("test-image_id", region_name=REGION)
    mock_client.enable_image_deregistration_protection.assert_called_once()


def test_enable_image_deregistration_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_image_deregistration_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_image_deregistration_protection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable image deregistration protection"):
        enable_image_deregistration_protection("test-image_id", region_name=REGION)


def test_enable_ipam_organization_admin_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_ipam_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_ipam_organization_admin_account("test-delegated_admin_account_id", region_name=REGION)
    mock_client.enable_ipam_organization_admin_account.assert_called_once()


def test_enable_ipam_organization_admin_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_ipam_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_ipam_organization_admin_account",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable ipam organization admin account"):
        enable_ipam_organization_admin_account("test-delegated_admin_account_id", region_name=REGION)


def test_enable_reachability_analyzer_organization_sharing(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_reachability_analyzer_organization_sharing.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_reachability_analyzer_organization_sharing(region_name=REGION)
    mock_client.enable_reachability_analyzer_organization_sharing.assert_called_once()


def test_enable_reachability_analyzer_organization_sharing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_reachability_analyzer_organization_sharing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_reachability_analyzer_organization_sharing",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable reachability analyzer organization sharing"):
        enable_reachability_analyzer_organization_sharing(region_name=REGION)


def test_enable_route_server_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_route_server_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_route_server_propagation("test-route_server_id", "test-route_table_id", region_name=REGION)
    mock_client.enable_route_server_propagation.assert_called_once()


def test_enable_route_server_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_route_server_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_route_server_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable route server propagation"):
        enable_route_server_propagation("test-route_server_id", "test-route_table_id", region_name=REGION)


def test_enable_serial_console_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_serial_console_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_serial_console_access(region_name=REGION)
    mock_client.enable_serial_console_access.assert_called_once()


def test_enable_serial_console_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_serial_console_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_serial_console_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable serial console access"):
        enable_serial_console_access(region_name=REGION)


def test_enable_snapshot_block_public_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_snapshot_block_public_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_snapshot_block_public_access("test-state", region_name=REGION)
    mock_client.enable_snapshot_block_public_access.assert_called_once()


def test_enable_snapshot_block_public_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_snapshot_block_public_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_snapshot_block_public_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable snapshot block public access"):
        enable_snapshot_block_public_access("test-state", region_name=REGION)


def test_enable_transit_gateway_route_table_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_transit_gateway_route_table_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.enable_transit_gateway_route_table_propagation.assert_called_once()


def test_enable_transit_gateway_route_table_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_transit_gateway_route_table_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_transit_gateway_route_table_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable transit gateway route table propagation"):
        enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", region_name=REGION)


def test_enable_vgw_route_propagation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vgw_route_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_vgw_route_propagation("test-gateway_id", "test-route_table_id", region_name=REGION)
    mock_client.enable_vgw_route_propagation.assert_called_once()


def test_enable_vgw_route_propagation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vgw_route_propagation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_vgw_route_propagation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable vgw route propagation"):
        enable_vgw_route_propagation("test-gateway_id", "test-route_table_id", region_name=REGION)


def test_enable_volume_io(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_volume_io.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_volume_io("test-volume_id", region_name=REGION)
    mock_client.enable_volume_io.assert_called_once()


def test_enable_volume_io_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_volume_io.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_volume_io",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable volume io"):
        enable_volume_io("test-volume_id", region_name=REGION)


def test_enable_vpc_classic_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vpc_classic_link.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_vpc_classic_link("test-vpc_id", region_name=REGION)
    mock_client.enable_vpc_classic_link.assert_called_once()


def test_enable_vpc_classic_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vpc_classic_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_vpc_classic_link",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable vpc classic link"):
        enable_vpc_classic_link("test-vpc_id", region_name=REGION)


def test_enable_vpc_classic_link_dns_support(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_vpc_classic_link_dns_support(region_name=REGION)
    mock_client.enable_vpc_classic_link_dns_support.assert_called_once()


def test_enable_vpc_classic_link_dns_support_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_vpc_classic_link_dns_support.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_vpc_classic_link_dns_support",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable vpc classic link dns support"):
        enable_vpc_classic_link_dns_support(region_name=REGION)


def test_export_client_vpn_client_certificate_revocation_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_client_vpn_client_certificate_revocation_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.export_client_vpn_client_certificate_revocation_list.assert_called_once()


def test_export_client_vpn_client_certificate_revocation_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_client_vpn_client_certificate_revocation_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_client_vpn_client_certificate_revocation_list",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export client vpn client certificate revocation list"):
        export_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", region_name=REGION)


def test_export_client_vpn_client_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_client_vpn_client_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_client_vpn_client_configuration("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.export_client_vpn_client_configuration.assert_called_once()


def test_export_client_vpn_client_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_client_vpn_client_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_client_vpn_client_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export client vpn client configuration"):
        export_client_vpn_client_configuration("test-client_vpn_endpoint_id", region_name=REGION)


def test_export_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_image("test-disk_image_format", "test-image_id", {}, region_name=REGION)
    mock_client.export_image.assert_called_once()


def test_export_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export image"):
        export_image("test-disk_image_format", "test-image_id", {}, region_name=REGION)


def test_export_transit_gateway_routes(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_transit_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", region_name=REGION)
    mock_client.export_transit_gateway_routes.assert_called_once()


def test_export_transit_gateway_routes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_transit_gateway_routes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_transit_gateway_routes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export transit gateway routes"):
        export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", region_name=REGION)


def test_export_verified_access_instance_client_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_verified_access_instance_client_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_verified_access_instance_client_configuration("test-verified_access_instance_id", region_name=REGION)
    mock_client.export_verified_access_instance_client_configuration.assert_called_once()


def test_export_verified_access_instance_client_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_verified_access_instance_client_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_verified_access_instance_client_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export verified access instance client configuration"):
        export_verified_access_instance_client_configuration("test-verified_access_instance_id", region_name=REGION)


def test_get_active_vpn_tunnel_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_active_vpn_tunnel_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_active_vpn_tunnel_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)
    mock_client.get_active_vpn_tunnel_status.assert_called_once()


def test_get_active_vpn_tunnel_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_active_vpn_tunnel_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_active_vpn_tunnel_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get active vpn tunnel status"):
        get_active_vpn_tunnel_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)


def test_get_allowed_images_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_allowed_images_settings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_allowed_images_settings(region_name=REGION)
    mock_client.get_allowed_images_settings.assert_called_once()


def test_get_allowed_images_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_allowed_images_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_allowed_images_settings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get allowed images settings"):
        get_allowed_images_settings(region_name=REGION)


def test_get_associated_enclave_certificate_iam_roles(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_associated_enclave_certificate_iam_roles.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_associated_enclave_certificate_iam_roles("test-certificate_arn", region_name=REGION)
    mock_client.get_associated_enclave_certificate_iam_roles.assert_called_once()


def test_get_associated_enclave_certificate_iam_roles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_associated_enclave_certificate_iam_roles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_associated_enclave_certificate_iam_roles",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get associated enclave certificate iam roles"):
        get_associated_enclave_certificate_iam_roles("test-certificate_arn", region_name=REGION)


def test_get_associated_ipv6_pool_cidrs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_associated_ipv6_pool_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_associated_ipv6_pool_cidrs("test-pool_id", region_name=REGION)
    mock_client.get_associated_ipv6_pool_cidrs.assert_called_once()


def test_get_associated_ipv6_pool_cidrs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_associated_ipv6_pool_cidrs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_associated_ipv6_pool_cidrs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get associated ipv6 pool cidrs"):
        get_associated_ipv6_pool_cidrs("test-pool_id", region_name=REGION)


def test_get_aws_network_performance_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aws_network_performance_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_aws_network_performance_data(region_name=REGION)
    mock_client.get_aws_network_performance_data.assert_called_once()


def test_get_aws_network_performance_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aws_network_performance_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aws_network_performance_data",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aws network performance data"):
        get_aws_network_performance_data(region_name=REGION)


def test_get_capacity_manager_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_manager_attributes(region_name=REGION)
    mock_client.get_capacity_manager_attributes.assert_called_once()


def test_get_capacity_manager_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_manager_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity manager attributes"):
        get_capacity_manager_attributes(region_name=REGION)


def test_get_capacity_manager_metric_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_manager_metric_data([], "test-start_time", "test-end_time", 1, region_name=REGION)
    mock_client.get_capacity_manager_metric_data.assert_called_once()


def test_get_capacity_manager_metric_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_manager_metric_data",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity manager metric data"):
        get_capacity_manager_metric_data([], "test-start_time", "test-end_time", 1, region_name=REGION)


def test_get_capacity_manager_metric_dimensions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_dimensions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_manager_metric_dimensions([], "test-start_time", "test-end_time", [], region_name=REGION)
    mock_client.get_capacity_manager_metric_dimensions.assert_called_once()


def test_get_capacity_manager_metric_dimensions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_dimensions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_manager_metric_dimensions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity manager metric dimensions"):
        get_capacity_manager_metric_dimensions([], "test-start_time", "test-end_time", [], region_name=REGION)


def test_get_capacity_reservation_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_reservation_usage.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_reservation_usage("test-capacity_reservation_id", region_name=REGION)
    mock_client.get_capacity_reservation_usage.assert_called_once()


def test_get_capacity_reservation_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_reservation_usage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_reservation_usage",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity reservation usage"):
        get_capacity_reservation_usage("test-capacity_reservation_id", region_name=REGION)


def test_get_coip_pool_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_coip_pool_usage.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_coip_pool_usage("test-pool_id", region_name=REGION)
    mock_client.get_coip_pool_usage.assert_called_once()


def test_get_coip_pool_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_coip_pool_usage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_coip_pool_usage",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get coip pool usage"):
        get_coip_pool_usage("test-pool_id", region_name=REGION)


def test_get_console_output(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_console_output.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_console_output("test-instance_id", region_name=REGION)
    mock_client.get_console_output.assert_called_once()


def test_get_console_output_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_console_output.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_console_output",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get console output"):
        get_console_output("test-instance_id", region_name=REGION)


def test_get_console_screenshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_console_screenshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_console_screenshot("test-instance_id", region_name=REGION)
    mock_client.get_console_screenshot.assert_called_once()


def test_get_console_screenshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_console_screenshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_console_screenshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get console screenshot"):
        get_console_screenshot("test-instance_id", region_name=REGION)


def test_get_declarative_policies_report_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_declarative_policies_report_summary.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_declarative_policies_report_summary("test-report_id", region_name=REGION)
    mock_client.get_declarative_policies_report_summary.assert_called_once()


def test_get_declarative_policies_report_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_declarative_policies_report_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_declarative_policies_report_summary",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get declarative policies report summary"):
        get_declarative_policies_report_summary("test-report_id", region_name=REGION)


def test_get_default_credit_specification(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_default_credit_specification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_default_credit_specification("test-instance_family", region_name=REGION)
    mock_client.get_default_credit_specification.assert_called_once()


def test_get_default_credit_specification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_default_credit_specification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_default_credit_specification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get default credit specification"):
        get_default_credit_specification("test-instance_family", region_name=REGION)


def test_get_ebs_default_kms_key_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ebs_default_kms_key_id.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ebs_default_kms_key_id(region_name=REGION)
    mock_client.get_ebs_default_kms_key_id.assert_called_once()


def test_get_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ebs_default_kms_key_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ebs_default_kms_key_id",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ebs default kms key id"):
        get_ebs_default_kms_key_id(region_name=REGION)


def test_get_ebs_encryption_by_default(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ebs_encryption_by_default.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ebs_encryption_by_default(region_name=REGION)
    mock_client.get_ebs_encryption_by_default.assert_called_once()


def test_get_ebs_encryption_by_default_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ebs_encryption_by_default.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ebs_encryption_by_default",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ebs encryption by default"):
        get_ebs_encryption_by_default(region_name=REGION)


def test_get_flow_logs_integration_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_logs_integration_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_flow_logs_integration_template("test-flow_log_id", "test-config_delivery_s3_destination_arn", {}, region_name=REGION)
    mock_client.get_flow_logs_integration_template.assert_called_once()


def test_get_flow_logs_integration_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_logs_integration_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_logs_integration_template",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow logs integration template"):
        get_flow_logs_integration_template("test-flow_log_id", "test-config_delivery_s3_destination_arn", {}, region_name=REGION)


def test_get_groups_for_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_groups_for_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_groups_for_capacity_reservation("test-capacity_reservation_id", region_name=REGION)
    mock_client.get_groups_for_capacity_reservation.assert_called_once()


def test_get_groups_for_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_groups_for_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_groups_for_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get groups for capacity reservation"):
        get_groups_for_capacity_reservation("test-capacity_reservation_id", region_name=REGION)


def test_get_host_reservation_purchase_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_host_reservation_purchase_preview.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_host_reservation_purchase_preview([], "test-offering_id", region_name=REGION)
    mock_client.get_host_reservation_purchase_preview.assert_called_once()


def test_get_host_reservation_purchase_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_host_reservation_purchase_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_host_reservation_purchase_preview",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get host reservation purchase preview"):
        get_host_reservation_purchase_preview([], "test-offering_id", region_name=REGION)


def test_get_image_ancestry(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_image_ancestry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_image_ancestry("test-image_id", region_name=REGION)
    mock_client.get_image_ancestry.assert_called_once()


def test_get_image_ancestry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_image_ancestry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_image_ancestry",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get image ancestry"):
        get_image_ancestry("test-image_id", region_name=REGION)


def test_get_image_block_public_access_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_image_block_public_access_state.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_image_block_public_access_state(region_name=REGION)
    mock_client.get_image_block_public_access_state.assert_called_once()


def test_get_image_block_public_access_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_image_block_public_access_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_image_block_public_access_state",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get image block public access state"):
        get_image_block_public_access_state(region_name=REGION)


def test_get_instance_metadata_defaults(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_metadata_defaults.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_instance_metadata_defaults(region_name=REGION)
    mock_client.get_instance_metadata_defaults.assert_called_once()


def test_get_instance_metadata_defaults_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_metadata_defaults.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_metadata_defaults",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get instance metadata defaults"):
        get_instance_metadata_defaults(region_name=REGION)


def test_get_instance_tpm_ek_pub(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_tpm_ek_pub.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_instance_tpm_ek_pub("test-instance_id", "test-key_type", "test-key_format", region_name=REGION)
    mock_client.get_instance_tpm_ek_pub.assert_called_once()


def test_get_instance_tpm_ek_pub_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_tpm_ek_pub.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_tpm_ek_pub",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get instance tpm ek pub"):
        get_instance_tpm_ek_pub("test-instance_id", "test-key_type", "test-key_format", region_name=REGION)


def test_get_instance_types_from_instance_requirements(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_types_from_instance_requirements.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_instance_types_from_instance_requirements([], [], {}, region_name=REGION)
    mock_client.get_instance_types_from_instance_requirements.assert_called_once()


def test_get_instance_types_from_instance_requirements_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_types_from_instance_requirements.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_types_from_instance_requirements",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get instance types from instance requirements"):
        get_instance_types_from_instance_requirements([], [], {}, region_name=REGION)


def test_get_instance_uefi_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_uefi_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_instance_uefi_data("test-instance_id", region_name=REGION)
    mock_client.get_instance_uefi_data.assert_called_once()


def test_get_instance_uefi_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_uefi_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_uefi_data",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get instance uefi data"):
        get_instance_uefi_data("test-instance_id", region_name=REGION)


def test_get_ipam_address_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_address_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_address_history("test-cidr", "test-ipam_scope_id", region_name=REGION)
    mock_client.get_ipam_address_history.assert_called_once()


def test_get_ipam_address_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_address_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_address_history",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam address history"):
        get_ipam_address_history("test-cidr", "test-ipam_scope_id", region_name=REGION)


def test_get_ipam_discovered_accounts(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_accounts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", region_name=REGION)
    mock_client.get_ipam_discovered_accounts.assert_called_once()


def test_get_ipam_discovered_accounts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_discovered_accounts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam discovered accounts"):
        get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", region_name=REGION)


def test_get_ipam_discovered_public_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_public_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", region_name=REGION)
    mock_client.get_ipam_discovered_public_addresses.assert_called_once()


def test_get_ipam_discovered_public_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_public_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_discovered_public_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam discovered public addresses"):
        get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", region_name=REGION)


def test_get_ipam_discovered_resource_cidrs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_resource_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", region_name=REGION)
    mock_client.get_ipam_discovered_resource_cidrs.assert_called_once()


def test_get_ipam_discovered_resource_cidrs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_resource_cidrs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_discovered_resource_cidrs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam discovered resource cidrs"):
        get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", region_name=REGION)


def test_get_ipam_pool_allocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_pool_allocations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_pool_allocations("test-ipam_pool_id", region_name=REGION)
    mock_client.get_ipam_pool_allocations.assert_called_once()


def test_get_ipam_pool_allocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_pool_allocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_pool_allocations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam pool allocations"):
        get_ipam_pool_allocations("test-ipam_pool_id", region_name=REGION)


def test_get_ipam_pool_cidrs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_pool_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_pool_cidrs("test-ipam_pool_id", region_name=REGION)
    mock_client.get_ipam_pool_cidrs.assert_called_once()


def test_get_ipam_pool_cidrs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_pool_cidrs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_pool_cidrs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam pool cidrs"):
        get_ipam_pool_cidrs("test-ipam_pool_id", region_name=REGION)


def test_get_ipam_prefix_list_resolver_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", region_name=REGION)
    mock_client.get_ipam_prefix_list_resolver_rules.assert_called_once()


def test_get_ipam_prefix_list_resolver_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_prefix_list_resolver_rules",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam prefix list resolver rules"):
        get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", region_name=REGION)


def test_get_ipam_prefix_list_resolver_version_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_version_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", 1, region_name=REGION)
    mock_client.get_ipam_prefix_list_resolver_version_entries.assert_called_once()


def test_get_ipam_prefix_list_resolver_version_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_version_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_prefix_list_resolver_version_entries",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam prefix list resolver version entries"):
        get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", 1, region_name=REGION)


def test_get_ipam_prefix_list_resolver_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", region_name=REGION)
    mock_client.get_ipam_prefix_list_resolver_versions.assert_called_once()


def test_get_ipam_prefix_list_resolver_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_prefix_list_resolver_versions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam prefix list resolver versions"):
        get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", region_name=REGION)


def test_get_ipam_resource_cidrs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_resource_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_resource_cidrs("test-ipam_scope_id", region_name=REGION)
    mock_client.get_ipam_resource_cidrs.assert_called_once()


def test_get_ipam_resource_cidrs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ipam_resource_cidrs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ipam_resource_cidrs",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ipam resource cidrs"):
        get_ipam_resource_cidrs("test-ipam_scope_id", region_name=REGION)


def test_get_launch_template_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_launch_template_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_launch_template_data("test-instance_id", region_name=REGION)
    mock_client.get_launch_template_data.assert_called_once()


def test_get_launch_template_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_launch_template_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_launch_template_data",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get launch template data"):
        get_launch_template_data("test-instance_id", region_name=REGION)


def test_get_managed_prefix_list_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_managed_prefix_list_associations("test-prefix_list_id", region_name=REGION)
    mock_client.get_managed_prefix_list_associations.assert_called_once()


def test_get_managed_prefix_list_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_managed_prefix_list_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get managed prefix list associations"):
        get_managed_prefix_list_associations("test-prefix_list_id", region_name=REGION)


def test_get_managed_prefix_list_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_managed_prefix_list_entries("test-prefix_list_id", region_name=REGION)
    mock_client.get_managed_prefix_list_entries.assert_called_once()


def test_get_managed_prefix_list_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_managed_prefix_list_entries",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get managed prefix list entries"):
        get_managed_prefix_list_entries("test-prefix_list_id", region_name=REGION)


def test_get_network_insights_access_scope_analysis_findings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_network_insights_access_scope_analysis_findings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", region_name=REGION)
    mock_client.get_network_insights_access_scope_analysis_findings.assert_called_once()


def test_get_network_insights_access_scope_analysis_findings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_network_insights_access_scope_analysis_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_network_insights_access_scope_analysis_findings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get network insights access scope analysis findings"):
        get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", region_name=REGION)


def test_get_network_insights_access_scope_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_network_insights_access_scope_content.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_network_insights_access_scope_content("test-network_insights_access_scope_id", region_name=REGION)
    mock_client.get_network_insights_access_scope_content.assert_called_once()


def test_get_network_insights_access_scope_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_network_insights_access_scope_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_network_insights_access_scope_content",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get network insights access scope content"):
        get_network_insights_access_scope_content("test-network_insights_access_scope_id", region_name=REGION)


def test_get_password_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_password_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_password_data("test-instance_id", region_name=REGION)
    mock_client.get_password_data.assert_called_once()


def test_get_password_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_password_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_password_data",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get password data"):
        get_password_data("test-instance_id", region_name=REGION)


def test_get_reserved_instances_exchange_quote(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_instances_exchange_quote.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_reserved_instances_exchange_quote([], region_name=REGION)
    mock_client.get_reserved_instances_exchange_quote.assert_called_once()


def test_get_reserved_instances_exchange_quote_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_instances_exchange_quote.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reserved_instances_exchange_quote",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reserved instances exchange quote"):
        get_reserved_instances_exchange_quote([], region_name=REGION)


def test_get_route_server_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_route_server_associations("test-route_server_id", region_name=REGION)
    mock_client.get_route_server_associations.assert_called_once()


def test_get_route_server_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_route_server_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get route server associations"):
        get_route_server_associations("test-route_server_id", region_name=REGION)


def test_get_route_server_propagations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_route_server_propagations("test-route_server_id", region_name=REGION)
    mock_client.get_route_server_propagations.assert_called_once()


def test_get_route_server_propagations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_propagations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_route_server_propagations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get route server propagations"):
        get_route_server_propagations("test-route_server_id", region_name=REGION)


def test_get_route_server_routing_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_routing_database.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_route_server_routing_database("test-route_server_id", region_name=REGION)
    mock_client.get_route_server_routing_database.assert_called_once()


def test_get_route_server_routing_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_route_server_routing_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_route_server_routing_database",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get route server routing database"):
        get_route_server_routing_database("test-route_server_id", region_name=REGION)


def test_get_security_groups_for_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_groups_for_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_security_groups_for_vpc("test-vpc_id", region_name=REGION)
    mock_client.get_security_groups_for_vpc.assert_called_once()


def test_get_security_groups_for_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_groups_for_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_security_groups_for_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get security groups for vpc"):
        get_security_groups_for_vpc("test-vpc_id", region_name=REGION)


def test_get_serial_console_access_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_serial_console_access_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_serial_console_access_status(region_name=REGION)
    mock_client.get_serial_console_access_status.assert_called_once()


def test_get_serial_console_access_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_serial_console_access_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_serial_console_access_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get serial console access status"):
        get_serial_console_access_status(region_name=REGION)


def test_get_snapshot_block_public_access_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_snapshot_block_public_access_state.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_snapshot_block_public_access_state(region_name=REGION)
    mock_client.get_snapshot_block_public_access_state.assert_called_once()


def test_get_snapshot_block_public_access_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_snapshot_block_public_access_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_snapshot_block_public_access_state",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get snapshot block public access state"):
        get_snapshot_block_public_access_state(region_name=REGION)


def test_get_spot_placement_scores(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_spot_placement_scores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_spot_placement_scores(1, region_name=REGION)
    mock_client.get_spot_placement_scores.assert_called_once()


def test_get_spot_placement_scores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_spot_placement_scores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_spot_placement_scores",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get spot placement scores"):
        get_spot_placement_scores(1, region_name=REGION)


def test_get_subnet_cidr_reservations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_subnet_cidr_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_subnet_cidr_reservations("test-subnet_id", region_name=REGION)
    mock_client.get_subnet_cidr_reservations.assert_called_once()


def test_get_subnet_cidr_reservations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_subnet_cidr_reservations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_subnet_cidr_reservations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get subnet cidr reservations"):
        get_subnet_cidr_reservations("test-subnet_id", region_name=REGION)


def test_get_transit_gateway_attachment_propagations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_attachment_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.get_transit_gateway_attachment_propagations.assert_called_once()


def test_get_transit_gateway_attachment_propagations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_attachment_propagations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_attachment_propagations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway attachment propagations"):
        get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", region_name=REGION)


def test_get_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", region_name=REGION)
    mock_client.get_transit_gateway_multicast_domain_associations.assert_called_once()


def test_get_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_multicast_domain_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_multicast_domain_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway multicast domain associations"):
        get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", region_name=REGION)


def test_get_transit_gateway_policy_table_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", region_name=REGION)
    mock_client.get_transit_gateway_policy_table_associations.assert_called_once()


def test_get_transit_gateway_policy_table_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_policy_table_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway policy table associations"):
        get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", region_name=REGION)


def test_get_transit_gateway_policy_table_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", region_name=REGION)
    mock_client.get_transit_gateway_policy_table_entries.assert_called_once()


def test_get_transit_gateway_policy_table_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_policy_table_entries",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway policy table entries"):
        get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", region_name=REGION)


def test_get_transit_gateway_prefix_list_references(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_prefix_list_references.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.get_transit_gateway_prefix_list_references.assert_called_once()


def test_get_transit_gateway_prefix_list_references_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_prefix_list_references.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_prefix_list_references",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway prefix list references"):
        get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", region_name=REGION)


def test_get_transit_gateway_route_table_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.get_transit_gateway_route_table_associations.assert_called_once()


def test_get_transit_gateway_route_table_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_route_table_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway route table associations"):
        get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", region_name=REGION)


def test_get_transit_gateway_route_table_propagations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.get_transit_gateway_route_table_propagations.assert_called_once()


def test_get_transit_gateway_route_table_propagations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_propagations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_transit_gateway_route_table_propagations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get transit gateway route table propagations"):
        get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", region_name=REGION)


def test_get_verified_access_endpoint_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_endpoint_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_verified_access_endpoint_policy("test-verified_access_endpoint_id", region_name=REGION)
    mock_client.get_verified_access_endpoint_policy.assert_called_once()


def test_get_verified_access_endpoint_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_endpoint_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_verified_access_endpoint_policy",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get verified access endpoint policy"):
        get_verified_access_endpoint_policy("test-verified_access_endpoint_id", region_name=REGION)


def test_get_verified_access_endpoint_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_endpoint_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_verified_access_endpoint_targets("test-verified_access_endpoint_id", region_name=REGION)
    mock_client.get_verified_access_endpoint_targets.assert_called_once()


def test_get_verified_access_endpoint_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_endpoint_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_verified_access_endpoint_targets",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get verified access endpoint targets"):
        get_verified_access_endpoint_targets("test-verified_access_endpoint_id", region_name=REGION)


def test_get_verified_access_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_verified_access_group_policy("test-verified_access_group_id", region_name=REGION)
    mock_client.get_verified_access_group_policy.assert_called_once()


def test_get_verified_access_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_verified_access_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_verified_access_group_policy",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get verified access group policy"):
        get_verified_access_group_policy("test-verified_access_group_id", region_name=REGION)


def test_get_vpn_connection_device_sample_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_sample_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", region_name=REGION)
    mock_client.get_vpn_connection_device_sample_configuration.assert_called_once()


def test_get_vpn_connection_device_sample_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_sample_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpn_connection_device_sample_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get vpn connection device sample configuration"):
        get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", region_name=REGION)


def test_get_vpn_connection_device_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_types.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_vpn_connection_device_types(region_name=REGION)
    mock_client.get_vpn_connection_device_types.assert_called_once()


def test_get_vpn_connection_device_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpn_connection_device_types",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get vpn connection device types"):
        get_vpn_connection_device_types(region_name=REGION)


def test_get_vpn_tunnel_replacement_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_tunnel_replacement_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_vpn_tunnel_replacement_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)
    mock_client.get_vpn_tunnel_replacement_status.assert_called_once()


def test_get_vpn_tunnel_replacement_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpn_tunnel_replacement_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpn_tunnel_replacement_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get vpn tunnel replacement status"):
        get_vpn_tunnel_replacement_status("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)


def test_import_client_vpn_client_certificate_revocation_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_client_vpn_client_certificate_revocation_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", "test-certificate_revocation_list", region_name=REGION)
    mock_client.import_client_vpn_client_certificate_revocation_list.assert_called_once()


def test_import_client_vpn_client_certificate_revocation_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_client_vpn_client_certificate_revocation_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_client_vpn_client_certificate_revocation_list",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import client vpn client certificate revocation list"):
        import_client_vpn_client_certificate_revocation_list("test-client_vpn_endpoint_id", "test-certificate_revocation_list", region_name=REGION)


def test_import_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_image(region_name=REGION)
    mock_client.import_image.assert_called_once()


def test_import_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import image"):
        import_image(region_name=REGION)


def test_import_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_instance("test-platform", region_name=REGION)
    mock_client.import_instance.assert_called_once()


def test_import_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import instance"):
        import_instance("test-platform", region_name=REGION)


def test_import_key_pair(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_key_pair("test-key_name", "test-public_key_material", region_name=REGION)
    mock_client.import_key_pair.assert_called_once()


def test_import_key_pair_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_key_pair",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import key pair"):
        import_key_pair("test-key_name", "test-public_key_material", region_name=REGION)


def test_import_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_snapshot(region_name=REGION)
    mock_client.import_snapshot.assert_called_once()


def test_import_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import snapshot"):
        import_snapshot(region_name=REGION)


def test_import_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_volume({}, {}, region_name=REGION)
    mock_client.import_volume.assert_called_once()


def test_import_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import volume"):
        import_volume({}, {}, region_name=REGION)


def test_list_images_in_recycle_bin(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_images_in_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    list_images_in_recycle_bin(region_name=REGION)
    mock_client.list_images_in_recycle_bin.assert_called_once()


def test_list_images_in_recycle_bin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_images_in_recycle_bin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_images_in_recycle_bin",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list images in recycle bin"):
        list_images_in_recycle_bin(region_name=REGION)


def test_list_snapshots_in_recycle_bin(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshots_in_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    list_snapshots_in_recycle_bin(region_name=REGION)
    mock_client.list_snapshots_in_recycle_bin.assert_called_once()


def test_list_snapshots_in_recycle_bin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshots_in_recycle_bin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_snapshots_in_recycle_bin",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list snapshots in recycle bin"):
        list_snapshots_in_recycle_bin(region_name=REGION)


def test_lock_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.lock_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    lock_snapshot("test-snapshot_id", "test-lock_mode", region_name=REGION)
    mock_client.lock_snapshot.assert_called_once()


def test_lock_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.lock_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "lock_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to lock snapshot"):
        lock_snapshot("test-snapshot_id", "test-lock_mode", region_name=REGION)


def test_modify_address_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_address_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_address_attribute("test-allocation_id", region_name=REGION)
    mock_client.modify_address_attribute.assert_called_once()


def test_modify_address_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_address_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_address_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify address attribute"):
        modify_address_attribute("test-allocation_id", region_name=REGION)


def test_modify_availability_zone_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_availability_zone_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_availability_zone_group("test-group_name", "test-opt_in_status", region_name=REGION)
    mock_client.modify_availability_zone_group.assert_called_once()


def test_modify_availability_zone_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_availability_zone_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_availability_zone_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify availability zone group"):
        modify_availability_zone_group("test-group_name", "test-opt_in_status", region_name=REGION)


def test_modify_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation("test-capacity_reservation_id", region_name=REGION)
    mock_client.modify_capacity_reservation.assert_called_once()


def test_modify_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_capacity_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify capacity reservation"):
        modify_capacity_reservation("test-capacity_reservation_id", region_name=REGION)


def test_modify_capacity_reservation_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", region_name=REGION)
    mock_client.modify_capacity_reservation_fleet.assert_called_once()


def test_modify_capacity_reservation_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_capacity_reservation_fleet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify capacity reservation fleet"):
        modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", region_name=REGION)


def test_modify_client_vpn_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_client_vpn_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_client_vpn_endpoint("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.modify_client_vpn_endpoint.assert_called_once()


def test_modify_client_vpn_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_client_vpn_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_client_vpn_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify client vpn endpoint"):
        modify_client_vpn_endpoint("test-client_vpn_endpoint_id", region_name=REGION)


def test_modify_default_credit_specification(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_default_credit_specification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_default_credit_specification("test-instance_family", "test-cpu_credits", region_name=REGION)
    mock_client.modify_default_credit_specification.assert_called_once()


def test_modify_default_credit_specification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_default_credit_specification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_default_credit_specification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify default credit specification"):
        modify_default_credit_specification("test-instance_family", "test-cpu_credits", region_name=REGION)


def test_modify_ebs_default_kms_key_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ebs_default_kms_key_id.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ebs_default_kms_key_id("test-kms_key_id", region_name=REGION)
    mock_client.modify_ebs_default_kms_key_id.assert_called_once()


def test_modify_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ebs_default_kms_key_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ebs_default_kms_key_id",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ebs default kms key id"):
        modify_ebs_default_kms_key_id("test-kms_key_id", region_name=REGION)


def test_modify_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_fleet("test-fleet_id", region_name=REGION)
    mock_client.modify_fleet.assert_called_once()


def test_modify_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_fleet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify fleet"):
        modify_fleet("test-fleet_id", region_name=REGION)


def test_modify_fpga_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_fpga_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_fpga_image_attribute("test-fpga_image_id", region_name=REGION)
    mock_client.modify_fpga_image_attribute.assert_called_once()


def test_modify_fpga_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_fpga_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_fpga_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify fpga image attribute"):
        modify_fpga_image_attribute("test-fpga_image_id", region_name=REGION)


def test_modify_hosts(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_hosts([], region_name=REGION)
    mock_client.modify_hosts.assert_called_once()


def test_modify_hosts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_hosts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_hosts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify hosts"):
        modify_hosts([], region_name=REGION)


def test_modify_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_id_format("test-resource", True, region_name=REGION)
    mock_client.modify_id_format.assert_called_once()


def test_modify_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify id format"):
        modify_id_format("test-resource", True, region_name=REGION)


def test_modify_identity_id_format(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_identity_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_identity_id_format("test-resource", True, "test-principal_arn", region_name=REGION)
    mock_client.modify_identity_id_format.assert_called_once()


def test_modify_identity_id_format_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_identity_id_format.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_identity_id_format",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify identity id format"):
        modify_identity_id_format("test-resource", True, "test-principal_arn", region_name=REGION)


def test_modify_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_image_attribute("test-image_id", region_name=REGION)
    mock_client.modify_image_attribute.assert_called_once()


def test_modify_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify image attribute"):
        modify_image_attribute("test-image_id", region_name=REGION)


def test_modify_instance_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_attribute("test-instance_id", region_name=REGION)
    mock_client.modify_instance_attribute.assert_called_once()


def test_modify_instance_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance attribute"):
        modify_instance_attribute("test-instance_id", region_name=REGION)


def test_modify_instance_capacity_reservation_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_capacity_reservation_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_capacity_reservation_attributes("test-instance_id", {}, region_name=REGION)
    mock_client.modify_instance_capacity_reservation_attributes.assert_called_once()


def test_modify_instance_capacity_reservation_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_capacity_reservation_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_capacity_reservation_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance capacity reservation attributes"):
        modify_instance_capacity_reservation_attributes("test-instance_id", {}, region_name=REGION)


def test_modify_instance_connect_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_connect_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_connect_endpoint("test-instance_connect_endpoint_id", region_name=REGION)
    mock_client.modify_instance_connect_endpoint.assert_called_once()


def test_modify_instance_connect_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_connect_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_connect_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance connect endpoint"):
        modify_instance_connect_endpoint("test-instance_connect_endpoint_id", region_name=REGION)


def test_modify_instance_cpu_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_cpu_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_cpu_options("test-instance_id", 1, 1, region_name=REGION)
    mock_client.modify_instance_cpu_options.assert_called_once()


def test_modify_instance_cpu_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_cpu_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_cpu_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance cpu options"):
        modify_instance_cpu_options("test-instance_id", 1, 1, region_name=REGION)


def test_modify_instance_credit_specification(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_credit_specification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_credit_specification([], region_name=REGION)
    mock_client.modify_instance_credit_specification.assert_called_once()


def test_modify_instance_credit_specification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_credit_specification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_credit_specification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance credit specification"):
        modify_instance_credit_specification([], region_name=REGION)


def test_modify_instance_event_start_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_event_start_time.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_event_start_time("test-instance_id", "test-instance_event_id", "test-not_before", region_name=REGION)
    mock_client.modify_instance_event_start_time.assert_called_once()


def test_modify_instance_event_start_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_event_start_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_event_start_time",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance event start time"):
        modify_instance_event_start_time("test-instance_id", "test-instance_event_id", "test-not_before", region_name=REGION)


def test_modify_instance_event_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_event_window("test-instance_event_window_id", region_name=REGION)
    mock_client.modify_instance_event_window.assert_called_once()


def test_modify_instance_event_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_event_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_event_window",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance event window"):
        modify_instance_event_window("test-instance_event_window_id", region_name=REGION)


def test_modify_instance_maintenance_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_maintenance_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_maintenance_options("test-instance_id", region_name=REGION)
    mock_client.modify_instance_maintenance_options.assert_called_once()


def test_modify_instance_maintenance_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_maintenance_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_maintenance_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance maintenance options"):
        modify_instance_maintenance_options("test-instance_id", region_name=REGION)


def test_modify_instance_metadata_defaults(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_defaults.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_metadata_defaults(region_name=REGION)
    mock_client.modify_instance_metadata_defaults.assert_called_once()


def test_modify_instance_metadata_defaults_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_defaults.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_metadata_defaults",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance metadata defaults"):
        modify_instance_metadata_defaults(region_name=REGION)


def test_modify_instance_metadata_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_metadata_options("test-instance_id", region_name=REGION)
    mock_client.modify_instance_metadata_options.assert_called_once()


def test_modify_instance_metadata_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_metadata_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance metadata options"):
        modify_instance_metadata_options("test-instance_id", region_name=REGION)


def test_modify_instance_network_performance_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_network_performance_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_network_performance_options("test-instance_id", "test-bandwidth_weighting", region_name=REGION)
    mock_client.modify_instance_network_performance_options.assert_called_once()


def test_modify_instance_network_performance_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_network_performance_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_network_performance_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance network performance options"):
        modify_instance_network_performance_options("test-instance_id", "test-bandwidth_weighting", region_name=REGION)


def test_modify_instance_placement(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_placement.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_placement("test-instance_id", region_name=REGION)
    mock_client.modify_instance_placement.assert_called_once()


def test_modify_instance_placement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_instance_placement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_instance_placement",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify instance placement"):
        modify_instance_placement("test-instance_id", region_name=REGION)


def test_modify_ipam(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam("test-ipam_id", region_name=REGION)
    mock_client.modify_ipam.assert_called_once()


def test_modify_ipam_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam"):
        modify_ipam("test-ipam_id", region_name=REGION)


def test_modify_ipam_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_pool("test-ipam_pool_id", region_name=REGION)
    mock_client.modify_ipam_pool.assert_called_once()


def test_modify_ipam_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_pool",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam pool"):
        modify_ipam_pool("test-ipam_pool_id", region_name=REGION)


def test_modify_ipam_prefix_list_resolver(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", region_name=REGION)
    mock_client.modify_ipam_prefix_list_resolver.assert_called_once()


def test_modify_ipam_prefix_list_resolver_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_prefix_list_resolver",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam prefix list resolver"):
        modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", region_name=REGION)


def test_modify_ipam_prefix_list_resolver_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", region_name=REGION)
    mock_client.modify_ipam_prefix_list_resolver_target.assert_called_once()


def test_modify_ipam_prefix_list_resolver_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_prefix_list_resolver_target",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam prefix list resolver target"):
        modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", region_name=REGION)


def test_modify_ipam_resource_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", True, region_name=REGION)
    mock_client.modify_ipam_resource_cidr.assert_called_once()


def test_modify_ipam_resource_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_resource_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam resource cidr"):
        modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", True, region_name=REGION)


def test_modify_ipam_resource_discovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_resource_discovery("test-ipam_resource_discovery_id", region_name=REGION)
    mock_client.modify_ipam_resource_discovery.assert_called_once()


def test_modify_ipam_resource_discovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_discovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_resource_discovery",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam resource discovery"):
        modify_ipam_resource_discovery("test-ipam_resource_discovery_id", region_name=REGION)


def test_modify_ipam_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_scope("test-ipam_scope_id", region_name=REGION)
    mock_client.modify_ipam_scope.assert_called_once()


def test_modify_ipam_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_ipam_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_ipam_scope",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify ipam scope"):
        modify_ipam_scope("test-ipam_scope_id", region_name=REGION)


def test_modify_launch_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_launch_template(region_name=REGION)
    mock_client.modify_launch_template.assert_called_once()


def test_modify_launch_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_launch_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_launch_template",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify launch template"):
        modify_launch_template(region_name=REGION)


def test_modify_local_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.modify_local_gateway_route.assert_called_once()


def test_modify_local_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_local_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_local_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify local gateway route"):
        modify_local_gateway_route("test-local_gateway_route_table_id", region_name=REGION)


def test_modify_managed_prefix_list(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_managed_prefix_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_managed_prefix_list("test-prefix_list_id", region_name=REGION)
    mock_client.modify_managed_prefix_list.assert_called_once()


def test_modify_managed_prefix_list_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_managed_prefix_list.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_managed_prefix_list",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify managed prefix list"):
        modify_managed_prefix_list("test-prefix_list_id", region_name=REGION)


def test_modify_network_interface_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_network_interface_attribute("test-network_interface_id", region_name=REGION)
    mock_client.modify_network_interface_attribute.assert_called_once()


def test_modify_network_interface_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_network_interface_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_network_interface_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify network interface attribute"):
        modify_network_interface_attribute("test-network_interface_id", region_name=REGION)


def test_modify_private_dns_name_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_private_dns_name_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_private_dns_name_options("test-instance_id", region_name=REGION)
    mock_client.modify_private_dns_name_options.assert_called_once()


def test_modify_private_dns_name_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_private_dns_name_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_private_dns_name_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify private dns name options"):
        modify_private_dns_name_options("test-instance_id", region_name=REGION)


def test_modify_public_ip_dns_name_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_public_ip_dns_name_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_public_ip_dns_name_options("test-network_interface_id", "test-hostname_type", region_name=REGION)
    mock_client.modify_public_ip_dns_name_options.assert_called_once()


def test_modify_public_ip_dns_name_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_public_ip_dns_name_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_public_ip_dns_name_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify public ip dns name options"):
        modify_public_ip_dns_name_options("test-network_interface_id", "test-hostname_type", region_name=REGION)


def test_modify_reserved_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_reserved_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_reserved_instances([], [], region_name=REGION)
    mock_client.modify_reserved_instances.assert_called_once()


def test_modify_reserved_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_reserved_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_reserved_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify reserved instances"):
        modify_reserved_instances([], [], region_name=REGION)


def test_modify_route_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_route_server("test-route_server_id", region_name=REGION)
    mock_client.modify_route_server.assert_called_once()


def test_modify_route_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_route_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_route_server",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify route server"):
        modify_route_server("test-route_server_id", region_name=REGION)


def test_modify_security_group_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_security_group_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_security_group_rules("test-group_id", [], region_name=REGION)
    mock_client.modify_security_group_rules.assert_called_once()


def test_modify_security_group_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_security_group_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_security_group_rules",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify security group rules"):
        modify_security_group_rules("test-group_id", [], region_name=REGION)


def test_modify_snapshot_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_attribute("test-snapshot_id", region_name=REGION)
    mock_client.modify_snapshot_attribute.assert_called_once()


def test_modify_snapshot_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_snapshot_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify snapshot attribute"):
        modify_snapshot_attribute("test-snapshot_id", region_name=REGION)


def test_modify_snapshot_tier(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_tier.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_tier("test-snapshot_id", region_name=REGION)
    mock_client.modify_snapshot_tier.assert_called_once()


def test_modify_snapshot_tier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_tier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_snapshot_tier",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify snapshot tier"):
        modify_snapshot_tier("test-snapshot_id", region_name=REGION)


def test_modify_spot_fleet_request(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_spot_fleet_request.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_spot_fleet_request("test-spot_fleet_request_id", region_name=REGION)
    mock_client.modify_spot_fleet_request.assert_called_once()


def test_modify_spot_fleet_request_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_spot_fleet_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_spot_fleet_request",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify spot fleet request"):
        modify_spot_fleet_request("test-spot_fleet_request_id", region_name=REGION)


def test_modify_subnet_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_subnet_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_subnet_attribute("test-subnet_id", region_name=REGION)
    mock_client.modify_subnet_attribute.assert_called_once()


def test_modify_subnet_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_subnet_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_subnet_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify subnet attribute"):
        modify_subnet_attribute("test-subnet_id", region_name=REGION)


def test_modify_traffic_mirror_filter_network_services(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_network_services.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", region_name=REGION)
    mock_client.modify_traffic_mirror_filter_network_services.assert_called_once()


def test_modify_traffic_mirror_filter_network_services_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_network_services.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_traffic_mirror_filter_network_services",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify traffic mirror filter network services"):
        modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", region_name=REGION)


def test_modify_traffic_mirror_filter_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_rule.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", region_name=REGION)
    mock_client.modify_traffic_mirror_filter_rule.assert_called_once()


def test_modify_traffic_mirror_filter_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_traffic_mirror_filter_rule",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify traffic mirror filter rule"):
        modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", region_name=REGION)


def test_modify_traffic_mirror_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_session.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_session("test-traffic_mirror_session_id", region_name=REGION)
    mock_client.modify_traffic_mirror_session.assert_called_once()


def test_modify_traffic_mirror_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_traffic_mirror_session",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify traffic mirror session"):
        modify_traffic_mirror_session("test-traffic_mirror_session_id", region_name=REGION)


def test_modify_transit_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway("test-transit_gateway_id", region_name=REGION)
    mock_client.modify_transit_gateway.assert_called_once()


def test_modify_transit_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_transit_gateway",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify transit gateway"):
        modify_transit_gateway("test-transit_gateway_id", region_name=REGION)


def test_modify_transit_gateway_prefix_list_reference(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_prefix_list_reference.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)
    mock_client.modify_transit_gateway_prefix_list_reference.assert_called_once()


def test_modify_transit_gateway_prefix_list_reference_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_prefix_list_reference.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_transit_gateway_prefix_list_reference",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify transit gateway prefix list reference"):
        modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", region_name=REGION)


def test_modify_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.modify_transit_gateway_vpc_attachment.assert_called_once()


def test_modify_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_vpc_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_transit_gateway_vpc_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify transit gateway vpc attachment"):
        modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_modify_verified_access_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_endpoint("test-verified_access_endpoint_id", region_name=REGION)
    mock_client.modify_verified_access_endpoint.assert_called_once()


def test_modify_verified_access_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access endpoint"):
        modify_verified_access_endpoint("test-verified_access_endpoint_id", region_name=REGION)


def test_modify_verified_access_endpoint_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", region_name=REGION)
    mock_client.modify_verified_access_endpoint_policy.assert_called_once()


def test_modify_verified_access_endpoint_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_endpoint_policy",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access endpoint policy"):
        modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", region_name=REGION)


def test_modify_verified_access_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_group("test-verified_access_group_id", region_name=REGION)
    mock_client.modify_verified_access_group.assert_called_once()


def test_modify_verified_access_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_group",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access group"):
        modify_verified_access_group("test-verified_access_group_id", region_name=REGION)


def test_modify_verified_access_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_group_policy("test-verified_access_group_id", region_name=REGION)
    mock_client.modify_verified_access_group_policy.assert_called_once()


def test_modify_verified_access_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_group_policy",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access group policy"):
        modify_verified_access_group_policy("test-verified_access_group_id", region_name=REGION)


def test_modify_verified_access_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_instance("test-verified_access_instance_id", region_name=REGION)
    mock_client.modify_verified_access_instance.assert_called_once()


def test_modify_verified_access_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_instance",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access instance"):
        modify_verified_access_instance("test-verified_access_instance_id", region_name=REGION)


def test_modify_verified_access_instance_logging_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance_logging_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", {}, region_name=REGION)
    mock_client.modify_verified_access_instance_logging_configuration.assert_called_once()


def test_modify_verified_access_instance_logging_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance_logging_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_instance_logging_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access instance logging configuration"):
        modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", {}, region_name=REGION)


def test_modify_verified_access_trust_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_trust_provider("test-verified_access_trust_provider_id", region_name=REGION)
    mock_client.modify_verified_access_trust_provider.assert_called_once()


def test_modify_verified_access_trust_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_verified_access_trust_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_verified_access_trust_provider",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify verified access trust provider"):
        modify_verified_access_trust_provider("test-verified_access_trust_provider_id", region_name=REGION)


def test_modify_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_volume("test-volume_id", region_name=REGION)
    mock_client.modify_volume.assert_called_once()


def test_modify_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_volume",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify volume"):
        modify_volume("test-volume_id", region_name=REGION)


def test_modify_volume_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_volume_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_volume_attribute("test-volume_id", region_name=REGION)
    mock_client.modify_volume_attribute.assert_called_once()


def test_modify_volume_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_volume_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_volume_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify volume attribute"):
        modify_volume_attribute("test-volume_id", region_name=REGION)


def test_modify_vpc_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_attribute("test-vpc_id", region_name=REGION)
    mock_client.modify_vpc_attribute.assert_called_once()


def test_modify_vpc_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc attribute"):
        modify_vpc_attribute("test-vpc_id", region_name=REGION)


def test_modify_vpc_block_public_access_exclusion(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_block_public_access_exclusion.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_block_public_access_exclusion("test-exclusion_id", "test-internet_gateway_exclusion_mode", region_name=REGION)
    mock_client.modify_vpc_block_public_access_exclusion.assert_called_once()


def test_modify_vpc_block_public_access_exclusion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_block_public_access_exclusion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_block_public_access_exclusion",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc block public access exclusion"):
        modify_vpc_block_public_access_exclusion("test-exclusion_id", "test-internet_gateway_exclusion_mode", region_name=REGION)


def test_modify_vpc_block_public_access_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_block_public_access_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_block_public_access_options("test-internet_gateway_block_mode", region_name=REGION)
    mock_client.modify_vpc_block_public_access_options.assert_called_once()


def test_modify_vpc_block_public_access_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_block_public_access_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_block_public_access_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc block public access options"):
        modify_vpc_block_public_access_options("test-internet_gateway_block_mode", region_name=REGION)


def test_modify_vpc_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint("test-vpc_endpoint_id", region_name=REGION)
    mock_client.modify_vpc_endpoint.assert_called_once()


def test_modify_vpc_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_endpoint",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc endpoint"):
        modify_vpc_endpoint("test-vpc_endpoint_id", region_name=REGION)


def test_modify_vpc_endpoint_connection_notification(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_connection_notification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_connection_notification("test-connection_notification_id", region_name=REGION)
    mock_client.modify_vpc_endpoint_connection_notification.assert_called_once()


def test_modify_vpc_endpoint_connection_notification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_connection_notification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_endpoint_connection_notification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc endpoint connection notification"):
        modify_vpc_endpoint_connection_notification("test-connection_notification_id", region_name=REGION)


def test_modify_vpc_endpoint_service_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_service_configuration("test-service_id", region_name=REGION)
    mock_client.modify_vpc_endpoint_service_configuration.assert_called_once()


def test_modify_vpc_endpoint_service_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_endpoint_service_configuration",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc endpoint service configuration"):
        modify_vpc_endpoint_service_configuration("test-service_id", region_name=REGION)


def test_modify_vpc_endpoint_service_payer_responsibility(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_payer_responsibility.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_service_payer_responsibility("test-service_id", "test-payer_responsibility", region_name=REGION)
    mock_client.modify_vpc_endpoint_service_payer_responsibility.assert_called_once()


def test_modify_vpc_endpoint_service_payer_responsibility_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_payer_responsibility.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_endpoint_service_payer_responsibility",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc endpoint service payer responsibility"):
        modify_vpc_endpoint_service_payer_responsibility("test-service_id", "test-payer_responsibility", region_name=REGION)


def test_modify_vpc_endpoint_service_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_service_permissions("test-service_id", region_name=REGION)
    mock_client.modify_vpc_endpoint_service_permissions.assert_called_once()


def test_modify_vpc_endpoint_service_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_endpoint_service_permissions",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc endpoint service permissions"):
        modify_vpc_endpoint_service_permissions("test-service_id", region_name=REGION)


def test_modify_vpc_peering_connection_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_peering_connection_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_peering_connection_options("test-vpc_peering_connection_id", region_name=REGION)
    mock_client.modify_vpc_peering_connection_options.assert_called_once()


def test_modify_vpc_peering_connection_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_peering_connection_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_peering_connection_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc peering connection options"):
        modify_vpc_peering_connection_options("test-vpc_peering_connection_id", region_name=REGION)


def test_modify_vpc_tenancy(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_tenancy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_tenancy("test-vpc_id", "test-instance_tenancy", region_name=REGION)
    mock_client.modify_vpc_tenancy.assert_called_once()


def test_modify_vpc_tenancy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpc_tenancy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpc_tenancy",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpc tenancy"):
        modify_vpc_tenancy("test-vpc_id", "test-instance_tenancy", region_name=REGION)


def test_modify_vpn_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_connection("test-vpn_connection_id", region_name=REGION)
    mock_client.modify_vpn_connection.assert_called_once()


def test_modify_vpn_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpn_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpn connection"):
        modify_vpn_connection("test-vpn_connection_id", region_name=REGION)


def test_modify_vpn_connection_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_connection_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_connection_options("test-vpn_connection_id", region_name=REGION)
    mock_client.modify_vpn_connection_options.assert_called_once()


def test_modify_vpn_connection_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_connection_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpn_connection_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpn connection options"):
        modify_vpn_connection_options("test-vpn_connection_id", region_name=REGION)


def test_modify_vpn_tunnel_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_tunnel_certificate.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_tunnel_certificate("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)
    mock_client.modify_vpn_tunnel_certificate.assert_called_once()


def test_modify_vpn_tunnel_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_tunnel_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpn_tunnel_certificate",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpn tunnel certificate"):
        modify_vpn_tunnel_certificate("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)


def test_modify_vpn_tunnel_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_tunnel_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, region_name=REGION)
    mock_client.modify_vpn_tunnel_options.assert_called_once()


def test_modify_vpn_tunnel_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_vpn_tunnel_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_vpn_tunnel_options",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify vpn tunnel options"):
        modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, region_name=REGION)


def test_monitor_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.monitor_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    monitor_instances([], region_name=REGION)
    mock_client.monitor_instances.assert_called_once()


def test_monitor_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.monitor_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "monitor_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to monitor instances"):
        monitor_instances([], region_name=REGION)


def test_move_address_to_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_address_to_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    move_address_to_vpc("test-public_ip", region_name=REGION)
    mock_client.move_address_to_vpc.assert_called_once()


def test_move_address_to_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_address_to_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "move_address_to_vpc",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to move address to vpc"):
        move_address_to_vpc("test-public_ip", region_name=REGION)


def test_move_byoip_cidr_to_ipam(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_byoip_cidr_to_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    move_byoip_cidr_to_ipam("test-cidr", "test-ipam_pool_id", "test-ipam_pool_owner", region_name=REGION)
    mock_client.move_byoip_cidr_to_ipam.assert_called_once()


def test_move_byoip_cidr_to_ipam_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_byoip_cidr_to_ipam.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "move_byoip_cidr_to_ipam",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to move byoip cidr to ipam"):
        move_byoip_cidr_to_ipam("test-cidr", "test-ipam_pool_id", "test-ipam_pool_owner", region_name=REGION)


def test_move_capacity_reservation_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_capacity_reservation_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, region_name=REGION)
    mock_client.move_capacity_reservation_instances.assert_called_once()


def test_move_capacity_reservation_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.move_capacity_reservation_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "move_capacity_reservation_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to move capacity reservation instances"):
        move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, region_name=REGION)


def test_provision_byoip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_byoip_cidr("test-cidr", region_name=REGION)
    mock_client.provision_byoip_cidr.assert_called_once()


def test_provision_byoip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_byoip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "provision_byoip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to provision byoip cidr"):
        provision_byoip_cidr("test-cidr", region_name=REGION)


def test_provision_ipam_byoasn(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_ipam_byoasn("test-ipam_id", "test-asn", {}, region_name=REGION)
    mock_client.provision_ipam_byoasn.assert_called_once()


def test_provision_ipam_byoasn_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_ipam_byoasn.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "provision_ipam_byoasn",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to provision ipam byoasn"):
        provision_ipam_byoasn("test-ipam_id", "test-asn", {}, region_name=REGION)


def test_provision_ipam_pool_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)
    mock_client.provision_ipam_pool_cidr.assert_called_once()


def test_provision_ipam_pool_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_ipam_pool_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "provision_ipam_pool_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to provision ipam pool cidr"):
        provision_ipam_pool_cidr("test-ipam_pool_id", region_name=REGION)


def test_provision_public_ipv4_pool_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_public_ipv4_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", 1, region_name=REGION)
    mock_client.provision_public_ipv4_pool_cidr.assert_called_once()


def test_provision_public_ipv4_pool_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.provision_public_ipv4_pool_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "provision_public_ipv4_pool_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to provision public ipv4 pool cidr"):
        provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", 1, region_name=REGION)


def test_purchase_capacity_block(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_capacity_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", region_name=REGION)
    mock_client.purchase_capacity_block.assert_called_once()


def test_purchase_capacity_block_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_capacity_block.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_capacity_block",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase capacity block"):
        purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", region_name=REGION)


def test_purchase_capacity_block_extension(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_capacity_block_extension.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_capacity_block_extension("test-capacity_block_extension_offering_id", "test-capacity_reservation_id", region_name=REGION)
    mock_client.purchase_capacity_block_extension.assert_called_once()


def test_purchase_capacity_block_extension_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_capacity_block_extension.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_capacity_block_extension",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase capacity block extension"):
        purchase_capacity_block_extension("test-capacity_block_extension_offering_id", "test-capacity_reservation_id", region_name=REGION)


def test_purchase_host_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_host_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_host_reservation([], "test-offering_id", region_name=REGION)
    mock_client.purchase_host_reservation.assert_called_once()


def test_purchase_host_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_host_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_host_reservation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase host reservation"):
        purchase_host_reservation([], "test-offering_id", region_name=REGION)


def test_purchase_reserved_instances_offering(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_instances_offering.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", region_name=REGION)
    mock_client.purchase_reserved_instances_offering.assert_called_once()


def test_purchase_reserved_instances_offering_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_instances_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_reserved_instances_offering",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase reserved instances offering"):
        purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", region_name=REGION)


def test_purchase_scheduled_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_scheduled_instances([], region_name=REGION)
    mock_client.purchase_scheduled_instances.assert_called_once()


def test_purchase_scheduled_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_scheduled_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_scheduled_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase scheduled instances"):
        purchase_scheduled_instances([], region_name=REGION)


def test_register_image(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_image("test-name", region_name=REGION)
    mock_client.register_image.assert_called_once()


def test_register_image_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_image",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register image"):
        register_image("test-name", region_name=REGION)


def test_register_instance_event_notification_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_instance_event_notification_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_instance_event_notification_attributes({}, region_name=REGION)
    mock_client.register_instance_event_notification_attributes.assert_called_once()


def test_register_instance_event_notification_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_instance_event_notification_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_instance_event_notification_attributes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register instance event notification attributes"):
        register_instance_event_notification_attributes({}, region_name=REGION)


def test_register_transit_gateway_multicast_group_members(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_members.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", [], region_name=REGION)
    mock_client.register_transit_gateway_multicast_group_members.assert_called_once()


def test_register_transit_gateway_multicast_group_members_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_members.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_transit_gateway_multicast_group_members",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register transit gateway multicast group members"):
        register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", [], region_name=REGION)


def test_register_transit_gateway_multicast_group_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_sources.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", [], region_name=REGION)
    mock_client.register_transit_gateway_multicast_group_sources.assert_called_once()


def test_register_transit_gateway_multicast_group_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_transit_gateway_multicast_group_sources",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register transit gateway multicast group sources"):
        register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", [], region_name=REGION)


def test_reject_capacity_reservation_billing_ownership(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_capacity_reservation_billing_ownership.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_capacity_reservation_billing_ownership("test-capacity_reservation_id", region_name=REGION)
    mock_client.reject_capacity_reservation_billing_ownership.assert_called_once()


def test_reject_capacity_reservation_billing_ownership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_capacity_reservation_billing_ownership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_capacity_reservation_billing_ownership",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject capacity reservation billing ownership"):
        reject_capacity_reservation_billing_ownership("test-capacity_reservation_id", region_name=REGION)


def test_reject_transit_gateway_multicast_domain_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_transit_gateway_multicast_domain_associations(region_name=REGION)
    mock_client.reject_transit_gateway_multicast_domain_associations.assert_called_once()


def test_reject_transit_gateway_multicast_domain_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_multicast_domain_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_transit_gateway_multicast_domain_associations",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject transit gateway multicast domain associations"):
        reject_transit_gateway_multicast_domain_associations(region_name=REGION)


def test_reject_transit_gateway_peering_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_peering_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.reject_transit_gateway_peering_attachment.assert_called_once()


def test_reject_transit_gateway_peering_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_peering_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_transit_gateway_peering_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject transit gateway peering attachment"):
        reject_transit_gateway_peering_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_reject_transit_gateway_vpc_attachment(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)
    mock_client.reject_transit_gateway_vpc_attachment.assert_called_once()


def test_reject_transit_gateway_vpc_attachment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_vpc_attachment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_transit_gateway_vpc_attachment",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject transit gateway vpc attachment"):
        reject_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", region_name=REGION)


def test_reject_vpc_endpoint_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_vpc_endpoint_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_vpc_endpoint_connections("test-service_id", [], region_name=REGION)
    mock_client.reject_vpc_endpoint_connections.assert_called_once()


def test_reject_vpc_endpoint_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_vpc_endpoint_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_vpc_endpoint_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject vpc endpoint connections"):
        reject_vpc_endpoint_connections("test-service_id", [], region_name=REGION)


def test_reject_vpc_peering_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_vpc_peering_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)
    mock_client.reject_vpc_peering_connection.assert_called_once()


def test_reject_vpc_peering_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_vpc_peering_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_vpc_peering_connection",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject vpc peering connection"):
        reject_vpc_peering_connection("test-vpc_peering_connection_id", region_name=REGION)


def test_release_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    release_address(region_name=REGION)
    mock_client.release_address.assert_called_once()


def test_release_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "release_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to release address"):
        release_address(region_name=REGION)


def test_release_hosts(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    release_hosts([], region_name=REGION)
    mock_client.release_hosts.assert_called_once()


def test_release_hosts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_hosts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "release_hosts",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to release hosts"):
        release_hosts([], region_name=REGION)


def test_release_ipam_pool_allocation(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_ipam_pool_allocation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    release_ipam_pool_allocation("test-ipam_pool_id", "test-cidr", "test-ipam_pool_allocation_id", region_name=REGION)
    mock_client.release_ipam_pool_allocation.assert_called_once()


def test_release_ipam_pool_allocation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_ipam_pool_allocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "release_ipam_pool_allocation",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to release ipam pool allocation"):
        release_ipam_pool_allocation("test-ipam_pool_id", "test-cidr", "test-ipam_pool_allocation_id", region_name=REGION)


def test_replace_iam_instance_profile_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_iam_instance_profile_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_iam_instance_profile_association({}, "test-association_id", region_name=REGION)
    mock_client.replace_iam_instance_profile_association.assert_called_once()


def test_replace_iam_instance_profile_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_iam_instance_profile_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_iam_instance_profile_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace iam instance profile association"):
        replace_iam_instance_profile_association({}, "test-association_id", region_name=REGION)


def test_replace_image_criteria_in_allowed_images_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_image_criteria_in_allowed_images_settings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_image_criteria_in_allowed_images_settings(region_name=REGION)
    mock_client.replace_image_criteria_in_allowed_images_settings.assert_called_once()


def test_replace_image_criteria_in_allowed_images_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_image_criteria_in_allowed_images_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_image_criteria_in_allowed_images_settings",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace image criteria in allowed images settings"):
        replace_image_criteria_in_allowed_images_settings(region_name=REGION)


def test_replace_network_acl_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_network_acl_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_network_acl_association("test-association_id", "test-network_acl_id", region_name=REGION)
    mock_client.replace_network_acl_association.assert_called_once()


def test_replace_network_acl_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_network_acl_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_network_acl_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace network acl association"):
        replace_network_acl_association("test-association_id", "test-network_acl_id", region_name=REGION)


def test_replace_network_acl_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_network_acl_entry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, region_name=REGION)
    mock_client.replace_network_acl_entry.assert_called_once()


def test_replace_network_acl_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_network_acl_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_network_acl_entry",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace network acl entry"):
        replace_network_acl_entry("test-network_acl_id", 1, "test-protocol", "test-rule_action", True, region_name=REGION)


def test_replace_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_route("test-route_table_id", region_name=REGION)
    mock_client.replace_route.assert_called_once()


def test_replace_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace route"):
        replace_route("test-route_table_id", region_name=REGION)


def test_replace_route_table_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_route_table_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_route_table_association("test-association_id", "test-route_table_id", region_name=REGION)
    mock_client.replace_route_table_association.assert_called_once()


def test_replace_route_table_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_route_table_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_route_table_association",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace route table association"):
        replace_route_table_association("test-association_id", "test-route_table_id", region_name=REGION)


def test_replace_transit_gateway_route(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_transit_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", region_name=REGION)
    mock_client.replace_transit_gateway_route.assert_called_once()


def test_replace_transit_gateway_route_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_transit_gateway_route.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_transit_gateway_route",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace transit gateway route"):
        replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", region_name=REGION)


def test_replace_vpn_tunnel(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_vpn_tunnel.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)
    mock_client.replace_vpn_tunnel.assert_called_once()


def test_replace_vpn_tunnel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replace_vpn_tunnel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_vpn_tunnel",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replace vpn tunnel"):
        replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", region_name=REGION)


def test_report_instance_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.report_instance_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    report_instance_status([], "test-status", [], region_name=REGION)
    mock_client.report_instance_status.assert_called_once()


def test_report_instance_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.report_instance_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "report_instance_status",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to report instance status"):
        report_instance_status([], "test-status", [], region_name=REGION)


def test_request_spot_fleet(monkeypatch):
    mock_client = MagicMock()
    mock_client.request_spot_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    request_spot_fleet({}, region_name=REGION)
    mock_client.request_spot_fleet.assert_called_once()


def test_request_spot_fleet_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.request_spot_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "request_spot_fleet",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to request spot fleet"):
        request_spot_fleet({}, region_name=REGION)


def test_request_spot_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.request_spot_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    request_spot_instances(region_name=REGION)
    mock_client.request_spot_instances.assert_called_once()


def test_request_spot_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.request_spot_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "request_spot_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to request spot instances"):
        request_spot_instances(region_name=REGION)


def test_reset_address_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_address_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_address_attribute("test-allocation_id", "test-attribute", region_name=REGION)
    mock_client.reset_address_attribute.assert_called_once()


def test_reset_address_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_address_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_address_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset address attribute"):
        reset_address_attribute("test-allocation_id", "test-attribute", region_name=REGION)


def test_reset_ebs_default_kms_key_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_ebs_default_kms_key_id.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_ebs_default_kms_key_id(region_name=REGION)
    mock_client.reset_ebs_default_kms_key_id.assert_called_once()


def test_reset_ebs_default_kms_key_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_ebs_default_kms_key_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_ebs_default_kms_key_id",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset ebs default kms key id"):
        reset_ebs_default_kms_key_id(region_name=REGION)


def test_reset_fpga_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_fpga_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_fpga_image_attribute("test-fpga_image_id", region_name=REGION)
    mock_client.reset_fpga_image_attribute.assert_called_once()


def test_reset_fpga_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_fpga_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_fpga_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset fpga image attribute"):
        reset_fpga_image_attribute("test-fpga_image_id", region_name=REGION)


def test_reset_image_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_image_attribute("test-attribute", "test-image_id", region_name=REGION)
    mock_client.reset_image_attribute.assert_called_once()


def test_reset_image_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_image_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_image_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset image attribute"):
        reset_image_attribute("test-attribute", "test-image_id", region_name=REGION)


def test_reset_instance_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_instance_attribute("test-instance_id", "test-attribute", region_name=REGION)
    mock_client.reset_instance_attribute.assert_called_once()


def test_reset_instance_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_instance_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_instance_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset instance attribute"):
        reset_instance_attribute("test-instance_id", "test-attribute", region_name=REGION)


def test_reset_network_interface_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_network_interface_attribute("test-network_interface_id", region_name=REGION)
    mock_client.reset_network_interface_attribute.assert_called_once()


def test_reset_network_interface_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_network_interface_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_network_interface_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset network interface attribute"):
        reset_network_interface_attribute("test-network_interface_id", region_name=REGION)


def test_reset_snapshot_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_snapshot_attribute("test-attribute", "test-snapshot_id", region_name=REGION)
    mock_client.reset_snapshot_attribute.assert_called_once()


def test_reset_snapshot_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_snapshot_attribute",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset snapshot attribute"):
        reset_snapshot_attribute("test-attribute", "test-snapshot_id", region_name=REGION)


def test_restore_address_to_classic(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_address_to_classic.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_address_to_classic("test-public_ip", region_name=REGION)
    mock_client.restore_address_to_classic.assert_called_once()


def test_restore_address_to_classic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_address_to_classic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_address_to_classic",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore address to classic"):
        restore_address_to_classic("test-public_ip", region_name=REGION)


def test_restore_image_from_recycle_bin(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_image_from_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_image_from_recycle_bin("test-image_id", region_name=REGION)
    mock_client.restore_image_from_recycle_bin.assert_called_once()


def test_restore_image_from_recycle_bin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_image_from_recycle_bin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_image_from_recycle_bin",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore image from recycle bin"):
        restore_image_from_recycle_bin("test-image_id", region_name=REGION)


def test_restore_managed_prefix_list_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_managed_prefix_list_version.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_managed_prefix_list_version("test-prefix_list_id", 1, 1, region_name=REGION)
    mock_client.restore_managed_prefix_list_version.assert_called_once()


def test_restore_managed_prefix_list_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_managed_prefix_list_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_managed_prefix_list_version",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore managed prefix list version"):
        restore_managed_prefix_list_version("test-prefix_list_id", 1, 1, region_name=REGION)


def test_restore_snapshot_from_recycle_bin(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_snapshot_from_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_snapshot_from_recycle_bin("test-snapshot_id", region_name=REGION)
    mock_client.restore_snapshot_from_recycle_bin.assert_called_once()


def test_restore_snapshot_from_recycle_bin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_snapshot_from_recycle_bin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_snapshot_from_recycle_bin",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore snapshot from recycle bin"):
        restore_snapshot_from_recycle_bin("test-snapshot_id", region_name=REGION)


def test_restore_snapshot_tier(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_snapshot_tier.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_snapshot_tier("test-snapshot_id", region_name=REGION)
    mock_client.restore_snapshot_tier.assert_called_once()


def test_restore_snapshot_tier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_snapshot_tier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_snapshot_tier",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore snapshot tier"):
        restore_snapshot_tier("test-snapshot_id", region_name=REGION)


def test_revoke_client_vpn_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_client_vpn_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", region_name=REGION)
    mock_client.revoke_client_vpn_ingress.assert_called_once()


def test_revoke_client_vpn_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_client_vpn_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_client_vpn_ingress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke client vpn ingress"):
        revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", region_name=REGION)


def test_revoke_security_group_egress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_security_group_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_security_group_egress("test-group_id", region_name=REGION)
    mock_client.revoke_security_group_egress.assert_called_once()


def test_revoke_security_group_egress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_security_group_egress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_security_group_egress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke security group egress"):
        revoke_security_group_egress("test-group_id", region_name=REGION)


def test_revoke_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_security_group_ingress(region_name=REGION)
    mock_client.revoke_security_group_ingress.assert_called_once()


def test_revoke_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke security group ingress"):
        revoke_security_group_ingress(region_name=REGION)


def test_run_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    run_instances(1, 1, region_name=REGION)
    mock_client.run_instances.assert_called_once()


def test_run_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run instances"):
        run_instances(1, 1, region_name=REGION)


def test_run_scheduled_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    run_scheduled_instances({}, "test-scheduled_instance_id", region_name=REGION)
    mock_client.run_scheduled_instances.assert_called_once()


def test_run_scheduled_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_scheduled_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_scheduled_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run scheduled instances"):
        run_scheduled_instances({}, "test-scheduled_instance_id", region_name=REGION)


def test_search_local_gateway_routes(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_local_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_local_gateway_routes("test-local_gateway_route_table_id", region_name=REGION)
    mock_client.search_local_gateway_routes.assert_called_once()


def test_search_local_gateway_routes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_local_gateway_routes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_local_gateway_routes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search local gateway routes"):
        search_local_gateway_routes("test-local_gateway_route_table_id", region_name=REGION)


def test_search_transit_gateway_multicast_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_transit_gateway_multicast_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", region_name=REGION)
    mock_client.search_transit_gateway_multicast_groups.assert_called_once()


def test_search_transit_gateway_multicast_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_transit_gateway_multicast_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_transit_gateway_multicast_groups",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search transit gateway multicast groups"):
        search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", region_name=REGION)


def test_search_transit_gateway_routes(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_transit_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_transit_gateway_routes("test-transit_gateway_route_table_id", [], region_name=REGION)
    mock_client.search_transit_gateway_routes.assert_called_once()


def test_search_transit_gateway_routes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_transit_gateway_routes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_transit_gateway_routes",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search transit gateway routes"):
        search_transit_gateway_routes("test-transit_gateway_route_table_id", [], region_name=REGION)


def test_send_diagnostic_interrupt(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_diagnostic_interrupt.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    send_diagnostic_interrupt("test-instance_id", region_name=REGION)
    mock_client.send_diagnostic_interrupt.assert_called_once()


def test_send_diagnostic_interrupt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_diagnostic_interrupt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_diagnostic_interrupt",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send diagnostic interrupt"):
        send_diagnostic_interrupt("test-instance_id", region_name=REGION)


def test_start_declarative_policies_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_declarative_policies_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_declarative_policies_report("test-s3_bucket", "test-target_id", region_name=REGION)
    mock_client.start_declarative_policies_report.assert_called_once()


def test_start_declarative_policies_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_declarative_policies_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_declarative_policies_report",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start declarative policies report"):
        start_declarative_policies_report("test-s3_bucket", "test-target_id", region_name=REGION)


def test_start_network_insights_access_scope_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_network_insights_access_scope_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", region_name=REGION)
    mock_client.start_network_insights_access_scope_analysis.assert_called_once()


def test_start_network_insights_access_scope_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_network_insights_access_scope_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_network_insights_access_scope_analysis",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start network insights access scope analysis"):
        start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", region_name=REGION)


def test_start_network_insights_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_network_insights_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_network_insights_analysis("test-network_insights_path_id", "test-client_token", region_name=REGION)
    mock_client.start_network_insights_analysis.assert_called_once()


def test_start_network_insights_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_network_insights_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_network_insights_analysis",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start network insights analysis"):
        start_network_insights_analysis("test-network_insights_path_id", "test-client_token", region_name=REGION)


def test_start_vpc_endpoint_service_private_dns_verification(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_vpc_endpoint_service_private_dns_verification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_vpc_endpoint_service_private_dns_verification("test-service_id", region_name=REGION)
    mock_client.start_vpc_endpoint_service_private_dns_verification.assert_called_once()


def test_start_vpc_endpoint_service_private_dns_verification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_vpc_endpoint_service_private_dns_verification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_vpc_endpoint_service_private_dns_verification",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start vpc endpoint service private dns verification"):
        start_vpc_endpoint_service_private_dns_verification("test-service_id", region_name=REGION)


def test_terminate_client_vpn_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_client_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    terminate_client_vpn_connections("test-client_vpn_endpoint_id", region_name=REGION)
    mock_client.terminate_client_vpn_connections.assert_called_once()


def test_terminate_client_vpn_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_client_vpn_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "terminate_client_vpn_connections",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate client vpn connections"):
        terminate_client_vpn_connections("test-client_vpn_endpoint_id", region_name=REGION)


def test_unassign_ipv6_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_ipv6_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_ipv6_addresses("test-network_interface_id", region_name=REGION)
    mock_client.unassign_ipv6_addresses.assert_called_once()


def test_unassign_ipv6_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_ipv6_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unassign_ipv6_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unassign ipv6 addresses"):
        unassign_ipv6_addresses("test-network_interface_id", region_name=REGION)


def test_unassign_private_ip_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_private_ip_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_private_ip_addresses("test-network_interface_id", region_name=REGION)
    mock_client.unassign_private_ip_addresses.assert_called_once()


def test_unassign_private_ip_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_private_ip_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unassign_private_ip_addresses",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unassign private ip addresses"):
        unassign_private_ip_addresses("test-network_interface_id", region_name=REGION)


def test_unassign_private_nat_gateway_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_private_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_private_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)
    mock_client.unassign_private_nat_gateway_address.assert_called_once()


def test_unassign_private_nat_gateway_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unassign_private_nat_gateway_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unassign_private_nat_gateway_address",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unassign private nat gateway address"):
        unassign_private_nat_gateway_address("test-nat_gateway_id", [], region_name=REGION)


def test_unlock_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.unlock_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unlock_snapshot("test-snapshot_id", region_name=REGION)
    mock_client.unlock_snapshot.assert_called_once()


def test_unlock_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unlock_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unlock_snapshot",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unlock snapshot"):
        unlock_snapshot("test-snapshot_id", region_name=REGION)


def test_unmonitor_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.unmonitor_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unmonitor_instances([], region_name=REGION)
    mock_client.unmonitor_instances.assert_called_once()


def test_unmonitor_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unmonitor_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unmonitor_instances",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unmonitor instances"):
        unmonitor_instances([], region_name=REGION)


def test_update_capacity_manager_organizations_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_manager_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_capacity_manager_organizations_access(True, region_name=REGION)
    mock_client.update_capacity_manager_organizations_access.assert_called_once()


def test_update_capacity_manager_organizations_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_manager_organizations_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_capacity_manager_organizations_access",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update capacity manager organizations access"):
        update_capacity_manager_organizations_access(True, region_name=REGION)


def test_update_security_group_rule_descriptions_egress(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_security_group_rule_descriptions_egress(region_name=REGION)
    mock_client.update_security_group_rule_descriptions_egress.assert_called_once()


def test_update_security_group_rule_descriptions_egress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_egress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_group_rule_descriptions_egress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security group rule descriptions egress"):
        update_security_group_rule_descriptions_egress(region_name=REGION)


def test_update_security_group_rule_descriptions_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_security_group_rule_descriptions_ingress(region_name=REGION)
    mock_client.update_security_group_rule_descriptions_ingress.assert_called_once()


def test_update_security_group_rule_descriptions_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_group_rule_descriptions_ingress",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security group rule descriptions ingress"):
        update_security_group_rule_descriptions_ingress(region_name=REGION)


def test_withdraw_byoip_cidr(monkeypatch):
    mock_client = MagicMock()
    mock_client.withdraw_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    withdraw_byoip_cidr("test-cidr", region_name=REGION)
    mock_client.withdraw_byoip_cidr.assert_called_once()


def test_withdraw_byoip_cidr_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.withdraw_byoip_cidr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "withdraw_byoip_cidr",
    )
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to withdraw byoip cidr"):
        withdraw_byoip_cidr("test-cidr", region_name=REGION)


def test_accept_address_transfer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import accept_address_transfer
    mock_client = MagicMock()
    mock_client.accept_address_transfer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_address_transfer("test-address", tag_specifications={}, region_name="us-east-1")
    mock_client.accept_address_transfer.assert_called_once()

def test_accept_reserved_instances_exchange_quote_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import accept_reserved_instances_exchange_quote
    mock_client = MagicMock()
    mock_client.accept_reserved_instances_exchange_quote.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_reserved_instances_exchange_quote("test-reserved_instance_ids", target_configurations={}, region_name="us-east-1")
    mock_client.accept_reserved_instances_exchange_quote.assert_called_once()

def test_accept_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import accept_transit_gateway_multicast_domain_associations
    mock_client = MagicMock()
    mock_client.accept_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    accept_transit_gateway_multicast_domain_associations(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.accept_transit_gateway_multicast_domain_associations.assert_called_once()

def test_advertise_byoip_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import advertise_byoip_cidr
    mock_client = MagicMock()
    mock_client.advertise_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    advertise_byoip_cidr("test-cidr", asn="test-asn", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.advertise_byoip_cidr.assert_called_once()

def test_allocate_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import allocate_address
    mock_client = MagicMock()
    mock_client.allocate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_address(domain="test-domain", address="test-address", public_ipv4_pool="test-public_ipv4_pool", network_border_group="test-network_border_group", customer_owned_ipv4_pool="test-customer_owned_ipv4_pool", tag_specifications={}, ipam_pool_id="test-ipam_pool_id", region_name="us-east-1")
    mock_client.allocate_address.assert_called_once()

def test_allocate_hosts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import allocate_hosts
    mock_client = MagicMock()
    mock_client.allocate_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_hosts(instance_family="test-instance_family", tag_specifications={}, host_recovery="test-host_recovery", outpost_arn="test-outpost_arn", host_maintenance="test-host_maintenance", asset_ids="test-asset_ids", availability_zone_id="test-availability_zone_id", auto_placement=True, client_token="test-client_token", instance_type="test-instance_type", quantity="test-quantity", availability_zone="test-availability_zone", region_name="us-east-1")
    mock_client.allocate_hosts.assert_called_once()

def test_allocate_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import allocate_ipam_pool_cidr
    mock_client = MagicMock()
    mock_client.allocate_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    allocate_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", netmask_length="test-netmask_length", client_token="test-client_token", description="test-description", preview_next_cidr="test-preview_next_cidr", allowed_cidrs=True, disallowed_cidrs="test-disallowed_cidrs", region_name="us-east-1")
    mock_client.allocate_ipam_pool_cidr.assert_called_once()

def test_assign_ipv6_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import assign_ipv6_addresses
    mock_client = MagicMock()
    mock_client.assign_ipv6_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_ipv6_addresses("test-network_interface_id", ipv6_prefix_count=1, ipv6_prefixes="test-ipv6_prefixes", ipv6_addresses="test-ipv6_addresses", ipv6_address_count=1, region_name="us-east-1")
    mock_client.assign_ipv6_addresses.assert_called_once()

def test_assign_private_ip_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import assign_private_ip_addresses
    mock_client = MagicMock()
    mock_client.assign_private_ip_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_private_ip_addresses("test-network_interface_id", ipv4_prefixes="test-ipv4_prefixes", ipv4_prefix_count=1, private_ip_addresses="test-private_ip_addresses", secondary_private_ip_address_count=1, allow_reassignment=True, region_name="us-east-1")
    mock_client.assign_private_ip_addresses.assert_called_once()

def test_assign_private_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import assign_private_nat_gateway_address
    mock_client = MagicMock()
    mock_client.assign_private_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    assign_private_nat_gateway_address("test-nat_gateway_id", private_ip_addresses="test-private_ip_addresses", private_ip_address_count=1, region_name="us-east-1")
    mock_client.assign_private_nat_gateway_address.assert_called_once()

def test_associate_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_address
    mock_client = MagicMock()
    mock_client.associate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_address(allocation_id="test-allocation_id", instance_id="test-instance_id", public_ip="test-public_ip", network_interface_id="test-network_interface_id", private_ip_address="test-private_ip_address", allow_reassociation=True, region_name="us-east-1")
    mock_client.associate_address.assert_called_once()

def test_associate_client_vpn_target_network_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_client_vpn_target_network
    mock_client = MagicMock()
    mock_client.associate_client_vpn_target_network.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_client_vpn_target_network("test-client_vpn_endpoint_id", "test-subnet_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_client_vpn_target_network.assert_called_once()

def test_associate_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_ipam_resource_discovery
    mock_client = MagicMock()
    mock_client.associate_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_ipam_resource_discovery("test-ipam_id", "test-ipam_resource_discovery_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_ipam_resource_discovery.assert_called_once()

def test_associate_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_nat_gateway_address
    mock_client = MagicMock()
    mock_client.associate_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_nat_gateway_address("test-nat_gateway_id", "test-allocation_ids", private_ip_addresses="test-private_ip_addresses", region_name="us-east-1")
    mock_client.associate_nat_gateway_address.assert_called_once()

def test_associate_route_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_route_table
    mock_client = MagicMock()
    mock_client.associate_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_route_table("test-route_table_id", gateway_id="test-gateway_id", public_ipv4_pool="test-public_ipv4_pool", subnet_id="test-subnet_id", region_name="us-east-1")
    mock_client.associate_route_table.assert_called_once()

def test_associate_subnet_cidr_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_subnet_cidr_block
    mock_client = MagicMock()
    mock_client.associate_subnet_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_subnet_cidr_block("test-subnet_id", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", ipv6_cidr_block="test-ipv6_cidr_block", region_name="us-east-1")
    mock_client.associate_subnet_cidr_block.assert_called_once()

def test_associate_trunk_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_trunk_interface
    mock_client = MagicMock()
    mock_client.associate_trunk_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_trunk_interface("test-branch_interface_id", "test-trunk_interface_id", vlan_id="test-vlan_id", gre_key="test-gre_key", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_trunk_interface.assert_called_once()

def test_associate_vpc_cidr_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import associate_vpc_cidr_block
    mock_client = MagicMock()
    mock_client.associate_vpc_cidr_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    associate_vpc_cidr_block("test-vpc_id", cidr_block="test-cidr_block", ipv6_cidr_block_network_border_group="test-ipv6_cidr_block_network_border_group", ipv6_pool="test-ipv6_pool", ipv6_cidr_block="test-ipv6_cidr_block", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", amazon_provided_ipv6_cidr_block="test-amazon_provided_ipv6_cidr_block", region_name="us-east-1")
    mock_client.associate_vpc_cidr_block.assert_called_once()

def test_attach_network_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import attach_network_interface
    mock_client = MagicMock()
    mock_client.attach_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_network_interface("test-network_interface_id", "test-instance_id", "test-device_index", network_card_index="test-network_card_index", ena_srd_specification={}, ena_queue_count=1, region_name="us-east-1")
    mock_client.attach_network_interface.assert_called_once()

def test_attach_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import attach_verified_access_trust_provider
    mock_client = MagicMock()
    mock_client.attach_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    attach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.attach_verified_access_trust_provider.assert_called_once()

def test_authorize_client_vpn_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import authorize_client_vpn_ingress
    mock_client = MagicMock()
    mock_client.authorize_client_vpn_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", access_group_id="test-access_group_id", authorize_all_groups="test-authorize_all_groups", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.authorize_client_vpn_ingress.assert_called_once()

def test_authorize_security_group_egress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import authorize_security_group_egress
    mock_client = MagicMock()
    mock_client.authorize_security_group_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_security_group_egress("test-group_id", tag_specifications={}, source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", ip_protocol="test-ip_protocol", from_port=1, to_port=1, cidr_ip="test-cidr_ip", ip_permissions="test-ip_permissions", region_name="us-east-1")
    mock_client.authorize_security_group_egress.assert_called_once()

def test_authorize_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import authorize_security_group_ingress
    mock_client = MagicMock()
    mock_client.authorize_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    authorize_security_group_ingress(cidr_ip="test-cidr_ip", from_port=1, group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", ip_protocol="test-ip_protocol", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", to_port=1, tag_specifications={}, region_name="us-east-1")
    mock_client.authorize_security_group_ingress.assert_called_once()

def test_cancel_conversion_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import cancel_conversion_task
    mock_client = MagicMock()
    mock_client.cancel_conversion_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_conversion_task("test-conversion_task_id", reason_message="test-reason_message", region_name="us-east-1")
    mock_client.cancel_conversion_task.assert_called_once()

def test_cancel_import_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import cancel_import_task
    mock_client = MagicMock()
    mock_client.cancel_import_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    cancel_import_task(cancel_reason="test-cancel_reason", import_task_id=1, region_name="us-east-1")
    mock_client.cancel_import_task.assert_called_once()

def test_copy_fpga_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import copy_fpga_image
    mock_client = MagicMock()
    mock_client.copy_fpga_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_fpga_image("test-source_fpga_image_id", "test-source_region", description="test-description", name="test-name", client_token="test-client_token", region_name="us-east-1")
    mock_client.copy_fpga_image.assert_called_once()

def test_copy_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import copy_image
    mock_client = MagicMock()
    mock_client.copy_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_image("test-name", "test-source_image_id", "test-source_region", client_token="test-client_token", description="test-description", encrypted=True, kms_key_id="test-kms_key_id", destination_outpost_arn="test-destination_outpost_arn", copy_image_tags=[{"Key": "k", "Value": "v"}], tag_specifications={}, snapshot_copy_completion_duration_minutes=1, destination_availability_zone="test-destination_availability_zone", destination_availability_zone_id="test-destination_availability_zone_id", region_name="us-east-1")
    mock_client.copy_image.assert_called_once()

def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import copy_snapshot
    mock_client = MagicMock()
    mock_client.copy_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_snapshot("test-source_region", "test-source_snapshot_id", description="test-description", destination_outpost_arn="test-destination_outpost_arn", destination_region="test-destination_region", encrypted=True, kms_key_id="test-kms_key_id", presigned_url="test-presigned_url", tag_specifications={}, completion_duration_minutes=1, destination_availability_zone="test-destination_availability_zone", region_name="us-east-1")
    mock_client.copy_snapshot.assert_called_once()

def test_copy_volumes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import copy_volumes
    mock_client = MagicMock()
    mock_client.copy_volumes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    copy_volumes("test-source_volume_id", iops="test-iops", size=1, volume_type="test-volume_type", tag_specifications={}, multi_attach_enabled=True, throughput="test-throughput", client_token="test-client_token", region_name="us-east-1")
    mock_client.copy_volumes.assert_called_once()

def test_create_capacity_manager_data_export_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_capacity_manager_data_export
    mock_client = MagicMock()
    mock_client.create_capacity_manager_data_export.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_manager_data_export("test-s3_bucket_name", "test-schedule", "test-output_format", s3_bucket_prefix="test-s3_bucket_prefix", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_capacity_manager_data_export.assert_called_once()

def test_create_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_capacity_reservation
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation("test-instance_type", "test-instance_platform", 1, client_token="test-client_token", availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", tenancy="test-tenancy", ebs_optimized="test-ebs_optimized", ephemeral_storage="test-ephemeral_storage", end_date="test-end_date", end_date_type="test-end_date_type", instance_match_criteria="test-instance_match_criteria", tag_specifications={}, outpost_arn="test-outpost_arn", placement_group_arn="test-placement_group_arn", start_date="test-start_date", commitment_duration=1, delivery_preference="test-delivery_preference", region_name="us-east-1")
    mock_client.create_capacity_reservation.assert_called_once()

def test_create_capacity_reservation_by_splitting_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_capacity_reservation_by_splitting
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_by_splitting.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation_by_splitting("test-source_capacity_reservation_id", 1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_capacity_reservation_by_splitting.assert_called_once()

def test_create_capacity_reservation_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_capacity_reservation_fleet
    mock_client = MagicMock()
    mock_client.create_capacity_reservation_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation_fleet({}, "test-total_target_capacity", allocation_strategy="test-allocation_strategy", client_token="test-client_token", tenancy="test-tenancy", end_date="test-end_date", instance_match_criteria="test-instance_match_criteria", tag_specifications={}, region_name="us-east-1")
    mock_client.create_capacity_reservation_fleet.assert_called_once()

def test_create_carrier_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_carrier_gateway
    mock_client = MagicMock()
    mock_client.create_carrier_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_carrier_gateway("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_carrier_gateway.assert_called_once()

def test_create_client_vpn_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_client_vpn_endpoint
    mock_client = MagicMock()
    mock_client.create_client_vpn_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_client_vpn_endpoint("test-server_certificate_arn", {}, {}, client_cidr_block="test-client_cidr_block", dns_servers="test-dns_servers", transport_protocol=1, vpn_port=1, description="test-description", split_tunnel="test-split_tunnel", client_token="test-client_token", tag_specifications={}, security_group_ids="test-security_group_ids", vpc_id="test-vpc_id", self_service_portal=1, client_connect_options={}, session_timeout_hours=1, client_login_banner_options={}, client_route_enforcement_options={}, disconnect_on_session_timeout=1, endpoint_ip_address_type="test-endpoint_ip_address_type", traffic_ip_address_type="test-traffic_ip_address_type", region_name="us-east-1")
    mock_client.create_client_vpn_endpoint.assert_called_once()

def test_create_client_vpn_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_client_vpn_route
    mock_client = MagicMock()
    mock_client.create_client_vpn_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", "test-target_vpc_subnet_id", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_client_vpn_route.assert_called_once()

def test_create_coip_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_coip_pool
    mock_client = MagicMock()
    mock_client.create_coip_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_coip_pool("test-local_gateway_route_table_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_coip_pool.assert_called_once()

def test_create_customer_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_customer_gateway
    mock_client = MagicMock()
    mock_client.create_customer_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_customer_gateway("test-type_value", bgp_asn="test-bgp_asn", public_ip="test-public_ip", certificate_arn="test-certificate_arn", tag_specifications={}, device_name="test-device_name", ip_address="test-ip_address", bgp_asn_extended="test-bgp_asn_extended", region_name="us-east-1")
    mock_client.create_customer_gateway.assert_called_once()

def test_create_default_subnet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_default_subnet
    mock_client = MagicMock()
    mock_client.create_default_subnet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_default_subnet(availability_zone="test-availability_zone", ipv6_native="test-ipv6_native", availability_zone_id="test-availability_zone_id", region_name="us-east-1")
    mock_client.create_default_subnet.assert_called_once()

def test_create_delegate_mac_volume_ownership_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_delegate_mac_volume_ownership_task
    mock_client = MagicMock()
    mock_client.create_delegate_mac_volume_ownership_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_delegate_mac_volume_ownership_task("test-instance_id", "test-mac_credentials", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_delegate_mac_volume_ownership_task.assert_called_once()

def test_create_dhcp_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_dhcp_options
    mock_client = MagicMock()
    mock_client.create_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_dhcp_options({}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_dhcp_options.assert_called_once()

def test_create_egress_only_internet_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_egress_only_internet_gateway
    mock_client = MagicMock()
    mock_client.create_egress_only_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_egress_only_internet_gateway("test-vpc_id", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_egress_only_internet_gateway.assert_called_once()

def test_create_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_fleet
    mock_client = MagicMock()
    mock_client.create_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_fleet({}, {}, client_token="test-client_token", spot_options={}, on_demand_options={}, excess_capacity_termination_policy="{}", terminate_instances_with_expiration="test-terminate_instances_with_expiration", type_value="test-type_value", valid_from="test-valid_from", valid_until="test-valid_until", replace_unhealthy_instances="test-replace_unhealthy_instances", tag_specifications={}, context={}, region_name="us-east-1")
    mock_client.create_fleet.assert_called_once()

def test_create_flow_logs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_flow_logs
    mock_client = MagicMock()
    mock_client.create_flow_logs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_flow_logs("test-resource_ids", "test-resource_type", client_token="test-client_token", deliver_logs_permission_arn="test-deliver_logs_permission_arn", deliver_cross_account_role=1, log_group_name="test-log_group_name", traffic_type="test-traffic_type", log_destination_type="test-log_destination_type", log_destination="test-log_destination", log_format="test-log_format", tag_specifications={}, max_aggregation_interval=1, destination_options={}, region_name="us-east-1")
    mock_client.create_flow_logs.assert_called_once()

def test_create_fpga_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_fpga_image
    mock_client = MagicMock()
    mock_client.create_fpga_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_fpga_image("test-input_storage_location", logs_storage_location="test-logs_storage_location", description="test-description", name="test-name", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_fpga_image.assert_called_once()

def test_create_image_usage_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_image_usage_report
    mock_client = MagicMock()
    mock_client.create_image_usage_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_image_usage_report("test-image_id", "test-resource_types", account_ids=1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_image_usage_report.assert_called_once()

def test_create_instance_connect_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_instance_connect_endpoint
    mock_client = MagicMock()
    mock_client.create_instance_connect_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_connect_endpoint("test-subnet_id", security_group_ids="test-security_group_ids", preserve_client_ip="test-preserve_client_ip", client_token="test-client_token", tag_specifications={}, ip_address_type="test-ip_address_type", region_name="us-east-1")
    mock_client.create_instance_connect_endpoint.assert_called_once()

def test_create_instance_event_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_instance_event_window
    mock_client = MagicMock()
    mock_client.create_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_event_window(name="test-name", time_ranges="test-time_ranges", cron_expression="test-cron_expression", tag_specifications={}, region_name="us-east-1")
    mock_client.create_instance_event_window.assert_called_once()

def test_create_instance_export_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_instance_export_task
    mock_client = MagicMock()
    mock_client.create_instance_export_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_instance_export_task("test-instance_id", "test-target_environment", 1, tag_specifications={}, description="test-description", region_name="us-east-1")
    mock_client.create_instance_export_task.assert_called_once()

def test_create_internet_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_internet_gateway
    mock_client = MagicMock()
    mock_client.create_internet_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_internet_gateway(tag_specifications={}, region_name="us-east-1")
    mock_client.create_internet_gateway.assert_called_once()

def test_create_ipam_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam
    mock_client = MagicMock()
    mock_client.create_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam(description="test-description", operating_regions="test-operating_regions", tag_specifications={}, client_token="test-client_token", tier="test-tier", enable_private_gua=True, metered_account=1, region_name="us-east-1")
    mock_client.create_ipam.assert_called_once()

def test_create_ipam_external_resource_verification_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_external_resource_verification_token
    mock_client = MagicMock()
    mock_client.create_ipam_external_resource_verification_token.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_external_resource_verification_token("test-ipam_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_ipam_external_resource_verification_token.assert_called_once()

def test_create_ipam_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_pool
    mock_client = MagicMock()
    mock_client.create_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_pool("test-ipam_scope_id", "test-address_family", locale="test-locale", source_ipam_pool_id="test-source_ipam_pool_id", description="test-description", auto_import=True, publicly_advertisable="test-publicly_advertisable", allocation_min_netmask_length="test-allocation_min_netmask_length", allocation_max_netmask_length=1, allocation_default_netmask_length="test-allocation_default_netmask_length", allocation_resource_tags=[{"Key": "k", "Value": "v"}], tag_specifications={}, client_token="test-client_token", aws_service="test-aws_service", public_ip_source="test-public_ip_source", source_resource="test-source_resource", region_name="us-east-1")
    mock_client.create_ipam_pool.assert_called_once()

def test_create_ipam_prefix_list_resolver_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_prefix_list_resolver
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_prefix_list_resolver("test-ipam_id", "test-address_family", description="test-description", rules="test-rules", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_ipam_prefix_list_resolver.assert_called_once()

def test_create_ipam_prefix_list_resolver_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_prefix_list_resolver_target
    mock_client = MagicMock()
    mock_client.create_ipam_prefix_list_resolver_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_id", "test-prefix_list_id", "test-prefix_list_region", "test-track_latest_version", desired_version="test-desired_version", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_ipam_prefix_list_resolver_target.assert_called_once()

def test_create_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_resource_discovery
    mock_client = MagicMock()
    mock_client.create_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_resource_discovery(description="test-description", operating_regions="test-operating_regions", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_ipam_resource_discovery.assert_called_once()

def test_create_ipam_scope_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_ipam_scope
    mock_client = MagicMock()
    mock_client.create_ipam_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_ipam_scope("test-ipam_id", description="test-description", tag_specifications={}, client_token="test-client_token", external_authority_configuration={}, region_name="us-east-1")
    mock_client.create_ipam_scope.assert_called_once()

def test_create_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_key_pair
    mock_client = MagicMock()
    mock_client.create_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_key_pair("test-key_name", key_type="test-key_type", tag_specifications={}, key_format="test-key_format", region_name="us-east-1")
    mock_client.create_key_pair.assert_called_once()

def test_create_launch_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_launch_template
    mock_client = MagicMock()
    mock_client.create_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_launch_template("test-launch_template_name", "test-launch_template_data", client_token="test-client_token", version_description="test-version_description", operator="test-operator", tag_specifications={}, region_name="us-east-1")
    mock_client.create_launch_template.assert_called_once()

def test_create_launch_template_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_launch_template_version
    mock_client = MagicMock()
    mock_client.create_launch_template_version.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_launch_template_version("test-launch_template_data", client_token="test-client_token", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", source_version="test-source_version", version_description="test-version_description", resolve_alias="test-resolve_alias", region_name="us-east-1")
    mock_client.create_launch_template_version.assert_called_once()

def test_create_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_route
    mock_client = MagicMock()
    mock_client.create_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", local_gateway_virtual_interface_group_id="test-local_gateway_virtual_interface_group_id", network_interface_id="test-network_interface_id", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.create_local_gateway_route.assert_called_once()

def test_create_local_gateway_route_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_route_table
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table("test-local_gateway_id", mode="test-mode", tag_specifications={}, region_name="us-east-1")
    mock_client.create_local_gateway_route_table.assert_called_once()

def test_create_local_gateway_route_table_virtual_interface_group_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_route_table_virtual_interface_group_association
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_virtual_interface_group_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table_virtual_interface_group_association("test-local_gateway_route_table_id", "test-local_gateway_virtual_interface_group_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_local_gateway_route_table_virtual_interface_group_association.assert_called_once()

def test_create_local_gateway_route_table_vpc_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_route_table_vpc_association
    mock_client = MagicMock()
    mock_client.create_local_gateway_route_table_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_route_table_vpc_association("test-local_gateway_route_table_id", "test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_local_gateway_route_table_vpc_association.assert_called_once()

def test_create_local_gateway_virtual_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_virtual_interface
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_virtual_interface("test-local_gateway_virtual_interface_group_id", "test-outpost_lag_id", "test-vlan", "test-local_address", "test-peer_address", peer_bgp_asn="test-peer_bgp_asn", tag_specifications={}, peer_bgp_asn_extended="test-peer_bgp_asn_extended", region_name="us-east-1")
    mock_client.create_local_gateway_virtual_interface.assert_called_once()

def test_create_local_gateway_virtual_interface_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_local_gateway_virtual_interface_group
    mock_client = MagicMock()
    mock_client.create_local_gateway_virtual_interface_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_local_gateway_virtual_interface_group("test-local_gateway_id", local_bgp_asn="test-local_bgp_asn", local_bgp_asn_extended="test-local_bgp_asn_extended", tag_specifications={}, region_name="us-east-1")
    mock_client.create_local_gateway_virtual_interface_group.assert_called_once()

def test_create_mac_system_integrity_protection_modification_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_mac_system_integrity_protection_modification_task
    mock_client = MagicMock()
    mock_client.create_mac_system_integrity_protection_modification_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_mac_system_integrity_protection_modification_task("test-instance_id", "test-mac_system_integrity_protection_status", client_token="test-client_token", mac_credentials="test-mac_credentials", mac_system_integrity_protection_configuration={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_mac_system_integrity_protection_modification_task.assert_called_once()

def test_create_managed_prefix_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_managed_prefix_list
    mock_client = MagicMock()
    mock_client.create_managed_prefix_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_managed_prefix_list("test-prefix_list_name", 1, "test-address_family", entries="test-entries", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_managed_prefix_list.assert_called_once()

def test_create_nat_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_nat_gateway
    mock_client = MagicMock()
    mock_client.create_nat_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_nat_gateway("test-subnet_id", allocation_id="test-allocation_id", client_token="test-client_token", tag_specifications={}, connectivity_type="test-connectivity_type", private_ip_address="test-private_ip_address", secondary_allocation_ids="test-secondary_allocation_ids", secondary_private_ip_addresses="test-secondary_private_ip_addresses", secondary_private_ip_address_count=1, region_name="us-east-1")
    mock_client.create_nat_gateway.assert_called_once()

def test_create_network_acl_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_acl
    mock_client = MagicMock()
    mock_client.create_network_acl.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_acl("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_network_acl.assert_called_once()

def test_create_network_acl_entry_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_acl_entry
    mock_client = MagicMock()
    mock_client.create_network_acl_entry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_acl_entry("test-network_acl_id", "test-rule_number", "test-protocol", "test-rule_action", "test-egress", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", icmp_type_code="test-icmp_type_code", port_range=1, region_name="us-east-1")
    mock_client.create_network_acl_entry.assert_called_once()

def test_create_network_insights_access_scope_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_insights_access_scope
    mock_client = MagicMock()
    mock_client.create_network_insights_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_insights_access_scope("test-client_token", match_paths="test-match_paths", exclude_paths="test-exclude_paths", tag_specifications={}, region_name="us-east-1")
    mock_client.create_network_insights_access_scope.assert_called_once()

def test_create_network_insights_path_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_insights_path
    mock_client = MagicMock()
    mock_client.create_network_insights_path.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_insights_path("test-source", "test-protocol", "test-client_token", source_ip="test-source_ip", destination_ip="test-destination_ip", destination="test-destination", destination_port=1, tag_specifications={}, filter_at_source="test-filter_at_source", filter_at_destination="test-filter_at_destination", region_name="us-east-1")
    mock_client.create_network_insights_path.assert_called_once()

def test_create_network_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_interface
    mock_client = MagicMock()
    mock_client.create_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_interface("test-subnet_id", ipv4_prefixes="test-ipv4_prefixes", ipv4_prefix_count=1, ipv6_prefixes="test-ipv6_prefixes", ipv6_prefix_count=1, interface_type="test-interface_type", tag_specifications={}, client_token="test-client_token", enable_primary_ipv6=True, connection_tracking_specification={}, operator="test-operator", description="test-description", private_ip_address="test-private_ip_address", groups="test-groups", private_ip_addresses="test-private_ip_addresses", secondary_private_ip_address_count=1, ipv6_addresses="test-ipv6_addresses", ipv6_address_count=1, region_name="us-east-1")
    mock_client.create_network_interface.assert_called_once()

def test_create_network_interface_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_network_interface_permission
    mock_client = MagicMock()
    mock_client.create_network_interface_permission.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_network_interface_permission("test-network_interface_id", "test-permission", aws_account_id=1, aws_service="test-aws_service", region_name="us-east-1")
    mock_client.create_network_interface_permission.assert_called_once()

def test_create_placement_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_placement_group
    mock_client = MagicMock()
    mock_client.create_placement_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_placement_group(partition_count=1, tag_specifications={}, spread_level="test-spread_level", group_name="test-group_name", strategy="test-strategy", region_name="us-east-1")
    mock_client.create_placement_group.assert_called_once()

def test_create_public_ipv4_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_public_ipv4_pool
    mock_client = MagicMock()
    mock_client.create_public_ipv4_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_public_ipv4_pool(tag_specifications={}, network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.create_public_ipv4_pool.assert_called_once()

def test_create_replace_root_volume_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_replace_root_volume_task
    mock_client = MagicMock()
    mock_client.create_replace_root_volume_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_replace_root_volume_task("test-instance_id", snapshot_id="test-snapshot_id", client_token="test-client_token", tag_specifications={}, image_id="test-image_id", delete_replaced_root_volume=True, volume_initialization_rate="test-volume_initialization_rate", region_name="us-east-1")
    mock_client.create_replace_root_volume_task.assert_called_once()

def test_create_restore_image_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_restore_image_task
    mock_client = MagicMock()
    mock_client.create_restore_image_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_restore_image_task("test-bucket", "test-object_key", name="test-name", tag_specifications={}, region_name="us-east-1")
    mock_client.create_restore_image_task.assert_called_once()

def test_create_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_route
    mock_client = MagicMock()
    mock_client.create_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", vpc_endpoint_id="test-vpc_endpoint_id", transit_gateway_id="test-transit_gateway_id", local_gateway_id="test-local_gateway_id", carrier_gateway_id="test-carrier_gateway_id", core_network_arn="test-core_network_arn", odb_network_arn="test-odb_network_arn", destination_cidr_block="test-destination_cidr_block", gateway_id="test-gateway_id", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", egress_only_internet_gateway_id="test-egress_only_internet_gateway_id", instance_id="test-instance_id", network_interface_id="test-network_interface_id", vpc_peering_connection_id="test-vpc_peering_connection_id", nat_gateway_id="test-nat_gateway_id", region_name="us-east-1")
    mock_client.create_route.assert_called_once()

def test_create_route_server_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_route_server
    mock_client = MagicMock()
    mock_client.create_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server("test-amazon_side_asn", client_token="test-client_token", persist_routes="test-persist_routes", persist_routes_duration=1, sns_notifications_enabled="test-sns_notifications_enabled", tag_specifications={}, region_name="us-east-1")
    mock_client.create_route_server.assert_called_once()

def test_create_route_server_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_route_server_endpoint
    mock_client = MagicMock()
    mock_client.create_route_server_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server_endpoint("test-route_server_id", "test-subnet_id", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_route_server_endpoint.assert_called_once()

def test_create_route_server_peer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_route_server_peer
    mock_client = MagicMock()
    mock_client.create_route_server_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_server_peer("test-route_server_endpoint_id", "test-peer_address", {}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_route_server_peer.assert_called_once()

def test_create_route_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_route_table
    mock_client = MagicMock()
    mock_client.create_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_route_table("test-vpc_id", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_route_table.assert_called_once()

def test_create_security_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_security_group
    mock_client = MagicMock()
    mock_client.create_security_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_security_group("test-description", "test-group_name", vpc_id="test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_security_group.assert_called_once()

def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_snapshot
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-volume_id", description="test-description", outpost_arn="test-outpost_arn", tag_specifications={}, location="test-location", region_name="us-east-1")
    mock_client.create_snapshot.assert_called_once()

def test_create_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_snapshots
    mock_client = MagicMock()
    mock_client.create_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_snapshots({}, description="test-description", outpost_arn="test-outpost_arn", tag_specifications={}, copy_tags_from_source=[{"Key": "k", "Value": "v"}], location="test-location", region_name="us-east-1")
    mock_client.create_snapshots.assert_called_once()

def test_create_spot_datafeed_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_spot_datafeed_subscription
    mock_client = MagicMock()
    mock_client.create_spot_datafeed_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_spot_datafeed_subscription("test-bucket", prefix="test-prefix", region_name="us-east-1")
    mock_client.create_spot_datafeed_subscription.assert_called_once()

def test_create_store_image_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_store_image_task
    mock_client = MagicMock()
    mock_client.create_store_image_task.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_store_image_task("test-image_id", "test-bucket", s3_object_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_store_image_task.assert_called_once()

def test_create_subnet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_subnet
    mock_client = MagicMock()
    mock_client.create_subnet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_subnet("test-vpc_id", tag_specifications={}, availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", outpost_arn="test-outpost_arn", ipv6_native="test-ipv6_native", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", region_name="us-east-1")
    mock_client.create_subnet.assert_called_once()

def test_create_subnet_cidr_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_subnet_cidr_reservation
    mock_client = MagicMock()
    mock_client.create_subnet_cidr_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_subnet_cidr_reservation("test-subnet_id", "test-cidr", "test-reservation_type", description="test-description", tag_specifications={}, region_name="us-east-1")
    mock_client.create_subnet_cidr_reservation.assert_called_once()

def test_create_traffic_mirror_filter_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_traffic_mirror_filter
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_filter(description="test-description", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_traffic_mirror_filter.assert_called_once()

def test_create_traffic_mirror_filter_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_traffic_mirror_filter_rule
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_filter_rule.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_filter_rule("test-traffic_mirror_filter_id", "test-traffic_direction", "test-rule_number", "test-rule_action", "test-destination_cidr_block", "test-source_cidr_block", destination_port_range=1, source_port_range=1, protocol="test-protocol", description="test-description", client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_traffic_mirror_filter_rule.assert_called_once()

def test_create_traffic_mirror_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_traffic_mirror_session
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_session.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_session("test-network_interface_id", "test-traffic_mirror_target_id", "test-traffic_mirror_filter_id", "test-session_number", packet_length="test-packet_length", virtual_network_id="test-virtual_network_id", description="test-description", tag_specifications={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_traffic_mirror_session.assert_called_once()

def test_create_traffic_mirror_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_traffic_mirror_target
    mock_client = MagicMock()
    mock_client.create_traffic_mirror_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_traffic_mirror_target(network_interface_id="test-network_interface_id", network_load_balancer_arn="test-network_load_balancer_arn", description="test-description", tag_specifications={}, client_token="test-client_token", gateway_load_balancer_endpoint_id="test-gateway_load_balancer_endpoint_id", region_name="us-east-1")
    mock_client.create_traffic_mirror_target.assert_called_once()

def test_create_transit_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway
    mock_client = MagicMock()
    mock_client.create_transit_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway(description="test-description", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway.assert_called_once()

def test_create_transit_gateway_connect_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_connect
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_connect(1, {}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_connect.assert_called_once()

def test_create_transit_gateway_connect_peer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_connect_peer
    mock_client = MagicMock()
    mock_client.create_transit_gateway_connect_peer.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_connect_peer("test-transit_gateway_attachment_id", "test-peer_address", "test-inside_cidr_blocks", transit_gateway_address="test-transit_gateway_address", bgp_options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_connect_peer.assert_called_once()

def test_create_transit_gateway_multicast_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_multicast_domain
    mock_client = MagicMock()
    mock_client.create_transit_gateway_multicast_domain.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_multicast_domain("test-transit_gateway_id", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_multicast_domain.assert_called_once()

def test_create_transit_gateway_peering_attachment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_peering_attachment
    mock_client = MagicMock()
    mock_client.create_transit_gateway_peering_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_peering_attachment("test-transit_gateway_id", "test-peer_transit_gateway_id", 1, "test-peer_region", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_peering_attachment.assert_called_once()

def test_create_transit_gateway_policy_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_policy_table
    mock_client = MagicMock()
    mock_client.create_transit_gateway_policy_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_policy_table("test-transit_gateway_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_policy_table.assert_called_once()

def test_create_transit_gateway_prefix_list_reference_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_prefix_list_reference
    mock_client = MagicMock()
    mock_client.create_transit_gateway_prefix_list_reference.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.create_transit_gateway_prefix_list_reference.assert_called_once()

def test_create_transit_gateway_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_route
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.create_transit_gateway_route.assert_called_once()

def test_create_transit_gateway_route_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_route_table
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route_table("test-transit_gateway_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_route_table.assert_called_once()

def test_create_transit_gateway_route_table_announcement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_route_table_announcement
    mock_client = MagicMock()
    mock_client.create_transit_gateway_route_table_announcement.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_route_table_announcement("test-transit_gateway_route_table_id", "test-peering_attachment_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_route_table_announcement.assert_called_once()

def test_create_transit_gateway_vpc_attachment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_transit_gateway_vpc_attachment
    mock_client = MagicMock()
    mock_client.create_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_transit_gateway_vpc_attachment("test-transit_gateway_id", "test-vpc_id", "test-subnet_ids", options={}, tag_specifications={}, region_name="us-east-1")
    mock_client.create_transit_gateway_vpc_attachment.assert_called_once()

def test_create_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_verified_access_endpoint
    mock_client = MagicMock()
    mock_client.create_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_endpoint("test-verified_access_group_id", "test-endpoint_type", "test-attachment_type", domain_certificate_arn="test-domain_certificate_arn", application_domain="test-application_domain", endpoint_domain_prefix="test-endpoint_domain_prefix", security_group_ids="test-security_group_ids", load_balancer_options={}, network_interface_options={}, description="test-description", policy_document="test-policy_document", tag_specifications={}, client_token="test-client_token", sse_specification={}, rds_options={}, cidr_options={}, region_name="us-east-1")
    mock_client.create_verified_access_endpoint.assert_called_once()

def test_create_verified_access_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_verified_access_group
    mock_client = MagicMock()
    mock_client.create_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_group("test-verified_access_instance_id", description="test-description", policy_document="test-policy_document", tag_specifications={}, client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.create_verified_access_group.assert_called_once()

def test_create_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_verified_access_instance
    mock_client = MagicMock()
    mock_client.create_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_instance(description="test-description", tag_specifications={}, client_token="test-client_token", fips_enabled="test-fips_enabled", cidr_endpoints_custom_sub_domain="test-cidr_endpoints_custom_sub_domain", region_name="us-east-1")
    mock_client.create_verified_access_instance.assert_called_once()

def test_create_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_verified_access_trust_provider
    mock_client = MagicMock()
    mock_client.create_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_verified_access_trust_provider("test-trust_provider_type", "test-policy_reference_name", user_trust_provider_type="test-user_trust_provider_type", device_trust_provider_type="test-device_trust_provider_type", oidc_options={}, device_options={}, description="test-description", tag_specifications={}, client_token="test-client_token", sse_specification={}, native_application_oidc_options={}, region_name="us-east-1")
    mock_client.create_verified_access_trust_provider.assert_called_once()

def test_create_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_volume
    mock_client = MagicMock()
    mock_client.create_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_volume(availability_zone="test-availability_zone", availability_zone_id="test-availability_zone_id", encrypted=True, iops="test-iops", kms_key_id="test-kms_key_id", outpost_arn="test-outpost_arn", size=1, snapshot_id="test-snapshot_id", volume_type="test-volume_type", tag_specifications={}, multi_attach_enabled=True, throughput="test-throughput", client_token="test-client_token", volume_initialization_rate="test-volume_initialization_rate", operator="test-operator", region_name="us-east-1")
    mock_client.create_volume.assert_called_once()

def test_create_vpc_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc
    mock_client = MagicMock()
    mock_client.create_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc(cidr_block="test-cidr_block", ipv6_pool="test-ipv6_pool", ipv6_cidr_block="test-ipv6_cidr_block", ipv4_ipam_pool_id="test-ipv4_ipam_pool_id", ipv4_netmask_length="test-ipv4_netmask_length", ipv6_ipam_pool_id="test-ipv6_ipam_pool_id", ipv6_netmask_length="test-ipv6_netmask_length", ipv6_cidr_block_network_border_group="test-ipv6_cidr_block_network_border_group", tag_specifications={}, instance_tenancy="test-instance_tenancy", amazon_provided_ipv6_cidr_block="test-amazon_provided_ipv6_cidr_block", region_name="us-east-1")
    mock_client.create_vpc.assert_called_once()

def test_create_vpc_block_public_access_exclusion_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc_block_public_access_exclusion
    mock_client = MagicMock()
    mock_client.create_vpc_block_public_access_exclusion.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_block_public_access_exclusion("test-internet_gateway_exclusion_mode", subnet_id="test-subnet_id", vpc_id="test-vpc_id", tag_specifications={}, region_name="us-east-1")
    mock_client.create_vpc_block_public_access_exclusion.assert_called_once()

def test_create_vpc_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc_endpoint
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint("test-vpc_id", vpc_endpoint_type="test-vpc_endpoint_type", service_name="test-service_name", policy_document="test-policy_document", route_table_ids="test-route_table_ids", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", ip_address_type="test-ip_address_type", dns_options={}, client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", tag_specifications={}, subnet_configurations={}, service_network_arn="test-service_network_arn", resource_configuration_arn={}, service_region="test-service_region", region_name="us-east-1")
    mock_client.create_vpc_endpoint.assert_called_once()

def test_create_vpc_endpoint_connection_notification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc_endpoint_connection_notification
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_connection_notification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint_connection_notification("test-connection_notification_arn", "test-connection_events", service_id="test-service_id", vpc_endpoint_id="test-vpc_endpoint_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_vpc_endpoint_connection_notification.assert_called_once()

def test_create_vpc_endpoint_service_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc_endpoint_service_configuration
    mock_client = MagicMock()
    mock_client.create_vpc_endpoint_service_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_endpoint_service_configuration(acceptance_required="test-acceptance_required", private_dns_name="test-private_dns_name", network_load_balancer_arns="test-network_load_balancer_arns", gateway_load_balancer_arns="test-gateway_load_balancer_arns", supported_ip_address_types=1, supported_regions=1, client_token="test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.create_vpc_endpoint_service_configuration.assert_called_once()

def test_create_vpc_peering_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpc_peering_connection
    mock_client = MagicMock()
    mock_client.create_vpc_peering_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpc_peering_connection("test-vpc_id", peer_region="test-peer_region", tag_specifications={}, peer_vpc_id="test-peer_vpc_id", peer_owner_id="test-peer_owner_id", region_name="us-east-1")
    mock_client.create_vpc_peering_connection.assert_called_once()

def test_create_vpn_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpn_connection
    mock_client = MagicMock()
    mock_client.create_vpn_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpn_connection("test-customer_gateway_id", "test-type_value", vpn_gateway_id="test-vpn_gateway_id", transit_gateway_id="test-transit_gateway_id", tag_specifications={}, pre_shared_key_storage="test-pre_shared_key_storage", options={}, region_name="us-east-1")
    mock_client.create_vpn_connection.assert_called_once()

def test_create_vpn_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import create_vpn_gateway
    mock_client = MagicMock()
    mock_client.create_vpn_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    create_vpn_gateway("test-type_value", availability_zone="test-availability_zone", tag_specifications={}, amazon_side_asn="test-amazon_side_asn", region_name="us-east-1")
    mock_client.create_vpn_gateway.assert_called_once()

def test_delete_client_vpn_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_client_vpn_route
    mock_client = MagicMock()
    mock_client.delete_client_vpn_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_client_vpn_route("test-client_vpn_endpoint_id", "test-destination_cidr_block", target_vpc_subnet_id="test-target_vpc_subnet_id", region_name="us-east-1")
    mock_client.delete_client_vpn_route.assert_called_once()

def test_delete_instance_event_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_instance_event_window
    mock_client = MagicMock()
    mock_client.delete_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_instance_event_window("test-instance_event_window_id", force_delete=True, region_name="us-east-1")
    mock_client.delete_instance_event_window.assert_called_once()

def test_delete_ipam_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_ipam
    mock_client = MagicMock()
    mock_client.delete_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam("test-ipam_id", cascade="test-cascade", region_name="us-east-1")
    mock_client.delete_ipam.assert_called_once()

def test_delete_ipam_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_ipam_pool
    mock_client = MagicMock()
    mock_client.delete_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_ipam_pool("test-ipam_pool_id", cascade="test-cascade", region_name="us-east-1")
    mock_client.delete_ipam_pool.assert_called_once()

def test_delete_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_key_pair
    mock_client = MagicMock()
    mock_client.delete_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_key_pair(key_name="test-key_name", key_pair_id="test-key_pair_id", region_name="us-east-1")
    mock_client.delete_key_pair.assert_called_once()

def test_delete_launch_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_launch_template
    mock_client = MagicMock()
    mock_client.delete_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_launch_template(launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", region_name="us-east-1")
    mock_client.delete_launch_template.assert_called_once()

def test_delete_launch_template_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_launch_template_versions
    mock_client = MagicMock()
    mock_client.delete_launch_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_launch_template_versions("test-versions", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", region_name="us-east-1")
    mock_client.delete_launch_template_versions.assert_called_once()

def test_delete_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_local_gateway_route
    mock_client = MagicMock()
    mock_client.delete_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.delete_local_gateway_route.assert_called_once()

def test_delete_network_interface_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_network_interface_permission
    mock_client = MagicMock()
    mock_client.delete_network_interface_permission.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_network_interface_permission("test-network_interface_permission_id", force=True, region_name="us-east-1")
    mock_client.delete_network_interface_permission.assert_called_once()

def test_delete_public_ipv4_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_public_ipv4_pool
    mock_client = MagicMock()
    mock_client.delete_public_ipv4_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_public_ipv4_pool("test-pool_id", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.delete_public_ipv4_pool.assert_called_once()

def test_delete_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_route
    mock_client = MagicMock()
    mock_client.delete_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", destination_cidr_block="test-destination_cidr_block", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", region_name="us-east-1")
    mock_client.delete_route.assert_called_once()

def test_delete_security_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_security_group
    mock_client = MagicMock()
    mock_client.delete_security_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_security_group(group_id="test-group_id", group_name="test-group_name", region_name="us-east-1")
    mock_client.delete_security_group.assert_called_once()

def test_delete_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_tags
    mock_client = MagicMock()
    mock_client.delete_tags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_tags("test-resources", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.delete_tags.assert_called_once()

def test_delete_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_verified_access_endpoint
    mock_client = MagicMock()
    mock_client.delete_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_endpoint("test-verified_access_endpoint_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_verified_access_endpoint.assert_called_once()

def test_delete_verified_access_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_verified_access_group
    mock_client = MagicMock()
    mock_client.delete_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_group("test-verified_access_group_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_verified_access_group.assert_called_once()

def test_delete_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_verified_access_instance
    mock_client = MagicMock()
    mock_client.delete_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_instance("test-verified_access_instance_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_verified_access_instance.assert_called_once()

def test_delete_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import delete_verified_access_trust_provider
    mock_client = MagicMock()
    mock_client.delete_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    delete_verified_access_trust_provider("test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_verified_access_trust_provider.assert_called_once()

def test_deprovision_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import deprovision_ipam_pool_cidr
    mock_client = MagicMock()
    mock_client.deprovision_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deprovision_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", region_name="us-east-1")
    mock_client.deprovision_ipam_pool_cidr.assert_called_once()

def test_deregister_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import deregister_image
    mock_client = MagicMock()
    mock_client.deregister_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_image("test-image_id", delete_associated_snapshots=True, region_name="us-east-1")
    mock_client.deregister_image.assert_called_once()

def test_deregister_transit_gateway_multicast_group_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import deregister_transit_gateway_multicast_group_members
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_members.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_transit_gateway_multicast_group_members(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", group_ip_address="test-group_ip_address", network_interface_ids="test-network_interface_ids", region_name="us-east-1")
    mock_client.deregister_transit_gateway_multicast_group_members.assert_called_once()

def test_deregister_transit_gateway_multicast_group_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import deregister_transit_gateway_multicast_group_sources
    mock_client = MagicMock()
    mock_client.deregister_transit_gateway_multicast_group_sources.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    deregister_transit_gateway_multicast_group_sources(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", group_ip_address="test-group_ip_address", network_interface_ids="test-network_interface_ids", region_name="us-east-1")
    mock_client.deregister_transit_gateway_multicast_group_sources.assert_called_once()

def test_describe_account_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_account_attributes
    mock_client = MagicMock()
    mock_client.describe_account_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_account_attributes(attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.describe_account_attributes.assert_called_once()

def test_describe_address_transfers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_address_transfers
    mock_client = MagicMock()
    mock_client.describe_address_transfers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_address_transfers(allocation_ids="test-allocation_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_address_transfers.assert_called_once()

def test_describe_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_addresses
    mock_client = MagicMock()
    mock_client.describe_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_addresses(public_ips="test-public_ips", filters=[{}], allocation_ids="test-allocation_ids", region_name="us-east-1")
    mock_client.describe_addresses.assert_called_once()

def test_describe_addresses_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_addresses_attribute
    mock_client = MagicMock()
    mock_client.describe_addresses_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_addresses_attribute(allocation_ids="test-allocation_ids", attribute="test-attribute", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_addresses_attribute.assert_called_once()

def test_describe_availability_zones_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_availability_zones
    mock_client = MagicMock()
    mock_client.describe_availability_zones.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_availability_zones(zone_names="test-zone_names", zone_ids="test-zone_ids", all_availability_zones="test-all_availability_zones", filters=[{}], region_name="us-east-1")
    mock_client.describe_availability_zones.assert_called_once()

def test_describe_aws_network_performance_metric_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_aws_network_performance_metric_subscriptions
    mock_client = MagicMock()
    mock_client.describe_aws_network_performance_metric_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_aws_network_performance_metric_subscriptions(max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_aws_network_performance_metric_subscriptions.assert_called_once()

def test_describe_bundle_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_bundle_tasks
    mock_client = MagicMock()
    mock_client.describe_bundle_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_bundle_tasks(bundle_ids="test-bundle_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_bundle_tasks.assert_called_once()

def test_describe_byoip_cidrs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_byoip_cidrs
    mock_client = MagicMock()
    mock_client.describe_byoip_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_byoip_cidrs(1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_byoip_cidrs.assert_called_once()

def test_describe_capacity_block_extension_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_block_extension_history
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_extension_history(capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_block_extension_history.assert_called_once()

def test_describe_capacity_block_extension_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_block_extension_offerings
    mock_client = MagicMock()
    mock_client.describe_capacity_block_extension_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_extension_offerings(1, "test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_capacity_block_extension_offerings.assert_called_once()

def test_describe_capacity_block_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_block_offerings
    mock_client = MagicMock()
    mock_client.describe_capacity_block_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_offerings(1, instance_type="test-instance_type", instance_count=1, start_date_range="test-start_date_range", end_date_range="test-end_date_range", next_token="test-next_token", max_results=1, ultraserver_type="test-ultraserver_type", ultraserver_count=1, region_name="us-east-1")
    mock_client.describe_capacity_block_offerings.assert_called_once()

def test_describe_capacity_block_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_block_status
    mock_client = MagicMock()
    mock_client.describe_capacity_block_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_block_status(capacity_block_ids="test-capacity_block_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_block_status.assert_called_once()

def test_describe_capacity_blocks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_blocks
    mock_client = MagicMock()
    mock_client.describe_capacity_blocks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_blocks(capacity_block_ids="test-capacity_block_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_blocks.assert_called_once()

def test_describe_capacity_manager_data_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_manager_data_exports
    mock_client = MagicMock()
    mock_client.describe_capacity_manager_data_exports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_manager_data_exports(capacity_manager_data_export_ids=1, max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_manager_data_exports.assert_called_once()

def test_describe_capacity_reservation_billing_requests_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_reservation_billing_requests
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_billing_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_billing_requests("test-role", capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_reservation_billing_requests.assert_called_once()

def test_describe_capacity_reservation_fleets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_reservation_fleets
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_fleets(capacity_reservation_fleet_ids="test-capacity_reservation_fleet_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_reservation_fleets.assert_called_once()

def test_describe_capacity_reservation_topology_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_reservation_topology
    mock_client = MagicMock()
    mock_client.describe_capacity_reservation_topology.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservation_topology(next_token="test-next_token", max_results=1, capacity_reservation_ids="test-capacity_reservation_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_reservation_topology.assert_called_once()

def test_describe_capacity_reservations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_capacity_reservations
    mock_client = MagicMock()
    mock_client.describe_capacity_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_capacity_reservations(capacity_reservation_ids="test-capacity_reservation_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_capacity_reservations.assert_called_once()

def test_describe_carrier_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_carrier_gateways
    mock_client = MagicMock()
    mock_client.describe_carrier_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_carrier_gateways(carrier_gateway_ids="test-carrier_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_carrier_gateways.assert_called_once()

def test_describe_classic_link_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_classic_link_instances
    mock_client = MagicMock()
    mock_client.describe_classic_link_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_classic_link_instances(instance_ids="test-instance_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_classic_link_instances.assert_called_once()

def test_describe_client_vpn_authorization_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_client_vpn_authorization_rules
    mock_client = MagicMock()
    mock_client.describe_client_vpn_authorization_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_authorization_rules("test-client_vpn_endpoint_id", next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.describe_client_vpn_authorization_rules.assert_called_once()

def test_describe_client_vpn_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_client_vpn_connections
    mock_client = MagicMock()
    mock_client.describe_client_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_connections("test-client_vpn_endpoint_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_client_vpn_connections.assert_called_once()

def test_describe_client_vpn_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_client_vpn_endpoints
    mock_client = MagicMock()
    mock_client.describe_client_vpn_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_endpoints(client_vpn_endpoint_ids="test-client_vpn_endpoint_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_client_vpn_endpoints.assert_called_once()

def test_describe_client_vpn_routes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_client_vpn_routes
    mock_client = MagicMock()
    mock_client.describe_client_vpn_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_routes("test-client_vpn_endpoint_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_client_vpn_routes.assert_called_once()

def test_describe_client_vpn_target_networks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_client_vpn_target_networks
    mock_client = MagicMock()
    mock_client.describe_client_vpn_target_networks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_client_vpn_target_networks("test-client_vpn_endpoint_id", association_ids="test-association_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_client_vpn_target_networks.assert_called_once()

def test_describe_coip_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_coip_pools
    mock_client = MagicMock()
    mock_client.describe_coip_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_coip_pools(pool_ids="test-pool_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_coip_pools.assert_called_once()

def test_describe_conversion_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_conversion_tasks
    mock_client = MagicMock()
    mock_client.describe_conversion_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_conversion_tasks(conversion_task_ids="test-conversion_task_ids", region_name="us-east-1")
    mock_client.describe_conversion_tasks.assert_called_once()

def test_describe_customer_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_customer_gateways
    mock_client = MagicMock()
    mock_client.describe_customer_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_customer_gateways(customer_gateway_ids="test-customer_gateway_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_customer_gateways.assert_called_once()

def test_describe_declarative_policies_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_declarative_policies_reports
    mock_client = MagicMock()
    mock_client.describe_declarative_policies_reports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_declarative_policies_reports(next_token="test-next_token", max_results=1, report_ids=1, region_name="us-east-1")
    mock_client.describe_declarative_policies_reports.assert_called_once()

def test_describe_dhcp_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_dhcp_options
    mock_client = MagicMock()
    mock_client.describe_dhcp_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_dhcp_options(dhcp_options_ids={}, next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_dhcp_options.assert_called_once()

def test_describe_egress_only_internet_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_egress_only_internet_gateways
    mock_client = MagicMock()
    mock_client.describe_egress_only_internet_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_egress_only_internet_gateways(egress_only_internet_gateway_ids="test-egress_only_internet_gateway_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_egress_only_internet_gateways.assert_called_once()

def test_describe_elastic_gpus_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_elastic_gpus
    mock_client = MagicMock()
    mock_client.describe_elastic_gpus.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_elastic_gpus(elastic_gpu_ids="test-elastic_gpu_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_elastic_gpus.assert_called_once()

def test_describe_export_image_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_export_image_tasks
    mock_client = MagicMock()
    mock_client.describe_export_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_export_image_tasks(filters=[{}], export_image_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_export_image_tasks.assert_called_once()

def test_describe_export_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_export_tasks
    mock_client = MagicMock()
    mock_client.describe_export_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_export_tasks(filters=[{}], export_task_ids=1, region_name="us-east-1")
    mock_client.describe_export_tasks.assert_called_once()

def test_describe_fast_launch_images_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fast_launch_images
    mock_client = MagicMock()
    mock_client.describe_fast_launch_images.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fast_launch_images(image_ids="test-image_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fast_launch_images.assert_called_once()

def test_describe_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fast_snapshot_restores
    mock_client = MagicMock()
    mock_client.describe_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fast_snapshot_restores(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fast_snapshot_restores.assert_called_once()

def test_describe_fleet_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fleet_history
    mock_client = MagicMock()
    mock_client.describe_fleet_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleet_history("test-fleet_id", "test-start_time", event_type="test-event_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_fleet_history.assert_called_once()

def test_describe_fleet_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fleet_instances
    mock_client = MagicMock()
    mock_client.describe_fleet_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleet_instances("test-fleet_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_fleet_instances.assert_called_once()

def test_describe_fleets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fleets
    mock_client = MagicMock()
    mock_client.describe_fleets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fleets(max_results=1, next_token="test-next_token", fleet_ids="test-fleet_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_fleets.assert_called_once()

def test_describe_flow_logs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_flow_logs
    mock_client = MagicMock()
    mock_client.describe_flow_logs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_flow_logs(filter="test-filter", flow_log_ids="test-flow_log_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_flow_logs.assert_called_once()

def test_describe_fpga_images_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_fpga_images
    mock_client = MagicMock()
    mock_client.describe_fpga_images.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_fpga_images(fpga_image_ids="test-fpga_image_ids", owners="test-owners", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_fpga_images.assert_called_once()

def test_describe_host_reservation_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_host_reservation_offerings
    mock_client = MagicMock()
    mock_client.describe_host_reservation_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_host_reservation_offerings(filter="test-filter", max_duration=1, max_results=1, min_duration=1, next_token="test-next_token", offering_id="test-offering_id", region_name="us-east-1")
    mock_client.describe_host_reservation_offerings.assert_called_once()

def test_describe_host_reservations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_host_reservations
    mock_client = MagicMock()
    mock_client.describe_host_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_host_reservations(filter="test-filter", host_reservation_id_set="test-host_reservation_id_set", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_host_reservations.assert_called_once()

def test_describe_hosts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_hosts
    mock_client = MagicMock()
    mock_client.describe_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_hosts(host_ids="test-host_ids", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.describe_hosts.assert_called_once()

def test_describe_iam_instance_profile_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_iam_instance_profile_associations
    mock_client = MagicMock()
    mock_client.describe_iam_instance_profile_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_iam_instance_profile_associations(association_ids="test-association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_iam_instance_profile_associations.assert_called_once()

def test_describe_id_format_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_id_format
    mock_client = MagicMock()
    mock_client.describe_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_id_format(resource="test-resource", region_name="us-east-1")
    mock_client.describe_id_format.assert_called_once()

def test_describe_identity_id_format_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_identity_id_format
    mock_client = MagicMock()
    mock_client.describe_identity_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_identity_id_format("test-principal_arn", resource="test-resource", region_name="us-east-1")
    mock_client.describe_identity_id_format.assert_called_once()

def test_describe_image_references_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_image_references
    mock_client = MagicMock()
    mock_client.describe_image_references.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_references("test-image_ids", include_all_resource_types=True, resource_types="test-resource_types", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_image_references.assert_called_once()

def test_describe_image_usage_report_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_image_usage_report_entries
    mock_client = MagicMock()
    mock_client.describe_image_usage_report_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_usage_report_entries(image_ids="test-image_ids", report_ids=1, next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.describe_image_usage_report_entries.assert_called_once()

def test_describe_image_usage_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_image_usage_reports
    mock_client = MagicMock()
    mock_client.describe_image_usage_reports.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_image_usage_reports(image_ids="test-image_ids", report_ids=1, next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.describe_image_usage_reports.assert_called_once()

def test_describe_import_image_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_import_image_tasks
    mock_client = MagicMock()
    mock_client.describe_import_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_import_image_tasks(filters=[{}], import_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_import_image_tasks.assert_called_once()

def test_describe_import_snapshot_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_import_snapshot_tasks
    mock_client = MagicMock()
    mock_client.describe_import_snapshot_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_import_snapshot_tasks(filters=[{}], import_task_ids=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_import_snapshot_tasks.assert_called_once()

def test_describe_instance_connect_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_connect_endpoints
    mock_client = MagicMock()
    mock_client.describe_instance_connect_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_connect_endpoints(max_results=1, next_token="test-next_token", filters=[{}], instance_connect_endpoint_ids="test-instance_connect_endpoint_ids", region_name="us-east-1")
    mock_client.describe_instance_connect_endpoints.assert_called_once()

def test_describe_instance_credit_specifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_credit_specifications
    mock_client = MagicMock()
    mock_client.describe_instance_credit_specifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_credit_specifications(filters=[{}], instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_credit_specifications.assert_called_once()

def test_describe_instance_event_windows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_event_windows
    mock_client = MagicMock()
    mock_client.describe_instance_event_windows.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_event_windows(instance_event_window_ids="test-instance_event_window_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_event_windows.assert_called_once()

def test_describe_instance_image_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_image_metadata
    mock_client = MagicMock()
    mock_client.describe_instance_image_metadata.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_image_metadata(filters=[{}], instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_image_metadata.assert_called_once()

def test_describe_instance_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_status
    mock_client = MagicMock()
    mock_client.describe_instance_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_status(instance_ids="test-instance_ids", max_results=1, next_token="test-next_token", filters=[{}], include_all_instances=True, region_name="us-east-1")
    mock_client.describe_instance_status.assert_called_once()

def test_describe_instance_topology_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_topology
    mock_client = MagicMock()
    mock_client.describe_instance_topology.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_topology(next_token="test-next_token", max_results=1, instance_ids="test-instance_ids", group_names="test-group_names", filters=[{}], region_name="us-east-1")
    mock_client.describe_instance_topology.assert_called_once()

def test_describe_instance_type_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_type_offerings
    mock_client = MagicMock()
    mock_client.describe_instance_type_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_type_offerings(location_type="test-location_type", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_type_offerings.assert_called_once()

def test_describe_instance_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_instance_types
    mock_client = MagicMock()
    mock_client.describe_instance_types.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_instance_types(instance_types="test-instance_types", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_types.assert_called_once()

def test_describe_internet_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_internet_gateways
    mock_client = MagicMock()
    mock_client.describe_internet_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_internet_gateways(next_token="test-next_token", max_results=1, internet_gateway_ids="test-internet_gateway_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_internet_gateways.assert_called_once()

def test_describe_ipam_byoasn_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_byoasn
    mock_client = MagicMock()
    mock_client.describe_ipam_byoasn.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_byoasn(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_ipam_byoasn.assert_called_once()

def test_describe_ipam_external_resource_verification_tokens_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_external_resource_verification_tokens
    mock_client = MagicMock()
    mock_client.describe_ipam_external_resource_verification_tokens.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_external_resource_verification_tokens(filters=[{}], next_token="test-next_token", max_results=1, ipam_external_resource_verification_token_ids="test-ipam_external_resource_verification_token_ids", region_name="us-east-1")
    mock_client.describe_ipam_external_resource_verification_tokens.assert_called_once()

def test_describe_ipam_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_pools
    mock_client = MagicMock()
    mock_client.describe_ipam_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_pools(filters=[{}], max_results=1, next_token="test-next_token", ipam_pool_ids="test-ipam_pool_ids", region_name="us-east-1")
    mock_client.describe_ipam_pools.assert_called_once()

def test_describe_ipam_prefix_list_resolver_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_prefix_list_resolver_targets
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolver_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_prefix_list_resolver_targets(filters=[{}], max_results=1, next_token="test-next_token", ipam_prefix_list_resolver_target_ids="test-ipam_prefix_list_resolver_target_ids", ipam_prefix_list_resolver_id="test-ipam_prefix_list_resolver_id", region_name="us-east-1")
    mock_client.describe_ipam_prefix_list_resolver_targets.assert_called_once()

def test_describe_ipam_prefix_list_resolvers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_prefix_list_resolvers
    mock_client = MagicMock()
    mock_client.describe_ipam_prefix_list_resolvers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_prefix_list_resolvers(filters=[{}], max_results=1, next_token="test-next_token", ipam_prefix_list_resolver_ids="test-ipam_prefix_list_resolver_ids", region_name="us-east-1")
    mock_client.describe_ipam_prefix_list_resolvers.assert_called_once()

def test_describe_ipam_resource_discoveries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_resource_discoveries
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discoveries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_resource_discoveries(ipam_resource_discovery_ids="test-ipam_resource_discovery_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_ipam_resource_discoveries.assert_called_once()

def test_describe_ipam_resource_discovery_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_resource_discovery_associations
    mock_client = MagicMock()
    mock_client.describe_ipam_resource_discovery_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_resource_discovery_associations(ipam_resource_discovery_association_ids="test-ipam_resource_discovery_association_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_ipam_resource_discovery_associations.assert_called_once()

def test_describe_ipam_scopes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipam_scopes
    mock_client = MagicMock()
    mock_client.describe_ipam_scopes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipam_scopes(filters=[{}], max_results=1, next_token="test-next_token", ipam_scope_ids="test-ipam_scope_ids", region_name="us-east-1")
    mock_client.describe_ipam_scopes.assert_called_once()

def test_describe_ipams_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipams
    mock_client = MagicMock()
    mock_client.describe_ipams.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipams(filters=[{}], max_results=1, next_token="test-next_token", ipam_ids="test-ipam_ids", region_name="us-east-1")
    mock_client.describe_ipams.assert_called_once()

def test_describe_ipv6_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_ipv6_pools
    mock_client = MagicMock()
    mock_client.describe_ipv6_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_ipv6_pools(pool_ids="test-pool_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_ipv6_pools.assert_called_once()

def test_describe_key_pairs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_key_pairs
    mock_client = MagicMock()
    mock_client.describe_key_pairs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_key_pairs(key_names="test-key_names", key_pair_ids="test-key_pair_ids", include_public_key=True, filters=[{}], region_name="us-east-1")
    mock_client.describe_key_pairs.assert_called_once()

def test_describe_launch_template_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_launch_template_versions
    mock_client = MagicMock()
    mock_client.describe_launch_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_launch_template_versions(launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", versions="test-versions", min_version="test-min_version", max_version=1, next_token="test-next_token", max_results=1, filters=[{}], resolve_alias="test-resolve_alias", region_name="us-east-1")
    mock_client.describe_launch_template_versions.assert_called_once()

def test_describe_launch_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_launch_templates
    mock_client = MagicMock()
    mock_client.describe_launch_templates.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_launch_templates(launch_template_ids="test-launch_template_ids", launch_template_names="test-launch_template_names", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_launch_templates.assert_called_once()

def test_describe_local_gateway_route_table_virtual_interface_group_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateway_route_table_virtual_interface_group_associations
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_virtual_interface_group_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_table_virtual_interface_group_associations(local_gateway_route_table_virtual_interface_group_association_ids="test-local_gateway_route_table_virtual_interface_group_association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateway_route_table_virtual_interface_group_associations.assert_called_once()

def test_describe_local_gateway_route_table_vpc_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateway_route_table_vpc_associations
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_table_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_table_vpc_associations(local_gateway_route_table_vpc_association_ids="test-local_gateway_route_table_vpc_association_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateway_route_table_vpc_associations.assert_called_once()

def test_describe_local_gateway_route_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateway_route_tables
    mock_client = MagicMock()
    mock_client.describe_local_gateway_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_route_tables(local_gateway_route_table_ids="test-local_gateway_route_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateway_route_tables.assert_called_once()

def test_describe_local_gateway_virtual_interface_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateway_virtual_interface_groups
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interface_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_virtual_interface_groups(local_gateway_virtual_interface_group_ids="test-local_gateway_virtual_interface_group_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateway_virtual_interface_groups.assert_called_once()

def test_describe_local_gateway_virtual_interfaces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateway_virtual_interfaces
    mock_client = MagicMock()
    mock_client.describe_local_gateway_virtual_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateway_virtual_interfaces(local_gateway_virtual_interface_ids="test-local_gateway_virtual_interface_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateway_virtual_interfaces.assert_called_once()

def test_describe_local_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_local_gateways
    mock_client = MagicMock()
    mock_client.describe_local_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_local_gateways(local_gateway_ids="test-local_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_local_gateways.assert_called_once()

def test_describe_locked_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_locked_snapshots
    mock_client = MagicMock()
    mock_client.describe_locked_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_locked_snapshots(filters=[{}], max_results=1, next_token="test-next_token", snapshot_ids="test-snapshot_ids", region_name="us-east-1")
    mock_client.describe_locked_snapshots.assert_called_once()

def test_describe_mac_hosts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_mac_hosts
    mock_client = MagicMock()
    mock_client.describe_mac_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_mac_hosts(filters=[{}], host_ids="test-host_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_mac_hosts.assert_called_once()

def test_describe_mac_modification_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_mac_modification_tasks
    mock_client = MagicMock()
    mock_client.describe_mac_modification_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_mac_modification_tasks(filters=[{}], mac_modification_task_ids="test-mac_modification_task_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_mac_modification_tasks.assert_called_once()

def test_describe_managed_prefix_lists_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_managed_prefix_lists
    mock_client = MagicMock()
    mock_client.describe_managed_prefix_lists.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_managed_prefix_lists(filters=[{}], max_results=1, next_token="test-next_token", prefix_list_ids="test-prefix_list_ids", region_name="us-east-1")
    mock_client.describe_managed_prefix_lists.assert_called_once()

def test_describe_moving_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_moving_addresses
    mock_client = MagicMock()
    mock_client.describe_moving_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_moving_addresses(public_ips="test-public_ips", next_token="test-next_token", filters=[{}], max_results=1, region_name="us-east-1")
    mock_client.describe_moving_addresses.assert_called_once()

def test_describe_nat_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_nat_gateways
    mock_client = MagicMock()
    mock_client.describe_nat_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_nat_gateways(filter="test-filter", max_results=1, nat_gateway_ids="test-nat_gateway_ids", next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_nat_gateways.assert_called_once()

def test_describe_network_acls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_acls
    mock_client = MagicMock()
    mock_client.describe_network_acls.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_acls(next_token="test-next_token", max_results=1, network_acl_ids="test-network_acl_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_network_acls.assert_called_once()

def test_describe_network_insights_access_scope_analyses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_insights_access_scope_analyses
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scope_analyses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_access_scope_analyses(network_insights_access_scope_analysis_ids="test-network_insights_access_scope_analysis_ids", network_insights_access_scope_id="test-network_insights_access_scope_id", analysis_start_time_begin="test-analysis_start_time_begin", analysis_start_time_end="test-analysis_start_time_end", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_network_insights_access_scope_analyses.assert_called_once()

def test_describe_network_insights_access_scopes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_insights_access_scopes
    mock_client = MagicMock()
    mock_client.describe_network_insights_access_scopes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_access_scopes(network_insights_access_scope_ids="test-network_insights_access_scope_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_network_insights_access_scopes.assert_called_once()

def test_describe_network_insights_analyses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_insights_analyses
    mock_client = MagicMock()
    mock_client.describe_network_insights_analyses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_analyses(network_insights_analysis_ids="test-network_insights_analysis_ids", network_insights_path_id="test-network_insights_path_id", analysis_start_time="test-analysis_start_time", analysis_end_time="test-analysis_end_time", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_network_insights_analyses.assert_called_once()

def test_describe_network_insights_paths_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_insights_paths
    mock_client = MagicMock()
    mock_client.describe_network_insights_paths.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_insights_paths(network_insights_path_ids="test-network_insights_path_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_network_insights_paths.assert_called_once()

def test_describe_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_interface_attribute
    mock_client = MagicMock()
    mock_client.describe_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interface_attribute("test-network_interface_id", attribute="test-attribute", region_name="us-east-1")
    mock_client.describe_network_interface_attribute.assert_called_once()

def test_describe_network_interface_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_interface_permissions
    mock_client = MagicMock()
    mock_client.describe_network_interface_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interface_permissions(network_interface_permission_ids="test-network_interface_permission_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_network_interface_permissions.assert_called_once()

def test_describe_network_interfaces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_network_interfaces
    mock_client = MagicMock()
    mock_client.describe_network_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_network_interfaces(next_token="test-next_token", max_results=1, network_interface_ids="test-network_interface_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_network_interfaces.assert_called_once()

def test_describe_outpost_lags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_outpost_lags
    mock_client = MagicMock()
    mock_client.describe_outpost_lags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_outpost_lags(outpost_lag_ids="test-outpost_lag_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_outpost_lags.assert_called_once()

def test_describe_placement_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_placement_groups
    mock_client = MagicMock()
    mock_client.describe_placement_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_placement_groups(group_ids="test-group_ids", group_names="test-group_names", filters=[{}], region_name="us-east-1")
    mock_client.describe_placement_groups.assert_called_once()

def test_describe_prefix_lists_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_prefix_lists
    mock_client = MagicMock()
    mock_client.describe_prefix_lists.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_prefix_lists(filters=[{}], max_results=1, next_token="test-next_token", prefix_list_ids="test-prefix_list_ids", region_name="us-east-1")
    mock_client.describe_prefix_lists.assert_called_once()

def test_describe_principal_id_format_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_principal_id_format
    mock_client = MagicMock()
    mock_client.describe_principal_id_format.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_principal_id_format(resources="test-resources", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_principal_id_format.assert_called_once()

def test_describe_public_ipv4_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_public_ipv4_pools
    mock_client = MagicMock()
    mock_client.describe_public_ipv4_pools.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_public_ipv4_pools(pool_ids="test-pool_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_public_ipv4_pools.assert_called_once()

def test_describe_regions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_regions
    mock_client = MagicMock()
    mock_client.describe_regions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_regions(region_names="test-region_names", all_regions="test-all_regions", filters=[{}], region_name="us-east-1")
    mock_client.describe_regions.assert_called_once()

def test_describe_replace_root_volume_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_replace_root_volume_tasks
    mock_client = MagicMock()
    mock_client.describe_replace_root_volume_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_replace_root_volume_tasks(replace_root_volume_task_ids="test-replace_root_volume_task_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_replace_root_volume_tasks.assert_called_once()

def test_describe_reserved_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_reserved_instances
    mock_client = MagicMock()
    mock_client.describe_reserved_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances(offering_class="test-offering_class", reserved_instances_ids="test-reserved_instances_ids", filters=[{}], offering_type="test-offering_type", region_name="us-east-1")
    mock_client.describe_reserved_instances.assert_called_once()

def test_describe_reserved_instances_listings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_reserved_instances_listings
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_listings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_listings(reserved_instances_id="test-reserved_instances_id", reserved_instances_listing_id="test-reserved_instances_listing_id", filters=[{}], region_name="us-east-1")
    mock_client.describe_reserved_instances_listings.assert_called_once()

def test_describe_reserved_instances_modifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_reserved_instances_modifications
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_modifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_modifications(reserved_instances_modification_ids="test-reserved_instances_modification_ids", next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_reserved_instances_modifications.assert_called_once()

def test_describe_reserved_instances_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_reserved_instances_offerings
    mock_client = MagicMock()
    mock_client.describe_reserved_instances_offerings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_reserved_instances_offerings(availability_zone="test-availability_zone", include_marketplace=True, instance_type="test-instance_type", max_duration=1, max_instance_count=1, min_duration=1, offering_class="test-offering_class", product_description="test-product_description", reserved_instances_offering_ids="test-reserved_instances_offering_ids", availability_zone_id="test-availability_zone_id", filters=[{}], instance_tenancy="test-instance_tenancy", offering_type="test-offering_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_reserved_instances_offerings.assert_called_once()

def test_describe_route_server_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_route_server_endpoints
    mock_client = MagicMock()
    mock_client.describe_route_server_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_server_endpoints(route_server_endpoint_ids="test-route_server_endpoint_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_route_server_endpoints.assert_called_once()

def test_describe_route_server_peers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_route_server_peers
    mock_client = MagicMock()
    mock_client.describe_route_server_peers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_server_peers(route_server_peer_ids="test-route_server_peer_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_route_server_peers.assert_called_once()

def test_describe_route_servers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_route_servers
    mock_client = MagicMock()
    mock_client.describe_route_servers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_servers(route_server_ids="test-route_server_ids", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_route_servers.assert_called_once()

def test_describe_route_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_route_tables
    mock_client = MagicMock()
    mock_client.describe_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_route_tables(next_token="test-next_token", max_results=1, route_table_ids="test-route_table_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_route_tables.assert_called_once()

def test_describe_scheduled_instance_availability_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_scheduled_instance_availability
    mock_client = MagicMock()
    mock_client.describe_scheduled_instance_availability.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_instance_availability("test-first_slot_start_time_range", "test-recurrence", filters=[{}], max_results=1, max_slot_duration_in_hours=1, min_slot_duration_in_hours=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_scheduled_instance_availability.assert_called_once()

def test_describe_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_scheduled_instances
    mock_client = MagicMock()
    mock_client.describe_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_instances(filters=[{}], max_results=1, next_token="test-next_token", scheduled_instance_ids="test-scheduled_instance_ids", slot_start_time_range="test-slot_start_time_range", region_name="us-east-1")
    mock_client.describe_scheduled_instances.assert_called_once()

def test_describe_security_group_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_security_group_rules
    mock_client = MagicMock()
    mock_client.describe_security_group_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_security_group_rules(filters=[{}], security_group_rule_ids="test-security_group_rule_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_security_group_rules.assert_called_once()

def test_describe_security_group_vpc_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_security_group_vpc_associations
    mock_client = MagicMock()
    mock_client.describe_security_group_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_security_group_vpc_associations(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_security_group_vpc_associations.assert_called_once()

def test_describe_service_link_virtual_interfaces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_service_link_virtual_interfaces
    mock_client = MagicMock()
    mock_client.describe_service_link_virtual_interfaces.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_service_link_virtual_interfaces(service_link_virtual_interface_ids="test-service_link_virtual_interface_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_service_link_virtual_interfaces.assert_called_once()

def test_describe_snapshot_tier_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_snapshot_tier_status
    mock_client = MagicMock()
    mock_client.describe_snapshot_tier_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_tier_status(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_snapshot_tier_status.assert_called_once()

def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_snapshots
    mock_client = MagicMock()
    mock_client.describe_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_snapshots(max_results=1, next_token="test-next_token", owner_ids="test-owner_ids", restorable_by_user_ids="test-restorable_by_user_ids", snapshot_ids="test-snapshot_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_snapshots.assert_called_once()

def test_describe_spot_fleet_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_spot_fleet_instances
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_instances("test-spot_fleet_request_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_spot_fleet_instances.assert_called_once()

def test_describe_spot_fleet_request_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_spot_fleet_request_history
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_request_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_request_history("test-spot_fleet_request_id", "test-start_time", event_type="test-event_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_spot_fleet_request_history.assert_called_once()

def test_describe_spot_fleet_requests_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_spot_fleet_requests
    mock_client = MagicMock()
    mock_client.describe_spot_fleet_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_fleet_requests(spot_fleet_request_ids="test-spot_fleet_request_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_spot_fleet_requests.assert_called_once()

def test_describe_spot_instance_requests_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_spot_instance_requests
    mock_client = MagicMock()
    mock_client.describe_spot_instance_requests.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_instance_requests(next_token="test-next_token", max_results=1, spot_instance_request_ids="test-spot_instance_request_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_spot_instance_requests.assert_called_once()

def test_describe_spot_price_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_spot_price_history
    mock_client = MagicMock()
    mock_client.describe_spot_price_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_spot_price_history(availability_zone_id="test-availability_zone_id", start_time="test-start_time", end_time="test-end_time", instance_types="test-instance_types", product_descriptions="test-product_descriptions", filters=[{}], availability_zone="test-availability_zone", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_spot_price_history.assert_called_once()

def test_describe_stale_security_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_stale_security_groups
    mock_client = MagicMock()
    mock_client.describe_stale_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_stale_security_groups("test-vpc_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_stale_security_groups.assert_called_once()

def test_describe_store_image_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_store_image_tasks
    mock_client = MagicMock()
    mock_client.describe_store_image_tasks.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_store_image_tasks(image_ids="test-image_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_store_image_tasks.assert_called_once()

def test_describe_subnets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_subnets
    mock_client = MagicMock()
    mock_client.describe_subnets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_subnets(filters=[{}], subnet_ids="test-subnet_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_subnets.assert_called_once()

def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_tags
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_tags(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_tags.assert_called_once()

def test_describe_traffic_mirror_filter_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_traffic_mirror_filter_rules
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filter_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_filter_rules(traffic_mirror_filter_rule_ids="test-traffic_mirror_filter_rule_ids", traffic_mirror_filter_id="test-traffic_mirror_filter_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_traffic_mirror_filter_rules.assert_called_once()

def test_describe_traffic_mirror_filters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_traffic_mirror_filters
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_filters.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_filters(traffic_mirror_filter_ids="test-traffic_mirror_filter_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_traffic_mirror_filters.assert_called_once()

def test_describe_traffic_mirror_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_traffic_mirror_sessions
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_sessions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_sessions(traffic_mirror_session_ids="test-traffic_mirror_session_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_traffic_mirror_sessions.assert_called_once()

def test_describe_traffic_mirror_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_traffic_mirror_targets
    mock_client = MagicMock()
    mock_client.describe_traffic_mirror_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_traffic_mirror_targets(traffic_mirror_target_ids="test-traffic_mirror_target_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_traffic_mirror_targets.assert_called_once()

def test_describe_transit_gateway_attachments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_attachments
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_attachments.assert_called_once()

def test_describe_transit_gateway_connect_peers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_connect_peers
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connect_peers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_connect_peers(transit_gateway_connect_peer_ids="test-transit_gateway_connect_peer_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_connect_peers.assert_called_once()

def test_describe_transit_gateway_connects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_connects
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_connects.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_connects(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_connects.assert_called_once()

def test_describe_transit_gateway_multicast_domains_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_multicast_domains
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_multicast_domains.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_multicast_domains(transit_gateway_multicast_domain_ids="test-transit_gateway_multicast_domain_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_multicast_domains.assert_called_once()

def test_describe_transit_gateway_peering_attachments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_peering_attachments
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_peering_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_peering_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_peering_attachments.assert_called_once()

def test_describe_transit_gateway_policy_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_policy_tables
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_policy_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_policy_tables(transit_gateway_policy_table_ids="test-transit_gateway_policy_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_policy_tables.assert_called_once()

def test_describe_transit_gateway_route_table_announcements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_route_table_announcements
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_table_announcements.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_route_table_announcements(transit_gateway_route_table_announcement_ids="test-transit_gateway_route_table_announcement_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_route_table_announcements.assert_called_once()

def test_describe_transit_gateway_route_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_route_tables
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_route_tables.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_route_tables(transit_gateway_route_table_ids="test-transit_gateway_route_table_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_route_tables.assert_called_once()

def test_describe_transit_gateway_vpc_attachments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateway_vpc_attachments
    mock_client = MagicMock()
    mock_client.describe_transit_gateway_vpc_attachments.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateway_vpc_attachments(transit_gateway_attachment_ids="test-transit_gateway_attachment_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateway_vpc_attachments.assert_called_once()

def test_describe_transit_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_transit_gateways
    mock_client = MagicMock()
    mock_client.describe_transit_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_transit_gateways(transit_gateway_ids="test-transit_gateway_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_transit_gateways.assert_called_once()

def test_describe_trunk_interface_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_trunk_interface_associations
    mock_client = MagicMock()
    mock_client.describe_trunk_interface_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_trunk_interface_associations(association_ids="test-association_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_trunk_interface_associations.assert_called_once()

def test_describe_verified_access_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_verified_access_endpoints
    mock_client = MagicMock()
    mock_client.describe_verified_access_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_endpoints(verified_access_endpoint_ids="test-verified_access_endpoint_ids", verified_access_instance_id="test-verified_access_instance_id", verified_access_group_id="test-verified_access_group_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_verified_access_endpoints.assert_called_once()

def test_describe_verified_access_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_verified_access_groups
    mock_client = MagicMock()
    mock_client.describe_verified_access_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_groups(verified_access_group_ids="test-verified_access_group_ids", verified_access_instance_id="test-verified_access_instance_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_verified_access_groups.assert_called_once()

def test_describe_verified_access_instance_logging_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_verified_access_instance_logging_configurations
    mock_client = MagicMock()
    mock_client.describe_verified_access_instance_logging_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_instance_logging_configurations(verified_access_instance_ids="test-verified_access_instance_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_verified_access_instance_logging_configurations.assert_called_once()

def test_describe_verified_access_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_verified_access_instances
    mock_client = MagicMock()
    mock_client.describe_verified_access_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_instances(verified_access_instance_ids="test-verified_access_instance_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_verified_access_instances.assert_called_once()

def test_describe_verified_access_trust_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_verified_access_trust_providers
    mock_client = MagicMock()
    mock_client.describe_verified_access_trust_providers.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_verified_access_trust_providers(verified_access_trust_provider_ids="test-verified_access_trust_provider_ids", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_verified_access_trust_providers.assert_called_once()

def test_describe_volume_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_volume_status
    mock_client = MagicMock()
    mock_client.describe_volume_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volume_status(max_results=1, next_token="test-next_token", volume_ids="test-volume_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_volume_status.assert_called_once()

def test_describe_volumes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_volumes
    mock_client = MagicMock()
    mock_client.describe_volumes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volumes(volume_ids="test-volume_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_volumes.assert_called_once()

def test_describe_volumes_modifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_volumes_modifications
    mock_client = MagicMock()
    mock_client.describe_volumes_modifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_volumes_modifications(volume_ids="test-volume_ids", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_volumes_modifications.assert_called_once()

def test_describe_vpc_block_public_access_exclusions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_block_public_access_exclusions
    mock_client = MagicMock()
    mock_client.describe_vpc_block_public_access_exclusions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_block_public_access_exclusions(filters=[{}], exclusion_ids="test-exclusion_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_vpc_block_public_access_exclusions.assert_called_once()

def test_describe_vpc_classic_link_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_classic_link
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_classic_link(vpc_ids="test-vpc_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_vpc_classic_link.assert_called_once()

def test_describe_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_classic_link_dns_support
    mock_client = MagicMock()
    mock_client.describe_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_classic_link_dns_support(vpc_ids="test-vpc_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_classic_link_dns_support.assert_called_once()

def test_describe_vpc_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_associations
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_associations(vpc_endpoint_ids="test-vpc_endpoint_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_associations.assert_called_once()

def test_describe_vpc_endpoint_connection_notifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_connection_notifications
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connection_notifications.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_connection_notifications(connection_notification_id="test-connection_notification_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_connection_notifications.assert_called_once()

def test_describe_vpc_endpoint_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_connections
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_connections(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_connections.assert_called_once()

def test_describe_vpc_endpoint_service_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_service_configurations
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_service_configurations(service_ids="test-service_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_service_configurations.assert_called_once()

def test_describe_vpc_endpoint_service_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_service_permissions
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_service_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_service_permissions("test-service_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_service_permissions.assert_called_once()

def test_describe_vpc_endpoint_services_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoint_services
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoint_services.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoint_services(service_names="test-service_names", filters=[{}], max_results=1, next_token="test-next_token", service_regions="test-service_regions", region_name="us-east-1")
    mock_client.describe_vpc_endpoint_services.assert_called_once()

def test_describe_vpc_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_endpoints
    mock_client = MagicMock()
    mock_client.describe_vpc_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_endpoints(vpc_endpoint_ids="test-vpc_endpoint_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_vpc_endpoints.assert_called_once()

def test_describe_vpc_peering_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpc_peering_connections
    mock_client = MagicMock()
    mock_client.describe_vpc_peering_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpc_peering_connections(next_token="test-next_token", max_results=1, vpc_peering_connection_ids="test-vpc_peering_connection_ids", filters=[{}], region_name="us-east-1")
    mock_client.describe_vpc_peering_connections.assert_called_once()

def test_describe_vpcs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpcs
    mock_client = MagicMock()
    mock_client.describe_vpcs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpcs(filters=[{}], vpc_ids="test-vpc_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_vpcs.assert_called_once()

def test_describe_vpn_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpn_connections
    mock_client = MagicMock()
    mock_client.describe_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpn_connections(filters=[{}], vpn_connection_ids="test-vpn_connection_ids", region_name="us-east-1")
    mock_client.describe_vpn_connections.assert_called_once()

def test_describe_vpn_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import describe_vpn_gateways
    mock_client = MagicMock()
    mock_client.describe_vpn_gateways.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    describe_vpn_gateways(filters=[{}], vpn_gateway_ids="test-vpn_gateway_ids", region_name="us-east-1")
    mock_client.describe_vpn_gateways.assert_called_once()

def test_detach_network_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import detach_network_interface
    mock_client = MagicMock()
    mock_client.detach_network_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_network_interface("test-attachment_id", force=True, region_name="us-east-1")
    mock_client.detach_network_interface.assert_called_once()

def test_detach_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import detach_verified_access_trust_provider
    mock_client = MagicMock()
    mock_client.detach_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_verified_access_trust_provider("test-verified_access_instance_id", "test-verified_access_trust_provider_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.detach_verified_access_trust_provider.assert_called_once()

def test_detach_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import detach_volume
    mock_client = MagicMock()
    mock_client.detach_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    detach_volume("test-volume_id", device="test-device", force=True, instance_id="test-instance_id", region_name="us-east-1")
    mock_client.detach_volume.assert_called_once()

def test_disable_aws_network_performance_metric_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_aws_network_performance_metric_subscription
    mock_client = MagicMock()
    mock_client.disable_aws_network_performance_metric_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_aws_network_performance_metric_subscription(source="test-source", destination="test-destination", metric="test-metric", statistic="test-statistic", region_name="us-east-1")
    mock_client.disable_aws_network_performance_metric_subscription.assert_called_once()

def test_disable_capacity_manager_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_capacity_manager
    mock_client = MagicMock()
    mock_client.disable_capacity_manager.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_capacity_manager(client_token="test-client_token", region_name="us-east-1")
    mock_client.disable_capacity_manager.assert_called_once()

def test_disable_fast_launch_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_fast_launch
    mock_client = MagicMock()
    mock_client.disable_fast_launch.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_fast_launch("test-image_id", force=True, region_name="us-east-1")
    mock_client.disable_fast_launch.assert_called_once()

def test_disable_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_fast_snapshot_restores
    mock_client = MagicMock()
    mock_client.disable_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_fast_snapshot_restores("test-source_snapshot_ids", availability_zones="test-availability_zones", availability_zone_ids="test-availability_zone_ids", region_name="us-east-1")
    mock_client.disable_fast_snapshot_restores.assert_called_once()

def test_disable_transit_gateway_route_table_propagation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_transit_gateway_route_table_propagation
    mock_client = MagicMock()
    mock_client.disable_transit_gateway_route_table_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", transit_gateway_route_table_announcement_id="test-transit_gateway_route_table_announcement_id", region_name="us-east-1")
    mock_client.disable_transit_gateway_route_table_propagation.assert_called_once()

def test_disable_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disable_vpc_classic_link_dns_support
    mock_client = MagicMock()
    mock_client.disable_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disable_vpc_classic_link_dns_support(vpc_id="test-vpc_id", region_name="us-east-1")
    mock_client.disable_vpc_classic_link_dns_support.assert_called_once()

def test_disassociate_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disassociate_address
    mock_client = MagicMock()
    mock_client.disassociate_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_address(association_id="test-association_id", public_ip="test-public_ip", region_name="us-east-1")
    mock_client.disassociate_address.assert_called_once()

def test_disassociate_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disassociate_nat_gateway_address
    mock_client = MagicMock()
    mock_client.disassociate_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_nat_gateway_address("test-nat_gateway_id", "test-association_ids", max_drain_duration_seconds=1, region_name="us-east-1")
    mock_client.disassociate_nat_gateway_address.assert_called_once()

def test_disassociate_trunk_interface_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import disassociate_trunk_interface
    mock_client = MagicMock()
    mock_client.disassociate_trunk_interface.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    disassociate_trunk_interface("test-association_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_trunk_interface.assert_called_once()

def test_enable_aws_network_performance_metric_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_aws_network_performance_metric_subscription
    mock_client = MagicMock()
    mock_client.enable_aws_network_performance_metric_subscription.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_aws_network_performance_metric_subscription(source="test-source", destination="test-destination", metric="test-metric", statistic="test-statistic", region_name="us-east-1")
    mock_client.enable_aws_network_performance_metric_subscription.assert_called_once()

def test_enable_capacity_manager_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_capacity_manager
    mock_client = MagicMock()
    mock_client.enable_capacity_manager.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_capacity_manager(organizations_access="test-organizations_access", client_token="test-client_token", region_name="us-east-1")
    mock_client.enable_capacity_manager.assert_called_once()

def test_enable_fast_launch_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_fast_launch
    mock_client = MagicMock()
    mock_client.enable_fast_launch.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_fast_launch("test-image_id", resource_type="test-resource_type", snapshot_configuration={}, launch_template="test-launch_template", max_parallel_launches=1, region_name="us-east-1")
    mock_client.enable_fast_launch.assert_called_once()

def test_enable_fast_snapshot_restores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_fast_snapshot_restores
    mock_client = MagicMock()
    mock_client.enable_fast_snapshot_restores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_fast_snapshot_restores("test-source_snapshot_ids", availability_zones="test-availability_zones", availability_zone_ids="test-availability_zone_ids", region_name="us-east-1")
    mock_client.enable_fast_snapshot_restores.assert_called_once()

def test_enable_image_deregistration_protection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_image_deregistration_protection
    mock_client = MagicMock()
    mock_client.enable_image_deregistration_protection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_image_deregistration_protection("test-image_id", with_cooldown="test-with_cooldown", region_name="us-east-1")
    mock_client.enable_image_deregistration_protection.assert_called_once()

def test_enable_transit_gateway_route_table_propagation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_transit_gateway_route_table_propagation
    mock_client = MagicMock()
    mock_client.enable_transit_gateway_route_table_propagation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_transit_gateway_route_table_propagation("test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", transit_gateway_route_table_announcement_id="test-transit_gateway_route_table_announcement_id", region_name="us-east-1")
    mock_client.enable_transit_gateway_route_table_propagation.assert_called_once()

def test_enable_vpc_classic_link_dns_support_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import enable_vpc_classic_link_dns_support
    mock_client = MagicMock()
    mock_client.enable_vpc_classic_link_dns_support.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    enable_vpc_classic_link_dns_support(vpc_id="test-vpc_id", region_name="us-east-1")
    mock_client.enable_vpc_classic_link_dns_support.assert_called_once()

def test_export_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import export_image
    mock_client = MagicMock()
    mock_client.export_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_image("test-disk_image_format", "test-image_id", 1, client_token="test-client_token", description="test-description", role_name="test-role_name", tag_specifications={}, region_name="us-east-1")
    mock_client.export_image.assert_called_once()

def test_export_transit_gateway_routes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import export_transit_gateway_routes
    mock_client = MagicMock()
    mock_client.export_transit_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    export_transit_gateway_routes("test-transit_gateway_route_table_id", "test-s3_bucket", filters=[{}], region_name="us-east-1")
    mock_client.export_transit_gateway_routes.assert_called_once()

def test_get_associated_ipv6_pool_cidrs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_associated_ipv6_pool_cidrs
    mock_client = MagicMock()
    mock_client.get_associated_ipv6_pool_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_associated_ipv6_pool_cidrs("test-pool_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_associated_ipv6_pool_cidrs.assert_called_once()

def test_get_aws_network_performance_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_aws_network_performance_data
    mock_client = MagicMock()
    mock_client.get_aws_network_performance_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_aws_network_performance_data(data_queries="test-data_queries", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_aws_network_performance_data.assert_called_once()

def test_get_capacity_manager_metric_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_capacity_manager_metric_data
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_manager_metric_data("test-metric_names", "test-start_time", "test-end_time", "test-period", group_by="test-group_by", filter_by="test-filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_capacity_manager_metric_data.assert_called_once()

def test_get_capacity_manager_metric_dimensions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_capacity_manager_metric_dimensions
    mock_client = MagicMock()
    mock_client.get_capacity_manager_metric_dimensions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_manager_metric_dimensions("test-group_by", "test-start_time", "test-end_time", "test-metric_names", filter_by="test-filter_by", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_capacity_manager_metric_dimensions.assert_called_once()

def test_get_capacity_reservation_usage_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_capacity_reservation_usage
    mock_client = MagicMock()
    mock_client.get_capacity_reservation_usage.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_capacity_reservation_usage("test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_capacity_reservation_usage.assert_called_once()

def test_get_coip_pool_usage_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_coip_pool_usage
    mock_client = MagicMock()
    mock_client.get_coip_pool_usage.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_coip_pool_usage("test-pool_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_coip_pool_usage.assert_called_once()

def test_get_console_output_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_console_output
    mock_client = MagicMock()
    mock_client.get_console_output.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_console_output("test-instance_id", latest="test-latest", region_name="us-east-1")
    mock_client.get_console_output.assert_called_once()

def test_get_console_screenshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_console_screenshot
    mock_client = MagicMock()
    mock_client.get_console_screenshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_console_screenshot("test-instance_id", wake_up="test-wake_up", region_name="us-east-1")
    mock_client.get_console_screenshot.assert_called_once()

def test_get_groups_for_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_groups_for_capacity_reservation
    mock_client = MagicMock()
    mock_client.get_groups_for_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_groups_for_capacity_reservation("test-capacity_reservation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_groups_for_capacity_reservation.assert_called_once()

def test_get_instance_types_from_instance_requirements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_instance_types_from_instance_requirements
    mock_client = MagicMock()
    mock_client.get_instance_types_from_instance_requirements.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_instance_types_from_instance_requirements("test-architecture_types", "test-virtualization_types", "test-instance_requirements", max_results=1, next_token="test-next_token", context={}, region_name="us-east-1")
    mock_client.get_instance_types_from_instance_requirements.assert_called_once()

def test_get_ipam_address_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_address_history
    mock_client = MagicMock()
    mock_client.get_ipam_address_history.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_address_history("test-cidr", "test-ipam_scope_id", vpc_id="test-vpc_id", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_address_history.assert_called_once()

def test_get_ipam_discovered_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_discovered_accounts
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_accounts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_accounts("test-ipam_resource_discovery_id", "test-discovery_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_ipam_discovered_accounts.assert_called_once()

def test_get_ipam_discovered_public_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_discovered_public_addresses
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_public_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_public_addresses("test-ipam_resource_discovery_id", "test-address_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_ipam_discovered_public_addresses.assert_called_once()

def test_get_ipam_discovered_resource_cidrs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_discovered_resource_cidrs
    mock_client = MagicMock()
    mock_client.get_ipam_discovered_resource_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_discovered_resource_cidrs("test-ipam_resource_discovery_id", "test-resource_region", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_ipam_discovered_resource_cidrs.assert_called_once()

def test_get_ipam_pool_allocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_pool_allocations
    mock_client = MagicMock()
    mock_client.get_ipam_pool_allocations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_pool_allocations("test-ipam_pool_id", ipam_pool_allocation_id="test-ipam_pool_allocation_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_pool_allocations.assert_called_once()

def test_get_ipam_pool_cidrs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_pool_cidrs
    mock_client = MagicMock()
    mock_client.get_ipam_pool_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_pool_cidrs("test-ipam_pool_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_pool_cidrs.assert_called_once()

def test_get_ipam_prefix_list_resolver_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_prefix_list_resolver_rules
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_rules.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_rules("test-ipam_prefix_list_resolver_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_prefix_list_resolver_rules.assert_called_once()

def test_get_ipam_prefix_list_resolver_version_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_prefix_list_resolver_version_entries
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_version_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_version_entries("test-ipam_prefix_list_resolver_id", "test-ipam_prefix_list_resolver_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_prefix_list_resolver_version_entries.assert_called_once()

def test_get_ipam_prefix_list_resolver_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_prefix_list_resolver_versions
    mock_client = MagicMock()
    mock_client.get_ipam_prefix_list_resolver_versions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_prefix_list_resolver_versions("test-ipam_prefix_list_resolver_id", ipam_prefix_list_resolver_versions="test-ipam_prefix_list_resolver_versions", max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ipam_prefix_list_resolver_versions.assert_called_once()

def test_get_ipam_resource_cidrs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_ipam_resource_cidrs
    mock_client = MagicMock()
    mock_client.get_ipam_resource_cidrs.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_ipam_resource_cidrs("test-ipam_scope_id", filters=[{}], max_results=1, next_token="test-next_token", ipam_pool_id="test-ipam_pool_id", resource_id="test-resource_id", resource_type="test-resource_type", resource_tag="test-resource_tag", resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.get_ipam_resource_cidrs.assert_called_once()

def test_get_managed_prefix_list_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_managed_prefix_list_associations
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_managed_prefix_list_associations("test-prefix_list_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_managed_prefix_list_associations.assert_called_once()

def test_get_managed_prefix_list_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_managed_prefix_list_entries
    mock_client = MagicMock()
    mock_client.get_managed_prefix_list_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_managed_prefix_list_entries("test-prefix_list_id", target_version="test-target_version", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_managed_prefix_list_entries.assert_called_once()

def test_get_network_insights_access_scope_analysis_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_network_insights_access_scope_analysis_findings
    mock_client = MagicMock()
    mock_client.get_network_insights_access_scope_analysis_findings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_network_insights_access_scope_analysis_findings("test-network_insights_access_scope_analysis_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_network_insights_access_scope_analysis_findings.assert_called_once()

def test_get_reserved_instances_exchange_quote_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_reserved_instances_exchange_quote
    mock_client = MagicMock()
    mock_client.get_reserved_instances_exchange_quote.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_reserved_instances_exchange_quote("test-reserved_instance_ids", target_configurations={}, region_name="us-east-1")
    mock_client.get_reserved_instances_exchange_quote.assert_called_once()

def test_get_route_server_propagations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_route_server_propagations
    mock_client = MagicMock()
    mock_client.get_route_server_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_route_server_propagations("test-route_server_id", route_table_id="test-route_table_id", region_name="us-east-1")
    mock_client.get_route_server_propagations.assert_called_once()

def test_get_route_server_routing_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_route_server_routing_database
    mock_client = MagicMock()
    mock_client.get_route_server_routing_database.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_route_server_routing_database("test-route_server_id", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.get_route_server_routing_database.assert_called_once()

def test_get_security_groups_for_vpc_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_security_groups_for_vpc
    mock_client = MagicMock()
    mock_client.get_security_groups_for_vpc.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_security_groups_for_vpc("test-vpc_id", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.get_security_groups_for_vpc.assert_called_once()

def test_get_spot_placement_scores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_spot_placement_scores
    mock_client = MagicMock()
    mock_client.get_spot_placement_scores.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_spot_placement_scores("test-target_capacity", instance_types="test-instance_types", target_capacity_unit_type="test-target_capacity_unit_type", single_availability_zone="test-single_availability_zone", region_names="test-region_names", instance_requirements_with_metadata="test-instance_requirements_with_metadata", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_spot_placement_scores.assert_called_once()

def test_get_subnet_cidr_reservations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_subnet_cidr_reservations
    mock_client = MagicMock()
    mock_client.get_subnet_cidr_reservations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_subnet_cidr_reservations("test-subnet_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_subnet_cidr_reservations.assert_called_once()

def test_get_transit_gateway_attachment_propagations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_attachment_propagations
    mock_client = MagicMock()
    mock_client.get_transit_gateway_attachment_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_attachment_propagations("test-transit_gateway_attachment_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_attachment_propagations.assert_called_once()

def test_get_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_multicast_domain_associations
    mock_client = MagicMock()
    mock_client.get_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_multicast_domain_associations("test-transit_gateway_multicast_domain_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_multicast_domain_associations.assert_called_once()

def test_get_transit_gateway_policy_table_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_policy_table_associations
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_policy_table_associations("test-transit_gateway_policy_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_policy_table_associations.assert_called_once()

def test_get_transit_gateway_policy_table_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_policy_table_entries
    mock_client = MagicMock()
    mock_client.get_transit_gateway_policy_table_entries.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_policy_table_entries("test-transit_gateway_policy_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_policy_table_entries.assert_called_once()

def test_get_transit_gateway_prefix_list_references_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_prefix_list_references
    mock_client = MagicMock()
    mock_client.get_transit_gateway_prefix_list_references.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_prefix_list_references("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_prefix_list_references.assert_called_once()

def test_get_transit_gateway_route_table_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_route_table_associations
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_route_table_associations("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_route_table_associations.assert_called_once()

def test_get_transit_gateway_route_table_propagations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_transit_gateway_route_table_propagations
    mock_client = MagicMock()
    mock_client.get_transit_gateway_route_table_propagations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_transit_gateway_route_table_propagations("test-transit_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_transit_gateway_route_table_propagations.assert_called_once()

def test_get_verified_access_endpoint_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_verified_access_endpoint_targets
    mock_client = MagicMock()
    mock_client.get_verified_access_endpoint_targets.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_verified_access_endpoint_targets("test-verified_access_endpoint_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_verified_access_endpoint_targets.assert_called_once()

def test_get_vpn_connection_device_sample_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_vpn_connection_device_sample_configuration
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_sample_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_vpn_connection_device_sample_configuration("test-vpn_connection_id", "test-vpn_connection_device_type_id", internet_key_exchange_version="test-internet_key_exchange_version", sample_type="test-sample_type", region_name="us-east-1")
    mock_client.get_vpn_connection_device_sample_configuration.assert_called_once()

def test_get_vpn_connection_device_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import get_vpn_connection_device_types
    mock_client = MagicMock()
    mock_client.get_vpn_connection_device_types.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    get_vpn_connection_device_types(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_vpn_connection_device_types.assert_called_once()

def test_import_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import import_image
    mock_client = MagicMock()
    mock_client.import_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_image(architecture="test-architecture", client_data="test-client_data", client_token="test-client_token", description="test-description", disk_containers="test-disk_containers", encrypted=True, hypervisor="test-hypervisor", kms_key_id="test-kms_key_id", license_type="test-license_type", platform="test-platform", role_name="test-role_name", license_specifications={}, tag_specifications={}, usage_operation="test-usage_operation", boot_mode="test-boot_mode", region_name="us-east-1")
    mock_client.import_image.assert_called_once()

def test_import_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import import_instance
    mock_client = MagicMock()
    mock_client.import_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_instance("test-platform", description="test-description", launch_specification={}, disk_images="test-disk_images", region_name="us-east-1")
    mock_client.import_instance.assert_called_once()

def test_import_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import import_key_pair
    mock_client = MagicMock()
    mock_client.import_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_key_pair("test-key_name", "test-public_key_material", tag_specifications={}, region_name="us-east-1")
    mock_client.import_key_pair.assert_called_once()

def test_import_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import import_snapshot
    mock_client = MagicMock()
    mock_client.import_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_snapshot(client_data="test-client_data", client_token="test-client_token", description="test-description", disk_container="test-disk_container", encrypted=True, kms_key_id="test-kms_key_id", role_name="test-role_name", tag_specifications={}, region_name="us-east-1")
    mock_client.import_snapshot.assert_called_once()

def test_import_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import import_volume
    mock_client = MagicMock()
    mock_client.import_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    import_volume("test-image", "test-volume", availability_zone_id="test-availability_zone_id", availability_zone="test-availability_zone", description="test-description", region_name="us-east-1")
    mock_client.import_volume.assert_called_once()

def test_list_images_in_recycle_bin_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import list_images_in_recycle_bin
    mock_client = MagicMock()
    mock_client.list_images_in_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    list_images_in_recycle_bin(image_ids="test-image_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_images_in_recycle_bin.assert_called_once()

def test_list_snapshots_in_recycle_bin_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import list_snapshots_in_recycle_bin
    mock_client = MagicMock()
    mock_client.list_snapshots_in_recycle_bin.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    list_snapshots_in_recycle_bin(max_results=1, next_token="test-next_token", snapshot_ids="test-snapshot_ids", region_name="us-east-1")
    mock_client.list_snapshots_in_recycle_bin.assert_called_once()

def test_lock_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import lock_snapshot
    mock_client = MagicMock()
    mock_client.lock_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    lock_snapshot("test-snapshot_id", "test-lock_mode", cool_off_period="test-cool_off_period", lock_duration=1, expiration_date="test-expiration_date", region_name="us-east-1")
    mock_client.lock_snapshot.assert_called_once()

def test_modify_address_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_address_attribute
    mock_client = MagicMock()
    mock_client.modify_address_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_address_attribute("test-allocation_id", domain_name="test-domain_name", region_name="us-east-1")
    mock_client.modify_address_attribute.assert_called_once()

def test_modify_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_capacity_reservation
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation("test-capacity_reservation_id", instance_count=1, end_date="test-end_date", end_date_type="test-end_date_type", accept="test-accept", additional_info="test-additional_info", instance_match_criteria="test-instance_match_criteria", region_name="us-east-1")
    mock_client.modify_capacity_reservation.assert_called_once()

def test_modify_capacity_reservation_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_capacity_reservation_fleet
    mock_client = MagicMock()
    mock_client.modify_capacity_reservation_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_capacity_reservation_fleet("test-capacity_reservation_fleet_id", total_target_capacity="test-total_target_capacity", end_date="test-end_date", remove_end_date="test-remove_end_date", region_name="us-east-1")
    mock_client.modify_capacity_reservation_fleet.assert_called_once()

def test_modify_client_vpn_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_client_vpn_endpoint
    mock_client = MagicMock()
    mock_client.modify_client_vpn_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_client_vpn_endpoint("test-client_vpn_endpoint_id", server_certificate_arn="test-server_certificate_arn", connection_log_options={}, dns_servers="test-dns_servers", vpn_port=1, description="test-description", split_tunnel="test-split_tunnel", security_group_ids="test-security_group_ids", vpc_id="test-vpc_id", self_service_portal=1, client_connect_options={}, session_timeout_hours=1, client_login_banner_options={}, client_route_enforcement_options={}, disconnect_on_session_timeout=1, region_name="us-east-1")
    mock_client.modify_client_vpn_endpoint.assert_called_once()

def test_modify_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_fleet
    mock_client = MagicMock()
    mock_client.modify_fleet.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_fleet("test-fleet_id", excess_capacity_termination_policy="{}", launch_template_configs={}, target_capacity_specification={}, context={}, region_name="us-east-1")
    mock_client.modify_fleet.assert_called_once()

def test_modify_fpga_image_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_fpga_image_attribute
    mock_client = MagicMock()
    mock_client.modify_fpga_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_fpga_image_attribute("test-fpga_image_id", attribute="test-attribute", operation_type="test-operation_type", user_ids="test-user_ids", user_groups="test-user_groups", product_codes="test-product_codes", load_permission="test-load_permission", description="test-description", name="test-name", region_name="us-east-1")
    mock_client.modify_fpga_image_attribute.assert_called_once()

def test_modify_hosts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_hosts
    mock_client = MagicMock()
    mock_client.modify_hosts.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_hosts("test-host_ids", host_recovery="test-host_recovery", instance_type="test-instance_type", instance_family="test-instance_family", host_maintenance="test-host_maintenance", auto_placement=True, region_name="us-east-1")
    mock_client.modify_hosts.assert_called_once()

def test_modify_image_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_image_attribute
    mock_client = MagicMock()
    mock_client.modify_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_image_attribute("test-image_id", attribute="test-attribute", description="test-description", launch_permission="test-launch_permission", operation_type="test-operation_type", product_codes="test-product_codes", user_groups="test-user_groups", user_ids="test-user_ids", value="test-value", organization_arns="test-organization_arns", organizational_unit_arns="test-organizational_unit_arns", imds_support=1, region_name="us-east-1")
    mock_client.modify_image_attribute.assert_called_once()

def test_modify_instance_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_attribute
    mock_client = MagicMock()
    mock_client.modify_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_attribute("test-instance_id", source_dest_check="test-source_dest_check", disable_api_stop=True, attribute="test-attribute", value="test-value", block_device_mappings={}, disable_api_termination=True, instance_type="test-instance_type", kernel="test-kernel", ramdisk="test-ramdisk", user_data="test-user_data", instance_initiated_shutdown_behavior="test-instance_initiated_shutdown_behavior", groups="test-groups", ebs_optimized="test-ebs_optimized", sriov_net_support=1, ena_support=1, region_name="us-east-1")
    mock_client.modify_instance_attribute.assert_called_once()

def test_modify_instance_connect_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_connect_endpoint
    mock_client = MagicMock()
    mock_client.modify_instance_connect_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_connect_endpoint("test-instance_connect_endpoint_id", ip_address_type="test-ip_address_type", security_group_ids="test-security_group_ids", preserve_client_ip="test-preserve_client_ip", region_name="us-east-1")
    mock_client.modify_instance_connect_endpoint.assert_called_once()

def test_modify_instance_credit_specification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_credit_specification
    mock_client = MagicMock()
    mock_client.modify_instance_credit_specification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_credit_specification({}, client_token="test-client_token", region_name="us-east-1")
    mock_client.modify_instance_credit_specification.assert_called_once()

def test_modify_instance_event_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_event_window
    mock_client = MagicMock()
    mock_client.modify_instance_event_window.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_event_window("test-instance_event_window_id", name="test-name", time_ranges="test-time_ranges", cron_expression="test-cron_expression", region_name="us-east-1")
    mock_client.modify_instance_event_window.assert_called_once()

def test_modify_instance_maintenance_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_maintenance_options
    mock_client = MagicMock()
    mock_client.modify_instance_maintenance_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_maintenance_options("test-instance_id", auto_recovery=True, reboot_migration="test-reboot_migration", region_name="us-east-1")
    mock_client.modify_instance_maintenance_options.assert_called_once()

def test_modify_instance_metadata_defaults_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_metadata_defaults
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_defaults.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_metadata_defaults(http_tokens="test-http_tokens", http_put_response_hop_limit=1, http_endpoint="test-http_endpoint", instance_metadata_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.modify_instance_metadata_defaults.assert_called_once()

def test_modify_instance_metadata_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_metadata_options
    mock_client = MagicMock()
    mock_client.modify_instance_metadata_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_metadata_options("test-instance_id", http_tokens="test-http_tokens", http_put_response_hop_limit=1, http_endpoint="test-http_endpoint", http_protocol_ipv6="test-http_protocol_ipv6", instance_metadata_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.modify_instance_metadata_options.assert_called_once()

def test_modify_instance_placement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_instance_placement
    mock_client = MagicMock()
    mock_client.modify_instance_placement.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_instance_placement("test-instance_id", group_name="test-group_name", partition_number="test-partition_number", host_resource_group_arn="test-host_resource_group_arn", group_id="test-group_id", tenancy="test-tenancy", affinity="test-affinity", host_id="test-host_id", region_name="us-east-1")
    mock_client.modify_instance_placement.assert_called_once()

def test_modify_ipam_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam
    mock_client = MagicMock()
    mock_client.modify_ipam.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam("test-ipam_id", description="test-description", add_operating_regions="test-add_operating_regions", remove_operating_regions="test-remove_operating_regions", tier="test-tier", enable_private_gua=True, metered_account=1, region_name="us-east-1")
    mock_client.modify_ipam.assert_called_once()

def test_modify_ipam_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_pool
    mock_client = MagicMock()
    mock_client.modify_ipam_pool.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_pool("test-ipam_pool_id", description="test-description", auto_import=True, allocation_min_netmask_length="test-allocation_min_netmask_length", allocation_max_netmask_length=1, allocation_default_netmask_length="test-allocation_default_netmask_length", clear_allocation_default_netmask_length="test-clear_allocation_default_netmask_length", add_allocation_resource_tags=[{"Key": "k", "Value": "v"}], remove_allocation_resource_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.modify_ipam_pool.assert_called_once()

def test_modify_ipam_prefix_list_resolver_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_prefix_list_resolver
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_prefix_list_resolver("test-ipam_prefix_list_resolver_id", description="test-description", rules="test-rules", region_name="us-east-1")
    mock_client.modify_ipam_prefix_list_resolver.assert_called_once()

def test_modify_ipam_prefix_list_resolver_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_prefix_list_resolver_target
    mock_client = MagicMock()
    mock_client.modify_ipam_prefix_list_resolver_target.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_prefix_list_resolver_target("test-ipam_prefix_list_resolver_target_id", desired_version="test-desired_version", track_latest_version="test-track_latest_version", client_token="test-client_token", region_name="us-east-1")
    mock_client.modify_ipam_prefix_list_resolver_target.assert_called_once()

def test_modify_ipam_resource_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_resource_cidr
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_resource_cidr("test-resource_id", "test-resource_cidr", "test-resource_region", "test-current_ipam_scope_id", "test-monitored", destination_ipam_scope_id="test-destination_ipam_scope_id", region_name="us-east-1")
    mock_client.modify_ipam_resource_cidr.assert_called_once()

def test_modify_ipam_resource_discovery_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_resource_discovery
    mock_client = MagicMock()
    mock_client.modify_ipam_resource_discovery.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_resource_discovery("test-ipam_resource_discovery_id", description="test-description", add_operating_regions="test-add_operating_regions", remove_operating_regions="test-remove_operating_regions", add_organizational_unit_exclusions="test-add_organizational_unit_exclusions", remove_organizational_unit_exclusions="test-remove_organizational_unit_exclusions", region_name="us-east-1")
    mock_client.modify_ipam_resource_discovery.assert_called_once()

def test_modify_ipam_scope_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_ipam_scope
    mock_client = MagicMock()
    mock_client.modify_ipam_scope.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_ipam_scope("test-ipam_scope_id", description="test-description", external_authority_configuration={}, remove_external_authority_configuration={}, region_name="us-east-1")
    mock_client.modify_ipam_scope.assert_called_once()

def test_modify_launch_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_launch_template
    mock_client = MagicMock()
    mock_client.modify_launch_template.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_launch_template(client_token="test-client_token", launch_template_id="test-launch_template_id", launch_template_name="test-launch_template_name", default_version="test-default_version", region_name="us-east-1")
    mock_client.modify_launch_template.assert_called_once()

def test_modify_local_gateway_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_local_gateway_route
    mock_client = MagicMock()
    mock_client.modify_local_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_local_gateway_route("test-local_gateway_route_table_id", destination_cidr_block="test-destination_cidr_block", local_gateway_virtual_interface_group_id="test-local_gateway_virtual_interface_group_id", network_interface_id="test-network_interface_id", destination_prefix_list_id="test-destination_prefix_list_id", region_name="us-east-1")
    mock_client.modify_local_gateway_route.assert_called_once()

def test_modify_managed_prefix_list_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_managed_prefix_list
    mock_client = MagicMock()
    mock_client.modify_managed_prefix_list.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_managed_prefix_list("test-prefix_list_id", current_version="test-current_version", prefix_list_name="test-prefix_list_name", add_entries="test-add_entries", remove_entries="test-remove_entries", max_entries=1, ipam_prefix_list_resolver_sync_enabled="test-ipam_prefix_list_resolver_sync_enabled", region_name="us-east-1")
    mock_client.modify_managed_prefix_list.assert_called_once()

def test_modify_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_network_interface_attribute
    mock_client = MagicMock()
    mock_client.modify_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_network_interface_attribute("test-network_interface_id", ena_srd_specification={}, enable_primary_ipv6=True, connection_tracking_specification={}, associate_public_ip_address="test-associate_public_ip_address", associated_subnet_ids="test-associated_subnet_ids", description="test-description", source_dest_check="test-source_dest_check", groups="test-groups", attachment="test-attachment", region_name="us-east-1")
    mock_client.modify_network_interface_attribute.assert_called_once()

def test_modify_private_dns_name_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_private_dns_name_options
    mock_client = MagicMock()
    mock_client.modify_private_dns_name_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_private_dns_name_options("test-instance_id", private_dns_hostname_type="test-private_dns_hostname_type", enable_resource_name_dns_a_record=True, enable_resource_name_dns_aaaa_record=True, region_name="us-east-1")
    mock_client.modify_private_dns_name_options.assert_called_once()

def test_modify_reserved_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_reserved_instances
    mock_client = MagicMock()
    mock_client.modify_reserved_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_reserved_instances("test-reserved_instances_ids", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.modify_reserved_instances.assert_called_once()

def test_modify_route_server_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_route_server
    mock_client = MagicMock()
    mock_client.modify_route_server.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_route_server("test-route_server_id", persist_routes="test-persist_routes", persist_routes_duration=1, sns_notifications_enabled="test-sns_notifications_enabled", region_name="us-east-1")
    mock_client.modify_route_server.assert_called_once()

def test_modify_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_snapshot_attribute
    mock_client = MagicMock()
    mock_client.modify_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_attribute("test-snapshot_id", attribute="test-attribute", create_volume_permission="test-create_volume_permission", group_names="test-group_names", operation_type="test-operation_type", user_ids="test-user_ids", region_name="us-east-1")
    mock_client.modify_snapshot_attribute.assert_called_once()

def test_modify_snapshot_tier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_snapshot_tier
    mock_client = MagicMock()
    mock_client.modify_snapshot_tier.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_tier("test-snapshot_id", storage_tier="test-storage_tier", region_name="us-east-1")
    mock_client.modify_snapshot_tier.assert_called_once()

def test_modify_spot_fleet_request_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_spot_fleet_request
    mock_client = MagicMock()
    mock_client.modify_spot_fleet_request.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_spot_fleet_request("test-spot_fleet_request_id", launch_template_configs={}, on_demand_target_capacity="test-on_demand_target_capacity", context={}, target_capacity="test-target_capacity", excess_capacity_termination_policy="{}", region_name="us-east-1")
    mock_client.modify_spot_fleet_request.assert_called_once()

def test_modify_subnet_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_subnet_attribute
    mock_client = MagicMock()
    mock_client.modify_subnet_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_subnet_attribute("test-subnet_id", assign_ipv6_address_on_creation="test-assign_ipv6_address_on_creation", map_public_ip_on_launch="test-map_public_ip_on_launch", map_customer_owned_ip_on_launch="test-map_customer_owned_ip_on_launch", customer_owned_ipv4_pool="test-customer_owned_ipv4_pool", enable_dns64=True, private_dns_hostname_type_on_launch="test-private_dns_hostname_type_on_launch", enable_resource_name_dns_a_record_on_launch=True, enable_resource_name_dns_aaaa_record_on_launch=True, enable_lni_at_device_index=True, disable_lni_at_device_index=True, region_name="us-east-1")
    mock_client.modify_subnet_attribute.assert_called_once()

def test_modify_traffic_mirror_filter_network_services_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_traffic_mirror_filter_network_services
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_network_services.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_filter_network_services("test-traffic_mirror_filter_id", add_network_services="test-add_network_services", remove_network_services="test-remove_network_services", region_name="us-east-1")
    mock_client.modify_traffic_mirror_filter_network_services.assert_called_once()

def test_modify_traffic_mirror_filter_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_traffic_mirror_filter_rule
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_filter_rule.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_filter_rule("test-traffic_mirror_filter_rule_id", traffic_direction="test-traffic_direction", rule_number="test-rule_number", rule_action="test-rule_action", destination_port_range=1, source_port_range=1, protocol="test-protocol", destination_cidr_block="test-destination_cidr_block", source_cidr_block="test-source_cidr_block", description="test-description", remove_fields="test-remove_fields", region_name="us-east-1")
    mock_client.modify_traffic_mirror_filter_rule.assert_called_once()

def test_modify_traffic_mirror_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_traffic_mirror_session
    mock_client = MagicMock()
    mock_client.modify_traffic_mirror_session.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_traffic_mirror_session("test-traffic_mirror_session_id", traffic_mirror_target_id="test-traffic_mirror_target_id", traffic_mirror_filter_id="test-traffic_mirror_filter_id", packet_length="test-packet_length", session_number="test-session_number", virtual_network_id="test-virtual_network_id", description="test-description", remove_fields="test-remove_fields", region_name="us-east-1")
    mock_client.modify_traffic_mirror_session.assert_called_once()

def test_modify_transit_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_transit_gateway
    mock_client = MagicMock()
    mock_client.modify_transit_gateway.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway("test-transit_gateway_id", description="test-description", options={}, region_name="us-east-1")
    mock_client.modify_transit_gateway.assert_called_once()

def test_modify_transit_gateway_prefix_list_reference_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_transit_gateway_prefix_list_reference
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_prefix_list_reference.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway_prefix_list_reference("test-transit_gateway_route_table_id", "test-prefix_list_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.modify_transit_gateway_prefix_list_reference.assert_called_once()

def test_modify_transit_gateway_vpc_attachment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_transit_gateway_vpc_attachment
    mock_client = MagicMock()
    mock_client.modify_transit_gateway_vpc_attachment.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_transit_gateway_vpc_attachment("test-transit_gateway_attachment_id", add_subnet_ids="test-add_subnet_ids", remove_subnet_ids="test-remove_subnet_ids", options={}, region_name="us-east-1")
    mock_client.modify_transit_gateway_vpc_attachment.assert_called_once()

def test_modify_verified_access_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_endpoint
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_endpoint("test-verified_access_endpoint_id", verified_access_group_id="test-verified_access_group_id", load_balancer_options={}, network_interface_options={}, description="test-description", client_token="test-client_token", rds_options={}, cidr_options={}, region_name="us-east-1")
    mock_client.modify_verified_access_endpoint.assert_called_once()

def test_modify_verified_access_endpoint_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_endpoint_policy
    mock_client = MagicMock()
    mock_client.modify_verified_access_endpoint_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_endpoint_policy("test-verified_access_endpoint_id", policy_enabled="test-policy_enabled", policy_document="test-policy_document", client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.modify_verified_access_endpoint_policy.assert_called_once()

def test_modify_verified_access_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_group
    mock_client = MagicMock()
    mock_client.modify_verified_access_group.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_group("test-verified_access_group_id", verified_access_instance_id="test-verified_access_instance_id", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.modify_verified_access_group.assert_called_once()

def test_modify_verified_access_group_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_group_policy
    mock_client = MagicMock()
    mock_client.modify_verified_access_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_group_policy("test-verified_access_group_id", policy_enabled="test-policy_enabled", policy_document="test-policy_document", client_token="test-client_token", sse_specification={}, region_name="us-east-1")
    mock_client.modify_verified_access_group_policy.assert_called_once()

def test_modify_verified_access_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_instance
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_instance("test-verified_access_instance_id", description="test-description", client_token="test-client_token", cidr_endpoints_custom_sub_domain="test-cidr_endpoints_custom_sub_domain", region_name="us-east-1")
    mock_client.modify_verified_access_instance.assert_called_once()

def test_modify_verified_access_instance_logging_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_instance_logging_configuration
    mock_client = MagicMock()
    mock_client.modify_verified_access_instance_logging_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_instance_logging_configuration("test-verified_access_instance_id", "test-access_logs", client_token="test-client_token", region_name="us-east-1")
    mock_client.modify_verified_access_instance_logging_configuration.assert_called_once()

def test_modify_verified_access_trust_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_verified_access_trust_provider
    mock_client = MagicMock()
    mock_client.modify_verified_access_trust_provider.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_verified_access_trust_provider("test-verified_access_trust_provider_id", oidc_options={}, device_options={}, description="test-description", client_token="test-client_token", sse_specification={}, native_application_oidc_options={}, region_name="us-east-1")
    mock_client.modify_verified_access_trust_provider.assert_called_once()

def test_modify_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_volume
    mock_client = MagicMock()
    mock_client.modify_volume.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_volume("test-volume_id", size=1, volume_type="test-volume_type", iops="test-iops", throughput="test-throughput", multi_attach_enabled=True, region_name="us-east-1")
    mock_client.modify_volume.assert_called_once()

def test_modify_volume_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_volume_attribute
    mock_client = MagicMock()
    mock_client.modify_volume_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_volume_attribute("test-volume_id", auto_enable_io=True, region_name="us-east-1")
    mock_client.modify_volume_attribute.assert_called_once()

def test_modify_vpc_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_attribute
    mock_client = MagicMock()
    mock_client.modify_vpc_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_attribute("test-vpc_id", enable_dns_hostnames=True, enable_dns_support=True, enable_network_address_usage_metrics=True, region_name="us-east-1")
    mock_client.modify_vpc_attribute.assert_called_once()

def test_modify_vpc_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_endpoint
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint("test-vpc_endpoint_id", reset_policy="{}", policy_document="test-policy_document", add_route_table_ids="test-add_route_table_ids", remove_route_table_ids="test-remove_route_table_ids", add_subnet_ids="test-add_subnet_ids", remove_subnet_ids="test-remove_subnet_ids", add_security_group_ids="test-add_security_group_ids", remove_security_group_ids="test-remove_security_group_ids", ip_address_type="test-ip_address_type", dns_options={}, private_dns_enabled="test-private_dns_enabled", subnet_configurations={}, region_name="us-east-1")
    mock_client.modify_vpc_endpoint.assert_called_once()

def test_modify_vpc_endpoint_connection_notification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_endpoint_connection_notification
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_connection_notification.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_connection_notification("test-connection_notification_id", connection_notification_arn="test-connection_notification_arn", connection_events="test-connection_events", region_name="us-east-1")
    mock_client.modify_vpc_endpoint_connection_notification.assert_called_once()

def test_modify_vpc_endpoint_service_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_endpoint_service_configuration
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_service_configuration("test-service_id", private_dns_name="test-private_dns_name", remove_private_dns_name="test-remove_private_dns_name", acceptance_required="test-acceptance_required", add_network_load_balancer_arns="test-add_network_load_balancer_arns", remove_network_load_balancer_arns="test-remove_network_load_balancer_arns", add_gateway_load_balancer_arns="test-add_gateway_load_balancer_arns", remove_gateway_load_balancer_arns="test-remove_gateway_load_balancer_arns", add_supported_ip_address_types=1, remove_supported_ip_address_types=1, add_supported_regions=1, remove_supported_regions=1, region_name="us-east-1")
    mock_client.modify_vpc_endpoint_service_configuration.assert_called_once()

def test_modify_vpc_endpoint_service_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_endpoint_service_permissions
    mock_client = MagicMock()
    mock_client.modify_vpc_endpoint_service_permissions.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_endpoint_service_permissions("test-service_id", add_allowed_principals="test-add_allowed_principals", remove_allowed_principals="test-remove_allowed_principals", region_name="us-east-1")
    mock_client.modify_vpc_endpoint_service_permissions.assert_called_once()

def test_modify_vpc_peering_connection_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpc_peering_connection_options
    mock_client = MagicMock()
    mock_client.modify_vpc_peering_connection_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpc_peering_connection_options("test-vpc_peering_connection_id", accepter_peering_connection_options={}, requester_peering_connection_options={}, region_name="us-east-1")
    mock_client.modify_vpc_peering_connection_options.assert_called_once()

def test_modify_vpn_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpn_connection
    mock_client = MagicMock()
    mock_client.modify_vpn_connection.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_connection("test-vpn_connection_id", transit_gateway_id="test-transit_gateway_id", customer_gateway_id="test-customer_gateway_id", vpn_gateway_id="test-vpn_gateway_id", region_name="us-east-1")
    mock_client.modify_vpn_connection.assert_called_once()

def test_modify_vpn_connection_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpn_connection_options
    mock_client = MagicMock()
    mock_client.modify_vpn_connection_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_connection_options("test-vpn_connection_id", local_ipv4_network_cidr="test-local_ipv4_network_cidr", remote_ipv4_network_cidr="test-remote_ipv4_network_cidr", local_ipv6_network_cidr="test-local_ipv6_network_cidr", remote_ipv6_network_cidr="test-remote_ipv6_network_cidr", region_name="us-east-1")
    mock_client.modify_vpn_connection_options.assert_called_once()

def test_modify_vpn_tunnel_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import modify_vpn_tunnel_options
    mock_client = MagicMock()
    mock_client.modify_vpn_tunnel_options.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    modify_vpn_tunnel_options("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", {}, skip_tunnel_replacement=True, pre_shared_key_storage="test-pre_shared_key_storage", region_name="us-east-1")
    mock_client.modify_vpn_tunnel_options.assert_called_once()

def test_move_capacity_reservation_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import move_capacity_reservation_instances
    mock_client = MagicMock()
    mock_client.move_capacity_reservation_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    move_capacity_reservation_instances("test-source_capacity_reservation_id", "test-destination_capacity_reservation_id", 1, client_token="test-client_token", region_name="us-east-1")
    mock_client.move_capacity_reservation_instances.assert_called_once()

def test_provision_byoip_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import provision_byoip_cidr
    mock_client = MagicMock()
    mock_client.provision_byoip_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_byoip_cidr("test-cidr", cidr_authorization_context={}, publicly_advertisable="test-publicly_advertisable", description="test-description", pool_tag_specifications={}, multi_region=True, network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.provision_byoip_cidr.assert_called_once()

def test_provision_ipam_pool_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import provision_ipam_pool_cidr
    mock_client = MagicMock()
    mock_client.provision_ipam_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_ipam_pool_cidr("test-ipam_pool_id", cidr="test-cidr", cidr_authorization_context={}, netmask_length="test-netmask_length", client_token="test-client_token", verification_method="test-verification_method", ipam_external_resource_verification_token_id="test-ipam_external_resource_verification_token_id", region_name="us-east-1")
    mock_client.provision_ipam_pool_cidr.assert_called_once()

def test_provision_public_ipv4_pool_cidr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import provision_public_ipv4_pool_cidr
    mock_client = MagicMock()
    mock_client.provision_public_ipv4_pool_cidr.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    provision_public_ipv4_pool_cidr("test-ipam_pool_id", "test-pool_id", "test-netmask_length", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.provision_public_ipv4_pool_cidr.assert_called_once()

def test_purchase_capacity_block_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import purchase_capacity_block
    mock_client = MagicMock()
    mock_client.purchase_capacity_block.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_capacity_block("test-capacity_block_offering_id", "test-instance_platform", tag_specifications={}, region_name="us-east-1")
    mock_client.purchase_capacity_block.assert_called_once()

def test_purchase_host_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import purchase_host_reservation
    mock_client = MagicMock()
    mock_client.purchase_host_reservation.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_host_reservation("test-host_id_set", "test-offering_id", client_token="test-client_token", currency_code="test-currency_code", limit_price=1, tag_specifications={}, region_name="us-east-1")
    mock_client.purchase_host_reservation.assert_called_once()

def test_purchase_reserved_instances_offering_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import purchase_reserved_instances_offering
    mock_client = MagicMock()
    mock_client.purchase_reserved_instances_offering.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_instances_offering(1, "test-reserved_instances_offering_id", purchase_time="test-purchase_time", limit_price=1, region_name="us-east-1")
    mock_client.purchase_reserved_instances_offering.assert_called_once()

def test_purchase_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import purchase_scheduled_instances
    mock_client = MagicMock()
    mock_client.purchase_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    purchase_scheduled_instances("test-purchase_requests", client_token="test-client_token", region_name="us-east-1")
    mock_client.purchase_scheduled_instances.assert_called_once()

def test_register_image_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import register_image
    mock_client = MagicMock()
    mock_client.register_image.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_image("test-name", image_location="test-image_location", billing_products="test-billing_products", boot_mode="test-boot_mode", tpm_support=1, uefi_data="test-uefi_data", imds_support=1, tag_specifications={}, description="test-description", architecture="test-architecture", kernel_id="test-kernel_id", ramdisk_id="test-ramdisk_id", root_device_name="test-root_device_name", block_device_mappings={}, virtualization_type="test-virtualization_type", sriov_net_support=1, ena_support=1, region_name="us-east-1")
    mock_client.register_image.assert_called_once()

def test_register_transit_gateway_multicast_group_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import register_transit_gateway_multicast_group_members
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_members.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_transit_gateway_multicast_group_members("test-transit_gateway_multicast_domain_id", "test-network_interface_ids", group_ip_address="test-group_ip_address", region_name="us-east-1")
    mock_client.register_transit_gateway_multicast_group_members.assert_called_once()

def test_register_transit_gateway_multicast_group_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import register_transit_gateway_multicast_group_sources
    mock_client = MagicMock()
    mock_client.register_transit_gateway_multicast_group_sources.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    register_transit_gateway_multicast_group_sources("test-transit_gateway_multicast_domain_id", "test-network_interface_ids", group_ip_address="test-group_ip_address", region_name="us-east-1")
    mock_client.register_transit_gateway_multicast_group_sources.assert_called_once()

def test_reject_transit_gateway_multicast_domain_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import reject_transit_gateway_multicast_domain_associations
    mock_client = MagicMock()
    mock_client.reject_transit_gateway_multicast_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reject_transit_gateway_multicast_domain_associations(transit_gateway_multicast_domain_id="test-transit_gateway_multicast_domain_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.reject_transit_gateway_multicast_domain_associations.assert_called_once()

def test_release_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import release_address
    mock_client = MagicMock()
    mock_client.release_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    release_address(allocation_id="test-allocation_id", public_ip="test-public_ip", network_border_group="test-network_border_group", region_name="us-east-1")
    mock_client.release_address.assert_called_once()

def test_replace_image_criteria_in_allowed_images_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import replace_image_criteria_in_allowed_images_settings
    mock_client = MagicMock()
    mock_client.replace_image_criteria_in_allowed_images_settings.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_image_criteria_in_allowed_images_settings(image_criteria="test-image_criteria", region_name="us-east-1")
    mock_client.replace_image_criteria_in_allowed_images_settings.assert_called_once()

def test_replace_network_acl_entry_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import replace_network_acl_entry
    mock_client = MagicMock()
    mock_client.replace_network_acl_entry.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_network_acl_entry("test-network_acl_id", "test-rule_number", "test-protocol", "test-rule_action", "test-egress", cidr_block="test-cidr_block", ipv6_cidr_block="test-ipv6_cidr_block", icmp_type_code="test-icmp_type_code", port_range=1, region_name="us-east-1")
    mock_client.replace_network_acl_entry.assert_called_once()

def test_replace_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import replace_route
    mock_client = MagicMock()
    mock_client.replace_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_route("test-route_table_id", destination_prefix_list_id="test-destination_prefix_list_id", vpc_endpoint_id="test-vpc_endpoint_id", local_target="test-local_target", transit_gateway_id="test-transit_gateway_id", local_gateway_id="test-local_gateway_id", carrier_gateway_id="test-carrier_gateway_id", core_network_arn="test-core_network_arn", odb_network_arn="test-odb_network_arn", destination_cidr_block="test-destination_cidr_block", gateway_id="test-gateway_id", destination_ipv6_cidr_block="test-destination_ipv6_cidr_block", egress_only_internet_gateway_id="test-egress_only_internet_gateway_id", instance_id="test-instance_id", network_interface_id="test-network_interface_id", vpc_peering_connection_id="test-vpc_peering_connection_id", nat_gateway_id="test-nat_gateway_id", region_name="us-east-1")
    mock_client.replace_route.assert_called_once()

def test_replace_transit_gateway_route_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import replace_transit_gateway_route
    mock_client = MagicMock()
    mock_client.replace_transit_gateway_route.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_transit_gateway_route("test-destination_cidr_block", "test-transit_gateway_route_table_id", transit_gateway_attachment_id="test-transit_gateway_attachment_id", blackhole="test-blackhole", region_name="us-east-1")
    mock_client.replace_transit_gateway_route.assert_called_once()

def test_replace_vpn_tunnel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import replace_vpn_tunnel
    mock_client = MagicMock()
    mock_client.replace_vpn_tunnel.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    replace_vpn_tunnel("test-vpn_connection_id", "test-vpn_tunnel_outside_ip_address", apply_pending_maintenance=True, region_name="us-east-1")
    mock_client.replace_vpn_tunnel.assert_called_once()

def test_report_instance_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import report_instance_status
    mock_client = MagicMock()
    mock_client.report_instance_status.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    report_instance_status("test-instances", "test-status", "test-reason_codes", start_time="test-start_time", end_time="test-end_time", description="test-description", region_name="us-east-1")
    mock_client.report_instance_status.assert_called_once()

def test_request_spot_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import request_spot_instances
    mock_client = MagicMock()
    mock_client.request_spot_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    request_spot_instances(launch_specification={}, tag_specifications={}, instance_interruption_behavior="test-instance_interruption_behavior", spot_price="test-spot_price", client_token="test-client_token", instance_count=1, type_value="test-type_value", valid_from="test-valid_from", valid_until="test-valid_until", launch_group="test-launch_group", availability_zone_group="test-availability_zone_group", block_duration_minutes=1, region_name="us-east-1")
    mock_client.request_spot_instances.assert_called_once()

def test_reset_fpga_image_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import reset_fpga_image_attribute
    mock_client = MagicMock()
    mock_client.reset_fpga_image_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_fpga_image_attribute("test-fpga_image_id", attribute="test-attribute", region_name="us-east-1")
    mock_client.reset_fpga_image_attribute.assert_called_once()

def test_reset_network_interface_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import reset_network_interface_attribute
    mock_client = MagicMock()
    mock_client.reset_network_interface_attribute.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    reset_network_interface_attribute("test-network_interface_id", source_dest_check="test-source_dest_check", region_name="us-east-1")
    mock_client.reset_network_interface_attribute.assert_called_once()

def test_restore_snapshot_tier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import restore_snapshot_tier
    mock_client = MagicMock()
    mock_client.restore_snapshot_tier.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    restore_snapshot_tier("test-snapshot_id", temporary_restore_days="test-temporary_restore_days", permanent_restore="test-permanent_restore", region_name="us-east-1")
    mock_client.restore_snapshot_tier.assert_called_once()

def test_revoke_client_vpn_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import revoke_client_vpn_ingress
    mock_client = MagicMock()
    mock_client.revoke_client_vpn_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_client_vpn_ingress("test-client_vpn_endpoint_id", "test-target_network_cidr", access_group_id="test-access_group_id", revoke_all_groups="test-revoke_all_groups", region_name="us-east-1")
    mock_client.revoke_client_vpn_ingress.assert_called_once()

def test_revoke_security_group_egress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import revoke_security_group_egress
    mock_client = MagicMock()
    mock_client.revoke_security_group_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_security_group_egress("test-group_id", security_group_rule_ids="test-security_group_rule_ids", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", ip_protocol="test-ip_protocol", from_port=1, to_port=1, cidr_ip="test-cidr_ip", ip_permissions="test-ip_permissions", region_name="us-east-1")
    mock_client.revoke_security_group_egress.assert_called_once()

def test_revoke_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import revoke_security_group_ingress
    mock_client = MagicMock()
    mock_client.revoke_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    revoke_security_group_ingress(cidr_ip="test-cidr_ip", from_port=1, group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", ip_protocol="test-ip_protocol", source_security_group_name="test-source_security_group_name", source_security_group_owner_id="test-source_security_group_owner_id", to_port=1, security_group_rule_ids="test-security_group_rule_ids", region_name="us-east-1")
    mock_client.revoke_security_group_ingress.assert_called_once()

def test_run_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import run_instances
    mock_client = MagicMock()
    mock_client.run_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    run_instances(1, 1, block_device_mappings={}, image_id="test-image_id", instance_type="test-instance_type", ipv6_address_count=1, ipv6_addresses="test-ipv6_addresses", kernel_id="test-kernel_id", key_name="test-key_name", monitoring="test-monitoring", placement="test-placement", ramdisk_id="test-ramdisk_id", security_group_ids="test-security_group_ids", security_groups="test-security_groups", subnet_id="test-subnet_id", user_data="test-user_data", elastic_gpu_specification={}, elastic_inference_accelerators="test-elastic_inference_accelerators", tag_specifications={}, launch_template="test-launch_template", instance_market_options={}, credit_specification={}, cpu_options={}, capacity_reservation_specification={}, hibernation_options={}, license_specifications={}, metadata_options={}, enclave_options={}, private_dns_name_options={}, maintenance_options={}, disable_api_stop=True, enable_primary_ipv6=True, network_performance_options={}, operator="test-operator", disable_api_termination=True, instance_initiated_shutdown_behavior="test-instance_initiated_shutdown_behavior", private_ip_address="test-private_ip_address", client_token="test-client_token", additional_info="test-additional_info", network_interfaces="test-network_interfaces", iam_instance_profile="test-iam_instance_profile", ebs_optimized="test-ebs_optimized", region_name="us-east-1")
    mock_client.run_instances.assert_called_once()

def test_run_scheduled_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import run_scheduled_instances
    mock_client = MagicMock()
    mock_client.run_scheduled_instances.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    run_scheduled_instances({}, "test-scheduled_instance_id", client_token="test-client_token", instance_count=1, region_name="us-east-1")
    mock_client.run_scheduled_instances.assert_called_once()

def test_search_local_gateway_routes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import search_local_gateway_routes
    mock_client = MagicMock()
    mock_client.search_local_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_local_gateway_routes("test-local_gateway_route_table_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.search_local_gateway_routes.assert_called_once()

def test_search_transit_gateway_multicast_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import search_transit_gateway_multicast_groups
    mock_client = MagicMock()
    mock_client.search_transit_gateway_multicast_groups.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_transit_gateway_multicast_groups("test-transit_gateway_multicast_domain_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.search_transit_gateway_multicast_groups.assert_called_once()

def test_search_transit_gateway_routes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import search_transit_gateway_routes
    mock_client = MagicMock()
    mock_client.search_transit_gateway_routes.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    search_transit_gateway_routes("test-transit_gateway_route_table_id", [{}], max_results=1, region_name="us-east-1")
    mock_client.search_transit_gateway_routes.assert_called_once()

def test_start_declarative_policies_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import start_declarative_policies_report
    mock_client = MagicMock()
    mock_client.start_declarative_policies_report.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_declarative_policies_report("test-s3_bucket", "test-target_id", s3_prefix="test-s3_prefix", tag_specifications={}, region_name="us-east-1")
    mock_client.start_declarative_policies_report.assert_called_once()

def test_start_network_insights_access_scope_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import start_network_insights_access_scope_analysis
    mock_client = MagicMock()
    mock_client.start_network_insights_access_scope_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_network_insights_access_scope_analysis("test-network_insights_access_scope_id", "test-client_token", tag_specifications={}, region_name="us-east-1")
    mock_client.start_network_insights_access_scope_analysis.assert_called_once()

def test_start_network_insights_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import start_network_insights_analysis
    mock_client = MagicMock()
    mock_client.start_network_insights_analysis.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    start_network_insights_analysis("test-network_insights_path_id", "test-client_token", additional_accounts=1, filter_in_arns="test-filter_in_arns", filter_out_arns="test-filter_out_arns", tag_specifications={}, region_name="us-east-1")
    mock_client.start_network_insights_analysis.assert_called_once()

def test_terminate_client_vpn_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import terminate_client_vpn_connections
    mock_client = MagicMock()
    mock_client.terminate_client_vpn_connections.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    terminate_client_vpn_connections("test-client_vpn_endpoint_id", connection_id="test-connection_id", username="test-username", region_name="us-east-1")
    mock_client.terminate_client_vpn_connections.assert_called_once()

def test_unassign_ipv6_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import unassign_ipv6_addresses
    mock_client = MagicMock()
    mock_client.unassign_ipv6_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_ipv6_addresses("test-network_interface_id", ipv6_prefixes="test-ipv6_prefixes", ipv6_addresses="test-ipv6_addresses", region_name="us-east-1")
    mock_client.unassign_ipv6_addresses.assert_called_once()

def test_unassign_private_ip_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import unassign_private_ip_addresses
    mock_client = MagicMock()
    mock_client.unassign_private_ip_addresses.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_private_ip_addresses("test-network_interface_id", ipv4_prefixes="test-ipv4_prefixes", private_ip_addresses="test-private_ip_addresses", region_name="us-east-1")
    mock_client.unassign_private_ip_addresses.assert_called_once()

def test_unassign_private_nat_gateway_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import unassign_private_nat_gateway_address
    mock_client = MagicMock()
    mock_client.unassign_private_nat_gateway_address.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    unassign_private_nat_gateway_address("test-nat_gateway_id", "test-private_ip_addresses", max_drain_duration_seconds=1, region_name="us-east-1")
    mock_client.unassign_private_nat_gateway_address.assert_called_once()

def test_update_capacity_manager_organizations_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import update_capacity_manager_organizations_access
    mock_client = MagicMock()
    mock_client.update_capacity_manager_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_capacity_manager_organizations_access("test-organizations_access", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_capacity_manager_organizations_access.assert_called_once()

def test_update_security_group_rule_descriptions_egress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import update_security_group_rule_descriptions_egress
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_egress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_security_group_rule_descriptions_egress(group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", security_group_rule_descriptions="test-security_group_rule_descriptions", region_name="us-east-1")
    mock_client.update_security_group_rule_descriptions_egress.assert_called_once()

def test_update_security_group_rule_descriptions_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ec2 import update_security_group_rule_descriptions_ingress
    mock_client = MagicMock()
    mock_client.update_security_group_rule_descriptions_ingress.return_value = {}
    monkeypatch.setattr("aws_util.ec2.get_client", lambda *a, **kw: mock_client)
    update_security_group_rule_descriptions_ingress(group_id="test-group_id", group_name="test-group_name", ip_permissions="test-ip_permissions", security_group_rule_descriptions="test-security_group_rule_descriptions", region_name="us-east-1")
    mock_client.update_security_group_rule_descriptions_ingress.assert_called_once()
