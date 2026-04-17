"""Tests for aws_util.health -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.health import (
    AffectedAccountResult,
    AffectedEntityResult,
    EventAggregateResult,
    EventDetailResult,
    EventResult,
    EventTypeResult,
    OrgEventDetailResult,
    OrgEventResult,
    _parse_entity,
    _parse_event,
    _parse_event_aggregate,
    _parse_event_type,
    _parse_org_event,
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

_ERR = ClientError(
    {"Error": {"Code": "ValidationException", "Message": "bad"}}, "op"
)

# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_event_result_minimal(self):
        e = EventResult(arn="arn:event")
        assert e.arn == "arn:event"
        assert e.service is None
        assert e.extra == {}

    def test_event_detail_result(self):
        ev = EventResult(arn="arn:event")
        ed = EventDetailResult(event=ev, event_description="desc")
        assert ed.event_description == "desc"

    def test_affected_entity_result(self):
        ae = AffectedEntityResult(
            entity_value="i-123", event_arn="arn:event",
            tags={"a": "b"},
        )
        assert ae.entity_value == "i-123"
        assert ae.tags == {"a": "b"}

    def test_event_type_result(self):
        et = EventTypeResult(service="EC2", code="AWS_EC2_OP_ISSUE")
        assert et.code == "AWS_EC2_OP_ISSUE"

    def test_event_aggregate_result(self):
        ea = EventAggregateResult(aggregate_value="issue", count=5)
        assert ea.count == 5

    def test_affected_account_result(self):
        aa = AffectedAccountResult(account_id="123456789012")
        assert aa.account_id == "123456789012"

    def test_org_event_result(self):
        oe = OrgEventResult(arn="arn:org-event")
        assert oe.service is None

    def test_org_event_detail_result(self):
        oe = OrgEventResult(arn="arn:org-event")
        oed = OrgEventDetailResult(
            event=oe, event_description="desc",
            aws_account_id="123",
        )
        assert oed.aws_account_id == "123"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_event_full(self):
        raw = {
            "arn": "arn:event",
            "service": "EC2",
            "eventTypeCode": "AWS_EC2_OP_ISSUE",
            "eventTypeCategory": "issue",
            "region": "us-east-1",
            "startTime": "2024-01-01",
            "endTime": "2024-01-02",
            "lastUpdatedTime": "2024-01-03",
            "statusCode": "open",
            "extra_field": "val",
        }
        e = _parse_event(raw)
        assert e.start_time == "2024-01-01"
        assert e.end_time == "2024-01-02"
        assert e.last_updated_time == "2024-01-03"
        assert e.extra == {"extra_field": "val"}

    def test_parse_event_no_times(self):
        raw = {"arn": "arn:event"}
        e = _parse_event(raw)
        assert e.start_time is None
        assert e.end_time is None
        assert e.last_updated_time is None

    def test_parse_entity_full(self):
        raw = {
            "entityValue": "i-123",
            "eventArn": "arn:event",
            "awsAccountId": "123",
            "entityUrl": "https://example.com",
            "statusCode": "IMPAIRED",
            "lastUpdatedTime": "2024-01-01",
            "tags": {"env": "prod"},
            "extra_field": "val",
        }
        ae = _parse_entity(raw)
        assert ae.last_updated_time == "2024-01-01"
        assert ae.extra == {"extra_field": "val"}

    def test_parse_entity_no_time(self):
        raw = {"entityValue": "i-123", "eventArn": "arn:event"}
        ae = _parse_entity(raw)
        assert ae.last_updated_time is None

    def test_parse_event_type(self):
        raw = {"service": "EC2", "code": "OP_ISSUE", "category": "issue", "x": 1}
        et = _parse_event_type(raw)
        assert et.extra == {"x": 1}

    def test_parse_event_aggregate(self):
        raw = {"aggregateValue": "issue", "count": 5, "x": 1}
        ea = _parse_event_aggregate(raw)
        assert ea.extra == {"x": 1}

    def test_parse_org_event_full(self):
        raw = {
            "arn": "arn:org-event",
            "service": "EC2",
            "eventTypeCode": "OP",
            "eventTypeCategory": "issue",
            "region": "us-east-1",
            "startTime": "2024-01-01",
            "endTime": "2024-01-02",
            "lastUpdatedTime": "2024-01-03",
            "statusCode": "open",
            "extra_field": "val",
        }
        oe = _parse_org_event(raw)
        assert oe.start_time == "2024-01-01"
        assert oe.extra == {"extra_field": "val"}

    def test_parse_org_event_no_times(self):
        raw = {"arn": "arn:org-event"}
        oe = _parse_org_event(raw)
        assert oe.start_time is None


# ---------------------------------------------------------------------------
# Function tests
# ---------------------------------------------------------------------------


class TestDescribeEvents:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_events.return_value = {
            "events": [{"arn": "arn:event"}]
        }
        mock_gc.return_value = client
        result = describe_events()
        assert len(result) == 1

    @patch("aws_util.health.get_client")
    def test_with_filter(self, mock_gc):
        client = MagicMock()
        client.describe_events.return_value = {"events": []}
        mock_gc.return_value = client
        result = describe_events(filter={"services": ["EC2"]})
        assert result == []

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_events.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_events()


class TestDescribeEventDetails:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_event_details.return_value = {
            "successfulSet": [
                {
                    "event": {"arn": "arn:event"},
                    "eventDescription": {"latestDescription": "desc"},
                    "extra_key": "extra_val",
                }
            ]
        }
        mock_gc.return_value = client
        result = describe_event_details(["arn:event"])
        assert len(result) == 1
        assert result[0].event_description == "desc"
        assert result[0].extra == {"extra_key": "extra_val"}

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_event_details.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_event_details(["arn:event"])


class TestDescribeAffectedEntities:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_affected_entities.return_value = {
            "entities": [
                {"entityValue": "i-123", "eventArn": "arn:event"}
            ]
        }
        mock_gc.return_value = client
        result = describe_affected_entities(
            filter={"eventArns": ["arn:event"]}
        )
        assert len(result) == 1

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_affected_entities.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_affected_entities(
                filter={"eventArns": ["arn:event"]}
            )


class TestDescribeEventTypes:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_event_types.return_value = {
            "eventTypes": [{"service": "EC2", "code": "OP"}]
        }
        mock_gc.return_value = client
        result = describe_event_types()
        assert len(result) == 1

    @patch("aws_util.health.get_client")
    def test_with_filter(self, mock_gc):
        client = MagicMock()
        client.describe_event_types.return_value = {"eventTypes": []}
        mock_gc.return_value = client
        result = describe_event_types(
            filter={"services": ["EC2"]},
            region_name="us-east-1",
        )
        assert result == []

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_event_types.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_event_types()


class TestDescribeEventAggregates:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_event_aggregates.return_value = {
            "eventAggregates": [{"aggregateValue": "issue", "count": 5}]
        }
        mock_gc.return_value = client
        result = describe_event_aggregates("eventTypeCategory")
        assert len(result) == 1

    @patch("aws_util.health.get_client")
    def test_with_filter(self, mock_gc):
        client = MagicMock()
        client.describe_event_aggregates.return_value = {
            "eventAggregates": []
        }
        mock_gc.return_value = client
        result = describe_event_aggregates(
            "eventTypeCategory",
            filter={"services": ["EC2"]},
            region_name="us-east-1",
        )
        assert result == []

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_event_aggregates.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_event_aggregates("eventTypeCategory")


class TestDescribeAffectedAccountsForOrganization:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_affected_accounts_for_organization.return_value = {
            "affectedAccounts": ["123456789012"]
        }
        mock_gc.return_value = client
        result = describe_affected_accounts_for_organization("arn:event")
        assert len(result) == 1
        assert result[0].account_id == "123456789012"

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_affected_accounts_for_organization.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_affected_accounts_for_organization("arn:event")


class TestDescribeEventsForOrganization:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_events_for_organization.return_value = {
            "events": [{"arn": "arn:org-event"}]
        }
        mock_gc.return_value = client
        result = describe_events_for_organization()
        assert len(result) == 1

    @patch("aws_util.health.get_client")
    def test_with_filter(self, mock_gc):
        client = MagicMock()
        client.describe_events_for_organization.return_value = {
            "events": []
        }
        mock_gc.return_value = client
        result = describe_events_for_organization(
            filter={"services": ["EC2"]}
        )
        assert result == []

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_events_for_organization.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_events_for_organization()


class TestDescribeEventDetailsForOrganization:
    @patch("aws_util.health.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.describe_event_details_for_organization.return_value = {
            "successfulSet": [
                {
                    "event": {"arn": "arn:org-event"},
                    "eventDescription": {"latestDescription": "desc"},
                    "awsAccountId": "123",
                    "extra_key": "extra_val",
                }
            ]
        }
        mock_gc.return_value = client
        result = describe_event_details_for_organization(
            [{"eventArn": "arn:org-event"}]
        )
        assert len(result) == 1
        assert result[0].aws_account_id == "123"
        assert result[0].extra == {"extra_key": "extra_val"}

    @patch("aws_util.health.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.describe_event_details_for_organization.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            describe_event_details_for_organization(
                [{"eventArn": "arn:org-event"}]
            )


REGION = "us-east-1"


@patch("aws_util.health.get_client")
def test_describe_affected_entities_for_organization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_affected_entities_for_organization.return_value = {}
    describe_affected_entities_for_organization(region_name=REGION)
    mock_client.describe_affected_entities_for_organization.assert_called_once()


@patch("aws_util.health.get_client")
def test_describe_affected_entities_for_organization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_affected_entities_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_affected_entities_for_organization",
    )
    with pytest.raises(RuntimeError, match="Failed to describe affected entities for organization"):
        describe_affected_entities_for_organization(region_name=REGION)


@patch("aws_util.health.get_client")
def test_describe_entity_aggregates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_entity_aggregates.return_value = {}
    describe_entity_aggregates(region_name=REGION)
    mock_client.describe_entity_aggregates.assert_called_once()


@patch("aws_util.health.get_client")
def test_describe_entity_aggregates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_entity_aggregates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_entity_aggregates",
    )
    with pytest.raises(RuntimeError, match="Failed to describe entity aggregates"):
        describe_entity_aggregates(region_name=REGION)


@patch("aws_util.health.get_client")
def test_describe_entity_aggregates_for_organization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_entity_aggregates_for_organization.return_value = {}
    describe_entity_aggregates_for_organization([], region_name=REGION)
    mock_client.describe_entity_aggregates_for_organization.assert_called_once()


@patch("aws_util.health.get_client")
def test_describe_entity_aggregates_for_organization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_entity_aggregates_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_entity_aggregates_for_organization",
    )
    with pytest.raises(RuntimeError, match="Failed to describe entity aggregates for organization"):
        describe_entity_aggregates_for_organization([], region_name=REGION)


@patch("aws_util.health.get_client")
def test_describe_health_service_status_for_organization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_health_service_status_for_organization.return_value = {}
    describe_health_service_status_for_organization(region_name=REGION)
    mock_client.describe_health_service_status_for_organization.assert_called_once()


@patch("aws_util.health.get_client")
def test_describe_health_service_status_for_organization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_health_service_status_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_health_service_status_for_organization",
    )
    with pytest.raises(RuntimeError, match="Failed to describe health service status for organization"):
        describe_health_service_status_for_organization(region_name=REGION)


@patch("aws_util.health.get_client")
def test_disable_health_service_access_for_organization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_health_service_access_for_organization.return_value = {}
    disable_health_service_access_for_organization(region_name=REGION)
    mock_client.disable_health_service_access_for_organization.assert_called_once()


@patch("aws_util.health.get_client")
def test_disable_health_service_access_for_organization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_health_service_access_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_health_service_access_for_organization",
    )
    with pytest.raises(RuntimeError, match="Failed to disable health service access for organization"):
        disable_health_service_access_for_organization(region_name=REGION)


@patch("aws_util.health.get_client")
def test_enable_health_service_access_for_organization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_health_service_access_for_organization.return_value = {}
    enable_health_service_access_for_organization(region_name=REGION)
    mock_client.enable_health_service_access_for_organization.assert_called_once()


@patch("aws_util.health.get_client")
def test_enable_health_service_access_for_organization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_health_service_access_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_health_service_access_for_organization",
    )
    with pytest.raises(RuntimeError, match="Failed to enable health service access for organization"):
        enable_health_service_access_for_organization(region_name=REGION)


def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_events(filter="test-filter", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_event_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_event_types
    mock_client = MagicMock()
    mock_client.describe_event_types.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_event_types(filter="test-filter", region_name="us-east-1")
    mock_client.describe_event_types.assert_called_once()

def test_describe_event_aggregates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_event_aggregates
    mock_client = MagicMock()
    mock_client.describe_event_aggregates.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_event_aggregates("test-aggregate_field", filter="test-filter", region_name="us-east-1")
    mock_client.describe_event_aggregates.assert_called_once()

def test_describe_events_for_organization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_events_for_organization
    mock_client = MagicMock()
    mock_client.describe_events_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_events_for_organization(filter="test-filter", region_name="us-east-1")
    mock_client.describe_events_for_organization.assert_called_once()

def test_describe_affected_entities_for_organization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_affected_entities_for_organization
    mock_client = MagicMock()
    mock_client.describe_affected_entities_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_affected_entities_for_organization(organization_entity_filters="test-organization_entity_filters", locale="test-locale", next_token="test-next_token", max_results=1, organization_entity_account_filters=1, region_name="us-east-1")
    mock_client.describe_affected_entities_for_organization.assert_called_once()

def test_describe_entity_aggregates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_entity_aggregates
    mock_client = MagicMock()
    mock_client.describe_entity_aggregates.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_entity_aggregates(event_arns="test-event_arns", region_name="us-east-1")
    mock_client.describe_entity_aggregates.assert_called_once()

def test_describe_entity_aggregates_for_organization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.health import describe_entity_aggregates_for_organization
    mock_client = MagicMock()
    mock_client.describe_entity_aggregates_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.health.get_client", lambda *a, **kw: mock_client)
    describe_entity_aggregates_for_organization("test-event_arns", aws_account_ids=1, region_name="us-east-1")
    mock_client.describe_entity_aggregates_for_organization.assert_called_once()
