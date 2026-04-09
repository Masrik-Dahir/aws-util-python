"""Tests for aws_util.eventbridge module."""
from __future__ import annotations

import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.eventbridge as eb_mod
from aws_util.eventbridge import (
    EventEntry,
    PutEventsResult,
    put_event,
    put_events,
    put_events_chunked,
    list_rules,
    activate_event_source,
    cancel_replay,
    create_api_destination,
    create_archive,
    create_connection,
    create_endpoint,
    create_event_bus,
    create_partner_event_source,
    deactivate_event_source,
    deauthorize_connection,
    delete_api_destination,
    delete_archive,
    delete_connection,
    delete_endpoint,
    delete_event_bus,
    delete_partner_event_source,
    delete_rule,
    describe_api_destination,
    describe_archive,
    describe_connection,
    describe_endpoint,
    describe_event_bus,
    describe_event_source,
    describe_partner_event_source,
    describe_replay,
    describe_rule,
    disable_rule,
    enable_rule,
    list_api_destinations,
    list_archives,
    list_connections,
    list_endpoints,
    list_event_buses,
    list_event_sources,
    list_partner_event_source_accounts,
    list_partner_event_sources,
    list_replays,
    list_rule_names_by_target,
    list_tags_for_resource,
    list_targets_by_rule,
    put_partner_events,
    put_permission,
    put_rule,
    put_targets,
    remove_permission,
    remove_targets,
    run_event_pattern,
    start_replay,
    tag_resource,
    untag_resource,
    update_api_destination,
    update_archive,
    update_connection,
    update_endpoint,
    update_event_bus,
)

REGION = "us-east-1"


def _make_entry(**kwargs) -> EventEntry:
    defaults = {
        "source": "com.test.app",
        "detail_type": "OrderPlaced",
        "detail": {"order_id": "123"},
    }
    defaults.update(kwargs)
    return EventEntry(**defaults)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_event_entry_model():
    entry = _make_entry()
    assert entry.source == "com.test.app"
    assert entry.event_bus_name == "default"
    assert entry.resources == []


def test_put_events_result_model():
    result = PutEventsResult(failed_count=0, successful_count=2, entries=[])
    assert result.successful_count == 2


# ---------------------------------------------------------------------------
# put_events
# ---------------------------------------------------------------------------

def test_put_events_success():
    entries = [_make_entry()]
    result = put_events(entries, region_name=REGION)
    assert isinstance(result, PutEventsResult)
    assert result.failed_count == 0
    assert result.successful_count == 1


def test_put_events_too_many_raises():
    with pytest.raises(ValueError, match="at most 10"):
        put_events([_make_entry()] * 11, region_name=REGION)


