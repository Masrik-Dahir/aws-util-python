"""Tests for aws_util.route53 module."""
from __future__ import annotations

import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.route53 as r53_mod
from aws_util.route53 import (
    HostedZone,
    ResourceRecord,
    list_hosted_zones,
    get_hosted_zone,
    list_records,
    upsert_record,
    delete_record,
    wait_for_change,
    bulk_upsert_records,
    activate_key_signing_key,
    associate_vpc_with_hosted_zone,
    change_cidr_collection,
    change_resource_record_sets,
    change_tags_for_resource,
    create_cidr_collection,
    create_health_check,
    create_hosted_zone,
    create_key_signing_key,
    create_query_logging_config,
    create_reusable_delegation_set,
    create_traffic_policy,
    create_traffic_policy_instance,
    create_traffic_policy_version,
    create_vpc_association_authorization,
    deactivate_key_signing_key,
    delete_cidr_collection,
    delete_health_check,
    delete_hosted_zone,
    delete_key_signing_key,
    delete_query_logging_config,
    delete_reusable_delegation_set,
    delete_traffic_policy,
    delete_traffic_policy_instance,
    delete_vpc_association_authorization,
    disable_hosted_zone_dnssec,
    disassociate_vpc_from_hosted_zone,
    enable_hosted_zone_dnssec,
    get_account_limit,
    get_change,
    get_checker_ip_ranges,
    get_dnssec,
    get_geo_location,
    get_health_check,
    get_health_check_count,
    get_health_check_last_failure_reason,
    get_health_check_status,
    get_hosted_zone_count,
    get_hosted_zone_limit,
    get_query_logging_config,
    get_reusable_delegation_set,
    get_reusable_delegation_set_limit,
    get_traffic_policy,
    get_traffic_policy_instance,
    get_traffic_policy_instance_count,
    list_cidr_blocks,
    list_cidr_collections,
    list_cidr_locations,
    list_geo_locations,
    list_health_checks,
    list_hosted_zones_by_name,
    list_hosted_zones_by_vpc,
    list_query_logging_configs,
    list_resource_record_sets,
    list_reusable_delegation_sets,
    list_tags_for_resource,
    list_tags_for_resources,
    list_traffic_policies,
    list_traffic_policy_instances,
    list_traffic_policy_instances_by_hosted_zone,
    list_traffic_policy_instances_by_policy,
    list_traffic_policy_versions,
    list_vpc_association_authorizations,
    run_dns_answer,
    update_health_check,
    update_hosted_zone_comment,
    update_traffic_policy_comment,
    update_traffic_policy_instance,
)

REGION = "us-east-1"
DOMAIN = "example.com."


@pytest.fixture
def hosted_zone():
    client = boto3.client("route53", region_name=REGION)
    resp = client.create_hosted_zone(
        Name=DOMAIN,
        CallerReference="unique-ref-1",
    )
    zone_id = resp["HostedZone"]["Id"].split("/")[-1]
    return zone_id


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_hosted_zone_model():
    zone = HostedZone(zone_id="Z123", name=DOMAIN, record_count=2)
    assert zone.zone_id == "Z123"
    assert zone.private_zone is False


def test_resource_record_model():
    rec = ResourceRecord(name="api.example.com.", record_type="A", values=["1.2.3.4"])
    assert rec.record_type == "A"
    assert rec.alias_dns_name is None


# ---------------------------------------------------------------------------
# list_hosted_zones
# ---------------------------------------------------------------------------

def test_list_hosted_zones_returns_list(hosted_zone):
    result = list_hosted_zones(region_name=REGION)
    assert isinstance(result, list)
    assert any(z.zone_id == hosted_zone for z in result)


def test_list_hosted_zones_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListHostedZones"
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_hosted_zones failed"):
        list_hosted_zones(region_name=REGION)


# ---------------------------------------------------------------------------
# get_hosted_zone
# ---------------------------------------------------------------------------

def test_get_hosted_zone_found(hosted_zone):
    result = get_hosted_zone(hosted_zone, region_name=REGION)
    assert result is not None
    assert result.zone_id == hosted_zone


def test_get_hosted_zone_not_found(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "NoSuchHostedZone", "Message": "not found"}}, "GetHostedZone"
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_hosted_zone("Z_NONEXISTENT", region_name=REGION)
    assert result is None


def test_get_hosted_zone_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "GetHostedZone"
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_hosted_zone failed"):
        get_hosted_zone("Z123", region_name=REGION)


# ---------------------------------------------------------------------------
# list_records
# ---------------------------------------------------------------------------

def test_list_records_returns_list(hosted_zone):
    result = list_records(hosted_zone, region_name=REGION)
    assert isinstance(result, list)
    # New zone has NS and SOA records
    assert len(result) >= 2


def test_list_records_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "NoSuchHostedZone", "Message": "not found"}},
        "ListResourceRecordSets",
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_records failed"):
        list_records("Z_NONEXISTENT", region_name=REGION)


# ---------------------------------------------------------------------------
# upsert_record
# ---------------------------------------------------------------------------

