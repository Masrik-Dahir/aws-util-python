"""Tests for aws_util.forecast_query module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.forecast_query import (
    ForecastQueryResult,
    query_forecast,
    query_what_if_forecast,
)

REGION = "us-east-1"
FORECAST_ARN = "arn:aws:forecast:us-east-1:123:forecast/my-forecast"
WIF_ARN = "arn:aws:forecast:us-east-1:123:what-if-forecast/my-wif"
FILTERS = {"item_id": "item-001"}


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_forecast_query_result_model():
    r = ForecastQueryResult(forecast={"p50": [1, 2, 3]})
    assert r.forecast == {"p50": [1, 2, 3]}


def test_forecast_query_result_default():
    r = ForecastQueryResult()
    assert r.forecast == {}


# ---------------------------------------------------------------------------
# query_forecast
# ---------------------------------------------------------------------------


@patch("aws_util.forecast_query.get_client")
def test_query_forecast_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_forecast.return_value = {
        "Forecast": {"Predictions": {"p50": [{"Timestamp": "2024-01-01", "Value": 42}]}},
    }
    result = query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)
    assert isinstance(result, ForecastQueryResult)
    assert "Predictions" in result.forecast


@patch("aws_util.forecast_query.get_client")
def test_query_forecast_with_dates(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_forecast.return_value = {"Forecast": {"p10": []}}
    result = query_forecast(
        FORECAST_ARN,
        FILTERS,
        start_date="2024-01-01",
        end_date="2024-01-31",
        region_name=REGION,
    )
    assert isinstance(result, ForecastQueryResult)


@patch("aws_util.forecast_query.get_client")
def test_query_forecast_empty(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_forecast.return_value = {}
    result = query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)
    assert result.forecast == {}


@patch("aws_util.forecast_query.get_client")
def test_query_forecast_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_forecast.side_effect = _client_error("ResourceNotFoundException")
    with pytest.raises(RuntimeError):
        query_forecast(FORECAST_ARN, FILTERS, region_name=REGION)


# ---------------------------------------------------------------------------
# query_what_if_forecast
# ---------------------------------------------------------------------------


@patch("aws_util.forecast_query.get_client")
def test_query_what_if_forecast_success(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_what_if_forecast.return_value = {
        "Forecast": {"Predictions": {"p90": []}},
    }
    result = query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
    assert isinstance(result, ForecastQueryResult)


@patch("aws_util.forecast_query.get_client")
def test_query_what_if_forecast_with_dates(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_what_if_forecast.return_value = {"Forecast": {}}
    result = query_what_if_forecast(
        WIF_ARN,
        FILTERS,
        start_date="2024-01-01",
        end_date="2024-06-01",
        region_name=REGION,
    )
    assert isinstance(result, ForecastQueryResult)


@patch("aws_util.forecast_query.get_client")
def test_query_what_if_forecast_empty(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_what_if_forecast.return_value = {}
    result = query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
    assert result.forecast == {}


@patch("aws_util.forecast_query.get_client")
def test_query_what_if_forecast_error(mock_gc: MagicMock):
    client = MagicMock()
    mock_gc.return_value = client
    client.query_what_if_forecast.side_effect = _client_error("InvalidInputException")
    with pytest.raises(RuntimeError):
        query_what_if_forecast(WIF_ARN, FILTERS, region_name=REGION)
