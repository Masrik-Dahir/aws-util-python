"""Native async Lightsail utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.lightsail import (
    AttachCertificateToDistributionResult,
    AttachDiskResult,
    AttachInstancesToLoadBalancerResult,
    AttachLoadBalancerTlsCertificateResult,
    AttachStaticIpResult,
    CloseInstancePublicPortsResult,
    CopySnapshotResult,
    CreateBucketAccessKeyResult,
    CreateBucketResult,
    CreateCertificateResult,
    CreateCloudFormationStackResult,
    CreateContactMethodResult,
    CreateContainerServiceDeploymentResult,
    CreateContainerServiceRegistryLoginResult,
    CreateContainerServiceResult,
    CreateDiskFromSnapshotResult,
    CreateDiskResult,
    CreateDiskSnapshotResult,
    CreateDistributionResult,
    CreateDomainEntryResult,
    CreateDomainResult,
    CreateGuiSessionAccessDetailsResult,
    CreateInstancesFromSnapshotResult,
    CreateKeyPairResult,
    CreateLoadBalancerResult,
    CreateLoadBalancerTlsCertificateResult,
    CreateRelationalDatabaseFromSnapshotResult,
    CreateRelationalDatabaseResult,
    CreateRelationalDatabaseSnapshotResult,
    DatabaseResult,
    DeleteAlarmResult,
    DeleteAutoSnapshotResult,
    DeleteBucketAccessKeyResult,
    DeleteBucketResult,
    DeleteCertificateResult,
    DeleteContactMethodResult,
    DeleteDiskResult,
    DeleteDiskSnapshotResult,
    DeleteDistributionResult,
    DeleteDomainEntryResult,
    DeleteDomainResult,
    DeleteKeyPairResult,
    DeleteKnownHostKeysResult,
    DeleteLoadBalancerResult,
    DeleteLoadBalancerTlsCertificateResult,
    DeleteRelationalDatabaseResult,
    DeleteRelationalDatabaseSnapshotResult,
    DetachCertificateFromDistributionResult,
    DetachDiskResult,
    DetachInstancesFromLoadBalancerResult,
    DetachStaticIpResult,
    DisableAddOnResult,
    DownloadDefaultKeyPairResult,
    EnableAddOnResult,
    ExportSnapshotResult,
    GetActiveNamesResult,
    GetAlarmsResult,
    GetAutoSnapshotsResult,
    GetBlueprintsResult,
    GetBucketAccessKeysResult,
    GetBucketBundlesResult,
    GetBucketMetricDataResult,
    GetBucketsResult,
    GetBundlesResult,
    GetCertificatesResult,
    GetCloudFormationStackRecordsResult,
    GetContactMethodsResult,
    GetContainerApiMetadataResult,
    GetContainerImagesResult,
    GetContainerLogResult,
    GetContainerServiceDeploymentsResult,
    GetContainerServiceMetricDataResult,
    GetContainerServicePowersResult,
    GetContainerServicesResult,
    GetCostEstimateResult,
    GetDiskResult,
    GetDiskSnapshotResult,
    GetDiskSnapshotsResult,
    GetDisksResult,
    GetDistributionBundlesResult,
    GetDistributionLatestCacheResetResult,
    GetDistributionMetricDataResult,
    GetDistributionsResult,
    GetDomainResult,
    GetDomainsResult,
    GetExportSnapshotRecordsResult,
    GetInstanceAccessDetailsResult,
    GetInstanceMetricDataResult,
    GetInstancePortStatesResult,
    GetInstanceSnapshotResult,
    GetInstanceStateResult,
    GetKeyPairResult,
    GetKeyPairsResult,
    GetLoadBalancerMetricDataResult,
    GetLoadBalancerResult,
    GetLoadBalancersResult,
    GetLoadBalancerTlsCertificatesResult,
    GetLoadBalancerTlsPoliciesResult,
    GetOperationResult,
    GetOperationsForResourceResult,
    GetOperationsResult,
    GetRegionsResult,
    GetRelationalDatabaseBlueprintsResult,
    GetRelationalDatabaseBundlesResult,
    GetRelationalDatabaseEventsResult,
    GetRelationalDatabaseLogEventsResult,
    GetRelationalDatabaseLogStreamsResult,
    GetRelationalDatabaseMasterUserPasswordResult,
    GetRelationalDatabaseMetricDataResult,
    GetRelationalDatabaseParametersResult,
    GetRelationalDatabaseResult,
    GetRelationalDatabaseSnapshotResult,
    GetRelationalDatabaseSnapshotsResult,
    GetRelationalDatabasesResult,
    GetSetupHistoryResult,
    GetStaticIpsResult,
    ImportKeyPairResult,
    InstanceResult,
    IsVpcPeeredResult,
    OpenInstancePublicPortsResult,
    PeerVpcResult,
    PutAlarmResult,
    PutInstancePublicPortsResult,
    RebootRelationalDatabaseResult,
    RegisterContainerImageResult,
    ResetDistributionCacheResult,
    RunAlarmResult,
    SendContactMethodVerificationResult,
    SetIpAddressTypeResult,
    SetResourceAccessForBucketResult,
    SetupInstanceHttpsResult,
    SnapshotResult,
    StartGuiSessionResult,
    StartRelationalDatabaseResult,
    StaticIpResult,
    StopGuiSessionResult,
    StopRelationalDatabaseResult,
    TagResourceResult,
    UnpeerVpcResult,
    UntagResourceResult,
    UpdateBucketBundleResult,
    UpdateBucketResult,
    UpdateContainerServiceResult,
    UpdateDistributionBundleResult,
    UpdateDistributionResult,
    UpdateDomainEntryResult,
    UpdateInstanceMetadataOptionsResult,
    UpdateLoadBalancerAttributeResult,
    UpdateRelationalDatabaseParametersResult,
    UpdateRelationalDatabaseResult,
    _parse_database,
    _parse_instance,
    _parse_snapshot,
    _parse_static_ip,
)

__all__ = [
    "AttachCertificateToDistributionResult",
    "AttachDiskResult",
    "AttachInstancesToLoadBalancerResult",
    "AttachLoadBalancerTlsCertificateResult",
    "AttachStaticIpResult",
    "CloseInstancePublicPortsResult",
    "CopySnapshotResult",
    "CreateBucketAccessKeyResult",
    "CreateBucketResult",
    "CreateCertificateResult",
    "CreateCloudFormationStackResult",
    "CreateContactMethodResult",
    "CreateContainerServiceDeploymentResult",
    "CreateContainerServiceRegistryLoginResult",
    "CreateContainerServiceResult",
    "CreateDiskFromSnapshotResult",
    "CreateDiskResult",
    "CreateDiskSnapshotResult",
    "CreateDistributionResult",
    "CreateDomainEntryResult",
    "CreateDomainResult",
    "CreateGuiSessionAccessDetailsResult",
    "CreateInstancesFromSnapshotResult",
    "CreateKeyPairResult",
    "CreateLoadBalancerResult",
    "CreateLoadBalancerTlsCertificateResult",
    "CreateRelationalDatabaseFromSnapshotResult",
    "CreateRelationalDatabaseResult",
    "CreateRelationalDatabaseSnapshotResult",
    "DatabaseResult",
    "DeleteAlarmResult",
    "DeleteAutoSnapshotResult",
    "DeleteBucketAccessKeyResult",
    "DeleteBucketResult",
    "DeleteCertificateResult",
    "DeleteContactMethodResult",
    "DeleteDiskResult",
    "DeleteDiskSnapshotResult",
    "DeleteDistributionResult",
    "DeleteDomainEntryResult",
    "DeleteDomainResult",
    "DeleteKeyPairResult",
    "DeleteKnownHostKeysResult",
    "DeleteLoadBalancerResult",
    "DeleteLoadBalancerTlsCertificateResult",
    "DeleteRelationalDatabaseResult",
    "DeleteRelationalDatabaseSnapshotResult",
    "DetachCertificateFromDistributionResult",
    "DetachDiskResult",
    "DetachInstancesFromLoadBalancerResult",
    "DetachStaticIpResult",
    "DisableAddOnResult",
    "DownloadDefaultKeyPairResult",
    "EnableAddOnResult",
    "ExportSnapshotResult",
    "GetActiveNamesResult",
    "GetAlarmsResult",
    "GetAutoSnapshotsResult",
    "GetBlueprintsResult",
    "GetBucketAccessKeysResult",
    "GetBucketBundlesResult",
    "GetBucketMetricDataResult",
    "GetBucketsResult",
    "GetBundlesResult",
    "GetCertificatesResult",
    "GetCloudFormationStackRecordsResult",
    "GetContactMethodsResult",
    "GetContainerApiMetadataResult",
    "GetContainerImagesResult",
    "GetContainerLogResult",
    "GetContainerServiceDeploymentsResult",
    "GetContainerServiceMetricDataResult",
    "GetContainerServicePowersResult",
    "GetContainerServicesResult",
    "GetCostEstimateResult",
    "GetDiskResult",
    "GetDiskSnapshotResult",
    "GetDiskSnapshotsResult",
    "GetDisksResult",
    "GetDistributionBundlesResult",
    "GetDistributionLatestCacheResetResult",
    "GetDistributionMetricDataResult",
    "GetDistributionsResult",
    "GetDomainResult",
    "GetDomainsResult",
    "GetExportSnapshotRecordsResult",
    "GetInstanceAccessDetailsResult",
    "GetInstanceMetricDataResult",
    "GetInstancePortStatesResult",
    "GetInstanceSnapshotResult",
    "GetInstanceStateResult",
    "GetKeyPairResult",
    "GetKeyPairsResult",
    "GetLoadBalancerMetricDataResult",
    "GetLoadBalancerResult",
    "GetLoadBalancerTlsCertificatesResult",
    "GetLoadBalancerTlsPoliciesResult",
    "GetLoadBalancersResult",
    "GetOperationResult",
    "GetOperationsForResourceResult",
    "GetOperationsResult",
    "GetRegionsResult",
    "GetRelationalDatabaseBlueprintsResult",
    "GetRelationalDatabaseBundlesResult",
    "GetRelationalDatabaseEventsResult",
    "GetRelationalDatabaseLogEventsResult",
    "GetRelationalDatabaseLogStreamsResult",
    "GetRelationalDatabaseMasterUserPasswordResult",
    "GetRelationalDatabaseMetricDataResult",
    "GetRelationalDatabaseParametersResult",
    "GetRelationalDatabaseResult",
    "GetRelationalDatabaseSnapshotResult",
    "GetRelationalDatabaseSnapshotsResult",
    "GetRelationalDatabasesResult",
    "GetSetupHistoryResult",
    "GetStaticIpsResult",
    "ImportKeyPairResult",
    "InstanceResult",
    "IsVpcPeeredResult",
    "OpenInstancePublicPortsResult",
    "PeerVpcResult",
    "PutAlarmResult",
    "PutInstancePublicPortsResult",
    "RebootRelationalDatabaseResult",
    "RegisterContainerImageResult",
    "ResetDistributionCacheResult",
    "RunAlarmResult",
    "SendContactMethodVerificationResult",
    "SetIpAddressTypeResult",
    "SetResourceAccessForBucketResult",
    "SetupInstanceHttpsResult",
    "SnapshotResult",
    "StartGuiSessionResult",
    "StartRelationalDatabaseResult",
    "StaticIpResult",
    "StopGuiSessionResult",
    "StopRelationalDatabaseResult",
    "TagResourceResult",
    "UnpeerVpcResult",
    "UntagResourceResult",
    "UpdateBucketBundleResult",
    "UpdateBucketResult",
    "UpdateContainerServiceResult",
    "UpdateDistributionBundleResult",
    "UpdateDistributionResult",
    "UpdateDomainEntryResult",
    "UpdateInstanceMetadataOptionsResult",
    "UpdateLoadBalancerAttributeResult",
    "UpdateRelationalDatabaseParametersResult",
    "UpdateRelationalDatabaseResult",
    "allocate_static_ip",
    "attach_certificate_to_distribution",
    "attach_disk",
    "attach_instances_to_load_balancer",
    "attach_load_balancer_tls_certificate",
    "attach_static_ip",
    "close_instance_public_ports",
    "copy_snapshot",
    "create_bucket",
    "create_bucket_access_key",
    "create_certificate",
    "create_cloud_formation_stack",
    "create_contact_method",
    "create_container_service",
    "create_container_service_deployment",
    "create_container_service_registry_login",
    "create_database",
    "create_disk",
    "create_disk_from_snapshot",
    "create_disk_snapshot",
    "create_distribution",
    "create_domain",
    "create_domain_entry",
    "create_gui_session_access_details",
    "create_instance_snapshot",
    "create_instances",
    "create_instances_from_snapshot",
    "create_key_pair",
    "create_load_balancer",
    "create_load_balancer_tls_certificate",
    "create_relational_database",
    "create_relational_database_from_snapshot",
    "create_relational_database_snapshot",
    "delete_alarm",
    "delete_auto_snapshot",
    "delete_bucket",
    "delete_bucket_access_key",
    "delete_certificate",
    "delete_contact_method",
    "delete_container_image",
    "delete_container_service",
    "delete_database",
    "delete_disk",
    "delete_disk_snapshot",
    "delete_distribution",
    "delete_domain",
    "delete_domain_entry",
    "delete_instance",
    "delete_instance_snapshot",
    "delete_key_pair",
    "delete_known_host_keys",
    "delete_load_balancer",
    "delete_load_balancer_tls_certificate",
    "delete_relational_database",
    "delete_relational_database_snapshot",
    "detach_certificate_from_distribution",
    "detach_disk",
    "detach_instances_from_load_balancer",
    "detach_static_ip",
    "disable_add_on",
    "download_default_key_pair",
    "enable_add_on",
    "export_snapshot",
    "get_active_names",
    "get_alarms",
    "get_auto_snapshots",
    "get_blueprints",
    "get_bucket_access_keys",
    "get_bucket_bundles",
    "get_bucket_metric_data",
    "get_buckets",
    "get_bundles",
    "get_certificates",
    "get_cloud_formation_stack_records",
    "get_contact_methods",
    "get_container_api_metadata",
    "get_container_images",
    "get_container_log",
    "get_container_service_deployments",
    "get_container_service_metric_data",
    "get_container_service_powers",
    "get_container_services",
    "get_cost_estimate",
    "get_database",
    "get_databases",
    "get_disk",
    "get_disk_snapshot",
    "get_disk_snapshots",
    "get_disks",
    "get_distribution_bundles",
    "get_distribution_latest_cache_reset",
    "get_distribution_metric_data",
    "get_distributions",
    "get_domain",
    "get_domains",
    "get_export_snapshot_records",
    "get_instance",
    "get_instance_access_details",
    "get_instance_metric_data",
    "get_instance_port_states",
    "get_instance_snapshot",
    "get_instance_snapshots",
    "get_instance_state",
    "get_instances",
    "get_key_pair",
    "get_key_pairs",
    "get_load_balancer",
    "get_load_balancer_metric_data",
    "get_load_balancer_tls_certificates",
    "get_load_balancer_tls_policies",
    "get_load_balancers",
    "get_operation",
    "get_operations",
    "get_operations_for_resource",
    "get_regions",
    "get_relational_database",
    "get_relational_database_blueprints",
    "get_relational_database_bundles",
    "get_relational_database_events",
    "get_relational_database_log_events",
    "get_relational_database_log_streams",
    "get_relational_database_master_user_password",
    "get_relational_database_metric_data",
    "get_relational_database_parameters",
    "get_relational_database_snapshot",
    "get_relational_database_snapshots",
    "get_relational_databases",
    "get_setup_history",
    "get_static_ip",
    "get_static_ips",
    "import_key_pair",
    "is_vpc_peered",
    "open_instance_public_ports",
    "peer_vpc",
    "put_alarm",
    "put_instance_public_ports",
    "reboot_instance",
    "reboot_relational_database",
    "register_container_image",
    "release_static_ip",
    "reset_distribution_cache",
    "run_alarm",
    "send_contact_method_verification",
    "set_ip_address_type",
    "set_resource_access_for_bucket",
    "setup_instance_https",
    "start_gui_session",
    "start_instance",
    "start_relational_database",
    "stop_gui_session",
    "stop_instance",
    "stop_relational_database",
    "tag_resource",
    "unpeer_vpc",
    "untag_resource",
    "update_bucket",
    "update_bucket_bundle",
    "update_container_service",
    "update_distribution",
    "update_distribution_bundle",
    "update_domain_entry",
    "update_instance_metadata_options",
    "update_load_balancer_attribute",
    "update_relational_database",
    "update_relational_database_parameters",
]


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


async def create_instances(
    instance_names: list[str],
    *,
    availability_zone: str,
    blueprint_id: str,
    bundle_id: str,
    region_name: str | None = None,
) -> list[InstanceResult]:
    """Create one or more Lightsail instances.

    Args:
        instance_names: Names for the new instances.
        availability_zone: AZ (e.g. ``"us-east-1a"``).
        blueprint_id: OS/app blueprint (e.g. ``"amazon_linux_2"``).
        bundle_id: Instance plan (e.g. ``"nano_2_0"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceResult` for each operation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call(
            "CreateInstances",
            instanceNames=instance_names,
            availabilityZone=availability_zone,
            blueprintId=blueprint_id,
            bundleId=bundle_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "create_instances failed") from exc
    operations = resp.get("operations", [])
    results: list[InstanceResult] = []
    for op in operations:
        results.append(
            InstanceResult(
                name=op.get("resourceName", ""),
                arn="",
                state=op.get("status", ""),
            )
        )
    return results


async def get_instance(
    instance_name: str,
    *,
    region_name: str | None = None,
) -> InstanceResult:
    """Get details for a single Lightsail instance.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Returns:
        An :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("GetInstance", instanceName=instance_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_instance failed for {instance_name!r}") from exc
    return _parse_instance(resp["instance"])


async def get_instances(
    *,
    region_name: str | None = None,
) -> list[InstanceResult]:
    """List all Lightsail instances.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("GetInstances")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_instances failed") from exc
    return [_parse_instance(i) for i in resp.get("instances", [])]


async def delete_instance(
    instance_name: str,
    *,
    force: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete a Lightsail instance.

    Args:
        instance_name: Instance name.
        force: Force-delete even with attached resources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {"instanceName": instance_name}
    if force:
        kwargs["forceDeleteAddOns"] = True
    try:
        await client.call("DeleteInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_instance failed for {instance_name!r}") from exc


async def start_instance(
    instance_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Start a stopped Lightsail instance.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        await client.call("StartInstance", instanceName=instance_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"start_instance failed for {instance_name!r}") from exc


async def stop_instance(
    instance_name: str,
    *,
    force: bool = False,
    region_name: str | None = None,
) -> None:
    """Stop a running Lightsail instance.

    Args:
        instance_name: Instance name.
        force: Force-stop the instance.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {"instanceName": instance_name}
    if force:
        kwargs["force"] = True
    try:
        await client.call("StopInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"stop_instance failed for {instance_name!r}") from exc


async def reboot_instance(
    instance_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Reboot a Lightsail instance.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        await client.call("RebootInstance", instanceName=instance_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"reboot_instance failed for {instance_name!r}") from exc


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def create_instance_snapshot(
    instance_name: str,
    snapshot_name: str,
    *,
    region_name: str | None = None,
) -> SnapshotResult:
    """Create a snapshot of a Lightsail instance.

    Args:
        instance_name: Source instance name.
        snapshot_name: Name for the snapshot.
        region_name: AWS region override.

    Returns:
        A :class:`SnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call(
            "CreateInstanceSnapshot",
            instanceName=instance_name,
            instanceSnapshotName=snapshot_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_instance_snapshot failed for {snapshot_name!r}") from exc
    ops = resp.get("operations", [])
    if ops:
        return SnapshotResult(
            name=snapshot_name,
            state=ops[0].get("status", ""),
            from_instance_name=instance_name,
        )
    return SnapshotResult(name=snapshot_name, from_instance_name=instance_name)


async def get_instance_snapshots(
    *,
    region_name: str | None = None,
) -> list[SnapshotResult]:
    """List all Lightsail instance snapshots.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`SnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("GetInstanceSnapshots")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_instance_snapshots failed") from exc
    return [_parse_snapshot(s) for s in resp.get("instanceSnapshots", [])]


async def delete_instance_snapshot(
    snapshot_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Lightsail instance snapshot.

    Args:
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        await client.call(
            "DeleteInstanceSnapshot",
            instanceSnapshotName=snapshot_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_instance_snapshot failed for {snapshot_name!r}") from exc


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


async def create_database(
    database_name: str,
    *,
    availability_zone: str,
    master_database_name: str,
    master_username: str,
    master_user_password: str,
    blueprint_id: str = "mysql_8_0",
    bundle_id: str = "micro_2_0",
    region_name: str | None = None,
) -> DatabaseResult:
    """Create a Lightsail managed database.

    Args:
        database_name: Database resource name.
        availability_zone: AZ for the database.
        master_database_name: Name of the initial database.
        master_username: Master username.
        master_user_password: Master password.
        blueprint_id: Database engine blueprint.
        bundle_id: Database plan bundle.
        region_name: AWS region override.

    Returns:
        A :class:`DatabaseResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call(
            "CreateRelationalDatabase",
            relationalDatabaseName=database_name,
            availabilityZone=availability_zone,
            relationalDatabaseBlueprintId=blueprint_id,
            relationalDatabaseBundleId=bundle_id,
            masterDatabaseName=master_database_name,
            masterUsername=master_username,
            masterUserPassword=master_user_password,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_database failed for {database_name!r}") from exc
    ops = resp.get("operations", [])
    if ops:
        return DatabaseResult(
            name=database_name,
            state=ops[0].get("status", ""),
            engine=blueprint_id,
            master_username=master_username,
        )
    return DatabaseResult(
        name=database_name,
        engine=blueprint_id,
        master_username=master_username,
    )


async def get_database(
    database_name: str,
    *,
    region_name: str | None = None,
) -> DatabaseResult:
    """Get details for a single Lightsail managed database.

    Args:
        database_name: Database resource name.
        region_name: AWS region override.

    Returns:
        A :class:`DatabaseResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call(
            "GetRelationalDatabase",
            relationalDatabaseName=database_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_database failed for {database_name!r}") from exc
    return _parse_database(resp["relationalDatabase"])


async def get_databases(
    *,
    region_name: str | None = None,
) -> list[DatabaseResult]:
    """List all Lightsail managed databases.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`DatabaseResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("GetRelationalDatabases")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_databases failed") from exc
    return [_parse_database(db) for db in resp.get("relationalDatabases", [])]


async def delete_database(
    database_name: str,
    *,
    skip_final_snapshot: bool = True,
    region_name: str | None = None,
) -> None:
    """Delete a Lightsail managed database.

    Args:
        database_name: Database resource name.
        skip_final_snapshot: Skip the final snapshot on deletion.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        await client.call(
            "DeleteRelationalDatabase",
            relationalDatabaseName=database_name,
            skipFinalSnapshot=skip_final_snapshot,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_database failed for {database_name!r}") from exc


# ---------------------------------------------------------------------------
# Static IP operations
# ---------------------------------------------------------------------------


async def allocate_static_ip(
    static_ip_name: str,
    *,
    region_name: str | None = None,
) -> StaticIpResult:
    """Allocate a Lightsail static IP.

    Args:
        static_ip_name: Name for the static IP.
        region_name: AWS region override.

    Returns:
        A :class:`StaticIpResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("AllocateStaticIp", staticIpName=static_ip_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"allocate_static_ip failed for {static_ip_name!r}") from exc
    ops = resp.get("operations", [])
    if ops:
        return StaticIpResult(
            name=static_ip_name,
            state=ops[0].get("status", ""),
        )
    return StaticIpResult(name=static_ip_name)


async def get_static_ip(
    static_ip_name: str,
    *,
    region_name: str | None = None,
) -> StaticIpResult:
    """Get details for a Lightsail static IP.

    Args:
        static_ip_name: Static IP name.
        region_name: AWS region override.

    Returns:
        A :class:`StaticIpResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        resp = await client.call("GetStaticIp", staticIpName=static_ip_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_static_ip failed for {static_ip_name!r}") from exc
    return _parse_static_ip(resp["staticIp"])


async def release_static_ip(
    static_ip_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Release a Lightsail static IP.

    Args:
        static_ip_name: Static IP name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    try:
        await client.call("ReleaseStaticIp", staticIpName=static_ip_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"release_static_ip failed for {static_ip_name!r}") from exc


async def attach_certificate_to_distribution(
    distribution_name: str,
    certificate_name: str,
    region_name: str | None = None,
) -> AttachCertificateToDistributionResult:
    """Attach certificate to distribution.

    Args:
        distribution_name: Distribution name.
        certificate_name: Certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["distributionName"] = distribution_name
    kwargs["certificateName"] = certificate_name
    try:
        resp = await client.call("AttachCertificateToDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach certificate to distribution") from exc
    return AttachCertificateToDistributionResult(
        operation=resp.get("operation"),
    )


async def attach_disk(
    disk_name: str,
    instance_name: str,
    disk_path: str,
    *,
    auto_mounting: bool | None = None,
    region_name: str | None = None,
) -> AttachDiskResult:
    """Attach disk.

    Args:
        disk_name: Disk name.
        instance_name: Instance name.
        disk_path: Disk path.
        auto_mounting: Auto mounting.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    kwargs["instanceName"] = instance_name
    kwargs["diskPath"] = disk_path
    if auto_mounting is not None:
        kwargs["autoMounting"] = auto_mounting
    try:
        resp = await client.call("AttachDisk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach disk") from exc
    return AttachDiskResult(
        operations=resp.get("operations"),
    )


async def attach_instances_to_load_balancer(
    load_balancer_name: str,
    instance_names: list[str],
    region_name: str | None = None,
) -> AttachInstancesToLoadBalancerResult:
    """Attach instances to load balancer.

    Args:
        load_balancer_name: Load balancer name.
        instance_names: Instance names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["instanceNames"] = instance_names
    try:
        resp = await client.call("AttachInstancesToLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach instances to load balancer") from exc
    return AttachInstancesToLoadBalancerResult(
        operations=resp.get("operations"),
    )


async def attach_load_balancer_tls_certificate(
    load_balancer_name: str,
    certificate_name: str,
    region_name: str | None = None,
) -> AttachLoadBalancerTlsCertificateResult:
    """Attach load balancer tls certificate.

    Args:
        load_balancer_name: Load balancer name.
        certificate_name: Certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["certificateName"] = certificate_name
    try:
        resp = await client.call("AttachLoadBalancerTlsCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach load balancer tls certificate") from exc
    return AttachLoadBalancerTlsCertificateResult(
        operations=resp.get("operations"),
    )


async def attach_static_ip(
    static_ip_name: str,
    instance_name: str,
    region_name: str | None = None,
) -> AttachStaticIpResult:
    """Attach static ip.

    Args:
        static_ip_name: Static ip name.
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["staticIpName"] = static_ip_name
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("AttachStaticIp", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach static ip") from exc
    return AttachStaticIpResult(
        operations=resp.get("operations"),
    )


async def close_instance_public_ports(
    port_info: dict[str, Any],
    instance_name: str,
    region_name: str | None = None,
) -> CloseInstancePublicPortsResult:
    """Close instance public ports.

    Args:
        port_info: Port info.
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portInfo"] = port_info
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("CloseInstancePublicPorts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to close instance public ports") from exc
    return CloseInstancePublicPortsResult(
        operation=resp.get("operation"),
    )


async def copy_snapshot(
    target_snapshot_name: str,
    source_region: str,
    *,
    source_snapshot_name: str | None = None,
    source_resource_name: str | None = None,
    restore_date: str | None = None,
    use_latest_restorable_auto_snapshot: bool | None = None,
    region_name: str | None = None,
) -> CopySnapshotResult:
    """Copy snapshot.

    Args:
        target_snapshot_name: Target snapshot name.
        source_region: Source region.
        source_snapshot_name: Source snapshot name.
        source_resource_name: Source resource name.
        restore_date: Restore date.
        use_latest_restorable_auto_snapshot: Use latest restorable auto snapshot.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetSnapshotName"] = target_snapshot_name
    kwargs["sourceRegion"] = source_region
    if source_snapshot_name is not None:
        kwargs["sourceSnapshotName"] = source_snapshot_name
    if source_resource_name is not None:
        kwargs["sourceResourceName"] = source_resource_name
    if restore_date is not None:
        kwargs["restoreDate"] = restore_date
    if use_latest_restorable_auto_snapshot is not None:
        kwargs["useLatestRestorableAutoSnapshot"] = use_latest_restorable_auto_snapshot
    try:
        resp = await client.call("CopySnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy snapshot") from exc
    return CopySnapshotResult(
        operations=resp.get("operations"),
    )


async def create_bucket(
    bucket_name: str,
    bundle_id: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    enable_object_versioning: bool | None = None,
    region_name: str | None = None,
) -> CreateBucketResult:
    """Create bucket.

    Args:
        bucket_name: Bucket name.
        bundle_id: Bundle id.
        tags: Tags.
        enable_object_versioning: Enable object versioning.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    kwargs["bundleId"] = bundle_id
    if tags is not None:
        kwargs["tags"] = tags
    if enable_object_versioning is not None:
        kwargs["enableObjectVersioning"] = enable_object_versioning
    try:
        resp = await client.call("CreateBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bucket") from exc
    return CreateBucketResult(
        bucket=resp.get("bucket"),
        operations=resp.get("operations"),
    )


async def create_bucket_access_key(
    bucket_name: str,
    region_name: str | None = None,
) -> CreateBucketAccessKeyResult:
    """Create bucket access key.

    Args:
        bucket_name: Bucket name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    try:
        resp = await client.call("CreateBucketAccessKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bucket access key") from exc
    return CreateBucketAccessKeyResult(
        access_key=resp.get("accessKey"),
        operations=resp.get("operations"),
    )


async def create_certificate(
    certificate_name: str,
    domain_name: str,
    *,
    subject_alternative_names: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCertificateResult:
    """Create certificate.

    Args:
        certificate_name: Certificate name.
        domain_name: Domain name.
        subject_alternative_names: Subject alternative names.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateName"] = certificate_name
    kwargs["domainName"] = domain_name
    if subject_alternative_names is not None:
        kwargs["subjectAlternativeNames"] = subject_alternative_names
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create certificate") from exc
    return CreateCertificateResult(
        certificate=resp.get("certificate"),
        operations=resp.get("operations"),
    )


async def create_cloud_formation_stack(
    instances: list[dict[str, Any]],
    region_name: str | None = None,
) -> CreateCloudFormationStackResult:
    """Create cloud formation stack.

    Args:
        instances: Instances.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instances"] = instances
    try:
        resp = await client.call("CreateCloudFormationStack", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cloud formation stack") from exc
    return CreateCloudFormationStackResult(
        operations=resp.get("operations"),
    )


async def create_contact_method(
    protocol: str,
    contact_endpoint: str,
    region_name: str | None = None,
) -> CreateContactMethodResult:
    """Create contact method.

    Args:
        protocol: Protocol.
        contact_endpoint: Contact endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["protocol"] = protocol
    kwargs["contactEndpoint"] = contact_endpoint
    try:
        resp = await client.call("CreateContactMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create contact method") from exc
    return CreateContactMethodResult(
        operations=resp.get("operations"),
    )


async def create_container_service(
    service_name: str,
    power: str,
    scale: int,
    *,
    tags: list[dict[str, Any]] | None = None,
    public_domain_names: dict[str, Any] | None = None,
    deployment: dict[str, Any] | None = None,
    private_registry_access: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateContainerServiceResult:
    """Create container service.

    Args:
        service_name: Service name.
        power: Power.
        scale: Scale.
        tags: Tags.
        public_domain_names: Public domain names.
        deployment: Deployment.
        private_registry_access: Private registry access.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    kwargs["power"] = power
    kwargs["scale"] = scale
    if tags is not None:
        kwargs["tags"] = tags
    if public_domain_names is not None:
        kwargs["publicDomainNames"] = public_domain_names
    if deployment is not None:
        kwargs["deployment"] = deployment
    if private_registry_access is not None:
        kwargs["privateRegistryAccess"] = private_registry_access
    try:
        resp = await client.call("CreateContainerService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create container service") from exc
    return CreateContainerServiceResult(
        container_service=resp.get("containerService"),
    )


async def create_container_service_deployment(
    service_name: str,
    *,
    containers: dict[str, Any] | None = None,
    public_endpoint: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateContainerServiceDeploymentResult:
    """Create container service deployment.

    Args:
        service_name: Service name.
        containers: Containers.
        public_endpoint: Public endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    if containers is not None:
        kwargs["containers"] = containers
    if public_endpoint is not None:
        kwargs["publicEndpoint"] = public_endpoint
    try:
        resp = await client.call("CreateContainerServiceDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create container service deployment") from exc
    return CreateContainerServiceDeploymentResult(
        container_service=resp.get("containerService"),
    )


async def create_container_service_registry_login(
    region_name: str | None = None,
) -> CreateContainerServiceRegistryLoginResult:
    """Create container service registry login.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("CreateContainerServiceRegistryLogin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create container service registry login") from exc
    return CreateContainerServiceRegistryLoginResult(
        registry_login=resp.get("registryLogin"),
    )


async def create_disk(
    disk_name: str,
    availability_zone: str,
    size_in_gb: int,
    *,
    tags: list[dict[str, Any]] | None = None,
    add_ons: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDiskResult:
    """Create disk.

    Args:
        disk_name: Disk name.
        availability_zone: Availability zone.
        size_in_gb: Size in gb.
        tags: Tags.
        add_ons: Add ons.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    kwargs["availabilityZone"] = availability_zone
    kwargs["sizeInGb"] = size_in_gb
    if tags is not None:
        kwargs["tags"] = tags
    if add_ons is not None:
        kwargs["addOns"] = add_ons
    try:
        resp = await client.call("CreateDisk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create disk") from exc
    return CreateDiskResult(
        operations=resp.get("operations"),
    )


async def create_disk_from_snapshot(
    disk_name: str,
    availability_zone: str,
    size_in_gb: int,
    *,
    disk_snapshot_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    add_ons: list[dict[str, Any]] | None = None,
    source_disk_name: str | None = None,
    restore_date: str | None = None,
    use_latest_restorable_auto_snapshot: bool | None = None,
    region_name: str | None = None,
) -> CreateDiskFromSnapshotResult:
    """Create disk from snapshot.

    Args:
        disk_name: Disk name.
        availability_zone: Availability zone.
        size_in_gb: Size in gb.
        disk_snapshot_name: Disk snapshot name.
        tags: Tags.
        add_ons: Add ons.
        source_disk_name: Source disk name.
        restore_date: Restore date.
        use_latest_restorable_auto_snapshot: Use latest restorable auto snapshot.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    kwargs["availabilityZone"] = availability_zone
    kwargs["sizeInGb"] = size_in_gb
    if disk_snapshot_name is not None:
        kwargs["diskSnapshotName"] = disk_snapshot_name
    if tags is not None:
        kwargs["tags"] = tags
    if add_ons is not None:
        kwargs["addOns"] = add_ons
    if source_disk_name is not None:
        kwargs["sourceDiskName"] = source_disk_name
    if restore_date is not None:
        kwargs["restoreDate"] = restore_date
    if use_latest_restorable_auto_snapshot is not None:
        kwargs["useLatestRestorableAutoSnapshot"] = use_latest_restorable_auto_snapshot
    try:
        resp = await client.call("CreateDiskFromSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create disk from snapshot") from exc
    return CreateDiskFromSnapshotResult(
        operations=resp.get("operations"),
    )


async def create_disk_snapshot(
    disk_snapshot_name: str,
    *,
    disk_name: str | None = None,
    instance_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDiskSnapshotResult:
    """Create disk snapshot.

    Args:
        disk_snapshot_name: Disk snapshot name.
        disk_name: Disk name.
        instance_name: Instance name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskSnapshotName"] = disk_snapshot_name
    if disk_name is not None:
        kwargs["diskName"] = disk_name
    if instance_name is not None:
        kwargs["instanceName"] = instance_name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDiskSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create disk snapshot") from exc
    return CreateDiskSnapshotResult(
        operations=resp.get("operations"),
    )


async def create_distribution(
    distribution_name: str,
    origin: dict[str, Any],
    default_cache_behavior: dict[str, Any],
    bundle_id: str,
    *,
    cache_behavior_settings: dict[str, Any] | None = None,
    cache_behaviors: list[dict[str, Any]] | None = None,
    ip_address_type: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    certificate_name: str | None = None,
    viewer_minimum_tls_protocol_version: str | None = None,
    region_name: str | None = None,
) -> CreateDistributionResult:
    """Create distribution.

    Args:
        distribution_name: Distribution name.
        origin: Origin.
        default_cache_behavior: Default cache behavior.
        bundle_id: Bundle id.
        cache_behavior_settings: Cache behavior settings.
        cache_behaviors: Cache behaviors.
        ip_address_type: Ip address type.
        tags: Tags.
        certificate_name: Certificate name.
        viewer_minimum_tls_protocol_version: Viewer minimum tls protocol version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["distributionName"] = distribution_name
    kwargs["origin"] = origin
    kwargs["defaultCacheBehavior"] = default_cache_behavior
    kwargs["bundleId"] = bundle_id
    if cache_behavior_settings is not None:
        kwargs["cacheBehaviorSettings"] = cache_behavior_settings
    if cache_behaviors is not None:
        kwargs["cacheBehaviors"] = cache_behaviors
    if ip_address_type is not None:
        kwargs["ipAddressType"] = ip_address_type
    if tags is not None:
        kwargs["tags"] = tags
    if certificate_name is not None:
        kwargs["certificateName"] = certificate_name
    if viewer_minimum_tls_protocol_version is not None:
        kwargs["viewerMinimumTlsProtocolVersion"] = viewer_minimum_tls_protocol_version
    try:
        resp = await client.call("CreateDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create distribution") from exc
    return CreateDistributionResult(
        distribution=resp.get("distribution"),
        operation=resp.get("operation"),
    )


async def create_domain(
    domain_name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDomainResult:
    """Create domain.

    Args:
        domain_name: Domain name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create domain") from exc
    return CreateDomainResult(
        operation=resp.get("operation"),
    )


async def create_domain_entry(
    domain_name: str,
    domain_entry: dict[str, Any],
    region_name: str | None = None,
) -> CreateDomainEntryResult:
    """Create domain entry.

    Args:
        domain_name: Domain name.
        domain_entry: Domain entry.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["domainEntry"] = domain_entry
    try:
        resp = await client.call("CreateDomainEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create domain entry") from exc
    return CreateDomainEntryResult(
        operation=resp.get("operation"),
    )


async def create_gui_session_access_details(
    resource_name: str,
    region_name: str | None = None,
) -> CreateGuiSessionAccessDetailsResult:
    """Create gui session access details.

    Args:
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    try:
        resp = await client.call("CreateGUISessionAccessDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create gui session access details") from exc
    return CreateGuiSessionAccessDetailsResult(
        resource_name=resp.get("resourceName"),
        status=resp.get("status"),
        percentage_complete=resp.get("percentageComplete"),
        failure_reason=resp.get("failureReason"),
        sessions=resp.get("sessions"),
    )


async def create_instances_from_snapshot(
    instance_names: list[str],
    availability_zone: str,
    bundle_id: str,
    *,
    attached_disk_mapping: dict[str, Any] | None = None,
    instance_snapshot_name: str | None = None,
    user_data: str | None = None,
    key_pair_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    add_ons: list[dict[str, Any]] | None = None,
    ip_address_type: str | None = None,
    source_instance_name: str | None = None,
    restore_date: str | None = None,
    use_latest_restorable_auto_snapshot: bool | None = None,
    region_name: str | None = None,
) -> CreateInstancesFromSnapshotResult:
    """Create instances from snapshot.

    Args:
        instance_names: Instance names.
        availability_zone: Availability zone.
        bundle_id: Bundle id.
        attached_disk_mapping: Attached disk mapping.
        instance_snapshot_name: Instance snapshot name.
        user_data: User data.
        key_pair_name: Key pair name.
        tags: Tags.
        add_ons: Add ons.
        ip_address_type: Ip address type.
        source_instance_name: Source instance name.
        restore_date: Restore date.
        use_latest_restorable_auto_snapshot: Use latest restorable auto snapshot.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceNames"] = instance_names
    kwargs["availabilityZone"] = availability_zone
    kwargs["bundleId"] = bundle_id
    if attached_disk_mapping is not None:
        kwargs["attachedDiskMapping"] = attached_disk_mapping
    if instance_snapshot_name is not None:
        kwargs["instanceSnapshotName"] = instance_snapshot_name
    if user_data is not None:
        kwargs["userData"] = user_data
    if key_pair_name is not None:
        kwargs["keyPairName"] = key_pair_name
    if tags is not None:
        kwargs["tags"] = tags
    if add_ons is not None:
        kwargs["addOns"] = add_ons
    if ip_address_type is not None:
        kwargs["ipAddressType"] = ip_address_type
    if source_instance_name is not None:
        kwargs["sourceInstanceName"] = source_instance_name
    if restore_date is not None:
        kwargs["restoreDate"] = restore_date
    if use_latest_restorable_auto_snapshot is not None:
        kwargs["useLatestRestorableAutoSnapshot"] = use_latest_restorable_auto_snapshot
    try:
        resp = await client.call("CreateInstancesFromSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create instances from snapshot") from exc
    return CreateInstancesFromSnapshotResult(
        operations=resp.get("operations"),
    )


async def create_key_pair(
    key_pair_name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateKeyPairResult:
    """Create key pair.

    Args:
        key_pair_name: Key pair name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyPairName"] = key_pair_name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create key pair") from exc
    return CreateKeyPairResult(
        key_pair=resp.get("keyPair"),
        public_key_base64=resp.get("publicKeyBase64"),
        private_key_base64=resp.get("privateKeyBase64"),
        operation=resp.get("operation"),
    )


async def create_load_balancer(
    load_balancer_name: str,
    instance_port: int,
    *,
    health_check_path: str | None = None,
    certificate_name: str | None = None,
    certificate_domain_name: str | None = None,
    certificate_alternative_names: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    ip_address_type: str | None = None,
    tls_policy_name: str | None = None,
    region_name: str | None = None,
) -> CreateLoadBalancerResult:
    """Create load balancer.

    Args:
        load_balancer_name: Load balancer name.
        instance_port: Instance port.
        health_check_path: Health check path.
        certificate_name: Certificate name.
        certificate_domain_name: Certificate domain name.
        certificate_alternative_names: Certificate alternative names.
        tags: Tags.
        ip_address_type: Ip address type.
        tls_policy_name: Tls policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["instancePort"] = instance_port
    if health_check_path is not None:
        kwargs["healthCheckPath"] = health_check_path
    if certificate_name is not None:
        kwargs["certificateName"] = certificate_name
    if certificate_domain_name is not None:
        kwargs["certificateDomainName"] = certificate_domain_name
    if certificate_alternative_names is not None:
        kwargs["certificateAlternativeNames"] = certificate_alternative_names
    if tags is not None:
        kwargs["tags"] = tags
    if ip_address_type is not None:
        kwargs["ipAddressType"] = ip_address_type
    if tls_policy_name is not None:
        kwargs["tlsPolicyName"] = tls_policy_name
    try:
        resp = await client.call("CreateLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create load balancer") from exc
    return CreateLoadBalancerResult(
        operations=resp.get("operations"),
    )


async def create_load_balancer_tls_certificate(
    load_balancer_name: str,
    certificate_name: str,
    certificate_domain_name: str,
    *,
    certificate_alternative_names: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateLoadBalancerTlsCertificateResult:
    """Create load balancer tls certificate.

    Args:
        load_balancer_name: Load balancer name.
        certificate_name: Certificate name.
        certificate_domain_name: Certificate domain name.
        certificate_alternative_names: Certificate alternative names.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["certificateName"] = certificate_name
    kwargs["certificateDomainName"] = certificate_domain_name
    if certificate_alternative_names is not None:
        kwargs["certificateAlternativeNames"] = certificate_alternative_names
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateLoadBalancerTlsCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create load balancer tls certificate") from exc
    return CreateLoadBalancerTlsCertificateResult(
        operations=resp.get("operations"),
    )


async def create_relational_database(
    relational_database_name: str,
    relational_database_blueprint_id: str,
    relational_database_bundle_id: str,
    master_database_name: str,
    master_username: str,
    *,
    availability_zone: str | None = None,
    master_user_password: str | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRelationalDatabaseResult:
    """Create relational database.

    Args:
        relational_database_name: Relational database name.
        relational_database_blueprint_id: Relational database blueprint id.
        relational_database_bundle_id: Relational database bundle id.
        master_database_name: Master database name.
        master_username: Master username.
        availability_zone: Availability zone.
        master_user_password: Master user password.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    kwargs["relationalDatabaseBlueprintId"] = relational_database_blueprint_id
    kwargs["relationalDatabaseBundleId"] = relational_database_bundle_id
    kwargs["masterDatabaseName"] = master_database_name
    kwargs["masterUsername"] = master_username
    if availability_zone is not None:
        kwargs["availabilityZone"] = availability_zone
    if master_user_password is not None:
        kwargs["masterUserPassword"] = master_user_password
    if preferred_backup_window is not None:
        kwargs["preferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["preferredMaintenanceWindow"] = preferred_maintenance_window
    if publicly_accessible is not None:
        kwargs["publiclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create relational database") from exc
    return CreateRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def create_relational_database_from_snapshot(
    relational_database_name: str,
    *,
    availability_zone: str | None = None,
    publicly_accessible: bool | None = None,
    relational_database_snapshot_name: str | None = None,
    relational_database_bundle_id: str | None = None,
    source_relational_database_name: str | None = None,
    restore_time: str | None = None,
    use_latest_restorable_time: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRelationalDatabaseFromSnapshotResult:
    """Create relational database from snapshot.

    Args:
        relational_database_name: Relational database name.
        availability_zone: Availability zone.
        publicly_accessible: Publicly accessible.
        relational_database_snapshot_name: Relational database snapshot name.
        relational_database_bundle_id: Relational database bundle id.
        source_relational_database_name: Source relational database name.
        restore_time: Restore time.
        use_latest_restorable_time: Use latest restorable time.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if availability_zone is not None:
        kwargs["availabilityZone"] = availability_zone
    if publicly_accessible is not None:
        kwargs["publiclyAccessible"] = publicly_accessible
    if relational_database_snapshot_name is not None:
        kwargs["relationalDatabaseSnapshotName"] = relational_database_snapshot_name
    if relational_database_bundle_id is not None:
        kwargs["relationalDatabaseBundleId"] = relational_database_bundle_id
    if source_relational_database_name is not None:
        kwargs["sourceRelationalDatabaseName"] = source_relational_database_name
    if restore_time is not None:
        kwargs["restoreTime"] = restore_time
    if use_latest_restorable_time is not None:
        kwargs["useLatestRestorableTime"] = use_latest_restorable_time
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRelationalDatabaseFromSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create relational database from snapshot") from exc
    return CreateRelationalDatabaseFromSnapshotResult(
        operations=resp.get("operations"),
    )


async def create_relational_database_snapshot(
    relational_database_name: str,
    relational_database_snapshot_name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRelationalDatabaseSnapshotResult:
    """Create relational database snapshot.

    Args:
        relational_database_name: Relational database name.
        relational_database_snapshot_name: Relational database snapshot name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    kwargs["relationalDatabaseSnapshotName"] = relational_database_snapshot_name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRelationalDatabaseSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create relational database snapshot") from exc
    return CreateRelationalDatabaseSnapshotResult(
        operations=resp.get("operations"),
    )


async def delete_alarm(
    alarm_name: str,
    region_name: str | None = None,
) -> DeleteAlarmResult:
    """Delete alarm.

    Args:
        alarm_name: Alarm name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["alarmName"] = alarm_name
    try:
        resp = await client.call("DeleteAlarm", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete alarm") from exc
    return DeleteAlarmResult(
        operations=resp.get("operations"),
    )


async def delete_auto_snapshot(
    resource_name: str,
    date: str,
    region_name: str | None = None,
) -> DeleteAutoSnapshotResult:
    """Delete auto snapshot.

    Args:
        resource_name: Resource name.
        date: Date.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["date"] = date
    try:
        resp = await client.call("DeleteAutoSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete auto snapshot") from exc
    return DeleteAutoSnapshotResult(
        operations=resp.get("operations"),
    )


async def delete_bucket(
    bucket_name: str,
    *,
    force_delete: bool | None = None,
    region_name: str | None = None,
) -> DeleteBucketResult:
    """Delete bucket.

    Args:
        bucket_name: Bucket name.
        force_delete: Force delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    if force_delete is not None:
        kwargs["forceDelete"] = force_delete
    try:
        resp = await client.call("DeleteBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket") from exc
    return DeleteBucketResult(
        operations=resp.get("operations"),
    )


async def delete_bucket_access_key(
    bucket_name: str,
    access_key_id: str,
    region_name: str | None = None,
) -> DeleteBucketAccessKeyResult:
    """Delete bucket access key.

    Args:
        bucket_name: Bucket name.
        access_key_id: Access key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    kwargs["accessKeyId"] = access_key_id
    try:
        resp = await client.call("DeleteBucketAccessKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete bucket access key") from exc
    return DeleteBucketAccessKeyResult(
        operations=resp.get("operations"),
    )


async def delete_certificate(
    certificate_name: str,
    region_name: str | None = None,
) -> DeleteCertificateResult:
    """Delete certificate.

    Args:
        certificate_name: Certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateName"] = certificate_name
    try:
        resp = await client.call("DeleteCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete certificate") from exc
    return DeleteCertificateResult(
        operations=resp.get("operations"),
    )


async def delete_contact_method(
    protocol: str,
    region_name: str | None = None,
) -> DeleteContactMethodResult:
    """Delete contact method.

    Args:
        protocol: Protocol.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["protocol"] = protocol
    try:
        resp = await client.call("DeleteContactMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete contact method") from exc
    return DeleteContactMethodResult(
        operations=resp.get("operations"),
    )


async def delete_container_image(
    service_name: str,
    image: str,
    region_name: str | None = None,
) -> None:
    """Delete container image.

    Args:
        service_name: Service name.
        image: Image.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    kwargs["image"] = image
    try:
        await client.call("DeleteContainerImage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete container image") from exc
    return None


async def delete_container_service(
    service_name: str,
    region_name: str | None = None,
) -> None:
    """Delete container service.

    Args:
        service_name: Service name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    try:
        await client.call("DeleteContainerService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete container service") from exc
    return None


async def delete_disk(
    disk_name: str,
    *,
    force_delete_add_ons: bool | None = None,
    region_name: str | None = None,
) -> DeleteDiskResult:
    """Delete disk.

    Args:
        disk_name: Disk name.
        force_delete_add_ons: Force delete add ons.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    if force_delete_add_ons is not None:
        kwargs["forceDeleteAddOns"] = force_delete_add_ons
    try:
        resp = await client.call("DeleteDisk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete disk") from exc
    return DeleteDiskResult(
        operations=resp.get("operations"),
    )


async def delete_disk_snapshot(
    disk_snapshot_name: str,
    region_name: str | None = None,
) -> DeleteDiskSnapshotResult:
    """Delete disk snapshot.

    Args:
        disk_snapshot_name: Disk snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskSnapshotName"] = disk_snapshot_name
    try:
        resp = await client.call("DeleteDiskSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete disk snapshot") from exc
    return DeleteDiskSnapshotResult(
        operations=resp.get("operations"),
    )


async def delete_distribution(
    *,
    distribution_name: str | None = None,
    region_name: str | None = None,
) -> DeleteDistributionResult:
    """Delete distribution.

    Args:
        distribution_name: Distribution name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if distribution_name is not None:
        kwargs["distributionName"] = distribution_name
    try:
        resp = await client.call("DeleteDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete distribution") from exc
    return DeleteDistributionResult(
        operation=resp.get("operation"),
    )


async def delete_domain(
    domain_name: str,
    region_name: str | None = None,
) -> DeleteDomainResult:
    """Delete domain.

    Args:
        domain_name: Domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    try:
        resp = await client.call("DeleteDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain") from exc
    return DeleteDomainResult(
        operation=resp.get("operation"),
    )


async def delete_domain_entry(
    domain_name: str,
    domain_entry: dict[str, Any],
    region_name: str | None = None,
) -> DeleteDomainEntryResult:
    """Delete domain entry.

    Args:
        domain_name: Domain name.
        domain_entry: Domain entry.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["domainEntry"] = domain_entry
    try:
        resp = await client.call("DeleteDomainEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain entry") from exc
    return DeleteDomainEntryResult(
        operation=resp.get("operation"),
    )


async def delete_key_pair(
    key_pair_name: str,
    *,
    expected_fingerprint: str | None = None,
    region_name: str | None = None,
) -> DeleteKeyPairResult:
    """Delete key pair.

    Args:
        key_pair_name: Key pair name.
        expected_fingerprint: Expected fingerprint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyPairName"] = key_pair_name
    if expected_fingerprint is not None:
        kwargs["expectedFingerprint"] = expected_fingerprint
    try:
        resp = await client.call("DeleteKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete key pair") from exc
    return DeleteKeyPairResult(
        operation=resp.get("operation"),
    )


async def delete_known_host_keys(
    instance_name: str,
    region_name: str | None = None,
) -> DeleteKnownHostKeysResult:
    """Delete known host keys.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("DeleteKnownHostKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete known host keys") from exc
    return DeleteKnownHostKeysResult(
        operations=resp.get("operations"),
    )


async def delete_load_balancer(
    load_balancer_name: str,
    region_name: str | None = None,
) -> DeleteLoadBalancerResult:
    """Delete load balancer.

    Args:
        load_balancer_name: Load balancer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    try:
        resp = await client.call("DeleteLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete load balancer") from exc
    return DeleteLoadBalancerResult(
        operations=resp.get("operations"),
    )


async def delete_load_balancer_tls_certificate(
    load_balancer_name: str,
    certificate_name: str,
    *,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeleteLoadBalancerTlsCertificateResult:
    """Delete load balancer tls certificate.

    Args:
        load_balancer_name: Load balancer name.
        certificate_name: Certificate name.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["certificateName"] = certificate_name
    if force is not None:
        kwargs["force"] = force
    try:
        resp = await client.call("DeleteLoadBalancerTlsCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete load balancer tls certificate") from exc
    return DeleteLoadBalancerTlsCertificateResult(
        operations=resp.get("operations"),
    )


async def delete_relational_database(
    relational_database_name: str,
    *,
    skip_final_snapshot: bool | None = None,
    final_relational_database_snapshot_name: str | None = None,
    region_name: str | None = None,
) -> DeleteRelationalDatabaseResult:
    """Delete relational database.

    Args:
        relational_database_name: Relational database name.
        skip_final_snapshot: Skip final snapshot.
        final_relational_database_snapshot_name: Final relational database snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if skip_final_snapshot is not None:
        kwargs["skipFinalSnapshot"] = skip_final_snapshot
    if final_relational_database_snapshot_name is not None:
        kwargs["finalRelationalDatabaseSnapshotName"] = final_relational_database_snapshot_name
    try:
        resp = await client.call("DeleteRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete relational database") from exc
    return DeleteRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def delete_relational_database_snapshot(
    relational_database_snapshot_name: str,
    region_name: str | None = None,
) -> DeleteRelationalDatabaseSnapshotResult:
    """Delete relational database snapshot.

    Args:
        relational_database_snapshot_name: Relational database snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseSnapshotName"] = relational_database_snapshot_name
    try:
        resp = await client.call("DeleteRelationalDatabaseSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete relational database snapshot") from exc
    return DeleteRelationalDatabaseSnapshotResult(
        operations=resp.get("operations"),
    )


async def detach_certificate_from_distribution(
    distribution_name: str,
    region_name: str | None = None,
) -> DetachCertificateFromDistributionResult:
    """Detach certificate from distribution.

    Args:
        distribution_name: Distribution name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["distributionName"] = distribution_name
    try:
        resp = await client.call("DetachCertificateFromDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach certificate from distribution") from exc
    return DetachCertificateFromDistributionResult(
        operation=resp.get("operation"),
    )


async def detach_disk(
    disk_name: str,
    region_name: str | None = None,
) -> DetachDiskResult:
    """Detach disk.

    Args:
        disk_name: Disk name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    try:
        resp = await client.call("DetachDisk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach disk") from exc
    return DetachDiskResult(
        operations=resp.get("operations"),
    )


async def detach_instances_from_load_balancer(
    load_balancer_name: str,
    instance_names: list[str],
    region_name: str | None = None,
) -> DetachInstancesFromLoadBalancerResult:
    """Detach instances from load balancer.

    Args:
        load_balancer_name: Load balancer name.
        instance_names: Instance names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["instanceNames"] = instance_names
    try:
        resp = await client.call("DetachInstancesFromLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach instances from load balancer") from exc
    return DetachInstancesFromLoadBalancerResult(
        operations=resp.get("operations"),
    )


async def detach_static_ip(
    static_ip_name: str,
    region_name: str | None = None,
) -> DetachStaticIpResult:
    """Detach static ip.

    Args:
        static_ip_name: Static ip name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["staticIpName"] = static_ip_name
    try:
        resp = await client.call("DetachStaticIp", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach static ip") from exc
    return DetachStaticIpResult(
        operations=resp.get("operations"),
    )


async def disable_add_on(
    add_on_type: str,
    resource_name: str,
    region_name: str | None = None,
) -> DisableAddOnResult:
    """Disable add on.

    Args:
        add_on_type: Add on type.
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["addOnType"] = add_on_type
    kwargs["resourceName"] = resource_name
    try:
        resp = await client.call("DisableAddOn", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable add on") from exc
    return DisableAddOnResult(
        operations=resp.get("operations"),
    )


async def download_default_key_pair(
    region_name: str | None = None,
) -> DownloadDefaultKeyPairResult:
    """Download default key pair.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DownloadDefaultKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to download default key pair") from exc
    return DownloadDefaultKeyPairResult(
        public_key_base64=resp.get("publicKeyBase64"),
        private_key_base64=resp.get("privateKeyBase64"),
        created_at=resp.get("createdAt"),
    )


async def enable_add_on(
    resource_name: str,
    add_on_request: dict[str, Any],
    region_name: str | None = None,
) -> EnableAddOnResult:
    """Enable add on.

    Args:
        resource_name: Resource name.
        add_on_request: Add on request.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["addOnRequest"] = add_on_request
    try:
        resp = await client.call("EnableAddOn", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable add on") from exc
    return EnableAddOnResult(
        operations=resp.get("operations"),
    )


async def export_snapshot(
    source_snapshot_name: str,
    region_name: str | None = None,
) -> ExportSnapshotResult:
    """Export snapshot.

    Args:
        source_snapshot_name: Source snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sourceSnapshotName"] = source_snapshot_name
    try:
        resp = await client.call("ExportSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to export snapshot") from exc
    return ExportSnapshotResult(
        operations=resp.get("operations"),
    )


async def get_active_names(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetActiveNamesResult:
    """Get active names.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetActiveNames", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get active names") from exc
    return GetActiveNamesResult(
        active_names=resp.get("activeNames"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_alarms(
    *,
    alarm_name: str | None = None,
    page_token: str | None = None,
    monitored_resource_name: str | None = None,
    region_name: str | None = None,
) -> GetAlarmsResult:
    """Get alarms.

    Args:
        alarm_name: Alarm name.
        page_token: Page token.
        monitored_resource_name: Monitored resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if alarm_name is not None:
        kwargs["alarmName"] = alarm_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if monitored_resource_name is not None:
        kwargs["monitoredResourceName"] = monitored_resource_name
    try:
        resp = await client.call("GetAlarms", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get alarms") from exc
    return GetAlarmsResult(
        alarms=resp.get("alarms"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_auto_snapshots(
    resource_name: str,
    region_name: str | None = None,
) -> GetAutoSnapshotsResult:
    """Get auto snapshots.

    Args:
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    try:
        resp = await client.call("GetAutoSnapshots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get auto snapshots") from exc
    return GetAutoSnapshotsResult(
        resource_name=resp.get("resourceName"),
        resource_type=resp.get("resourceType"),
        auto_snapshots=resp.get("autoSnapshots"),
    )


async def get_blueprints(
    *,
    include_inactive: bool | None = None,
    page_token: str | None = None,
    app_category: str | None = None,
    region_name: str | None = None,
) -> GetBlueprintsResult:
    """Get blueprints.

    Args:
        include_inactive: Include inactive.
        page_token: Page token.
        app_category: App category.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if include_inactive is not None:
        kwargs["includeInactive"] = include_inactive
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if app_category is not None:
        kwargs["appCategory"] = app_category
    try:
        resp = await client.call("GetBlueprints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get blueprints") from exc
    return GetBlueprintsResult(
        blueprints=resp.get("blueprints"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_bucket_access_keys(
    bucket_name: str,
    region_name: str | None = None,
) -> GetBucketAccessKeysResult:
    """Get bucket access keys.

    Args:
        bucket_name: Bucket name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    try:
        resp = await client.call("GetBucketAccessKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket access keys") from exc
    return GetBucketAccessKeysResult(
        access_keys=resp.get("accessKeys"),
    )


async def get_bucket_bundles(
    *,
    include_inactive: bool | None = None,
    region_name: str | None = None,
) -> GetBucketBundlesResult:
    """Get bucket bundles.

    Args:
        include_inactive: Include inactive.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if include_inactive is not None:
        kwargs["includeInactive"] = include_inactive
    try:
        resp = await client.call("GetBucketBundles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket bundles") from exc
    return GetBucketBundlesResult(
        bundles=resp.get("bundles"),
    )


async def get_bucket_metric_data(
    bucket_name: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int,
    statistics: list[str],
    unit: str,
    region_name: str | None = None,
) -> GetBucketMetricDataResult:
    """Get bucket metric data.

    Args:
        bucket_name: Bucket name.
        metric_name: Metric name.
        start_time: Start time.
        end_time: End time.
        period: Period.
        statistics: Statistics.
        unit: Unit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    kwargs["metricName"] = metric_name
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["period"] = period
    kwargs["statistics"] = statistics
    kwargs["unit"] = unit
    try:
        resp = await client.call("GetBucketMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bucket metric data") from exc
    return GetBucketMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_buckets(
    *,
    bucket_name: str | None = None,
    page_token: str | None = None,
    include_connected_resources: bool | None = None,
    include_cors: bool | None = None,
    region_name: str | None = None,
) -> GetBucketsResult:
    """Get buckets.

    Args:
        bucket_name: Bucket name.
        page_token: Page token.
        include_connected_resources: Include connected resources.
        include_cors: Include cors.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if bucket_name is not None:
        kwargs["bucketName"] = bucket_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if include_connected_resources is not None:
        kwargs["includeConnectedResources"] = include_connected_resources
    if include_cors is not None:
        kwargs["includeCors"] = include_cors
    try:
        resp = await client.call("GetBuckets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get buckets") from exc
    return GetBucketsResult(
        buckets=resp.get("buckets"),
        next_page_token=resp.get("nextPageToken"),
        account_level_bpa_sync=resp.get("accountLevelBpaSync"),
    )


async def get_bundles(
    *,
    include_inactive: bool | None = None,
    page_token: str | None = None,
    app_category: str | None = None,
    region_name: str | None = None,
) -> GetBundlesResult:
    """Get bundles.

    Args:
        include_inactive: Include inactive.
        page_token: Page token.
        app_category: App category.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if include_inactive is not None:
        kwargs["includeInactive"] = include_inactive
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if app_category is not None:
        kwargs["appCategory"] = app_category
    try:
        resp = await client.call("GetBundles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get bundles") from exc
    return GetBundlesResult(
        bundles=resp.get("bundles"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_certificates(
    *,
    certificate_statuses: list[str] | None = None,
    include_certificate_details: bool | None = None,
    certificate_name: str | None = None,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetCertificatesResult:
    """Get certificates.

    Args:
        certificate_statuses: Certificate statuses.
        include_certificate_details: Include certificate details.
        certificate_name: Certificate name.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if certificate_statuses is not None:
        kwargs["certificateStatuses"] = certificate_statuses
    if include_certificate_details is not None:
        kwargs["includeCertificateDetails"] = include_certificate_details
    if certificate_name is not None:
        kwargs["certificateName"] = certificate_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get certificates") from exc
    return GetCertificatesResult(
        certificates=resp.get("certificates"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_cloud_formation_stack_records(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetCloudFormationStackRecordsResult:
    """Get cloud formation stack records.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetCloudFormationStackRecords", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cloud formation stack records") from exc
    return GetCloudFormationStackRecordsResult(
        cloud_formation_stack_records=resp.get("cloudFormationStackRecords"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_contact_methods(
    *,
    protocols: list[str] | None = None,
    region_name: str | None = None,
) -> GetContactMethodsResult:
    """Get contact methods.

    Args:
        protocols: Protocols.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if protocols is not None:
        kwargs["protocols"] = protocols
    try:
        resp = await client.call("GetContactMethods", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get contact methods") from exc
    return GetContactMethodsResult(
        contact_methods=resp.get("contactMethods"),
    )


async def get_container_api_metadata(
    region_name: str | None = None,
) -> GetContainerApiMetadataResult:
    """Get container api metadata.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetContainerAPIMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container api metadata") from exc
    return GetContainerApiMetadataResult(
        metadata=resp.get("metadata"),
    )


async def get_container_images(
    service_name: str,
    region_name: str | None = None,
) -> GetContainerImagesResult:
    """Get container images.

    Args:
        service_name: Service name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    try:
        resp = await client.call("GetContainerImages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container images") from exc
    return GetContainerImagesResult(
        container_images=resp.get("containerImages"),
    )


async def get_container_log(
    service_name: str,
    container_name: str,
    *,
    start_time: str | None = None,
    end_time: str | None = None,
    filter_pattern: str | None = None,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetContainerLogResult:
    """Get container log.

    Args:
        service_name: Service name.
        container_name: Container name.
        start_time: Start time.
        end_time: End time.
        filter_pattern: Filter pattern.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    kwargs["containerName"] = container_name
    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time
    if filter_pattern is not None:
        kwargs["filterPattern"] = filter_pattern
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetContainerLog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container log") from exc
    return GetContainerLogResult(
        log_events=resp.get("logEvents"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_container_service_deployments(
    service_name: str,
    region_name: str | None = None,
) -> GetContainerServiceDeploymentsResult:
    """Get container service deployments.

    Args:
        service_name: Service name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    try:
        resp = await client.call("GetContainerServiceDeployments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container service deployments") from exc
    return GetContainerServiceDeploymentsResult(
        deployments=resp.get("deployments"),
    )


async def get_container_service_metric_data(
    service_name: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int,
    statistics: list[str],
    region_name: str | None = None,
) -> GetContainerServiceMetricDataResult:
    """Get container service metric data.

    Args:
        service_name: Service name.
        metric_name: Metric name.
        start_time: Start time.
        end_time: End time.
        period: Period.
        statistics: Statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    kwargs["metricName"] = metric_name
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["period"] = period
    kwargs["statistics"] = statistics
    try:
        resp = await client.call("GetContainerServiceMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container service metric data") from exc
    return GetContainerServiceMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_container_service_powers(
    region_name: str | None = None,
) -> GetContainerServicePowersResult:
    """Get container service powers.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetContainerServicePowers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container service powers") from exc
    return GetContainerServicePowersResult(
        powers=resp.get("powers"),
    )


async def get_container_services(
    *,
    service_name: str | None = None,
    region_name: str | None = None,
) -> GetContainerServicesResult:
    """Get container services.

    Args:
        service_name: Service name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if service_name is not None:
        kwargs["serviceName"] = service_name
    try:
        resp = await client.call("GetContainerServices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get container services") from exc
    return GetContainerServicesResult(
        container_services=resp.get("containerServices"),
    )


async def get_cost_estimate(
    resource_name: str,
    start_time: str,
    end_time: str,
    region_name: str | None = None,
) -> GetCostEstimateResult:
    """Get cost estimate.

    Args:
        resource_name: Resource name.
        start_time: Start time.
        end_time: End time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    try:
        resp = await client.call("GetCostEstimate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cost estimate") from exc
    return GetCostEstimateResult(
        resources_budget_estimate=resp.get("resourcesBudgetEstimate"),
    )


async def get_disk(
    disk_name: str,
    region_name: str | None = None,
) -> GetDiskResult:
    """Get disk.

    Args:
        disk_name: Disk name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskName"] = disk_name
    try:
        resp = await client.call("GetDisk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get disk") from exc
    return GetDiskResult(
        disk=resp.get("disk"),
    )


async def get_disk_snapshot(
    disk_snapshot_name: str,
    region_name: str | None = None,
) -> GetDiskSnapshotResult:
    """Get disk snapshot.

    Args:
        disk_snapshot_name: Disk snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["diskSnapshotName"] = disk_snapshot_name
    try:
        resp = await client.call("GetDiskSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get disk snapshot") from exc
    return GetDiskSnapshotResult(
        disk_snapshot=resp.get("diskSnapshot"),
    )


async def get_disk_snapshots(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetDiskSnapshotsResult:
    """Get disk snapshots.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetDiskSnapshots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get disk snapshots") from exc
    return GetDiskSnapshotsResult(
        disk_snapshots=resp.get("diskSnapshots"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_disks(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetDisksResult:
    """Get disks.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetDisks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get disks") from exc
    return GetDisksResult(
        disks=resp.get("disks"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_distribution_bundles(
    region_name: str | None = None,
) -> GetDistributionBundlesResult:
    """Get distribution bundles.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetDistributionBundles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution bundles") from exc
    return GetDistributionBundlesResult(
        bundles=resp.get("bundles"),
    )


async def get_distribution_latest_cache_reset(
    *,
    distribution_name: str | None = None,
    region_name: str | None = None,
) -> GetDistributionLatestCacheResetResult:
    """Get distribution latest cache reset.

    Args:
        distribution_name: Distribution name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if distribution_name is not None:
        kwargs["distributionName"] = distribution_name
    try:
        resp = await client.call("GetDistributionLatestCacheReset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution latest cache reset") from exc
    return GetDistributionLatestCacheResetResult(
        status=resp.get("status"),
        create_time=resp.get("createTime"),
    )


async def get_distribution_metric_data(
    distribution_name: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    period: int,
    unit: str,
    statistics: list[str],
    region_name: str | None = None,
) -> GetDistributionMetricDataResult:
    """Get distribution metric data.

    Args:
        distribution_name: Distribution name.
        metric_name: Metric name.
        start_time: Start time.
        end_time: End time.
        period: Period.
        unit: Unit.
        statistics: Statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["distributionName"] = distribution_name
    kwargs["metricName"] = metric_name
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["period"] = period
    kwargs["unit"] = unit
    kwargs["statistics"] = statistics
    try:
        resp = await client.call("GetDistributionMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distribution metric data") from exc
    return GetDistributionMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_distributions(
    *,
    distribution_name: str | None = None,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetDistributionsResult:
    """Get distributions.

    Args:
        distribution_name: Distribution name.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if distribution_name is not None:
        kwargs["distributionName"] = distribution_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetDistributions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get distributions") from exc
    return GetDistributionsResult(
        distributions=resp.get("distributions"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_domain(
    domain_name: str,
    region_name: str | None = None,
) -> GetDomainResult:
    """Get domain.

    Args:
        domain_name: Domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    try:
        resp = await client.call("GetDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain") from exc
    return GetDomainResult(
        domain=resp.get("domain"),
    )


async def get_domains(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetDomainsResult:
    """Get domains.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetDomains", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domains") from exc
    return GetDomainsResult(
        domains=resp.get("domains"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_export_snapshot_records(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetExportSnapshotRecordsResult:
    """Get export snapshot records.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetExportSnapshotRecords", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get export snapshot records") from exc
    return GetExportSnapshotRecordsResult(
        export_snapshot_records=resp.get("exportSnapshotRecords"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_instance_access_details(
    instance_name: str,
    *,
    protocol: str | None = None,
    region_name: str | None = None,
) -> GetInstanceAccessDetailsResult:
    """Get instance access details.

    Args:
        instance_name: Instance name.
        protocol: Protocol.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    if protocol is not None:
        kwargs["protocol"] = protocol
    try:
        resp = await client.call("GetInstanceAccessDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance access details") from exc
    return GetInstanceAccessDetailsResult(
        access_details=resp.get("accessDetails"),
    )


async def get_instance_metric_data(
    instance_name: str,
    metric_name: str,
    period: int,
    start_time: str,
    end_time: str,
    unit: str,
    statistics: list[str],
    region_name: str | None = None,
) -> GetInstanceMetricDataResult:
    """Get instance metric data.

    Args:
        instance_name: Instance name.
        metric_name: Metric name.
        period: Period.
        start_time: Start time.
        end_time: End time.
        unit: Unit.
        statistics: Statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    kwargs["metricName"] = metric_name
    kwargs["period"] = period
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["unit"] = unit
    kwargs["statistics"] = statistics
    try:
        resp = await client.call("GetInstanceMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance metric data") from exc
    return GetInstanceMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_instance_port_states(
    instance_name: str,
    region_name: str | None = None,
) -> GetInstancePortStatesResult:
    """Get instance port states.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("GetInstancePortStates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance port states") from exc
    return GetInstancePortStatesResult(
        port_states=resp.get("portStates"),
    )


async def get_instance_snapshot(
    instance_snapshot_name: str,
    region_name: str | None = None,
) -> GetInstanceSnapshotResult:
    """Get instance snapshot.

    Args:
        instance_snapshot_name: Instance snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceSnapshotName"] = instance_snapshot_name
    try:
        resp = await client.call("GetInstanceSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance snapshot") from exc
    return GetInstanceSnapshotResult(
        instance_snapshot=resp.get("instanceSnapshot"),
    )


async def get_instance_state(
    instance_name: str,
    region_name: str | None = None,
) -> GetInstanceStateResult:
    """Get instance state.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("GetInstanceState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance state") from exc
    return GetInstanceStateResult(
        state=resp.get("state"),
    )


async def get_key_pair(
    key_pair_name: str,
    region_name: str | None = None,
) -> GetKeyPairResult:
    """Get key pair.

    Args:
        key_pair_name: Key pair name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyPairName"] = key_pair_name
    try:
        resp = await client.call("GetKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get key pair") from exc
    return GetKeyPairResult(
        key_pair=resp.get("keyPair"),
    )


async def get_key_pairs(
    *,
    page_token: str | None = None,
    include_default_key_pair: bool | None = None,
    region_name: str | None = None,
) -> GetKeyPairsResult:
    """Get key pairs.

    Args:
        page_token: Page token.
        include_default_key_pair: Include default key pair.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if include_default_key_pair is not None:
        kwargs["includeDefaultKeyPair"] = include_default_key_pair
    try:
        resp = await client.call("GetKeyPairs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get key pairs") from exc
    return GetKeyPairsResult(
        key_pairs=resp.get("keyPairs"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_load_balancer(
    load_balancer_name: str,
    region_name: str | None = None,
) -> GetLoadBalancerResult:
    """Get load balancer.

    Args:
        load_balancer_name: Load balancer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    try:
        resp = await client.call("GetLoadBalancer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get load balancer") from exc
    return GetLoadBalancerResult(
        load_balancer=resp.get("loadBalancer"),
    )


async def get_load_balancer_metric_data(
    load_balancer_name: str,
    metric_name: str,
    period: int,
    start_time: str,
    end_time: str,
    unit: str,
    statistics: list[str],
    region_name: str | None = None,
) -> GetLoadBalancerMetricDataResult:
    """Get load balancer metric data.

    Args:
        load_balancer_name: Load balancer name.
        metric_name: Metric name.
        period: Period.
        start_time: Start time.
        end_time: End time.
        unit: Unit.
        statistics: Statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["metricName"] = metric_name
    kwargs["period"] = period
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["unit"] = unit
    kwargs["statistics"] = statistics
    try:
        resp = await client.call("GetLoadBalancerMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get load balancer metric data") from exc
    return GetLoadBalancerMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_load_balancer_tls_certificates(
    load_balancer_name: str,
    region_name: str | None = None,
) -> GetLoadBalancerTlsCertificatesResult:
    """Get load balancer tls certificates.

    Args:
        load_balancer_name: Load balancer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    try:
        resp = await client.call("GetLoadBalancerTlsCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get load balancer tls certificates") from exc
    return GetLoadBalancerTlsCertificatesResult(
        tls_certificates=resp.get("tlsCertificates"),
    )


async def get_load_balancer_tls_policies(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetLoadBalancerTlsPoliciesResult:
    """Get load balancer tls policies.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetLoadBalancerTlsPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get load balancer tls policies") from exc
    return GetLoadBalancerTlsPoliciesResult(
        tls_policies=resp.get("tlsPolicies"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_load_balancers(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetLoadBalancersResult:
    """Get load balancers.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetLoadBalancers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get load balancers") from exc
    return GetLoadBalancersResult(
        load_balancers=resp.get("loadBalancers"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_operation(
    operation_id: str,
    region_name: str | None = None,
) -> GetOperationResult:
    """Get operation.

    Args:
        operation_id: Operation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["operationId"] = operation_id
    try:
        resp = await client.call("GetOperation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get operation") from exc
    return GetOperationResult(
        operation=resp.get("operation"),
    )


async def get_operations(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetOperationsResult:
    """Get operations.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetOperations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get operations") from exc
    return GetOperationsResult(
        operations=resp.get("operations"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_operations_for_resource(
    resource_name: str,
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetOperationsForResourceResult:
    """Get operations for resource.

    Args:
        resource_name: Resource name.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetOperationsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get operations for resource") from exc
    return GetOperationsForResourceResult(
        operations=resp.get("operations"),
        next_page_count=resp.get("nextPageCount"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_regions(
    *,
    include_availability_zones: bool | None = None,
    include_relational_database_availability_zones: bool | None = None,
    region_name: str | None = None,
) -> GetRegionsResult:
    """Get regions.

    Args:
        include_availability_zones: Include availability zones.
        include_relational_database_availability_zones: Include relational database availability zones.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if include_availability_zones is not None:
        kwargs["includeAvailabilityZones"] = include_availability_zones
    if include_relational_database_availability_zones is not None:
        kwargs["includeRelationalDatabaseAvailabilityZones"] = (
            include_relational_database_availability_zones
        )
    try:
        resp = await client.call("GetRegions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get regions") from exc
    return GetRegionsResult(
        regions=resp.get("regions"),
    )


async def get_relational_database(
    relational_database_name: str,
    region_name: str | None = None,
) -> GetRelationalDatabaseResult:
    """Get relational database.

    Args:
        relational_database_name: Relational database name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    try:
        resp = await client.call("GetRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database") from exc
    return GetRelationalDatabaseResult(
        relational_database=resp.get("relationalDatabase"),
    )


async def get_relational_database_blueprints(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseBlueprintsResult:
    """Get relational database blueprints.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabaseBlueprints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database blueprints") from exc
    return GetRelationalDatabaseBlueprintsResult(
        blueprints=resp.get("blueprints"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_relational_database_bundles(
    *,
    page_token: str | None = None,
    include_inactive: bool | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseBundlesResult:
    """Get relational database bundles.

    Args:
        page_token: Page token.
        include_inactive: Include inactive.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    if include_inactive is not None:
        kwargs["includeInactive"] = include_inactive
    try:
        resp = await client.call("GetRelationalDatabaseBundles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database bundles") from exc
    return GetRelationalDatabaseBundlesResult(
        bundles=resp.get("bundles"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_relational_database_events(
    relational_database_name: str,
    *,
    duration_in_minutes: int | None = None,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseEventsResult:
    """Get relational database events.

    Args:
        relational_database_name: Relational database name.
        duration_in_minutes: Duration in minutes.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if duration_in_minutes is not None:
        kwargs["durationInMinutes"] = duration_in_minutes
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabaseEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database events") from exc
    return GetRelationalDatabaseEventsResult(
        relational_database_events=resp.get("relationalDatabaseEvents"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_relational_database_log_events(
    relational_database_name: str,
    log_stream_name: str,
    *,
    start_time: str | None = None,
    end_time: str | None = None,
    start_from_head: bool | None = None,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseLogEventsResult:
    """Get relational database log events.

    Args:
        relational_database_name: Relational database name.
        log_stream_name: Log stream name.
        start_time: Start time.
        end_time: End time.
        start_from_head: Start from head.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    kwargs["logStreamName"] = log_stream_name
    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time
    if start_from_head is not None:
        kwargs["startFromHead"] = start_from_head
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabaseLogEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database log events") from exc
    return GetRelationalDatabaseLogEventsResult(
        resource_log_events=resp.get("resourceLogEvents"),
        next_backward_token=resp.get("nextBackwardToken"),
        next_forward_token=resp.get("nextForwardToken"),
    )


async def get_relational_database_log_streams(
    relational_database_name: str,
    region_name: str | None = None,
) -> GetRelationalDatabaseLogStreamsResult:
    """Get relational database log streams.

    Args:
        relational_database_name: Relational database name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    try:
        resp = await client.call("GetRelationalDatabaseLogStreams", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database log streams") from exc
    return GetRelationalDatabaseLogStreamsResult(
        log_streams=resp.get("logStreams"),
    )


async def get_relational_database_master_user_password(
    relational_database_name: str,
    *,
    password_version: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseMasterUserPasswordResult:
    """Get relational database master user password.

    Args:
        relational_database_name: Relational database name.
        password_version: Password version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if password_version is not None:
        kwargs["passwordVersion"] = password_version
    try:
        resp = await client.call("GetRelationalDatabaseMasterUserPassword", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database master user password") from exc
    return GetRelationalDatabaseMasterUserPasswordResult(
        master_user_password=resp.get("masterUserPassword"),
        created_at=resp.get("createdAt"),
    )


async def get_relational_database_metric_data(
    relational_database_name: str,
    metric_name: str,
    period: int,
    start_time: str,
    end_time: str,
    unit: str,
    statistics: list[str],
    region_name: str | None = None,
) -> GetRelationalDatabaseMetricDataResult:
    """Get relational database metric data.

    Args:
        relational_database_name: Relational database name.
        metric_name: Metric name.
        period: Period.
        start_time: Start time.
        end_time: End time.
        unit: Unit.
        statistics: Statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    kwargs["metricName"] = metric_name
    kwargs["period"] = period
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    kwargs["unit"] = unit
    kwargs["statistics"] = statistics
    try:
        resp = await client.call("GetRelationalDatabaseMetricData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database metric data") from exc
    return GetRelationalDatabaseMetricDataResult(
        metric_name=resp.get("metricName"),
        metric_data=resp.get("metricData"),
    )


async def get_relational_database_parameters(
    relational_database_name: str,
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseParametersResult:
    """Get relational database parameters.

    Args:
        relational_database_name: Relational database name.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabaseParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database parameters") from exc
    return GetRelationalDatabaseParametersResult(
        parameters=resp.get("parameters"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_relational_database_snapshot(
    relational_database_snapshot_name: str,
    region_name: str | None = None,
) -> GetRelationalDatabaseSnapshotResult:
    """Get relational database snapshot.

    Args:
        relational_database_snapshot_name: Relational database snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseSnapshotName"] = relational_database_snapshot_name
    try:
        resp = await client.call("GetRelationalDatabaseSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database snapshot") from exc
    return GetRelationalDatabaseSnapshotResult(
        relational_database_snapshot=resp.get("relationalDatabaseSnapshot"),
    )


async def get_relational_database_snapshots(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabaseSnapshotsResult:
    """Get relational database snapshots.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabaseSnapshots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational database snapshots") from exc
    return GetRelationalDatabaseSnapshotsResult(
        relational_database_snapshots=resp.get("relationalDatabaseSnapshots"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_relational_databases(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetRelationalDatabasesResult:
    """Get relational databases.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetRelationalDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get relational databases") from exc
    return GetRelationalDatabasesResult(
        relational_databases=resp.get("relationalDatabases"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_setup_history(
    resource_name: str,
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetSetupHistoryResult:
    """Get setup history.

    Args:
        resource_name: Resource name.
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetSetupHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get setup history") from exc
    return GetSetupHistoryResult(
        setup_history=resp.get("setupHistory"),
        next_page_token=resp.get("nextPageToken"),
    )


async def get_static_ips(
    *,
    page_token: str | None = None,
    region_name: str | None = None,
) -> GetStaticIpsResult:
    """Get static ips.

    Args:
        page_token: Page token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if page_token is not None:
        kwargs["pageToken"] = page_token
    try:
        resp = await client.call("GetStaticIps", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get static ips") from exc
    return GetStaticIpsResult(
        static_ips=resp.get("staticIps"),
        next_page_token=resp.get("nextPageToken"),
    )


async def import_key_pair(
    key_pair_name: str,
    public_key_base64: str,
    region_name: str | None = None,
) -> ImportKeyPairResult:
    """Import key pair.

    Args:
        key_pair_name: Key pair name.
        public_key_base64: Public key base64.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyPairName"] = key_pair_name
    kwargs["publicKeyBase64"] = public_key_base64
    try:
        resp = await client.call("ImportKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import key pair") from exc
    return ImportKeyPairResult(
        operation=resp.get("operation"),
    )


async def is_vpc_peered(
    region_name: str | None = None,
) -> IsVpcPeeredResult:
    """Is vpc peered.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("IsVpcPeered", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to is vpc peered") from exc
    return IsVpcPeeredResult(
        is_peered=resp.get("isPeered"),
    )


async def open_instance_public_ports(
    port_info: dict[str, Any],
    instance_name: str,
    region_name: str | None = None,
) -> OpenInstancePublicPortsResult:
    """Open instance public ports.

    Args:
        port_info: Port info.
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portInfo"] = port_info
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("OpenInstancePublicPorts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to open instance public ports") from exc
    return OpenInstancePublicPortsResult(
        operation=resp.get("operation"),
    )


async def peer_vpc(
    region_name: str | None = None,
) -> PeerVpcResult:
    """Peer vpc.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("PeerVpc", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to peer vpc") from exc
    return PeerVpcResult(
        operation=resp.get("operation"),
    )


async def put_alarm(
    alarm_name: str,
    metric_name: str,
    monitored_resource_name: str,
    comparison_operator: str,
    threshold: float,
    evaluation_periods: int,
    *,
    datapoints_to_alarm: int | None = None,
    treat_missing_data: str | None = None,
    contact_protocols: list[str] | None = None,
    notification_triggers: list[str] | None = None,
    notification_enabled: bool | None = None,
    region_name: str | None = None,
) -> PutAlarmResult:
    """Put alarm.

    Args:
        alarm_name: Alarm name.
        metric_name: Metric name.
        monitored_resource_name: Monitored resource name.
        comparison_operator: Comparison operator.
        threshold: Threshold.
        evaluation_periods: Evaluation periods.
        datapoints_to_alarm: Datapoints to alarm.
        treat_missing_data: Treat missing data.
        contact_protocols: Contact protocols.
        notification_triggers: Notification triggers.
        notification_enabled: Notification enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["alarmName"] = alarm_name
    kwargs["metricName"] = metric_name
    kwargs["monitoredResourceName"] = monitored_resource_name
    kwargs["comparisonOperator"] = comparison_operator
    kwargs["threshold"] = threshold
    kwargs["evaluationPeriods"] = evaluation_periods
    if datapoints_to_alarm is not None:
        kwargs["datapointsToAlarm"] = datapoints_to_alarm
    if treat_missing_data is not None:
        kwargs["treatMissingData"] = treat_missing_data
    if contact_protocols is not None:
        kwargs["contactProtocols"] = contact_protocols
    if notification_triggers is not None:
        kwargs["notificationTriggers"] = notification_triggers
    if notification_enabled is not None:
        kwargs["notificationEnabled"] = notification_enabled
    try:
        resp = await client.call("PutAlarm", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put alarm") from exc
    return PutAlarmResult(
        operations=resp.get("operations"),
    )


async def put_instance_public_ports(
    port_infos: list[dict[str, Any]],
    instance_name: str,
    region_name: str | None = None,
) -> PutInstancePublicPortsResult:
    """Put instance public ports.

    Args:
        port_infos: Port infos.
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portInfos"] = port_infos
    kwargs["instanceName"] = instance_name
    try:
        resp = await client.call("PutInstancePublicPorts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put instance public ports") from exc
    return PutInstancePublicPortsResult(
        operation=resp.get("operation"),
    )


async def reboot_relational_database(
    relational_database_name: str,
    region_name: str | None = None,
) -> RebootRelationalDatabaseResult:
    """Reboot relational database.

    Args:
        relational_database_name: Relational database name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    try:
        resp = await client.call("RebootRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reboot relational database") from exc
    return RebootRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def register_container_image(
    service_name: str,
    label: str,
    digest: str,
    region_name: str | None = None,
) -> RegisterContainerImageResult:
    """Register container image.

    Args:
        service_name: Service name.
        label: Label.
        digest: Digest.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    kwargs["label"] = label
    kwargs["digest"] = digest
    try:
        resp = await client.call("RegisterContainerImage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register container image") from exc
    return RegisterContainerImageResult(
        container_image=resp.get("containerImage"),
    )


async def reset_distribution_cache(
    *,
    distribution_name: str | None = None,
    region_name: str | None = None,
) -> ResetDistributionCacheResult:
    """Reset distribution cache.

    Args:
        distribution_name: Distribution name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if distribution_name is not None:
        kwargs["distributionName"] = distribution_name
    try:
        resp = await client.call("ResetDistributionCache", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset distribution cache") from exc
    return ResetDistributionCacheResult(
        status=resp.get("status"),
        create_time=resp.get("createTime"),
        operation=resp.get("operation"),
    )


async def run_alarm(
    alarm_name: str,
    state: str,
    region_name: str | None = None,
) -> RunAlarmResult:
    """Run alarm.

    Args:
        alarm_name: Alarm name.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["alarmName"] = alarm_name
    kwargs["state"] = state
    try:
        resp = await client.call("TestAlarm", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run alarm") from exc
    return RunAlarmResult(
        operations=resp.get("operations"),
    )


async def send_contact_method_verification(
    protocol: str,
    region_name: str | None = None,
) -> SendContactMethodVerificationResult:
    """Send contact method verification.

    Args:
        protocol: Protocol.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["protocol"] = protocol
    try:
        resp = await client.call("SendContactMethodVerification", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send contact method verification") from exc
    return SendContactMethodVerificationResult(
        operations=resp.get("operations"),
    )


async def set_ip_address_type(
    resource_type: str,
    resource_name: str,
    ip_address_type: str,
    *,
    accept_bundle_update: bool | None = None,
    region_name: str | None = None,
) -> SetIpAddressTypeResult:
    """Set ip address type.

    Args:
        resource_type: Resource type.
        resource_name: Resource name.
        ip_address_type: Ip address type.
        accept_bundle_update: Accept bundle update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceType"] = resource_type
    kwargs["resourceName"] = resource_name
    kwargs["ipAddressType"] = ip_address_type
    if accept_bundle_update is not None:
        kwargs["acceptBundleUpdate"] = accept_bundle_update
    try:
        resp = await client.call("SetIpAddressType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set ip address type") from exc
    return SetIpAddressTypeResult(
        operations=resp.get("operations"),
    )


async def set_resource_access_for_bucket(
    resource_name: str,
    bucket_name: str,
    access: str,
    region_name: str | None = None,
) -> SetResourceAccessForBucketResult:
    """Set resource access for bucket.

    Args:
        resource_name: Resource name.
        bucket_name: Bucket name.
        access: Access.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["bucketName"] = bucket_name
    kwargs["access"] = access
    try:
        resp = await client.call("SetResourceAccessForBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set resource access for bucket") from exc
    return SetResourceAccessForBucketResult(
        operations=resp.get("operations"),
    )


async def setup_instance_https(
    instance_name: str,
    email_address: str,
    domain_names: list[str],
    certificate_provider: str,
    region_name: str | None = None,
) -> SetupInstanceHttpsResult:
    """Setup instance https.

    Args:
        instance_name: Instance name.
        email_address: Email address.
        domain_names: Domain names.
        certificate_provider: Certificate provider.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    kwargs["emailAddress"] = email_address
    kwargs["domainNames"] = domain_names
    kwargs["certificateProvider"] = certificate_provider
    try:
        resp = await client.call("SetupInstanceHttps", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to setup instance https") from exc
    return SetupInstanceHttpsResult(
        operations=resp.get("operations"),
    )


async def start_gui_session(
    resource_name: str,
    region_name: str | None = None,
) -> StartGuiSessionResult:
    """Start gui session.

    Args:
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    try:
        resp = await client.call("StartGUISession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start gui session") from exc
    return StartGuiSessionResult(
        operations=resp.get("operations"),
    )


async def start_relational_database(
    relational_database_name: str,
    region_name: str | None = None,
) -> StartRelationalDatabaseResult:
    """Start relational database.

    Args:
        relational_database_name: Relational database name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    try:
        resp = await client.call("StartRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start relational database") from exc
    return StartRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def stop_gui_session(
    resource_name: str,
    region_name: str | None = None,
) -> StopGuiSessionResult:
    """Stop gui session.

    Args:
        resource_name: Resource name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    try:
        resp = await client.call("StopGUISession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop gui session") from exc
    return StopGuiSessionResult(
        operations=resp.get("operations"),
    )


async def stop_relational_database(
    relational_database_name: str,
    *,
    relational_database_snapshot_name: str | None = None,
    region_name: str | None = None,
) -> StopRelationalDatabaseResult:
    """Stop relational database.

    Args:
        relational_database_name: Relational database name.
        relational_database_snapshot_name: Relational database snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if relational_database_snapshot_name is not None:
        kwargs["relationalDatabaseSnapshotName"] = relational_database_snapshot_name
    try:
        resp = await client.call("StopRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop relational database") from exc
    return StopRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def tag_resource(
    resource_name: str,
    tags: list[dict[str, Any]],
    *,
    resource_arn: str | None = None,
    region_name: str | None = None,
) -> TagResourceResult:
    """Tag resource.

    Args:
        resource_name: Resource name.
        tags: Tags.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["tags"] = tags
    if resource_arn is not None:
        kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return TagResourceResult(
        operations=resp.get("operations"),
    )


async def unpeer_vpc(
    region_name: str | None = None,
) -> UnpeerVpcResult:
    """Unpeer vpc.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("UnpeerVpc", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to unpeer vpc") from exc
    return UnpeerVpcResult(
        operation=resp.get("operation"),
    )


async def untag_resource(
    resource_name: str,
    tag_keys: list[str],
    *,
    resource_arn: str | None = None,
    region_name: str | None = None,
) -> UntagResourceResult:
    """Untag resource.

    Args:
        resource_name: Resource name.
        tag_keys: Tag keys.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceName"] = resource_name
    kwargs["tagKeys"] = tag_keys
    if resource_arn is not None:
        kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return UntagResourceResult(
        operations=resp.get("operations"),
    )


async def update_bucket(
    bucket_name: str,
    *,
    access_rules: dict[str, Any] | None = None,
    versioning: str | None = None,
    readonly_access_accounts: list[str] | None = None,
    access_log_config: dict[str, Any] | None = None,
    cors: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateBucketResult:
    """Update bucket.

    Args:
        bucket_name: Bucket name.
        access_rules: Access rules.
        versioning: Versioning.
        readonly_access_accounts: Readonly access accounts.
        access_log_config: Access log config.
        cors: Cors.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    if access_rules is not None:
        kwargs["accessRules"] = access_rules
    if versioning is not None:
        kwargs["versioning"] = versioning
    if readonly_access_accounts is not None:
        kwargs["readonlyAccessAccounts"] = readonly_access_accounts
    if access_log_config is not None:
        kwargs["accessLogConfig"] = access_log_config
    if cors is not None:
        kwargs["cors"] = cors
    try:
        resp = await client.call("UpdateBucket", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bucket") from exc
    return UpdateBucketResult(
        bucket=resp.get("bucket"),
        operations=resp.get("operations"),
    )


async def update_bucket_bundle(
    bucket_name: str,
    bundle_id: str,
    region_name: str | None = None,
) -> UpdateBucketBundleResult:
    """Update bucket bundle.

    Args:
        bucket_name: Bucket name.
        bundle_id: Bundle id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["bucketName"] = bucket_name
    kwargs["bundleId"] = bundle_id
    try:
        resp = await client.call("UpdateBucketBundle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update bucket bundle") from exc
    return UpdateBucketBundleResult(
        operations=resp.get("operations"),
    )


async def update_container_service(
    service_name: str,
    *,
    power: str | None = None,
    scale: int | None = None,
    is_disabled: bool | None = None,
    public_domain_names: dict[str, Any] | None = None,
    private_registry_access: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateContainerServiceResult:
    """Update container service.

    Args:
        service_name: Service name.
        power: Power.
        scale: Scale.
        is_disabled: Is disabled.
        public_domain_names: Public domain names.
        private_registry_access: Private registry access.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    if power is not None:
        kwargs["power"] = power
    if scale is not None:
        kwargs["scale"] = scale
    if is_disabled is not None:
        kwargs["isDisabled"] = is_disabled
    if public_domain_names is not None:
        kwargs["publicDomainNames"] = public_domain_names
    if private_registry_access is not None:
        kwargs["privateRegistryAccess"] = private_registry_access
    try:
        resp = await client.call("UpdateContainerService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update container service") from exc
    return UpdateContainerServiceResult(
        container_service=resp.get("containerService"),
    )


async def update_distribution(
    distribution_name: str,
    *,
    origin: dict[str, Any] | None = None,
    default_cache_behavior: dict[str, Any] | None = None,
    cache_behavior_settings: dict[str, Any] | None = None,
    cache_behaviors: list[dict[str, Any]] | None = None,
    is_enabled: bool | None = None,
    viewer_minimum_tls_protocol_version: str | None = None,
    certificate_name: str | None = None,
    use_default_certificate: bool | None = None,
    region_name: str | None = None,
) -> UpdateDistributionResult:
    """Update distribution.

    Args:
        distribution_name: Distribution name.
        origin: Origin.
        default_cache_behavior: Default cache behavior.
        cache_behavior_settings: Cache behavior settings.
        cache_behaviors: Cache behaviors.
        is_enabled: Is enabled.
        viewer_minimum_tls_protocol_version: Viewer minimum tls protocol version.
        certificate_name: Certificate name.
        use_default_certificate: Use default certificate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["distributionName"] = distribution_name
    if origin is not None:
        kwargs["origin"] = origin
    if default_cache_behavior is not None:
        kwargs["defaultCacheBehavior"] = default_cache_behavior
    if cache_behavior_settings is not None:
        kwargs["cacheBehaviorSettings"] = cache_behavior_settings
    if cache_behaviors is not None:
        kwargs["cacheBehaviors"] = cache_behaviors
    if is_enabled is not None:
        kwargs["isEnabled"] = is_enabled
    if viewer_minimum_tls_protocol_version is not None:
        kwargs["viewerMinimumTlsProtocolVersion"] = viewer_minimum_tls_protocol_version
    if certificate_name is not None:
        kwargs["certificateName"] = certificate_name
    if use_default_certificate is not None:
        kwargs["useDefaultCertificate"] = use_default_certificate
    try:
        resp = await client.call("UpdateDistribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update distribution") from exc
    return UpdateDistributionResult(
        operation=resp.get("operation"),
    )


async def update_distribution_bundle(
    *,
    distribution_name: str | None = None,
    bundle_id: str | None = None,
    region_name: str | None = None,
) -> UpdateDistributionBundleResult:
    """Update distribution bundle.

    Args:
        distribution_name: Distribution name.
        bundle_id: Bundle id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    if distribution_name is not None:
        kwargs["distributionName"] = distribution_name
    if bundle_id is not None:
        kwargs["bundleId"] = bundle_id
    try:
        resp = await client.call("UpdateDistributionBundle", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update distribution bundle") from exc
    return UpdateDistributionBundleResult(
        operation=resp.get("operation"),
    )


async def update_domain_entry(
    domain_name: str,
    domain_entry: dict[str, Any],
    region_name: str | None = None,
) -> UpdateDomainEntryResult:
    """Update domain entry.

    Args:
        domain_name: Domain name.
        domain_entry: Domain entry.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["domainEntry"] = domain_entry
    try:
        resp = await client.call("UpdateDomainEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update domain entry") from exc
    return UpdateDomainEntryResult(
        operations=resp.get("operations"),
    )


async def update_instance_metadata_options(
    instance_name: str,
    *,
    http_tokens: str | None = None,
    http_endpoint: str | None = None,
    http_put_response_hop_limit: int | None = None,
    http_protocol_ipv6: str | None = None,
    region_name: str | None = None,
) -> UpdateInstanceMetadataOptionsResult:
    """Update instance metadata options.

    Args:
        instance_name: Instance name.
        http_tokens: Http tokens.
        http_endpoint: Http endpoint.
        http_put_response_hop_limit: Http put response hop limit.
        http_protocol_ipv6: Http protocol ipv6.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    if http_tokens is not None:
        kwargs["httpTokens"] = http_tokens
    if http_endpoint is not None:
        kwargs["httpEndpoint"] = http_endpoint
    if http_put_response_hop_limit is not None:
        kwargs["httpPutResponseHopLimit"] = http_put_response_hop_limit
    if http_protocol_ipv6 is not None:
        kwargs["httpProtocolIpv6"] = http_protocol_ipv6
    try:
        resp = await client.call("UpdateInstanceMetadataOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update instance metadata options") from exc
    return UpdateInstanceMetadataOptionsResult(
        operation=resp.get("operation"),
    )


async def update_load_balancer_attribute(
    load_balancer_name: str,
    attribute_name: str,
    attribute_value: str,
    region_name: str | None = None,
) -> UpdateLoadBalancerAttributeResult:
    """Update load balancer attribute.

    Args:
        load_balancer_name: Load balancer name.
        attribute_name: Attribute name.
        attribute_value: Attribute value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loadBalancerName"] = load_balancer_name
    kwargs["attributeName"] = attribute_name
    kwargs["attributeValue"] = attribute_value
    try:
        resp = await client.call("UpdateLoadBalancerAttribute", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update load balancer attribute") from exc
    return UpdateLoadBalancerAttributeResult(
        operations=resp.get("operations"),
    )


async def update_relational_database(
    relational_database_name: str,
    *,
    master_user_password: str | None = None,
    rotate_master_user_password: bool | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    enable_backup_retention: bool | None = None,
    disable_backup_retention: bool | None = None,
    publicly_accessible: bool | None = None,
    apply_immediately: bool | None = None,
    ca_certificate_identifier: str | None = None,
    relational_database_blueprint_id: str | None = None,
    region_name: str | None = None,
) -> UpdateRelationalDatabaseResult:
    """Update relational database.

    Args:
        relational_database_name: Relational database name.
        master_user_password: Master user password.
        rotate_master_user_password: Rotate master user password.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        enable_backup_retention: Enable backup retention.
        disable_backup_retention: Disable backup retention.
        publicly_accessible: Publicly accessible.
        apply_immediately: Apply immediately.
        ca_certificate_identifier: Ca certificate identifier.
        relational_database_blueprint_id: Relational database blueprint id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    if master_user_password is not None:
        kwargs["masterUserPassword"] = master_user_password
    if rotate_master_user_password is not None:
        kwargs["rotateMasterUserPassword"] = rotate_master_user_password
    if preferred_backup_window is not None:
        kwargs["preferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["preferredMaintenanceWindow"] = preferred_maintenance_window
    if enable_backup_retention is not None:
        kwargs["enableBackupRetention"] = enable_backup_retention
    if disable_backup_retention is not None:
        kwargs["disableBackupRetention"] = disable_backup_retention
    if publicly_accessible is not None:
        kwargs["publiclyAccessible"] = publicly_accessible
    if apply_immediately is not None:
        kwargs["applyImmediately"] = apply_immediately
    if ca_certificate_identifier is not None:
        kwargs["caCertificateIdentifier"] = ca_certificate_identifier
    if relational_database_blueprint_id is not None:
        kwargs["relationalDatabaseBlueprintId"] = relational_database_blueprint_id
    try:
        resp = await client.call("UpdateRelationalDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update relational database") from exc
    return UpdateRelationalDatabaseResult(
        operations=resp.get("operations"),
    )


async def update_relational_database_parameters(
    relational_database_name: str,
    parameters: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateRelationalDatabaseParametersResult:
    """Update relational database parameters.

    Args:
        relational_database_name: Relational database name.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("lightsail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["relationalDatabaseName"] = relational_database_name
    kwargs["parameters"] = parameters
    try:
        resp = await client.call("UpdateRelationalDatabaseParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update relational database parameters") from exc
    return UpdateRelationalDatabaseParametersResult(
        operations=resp.get("operations"),
    )
