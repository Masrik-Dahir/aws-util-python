"""Tests for aws_util.aio.eventbridge — native async EventBridge utilities."""
from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.eventbridge import (
    EventEntry,
    PutEventsResult,
    list_rules,
    put_event,
    put_events,
    put_events_chunked,
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EVENT_BUS = "default"


def _make_entry(**overrides) -> EventEntry:
    defaults = {
        "source": "com.test.app",
        "detail_type": "TestEvent",
        "detail": {"key": "value"},
        "event_bus_name": EVENT_BUS,
        "resources": [],
    }
    defaults.update(overrides)
    return EventEntry(**defaults)


def _mock_client(return_value: dict | None = None) -> AsyncMock:
    mock = AsyncMock()
    if return_value is not None:
        mock.call.return_value = return_value
    return mock


# ---------------------------------------------------------------------------
# put_event
# ---------------------------------------------------------------------------


async def test_put_event_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """put_event delegates to put_events with a single entry."""
    captured: list[list[EventEntry]] = []

    async def fake_put_events(events, region_name=None):
        captured.append(events)
        return PutEventsResult(
            failed_count=0,
            successful_count=1,
            entries=[{"EventId": "eid-1"}],
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    result = await put_event(
        "com.app", "Order", {"id": 1}, resources=["arn:res"]
    )
    assert isinstance(result, PutEventsResult)
    assert result.successful_count == 1
    assert len(captured) == 1
    entry = captured[0][0]
    assert entry.source == "com.app"
    assert entry.detail_type == "Order"
    assert entry.detail == {"id": 1}
    assert entry.resources == ["arn:res"]
    assert entry.event_bus_name == "default"


async def test_put_event_no_resources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When resources is None, it defaults to []."""
    captured: list[list[EventEntry]] = []

    async def fake_put_events(events, region_name=None):
        captured.append(events)
        return PutEventsResult(
            failed_count=0, successful_count=1, entries=[]
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    await put_event("src", "dt", {})
    assert captured[0][0].resources == []


async def test_put_event_custom_bus_and_region(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_region: list = []

    async def fake_put_events(events, region_name=None):
        captured_region.append(region_name)
        return PutEventsResult(
            failed_count=0, successful_count=1, entries=[]
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    await put_event(
        "src", "dt", {}, event_bus_name="custom", region_name="us-west-2"
    )
    assert captured_region == ["us-west-2"]


# ---------------------------------------------------------------------------
# put_events
# ---------------------------------------------------------------------------


async def test_put_events_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = _mock_client(
        {
            "FailedEntryCount": 0,
            "Entries": [{"EventId": "e-1"}, {"EventId": "e-2"}],
        }
    )
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    entries = [_make_entry(), _make_entry(source="com.other")]
    result = await put_events(entries)
    assert isinstance(result, PutEventsResult)
    assert result.failed_count == 0
    assert result.successful_count == 2
    assert len(result.entries) == 2
    # Verify serialization
    api_entries = mock.call.call_args[1]["Entries"]
    assert api_entries[0]["Source"] == "com.test.app"
    assert api_entries[0]["Detail"] == json.dumps({"key": "value"})
    assert api_entries[0]["EventBusName"] == EVENT_BUS
    assert api_entries[0]["Resources"] == []


async def test_put_events_too_many() -> None:
    entries = [_make_entry() for _ in range(11)]
    with pytest.raises(ValueError, match="at most 10"):
        await put_events(entries)


async def test_put_events_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = AsyncMock()
    mock.call.side_effect = RuntimeError("api error")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="Failed to put events"):
        await put_events([_make_entry()])


async def test_put_events_partial_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = _mock_client(
        {
            "FailedEntryCount": 1,
            "Entries": [
                {"EventId": "e-ok"},
                {"ErrorCode": "InternalError", "ErrorMessage": "boom"},
            ],
        }
    )
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    # Partial failures return a result (only ALL-fail raises)
    result = await put_events([_make_entry(), _make_entry()])
    assert result.failed_count == 1
    assert result.successful_count == 1


async def test_put_events_zero_failed_no_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """FailedEntryCount = 0 should not raise."""
    mock = _mock_client(
        {
            "FailedEntryCount": 0,
            "Entries": [{"EventId": "e-1"}],
        }
    )
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    result = await put_events([_make_entry()])
    assert result.failed_count == 0


async def test_put_events_no_failed_entry_count_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When FailedEntryCount key is missing, defaults to 0."""
    mock = _mock_client(
        {
            "Entries": [{"EventId": "e-1"}],
        }
    )
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    result = await put_events([_make_entry()])
    assert result.failed_count == 0
    assert result.successful_count == 1


# ---------------------------------------------------------------------------
# put_events_chunked
# ---------------------------------------------------------------------------


async def test_put_events_chunked_single_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_counts: list[int] = []

    async def fake_put_events(events, region_name=None):
        call_counts.append(len(events))
        return PutEventsResult(
            failed_count=0,
            successful_count=len(events),
            entries=[],
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    entries = [_make_entry() for _ in range(5)]
    results = await put_events_chunked(entries)
    assert len(results) == 1
    assert call_counts == [5]


async def test_put_events_chunked_multiple_batches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_counts: list[int] = []

    async def fake_put_events(events, region_name=None):
        call_counts.append(len(events))
        return PutEventsResult(
            failed_count=0,
            successful_count=len(events),
            entries=[],
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    entries = [_make_entry() for _ in range(23)]
    results = await put_events_chunked(entries)
    assert len(results) == 3
    assert call_counts == [10, 10, 3]


async def test_put_events_chunked_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results = await put_events_chunked([])
    assert results == []


async def test_put_events_chunked_with_region(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_regions: list = []

    async def fake_put_events(events, region_name=None):
        captured_regions.append(region_name)
        return PutEventsResult(
            failed_count=0, successful_count=len(events), entries=[]
        )

    monkeypatch.setattr(
        "aws_util.aio.eventbridge.put_events", fake_put_events
    )
    await put_events_chunked(
        [_make_entry()], region_name="ap-southeast-1"
    )
    assert captured_regions == ["ap-southeast-1"]


# ---------------------------------------------------------------------------
# list_rules
# ---------------------------------------------------------------------------


async def test_list_rules_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = AsyncMock()
    mock.paginate.return_value = [
        {"Name": "rule-1", "State": "ENABLED"},
        {"Name": "rule-2", "State": "DISABLED"},
    ]
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    rules = await list_rules()
    assert len(rules) == 2
    assert rules[0]["Name"] == "rule-1"
    mock.paginate.assert_awaited_once_with(
        "ListRules", "Rules", EventBusName="default"
    )


async def test_list_rules_custom_bus(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = AsyncMock()
    mock.paginate.return_value = []
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    rules = await list_rules(event_bus_name="custom-bus")
    assert rules == []
    mock.paginate.assert_awaited_once_with(
        "ListRules", "Rules", EventBusName="custom-bus"
    )


async def test_put_events_all_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When ALL events fail (failed > 0, successful == 0), raise AwsServiceError."""
    mock = _mock_client(
        {
            "FailedEntryCount": 2,
            "Entries": [
                {"ErrorCode": "InternalError", "ErrorMessage": "boom"},
                {"ErrorCode": "InternalError", "ErrorMessage": "boom2"},
            ],
        }
    )
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="All 2 event"):
        await put_events([_make_entry(), _make_entry()])


async def test_list_rules_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = AsyncMock()
    mock.paginate.side_effect = RuntimeError("list fail")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="list_rules failed"):
        await list_rules()


async def test_activate_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await activate_event_source("test-name", )
    mock_client.call.assert_called_once()


async def test_activate_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await activate_event_source("test-name", )


async def test_cancel_replay(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_replay("test-replay_name", )
    mock_client.call.assert_called_once()


async def test_cancel_replay_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_replay("test-replay_name", )


async def test_create_api_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", )
    mock_client.call.assert_called_once()


async def test_create_api_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", )


async def test_create_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_archive("test-archive_name", "test-event_source_arn", )
    mock_client.call.assert_called_once()


async def test_create_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_archive("test-archive_name", "test-event_source_arn", )


async def test_create_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_connection("test-name", "test-authorization_type", {}, )
    mock_client.call.assert_called_once()


async def test_create_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_connection("test-name", "test-authorization_type", {}, )


async def test_create_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_endpoint("test-name", {}, [], )
    mock_client.call.assert_called_once()


async def test_create_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_endpoint("test-name", {}, [], )


async def test_create_event_bus(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_bus("test-name", )
    mock_client.call.assert_called_once()


async def test_create_event_bus_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_bus("test-name", )


async def test_create_partner_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_partner_event_source("test-name", "test-account", )
    mock_client.call.assert_called_once()


async def test_create_partner_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_partner_event_source("test-name", "test-account", )


async def test_deactivate_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_event_source("test-name", )
    mock_client.call.assert_called_once()


async def test_deactivate_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_event_source("test-name", )


async def test_deauthorize_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await deauthorize_connection("test-name", )
    mock_client.call.assert_called_once()


async def test_deauthorize_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deauthorize_connection("test-name", )


async def test_delete_api_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_api_destination("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_api_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_api_destination("test-name", )


async def test_delete_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_archive("test-archive_name", )
    mock_client.call.assert_called_once()


async def test_delete_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_archive("test-archive_name", )


async def test_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connection("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection("test-name", )


async def test_delete_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_endpoint("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_endpoint("test-name", )


async def test_delete_event_bus(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_bus("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_event_bus_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_bus("test-name", )


async def test_delete_partner_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_partner_event_source("test-name", "test-account", )
    mock_client.call.assert_called_once()


async def test_delete_partner_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_partner_event_source("test-name", "test-account", )


async def test_delete_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_rule("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_rule("test-name", )


async def test_describe_api_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_api_destination("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_api_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_api_destination("test-name", )


async def test_describe_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_archive("test-archive_name", )
    mock_client.call.assert_called_once()


async def test_describe_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_archive("test-archive_name", )


async def test_describe_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_connection("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_connection("test-name", )


async def test_describe_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint("test-name", )


async def test_describe_event_bus(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_bus()
    mock_client.call.assert_called_once()


async def test_describe_event_bus_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_bus()


async def test_describe_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_source("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_source("test-name", )


async def test_describe_partner_event_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_partner_event_source("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_partner_event_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_partner_event_source("test-name", )


async def test_describe_replay(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replay("test-replay_name", )
    mock_client.call.assert_called_once()


async def test_describe_replay_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replay("test-replay_name", )


async def test_describe_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_rule("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_rule("test-name", )


async def test_disable_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_rule("test-name", )
    mock_client.call.assert_called_once()


async def test_disable_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_rule("test-name", )


async def test_enable_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_rule("test-name", )
    mock_client.call.assert_called_once()


async def test_enable_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_rule("test-name", )


async def test_list_api_destinations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_api_destinations()
    mock_client.call.assert_called_once()


async def test_list_api_destinations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_api_destinations()


async def test_list_archives(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_archives()
    mock_client.call.assert_called_once()


async def test_list_archives_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_archives()


async def test_list_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_connections()
    mock_client.call.assert_called_once()


async def test_list_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_connections()


async def test_list_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_endpoints()
    mock_client.call.assert_called_once()


async def test_list_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_endpoints()


async def test_list_event_buses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_event_buses()
    mock_client.call.assert_called_once()


async def test_list_event_buses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_event_buses()


async def test_list_event_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_event_sources()
    mock_client.call.assert_called_once()


async def test_list_event_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_event_sources()


async def test_list_partner_event_source_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_partner_event_source_accounts("test-event_source_name", )
    mock_client.call.assert_called_once()


async def test_list_partner_event_source_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_partner_event_source_accounts("test-event_source_name", )


async def test_list_partner_event_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_partner_event_sources("test-name_prefix", )
    mock_client.call.assert_called_once()


async def test_list_partner_event_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_partner_event_sources("test-name_prefix", )


async def test_list_replays(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_replays()
    mock_client.call.assert_called_once()


async def test_list_replays_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_replays()


async def test_list_rule_names_by_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rule_names_by_target("test-target_arn", )
    mock_client.call.assert_called_once()


async def test_list_rule_names_by_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rule_names_by_target("test-target_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_targets_by_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_targets_by_rule("test-rule", )
    mock_client.call.assert_called_once()


async def test_list_targets_by_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_targets_by_rule("test-rule", )


async def test_put_partner_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_partner_events([], )
    mock_client.call.assert_called_once()


async def test_put_partner_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_partner_events([], )


async def test_put_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_permission()
    mock_client.call.assert_called_once()


async def test_put_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_permission()


async def test_put_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_rule("test-name", )
    mock_client.call.assert_called_once()


async def test_put_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_rule("test-name", )


async def test_put_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_targets("test-rule", [], )
    mock_client.call.assert_called_once()


async def test_put_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_targets("test-rule", [], )


async def test_remove_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_permission()
    mock_client.call.assert_called_once()


async def test_remove_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_permission()


async def test_remove_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_targets("test-rule", [], )
    mock_client.call.assert_called_once()


async def test_remove_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_targets("test-rule", [], )


async def test_run_event_pattern(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_event_pattern("test-event_pattern", "test-event", )
    mock_client.call.assert_called_once()


async def test_run_event_pattern_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_event_pattern("test-event_pattern", "test-event", )


async def test_start_replay(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", {}, )
    mock_client.call.assert_called_once()


async def test_start_replay_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", {}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_api_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_api_destination("test-name", )
    mock_client.call.assert_called_once()


async def test_update_api_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_api_destination("test-name", )


async def test_update_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_archive("test-archive_name", )
    mock_client.call.assert_called_once()


async def test_update_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_archive("test-archive_name", )


async def test_update_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_connection("test-name", )
    mock_client.call.assert_called_once()


async def test_update_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_connection("test-name", )


async def test_update_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_endpoint("test-name", )
    mock_client.call.assert_called_once()


async def test_update_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_endpoint("test-name", )


async def test_update_event_bus(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_event_bus()
    mock_client.call.assert_called_once()


async def test_update_event_bus_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eventbridge.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_event_bus()


@pytest.mark.asyncio
async def test_create_api_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import create_api_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await create_api_destination("test-name", "test-connection_arn", "test-invocation_endpoint", "test-http_method", description="test-description", invocation_rate_limit_per_second=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_archive_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import create_archive
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await create_archive("test-archive_name", "test-event_source_arn", description="test-description", event_pattern="test-event_pattern", retention_days="test-retention_days", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import create_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await create_connection("test-name", "test-authorization_type", "test-auth_parameters", description="test-description", invocation_connectivity_parameters="test-invocation_connectivity_parameters", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import create_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await create_endpoint("test-name", {}, "test-event_buses", description="test-description", replication_config={}, role_arn="test-role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_bus_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import create_event_bus
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await create_event_bus("test-name", event_source_name="test-event_source_name", description="test-description", kms_key_identifier="test-kms_key_identifier", dead_letter_config={}, log_config={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import delete_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await delete_rule("test-name", event_bus_name="test-event_bus_name", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import describe_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint("test-name", home_region="test-home_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_bus_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import describe_event_bus
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await describe_event_bus(name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import describe_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await describe_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import disable_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await disable_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import enable_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await enable_rule("test-name", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_api_destinations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_api_destinations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_api_destinations(name_prefix="test-name_prefix", connection_arn="test-connection_arn", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_archives_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_archives
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_archives(name_prefix="test-name_prefix", event_source_arn="test-event_source_arn", state="test-state", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_connections(name_prefix="test-name_prefix", connection_state="test-connection_state", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_endpoints(name_prefix="test-name_prefix", home_region="test-home_region", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_event_buses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_event_buses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_event_buses(name_prefix="test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_event_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_event_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_event_sources(name_prefix="test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_partner_event_source_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_partner_event_source_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_partner_event_source_accounts("test-event_source_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_partner_event_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_partner_event_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_partner_event_sources("test-name_prefix", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_replays_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_replays
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_replays(name_prefix="test-name_prefix", state="test-state", event_source_arn="test-event_source_arn", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rule_names_by_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_rule_names_by_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_rule_names_by_target("test-target_arn", event_bus_name="test-event_bus_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_targets_by_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import list_targets_by_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await list_targets_by_rule("test-rule", event_bus_name="test-event_bus_name", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import put_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await put_permission(event_bus_name="test-event_bus_name", action="test-action", principal="test-principal", statement_id="test-statement_id", condition="test-condition", policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import put_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await put_rule("test-name", schedule_expression="test-schedule_expression", event_pattern="test-event_pattern", state="test-state", description="test-description", role_arn="test-role_arn", tags=[{"Key": "k", "Value": "v"}], event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import put_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await put_targets("test-rule", "test-targets", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import remove_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await remove_permission(statement_id="test-statement_id", remove_all_permissions="test-remove_all_permissions", event_bus_name="test-event_bus_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import remove_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await remove_targets("test-rule", "test-ids", event_bus_name="test-event_bus_name", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_replay_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import start_replay
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await start_replay("test-replay_name", "test-event_source_arn", "test-event_start_time", "test-event_end_time", "test-destination", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_api_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import update_api_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await update_api_destination("test-name", description="test-description", connection_arn="test-connection_arn", invocation_endpoint="test-invocation_endpoint", http_method="test-http_method", invocation_rate_limit_per_second=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_archive_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import update_archive
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await update_archive("test-archive_name", description="test-description", event_pattern="test-event_pattern", retention_days="test-retention_days", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import update_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await update_connection("test-name", description="test-description", authorization_type="test-authorization_type", auth_parameters="test-auth_parameters", invocation_connectivity_parameters="test-invocation_connectivity_parameters", kms_key_identifier="test-kms_key_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import update_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await update_endpoint("test-name", description="test-description", routing_config={}, replication_config={}, event_buses="test-event_buses", role_arn="test-role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_event_bus_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eventbridge import update_event_bus
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eventbridge.async_client", lambda *a, **kw: mock_client)
    await update_event_bus(name="test-name", kms_key_identifier="test-kms_key_identifier", description="test-description", dead_letter_config={}, log_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()