def test_put_events_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_events.side_effect = ClientError(
        {"Error": {"Code": "InternalException", "Message": "error"}}, "PutEvents"
    )
    monkeypatch.setattr(eb_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put events"):
        put_events([_make_entry()], region_name=REGION)


def test_put_events_partial_failure_returns_result(monkeypatch):
    """When some events succeed and some fail, a result is returned (not raised)."""
    mock_client = MagicMock()
    mock_client.put_events.return_value = {
        "FailedEntryCount": 1,
        "Entries": [
            {"EventId": "abc123"},
            {"ErrorCode": "SomeError", "ErrorMessage": "fail"},
        ],
    }
    monkeypatch.setattr(eb_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_events([_make_entry(), _make_entry()], region_name=REGION)
    assert result.failed_count == 1
    assert result.successful_count == 1


def test_put_events_all_fail_raises(monkeypatch):
    """When ALL events fail, an AwsServiceError is raised."""
    mock_client = MagicMock()
    mock_client.put_events.return_value = {
        "FailedEntryCount": 1,
        "Entries": [{"ErrorCode": "SomeError", "ErrorMessage": "fail"}],
    }
    monkeypatch.setattr(eb_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="All.*event.*failed to publish"):
        put_events([_make_entry()], region_name=REGION)


def test_put_events_with_resources():
    entries = [_make_entry(resources=["arn:aws:s3:::my-bucket"])]
    result = put_events(entries, region_name=REGION)
    assert result.successful_count == 1


# ---------------------------------------------------------------------------
# put_event
# ---------------------------------------------------------------------------

def test_put_event_success():
    result = put_event(
        source="com.test",
        detail_type="TestEvent",
        detail={"key": "value"},
        region_name=REGION,
    )
    assert isinstance(result, PutEventsResult)
    assert result.successful_count == 1


def test_put_event_with_custom_bus():
    # moto creates default bus; use it
    result = put_event(
        source="com.test",
        detail_type="TestEvent",
        detail={},
        event_bus_name="default",
        resources=["arn:resource:1"],
        region_name=REGION,
    )
    assert result.failed_count == 0


# ---------------------------------------------------------------------------
# put_events_chunked
# ---------------------------------------------------------------------------

def test_put_events_chunked_single_batch():
    events = [_make_entry() for _ in range(5)]
    results = put_events_chunked(events, region_name=REGION)
    assert len(results) == 1
    assert results[0].successful_count == 5


def test_put_events_chunked_multiple_batches():
    events = [_make_entry() for _ in range(25)]
    results = put_events_chunked(events, region_name=REGION)
    assert len(results) == 3  # 10 + 10 + 5
    total = sum(r.successful_count for r in results)
    assert total == 25


def test_put_events_chunked_empty():
    results = put_events_chunked([], region_name=REGION)
    assert results == []


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------

def test_list_rules_returns_list():
    result = list_rules(region_name=REGION)
    assert isinstance(result, list)


def test_list_rules_with_created_rule():
    client = boto3.client("events", region_name=REGION)
    client.put_rule(
        Name="test-rule",
        ScheduleExpression="rate(5 minutes)",
        State="ENABLED",
    )
    result = list_rules(region_name=REGION)
    assert any(r.get("Name") == "test-rule" for r in result)


def test_list_rules_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListRules"
    )
    monkeypatch.setattr(eb_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_rules failed"):
        list_rules(region_name=REGION)


def test_activate_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    activate_event_source("test-name", region_name=REGION)
    mock_client.activate_event_source.assert_called_once()


def test_activate_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "activate_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to activate event source"):
        activate_event_source("test-name", region_name=REGION)


def test_cancel_replay(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_replay.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    cancel_replay("test-replay_name", region_name=REGION)
    mock_client.cancel_replay.assert_called_once()


def test_cancel_replay_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_replay.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_replay",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel replay"):
        cancel_replay("test-replay_name", region_name=REGION)


def test_create_api_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", region_name=REGION)
    mock_client.create_api_destination.assert_called_once()


def test_create_api_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_api_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_api_destination",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create api destination"):
        create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", region_name=REGION)


def test_create_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_archive("test-archive_name", "test-event_source_arn", region_name=REGION)
    mock_client.create_archive.assert_called_once()


def test_create_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_archive",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create archive"):
        create_archive("test-archive_name", "test-event_source_arn", region_name=REGION)


def test_create_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_connection("test-name", "test-authorization_type", {}, region_name=REGION)
    mock_client.create_connection.assert_called_once()


def test_create_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_connection",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create connection"):
        create_connection("test-name", "test-authorization_type", {}, region_name=REGION)


def test_create_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_endpoint("test-name", {}, [], region_name=REGION)
    mock_client.create_endpoint.assert_called_once()


def test_create_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_endpoint",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create endpoint"):
        create_endpoint("test-name", {}, [], region_name=REGION)


def test_create_event_bus(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_event_bus("test-name", region_name=REGION)
    mock_client.create_event_bus.assert_called_once()


def test_create_event_bus_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_bus.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_bus",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create event bus"):
        create_event_bus("test-name", region_name=REGION)


def test_create_partner_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partner_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_partner_event_source("test-name", "test-account", region_name=REGION)
    mock_client.create_partner_event_source.assert_called_once()


def test_create_partner_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partner_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_partner_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create partner event source"):
        create_partner_event_source("test-name", "test-account", region_name=REGION)


def test_deactivate_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    deactivate_event_source("test-name", region_name=REGION)
    mock_client.deactivate_event_source.assert_called_once()


def test_deactivate_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate event source"):
        deactivate_event_source("test-name", region_name=REGION)


def test_deauthorize_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.deauthorize_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    deauthorize_connection("test-name", region_name=REGION)
    mock_client.deauthorize_connection.assert_called_once()


def test_deauthorize_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deauthorize_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deauthorize_connection",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deauthorize connection"):
        deauthorize_connection("test-name", region_name=REGION)


def test_delete_api_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_api_destination("test-name", region_name=REGION)
    mock_client.delete_api_destination.assert_called_once()


def test_delete_api_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_api_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_api_destination",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete api destination"):
        delete_api_destination("test-name", region_name=REGION)


