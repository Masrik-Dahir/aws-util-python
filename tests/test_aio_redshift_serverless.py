

"""Tests for aws_util.aio.redshift_serverless -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.redshift_serverless as mod
from aws_util.redshift_serverless import NamespaceResult, WorkgroupResult
from aws_util.aio.redshift_serverless import (

    create_namespace,
    delete_namespace,
    update_namespace,
    create_workgroup,
    update_workgroup,
    convert_recovery_point_to_snapshot,
    create_endpoint_access,
    create_reservation,
    create_scheduled_action,
    create_snapshot,
    create_snapshot_copy_configuration,
    create_usage_limit,
    get_credentials,
    get_snapshot,
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
    list_tracks,
    list_usage_limits,
    restore_from_snapshot,
    restore_table_from_recovery_point,
    restore_table_from_snapshot,
    update_endpoint_access,
    update_scheduled_action,
    update_snapshot,
    update_snapshot_copy_configuration,
    update_usage_limit,
    create_custom_domain_association,
    delete_custom_domain_association,
    delete_endpoint_access,
    delete_resource_policy,
    delete_scheduled_action,
    delete_snapshot,
    delete_snapshot_copy_configuration,
    delete_usage_limit,
    get_custom_domain_association,
    get_endpoint_access,
    get_recovery_point,
    get_reservation,
    get_reservation_offering,
    get_resource_policy,
    get_scheduled_action,
    get_table_restore_status,
    get_track,
    get_usage_limit,
    list_tags_for_resource,
    put_resource_policy,
    restore_from_recovery_point,
    tag_resource,
    untag_resource,
    update_custom_domain_association,
)


REGION = "us-east-1"
_NS = {"namespaceName": "ns1", "namespaceId": "id1", "namespaceArn": "arn:ns1",
       "status": "AVAILABLE", "adminUsername": "admin", "dbName": "db",
       "creationDate": "2025-01-01", "iamRoles": ["r1"]}
_WG = {"workgroupName": "wg1", "workgroupId": "wgid1", "workgroupArn": "arn:wg1",
       "status": "AVAILABLE", "namespaceName": "ns1", "baseCapacity": 128,
       "creationDate": "2025-01-01", "endpoint": {"address": "ep"}}


@pytest.fixture()
def mc(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: client)
    return client


async def test_create_namespace_success(mc):
    mc.call.return_value = {"namespace": _NS}
    r = await mod.create_namespace("ns1")
    assert r.namespace_name == "ns1"


async def test_create_namespace_all_opts(mc):
    mc.call.return_value = {"namespace": _NS}
    await mod.create_namespace("ns1", admin_username="a", admin_user_password="p",
                               db_name="d", iam_roles=["r"], tags=[{"Key": "k", "Value": "v"}])
    mc.call.assert_called_once()


async def test_create_namespace_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_namespace("ns1")


async def test_create_namespace_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_namespace failed"):
        await mod.create_namespace("ns1")


async def test_get_namespace_success(mc):
    mc.call.return_value = {"namespace": _NS}
    r = await mod.get_namespace("ns1")
    assert r.namespace_name == "ns1"


async def test_get_namespace_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_namespace("ns1")


async def test_get_namespace_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_namespace failed"):
        await mod.get_namespace("ns1")


async def test_list_namespaces_success(mc):
    mc.call.return_value = {"namespaces": [_NS]}
    r = await mod.list_namespaces()
    assert len(r) == 1


async def test_list_namespaces_pagination(mc):
    mc.call.side_effect = [
        {"namespaces": [_NS], "nextToken": "t1"},
        {"namespaces": [_NS]},
    ]
    r = await mod.list_namespaces()
    assert len(r) == 2


async def test_list_namespaces_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_namespaces()


async def test_list_namespaces_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_namespaces failed"):
        await mod.list_namespaces()


async def test_delete_namespace_success(mc):
    mc.call.return_value = {"namespace": _NS}
    r = await mod.delete_namespace("ns1")
    assert r.namespace_name == "ns1"


async def test_delete_namespace_with_snapshot(mc):
    mc.call.return_value = {"namespace": _NS}
    await mod.delete_namespace("ns1", final_snapshot_name="snap")
    kw = mc.call.call_args[1]
    assert kw["finalSnapshotName"] == "snap"


async def test_delete_namespace_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_namespace("ns1")


async def test_delete_namespace_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_namespace failed"):
        await mod.delete_namespace("ns1")


async def test_update_namespace_success(mc):
    mc.call.return_value = {"namespace": _NS}
    r = await mod.update_namespace("ns1", admin_username="a", admin_user_password="p", iam_roles=["r"])
    assert r.namespace_name == "ns1"


async def test_update_namespace_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_namespace("ns1")


async def test_update_namespace_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_namespace failed"):
        await mod.update_namespace("ns1")


async def test_create_workgroup_success(mc):
    mc.call.return_value = {"workgroup": _WG}
    r = await mod.create_workgroup("wg1", namespace_name="ns1")
    assert r.workgroup_name == "wg1"


async def test_create_workgroup_all_opts(mc):
    mc.call.return_value = {"workgroup": _WG}
    await mod.create_workgroup("wg1", namespace_name="ns1", base_capacity=64,
                               subnet_ids=["s1"], security_group_ids=["sg1"],
                               tags=[{"Key": "k", "Value": "v"}])
    mc.call.assert_called_once()


async def test_create_workgroup_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_workgroup("wg1", namespace_name="ns1")


async def test_create_workgroup_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_workgroup failed"):
        await mod.create_workgroup("wg1", namespace_name="ns1")


async def test_get_workgroup_success(mc):
    mc.call.return_value = {"workgroup": _WG}
    r = await mod.get_workgroup("wg1")
    assert r.workgroup_name == "wg1"


async def test_get_workgroup_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_workgroup("wg1")


async def test_get_workgroup_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_workgroup failed"):
        await mod.get_workgroup("wg1")


async def test_list_workgroups_success(mc):
    mc.call.return_value = {"workgroups": [_WG]}
    r = await mod.list_workgroups()
    assert len(r) == 1


async def test_list_workgroups_pagination(mc):
    mc.call.side_effect = [
        {"workgroups": [_WG], "nextToken": "t1"},
        {"workgroups": [_WG]},
    ]
    r = await mod.list_workgroups()
    assert len(r) == 2


async def test_list_workgroups_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_workgroups()


async def test_list_workgroups_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_workgroups failed"):
        await mod.list_workgroups()


async def test_delete_workgroup_success(mc):
    mc.call.return_value = {"workgroup": _WG}
    r = await mod.delete_workgroup("wg1")
    assert r.workgroup_name == "wg1"


async def test_delete_workgroup_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_workgroup("wg1")


async def test_delete_workgroup_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_workgroup failed"):
        await mod.delete_workgroup("wg1")


async def test_update_workgroup_success(mc):
    mc.call.return_value = {"workgroup": _WG}
    r = await mod.update_workgroup("wg1", base_capacity=256, subnet_ids=["s"], security_group_ids=["sg"])
    assert r.workgroup_name == "wg1"


async def test_update_workgroup_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_workgroup("wg1")


async def test_update_workgroup_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_workgroup failed"):
        await mod.update_workgroup("wg1")


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_convert_recovery_point_to_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_convert_recovery_point_to_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", )


async def test_create_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_create_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", )


async def test_create_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_endpoint_access("test-endpoint_name", [], "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_create_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_endpoint_access("test-endpoint_name", [], "test-workgroup_name", )


async def test_create_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_reservation(1, "test-offering_id", )
    mock_client.call.assert_called_once()


async def test_create_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_reservation(1, "test-offering_id", )


async def test_create_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_scheduled_action("test-namespace_name", "test-role_arn", {}, "test-scheduled_action_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_scheduled_action("test-namespace_name", "test-role_arn", {}, "test-scheduled_action_name", {}, )


async def test_create_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot("test-namespace_name", "test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot("test-namespace_name", "test-snapshot_name", )


async def test_create_snapshot_copy_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_copy_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", )


async def test_create_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_usage_limit(1, "test-resource_arn", "test-usage_type", )
    mock_client.call.assert_called_once()


async def test_create_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_usage_limit(1, "test-resource_arn", "test-usage_type", )


async def test_delete_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_domain_association("test-custom_domain_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_domain_association("test-custom_domain_name", "test-workgroup_name", )


async def test_delete_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_endpoint_access("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_delete_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_endpoint_access("test-endpoint_name", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_scheduled_action("test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_delete_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_scheduled_action("test-scheduled_action_name", )


async def test_delete_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot("test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot("test-snapshot_name", )


async def test_delete_snapshot_copy_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot_copy_configuration("test-snapshot_copy_configuration_id", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_copy_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot_copy_configuration("test-snapshot_copy_configuration_id", )


async def test_delete_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_usage_limit("test-usage_limit_id", )
    mock_client.call.assert_called_once()


async def test_delete_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_usage_limit("test-usage_limit_id", )


async def test_get_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_credentials()
    mock_client.call.assert_called_once()


async def test_get_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_credentials()


async def test_get_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_custom_domain_association("test-custom_domain_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_get_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_domain_association("test-custom_domain_name", "test-workgroup_name", )


async def test_get_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_endpoint_access("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_get_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_endpoint_access("test-endpoint_name", )


async def test_get_recovery_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_recovery_point("test-recovery_point_id", )
    mock_client.call.assert_called_once()


async def test_get_recovery_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_recovery_point("test-recovery_point_id", )


async def test_get_reservation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reservation("test-reservation_id", )
    mock_client.call.assert_called_once()


async def test_get_reservation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reservation("test-reservation_id", )


async def test_get_reservation_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reservation_offering("test-offering_id", )
    mock_client.call.assert_called_once()


async def test_get_reservation_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reservation_offering("test-offering_id", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_get_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_scheduled_action("test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_get_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_scheduled_action("test-scheduled_action_name", )


async def test_get_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_snapshot()
    mock_client.call.assert_called_once()


async def test_get_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_snapshot()


async def test_get_table_restore_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table_restore_status("test-table_restore_request_id", )
    mock_client.call.assert_called_once()


async def test_get_table_restore_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_restore_status("test-table_restore_request_id", )


async def test_get_track(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_track("test-track_name", )
    mock_client.call.assert_called_once()


async def test_get_track_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_track("test-track_name", )


async def test_get_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_usage_limit("test-usage_limit_id", )
    mock_client.call.assert_called_once()


async def test_get_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_usage_limit("test-usage_limit_id", )


async def test_list_custom_domain_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_domain_associations()
    mock_client.call.assert_called_once()


async def test_list_custom_domain_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_domain_associations()


async def test_list_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_endpoint_access()
    mock_client.call.assert_called_once()


async def test_list_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_endpoint_access()


async def test_list_managed_workgroups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_managed_workgroups()
    mock_client.call.assert_called_once()


async def test_list_managed_workgroups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_managed_workgroups()


async def test_list_recovery_points(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recovery_points()
    mock_client.call.assert_called_once()


async def test_list_recovery_points_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recovery_points()


async def test_list_reservation_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_reservation_offerings()
    mock_client.call.assert_called_once()


async def test_list_reservation_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_reservation_offerings()


async def test_list_reservations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_reservations()
    mock_client.call.assert_called_once()


async def test_list_reservations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_reservations()


async def test_list_scheduled_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_scheduled_actions()
    mock_client.call.assert_called_once()


async def test_list_scheduled_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_scheduled_actions()


async def test_list_snapshot_copy_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_snapshot_copy_configurations()
    mock_client.call.assert_called_once()


async def test_list_snapshot_copy_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_snapshot_copy_configurations()


async def test_list_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_snapshots()
    mock_client.call.assert_called_once()


async def test_list_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_snapshots()


async def test_list_table_restore_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_table_restore_status()
    mock_client.call.assert_called_once()


async def test_list_table_restore_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_table_restore_status()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tracks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tracks()
    mock_client.call.assert_called_once()


async def test_list_tracks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tracks()


async def test_list_usage_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_usage_limits()
    mock_client.call.assert_called_once()


async def test_list_usage_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_usage_limits()


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-policy", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-policy", "test-resource_arn", )


async def test_restore_from_recovery_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_from_recovery_point("test-namespace_name", "test-recovery_point_id", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_restore_from_recovery_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_from_recovery_point("test-namespace_name", "test-recovery_point_id", "test-workgroup_name", )


async def test_restore_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_from_snapshot("test-namespace_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_restore_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_from_snapshot("test-namespace_name", "test-workgroup_name", )


async def test_restore_table_from_recovery_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_restore_table_from_recovery_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", )


async def test_restore_table_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_restore_table_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_custom_domain_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", )
    mock_client.call.assert_called_once()


async def test_update_custom_domain_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_domain_association("test-custom_domain_certificate_arn", "test-custom_domain_name", "test-workgroup_name", )


async def test_update_endpoint_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_endpoint_access("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_update_endpoint_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_endpoint_access("test-endpoint_name", )


async def test_update_scheduled_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_scheduled_action("test-scheduled_action_name", )
    mock_client.call.assert_called_once()


async def test_update_scheduled_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_scheduled_action("test-scheduled_action_name", )


async def test_update_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_snapshot("test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_update_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_snapshot("test-snapshot_name", )


async def test_update_snapshot_copy_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_snapshot_copy_configuration("test-snapshot_copy_configuration_id", )
    mock_client.call.assert_called_once()


async def test_update_snapshot_copy_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_snapshot_copy_configuration("test-snapshot_copy_configuration_id", )


async def test_update_usage_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_usage_limit("test-usage_limit_id", )
    mock_client.call.assert_called_once()


async def test_update_usage_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_usage_limit("test-usage_limit_id", )


@pytest.mark.asyncio
async def test_create_namespace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_namespace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_namespace("test-namespace_name", admin_username="test-admin_username", admin_user_password="test-admin_user_password", db_name="test-db_name", iam_roles="test-iam_roles", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_namespace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import delete_namespace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await delete_namespace("test-namespace_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_namespace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_namespace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_namespace("test-namespace_name", admin_username="test-admin_username", admin_user_password="test-admin_user_password", iam_roles="test-iam_roles", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_workgroup_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_workgroup
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_workgroup("test-workgroup_name", base_capacity="test-base_capacity", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_convert_recovery_point_to_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import convert_recovery_point_to_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await convert_recovery_point_to_snapshot("test-recovery_point_id", "test-snapshot_name", retention_period="test-retention_period", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_endpoint_access("test-endpoint_name", "test-subnet_ids", "test-workgroup_name", owner_account=1, vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_reservation("test-capacity", "test-offering_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_scheduled_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_scheduled_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_scheduled_action("test-namespace_name", "test-role_arn", "test-schedule", "test-scheduled_action_name", "test-target_action", enabled=True, end_time="test-end_time", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_snapshot("test-namespace_name", "test-snapshot_name", retention_period="test-retention_period", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_copy_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_snapshot_copy_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_snapshot_copy_configuration("test-destination_region", "test-namespace_name", destination_kms_key_id="test-destination_kms_key_id", snapshot_retention_period="test-snapshot_retention_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_usage_limit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import create_usage_limit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await create_usage_limit("test-amount", "test-resource_arn", "test-usage_type", breach_action="test-breach_action", period="test-period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import get_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await get_credentials(custom_domain_name="test-custom_domain_name", db_name="test-db_name", duration_seconds=1, workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import get_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await get_snapshot(owner_account=1, snapshot_arn="test-snapshot_arn", snapshot_name="test-snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_domain_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_custom_domain_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_custom_domain_associations(custom_domain_certificate_arn="test-custom_domain_certificate_arn", custom_domain_name="test-custom_domain_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_endpoint_access(max_results=1, next_token="test-next_token", owner_account=1, vpc_id="test-vpc_id", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_managed_workgroups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_managed_workgroups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_managed_workgroups(max_results=1, next_token="test-next_token", source_arn="test-source_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recovery_points_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_recovery_points
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_recovery_points(end_time="test-end_time", max_results=1, namespace_arn="test-namespace_arn", namespace_name="test-namespace_name", next_token="test-next_token", start_time="test-start_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reservation_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_reservation_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_reservation_offerings(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reservations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_reservations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_reservations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_scheduled_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_scheduled_actions(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_snapshot_copy_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_snapshot_copy_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_snapshot_copy_configurations(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_snapshots(end_time="test-end_time", max_results=1, namespace_arn="test-namespace_arn", namespace_name="test-namespace_name", next_token="test-next_token", owner_account=1, start_time="test-start_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_table_restore_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_table_restore_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_table_restore_status(max_results=1, namespace_name="test-namespace_name", next_token="test-next_token", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tracks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_tracks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_tracks(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_usage_limits_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import list_usage_limits
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await list_usage_limits(max_results=1, next_token="test-next_token", resource_arn="test-resource_arn", usage_type="test-usage_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import restore_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await restore_from_snapshot("test-namespace_name", "test-workgroup_name", admin_password_secret_kms_key_id="test-admin_password_secret_kms_key_id", manage_admin_password="test-manage_admin_password", owner_account=1, snapshot_arn="test-snapshot_arn", snapshot_name="test-snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_table_from_recovery_point_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import restore_table_from_recovery_point
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await restore_table_from_recovery_point("test-namespace_name", "test-new_table_name", "test-recovery_point_id", "test-source_database_name", "test-source_table_name", "test-workgroup_name", activate_case_sensitive_identifier=True, source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_table_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import restore_table_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await restore_table_from_snapshot("test-namespace_name", "test-new_table_name", "test-snapshot_name", "test-source_database_name", "test-source_table_name", "test-workgroup_name", activate_case_sensitive_identifier=True, source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_endpoint_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_endpoint_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_endpoint_access("test-endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_scheduled_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_scheduled_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_scheduled_action("test-scheduled_action_name", enabled=True, end_time="test-end_time", role_arn="test-role_arn", schedule="test-schedule", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", target_action="test-target_action", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_snapshot("test-snapshot_name", retention_period="test-retention_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_snapshot_copy_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_snapshot_copy_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_snapshot_copy_configuration({}, snapshot_retention_period="test-snapshot_retention_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_usage_limit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_serverless import update_usage_limit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_serverless.async_client", lambda *a, **kw: mock_client)
    await update_usage_limit(1, amount="test-amount", breach_action="test-breach_action", region_name="us-east-1")
    mock_client.call.assert_called_once()
