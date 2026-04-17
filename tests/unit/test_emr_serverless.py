"""Tests for aws_util.emr_serverless -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.emr_serverless import (
    ApplicationResult,
    JobRunResult,
    _parse_application,
    _parse_job_run,
    cancel_job_run,
    create_application,
    delete_application,
    get_application,
    get_job_run,
    list_applications,
    list_job_runs,
    start_job_run,
    update_application,
    get_dashboard_for_job_run,
    list_job_run_attempts,
    list_tags_for_resource,
    start_application,
    stop_application,
    tag_resource,
    untag_resource,
)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestApplicationResult:
    def test_minimal(self):
        app = ApplicationResult(application_id="app-1", name="test")
        assert app.application_id == "app-1"
        assert app.arn == ""
        assert app.release_label is None
        assert app.type is None
        assert app.created_at is None
        assert app.updated_at is None
        assert app.tags == {}
        assert app.extra == {}

    def test_full(self):
        app = ApplicationResult(
            application_id="app-1",
            name="test",
            arn="arn:app",
            state="STARTED",
            release_label="emr-6.9.0",
            type="SPARK",
            created_at="2024-01-01",
            updated_at="2024-01-02",
            tags={"env": "dev"},
            extra={"foo": "bar"},
        )
        assert app.type == "SPARK"


class TestJobRunResult:
    def test_minimal(self):
        jr = JobRunResult(application_id="app-1", job_run_id="jr-1")
        assert jr.name == ""
        assert jr.state_details is None
        assert jr.execution_role is None

    def test_full(self):
        jr = JobRunResult(
            application_id="app-1",
            job_run_id="jr-1",
            name="job",
            arn="arn:jr",
            state="SUCCESS",
            state_details="done",
            created_at="2024-01-01",
            updated_at="2024-01-02",
            execution_role="arn:role",
            extra={"k": "v"},
        )
        assert jr.execution_role == "arn:role"


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_application_full(self):
        data = {
            "applicationId": "app-1",
            "name": "test",
            "arn": "arn:app",
            "state": "STARTED",
            "releaseLabel": "emr-6.9.0",
            "type": "SPARK",
            "createdAt": "2024-01-01",
            "updatedAt": "2024-01-02",
            "tags": {"env": "dev"},
            "extraField": "val",
        }
        app = _parse_application(data)
        assert app.created_at == "2024-01-01"
        assert app.updated_at == "2024-01-02"
        assert app.extra == {"extraField": "val"}

    def test_parse_application_none_times(self):
        data = {"applicationId": "app-1", "name": "test"}
        app = _parse_application(data)
        assert app.created_at is None
        assert app.updated_at is None

    def test_parse_job_run_full(self):
        data = {
            "applicationId": "app-1",
            "jobRunId": "jr-1",
            "name": "job",
            "arn": "arn:jr",
            "state": "SUCCESS",
            "stateDetails": "done",
            "createdAt": "2024-01-01",
            "updatedAt": "2024-01-02",
            "executionRoleArn": "arn:role",
            "extra_key": "extra_val",
        }
        jr = _parse_job_run(data)
        assert jr.created_at == "2024-01-01"
        assert jr.execution_role == "arn:role"
        assert jr.extra == {"extra_key": "extra_val"}

    def test_parse_job_run_none_times(self):
        data = {"applicationId": "app-1", "jobRunId": "jr-1"}
        jr = _parse_job_run(data)
        assert jr.created_at is None
        assert jr.updated_at is None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ERR = ClientError(
    {"Error": {"Code": "ValidationException", "Message": "bad"}}, "op"
)


# ---------------------------------------------------------------------------
# Application function tests
# ---------------------------------------------------------------------------


class TestCreateApplication:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.create_application.return_value = {
            "applicationId": "app-1", "name": "test", "arn": "arn:app"
        }
        mock_gc.return_value = client
        result = create_application(
            "test", release_label="emr-6.9.0", application_type="SPARK"
        )
        assert result.application_id == "app-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_with_tags(self, mock_gc):
        client = MagicMock()
        client.create_application.return_value = {
            "applicationId": "app-1", "name": "test", "arn": "arn:app"
        }
        mock_gc.return_value = client
        result = create_application(
            "test",
            release_label="emr-6.9.0",
            application_type="SPARK",
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.application_id == "app-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.create_application.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            create_application(
                "test", release_label="emr-6.9.0",
                application_type="SPARK",
            )


class TestGetApplication:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_application.return_value = {
            "application": {
                "applicationId": "app-1", "name": "test",
                "state": "STARTED",
            }
        }
        mock_gc.return_value = client
        result = get_application("app-1")
        assert result.application_id == "app-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_application.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            get_application("app-1")


class TestListApplications:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"applications": [{"applicationId": "app-1", "name": "a"}]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_applications()
        assert len(result) == 1

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_applications()


class TestDeleteApplication:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        result = delete_application("app-1")
        assert result == {"application_id": "app-1"}

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.delete_application.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            delete_application("app-1")


class TestUpdateApplication:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.update_application.return_value = {
            "application": {"applicationId": "app-1", "name": "test"}
        }
        mock_gc.return_value = client
        result = update_application("app-1")
        assert result.application_id == "app-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_all_optionals(self, mock_gc):
        client = MagicMock()
        client.update_application.return_value = {
            "application": {"applicationId": "app-1", "name": "test"}
        }
        mock_gc.return_value = client
        result = update_application(
            "app-1",
            initial_capacity={"c": 1},
            maximum_capacity={"c": 10},
            auto_start_configuration={"enabled": True},
            auto_stop_configuration={"enabled": False},
            region_name="eu-west-1",
        )
        assert result.application_id == "app-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.update_application.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            update_application("app-1")


# ---------------------------------------------------------------------------
# Job run function tests
# ---------------------------------------------------------------------------


class TestStartJobRun:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.start_job_run.return_value = {
            "applicationId": "app-1", "jobRunId": "jr-1", "arn": "arn:jr"
        }
        mock_gc.return_value = client
        result = start_job_run(
            "app-1",
            execution_role_arn="arn:role",
            job_driver={"sparkSubmitJobDriver": {}},
        )
        assert result.job_run_id == "jr-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_with_optionals(self, mock_gc):
        client = MagicMock()
        client.start_job_run.return_value = {
            "applicationId": "app-1", "jobRunId": "jr-1", "arn": "arn:jr"
        }
        mock_gc.return_value = client
        result = start_job_run(
            "app-1",
            execution_role_arn="arn:role",
            job_driver={},
            name="my-job",
            configuration_overrides={"monitoring": {}},
            region_name="us-west-2",
        )
        assert result.job_run_id == "jr-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.start_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            start_job_run(
                "app-1",
                execution_role_arn="arn:role",
                job_driver={},
            )


class TestGetJobRun:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        client.get_job_run.return_value = {
            "jobRun": {
                "applicationId": "app-1", "jobRunId": "jr-1",
                "name": "job",
            }
        }
        mock_gc.return_value = client
        result = get_job_run("app-1", "jr-1")
        assert result.job_run_id == "jr-1"

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.get_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            get_job_run("app-1", "jr-1")


class TestListJobRuns:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.return_value = [
            {"jobRuns": [{"applicationId": "app-1", "jobRunId": "jr-1"}]},
        ]
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        result = list_job_runs("app-1")
        assert len(result) == 1

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _ERR
        client.get_paginator.return_value = paginator
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            list_job_runs("app-1")


class TestCancelJobRun:
    @patch("aws_util.emr_serverless.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        result = cancel_job_run("app-1", "jr-1")
        assert result == {
            "application_id": "app-1", "job_run_id": "jr-1"
        }

    @patch("aws_util.emr_serverless.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        client.cancel_job_run.side_effect = _ERR
        mock_gc.return_value = client
        with pytest.raises(RuntimeError):
            cancel_job_run("app-1", "jr-1")


REGION = "us-east-1"


@patch("aws_util.emr_serverless.get_client")
def test_get_dashboard_for_job_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_dashboard_for_job_run.return_value = {}
    get_dashboard_for_job_run("test-application_id", "test-job_run_id", region_name=REGION)
    mock_client.get_dashboard_for_job_run.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_get_dashboard_for_job_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_dashboard_for_job_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dashboard_for_job_run",
    )
    with pytest.raises(RuntimeError, match="Failed to get dashboard for job run"):
        get_dashboard_for_job_run("test-application_id", "test-job_run_id", region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_list_job_run_attempts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_run_attempts.return_value = {}
    list_job_run_attempts("test-application_id", "test-job_run_id", region_name=REGION)
    mock_client.list_job_run_attempts.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_list_job_run_attempts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_run_attempts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_job_run_attempts",
    )
    with pytest.raises(RuntimeError, match="Failed to list job run attempts"):
        list_job_run_attempts("test-application_id", "test-job_run_id", region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_start_application(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_application.return_value = {}
    start_application("test-application_id", region_name=REGION)
    mock_client.start_application.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_start_application_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_application",
    )
    with pytest.raises(RuntimeError, match="Failed to start application"):
        start_application("test-application_id", region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_stop_application(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_application.return_value = {}
    stop_application("test-application_id", region_name=REGION)
    mock_client.stop_application.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_stop_application_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_application",
    )
    with pytest.raises(RuntimeError, match="Failed to stop application"):
        stop_application("test-application_id", region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.emr_serverless.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.emr_serverless.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_serverless import update_application
    mock_client = MagicMock()
    mock_client.update_application.return_value = {}
    monkeypatch.setattr("aws_util.emr_serverless.get_client", lambda *a, **kw: mock_client)
    update_application("test-application_id", initial_capacity="test-initial_capacity", maximum_capacity=1, auto_start_configuration=True, auto_stop_configuration=True, region_name="us-east-1")
    mock_client.update_application.assert_called_once()

def test_get_dashboard_for_job_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_serverless import get_dashboard_for_job_run
    mock_client = MagicMock()
    mock_client.get_dashboard_for_job_run.return_value = {}
    monkeypatch.setattr("aws_util.emr_serverless.get_client", lambda *a, **kw: mock_client)
    get_dashboard_for_job_run("test-application_id", "test-job_run_id", attempt="test-attempt", access_system_profile_logs="test-access_system_profile_logs", region_name="us-east-1")
    mock_client.get_dashboard_for_job_run.assert_called_once()

def test_list_job_run_attempts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.emr_serverless import list_job_run_attempts
    mock_client = MagicMock()
    mock_client.list_job_run_attempts.return_value = {}
    monkeypatch.setattr("aws_util.emr_serverless.get_client", lambda *a, **kw: mock_client)
    list_job_run_attempts("test-application_id", "test-job_run_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_job_run_attempts.assert_called_once()
