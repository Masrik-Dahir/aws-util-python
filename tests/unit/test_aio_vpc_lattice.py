

"""Tests for aws_util.aio.vpc_lattice -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.vpc_lattice as mod
from aws_util.aio.vpc_lattice import (

    create_target_group,
    create_access_log_subscription,
    create_listener,
    create_resource_configuration,
    create_resource_gateway,
    create_rule,
    create_service_network_resource_association,
    create_service_network_service_association,
    create_service_network_vpc_association,
    list_access_log_subscriptions,
    list_domain_verifications,
    list_listeners,
    list_resource_configurations,
    list_resource_endpoint_associations,
    list_resource_gateways,
    list_rules,
    list_service_network_resource_associations,
    list_service_network_service_associations,
    list_service_network_vpc_associations,
    list_service_network_vpc_endpoint_associations,
    start_domain_verification,
    update_resource_configuration,
    update_resource_gateway,
    update_rule,
    batch_update_rule,
    delete_access_log_subscription,
    delete_auth_policy,
    delete_domain_verification,
    delete_listener,
    delete_resource_configuration,
    delete_resource_endpoint_association,
    delete_resource_gateway,
    delete_resource_policy,
    delete_rule,
    delete_service_network_resource_association,
    delete_service_network_service_association,
    delete_service_network_vpc_association,
    delete_target_group,
    get_access_log_subscription,
    get_auth_policy,
    get_domain_verification,
    get_listener,
    get_resource_configuration,
    get_resource_gateway,
    get_resource_policy,
    get_rule,
    get_service_network_resource_association,
    get_service_network_service_association,
    get_service_network_vpc_association,
    list_tags_for_resource,
    put_auth_policy,
    put_resource_policy,
    tag_resource,
    untag_resource,
    update_access_log_subscription,
    update_listener,
    update_service_network_vpc_association,
    update_target_group,
)



REGION = "us-east-1"
_SN = {"id": "sn-1", "arn": "arn:sn", "name": "sn", "authType": "NONE",
       "status": "ACTIVE", "extraSN": "x"}
_SVC = {"id": "svc-1", "arn": "arn:svc", "name": "svc", "status": "ACTIVE",
        "dnsEntry": {"domainName": "example.com"}, "extraSVC": "y"}
_TG = {"id": "tg-1", "arn": "arn:tg", "name": "tg", "type": "INSTANCE",
       "status": "ACTIVE", "extraTG": "z"}
_TGT = {"id": "i-1", "port": 80, "status": "HEALTHY", "extraTGT": "w"}


@pytest.fixture()
def mc(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: client)
    return client


# ---------------------------------------------------------------------------
# Service Network operations
# ---------------------------------------------------------------------------

async def test_create_service_network_success(mc):
    mc.call.return_value = _SN
    r = await mod.create_service_network("sn")
    assert r.id == "sn-1"

async def test_create_service_network_with_tags(mc):
    mc.call.return_value = _SN
    r = await mod.create_service_network("sn", tags={"k": "v"})
    assert r.id == "sn-1"

async def test_create_service_network_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_service_network("sn")

async def test_create_service_network_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_service_network failed"):
        await mod.create_service_network("sn")


async def test_get_service_network_success(mc):
    mc.call.return_value = _SN
    r = await mod.get_service_network("sn-1")
    assert r.id == "sn-1"

async def test_get_service_network_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_service_network("sn-1")

async def test_get_service_network_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_service_network failed"):
        await mod.get_service_network("sn-1")


async def test_list_service_networks_success(mc):
    mc.call.return_value = {"items": [_SN]}
    r = await mod.list_service_networks()
    assert len(r) == 1

async def test_list_service_networks_pagination(mc):
    mc.call.side_effect = [
        {"items": [_SN], "nextToken": "t1"},
        {"items": [_SN]},
    ]
    r = await mod.list_service_networks()
    assert len(r) == 2

async def test_list_service_networks_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_service_networks()

async def test_list_service_networks_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_service_networks failed"):
        await mod.list_service_networks()


async def test_update_service_network_success(mc):
    mc.call.return_value = _SN
    r = await mod.update_service_network("sn-1", auth_type="AWS_IAM")
    assert r.id == "sn-1"

async def test_update_service_network_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_service_network("sn-1", auth_type="AWS_IAM")

async def test_update_service_network_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_service_network failed"):
        await mod.update_service_network("sn-1", auth_type="AWS_IAM")


async def test_delete_service_network_success(mc):
    mc.call.return_value = {}
    await mod.delete_service_network("sn-1")
    mc.call.assert_called_once()

async def test_delete_service_network_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_service_network("sn-1")

async def test_delete_service_network_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_service_network failed"):
        await mod.delete_service_network("sn-1")


# ---------------------------------------------------------------------------
# Service operations
# ---------------------------------------------------------------------------

async def test_create_service_success(mc):
    mc.call.return_value = _SVC
    r = await mod.create_service("svc")
    assert r.id == "svc-1"

async def test_create_service_with_tags(mc):
    mc.call.return_value = _SVC
    r = await mod.create_service("svc", tags={"k": "v"})
    assert r.id == "svc-1"

async def test_create_service_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_service("svc")

async def test_create_service_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_service failed"):
        await mod.create_service("svc")


async def test_get_service_success(mc):
    mc.call.return_value = _SVC
    r = await mod.get_service("svc-1")
    assert r.id == "svc-1"

async def test_get_service_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_service("svc-1")

async def test_get_service_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_service failed"):
        await mod.get_service("svc-1")


async def test_list_services_success(mc):
    mc.call.return_value = {"items": [_SVC]}
    r = await mod.list_services()
    assert len(r) == 1

async def test_list_services_pagination(mc):
    mc.call.side_effect = [
        {"items": [_SVC], "nextToken": "t1"},
        {"items": [_SVC]},
    ]
    r = await mod.list_services()
    assert len(r) == 2

async def test_list_services_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_services()

async def test_list_services_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_services failed"):
        await mod.list_services()


async def test_update_service_success(mc):
    mc.call.return_value = _SVC
    r = await mod.update_service("svc-1", auth_type="AWS_IAM")
    assert r.id == "svc-1"

async def test_update_service_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_service("svc-1", auth_type="AWS_IAM")

async def test_update_service_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_service failed"):
        await mod.update_service("svc-1", auth_type="AWS_IAM")


async def test_delete_service_success(mc):
    mc.call.return_value = {}
    await mod.delete_service("svc-1")
    mc.call.assert_called_once()

async def test_delete_service_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_service("svc-1")

async def test_delete_service_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_service failed"):
        await mod.delete_service("svc-1")


# ---------------------------------------------------------------------------
# Target Group operations
# ---------------------------------------------------------------------------

async def test_create_target_group_success(mc):
    mc.call.return_value = _TG
    r = await mod.create_target_group("tg")
    assert r.id == "tg-1"

async def test_create_target_group_with_config_and_tags(mc):
    mc.call.return_value = _TG
    r = await mod.create_target_group(
        "tg", config={"port": 80}, tags={"k": "v"},
    )
    assert r.id == "tg-1"

async def test_create_target_group_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_target_group("tg")

async def test_create_target_group_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_target_group failed"):
        await mod.create_target_group("tg")


async def test_get_target_group_success(mc):
    mc.call.return_value = _TG
    r = await mod.get_target_group("tg-1")
    assert r.id == "tg-1"

async def test_get_target_group_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_target_group("tg-1")

async def test_get_target_group_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_target_group failed"):
        await mod.get_target_group("tg-1")


async def test_list_target_groups_success(mc):
    mc.call.return_value = {"items": [_TG]}
    r = await mod.list_target_groups()
    assert len(r) == 1

async def test_list_target_groups_pagination(mc):
    mc.call.side_effect = [
        {"items": [_TG], "nextToken": "t1"},
        {"items": [_TG]},
    ]
    r = await mod.list_target_groups()
    assert len(r) == 2

async def test_list_target_groups_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_target_groups()

async def test_list_target_groups_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_target_groups failed"):
        await mod.list_target_groups()


# ---------------------------------------------------------------------------
# Target registration
# ---------------------------------------------------------------------------

async def test_register_targets_success(mc):
    mc.call.return_value = {"successful": [{"id": "i-1"}]}
    r = await mod.register_targets("tg-1", targets=[{"id": "i-1"}])
    assert len(r) == 1

async def test_register_targets_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.register_targets("tg-1", targets=[{"id": "i-1"}])

async def test_register_targets_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="register_targets failed"):
        await mod.register_targets("tg-1", targets=[{"id": "i-1"}])


async def test_deregister_targets_success(mc):
    mc.call.return_value = {"successful": [{"id": "i-1"}]}
    r = await mod.deregister_targets("tg-1", targets=[{"id": "i-1"}])
    assert len(r) == 1

async def test_deregister_targets_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.deregister_targets("tg-1", targets=[{"id": "i-1"}])

async def test_deregister_targets_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="deregister_targets failed"):
        await mod.deregister_targets("tg-1", targets=[{"id": "i-1"}])


async def test_list_targets_success(mc):
    mc.call.return_value = {"items": [_TGT]}
    r = await mod.list_targets("tg-1")
    assert len(r) == 1

async def test_list_targets_pagination(mc):
    mc.call.side_effect = [
        {"items": [_TGT], "nextToken": "t1"},
        {"items": [_TGT]},
    ]
    r = await mod.list_targets("tg-1")
    assert len(r) == 2

async def test_list_targets_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_targets("tg-1")

async def test_list_targets_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_targets failed"):
        await mod.list_targets("tg-1")


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_batch_update_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_rule("test-service_identifier", "test-listener_identifier", [], )
    mock_client.call.assert_called_once()


async def test_batch_update_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_rule("test-service_identifier", "test-listener_identifier", [], )


async def test_create_access_log_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_access_log_subscription("test-resource_identifier", "test-destination_arn", )
    mock_client.call.assert_called_once()


async def test_create_access_log_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_access_log_subscription("test-resource_identifier", "test-destination_arn", )


async def test_create_listener(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_listener("test-service_identifier", "test-name", "test-protocol", {}, )
    mock_client.call.assert_called_once()


async def test_create_listener_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_listener("test-service_identifier", "test-name", "test-protocol", {}, )


async def test_create_resource_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_configuration("test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_resource_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_configuration("test-name", "test-type_value", )


async def test_create_resource_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_gateway("test-name", )
    mock_client.call.assert_called_once()


async def test_create_resource_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_gateway("test-name", )


async def test_create_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_rule("test-service_identifier", "test-listener_identifier", "test-name", {}, 1, {}, )
    mock_client.call.assert_called_once()


async def test_create_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_rule("test-service_identifier", "test-listener_identifier", "test-name", {}, 1, {}, )


async def test_create_service_network_resource_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_network_resource_association("test-resource_configuration_identifier", "test-service_network_identifier", )
    mock_client.call.assert_called_once()


async def test_create_service_network_resource_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_network_resource_association("test-resource_configuration_identifier", "test-service_network_identifier", )


async def test_create_service_network_service_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_network_service_association("test-service_identifier", "test-service_network_identifier", )
    mock_client.call.assert_called_once()


async def test_create_service_network_service_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_network_service_association("test-service_identifier", "test-service_network_identifier", )


async def test_create_service_network_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", )
    mock_client.call.assert_called_once()


async def test_create_service_network_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", )


async def test_delete_access_log_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_access_log_subscription("test-access_log_subscription_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_access_log_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_access_log_subscription("test-access_log_subscription_identifier", )


async def test_delete_auth_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_auth_policy("test-resource_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_auth_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_auth_policy("test-resource_identifier", )


async def test_delete_domain_verification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_domain_verification("test-domain_verification_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_domain_verification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_domain_verification("test-domain_verification_identifier", )


async def test_delete_listener(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_listener("test-service_identifier", "test-listener_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_listener_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_listener("test-service_identifier", "test-listener_identifier", )


async def test_delete_resource_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_configuration("test-resource_configuration_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_resource_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_configuration("test-resource_configuration_identifier", )


async def test_delete_resource_endpoint_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_endpoint_association("test-resource_endpoint_association_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_resource_endpoint_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_endpoint_association("test-resource_endpoint_association_identifier", )


async def test_delete_resource_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_gateway("test-resource_gateway_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_resource_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_gateway("test-resource_gateway_identifier", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )


async def test_delete_service_network_resource_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_network_resource_association("test-service_network_resource_association_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_service_network_resource_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_network_resource_association("test-service_network_resource_association_identifier", )


async def test_delete_service_network_service_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_network_service_association("test-service_network_service_association_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_service_network_service_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_network_service_association("test-service_network_service_association_identifier", )


async def test_delete_service_network_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_network_vpc_association("test-service_network_vpc_association_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_service_network_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_network_vpc_association("test-service_network_vpc_association_identifier", )


async def test_delete_target_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_target_group("test-target_group_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_target_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_target_group("test-target_group_identifier", )


async def test_get_access_log_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_access_log_subscription("test-access_log_subscription_identifier", )
    mock_client.call.assert_called_once()


async def test_get_access_log_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_access_log_subscription("test-access_log_subscription_identifier", )


async def test_get_auth_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_auth_policy("test-resource_identifier", )
    mock_client.call.assert_called_once()


async def test_get_auth_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_auth_policy("test-resource_identifier", )


async def test_get_domain_verification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_domain_verification("test-domain_verification_identifier", )
    mock_client.call.assert_called_once()


async def test_get_domain_verification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_domain_verification("test-domain_verification_identifier", )


async def test_get_listener(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_listener("test-service_identifier", "test-listener_identifier", )
    mock_client.call.assert_called_once()


async def test_get_listener_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_listener("test-service_identifier", "test-listener_identifier", )


async def test_get_resource_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_configuration("test-resource_configuration_identifier", )
    mock_client.call.assert_called_once()


async def test_get_resource_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_configuration("test-resource_configuration_identifier", )


async def test_get_resource_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_gateway("test-resource_gateway_identifier", )
    mock_client.call.assert_called_once()


async def test_get_resource_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_gateway("test-resource_gateway_identifier", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_get_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )
    mock_client.call.assert_called_once()


async def test_get_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )


async def test_get_service_network_resource_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_network_resource_association("test-service_network_resource_association_identifier", )
    mock_client.call.assert_called_once()


async def test_get_service_network_resource_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_network_resource_association("test-service_network_resource_association_identifier", )


async def test_get_service_network_service_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_network_service_association("test-service_network_service_association_identifier", )
    mock_client.call.assert_called_once()


async def test_get_service_network_service_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_network_service_association("test-service_network_service_association_identifier", )


async def test_get_service_network_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_network_vpc_association("test-service_network_vpc_association_identifier", )
    mock_client.call.assert_called_once()


async def test_get_service_network_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_network_vpc_association("test-service_network_vpc_association_identifier", )


async def test_list_access_log_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_log_subscriptions("test-resource_identifier", )
    mock_client.call.assert_called_once()


async def test_list_access_log_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_log_subscriptions("test-resource_identifier", )


async def test_list_domain_verifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_domain_verifications()
    mock_client.call.assert_called_once()


async def test_list_domain_verifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_domain_verifications()


async def test_list_listeners(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_listeners("test-service_identifier", )
    mock_client.call.assert_called_once()


async def test_list_listeners_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_listeners("test-service_identifier", )


async def test_list_resource_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_configurations()
    mock_client.call.assert_called_once()


async def test_list_resource_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_configurations()


async def test_list_resource_endpoint_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_endpoint_associations("test-resource_configuration_identifier", )
    mock_client.call.assert_called_once()


async def test_list_resource_endpoint_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_endpoint_associations("test-resource_configuration_identifier", )


async def test_list_resource_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_gateways()
    mock_client.call.assert_called_once()


async def test_list_resource_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_gateways()


async def test_list_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rules("test-service_identifier", "test-listener_identifier", )
    mock_client.call.assert_called_once()


async def test_list_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rules("test-service_identifier", "test-listener_identifier", )


async def test_list_service_network_resource_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_network_resource_associations()
    mock_client.call.assert_called_once()


async def test_list_service_network_resource_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_network_resource_associations()


async def test_list_service_network_service_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_network_service_associations()
    mock_client.call.assert_called_once()


async def test_list_service_network_service_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_network_service_associations()


async def test_list_service_network_vpc_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_network_vpc_associations()
    mock_client.call.assert_called_once()


async def test_list_service_network_vpc_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_network_vpc_associations()


async def test_list_service_network_vpc_endpoint_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_network_vpc_endpoint_associations("test-service_network_identifier", )
    mock_client.call.assert_called_once()


async def test_list_service_network_vpc_endpoint_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_network_vpc_endpoint_associations("test-service_network_identifier", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_auth_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_auth_policy("test-resource_identifier", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_auth_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_auth_policy("test-resource_identifier", "test-policy", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy", )


async def test_start_domain_verification(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_domain_verification("test-domain_name", )
    mock_client.call.assert_called_once()


async def test_start_domain_verification_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_domain_verification("test-domain_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_access_log_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_access_log_subscription("test-access_log_subscription_identifier", "test-destination_arn", )
    mock_client.call.assert_called_once()


async def test_update_access_log_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_access_log_subscription("test-access_log_subscription_identifier", "test-destination_arn", )


async def test_update_listener(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_listener("test-service_identifier", "test-listener_identifier", {}, )
    mock_client.call.assert_called_once()


async def test_update_listener_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_listener("test-service_identifier", "test-listener_identifier", {}, )


async def test_update_resource_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_configuration("test-resource_configuration_identifier", )
    mock_client.call.assert_called_once()


async def test_update_resource_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_configuration("test-resource_configuration_identifier", )


async def test_update_resource_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_gateway("test-resource_gateway_identifier", )
    mock_client.call.assert_called_once()


async def test_update_resource_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_gateway("test-resource_gateway_identifier", )


async def test_update_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )
    mock_client.call.assert_called_once()


async def test_update_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", )


async def test_update_service_network_vpc_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_service_network_vpc_association("test-service_network_vpc_association_identifier", [], )
    mock_client.call.assert_called_once()


async def test_update_service_network_vpc_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_service_network_vpc_association("test-service_network_vpc_association_identifier", [], )


async def test_update_target_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_target_group("test-target_group_identifier", {}, )
    mock_client.call.assert_called_once()


async def test_update_target_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.vpc_lattice.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_target_group("test-target_group_identifier", {}, )


@pytest.mark.asyncio
async def test_create_target_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_target_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_target_group("test-name", config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_access_log_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_access_log_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_access_log_subscription("test-resource_identifier", "test-destination_arn", client_token="test-client_token", service_network_log_type="test-service_network_log_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_listener_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_listener
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_listener("test-service_identifier", "test-name", "test-protocol", "test-default_action", port=1, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_resource_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_resource_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_resource_configuration("test-name", "test-type_value", port_ranges=1, protocol="test-protocol", resource_gateway_identifier="test-resource_gateway_identifier", resource_configuration_group_identifier={}, resource_configuration_definition={}, allow_association_to_shareable_service_network=True, custom_domain_name="test-custom_domain_name", group_domain="test-group_domain", domain_verification_identifier="test-domain_verification_identifier", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_resource_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_resource_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_resource_gateway("test-name", client_token="test-client_token", vpc_identifier="test-vpc_identifier", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", ip_address_type="test-ip_address_type", ipv4_addresses_per_eni="test-ipv4_addresses_per_eni", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_rule("test-service_identifier", "test-listener_identifier", "test-name", "test-match", "test-priority", "test-action", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_network_resource_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_service_network_resource_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_service_network_resource_association({}, "test-service_network_identifier", client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_network_service_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_service_network_service_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_service_network_service_association("test-service_identifier", "test-service_network_identifier", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_network_vpc_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import create_service_network_vpc_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], dns_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_log_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_access_log_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_access_log_subscriptions("test-resource_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_domain_verifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_domain_verifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_domain_verifications(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_listeners_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_listeners
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_listeners("test-service_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_resource_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_resource_configurations(resource_gateway_identifier="test-resource_gateway_identifier", resource_configuration_group_identifier={}, domain_verification_identifier="test-domain_verification_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_resource_endpoint_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_resource_endpoint_associations({}, resource_endpoint_association_identifier="test-resource_endpoint_association_identifier", vpc_endpoint_id="test-vpc_endpoint_id", vpc_endpoint_owner="test-vpc_endpoint_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_resource_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_resource_gateways(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_rules("test-service_identifier", "test-listener_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_network_resource_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_service_network_resource_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_service_network_resource_associations(service_network_identifier="test-service_network_identifier", resource_configuration_identifier={}, max_results=1, next_token="test-next_token", include_children=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_network_service_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_service_network_service_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_service_network_service_associations(service_network_identifier="test-service_network_identifier", service_identifier="test-service_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_network_vpc_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_service_network_vpc_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_service_network_vpc_associations(service_network_identifier="test-service_network_identifier", vpc_identifier="test-vpc_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_network_vpc_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import list_service_network_vpc_endpoint_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await list_service_network_vpc_endpoint_associations("test-service_network_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_domain_verification_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import start_domain_verification
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await start_domain_verification("test-domain_name", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import update_resource_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await update_resource_configuration({}, resource_configuration_definition={}, allow_association_to_shareable_service_network=True, port_ranges=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import update_resource_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await update_resource_gateway("test-resource_gateway_identifier", security_group_ids="test-security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.vpc_lattice import update_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.vpc_lattice.async_client", lambda *a, **kw: mock_client)
    await update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", match="test-match", priority="test-priority", action="test-action", region_name="us-east-1")
    mock_client.call.assert_called_once()