def test_upsert_record_success(hosted_zone):
    change_id = upsert_record(
        hosted_zone, "api.example.com", "A", ["1.2.3.4"], ttl=300, region_name=REGION
    )
    assert change_id


def test_upsert_record_adds_trailing_dot(hosted_zone):
    # Should work without trailing dot
    change_id = upsert_record(
        hosted_zone, "www.example.com", "CNAME", ["api.example.com"], region_name=REGION
    )
    assert change_id


def test_upsert_record_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_resource_record_sets.side_effect = ClientError(
        {"Error": {"Code": "NoSuchHostedZone", "Message": "not found"}},
        "ChangeResourceRecordSets",
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upsert record"):
        upsert_record("Z_NONEXISTENT", "api.example.com", "A", ["1.2.3.4"], region_name=REGION)


# ---------------------------------------------------------------------------
# delete_record
# ---------------------------------------------------------------------------

def test_delete_record_success(hosted_zone):
    # First create the record
    upsert_record(hosted_zone, "del.example.com", "A", ["1.2.3.4"], region_name=REGION)
    # Then delete it
    change_id = delete_record(
        hosted_zone, "del.example.com", "A", ["1.2.3.4"], ttl=300, region_name=REGION
    )
    assert change_id


def test_delete_record_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_resource_record_sets.side_effect = ClientError(
        {"Error": {"Code": "NoSuchHostedZone", "Message": "not found"}},
        "ChangeResourceRecordSets",
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete record"):
        delete_record("Z_NONEXISTENT", "a.example.com", "A", ["1.2.3.4"], region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_change
# ---------------------------------------------------------------------------

def test_wait_for_change_insync(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.return_value = {
        "ChangeInfo": {"Status": "INSYNC", "Id": "/change/C123"}
    }
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    status = wait_for_change("C123", timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert status == "INSYNC"


def test_wait_for_change_normalises_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.return_value = {
        "ChangeInfo": {"Status": "INSYNC", "Id": "/change/C123"}
    }
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    # Pass without /change/ prefix
    wait_for_change("C123", timeout=5.0, region_name=REGION)
    called_id = mock_client.get_change.call_args[1]["Id"]
    assert called_id == "/change/C123"


def test_wait_for_change_timeout(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.return_value = {
        "ChangeInfo": {"Status": "PENDING", "Id": "/change/C123"}
    }
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(TimeoutError):
        wait_for_change("C123", timeout=0.0, poll_interval=0.0, region_name=REGION)


def test_wait_for_change_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.side_effect = ClientError(
        {"Error": {"Code": "NoSuchChange", "Message": "not found"}}, "GetChange"
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="wait_for_change failed"):
        wait_for_change("/change/C123", timeout=5.0, region_name=REGION)


# ---------------------------------------------------------------------------
# bulk_upsert_records
# ---------------------------------------------------------------------------

def test_bulk_upsert_records_success(hosted_zone):
    records = [
        {"name": "a.example.com", "record_type": "A", "values": ["1.2.3.4"]},
        {"name": "b.example.com", "record_type": "A", "values": ["5.6.7.8"], "ttl": 60},
    ]
    change_id = bulk_upsert_records(hosted_zone, records, region_name=REGION)
    assert change_id


def test_bulk_upsert_records_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_resource_record_sets.side_effect = ClientError(
        {"Error": {"Code": "NoSuchHostedZone", "Message": "not found"}},
        "ChangeResourceRecordSets",
    )
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    records = [{"name": "a.example.com", "record_type": "A", "values": ["1.2.3.4"]}]
    with pytest.raises(RuntimeError, match="bulk_upsert_records failed"):
        bulk_upsert_records("Z_NONEXISTENT", records, region_name=REGION)


def test_wait_for_change_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_change (line 304)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}
    mock_client = MagicMock()

    def fake_get_change(Id):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return {"ChangeInfo": {"Status": "PENDING", "Id": Id}}
        return {"ChangeInfo": {"Status": "INSYNC", "Id": Id}}

    mock_client.get_change.side_effect = fake_get_change
    monkeypatch.setattr(r53_mod, "get_client", lambda *a, **kw: mock_client)
    wait_for_change("C123", timeout=10.0, poll_interval=0.001, region_name="us-east-1")


def test_activate_key_signing_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_key_signing_key.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    activate_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)
    mock_client.activate_key_signing_key.assert_called_once()


def test_activate_key_signing_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_key_signing_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "activate_key_signing_key",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to activate key signing key"):
        activate_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)


def test_associate_vpc_with_hosted_zone(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_vpc_with_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    associate_vpc_with_hosted_zone("test-hosted_zone_id", {}, region_name=REGION)
    mock_client.associate_vpc_with_hosted_zone.assert_called_once()


def test_associate_vpc_with_hosted_zone_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_vpc_with_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_vpc_with_hosted_zone",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate vpc with hosted zone"):
        associate_vpc_with_hosted_zone("test-hosted_zone_id", {}, region_name=REGION)


def test_change_cidr_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_cidr_collection.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    change_cidr_collection("test-id", [], region_name=REGION)
    mock_client.change_cidr_collection.assert_called_once()


def test_change_cidr_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_cidr_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "change_cidr_collection",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to change cidr collection"):
        change_cidr_collection("test-id", [], region_name=REGION)


def test_change_resource_record_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_resource_record_sets.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    change_resource_record_sets("test-hosted_zone_id", {}, region_name=REGION)
    mock_client.change_resource_record_sets.assert_called_once()


def test_change_resource_record_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_resource_record_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "change_resource_record_sets",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to change resource record sets"):
        change_resource_record_sets("test-hosted_zone_id", {}, region_name=REGION)


def test_change_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    change_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)
    mock_client.change_tags_for_resource.assert_called_once()


def test_change_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "change_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to change tags for resource"):
        change_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)


