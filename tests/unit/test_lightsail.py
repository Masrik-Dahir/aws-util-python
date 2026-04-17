"""Tests for aws_util.lightsail -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.lightsail import (
    DatabaseResult,
    InstanceResult,
    SnapshotResult,
    StaticIpResult,
    _parse_database,
    _parse_instance,
    _parse_snapshot,
    _parse_static_ip,
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

_ERR = ClientError({"Error": {"Code": "X", "Message": "fail"}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_instance_result_minimal():
    m = InstanceResult(name="i1")
    assert m.arn == ""
    assert m.state == ""
    assert m.extra == {}


def test_instance_result_full():
    m = InstanceResult(
        name="i1", arn="arn:1", state="running",
        blueprint_id="amazon_linux_2", bundle_id="nano",
        public_ip_address="1.2.3.4", private_ip_address="10.0.0.1",
        region_name="us-east-1", extra={"foo": "bar"},
    )
    assert m.public_ip_address == "1.2.3.4"


def test_snapshot_result_minimal():
    m = SnapshotResult(name="s1")
    assert m.created_at is None
    assert m.extra == {}


def test_snapshot_result_full():
    m = SnapshotResult(
        name="s1", arn="arn:1", state="available",
        from_instance_name="i1", created_at="2024-01-01",
        extra={"k": "v"},
    )
    assert m.from_instance_name == "i1"


def test_database_result_minimal():
    m = DatabaseResult(name="db1")
    assert m.engine == ""


def test_database_result_full():
    m = DatabaseResult(
        name="db1", arn="arn:1", state="available",
        engine="mysql", engine_version="8.0",
        master_username="admin", master_endpoint={"address": "x"},
        extra={"k": "v"},
    )
    assert m.master_username == "admin"


def test_static_ip_result_minimal():
    m = StaticIpResult(name="ip1")
    assert not m.is_attached


def test_static_ip_result_full():
    m = StaticIpResult(
        name="ip1", arn="arn:1", ip_address="1.2.3.4",
        is_attached=True, attached_to="i1", extra={"k": "v"},
    )
    assert m.attached_to == "i1"


# ---------------------------------------------------------------------------
# _parse helpers
# ---------------------------------------------------------------------------


def test_parse_instance_basic():
    data = {
        "name": "i1", "arn": "arn:1",
        "state": {"name": "running"},
        "blueprintId": "amazon_linux_2", "bundleId": "nano",
        "publicIpAddress": "1.2.3.4", "privateIpAddress": "10.0.0.1",
        "location": {"regionName": "us-east-1"},
        "extra_field": "val",
    }
    r = _parse_instance(data)
    assert r.state == "running"
    assert r.region_name == "us-east-1"
    assert "extra_field" in r.extra


def test_parse_instance_state_not_dict():
    data = {
        "name": "i1", "state": "running",
        "location": "not-a-dict",
    }
    r = _parse_instance(data)
    assert r.state == "running"
    assert r.region_name == ""


def test_parse_snapshot_with_created_at():
    data = {
        "name": "s1", "arn": "arn:1", "state": "available",
        "fromInstanceName": "i1", "createdAt": "2024-01-01",
    }
    r = _parse_snapshot(data)
    assert r.created_at == "2024-01-01"


def test_parse_snapshot_no_created_at():
    data = {"name": "s1", "state": "available"}
    r = _parse_snapshot(data)
    assert r.created_at is None


def test_parse_database():
    data = {
        "name": "db1", "arn": "arn:1", "state": "available",
        "engine": "mysql", "engineVersion": "8.0",
        "masterUsername": "admin", "masterEndpoint": {"address": "x"},
    }
    r = _parse_database(data)
    assert r.engine == "mysql"


def test_parse_static_ip():
    data = {
        "name": "ip1", "arn": "arn:1", "ipAddress": "1.2.3.4",
        "isAttached": True, "attachedTo": "i1",
    }
    r = _parse_static_ip(data)
    assert r.is_attached is True


# ---------------------------------------------------------------------------
# create_instances
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_create_instances_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_instances.return_value = {
        "operations": [{"resourceName": "i1", "status": "Succeeded"}],
    }
    r = create_instances(
        ["i1"],
        availability_zone="us-east-1a",
        blueprint_id="amazon_linux_2",
        bundle_id="nano",
    )
    assert len(r) == 1


@patch("aws_util.lightsail.get_client")
def test_create_instances_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_instances.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_instances failed"):
        create_instances(
            ["i1"], availability_zone="a",
            blueprint_id="b", bundle_id="c",
        )


# ---------------------------------------------------------------------------
# get_instance / get_instances
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_get_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instance.return_value = {
        "instance": {
            "name": "i1", "state": {"name": "running"},
            "location": {"regionName": "us-east-1"},
        },
    }
    r = get_instance("i1")
    assert r.name == "i1"


@patch("aws_util.lightsail.get_client")
def test_get_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_instance failed"):
        get_instance("i1")


@patch("aws_util.lightsail.get_client")
def test_get_instances_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instances.return_value = {
        "instances": [
            {"name": "i1", "state": {"name": "running"}, "location": {}},
        ],
    }
    r = get_instances()
    assert len(r) == 1


@patch("aws_util.lightsail.get_client")
def test_get_instances_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instances.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_instances failed"):
        get_instances()


# ---------------------------------------------------------------------------
# delete / start / stop / reboot instance
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_delete_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_instance("i1")
    client.delete_instance.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_instance_force(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_instance("i1", force=True)
    args = client.delete_instance.call_args
    assert args[1].get("forceDeleteAddOns") is True


@patch("aws_util.lightsail.get_client")
def test_delete_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_instance failed"):
        delete_instance("i1")


@patch("aws_util.lightsail.get_client")
def test_start_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    start_instance("i1")
    client.start_instance.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_start_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.start_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="start_instance failed"):
        start_instance("i1")


@patch("aws_util.lightsail.get_client")
def test_stop_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    stop_instance("i1")
    client.stop_instance.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_stop_instance_force(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    stop_instance("i1", force=True)


@patch("aws_util.lightsail.get_client")
def test_stop_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.stop_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="stop_instance failed"):
        stop_instance("i1")


@patch("aws_util.lightsail.get_client")
def test_reboot_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    reboot_instance("i1")
    client.reboot_instance.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_reboot_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.reboot_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="reboot_instance failed"):
        reboot_instance("i1")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_create_instance_snapshot_with_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_instance_snapshot.return_value = {
        "operations": [{"status": "Succeeded"}],
    }
    r = create_instance_snapshot("i1", "snap1")
    assert r.name == "snap1"
    assert r.state == "Succeeded"


@patch("aws_util.lightsail.get_client")
def test_create_instance_snapshot_no_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_instance_snapshot.return_value = {}
    r = create_instance_snapshot("i1", "snap1")
    assert r.name == "snap1"
    assert r.state == ""


@patch("aws_util.lightsail.get_client")
def test_create_instance_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_instance_snapshot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_instance_snapshot"):
        create_instance_snapshot("i1", "snap1")


@patch("aws_util.lightsail.get_client")
def test_get_instance_snapshots_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instance_snapshots.return_value = {
        "instanceSnapshots": [{"name": "s1", "state": "available"}],
    }
    r = get_instance_snapshots()
    assert len(r) == 1


@patch("aws_util.lightsail.get_client")
def test_get_instance_snapshots_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_instance_snapshots.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_instance_snapshots"):
        get_instance_snapshots()


@patch("aws_util.lightsail.get_client")
def test_delete_instance_snapshot_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_instance_snapshot("snap1")


@patch("aws_util.lightsail.get_client")
def test_delete_instance_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_instance_snapshot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_instance_snapshot"):
        delete_instance_snapshot("snap1")


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_create_database_with_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_relational_database.return_value = {
        "operations": [{"status": "Succeeded"}],
    }
    r = create_database(
        "db1", availability_zone="a",
        master_database_name="mydb",
        master_username="admin",
        master_user_password="pass",
    )
    assert r.name == "db1"
    assert r.state == "Succeeded"


@patch("aws_util.lightsail.get_client")
def test_create_database_no_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_relational_database.return_value = {}
    r = create_database(
        "db1", availability_zone="a",
        master_database_name="mydb",
        master_username="admin",
        master_user_password="pass",
    )
    assert r.name == "db1"
    assert r.state == ""


@patch("aws_util.lightsail.get_client")
def test_create_database_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_relational_database.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_database failed"):
        create_database(
            "db1", availability_zone="a",
            master_database_name="mydb",
            master_username="admin",
            master_user_password="pass",
        )


@patch("aws_util.lightsail.get_client")
def test_get_database_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_relational_database.return_value = {
        "relationalDatabase": {
            "name": "db1", "state": "available",
            "engine": "mysql", "engineVersion": "8.0",
            "masterUsername": "admin",
        },
    }
    r = get_database("db1")
    assert r.name == "db1"


@patch("aws_util.lightsail.get_client")
def test_get_database_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_relational_database.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_database failed"):
        get_database("db1")


@patch("aws_util.lightsail.get_client")
def test_get_databases_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_relational_databases.return_value = {
        "relationalDatabases": [{"name": "db1", "state": "available"}],
    }
    r = get_databases()
    assert len(r) == 1


@patch("aws_util.lightsail.get_client")
def test_get_databases_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_relational_databases.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_databases failed"):
        get_databases()


@patch("aws_util.lightsail.get_client")
def test_delete_database_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_database("db1")


@patch("aws_util.lightsail.get_client")
def test_delete_database_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_relational_database.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_database failed"):
        delete_database("db1")


# ---------------------------------------------------------------------------
# Static IP operations
# ---------------------------------------------------------------------------


@patch("aws_util.lightsail.get_client")
def test_allocate_static_ip_with_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.allocate_static_ip.return_value = {
        "operations": [{"status": "Succeeded"}],
    }
    r = allocate_static_ip("ip1")
    assert r.name == "ip1"


@patch("aws_util.lightsail.get_client")
def test_allocate_static_ip_no_ops(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.allocate_static_ip.return_value = {}
    r = allocate_static_ip("ip1")
    assert r.name == "ip1"


@patch("aws_util.lightsail.get_client")
def test_allocate_static_ip_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.allocate_static_ip.side_effect = _ERR
    with pytest.raises(RuntimeError, match="allocate_static_ip failed"):
        allocate_static_ip("ip1")


@patch("aws_util.lightsail.get_client")
def test_get_static_ip_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_static_ip.return_value = {
        "staticIp": {
            "name": "ip1", "ipAddress": "1.2.3.4",
            "isAttached": False,
        },
    }
    r = get_static_ip("ip1")
    assert r.ip_address == "1.2.3.4"


@patch("aws_util.lightsail.get_client")
def test_get_static_ip_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_static_ip.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_static_ip failed"):
        get_static_ip("ip1")


@patch("aws_util.lightsail.get_client")
def test_release_static_ip_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    release_static_ip("ip1")


@patch("aws_util.lightsail.get_client")
def test_release_static_ip_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.release_static_ip.side_effect = _ERR
    with pytest.raises(RuntimeError, match="release_static_ip failed"):
        release_static_ip("ip1")


REGION = "us-east-1"


@patch("aws_util.lightsail.get_client")
def test_attach_certificate_to_distribution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_certificate_to_distribution.return_value = {}
    attach_certificate_to_distribution("test-distribution_name", "test-certificate_name", region_name=REGION)
    mock_client.attach_certificate_to_distribution.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_attach_certificate_to_distribution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_certificate_to_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_certificate_to_distribution",
    )
    with pytest.raises(RuntimeError, match="Failed to attach certificate to distribution"):
        attach_certificate_to_distribution("test-distribution_name", "test-certificate_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_attach_disk(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_disk.return_value = {}
    attach_disk("test-disk_name", "test-instance_name", "test-disk_path", region_name=REGION)
    mock_client.attach_disk.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_attach_disk_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_disk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_disk",
    )
    with pytest.raises(RuntimeError, match="Failed to attach disk"):
        attach_disk("test-disk_name", "test-instance_name", "test-disk_path", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_attach_instances_to_load_balancer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_instances_to_load_balancer.return_value = {}
    attach_instances_to_load_balancer("test-load_balancer_name", [], region_name=REGION)
    mock_client.attach_instances_to_load_balancer.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_attach_instances_to_load_balancer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_instances_to_load_balancer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_instances_to_load_balancer",
    )
    with pytest.raises(RuntimeError, match="Failed to attach instances to load balancer"):
        attach_instances_to_load_balancer("test-load_balancer_name", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_attach_load_balancer_tls_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_load_balancer_tls_certificate.return_value = {}
    attach_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", region_name=REGION)
    mock_client.attach_load_balancer_tls_certificate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_attach_load_balancer_tls_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_load_balancer_tls_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_load_balancer_tls_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to attach load balancer tls certificate"):
        attach_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_attach_static_ip(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_static_ip.return_value = {}
    attach_static_ip("test-static_ip_name", "test-instance_name", region_name=REGION)
    mock_client.attach_static_ip.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_attach_static_ip_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_static_ip.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_static_ip",
    )
    with pytest.raises(RuntimeError, match="Failed to attach static ip"):
        attach_static_ip("test-static_ip_name", "test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_close_instance_public_ports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.close_instance_public_ports.return_value = {}
    close_instance_public_ports({}, "test-instance_name", region_name=REGION)
    mock_client.close_instance_public_ports.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_close_instance_public_ports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.close_instance_public_ports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "close_instance_public_ports",
    )
    with pytest.raises(RuntimeError, match="Failed to close instance public ports"):
        close_instance_public_ports({}, "test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_copy_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_snapshot.return_value = {}
    copy_snapshot("test-target_snapshot_name", "test-source_region", region_name=REGION)
    mock_client.copy_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_copy_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to copy snapshot"):
        copy_snapshot("test-target_snapshot_name", "test-source_region", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_bucket(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bucket.return_value = {}
    create_bucket("test-bucket_name", "test-bundle_id", region_name=REGION)
    mock_client.create_bucket.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_bucket_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bucket",
    )
    with pytest.raises(RuntimeError, match="Failed to create bucket"):
        create_bucket("test-bucket_name", "test-bundle_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_bucket_access_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bucket_access_key.return_value = {}
    create_bucket_access_key("test-bucket_name", region_name=REGION)
    mock_client.create_bucket_access_key.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_bucket_access_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bucket_access_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bucket_access_key",
    )
    with pytest.raises(RuntimeError, match="Failed to create bucket access key"):
        create_bucket_access_key("test-bucket_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate.return_value = {}
    create_certificate("test-certificate_name", "test-domain_name", region_name=REGION)
    mock_client.create_certificate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to create certificate"):
        create_certificate("test-certificate_name", "test-domain_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_cloud_formation_stack(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_cloud_formation_stack.return_value = {}
    create_cloud_formation_stack([], region_name=REGION)
    mock_client.create_cloud_formation_stack.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_cloud_formation_stack_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_cloud_formation_stack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cloud_formation_stack",
    )
    with pytest.raises(RuntimeError, match="Failed to create cloud formation stack"):
        create_cloud_formation_stack([], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_contact_method(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_contact_method.return_value = {}
    create_contact_method("test-protocol", "test-contact_endpoint", region_name=REGION)
    mock_client.create_contact_method.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_contact_method_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_contact_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_contact_method",
    )
    with pytest.raises(RuntimeError, match="Failed to create contact method"):
        create_contact_method("test-protocol", "test-contact_endpoint", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_container_service(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service.return_value = {}
    create_container_service("test-service_name", "test-power", 1, region_name=REGION)
    mock_client.create_container_service.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_container_service_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_container_service",
    )
    with pytest.raises(RuntimeError, match="Failed to create container service"):
        create_container_service("test-service_name", "test-power", 1, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_container_service_deployment(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service_deployment.return_value = {}
    create_container_service_deployment("test-service_name", region_name=REGION)
    mock_client.create_container_service_deployment.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_container_service_deployment_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_container_service_deployment",
    )
    with pytest.raises(RuntimeError, match="Failed to create container service deployment"):
        create_container_service_deployment("test-service_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_container_service_registry_login(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service_registry_login.return_value = {}
    create_container_service_registry_login(region_name=REGION)
    mock_client.create_container_service_registry_login.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_container_service_registry_login_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_container_service_registry_login.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_container_service_registry_login",
    )
    with pytest.raises(RuntimeError, match="Failed to create container service registry login"):
        create_container_service_registry_login(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_disk(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk.return_value = {}
    create_disk("test-disk_name", "test-availability_zone", 1, region_name=REGION)
    mock_client.create_disk.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_disk_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_disk",
    )
    with pytest.raises(RuntimeError, match="Failed to create disk"):
        create_disk("test-disk_name", "test-availability_zone", 1, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_disk_from_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk_from_snapshot.return_value = {}
    create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, region_name=REGION)
    mock_client.create_disk_from_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_disk_from_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_disk_from_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to create disk from snapshot"):
        create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_disk_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk_snapshot.return_value = {}
    create_disk_snapshot("test-disk_snapshot_name", region_name=REGION)
    mock_client.create_disk_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_disk_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_disk_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_disk_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to create disk snapshot"):
        create_disk_snapshot("test-disk_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_distribution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_distribution.return_value = {}
    create_distribution("test-distribution_name", {}, {}, "test-bundle_id", region_name=REGION)
    mock_client.create_distribution.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_distribution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_distribution",
    )
    with pytest.raises(RuntimeError, match="Failed to create distribution"):
        create_distribution("test-distribution_name", {}, {}, "test-bundle_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_domain(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain.return_value = {}
    create_domain("test-domain_name", region_name=REGION)
    mock_client.create_domain.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_domain_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_domain",
    )
    with pytest.raises(RuntimeError, match="Failed to create domain"):
        create_domain("test-domain_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_domain_entry(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain_entry.return_value = {}
    create_domain_entry("test-domain_name", {}, region_name=REGION)
    mock_client.create_domain_entry.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_domain_entry_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_domain_entry",
    )
    with pytest.raises(RuntimeError, match="Failed to create domain entry"):
        create_domain_entry("test-domain_name", {}, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_gui_session_access_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_gui_session_access_details.return_value = {}
    create_gui_session_access_details("test-resource_name", region_name=REGION)
    mock_client.create_gui_session_access_details.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_gui_session_access_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_gui_session_access_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_gui_session_access_details",
    )
    with pytest.raises(RuntimeError, match="Failed to create gui session access details"):
        create_gui_session_access_details("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_instances_from_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_instances_from_snapshot.return_value = {}
    create_instances_from_snapshot([], "test-availability_zone", "test-bundle_id", region_name=REGION)
    mock_client.create_instances_from_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_instances_from_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_instances_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instances_from_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to create instances from snapshot"):
        create_instances_from_snapshot([], "test-availability_zone", "test-bundle_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_key_pair.return_value = {}
    create_key_pair("test-key_pair_name", region_name=REGION)
    mock_client.create_key_pair.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to create key pair"):
        create_key_pair("test-key_pair_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_load_balancer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_load_balancer.return_value = {}
    create_load_balancer("test-load_balancer_name", 1, region_name=REGION)
    mock_client.create_load_balancer.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_load_balancer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_load_balancer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_load_balancer",
    )
    with pytest.raises(RuntimeError, match="Failed to create load balancer"):
        create_load_balancer("test-load_balancer_name", 1, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_load_balancer_tls_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_load_balancer_tls_certificate.return_value = {}
    create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", region_name=REGION)
    mock_client.create_load_balancer_tls_certificate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_load_balancer_tls_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_load_balancer_tls_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_load_balancer_tls_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to create load balancer tls certificate"):
        create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database.return_value = {}
    create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", region_name=REGION)
    mock_client.create_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to create relational database"):
        create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_relational_database_from_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database_from_snapshot.return_value = {}
    create_relational_database_from_snapshot("test-relational_database_name", region_name=REGION)
    mock_client.create_relational_database_from_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_relational_database_from_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_relational_database_from_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to create relational database from snapshot"):
        create_relational_database_from_snapshot("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_create_relational_database_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database_snapshot.return_value = {}
    create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", region_name=REGION)
    mock_client.create_relational_database_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_create_relational_database_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_relational_database_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_relational_database_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to create relational database snapshot"):
        create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_alarm(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_alarm.return_value = {}
    delete_alarm("test-alarm_name", region_name=REGION)
    mock_client.delete_alarm.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_alarm_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_alarm.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_alarm",
    )
    with pytest.raises(RuntimeError, match="Failed to delete alarm"):
        delete_alarm("test-alarm_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_auto_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_auto_snapshot.return_value = {}
    delete_auto_snapshot("test-resource_name", "test-date", region_name=REGION)
    mock_client.delete_auto_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_auto_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_auto_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_auto_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to delete auto snapshot"):
        delete_auto_snapshot("test-resource_name", "test-date", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_bucket(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bucket.return_value = {}
    delete_bucket("test-bucket_name", region_name=REGION)
    mock_client.delete_bucket.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_bucket_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bucket"):
        delete_bucket("test-bucket_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_bucket_access_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bucket_access_key.return_value = {}
    delete_bucket_access_key("test-bucket_name", "test-access_key_id", region_name=REGION)
    mock_client.delete_bucket_access_key.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_bucket_access_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_bucket_access_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bucket_access_key",
    )
    with pytest.raises(RuntimeError, match="Failed to delete bucket access key"):
        delete_bucket_access_key("test-bucket_name", "test-access_key_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.return_value = {}
    delete_certificate("test-certificate_name", region_name=REGION)
    mock_client.delete_certificate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to delete certificate"):
        delete_certificate("test-certificate_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_contact_method(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_contact_method.return_value = {}
    delete_contact_method("test-protocol", region_name=REGION)
    mock_client.delete_contact_method.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_contact_method_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_contact_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_method",
    )
    with pytest.raises(RuntimeError, match="Failed to delete contact method"):
        delete_contact_method("test-protocol", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_container_image(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_container_image.return_value = {}
    delete_container_image("test-service_name", "test-image", region_name=REGION)
    mock_client.delete_container_image.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_container_image_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_container_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_container_image",
    )
    with pytest.raises(RuntimeError, match="Failed to delete container image"):
        delete_container_image("test-service_name", "test-image", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_container_service(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_container_service.return_value = {}
    delete_container_service("test-service_name", region_name=REGION)
    mock_client.delete_container_service.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_container_service_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_container_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_container_service",
    )
    with pytest.raises(RuntimeError, match="Failed to delete container service"):
        delete_container_service("test-service_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_disk(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_disk.return_value = {}
    delete_disk("test-disk_name", region_name=REGION)
    mock_client.delete_disk.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_disk_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_disk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_disk",
    )
    with pytest.raises(RuntimeError, match="Failed to delete disk"):
        delete_disk("test-disk_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_disk_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_disk_snapshot.return_value = {}
    delete_disk_snapshot("test-disk_snapshot_name", region_name=REGION)
    mock_client.delete_disk_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_disk_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_disk_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_disk_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to delete disk snapshot"):
        delete_disk_snapshot("test-disk_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_distribution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_distribution.return_value = {}
    delete_distribution(region_name=REGION)
    mock_client.delete_distribution.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_distribution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_distribution",
    )
    with pytest.raises(RuntimeError, match="Failed to delete distribution"):
        delete_distribution(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_domain(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain.return_value = {}
    delete_domain("test-domain_name", region_name=REGION)
    mock_client.delete_domain.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_domain_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain",
    )
    with pytest.raises(RuntimeError, match="Failed to delete domain"):
        delete_domain("test-domain_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_domain_entry(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_entry.return_value = {}
    delete_domain_entry("test-domain_name", {}, region_name=REGION)
    mock_client.delete_domain_entry.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_domain_entry_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_entry",
    )
    with pytest.raises(RuntimeError, match="Failed to delete domain entry"):
        delete_domain_entry("test-domain_name", {}, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_key_pair.return_value = {}
    delete_key_pair("test-key_pair_name", region_name=REGION)
    mock_client.delete_key_pair.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to delete key pair"):
        delete_key_pair("test-key_pair_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_known_host_keys(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_known_host_keys.return_value = {}
    delete_known_host_keys("test-instance_name", region_name=REGION)
    mock_client.delete_known_host_keys.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_known_host_keys_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_known_host_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_known_host_keys",
    )
    with pytest.raises(RuntimeError, match="Failed to delete known host keys"):
        delete_known_host_keys("test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_load_balancer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_load_balancer.return_value = {}
    delete_load_balancer("test-load_balancer_name", region_name=REGION)
    mock_client.delete_load_balancer.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_load_balancer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_load_balancer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_load_balancer",
    )
    with pytest.raises(RuntimeError, match="Failed to delete load balancer"):
        delete_load_balancer("test-load_balancer_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_load_balancer_tls_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_load_balancer_tls_certificate.return_value = {}
    delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", region_name=REGION)
    mock_client.delete_load_balancer_tls_certificate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_load_balancer_tls_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_load_balancer_tls_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_load_balancer_tls_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to delete load balancer tls certificate"):
        delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_relational_database.return_value = {}
    delete_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.delete_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to delete relational database"):
        delete_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_delete_relational_database_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_relational_database_snapshot.return_value = {}
    delete_relational_database_snapshot("test-relational_database_snapshot_name", region_name=REGION)
    mock_client.delete_relational_database_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_delete_relational_database_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_relational_database_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_relational_database_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to delete relational database snapshot"):
        delete_relational_database_snapshot("test-relational_database_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_detach_certificate_from_distribution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_certificate_from_distribution.return_value = {}
    detach_certificate_from_distribution("test-distribution_name", region_name=REGION)
    mock_client.detach_certificate_from_distribution.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_detach_certificate_from_distribution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_certificate_from_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_certificate_from_distribution",
    )
    with pytest.raises(RuntimeError, match="Failed to detach certificate from distribution"):
        detach_certificate_from_distribution("test-distribution_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_detach_disk(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_disk.return_value = {}
    detach_disk("test-disk_name", region_name=REGION)
    mock_client.detach_disk.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_detach_disk_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_disk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_disk",
    )
    with pytest.raises(RuntimeError, match="Failed to detach disk"):
        detach_disk("test-disk_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_detach_instances_from_load_balancer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_instances_from_load_balancer.return_value = {}
    detach_instances_from_load_balancer("test-load_balancer_name", [], region_name=REGION)
    mock_client.detach_instances_from_load_balancer.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_detach_instances_from_load_balancer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_instances_from_load_balancer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_instances_from_load_balancer",
    )
    with pytest.raises(RuntimeError, match="Failed to detach instances from load balancer"):
        detach_instances_from_load_balancer("test-load_balancer_name", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_detach_static_ip(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_static_ip.return_value = {}
    detach_static_ip("test-static_ip_name", region_name=REGION)
    mock_client.detach_static_ip.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_detach_static_ip_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_static_ip.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_static_ip",
    )
    with pytest.raises(RuntimeError, match="Failed to detach static ip"):
        detach_static_ip("test-static_ip_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_disable_add_on(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_add_on.return_value = {}
    disable_add_on("test-add_on_type", "test-resource_name", region_name=REGION)
    mock_client.disable_add_on.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_disable_add_on_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_add_on.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_add_on",
    )
    with pytest.raises(RuntimeError, match="Failed to disable add on"):
        disable_add_on("test-add_on_type", "test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_download_default_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.download_default_key_pair.return_value = {}
    download_default_key_pair(region_name=REGION)
    mock_client.download_default_key_pair.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_download_default_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.download_default_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "download_default_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to download default key pair"):
        download_default_key_pair(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_enable_add_on(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_add_on.return_value = {}
    enable_add_on("test-resource_name", {}, region_name=REGION)
    mock_client.enable_add_on.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_enable_add_on_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_add_on.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_add_on",
    )
    with pytest.raises(RuntimeError, match="Failed to enable add on"):
        enable_add_on("test-resource_name", {}, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_export_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.export_snapshot.return_value = {}
    export_snapshot("test-source_snapshot_name", region_name=REGION)
    mock_client.export_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_export_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.export_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to export snapshot"):
        export_snapshot("test-source_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_active_names(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_active_names.return_value = {}
    get_active_names(region_name=REGION)
    mock_client.get_active_names.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_active_names_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_active_names.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_active_names",
    )
    with pytest.raises(RuntimeError, match="Failed to get active names"):
        get_active_names(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_alarms(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_alarms.return_value = {}
    get_alarms(region_name=REGION)
    mock_client.get_alarms.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_alarms_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_alarms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_alarms",
    )
    with pytest.raises(RuntimeError, match="Failed to get alarms"):
        get_alarms(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_auto_snapshots(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_auto_snapshots.return_value = {}
    get_auto_snapshots("test-resource_name", region_name=REGION)
    mock_client.get_auto_snapshots.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_auto_snapshots_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_auto_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_auto_snapshots",
    )
    with pytest.raises(RuntimeError, match="Failed to get auto snapshots"):
        get_auto_snapshots("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_blueprints(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_blueprints.return_value = {}
    get_blueprints(region_name=REGION)
    mock_client.get_blueprints.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_blueprints_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_blueprints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_blueprints",
    )
    with pytest.raises(RuntimeError, match="Failed to get blueprints"):
        get_blueprints(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_bucket_access_keys(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_access_keys.return_value = {}
    get_bucket_access_keys("test-bucket_name", region_name=REGION)
    mock_client.get_bucket_access_keys.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_bucket_access_keys_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_access_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_access_keys",
    )
    with pytest.raises(RuntimeError, match="Failed to get bucket access keys"):
        get_bucket_access_keys("test-bucket_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_bucket_bundles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_bundles.return_value = {}
    get_bucket_bundles(region_name=REGION)
    mock_client.get_bucket_bundles.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_bucket_bundles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_bundles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_bundles",
    )
    with pytest.raises(RuntimeError, match="Failed to get bucket bundles"):
        get_bucket_bundles(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_bucket_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_metric_data.return_value = {}
    get_bucket_metric_data("test-bucket_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], "test-unit", region_name=REGION)
    mock_client.get_bucket_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_bucket_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bucket_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bucket_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get bucket metric data"):
        get_bucket_metric_data("test-bucket_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], "test-unit", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_buckets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_buckets.return_value = {}
    get_buckets(region_name=REGION)
    mock_client.get_buckets.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_buckets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_buckets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_buckets",
    )
    with pytest.raises(RuntimeError, match="Failed to get buckets"):
        get_buckets(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_bundles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bundles.return_value = {}
    get_bundles(region_name=REGION)
    mock_client.get_bundles.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_bundles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_bundles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_bundles",
    )
    with pytest.raises(RuntimeError, match="Failed to get bundles"):
        get_bundles(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_certificates.return_value = {}
    get_certificates(region_name=REGION)
    mock_client.get_certificates.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to get certificates"):
        get_certificates(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_cloud_formation_stack_records(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cloud_formation_stack_records.return_value = {}
    get_cloud_formation_stack_records(region_name=REGION)
    mock_client.get_cloud_formation_stack_records.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_cloud_formation_stack_records_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cloud_formation_stack_records.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cloud_formation_stack_records",
    )
    with pytest.raises(RuntimeError, match="Failed to get cloud formation stack records"):
        get_cloud_formation_stack_records(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_contact_methods(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_contact_methods.return_value = {}
    get_contact_methods(region_name=REGION)
    mock_client.get_contact_methods.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_contact_methods_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_contact_methods.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_contact_methods",
    )
    with pytest.raises(RuntimeError, match="Failed to get contact methods"):
        get_contact_methods(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_api_metadata(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_api_metadata.return_value = {}
    get_container_api_metadata(region_name=REGION)
    mock_client.get_container_api_metadata.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_api_metadata_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_api_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_api_metadata",
    )
    with pytest.raises(RuntimeError, match="Failed to get container api metadata"):
        get_container_api_metadata(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_images(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_images.return_value = {}
    get_container_images("test-service_name", region_name=REGION)
    mock_client.get_container_images.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_images_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_images.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_images",
    )
    with pytest.raises(RuntimeError, match="Failed to get container images"):
        get_container_images("test-service_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_log(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_log.return_value = {}
    get_container_log("test-service_name", "test-container_name", region_name=REGION)
    mock_client.get_container_log.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_log_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_log.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_log",
    )
    with pytest.raises(RuntimeError, match="Failed to get container log"):
        get_container_log("test-service_name", "test-container_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_service_deployments(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_deployments.return_value = {}
    get_container_service_deployments("test-service_name", region_name=REGION)
    mock_client.get_container_service_deployments.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_service_deployments_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_service_deployments",
    )
    with pytest.raises(RuntimeError, match="Failed to get container service deployments"):
        get_container_service_deployments("test-service_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_service_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_metric_data.return_value = {}
    get_container_service_metric_data("test-service_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], region_name=REGION)
    mock_client.get_container_service_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_service_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_service_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get container service metric data"):
        get_container_service_metric_data("test-service_name", "test-metric_name", "test-start_time", "test-end_time", 1, [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_service_powers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_powers.return_value = {}
    get_container_service_powers(region_name=REGION)
    mock_client.get_container_service_powers.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_service_powers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_service_powers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_service_powers",
    )
    with pytest.raises(RuntimeError, match="Failed to get container service powers"):
        get_container_service_powers(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_container_services(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_services.return_value = {}
    get_container_services(region_name=REGION)
    mock_client.get_container_services.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_container_services_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_container_services.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_container_services",
    )
    with pytest.raises(RuntimeError, match="Failed to get container services"):
        get_container_services(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_cost_estimate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cost_estimate.return_value = {}
    get_cost_estimate("test-resource_name", "test-start_time", "test-end_time", region_name=REGION)
    mock_client.get_cost_estimate.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_cost_estimate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cost_estimate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cost_estimate",
    )
    with pytest.raises(RuntimeError, match="Failed to get cost estimate"):
        get_cost_estimate("test-resource_name", "test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_disk(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk.return_value = {}
    get_disk("test-disk_name", region_name=REGION)
    mock_client.get_disk.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_disk_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_disk",
    )
    with pytest.raises(RuntimeError, match="Failed to get disk"):
        get_disk("test-disk_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_disk_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk_snapshot.return_value = {}
    get_disk_snapshot("test-disk_snapshot_name", region_name=REGION)
    mock_client.get_disk_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_disk_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_disk_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to get disk snapshot"):
        get_disk_snapshot("test-disk_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_disk_snapshots(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk_snapshots.return_value = {}
    get_disk_snapshots(region_name=REGION)
    mock_client.get_disk_snapshots.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_disk_snapshots_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disk_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_disk_snapshots",
    )
    with pytest.raises(RuntimeError, match="Failed to get disk snapshots"):
        get_disk_snapshots(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_disks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disks.return_value = {}
    get_disks(region_name=REGION)
    mock_client.get_disks.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_disks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_disks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_disks",
    )
    with pytest.raises(RuntimeError, match="Failed to get disks"):
        get_disks(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_distribution_bundles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_bundles.return_value = {}
    get_distribution_bundles(region_name=REGION)
    mock_client.get_distribution_bundles.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_distribution_bundles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_bundles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_bundles",
    )
    with pytest.raises(RuntimeError, match="Failed to get distribution bundles"):
        get_distribution_bundles(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_distribution_latest_cache_reset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_latest_cache_reset.return_value = {}
    get_distribution_latest_cache_reset(region_name=REGION)
    mock_client.get_distribution_latest_cache_reset.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_distribution_latest_cache_reset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_latest_cache_reset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_latest_cache_reset",
    )
    with pytest.raises(RuntimeError, match="Failed to get distribution latest cache reset"):
        get_distribution_latest_cache_reset(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_distribution_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_metric_data.return_value = {}
    get_distribution_metric_data("test-distribution_name", "test-metric_name", "test-start_time", "test-end_time", 1, "test-unit", [], region_name=REGION)
    mock_client.get_distribution_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_distribution_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distribution_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distribution_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get distribution metric data"):
        get_distribution_metric_data("test-distribution_name", "test-metric_name", "test-start_time", "test-end_time", 1, "test-unit", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_distributions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distributions.return_value = {}
    get_distributions(region_name=REGION)
    mock_client.get_distributions.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_distributions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_distributions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_distributions",
    )
    with pytest.raises(RuntimeError, match="Failed to get distributions"):
        get_distributions(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_domain(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domain.return_value = {}
    get_domain("test-domain_name", region_name=REGION)
    mock_client.get_domain.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_domain_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain",
    )
    with pytest.raises(RuntimeError, match="Failed to get domain"):
        get_domain("test-domain_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_domains(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domains.return_value = {}
    get_domains(region_name=REGION)
    mock_client.get_domains.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_domains_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_domains.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domains",
    )
    with pytest.raises(RuntimeError, match="Failed to get domains"):
        get_domains(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_export_snapshot_records(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_export_snapshot_records.return_value = {}
    get_export_snapshot_records(region_name=REGION)
    mock_client.get_export_snapshot_records.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_export_snapshot_records_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_export_snapshot_records.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_export_snapshot_records",
    )
    with pytest.raises(RuntimeError, match="Failed to get export snapshot records"):
        get_export_snapshot_records(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_instance_access_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_access_details.return_value = {}
    get_instance_access_details("test-instance_name", region_name=REGION)
    mock_client.get_instance_access_details.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_instance_access_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_access_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_access_details",
    )
    with pytest.raises(RuntimeError, match="Failed to get instance access details"):
        get_instance_access_details("test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_instance_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_metric_data.return_value = {}
    get_instance_metric_data("test-instance_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)
    mock_client.get_instance_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_instance_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get instance metric data"):
        get_instance_metric_data("test-instance_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_instance_port_states(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_port_states.return_value = {}
    get_instance_port_states("test-instance_name", region_name=REGION)
    mock_client.get_instance_port_states.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_instance_port_states_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_port_states.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_port_states",
    )
    with pytest.raises(RuntimeError, match="Failed to get instance port states"):
        get_instance_port_states("test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_instance_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_snapshot.return_value = {}
    get_instance_snapshot("test-instance_snapshot_name", region_name=REGION)
    mock_client.get_instance_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_instance_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to get instance snapshot"):
        get_instance_snapshot("test-instance_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_instance_state(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_state.return_value = {}
    get_instance_state("test-instance_name", region_name=REGION)
    mock_client.get_instance_state.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_instance_state_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_instance_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_state",
    )
    with pytest.raises(RuntimeError, match="Failed to get instance state"):
        get_instance_state("test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_key_pair.return_value = {}
    get_key_pair("test-key_pair_name", region_name=REGION)
    mock_client.get_key_pair.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to get key pair"):
        get_key_pair("test-key_pair_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_key_pairs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_key_pairs.return_value = {}
    get_key_pairs(region_name=REGION)
    mock_client.get_key_pairs.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_key_pairs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_key_pairs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_key_pairs",
    )
    with pytest.raises(RuntimeError, match="Failed to get key pairs"):
        get_key_pairs(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer.return_value = {}
    get_load_balancer("test-load_balancer_name", region_name=REGION)
    mock_client.get_load_balancer.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_load_balancer",
    )
    with pytest.raises(RuntimeError, match="Failed to get load balancer"):
        get_load_balancer("test-load_balancer_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_metric_data.return_value = {}
    get_load_balancer_metric_data("test-load_balancer_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)
    mock_client.get_load_balancer_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_load_balancer_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get load balancer metric data"):
        get_load_balancer_metric_data("test-load_balancer_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_tls_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_tls_certificates.return_value = {}
    get_load_balancer_tls_certificates("test-load_balancer_name", region_name=REGION)
    mock_client.get_load_balancer_tls_certificates.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_tls_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_tls_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_load_balancer_tls_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to get load balancer tls certificates"):
        get_load_balancer_tls_certificates("test-load_balancer_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_tls_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_tls_policies.return_value = {}
    get_load_balancer_tls_policies(region_name=REGION)
    mock_client.get_load_balancer_tls_policies.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_load_balancer_tls_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancer_tls_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_load_balancer_tls_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to get load balancer tls policies"):
        get_load_balancer_tls_policies(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_load_balancers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancers.return_value = {}
    get_load_balancers(region_name=REGION)
    mock_client.get_load_balancers.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_load_balancers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_load_balancers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_load_balancers",
    )
    with pytest.raises(RuntimeError, match="Failed to get load balancers"):
        get_load_balancers(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_operation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operation.return_value = {}
    get_operation("test-operation_id", region_name=REGION)
    mock_client.get_operation.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_operation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_operation",
    )
    with pytest.raises(RuntimeError, match="Failed to get operation"):
        get_operation("test-operation_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_operations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operations.return_value = {}
    get_operations(region_name=REGION)
    mock_client.get_operations.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_operations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_operations",
    )
    with pytest.raises(RuntimeError, match="Failed to get operations"):
        get_operations(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_operations_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operations_for_resource.return_value = {}
    get_operations_for_resource("test-resource_name", region_name=REGION)
    mock_client.get_operations_for_resource.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_operations_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_operations_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_operations_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to get operations for resource"):
        get_operations_for_resource("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_regions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_regions.return_value = {}
    get_regions(region_name=REGION)
    mock_client.get_regions.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_regions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_regions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_regions",
    )
    with pytest.raises(RuntimeError, match="Failed to get regions"):
        get_regions(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database.return_value = {}
    get_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.get_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database"):
        get_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_blueprints(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_blueprints.return_value = {}
    get_relational_database_blueprints(region_name=REGION)
    mock_client.get_relational_database_blueprints.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_blueprints_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_blueprints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_blueprints",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database blueprints"):
        get_relational_database_blueprints(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_bundles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_bundles.return_value = {}
    get_relational_database_bundles(region_name=REGION)
    mock_client.get_relational_database_bundles.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_bundles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_bundles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_bundles",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database bundles"):
        get_relational_database_bundles(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_events.return_value = {}
    get_relational_database_events("test-relational_database_name", region_name=REGION)
    mock_client.get_relational_database_events.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_events",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database events"):
        get_relational_database_events("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_log_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_log_events.return_value = {}
    get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", region_name=REGION)
    mock_client.get_relational_database_log_events.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_log_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_log_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_log_events",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database log events"):
        get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_log_streams(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_log_streams.return_value = {}
    get_relational_database_log_streams("test-relational_database_name", region_name=REGION)
    mock_client.get_relational_database_log_streams.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_log_streams_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_log_streams.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_log_streams",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database log streams"):
        get_relational_database_log_streams("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_master_user_password(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_master_user_password.return_value = {}
    get_relational_database_master_user_password("test-relational_database_name", region_name=REGION)
    mock_client.get_relational_database_master_user_password.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_master_user_password_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_master_user_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_master_user_password",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database master user password"):
        get_relational_database_master_user_password("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_metric_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_metric_data.return_value = {}
    get_relational_database_metric_data("test-relational_database_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)
    mock_client.get_relational_database_metric_data.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_metric_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_metric_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database metric data"):
        get_relational_database_metric_data("test-relational_database_name", "test-metric_name", 1, "test-start_time", "test-end_time", "test-unit", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_parameters.return_value = {}
    get_relational_database_parameters("test-relational_database_name", region_name=REGION)
    mock_client.get_relational_database_parameters.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database parameters"):
        get_relational_database_parameters("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_snapshot.return_value = {}
    get_relational_database_snapshot("test-relational_database_snapshot_name", region_name=REGION)
    mock_client.get_relational_database_snapshot.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database snapshot"):
        get_relational_database_snapshot("test-relational_database_snapshot_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_snapshots(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_snapshots.return_value = {}
    get_relational_database_snapshots(region_name=REGION)
    mock_client.get_relational_database_snapshots.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_database_snapshots_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_database_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_database_snapshots",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational database snapshots"):
        get_relational_database_snapshots(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_relational_databases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_databases.return_value = {}
    get_relational_databases(region_name=REGION)
    mock_client.get_relational_databases.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_relational_databases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_relational_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_relational_databases",
    )
    with pytest.raises(RuntimeError, match="Failed to get relational databases"):
        get_relational_databases(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_setup_history(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_setup_history.return_value = {}
    get_setup_history("test-resource_name", region_name=REGION)
    mock_client.get_setup_history.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_setup_history_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_setup_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_setup_history",
    )
    with pytest.raises(RuntimeError, match="Failed to get setup history"):
        get_setup_history("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_get_static_ips(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_static_ips.return_value = {}
    get_static_ips(region_name=REGION)
    mock_client.get_static_ips.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_get_static_ips_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_static_ips.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_static_ips",
    )
    with pytest.raises(RuntimeError, match="Failed to get static ips"):
        get_static_ips(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_import_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_key_pair.return_value = {}
    import_key_pair("test-key_pair_name", "test-public_key_base64", region_name=REGION)
    mock_client.import_key_pair.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_import_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to import key pair"):
        import_key_pair("test-key_pair_name", "test-public_key_base64", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_is_vpc_peered(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.is_vpc_peered.return_value = {}
    is_vpc_peered(region_name=REGION)
    mock_client.is_vpc_peered.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_is_vpc_peered_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.is_vpc_peered.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "is_vpc_peered",
    )
    with pytest.raises(RuntimeError, match="Failed to is vpc peered"):
        is_vpc_peered(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_open_instance_public_ports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.open_instance_public_ports.return_value = {}
    open_instance_public_ports({}, "test-instance_name", region_name=REGION)
    mock_client.open_instance_public_ports.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_open_instance_public_ports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.open_instance_public_ports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "open_instance_public_ports",
    )
    with pytest.raises(RuntimeError, match="Failed to open instance public ports"):
        open_instance_public_ports({}, "test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_peer_vpc(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.peer_vpc.return_value = {}
    peer_vpc(region_name=REGION)
    mock_client.peer_vpc.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_peer_vpc_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.peer_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "peer_vpc",
    )
    with pytest.raises(RuntimeError, match="Failed to peer vpc"):
        peer_vpc(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_put_alarm(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_alarm.return_value = {}
    put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", 1, region_name=REGION)
    mock_client.put_alarm.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_put_alarm_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_alarm.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_alarm",
    )
    with pytest.raises(RuntimeError, match="Failed to put alarm"):
        put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", 1, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_put_instance_public_ports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_instance_public_ports.return_value = {}
    put_instance_public_ports([], "test-instance_name", region_name=REGION)
    mock_client.put_instance_public_ports.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_put_instance_public_ports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_instance_public_ports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_instance_public_ports",
    )
    with pytest.raises(RuntimeError, match="Failed to put instance public ports"):
        put_instance_public_ports([], "test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_reboot_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_relational_database.return_value = {}
    reboot_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.reboot_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_reboot_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to reboot relational database"):
        reboot_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_register_container_image(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_container_image.return_value = {}
    register_container_image("test-service_name", "test-label", "test-digest", region_name=REGION)
    mock_client.register_container_image.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_register_container_image_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_container_image.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_container_image",
    )
    with pytest.raises(RuntimeError, match="Failed to register container image"):
        register_container_image("test-service_name", "test-label", "test-digest", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_reset_distribution_cache(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_distribution_cache.return_value = {}
    reset_distribution_cache(region_name=REGION)
    mock_client.reset_distribution_cache.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_reset_distribution_cache_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_distribution_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_distribution_cache",
    )
    with pytest.raises(RuntimeError, match="Failed to reset distribution cache"):
        reset_distribution_cache(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_run_alarm(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_alarm.return_value = {}
    run_alarm("test-alarm_name", "test-state", region_name=REGION)
    mock_client.test_alarm.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_run_alarm_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_alarm.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_alarm",
    )
    with pytest.raises(RuntimeError, match="Failed to run alarm"):
        run_alarm("test-alarm_name", "test-state", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_send_contact_method_verification(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_contact_method_verification.return_value = {}
    send_contact_method_verification("test-protocol", region_name=REGION)
    mock_client.send_contact_method_verification.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_send_contact_method_verification_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_contact_method_verification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_contact_method_verification",
    )
    with pytest.raises(RuntimeError, match="Failed to send contact method verification"):
        send_contact_method_verification("test-protocol", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_set_ip_address_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_ip_address_type.return_value = {}
    set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", region_name=REGION)
    mock_client.set_ip_address_type.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_set_ip_address_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_ip_address_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_ip_address_type",
    )
    with pytest.raises(RuntimeError, match="Failed to set ip address type"):
        set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_set_resource_access_for_bucket(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_resource_access_for_bucket.return_value = {}
    set_resource_access_for_bucket("test-resource_name", "test-bucket_name", "test-access", region_name=REGION)
    mock_client.set_resource_access_for_bucket.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_set_resource_access_for_bucket_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_resource_access_for_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_resource_access_for_bucket",
    )
    with pytest.raises(RuntimeError, match="Failed to set resource access for bucket"):
        set_resource_access_for_bucket("test-resource_name", "test-bucket_name", "test-access", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_setup_instance_https(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.setup_instance_https.return_value = {}
    setup_instance_https("test-instance_name", "test-email_address", [], "test-certificate_provider", region_name=REGION)
    mock_client.setup_instance_https.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_setup_instance_https_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.setup_instance_https.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "setup_instance_https",
    )
    with pytest.raises(RuntimeError, match="Failed to setup instance https"):
        setup_instance_https("test-instance_name", "test-email_address", [], "test-certificate_provider", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_start_gui_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_gui_session.return_value = {}
    start_gui_session("test-resource_name", region_name=REGION)
    mock_client.start_gui_session.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_start_gui_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_gui_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_gui_session",
    )
    with pytest.raises(RuntimeError, match="Failed to start gui session"):
        start_gui_session("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_start_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_relational_database.return_value = {}
    start_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.start_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_start_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to start relational database"):
        start_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_stop_gui_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_gui_session.return_value = {}
    stop_gui_session("test-resource_name", region_name=REGION)
    mock_client.stop_gui_session.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_stop_gui_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_gui_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_gui_session",
    )
    with pytest.raises(RuntimeError, match="Failed to stop gui session"):
        stop_gui_session("test-resource_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_stop_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_relational_database.return_value = {}
    stop_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.stop_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_stop_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to stop relational database"):
        stop_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_name", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_unpeer_vpc(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unpeer_vpc.return_value = {}
    unpeer_vpc(region_name=REGION)
    mock_client.unpeer_vpc.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_unpeer_vpc_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unpeer_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unpeer_vpc",
    )
    with pytest.raises(RuntimeError, match="Failed to unpeer vpc"):
        unpeer_vpc(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_name", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_bucket(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bucket.return_value = {}
    update_bucket("test-bucket_name", region_name=REGION)
    mock_client.update_bucket.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_bucket_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bucket.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bucket",
    )
    with pytest.raises(RuntimeError, match="Failed to update bucket"):
        update_bucket("test-bucket_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_bucket_bundle(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bucket_bundle.return_value = {}
    update_bucket_bundle("test-bucket_name", "test-bundle_id", region_name=REGION)
    mock_client.update_bucket_bundle.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_bucket_bundle_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_bucket_bundle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bucket_bundle",
    )
    with pytest.raises(RuntimeError, match="Failed to update bucket bundle"):
        update_bucket_bundle("test-bucket_name", "test-bundle_id", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_container_service(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_container_service.return_value = {}
    update_container_service("test-service_name", region_name=REGION)
    mock_client.update_container_service.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_container_service_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_container_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_container_service",
    )
    with pytest.raises(RuntimeError, match="Failed to update container service"):
        update_container_service("test-service_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_distribution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_distribution.return_value = {}
    update_distribution("test-distribution_name", region_name=REGION)
    mock_client.update_distribution.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_distribution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_distribution",
    )
    with pytest.raises(RuntimeError, match="Failed to update distribution"):
        update_distribution("test-distribution_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_distribution_bundle(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_distribution_bundle.return_value = {}
    update_distribution_bundle(region_name=REGION)
    mock_client.update_distribution_bundle.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_distribution_bundle_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_distribution_bundle.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_distribution_bundle",
    )
    with pytest.raises(RuntimeError, match="Failed to update distribution bundle"):
        update_distribution_bundle(region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_domain_entry(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_domain_entry.return_value = {}
    update_domain_entry("test-domain_name", {}, region_name=REGION)
    mock_client.update_domain_entry.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_domain_entry_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_domain_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_domain_entry",
    )
    with pytest.raises(RuntimeError, match="Failed to update domain entry"):
        update_domain_entry("test-domain_name", {}, region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_instance_metadata_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_instance_metadata_options.return_value = {}
    update_instance_metadata_options("test-instance_name", region_name=REGION)
    mock_client.update_instance_metadata_options.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_instance_metadata_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_instance_metadata_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_instance_metadata_options",
    )
    with pytest.raises(RuntimeError, match="Failed to update instance metadata options"):
        update_instance_metadata_options("test-instance_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_load_balancer_attribute(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_load_balancer_attribute.return_value = {}
    update_load_balancer_attribute("test-load_balancer_name", "test-attribute_name", "test-attribute_value", region_name=REGION)
    mock_client.update_load_balancer_attribute.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_load_balancer_attribute_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_load_balancer_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_load_balancer_attribute",
    )
    with pytest.raises(RuntimeError, match="Failed to update load balancer attribute"):
        update_load_balancer_attribute("test-load_balancer_name", "test-attribute_name", "test-attribute_value", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_relational_database(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_relational_database.return_value = {}
    update_relational_database("test-relational_database_name", region_name=REGION)
    mock_client.update_relational_database.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_relational_database_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_relational_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_relational_database",
    )
    with pytest.raises(RuntimeError, match="Failed to update relational database"):
        update_relational_database("test-relational_database_name", region_name=REGION)


@patch("aws_util.lightsail.get_client")
def test_update_relational_database_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_relational_database_parameters.return_value = {}
    update_relational_database_parameters("test-relational_database_name", [], region_name=REGION)
    mock_client.update_relational_database_parameters.assert_called_once()


@patch("aws_util.lightsail.get_client")
def test_update_relational_database_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_relational_database_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_relational_database_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to update relational database parameters"):
        update_relational_database_parameters("test-relational_database_name", [], region_name=REGION)


def test_attach_disk_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import attach_disk
    mock_client = MagicMock()
    mock_client.attach_disk.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    attach_disk("test-disk_name", "test-instance_name", "test-disk_path", auto_mounting=True, region_name="us-east-1")
    mock_client.attach_disk.assert_called_once()

def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import copy_snapshot
    mock_client = MagicMock()
    mock_client.copy_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    copy_snapshot("test-target_snapshot_name", "test-source_region", source_snapshot_name="test-source_snapshot_name", source_resource_name="test-source_resource_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.copy_snapshot.assert_called_once()

def test_create_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_bucket
    mock_client = MagicMock()
    mock_client.create_bucket.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_bucket("test-bucket_name", "test-bundle_id", tags=[{"Key": "k", "Value": "v"}], enable_object_versioning=True, region_name="us-east-1")
    mock_client.create_bucket.assert_called_once()

def test_create_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_certificate
    mock_client = MagicMock()
    mock_client.create_certificate.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_certificate("test-certificate_name", "test-domain_name", subject_alternative_names="test-subject_alternative_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_certificate.assert_called_once()

def test_create_container_service_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_container_service
    mock_client = MagicMock()
    mock_client.create_container_service.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_container_service("test-service_name", "test-power", "test-scale", tags=[{"Key": "k", "Value": "v"}], public_domain_names="test-public_domain_names", deployment="test-deployment", private_registry_access="test-private_registry_access", region_name="us-east-1")
    mock_client.create_container_service.assert_called_once()

def test_create_container_service_deployment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_container_service_deployment
    mock_client = MagicMock()
    mock_client.create_container_service_deployment.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_container_service_deployment("test-service_name", containers="test-containers", public_endpoint="test-public_endpoint", region_name="us-east-1")
    mock_client.create_container_service_deployment.assert_called_once()

def test_create_disk_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_disk
    mock_client = MagicMock()
    mock_client.create_disk.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_disk("test-disk_name", "test-availability_zone", 1, tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", region_name="us-east-1")
    mock_client.create_disk.assert_called_once()

def test_create_disk_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_disk_from_snapshot
    mock_client = MagicMock()
    mock_client.create_disk_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_disk_from_snapshot("test-disk_name", "test-availability_zone", 1, disk_snapshot_name="test-disk_snapshot_name", tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", source_disk_name="test-source_disk_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.create_disk_from_snapshot.assert_called_once()

def test_create_disk_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_disk_snapshot
    mock_client = MagicMock()
    mock_client.create_disk_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_disk_snapshot("test-disk_snapshot_name", disk_name="test-disk_name", instance_name="test-instance_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_disk_snapshot.assert_called_once()

def test_create_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_distribution
    mock_client = MagicMock()
    mock_client.create_distribution.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_distribution("test-distribution_name", "test-origin", "test-default_cache_behavior", "test-bundle_id", cache_behavior_settings={}, cache_behaviors="test-cache_behaviors", ip_address_type="test-ip_address_type", tags=[{"Key": "k", "Value": "v"}], certificate_name="test-certificate_name", viewer_minimum_tls_protocol_version="test-viewer_minimum_tls_protocol_version", region_name="us-east-1")
    mock_client.create_distribution.assert_called_once()

def test_create_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_domain
    mock_client = MagicMock()
    mock_client.create_domain.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_domain("test-domain_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_domain.assert_called_once()

def test_create_instances_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_instances_from_snapshot
    mock_client = MagicMock()
    mock_client.create_instances_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_instances_from_snapshot("test-instance_names", "test-availability_zone", "test-bundle_id", attached_disk_mapping={}, instance_snapshot_name="test-instance_snapshot_name", user_data="test-user_data", key_pair_name="test-key_pair_name", tags=[{"Key": "k", "Value": "v"}], add_ons="test-add_ons", ip_address_type="test-ip_address_type", source_instance_name="test-source_instance_name", restore_date="test-restore_date", use_latest_restorable_auto_snapshot=True, region_name="us-east-1")
    mock_client.create_instances_from_snapshot.assert_called_once()

def test_create_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_key_pair
    mock_client = MagicMock()
    mock_client.create_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_key_pair("test-key_pair_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_key_pair.assert_called_once()

def test_create_load_balancer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_load_balancer
    mock_client = MagicMock()
    mock_client.create_load_balancer.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_load_balancer("test-load_balancer_name", 1, health_check_path="test-health_check_path", certificate_name="test-certificate_name", certificate_domain_name="test-certificate_domain_name", certificate_alternative_names="test-certificate_alternative_names", tags=[{"Key": "k", "Value": "v"}], ip_address_type="test-ip_address_type", tls_policy_name="test-tls_policy_name", region_name="us-east-1")
    mock_client.create_load_balancer.assert_called_once()

def test_create_load_balancer_tls_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_load_balancer_tls_certificate
    mock_client = MagicMock()
    mock_client.create_load_balancer_tls_certificate.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", "test-certificate_domain_name", certificate_alternative_names="test-certificate_alternative_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_load_balancer_tls_certificate.assert_called_once()

def test_create_relational_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_relational_database
    mock_client = MagicMock()
    mock_client.create_relational_database.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_relational_database("test-relational_database_name", "test-relational_database_blueprint_id", "test-relational_database_bundle_id", "test-master_database_name", "test-master_username", availability_zone="test-availability_zone", master_user_password="test-master_user_password", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_relational_database.assert_called_once()

def test_create_relational_database_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_relational_database_from_snapshot
    mock_client = MagicMock()
    mock_client.create_relational_database_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_relational_database_from_snapshot("test-relational_database_name", availability_zone="test-availability_zone", publicly_accessible="test-publicly_accessible", relational_database_snapshot_name="test-relational_database_snapshot_name", relational_database_bundle_id="test-relational_database_bundle_id", source_relational_database_name="test-source_relational_database_name", restore_time="test-restore_time", use_latest_restorable_time=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_relational_database_from_snapshot.assert_called_once()

def test_create_relational_database_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import create_relational_database_snapshot
    mock_client = MagicMock()
    mock_client.create_relational_database_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    create_relational_database_snapshot("test-relational_database_name", "test-relational_database_snapshot_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_relational_database_snapshot.assert_called_once()

def test_delete_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_bucket
    mock_client = MagicMock()
    mock_client.delete_bucket.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_bucket("test-bucket_name", force_delete=True, region_name="us-east-1")
    mock_client.delete_bucket.assert_called_once()

def test_delete_disk_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_disk
    mock_client = MagicMock()
    mock_client.delete_disk.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_disk("test-disk_name", force_delete_add_ons=True, region_name="us-east-1")
    mock_client.delete_disk.assert_called_once()

def test_delete_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_distribution
    mock_client = MagicMock()
    mock_client.delete_distribution.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_distribution(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.delete_distribution.assert_called_once()

def test_delete_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_key_pair
    mock_client = MagicMock()
    mock_client.delete_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_key_pair("test-key_pair_name", expected_fingerprint="test-expected_fingerprint", region_name="us-east-1")
    mock_client.delete_key_pair.assert_called_once()

def test_delete_load_balancer_tls_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_load_balancer_tls_certificate
    mock_client = MagicMock()
    mock_client.delete_load_balancer_tls_certificate.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_load_balancer_tls_certificate("test-load_balancer_name", "test-certificate_name", force=True, region_name="us-east-1")
    mock_client.delete_load_balancer_tls_certificate.assert_called_once()

def test_delete_relational_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import delete_relational_database
    mock_client = MagicMock()
    mock_client.delete_relational_database.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    delete_relational_database("test-relational_database_name", skip_final_snapshot=True, final_relational_database_snapshot_name="test-final_relational_database_snapshot_name", region_name="us-east-1")
    mock_client.delete_relational_database.assert_called_once()

def test_get_active_names_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_active_names
    mock_client = MagicMock()
    mock_client.get_active_names.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_active_names(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_active_names.assert_called_once()

def test_get_alarms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_alarms
    mock_client = MagicMock()
    mock_client.get_alarms.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_alarms(alarm_name="test-alarm_name", page_token="test-page_token", monitored_resource_name="test-monitored_resource_name", region_name="us-east-1")
    mock_client.get_alarms.assert_called_once()

def test_get_blueprints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_blueprints
    mock_client = MagicMock()
    mock_client.get_blueprints.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_blueprints(include_inactive=True, page_token="test-page_token", app_category="test-app_category", region_name="us-east-1")
    mock_client.get_blueprints.assert_called_once()

def test_get_bucket_bundles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_bucket_bundles
    mock_client = MagicMock()
    mock_client.get_bucket_bundles.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_bucket_bundles(include_inactive=True, region_name="us-east-1")
    mock_client.get_bucket_bundles.assert_called_once()

def test_get_buckets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_buckets
    mock_client = MagicMock()
    mock_client.get_buckets.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_buckets(bucket_name="test-bucket_name", page_token="test-page_token", include_connected_resources=True, include_cors=True, region_name="us-east-1")
    mock_client.get_buckets.assert_called_once()

def test_get_bundles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_bundles
    mock_client = MagicMock()
    mock_client.get_bundles.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_bundles(include_inactive=True, page_token="test-page_token", app_category="test-app_category", region_name="us-east-1")
    mock_client.get_bundles.assert_called_once()

def test_get_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_certificates
    mock_client = MagicMock()
    mock_client.get_certificates.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_certificates(certificate_statuses="test-certificate_statuses", include_certificate_details=True, certificate_name="test-certificate_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_certificates.assert_called_once()

def test_get_cloud_formation_stack_records_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_cloud_formation_stack_records
    mock_client = MagicMock()
    mock_client.get_cloud_formation_stack_records.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_cloud_formation_stack_records(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_cloud_formation_stack_records.assert_called_once()

def test_get_contact_methods_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_contact_methods
    mock_client = MagicMock()
    mock_client.get_contact_methods.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_contact_methods(protocols="test-protocols", region_name="us-east-1")
    mock_client.get_contact_methods.assert_called_once()

def test_get_container_log_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_container_log
    mock_client = MagicMock()
    mock_client.get_container_log.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_container_log("test-service_name", "test-container_name", start_time="test-start_time", end_time="test-end_time", filter_pattern="test-filter_pattern", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_container_log.assert_called_once()

def test_get_container_services_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_container_services
    mock_client = MagicMock()
    mock_client.get_container_services.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_container_services(service_name="test-service_name", region_name="us-east-1")
    mock_client.get_container_services.assert_called_once()

def test_get_disk_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_disk_snapshots
    mock_client = MagicMock()
    mock_client.get_disk_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_disk_snapshots(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_disk_snapshots.assert_called_once()

def test_get_disks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_disks
    mock_client = MagicMock()
    mock_client.get_disks.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_disks(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_disks.assert_called_once()

def test_get_distribution_latest_cache_reset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_distribution_latest_cache_reset
    mock_client = MagicMock()
    mock_client.get_distribution_latest_cache_reset.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_distribution_latest_cache_reset(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.get_distribution_latest_cache_reset.assert_called_once()

def test_get_distributions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_distributions
    mock_client = MagicMock()
    mock_client.get_distributions.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_distributions(distribution_name="test-distribution_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_distributions.assert_called_once()

def test_get_domains_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_domains
    mock_client = MagicMock()
    mock_client.get_domains.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_domains(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_domains.assert_called_once()

def test_get_export_snapshot_records_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_export_snapshot_records
    mock_client = MagicMock()
    mock_client.get_export_snapshot_records.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_export_snapshot_records(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_export_snapshot_records.assert_called_once()

def test_get_instance_access_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_instance_access_details
    mock_client = MagicMock()
    mock_client.get_instance_access_details.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_instance_access_details("test-instance_name", protocol="test-protocol", region_name="us-east-1")
    mock_client.get_instance_access_details.assert_called_once()

def test_get_key_pairs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_key_pairs
    mock_client = MagicMock()
    mock_client.get_key_pairs.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_key_pairs(page_token="test-page_token", include_default_key_pair=True, region_name="us-east-1")
    mock_client.get_key_pairs.assert_called_once()

def test_get_load_balancer_tls_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_load_balancer_tls_policies
    mock_client = MagicMock()
    mock_client.get_load_balancer_tls_policies.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_load_balancer_tls_policies(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_load_balancer_tls_policies.assert_called_once()

def test_get_load_balancers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_load_balancers
    mock_client = MagicMock()
    mock_client.get_load_balancers.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_load_balancers(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_load_balancers.assert_called_once()

def test_get_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_operations
    mock_client = MagicMock()
    mock_client.get_operations.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_operations(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_operations.assert_called_once()

def test_get_operations_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_operations_for_resource
    mock_client = MagicMock()
    mock_client.get_operations_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_operations_for_resource("test-resource_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_operations_for_resource.assert_called_once()

def test_get_regions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_regions
    mock_client = MagicMock()
    mock_client.get_regions.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_regions(include_availability_zones=True, include_relational_database_availability_zones=True, region_name="us-east-1")
    mock_client.get_regions.assert_called_once()

def test_get_relational_database_blueprints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_blueprints
    mock_client = MagicMock()
    mock_client.get_relational_database_blueprints.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_blueprints(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_database_blueprints.assert_called_once()

def test_get_relational_database_bundles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_bundles
    mock_client = MagicMock()
    mock_client.get_relational_database_bundles.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_bundles(page_token="test-page_token", include_inactive=True, region_name="us-east-1")
    mock_client.get_relational_database_bundles.assert_called_once()

def test_get_relational_database_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_events
    mock_client = MagicMock()
    mock_client.get_relational_database_events.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_events("test-relational_database_name", duration_in_minutes=1, page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_database_events.assert_called_once()

def test_get_relational_database_log_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_log_events
    mock_client = MagicMock()
    mock_client.get_relational_database_log_events.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_log_events("test-relational_database_name", "test-log_stream_name", start_time="test-start_time", end_time="test-end_time", start_from_head="test-start_from_head", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_database_log_events.assert_called_once()

def test_get_relational_database_master_user_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_master_user_password
    mock_client = MagicMock()
    mock_client.get_relational_database_master_user_password.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_master_user_password("test-relational_database_name", password_version="test-password_version", region_name="us-east-1")
    mock_client.get_relational_database_master_user_password.assert_called_once()

def test_get_relational_database_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_parameters
    mock_client = MagicMock()
    mock_client.get_relational_database_parameters.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_parameters("test-relational_database_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_database_parameters.assert_called_once()

def test_get_relational_database_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_database_snapshots
    mock_client = MagicMock()
    mock_client.get_relational_database_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_database_snapshots(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_database_snapshots.assert_called_once()

def test_get_relational_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_relational_databases
    mock_client = MagicMock()
    mock_client.get_relational_databases.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_relational_databases(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_relational_databases.assert_called_once()

def test_get_setup_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_setup_history
    mock_client = MagicMock()
    mock_client.get_setup_history.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_setup_history("test-resource_name", page_token="test-page_token", region_name="us-east-1")
    mock_client.get_setup_history.assert_called_once()

def test_get_static_ips_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import get_static_ips
    mock_client = MagicMock()
    mock_client.get_static_ips.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    get_static_ips(page_token="test-page_token", region_name="us-east-1")
    mock_client.get_static_ips.assert_called_once()

def test_put_alarm_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import put_alarm
    mock_client = MagicMock()
    mock_client.put_alarm.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    put_alarm("test-alarm_name", "test-metric_name", "test-monitored_resource_name", "test-comparison_operator", "test-threshold", "test-evaluation_periods", datapoints_to_alarm="test-datapoints_to_alarm", treat_missing_data="test-treat_missing_data", contact_protocols="test-contact_protocols", notification_triggers="test-notification_triggers", notification_enabled="test-notification_enabled", region_name="us-east-1")
    mock_client.put_alarm.assert_called_once()

def test_reset_distribution_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import reset_distribution_cache
    mock_client = MagicMock()
    mock_client.reset_distribution_cache.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    reset_distribution_cache(distribution_name="test-distribution_name", region_name="us-east-1")
    mock_client.reset_distribution_cache.assert_called_once()

def test_set_ip_address_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import set_ip_address_type
    mock_client = MagicMock()
    mock_client.set_ip_address_type.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    set_ip_address_type("test-resource_type", "test-resource_name", "test-ip_address_type", accept_bundle_update="test-accept_bundle_update", region_name="us-east-1")
    mock_client.set_ip_address_type.assert_called_once()

def test_stop_relational_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import stop_relational_database
    mock_client = MagicMock()
    mock_client.stop_relational_database.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    stop_relational_database("test-relational_database_name", relational_database_snapshot_name="test-relational_database_snapshot_name", region_name="us-east-1")
    mock_client.stop_relational_database.assert_called_once()

def test_tag_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import tag_resource
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_name", [{"Key": "k", "Value": "v"}], resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.tag_resource.assert_called_once()

def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import untag_resource
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_name", "test-tag_keys", resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.untag_resource.assert_called_once()

def test_update_bucket_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_bucket
    mock_client = MagicMock()
    mock_client.update_bucket.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_bucket("test-bucket_name", access_rules="test-access_rules", versioning="test-versioning", readonly_access_accounts=1, access_log_config={}, cors="test-cors", region_name="us-east-1")
    mock_client.update_bucket.assert_called_once()

def test_update_container_service_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_container_service
    mock_client = MagicMock()
    mock_client.update_container_service.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_container_service("test-service_name", power="test-power", scale="test-scale", is_disabled=True, public_domain_names="test-public_domain_names", private_registry_access="test-private_registry_access", region_name="us-east-1")
    mock_client.update_container_service.assert_called_once()

def test_update_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_distribution
    mock_client = MagicMock()
    mock_client.update_distribution.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_distribution("test-distribution_name", origin="test-origin", default_cache_behavior="test-default_cache_behavior", cache_behavior_settings={}, cache_behaviors="test-cache_behaviors", is_enabled=True, viewer_minimum_tls_protocol_version="test-viewer_minimum_tls_protocol_version", certificate_name="test-certificate_name", use_default_certificate=True, region_name="us-east-1")
    mock_client.update_distribution.assert_called_once()

def test_update_distribution_bundle_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_distribution_bundle
    mock_client = MagicMock()
    mock_client.update_distribution_bundle.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_distribution_bundle(distribution_name="test-distribution_name", bundle_id="test-bundle_id", region_name="us-east-1")
    mock_client.update_distribution_bundle.assert_called_once()

def test_update_instance_metadata_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_instance_metadata_options
    mock_client = MagicMock()
    mock_client.update_instance_metadata_options.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_instance_metadata_options("test-instance_name", http_tokens="test-http_tokens", http_endpoint="test-http_endpoint", http_put_response_hop_limit=1, http_protocol_ipv6="test-http_protocol_ipv6", region_name="us-east-1")
    mock_client.update_instance_metadata_options.assert_called_once()

def test_update_relational_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.lightsail import update_relational_database
    mock_client = MagicMock()
    mock_client.update_relational_database.return_value = {}
    monkeypatch.setattr("aws_util.lightsail.get_client", lambda *a, **kw: mock_client)
    update_relational_database("test-relational_database_name", master_user_password="test-master_user_password", rotate_master_user_password="test-rotate_master_user_password", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", enable_backup_retention=True, disable_backup_retention=True, publicly_accessible="test-publicly_accessible", apply_immediately=True, ca_certificate_identifier="test-ca_certificate_identifier", relational_database_blueprint_id="test-relational_database_blueprint_id", region_name="us-east-1")
    mock_client.update_relational_database.assert_called_once()
