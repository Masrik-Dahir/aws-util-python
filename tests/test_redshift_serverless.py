"""Tests for aws_util.redshift_serverless module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.redshift_serverless as mod
from aws_util.redshift_serverless import (
    NamespaceResult,
    WorkgroupResult,
    _parse_namespace,
    _parse_workgroup,
    create_namespace,
    create_workgroup,
    delete_namespace,
    delete_workgroup,
    get_namespace,
    get_workgroup,
    list_namespaces,
    list_workgroups,
    update_namespace,
    update_workgroup,
    convert_recovery_point_to_snapshot,
    create_custom_domain_association,
    create_endpoint_access,
    create_reservation,
    create_scheduled_action,
    create_snapshot,
    create_snapshot_copy_configuration,
    create_usage_limit,
    delete_custom_domain_association,
    delete_endpoint_access,
    delete_resource_policy,
    delete_scheduled_action,
    delete_snapshot,
    delete_snapshot_copy_configuration,
    delete_usage_limit,
    get_credentials,
    get_custom_domain_association,
    get_endpoint_access,
    get_recovery_point,
    get_reservation,
    get_reservation_offering,
    get_resource_policy,
    get_scheduled_action,
    get_snapshot,
    get_table_restore_status,
    get_track,
    get_usage_limit,
    list_custom_domain_associations,
    list_endpoint_access,
    list_managed_workgroups,
    list_recovery_points,
    list_reservation_offerings,
    list_reservations,
    list_scheduled_actions,
    list_snapshot_copy_configurations,
    list_snapshots,
    list_table_restore_status,
    list_tags_for_resource,
    list_tracks,
    list_usage_limits,
    put_resource_policy,
    restore_from_recovery_point,
    restore_from_snapshot,
    restore_table_from_recovery_point,
    restore_table_from_snapshot,
    tag_resource,
    untag_resource,
    update_custom_domain_association,
    update_endpoint_access,
    update_scheduled_action,
    update_snapshot,
    update_snapshot_copy_configuration,
    update_usage_limit,
)

REGION = "us-east-1"

_NS = {
    "namespaceName": "ns1",
    "namespaceId": "id1",
    "namespaceArn": "arn:ns1",
    "status": "AVAILABLE",
    "adminUsername": "admin",
    "dbName": "mydb",
    "creationDate": "2025-01-01",
    "iamRoles": ["arn:role1"],
    "extraField": "x",
}

_WG = {
    "workgroupName": "wg1",
    "workgroupId": "wgid1",
    "workgroupArn": "arn:wg1",
    "status": "AVAILABLE",
    "namespaceName": "ns1",
    "baseCapacity": 128,
    "creationDate": "2025-01-01",
    "endpoint": {"address": "wg1.endpoint"},
    "extraWg": "y",
}


def _ce(code: str = "ServiceException", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_namespace_result_model():
    r = NamespaceResult(namespace_name="ns")
    assert r.namespace_name == "ns"
    assert r.iam_roles == []


def test_workgroup_result_model():
    r = WorkgroupResult(workgroup_name="wg")
    assert r.workgroup_name == "wg"
    assert r.endpoint == {}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def test_parse_namespace():
    r = _parse_namespace(_NS)
    assert r.namespace_name == "ns1"
    assert r.admin_username == "admin"
    assert r.creation_date == "2025-01-01"
    assert "extraField" in r.extra


def test_parse_namespace_no_date():
    data = {**_NS, "creationDate": None}
    r = _parse_namespace(data)
    assert r.creation_date is None


def test_parse_workgroup():
    r = _parse_workgroup(_WG)
    assert r.workgroup_name == "wg1"
    assert r.base_capacity == 128
    assert "extraWg" in r.extra


def test_parse_workgroup_no_date():
    data = {**_WG, "creationDate": None}
    r = _parse_workgroup(data)
    assert r.creation_date is None


# ---------------------------------------------------------------------------
# create_namespace
# ---------------------------------------------------------------------------


def test_create_namespace_success(monkeypatch):
    client = MagicMock()
    client.create_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_namespace("ns1", region_name=REGION)
    assert r.namespace_name == "ns1"


def test_create_namespace_all_opts(monkeypatch):
    client = MagicMock()
    client.create_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_namespace(
        "ns1",
        admin_username="admin",
        admin_user_password="pw",
        db_name="db",
        iam_roles=["r1"],
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert r.namespace_name == "ns1"


def test_create_namespace_error(monkeypatch):
    client = MagicMock()
    client.create_namespace.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_namespace failed"):
        create_namespace("ns1", region_name=REGION)


# ---------------------------------------------------------------------------
# get_namespace
# ---------------------------------------------------------------------------


def test_get_namespace_success(monkeypatch):
    client = MagicMock()
    client.get_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_namespace("ns1", region_name=REGION)
    assert r.namespace_name == "ns1"


def test_get_namespace_error(monkeypatch):
    client = MagicMock()
    client.get_namespace.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_namespace failed"):
        get_namespace("ns1", region_name=REGION)


# ---------------------------------------------------------------------------
# list_namespaces
# ---------------------------------------------------------------------------


def test_list_namespaces_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"namespaces": [_NS]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_namespaces(region_name=REGION)
    assert len(r) == 1


def test_list_namespaces_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_namespaces failed"):
        list_namespaces(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_namespace
# ---------------------------------------------------------------------------


def test_delete_namespace_success(monkeypatch):
    client = MagicMock()
    client.delete_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = delete_namespace("ns1", region_name=REGION)
    assert r.namespace_name == "ns1"


def test_delete_namespace_with_snapshot(monkeypatch):
    client = MagicMock()
    client.delete_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_namespace("ns1", final_snapshot_name="snap", region_name=REGION)
    kw = client.delete_namespace.call_args[1]
    assert kw["finalSnapshotName"] == "snap"


def test_delete_namespace_error(monkeypatch):
    client = MagicMock()
    client.delete_namespace.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_namespace failed"):
        delete_namespace("ns1", region_name=REGION)


# ---------------------------------------------------------------------------
# update_namespace
# ---------------------------------------------------------------------------


def test_update_namespace_success(monkeypatch):
    client = MagicMock()
    client.update_namespace.return_value = {"namespace": _NS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_namespace(
        "ns1",
        admin_username="new",
        admin_user_password="pw",
        iam_roles=["r2"],
        region_name=REGION,
    )
    assert r.namespace_name == "ns1"


def test_update_namespace_error(monkeypatch):
    client = MagicMock()
    client.update_namespace.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_namespace failed"):
        update_namespace("ns1", region_name=REGION)


# ---------------------------------------------------------------------------
# create_workgroup
# ---------------------------------------------------------------------------


def test_create_workgroup_success(monkeypatch):
    client = MagicMock()
    client.create_workgroup.return_value = {"workgroup": _WG}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_workgroup("wg1", namespace_name="ns1", region_name=REGION)
    assert r.workgroup_name == "wg1"


def test_create_workgroup_all_opts(monkeypatch):
    client = MagicMock()
    client.create_workgroup.return_value = {"workgroup": _WG}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_workgroup(
        "wg1",
        namespace_name="ns1",
        base_capacity=64,
        subnet_ids=["s1"],
        security_group_ids=["sg1"],
        tags=[{"Key": "k", "Value": "v"}],
        region_name=REGION,
    )
    assert r.workgroup_name == "wg1"


def test_create_workgroup_error(monkeypatch):
    client = MagicMock()
    client.create_workgroup.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_workgroup failed"):
        create_workgroup("wg1", namespace_name="ns1", region_name=REGION)


# ---------------------------------------------------------------------------
# get_workgroup
# ---------------------------------------------------------------------------


def test_get_workgroup_success(monkeypatch):
    client = MagicMock()
    client.get_workgroup.return_value = {"workgroup": _WG}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_workgroup("wg1", region_name=REGION)
    assert r.workgroup_name == "wg1"


def test_get_workgroup_error(monkeypatch):
    client = MagicMock()
    client.get_workgroup.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_workgroup failed"):
        get_workgroup("wg1", region_name=REGION)


# ---------------------------------------------------------------------------
# list_workgroups
# ---------------------------------------------------------------------------


def test_list_workgroups_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"workgroups": [_WG]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_workgroups(region_name=REGION)
    assert len(r) == 1


def test_list_workgroups_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_workgroups failed"):
        list_workgroups(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_workgroup
# ---------------------------------------------------------------------------


def test_delete_workgroup_success(monkeypatch):
    client = MagicMock()
    client.delete_workgroup.return_value = {"workgroup": _WG}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = delete_workgroup("wg1", region_name=REGION)
    assert r.workgroup_name == "wg1"


def test_delete_workgroup_error(monkeypatch):
    client = MagicMock()
    client.delete_workgroup.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_workgroup failed"):
        delete_workgroup("wg1", region_name=REGION)


# ---------------------------------------------------------------------------
# update_workgroup
# ---------------------------------------------------------------------------


def test_update_workgroup_success(monkeypatch):
    client = MagicMock()
    client.update_workgroup.return_value = {"workgroup": _WG}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_workgroup(
        "wg1",
        base_capacity=256,
        subnet_ids=["s2"],
        security_group_ids=["sg2"],
        region_name=REGION,
    )
    assert r.workgroup_name == "wg1"


def test_update_workgroup_error(monkeypatch):
    client = MagicMock()
    client.update_workgroup.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_workgroup failed"):
        update_workgroup("wg1", region_name=REGION)


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_convert_recovery_point_to_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.convert_recovery_point_to_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", region_name=REGION)
    mock_client.convert_recovery_point_to_snapshot.assert_called_once()


def test_convert_recovery_point_to_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.convert_recovery_point_to_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "convert_recovery_point_to_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to convert recovery point to snapshot"):
        convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", region_name=REGION)


def test_create_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", region_name=REGION)
    mock_client.create_custom_domain_association.assert_called_once()


def test_create_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom domain association"):
        create_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", region_name=REGION)


def test_create_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_endpoint_access("test-endpoint_name", [], "test-workgroup_name", region_name=REGION)
    mock_client.create_endpoint_access.assert_called_once()


def test_create_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create endpoint access"):
        create_endpoint_access("test-endpoint_name", [], "test-workgroup_name", region_name=REGION)


def test_create_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reservation.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_reservation(1, "test-offering_id", region_name=REGION)
    mock_client.create_reservation.assert_called_once()


def test_create_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_reservation",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create reservation"):
        create_reservation(1, "test-offering_id", region_name=REGION)


def test_create_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_scheduled_action("test-namespace_name", "test-role_arn", {}, "test-scheduled_action_name", {}, region_name=REGION)
    mock_client.create_scheduled_action.assert_called_once()


def test_create_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create scheduled action"):
        create_scheduled_action("test-namespace_name", "test-role_arn", {}, "test-scheduled_action_name", {}, region_name=REGION)


def test_create_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-namespace_name", "test-snapshot_name", region_name=REGION)
    mock_client.create_snapshot.assert_called_once()


def test_create_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        create_snapshot("test-namespace_name", "test-snapshot_name", region_name=REGION)


def test_create_snapshot_copy_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", region_name=REGION)
    mock_client.create_snapshot_copy_configuration.assert_called_once()


def test_create_snapshot_copy_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot_copy_configuration",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot copy configuration"):
        create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", region_name=REGION)


def test_create_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_usage_limit(1, "test-resource_arn", "test-usage_type", region_name=REGION)
    mock_client.create_usage_limit.assert_called_once()


def test_create_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create usage limit"):
        create_usage_limit(1, "test-resource_arn", "test-usage_type", region_name=REGION)


def test_delete_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_custom_domain_association("test-custom_domain_name", "test-workgroup_name", region_name=REGION)
    mock_client.delete_custom_domain_association.assert_called_once()


def test_delete_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom domain association"):
        delete_custom_domain_association("test-custom_domain_name", "test-workgroup_name", region_name=REGION)


def test_delete_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_endpoint_access("test-endpoint_name", region_name=REGION)
    mock_client.delete_endpoint_access.assert_called_once()


def test_delete_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete endpoint access"):
        delete_endpoint_access("test-endpoint_name", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_scheduled_action("test-scheduled_action_name", region_name=REGION)
    mock_client.delete_scheduled_action.assert_called_once()


def test_delete_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete scheduled action"):
        delete_scheduled_action("test-scheduled_action_name", region_name=REGION)


def test_delete_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_snapshot("test-snapshot_name", region_name=REGION)
    mock_client.delete_snapshot.assert_called_once()


def test_delete_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        delete_snapshot("test-snapshot_name", region_name=REGION)


def test_delete_snapshot_copy_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_copy_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_snapshot_copy_configuration("test-snapshot_copy_configuration_id", region_name=REGION)
    mock_client.delete_snapshot_copy_configuration.assert_called_once()


def test_delete_snapshot_copy_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_copy_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot_copy_configuration",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot copy configuration"):
        delete_snapshot_copy_configuration("test-snapshot_copy_configuration_id", region_name=REGION)


def test_delete_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_usage_limit("test-usage_limit_id", region_name=REGION)
    mock_client.delete_usage_limit.assert_called_once()


def test_delete_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete usage limit"):
        delete_usage_limit("test-usage_limit_id", region_name=REGION)


def test_get_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_credentials.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_credentials(region_name=REGION)
    mock_client.get_credentials.assert_called_once()


def test_get_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_credentials",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get credentials"):
        get_credentials(region_name=REGION)


def test_get_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_custom_domain_association("test-custom_domain_name", "test-workgroup_name", region_name=REGION)
    mock_client.get_custom_domain_association.assert_called_once()


def test_get_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get custom domain association"):
        get_custom_domain_association("test-custom_domain_name", "test-workgroup_name", region_name=REGION)


def test_get_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_endpoint_access("test-endpoint_name", region_name=REGION)
    mock_client.get_endpoint_access.assert_called_once()


def test_get_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get endpoint access"):
        get_endpoint_access("test-endpoint_name", region_name=REGION)


def test_get_recovery_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_recovery_point("test-recovery_point_id", region_name=REGION)
    mock_client.get_recovery_point.assert_called_once()


def test_get_recovery_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_recovery_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_recovery_point",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get recovery point"):
        get_recovery_point("test-recovery_point_id", region_name=REGION)


def test_get_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reservation.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_reservation("test-reservation_id", region_name=REGION)
    mock_client.get_reservation.assert_called_once()


def test_get_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reservation",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reservation"):
        get_reservation("test-reservation_id", region_name=REGION)


def test_get_reservation_offering(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reservation_offering.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_reservation_offering("test-offering_id", region_name=REGION)
    mock_client.get_reservation_offering.assert_called_once()


def test_get_reservation_offering_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reservation_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reservation_offering",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reservation offering"):
        get_reservation_offering("test-offering_id", region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_get_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_scheduled_action("test-scheduled_action_name", region_name=REGION)
    mock_client.get_scheduled_action.assert_called_once()


def test_get_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get scheduled action"):
        get_scheduled_action("test-scheduled_action_name", region_name=REGION)


def test_get_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_snapshot(region_name=REGION)
    mock_client.get_snapshot.assert_called_once()


def test_get_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get snapshot"):
        get_snapshot(region_name=REGION)


def test_get_table_restore_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_restore_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_table_restore_status("test-table_restore_request_id", region_name=REGION)
    mock_client.get_table_restore_status.assert_called_once()


def test_get_table_restore_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_restore_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_restore_status",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table restore status"):
        get_table_restore_status("test-table_restore_request_id", region_name=REGION)


def test_get_track(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_track.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_track("test-track_name", region_name=REGION)
    mock_client.get_track.assert_called_once()


def test_get_track_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_track.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_track",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get track"):
        get_track("test-track_name", region_name=REGION)


def test_get_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_usage_limit("test-usage_limit_id", region_name=REGION)
    mock_client.get_usage_limit.assert_called_once()


def test_get_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get usage limit"):
        get_usage_limit("test-usage_limit_id", region_name=REGION)


def test_list_custom_domain_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_custom_domain_associations(region_name=REGION)
    mock_client.list_custom_domain_associations.assert_called_once()


def test_list_custom_domain_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_domain_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_domain_associations",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list custom domain associations"):
        list_custom_domain_associations(region_name=REGION)


def test_list_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_endpoint_access(region_name=REGION)
    mock_client.list_endpoint_access.assert_called_once()


def test_list_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list endpoint access"):
        list_endpoint_access(region_name=REGION)


def test_list_managed_workgroups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_managed_workgroups.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_managed_workgroups(region_name=REGION)
    mock_client.list_managed_workgroups.assert_called_once()


def test_list_managed_workgroups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_managed_workgroups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_managed_workgroups",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list managed workgroups"):
        list_managed_workgroups(region_name=REGION)


def test_list_recovery_points(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recovery_points.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_recovery_points(region_name=REGION)
    mock_client.list_recovery_points.assert_called_once()


def test_list_recovery_points_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recovery_points.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recovery_points",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list recovery points"):
        list_recovery_points(region_name=REGION)


def test_list_reservation_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reservation_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_reservation_offerings(region_name=REGION)
    mock_client.list_reservation_offerings.assert_called_once()


def test_list_reservation_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reservation_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reservation_offerings",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list reservation offerings"):
        list_reservation_offerings(region_name=REGION)


def test_list_reservations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reservations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_reservations(region_name=REGION)
    mock_client.list_reservations.assert_called_once()


def test_list_reservations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reservations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reservations",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list reservations"):
        list_reservations(region_name=REGION)


def test_list_scheduled_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_scheduled_actions(region_name=REGION)
    mock_client.list_scheduled_actions.assert_called_once()


def test_list_scheduled_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scheduled_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_scheduled_actions",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list scheduled actions"):
        list_scheduled_actions(region_name=REGION)


def test_list_snapshot_copy_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshot_copy_configurations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_snapshot_copy_configurations(region_name=REGION)
    mock_client.list_snapshot_copy_configurations.assert_called_once()


def test_list_snapshot_copy_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshot_copy_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_snapshot_copy_configurations",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list snapshot copy configurations"):
        list_snapshot_copy_configurations(region_name=REGION)


def test_list_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_snapshots(region_name=REGION)
    mock_client.list_snapshots.assert_called_once()


def test_list_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_snapshots",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list snapshots"):
        list_snapshots(region_name=REGION)


def test_list_table_restore_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_restore_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_table_restore_status(region_name=REGION)
    mock_client.list_table_restore_status.assert_called_once()


def test_list_table_restore_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_restore_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_table_restore_status",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list table restore status"):
        list_table_restore_status(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_tracks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tracks.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_tracks(region_name=REGION)
    mock_client.list_tracks.assert_called_once()


def test_list_tracks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tracks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tracks",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tracks"):
        list_tracks(region_name=REGION)


def test_list_usage_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_usage_limits.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_usage_limits(region_name=REGION)
    mock_client.list_usage_limits.assert_called_once()


def test_list_usage_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_usage_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_usage_limits",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list usage limits"):
        list_usage_limits(region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-policy", "test-resource_arn", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-policy", "test-resource_arn", region_name=REGION)


def test_restore_from_recovery_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_from_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_from_recovery_point("test-namespace_name", "test-recovery_point_id", "test-workgroup_name", region_name=REGION)
    mock_client.restore_from_recovery_point.assert_called_once()


def test_restore_from_recovery_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_from_recovery_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_from_recovery_point",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore from recovery point"):
        restore_from_recovery_point("test-namespace_name", "test-recovery_point_id", "test-workgroup_name", region_name=REGION)


def test_restore_from_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_from_snapshot("test-namespace_name", "test-workgroup_name", region_name=REGION)
    mock_client.restore_from_snapshot.assert_called_once()


def test_restore_from_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_from_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore from snapshot"):
        restore_from_snapshot("test-namespace_name", "test-workgroup_name", region_name=REGION)


def test_restore_table_from_recovery_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", region_name=REGION)
    mock_client.restore_table_from_recovery_point.assert_called_once()


def test_restore_table_from_recovery_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_recovery_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_table_from_recovery_point",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore table from recovery point"):
        restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", region_name=REGION)


def test_restore_table_from_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", region_name=REGION)
    mock_client.restore_table_from_snapshot.assert_called_once()


def test_restore_table_from_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_table_from_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore table from snapshot"):
        restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", region_name=REGION)
    mock_client.update_custom_domain_association.assert_called_once()


def test_update_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update custom domain association"):
        update_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", region_name=REGION)


def test_update_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_endpoint_access("test-endpoint_name", region_name=REGION)
    mock_client.update_endpoint_access.assert_called_once()


def test_update_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update endpoint access"):
        update_endpoint_access("test-endpoint_name", region_name=REGION)


def test_update_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_scheduled_action("test-scheduled_action_name", region_name=REGION)
    mock_client.update_scheduled_action.assert_called_once()


def test_update_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update scheduled action"):
        update_scheduled_action("test-scheduled_action_name", region_name=REGION)


def test_update_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_snapshot("test-snapshot_name", region_name=REGION)
    mock_client.update_snapshot.assert_called_once()


def test_update_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update snapshot"):
        update_snapshot("test-snapshot_name", region_name=REGION)


def test_update_snapshot_copy_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot_copy_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_snapshot_copy_configuration("test-snapshot_copy_configuration_id", region_name=REGION)
    mock_client.update_snapshot_copy_configuration.assert_called_once()


def test_update_snapshot_copy_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot_copy_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_snapshot_copy_configuration",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update snapshot copy configuration"):
        update_snapshot_copy_configuration("test-snapshot_copy_configuration_id", region_name=REGION)


def test_update_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_usage_limit("test-usage_limit_id", region_name=REGION)
    mock_client.update_usage_limit.assert_called_once()


def test_update_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update usage limit"):
        update_usage_limit("test-usage_limit_id", region_name=REGION)


def test_create_namespace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_namespace
    mock_client = MagicMock()
    mock_client.create_namespace.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_namespace("test-namespace_name", admin_username="test-admin_username", admin_user_password="test-admin_user_password", db_name="test-db_name", iam_roles="test-iam_roles", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_namespace.assert_called_once()

def test_delete_namespace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import delete_namespace
    mock_client = MagicMock()
    mock_client.delete_namespace.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    delete_namespace("test-namespace_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.delete_namespace.assert_called_once()

def test_update_namespace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_namespace
    mock_client = MagicMock()
    mock_client.update_namespace.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_namespace("test-namespace_name", admin_username="test-admin_username", admin_user_password="test-admin_user_password", iam_roles="test-iam_roles", region_name="us-east-1")
    mock_client.update_namespace.assert_called_once()

def test_update_workgroup_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_workgroup
    mock_client = MagicMock()
    mock_client.update_workgroup.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_workgroup("test-workgroup_name", base_capacity="test-base_capacity", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", region_name="us-east-1")
    mock_client.update_workgroup.assert_called_once()

def test_convert_recovery_point_to_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import convert_recovery_point_to_snapshot
    mock_client = MagicMock()
    mock_client.convert_recovery_point_to_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", retention_period="test-retention_period", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.convert_recovery_point_to_snapshot.assert_called_once()

def test_create_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_endpoint_access
    mock_client = MagicMock()
    mock_client.create_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_endpoint_access("test-endpoint_name", "test-subnet_ids", "test-workgroup_name", owner_account=1, vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.create_endpoint_access.assert_called_once()

def test_create_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_reservation
    mock_client = MagicMock()
    mock_client.create_reservation.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_reservation("test-capacity", "test-offering_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_reservation.assert_called_once()

def test_create_scheduled_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_scheduled_action
    mock_client = MagicMock()
    mock_client.create_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_scheduled_action("test-namespace_name", "test-role_arn", "test-schedule", "test-scheduled_action_name", "test-target_action", enabled=True, end_time="test-end_time", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", region_name="us-east-1")
    mock_client.create_scheduled_action.assert_called_once()

def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_snapshot
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-namespace_name", "test-snapshot_name", retention_period="test-retention_period", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_snapshot.assert_called_once()

def test_create_snapshot_copy_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_snapshot_copy_configuration
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", destination_kms_key_id="test-destination_kms_key_id", snapshot_retention_period="test-snapshot_retention_period", region_name="us-east-1")
    mock_client.create_snapshot_copy_configuration.assert_called_once()

def test_create_usage_limit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import create_usage_limit
    mock_client = MagicMock()
    mock_client.create_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    create_usage_limit("test-amount", "test-resource_arn", "test-usage_type", breach_action="test-breach_action", period="test-period", region_name="us-east-1")
    mock_client.create_usage_limit.assert_called_once()

def test_get_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import get_credentials
    mock_client = MagicMock()
    mock_client.get_credentials.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_credentials(custom_domain_name="test-custom_domain_name", db_name="test-db_name", duration_seconds=1, workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.get_credentials.assert_called_once()

def test_get_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import get_snapshot
    mock_client = MagicMock()
    mock_client.get_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    get_snapshot(owner_account=1, snapshot_arn="test-snapshot_arn", snapshot_name="test-snapshot_name", region_name="us-east-1")
    mock_client.get_snapshot.assert_called_once()

def test_list_custom_domain_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_custom_domain_associations
    mock_client = MagicMock()
    mock_client.list_custom_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_custom_domain_associations(custom_domain_certificate_arn="test-custom_domain_certificate_arn", custom_domain_name="test-custom_domain_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_custom_domain_associations.assert_called_once()

def test_list_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_endpoint_access
    mock_client = MagicMock()
    mock_client.list_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_endpoint_access(max_results=1, next_token="test-next_token", owner_account=1, vpc_id="test-vpc_id", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.list_endpoint_access.assert_called_once()

def test_list_managed_workgroups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_managed_workgroups
    mock_client = MagicMock()
    mock_client.list_managed_workgroups.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_managed_workgroups(max_results=1, next_token="test-next_token", source_arn="test-source_arn", region_name="us-east-1")
    mock_client.list_managed_workgroups.assert_called_once()

def test_list_recovery_points_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_recovery_points
    mock_client = MagicMock()
    mock_client.list_recovery_points.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_recovery_points(end_time="test-end_time", max_results=1, namespace_arn="test-namespace_arn", namespace_name="test-namespace_name", next_token="test-next_token", start_time="test-start_time", region_name="us-east-1")
    mock_client.list_recovery_points.assert_called_once()

def test_list_reservation_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_reservation_offerings
    mock_client = MagicMock()
    mock_client.list_reservation_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_reservation_offerings(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_reservation_offerings.assert_called_once()

def test_list_reservations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_reservations
    mock_client = MagicMock()
    mock_client.list_reservations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_reservations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_reservations.assert_called_once()

def test_list_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_scheduled_actions
    mock_client = MagicMock()
    mock_client.list_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_scheduled_actions(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_scheduled_actions.assert_called_once()

def test_list_snapshot_copy_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_snapshot_copy_configurations
    mock_client = MagicMock()
    mock_client.list_snapshot_copy_configurations.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_snapshot_copy_configurations(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_snapshot_copy_configurations.assert_called_once()

def test_list_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_snapshots
    mock_client = MagicMock()
    mock_client.list_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_snapshots(end_time="test-end_time", max_results=1, namespace_arn="test-namespace_arn", namespace_name="test-namespace_name", next_token="test-next_token", owner_account=1, start_time="test-start_time", region_name="us-east-1")
    mock_client.list_snapshots.assert_called_once()

def test_list_table_restore_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_table_restore_status
    mock_client = MagicMock()
    mock_client.list_table_restore_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_table_restore_status(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.list_table_restore_status.assert_called_once()

def test_list_tracks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_tracks
    mock_client = MagicMock()
    mock_client.list_tracks.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_tracks(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tracks.assert_called_once()

def test_list_usage_limits_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import list_usage_limits
    mock_client = MagicMock()
    mock_client.list_usage_limits.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    list_usage_limits(max_results=1, next_token="test-next_token", resource_arn="test-resource_arn", usage_type="test-usage_type", region_name="us-east-1")
    mock_client.list_usage_limits.assert_called_once()

def test_restore_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import restore_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_from_snapshot("test-namespace_name", "test-workgroup_name", admin_password_secret_kms_key_id="test-admin_password_secret_kms_key_id", manage_admin_password="test-manage_admin_password", owner_account=1, snapshot_arn="test-snapshot_arn", snapshot_name="test-snapshot_name", region_name="us-east-1")
    mock_client.restore_from_snapshot.assert_called_once()

def test_restore_table_from_recovery_point_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import restore_table_from_recovery_point
    mock_client = MagicMock()
    mock_client.restore_table_from_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", activate_case_sensitive_identifier=True, source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", region_name="us-east-1")
    mock_client.restore_table_from_recovery_point.assert_called_once()

def test_restore_table_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import restore_table_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_table_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", activate_case_sensitive_identifier=True, source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", region_name="us-east-1")
    mock_client.restore_table_from_snapshot.assert_called_once()

def test_update_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_endpoint_access
    mock_client = MagicMock()
    mock_client.update_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_endpoint_access("test-endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.update_endpoint_access.assert_called_once()

def test_update_scheduled_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_scheduled_action
    mock_client = MagicMock()
    mock_client.update_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_scheduled_action("test-scheduled_action_name", enabled=True, end_time="test-end_time", role_arn="test-role_arn", schedule="test-schedule", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", target_action="test-target_action", region_name="us-east-1")
    mock_client.update_scheduled_action.assert_called_once()

def test_update_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_snapshot
    mock_client = MagicMock()
    mock_client.update_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_snapshot("test-snapshot_name", retention_period="test-retention_period", region_name="us-east-1")
    mock_client.update_snapshot.assert_called_once()

def test_update_snapshot_copy_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_snapshot_copy_configuration
    mock_client = MagicMock()
    mock_client.update_snapshot_copy_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_snapshot_copy_configuration({}, snapshot_retention_period="test-snapshot_retention_period", region_name="us-east-1")
    mock_client.update_snapshot_copy_configuration.assert_called_once()

def test_update_usage_limit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_serverless import update_usage_limit
    mock_client = MagicMock()
    mock_client.update_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift_serverless.get_client", lambda *a, **kw: mock_client)
    update_usage_limit(1, amount="test-amount", breach_action="test-breach_action", region_name="us-east-1")
    mock_client.update_usage_limit.assert_called_once()