def test_create_cidr_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cidr_collection.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_cidr_collection("test-name", "test-caller_reference", region_name=REGION)
    mock_client.create_cidr_collection.assert_called_once()


def test_create_cidr_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cidr_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cidr_collection",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cidr collection"):
        create_cidr_collection("test-name", "test-caller_reference", region_name=REGION)


def test_create_health_check(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_health_check.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_health_check("test-caller_reference", {}, region_name=REGION)
    mock_client.create_health_check.assert_called_once()


def test_create_health_check_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_health_check.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_health_check",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create health check"):
        create_health_check("test-caller_reference", {}, region_name=REGION)


def test_create_hosted_zone(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_hosted_zone("test-name", "test-caller_reference", region_name=REGION)
    mock_client.create_hosted_zone.assert_called_once()


def test_create_hosted_zone_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_hosted_zone",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create hosted zone"):
        create_hosted_zone("test-name", "test-caller_reference", region_name=REGION)


def test_create_key_signing_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_signing_key.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_key_signing_key("test-caller_reference", "test-hosted_zone_id", "test-key_management_service_arn", "test-name", "test-status", region_name=REGION)
    mock_client.create_key_signing_key.assert_called_once()


def test_create_key_signing_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_key_signing_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_key_signing_key",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create key signing key"):
        create_key_signing_key("test-caller_reference", "test-hosted_zone_id", "test-key_management_service_arn", "test-name", "test-status", region_name=REGION)


def test_create_query_logging_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_query_logging_config.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_query_logging_config("test-hosted_zone_id", "test-cloud_watch_logs_log_group_arn", region_name=REGION)
    mock_client.create_query_logging_config.assert_called_once()


def test_create_query_logging_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_query_logging_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_query_logging_config",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create query logging config"):
        create_query_logging_config("test-hosted_zone_id", "test-cloud_watch_logs_log_group_arn", region_name=REGION)


def test_create_reusable_delegation_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reusable_delegation_set.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_reusable_delegation_set("test-caller_reference", region_name=REGION)
    mock_client.create_reusable_delegation_set.assert_called_once()


def test_create_reusable_delegation_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_reusable_delegation_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_reusable_delegation_set",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create reusable delegation set"):
        create_reusable_delegation_set("test-caller_reference", region_name=REGION)


def test_create_traffic_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_traffic_policy("test-name", "test-document", region_name=REGION)
    mock_client.create_traffic_policy.assert_called_once()


def test_create_traffic_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_policy",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic policy"):
        create_traffic_policy("test-name", "test-document", region_name=REGION)


def test_create_traffic_policy_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy_instance.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_traffic_policy_instance("test-hosted_zone_id", "test-name", 1, "test-traffic_policy_id", 1, region_name=REGION)
    mock_client.create_traffic_policy_instance.assert_called_once()


def test_create_traffic_policy_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_policy_instance",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic policy instance"):
        create_traffic_policy_instance("test-hosted_zone_id", "test-name", 1, "test-traffic_policy_id", 1, region_name=REGION)


def test_create_traffic_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_traffic_policy_version("test-id", "test-document", region_name=REGION)
    mock_client.create_traffic_policy_version.assert_called_once()


def test_create_traffic_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_policy_version",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic policy version"):
        create_traffic_policy_version("test-id", "test-document", region_name=REGION)


def test_create_vpc_association_authorization(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_association_authorization.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_vpc_association_authorization("test-hosted_zone_id", {}, region_name=REGION)
    mock_client.create_vpc_association_authorization.assert_called_once()


def test_create_vpc_association_authorization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_association_authorization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_association_authorization",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc association authorization"):
        create_vpc_association_authorization("test-hosted_zone_id", {}, region_name=REGION)


def test_deactivate_key_signing_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_key_signing_key.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    deactivate_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)
    mock_client.deactivate_key_signing_key.assert_called_once()


def test_deactivate_key_signing_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_key_signing_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_key_signing_key",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate key signing key"):
        deactivate_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)


def test_delete_cidr_collection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cidr_collection.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_cidr_collection("test-id", region_name=REGION)
    mock_client.delete_cidr_collection.assert_called_once()


def test_delete_cidr_collection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cidr_collection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cidr_collection",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cidr collection"):
        delete_cidr_collection("test-id", region_name=REGION)


