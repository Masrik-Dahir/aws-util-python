"""Tests for aws_util.aio.forecast module."""
from __future__ import annotations

import time as _time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.forecast import (
    DatasetGroupResult,
    DatasetImportJobResult,
    DatasetResult,
    ForecastExportJobResult,
    ForecastResult,
    PredictorResult,
    create_dataset,
    create_dataset_group,
    create_dataset_import_job,
    create_forecast,
    create_forecast_export_job,
    create_predictor,
    delete_resource_tree,
    describe_dataset,
    describe_dataset_import_job,
    describe_forecast,
    describe_forecast_export_job,
    describe_predictor,
    list_datasets,
    list_forecasts,
    wait_for_forecast,
    wait_for_predictor,
    create_auto_predictor,
    create_explainability,
    create_explainability_export,
    create_monitor,
    create_predictor_backtest_export_job,
    create_what_if_analysis,
    create_what_if_forecast,
    create_what_if_forecast_export,
    delete_dataset,
    delete_dataset_group,
    delete_dataset_import_job,
    delete_explainability,
    delete_explainability_export,
    delete_forecast,
    delete_forecast_export_job,
    delete_monitor,
    delete_predictor,
    delete_predictor_backtest_export_job,
    delete_what_if_analysis,
    delete_what_if_forecast,
    delete_what_if_forecast_export,
    describe_auto_predictor,
    describe_dataset_group,
    describe_explainability,
    describe_explainability_export,
    describe_monitor,
    describe_predictor_backtest_export_job,
    describe_what_if_analysis,
    describe_what_if_forecast,
    describe_what_if_forecast_export,
    get_accuracy_metrics,
    list_dataset_groups,
    list_dataset_import_jobs,
    list_explainabilities,
    list_explainability_exports,
    list_forecast_export_jobs,
    list_monitor_evaluations,
    list_monitors,
    list_predictor_backtest_export_jobs,
    list_predictors,
    list_tags_for_resource,
    list_what_if_analyses,
    list_what_if_forecast_exports,
    list_what_if_forecasts,
    resume_resource,
    stop_resource,
    tag_resource,
    untag_resource,
    update_dataset_group,
)
from aws_util.exceptions import AwsTimeoutError


REGION = "us-east-1"
DS_ARN = "arn:aws:forecast:us-east-1:123:dataset/ds1"
DSG_ARN = "arn:aws:forecast:us-east-1:123:dataset-group/dsg1"
PRED_ARN = "arn:aws:forecast:us-east-1:123:predictor/pred1"
FC_ARN = "arn:aws:forecast:us-east-1:123:forecast/fc1"
EXP_ARN = "arn:aws:forecast:us-east-1:123:forecast-export-job/exp1"
IMP_ARN = "arn:aws:forecast:us-east-1:123:dataset-import-job/imp1"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


async def test_create_dataset_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DatasetArn": DS_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_dataset(
        "ds1", "RETAIL", "TARGET_TIME_SERIES", {"Attributes": []},
        data_frequency="D", region_name=REGION,
    )
    assert result.dataset_arn == DS_ARN


async def test_create_dataset_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_dataset("ds", "RETAIL", "TARGET_TIME_SERIES", {}, region_name=REGION)


async def test_describe_dataset_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DatasetArn": DS_ARN, "DatasetName": "ds1",
        "Domain": "RETAIL", "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await describe_dataset(DS_ARN, region_name=REGION)
    assert result.dataset_arn == DS_ARN


async def test_describe_dataset_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_dataset(DS_ARN, region_name=REGION)


async def test_list_datasets_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Datasets": [{"DatasetArn": DS_ARN, "DatasetName": "ds1"}],
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await list_datasets(region_name=REGION)
    assert len(result) == 1


async def test_list_datasets_pagination(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "Datasets": [{"DatasetArn": DS_ARN}],
            "NextToken": "tok",
        },
        {
            "Datasets": [{"DatasetArn": DS_ARN + "2"}],
        },
    ]
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await list_datasets(region_name=REGION)
    assert len(result) == 2


async def test_list_datasets_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_datasets(region_name=REGION)


# ---------------------------------------------------------------------------
# Dataset group operations
# ---------------------------------------------------------------------------


