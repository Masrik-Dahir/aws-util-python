"""Tests for aws_util.databrew -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.databrew import (
    DatasetResult,
    JobResult,
    JobRunResult,
    ProjectResult,
    RecipeResult,
    _parse_dataset,
    _parse_job,
    _parse_job_run,
    _parse_project,
    _parse_recipe,
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


def _ce(code: str = "SomeError", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "Op")


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


class TestParseDataset:
    def test_minimal(self):
        r = _parse_dataset({"Name": "ds1"})
        assert isinstance(r, DatasetResult)
        assert r.name == "ds1"

    def test_full(self):
        r = _parse_dataset({
            "Name": "ds1", "AccountId": "123", "CreatedBy": "user",
            "CreateDate": "2024-01-01", "Format": "CSV",
            "Input": {"S3": {}}, "Tags": {"k": "v"}, "Custom": "x",
        })
        assert r.account_id == "123"
        assert r.created_by == "user"
        assert r.create_date == "2024-01-01"
        assert r.format == "CSV"
        assert r.extra == {"Custom": "x"}

    def test_no_create_date(self):
        r = _parse_dataset({"Name": "ds"})
        assert r.create_date is None


class TestParseProject:
    def test_minimal(self):
        r = _parse_project({"Name": "proj1"})
        assert isinstance(r, ProjectResult)

    def test_full(self):
        r = _parse_project({
            "Name": "proj1", "AccountId": "123", "RecipeName": "r",
            "DatasetName": "ds", "RoleArn": "arn:role",
            "CreateDate": "2024-01-01", "Tags": {"k": "v"}, "Custom": "x",
        })
        assert r.recipe_name == "r"
        assert r.dataset_name == "ds"
        assert r.extra == {"Custom": "x"}

    def test_no_create_date(self):
        r = _parse_project({"Name": "p"})
        assert r.create_date is None


class TestParseRecipe:
    def test_minimal(self):
        r = _parse_recipe({"Name": "rec1"})
        assert isinstance(r, RecipeResult)

    def test_full(self):
        r = _parse_recipe({
            "Name": "rec1", "RecipeVersion": "1.0",
            "Description": "desc", "Steps": [{"Action": {}}],
            "CreateDate": "2024-01-01", "Tags": {"k": "v"}, "Custom": "x",
        })
        assert r.recipe_version == "1.0"
        assert r.description == "desc"
        assert r.extra == {"Custom": "x"}

    def test_no_create_date(self):
        r = _parse_recipe({"Name": "r"})
        assert r.create_date is None


class TestParseJob:
    def test_minimal(self):
        r = _parse_job({"Name": "job1"})
        assert isinstance(r, JobResult)

    def test_full(self):
        r = _parse_job({
            "Name": "job1", "Type": "RECIPE", "DatasetName": "ds",
            "RoleArn": "arn:role", "Outputs": [{"Location": {}}],
            "CreateDate": "2024-01-01", "Tags": {"k": "v"}, "Custom": "x",
        })
        assert r.type == "RECIPE"
        assert r.extra == {"Custom": "x"}

    def test_no_create_date(self):
        r = _parse_job({"Name": "j"})
        assert r.create_date is None


class TestParseJobRun:
    def test_minimal(self):
        r = _parse_job_run({"RunId": "run1"})
        assert isinstance(r, JobRunResult)

    def test_full(self):
        r = _parse_job_run({
            "RunId": "run1", "JobName": "j", "State": "SUCCEEDED",
            "StartedOn": "2024-01-01", "CompletedOn": "2024-01-02",
            "ErrorMessage": None, "Custom": "x",
        })
        assert r.started_on == "2024-01-01"
        assert r.completed_on == "2024-01-02"
        assert r.extra == {"Custom": "x"}

    def test_no_dates(self):
        r = _parse_job_run({"RunId": "run1"})
        assert r.started_on is None
        assert r.completed_on is None


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


class TestCreateDataset:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_dataset.return_value = {"Name": "ds1"}
        r = create_dataset("ds1", input_config={"S3": {}})
        assert isinstance(r, DatasetResult)

    @patch("aws_util.databrew.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_dataset.return_value = {"Name": "ds1"}
        r = create_dataset(
            "ds1", input_config={"S3": {}},
            format_type="CSV", tags={"k": "v"},
        )
        assert isinstance(r, DatasetResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_dataset.side_effect = _ce()
        with pytest.raises(Exception):
            create_dataset("ds1", input_config={"S3": {}})


class TestDescribeDataset:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_dataset.return_value = {"Name": "ds1"}
        r = describe_dataset("ds1")
        assert isinstance(r, DatasetResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_dataset.side_effect = _ce()
        with pytest.raises(Exception):
            describe_dataset("ds1")


class TestListDatasets:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"Datasets": [{"Name": "ds1"}]}]
        r = list_datasets()
        assert len(r) == 1

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_datasets()


class TestDeleteDataset:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_dataset.return_value = {}
        r = delete_dataset("ds1")
        assert r == {"name": "ds1"}

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_dataset.side_effect = _ce()
        with pytest.raises(Exception):
            delete_dataset("ds1")


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


class TestCreateProject:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_project.return_value = {"Name": "proj1"}
        r = create_project(
            "proj1", dataset_name="ds", recipe_name="r", role_arn="arn:role",
        )
        assert isinstance(r, ProjectResult)

    @patch("aws_util.databrew.get_client")
    def test_with_tags(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_project.return_value = {"Name": "proj1"}
        r = create_project(
            "proj1", dataset_name="ds", recipe_name="r",
            role_arn="arn:role", tags={"k": "v"},
        )
        assert isinstance(r, ProjectResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_project.side_effect = _ce()
        with pytest.raises(Exception):
            create_project(
                "proj1", dataset_name="ds",
                recipe_name="r", role_arn="arn:role",
            )


class TestDescribeProject:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_project.return_value = {"Name": "proj1"}
        r = describe_project("proj1")
        assert isinstance(r, ProjectResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_project.side_effect = _ce()
        with pytest.raises(Exception):
            describe_project("proj1")


class TestListProjects:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"Projects": [{"Name": "p1"}]}]
        r = list_projects()
        assert len(r) == 1

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_projects()


class TestDeleteProject:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_project.return_value = {}
        r = delete_project("proj1")
        assert r == {"name": "proj1"}

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_project.side_effect = _ce()
        with pytest.raises(Exception):
            delete_project("proj1")


# ---------------------------------------------------------------------------
# Recipe operations
# ---------------------------------------------------------------------------


class TestCreateRecipe:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe.return_value = {"Name": "rec1"}
        r = create_recipe("rec1", steps=[{"Action": {}}])
        assert isinstance(r, RecipeResult)

    @patch("aws_util.databrew.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe.return_value = {"Name": "rec1"}
        r = create_recipe(
            "rec1", steps=[{"Action": {}}],
            description="desc", tags={"k": "v"},
        )
        assert isinstance(r, RecipeResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe.side_effect = _ce()
        with pytest.raises(Exception):
            create_recipe("rec1", steps=[{"Action": {}}])


class TestListRecipes:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"Recipes": [{"Name": "r1"}]}]
        r = list_recipes()
        assert len(r) == 1

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_recipes()


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


class TestCreateRecipeJob:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe_job.return_value = {"Name": "job1"}
        r = create_recipe_job("job1", role_arn="arn:role")
        assert isinstance(r, JobResult)

    @patch("aws_util.databrew.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe_job.return_value = {"Name": "job1"}
        r = create_recipe_job(
            "job1", role_arn="arn:role",
            dataset_name="ds", project_name="proj",
            outputs=[{"Location": {}}], tags={"k": "v"},
        )
        assert isinstance(r, JobResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_recipe_job.side_effect = _ce()
        with pytest.raises(Exception):
            create_recipe_job("job1", role_arn="arn:role")


class TestDescribeJob:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_job.return_value = {"Name": "job1"}
        r = describe_job("job1")
        assert isinstance(r, JobResult)

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_job.side_effect = _ce()
        with pytest.raises(Exception):
            describe_job("job1")


class TestListJobs:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [{"Jobs": [{"Name": "j1"}]}]
        r = list_jobs()
        assert len(r) == 1

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_jobs()


class TestStartJobRun:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.start_job_run.return_value = {"RunId": "run1"}
        r = start_job_run("job1")
        assert r == "run1"

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.start_job_run.side_effect = _ce()
        with pytest.raises(Exception):
            start_job_run("job1")


class TestListJobRuns:
    @patch("aws_util.databrew.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.return_value = [
            {"JobRuns": [{"RunId": "r1", "JobName": "j"}]},
        ]
        r = list_job_runs("job1")
        assert len(r) == 1

    @patch("aws_util.databrew.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        paginator = MagicMock()
        client.get_paginator.return_value = paginator
        paginator.paginate.side_effect = _ce()
        with pytest.raises(Exception):
            list_job_runs("job1")


REGION = "us-east-1"


@patch("aws_util.databrew.get_client")
def test_batch_delete_recipe_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_recipe_version.return_value = {}
    batch_delete_recipe_version("test-name", [], region_name=REGION)
    mock_client.batch_delete_recipe_version.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_batch_delete_recipe_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_recipe_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_recipe_version",
    )
    with pytest.raises(RuntimeError, match="Failed to batch delete recipe version"):
        batch_delete_recipe_version("test-name", [], region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_create_profile_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_profile_job.return_value = {}
    create_profile_job("test-dataset_name", "test-name", {}, "test-role_arn", region_name=REGION)
    mock_client.create_profile_job.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_create_profile_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_profile_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_profile_job",
    )
    with pytest.raises(RuntimeError, match="Failed to create profile job"):
        create_profile_job("test-dataset_name", "test-name", {}, "test-role_arn", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_create_ruleset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_ruleset.return_value = {}
    create_ruleset("test-name", "test-target_arn", [], region_name=REGION)
    mock_client.create_ruleset.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_create_ruleset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ruleset",
    )
    with pytest.raises(RuntimeError, match="Failed to create ruleset"):
        create_ruleset("test-name", "test-target_arn", [], region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_create_schedule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_schedule.return_value = {}
    create_schedule("test-cron_expression", "test-name", region_name=REGION)
    mock_client.create_schedule.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_create_schedule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_schedule",
    )
    with pytest.raises(RuntimeError, match="Failed to create schedule"):
        create_schedule("test-cron_expression", "test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_delete_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job.return_value = {}
    delete_job("test-name", region_name=REGION)
    mock_client.delete_job.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_delete_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job",
    )
    with pytest.raises(RuntimeError, match="Failed to delete job"):
        delete_job("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_delete_recipe_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_recipe_version.return_value = {}
    delete_recipe_version("test-name", "test-recipe_version", region_name=REGION)
    mock_client.delete_recipe_version.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_delete_recipe_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_recipe_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_recipe_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete recipe version"):
        delete_recipe_version("test-name", "test-recipe_version", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_delete_ruleset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ruleset.return_value = {}
    delete_ruleset("test-name", region_name=REGION)
    mock_client.delete_ruleset.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_delete_ruleset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ruleset",
    )
    with pytest.raises(RuntimeError, match="Failed to delete ruleset"):
        delete_ruleset("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_delete_schedule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_schedule.return_value = {}
    delete_schedule("test-name", region_name=REGION)
    mock_client.delete_schedule.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_delete_schedule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_schedule",
    )
    with pytest.raises(RuntimeError, match="Failed to delete schedule"):
        delete_schedule("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_describe_job_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_run.return_value = {}
    describe_job_run("test-name", "test-run_id", region_name=REGION)
    mock_client.describe_job_run.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_describe_job_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_job_run",
    )
    with pytest.raises(RuntimeError, match="Failed to describe job run"):
        describe_job_run("test-name", "test-run_id", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_describe_recipe(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recipe.return_value = {}
    describe_recipe("test-name", region_name=REGION)
    mock_client.describe_recipe.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_describe_recipe_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_recipe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_recipe",
    )
    with pytest.raises(RuntimeError, match="Failed to describe recipe"):
        describe_recipe("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_describe_ruleset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_ruleset.return_value = {}
    describe_ruleset("test-name", region_name=REGION)
    mock_client.describe_ruleset.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_describe_ruleset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ruleset",
    )
    with pytest.raises(RuntimeError, match="Failed to describe ruleset"):
        describe_ruleset("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_describe_schedule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_schedule.return_value = {}
    describe_schedule("test-name", region_name=REGION)
    mock_client.describe_schedule.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_describe_schedule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_schedule",
    )
    with pytest.raises(RuntimeError, match="Failed to describe schedule"):
        describe_schedule("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_list_recipe_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_recipe_versions.return_value = {}
    list_recipe_versions("test-name", region_name=REGION)
    mock_client.list_recipe_versions.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_list_recipe_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_recipe_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recipe_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list recipe versions"):
        list_recipe_versions("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_list_rulesets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rulesets.return_value = {}
    list_rulesets(region_name=REGION)
    mock_client.list_rulesets.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_list_rulesets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rulesets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rulesets",
    )
    with pytest.raises(RuntimeError, match="Failed to list rulesets"):
        list_rulesets(region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_list_schedules(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_schedules.return_value = {}
    list_schedules(region_name=REGION)
    mock_client.list_schedules.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_list_schedules_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_schedules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_schedules",
    )
    with pytest.raises(RuntimeError, match="Failed to list schedules"):
        list_schedules(region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_publish_recipe(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.publish_recipe.return_value = {}
    publish_recipe("test-name", region_name=REGION)
    mock_client.publish_recipe.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_publish_recipe_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.publish_recipe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_recipe",
    )
    with pytest.raises(RuntimeError, match="Failed to publish recipe"):
        publish_recipe("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_send_project_session_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_project_session_action.return_value = {}
    send_project_session_action("test-name", region_name=REGION)
    mock_client.send_project_session_action.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_send_project_session_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.send_project_session_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_project_session_action",
    )
    with pytest.raises(RuntimeError, match="Failed to send project session action"):
        send_project_session_action("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_start_project_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_project_session.return_value = {}
    start_project_session("test-name", region_name=REGION)
    mock_client.start_project_session.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_start_project_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_project_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_project_session",
    )
    with pytest.raises(RuntimeError, match="Failed to start project session"):
        start_project_session("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_stop_job_run(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_job_run.return_value = {}
    stop_job_run("test-name", "test-run_id", region_name=REGION)
    mock_client.stop_job_run.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_stop_job_run_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_job_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_job_run",
    )
    with pytest.raises(RuntimeError, match="Failed to stop job run"):
        stop_job_run("test-name", "test-run_id", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_dataset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dataset.return_value = {}
    update_dataset("test-name", {}, region_name=REGION)
    mock_client.update_dataset.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_dataset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dataset",
    )
    with pytest.raises(RuntimeError, match="Failed to update dataset"):
        update_dataset("test-name", {}, region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_profile_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_profile_job.return_value = {}
    update_profile_job("test-name", {}, "test-role_arn", region_name=REGION)
    mock_client.update_profile_job.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_profile_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_profile_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_profile_job",
    )
    with pytest.raises(RuntimeError, match="Failed to update profile job"):
        update_profile_job("test-name", {}, "test-role_arn", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project.return_value = {}
    update_project("test-role_arn", "test-name", region_name=REGION)
    mock_client.update_project.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_project",
    )
    with pytest.raises(RuntimeError, match="Failed to update project"):
        update_project("test-role_arn", "test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_recipe(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_recipe.return_value = {}
    update_recipe("test-name", region_name=REGION)
    mock_client.update_recipe.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_recipe_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_recipe.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_recipe",
    )
    with pytest.raises(RuntimeError, match="Failed to update recipe"):
        update_recipe("test-name", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_recipe_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_recipe_job.return_value = {}
    update_recipe_job("test-name", "test-role_arn", region_name=REGION)
    mock_client.update_recipe_job.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_recipe_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_recipe_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_recipe_job",
    )
    with pytest.raises(RuntimeError, match="Failed to update recipe job"):
        update_recipe_job("test-name", "test-role_arn", region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_ruleset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ruleset.return_value = {}
    update_ruleset("test-name", [], region_name=REGION)
    mock_client.update_ruleset.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_ruleset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ruleset",
    )
    with pytest.raises(RuntimeError, match="Failed to update ruleset"):
        update_ruleset("test-name", [], region_name=REGION)


@patch("aws_util.databrew.get_client")
def test_update_schedule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_schedule.return_value = {}
    update_schedule("test-cron_expression", "test-name", region_name=REGION)
    mock_client.update_schedule.assert_called_once()


@patch("aws_util.databrew.get_client")
def test_update_schedule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_schedule",
    )
    with pytest.raises(RuntimeError, match="Failed to update schedule"):
        update_schedule("test-cron_expression", "test-name", region_name=REGION)


def test_create_profile_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import create_profile_job
    mock_client = MagicMock()
    mock_client.create_profile_job.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    create_profile_job("test-dataset_name", "test-name", "test-output_location", "test-role_arn", encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, configuration={}, validation_configurations={}, tags=[{"Key": "k", "Value": "v"}], timeout=1, job_sample="test-job_sample", region_name="us-east-1")
    mock_client.create_profile_job.assert_called_once()

def test_create_ruleset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import create_ruleset
    mock_client = MagicMock()
    mock_client.create_ruleset.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    create_ruleset("test-name", "test-target_arn", "test-rules", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_ruleset.assert_called_once()

def test_create_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import create_schedule
    mock_client = MagicMock()
    mock_client.create_schedule.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    create_schedule("test-cron_expression", "test-name", job_names="test-job_names", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_schedule.assert_called_once()

def test_describe_recipe_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import describe_recipe
    mock_client = MagicMock()
    mock_client.describe_recipe.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    describe_recipe("test-name", recipe_version="test-recipe_version", region_name="us-east-1")
    mock_client.describe_recipe.assert_called_once()

def test_list_recipe_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import list_recipe_versions
    mock_client = MagicMock()
    mock_client.list_recipe_versions.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    list_recipe_versions("test-name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_recipe_versions.assert_called_once()

def test_list_rulesets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import list_rulesets
    mock_client = MagicMock()
    mock_client.list_rulesets.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    list_rulesets(target_arn="test-target_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_rulesets.assert_called_once()

def test_list_schedules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import list_schedules
    mock_client = MagicMock()
    mock_client.list_schedules.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    list_schedules(job_name="test-job_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_schedules.assert_called_once()

def test_publish_recipe_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import publish_recipe
    mock_client = MagicMock()
    mock_client.publish_recipe.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    publish_recipe("test-name", description="test-description", region_name="us-east-1")
    mock_client.publish_recipe.assert_called_once()

def test_send_project_session_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import send_project_session_action
    mock_client = MagicMock()
    mock_client.send_project_session_action.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    send_project_session_action("test-name", preview="test-preview", recipe_step="test-recipe_step", step_index="test-step_index", client_session_id="test-client_session_id", view_frame="test-view_frame", region_name="us-east-1")
    mock_client.send_project_session_action.assert_called_once()

def test_start_project_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import start_project_session
    mock_client = MagicMock()
    mock_client.start_project_session.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    start_project_session("test-name", assume_control="test-assume_control", region_name="us-east-1")
    mock_client.start_project_session.assert_called_once()

def test_update_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_dataset
    mock_client = MagicMock()
    mock_client.update_dataset.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_dataset("test-name", "test-input", format="test-format", format_options={}, path_options={}, region_name="us-east-1")
    mock_client.update_dataset.assert_called_once()

def test_update_profile_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_profile_job
    mock_client = MagicMock()
    mock_client.update_profile_job.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_profile_job("test-name", "test-output_location", "test-role_arn", configuration={}, encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, validation_configurations={}, timeout=1, job_sample="test-job_sample", region_name="us-east-1")
    mock_client.update_profile_job.assert_called_once()

def test_update_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_project
    mock_client = MagicMock()
    mock_client.update_project.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_project("test-role_arn", "test-name", sample="test-sample", region_name="us-east-1")
    mock_client.update_project.assert_called_once()

def test_update_recipe_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_recipe
    mock_client = MagicMock()
    mock_client.update_recipe.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_recipe("test-name", description="test-description", steps="test-steps", region_name="us-east-1")
    mock_client.update_recipe.assert_called_once()

def test_update_recipe_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_recipe_job
    mock_client = MagicMock()
    mock_client.update_recipe_job.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_recipe_job("test-name", "test-role_arn", encryption_key_arn="test-encryption_key_arn", encryption_mode="test-encryption_mode", log_subscription="test-log_subscription", max_capacity=1, max_retries=1, outputs="test-outputs", data_catalog_outputs="test-data_catalog_outputs", database_outputs="test-database_outputs", timeout=1, region_name="us-east-1")
    mock_client.update_recipe_job.assert_called_once()

def test_update_ruleset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_ruleset
    mock_client = MagicMock()
    mock_client.update_ruleset.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_ruleset("test-name", "test-rules", description="test-description", region_name="us-east-1")
    mock_client.update_ruleset.assert_called_once()

def test_update_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.databrew import update_schedule
    mock_client = MagicMock()
    mock_client.update_schedule.return_value = {}
    monkeypatch.setattr("aws_util.databrew.get_client", lambda *a, **kw: mock_client)
    update_schedule("test-cron_expression", "test-name", job_names="test-job_names", region_name="us-east-1")
    mock_client.update_schedule.assert_called_once()