def test_delete_health_check(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_health_check.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_health_check("test-health_check_id", region_name=REGION)
    mock_client.delete_health_check.assert_called_once()


def test_delete_health_check_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_health_check.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_health_check",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete health check"):
        delete_health_check("test-health_check_id", region_name=REGION)


def test_delete_hosted_zone(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_hosted_zone("test-id", region_name=REGION)
    mock_client.delete_hosted_zone.assert_called_once()


def test_delete_hosted_zone_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_hosted_zone",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete hosted zone"):
        delete_hosted_zone("test-id", region_name=REGION)


def test_delete_key_signing_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_signing_key.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)
    mock_client.delete_key_signing_key.assert_called_once()


def test_delete_key_signing_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_key_signing_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_key_signing_key",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete key signing key"):
        delete_key_signing_key("test-hosted_zone_id", "test-name", region_name=REGION)


def test_delete_query_logging_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_query_logging_config.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_query_logging_config("test-id", region_name=REGION)
    mock_client.delete_query_logging_config.assert_called_once()


def test_delete_query_logging_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_query_logging_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_query_logging_config",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete query logging config"):
        delete_query_logging_config("test-id", region_name=REGION)


def test_delete_reusable_delegation_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_reusable_delegation_set.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_reusable_delegation_set("test-id", region_name=REGION)
    mock_client.delete_reusable_delegation_set.assert_called_once()


def test_delete_reusable_delegation_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_reusable_delegation_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_reusable_delegation_set",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete reusable delegation set"):
        delete_reusable_delegation_set("test-id", region_name=REGION)


def test_delete_traffic_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_traffic_policy("test-id", 1, region_name=REGION)
    mock_client.delete_traffic_policy.assert_called_once()


def test_delete_traffic_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_policy",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic policy"):
        delete_traffic_policy("test-id", 1, region_name=REGION)


def test_delete_traffic_policy_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_policy_instance.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_traffic_policy_instance("test-id", region_name=REGION)
    mock_client.delete_traffic_policy_instance.assert_called_once()


def test_delete_traffic_policy_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_policy_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_policy_instance",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic policy instance"):
        delete_traffic_policy_instance("test-id", region_name=REGION)


def test_delete_vpc_association_authorization(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_association_authorization.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    delete_vpc_association_authorization("test-hosted_zone_id", {}, region_name=REGION)
    mock_client.delete_vpc_association_authorization.assert_called_once()


def test_delete_vpc_association_authorization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_association_authorization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_association_authorization",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc association authorization"):
        delete_vpc_association_authorization("test-hosted_zone_id", {}, region_name=REGION)


def test_disable_hosted_zone_dnssec(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_hosted_zone_dnssec.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    disable_hosted_zone_dnssec("test-hosted_zone_id", region_name=REGION)
    mock_client.disable_hosted_zone_dnssec.assert_called_once()


def test_disable_hosted_zone_dnssec_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_hosted_zone_dnssec.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_hosted_zone_dnssec",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable hosted zone dnssec"):
        disable_hosted_zone_dnssec("test-hosted_zone_id", region_name=REGION)


def test_disassociate_vpc_from_hosted_zone(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_vpc_from_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    disassociate_vpc_from_hosted_zone("test-hosted_zone_id", {}, region_name=REGION)
    mock_client.disassociate_vpc_from_hosted_zone.assert_called_once()


def test_disassociate_vpc_from_hosted_zone_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_vpc_from_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_vpc_from_hosted_zone",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate vpc from hosted zone"):
        disassociate_vpc_from_hosted_zone("test-hosted_zone_id", {}, region_name=REGION)


def test_enable_hosted_zone_dnssec(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_hosted_zone_dnssec.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    enable_hosted_zone_dnssec("test-hosted_zone_id", region_name=REGION)
    mock_client.enable_hosted_zone_dnssec.assert_called_once()


def test_enable_hosted_zone_dnssec_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_hosted_zone_dnssec.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_hosted_zone_dnssec",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable hosted zone dnssec"):
        enable_hosted_zone_dnssec("test-hosted_zone_id", region_name=REGION)


def test_get_account_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_limit.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_account_limit("test-type_value", region_name=REGION)
    mock_client.get_account_limit.assert_called_once()


def test_get_account_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_limit",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account limit"):
        get_account_limit("test-type_value", region_name=REGION)


def test_get_change(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_change("test-id", region_name=REGION)
    mock_client.get_change.assert_called_once()


def test_get_change_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_change.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_change",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get change"):
        get_change("test-id", region_name=REGION)


def test_get_checker_ip_ranges(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_checker_ip_ranges.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_checker_ip_ranges(region_name=REGION)
    mock_client.get_checker_ip_ranges.assert_called_once()


def test_get_checker_ip_ranges_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_checker_ip_ranges.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_checker_ip_ranges",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get checker ip ranges"):
        get_checker_ip_ranges(region_name=REGION)