async def test_create_dataset_group_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DatasetGroupArn": DSG_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_dataset_group(
        "dsg1", "RETAIL", dataset_arns=[DS_ARN], region_name=REGION,
    )
    assert result.dataset_group_arn == DSG_ARN


async def test_create_dataset_group_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_dataset_group("dsg", "RETAIL", region_name=REGION)


# ---------------------------------------------------------------------------
# Dataset import job
# ---------------------------------------------------------------------------


async def test_create_dataset_import_job_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DatasetImportJobArn": IMP_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_dataset_import_job(
        "imp1", DS_ARN, {"S3Config": {}},
        timestamp_format="yyyy-MM-dd", region_name=REGION,
    )
    assert result.dataset_import_job_arn == IMP_ARN


async def test_create_dataset_import_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_dataset_import_job("imp", DS_ARN, {}, region_name=REGION)


async def test_describe_dataset_import_job_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DatasetImportJobArn": IMP_ARN,
        "DatasetImportJobName": "imp1",
        "DatasetArn": DS_ARN,
        "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await describe_dataset_import_job(IMP_ARN, region_name=REGION)
    assert result.status == "ACTIVE"


async def test_describe_dataset_import_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_dataset_import_job(IMP_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Predictor operations
# ---------------------------------------------------------------------------


async def test_create_predictor_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"PredictorArn": PRED_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_predictor(
        "pred1", 10,
        dataset_group_arn=DSG_ARN,
        algorithm_arn="arn:...",
        forecast_types=["0.5"],
        perform_auto_ml=False,
        featurization_config={"ForecastFrequency": "D"},
        extra_params={"TrainingParameters": {}},
        region_name=REGION,
    )
    assert result.predictor_arn == PRED_ARN


async def test_create_predictor_with_input_data_config_only(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"PredictorArn": PRED_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_predictor(
        "pred1", 10,
        input_data_config={"DatasetGroupArn": DSG_ARN},
        region_name=REGION,
    )
    assert result.predictor_arn == PRED_ARN


async def test_create_predictor_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_predictor("pred", 10, region_name=REGION)


async def test_describe_predictor_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "PredictorArn": PRED_ARN, "PredictorName": "pred1",
        "ForecastHorizon": 10, "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await describe_predictor(PRED_ARN, region_name=REGION)
    assert result.predictor_arn == PRED_ARN


async def test_describe_predictor_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_predictor(PRED_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Forecast operations
# ---------------------------------------------------------------------------


async def test_create_forecast_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ForecastArn": FC_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_forecast(
        "fc1", PRED_ARN, forecast_types=["0.5"], region_name=REGION,
    )
    assert result.forecast_arn == FC_ARN


async def test_create_forecast_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_forecast("fc", PRED_ARN, region_name=REGION)


async def test_describe_forecast_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ForecastArn": FC_ARN, "ForecastName": "fc1",
        "PredictorArn": PRED_ARN, "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await describe_forecast(FC_ARN, region_name=REGION)
    assert result.forecast_arn == FC_ARN


async def test_describe_forecast_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_forecast(FC_ARN, region_name=REGION)


async def test_create_forecast_export_job_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ForecastExportJobArn": EXP_ARN}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await create_forecast_export_job(
        "exp1", FC_ARN, {"S3Config": {}}, region_name=REGION,
    )
    assert result.forecast_export_job_arn == EXP_ARN


async def test_create_forecast_export_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_forecast_export_job("exp", FC_ARN, {}, region_name=REGION)


async def test_describe_forecast_export_job_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ForecastExportJobArn": EXP_ARN,
        "ForecastExportJobName": "exp1",
        "ForecastArn": FC_ARN,
        "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await describe_forecast_export_job(EXP_ARN, region_name=REGION)
    assert result.status == "ACTIVE"


async def test_describe_forecast_export_job_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_forecast_export_job(EXP_ARN, region_name=REGION)


async def test_list_forecasts_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Forecasts": [{"ForecastArn": FC_ARN, "ForecastName": "fc1"}],
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await list_forecasts(region_name=REGION)
    assert len(result) == 1


async def test_list_forecasts_pagination(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "Forecasts": [{"ForecastArn": FC_ARN}],
            "NextToken": "tok",
        },
        {
            "Forecasts": [{"ForecastArn": FC_ARN + "2"}],
        },
    ]
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await list_forecasts(region_name=REGION)
    assert len(result) == 2


