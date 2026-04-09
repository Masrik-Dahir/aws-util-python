"""Tests for aws_util.aio.route53 -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.route53 import (
    HostedZone,
    ResourceRecord,
    bulk_upsert_records,
    delete_record,
    get_hosted_zone,
    list_hosted_zones,
    list_records,
    upsert_record,
    wait_for_change,
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# list_hosted_zones
# ---------------------------------------------------------------------------


async def test_list_hosted_zones_ok(monkeypatch):
    resp = {
        "HostedZones": [
            {
                "Id": "/hostedzone/Z1",
                "Name": "example.com.",
                "Config": {"PrivateZone": False, "Comment": "main"},
                "ResourceRecordSetCount": 5,
            }
        ],
        "IsTruncated": False,
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_hosted_zones()
    assert len(result) == 1
    z = result[0]
    assert isinstance(z, HostedZone)
    assert z.zone_id == "Z1"
    assert z.name == "example.com."
    assert z.private_zone is False
    assert z.record_count == 5
    assert z.comment == "main"


async def test_list_hosted_zones_pagination(monkeypatch):
    page1 = {
        "HostedZones": [
            {
                "Id": "/hostedzone/Z1",
                "Name": "a.com.",
                "Config": {},
            }
        ],
        "IsTruncated": True,
        "NextMarker": "tok",
    }
    page2 = {
        "HostedZones": [
            {
                "Id": "/hostedzone/Z2",
                "Name": "b.com.",
                "Config": {},
            }
        ],
        "IsTruncated": False,
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_hosted_zones()
    assert len(result) == 2


async def test_list_hosted_zones_no_comment(monkeypatch):
    resp = {
        "HostedZones": [
            {
                "Id": "/hostedzone/Z1",
                "Name": "x.com.",
                "Config": {"Comment": ""},
            }
        ],
        "IsTruncated": False,
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_hosted_zones()
    assert result[0].comment is None


async def test_list_hosted_zones_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await list_hosted_zones()


async def test_list_hosted_zones_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_hosted_zones failed"):
        await list_hosted_zones()


# ---------------------------------------------------------------------------
# get_hosted_zone
# ---------------------------------------------------------------------------


async def test_get_hosted_zone_found(monkeypatch):
    resp = {
        "HostedZone": {
            "Id": "/hostedzone/Z1",
            "Name": "example.com.",
            "Config": {"PrivateZone": True, "Comment": "note"},
            "ResourceRecordSetCount": 3,
        }
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await get_hosted_zone("Z1")
    assert result is not None
    assert result.zone_id == "Z1"
    assert result.private_zone is True


async def test_get_hosted_zone_not_found(monkeypatch):
    mc = _mc(se=RuntimeError("NoSuchHostedZone"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await get_hosted_zone("Z999")
    assert result is None


async def test_get_hosted_zone_other_error(monkeypatch):
    mc = _mc(se=RuntimeError("access denied"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="access denied"):
        await get_hosted_zone("Z1")


# ---------------------------------------------------------------------------
# list_records
# ---------------------------------------------------------------------------


async def test_list_records_ok(monkeypatch):
    resp = {
        "ResourceRecordSets": [
            {
                "Name": "api.example.com.",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [{"Value": "1.2.3.4"}],
            },
            {
                "Name": "cdn.example.com.",
                "Type": "CNAME",
                "AliasTarget": {
                    "DNSName": "d123.cloudfront.net.",
                    "HostedZoneId": "Z2F",
                },
            },
        ],
        "IsTruncated": False,
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_records("Z1")
    assert len(result) == 2
    assert result[0].values == ["1.2.3.4"]
    assert result[0].alias_dns_name is None
    assert result[1].alias_dns_name == "d123.cloudfront.net."
    assert result[1].alias_hosted_zone_id == "Z2F"


async def test_list_records_pagination(monkeypatch):
    page1 = {
        "ResourceRecordSets": [
            {
                "Name": "a.example.com.",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [{"Value": "1.1.1.1"}],
            }
        ],
        "IsTruncated": True,
        "NextRecordName": "b.example.com.",
        "NextRecordType": "A",
    }
    page2 = {
        "ResourceRecordSets": [
            {
                "Name": "b.example.com.",
                "Type": "A",
                "TTL": 300,
                "ResourceRecords": [{"Value": "2.2.2.2"}],
            }
        ],
        "IsTruncated": False,
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_records("Z1")
    assert len(result) == 2


async def test_list_records_empty_alias(monkeypatch):
    resp = {
        "ResourceRecordSets": [
            {
                "Name": "x.com.",
                "Type": "A",
                "AliasTarget": {"DNSName": "", "HostedZoneId": ""},
            }
        ],
        "IsTruncated": False,
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    result = await list_records("Z1")
    assert result[0].alias_dns_name is None
    assert result[0].alias_hosted_zone_id is None


async def test_list_records_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await list_records("Z1")


async def test_list_records_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_records failed"):
        await list_records("Z1")


# ---------------------------------------------------------------------------
# upsert_record
# ---------------------------------------------------------------------------


async def test_upsert_record_ok(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C1"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    cid = await upsert_record("Z1", "api.example.com", "A", ["1.2.3.4"])
    assert cid == "/change/C1"


async def test_upsert_record_trailing_dot(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C2"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    cid = await upsert_record("Z1", "api.example.com.", "A", ["1.2.3.4"])
    assert cid == "/change/C2"


async def test_upsert_record_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await upsert_record("Z1", "api.example.com", "A", ["1.2.3.4"])


async def test_upsert_record_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to upsert"):
        await upsert_record("Z1", "api.example.com", "A", ["1.2.3.4"])


# ---------------------------------------------------------------------------
# delete_record
# ---------------------------------------------------------------------------


async def test_delete_record_ok(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C3"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    cid = await delete_record("Z1", "api.example.com", "A", ["1.2.3.4"])
    assert cid == "/change/C3"


async def test_delete_record_trailing_dot(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C4"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    cid = await delete_record("Z1", "api.example.com.", "A", ["1.2.3.4"])
    assert cid == "/change/C4"


async def test_delete_record_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await delete_record("Z1", "api.example.com", "A", ["1.2.3.4"])


async def test_delete_record_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to delete"):
        await delete_record("Z1", "api.example.com", "A", ["1.2.3.4"])


# ---------------------------------------------------------------------------
# wait_for_change
# ---------------------------------------------------------------------------


async def test_wait_for_change_immediate(monkeypatch):
    mc = _mc({"ChangeInfo": {"Status": "INSYNC"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.route53.asyncio.sleep", AsyncMock())
    result = await wait_for_change("/change/C1")
    assert result == "INSYNC"


async def test_wait_for_change_normalise_id(monkeypatch):
    mc = _mc({"ChangeInfo": {"Status": "INSYNC"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.route53.asyncio.sleep", AsyncMock())
    result = await wait_for_change("C1")
    assert result == "INSYNC"
    # Verify the normalised ID was used
    kw = mc.call.call_args[1]
    assert kw["Id"] == "/change/C1"


async def test_wait_for_change_timeout(monkeypatch):
    mc = _mc({"ChangeInfo": {"Status": "PENDING"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.route53.asyncio.sleep", AsyncMock())

    import time

    _real = time.monotonic
    values = [0.0, 0.0, 500.0]
    _idx = 0

    def _fake():
        nonlocal _idx
        if _idx < len(values):
            v = values[_idx]
            _idx += 1
            return v
        return _real()

    monkeypatch.setattr(time, "monotonic", _fake)

    with pytest.raises(TimeoutError, match="did not reach INSYNC"):
        await wait_for_change("/change/C1", timeout=300.0)


async def test_wait_for_change_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.route53.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="boom"):
        await wait_for_change("/change/C1")


async def test_wait_for_change_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.route53.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="wait_for_change failed"):
        await wait_for_change("/change/C1")


# ---------------------------------------------------------------------------
# bulk_upsert_records
# ---------------------------------------------------------------------------


async def test_bulk_upsert_records_ok(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C5"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    records = [
        {"name": "a.example.com", "record_type": "A", "values": ["1.1.1.1"]},
        {"name": "b.example.com.", "record_type": "CNAME", "values": ["c.com."], "ttl": 600},
    ]
    cid = await bulk_upsert_records("Z1", records)
    assert cid == "/change/C5"

    # Verify the change batch was built correctly
    kw = mc.call.call_args[1]
    changes = kw["ChangeBatch"]["Changes"]
    assert len(changes) == 2
    # First record should have dot added
    assert changes[0]["ResourceRecordSet"]["Name"] == "a.example.com."
    # Second already has dot
    assert changes[1]["ResourceRecordSet"]["Name"] == "b.example.com."
    assert changes[1]["ResourceRecordSet"]["TTL"] == 600


async def test_bulk_upsert_records_default_ttl(monkeypatch):
    mc = _mc({"ChangeInfo": {"Id": "/change/C6"}})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    records = [
        {"name": "a.example.com", "record_type": "A", "values": ["1.1.1.1"]},
    ]
    await bulk_upsert_records("Z1", records)
    kw = mc.call.call_args[1]
    assert kw["ChangeBatch"]["Changes"][0]["ResourceRecordSet"]["TTL"] == 300


async def test_bulk_upsert_records_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await bulk_upsert_records("Z1", [{"name": "a.com", "record_type": "A", "values": ["1.1.1.1"]}])


async def test_bulk_upsert_records_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="bulk_upsert_records failed"):
        await bulk_upsert_records("Z1", [{"name": "a.com", "record_type": "A", "values": ["1.1.1.1"]}])


async def test_activate_key_signing_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await activate_key_signing_key("test-hosted_zone_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_activate_key_signing_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await activate_key_signing_key("test-hosted_zone_id", "test-name", )


async def test_associate_vpc_with_hosted_zone(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_vpc_with_hosted_zone("test-hosted_zone_id", {}, )
    mock_client.call.assert_called_once()


async def test_associate_vpc_with_hosted_zone_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_vpc_with_hosted_zone("test-hosted_zone_id", {}, )


async def test_change_cidr_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await change_cidr_collection("test-id", [], )
    mock_client.call.assert_called_once()


async def test_change_cidr_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await change_cidr_collection("test-id", [], )


async def test_change_resource_record_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await change_resource_record_sets("test-hosted_zone_id", {}, )
    mock_client.call.assert_called_once()


async def test_change_resource_record_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await change_resource_record_sets("test-hosted_zone_id", {}, )


async def test_change_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await change_tags_for_resource("test-resource_type", "test-resource_id", )
    mock_client.call.assert_called_once()


async def test_change_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await change_tags_for_resource("test-resource_type", "test-resource_id", )


async def test_create_cidr_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cidr_collection("test-name", "test-caller_reference", )
    mock_client.call.assert_called_once()


async def test_create_cidr_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cidr_collection("test-name", "test-caller_reference", )


async def test_create_health_check(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_health_check("test-caller_reference", {}, )
    mock_client.call.assert_called_once()


async def test_create_health_check_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_health_check("test-caller_reference", {}, )


async def test_create_hosted_zone(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_hosted_zone("test-name", "test-caller_reference", )
    mock_client.call.assert_called_once()


async def test_create_hosted_zone_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_hosted_zone("test-name", "test-caller_reference", )


async def test_create_key_signing_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_key_signing_key("test-caller_reference", "test-hosted_zone_id", "test-key_management_service_arn", "test-name", "test-status", )
    mock_client.call.assert_called_once()


async def test_create_key_signing_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_key_signing_key("test-caller_reference", "test-hosted_zone_id", "test-key_management_service_arn", "test-name", "test-status", )


async def test_create_query_logging_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_query_logging_config("test-hosted_zone_id", "test-cloud_watch_logs_log_group_arn", )
    mock_client.call.assert_called_once()


async def test_create_query_logging_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_query_logging_config("test-hosted_zone_id", "test-cloud_watch_logs_log_group_arn", )


async def test_create_reusable_delegation_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_reusable_delegation_set("test-caller_reference", )
    mock_client.call.assert_called_once()


async def test_create_reusable_delegation_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_reusable_delegation_set("test-caller_reference", )


async def test_create_traffic_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_policy("test-name", "test-document", )
    mock_client.call.assert_called_once()


async def test_create_traffic_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_policy("test-name", "test-document", )


async def test_create_traffic_policy_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_policy_instance("test-hosted_zone_id", "test-name", 1, "test-traffic_policy_id", 1, )
    mock_client.call.assert_called_once()


async def test_create_traffic_policy_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_policy_instance("test-hosted_zone_id", "test-name", 1, "test-traffic_policy_id", 1, )


async def test_create_traffic_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_policy_version("test-id", "test-document", )
    mock_client.call.assert_called_once()


async def test_create_traffic_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_policy_version("test-id", "test-document", )


async def test_create_vpc_association_authorization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_association_authorization("test-hosted_zone_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_vpc_association_authorization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_association_authorization("test-hosted_zone_id", {}, )


async def test_deactivate_key_signing_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_key_signing_key("test-hosted_zone_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_deactivate_key_signing_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_key_signing_key("test-hosted_zone_id", "test-name", )


async def test_delete_cidr_collection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cidr_collection("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_cidr_collection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cidr_collection("test-id", )


async def test_delete_health_check(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_health_check("test-health_check_id", )
    mock_client.call.assert_called_once()


async def test_delete_health_check_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_health_check("test-health_check_id", )


async def test_delete_hosted_zone(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_hosted_zone("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_hosted_zone_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_hosted_zone("test-id", )


async def test_delete_key_signing_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_key_signing_key("test-hosted_zone_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_delete_key_signing_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_key_signing_key("test-hosted_zone_id", "test-name", )


async def test_delete_query_logging_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_query_logging_config("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_query_logging_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_query_logging_config("test-id", )


async def test_delete_reusable_delegation_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_reusable_delegation_set("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_reusable_delegation_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_reusable_delegation_set("test-id", )


async def test_delete_traffic_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_policy("test-id", 1, )
    mock_client.call.assert_called_once()


async def test_delete_traffic_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_policy("test-id", 1, )


async def test_delete_traffic_policy_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_policy_instance("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_policy_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_policy_instance("test-id", )


async def test_delete_vpc_association_authorization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_association_authorization("test-hosted_zone_id", {}, )
    mock_client.call.assert_called_once()


async def test_delete_vpc_association_authorization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_association_authorization("test-hosted_zone_id", {}, )


async def test_disable_hosted_zone_dnssec(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_hosted_zone_dnssec("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_disable_hosted_zone_dnssec_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_hosted_zone_dnssec("test-hosted_zone_id", )


async def test_disassociate_vpc_from_hosted_zone(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_vpc_from_hosted_zone("test-hosted_zone_id", {}, )
    mock_client.call.assert_called_once()


async def test_disassociate_vpc_from_hosted_zone_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_vpc_from_hosted_zone("test-hosted_zone_id", {}, )


async def test_enable_hosted_zone_dnssec(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_hosted_zone_dnssec("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_enable_hosted_zone_dnssec_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_hosted_zone_dnssec("test-hosted_zone_id", )


async def test_get_account_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_limit("test-type_value", )
    mock_client.call.assert_called_once()


async def test_get_account_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_limit("test-type_value", )


async def test_get_change(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_change("test-id", )
    mock_client.call.assert_called_once()


async def test_get_change_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_change("test-id", )


async def test_get_checker_ip_ranges(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_checker_ip_ranges()
    mock_client.call.assert_called_once()


async def test_get_checker_ip_ranges_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_checker_ip_ranges()


async def test_get_dnssec(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dnssec("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_get_dnssec_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dnssec("test-hosted_zone_id", )


async def test_get_geo_location(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_geo_location()
    mock_client.call.assert_called_once()


async def test_get_geo_location_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_geo_location()


async def test_get_health_check(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_health_check("test-health_check_id", )
    mock_client.call.assert_called_once()


async def test_get_health_check_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_health_check("test-health_check_id", )


async def test_get_health_check_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_health_check_count()
    mock_client.call.assert_called_once()


async def test_get_health_check_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_health_check_count()


async def test_get_health_check_last_failure_reason(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_health_check_last_failure_reason("test-health_check_id", )
    mock_client.call.assert_called_once()


async def test_get_health_check_last_failure_reason_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_health_check_last_failure_reason("test-health_check_id", )


async def test_get_health_check_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_health_check_status("test-health_check_id", )
    mock_client.call.assert_called_once()


async def test_get_health_check_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_health_check_status("test-health_check_id", )


async def test_get_hosted_zone_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_hosted_zone_count()
    mock_client.call.assert_called_once()


async def test_get_hosted_zone_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_hosted_zone_count()


async def test_get_hosted_zone_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_hosted_zone_limit("test-type_value", "test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_get_hosted_zone_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_hosted_zone_limit("test-type_value", "test-hosted_zone_id", )


async def test_get_query_logging_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_query_logging_config("test-id", )
    mock_client.call.assert_called_once()


async def test_get_query_logging_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_query_logging_config("test-id", )


async def test_get_reusable_delegation_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reusable_delegation_set("test-id", )
    mock_client.call.assert_called_once()


async def test_get_reusable_delegation_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reusable_delegation_set("test-id", )


async def test_get_reusable_delegation_set_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_reusable_delegation_set_limit("test-type_value", "test-delegation_set_id", )
    mock_client.call.assert_called_once()


async def test_get_reusable_delegation_set_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_reusable_delegation_set_limit("test-type_value", "test-delegation_set_id", )


async def test_get_traffic_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_traffic_policy("test-id", 1, )
    mock_client.call.assert_called_once()


async def test_get_traffic_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_traffic_policy("test-id", 1, )


async def test_get_traffic_policy_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_traffic_policy_instance("test-id", )
    mock_client.call.assert_called_once()


async def test_get_traffic_policy_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_traffic_policy_instance("test-id", )


async def test_get_traffic_policy_instance_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_traffic_policy_instance_count()
    mock_client.call.assert_called_once()


async def test_get_traffic_policy_instance_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_traffic_policy_instance_count()


async def test_list_cidr_blocks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cidr_blocks("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_list_cidr_blocks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cidr_blocks("test-collection_id", )


async def test_list_cidr_collections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cidr_collections()
    mock_client.call.assert_called_once()


async def test_list_cidr_collections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cidr_collections()


async def test_list_cidr_locations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cidr_locations("test-collection_id", )
    mock_client.call.assert_called_once()


async def test_list_cidr_locations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cidr_locations("test-collection_id", )


async def test_list_geo_locations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_geo_locations()
    mock_client.call.assert_called_once()


async def test_list_geo_locations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_geo_locations()


async def test_list_health_checks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_health_checks()
    mock_client.call.assert_called_once()


async def test_list_health_checks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_health_checks()


async def test_list_hosted_zones_by_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_hosted_zones_by_name()
    mock_client.call.assert_called_once()


async def test_list_hosted_zones_by_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_hosted_zones_by_name()


async def test_list_hosted_zones_by_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", )
    mock_client.call.assert_called_once()


async def test_list_hosted_zones_by_vpc_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", )


async def test_list_query_logging_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_query_logging_configs()
    mock_client.call.assert_called_once()


async def test_list_query_logging_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_query_logging_configs()


async def test_list_resource_record_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_record_sets("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_list_resource_record_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_record_sets("test-hosted_zone_id", )


async def test_list_reusable_delegation_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_reusable_delegation_sets()
    mock_client.call.assert_called_once()


async def test_list_reusable_delegation_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_reusable_delegation_sets()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_type", "test-resource_id", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_type", "test-resource_id", )


async def test_list_tags_for_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resources("test-resource_type", [], )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resources("test-resource_type", [], )


async def test_list_traffic_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_policies()
    mock_client.call.assert_called_once()


async def test_list_traffic_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_policies()


async def test_list_traffic_policy_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_policy_instances()
    mock_client.call.assert_called_once()


async def test_list_traffic_policy_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_policy_instances()


async def test_list_traffic_policy_instances_by_hosted_zone(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_list_traffic_policy_instances_by_hosted_zone_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", )


async def test_list_traffic_policy_instances_by_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_policy_instances_by_policy("test-traffic_policy_id", 1, )
    mock_client.call.assert_called_once()


async def test_list_traffic_policy_instances_by_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_policy_instances_by_policy("test-traffic_policy_id", 1, )


async def test_list_traffic_policy_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_policy_versions("test-id", )
    mock_client.call.assert_called_once()


async def test_list_traffic_policy_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_policy_versions("test-id", )


async def test_list_vpc_association_authorizations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vpc_association_authorizations("test-hosted_zone_id", )
    mock_client.call.assert_called_once()


async def test_list_vpc_association_authorizations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_association_authorizations("test-hosted_zone_id", )


async def test_run_dns_answer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", )
    mock_client.call.assert_called_once()


async def test_run_dns_answer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", )


async def test_update_health_check(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_health_check("test-health_check_id", )
    mock_client.call.assert_called_once()


async def test_update_health_check_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_health_check("test-health_check_id", )


async def test_update_hosted_zone_comment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_hosted_zone_comment("test-id", )
    mock_client.call.assert_called_once()


async def test_update_hosted_zone_comment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_hosted_zone_comment("test-id", )


async def test_update_traffic_policy_comment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_traffic_policy_comment("test-id", 1, "test-comment", )
    mock_client.call.assert_called_once()


async def test_update_traffic_policy_comment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_traffic_policy_comment("test-id", 1, "test-comment", )


async def test_update_traffic_policy_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_traffic_policy_instance("test-id", 1, "test-traffic_policy_id", 1, )
    mock_client.call.assert_called_once()


async def test_update_traffic_policy_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.route53.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_traffic_policy_instance("test-id", 1, "test-traffic_policy_id", 1, )


@pytest.mark.asyncio
async def test_associate_vpc_with_hosted_zone_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import associate_vpc_with_hosted_zone
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await associate_vpc_with_hosted_zone("test-hosted_zone_id", "test-vpc", comment="test-comment", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_change_cidr_collection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import change_cidr_collection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await change_cidr_collection("test-id", "test-changes", collection_version="test-collection_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_change_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import change_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await change_tags_for_resource("test-resource_type", "test-resource_id", add_tags=[{"Key": "k", "Value": "v"}], remove_tag_keys="test-remove_tag_keys", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_hosted_zone_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import create_hosted_zone
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await create_hosted_zone("test-name", "test-caller_reference", vpc="test-vpc", hosted_zone_config={}, delegation_set_id="test-delegation_set_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_reusable_delegation_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import create_reusable_delegation_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await create_reusable_delegation_set("test-caller_reference", hosted_zone_id="test-hosted_zone_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import create_traffic_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await create_traffic_policy("test-name", "test-document", comment="test-comment", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_policy_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import create_traffic_policy_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await create_traffic_policy_version("test-id", "test-document", comment="test-comment", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_vpc_from_hosted_zone_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import disassociate_vpc_from_hosted_zone
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await disassociate_vpc_from_hosted_zone("test-hosted_zone_id", "test-vpc", comment="test-comment", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_geo_location_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import get_geo_location
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await get_geo_location(continent_code="test-continent_code", country_code=1, subdivision_code="test-subdivision_code", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cidr_blocks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_cidr_blocks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_cidr_blocks("test-collection_id", location_name="test-location_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cidr_collections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_cidr_collections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_cidr_collections(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cidr_locations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_cidr_locations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_cidr_locations("test-collection_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_geo_locations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_geo_locations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_geo_locations(start_continent_code="test-start_continent_code", start_country_code=1, start_subdivision_code="test-start_subdivision_code", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_health_checks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_health_checks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_health_checks(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_hosted_zones_by_name_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_hosted_zones_by_name
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_hosted_zones_by_name(dns_name="test-dns_name", hosted_zone_id="test-hosted_zone_id", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_hosted_zones_by_vpc_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_hosted_zones_by_vpc
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_hosted_zones_by_vpc("test-vpc_id", "test-vpc_region", max_items=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_query_logging_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_query_logging_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_query_logging_configs(hosted_zone_id="test-hosted_zone_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_record_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_resource_record_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_resource_record_sets("test-hosted_zone_id", start_record_name="test-start_record_name", start_record_type="test-start_record_type", start_record_identifier="test-start_record_identifier", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reusable_delegation_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_reusable_delegation_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_reusable_delegation_sets(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_traffic_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_traffic_policies(traffic_policy_id_marker="test-traffic_policy_id_marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_policy_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_traffic_policy_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_traffic_policy_instances(hosted_zone_id_marker="test-hosted_zone_id_marker", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_policy_instances_by_hosted_zone_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_traffic_policy_instances_by_hosted_zone
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_traffic_policy_instances_by_hosted_zone("test-hosted_zone_id", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_policy_instances_by_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_traffic_policy_instances_by_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_traffic_policy_instances_by_policy("test-traffic_policy_id", "test-traffic_policy_version", hosted_zone_id_marker="test-hosted_zone_id_marker", traffic_policy_instance_name_marker="test-traffic_policy_instance_name_marker", traffic_policy_instance_type_marker="test-traffic_policy_instance_type_marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_policy_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_traffic_policy_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_traffic_policy_versions("test-id", traffic_policy_version_marker="test-traffic_policy_version_marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_association_authorizations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import list_vpc_association_authorizations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await list_vpc_association_authorizations("test-hosted_zone_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_dns_answer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import run_dns_answer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await run_dns_answer("test-hosted_zone_id", "test-record_name", "test-record_type", resolver_ip="test-resolver_ip", edns0_client_subnet_ip="test-edns0_client_subnet_ip", edns0_client_subnet_mask="test-edns0_client_subnet_mask", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_health_check_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import update_health_check
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await update_health_check("test-health_check_id", health_check_version="test-health_check_version", ip_address="test-ip_address", port=1, resource_path="test-resource_path", fully_qualified_domain_name="test-fully_qualified_domain_name", search_string="test-search_string", failure_threshold="test-failure_threshold", inverted="test-inverted", disabled=True, health_threshold="test-health_threshold", child_health_checks="test-child_health_checks", enable_sni=True, regions="test-regions", alarm_identifier="test-alarm_identifier", insufficient_data_health_status="test-insufficient_data_health_status", reset_elements="test-reset_elements", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_hosted_zone_comment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.route53 import update_hosted_zone_comment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.route53.async_client", lambda *a, **kw: mock_client)
    await update_hosted_zone_comment("test-id", comment="test-comment", region_name="us-east-1")
    mock_client.call.assert_called_once()