def test_get_dnssec(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dnssec.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_dnssec("test-hosted_zone_id", region_name=REGION)
    mock_client.get_dnssec.assert_called_once()


def test_get_dnssec_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dnssec.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dnssec",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dnssec"):
        get_dnssec("test-hosted_zone_id", region_name=REGION)


def test_get_geo_location(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_geo_location.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_geo_location(region_name=REGION)
    mock_client.get_geo_location.assert_called_once()


def test_get_geo_location_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_geo_location.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_geo_location",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get geo location"):
        get_geo_location(region_name=REGION)


def test_get_health_check(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_health_check("test-health_check_id", region_name=REGION)
    mock_client.get_health_check.assert_called_once()


def test_get_health_check_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_health_check",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get health check"):
        get_health_check("test-health_check_id", region_name=REGION)


def test_get_health_check_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_count.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_health_check_count(region_name=REGION)
    mock_client.get_health_check_count.assert_called_once()


def test_get_health_check_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_health_check_count",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get health check count"):
        get_health_check_count(region_name=REGION)


def test_get_health_check_last_failure_reason(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_last_failure_reason.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_health_check_last_failure_reason("test-health_check_id", region_name=REGION)
    mock_client.get_health_check_last_failure_reason.assert_called_once()


def test_get_health_check_last_failure_reason_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_last_failure_reason.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_health_check_last_failure_reason",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get health check last failure reason"):
        get_health_check_last_failure_reason("test-health_check_id", region_name=REGION)


def test_get_health_check_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_status.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_health_check_status("test-health_check_id", region_name=REGION)
    mock_client.get_health_check_status.assert_called_once()


def test_get_health_check_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_health_check_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_health_check_status",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get health check status"):
        get_health_check_status("test-health_check_id", region_name=REGION)


def test_get_hosted_zone_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone_count.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_hosted_zone_count(region_name=REGION)
    mock_client.get_hosted_zone_count.assert_called_once()


def test_get_hosted_zone_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_hosted_zone_count",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get hosted zone count"):
        get_hosted_zone_count(region_name=REGION)


def test_get_hosted_zone_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone_limit.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_hosted_zone_limit("test-type_value", "test-hosted_zone_id", region_name=REGION)
    mock_client.get_hosted_zone_limit.assert_called_once()


def test_get_hosted_zone_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hosted_zone_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_hosted_zone_limit",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get hosted zone limit"):
        get_hosted_zone_limit("test-type_value", "test-hosted_zone_id", region_name=REGION)


def test_get_query_logging_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_logging_config.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_query_logging_config("test-id", region_name=REGION)
    mock_client.get_query_logging_config.assert_called_once()


def test_get_query_logging_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_logging_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_query_logging_config",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get query logging config"):
        get_query_logging_config("test-id", region_name=REGION)


def test_get_reusable_delegation_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reusable_delegation_set.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_reusable_delegation_set("test-id", region_name=REGION)
    mock_client.get_reusable_delegation_set.assert_called_once()


def test_get_reusable_delegation_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reusable_delegation_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reusable_delegation_set",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reusable delegation set"):
        get_reusable_delegation_set("test-id", region_name=REGION)


def test_get_reusable_delegation_set_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reusable_delegation_set_limit.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_reusable_delegation_set_limit("test-type_value", "test-delegation_set_id", region_name=REGION)
    mock_client.get_reusable_delegation_set_limit.assert_called_once()


def test_get_reusable_delegation_set_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reusable_delegation_set_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reusable_delegation_set_limit",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reusable delegation set limit"):
        get_reusable_delegation_set_limit("test-type_value", "test-delegation_set_id", region_name=REGION)


def test_get_traffic_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_traffic_policy("test-id", 1, region_name=REGION)
    mock_client.get_traffic_policy.assert_called_once()


def test_get_traffic_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_traffic_policy",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get traffic policy"):
        get_traffic_policy("test-id", 1, region_name=REGION)


def test_get_traffic_policy_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy_instance.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_traffic_policy_instance("test-id", region_name=REGION)
    mock_client.get_traffic_policy_instance.assert_called_once()


def test_get_traffic_policy_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_traffic_policy_instance",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get traffic policy instance"):
        get_traffic_policy_instance("test-id", region_name=REGION)


def test_get_traffic_policy_instance_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy_instance_count.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_traffic_policy_instance_count(region_name=REGION)
    mock_client.get_traffic_policy_instance_count.assert_called_once()


def test_get_traffic_policy_instance_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_policy_instance_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_traffic_policy_instance_count",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get traffic policy instance count"):
        get_traffic_policy_instance_count(region_name=REGION)


def test_list_cidr_blocks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_blocks.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_blocks("test-collection_id", region_name=REGION)
    mock_client.list_cidr_blocks.assert_called_once()


def test_list_cidr_blocks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_blocks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cidr_blocks",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cidr blocks"):
        list_cidr_blocks("test-collection_id", region_name=REGION)


def test_list_cidr_collections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_collections.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_collections(region_name=REGION)
    mock_client.list_cidr_collections.assert_called_once()


def test_list_cidr_collections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_collections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cidr_collections",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cidr collections"):
        list_cidr_collections(region_name=REGION)


