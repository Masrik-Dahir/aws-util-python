"""Native async Amazon Forecast utilities using the async engine."""

from __future__ import annotations

import asyncio
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error
from aws_util.forecast import (
    CreateAutoPredictorResult,
    CreateExplainabilityExportResult,
    CreateExplainabilityResult,
    CreateMonitorResult,
    CreatePredictorBacktestExportJobResult,
    CreateWhatIfAnalysisResult,
    CreateWhatIfForecastExportResult,
    CreateWhatIfForecastResult,
    DatasetGroupResult,
    DatasetImportJobResult,
    DatasetResult,
    DescribeAutoPredictorResult,
    DescribeDatasetGroupResult,
    DescribeExplainabilityExportResult,
    DescribeExplainabilityResult,
    DescribeMonitorResult,
    DescribePredictorBacktestExportJobResult,
    DescribeWhatIfAnalysisResult,
    DescribeWhatIfForecastExportResult,
    DescribeWhatIfForecastResult,
    ForecastExportJobResult,
    ForecastResult,
    GetAccuracyMetricsResult,
    ListDatasetGroupsResult,
    ListDatasetImportJobsResult,
    ListExplainabilitiesResult,
    ListExplainabilityExportsResult,
    ListForecastExportJobsResult,
    ListMonitorEvaluationsResult,
    ListMonitorsResult,
    ListPredictorBacktestExportJobsResult,
    ListPredictorsResult,
    ListTagsForResourceResult,
    ListWhatIfAnalysesResult,
    ListWhatIfForecastExportsResult,
    ListWhatIfForecastsResult,
    PredictorResult,
    _parse_dataset,
    _parse_forecast,
    _parse_predictor,
)

__all__ = [
    "CreateAutoPredictorResult",
    "CreateExplainabilityExportResult",
    "CreateExplainabilityResult",
    "CreateMonitorResult",
    "CreatePredictorBacktestExportJobResult",
    "CreateWhatIfAnalysisResult",
    "CreateWhatIfForecastExportResult",
    "CreateWhatIfForecastResult",
    "DatasetGroupResult",
    "DatasetImportJobResult",
    "DatasetResult",
    "DescribeAutoPredictorResult",
    "DescribeDatasetGroupResult",
    "DescribeExplainabilityExportResult",
    "DescribeExplainabilityResult",
    "DescribeMonitorResult",
    "DescribePredictorBacktestExportJobResult",
    "DescribeWhatIfAnalysisResult",
    "DescribeWhatIfForecastExportResult",
    "DescribeWhatIfForecastResult",
    "ForecastExportJobResult",
    "ForecastResult",
    "GetAccuracyMetricsResult",
    "ListDatasetGroupsResult",
    "ListDatasetImportJobsResult",
    "ListExplainabilitiesResult",
    "ListExplainabilityExportsResult",
    "ListForecastExportJobsResult",
    "ListMonitorEvaluationsResult",
    "ListMonitorsResult",
    "ListPredictorBacktestExportJobsResult",
    "ListPredictorsResult",
    "ListTagsForResourceResult",
    "ListWhatIfAnalysesResult",
    "ListWhatIfForecastExportsResult",
    "ListWhatIfForecastsResult",
    "PredictorResult",
    "create_auto_predictor",
    "create_dataset",
    "create_dataset_group",
    "create_dataset_import_job",
    "create_explainability",
    "create_explainability_export",
    "create_forecast",
    "create_forecast_export_job",
    "create_monitor",
    "create_predictor",
    "create_predictor_backtest_export_job",
    "create_what_if_analysis",
    "create_what_if_forecast",
    "create_what_if_forecast_export",
    "delete_dataset",
    "delete_dataset_group",
    "delete_dataset_import_job",
    "delete_explainability",
    "delete_explainability_export",
    "delete_forecast",
    "delete_forecast_export_job",
    "delete_monitor",
    "delete_predictor",
    "delete_predictor_backtest_export_job",
    "delete_resource_tree",
    "delete_what_if_analysis",
    "delete_what_if_forecast",
    "delete_what_if_forecast_export",
    "describe_auto_predictor",
    "describe_dataset",
    "describe_dataset_group",
    "describe_dataset_import_job",
    "describe_explainability",
    "describe_explainability_export",
    "describe_forecast",
    "describe_forecast_export_job",
    "describe_monitor",
    "describe_predictor",
    "describe_predictor_backtest_export_job",
    "describe_what_if_analysis",
    "describe_what_if_forecast",
    "describe_what_if_forecast_export",
    "get_accuracy_metrics",
    "list_dataset_groups",
    "list_dataset_import_jobs",
    "list_datasets",
    "list_explainabilities",
    "list_explainability_exports",
    "list_forecast_export_jobs",
    "list_forecasts",
    "list_monitor_evaluations",
    "list_monitors",
    "list_predictor_backtest_export_jobs",
    "list_predictors",
    "list_tags_for_resource",
    "list_what_if_analyses",
    "list_what_if_forecast_exports",
    "list_what_if_forecasts",
    "resume_resource",
    "stop_resource",
    "tag_resource",
    "untag_resource",
    "update_dataset_group",
    "wait_for_forecast",
    "wait_for_predictor",
]


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


