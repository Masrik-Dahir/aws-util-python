from __future__ import annotations

import datetime
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.cloudwatch import (
    LogEvent,
    MetricDatum,
    MetricDimension,
    create_alarm,
    create_log_group,
    create_log_stream,
    get_log_events,
    get_metric_statistics,
    put_log_events,
    put_metric,
    put_metrics,
    tail_log_stream,
    delete_alarms,
    delete_anomaly_detector,
    delete_dashboards,
    delete_insight_rules,
    delete_metric_stream,
    describe_alarm_contributors,
    describe_alarm_history,
    describe_alarms,
    describe_alarms_for_metric,
    describe_anomaly_detectors,
    describe_insight_rules,
    disable_alarm_actions,
    disable_insight_rules,
    enable_alarm_actions,
    enable_insight_rules,
    get_dashboard,
    get_insight_rule_report,
    get_metric_data,
    get_metric_stream,
    get_metric_widget_image,
    list_dashboards,
    list_managed_insight_rules,
    list_metric_streams,
    list_metrics,
    list_tags_for_resource,
    put_anomaly_detector,
    put_composite_alarm,
    put_dashboard,
    put_insight_rule,
    put_managed_insight_rules,
    put_metric_alarm,
    put_metric_data,
    put_metric_stream,
    set_alarm_state,
    start_metric_streams,
    stop_metric_streams,
    tag_resource,
    untag_resource,
)


# ---------------------------------------------------------------------------
# put_metric / put_metrics
# ---------------------------------------------------------------------------


async def test_put_metric_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metric("NS", "MyMetric", 42.0)
    mock_client.call.assert_awaited_once()


async def test_put_metric_with_dimensions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    dims = [MetricDimension(name="Env", value="prod")]
    await put_metric("NS", "MyMetric", 1.0, dimensions=dims, unit="Count")
    mock_client.call.assert_awaited_once()


async def test_put_metric_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metric("NS", "M", 1.0, region_name="eu-west-1")
    mock_client.call.assert_awaited_once()


async def test_put_metrics_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    metrics = [MetricDatum(metric_name="M", value=1.0)]
    await put_metrics("NS", metrics)
    mock_client.call.assert_awaited_once()


