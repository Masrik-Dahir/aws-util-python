"""Tests for aws_util.aio.forecast_query module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.forecast_query import (
    ForecastQueryResult,
    query_forecast,
    query_what_if_forecast,
)



REGION = "us-east-1"
FORECAST_ARN = "arn:aws:forecast:us-east-1:123:forecast/my-forecast"
WIF_ARN = "arn:aws:forecast:us-east-1:123:what-if-forecast/my-wif"
FILTERS = {"item_id": "item-001"}


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# query_forecast
# ---------------------------------------------------------------------------


async def test_query_forecast_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Forecast": {"Predictions": {"p50": []}},
    }
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)
    assert isinstance(result, ForecastQueryResult)
    assert "Predictions" in result.forecast


async def test_query_forecast_with_dates(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Forecast": {}}
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_forecast(
        FORECAST_ARN,
        FILTERS,
        start_date="2024-01-01",
        end_date="2024-01-31",
        region_name=REGION,
    )
    assert isinstance(result, ForecastQueryResult)


async def test_query_forecast_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)
    assert result.forecast == {}


async def test_query_forecast_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)


# ---------------------------------------------------------------------------
# query_what_if_forecast
# ---------------------------------------------------------------------------


async def test_query_what_if_forecast_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Forecast": {"Predictions": {"p90": []}},
    }
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
    assert isinstance(result, ForecastQueryResult)


async def test_query_what_if_forecast_with_dates(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Forecast": {}}
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_what_if_forecast(
        WIF_ARN,
        FILTERS,
        start_date="2024-01-01",
        end_date="2024-06-01",
        region_name=REGION,
    )
    assert isinstance(result, ForecastQueryResult)


async def test_query_what_if_forecast_empty(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    result = await query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
    assert result.forecast == {}


async def test_query_what_if_forecast_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.forecast_query.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
