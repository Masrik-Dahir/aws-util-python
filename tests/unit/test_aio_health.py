"""Tests for aws_util.aio.health -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.health import (
    AffectedAccountResult,
    AffectedEntityResult,
    EventAggregateResult,
    EventDetailResult,
    EventResult,
    EventTypeResult,
    OrgEventDetailResult,
    OrgEventResult,
    describe_affected_accounts_for_organization,
    describe_affected_entities,
    describe_event_aggregates,
    describe_event_details,
    describe_event_details_for_organization,
    describe_event_types,
    describe_events,
    describe_events_for_organization,
    describe_affected_entities_for_organization,
    describe_entity_aggregates,
    describe_entity_aggregates_for_organization,
    describe_health_service_status_for_organization,
    disable_health_service_access_for_organization,
    enable_health_service_access_for_organization,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


def test_models_re_exported():
    assert EventResult is not None
    assert EventDetailResult is not None
    assert AffectedEntityResult is not None
    assert EventTypeResult is not None
    assert EventAggregateResult is not None
    assert AffectedAccountResult is not None
    assert OrgEventResult is not None
    assert OrgEventDetailResult is not None


class TestDescribeEvents:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"events": [{"arn": "arn:event"}]})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_events()
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_with_filter(self, monkeypatch):
        mc = _mc({"events": []})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_events(filter={"services": ["EC2"]})
        assert result == []

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_events()


class TestDescribeEventDetails:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "successfulSet": [
                {
                    "event": {"arn": "arn:event"},
                    "eventDescription": {"latestDescription": "desc"},
                    "extra_key": "extra_val",
                }
            ]
        })
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_details(["arn:event"])
        assert len(result) == 1
        assert result[0].event_description == "desc"
        assert result[0].extra == {"extra_key": "extra_val"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_event_details(["arn:event"])


class TestDescribeAffectedEntities:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "entities": [
                {"entityValue": "i-123", "eventArn": "arn:event"}
            ]
        })
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_affected_entities(
            filter={"eventArns": ["arn:event"]}
        )
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_affected_entities(
                filter={"eventArns": ["arn:event"]}
            )


class TestDescribeEventTypes:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"eventTypes": [{"service": "EC2", "code": "OP"}]})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_types()
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_with_filter(self, monkeypatch):
        mc = _mc({"eventTypes": []})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_types(
            filter={"services": ["EC2"]},
            region_name="us-east-1",
        )
        assert result == []

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_event_types()


class TestDescribeEventAggregates:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "eventAggregates": [
                {"aggregateValue": "issue", "count": 5}
            ]
        })
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_aggregates("eventTypeCategory")
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_with_filter(self, monkeypatch):
        mc = _mc({"eventAggregates": []})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_aggregates(
            "eventTypeCategory",
            filter={"services": ["EC2"]},
            region_name="us-east-1",
        )
        assert result == []

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_event_aggregates("eventTypeCategory")


class TestDescribeAffectedAccountsForOrganization:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"affectedAccounts": ["123456789012"]})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_affected_accounts_for_organization(
            "arn:event"
        )
        assert len(result) == 1
        assert result[0].account_id == "123456789012"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_affected_accounts_for_organization("arn:event")


class TestDescribeEventsForOrganization:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"events": [{"arn": "arn:org-event"}]})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_events_for_organization()
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_with_filter(self, monkeypatch):
        mc = _mc({"events": []})
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_events_for_organization(
            filter={"services": ["EC2"]}
        )
        assert result == []

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_events_for_organization()


class TestDescribeEventDetailsForOrganization:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "successfulSet": [
                {
                    "event": {"arn": "arn:org-event"},
                    "eventDescription": {"latestDescription": "desc"},
                    "awsAccountId": "123",
                    "extra_key": "extra_val",
                }
            ]
        })
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        result = await describe_event_details_for_organization(
            [{"eventArn": "arn:org-event"}]
        )
        assert len(result) == 1
        assert result[0].aws_account_id == "123"
        assert result[0].extra == {"extra_key": "extra_val"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.health.async_client", lambda *a, **kw: mc
        )
        with pytest.raises(RuntimeError):
            await describe_event_details_for_organization(
                [{"eventArn": "arn:org-event"}]
            )


async def test_describe_affected_entities_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_affected_entities_for_organization()
    mock_client.call.assert_called_once()


async def test_describe_affected_entities_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_affected_entities_for_organization()


async def test_describe_entity_aggregates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_entity_aggregates()
    mock_client.call.assert_called_once()


async def test_describe_entity_aggregates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_entity_aggregates()


async def test_describe_entity_aggregates_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_entity_aggregates_for_organization([], )
    mock_client.call.assert_called_once()


async def test_describe_entity_aggregates_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_entity_aggregates_for_organization([], )


async def test_describe_health_service_status_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_health_service_status_for_organization()
    mock_client.call.assert_called_once()


async def test_describe_health_service_status_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_health_service_status_for_organization()


async def test_disable_health_service_access_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_health_service_access_for_organization()
    mock_client.call.assert_called_once()


async def test_disable_health_service_access_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_health_service_access_for_organization()


async def test_enable_health_service_access_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_health_service_access_for_organization()
    mock_client.call.assert_called_once()


async def test_enable_health_service_access_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.health.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_health_service_access_for_organization()


@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_events(filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_event_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_event_types(filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_aggregates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_event_aggregates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_event_aggregates("test-aggregate_field", filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_for_organization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_events_for_organization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_events_for_organization(filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_affected_entities_for_organization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_affected_entities_for_organization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_affected_entities_for_organization(organization_entity_filters="test-organization_entity_filters", locale="test-locale", next_token="test-next_token", max_results=1, organization_entity_account_filters=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_entity_aggregates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_entity_aggregates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_entity_aggregates(event_arns="test-event_arns", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_entity_aggregates_for_organization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.health import describe_entity_aggregates_for_organization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.health.async_client", lambda *a, **kw: mock_client)
    await describe_entity_aggregates_for_organization("test-event_arns", aws_account_ids=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
