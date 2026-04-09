"""Tests for aws_util.forecast module."""
from __future__ import annotations

import time as _time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.forecast as forecast_mod
from aws_util.forecast import (
    DatasetGroupResult,
    DatasetImportJobResult,
    DatasetResult,
    ForecastExportJobResult,
    ForecastResult,
    PredictorResult,
    _parse_dataset,
    _parse_forecast,
    _parse_predictor,
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


def _client_error(code: str = "ServiceException", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_dataset():
    result = _parse_dataset({
        "DatasetArn": DS_ARN, "DatasetName": "ds1",
        "Domain": "RETAIL", "DatasetType": "TARGET_TIME_SERIES",
        "Status": "ACTIVE",
    })
    assert result.dataset_arn == DS_ARN


def test_parse_predictor():
    result = _parse_predictor({
        "PredictorArn": PRED_ARN, "PredictorName": "pred1",
        "ForecastHorizon": 10, "Status": "ACTIVE",
    })
    assert result.predictor_arn == PRED_ARN


def test_parse_forecast():
    result = _parse_forecast({
        "ForecastArn": FC_ARN, "ForecastName": "fc1",
        "PredictorArn": PRED_ARN, "Status": "ACTIVE",
    })
    assert result.forecast_arn == FC_ARN


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_create_dataset_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset.return_value = {"DatasetArn": DS_ARN}
    result = create_dataset(
        "ds1", "RETAIL", "TARGET_TIME_SERIES", {"Attributes": []},
        data_frequency="D", region_name=REGION,
    )
    assert result.dataset_arn == DS_ARN
    assert result.dataset_name == "ds1"


@patch("aws_util.forecast.get_client")
def test_create_dataset_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_dataset("ds", "RETAIL", "TARGET_TIME_SERIES", {}, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_describe_dataset_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_dataset.return_value = {
        "DatasetArn": DS_ARN, "DatasetName": "ds1",
        "Domain": "RETAIL", "Status": "ACTIVE",
    }
    result = describe_dataset(DS_ARN, region_name=REGION)
    assert result.dataset_arn == DS_ARN


@patch("aws_util.forecast.get_client")
def test_describe_dataset_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_dataset.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_dataset(DS_ARN, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_list_datasets_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_datasets.return_value = {
        "Datasets": [{"DatasetArn": DS_ARN, "DatasetName": "ds1"}],
    }
    result = list_datasets(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.forecast.get_client")
def test_list_datasets_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_datasets.side_effect = [
        {
            "Datasets": [{"DatasetArn": DS_ARN}],
            "NextToken": "tok",
        },
        {
            "Datasets": [{"DatasetArn": DS_ARN + "2"}],
        },
    ]
    result = list_datasets(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.forecast.get_client")
def test_list_datasets_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_datasets.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_datasets(region_name=REGION)


# ---------------------------------------------------------------------------
# Dataset group operations
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_create_dataset_group_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset_group.return_value = {"DatasetGroupArn": DSG_ARN}
    result = create_dataset_group(
        "dsg1", "RETAIL", dataset_arns=[DS_ARN], region_name=REGION,
    )
    assert result.dataset_group_arn == DSG_ARN


@patch("aws_util.forecast.get_client")
def test_create_dataset_group_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset_group.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_dataset_group("dsg", "RETAIL", region_name=REGION)


# ---------------------------------------------------------------------------
# Dataset import job
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_create_dataset_import_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset_import_job.return_value = {
        "DatasetImportJobArn": IMP_ARN,
    }
    result = create_dataset_import_job(
        "imp1", DS_ARN, {"S3Config": {}},
        timestamp_format="yyyy-MM-dd", region_name=REGION,
    )
    assert result.dataset_import_job_arn == IMP_ARN


@patch("aws_util.forecast.get_client")
def test_create_dataset_import_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_dataset_import_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_dataset_import_job("imp", DS_ARN, {}, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_describe_dataset_import_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_dataset_import_job.return_value = {
        "DatasetImportJobArn": IMP_ARN,
        "DatasetImportJobName": "imp1",
        "DatasetArn": DS_ARN,
        "Status": "ACTIVE",
    }
    result = describe_dataset_import_job(IMP_ARN, region_name=REGION)
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_describe_dataset_import_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_dataset_import_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_dataset_import_job(IMP_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Predictor operations
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_create_predictor_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_predictor.return_value = {"PredictorArn": PRED_ARN}
    result = create_predictor(
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


@patch("aws_util.forecast.get_client")
def test_create_predictor_with_input_data_config(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_predictor.return_value = {"PredictorArn": PRED_ARN}
    result = create_predictor(
        "pred1", 10,
        input_data_config={"DatasetGroupArn": DSG_ARN},
        region_name=REGION,
    )
    assert result.predictor_arn == PRED_ARN


@patch("aws_util.forecast.get_client")
def test_create_predictor_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_predictor.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_predictor("pred", 10, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_describe_predictor_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.return_value = {
        "PredictorArn": PRED_ARN, "PredictorName": "pred1",
        "ForecastHorizon": 10, "Status": "ACTIVE",
    }
    result = describe_predictor(PRED_ARN, region_name=REGION)
    assert result.predictor_arn == PRED_ARN


@patch("aws_util.forecast.get_client")
def test_describe_predictor_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_predictor(PRED_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Forecast operations
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_create_forecast_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_forecast.return_value = {"ForecastArn": FC_ARN}
    result = create_forecast(
        "fc1", PRED_ARN, forecast_types=["0.5"], region_name=REGION,
    )
    assert result.forecast_arn == FC_ARN


@patch("aws_util.forecast.get_client")
def test_create_forecast_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_forecast.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_forecast("fc", PRED_ARN, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_describe_forecast_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.return_value = {
        "ForecastArn": FC_ARN, "ForecastName": "fc1",
        "PredictorArn": PRED_ARN, "Status": "ACTIVE",
    }
    result = describe_forecast(FC_ARN, region_name=REGION)
    assert result.forecast_arn == FC_ARN


@patch("aws_util.forecast.get_client")
def test_describe_forecast_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_forecast(FC_ARN, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_create_forecast_export_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_forecast_export_job.return_value = {
        "ForecastExportJobArn": EXP_ARN,
    }
    result = create_forecast_export_job(
        "exp1", FC_ARN, {"S3Config": {}}, region_name=REGION,
    )
    assert result.forecast_export_job_arn == EXP_ARN


@patch("aws_util.forecast.get_client")
def test_create_forecast_export_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_forecast_export_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_forecast_export_job("exp", FC_ARN, {}, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_describe_forecast_export_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast_export_job.return_value = {
        "ForecastExportJobArn": EXP_ARN,
        "ForecastExportJobName": "exp1",
        "ForecastArn": FC_ARN,
        "Status": "ACTIVE",
    }
    result = describe_forecast_export_job(EXP_ARN, region_name=REGION)
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_describe_forecast_export_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast_export_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_forecast_export_job(EXP_ARN, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_list_forecasts_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_forecasts.return_value = {
        "Forecasts": [{"ForecastArn": FC_ARN, "ForecastName": "fc1"}],
    }
    result = list_forecasts(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.forecast.get_client")
def test_list_forecasts_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_forecasts.side_effect = [
        {
            "Forecasts": [{"ForecastArn": FC_ARN}],
            "NextToken": "tok",
        },
        {
            "Forecasts": [{"ForecastArn": FC_ARN + "2"}],
        },
    ]
    result = list_forecasts(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.forecast.get_client")
def test_list_forecasts_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.list_forecasts.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_forecasts(region_name=REGION)


# ---------------------------------------------------------------------------
# Resource cleanup
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_delete_resource_tree_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_resource_tree(DS_ARN, region_name=REGION)
    client.delete_resource_tree.assert_called_once()


@patch("aws_util.forecast.get_client")
def test_delete_resource_tree_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_resource_tree.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_resource_tree(DS_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


@patch("aws_util.forecast.get_client")
def test_wait_for_predictor_immediate(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.return_value = {
        "PredictorArn": PRED_ARN, "Status": "ACTIVE",
    }
    result = wait_for_predictor(PRED_ARN, timeout=5, region_name=REGION)
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_wait_for_predictor_failure(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.return_value = {
        "PredictorArn": PRED_ARN, "Status": "FAILED", "Message": "oops",
    }
    with pytest.raises(RuntimeError):
        wait_for_predictor(PRED_ARN, timeout=5, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_wait_for_predictor_poll_then_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.side_effect = [
        {"PredictorArn": PRED_ARN, "Status": "CREATE_IN_PROGRESS"},
        {"PredictorArn": PRED_ARN, "Status": "ACTIVE"},
    ]
    with patch.object(_time, "sleep"):
        result = wait_for_predictor(
            PRED_ARN, timeout=3600, poll_interval=1, region_name=REGION,
        )
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_wait_for_predictor_timeout(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_predictor.return_value = {
        "PredictorArn": PRED_ARN, "Status": "CREATE_IN_PROGRESS",
    }
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    with patch.object(_time, "monotonic", _mono), \
         patch.object(_time, "sleep"):
        with pytest.raises(AwsTimeoutError):
            wait_for_predictor(
                PRED_ARN, timeout=1, poll_interval=0.1, region_name=REGION,
            )


@patch("aws_util.forecast.get_client")
def test_wait_for_forecast_immediate(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.return_value = {
        "ForecastArn": FC_ARN, "Status": "ACTIVE",
    }
    result = wait_for_forecast(FC_ARN, timeout=5, region_name=REGION)
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_wait_for_forecast_failure(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.return_value = {
        "ForecastArn": FC_ARN, "Status": "FAILED", "Message": "oops",
    }
    with pytest.raises(RuntimeError):
        wait_for_forecast(FC_ARN, timeout=5, region_name=REGION)


@patch("aws_util.forecast.get_client")
def test_wait_for_forecast_poll_then_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.side_effect = [
        {"ForecastArn": FC_ARN, "Status": "CREATE_IN_PROGRESS"},
        {"ForecastArn": FC_ARN, "Status": "ACTIVE"},
    ]
    with patch.object(_time, "sleep"):
        result = wait_for_forecast(
            FC_ARN, timeout=3600, poll_interval=1, region_name=REGION,
        )
    assert result.status == "ACTIVE"


@patch("aws_util.forecast.get_client")
def test_wait_for_forecast_timeout(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_forecast.return_value = {
        "ForecastArn": FC_ARN, "Status": "CREATE_IN_PROGRESS",
    }
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    with patch.object(_time, "monotonic", _mono), \
         patch.object(_time, "sleep"):
        with pytest.raises(AwsTimeoutError):
            wait_for_forecast(
                FC_ARN, timeout=1, poll_interval=0.1, region_name=REGION,
            )


def test_create_auto_predictor(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_auto_predictor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_auto_predictor("test-predictor_name", region_name=REGION)
    mock_client.create_auto_predictor.assert_called_once()


def test_create_auto_predictor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_auto_predictor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_auto_predictor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create auto predictor"):
        create_auto_predictor("test-predictor_name", region_name=REGION)


def test_create_explainability(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_explainability.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_explainability("test-explainability_name", "test-resource_arn", {}, region_name=REGION)
    mock_client.create_explainability.assert_called_once()


def test_create_explainability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_explainability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_explainability",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create explainability"):
        create_explainability("test-explainability_name", "test-resource_arn", {}, region_name=REGION)


def test_create_explainability_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_explainability_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_explainability_export("test-explainability_export_name", "test-explainability_arn", {}, region_name=REGION)
    mock_client.create_explainability_export.assert_called_once()


def test_create_explainability_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_explainability_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_explainability_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create explainability export"):
        create_explainability_export("test-explainability_export_name", "test-explainability_arn", {}, region_name=REGION)


def test_create_monitor(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_monitor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_monitor("test-monitor_name", "test-resource_arn", region_name=REGION)
    mock_client.create_monitor.assert_called_once()


def test_create_monitor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_monitor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_monitor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create monitor"):
        create_monitor("test-monitor_name", "test-resource_arn", region_name=REGION)


def test_create_predictor_backtest_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_predictor_backtest_export_job.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_predictor_backtest_export_job("test-predictor_backtest_export_job_name", "test-predictor_arn", {}, region_name=REGION)
    mock_client.create_predictor_backtest_export_job.assert_called_once()


def test_create_predictor_backtest_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_predictor_backtest_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_predictor_backtest_export_job",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create predictor backtest export job"):
        create_predictor_backtest_export_job("test-predictor_backtest_export_job_name", "test-predictor_arn", {}, region_name=REGION)


def test_create_what_if_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_analysis.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", region_name=REGION)
    mock_client.create_what_if_analysis.assert_called_once()


def test_create_what_if_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_what_if_analysis",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create what if analysis"):
        create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", region_name=REGION)


def test_create_what_if_forecast(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_forecast.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", region_name=REGION)
    mock_client.create_what_if_forecast.assert_called_once()


def test_create_what_if_forecast_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_forecast.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_what_if_forecast",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create what if forecast"):
        create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", region_name=REGION)


def test_create_what_if_forecast_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_forecast_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    create_what_if_forecast_export("test-what_if_forecast_export_name", [], {}, region_name=REGION)
    mock_client.create_what_if_forecast_export.assert_called_once()


def test_create_what_if_forecast_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_what_if_forecast_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_what_if_forecast_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create what if forecast export"):
        create_what_if_forecast_export("test-what_if_forecast_export_name", [], {}, region_name=REGION)


def test_delete_dataset(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_dataset("test-dataset_arn", region_name=REGION)
    mock_client.delete_dataset.assert_called_once()


def test_delete_dataset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset"):
        delete_dataset("test-dataset_arn", region_name=REGION)


def test_delete_dataset_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_group.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_dataset_group("test-dataset_group_arn", region_name=REGION)
    mock_client.delete_dataset_group.assert_called_once()


def test_delete_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset_group",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset group"):
        delete_dataset_group("test-dataset_group_arn", region_name=REGION)


def test_delete_dataset_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_import_job.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_dataset_import_job("test-dataset_import_job_arn", region_name=REGION)
    mock_client.delete_dataset_import_job.assert_called_once()


def test_delete_dataset_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dataset_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset_import_job",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dataset import job"):
        delete_dataset_import_job("test-dataset_import_job_arn", region_name=REGION)


def test_delete_explainability(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_explainability.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_explainability("test-explainability_arn", region_name=REGION)
    mock_client.delete_explainability.assert_called_once()


def test_delete_explainability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_explainability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_explainability",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete explainability"):
        delete_explainability("test-explainability_arn", region_name=REGION)


def test_delete_explainability_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_explainability_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_explainability_export("test-explainability_export_arn", region_name=REGION)
    mock_client.delete_explainability_export.assert_called_once()


def test_delete_explainability_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_explainability_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_explainability_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete explainability export"):
        delete_explainability_export("test-explainability_export_arn", region_name=REGION)


def test_delete_forecast(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_forecast.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_forecast("test-forecast_arn", region_name=REGION)
    mock_client.delete_forecast.assert_called_once()


def test_delete_forecast_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_forecast.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_forecast",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete forecast"):
        delete_forecast("test-forecast_arn", region_name=REGION)


def test_delete_forecast_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_forecast_export_job.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_forecast_export_job("test-forecast_export_job_arn", region_name=REGION)
    mock_client.delete_forecast_export_job.assert_called_once()


def test_delete_forecast_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_forecast_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_forecast_export_job",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete forecast export job"):
        delete_forecast_export_job("test-forecast_export_job_arn", region_name=REGION)


def test_delete_monitor(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_monitor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_monitor("test-monitor_arn", region_name=REGION)
    mock_client.delete_monitor.assert_called_once()


def test_delete_monitor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_monitor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_monitor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete monitor"):
        delete_monitor("test-monitor_arn", region_name=REGION)


def test_delete_predictor(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predictor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_predictor("test-predictor_arn", region_name=REGION)
    mock_client.delete_predictor.assert_called_once()


def test_delete_predictor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predictor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_predictor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete predictor"):
        delete_predictor("test-predictor_arn", region_name=REGION)


def test_delete_predictor_backtest_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predictor_backtest_export_job.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", region_name=REGION)
    mock_client.delete_predictor_backtest_export_job.assert_called_once()


def test_delete_predictor_backtest_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predictor_backtest_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_predictor_backtest_export_job",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete predictor backtest export job"):
        delete_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", region_name=REGION)


def test_delete_what_if_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_analysis.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_what_if_analysis("test-what_if_analysis_arn", region_name=REGION)
    mock_client.delete_what_if_analysis.assert_called_once()


def test_delete_what_if_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_what_if_analysis",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete what if analysis"):
        delete_what_if_analysis("test-what_if_analysis_arn", region_name=REGION)


def test_delete_what_if_forecast(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_forecast.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_what_if_forecast("test-what_if_forecast_arn", region_name=REGION)
    mock_client.delete_what_if_forecast.assert_called_once()


def test_delete_what_if_forecast_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_forecast.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_what_if_forecast",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete what if forecast"):
        delete_what_if_forecast("test-what_if_forecast_arn", region_name=REGION)


def test_delete_what_if_forecast_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_forecast_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    delete_what_if_forecast_export("test-what_if_forecast_export_arn", region_name=REGION)
    mock_client.delete_what_if_forecast_export.assert_called_once()


def test_delete_what_if_forecast_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_what_if_forecast_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_what_if_forecast_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete what if forecast export"):
        delete_what_if_forecast_export("test-what_if_forecast_export_arn", region_name=REGION)


def test_describe_auto_predictor(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_predictor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_auto_predictor("test-predictor_arn", region_name=REGION)
    mock_client.describe_auto_predictor.assert_called_once()


def test_describe_auto_predictor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_auto_predictor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_auto_predictor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe auto predictor"):
        describe_auto_predictor("test-predictor_arn", region_name=REGION)


def test_describe_dataset_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_group.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_dataset_group("test-dataset_group_arn", region_name=REGION)
    mock_client.describe_dataset_group.assert_called_once()


def test_describe_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset_group",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dataset group"):
        describe_dataset_group("test-dataset_group_arn", region_name=REGION)


def test_describe_explainability(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_explainability.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_explainability("test-explainability_arn", region_name=REGION)
    mock_client.describe_explainability.assert_called_once()


def test_describe_explainability_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_explainability.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_explainability",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe explainability"):
        describe_explainability("test-explainability_arn", region_name=REGION)


def test_describe_explainability_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_explainability_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_explainability_export("test-explainability_export_arn", region_name=REGION)
    mock_client.describe_explainability_export.assert_called_once()


def test_describe_explainability_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_explainability_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_explainability_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe explainability export"):
        describe_explainability_export("test-explainability_export_arn", region_name=REGION)


def test_describe_monitor(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_monitor.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_monitor("test-monitor_arn", region_name=REGION)
    mock_client.describe_monitor.assert_called_once()


def test_describe_monitor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_monitor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_monitor",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe monitor"):
        describe_monitor("test-monitor_arn", region_name=REGION)


def test_describe_predictor_backtest_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_predictor_backtest_export_job.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", region_name=REGION)
    mock_client.describe_predictor_backtest_export_job.assert_called_once()


def test_describe_predictor_backtest_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_predictor_backtest_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_predictor_backtest_export_job",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe predictor backtest export job"):
        describe_predictor_backtest_export_job("test-predictor_backtest_export_job_arn", region_name=REGION)


def test_describe_what_if_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_analysis.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_what_if_analysis("test-what_if_analysis_arn", region_name=REGION)
    mock_client.describe_what_if_analysis.assert_called_once()


def test_describe_what_if_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_what_if_analysis",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe what if analysis"):
        describe_what_if_analysis("test-what_if_analysis_arn", region_name=REGION)


def test_describe_what_if_forecast(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_forecast.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_what_if_forecast("test-what_if_forecast_arn", region_name=REGION)
    mock_client.describe_what_if_forecast.assert_called_once()


def test_describe_what_if_forecast_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_forecast.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_what_if_forecast",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe what if forecast"):
        describe_what_if_forecast("test-what_if_forecast_arn", region_name=REGION)


def test_describe_what_if_forecast_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_forecast_export.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    describe_what_if_forecast_export("test-what_if_forecast_export_arn", region_name=REGION)
    mock_client.describe_what_if_forecast_export.assert_called_once()


def test_describe_what_if_forecast_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_what_if_forecast_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_what_if_forecast_export",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe what if forecast export"):
        describe_what_if_forecast_export("test-what_if_forecast_export_arn", region_name=REGION)


def test_get_accuracy_metrics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_accuracy_metrics.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    get_accuracy_metrics("test-predictor_arn", region_name=REGION)
    mock_client.get_accuracy_metrics.assert_called_once()


def test_get_accuracy_metrics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_accuracy_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_accuracy_metrics",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get accuracy metrics"):
        get_accuracy_metrics("test-predictor_arn", region_name=REGION)


def test_list_dataset_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_groups.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_dataset_groups(region_name=REGION)
    mock_client.list_dataset_groups.assert_called_once()


def test_list_dataset_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_groups",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset groups"):
        list_dataset_groups(region_name=REGION)


def test_list_dataset_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_dataset_import_jobs(region_name=REGION)
    mock_client.list_dataset_import_jobs.assert_called_once()


def test_list_dataset_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dataset_import_jobs",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dataset import jobs"):
        list_dataset_import_jobs(region_name=REGION)


def test_list_explainabilities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_explainabilities.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_explainabilities(region_name=REGION)
    mock_client.list_explainabilities.assert_called_once()


def test_list_explainabilities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_explainabilities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_explainabilities",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list explainabilities"):
        list_explainabilities(region_name=REGION)


def test_list_explainability_exports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_explainability_exports.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_explainability_exports(region_name=REGION)
    mock_client.list_explainability_exports.assert_called_once()


def test_list_explainability_exports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_explainability_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_explainability_exports",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list explainability exports"):
        list_explainability_exports(region_name=REGION)


def test_list_forecast_export_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_forecast_export_jobs.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_forecast_export_jobs(region_name=REGION)
    mock_client.list_forecast_export_jobs.assert_called_once()


def test_list_forecast_export_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_forecast_export_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_forecast_export_jobs",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list forecast export jobs"):
        list_forecast_export_jobs(region_name=REGION)


def test_list_monitor_evaluations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_monitor_evaluations.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_monitor_evaluations("test-monitor_arn", region_name=REGION)
    mock_client.list_monitor_evaluations.assert_called_once()


def test_list_monitor_evaluations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_monitor_evaluations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_monitor_evaluations",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list monitor evaluations"):
        list_monitor_evaluations("test-monitor_arn", region_name=REGION)


def test_list_monitors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_monitors.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_monitors(region_name=REGION)
    mock_client.list_monitors.assert_called_once()


def test_list_monitors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_monitors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_monitors",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list monitors"):
        list_monitors(region_name=REGION)


def test_list_predictor_backtest_export_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predictor_backtest_export_jobs.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_predictor_backtest_export_jobs(region_name=REGION)
    mock_client.list_predictor_backtest_export_jobs.assert_called_once()


def test_list_predictor_backtest_export_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predictor_backtest_export_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_predictor_backtest_export_jobs",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list predictor backtest export jobs"):
        list_predictor_backtest_export_jobs(region_name=REGION)


def test_list_predictors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predictors.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_predictors(region_name=REGION)
    mock_client.list_predictors.assert_called_once()


def test_list_predictors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predictors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_predictors",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list predictors"):
        list_predictors(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_what_if_analyses(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_analyses.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_what_if_analyses(region_name=REGION)
    mock_client.list_what_if_analyses.assert_called_once()


def test_list_what_if_analyses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_analyses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_what_if_analyses",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list what if analyses"):
        list_what_if_analyses(region_name=REGION)


def test_list_what_if_forecast_exports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_forecast_exports.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_what_if_forecast_exports(region_name=REGION)
    mock_client.list_what_if_forecast_exports.assert_called_once()


def test_list_what_if_forecast_exports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_forecast_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_what_if_forecast_exports",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list what if forecast exports"):
        list_what_if_forecast_exports(region_name=REGION)


def test_list_what_if_forecasts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_forecasts.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    list_what_if_forecasts(region_name=REGION)
    mock_client.list_what_if_forecasts.assert_called_once()


def test_list_what_if_forecasts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_what_if_forecasts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_what_if_forecasts",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list what if forecasts"):
        list_what_if_forecasts(region_name=REGION)


def test_resume_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_resource.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    resume_resource("test-resource_arn", region_name=REGION)
    mock_client.resume_resource.assert_called_once()


def test_resume_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_resource",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume resource"):
        resume_resource("test-resource_arn", region_name=REGION)


def test_stop_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_resource.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    stop_resource("test-resource_arn", region_name=REGION)
    mock_client.stop_resource.assert_called_once()


def test_stop_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_resource",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop resource"):
        stop_resource("test-resource_arn", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_dataset_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset_group.return_value = {}
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    update_dataset_group("test-dataset_group_arn", [], region_name=REGION)
    mock_client.update_dataset_group.assert_called_once()


def test_update_dataset_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dataset_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dataset_group",
    )
    monkeypatch.setattr(forecast_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dataset group"):
        update_dataset_group("test-dataset_group_arn", [], region_name=REGION)


def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_dataset
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_dataset("test-dataset_name", "test-domain", "test-dataset_type", "test-schema", data_frequency="test-data_frequency", region_name="us-east-1")
    mock_client.create_dataset.assert_called_once()

def test_create_forecast_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_forecast
    mock_client = MagicMock()
    mock_client.create_forecast.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_forecast("test-forecast_name", "test-predictor_arn", forecast_types="test-forecast_types", region_name="us-east-1")
    mock_client.create_forecast.assert_called_once()

def test_create_auto_predictor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_auto_predictor
    mock_client = MagicMock()
    mock_client.create_auto_predictor.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_auto_predictor("test-predictor_name", forecast_horizon="test-forecast_horizon", forecast_types="test-forecast_types", forecast_dimensions="test-forecast_dimensions", forecast_frequency="test-forecast_frequency", data_config={}, encryption_config={}, reference_predictor_arn="test-reference_predictor_arn", optimization_metric="test-optimization_metric", explain_predictor="test-explain_predictor", tags=[{"Key": "k", "Value": "v"}], monitor_config={}, time_alignment_boundary="test-time_alignment_boundary", region_name="us-east-1")
    mock_client.create_auto_predictor.assert_called_once()

def test_create_explainability_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_explainability
    mock_client = MagicMock()
    mock_client.create_explainability.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_explainability("test-explainability_name", "test-resource_arn", {}, data_source="test-data_source", schema="test-schema", enable_visualization=True, start_date_time="test-start_date_time", end_date_time="test-end_date_time", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_explainability.assert_called_once()

def test_create_explainability_export_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_explainability_export
    mock_client = MagicMock()
    mock_client.create_explainability_export.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_explainability_export(1, "test-explainability_arn", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.create_explainability_export.assert_called_once()

def test_create_monitor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_monitor
    mock_client = MagicMock()
    mock_client.create_monitor.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_monitor("test-monitor_name", "test-resource_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_monitor.assert_called_once()

def test_create_predictor_backtest_export_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_predictor_backtest_export_job
    mock_client = MagicMock()
    mock_client.create_predictor_backtest_export_job.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_predictor_backtest_export_job(1, "test-predictor_arn", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.create_predictor_backtest_export_job.assert_called_once()

def test_create_what_if_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_what_if_analysis
    mock_client = MagicMock()
    mock_client.create_what_if_analysis.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_what_if_analysis("test-what_if_analysis_name", "test-forecast_arn", time_series_selector="test-time_series_selector", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_what_if_analysis.assert_called_once()

def test_create_what_if_forecast_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_what_if_forecast
    mock_client = MagicMock()
    mock_client.create_what_if_forecast.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_what_if_forecast("test-what_if_forecast_name", "test-what_if_analysis_arn", time_series_transformations="test-time_series_transformations", time_series_replacements_data_source="test-time_series_replacements_data_source", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_what_if_forecast.assert_called_once()

def test_create_what_if_forecast_export_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import create_what_if_forecast_export
    mock_client = MagicMock()
    mock_client.create_what_if_forecast_export.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    create_what_if_forecast_export(1, "test-what_if_forecast_arns", "test-destination", tags=[{"Key": "k", "Value": "v"}], format="test-format", region_name="us-east-1")
    mock_client.create_what_if_forecast_export.assert_called_once()

def test_list_dataset_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_dataset_groups
    mock_client = MagicMock()
    mock_client.list_dataset_groups.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_dataset_groups(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dataset_groups.assert_called_once()

def test_list_dataset_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_dataset_import_jobs
    mock_client = MagicMock()
    mock_client.list_dataset_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_dataset_import_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_dataset_import_jobs.assert_called_once()

def test_list_explainabilities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_explainabilities
    mock_client = MagicMock()
    mock_client.list_explainabilities.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_explainabilities(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_explainabilities.assert_called_once()

def test_list_explainability_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_explainability_exports
    mock_client = MagicMock()
    mock_client.list_explainability_exports.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_explainability_exports(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_explainability_exports.assert_called_once()

def test_list_forecast_export_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_forecast_export_jobs
    mock_client = MagicMock()
    mock_client.list_forecast_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_forecast_export_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_forecast_export_jobs.assert_called_once()

def test_list_monitor_evaluations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_monitor_evaluations
    mock_client = MagicMock()
    mock_client.list_monitor_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_monitor_evaluations("test-monitor_arn", next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_monitor_evaluations.assert_called_once()

def test_list_monitors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_monitors
    mock_client = MagicMock()
    mock_client.list_monitors.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_monitors(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_monitors.assert_called_once()

def test_list_predictor_backtest_export_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_predictor_backtest_export_jobs
    mock_client = MagicMock()
    mock_client.list_predictor_backtest_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_predictor_backtest_export_jobs(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_predictor_backtest_export_jobs.assert_called_once()

def test_list_predictors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_predictors
    mock_client = MagicMock()
    mock_client.list_predictors.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_predictors(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_predictors.assert_called_once()

def test_list_what_if_analyses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_what_if_analyses
    mock_client = MagicMock()
    mock_client.list_what_if_analyses.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_what_if_analyses(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_what_if_analyses.assert_called_once()

def test_list_what_if_forecast_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_what_if_forecast_exports
    mock_client = MagicMock()
    mock_client.list_what_if_forecast_exports.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_what_if_forecast_exports(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_what_if_forecast_exports.assert_called_once()

def test_list_what_if_forecasts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.forecast import list_what_if_forecasts
    mock_client = MagicMock()
    mock_client.list_what_if_forecasts.return_value = {}
    monkeypatch.setattr("aws_util.forecast.get_client", lambda *a, **kw: mock_client)
    list_what_if_forecasts(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_what_if_forecasts.assert_called_once()
