"""Tests for aws_util.aio.emr_serverless -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.emr_serverless import (
    ApplicationResult,
    JobRunResult,
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


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


def test_models_re_exported():
    assert ApplicationResult is not None
    assert JobRunResult is not None


# ---------------------------------------------------------------------------
# Application operations
# ---------------------------------------------------------------------------


class TestCreateApplication:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"applicationId": "app-1", "name": "test", "arn": "arn:app"})
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await create_application(
            "test", release_label="emr-6.9.0", application_type="SPARK"
        )
        assert result.application_id == "app-1"

    @pytest.mark.asyncio
    async def test_with_tags(self, monkeypatch):
        mc = _mc({"applicationId": "app-1", "name": "test", "arn": "arn:app"})
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await create_application(
            "test",
            release_label="emr-6.9.0",
            application_type="SPARK",
            tags={"env": "dev"},
            region_name="us-west-2",
        )
        assert result.application_id == "app-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await create_application(
                "test", release_label="emr-6.9.0",
                application_type="SPARK",
            )


class TestGetApplication:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "application": {
                "applicationId": "app-1", "name": "test",
                "state": "STARTED",
            }
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await get_application("app-1")
        assert result.application_id == "app-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await get_application("app-1")


class TestListApplications:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"applications": [{"applicationId": "app-1", "name": "a"}], "nextToken": "tok"},
            {"applications": [{"applicationId": "app-2", "name": "b"}]},
        ]
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await list_applications()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await list_applications()


class TestDeleteApplication:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await delete_application("app-1")
        assert result == {"application_id": "app-1"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await delete_application("app-1")


class TestUpdateApplication:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "application": {"applicationId": "app-1", "name": "test"}
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await update_application("app-1")
        assert result.application_id == "app-1"

    @pytest.mark.asyncio
    async def test_all_optionals(self, monkeypatch):
        mc = _mc({
            "application": {"applicationId": "app-1", "name": "test"}
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await update_application(
            "app-1",
            initial_capacity={"c": 1},
            maximum_capacity={"c": 10},
            auto_start_configuration={"enabled": True},
            auto_stop_configuration={"enabled": False},
            region_name="eu-west-1",
        )
        assert result.application_id == "app-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await update_application("app-1")


# ---------------------------------------------------------------------------
# Job run operations
# ---------------------------------------------------------------------------


class TestStartJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "applicationId": "app-1", "jobRunId": "jr-1", "arn": "arn:jr"
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await start_job_run(
            "app-1",
            execution_role_arn="arn:role",
            job_driver={"sparkSubmitJobDriver": {}},
        )
        assert result.job_run_id == "jr-1"

    @pytest.mark.asyncio
    async def test_with_optionals(self, monkeypatch):
        mc = _mc({
            "applicationId": "app-1", "jobRunId": "jr-1", "arn": "arn:jr"
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await start_job_run(
            "app-1",
            execution_role_arn="arn:role",
            job_driver={},
            name="my-job",
            configuration_overrides={"monitoring": {}},
            region_name="us-west-2",
        )
        assert result.job_run_id == "jr-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await start_job_run(
                "app-1",
                execution_role_arn="arn:role",
                job_driver={},
            )


class TestGetJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "jobRun": {
                "applicationId": "app-1", "jobRunId": "jr-1",
                "name": "job",
            }
        })
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await get_job_run("app-1", "jr-1")
        assert result.job_run_id == "jr-1"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await get_job_run("app-1", "jr-1")


class TestListJobRuns:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"jobRuns": [{"applicationId": "app-1", "jobRunId": "jr-1"}], "nextToken": "tok"},
            {"jobRuns": [{"applicationId": "app-1", "jobRunId": "jr-2"}]},
        ]
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await list_job_runs("app-1")
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await list_job_runs("app-1")


class TestCancelJobRun:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        result = await cancel_job_run("app-1", "jr-1")
        assert result == {"application_id": "app-1", "job_run_id": "jr-1"}

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr(
            "aws_util.aio.emr_serverless.async_client",
            lambda *a, **kw: mc,
        )
        with pytest.raises(RuntimeError):
            await cancel_job_run("app-1", "jr-1")


async def test_get_dashboard_for_job_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dashboard_for_job_run("test-application_id", "test-job_run_id", )
    mock_client.call.assert_called_once()


async def test_get_dashboard_for_job_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dashboard_for_job_run("test-application_id", "test-job_run_id", )


async def test_list_job_run_attempts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_job_run_attempts("test-application_id", "test-job_run_id", )
    mock_client.call.assert_called_once()


async def test_list_job_run_attempts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_job_run_attempts("test-application_id", "test-job_run_id", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_start_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_application("test-application_id", )
    mock_client.call.assert_called_once()


async def test_start_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_application("test-application_id", )


async def test_stop_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_application("test-application_id", )
    mock_client.call.assert_called_once()


async def test_stop_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_application("test-application_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr_serverless.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_update_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_serverless import update_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_serverless.async_client", lambda *a, **kw: mock_client)
    await update_application("test-application_id", initial_capacity="test-initial_capacity", maximum_capacity=1, auto_start_configuration=True, auto_stop_configuration=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_dashboard_for_job_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_serverless import get_dashboard_for_job_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_serverless.async_client", lambda *a, **kw: mock_client)
    await get_dashboard_for_job_run("test-application_id", "test-job_run_id", attempt="test-attempt", access_system_profile_logs="test-access_system_profile_logs", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_run_attempts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr_serverless import list_job_run_attempts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr_serverless.async_client", lambda *a, **kw: mock_client)
    await list_job_run_attempts("test-application_id", "test-job_run_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
