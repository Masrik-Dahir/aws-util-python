"""Tests for aws_util.aio.lightsail -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.lightsail import (
    DatabaseResult,
    InstanceResult,
    SnapshotResult,
    StaticIpResult,
    allocate_static_ip,
    create_database,
    create_instance_snapshot,
    create_instances,
    delete_database,
    delete_instance,
    delete_instance_snapshot,
    get_database,
    get_databases,
    get_instance,
    get_instance_snapshots,
    get_instances,
    get_static_ip,
    reboot_instance,
    release_static_ip,
    start_instance,
    stop_instance,
    attach_certificate_to_distribution,
    attach_disk,
    attach_instances_to_load_balancer,
    attach_load_balancer_tls_certificate,
    attach_static_ip,
    close_instance_public_ports,
    copy_snapshot,
    create_bucket,
    create_bucket_access_key,
    create_certificate,
    create_cloud_formation_stack,
    create_contact_method,
    create_container_service,
    create_container_service_deployment,
    create_container_service_registry_login,
    create_disk,
    create_disk_from_snapshot,
    create_disk_snapshot,
    create_distribution,
    create_domain,
    create_domain_entry,
    create_gui_session_access_details,
    create_instances_from_snapshot,
    create_key_pair,
    create_load_balancer,
    create_load_balancer_tls_certificate,
    create_relational_database,
    create_relational_database_from_snapshot,
    create_relational_database_snapshot,
    delete_alarm,
    delete_auto_snapshot,
    delete_bucket,
    delete_bucket_access_key,
    delete_certificate,
    delete_contact_method,
    delete_container_image,
    delete_container_service,
    delete_disk,
    delete_disk_snapshot,
    delete_distribution,
    delete_domain,
    delete_domain_entry,
    delete_key_pair,
    delete_known_host_keys,
    delete_load_balancer,
    delete_load_balancer_tls_certificate,
    delete_relational_database,
    delete_relational_database_snapshot,
    detach_certificate_from_distribution,
    detach_disk,
    detach_instances_from_load_balancer,
    detach_static_ip,
    disable_add_on,
    download_default_key_pair,
    enable_add_on,
    export_snapshot,
    get_active_names,
    get_alarms,
    get_auto_snapshots,
    get_blueprints,
    get_bucket_access_keys,
    get_bucket_bundles,
    get_bucket_metric_data,
    get_buckets,
    get_bundles,
    get_certificates,
    get_cloud_formation_stack_records,
    get_contact_methods,
    get_container_api_metadata,
    get_container_images,
    get_container_log,
    get_container_service_deployments,
    get_container_service_metric_data,
    get_container_service_powers,
    get_container_services,
    get_cost_estimate,
    get_disk,
    get_disk_snapshot,
    get_disk_snapshots,
    get_disks,
    get_distribution_bundles,
    get_distribution_latest_cache_reset,
    get_distribution_metric_data,
    get_distributions,
    get_domain,
    get_domains,
    get_export_snapshot_records,
    get_instance_access_details,
    get_instance_metric_data,
    get_instance_port_states,
    get_instance_snapshot,
    get_instance_state,
    get_key_pair,
    get_key_pairs,
    get_load_balancer,
    get_load_balancer_metric_data,
    get_load_balancer_tls_certificates,
    get_load_balancer_tls_policies,
    get_load_balancers,
    get_operation,
    get_operations,
    get_operations_for_resource,
    get_regions,
    get_relational_database,
    get_relational_database_blueprints,
    get_relational_database_bundles,
    get_relational_database_events,
    get_relational_database_log_events,
    get_relational_database_log_streams,
    get_relational_database_master_user_password,
    get_relational_database_metric_data,
    get_relational_database_parameters,
    get_relational_database_snapshot,
    get_relational_database_snapshots,
    get_relational_databases,
    get_setup_history,
    get_static_ips,
    import_key_pair,
    is_vpc_peered,
    open_instance_public_ports,
    peer_vpc,
    put_alarm,
    put_instance_public_ports,
    reboot_relational_database,
    register_container_image,
    reset_distribution_cache,
    run_alarm,
    send_contact_method_verification,
    set_ip_address_type,
    set_resource_access_for_bucket,
    setup_instance_https,
    start_gui_session,
    start_relational_database,
    stop_gui_session,
    stop_relational_database,
    tag_resource,
    unpeer_vpc,
    untag_resource,
    update_bucket,
    update_bucket_bundle,
    update_container_service,
    update_distribution,
    update_distribution_bundle,
    update_domain_entry,
    update_instance_metadata_options,
    update_load_balancer_attribute,
    update_relational_database,
    update_relational_database_parameters,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


_PATCH = "aws_util.aio.lightsail.async_client"


# ---------------------------------------------------------------------------
# create_instances
# ---------------------------------------------------------------------------


async def test_create_instances_ok(monkeypatch):
    mc = _mc({"operations": [{"resourceName": "i1", "status": "Succeeded"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_instances(
        ["i1"], availability_zone="a", blueprint_id="b", bundle_id="c",
    )
    assert len(r) == 1
    assert r[0].name == "i1"


async def test_create_instances_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_instances failed"):
        await create_instances(
            ["i1"], availability_zone="a",
            blueprint_id="b", bundle_id="c",
        )


# ---------------------------------------------------------------------------
# get_instance / get_instances
# ---------------------------------------------------------------------------


async def test_get_instance_ok(monkeypatch):
    mc = _mc({
        "instance": {
            "name": "i1", "state": {"name": "running"},
            "location": {"regionName": "us-east-1"},
        },
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_instance("i1")
    assert r.name == "i1"


async def test_get_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_instance failed"):
        await get_instance("i1")


async def test_get_instances_ok(monkeypatch):
    mc = _mc({
        "instances": [
            {"name": "i1", "state": {"name": "running"}, "location": {}},
        ],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_instances()
    assert len(r) == 1


async def test_get_instances_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_instances failed"):
        await get_instances()


# ---------------------------------------------------------------------------
# delete / start / stop / reboot
# ---------------------------------------------------------------------------


async def test_delete_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_instance("i1")
    mc.call.assert_awaited_once()


async def test_delete_instance_force(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_instance("i1", force=True)


async def test_delete_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_instance failed"):
        await delete_instance("i1")


async def test_start_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await start_instance("i1")


async def test_start_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="start_instance failed"):
        await start_instance("i1")


async def test_stop_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await stop_instance("i1")


async def test_stop_instance_force(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await stop_instance("i1", force=True)


async def test_stop_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="stop_instance failed"):
        await stop_instance("i1")


async def test_reboot_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await reboot_instance("i1")


async def test_reboot_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="reboot_instance failed"):
        await reboot_instance("i1")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def test_create_instance_snapshot_with_ops(monkeypatch):
    mc = _mc({"operations": [{"status": "Succeeded"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_instance_snapshot("i1", "snap1")
    assert r.name == "snap1"
    assert r.state == "Succeeded"
    assert r.from_instance_name == "i1"


async def test_create_instance_snapshot_no_ops(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_instance_snapshot("i1", "snap1")
    assert r.name == "snap1"
    assert r.from_instance_name == "i1"


async def test_create_instance_snapshot_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_instance_snapshot"):
        await create_instance_snapshot("i1", "snap1")


async def test_get_instance_snapshots_ok(monkeypatch):
    mc = _mc({
        "instanceSnapshots": [{"name": "s1", "state": "available"}],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_instance_snapshots()
    assert len(r) == 1


async def test_get_instance_snapshots_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_instance_snapshots"):
        await get_instance_snapshots()


async def test_delete_instance_snapshot_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_instance_snapshot("snap1")


async def test_delete_instance_snapshot_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_instance_snapshot"):
        await delete_instance_snapshot("snap1")


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


async def test_create_database_with_ops(monkeypatch):
    mc = _mc({"operations": [{"status": "Succeeded"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_database(
        "db1", availability_zone="a",
        master_database_name="mydb",
        master_username="admin",
        master_user_password="pass",
    )
    assert r.name == "db1"
    assert r.state == "Succeeded"
    assert r.master_username == "admin"


async def test_create_database_no_ops(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_database(
        "db1", availability_zone="a",
        master_database_name="mydb",
        master_username="admin",
        master_user_password="pass",
    )
    assert r.name == "db1"


async def test_create_database_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_database failed"):
        await create_database(
            "db1", availability_zone="a",
            master_database_name="mydb",
            master_username="admin",
            master_user_password="pass",
        )


async def test_get_database_ok(monkeypatch):
    mc = _mc({
        "relationalDatabase": {
            "name": "db1", "state": "available",
            "engine": "mysql",
        },
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_database("db1")
    assert r.name == "db1"


async def test_get_database_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_database failed"):
        await get_database("db1")


async def test_get_databases_ok(monkeypatch):
    mc = _mc({
        "relationalDatabases": [{"name": "db1", "state": "available"}],
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_databases()
    assert len(r) == 1


async def test_get_databases_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_databases failed"):
        await get_databases()


async def test_delete_database_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_database("db1")


async def test_delete_database_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_database failed"):
        await delete_database("db1")


# ---------------------------------------------------------------------------
# Static IP operations
# ---------------------------------------------------------------------------


async def test_allocate_static_ip_with_ops(monkeypatch):
    mc = _mc({"operations": [{"status": "Succeeded"}]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await allocate_static_ip("ip1")
    assert r.name == "ip1"


async def test_allocate_static_ip_no_ops(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await allocate_static_ip("ip1")
    assert r.name == "ip1"


async def test_allocate_static_ip_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="allocate_static_ip failed"):
        await allocate_static_ip("ip1")


async def test_get_static_ip_ok(monkeypatch):
    mc = _mc({
        "staticIp": {"name": "ip1", "ipAddress": "1.2.3.4"},
    })
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await get_static_ip("ip1")
    assert r.ip_address == "1.2.3.4"


async def test_get_static_ip_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_static_ip failed"):
        await get_static_ip("ip1")


async def test_release_static_ip_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await release_static_ip("ip1")


async def test_release_static_ip_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="release_static_ip failed"):
        await release_static_ip("ip1")


async def test_attach_certificate_to_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_certificate_to_distribution("test-distribution_name", "test-certificate_name", )
    mock_client.call.assert_called_once()


async def test_attach_certificate_to_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_certificate_to_distribution("test-distribution_name", "test-certificate_name", )


async def test_attach_disk(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_disk("test-disk_name", "test-instance_name", "test-disk_path", )
    mock_client.call.assert_called_once()


async def test_attach_disk_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_disk("test-disk_name", "test-instance_name", "test-disk_path", )


async def test_attach_instances_to_load_balancer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_instances_to_load_balancer("test-load_balancer_name", [], )
    mock_client.call.assert_called_once()


async def test_attach_instances_to_load_balancer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_instances_to_load_balancer("test-load_balancer_name", [], )


async def test_attach_load_balancer_tls_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", )
    mock_client.call.assert_called_once()


async def test_attach_load_balancer_tls_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", )


async def test_attach_static_ip(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_static_ip("test-static_ip_name", "test-instance_name", )
    mock_client.call.assert_called_once()


async def test_attach_static_ip_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_static_ip("test-static_ip_name", "test-instance_name", )


async def test_close_instance_public_ports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await close_instance_public_ports({}, "test-instance_name", )
    mock_client.call.assert_called_once()


async def test_close_instance_public_ports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await close_instance_public_ports({}, "test-instance_name", )


async def test_copy_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_snapshot("test-target_snapshot_name", "test-source_region", )
    mock_client.call.assert_called_once()


async def test_copy_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_snapshot("test-target_snapshot_name", "test-source_region", )


async def test_create_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bucket("test-bucket_name", "test-bundle_id", )
    mock_client.call.assert_called_once()


async def test_create_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bucket("test-bucket_name", "test-bundle_id", )


async def test_create_bucket_access_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bucket_access_key("test-bucket_name", )
    mock_client.call.assert_called_once()


async def test_create_bucket_access_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bucket_access_key("test-bucket_name", )


async def test_create_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_certificate("test-certificate_name", "test-domain_name", )
    mock_client.call.assert_called_once()


async def test_create_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_certificate("test-certificate_name", "test-domain_name", )


async def test_create_cloud_formation_stack(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cloud_formation_stack([], )
    mock_client.call.assert_called_once()


async def test_create_cloud_formation_stack_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cloud_formation_stack([], )


async def test_create_contact_method(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_contact_method("test-protocol", "test-contact_endpoint", )
    mock_client.call.assert_called_once()


async def test_create_contact_method_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_contact_method("test-protocol", "test-contact_endpoint", )


async def test_create_container_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_container_service("test-service_name", "test-power", 1, )
    mock_client.call.assert_called_once()


async def test_create_container_service_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_container_service("test-service_name", "test-power", 1, )


async def test_create_container_service_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_container_service_deployment("test-service_name", )
    mock_client.call.assert_called_once()


async def test_create_container_service_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_container_service_deployment("test-service_name", )


async def test_create_container_service_registry_login(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_container_service_registry_login()
    mock_client.call.assert_called_once()


async def test_create_container_service_registry_login_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_container_service_registry_login()


async def test_create_disk(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_disk("test-disk_name", "test-availability_zone", 1, )
    mock_client.call.assert_called_once()


async def test_create_disk_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_disk("test-disk_name", "test-availability_zone", 1, )


async def test_create_disk_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, )
    mock_client.call.assert_called_once()


async def test_create_disk_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, )


async def test_create_disk_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_disk_snapshot("test-disk_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_create_disk_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_disk_snapshot("test-disk_snapshot_name", )


async def test_create_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_distribution("test-distribution_name", {}, {}, "test-bundle_id", )
    mock_client.call.assert_called_once()


async def test_create_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_distribution("test-distribution_name", {}, {}, "test-bundle_id", )


async def test_create_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_domain("test-domain_name", )
    mock_client.call.assert_called_once()


async def test_create_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_domain("test-domain_name", )


async def test_create_domain_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_domain_entry("test-domain_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_domain_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_domain_entry("test-domain_name", {}, )


async def test_create_gui_session_access_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_gui_session_access_details("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_create_gui_session_access_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_gui_session_access_details("test-resource_name", )


async def test_create_instances_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instances_from_snapshot([], "test-availability_zone", "test-bundle_id", )
    mock_client.call.assert_called_once()


async def test_create_instances_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instances_from_snapshot([], "test-availability_zone", "test-bundle_id", )


async def test_create_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_key_pair("test-key_pair_name", )
    mock_client.call.assert_called_once()


async def test_create_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_key_pair("test-key_pair_name", )


async def test_create_load_balancer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_load_balancer("test-load_balancer_name", 1, )
    mock_client.call.assert_called_once()


async def test_create_load_balancer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_load_balancer("test-load_balancer_name", 1, )


async def test_create_load_balancer_tls_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", )
    mock_client.call.assert_called_once()


async def test_create_load_balancer_tls_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", )


async def test_create_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", )
    mock_client.call.assert_called_once()


async def test_create_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", )


async def test_create_relational_database_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_relational_database_from_snapshot("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_create_relational_database_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_relational_database_from_snapshot("test-relational_database_name", )


async def test_create_relational_database_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_create_relational_database_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", )


async def test_delete_alarm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_alarm("test-alarm_name", )
    mock_client.call.assert_called_once()


async def test_delete_alarm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_alarm("test-alarm_name", )


async def test_delete_auto_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_auto_snapshot("test-resource_name", "test-date", )
    mock_client.call.assert_called_once()


async def test_delete_auto_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_auto_snapshot("test-resource_name", "test-date", )


async def test_delete_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket("test-bucket_name", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket("test-bucket_name", )


async def test_delete_bucket_access_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bucket_access_key("test-bucket_name", "test-access_key_id", )
    mock_client.call.assert_called_once()


async def test_delete_bucket_access_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bucket_access_key("test-bucket_name", "test-access_key_id", )


async def test_delete_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_certificate("test-certificate_name", )
    mock_client.call.assert_called_once()


async def test_delete_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_certificate("test-certificate_name", )


async def test_delete_contact_method(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_contact_method("test-protocol", )
    mock_client.call.assert_called_once()


async def test_delete_contact_method_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_method("test-protocol", )


async def test_delete_container_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_container_image("test-service_name", "test-image", )
    mock_client.call.assert_called_once()


async def test_delete_container_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_container_image("test-service_name", "test-image", )


async def test_delete_container_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_container_service("test-service_name", )
    mock_client.call.assert_called_once()


async def test_delete_container_service_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_container_service("test-service_name", )


async def test_delete_disk(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_disk("test-disk_name", )
    mock_client.call.assert_called_once()


async def test_delete_disk_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_disk("test-disk_name", )


async def test_delete_disk_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_disk_snapshot("test-disk_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_delete_disk_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_disk_snapshot("test-disk_snapshot_name", )


async def test_delete_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_distribution()
    mock_client.call.assert_called_once()


async def test_delete_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_distribution()


async def test_delete_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_domain("test-domain_name", )
    mock_client.call.assert_called_once()


async def test_delete_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_domain("test-domain_name", )


async def test_delete_domain_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_domain_entry("test-domain_name", {}, )
    mock_client.call.assert_called_once()


async def test_delete_domain_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_domain_entry("test-domain_name", {}, )


async def test_delete_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_key_pair("test-key_pair_name", )
    mock_client.call.assert_called_once()


async def test_delete_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_key_pair("test-key_pair_name", )


async def test_delete_known_host_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_known_host_keys("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_delete_known_host_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_known_host_keys("test-instance_name", )


async def test_delete_load_balancer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_load_balancer("test-load_balancer_name", )
    mock_client.call.assert_called_once()


async def test_delete_load_balancer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_load_balancer("test-load_balancer_name", )


async def test_delete_load_balancer_tls_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", )
    mock_client.call.assert_called_once()


async def test_delete_load_balancer_tls_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", )


async def test_delete_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_delete_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_relational_database("test-relational_database_name", )


async def test_delete_relational_database_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_relational_database_snapshot("test-relational_database_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_delete_relational_database_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_relational_database_snapshot("test-relational_database_snapshot_name", )


async def test_detach_certificate_from_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_certificate_from_distribution("test-distribution_name", )
    mock_client.call.assert_called_once()


async def test_detach_certificate_from_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_certificate_from_distribution("test-distribution_name", )


async def test_detach_disk(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_disk("test-disk_name", )
    mock_client.call.assert_called_once()


async def test_detach_disk_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_disk("test-disk_name", )


async def test_detach_instances_from_load_balancer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_instances_from_load_balancer("test-load_balancer_name", [], )
    mock_client.call.assert_called_once()


async def test_detach_instances_from_load_balancer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_instances_from_load_balancer("test-load_balancer_name", [], )


async def test_detach_static_ip(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_static_ip("test-static_ip_name", )
    mock_client.call.assert_called_once()


async def test_detach_static_ip_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_static_ip("test-static_ip_name", )


async def test_disable_add_on(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_add_on("test-add_on_type", "test-resource_name", )
    mock_client.call.assert_called_once()


async def test_disable_add_on_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_add_on("test-add_on_type", "test-resource_name", )


async def test_download_default_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await download_default_key_pair()
    mock_client.call.assert_called_once()


async def test_download_default_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await download_default_key_pair()


async def test_enable_add_on(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_add_on("test-resource_name", {}, )
    mock_client.call.assert_called_once()


async def test_enable_add_on_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_add_on("test-resource_name", {}, )


async def test_export_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_snapshot("test-source_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_export_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_snapshot("test-source_snapshot_name", )


async def test_get_active_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_active_names()
    mock_client.call.assert_called_once()


async def test_get_active_names_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_active_names()


async def test_get_alarms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_alarms()
    mock_client.call.assert_called_once()


async def test_get_alarms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_alarms()


async def test_get_auto_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_auto_snapshots("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_get_auto_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_auto_snapshots("test-resource_name", )


async def test_get_blueprints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_blueprints()
    mock_client.call.assert_called_once()


async def test_get_blueprints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_blueprints()


async def test_get_bucket_access_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_access_keys("test-bucket_name", )
    mock_client.call.assert_called_once()


async def test_get_bucket_access_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_access_keys("test-bucket_name", )


async def test_get_bucket_bundles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_bundles()
    mock_client.call.assert_called_once()


async def test_get_bucket_bundles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_bundles()


async def test_get_bucket_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bucket_metric_data("test-bucket_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], "test-unit", )
    mock_client.call.assert_called_once()


async def test_get_bucket_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bucket_metric_data("test-bucket_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], "test-unit", )


async def test_get_buckets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_buckets()
    mock_client.call.assert_called_once()


async def test_get_buckets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_buckets()


async def test_get_bundles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_bundles()
    mock_client.call.assert_called_once()


async def test_get_bundles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_bundles()


async def test_get_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_certificates()
    mock_client.call.assert_called_once()


async def test_get_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_certificates()


async def test_get_cloud_formation_stack_records(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cloud_formation_stack_records()
    mock_client.call.assert_called_once()


async def test_get_cloud_formation_stack_records_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cloud_formation_stack_records()


async def test_get_contact_methods(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_contact_methods()
    mock_client.call.assert_called_once()


async def test_get_contact_methods_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_contact_methods()


async def test_get_container_api_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_api_metadata()
    mock_client.call.assert_called_once()


async def test_get_container_api_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_api_metadata()


async def test_get_container_images(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_images("test-service_name", )
    mock_client.call.assert_called_once()


async def test_get_container_images_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_images("test-service_name", )


async def test_get_container_log(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_log("test-service_name", "test-container_name", )
    mock_client.call.assert_called_once()


async def test_get_container_log_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_log("test-service_name", "test-container_name", )


async def test_get_container_service_deployments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_service_deployments("test-service_name", )
    mock_client.call.assert_called_once()


async def test_get_container_service_deployments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_service_deployments("test-service_name", )


async def test_get_container_service_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_service_metric_data("test-service_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], )
    mock_client.call.assert_called_once()


async def test_get_container_service_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_service_metric_data("test-service_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], )


async def test_get_container_service_powers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_service_powers()
    mock_client.call.assert_called_once()


async def test_get_container_service_powers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_service_powers()


async def test_get_container_services(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_container_services()
    mock_client.call.assert_called_once()


async def test_get_container_services_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_container_services()


async def test_get_cost_estimate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cost_estimate("test-resource_name", "test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_get_cost_estimate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cost_estimate("test-resource_name", "test-start_time", "test-end_time", )


async def test_get_disk(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_disk("test-disk_name", )
    mock_client.call.assert_called_once()


async def test_get_disk_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_disk("test-disk_name", )


async def test_get_disk_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_disk_snapshot("test-disk_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_get_disk_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_disk_snapshot("test-disk_snapshot_name", )


async def test_get_disk_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_disk_snapshots()
    mock_client.call.assert_called_once()


async def test_get_disk_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_disk_snapshots()


async def test_get_disks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_disks()
    mock_client.call.assert_called_once()


async def test_get_disks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_disks()


async def test_get_distribution_bundles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_distribution_bundles()
    mock_client.call.assert_called_once()


async def test_get_distribution_bundles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_bundles()


async def test_get_distribution_latest_cache_reset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_distribution_latest_cache_reset()
    mock_client.call.assert_called_once()


async def test_get_distribution_latest_cache_reset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_latest_cache_reset()


async def test_get_distribution_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_distribution_metric_data("test-distribution_name", "test-metric_name", "test-start_time", "test-end_time", 1, "test-unit", [], )
    mock_client.call.assert_called_once()


async def test_get_distribution_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_distribution_metric_data("test-distribution_name", "test-metric_name", "test-start_time", "test-end_time", 1, "test-unit", [], )


async def test_get_distributions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_distributions()
    mock_client.call.assert_called_once()


async def test_get_distributions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_distributions()


async def test_get_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_domain("test-domain_name", )
    mock_client.call.assert_called_once()


async def test_get_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_domain("test-domain_name", )


async def test_get_domains(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_domains()
    mock_client.call.assert_called_once()


async def test_get_domains_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_domains()


async def test_get_export_snapshot_records(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_export_snapshot_records()
    mock_client.call.assert_called_once()


async def test_get_export_snapshot_records_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_export_snapshot_records()


async def test_get_instance_access_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_access_details("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_get_instance_access_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_access_details("test-instance_name", )


async def test_get_instance_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_metric_data("test-instance_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )
    mock_client.call.assert_called_once()


async def test_get_instance_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_metric_data("test-instance_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )


async def test_get_instance_port_states(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_port_states("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_get_instance_port_states_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_port_states("test-instance_name", )


async def test_get_instance_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_snapshot("test-instance_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_get_instance_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_snapshot("test-instance_snapshot_name", )


async def test_get_instance_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_state("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_get_instance_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_state("test-instance_name", )


async def test_get_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_key_pair("test-key_pair_name", )
    mock_client.call.assert_called_once()


async def test_get_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_pair("test-key_pair_name", )


async def test_get_key_pairs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_key_pairs()
    mock_client.call.assert_called_once()


async def test_get_key_pairs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_key_pairs()


async def test_get_load_balancer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_load_balancer("test-load_balancer_name", )
    mock_client.call.assert_called_once()


async def test_get_load_balancer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_load_balancer("test-load_balancer_name", )


async def test_get_load_balancer_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_load_balancer_metric_data("test-load_balancer_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )
    mock_client.call.assert_called_once()


async def test_get_load_balancer_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_load_balancer_metric_data("test-load_balancer_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )


async def test_get_load_balancer_tls_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_load_balancer_tls_certificates("test-load_balancer_name", )
    mock_client.call.assert_called_once()


async def test_get_load_balancer_tls_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_load_balancer_tls_certificates("test-load_balancer_name", )


async def test_get_load_balancer_tls_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_load_balancer_tls_policies()
    mock_client.call.assert_called_once()


async def test_get_load_balancer_tls_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_load_balancer_tls_policies()


async def test_get_load_balancers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_load_balancers()
    mock_client.call.assert_called_once()


async def test_get_load_balancers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_load_balancers()


async def test_get_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_operation("test-operation_id", )
    mock_client.call.assert_called_once()


async def test_get_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_operation("test-operation_id", )


async def test_get_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_operations()
    mock_client.call.assert_called_once()


async def test_get_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_operations()


async def test_get_operations_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_operations_for_resource("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_get_operations_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_operations_for_resource("test-resource_name", )


async def test_get_regions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_regions()
    mock_client.call.assert_called_once()


async def test_get_regions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_regions()


async def test_get_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database("test-relational_database_name", )


async def test_get_relational_database_blueprints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_blueprints()
    mock_client.call.assert_called_once()


async def test_get_relational_database_blueprints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_blueprints()


async def test_get_relational_database_bundles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_bundles()
    mock_client.call.assert_called_once()


async def test_get_relational_database_bundles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_bundles()


async def test_get_relational_database_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_events("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_events("test-relational_database_name", )


async def test_get_relational_database_log_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_log_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", )


async def test_get_relational_database_log_streams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_log_streams("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_log_streams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_log_streams("test-relational_database_name", )


async def test_get_relational_database_master_user_password(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_master_user_password("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_master_user_password_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_master_user_password("test-relational_database_name", )


async def test_get_relational_database_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_metric_data("test-relational_database_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )
    mock_client.call.assert_called_once()


async def test_get_relational_database_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_metric_data("test-relational_database_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], )


async def test_get_relational_database_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_parameters("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_parameters("test-relational_database_name", )


async def test_get_relational_database_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_snapshot("test-relational_database_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_get_relational_database_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_snapshot("test-relational_database_snapshot_name", )


async def test_get_relational_database_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_database_snapshots()
    mock_client.call.assert_called_once()


async def test_get_relational_database_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_database_snapshots()


async def test_get_relational_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_relational_databases()
    mock_client.call.assert_called_once()


async def test_get_relational_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_relational_databases()


async def test_get_setup_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_setup_history("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_get_setup_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_setup_history("test-resource_name", )


async def test_get_static_ips(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_static_ips()
    mock_client.call.assert_called_once()


async def test_get_static_ips_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_static_ips()


async def test_import_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_key_pair("test-key_pair_name", "test-public_key_base64", )
    mock_client.call.assert_called_once()


async def test_import_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_key_pair("test-key_pair_name", "test-public_key_base64", )


async def test_is_vpc_peered(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await is_vpc_peered()
    mock_client.call.assert_called_once()


async def test_is_vpc_peered_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await is_vpc_peered()


async def test_open_instance_public_ports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await open_instance_public_ports({}, "test-instance_name", )
    mock_client.call.assert_called_once()


async def test_open_instance_public_ports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await open_instance_public_ports({}, "test-instance_name", )


async def test_peer_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await peer_vpc()
    mock_client.call.assert_called_once()


async def test_peer_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await peer_vpc()


async def test_put_alarm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", 1, )
    mock_client.call.assert_called_once()


async def test_put_alarm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", 1, )


async def test_put_instance_public_ports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_instance_public_ports([], "test-instance_name", )
    mock_client.call.assert_called_once()


async def test_put_instance_public_ports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_instance_public_ports([], "test-instance_name", )


async def test_reboot_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_reboot_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_relational_database("test-relational_database_name", )


async def test_register_container_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_container_image("test-service_name", "test-label", "test-digest", )
    mock_client.call.assert_called_once()


async def test_register_container_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_container_image("test-service_name", "test-label", "test-digest", )


async def test_reset_distribution_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_distribution_cache()
    mock_client.call.assert_called_once()


async def test_reset_distribution_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_distribution_cache()


async def test_run_alarm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_alarm("test-alarm_name", "test-state", )
    mock_client.call.assert_called_once()


async def test_run_alarm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_alarm("test-alarm_name", "test-state", )


async def test_send_contact_method_verification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_contact_method_verification("test-protocol", )
    mock_client.call.assert_called_once()


async def test_send_contact_method_verification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_contact_method_verification("test-protocol", )


async def test_set_ip_address_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", )
    mock_client.call.assert_called_once()


async def test_set_ip_address_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", )


async def test_set_resource_access_for_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_resource_access_for_bucket("test-resource_name", "test-bucket_name", "test-access", )
    mock_client.call.assert_called_once()


async def test_set_resource_access_for_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_resource_access_for_bucket("test-resource_name", "test-bucket_name", "test-access", )


async def test_setup_instance_https(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await setup_instance_https("test-instance_name", "test-email_address", [], "test-certificate_provider", )
    mock_client.call.assert_called_once()


async def test_setup_instance_https_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await setup_instance_https("test-instance_name", "test-email_address", [], "test-certificate_provider", )


async def test_start_gui_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_gui_session("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_start_gui_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_gui_session("test-resource_name", )


async def test_start_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_start_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_relational_database("test-relational_database_name", )


async def test_stop_gui_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_gui_session("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_stop_gui_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_gui_session("test-resource_name", )


async def test_stop_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_stop_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_relational_database("test-relational_database_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_name", [], )


async def test_unpeer_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await unpeer_vpc()
    mock_client.call.assert_called_once()


async def test_unpeer_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unpeer_vpc()


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_name", [], )


async def test_update_bucket(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bucket("test-bucket_name", )
    mock_client.call.assert_called_once()


async def test_update_bucket_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bucket("test-bucket_name", )


async def test_update_bucket_bundle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bucket_bundle("test-bucket_name", "test-bundle_id", )
    mock_client.call.assert_called_once()


async def test_update_bucket_bundle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bucket_bundle("test-bucket_name", "test-bundle_id", )


async def test_update_container_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_container_service("test-service_name", )
    mock_client.call.assert_called_once()


async def test_update_container_service_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_container_service("test-service_name", )


async def test_update_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_distribution("test-distribution_name", )
    mock_client.call.assert_called_once()


async def test_update_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_distribution("test-distribution_name", )


async def test_update_distribution_bundle(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_distribution_bundle()
    mock_client.call.assert_called_once()


async def test_update_distribution_bundle_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_distribution_bundle()


async def test_update_domain_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_domain_entry("test-domain_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_domain_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_domain_entry("test-domain_name", {}, )


async def test_update_instance_metadata_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_instance_metadata_options("test-instance_name", )
    mock_client.call.assert_called_once()


async def test_update_instance_metadata_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_instance_metadata_options("test-instance_name", )


async def test_update_load_balancer_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_load_balancer_attribute("test-load_balancer_name", "test-attribute_name", "test-attribute_value", )
    mock_client.call.assert_called_once()


async def test_update_load_balancer_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_load_balancer_attribute("test-load_balancer_name", "test-attribute_name", "test-attribute_value", )


async def test_update_relational_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_relational_database("test-relational_database_name", )
    mock_client.call.assert_called_once()


async def test_update_relational_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_relational_database("test-relational_database_name", )


async def test_update_relational_database_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_relational_database_parameters("test-relational_database_name", [], )
    mock_client.call.assert_called_once()


async def test_update_relational_database_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.lightsail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_relational_database_parameters("test-relational_database_name", [], )


@pytest.mark.asyncio
async def test_attach_disk_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import attach_disk
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await attach_disk("test-disk_name", "test-instance_name", "test-disk_path", auto_mounting=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import copy_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await copy_snapshot("test-target_snapshot_name", "test-source_region", source_snapshot_name="test-source_snapshot_name", source_resource_name="test-source_resource_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_bucket("test-bucket_name", "test-bundle_id", tags=[{"Key": "k", "Value": "v"}], enable_object_versioning=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_certificate("test-certificate_name", "test-domain_name", subject_alternative_names="test-subject_alternative_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_container_service_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_container_service
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_container_service("test-service_name", "test-power", "test-scale", tags=[{"Key": "k", "Value": "v"}], public_domain_names="test-public_domain_names", deployment="test-deployment", private_registry_access="test-private_registry_access", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_container_service_deployment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_container_service_deployment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_container_service_deployment("test-service_name", containers="test-containers", public_endpoint="test-public_endpoint", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_disk_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_disk
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_disk("test-disk_name", "test-availability_zone", 1, tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_disk_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_disk_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, disk_snapshot_name="test-disk_snapshot_name", tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", source_disk_name="test-source_disk_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_disk_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_disk_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_disk_snapshot("test-disk_snapshot_name", disk_name="test-disk_name", instance_name="test-instance_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_distribution("test-distribution_name", "test-origin", "test-default_cache_behavior", "test-bundle_id", cache_behavior_settings={}, cache_behaviors="test-cache_behaviors", ip_address_type="test-ip_address_type", tags=[{"Key": "k", "Value": "v"}], certificate_name="test-certificate_name", viewer_minimum_tls_protocol_version="test-viewer_minimum_tls_protocol_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_domain("test-domain_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instances_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_instances_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_instances_from_snapshot("test-instance_names", "test-availability_zone", "test-bundle_id", attached_disk_mapping={}, instance_snapshot_name="test-instance_snapshot_name", user_data="test-user_data", key_pair_name="test-key_pair_name", tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", ip_address_type="test-ip_address_type", source_instance_name="test-source_instance_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_key_pair("test-key_pair_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_load_balancer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_load_balancer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_load_balancer("test-load_balancer_name", 1, health_check_path="test-health_check_path", certificate_name="test-certificate_name", certificate_domain_name="test-certificate_domain_name", certificate_alternative_names="test-certificate_alternative_names", tags=[{"Key": "k", "Value": "v"}], ip_address_type="test-ip_address_type", tls_policy_name="test-tls_policy_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_load_balancer_tls_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_load_balancer_tls_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", certificate_alternative_names="test-certificate_alternative_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_relational_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_relational_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", availability_zone="test-availability_zone", master_user_password="test-master_user_password", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_relational_database_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_relational_database_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_relational_database_from_snapshot("test-relational_database_name", availability_zone="test-availability_zone", publicly_accessible="test-publicly_accessible", relational_database_snapshot_name="test-relational_database_snapshot_name", relational_database_bundle_id="test-relational_database_bundle_id", source_relational_database_name="test-source_relational_database_name", restore_time="test-restore_time", use_latest_restorable_time=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_relational_database_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import create_relational_database_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_bucket("test-bucket_name", force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_disk_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_disk
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_disk("test-disk_name", force_delete_add_ons=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_distribution(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_key_pair("test-key_pair_name", expected_fingerprint="test-expected_fingerprint", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_load_balancer_tls_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_load_balancer_tls_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_relational_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import delete_relational_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await delete_relational_database("test-relational_database_name", skip_final_snapshot=True, final_relational_database_snapshot_name="test-final_relational_database_snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_active_names_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_active_names
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_active_names(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_alarms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_alarms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_alarms(alarm_name="test-alarm_name", page_token="test-page_token", monitored_resource_name="test-monitored_resource_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_blueprints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_blueprints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_blueprints(include_inactive=True, page_token="test-page_token", app_category="test-app_category", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bucket_bundles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_bucket_bundles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_bucket_bundles(include_inactive=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_buckets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_buckets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_buckets(bucket_name="test-bucket_name", page_token="test-page_token", include_connected_resources=True, include_cors=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_bundles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_bundles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_bundles(include_inactive=True, page_token="test-page_token", app_category="test-app_category", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_certificates(certificate_statuses="test-certificate_statuses", include_certificate_details=True, certificate_name="test-certificate_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cloud_formation_stack_records_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_cloud_formation_stack_records
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_cloud_formation_stack_records(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_contact_methods_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_contact_methods
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_contact_methods(protocols="test-protocols", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_container_log_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_container_log
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_container_log("test-service_name", "test-container_name", start_time="test-start_time", end_time="test-end_time", filter_pattern="test-filter_pattern", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_container_services_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_container_services
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_container_services(service_name="test-service_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_disk_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_disk_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_disk_snapshots(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_disks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_disks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_disks(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_distribution_latest_cache_reset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_distribution_latest_cache_reset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_distribution_latest_cache_reset(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_distributions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_distributions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_distributions(distribution_name="test-distribution_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_domains_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_domains
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_domains(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_export_snapshot_records_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_export_snapshot_records
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_export_snapshot_records(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_instance_access_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_instance_access_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_instance_access_details("test-instance_name", protocol="test-protocol", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_key_pairs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_key_pairs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_key_pairs(page_token="test-page_token", include_default_key_pair=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_load_balancer_tls_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_load_balancer_tls_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_load_balancer_tls_policies(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_load_balancers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_load_balancers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_load_balancers(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_operations(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_operations_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_operations_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_operations_for_resource("test-resource_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_regions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_regions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_regions(include_availability_zones=True, include_relational_database_availability_zones=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_blueprints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_blueprints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_blueprints(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_bundles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_bundles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_bundles(page_token="test-page_token", include_inactive=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_events("test-relational_database_name", duration_in_minutes=1, page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_log_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_log_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", start_time="test-start_time", end_time="test-end_time", start_from_head="test-start_from_head", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_master_user_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_master_user_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_master_user_password("test-relational_database_name", password_version="test-password_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_parameters("test-relational_database_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_database_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_database_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_database_snapshots(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_relational_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_relational_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_relational_databases(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_setup_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_setup_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_setup_history("test-resource_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_static_ips_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import get_static_ips
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await get_static_ips(page_token="test-page_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_alarm_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import put_alarm
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", "test-evaluation_periods", datapoints_to_alarm="test-datapoints_to_alarm", treat_missing_data="test-treat_missing_data", contact_protocols="test-contact_protocols", notification_triggers="test-notification_triggers", notification_enabled="test-notification_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_distribution_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import reset_distribution_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await reset_distribution_cache(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_ip_address_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import set_ip_address_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", accept_bundle_update="test-accept_bundle_update", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_relational_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import stop_relational_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await stop_relational_database("test-relational_database_name", relational_database_snapshot_name="test-relational_database_snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_tag_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import tag_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await tag_resource("test-resource_name", [{"Key": "k", "Value": "v"}], resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import untag_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await untag_resource("test-resource_name", "test-tag_keys", resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bucket_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_bucket
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_bucket("test-bucket_name", access_rules="test-access_rules", versioning="test-versioning", readonly_access_accounts=1, access_log_config={}, cors="test-cors", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_container_service_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_container_service
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_container_service("test-service_name", power="test-power", scale="test-scale", is_disabled=True, public_domain_names="test-public_domain_names", private_registry_access="test-private_registry_access", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_distribution("test-distribution_name", origin="test-origin", default_cache_behavior="test-default_cache_behavior", cache_behavior_settings={}, cache_behaviors="test-cache_behaviors", is_enabled=True, viewer_minimum_tls_protocol_version="test-viewer_minimum_tls_protocol_version", certificate_name="test-certificate_name", use_default_certificate=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_distribution_bundle_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_distribution_bundle
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_distribution_bundle(distribution_name="test-distribution_name", bundle_id="test-bundle_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_instance_metadata_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_instance_metadata_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_instance_metadata_options("test-instance_name", http_tokens="test-http_tokens", http_endpoint="test-http_endpoint", http_put_response_hop_limit=1, http_protocol_ipv6="test-http_protocol_ipv6", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_relational_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.lightsail import update_relational_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.lightsail.async_client", lambda *a, **kw: mock_client)
    await update_relational_database("test-relational_database_name", master_user_password="test-master_user_password", rotate_master_user_password="test-rotate_master_user_password", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", enable_backup_retention=True, disable_backup_retention=True, publicly_accessible="test-publicly_accessible", apply_immediately=True, ca_certificate_identifier="test-ca_certificate_identifier", relational_database_blueprint_id="test-relational_database_blueprint_id", region_name="us-east-1")
    mock_client.call.assert_called_once()