async def test_put_metrics_chunking(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    metrics = [
        MetricDatum(metric_name=f"M{i}", value=float(i)) for i in range(25)
    ]
    await put_metrics("NS", metrics)
    assert mock_client.call.await_count == 2


async def test_put_metrics_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_metrics("NS", [MetricDatum(metric_name="M", value=1.0)])


async def test_put_metrics_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to put metrics"):
        await put_metrics("NS", [MetricDatum(metric_name="M", value=1.0)])


# ---------------------------------------------------------------------------
# create_log_group
# ---------------------------------------------------------------------------


async def test_create_log_group_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_log_group("/myapp/api")
    mock_client.call.assert_awaited_once()


async def test_create_log_group_already_exists(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceAlreadyExistsException"
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_log_group("/myapp/api")


async def test_create_log_group_other_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await create_log_group("/myapp/api")


# ---------------------------------------------------------------------------
# create_log_stream
# ---------------------------------------------------------------------------


async def test_create_log_stream_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_log_stream("/myapp", "stream-1")
    mock_client.call.assert_awaited_once()


async def test_create_log_stream_already_exists(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError(
        "ResourceAlreadyExistsException"
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_log_stream("/myapp", "stream-1")


async def test_create_log_stream_other_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("oops")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="oops"):
        await create_log_stream("/myapp", "stream-1")


# ---------------------------------------------------------------------------
# put_log_events
# ---------------------------------------------------------------------------


async def test_put_log_events_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    events = [LogEvent(timestamp=1000, message="hi")]
    await put_log_events("/grp", "stream", events)
    mock_client.call.assert_awaited_once()


async def test_put_log_events_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await put_log_events(
            "/grp", "stream", [LogEvent(timestamp=1, message="m")]
        )


async def test_put_log_events_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to put log events"):
        await put_log_events(
            "/grp", "stream", [LogEvent(timestamp=1, message="m")]
        )


# ---------------------------------------------------------------------------
# get_log_events
# ---------------------------------------------------------------------------


async def test_get_log_events_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "events": [{"timestamp": 100, "message": "hello"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_log_events("/grp", "stream")
    assert len(result) == 1
    assert result[0].message == "hello"


async def test_get_log_events_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_log_events("/grp", "stream")
    assert result == []


async def test_get_log_events_with_time_range(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"events": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_log_events(
        "/grp", "stream", start_time=100, end_time=200
    )
    assert result == []


async def test_get_log_events_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_log_events("/grp", "stream")


async def test_get_log_events_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to get log events"):
        await get_log_events("/grp", "stream")


# ---------------------------------------------------------------------------
# get_metric_statistics
# ---------------------------------------------------------------------------


async def test_get_metric_statistics_success(monkeypatch):
    mock_client = AsyncMock()
    t1 = datetime.datetime(2024, 1, 1, 0, 0)
    t2 = datetime.datetime(2024, 1, 1, 1, 0)
    mock_client.call.return_value = {
        "Datapoints": [
            {"Timestamp": t2, "Average": 10},
            {"Timestamp": t1, "Average": 5},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_metric_statistics("NS", "M", t1, t2)
    assert len(result) == 2
    assert result[0]["Timestamp"] == t1

async def test_get_metric_statistics_empty_datapoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    t1 = datetime.datetime(2024, 1, 1)
    t2 = datetime.datetime(2024, 1, 2)
    result = await get_metric_statistics("NS", "M", t1, t2)
    assert result == []


async def test_get_metric_statistics_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    t1 = datetime.datetime(2024, 1, 1)
    t2 = datetime.datetime(2024, 1, 2)
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_statistics("NS", "M", t1, t2)


async def test_get_metric_statistics_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    t1 = datetime.datetime(2024, 1, 1)
    t2 = datetime.datetime(2024, 1, 2)
    with pytest.raises(RuntimeError, match="get_metric_statistics failed"):
        await get_metric_statistics("NS", "M", t1, t2)


# ---------------------------------------------------------------------------
# create_alarm
# ---------------------------------------------------------------------------


async def test_create_alarm_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_alarm("MyAlarm", "NS", "M", 100.0)
    mock_client.call.assert_awaited_once()

async def test_create_alarm_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_alarm("A", "NS", "M", 1.0)


async def test_create_alarm_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_alarm failed"):
        await create_alarm("A", "NS", "M", 1.0)


# ---------------------------------------------------------------------------
# tail_log_stream
# ---------------------------------------------------------------------------


async def test_tail_log_stream_yields_events(monkeypatch):
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "events": [{"timestamp": 1, "message": "line1"}],
                "nextForwardToken": "tok1",
            }
        return {"events": [], "nextForwardToken": None}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.asyncio.sleep", AsyncMock()
    )

    collected = []
    async for event in tail_log_stream(
        "/grp", "stream", duration_seconds=0.01
    ):
        collected.append(event)
    assert any(e.message == "line1" for e in collected)


async def test_tail_log_stream_runtime_error_breaks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.asyncio.sleep", AsyncMock()
    )

    collected = []
    async for event in tail_log_stream(
        "/grp", "stream", duration_seconds=5.0
    ):
        collected.append(event)
    assert collected == []


async def test_tail_log_stream_no_next_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "events": [{"timestamp": 10, "message": "hi"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.asyncio.sleep", AsyncMock()
    )

    collected = []
    async for event in tail_log_stream(
        "/grp", "stream", duration_seconds=0.01
    ):
        collected.append(event)
    assert len(collected) >= 1


async def test_tail_log_stream_empty_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"events": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.asyncio.sleep", AsyncMock()
    )

    collected = []
    async for event in tail_log_stream(
        "/grp", "stream", duration_seconds=0.01
    ):
        collected.append(event)
    assert collected == []


async def test_delete_alarms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_alarms([], )
    mock_client.call.assert_called_once()


async def test_delete_alarms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_alarms([], )


async def test_delete_anomaly_detector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_anomaly_detector()
    mock_client.call.assert_called_once()


async def test_delete_anomaly_detector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_anomaly_detector()


async def test_delete_dashboards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dashboards([], )
    mock_client.call.assert_called_once()


async def test_delete_dashboards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dashboards([], )


async def test_delete_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_insight_rules([], )
    mock_client.call.assert_called_once()


async def test_delete_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_insight_rules([], )


async def test_delete_metric_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_metric_stream("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_metric_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_metric_stream("test-name", )


async def test_describe_alarm_contributors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_alarm_contributors("test-alarm_name", )
    mock_client.call.assert_called_once()


async def test_describe_alarm_contributors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_alarm_contributors("test-alarm_name", )


async def test_describe_alarm_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_alarm_history()
    mock_client.call.assert_called_once()


async def test_describe_alarm_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_alarm_history()


async def test_describe_alarms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_alarms()
    mock_client.call.assert_called_once()


async def test_describe_alarms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_alarms()


async def test_describe_alarms_for_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_alarms_for_metric("test-metric_name", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_alarms_for_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_alarms_for_metric("test-metric_name", "test-namespace", )


async def test_describe_anomaly_detectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_anomaly_detectors()
    mock_client.call.assert_called_once()


async def test_describe_anomaly_detectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_anomaly_detectors()


async def test_describe_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_insight_rules()
    mock_client.call.assert_called_once()


async def test_describe_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_insight_rules()


async def test_disable_alarm_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_alarm_actions([], )
    mock_client.call.assert_called_once()


async def test_disable_alarm_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_alarm_actions([], )


async def test_disable_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_insight_rules([], )
    mock_client.call.assert_called_once()


async def test_disable_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_insight_rules([], )


async def test_enable_alarm_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_alarm_actions([], )
    mock_client.call.assert_called_once()


async def test_enable_alarm_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_alarm_actions([], )


async def test_enable_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_insight_rules([], )
    mock_client.call.assert_called_once()


async def test_enable_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_insight_rules([], )


async def test_get_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dashboard("test-dashboard_name", )
    mock_client.call.assert_called_once()


async def test_get_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dashboard("test-dashboard_name", )


async def test_get_insight_rule_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_insight_rule_report("test-rule_name", "test-start_time", "test-end_time", 1, )
    mock_client.call.assert_called_once()


async def test_get_insight_rule_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_insight_rule_report("test-rule_name", "test-start_time", "test-end_time", 1, )


async def test_get_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_metric_data([], "test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_get_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_data([], "test-start_time", "test-end_time", )


async def test_get_metric_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_metric_stream("test-name", )
    mock_client.call.assert_called_once()


async def test_get_metric_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_stream("test-name", )


async def test_get_metric_widget_image(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_metric_widget_image("test-metric_widget", )
    mock_client.call.assert_called_once()


async def test_get_metric_widget_image_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_widget_image("test-metric_widget", )


async def test_list_dashboards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dashboards()
    mock_client.call.assert_called_once()


async def test_list_dashboards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dashboards()


async def test_list_managed_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_managed_insight_rules("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_managed_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_managed_insight_rules("test-resource_arn", )


async def test_list_metric_streams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_metric_streams()
    mock_client.call.assert_called_once()


async def test_list_metric_streams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_metric_streams()


async def test_list_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_metrics()
    mock_client.call.assert_called_once()


async def test_list_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_metrics()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_anomaly_detector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_anomaly_detector()
    mock_client.call.assert_called_once()


async def test_put_anomaly_detector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_anomaly_detector()


async def test_put_composite_alarm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_composite_alarm("test-alarm_name", "test-alarm_rule", )
    mock_client.call.assert_called_once()


async def test_put_composite_alarm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_composite_alarm("test-alarm_name", "test-alarm_rule", )


async def test_put_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_dashboard("test-dashboard_name", "test-dashboard_body", )
    mock_client.call.assert_called_once()


async def test_put_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_dashboard("test-dashboard_name", "test-dashboard_body", )


async def test_put_insight_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_insight_rule("test-rule_name", "test-rule_definition", )
    mock_client.call.assert_called_once()


async def test_put_insight_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_insight_rule("test-rule_name", "test-rule_definition", )


async def test_put_managed_insight_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_managed_insight_rules([], )
    mock_client.call.assert_called_once()


async def test_put_managed_insight_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_managed_insight_rules([], )


async def test_put_metric_alarm(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metric_alarm("test-alarm_name", 1, "test-comparison_operator", )
    mock_client.call.assert_called_once()


async def test_put_metric_alarm_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_metric_alarm("test-alarm_name", 1, "test-comparison_operator", )


async def test_put_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metric_data("test-namespace", )
    mock_client.call.assert_called_once()


async def test_put_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_metric_data("test-namespace", )


async def test_put_metric_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metric_stream("test-name", "test-firehose_arn", "test-role_arn", "test-output_format", )
    mock_client.call.assert_called_once()


async def test_put_metric_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_metric_stream("test-name", "test-firehose_arn", "test-role_arn", "test-output_format", )


async def test_set_alarm_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_alarm_state("test-alarm_name", "test-state_value", "test-state_reason", )
    mock_client.call.assert_called_once()


async def test_set_alarm_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_alarm_state("test-alarm_name", "test-state_value", "test-state_reason", )


async def test_start_metric_streams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_metric_streams([], )
    mock_client.call.assert_called_once()


async def test_start_metric_streams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_metric_streams([], )


async def test_stop_metric_streams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_metric_streams([], )
    mock_client.call.assert_called_once()


async def test_stop_metric_streams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_metric_streams([], )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudwatch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_get_log_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import get_log_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await get_log_events("test-log_group_name", "test-log_stream_name", start_time="test-start_time", end_time="test-end_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_anomaly_detector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import delete_anomaly_detector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await delete_anomaly_detector(namespace="test-namespace", metric_name="test-metric_name", dimensions="test-dimensions", stat="test-stat", single_metric_anomaly_detector="test-single_metric_anomaly_detector", metric_math_anomaly_detector="test-metric_math_anomaly_detector", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_alarm_contributors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_alarm_contributors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_alarm_contributors("test-alarm_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_alarm_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_alarm_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_alarm_history(alarm_name="test-alarm_name", alarm_contributor_id="test-alarm_contributor_id", alarm_types="test-alarm_types", history_item_type="test-history_item_type", start_date="test-start_date", end_date="test-end_date", max_records=1, next_token="test-next_token", scan_by="test-scan_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_alarms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_alarms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_alarms(alarm_names="test-alarm_names", alarm_name_prefix="test-alarm_name_prefix", alarm_types="test-alarm_types", children_of_alarm_name="test-children_of_alarm_name", parents_of_alarm_name="test-parents_of_alarm_name", state_value="test-state_value", action_prefix="test-action_prefix", max_records=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_alarms_for_metric_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_alarms_for_metric
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_alarms_for_metric("test-metric_name", "test-namespace", statistic="test-statistic", extended_statistic="test-extended_statistic", dimensions="test-dimensions", period="test-period", unit="test-unit", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_anomaly_detectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_anomaly_detectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_anomaly_detectors(next_token="test-next_token", max_results=1, namespace="test-namespace", metric_name="test-metric_name", dimensions="test-dimensions", anomaly_detector_types="test-anomaly_detector_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_insight_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import describe_insight_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await describe_insight_rules(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_insight_rule_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import get_insight_rule_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await get_insight_rule_report("test-rule_name", "test-start_time", "test-end_time", "test-period", max_contributor_count=1, metrics="test-metrics", order_by="test-order_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import get_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await get_metric_data("test-metric_data_queries", "test-start_time", "test-end_time", next_token="test-next_token", scan_by="test-scan_by", max_datapoints=1, label_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_metric_widget_image_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import get_metric_widget_image
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await get_metric_widget_image("test-metric_widget", output_format="test-output_format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dashboards_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import list_dashboards
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await list_dashboards(dashboard_name_prefix="test-dashboard_name_prefix", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_managed_insight_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import list_managed_insight_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await list_managed_insight_rules("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_metric_streams_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import list_metric_streams
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await list_metric_streams(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import list_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await list_metrics(namespace="test-namespace", metric_name="test-metric_name", dimensions="test-dimensions", next_token="test-next_token", recently_active="test-recently_active", include_linked_accounts=True, owning_account=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_anomaly_detector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_anomaly_detector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_anomaly_detector(namespace="test-namespace", metric_name="test-metric_name", dimensions="test-dimensions", stat="test-stat", configuration={}, metric_characteristics="test-metric_characteristics", single_metric_anomaly_detector="test-single_metric_anomaly_detector", metric_math_anomaly_detector="test-metric_math_anomaly_detector", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_composite_alarm_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_composite_alarm
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_composite_alarm("test-alarm_name", "test-alarm_rule", actions_enabled="test-actions_enabled", alarm_actions="test-alarm_actions", alarm_description="test-alarm_description", insufficient_data_actions="test-insufficient_data_actions", ok_actions="test-ok_actions", tags=[{"Key": "k", "Value": "v"}], actions_suppressor="test-actions_suppressor", actions_suppressor_wait_period="test-actions_suppressor_wait_period", actions_suppressor_extension_period="test-actions_suppressor_extension_period", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_insight_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_insight_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_insight_rule("test-rule_name", {}, rule_state="test-rule_state", tags=[{"Key": "k", "Value": "v"}], apply_on_transformed_logs=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_metric_alarm_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_metric_alarm
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_metric_alarm("test-alarm_name", "test-evaluation_periods", "test-comparison_operator", alarm_description="test-alarm_description", actions_enabled="test-actions_enabled", ok_actions="test-ok_actions", alarm_actions="test-alarm_actions", insufficient_data_actions="test-insufficient_data_actions", metric_name="test-metric_name", namespace="test-namespace", statistic="test-statistic", extended_statistic="test-extended_statistic", dimensions="test-dimensions", period="test-period", unit="test-unit", datapoints_to_alarm="test-datapoints_to_alarm", threshold="test-threshold", treat_missing_data="test-treat_missing_data", evaluate_low_sample_count_percentile=1, metrics="test-metrics", tags=[{"Key": "k", "Value": "v"}], threshold_metric_id="test-threshold_metric_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_metric_data("test-namespace", metric_data="test-metric_data", entity_metric_data="test-entity_metric_data", strict_entity_validation="test-strict_entity_validation", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_metric_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import put_metric_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await put_metric_stream("test-name", "test-firehose_arn", "test-role_arn", "test-output_format", include_filters=True, exclude_filters="test-exclude_filters", tags=[{"Key": "k", "Value": "v"}], statistics_configurations={}, include_linked_accounts_metrics=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_alarm_state_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import set_alarm_state
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await set_alarm_state("test-alarm_name", "test-state_value", "test-state_reason", state_reason_data="test-state_reason_data", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_alarm_with_dimensions(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import create_alarm
    from aws_util.cloudwatch import MetricDimension
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: mock_client)
    await create_alarm("test-alarm", "ns", "metric", 1.0, dimensions=[MetricDimension(name="k", value="v")], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_metric_statistics_with_dimensions(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudwatch import get_metric_statistics
    from aws_util.cloudwatch import MetricDimension
    from datetime import datetime, timedelta
    m = AsyncMock(); m.call = AsyncMock(return_value={"Datapoints": []})
    monkeypatch.setattr("aws_util.aio.cloudwatch.async_client", lambda *a, **kw: m)
    await get_metric_statistics("ns", "metric", datetime.now()-timedelta(hours=1), datetime.now(), 300, ["Average"], dimensions=[MetricDimension(name="k", value="v")], region_name="us-east-1")
