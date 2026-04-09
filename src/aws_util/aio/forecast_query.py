"""Native async Amazon Forecast Query utilities using the async engine."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.forecast_query import ForecastQueryResult

__all__ = [
    "ForecastQueryResult",
    "query_forecast",
    "query_what_if_forecast",
]


# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------


async def query_forecast(
    forecast_arn: str,
    filters: dict[str, str],
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    region_name: str | None = None,
) -> ForecastQueryResult:
    """Query a generated forecast for a specific item and time range.

    Args:
        forecast_arn: ARN of the forecast to query.
        filters: Key-value pairs identifying the item to forecast
            (e.g. ``{"item_id": "electricity_001"}``).
        start_date: Optional start date for the query window
            (ISO 8601 format).
        end_date: Optional end date for the query window
            (ISO 8601 format).
        region_name: AWS region override.

    Returns:
        A :class:`ForecastQueryResult` with the forecast data.

    Raises:
        RuntimeError: If the query fails.
    """
    client = async_client("forecastquery", region_name)
    kwargs: dict[str, Any] = {
        "ForecastArn": forecast_arn,
        "Filters": filters,
    }
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    try:
        resp = await client.call("QueryForecast", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "query_forecast failed") from exc
    return ForecastQueryResult(
        forecast=resp.get("Forecast", {}),
    )


async def query_what_if_forecast(
    what_if_forecast_arn: str,
    filters: dict[str, str],
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    region_name: str | None = None,
) -> ForecastQueryResult:
    """Query a what-if forecast for a specific item and time range.

    Args:
        what_if_forecast_arn: ARN of the what-if forecast to query.
        filters: Key-value pairs identifying the item to forecast.
        start_date: Optional start date for the query window
            (ISO 8601 format).
        end_date: Optional end date for the query window
            (ISO 8601 format).
        region_name: AWS region override.

    Returns:
        A :class:`ForecastQueryResult` with the forecast data.

    Raises:
        RuntimeError: If the query fails.
    """
    client = async_client("forecastquery", region_name)
    kwargs: dict[str, Any] = {
        "WhatIfForecastArn": what_if_forecast_arn,
        "Filters": filters,
    }
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    try:
        resp = await client.call("QueryWhatIfForecast", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "query_what_if_forecast failed") from exc
    return ForecastQueryResult(
        forecast=resp.get("Forecast", {}),
    )