async def test_list_forecasts_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_forecasts(region_name=REGION)


# ---------------------------------------------------------------------------
# Resource cleanup
# ---------------------------------------------------------------------------


async def test_delete_resource_tree_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    await delete_resource_tree(DS_ARN, region_name=REGION)


async def test_delete_resource_tree_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_resource_tree(DS_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def test_wait_for_predictor_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "PredictorArn": PRED_ARN, "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await wait_for_predictor(PRED_ARN, timeout=5, region_name=REGION)
    assert result.status == "ACTIVE"


async def test_wait_for_predictor_failure(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "PredictorArn": PRED_ARN, "Status": "FAILED", "Message": "oops",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await wait_for_predictor(PRED_ARN, timeout=5, region_name=REGION)


async def test_wait_for_predictor_poll_then_success(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"PredictorArn": PRED_ARN, "Status": "CREATE_IN_PROGRESS"},
        {"PredictorArn": PRED_ARN, "Status": "ACTIVE"},
    ]
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_predictor(
        PRED_ARN, timeout=3600, poll_interval=1, region_name=REGION,
    )
    assert result.status == "ACTIVE"


async def test_wait_for_predictor_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "PredictorArn": PRED_ARN, "Status": "CREATE_IN_PROGRESS",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(_time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_predictor(
            PRED_ARN, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_forecast_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ForecastArn": FC_ARN, "Status": "ACTIVE",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    result = await wait_for_forecast(FC_ARN, timeout=5, region_name=REGION)
    assert result.status == "ACTIVE"


async def test_wait_for_forecast_failure(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ForecastArn": FC_ARN, "Status": "FAILED", "Message": "oops",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await wait_for_forecast(FC_ARN, timeout=5, region_name=REGION)


async def test_wait_for_forecast_poll_then_success(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"ForecastArn": FC_ARN, "Status": "CREATE_IN_PROGRESS"},
        {"ForecastArn": FC_ARN, "Status": "ACTIVE"},
    ]
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_forecast(
        FC_ARN, timeout=3600, poll_interval=1, region_name=REGION,
    )
    assert result.status == "ACTIVE"


async def test_wait_for_forecast_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "ForecastArn": FC_ARN, "Status": "CREATE_IN_PROGRESS",
    }
    monkeypatch.setattr("aws_util.aio.forecast.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(_time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_forecast(
            FC_ARN, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_create_auto_predictor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_auto_predictor("test-predictor_name", )
    mock_client.call.assert_called_once()


async def test_create_auto_predictor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_auto_predictor("test-predictor_name", )


async def test_create_explainability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_explainability("test-explainability_name", "test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_explainability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_explainability("test-explainability_name", "test-resource_arn", {}, )


async def test_create_explainability_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_explainability_export("test-explainability_export_name", "test-explainability_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_explainability_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_explainability_export("test-explainability_export_name", "test-explainability_arn", {}, )


async def test_create_monitor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_monitor("test-monitor_name", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_create_monitor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_monitor("test-monitor_name", "test-resource_arn", )


async def test_create_predictor_backtest_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_predictor_backtest_export_job("test-predictor_backtest_export_job_name", "test-predictor_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_predictor_backtest_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_predictor_backtest_export_job("test-predictor_backtest_export_job_name", "test-predictor_arn", {}, )


async def test_create_what_if_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", )
    mock_client.call.assert_called_once()


async def test_create_what_if_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", )


async def test_create_what_if_forecast(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", )
    mock_client.call.assert_called_once()


async def test_create_what_if_forecast_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", )


async def test_create_what_if_forecast_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_what_if_forecast_export("test-what_if_forecast_export_name", [], {}, )
    mock_client.call.assert_called_once()


async def test_create_what_if_forecast_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_what_if_forecast_export("test-what_if_forecast_export_name", [], {}, )


async def test_delete_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset("test-dataset_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset("test-dataset_arn", )


async def test_delete_dataset_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset_group("test-dataset_group_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset_group("test-dataset_group_arn", )


async def test_delete_dataset_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset_import_job("test-dataset_import_job_arn", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset_import_job("test-dataset_import_job_arn", )


async def test_delete_explainability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_explainability("test-explainability_arn", )
    mock_client.call.assert_called_once()


async def test_delete_explainability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_explainability("test-explainability_arn", )


async def test_delete_explainability_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_explainability_export("test-explainability_export_arn", )
    mock_client.call.assert_called_once()


async def test_delete_explainability_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_explainability_export("test-explainability_export_arn", )


async def test_delete_forecast(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_forecast("test-forecast_arn", )
    mock_client.call.assert_called_once()


async def test_delete_forecast_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_forecast("test-forecast_arn", )


async def test_delete_forecast_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_forecast_export_job("test-forecast_export_job_arn", )
    mock_client.call.assert_called_once()


async def test_delete_forecast_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_forecast_export_job("test-forecast_export_job_arn", )


async def test_delete_monitor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_monitor("test-monitor_arn", )
    mock_client.call.assert_called_once()


async def test_delete_monitor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_monitor("test-monitor_arn", )


async def test_delete_predictor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_predictor("test-predictor_arn", )
    mock_client.call.assert_called_once()


async def test_delete_predictor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_predictor("test-predictor_arn", )


async def test_delete_predictor_backtest_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", )
    mock_client.call.assert_called_once()


async def test_delete_predictor_backtest_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", )


async def test_delete_what_if_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_what_if_analysis("test-what_if_analysis_arn", )
    mock_client.call.assert_called_once()


async def test_delete_what_if_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_what_if_analysis("test-what_if_analysis_arn", )


async def test_delete_what_if_forecast(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_what_if_forecast("test-what_if_forecast_arn", )
    mock_client.call.assert_called_once()


async def test_delete_what_if_forecast_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_what_if_forecast("test-what_if_forecast_arn", )


async def test_delete_what_if_forecast_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_what_if_forecast_export("test-what_if_forecast_export_arn", )
    mock_client.call.assert_called_once()


async def test_delete_what_if_forecast_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_what_if_forecast_export("test-what_if_forecast_export_arn", )


async def test_describe_auto_predictor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_auto_predictor("test-predictor_arn", )
    mock_client.call.assert_called_once()


async def test_describe_auto_predictor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_auto_predictor("test-predictor_arn", )


async def test_describe_dataset_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset_group("test-dataset_group_arn", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset_group("test-dataset_group_arn", )


async def test_describe_explainability(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_explainability("test-explainability_arn", )
    mock_client.call.assert_called_once()


async def test_describe_explainability_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_explainability("test-explainability_arn", )


async def test_describe_explainability_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_explainability_export("test-explainability_export_arn", )
    mock_client.call.assert_called_once()


async def test_describe_explainability_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_explainability_export("test-explainability_export_arn", )


async def test_describe_monitor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_monitor("test-monitor_arn", )
    mock_client.call.assert_called_once()


async def test_describe_monitor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_monitor("test-monitor_arn", )


async def test_describe_predictor_backtest_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", )
    mock_client.call.assert_called_once()


async def test_describe_predictor_backtest_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", )


async def test_describe_what_if_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_what_if_analysis("test-what_if_analysis_arn", )
    mock_client.call.assert_called_once()


async def test_describe_what_if_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_what_if_analysis("test-what_if_analysis_arn", )


async def test_describe_what_if_forecast(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_what_if_forecast("test-what_if_forecast_arn", )
    mock_client.call.assert_called_once()


async def test_describe_what_if_forecast_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_what_if_forecast("test-what_if_forecast_arn", )


async def test_describe_what_if_forecast_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_what_if_forecast_export("test-what_if_forecast_export_arn", )
    mock_client.call.assert_called_once()


async def test_describe_what_if_forecast_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_what_if_forecast_export("test-what_if_forecast_export_arn", )


async def test_get_accuracy_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_accuracy_metrics("test-predictor_arn", )
    mock_client.call.assert_called_once()


async def test_get_accuracy_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_accuracy_metrics("test-predictor_arn", )


async def test_list_dataset_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_groups()
    mock_client.call.assert_called_once()


async def test_list_dataset_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_groups()


async def test_list_dataset_import_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dataset_import_jobs()
    mock_client.call.assert_called_once()


async def test_list_dataset_import_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dataset_import_jobs()


async def test_list_explainabilities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_explainabilities()
    mock_client.call.assert_called_once()


async def test_list_explainabilities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_explainabilities()


async def test_list_explainability_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_explainability_exports()
    mock_client.call.assert_called_once()


async def test_list_explainability_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_explainability_exports()


async def test_list_forecast_export_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_forecast_export_jobs()
    mock_client.call.assert_called_once()


async def test_list_forecast_export_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_forecast_export_jobs()


async def test_list_monitor_evaluations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_monitor_evaluations("test-monitor_arn", )
    mock_client.call.assert_called_once()


async def test_list_monitor_evaluations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_monitor_evaluations("test-monitor_arn", )


async def test_list_monitors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_monitors()
    mock_client.call.assert_called_once()


async def test_list_monitors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_monitors()


async def test_list_predictor_backtest_export_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_predictor_backtest_export_jobs()
    mock_client.call.assert_called_once()


async def test_list_predictor_backtest_export_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_predictor_backtest_export_jobs()


async def test_list_predictors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_predictors()
    mock_client.call.assert_called_once()


async def test_list_predictors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_predictors()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_what_if_analyses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_what_if_analyses()
    mock_client.call.assert_called_once()


async def test_list_what_if_analyses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_what_if_analyses()


async def test_list_what_if_forecast_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_what_if_forecast_exports()
    mock_client.call.assert_called_once()


async def test_list_what_if_forecast_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_what_if_forecast_exports()


async def test_list_what_if_forecasts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_what_if_forecasts()
    mock_client.call.assert_called_once()


async def test_list_what_if_forecasts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_what_if_forecasts()


async def test_resume_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_resume_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_resource("test-resource_arn", )


async def test_stop_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_stop_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_resource("test-resource_arn", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_dataset_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dataset_group("test-dataset_group_arn", [], )
    mock_client.call.assert_called_once()


async def test_update_dataset_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.forecast.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dataset_group("test-dataset_group_arn", [], )


@pytest.mark.asyncio
async def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_dataset("test-dataset_name", "test-domain", "test-dataset_type", "test-schema", data_frequency="test-data_frequency", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_forecast_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_forecast
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_forecast("test-forecast_name", "test-predictor_arn", forecast_types="test-forecast_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_auto_predictor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_auto_predictor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_auto_predictor("test-predictor_name", forecast_horizon="test-forecast_horizon", forecast_types="test-forecast_types", forecast_dimensions="test-forecast_dimensions", forecast_frequency="test-forecast_frequency", data_config={}, encryption_config={}, reference_predictor_arn="test-reference_predictor_arn", optimization_metric="test-optimization_metric", explain_predictor="test-explain_predictor", tags=[{"Key": "k", "Value": "v"}], monitor_config={}, time_alignment_boundary="test-time_alignment_boundary", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_explainability_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_explainability
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_explainability("test-explainability_name", "test-resource_arn", {}, data_source="test-data_source", schema="test-schema", enable_visualization=True, start_date_time="test-start_date_time", end_date_time="test-end_date_time", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_explainability_export_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_explainability_export
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_explainability_export(1, "test-explainability_arn", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_monitor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_monitor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_monitor("test-monitor_name", "test-resource_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_predictor_backtest_export_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_predictor_backtest_export_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_predictor_backtest_export_job(1, "test-predictor_arn", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_what_if_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_what_if_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", time_series_selector="test-time_series_selector", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_what_if_forecast_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_what_if_forecast
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", time_series_transformations="test-time_series_transformations", time_series_replacements_data_source="test-time_series_replacements_data_source", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_what_if_forecast_export_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import create_what_if_forecast_export
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await create_what_if_forecast_export(1, "test-what_if_forecast_arns", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_dataset_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_dataset_groups(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dataset_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_dataset_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_dataset_import_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_explainabilities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_explainabilities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_explainabilities(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_explainability_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_explainability_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_explainability_exports(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_forecast_export_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_forecast_export_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_forecast_export_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_monitor_evaluations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_monitor_evaluations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_monitor_evaluations("test-monitor_arn", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_monitors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_monitors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_monitors(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_predictor_backtest_export_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_predictor_backtest_export_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_predictor_backtest_export_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_predictors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_predictors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_predictors(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_what_if_analyses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_what_if_analyses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_what_if_analyses(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_what_if_forecast_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_what_if_forecast_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_what_if_forecast_exports(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_what_if_forecasts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.forecast import list_what_if_forecasts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.forecast.async_client", lambda *a, **kw: mock_client)
    await list_what_if_forecasts(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()