def test_list_cidr_locations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_locations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_locations("test-collection_id", region_name=REGION)
    mock_client.list_cidr_locations.assert_called_once()


def test_list_cidr_locations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cidr_locations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cidr_locations",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cidr locations"):
        list_cidr_locations("test-collection_id", region_name=REGION)


def test_list_geo_locations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_geo_locations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_geo_locations(region_name=REGION)
    mock_client.list_geo_locations.assert_called_once()


def test_list_geo_locations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_geo_locations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_geo_locations",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list geo locations"):
        list_geo_locations(region_name=REGION)


def test_list_health_checks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_health_checks.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_health_checks(region_name=REGION)
    mock_client.list_health_checks.assert_called_once()


def test_list_health_checks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_health_checks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_health_checks",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list health checks"):
        list_health_checks(region_name=REGION)


def test_list_hosted_zones_by_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_name.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_hosted_zones_by_name(region_name=REGION)
    mock_client.list_hosted_zones_by_name.assert_called_once()


def test_list_hosted_zones_by_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_hosted_zones_by_name",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list hosted zones by name"):
        list_hosted_zones_by_name(region_name=REGION)


def test_list_hosted_zones_by_vpc(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_vpc.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", region_name=REGION)
    mock_client.list_hosted_zones_by_vpc.assert_called_once()


def test_list_hosted_zones_by_vpc_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_vpc.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_hosted_zones_by_vpc",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list hosted zones by vpc"):
        list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", region_name=REGION)


def test_list_query_logging_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_query_logging_configs.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_query_logging_configs(region_name=REGION)
    mock_client.list_query_logging_configs.assert_called_once()


def test_list_query_logging_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_query_logging_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_query_logging_configs",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list query logging configs"):
        list_query_logging_configs(region_name=REGION)


def test_list_resource_record_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_record_sets.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_resource_record_sets("test-hosted_zone_id", region_name=REGION)
    mock_client.list_resource_record_sets.assert_called_once()


def test_list_resource_record_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_record_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_record_sets",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource record sets"):
        list_resource_record_sets("test-hosted_zone_id", region_name=REGION)


def test_list_reusable_delegation_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reusable_delegation_sets.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_reusable_delegation_sets(region_name=REGION)
    mock_client.list_reusable_delegation_sets.assert_called_once()


def test_list_reusable_delegation_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_reusable_delegation_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reusable_delegation_sets",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list reusable delegation sets"):
        list_reusable_delegation_sets(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)


def test_list_tags_for_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resources.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resources("test-resource_type", [], region_name=REGION)
    mock_client.list_tags_for_resources.assert_called_once()


def test_list_tags_for_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resources",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resources"):
        list_tags_for_resources("test-resource_type", [], region_name=REGION)


def test_list_traffic_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policies.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policies(region_name=REGION)
    mock_client.list_traffic_policies.assert_called_once()


def test_list_traffic_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_policies",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic policies"):
        list_traffic_policies(region_name=REGION)


def test_list_traffic_policy_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances(region_name=REGION)
    mock_client.list_traffic_policy_instances.assert_called_once()


def test_list_traffic_policy_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_policy_instances",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic policy instances"):
        list_traffic_policy_instances(region_name=REGION)


def test_list_traffic_policy_instances_by_hosted_zone(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", region_name=REGION)
    mock_client.list_traffic_policy_instances_by_hosted_zone.assert_called_once()


def test_list_traffic_policy_instances_by_hosted_zone_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_hosted_zone.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_policy_instances_by_hosted_zone",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic policy instances by hosted zone"):
        list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", region_name=REGION)


def test_list_traffic_policy_instances_by_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances_by_policy("test-traffic_policy_id", 1, region_name=REGION)
    mock_client.list_traffic_policy_instances_by_policy.assert_called_once()


def test_list_traffic_policy_instances_by_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_policy_instances_by_policy",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic policy instances by policy"):
        list_traffic_policy_instances_by_policy("test-traffic_policy_id", 1, region_name=REGION)


def test_list_traffic_policy_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_versions.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_versions("test-id", region_name=REGION)
    mock_client.list_traffic_policy_versions.assert_called_once()


def test_list_traffic_policy_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_policy_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_policy_versions",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic policy versions"):
        list_traffic_policy_versions("test-id", region_name=REGION)


def test_list_vpc_association_authorizations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_association_authorizations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_vpc_association_authorizations("test-hosted_zone_id", region_name=REGION)
    mock_client.list_vpc_association_authorizations.assert_called_once()


def test_list_vpc_association_authorizations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_association_authorizations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_association_authorizations",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc association authorizations"):
        list_vpc_association_authorizations("test-hosted_zone_id", region_name=REGION)


def test_run_dns_answer(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_dns_answer.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", region_name=REGION)
    mock_client.test_dns_answer.assert_called_once()


def test_run_dns_answer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_dns_answer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_dns_answer",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run dns answer"):
        run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", region_name=REGION)