async def create_dataset(
    dataset_name: str,
    domain: str,
    dataset_type: str,
    schema: dict[str, Any],
    *,
    data_frequency: str | None = None,
    region_name: str | None = None,
) -> DatasetResult:
    """Create an Amazon Forecast dataset.

    Args:
        dataset_name: Human-readable name for the dataset.
        domain: The forecast domain (e.g. ``"RETAIL"``, ``"CUSTOM"``).
        dataset_type: One of ``"TARGET_TIME_SERIES"``,
            ``"RELATED_TIME_SERIES"``, or ``"ITEM_METADATA"``.
        schema: The dataset schema definition.
        data_frequency: Data collection frequency (e.g. ``"D"``, ``"H"``).
        region_name: AWS region override.

    Returns:
        A :class:`DatasetResult` with the created dataset metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {
        "DatasetName": dataset_name,
        "Domain": domain,
        "DatasetType": dataset_type,
        "Schema": schema,
    }
    if data_frequency is not None:
        kwargs["DataFrequency"] = data_frequency
    try:
        resp = await client.call("CreateDataset", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_dataset failed") from exc
    return DatasetResult(
        dataset_arn=resp.get("DatasetArn", ""),
        dataset_name=dataset_name,
        domain=domain,
        dataset_type=dataset_type,
        data_frequency=data_frequency,
    )


async def describe_dataset(
    dataset_arn: str,
    *,
    region_name: str | None = None,
) -> DatasetResult:
    """Describe an Amazon Forecast dataset.

    Args:
        dataset_arn: ARN of the dataset to describe.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetResult` with the dataset metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call("DescribeDataset", DatasetArn=dataset_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_dataset failed") from exc
    return _parse_dataset(resp)


async def list_datasets(
    *,
    region_name: str | None = None,
) -> list[DatasetResult]:
    """List all Amazon Forecast datasets.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`DatasetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    results: list[DatasetResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListDatasets", **kwargs)
            for ds in resp.get("Datasets", []):
                results.append(
                    DatasetResult(
                        dataset_arn=ds.get("DatasetArn", ""),
                        dataset_name=ds.get("DatasetName"),
                        domain=ds.get("Domain"),
                        dataset_type=ds.get("DatasetType"),
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_datasets failed") from exc
    return results


# ---------------------------------------------------------------------------
# Dataset group operations
# ---------------------------------------------------------------------------


async def create_dataset_group(
    dataset_group_name: str,
    domain: str,
    *,
    dataset_arns: list[str] | None = None,
    region_name: str | None = None,
) -> DatasetGroupResult:
    """Create an Amazon Forecast dataset group.

    Args:
        dataset_group_name: Name for the dataset group.
        domain: The forecast domain (e.g. ``"RETAIL"``, ``"CUSTOM"``).
        dataset_arns: Optional list of dataset ARNs to include.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetGroupResult` with the created group metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {
        "DatasetGroupName": dataset_group_name,
        "Domain": domain,
    }
    if dataset_arns is not None:
        kwargs["DatasetArns"] = dataset_arns
    try:
        resp = await client.call("CreateDatasetGroup", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_dataset_group failed") from exc
    return DatasetGroupResult(
        dataset_group_arn=resp.get("DatasetGroupArn", ""),
        dataset_group_name=dataset_group_name,
        domain=domain,
        dataset_arns=dataset_arns or [],
    )


# ---------------------------------------------------------------------------
# Dataset import job operations
# ---------------------------------------------------------------------------


async def create_dataset_import_job(
    dataset_import_job_name: str,
    dataset_arn: str,
    data_source: dict[str, Any],
    *,
    timestamp_format: str | None = None,
    region_name: str | None = None,
) -> DatasetImportJobResult:
    """Create a dataset import job.

    Args:
        dataset_import_job_name: Name for the import job.
        dataset_arn: ARN of the target dataset.
        data_source: Data source configuration with S3 path and role ARN.
        timestamp_format: Optional timestamp format string.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetImportJobResult` with the import job metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {
        "DatasetImportJobName": dataset_import_job_name,
        "DatasetArn": dataset_arn,
        "DataSource": data_source,
    }
    if timestamp_format is not None:
        kwargs["TimestampFormat"] = timestamp_format
    try:
        resp = await client.call("CreateDatasetImportJob", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_dataset_import_job failed") from exc
    return DatasetImportJobResult(
        dataset_import_job_arn=resp.get("DatasetImportJobArn", ""),
        dataset_import_job_name=dataset_import_job_name,
        dataset_arn=dataset_arn,
    )


async def describe_dataset_import_job(
    dataset_import_job_arn: str,
    *,
    region_name: str | None = None,
) -> DatasetImportJobResult:
    """Describe a dataset import job.

    Args:
        dataset_import_job_arn: ARN of the import job.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetImportJobResult` with the import job metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call(
            "DescribeDatasetImportJob",
            DatasetImportJobArn=dataset_import_job_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_dataset_import_job failed") from exc
    return DatasetImportJobResult(
        dataset_import_job_arn=resp.get("DatasetImportJobArn", ""),
        dataset_import_job_name=resp.get("DatasetImportJobName"),
        dataset_arn=resp.get("DatasetArn"),
        status=resp.get("Status"),
        message=resp.get("Message"),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "DatasetImportJobArn",
                "DatasetImportJobName",
                "DatasetArn",
                "Status",
                "Message",
            }
        },
    )


# ---------------------------------------------------------------------------
# Predictor operations
# ---------------------------------------------------------------------------


async def create_predictor(
    predictor_name: str,
    forecast_horizon: int,
    *,
    dataset_group_arn: str | None = None,
    algorithm_arn: str | None = None,
    forecast_types: list[str] | None = None,
    perform_auto_ml: bool | None = None,
    input_data_config: dict[str, Any] | None = None,
    featurization_config: dict[str, Any] | None = None,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PredictorResult:
    """Create an Amazon Forecast predictor.

    Args:
        predictor_name: Name for the predictor.
        forecast_horizon: Number of time steps to forecast.
        dataset_group_arn: ARN of the dataset group to train on.
        algorithm_arn: ARN of the algorithm to use (omit for AutoML).
        forecast_types: Forecast quantile types (e.g. ``["0.1", "0.5", "0.9"]``).
        perform_auto_ml: Whether to use AutoML to select the algorithm.
        input_data_config: Input data configuration.
        featurization_config: Featurization configuration.
        extra_params: Additional API parameters to pass through.
        region_name: AWS region override.

    Returns:
        A :class:`PredictorResult` with the predictor metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {
        "PredictorName": predictor_name,
        "ForecastHorizon": forecast_horizon,
    }
    if dataset_group_arn is not None:
        kwargs["InputDataConfig"] = input_data_config or {
            "DatasetGroupArn": dataset_group_arn,
        }
    elif input_data_config is not None:
        kwargs["InputDataConfig"] = input_data_config
    if algorithm_arn is not None:
        kwargs["AlgorithmArn"] = algorithm_arn
    if forecast_types is not None:
        kwargs["ForecastTypes"] = forecast_types
    if perform_auto_ml is not None:
        kwargs["PerformAutoML"] = perform_auto_ml
    if featurization_config is not None:
        kwargs["FeaturizationConfig"] = featurization_config
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = await client.call("CreatePredictor", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_predictor failed") from exc
    return PredictorResult(
        predictor_arn=resp.get("PredictorArn", ""),
        predictor_name=predictor_name,
        forecast_horizon=forecast_horizon,
    )


async def describe_predictor(
    predictor_arn: str,
    *,
    region_name: str | None = None,
) -> PredictorResult:
    """Describe an Amazon Forecast predictor.

    Args:
        predictor_arn: ARN of the predictor.
        region_name: AWS region override.

    Returns:
        A :class:`PredictorResult` with the predictor metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call(
            "DescribePredictor",
            PredictorArn=predictor_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_predictor failed") from exc
    return _parse_predictor(resp)


# ---------------------------------------------------------------------------
# Forecast operations
# ---------------------------------------------------------------------------


async def create_forecast(
    forecast_name: str,
    predictor_arn: str,
    *,
    forecast_types: list[str] | None = None,
    region_name: str | None = None,
) -> ForecastResult:
    """Create an Amazon Forecast forecast.

    Args:
        forecast_name: Name for the forecast.
        predictor_arn: ARN of the predictor to generate the forecast from.
        forecast_types: Forecast quantile types (e.g. ``["0.1", "0.5", "0.9"]``).
        region_name: AWS region override.

    Returns:
        A :class:`ForecastResult` with the forecast metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {
        "ForecastName": forecast_name,
        "PredictorArn": predictor_arn,
    }
    if forecast_types is not None:
        kwargs["ForecastTypes"] = forecast_types
    try:
        resp = await client.call("CreateForecast", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_forecast failed") from exc
    return ForecastResult(
        forecast_arn=resp.get("ForecastArn", ""),
        forecast_name=forecast_name,
        predictor_arn=predictor_arn,
    )


async def describe_forecast(
    forecast_arn: str,
    *,
    region_name: str | None = None,
) -> ForecastResult:
    """Describe an Amazon Forecast forecast.

    Args:
        forecast_arn: ARN of the forecast.
        region_name: AWS region override.

    Returns:
        A :class:`ForecastResult` with the forecast metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call(
            "DescribeForecast",
            ForecastArn=forecast_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_forecast failed") from exc
    return _parse_forecast(resp)


async def create_forecast_export_job(
    forecast_export_job_name: str,
    forecast_arn: str,
    destination: dict[str, Any],
    *,
    region_name: str | None = None,
) -> ForecastExportJobResult:
    """Create a forecast export job.

    Args:
        forecast_export_job_name: Name for the export job.
        forecast_arn: ARN of the forecast to export.
        destination: S3 destination configuration with path and role ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ForecastExportJobResult` with the export job metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call(
            "CreateForecastExportJob",
            ForecastExportJobName=forecast_export_job_name,
            ForecastArn=forecast_arn,
            Destination=destination,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_forecast_export_job failed") from exc
    return ForecastExportJobResult(
        forecast_export_job_arn=resp.get("ForecastExportJobArn", ""),
        forecast_export_job_name=forecast_export_job_name,
        forecast_arn=forecast_arn,
    )


async def describe_forecast_export_job(
    forecast_export_job_arn: str,
    *,
    region_name: str | None = None,
) -> ForecastExportJobResult:
    """Describe a forecast export job.

    Args:
        forecast_export_job_arn: ARN of the export job.
        region_name: AWS region override.

    Returns:
        A :class:`ForecastExportJobResult` with the export job metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    try:
        resp = await client.call(
            "DescribeForecastExportJob",
            ForecastExportJobArn=forecast_export_job_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_forecast_export_job failed") from exc
    return ForecastExportJobResult(
        forecast_export_job_arn=resp.get("ForecastExportJobArn", ""),
        forecast_export_job_name=resp.get("ForecastExportJobName"),
        forecast_arn=resp.get("ForecastArn"),
        status=resp.get("Status"),
        message=resp.get("Message"),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "ForecastExportJobArn",
                "ForecastExportJobName",
                "ForecastArn",
                "Status",
                "Message",
            }
        },
    )


async def list_forecasts(
    *,
    region_name: str | None = None,
) -> list[ForecastResult]:
    """List all Amazon Forecast forecasts.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ForecastResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    results: list[ForecastResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListForecasts", **kwargs)
            for fc in resp.get("Forecasts", []):
                results.append(
                    ForecastResult(
                        forecast_arn=fc.get("ForecastArn", ""),
                        forecast_name=fc.get("ForecastName"),
                        predictor_arn=fc.get("PredictorArn"),
                        dataset_group_arn=fc.get("DatasetGroupArn"),
                        status=fc.get("Status"),
                        message=fc.get("Message"),
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_forecasts failed") from exc
    return results


# ---------------------------------------------------------------------------
# Resource cleanup
# ---------------------------------------------------------------------------


async def delete_resource_tree(
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Forecast resource and all dependent child resources.

    Args:
        resource_arn: ARN of the root resource to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    client = async_client("forecast", region_name)
    try:
        await client.call("DeleteResourceTree", ResourceArn=resource_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "delete_resource_tree failed") from exc


# ---------------------------------------------------------------------------
# Polling / waiters
# ---------------------------------------------------------------------------


async def wait_for_predictor(
    predictor_arn: str,
    *,
    target_status: str = "ACTIVE",
    timeout: float = 3600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> PredictorResult:
    """Poll until a predictor reaches *target_status*.

    Args:
        predictor_arn: ARN of the predictor to wait for.
        target_status: Status to wait for (default ``"ACTIVE"``).
        timeout: Maximum wait time in seconds (default 3600).
        poll_interval: Seconds between polls (default 30).
        region_name: AWS region override.

    Returns:
        The :class:`PredictorResult` once the target status is reached.

    Raises:
        AwsTimeoutError: If the timeout is exceeded.
        RuntimeError: If the predictor enters a ``FAILED`` state or the
            describe call fails.
    """
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = await describe_predictor(
            predictor_arn,
            region_name=region_name,
        )
        if result.status == target_status:
            return result
        if result.status == "FAILED":
            raise wrap_aws_error(
                RuntimeError(f"Predictor {predictor_arn!r} failed: {result.message}"),
            )
        await asyncio.sleep(poll_interval)
    raise AwsTimeoutError(
        f"Predictor {predictor_arn!r} did not reach {target_status!r} within {timeout}s"
    )


async def wait_for_forecast(
    forecast_arn: str,
    *,
    target_status: str = "ACTIVE",
    timeout: float = 3600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> ForecastResult:
    """Poll until a forecast reaches *target_status*.

    Args:
        forecast_arn: ARN of the forecast to wait for.
        target_status: Status to wait for (default ``"ACTIVE"``).
        timeout: Maximum wait time in seconds (default 3600).
        poll_interval: Seconds between polls (default 30).
        region_name: AWS region override.

    Returns:
        The :class:`ForecastResult` once the target status is reached.

    Raises:
        AwsTimeoutError: If the timeout is exceeded.
        RuntimeError: If the forecast enters a ``FAILED`` state or the
            describe call fails.
    """
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = await describe_forecast(
            forecast_arn,
            region_name=region_name,
        )
        if result.status == target_status:
            return result
        if result.status == "FAILED":
            raise wrap_aws_error(
                RuntimeError(f"Forecast {forecast_arn!r} failed: {result.message}"),
            )
        await asyncio.sleep(poll_interval)
    raise AwsTimeoutError(
        f"Forecast {forecast_arn!r} did not reach {target_status!r} within {timeout}s"
    )


async def create_auto_predictor(
    predictor_name: str,
    *,
    forecast_horizon: int | None = None,
    forecast_types: list[str] | None = None,
    forecast_dimensions: list[str] | None = None,
    forecast_frequency: str | None = None,
    data_config: dict[str, Any] | None = None,
    encryption_config: dict[str, Any] | None = None,
    reference_predictor_arn: str | None = None,
    optimization_metric: str | None = None,
    explain_predictor: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    monitor_config: dict[str, Any] | None = None,
    time_alignment_boundary: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAutoPredictorResult:
    """Create auto predictor.

    Args:
        predictor_name: Predictor name.
        forecast_horizon: Forecast horizon.
        forecast_types: Forecast types.
        forecast_dimensions: Forecast dimensions.
        forecast_frequency: Forecast frequency.
        data_config: Data config.
        encryption_config: Encryption config.
        reference_predictor_arn: Reference predictor arn.
        optimization_metric: Optimization metric.
        explain_predictor: Explain predictor.
        tags: Tags.
        monitor_config: Monitor config.
        time_alignment_boundary: Time alignment boundary.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorName"] = predictor_name
    if forecast_horizon is not None:
        kwargs["ForecastHorizon"] = forecast_horizon
    if forecast_types is not None:
        kwargs["ForecastTypes"] = forecast_types
    if forecast_dimensions is not None:
        kwargs["ForecastDimensions"] = forecast_dimensions
    if forecast_frequency is not None:
        kwargs["ForecastFrequency"] = forecast_frequency
    if data_config is not None:
        kwargs["DataConfig"] = data_config
    if encryption_config is not None:
        kwargs["EncryptionConfig"] = encryption_config
    if reference_predictor_arn is not None:
        kwargs["ReferencePredictorArn"] = reference_predictor_arn
    if optimization_metric is not None:
        kwargs["OptimizationMetric"] = optimization_metric
    if explain_predictor is not None:
        kwargs["ExplainPredictor"] = explain_predictor
    if tags is not None:
        kwargs["Tags"] = tags
    if monitor_config is not None:
        kwargs["MonitorConfig"] = monitor_config
    if time_alignment_boundary is not None:
        kwargs["TimeAlignmentBoundary"] = time_alignment_boundary
    try:
        resp = await client.call("CreateAutoPredictor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create auto predictor") from exc
    return CreateAutoPredictorResult(
        predictor_arn=resp.get("PredictorArn"),
    )


async def create_explainability(
    explainability_name: str,
    resource_arn: str,
    explainability_config: dict[str, Any],
    *,
    data_source: dict[str, Any] | None = None,
    schema: dict[str, Any] | None = None,
    enable_visualization: bool | None = None,
    start_date_time: str | None = None,
    end_date_time: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateExplainabilityResult:
    """Create explainability.

    Args:
        explainability_name: Explainability name.
        resource_arn: Resource arn.
        explainability_config: Explainability config.
        data_source: Data source.
        schema: Schema.
        enable_visualization: Enable visualization.
        start_date_time: Start date time.
        end_date_time: End date time.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityName"] = explainability_name
    kwargs["ResourceArn"] = resource_arn
    kwargs["ExplainabilityConfig"] = explainability_config
    if data_source is not None:
        kwargs["DataSource"] = data_source
    if schema is not None:
        kwargs["Schema"] = schema
    if enable_visualization is not None:
        kwargs["EnableVisualization"] = enable_visualization
    if start_date_time is not None:
        kwargs["StartDateTime"] = start_date_time
    if end_date_time is not None:
        kwargs["EndDateTime"] = end_date_time
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateExplainability", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create explainability") from exc
    return CreateExplainabilityResult(
        explainability_arn=resp.get("ExplainabilityArn"),
    )


async def create_explainability_export(
    explainability_export_name: str,
    explainability_arn: str,
    destination: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    format: str | None = None,
    region_name: str | None = None,
) -> CreateExplainabilityExportResult:
    """Create explainability export.

    Args:
        explainability_export_name: Explainability export name.
        explainability_arn: Explainability arn.
        destination: Destination.
        tags: Tags.
        format: Format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityExportName"] = explainability_export_name
    kwargs["ExplainabilityArn"] = explainability_arn
    kwargs["Destination"] = destination
    if tags is not None:
        kwargs["Tags"] = tags
    if format is not None:
        kwargs["Format"] = format
    try:
        resp = await client.call("CreateExplainabilityExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create explainability export") from exc
    return CreateExplainabilityExportResult(
        explainability_export_arn=resp.get("ExplainabilityExportArn"),
    )


async def create_monitor(
    monitor_name: str,
    resource_arn: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMonitorResult:
    """Create monitor.

    Args:
        monitor_name: Monitor name.
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MonitorName"] = monitor_name
    kwargs["ResourceArn"] = resource_arn
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateMonitor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create monitor") from exc
    return CreateMonitorResult(
        monitor_arn=resp.get("MonitorArn"),
    )


async def create_predictor_backtest_export_job(
    predictor_backtest_export_job_name: str,
    predictor_arn: str,
    destination: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    format: str | None = None,
    region_name: str | None = None,
) -> CreatePredictorBacktestExportJobResult:
    """Create predictor backtest export job.

    Args:
        predictor_backtest_export_job_name: Predictor backtest export job name.
        predictor_arn: Predictor arn.
        destination: Destination.
        tags: Tags.
        format: Format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorBacktestExportJobName"] = predictor_backtest_export_job_name
    kwargs["PredictorArn"] = predictor_arn
    kwargs["Destination"] = destination
    if tags is not None:
        kwargs["Tags"] = tags
    if format is not None:
        kwargs["Format"] = format
    try:
        resp = await client.call("CreatePredictorBacktestExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create predictor backtest export job") from exc
    return CreatePredictorBacktestExportJobResult(
        predictor_backtest_export_job_arn=resp.get("PredictorBacktestExportJobArn"),
    )


async def create_what_if_analysis(
    what_if_analysis_name: str,
    forecast_arn: str,
    *,
    time_series_selector: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateWhatIfAnalysisResult:
    """Create what if analysis.

    Args:
        what_if_analysis_name: What if analysis name.
        forecast_arn: Forecast arn.
        time_series_selector: Time series selector.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfAnalysisName"] = what_if_analysis_name
    kwargs["ForecastArn"] = forecast_arn
    if time_series_selector is not None:
        kwargs["TimeSeriesSelector"] = time_series_selector
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateWhatIfAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create what if analysis") from exc
    return CreateWhatIfAnalysisResult(
        what_if_analysis_arn=resp.get("WhatIfAnalysisArn"),
    )


async def create_what_if_forecast(
    what_if_forecast_name: str,
    what_if_analysis_arn: str,
    *,
    time_series_transformations: list[dict[str, Any]] | None = None,
    time_series_replacements_data_source: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateWhatIfForecastResult:
    """Create what if forecast.

    Args:
        what_if_forecast_name: What if forecast name.
        what_if_analysis_arn: What if analysis arn.
        time_series_transformations: Time series transformations.
        time_series_replacements_data_source: Time series replacements data source.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastName"] = what_if_forecast_name
    kwargs["WhatIfAnalysisArn"] = what_if_analysis_arn
    if time_series_transformations is not None:
        kwargs["TimeSeriesTransformations"] = time_series_transformations
    if time_series_replacements_data_source is not None:
        kwargs["TimeSeriesReplacementsDataSource"] = time_series_replacements_data_source
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateWhatIfForecast", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create what if forecast") from exc
    return CreateWhatIfForecastResult(
        what_if_forecast_arn=resp.get("WhatIfForecastArn"),
    )


async def create_what_if_forecast_export(
    what_if_forecast_export_name: str,
    what_if_forecast_arns: list[str],
    destination: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    format: str | None = None,
    region_name: str | None = None,
) -> CreateWhatIfForecastExportResult:
    """Create what if forecast export.

    Args:
        what_if_forecast_export_name: What if forecast export name.
        what_if_forecast_arns: What if forecast arns.
        destination: Destination.
        tags: Tags.
        format: Format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastExportName"] = what_if_forecast_export_name
    kwargs["WhatIfForecastArns"] = what_if_forecast_arns
    kwargs["Destination"] = destination
    if tags is not None:
        kwargs["Tags"] = tags
    if format is not None:
        kwargs["Format"] = format
    try:
        resp = await client.call("CreateWhatIfForecastExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create what if forecast export") from exc
    return CreateWhatIfForecastExportResult(
        what_if_forecast_export_arn=resp.get("WhatIfForecastExportArn"),
    )


async def delete_dataset(
    dataset_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset.

    Args:
        dataset_arn: Dataset arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetArn"] = dataset_arn
    try:
        await client.call("DeleteDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset") from exc
    return None


async def delete_dataset_group(
    dataset_group_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset group.

    Args:
        dataset_group_arn: Dataset group arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetGroupArn"] = dataset_group_arn
    try:
        await client.call("DeleteDatasetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset group") from exc
    return None


async def delete_dataset_import_job(
    dataset_import_job_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset import job.

    Args:
        dataset_import_job_arn: Dataset import job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetImportJobArn"] = dataset_import_job_arn
    try:
        await client.call("DeleteDatasetImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset import job") from exc
    return None


async def delete_explainability(
    explainability_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete explainability.

    Args:
        explainability_arn: Explainability arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityArn"] = explainability_arn
    try:
        await client.call("DeleteExplainability", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete explainability") from exc
    return None


async def delete_explainability_export(
    explainability_export_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete explainability export.

    Args:
        explainability_export_arn: Explainability export arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityExportArn"] = explainability_export_arn
    try:
        await client.call("DeleteExplainabilityExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete explainability export") from exc
    return None


async def delete_forecast(
    forecast_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete forecast.

    Args:
        forecast_arn: Forecast arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ForecastArn"] = forecast_arn
    try:
        await client.call("DeleteForecast", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete forecast") from exc
    return None


async def delete_forecast_export_job(
    forecast_export_job_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete forecast export job.

    Args:
        forecast_export_job_arn: Forecast export job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ForecastExportJobArn"] = forecast_export_job_arn
    try:
        await client.call("DeleteForecastExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete forecast export job") from exc
    return None


async def delete_monitor(
    monitor_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete monitor.

    Args:
        monitor_arn: Monitor arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MonitorArn"] = monitor_arn
    try:
        await client.call("DeleteMonitor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete monitor") from exc
    return None


async def delete_predictor(
    predictor_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete predictor.

    Args:
        predictor_arn: Predictor arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorArn"] = predictor_arn
    try:
        await client.call("DeletePredictor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete predictor") from exc
    return None


async def delete_predictor_backtest_export_job(
    predictor_backtest_export_job_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete predictor backtest export job.

    Args:
        predictor_backtest_export_job_arn: Predictor backtest export job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorBacktestExportJobArn"] = predictor_backtest_export_job_arn
    try:
        await client.call("DeletePredictorBacktestExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete predictor backtest export job") from exc
    return None


async def delete_what_if_analysis(
    what_if_analysis_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete what if analysis.

    Args:
        what_if_analysis_arn: What if analysis arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfAnalysisArn"] = what_if_analysis_arn
    try:
        await client.call("DeleteWhatIfAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete what if analysis") from exc
    return None


async def delete_what_if_forecast(
    what_if_forecast_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete what if forecast.

    Args:
        what_if_forecast_arn: What if forecast arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastArn"] = what_if_forecast_arn
    try:
        await client.call("DeleteWhatIfForecast", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete what if forecast") from exc
    return None


async def delete_what_if_forecast_export(
    what_if_forecast_export_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete what if forecast export.

    Args:
        what_if_forecast_export_arn: What if forecast export arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastExportArn"] = what_if_forecast_export_arn
    try:
        await client.call("DeleteWhatIfForecastExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete what if forecast export") from exc
    return None


async def describe_auto_predictor(
    predictor_arn: str,
    region_name: str | None = None,
) -> DescribeAutoPredictorResult:
    """Describe auto predictor.

    Args:
        predictor_arn: Predictor arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorArn"] = predictor_arn
    try:
        resp = await client.call("DescribeAutoPredictor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe auto predictor") from exc
    return DescribeAutoPredictorResult(
        predictor_arn=resp.get("PredictorArn"),
        predictor_name=resp.get("PredictorName"),
        forecast_horizon=resp.get("ForecastHorizon"),
        forecast_types=resp.get("ForecastTypes"),
        forecast_frequency=resp.get("ForecastFrequency"),
        forecast_dimensions=resp.get("ForecastDimensions"),
        dataset_import_job_arns=resp.get("DatasetImportJobArns"),
        data_config=resp.get("DataConfig"),
        encryption_config=resp.get("EncryptionConfig"),
        reference_predictor_summary=resp.get("ReferencePredictorSummary"),
        estimated_time_remaining_in_minutes=resp.get("EstimatedTimeRemainingInMinutes"),
        status=resp.get("Status"),
        message=resp.get("Message"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        optimization_metric=resp.get("OptimizationMetric"),
        explainability_info=resp.get("ExplainabilityInfo"),
        monitor_info=resp.get("MonitorInfo"),
        time_alignment_boundary=resp.get("TimeAlignmentBoundary"),
    )


async def describe_dataset_group(
    dataset_group_arn: str,
    region_name: str | None = None,
) -> DescribeDatasetGroupResult:
    """Describe dataset group.

    Args:
        dataset_group_arn: Dataset group arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetGroupArn"] = dataset_group_arn
    try:
        resp = await client.call("DescribeDatasetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset group") from exc
    return DescribeDatasetGroupResult(
        dataset_group_name=resp.get("DatasetGroupName"),
        dataset_group_arn=resp.get("DatasetGroupArn"),
        dataset_arns=resp.get("DatasetArns"),
        domain=resp.get("Domain"),
        status=resp.get("Status"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
    )


async def describe_explainability(
    explainability_arn: str,
    region_name: str | None = None,
) -> DescribeExplainabilityResult:
    """Describe explainability.

    Args:
        explainability_arn: Explainability arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityArn"] = explainability_arn
    try:
        resp = await client.call("DescribeExplainability", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe explainability") from exc
    return DescribeExplainabilityResult(
        explainability_arn=resp.get("ExplainabilityArn"),
        explainability_name=resp.get("ExplainabilityName"),
        resource_arn=resp.get("ResourceArn"),
        explainability_config=resp.get("ExplainabilityConfig"),
        enable_visualization=resp.get("EnableVisualization"),
        data_source=resp.get("DataSource"),
        model_schema=resp.get("Schema"),
        start_date_time=resp.get("StartDateTime"),
        end_date_time=resp.get("EndDateTime"),
        estimated_time_remaining_in_minutes=resp.get("EstimatedTimeRemainingInMinutes"),
        message=resp.get("Message"),
        status=resp.get("Status"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
    )


async def describe_explainability_export(
    explainability_export_arn: str,
    region_name: str | None = None,
) -> DescribeExplainabilityExportResult:
    """Describe explainability export.

    Args:
        explainability_export_arn: Explainability export arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExplainabilityExportArn"] = explainability_export_arn
    try:
        resp = await client.call("DescribeExplainabilityExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe explainability export") from exc
    return DescribeExplainabilityExportResult(
        explainability_export_arn=resp.get("ExplainabilityExportArn"),
        explainability_export_name=resp.get("ExplainabilityExportName"),
        explainability_arn=resp.get("ExplainabilityArn"),
        destination=resp.get("Destination"),
        message=resp.get("Message"),
        status=resp.get("Status"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        format=resp.get("Format"),
    )


async def describe_monitor(
    monitor_arn: str,
    region_name: str | None = None,
) -> DescribeMonitorResult:
    """Describe monitor.

    Args:
        monitor_arn: Monitor arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MonitorArn"] = monitor_arn
    try:
        resp = await client.call("DescribeMonitor", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe monitor") from exc
    return DescribeMonitorResult(
        monitor_name=resp.get("MonitorName"),
        monitor_arn=resp.get("MonitorArn"),
        resource_arn=resp.get("ResourceArn"),
        status=resp.get("Status"),
        last_evaluation_time=resp.get("LastEvaluationTime"),
        last_evaluation_state=resp.get("LastEvaluationState"),
        baseline=resp.get("Baseline"),
        message=resp.get("Message"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        estimated_evaluation_time_remaining_in_minutes=resp.get(
            "EstimatedEvaluationTimeRemainingInMinutes"
        ),
    )


async def describe_predictor_backtest_export_job(
    predictor_backtest_export_job_arn: str,
    region_name: str | None = None,
) -> DescribePredictorBacktestExportJobResult:
    """Describe predictor backtest export job.

    Args:
        predictor_backtest_export_job_arn: Predictor backtest export job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorBacktestExportJobArn"] = predictor_backtest_export_job_arn
    try:
        resp = await client.call("DescribePredictorBacktestExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe predictor backtest export job") from exc
    return DescribePredictorBacktestExportJobResult(
        predictor_backtest_export_job_arn=resp.get("PredictorBacktestExportJobArn"),
        predictor_backtest_export_job_name=resp.get("PredictorBacktestExportJobName"),
        predictor_arn=resp.get("PredictorArn"),
        destination=resp.get("Destination"),
        message=resp.get("Message"),
        status=resp.get("Status"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        format=resp.get("Format"),
    )


async def describe_what_if_analysis(
    what_if_analysis_arn: str,
    region_name: str | None = None,
) -> DescribeWhatIfAnalysisResult:
    """Describe what if analysis.

    Args:
        what_if_analysis_arn: What if analysis arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfAnalysisArn"] = what_if_analysis_arn
    try:
        resp = await client.call("DescribeWhatIfAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe what if analysis") from exc
    return DescribeWhatIfAnalysisResult(
        what_if_analysis_name=resp.get("WhatIfAnalysisName"),
        what_if_analysis_arn=resp.get("WhatIfAnalysisArn"),
        forecast_arn=resp.get("ForecastArn"),
        estimated_time_remaining_in_minutes=resp.get("EstimatedTimeRemainingInMinutes"),
        status=resp.get("Status"),
        message=resp.get("Message"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        time_series_selector=resp.get("TimeSeriesSelector"),
    )


async def describe_what_if_forecast(
    what_if_forecast_arn: str,
    region_name: str | None = None,
) -> DescribeWhatIfForecastResult:
    """Describe what if forecast.

    Args:
        what_if_forecast_arn: What if forecast arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastArn"] = what_if_forecast_arn
    try:
        resp = await client.call("DescribeWhatIfForecast", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe what if forecast") from exc
    return DescribeWhatIfForecastResult(
        what_if_forecast_name=resp.get("WhatIfForecastName"),
        what_if_forecast_arn=resp.get("WhatIfForecastArn"),
        what_if_analysis_arn=resp.get("WhatIfAnalysisArn"),
        estimated_time_remaining_in_minutes=resp.get("EstimatedTimeRemainingInMinutes"),
        status=resp.get("Status"),
        message=resp.get("Message"),
        creation_time=resp.get("CreationTime"),
        last_modification_time=resp.get("LastModificationTime"),
        time_series_transformations=resp.get("TimeSeriesTransformations"),
        time_series_replacements_data_source=resp.get("TimeSeriesReplacementsDataSource"),
        forecast_types=resp.get("ForecastTypes"),
    )


async def describe_what_if_forecast_export(
    what_if_forecast_export_arn: str,
    region_name: str | None = None,
) -> DescribeWhatIfForecastExportResult:
    """Describe what if forecast export.

    Args:
        what_if_forecast_export_arn: What if forecast export arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WhatIfForecastExportArn"] = what_if_forecast_export_arn
    try:
        resp = await client.call("DescribeWhatIfForecastExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe what if forecast export") from exc
    return DescribeWhatIfForecastExportResult(
        what_if_forecast_export_arn=resp.get("WhatIfForecastExportArn"),
        what_if_forecast_export_name=resp.get("WhatIfForecastExportName"),
        what_if_forecast_arns=resp.get("WhatIfForecastArns"),
        destination=resp.get("Destination"),
        message=resp.get("Message"),
        status=resp.get("Status"),
        creation_time=resp.get("CreationTime"),
        estimated_time_remaining_in_minutes=resp.get("EstimatedTimeRemainingInMinutes"),
        last_modification_time=resp.get("LastModificationTime"),
        format=resp.get("Format"),
    )


async def get_accuracy_metrics(
    predictor_arn: str,
    region_name: str | None = None,
) -> GetAccuracyMetricsResult:
    """Get accuracy metrics.

    Args:
        predictor_arn: Predictor arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PredictorArn"] = predictor_arn
    try:
        resp = await client.call("GetAccuracyMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get accuracy metrics") from exc
    return GetAccuracyMetricsResult(
        predictor_evaluation_results=resp.get("PredictorEvaluationResults"),
        is_auto_predictor=resp.get("IsAutoPredictor"),
        auto_ml_override_strategy=resp.get("AutoMLOverrideStrategy"),
        optimization_metric=resp.get("OptimizationMetric"),
    )


async def list_dataset_groups(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetGroupsResult:
    """List dataset groups.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDatasetGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dataset groups") from exc
    return ListDatasetGroupsResult(
        dataset_groups=resp.get("DatasetGroups"),
        next_token=resp.get("NextToken"),
    )


async def list_dataset_import_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListDatasetImportJobsResult:
    """List dataset import jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListDatasetImportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dataset import jobs") from exc
    return ListDatasetImportJobsResult(
        dataset_import_jobs=resp.get("DatasetImportJobs"),
        next_token=resp.get("NextToken"),
    )


async def list_explainabilities(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListExplainabilitiesResult:
    """List explainabilities.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListExplainabilities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list explainabilities") from exc
    return ListExplainabilitiesResult(
        explainabilities=resp.get("Explainabilities"),
        next_token=resp.get("NextToken"),
    )


async def list_explainability_exports(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListExplainabilityExportsResult:
    """List explainability exports.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListExplainabilityExports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list explainability exports") from exc
    return ListExplainabilityExportsResult(
        explainability_exports=resp.get("ExplainabilityExports"),
        next_token=resp.get("NextToken"),
    )


async def list_forecast_export_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListForecastExportJobsResult:
    """List forecast export jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListForecastExportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list forecast export jobs") from exc
    return ListForecastExportJobsResult(
        forecast_export_jobs=resp.get("ForecastExportJobs"),
        next_token=resp.get("NextToken"),
    )


async def list_monitor_evaluations(
    monitor_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListMonitorEvaluationsResult:
    """List monitor evaluations.

    Args:
        monitor_arn: Monitor arn.
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MonitorArn"] = monitor_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListMonitorEvaluations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list monitor evaluations") from exc
    return ListMonitorEvaluationsResult(
        next_token=resp.get("NextToken"),
        predictor_monitor_evaluations=resp.get("PredictorMonitorEvaluations"),
    )


async def list_monitors(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListMonitorsResult:
    """List monitors.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListMonitors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list monitors") from exc
    return ListMonitorsResult(
        monitors=resp.get("Monitors"),
        next_token=resp.get("NextToken"),
    )


async def list_predictor_backtest_export_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListPredictorBacktestExportJobsResult:
    """List predictor backtest export jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListPredictorBacktestExportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list predictor backtest export jobs") from exc
    return ListPredictorBacktestExportJobsResult(
        predictor_backtest_export_jobs=resp.get("PredictorBacktestExportJobs"),
        next_token=resp.get("NextToken"),
    )


async def list_predictors(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListPredictorsResult:
    """List predictors.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListPredictors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list predictors") from exc
    return ListPredictorsResult(
        predictors=resp.get("Predictors"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_what_if_analyses(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListWhatIfAnalysesResult:
    """List what if analyses.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListWhatIfAnalyses", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list what if analyses") from exc
    return ListWhatIfAnalysesResult(
        what_if_analyses=resp.get("WhatIfAnalyses"),
        next_token=resp.get("NextToken"),
    )


async def list_what_if_forecast_exports(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListWhatIfForecastExportsResult:
    """List what if forecast exports.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListWhatIfForecastExports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list what if forecast exports") from exc
    return ListWhatIfForecastExportsResult(
        what_if_forecast_exports=resp.get("WhatIfForecastExports"),
        next_token=resp.get("NextToken"),
    )


async def list_what_if_forecasts(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListWhatIfForecastsResult:
    """List what if forecasts.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListWhatIfForecasts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list what if forecasts") from exc
    return ListWhatIfForecastsResult(
        what_if_forecasts=resp.get("WhatIfForecasts"),
        next_token=resp.get("NextToken"),
    )


async def resume_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Resume resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("ResumeResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resume resource") from exc
    return None


async def stop_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Stop resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("StopResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop resource") from exc
    return None


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_dataset_group(
    dataset_group_arn: str,
    dataset_arns: list[str],
    region_name: str | None = None,
) -> None:
    """Update dataset group.

    Args:
        dataset_group_arn: Dataset group arn.
        dataset_arns: Dataset arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("forecast", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetGroupArn"] = dataset_group_arn
    kwargs["DatasetArns"] = dataset_arns
    try:
        await client.call("UpdateDatasetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dataset group") from exc
    return None
