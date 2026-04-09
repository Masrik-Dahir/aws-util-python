"""Tests for aws_util.aio.databrew -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.databrew import (
    DatasetResult,
    JobResult,
    JobRunResult,
    ProjectResult,
    RecipeResult,
    create_dataset,
    create_project,
    create_recipe,
    create_recipe_job,
    delete_dataset,
    delete_project,
    describe_dataset,
    describe_job,
    describe_project,
    list_datasets,
    list_job_runs,
    list_jobs,
    list_projects,
    list_recipes,
    start_job_run,
    batch_delete_recipe_version,
    create_profile_job,
    create_ruleset,
    create_schedule,
    delete_job,
    delete_recipe_version,
    delete_ruleset,
    delete_schedule,
    describe_job_run,
    describe_recipe,
    describe_ruleset,
    describe_schedule,
    list_recipe_versions,
    list_rulesets,
    list_schedules,
    list_tags_for_resource,
    publish_recipe,
    send_project_session_action,
    start_project_session,
    stop_job_run,
    tag_resource,
    untag_resource,
    update_dataset,
    update_profile_job,
    update_project,
    update_recipe,
    update_recipe_job,
    update_ruleset,
    update_schedule,
)


def _mock_factory(mc):
    return lambda *a, **kw: mc


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_dataset_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "ds1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_dataset("ds1", input_config={"S3": {}})
    assert isinstance(r, DatasetResult)


@pytest.mark.asyncio
async def test_create_dataset_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "ds1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_dataset(
        "ds1", input_config={"S3": {}},
        format_type="CSV", tags={"k": "v"},
    )
    assert isinstance(r, DatasetResult)


@pytest.mark.asyncio
async def test_create_dataset_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_dataset("ds1", input_config={"S3": {}})


@pytest.mark.asyncio
async def test_create_dataset_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await create_dataset("ds1", input_config={"S3": {}})


@pytest.mark.asyncio
async def test_describe_dataset_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "ds1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await describe_dataset("ds1")
    assert isinstance(r, DatasetResult)


@pytest.mark.asyncio
async def test_describe_dataset_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_dataset("ds1")


@pytest.mark.asyncio
async def test_describe_dataset_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await describe_dataset("ds1")


@pytest.mark.asyncio
async def test_list_datasets_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Datasets": [{"Name": "ds1"}]}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_datasets()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_datasets_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Datasets": [{"Name": "ds1"}], "NextToken": "tok"},
        {"Datasets": [{"Name": "ds2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_datasets()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_datasets_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_datasets()


@pytest.mark.asyncio
async def test_list_datasets_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await list_datasets()


@pytest.mark.asyncio
async def test_delete_dataset_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await delete_dataset("ds1")
    assert r == {"name": "ds1"}


@pytest.mark.asyncio
async def test_delete_dataset_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_dataset("ds1")


@pytest.mark.asyncio
async def test_delete_dataset_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await delete_dataset("ds1")


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_project_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "proj1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_project(
        "proj1", dataset_name="ds", recipe_name="r", role_arn="arn:role",
    )
    assert isinstance(r, ProjectResult)


@pytest.mark.asyncio
async def test_create_project_with_tags(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "proj1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_project(
        "proj1", dataset_name="ds", recipe_name="r",
        role_arn="arn:role", tags={"k": "v"},
    )
    assert isinstance(r, ProjectResult)


@pytest.mark.asyncio
async def test_create_project_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_project(
            "proj1", dataset_name="ds",
            recipe_name="r", role_arn="arn:role",
        )


@pytest.mark.asyncio
async def test_create_project_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await create_project(
            "proj1", dataset_name="ds",
            recipe_name="r", role_arn="arn:role",
        )


@pytest.mark.asyncio
async def test_describe_project_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "proj1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await describe_project("proj1")
    assert isinstance(r, ProjectResult)


@pytest.mark.asyncio
async def test_describe_project_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_project("proj1")


@pytest.mark.asyncio
async def test_describe_project_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await describe_project("proj1")


@pytest.mark.asyncio
async def test_list_projects_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Projects": [{"Name": "p1"}]}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_projects()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_projects_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Projects": [{"Name": "p1"}], "NextToken": "tok"},
        {"Projects": [{"Name": "p2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_projects()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_projects_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_projects()


@pytest.mark.asyncio
async def test_list_projects_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await list_projects()


@pytest.mark.asyncio
async def test_delete_project_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await delete_project("proj1")
    assert r == {"name": "proj1"}


@pytest.mark.asyncio
async def test_delete_project_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_project("proj1")


@pytest.mark.asyncio
async def test_delete_project_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await delete_project("proj1")


# ---------------------------------------------------------------------------
# Recipe operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_recipe_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "rec1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_recipe("rec1", steps=[{"Action": {}}])
    assert isinstance(r, RecipeResult)


@pytest.mark.asyncio
async def test_create_recipe_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "rec1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_recipe(
        "rec1", steps=[{"Action": {}}],
        description="desc", tags={"k": "v"},
    )
    assert isinstance(r, RecipeResult)


@pytest.mark.asyncio
async def test_create_recipe_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_recipe("rec1", steps=[{"Action": {}}])


@pytest.mark.asyncio
async def test_create_recipe_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await create_recipe("rec1", steps=[{"Action": {}}])


@pytest.mark.asyncio
async def test_list_recipes_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Recipes": [{"Name": "r1"}]}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_recipes()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_recipes_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Recipes": [{"Name": "r1"}], "NextToken": "tok"},
        {"Recipes": [{"Name": "r2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_recipes()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_recipes_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_recipes()


@pytest.mark.asyncio
async def test_list_recipes_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await list_recipes()


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_recipe_job_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "job1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_recipe_job("job1", role_arn="arn:role")
    assert isinstance(r, JobResult)


@pytest.mark.asyncio
async def test_create_recipe_job_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "job1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await create_recipe_job(
        "job1", role_arn="arn:role",
        dataset_name="ds", project_name="proj",
        outputs=[{"Location": {}}], tags={"k": "v"},
    )
    assert isinstance(r, JobResult)


@pytest.mark.asyncio
async def test_create_recipe_job_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_recipe_job("job1", role_arn="arn:role")


@pytest.mark.asyncio
async def test_create_recipe_job_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await create_recipe_job("job1", role_arn="arn:role")


@pytest.mark.asyncio
async def test_describe_job_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Name": "job1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await describe_job("job1")
    assert isinstance(r, JobResult)


@pytest.mark.asyncio
async def test_describe_job_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_job("job1")


@pytest.mark.asyncio
async def test_describe_job_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await describe_job("job1")


@pytest.mark.asyncio
async def test_list_jobs_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Jobs": [{"Name": "j1"}]}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_jobs()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_jobs_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Jobs": [{"Name": "j1"}], "NextToken": "tok"},
        {"Jobs": [{"Name": "j2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_jobs()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_jobs_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_jobs()


@pytest.mark.asyncio
async def test_list_jobs_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await list_jobs()


@pytest.mark.asyncio
async def test_start_job_run_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"RunId": "run1"}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await start_job_run("job1")
    assert r == "run1"


@pytest.mark.asyncio
async def test_start_job_run_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await start_job_run("job1")


@pytest.mark.asyncio
async def test_start_job_run_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await start_job_run("job1")


@pytest.mark.asyncio
async def test_list_job_runs_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"JobRuns": [{"RunId": "r1", "JobName": "j"}]}
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_job_runs("job1")
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_job_runs_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"JobRuns": [{"RunId": "r1"}], "NextToken": "tok"},
        {"JobRuns": [{"RunId": "r2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    r = await list_job_runs("job1")
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_job_runs_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_job_runs("job1")


@pytest.mark.asyncio
async def test_list_job_runs_runtime_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = RuntimeError("already classified")
    monkeypatch.setattr("aws_util.aio.databrew.async_client", _mock_factory(mc))
    with pytest.raises(RuntimeError, match="already classified"):
        await list_job_runs("job1")


async def test_batch_delete_recipe_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_recipe_version("test-name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_recipe_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_recipe_version("test-name", [], )


async def test_create_profile_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_profile_job("test-dataset_name", "test-name", {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_profile_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_profile_job("test-dataset_name", "test-name", {}, "test-role_arn", )


async def test_create_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ruleset("test-name", "test-target_arn", [], )
    mock_client.call.assert_called_once()


async def test_create_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ruleset("test-name", "test-target_arn", [], )


async def test_create_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_schedule("test-cron_expression", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_schedule("test-cron_expression", "test-name", )


async def test_delete_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job("test-name", )


async def test_delete_recipe_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_recipe_version("test-name", "test-recipe_version", )
    mock_client.call.assert_called_once()


async def test_delete_recipe_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_recipe_version("test-name", "test-recipe_version", )


async def test_delete_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ruleset("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ruleset("test-name", )


async def test_delete_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_schedule("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_schedule("test-name", )


async def test_describe_job_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_job_run("test-name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_describe_job_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_job_run("test-name", "test-run_id", )


async def test_describe_recipe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_recipe("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_recipe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_recipe("test-name", )


async def test_describe_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ruleset("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ruleset("test-name", )


async def test_describe_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_schedule("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_schedule("test-name", )


async def test_list_recipe_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_recipe_versions("test-name", )
    mock_client.call.assert_called_once()


async def test_list_recipe_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_recipe_versions("test-name", )


async def test_list_rulesets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rulesets()
    mock_client.call.assert_called_once()


async def test_list_rulesets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rulesets()


async def test_list_schedules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_schedules()
    mock_client.call.assert_called_once()


async def test_list_schedules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_schedules()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_publish_recipe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_recipe("test-name", )
    mock_client.call.assert_called_once()


async def test_publish_recipe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_recipe("test-name", )


async def test_send_project_session_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_project_session_action("test-name", )
    mock_client.call.assert_called_once()


async def test_send_project_session_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_project_session_action("test-name", )


async def test_start_project_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_project_session("test-name", )
    mock_client.call.assert_called_once()


async def test_start_project_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_project_session("test-name", )


async def test_stop_job_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_job_run("test-name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_stop_job_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_job_run("test-name", "test-run_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dataset("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dataset("test-name", {}, )


async def test_update_profile_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_profile_job("test-name", {}, "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_update_profile_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_profile_job("test-name", {}, "test-role_arn", )


async def test_update_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_project("test-role_arn", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_project("test-role_arn", "test-name", )


async def test_update_recipe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_recipe("test-name", )
    mock_client.call.assert_called_once()


async def test_update_recipe_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_recipe("test-name", )


async def test_update_recipe_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_recipe_job("test-name", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_update_recipe_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_recipe_job("test-name", "test-role_arn", )


async def test_update_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ruleset("test-name", [], )
    mock_client.call.assert_called_once()


async def test_update_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ruleset("test-name", [], )


async def test_update_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_schedule("test-cron_expression", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.databrew.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_schedule("test-cron_expression", "test-name", )


@pytest.mark.asyncio
async def test_create_profile_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import create_profile_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await create_profile_job("test-dataset_name", "test-name", "test-output_location", "test-role_arn", encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, configuration={}, validation_configurations={}, tags=[{"Key": "k", "Value": "v"}], timeout=1, job_sample="test-job_sample", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ruleset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import create_ruleset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await create_ruleset("test-name", "test-target_arn", "test-rules", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import create_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await create_schedule("test-cron_expression", "test-name", job_names="test-job_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_recipe_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import describe_recipe
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await describe_recipe("test-name", recipe_version="test-recipe_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recipe_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import list_recipe_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await list_recipe_versions("test-name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rulesets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import list_rulesets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await list_rulesets(target_arn="test-target_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_schedules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import list_schedules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await list_schedules(job_name="test-job_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_recipe_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import publish_recipe
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await publish_recipe("test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_project_session_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import send_project_session_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await send_project_session_action("test-name", preview="test-preview", recipe_step="test-recipe_step", step_index="test-step_index", client_session_id="test-client_session_id", view_frame="test-view_frame", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_project_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import start_project_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await start_project_session("test-name", assume_control="test-assume_control", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_dataset("test-name", "test-input", format="test-format", format_options={}, path_options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_profile_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_profile_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_profile_job("test-name", "test-output_location", "test-role_arn", configuration={}, encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, validation_configurations={}, timeout=1, job_sample="test-job_sample", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_project("test-role_arn", "test-name", sample="test-sample", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_recipe_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_recipe
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_recipe("test-name", description="test-description", steps="test-steps", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_recipe_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_recipe_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_recipe_job("test-name", "test-role_arn", encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, outputs="test-outputs", data_catalog_outputs="test-data_catalog_outputs", database_outputs="test-database_outputs", timeout=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ruleset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_ruleset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_ruleset("test-name", "test-rules", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.databrew import update_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.databrew.async_client", lambda *a, **kw: mock_client)
    await update_schedule("test-cron_expression", "test-name", job_names="test-job_names", region_name="us-east-1")
    mock_client.call.assert_called_once()