def test_delete_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_archive("test-archive_name", region_name=REGION)
    mock_client.delete_archive.assert_called_once()


def test_delete_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_archive",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete archive"):
        delete_archive("test-archive_name", region_name=REGION)


def test_delete_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_connection("test-name", region_name=REGION)
    mock_client.delete_connection.assert_called_once()


def test_delete_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connection"):
        delete_connection("test-name", region_name=REGION)


def test_delete_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_endpoint("test-name", region_name=REGION)
    mock_client.delete_endpoint.assert_called_once()


def test_delete_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_endpoint",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete endpoint"):
        delete_endpoint("test-name", region_name=REGION)


def test_delete_event_bus(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_event_bus("test-name", region_name=REGION)
    mock_client.delete_event_bus.assert_called_once()


def test_delete_event_bus_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_bus.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_bus",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete event bus"):
        delete_event_bus("test-name", region_name=REGION)


def test_delete_partner_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partner_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_partner_event_source("test-name", "test-account", region_name=REGION)
    mock_client.delete_partner_event_source.assert_called_once()


def test_delete_partner_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partner_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_partner_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete partner event source"):
        delete_partner_event_source("test-name", "test-account", region_name=REGION)


def test_delete_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_rule("test-name", region_name=REGION)
    mock_client.delete_rule.assert_called_once()


def test_delete_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete rule"):
        delete_rule("test-name", region_name=REGION)


def test_describe_api_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_api_destination("test-name", region_name=REGION)
    mock_client.describe_api_destination.assert_called_once()


def test_describe_api_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_api_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_api_destination",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe api destination"):
        describe_api_destination("test-name", region_name=REGION)


def test_describe_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_archive("test-archive_name", region_name=REGION)
    mock_client.describe_archive.assert_called_once()


def test_describe_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_archive",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe archive"):
        describe_archive("test-archive_name", region_name=REGION)


def test_describe_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_connection("test-name", region_name=REGION)
    mock_client.describe_connection.assert_called_once()


def test_describe_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_connection",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe connection"):
        describe_connection("test-name", region_name=REGION)


def test_describe_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_endpoint("test-name", region_name=REGION)
    mock_client.describe_endpoint.assert_called_once()


def test_describe_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoint"):
        describe_endpoint("test-name", region_name=REGION)


def test_describe_event_bus(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_event_bus(region_name=REGION)
    mock_client.describe_event_bus.assert_called_once()


def test_describe_event_bus_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_bus.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_bus",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event bus"):
        describe_event_bus(region_name=REGION)


def test_describe_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_event_source("test-name", region_name=REGION)
    mock_client.describe_event_source.assert_called_once()


def test_describe_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event source"):
        describe_event_source("test-name", region_name=REGION)


def test_describe_partner_event_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_partner_event_source.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_partner_event_source("test-name", region_name=REGION)
    mock_client.describe_partner_event_source.assert_called_once()


def test_describe_partner_event_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_partner_event_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_partner_event_source",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe partner event source"):
        describe_partner_event_source("test-name", region_name=REGION)


def test_describe_replay(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replay.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_replay("test-replay_name", region_name=REGION)
    mock_client.describe_replay.assert_called_once()


def test_describe_replay_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replay.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replay",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe replay"):
        describe_replay("test-replay_name", region_name=REGION)


def test_describe_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_rule("test-name", region_name=REGION)
    mock_client.describe_rule.assert_called_once()


def test_describe_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe rule"):
        describe_rule("test-name", region_name=REGION)


def test_disable_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    disable_rule("test-name", region_name=REGION)
    mock_client.disable_rule.assert_called_once()


def test_disable_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable rule"):
        disable_rule("test-name", region_name=REGION)


def test_enable_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    enable_rule("test-name", region_name=REGION)
    mock_client.enable_rule.assert_called_once()


def test_enable_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable rule"):
        enable_rule("test-name", region_name=REGION)


def test_list_api_destinations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_api_destinations.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_api_destinations(region_name=REGION)
    mock_client.list_api_destinations.assert_called_once()


def test_list_api_destinations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_api_destinations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_api_destinations",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list api destinations"):
        list_api_destinations(region_name=REGION)


def test_list_archives(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_archives.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_archives(region_name=REGION)
    mock_client.list_archives.assert_called_once()


def test_list_archives_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_archives.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_archives",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list archives"):
        list_archives(region_name=REGION)


def test_list_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_connections(region_name=REGION)
    mock_client.list_connections.assert_called_once()


