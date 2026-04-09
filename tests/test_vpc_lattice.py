"""Tests for aws_util.vpc_lattice module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.vpc_lattice as mod
from aws_util.vpc_lattice import (
    ServiceNetworkResult, ServiceResult, TargetGroupResult, TargetResult,
    _parse_sn, _parse_svc, _parse_tg, _parse_target,
    create_service, create_service_network, create_target_group,
    delete_service, delete_service_network, deregister_targets,
    get_service, get_service_network, get_target_group,
    list_service_networks, list_services, list_target_groups,
    list_targets, register_targets, update_service,
    update_service_network,
    batch_update_rule,
    create_access_log_subscription,
    create_listener,
    create_resource_configuration,
    create_resource_gateway,
    create_rule,
    create_service_network_resource_association,
    create_service_network_service_association,
    create_service_network_vpc_association,
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
    list_tags_for_resource,
    put_auth_policy,
    put_resource_policy,
    start_domain_verification,
    tag_resource,
    untag_resource,
    update_access_log_subscription,
    update_listener,
    update_resource_configuration,
    update_resource_gateway,
    update_rule,
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


def _ce(code="ServiceException", msg="fail"):
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# Models
def test_service_network_result():
    r = ServiceNetworkResult(id="sn-1", arn="arn:sn", name="sn")
    assert r.id == "sn-1"

def test_service_result():
    r = ServiceResult(id="svc-1", arn="arn:svc", name="svc")
    assert r.id == "svc-1"

def test_target_group_result():
    r = TargetGroupResult(id="tg-1", arn="arn:tg", name="tg")
    assert r.id == "tg-1"

def test_target_result():
    r = TargetResult(id="i-1")
    assert r.id == "i-1"


# Parsers
def test_parse_sn():
    r = _parse_sn(_SN)
    assert r.id == "sn-1"
    assert r.arn == "arn:sn"
    assert r.auth_type == "NONE"
    assert "extraSN" in r.extra

def test_parse_svc():
    r = _parse_svc(_SVC)
    assert r.id == "svc-1"
    assert r.dns_entry == {"domainName": "example.com"}
    assert "extraSVC" in r.extra

def test_parse_tg():
    r = _parse_tg(_TG)
    assert r.id == "tg-1"
    assert r.type == "INSTANCE"
    assert "extraTG" in r.extra

def test_parse_target():
    r = _parse_target(_TGT)
    assert r.id == "i-1"
    assert r.port == 80
    assert "extraTGT" in r.extra


# create_service_network
def test_create_service_network_success(monkeypatch):
    client = MagicMock()
    client.create_service_network.return_value = _SN
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_service_network("sn", region_name=REGION)
    assert r.id == "sn-1"

def test_create_service_network_with_tags(monkeypatch):
    client = MagicMock()
    client.create_service_network.return_value = _SN
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_service_network("sn", tags={"k": "v"}, region_name=REGION)
    assert r.id == "sn-1"
    call_kwargs = client.create_service_network.call_args[1]
    assert call_kwargs["tags"] == {"k": "v"}

def test_create_service_network_error(monkeypatch):
    client = MagicMock()
    client.create_service_network.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_service_network failed"):
        create_service_network("sn", region_name=REGION)


# get_service_network
def test_get_service_network_success(monkeypatch):
    client = MagicMock()
    client.get_service_network.return_value = _SN
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_service_network("sn-1", region_name=REGION)
    assert r.id == "sn-1"

def test_get_service_network_error(monkeypatch):
    client = MagicMock()
    client.get_service_network.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_service_network failed"):
        get_service_network("sn-1", region_name=REGION)


# list_service_networks
def test_list_service_networks_success(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"items": [_SN]}]
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_service_networks(region_name=REGION)
    assert len(r) == 1

def test_list_service_networks_error(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _ce()
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_service_networks failed"):
        list_service_networks(region_name=REGION)


# update_service_network
def test_update_service_network_success(monkeypatch):
    client = MagicMock()
    client.update_service_network.return_value = _SN
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_service_network("sn-1", auth_type="AWS_IAM", region_name=REGION)
    assert r.id == "sn-1"

def test_update_service_network_error(monkeypatch):
    client = MagicMock()
    client.update_service_network.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_service_network failed"):
        update_service_network("sn-1", auth_type="AWS_IAM", region_name=REGION)


# delete_service_network
def test_delete_service_network_success(monkeypatch):
    client = MagicMock()
    client.delete_service_network.return_value = {}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_service_network("sn-1", region_name=REGION)
    client.delete_service_network.assert_called_once()

def test_delete_service_network_error(monkeypatch):
    client = MagicMock()
    client.delete_service_network.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_service_network failed"):
        delete_service_network("sn-1", region_name=REGION)


# create_service
def test_create_service_success(monkeypatch):
    client = MagicMock()
    client.create_service.return_value = _SVC
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_service("svc", region_name=REGION)
    assert r.id == "svc-1"

def test_create_service_with_tags(monkeypatch):
    client = MagicMock()
    client.create_service.return_value = _SVC
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_service("svc", tags={"k": "v"}, region_name=REGION)
    assert r.id == "svc-1"
    call_kwargs = client.create_service.call_args[1]
    assert call_kwargs["tags"] == {"k": "v"}

def test_create_service_error(monkeypatch):
    client = MagicMock()
    client.create_service.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_service failed"):
        create_service("svc", region_name=REGION)


# get_service
def test_get_service_success(monkeypatch):
    client = MagicMock()
    client.get_service.return_value = _SVC
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_service("svc-1", region_name=REGION)
    assert r.id == "svc-1"

def test_get_service_error(monkeypatch):
    client = MagicMock()
    client.get_service.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_service failed"):
        get_service("svc-1", region_name=REGION)


# list_services
def test_list_services_success(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"items": [_SVC]}]
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_services(region_name=REGION)
    assert len(r) == 1

def test_list_services_error(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _ce()
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_services failed"):
        list_services(region_name=REGION)


# update_service
def test_update_service_success(monkeypatch):
    client = MagicMock()
    client.update_service.return_value = _SVC
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_service("svc-1", auth_type="AWS_IAM", region_name=REGION)
    assert r.id == "svc-1"

def test_update_service_error(monkeypatch):
    client = MagicMock()
    client.update_service.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_service failed"):
        update_service("svc-1", auth_type="AWS_IAM", region_name=REGION)


# delete_service
def test_delete_service_success(monkeypatch):
    client = MagicMock()
    client.delete_service.return_value = {}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_service("svc-1", region_name=REGION)
    client.delete_service.assert_called_once()

def test_delete_service_error(monkeypatch):
    client = MagicMock()
    client.delete_service.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_service failed"):
        delete_service("svc-1", region_name=REGION)


# create_target_group
def test_create_target_group_success(monkeypatch):
    client = MagicMock()
    client.create_target_group.return_value = _TG
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_target_group("tg", region_name=REGION)
    assert r.id == "tg-1"

def test_create_target_group_with_config_and_tags(monkeypatch):
    client = MagicMock()
    client.create_target_group.return_value = _TG
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_target_group(
        "tg", config={"port": 80, "protocol": "HTTP"},
        tags={"k": "v"}, region_name=REGION,
    )
    assert r.id == "tg-1"
    call_kwargs = client.create_target_group.call_args[1]
    assert call_kwargs["config"] == {"port": 80, "protocol": "HTTP"}
    assert call_kwargs["tags"] == {"k": "v"}

def test_create_target_group_error(monkeypatch):
    client = MagicMock()
    client.create_target_group.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_target_group failed"):
        create_target_group("tg", region_name=REGION)


# get_target_group
def test_get_target_group_success(monkeypatch):
    client = MagicMock()
    client.get_target_group.return_value = _TG
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_target_group("tg-1", region_name=REGION)
    assert r.id == "tg-1"

def test_get_target_group_error(monkeypatch):
    client = MagicMock()
    client.get_target_group.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_target_group failed"):
        get_target_group("tg-1", region_name=REGION)


# list_target_groups
def test_list_target_groups_success(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"items": [_TG]}]
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_target_groups(region_name=REGION)
    assert len(r) == 1

def test_list_target_groups_error(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _ce()
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_target_groups failed"):
        list_target_groups(region_name=REGION)


# register_targets
def test_register_targets_success(monkeypatch):
    client = MagicMock()
    client.register_targets.return_value = {"successful": [{"id": "i-1"}]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = register_targets("tg-1", targets=[{"id": "i-1"}], region_name=REGION)
    assert len(r) == 1

def test_register_targets_error(monkeypatch):
    client = MagicMock()
    client.register_targets.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="register_targets failed"):
        register_targets("tg-1", targets=[{"id": "i-1"}], region_name=REGION)


# deregister_targets
def test_deregister_targets_success(monkeypatch):
    client = MagicMock()
    client.deregister_targets.return_value = {"successful": [{"id": "i-1"}]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = deregister_targets("tg-1", targets=[{"id": "i-1"}], region_name=REGION)
    assert len(r) == 1

def test_deregister_targets_error(monkeypatch):
    client = MagicMock()
    client.deregister_targets.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="deregister_targets failed"):
        deregister_targets("tg-1", targets=[{"id": "i-1"}], region_name=REGION)


# list_targets
def test_list_targets_success(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"items": [_TGT]}]
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_targets("tg-1", region_name=REGION)
    assert len(r) == 1

def test_list_targets_error(monkeypatch):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _ce()
    client.get_paginator.return_value = paginator
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_targets failed"):
        list_targets("tg-1", region_name=REGION)


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_batch_update_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    batch_update_rule("test-service_identifier", "test-listener_identifier", [], region_name=REGION)
    mock_client.batch_update_rule.assert_called_once()


def test_batch_update_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_rule",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update rule"):
        batch_update_rule("test-service_identifier", "test-listener_identifier", [], region_name=REGION)


def test_create_access_log_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_log_subscription.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_access_log_subscription("test-resource_identifier", "test-destination_arn", region_name=REGION)
    mock_client.create_access_log_subscription.assert_called_once()


def test_create_access_log_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_log_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_access_log_subscription",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create access log subscription"):
        create_access_log_subscription("test-resource_identifier", "test-destination_arn", region_name=REGION)


def test_create_listener(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_listener.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_listener("test-service_identifier", "test-name", "test-protocol", {}, region_name=REGION)
    mock_client.create_listener.assert_called_once()


def test_create_listener_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_listener.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_listener",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create listener"):
        create_listener("test-service_identifier", "test-name", "test-protocol", {}, region_name=REGION)


def test_create_resource_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_resource_configuration("test-name", "test-type_value", region_name=REGION)
    mock_client.create_resource_configuration.assert_called_once()


def test_create_resource_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_configuration",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create resource configuration"):
        create_resource_configuration("test-name", "test-type_value", region_name=REGION)


def test_create_resource_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_resource_gateway("test-name", region_name=REGION)
    mock_client.create_resource_gateway.assert_called_once()


def test_create_resource_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_gateway",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create resource gateway"):
        create_resource_gateway("test-name", region_name=REGION)


def test_create_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_rule("test-service_identifier", "test-listener_identifier", "test-name", {}, 1, {}, region_name=REGION)
    mock_client.create_rule.assert_called_once()


def test_create_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_rule",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create rule"):
        create_rule("test-service_identifier", "test-listener_identifier", "test-name", {}, 1, {}, region_name=REGION)


def test_create_service_network_resource_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_resource_association("test-resource_configuration_identifier", "test-service_network_identifier", region_name=REGION)
    mock_client.create_service_network_resource_association.assert_called_once()


def test_create_service_network_resource_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_resource_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_network_resource_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service network resource association"):
        create_service_network_resource_association("test-resource_configuration_identifier", "test-service_network_identifier", region_name=REGION)


def test_create_service_network_service_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_service_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_service_association("test-service_identifier", "test-service_network_identifier", region_name=REGION)
    mock_client.create_service_network_service_association.assert_called_once()


def test_create_service_network_service_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_service_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_network_service_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service network service association"):
        create_service_network_service_association("test-service_identifier", "test-service_network_identifier", region_name=REGION)


def test_create_service_network_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", region_name=REGION)
    mock_client.create_service_network_vpc_association.assert_called_once()


def test_create_service_network_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_network_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_network_vpc_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service network vpc association"):
        create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", region_name=REGION)


def test_delete_access_log_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_log_subscription.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_access_log_subscription("test-access_log_subscription_identifier", region_name=REGION)
    mock_client.delete_access_log_subscription.assert_called_once()


def test_delete_access_log_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_log_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_access_log_subscription",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete access log subscription"):
        delete_access_log_subscription("test-access_log_subscription_identifier", region_name=REGION)


def test_delete_auth_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_auth_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_auth_policy("test-resource_identifier", region_name=REGION)
    mock_client.delete_auth_policy.assert_called_once()


def test_delete_auth_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_auth_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_auth_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete auth policy"):
        delete_auth_policy("test-resource_identifier", region_name=REGION)


def test_delete_domain_verification(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_verification.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_domain_verification("test-domain_verification_identifier", region_name=REGION)
    mock_client.delete_domain_verification.assert_called_once()


def test_delete_domain_verification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_verification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_verification",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete domain verification"):
        delete_domain_verification("test-domain_verification_identifier", region_name=REGION)


def test_delete_listener(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_listener.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_listener("test-service_identifier", "test-listener_identifier", region_name=REGION)
    mock_client.delete_listener.assert_called_once()


def test_delete_listener_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_listener.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_listener",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete listener"):
        delete_listener("test-service_identifier", "test-listener_identifier", region_name=REGION)


def test_delete_resource_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_resource_configuration("test-resource_configuration_identifier", region_name=REGION)
    mock_client.delete_resource_configuration.assert_called_once()


def test_delete_resource_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_configuration",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource configuration"):
        delete_resource_configuration("test-resource_configuration_identifier", region_name=REGION)


def test_delete_resource_endpoint_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_endpoint_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_resource_endpoint_association("test-resource_endpoint_association_identifier", region_name=REGION)
    mock_client.delete_resource_endpoint_association.assert_called_once()


def test_delete_resource_endpoint_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_endpoint_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_endpoint_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource endpoint association"):
        delete_resource_endpoint_association("test-resource_endpoint_association_identifier", region_name=REGION)


def test_delete_resource_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_resource_gateway("test-resource_gateway_identifier", region_name=REGION)
    mock_client.delete_resource_gateway.assert_called_once()


def test_delete_resource_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_gateway",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource gateway"):
        delete_resource_gateway("test-resource_gateway_identifier", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)
    mock_client.delete_rule.assert_called_once()


def test_delete_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_rule",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete rule"):
        delete_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)


def test_delete_service_network_resource_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_service_network_resource_association("test-service_network_resource_association_identifier", region_name=REGION)
    mock_client.delete_service_network_resource_association.assert_called_once()


def test_delete_service_network_resource_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_resource_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_network_resource_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service network resource association"):
        delete_service_network_resource_association("test-service_network_resource_association_identifier", region_name=REGION)


def test_delete_service_network_service_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_service_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_service_network_service_association("test-service_network_service_association_identifier", region_name=REGION)
    mock_client.delete_service_network_service_association.assert_called_once()


def test_delete_service_network_service_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_service_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_network_service_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service network service association"):
        delete_service_network_service_association("test-service_network_service_association_identifier", region_name=REGION)


def test_delete_service_network_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_service_network_vpc_association("test-service_network_vpc_association_identifier", region_name=REGION)
    mock_client.delete_service_network_vpc_association.assert_called_once()


def test_delete_service_network_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_network_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_network_vpc_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service network vpc association"):
        delete_service_network_vpc_association("test-service_network_vpc_association_identifier", region_name=REGION)


def test_delete_target_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_target_group.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    delete_target_group("test-target_group_identifier", region_name=REGION)
    mock_client.delete_target_group.assert_called_once()


def test_delete_target_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_target_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_target_group",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete target group"):
        delete_target_group("test-target_group_identifier", region_name=REGION)


def test_get_access_log_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_log_subscription.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_access_log_subscription("test-access_log_subscription_identifier", region_name=REGION)
    mock_client.get_access_log_subscription.assert_called_once()


def test_get_access_log_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_log_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_access_log_subscription",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get access log subscription"):
        get_access_log_subscription("test-access_log_subscription_identifier", region_name=REGION)


def test_get_auth_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auth_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_auth_policy("test-resource_identifier", region_name=REGION)
    mock_client.get_auth_policy.assert_called_once()


def test_get_auth_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_auth_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_auth_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get auth policy"):
        get_auth_policy("test-resource_identifier", region_name=REGION)


def test_get_domain_verification(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_verification.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_domain_verification("test-domain_verification_identifier", region_name=REGION)
    mock_client.get_domain_verification.assert_called_once()


def test_get_domain_verification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_verification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_verification",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get domain verification"):
        get_domain_verification("test-domain_verification_identifier", region_name=REGION)


def test_get_listener(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_listener.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_listener("test-service_identifier", "test-listener_identifier", region_name=REGION)
    mock_client.get_listener.assert_called_once()


def test_get_listener_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_listener.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_listener",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get listener"):
        get_listener("test-service_identifier", "test-listener_identifier", region_name=REGION)


def test_get_resource_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_resource_configuration("test-resource_configuration_identifier", region_name=REGION)
    mock_client.get_resource_configuration.assert_called_once()


def test_get_resource_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_configuration",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource configuration"):
        get_resource_configuration("test-resource_configuration_identifier", region_name=REGION)


def test_get_resource_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_resource_gateway("test-resource_gateway_identifier", region_name=REGION)
    mock_client.get_resource_gateway.assert_called_once()


def test_get_resource_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_gateway",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource gateway"):
        get_resource_gateway("test-resource_gateway_identifier", region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_get_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)
    mock_client.get_rule.assert_called_once()


def test_get_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_rule",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get rule"):
        get_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)


def test_get_service_network_resource_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_service_network_resource_association("test-service_network_resource_association_identifier", region_name=REGION)
    mock_client.get_service_network_resource_association.assert_called_once()


def test_get_service_network_resource_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_resource_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_network_resource_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service network resource association"):
        get_service_network_resource_association("test-service_network_resource_association_identifier", region_name=REGION)


def test_get_service_network_service_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_service_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_service_network_service_association("test-service_network_service_association_identifier", region_name=REGION)
    mock_client.get_service_network_service_association.assert_called_once()


def test_get_service_network_service_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_service_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_network_service_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service network service association"):
        get_service_network_service_association("test-service_network_service_association_identifier", region_name=REGION)


def test_get_service_network_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    get_service_network_vpc_association("test-service_network_vpc_association_identifier", region_name=REGION)
    mock_client.get_service_network_vpc_association.assert_called_once()


def test_get_service_network_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_network_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_network_vpc_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service network vpc association"):
        get_service_network_vpc_association("test-service_network_vpc_association_identifier", region_name=REGION)


def test_list_access_log_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_log_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_access_log_subscriptions("test-resource_identifier", region_name=REGION)
    mock_client.list_access_log_subscriptions.assert_called_once()


def test_list_access_log_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_log_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_log_subscriptions",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access log subscriptions"):
        list_access_log_subscriptions("test-resource_identifier", region_name=REGION)


def test_list_domain_verifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_verifications.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_domain_verifications(region_name=REGION)
    mock_client.list_domain_verifications.assert_called_once()


def test_list_domain_verifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_domain_verifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_domain_verifications",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list domain verifications"):
        list_domain_verifications(region_name=REGION)


def test_list_listeners(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_listeners.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_listeners("test-service_identifier", region_name=REGION)
    mock_client.list_listeners.assert_called_once()


def test_list_listeners_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_listeners.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_listeners",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list listeners"):
        list_listeners("test-service_identifier", region_name=REGION)


def test_list_resource_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_configurations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_configurations(region_name=REGION)
    mock_client.list_resource_configurations.assert_called_once()


def test_list_resource_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_configurations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource configurations"):
        list_resource_configurations(region_name=REGION)


def test_list_resource_endpoint_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_endpoint_associations("test-resource_configuration_identifier", region_name=REGION)
    mock_client.list_resource_endpoint_associations.assert_called_once()


def test_list_resource_endpoint_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_endpoint_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_endpoint_associations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource endpoint associations"):
        list_resource_endpoint_associations("test-resource_configuration_identifier", region_name=REGION)


def test_list_resource_gateways(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_gateways.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_gateways(region_name=REGION)
    mock_client.list_resource_gateways.assert_called_once()


def test_list_resource_gateways_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_gateways",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource gateways"):
        list_resource_gateways(region_name=REGION)


def test_list_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rules.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_rules("test-service_identifier", "test-listener_identifier", region_name=REGION)
    mock_client.list_rules.assert_called_once()


def test_list_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rules",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list rules"):
        list_rules("test-service_identifier", "test-listener_identifier", region_name=REGION)


def test_list_service_network_resource_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_resource_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_resource_associations(region_name=REGION)
    mock_client.list_service_network_resource_associations.assert_called_once()


def test_list_service_network_resource_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_resource_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_network_resource_associations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service network resource associations"):
        list_service_network_resource_associations(region_name=REGION)


def test_list_service_network_service_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_service_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_service_associations(region_name=REGION)
    mock_client.list_service_network_service_associations.assert_called_once()


def test_list_service_network_service_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_service_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_network_service_associations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service network service associations"):
        list_service_network_service_associations(region_name=REGION)


def test_list_service_network_vpc_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_vpc_associations(region_name=REGION)
    mock_client.list_service_network_vpc_associations.assert_called_once()


def test_list_service_network_vpc_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_network_vpc_associations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service network vpc associations"):
        list_service_network_vpc_associations(region_name=REGION)


def test_list_service_network_vpc_endpoint_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_vpc_endpoint_associations("test-service_network_identifier", region_name=REGION)
    mock_client.list_service_network_vpc_endpoint_associations.assert_called_once()


def test_list_service_network_vpc_endpoint_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_endpoint_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_network_vpc_endpoint_associations",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service network vpc endpoint associations"):
        list_service_network_vpc_endpoint_associations("test-service_network_identifier", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_put_auth_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_auth_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    put_auth_policy("test-resource_identifier", "test-policy", region_name=REGION)
    mock_client.put_auth_policy.assert_called_once()


def test_put_auth_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_auth_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_auth_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put auth policy"):
        put_auth_policy("test-resource_identifier", "test-policy", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


def test_start_domain_verification(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_domain_verification.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    start_domain_verification("test-domain_name", region_name=REGION)
    mock_client.start_domain_verification.assert_called_once()


def test_start_domain_verification_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_domain_verification.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_domain_verification",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start domain verification"):
        start_domain_verification("test-domain_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_access_log_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_log_subscription.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_access_log_subscription("test-access_log_subscription_identifier", "test-destination_arn", region_name=REGION)
    mock_client.update_access_log_subscription.assert_called_once()


def test_update_access_log_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_log_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_access_log_subscription",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update access log subscription"):
        update_access_log_subscription("test-access_log_subscription_identifier", "test-destination_arn", region_name=REGION)


def test_update_listener(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_listener.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_listener("test-service_identifier", "test-listener_identifier", {}, region_name=REGION)
    mock_client.update_listener.assert_called_once()


def test_update_listener_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_listener.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_listener",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update listener"):
        update_listener("test-service_identifier", "test-listener_identifier", {}, region_name=REGION)


def test_update_resource_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_resource_configuration("test-resource_configuration_identifier", region_name=REGION)
    mock_client.update_resource_configuration.assert_called_once()


def test_update_resource_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_configuration",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update resource configuration"):
        update_resource_configuration("test-resource_configuration_identifier", region_name=REGION)


def test_update_resource_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_resource_gateway("test-resource_gateway_identifier", region_name=REGION)
    mock_client.update_resource_gateway.assert_called_once()


def test_update_resource_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_gateway",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update resource gateway"):
        update_resource_gateway("test-resource_gateway_identifier", region_name=REGION)


def test_update_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)
    mock_client.update_rule.assert_called_once()


def test_update_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_rule",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update rule"):
        update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", region_name=REGION)


def test_update_service_network_vpc_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_network_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_service_network_vpc_association("test-service_network_vpc_association_identifier", [], region_name=REGION)
    mock_client.update_service_network_vpc_association.assert_called_once()


def test_update_service_network_vpc_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_network_vpc_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_service_network_vpc_association",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update service network vpc association"):
        update_service_network_vpc_association("test-service_network_vpc_association_identifier", [], region_name=REGION)


def test_update_target_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_target_group.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_target_group("test-target_group_identifier", {}, region_name=REGION)
    mock_client.update_target_group.assert_called_once()


def test_update_target_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_target_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_target_group",
    )
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update target group"):
        update_target_group("test-target_group_identifier", {}, region_name=REGION)


def test_create_target_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_target_group
    mock_client = MagicMock()
    mock_client.create_target_group.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_target_group("test-name", config={}, region_name="us-east-1")
    mock_client.create_target_group.assert_called_once()

def test_create_access_log_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_access_log_subscription
    mock_client = MagicMock()
    mock_client.create_access_log_subscription.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_access_log_subscription("test-resource_identifier", "test-destination_arn", client_token="test-client_token", service_network_log_type="test-service_network_log_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_access_log_subscription.assert_called_once()

def test_create_listener_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_listener
    mock_client = MagicMock()
    mock_client.create_listener.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_listener("test-service_identifier", "test-name", "test-protocol", "test-default_action", port=1, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_listener.assert_called_once()

def test_create_resource_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_resource_configuration
    mock_client = MagicMock()
    mock_client.create_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_resource_configuration("test-name", "test-type_value", port_ranges=1, protocol="test-protocol", resource_gateway_identifier="test-resource_gateway_identifier", resource_configuration_group_identifier={}, resource_configuration_definition={}, allow_association_to_shareable_service_network=True, custom_domain_name="test-custom_domain_name", group_domain="test-group_domain", domain_verification_identifier="test-domain_verification_identifier", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_resource_configuration.assert_called_once()

def test_create_resource_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_resource_gateway
    mock_client = MagicMock()
    mock_client.create_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_resource_gateway("test-name", client_token="test-client_token", vpc_identifier="test-vpc_identifier", subnet_ids="test-subnet_ids", security_group_ids="test-security_group_ids", ip_address_type="test-ip_address_type", ipv4_addresses_per_eni="test-ipv4_addresses_per_eni", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_resource_gateway.assert_called_once()

def test_create_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_rule
    mock_client = MagicMock()
    mock_client.create_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_rule("test-service_identifier", "test-listener_identifier", "test-name", "test-match", "test-priority", "test-action", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_rule.assert_called_once()

def test_create_service_network_resource_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_service_network_resource_association
    mock_client = MagicMock()
    mock_client.create_service_network_resource_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_resource_association({}, "test-service_network_identifier", client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_service_network_resource_association.assert_called_once()

def test_create_service_network_service_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_service_network_service_association
    mock_client = MagicMock()
    mock_client.create_service_network_service_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_service_association("test-service_identifier", "test-service_network_identifier", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_service_network_service_association.assert_called_once()

def test_create_service_network_vpc_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import create_service_network_vpc_association
    mock_client = MagicMock()
    mock_client.create_service_network_vpc_association.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    create_service_network_vpc_association("test-service_network_identifier", "test-vpc_identifier", client_token="test-client_token", private_dns_enabled="test-private_dns_enabled", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], dns_options={}, region_name="us-east-1")
    mock_client.create_service_network_vpc_association.assert_called_once()

def test_list_access_log_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_access_log_subscriptions
    mock_client = MagicMock()
    mock_client.list_access_log_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_access_log_subscriptions("test-resource_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_access_log_subscriptions.assert_called_once()

def test_list_domain_verifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_domain_verifications
    mock_client = MagicMock()
    mock_client.list_domain_verifications.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_domain_verifications(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_domain_verifications.assert_called_once()

def test_list_listeners_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_listeners
    mock_client = MagicMock()
    mock_client.list_listeners.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_listeners("test-service_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_listeners.assert_called_once()

def test_list_resource_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_resource_configurations
    mock_client = MagicMock()
    mock_client.list_resource_configurations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_configurations(resource_gateway_identifier="test-resource_gateway_identifier", resource_configuration_group_identifier={}, domain_verification_identifier="test-domain_verification_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_configurations.assert_called_once()

def test_list_resource_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_resource_endpoint_associations
    mock_client = MagicMock()
    mock_client.list_resource_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_endpoint_associations({}, resource_endpoint_association_identifier="test-resource_endpoint_association_identifier", vpc_endpoint_id="test-vpc_endpoint_id", vpc_endpoint_owner="test-vpc_endpoint_owner", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_endpoint_associations.assert_called_once()

def test_list_resource_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_resource_gateways
    mock_client = MagicMock()
    mock_client.list_resource_gateways.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_resource_gateways(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_gateways.assert_called_once()

def test_list_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_rules
    mock_client = MagicMock()
    mock_client.list_rules.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_rules("test-service_identifier", "test-listener_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_rules.assert_called_once()

def test_list_service_network_resource_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_service_network_resource_associations
    mock_client = MagicMock()
    mock_client.list_service_network_resource_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_resource_associations(service_network_identifier="test-service_network_identifier", resource_configuration_identifier={}, max_results=1, next_token="test-next_token", include_children=True, region_name="us-east-1")
    mock_client.list_service_network_resource_associations.assert_called_once()

def test_list_service_network_service_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_service_network_service_associations
    mock_client = MagicMock()
    mock_client.list_service_network_service_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_service_associations(service_network_identifier="test-service_network_identifier", service_identifier="test-service_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_service_network_service_associations.assert_called_once()

def test_list_service_network_vpc_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_service_network_vpc_associations
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_vpc_associations(service_network_identifier="test-service_network_identifier", vpc_identifier="test-vpc_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_service_network_vpc_associations.assert_called_once()

def test_list_service_network_vpc_endpoint_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import list_service_network_vpc_endpoint_associations
    mock_client = MagicMock()
    mock_client.list_service_network_vpc_endpoint_associations.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    list_service_network_vpc_endpoint_associations("test-service_network_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_service_network_vpc_endpoint_associations.assert_called_once()

def test_start_domain_verification_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import start_domain_verification
    mock_client = MagicMock()
    mock_client.start_domain_verification.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    start_domain_verification("test-domain_name", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_domain_verification.assert_called_once()

def test_update_resource_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import update_resource_configuration
    mock_client = MagicMock()
    mock_client.update_resource_configuration.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_resource_configuration({}, resource_configuration_definition={}, allow_association_to_shareable_service_network=True, port_ranges=1, region_name="us-east-1")
    mock_client.update_resource_configuration.assert_called_once()

def test_update_resource_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import update_resource_gateway
    mock_client = MagicMock()
    mock_client.update_resource_gateway.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_resource_gateway("test-resource_gateway_identifier", security_group_ids="test-security_group_ids", region_name="us-east-1")
    mock_client.update_resource_gateway.assert_called_once()

def test_update_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.vpc_lattice import update_rule
    mock_client = MagicMock()
    mock_client.update_rule.return_value = {}
    monkeypatch.setattr("aws_util.vpc_lattice.get_client", lambda *a, **kw: mock_client)
    update_rule("test-service_identifier", "test-listener_identifier", "test-rule_identifier", match="test-match", priority="test-priority", action="test-action", region_name="us-east-1")
    mock_client.update_rule.assert_called_once()
