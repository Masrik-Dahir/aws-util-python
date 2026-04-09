"""aws_util.forecast_query — Amazon Forecast Query utilities.

Provides helpers for querying generated forecasts using the
``forecastquery`` service.

Boto3 docs: https://docs.aws.amazon.com/forecast/latest/dg/querying.html
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ForecastQueryResult",
    "query_forecast",
    "query_what_if_forecast",
]


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class ForecastQueryResult(BaseModel):
    """Result of a forecast query."""

    model_config = ConfigDict(populate_by_name=True)

    forecast: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------


def query_forecast(
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
    client = get_client("forecastquery", region_name)
    kwargs: dict[str, Any] = {
        "ForecastArn": forecast_arn,
        "Filters": filters,
    }
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    try:
        resp = client.query_forecast(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "query_forecast failed") from exc
    return ForecastQueryResult(
        forecast=resp.get("Forecast", {}),
    )


def query_what_if_forecast(
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
    client = get_client("forecastquery", region_name)
    kwargs: dict[str, Any] = {
        "WhatIfForecastArn": what_if_forecast_arn,
        "Filters": filters,
    }
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    try:
        resp = client.query_what_if_forecast(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "query_what_if_forecast failed") from exc
    return ForecastQueryResult(
        forecast=resp.get("Forecast", {}),
    )
