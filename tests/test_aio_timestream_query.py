"""Tests for aws_util.aio.timestream_query module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.timestream_query import (
    ColumnInfo,
    EndpointInfo,
    QueryResult,
    Row,
    ScheduledQueryDescription,
    cancel_query,
    create_scheduled_query,
    delete_scheduled_query,
    describe_endpoints,
    execute_scheduled_query,
    list_scheduled_queries,
    query,
    run_query,
    describe_account_settings,
    describe_scheduled_query,
    list_tags_for_resource,
    prepare_query,
    tag_resource,
    untag_resource,
    update_account_settings,
    update_scheduled_query,
)



REGION = "us-east-1"
QUERY_ID = "qid-12345"
SQ_ARN = "arn:aws:timestream:us-east-1:123:scheduled-query/my-sq"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# query
# ---------------------------------------------------------------------------


async def test_query_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "QueryId": QUERY_ID,
        "Rows": [{"Data": []}],
        "ColumnInfo": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await query("SELECT 1", region_name=REGION)
    assert result.query_id == QUERY_ID

async def test_query_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await query("BAD", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_endpoints
# ---------------------------------------------------------------------------


async def test_describe_endpoints_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Endpoints": [
            {"Address": "ep.example.com", "CachePeriodInMinutes": 5},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await describe_endpoints(region_name=REGION)
    assert len(result) == 1
    assert result[0].address == "ep.example.com"


async def test_describe_endpoints_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_endpoints(region_name=REGION)


# ---------------------------------------------------------------------------
# cancel_query
# ---------------------------------------------------------------------------


async def test_cancel_query_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await cancel_query(QUERY_ID, region_name=REGION)
    assert result is True


async def test_cancel_query_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await cancel_query(QUERY_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


async def test_run_query_single_page(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "QueryId": QUERY_ID,
        "Rows": [{"Data": [{"ScalarValue": "1"}]}],
        "ColumnInfo": [{"Name": "c", "Type": {"ScalarType": "BIGINT"}}],
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await run_query("SELECT 1", region_name=REGION)
    assert len(result.rows) == 1


async def test_run_query_multi_page(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "QueryId": QUERY_ID,
            "Rows": [{"Data": [{"ScalarValue": "1"}]}],
            "ColumnInfo": [{"Name": "c", "Type": {"ScalarType": "BIGINT"}}],
            "NextToken": "p2",
        },
        {
            "QueryId": QUERY_ID,
            "Rows": [{"Data": [{"ScalarValue": "2"}]}],
            "ColumnInfo": [],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await run_query("SELECT *", max_rows=1, region_name=REGION)
    assert len(result.rows) == 2


# ---------------------------------------------------------------------------
# create_scheduled_query
# ---------------------------------------------------------------------------


async def test_create_scheduled_query_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ScheduledQuery": {"Arn": SQ_ARN, "Name": "sq1"},
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await create_scheduled_query(
        "sq1", "SELECT 1", "rate(1 hour)", region_name=REGION,
    )
    assert result.arn == SQ_ARN


async def test_create_scheduled_query_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ScheduledQuery": {"Arn": SQ_ARN, "Name": "sq2"},
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await create_scheduled_query(
        "sq2",
        "SELECT 1",
        "rate(1 hour)",
        target_database="db",
        target_table="tbl",
        notification_sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
        scheduled_query_execution_role_arn="arn:aws:iam::123:role/r",
        tags=[{"Key": "env", "Value": "test"}],
        region_name=REGION,
    )
    assert result.arn == SQ_ARN


async def test_create_scheduled_query_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_scheduled_query(
            "sq", "SELECT 1", "rate(1 hour)", region_name=REGION,
        )


# ---------------------------------------------------------------------------
# list_scheduled_queries
# ---------------------------------------------------------------------------


async def test_list_scheduled_queries_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ScheduledQueries": [{"Arn": SQ_ARN, "Name": "sq1"}],
        "NextToken": "tok",
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    queries, token = await list_scheduled_queries(
        max_results=10, region_name=REGION,
    )
    assert len(queries) == 1
    assert token == "tok"


async def test_list_scheduled_queries_with_token(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ScheduledQueries": []}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    queries, token = await list_scheduled_queries(
        next_token="prev", region_name=REGION,
    )
    assert queries == []
    assert token is None


async def test_list_scheduled_queries_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_scheduled_queries(region_name=REGION)


# ---------------------------------------------------------------------------
# execute_scheduled_query
# ---------------------------------------------------------------------------


async def test_execute_scheduled_query_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await execute_scheduled_query(
        SQ_ARN, "2024-01-01T00:00:00Z", region_name=REGION,
    )
    assert result is True


async def test_execute_scheduled_query_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await execute_scheduled_query(
            SQ_ARN, "2024-01-01T00:00:00Z", region_name=REGION,
        )


# ---------------------------------------------------------------------------
# delete_scheduled_query
# ---------------------------------------------------------------------------


async def test_delete_scheduled_query_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    result = await delete_scheduled_query(SQ_ARN, region_name=REGION)
    assert result is True


async def test_delete_scheduled_query_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_scheduled_query(SQ_ARN, region_name=REGION)


async def test_describe_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_settings()
    mock_client.call.assert_called_once()


async def test_describe_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_settings()


async def test_describe_scheduled_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_query("test-scheduled_query_arn", )
    mock_client.call.assert_called_once()


async def test_describe_scheduled_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_query("test-scheduled_query_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_prepare_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await prepare_query("test-query_string", )
    mock_client.call.assert_called_once()


async def test_prepare_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await prepare_query("test-query_string", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_settings()
    mock_client.call.assert_called_once()


async def test_update_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_settings()


async def test_update_scheduled_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_scheduled_query("test-scheduled_query_arn", "test-state", )
    mock_client.call.assert_called_once()


async def test_update_scheduled_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_query.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_scheduled_query("test-scheduled_query_arn", "test-state", )


@pytest.mark.asyncio
async def test_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await query("test-query_string", max_rows=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_scheduled_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import create_scheduled_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await create_scheduled_query("test-name", "test-query_string", "test-schedule_expression", notification_sns_topic_arn="test-notification_sns_topic_arn", scheduled_query_execution_role_arn="test-scheduled_query_execution_role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_scheduled_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import list_scheduled_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await list_scheduled_queries(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_prepare_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import prepare_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await prepare_query("test-query_string", validate_only="test-validate_only", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_query import update_account_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_query.async_client", lambda *a, **kw: mock_client)
    await update_account_settings(max_query_tcu=1, query_pricing_model="test-query_pricing_model", query_compute="test-query_compute", region_name="us-east-1")
    mock_client.call.assert_called_once()