def test_list_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_connections",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list connections"):
        list_connections(region_name=REGION)


def test_list_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_endpoints(region_name=REGION)
    mock_client.list_endpoints.assert_called_once()


def test_list_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_endpoints",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list endpoints"):
        list_endpoints(region_name=REGION)


def test_list_event_buses(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_buses.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_event_buses(region_name=REGION)
    mock_client.list_event_buses.assert_called_once()


def test_list_event_buses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_buses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_event_buses",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list event buses"):
        list_event_buses(region_name=REGION)


def test_list_event_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_sources.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_event_sources(region_name=REGION)
    mock_client.list_event_sources.assert_called_once()


def test_list_event_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_event_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_event_sources",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list event sources"):
        list_event_sources(region_name=REGION)


def test_list_partner_event_source_accounts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_partner_event_source_accounts.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_partner_event_source_accounts("test-event_source_name", region_name=REGION)
    mock_client.list_partner_event_source_accounts.assert_called_once()


def test_list_partner_event_source_accounts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_partner_event_source_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_partner_event_source_accounts",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list partner event source accounts"):
        list_partner_event_source_accounts("test-event_source_name", region_name=REGION)


def test_list_partner_event_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_partner_event_sources.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_partner_event_sources("test-name_prefix", region_name=REGION)
    mock_client.list_partner_event_sources.assert_called_once()


def test_list_partner_event_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_partner_event_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_partner_event_sources",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list partner event sources"):
        list_partner_event_sources("test-name_prefix", region_name=REGION)


def test_list_replays(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_replays.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_replays(region_name=REGION)
    mock_client.list_replays.assert_called_once()


def test_list_replays_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_replays.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_replays",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list replays"):
        list_replays(region_name=REGION)


def test_list_rule_names_by_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rule_names_by_target.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_rule_names_by_target("test-target_arn", region_name=REGION)
    mock_client.list_rule_names_by_target.assert_called_once()


def test_list_rule_names_by_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rule_names_by_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rule_names_by_target",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list rule names by target"):
        list_rule_names_by_target("test-target_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_targets_by_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targets_by_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_targets_by_rule("test-rule", region_name=REGION)
    mock_client.list_targets_by_rule.assert_called_once()


def test_list_targets_by_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targets_by_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_targets_by_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list targets by rule"):
        list_targets_by_rule("test-rule", region_name=REGION)


def test_put_partner_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_partner_events.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_partner_events([], region_name=REGION)
    mock_client.put_partner_events.assert_called_once()


def test_put_partner_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_partner_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_partner_events",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put partner events"):
        put_partner_events([], region_name=REGION)


def test_put_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_permission.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_permission(region_name=REGION)
    mock_client.put_permission.assert_called_once()


def test_put_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_permission",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put permission"):
        put_permission(region_name=REGION)


def test_put_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_rule("test-name", region_name=REGION)
    mock_client.put_rule.assert_called_once()


def test_put_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_rule",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put rule"):
        put_rule("test-name", region_name=REGION)


def test_put_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_targets.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_targets("test-rule", [], region_name=REGION)
    mock_client.put_targets.assert_called_once()


def test_put_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_targets",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put targets"):
        put_targets("test-rule", [], region_name=REGION)


def test_remove_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    remove_permission(region_name=REGION)
    mock_client.remove_permission.assert_called_once()


def test_remove_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_permission",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove permission"):
        remove_permission(region_name=REGION)


def test_remove_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_targets.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    remove_targets("test-rule", [], region_name=REGION)
    mock_client.remove_targets.assert_called_once()


def test_remove_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_targets",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove targets"):
        remove_targets("test-rule", [], region_name=REGION)


def test_run_event_pattern(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_event_pattern.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    run_event_pattern("test-event_pattern", "test-event", region_name=REGION)
    mock_client.test_event_pattern.assert_called_once()


def test_run_event_pattern_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_event_pattern.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_event_pattern",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run event pattern"):
        run_event_pattern("test-event_pattern", "test-event", region_name=REGION)


def test_start_replay(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_replay.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", {}, region_name=REGION)
    mock_client.start_replay.assert_called_once()


def test_start_replay_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_replay.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_replay",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start replay"):
        start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", {}, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_api_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_api_destination("test-name", region_name=REGION)
    mock_client.update_api_destination.assert_called_once()


def test_update_api_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_api_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_api_destination",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update api destination"):
        update_api_destination("test-name", region_name=REGION)


