

"""Tests for aws_util.aio.service_quotas -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.service_quotas as mod
from aws_util.aio.service_quotas import (

    list_requested_service_quota_changes,
    list_aws_default_service_quotas,
    list_requested_service_quota_change_history,
    list_requested_service_quota_change_history_by_quota,
    list_service_quota_increase_requests_in_template,
    start_auto_management,
    update_auto_management,
    associate_service_quota_template,
    create_support_case,
    delete_service_quota_increase_request_from_template,
    disassociate_service_quota_template,
    get_association_for_service_quota_template,
    get_auto_management_configuration,
    get_service_quota_increase_request_from_template,
    list_tags_for_resource,
    put_service_quota_increase_request_into_template,
    stop_auto_management,
    tag_resource,
    untag_resource,
)



REGION = "us-east-1"
_SVC = {"ServiceCode": "ec2", "ServiceName": "Amazon EC2"}
_QUOTA = {"ServiceCode": "ec2", "QuotaCode": "L-1234", "Value": 100.0}
_CHANGE = {"Id": "ch-1", "ServiceCode": "ec2", "QuotaCode": "L-1234",
           "Status": "PENDING", "DesiredValue": 200.0}


@pytest.fixture()
def mc(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: client)
    return client


async def test_list_services_success(mc):
    mc.call.return_value = {"Services": [_SVC]}
    r = await mod.list_services()
    assert len(r) == 1


async def test_list_services_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_services()


async def test_list_services_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_services failed"):
        await mod.list_services()


async def test_list_service_quotas_success(mc):
    mc.call.return_value = {"Quotas": [_QUOTA]}
    r = await mod.list_service_quotas("ec2")
    assert len(r) == 1


async def test_list_service_quotas_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_service_quotas("ec2")


async def test_list_service_quotas_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_service_quotas failed"):
        await mod.list_service_quotas("ec2")


async def test_get_service_quota_success(mc):
    mc.call.return_value = {"Quota": _QUOTA}
    r = await mod.get_service_quota("ec2", "L-1234")
    assert r.quota_code == "L-1234"


async def test_get_service_quota_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_service_quota("ec2", "L-1234")


async def test_get_service_quota_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_service_quota failed"):
        await mod.get_service_quota("ec2", "L-1234")


async def test_get_aws_default_success(mc):
    mc.call.return_value = {"Quota": _QUOTA}
    r = await mod.get_aws_default_service_quota("ec2", "L-1234")
    assert r.quota_code == "L-1234"


async def test_get_aws_default_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_aws_default_service_quota("ec2", "L-1234")


async def test_get_aws_default_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_aws_default_service_quota failed"):
        await mod.get_aws_default_service_quota("ec2", "L-1234")


async def test_request_increase_success(mc):
    mc.call.return_value = {"RequestedQuota": _CHANGE}
    r = await mod.request_service_quota_increase("ec2", "L-1234", 200.0)
    assert r.id == "ch-1"


async def test_request_increase_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.request_service_quota_increase("ec2", "L-1234", 200.0)


async def test_request_increase_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="request_service_quota_increase failed"):
        await mod.request_service_quota_increase("ec2", "L-1234", 200.0)


async def test_list_requested_changes_success(mc):
    mc.call.return_value = {"RequestedQuotas": [_CHANGE]}
    r = await mod.list_requested_service_quota_changes()
    assert len(r) == 1


async def test_list_requested_changes_filters(mc):
    mc.call.return_value = {"RequestedQuotas": []}
    await mod.list_requested_service_quota_changes(service_code="ec2", status="PENDING")
    kw = mc.call.call_args[1]
    assert kw["ServiceCode"] == "ec2"
    assert kw["Status"] == "PENDING"


async def test_list_requested_changes_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_requested_service_quota_changes()


async def test_list_requested_changes_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_requested_service_quota_changes failed"):
        await mod.list_requested_service_quota_changes()


async def test_get_requested_change_success(mc):
    mc.call.return_value = {"RequestedQuota": _CHANGE}
    r = await mod.get_requested_service_quota_change("ch-1")
    assert r.id == "ch-1"


async def test_get_requested_change_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_requested_service_quota_change("ch-1")


async def test_get_requested_change_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_requested_service_quota_change failed"):
        await mod.get_requested_service_quota_change("ch-1")


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_associate_service_quota_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_service_quota_template()
    mock_client.call.assert_called_once()


async def test_associate_service_quota_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_service_quota_template()


async def test_create_support_case(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_support_case("test-request_id", )
    mock_client.call.assert_called_once()


async def test_create_support_case_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_support_case("test-request_id", )


async def test_delete_service_quota_increase_request_from_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", )
    mock_client.call.assert_called_once()


async def test_delete_service_quota_increase_request_from_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", )


async def test_disassociate_service_quota_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_service_quota_template()
    mock_client.call.assert_called_once()


async def test_disassociate_service_quota_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_service_quota_template()


async def test_get_association_for_service_quota_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_association_for_service_quota_template()
    mock_client.call.assert_called_once()


async def test_get_association_for_service_quota_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_association_for_service_quota_template()


async def test_get_auto_management_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_auto_management_configuration()
    mock_client.call.assert_called_once()


async def test_get_auto_management_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_auto_management_configuration()


async def test_get_service_quota_increase_request_from_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", )
    mock_client.call.assert_called_once()


async def test_get_service_quota_increase_request_from_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_quota_increase_request_from_template("test-service_code", "test-quota_code", "test-aws_region", )


async def test_list_aws_default_service_quotas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_aws_default_service_quotas("test-service_code", )
    mock_client.call.assert_called_once()


async def test_list_aws_default_service_quotas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_aws_default_service_quotas("test-service_code", )


async def test_list_requested_service_quota_change_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_requested_service_quota_change_history()
    mock_client.call.assert_called_once()


async def test_list_requested_service_quota_change_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_requested_service_quota_change_history()


async def test_list_requested_service_quota_change_history_by_quota(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", )
    mock_client.call.assert_called_once()


async def test_list_requested_service_quota_change_history_by_quota_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", )


async def test_list_service_quota_increase_requests_in_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_quota_increase_requests_in_template()
    mock_client.call.assert_called_once()


async def test_list_service_quota_increase_requests_in_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_quota_increase_requests_in_template()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_service_quota_increase_request_into_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_service_quota_increase_request_into_template("test-quota_code", "test-service_code", "test-aws_region", "test-desired_value", )
    mock_client.call.assert_called_once()


async def test_put_service_quota_increase_request_into_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_service_quota_increase_request_into_template("test-quota_code", "test-service_code", "test-aws_region", "test-desired_value", )


async def test_start_auto_management(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_auto_management("test-opt_in_level", "test-opt_in_type", )
    mock_client.call.assert_called_once()


async def test_start_auto_management_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_auto_management("test-opt_in_level", "test-opt_in_type", )


async def test_stop_auto_management(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_auto_management()
    mock_client.call.assert_called_once()


async def test_stop_auto_management_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_auto_management()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_auto_management(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_auto_management()
    mock_client.call.assert_called_once()


async def test_update_auto_management_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.service_quotas.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_auto_management()


@pytest.mark.asyncio
async def test_list_requested_service_quota_changes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import list_requested_service_quota_changes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await list_requested_service_quota_changes(service_code="test-service_code", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aws_default_service_quotas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import list_aws_default_service_quotas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await list_aws_default_service_quotas("test-service_code", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_requested_service_quota_change_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import list_requested_service_quota_change_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await list_requested_service_quota_change_history(service_code="test-service_code", status="test-status", next_token="test-next_token", max_results=1, quota_requested_at_level="test-quota_requested_at_level", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_requested_service_quota_change_history_by_quota_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import list_requested_service_quota_change_history_by_quota
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await list_requested_service_quota_change_history_by_quota("test-service_code", "test-quota_code", status="test-status", next_token="test-next_token", max_results=1, quota_requested_at_level="test-quota_requested_at_level", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_quota_increase_requests_in_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import list_service_quota_increase_requests_in_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await list_service_quota_increase_requests_in_template(service_code="test-service_code", aws_region="test-aws_region", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_auto_management_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import start_auto_management
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await start_auto_management("test-opt_in_level", "test-opt_in_type", notification_arn="test-notification_arn", exclusion_list="test-exclusion_list", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_auto_management_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.service_quotas import update_auto_management
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.service_quotas.async_client", lambda *a, **kw: mock_client)
    await update_auto_management(opt_in_type="test-opt_in_type", notification_arn="test-notification_arn", exclusion_list="test-exclusion_list", region_name="us-east-1")
    mock_client.call.assert_called_once()