def test_update_health_check(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_health_check.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_health_check("test-health_check_id", region_name=REGION)
    mock_client.update_health_check.assert_called_once()


def test_update_health_check_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_health_check.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_health_check",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update health check"):
        update_health_check("test-health_check_id", region_name=REGION)


def test_update_hosted_zone_comment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hosted_zone_comment.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_hosted_zone_comment("test-id", region_name=REGION)
    mock_client.update_hosted_zone_comment.assert_called_once()


def test_update_hosted_zone_comment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hosted_zone_comment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_hosted_zone_comment",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update hosted zone comment"):
        update_hosted_zone_comment("test-id", region_name=REGION)


def test_update_traffic_policy_comment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_policy_comment.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_traffic_policy_comment("test-id", 1, "test-comment", region_name=REGION)
    mock_client.update_traffic_policy_comment.assert_called_once()


def test_update_traffic_policy_comment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_policy_comment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_traffic_policy_comment",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update traffic policy comment"):
        update_traffic_policy_comment("test-id", 1, "test-comment", region_name=REGION)


def test_update_traffic_policy_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_policy_instance.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_traffic_policy_instance("test-id", 1, "test-traffic_policy_id", 1, region_name=REGION)
    mock_client.update_traffic_policy_instance.assert_called_once()


def test_update_traffic_policy_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_policy_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_traffic_policy_instance",
    )
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update traffic policy instance"):
        update_traffic_policy_instance("test-id", 1, "test-traffic_policy_id", 1, region_name=REGION)


def test_associate_vpc_with_hosted_zone_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import associate_vpc_with_hosted_zone
    mock_client = MagicMock()
    mock_client.associate_vpc_with_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    associate_vpc_with_hosted_zone("test-hosted_zone_id", "test-vpc", comment="test-comment", region_name="us-east-1")
    mock_client.associate_vpc_with_hosted_zone.assert_called_once()

def test_change_cidr_collection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import change_cidr_collection
    mock_client = MagicMock()
    mock_client.change_cidr_collection.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    change_cidr_collection("test-id", "test-changes", collection_version="test-collection_version", region_name="us-east-1")
    mock_client.change_cidr_collection.assert_called_once()

def test_change_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import change_tags_for_resource
    mock_client = MagicMock()
    mock_client.change_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    change_tags_for_resource("test-resource_type", "test-resource_id", add_tags=[{"Key": "k", "Value": "v"}], remove_tag_keys="test-remove_tag_keys", region_name="us-east-1")
    mock_client.change_tags_for_resource.assert_called_once()

def test_create_hosted_zone_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import create_hosted_zone
    mock_client = MagicMock()
    mock_client.create_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_hosted_zone("test-name", "test-caller_reference", vpc="test-vpc", hosted_zone_config={}, delegation_set_id="test-delegation_set_id", region_name="us-east-1")
    mock_client.create_hosted_zone.assert_called_once()

def test_create_reusable_delegation_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import create_reusable_delegation_set
    mock_client = MagicMock()
    mock_client.create_reusable_delegation_set.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_reusable_delegation_set("test-caller_reference", hosted_zone_id="test-hosted_zone_id", region_name="us-east-1")
    mock_client.create_reusable_delegation_set.assert_called_once()

def test_create_traffic_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import create_traffic_policy
    mock_client = MagicMock()
    mock_client.create_traffic_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_traffic_policy("test-name", "test-document", comment="test-comment", region_name="us-east-1")
    mock_client.create_traffic_policy.assert_called_once()

def test_create_traffic_policy_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import create_traffic_policy_version
    mock_client = MagicMock()
    mock_client.create_traffic_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    create_traffic_policy_version("test-id", "test-document", comment="test-comment", region_name="us-east-1")
    mock_client.create_traffic_policy_version.assert_called_once()

def test_disassociate_vpc_from_hosted_zone_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import disassociate_vpc_from_hosted_zone
    mock_client = MagicMock()
    mock_client.disassociate_vpc_from_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    disassociate_vpc_from_hosted_zone("test-hosted_zone_id", "test-vpc", comment="test-comment", region_name="us-east-1")
    mock_client.disassociate_vpc_from_hosted_zone.assert_called_once()

def test_get_geo_location_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import get_geo_location
    mock_client = MagicMock()
    mock_client.get_geo_location.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    get_geo_location(continent_code="test-continent_code", country_code=1, subdivision_code="test-subdivision_code", region_name="us-east-1")
    mock_client.get_geo_location.assert_called_once()