def test_update_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_archive("test-archive_name", region_name=REGION)
    mock_client.update_archive.assert_called_once()


def test_update_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_archive",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update archive"):
        update_archive("test-archive_name", region_name=REGION)


def test_update_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_connection("test-name", region_name=REGION)
    mock_client.update_connection.assert_called_once()


def test_update_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connection",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connection"):
        update_connection("test-name", region_name=REGION)


def test_update_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_endpoint("test-name", region_name=REGION)
    mock_client.update_endpoint.assert_called_once()


def test_update_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_endpoint",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update endpoint"):
        update_endpoint("test-name", region_name=REGION)


def test_update_event_bus(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_event_bus(region_name=REGION)
    mock_client.update_event_bus.assert_called_once()


def test_update_event_bus_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_bus.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_event_bus",
    )
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update event bus"):
        update_event_bus(region_name=REGION)


def test_create_api_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import create_api_destination
    mock_client = MagicMock()
    mock_client.create_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", description="test-description", invocation_rate_limit_per_second=1, region_name="us-east-1")
    mock_client.create_api_destination.assert_called_once()

def test_create_archive_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import create_archive
    mock_client = MagicMock()
    mock_client.create_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_archive("test-archive_name", "test-event_source_arn", description="test-description", event_pattern="test-event_pattern", retention_days="test-retention_days", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.create_archive.assert_called_once()

def test_create_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import create_connection
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_connection("test-name", "test-authorization_type", "test-auth_parameters", description="test-description", invocation_connectivity_parameters="test-invocation_connectivity_parameters", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.create_connection.assert_called_once()

def test_create_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import create_endpoint
    mock_client = MagicMock()
    mock_client.create_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_endpoint("test-name", {}, "test-event_buses", description="test-description", replication_config={}, role_arn="test-role_arn", region_name="us-east-1")
    mock_client.create_endpoint.assert_called_once()

def test_create_event_bus_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import create_event_bus
    mock_client = MagicMock()
    mock_client.create_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    create_event_bus("test-name", event_source_name="test-event_source_name", description="test-description", kms_key_identifier="test-kms_key_identifier", dead_letter_config={}, log_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_bus.assert_called_once()

def test_delete_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import delete_rule
    mock_client = MagicMock()
    mock_client.delete_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    delete_rule("test-name", event_bus_name="test-event_bus_name", force=True, region_name="us-east-1")
    mock_client.delete_rule.assert_called_once()

def test_describe_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import describe_endpoint
    mock_client = MagicMock()
    mock_client.describe_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_endpoint("test-name", home_region="test-home_region", region_name="us-east-1")
    mock_client.describe_endpoint.assert_called_once()

def test_describe_event_bus_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import describe_event_bus
    mock_client = MagicMock()
    mock_client.describe_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_event_bus(name="test-name", region_name="us-east-1")
    mock_client.describe_event_bus.assert_called_once()

def test_describe_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import describe_rule
    mock_client = MagicMock()
    mock_client.describe_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    describe_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.describe_rule.assert_called_once()

def test_disable_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import disable_rule
    mock_client = MagicMock()
    mock_client.disable_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    disable_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.disable_rule.assert_called_once()

def test_enable_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import enable_rule
    mock_client = MagicMock()
    mock_client.enable_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    enable_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.enable_rule.assert_called_once()

def test_list_api_destinations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_api_destinations
    mock_client = MagicMock()
    mock_client.list_api_destinations.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_api_destinations(name_prefix="test-name_prefix", connection_arn="test-connection_arn", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_api_destinations.assert_called_once()

def test_list_archives_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_archives
    mock_client = MagicMock()
    mock_client.list_archives.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_archives(name_prefix="test-name_prefix", event_source_arn="test-event_source_arn", state="test-state", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_archives.assert_called_once()

def test_list_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_connections
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_connections(name_prefix="test-name_prefix", connection_state="test-connection_state", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_connections.assert_called_once()

def test_list_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_endpoints
    mock_client = MagicMock()
    mock_client.list_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_endpoints(name_prefix="test-name_prefix", home_region="test-home_region", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_endpoints.assert_called_once()

def test_list_event_buses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_event_buses
    mock_client = MagicMock()
    mock_client.list_event_buses.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_event_buses(name_prefix="test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_event_buses.assert_called_once()

def test_list_event_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_event_sources
    mock_client = MagicMock()
    mock_client.list_event_sources.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_event_sources(name_prefix="test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_event_sources.assert_called_once()

def test_list_partner_event_source_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_partner_event_source_accounts
    mock_client = MagicMock()
    mock_client.list_partner_event_source_accounts.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_partner_event_source_accounts("test-event_source_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_partner_event_source_accounts.assert_called_once()

def test_list_partner_event_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_partner_event_sources
    mock_client = MagicMock()
    mock_client.list_partner_event_sources.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_partner_event_sources("test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_partner_event_sources.assert_called_once()

def test_list_replays_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_replays
    mock_client = MagicMock()
    mock_client.list_replays.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_replays(name_prefix="test-name_prefix", state="test-state", event_source_arn="test-event_source_arn", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_replays.assert_called_once()

def test_list_rule_names_by_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_rule_names_by_target
    mock_client = MagicMock()
    mock_client.list_rule_names_by_target.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_rule_names_by_target("test-target_arn", event_bus_name="test-event_bus_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_rule_names_by_target.assert_called_once()

def test_list_targets_by_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import list_targets_by_rule
    mock_client = MagicMock()
    mock_client.list_targets_by_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    list_targets_by_rule("test-rule", event_bus_name="test-event_bus_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.list_targets_by_rule.assert_called_once()

def test_put_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import put_permission
    mock_client = MagicMock()
    mock_client.put_permission.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_permission(event_bus_name="test-event_bus_name", action="test-action", principal="test-principal", statement_id="test-statement_id", condition="test-condition", policy="{}", region_name="us-east-1")
    mock_client.put_permission.assert_called_once()

def test_put_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import put_rule
    mock_client = MagicMock()
    mock_client.put_rule.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_rule("test-name", schedule_expression="test-schedule_expression", event_pattern="test-event_pattern", state="test-state", description="test-description", role_arn="test-role_arn", tags=[{"Key": "k", "Value": "v"}], event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.put_rule.assert_called_once()

def test_put_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import put_targets
    mock_client = MagicMock()
    mock_client.put_targets.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    put_targets("test-rule", "test-targets", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.put_targets.assert_called_once()

def test_remove_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import remove_permission
    mock_client = MagicMock()
    mock_client.remove_permission.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    remove_permission(statement_id="test-statement_id", remove_all_permissions="test-remove_all_permissions", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.remove_permission.assert_called_once()

def test_remove_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import remove_targets
    mock_client = MagicMock()
    mock_client.remove_targets.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    remove_targets("test-rule", "test-ids", event_bus_name="test-event_bus_name", force=True, region_name="us-east-1")
    mock_client.remove_targets.assert_called_once()

def test_start_replay_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import start_replay
    mock_client = MagicMock()
    mock_client.start_replay.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", "test-destination", description="test-description", region_name="us-east-1")
    mock_client.start_replay.assert_called_once()

def test_update_api_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import update_api_destination
    mock_client = MagicMock()
    mock_client.update_api_destination.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_api_destination("test-name", description="test-description", connection_arn="test-connection_arn", invocation_endpoint="test-invocation_endpoint", http_method="test-http_method", invocation_rate_limit_per_second=1, region_name="us-east-1")
    mock_client.update_api_destination.assert_called_once()

def test_update_archive_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import update_archive
    mock_client = MagicMock()
    mock_client.update_archive.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_archive("test-archive_name", description="test-description", event_pattern="test-event_pattern", retention_days="test-retention_days", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.update_archive.assert_called_once()

def test_update_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import update_connection
    mock_client = MagicMock()
    mock_client.update_connection.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_connection("test-name", description="test-description", authorization_type="test-authorization_type", auth_parameters="test-auth_parameters", invocation_connectivity_parameters="test-invocation_connectivity_parameters", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.update_connection.assert_called_once()

def test_update_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import update_endpoint
    mock_client = MagicMock()
    mock_client.update_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_endpoint("test-name", description="test-description", routing_config={}, replication_config={}, event_buses="test-event_buses", role_arn="test-role_arn", region_name="us-east-1")
    mock_client.update_endpoint.assert_called_once()

def test_update_event_bus_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eventbridge import update_event_bus
    mock_client = MagicMock()
    mock_client.update_event_bus.return_value = {}
    monkeypatch.setattr("aws_util.eventbridge.get_client", lambda *a, **kw: mock_client)
    update_event_bus(name="test-name", kms_key_identifier="test-kms_key_identifier", description="test-description", dead_letter_config={}, log_config={}, region_name="us-east-1")
    mock_client.update_event_bus.assert_called_once()