def test_list_cidr_blocks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_cidr_blocks
    mock_client = MagicMock()
    mock_client.list_cidr_blocks.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_blocks("test-collection_id", location_name="test-location_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cidr_blocks.assert_called_once()

def test_list_cidr_collections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_cidr_collections
    mock_client = MagicMock()
    mock_client.list_cidr_collections.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_collections(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cidr_collections.assert_called_once()

def test_list_cidr_locations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_cidr_locations
    mock_client = MagicMock()
    mock_client.list_cidr_locations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_cidr_locations("test-collection_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_cidr_locations.assert_called_once()

def test_list_geo_locations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_geo_locations
    mock_client = MagicMock()
    mock_client.list_geo_locations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_geo_locations(start_continent_code="test-start_continent_code", start_country_code=1, start_subdivision_code="test-start_subdivision_code", max_items=1, region_name="us-east-1")
    mock_client.list_geo_locations.assert_called_once()

def test_list_health_checks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_health_checks
    mock_client = MagicMock()
    mock_client.list_health_checks.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_health_checks(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_health_checks.assert_called_once()

def test_list_hosted_zones_by_name_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_hosted_zones_by_name
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_name.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_hosted_zones_by_name(dns_name="test-dns_name", hosted_zone_id="test-hosted_zone_id", max_items=1, region_name="us-east-1")
    mock_client.list_hosted_zones_by_name.assert_called_once()

def test_list_hosted_zones_by_vpc_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_hosted_zones_by_vpc
    mock_client = MagicMock()
    mock_client.list_hosted_zones_by_vpc.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", max_items=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_hosted_zones_by_vpc.assert_called_once()

def test_list_query_logging_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_query_logging_configs
    mock_client = MagicMock()
    mock_client.list_query_logging_configs.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_query_logging_configs(hosted_zone_id="test-hosted_zone_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_query_logging_configs.assert_called_once()

def test_list_resource_record_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_resource_record_sets
    mock_client = MagicMock()
    mock_client.list_resource_record_sets.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_resource_record_sets("test-hosted_zone_id", start_record_name="test-start_record_name", start_record_type="test-start_record_type", start_record_identifier="test-start_record_identifier", max_items=1, region_name="us-east-1")
    mock_client.list_resource_record_sets.assert_called_once()

def test_list_reusable_delegation_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_reusable_delegation_sets
    mock_client = MagicMock()
    mock_client.list_reusable_delegation_sets.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_reusable_delegation_sets(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_reusable_delegation_sets.assert_called_once()

def test_list_traffic_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_traffic_policies
    mock_client = MagicMock()
    mock_client.list_traffic_policies.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policies(traffic_policy_id_marker="test-traffic_policy_id_marker", max_items=1, region_name="us-east-1")
    mock_client.list_traffic_policies.assert_called_once()

def test_list_traffic_policy_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_traffic_policy_instances
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances(hosted_zone_id_marker="test-hosted_zone_id_marker", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.list_traffic_policy_instances.assert_called_once()

def test_list_traffic_policy_instances_by_hosted_zone_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_traffic_policy_instances_by_hosted_zone
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_hosted_zone.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.list_traffic_policy_instances_by_hosted_zone.assert_called_once()

def test_list_traffic_policy_instances_by_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_traffic_policy_instances_by_policy
    mock_client = MagicMock()
    mock_client.list_traffic_policy_instances_by_policy.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_instances_by_policy("test-traffic_policy_id", "test-traffic_policy_version", hosted_zone_id_marker="test-hosted_zone_id_marker", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.list_traffic_policy_instances_by_policy.assert_called_once()

def test_list_traffic_policy_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_traffic_policy_versions
    mock_client = MagicMock()
    mock_client.list_traffic_policy_versions.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_traffic_policy_versions("test-id", traffic_policy_version_marker="test-traffic_policy_version_marker", max_items=1, region_name="us-east-1")
    mock_client.list_traffic_policy_versions.assert_called_once()

def test_list_vpc_association_authorizations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import list_vpc_association_authorizations
    mock_client = MagicMock()
    mock_client.list_vpc_association_authorizations.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    list_vpc_association_authorizations("test-hosted_zone_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_vpc_association_authorizations.assert_called_once()

def test_run_dns_answer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import run_dns_answer
    mock_client = MagicMock()
    mock_client.test_dns_answer.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", resolver_ip="test-resolver_ip", edns0_client_subnet_ip="test-edns0_client_subnet_ip", edns0_client_subnet_mask="test-edns0_client_subnet_mask", region_name="us-east-1")
    mock_client.test_dns_answer.assert_called_once()

def test_update_health_check_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import update_health_check
    mock_client = MagicMock()
    mock_client.update_health_check.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_health_check("test-health_check_id", health_check_version="test-health_check_version", ip_address="test-ip_address", port=1, resource_path="test-resource_path", fully_qualified_domain_name="test-fully_qualified_domain_name", search_string="test-search_string", failure_threshold="test-failure_threshold", inverted="test-inverted", disabled=True, health_threshold="test-health_threshold", child_health_checks="test-child_health_checks", enable_sni=True, regions="test-regions", alarm_identifier="test-alarm_identifier", insufficient_data_health_status="test-insufficient_data_health_status", reset_elements="test-reset_elements", region_name="us-east-1")
    mock_client.update_health_check.assert_called_once()

def test_update_hosted_zone_comment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.route53 import update_hosted_zone_comment
    mock_client = MagicMock()
    mock_client.update_hosted_zone_comment.return_value = {}
    monkeypatch.setattr("aws_util.route53.get_client", lambda *a, **kw: mock_client)
    update_hosted_zone_comment("test-id", comment="test-comment", region_name="us-east-1")
    mock_client.update_hosted_zone_comment.assert_called_once()
