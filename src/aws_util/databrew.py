"""aws_util.databrew — AWS Glue DataBrew utilities.

Provides convenience wrappers around DataBrew dataset, project, recipe, and
job management operations with Pydantic-modelled results.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchDeleteRecipeVersionResult",
    "CreateProfileJobResult",
    "CreateRulesetResult",
    "CreateScheduleResult",
    "DatasetResult",
    "DeleteJobResult",
    "DeleteRecipeVersionResult",
    "DeleteRulesetResult",
    "DeleteScheduleResult",
    "DescribeJobRunResult",
    "DescribeRecipeResult",
    "DescribeRulesetResult",
    "DescribeScheduleResult",
    "JobResult",
    "JobRunResult",
    "ListRecipeVersionsResult",
    "ListRulesetsResult",
    "ListSchedulesResult",
    "ListTagsForResourceResult",
    "ProjectResult",
    "PublishRecipeResult",
    "RecipeResult",
    "SendProjectSessionActionResult",
    "StartProjectSessionResult",
    "StopJobRunResult",
    "UpdateDatasetResult",
    "UpdateProfileJobResult",
    "UpdateProjectResult",
    "UpdateRecipeJobResult",
    "UpdateRecipeResult",
    "UpdateRulesetResult",
    "UpdateScheduleResult",
    "batch_delete_recipe_version",
    "create_dataset",
    "create_profile_job",
    "create_project",
    "create_recipe",
    "create_recipe_job",
    "create_ruleset",
    "create_schedule",
    "delete_dataset",
    "delete_job",
    "delete_project",
    "delete_recipe_version",
    "delete_ruleset",
    "delete_schedule",
    "describe_dataset",
    "describe_job",
    "describe_job_run",
    "describe_project",
    "describe_recipe",
    "describe_ruleset",
    "describe_schedule",
    "list_datasets",
    "list_job_runs",
    "list_jobs",
    "list_projects",
    "list_recipe_versions",
    "list_recipes",
    "list_rulesets",
    "list_schedules",
    "list_tags_for_resource",
    "publish_recipe",
    "send_project_session_action",
    "start_job_run",
    "start_project_session",
    "stop_job_run",
    "tag_resource",
    "untag_resource",
    "update_dataset",
    "update_profile_job",
    "update_project",
    "update_recipe",
    "update_recipe_job",
    "update_ruleset",
    "update_schedule",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class DatasetResult(BaseModel):
    """Metadata for a DataBrew dataset."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    account_id: str | None = None
    created_by: str | None = None
    create_date: str | None = None
    format: str | None = None
    input: dict[str, Any] = {}
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class ProjectResult(BaseModel):
    """Metadata for a DataBrew project."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    account_id: str | None = None
    recipe_name: str | None = None
    dataset_name: str | None = None
    role_arn: str | None = None
    create_date: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class RecipeResult(BaseModel):
    """Metadata for a DataBrew recipe."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    recipe_version: str | None = None
    description: str | None = None
    steps: list[dict[str, Any]] = []
    create_date: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class JobResult(BaseModel):
    """Metadata for a DataBrew job."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    type: str | None = None
    dataset_name: str | None = None
    role_arn: str | None = None
    outputs: list[dict[str, Any]] = []
    create_date: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class JobRunResult(BaseModel):
    """Metadata for a DataBrew job run."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    run_id: str
    job_name: str = ""
    state: str = ""
    started_on: str | None = None
    completed_on: str | None = None
    error_message: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_DS_FIELDS = {
    "Name",
    "AccountId",
    "CreatedBy",
    "CreateDate",
    "Format",
    "Input",
    "Tags",
}
_PROJ_FIELDS = {
    "Name",
    "AccountId",
    "RecipeName",
    "DatasetName",
    "RoleArn",
    "CreateDate",
    "Tags",
}
_RECIPE_FIELDS = {
    "Name",
    "RecipeVersion",
    "Description",
    "Steps",
    "CreateDate",
    "Tags",
}
_JOB_FIELDS = {
    "Name",
    "Type",
    "DatasetName",
    "RoleArn",
    "Outputs",
    "CreateDate",
    "Tags",
}
_RUN_FIELDS = {
    "RunId",
    "JobName",
    "State",
    "StartedOn",
    "CompletedOn",
    "ErrorMessage",
}


def _parse_dataset(data: dict[str, Any]) -> DatasetResult:
    """Parse a raw DataBrew dataset dict."""
    created = data.get("CreateDate")
    return DatasetResult(
        name=data.get("Name", ""),
        account_id=data.get("AccountId"),
        created_by=data.get("CreatedBy"),
        create_date=str(created) if created is not None else None,
        format=data.get("Format"),
        input=data.get("Input", {}),
        tags=data.get("Tags", {}),
        extra={k: v for k, v in data.items() if k not in _DS_FIELDS},
    )


def _parse_project(data: dict[str, Any]) -> ProjectResult:
    """Parse a raw DataBrew project dict."""
    created = data.get("CreateDate")
    return ProjectResult(
        name=data.get("Name", ""),
        account_id=data.get("AccountId"),
        recipe_name=data.get("RecipeName"),
        dataset_name=data.get("DatasetName"),
        role_arn=data.get("RoleArn"),
        create_date=str(created) if created is not None else None,
        tags=data.get("Tags", {}),
        extra={k: v for k, v in data.items() if k not in _PROJ_FIELDS},
    )


def _parse_recipe(data: dict[str, Any]) -> RecipeResult:
    """Parse a raw DataBrew recipe dict."""
    created = data.get("CreateDate")
    return RecipeResult(
        name=data.get("Name", ""),
        recipe_version=data.get("RecipeVersion"),
        description=data.get("Description"),
        steps=data.get("Steps", []),
        create_date=str(created) if created is not None else None,
        tags=data.get("Tags", {}),
        extra={k: v for k, v in data.items() if k not in _RECIPE_FIELDS},
    )


def _parse_job(data: dict[str, Any]) -> JobResult:
    """Parse a raw DataBrew job dict."""
    created = data.get("CreateDate")
    return JobResult(
        name=data.get("Name", ""),
        type=data.get("Type"),
        dataset_name=data.get("DatasetName"),
        role_arn=data.get("RoleArn"),
        outputs=data.get("Outputs", []),
        create_date=str(created) if created is not None else None,
        tags=data.get("Tags", {}),
        extra={k: v for k, v in data.items() if k not in _JOB_FIELDS},
    )


def _parse_job_run(data: dict[str, Any]) -> JobRunResult:
    """Parse a raw DataBrew job run dict."""
    started = data.get("StartedOn")
    completed = data.get("CompletedOn")
    return JobRunResult(
        run_id=data.get("RunId", ""),
        job_name=data.get("JobName", ""),
        state=data.get("State", ""),
        started_on=str(started) if started is not None else None,
        completed_on=str(completed) if completed is not None else None,
        error_message=data.get("ErrorMessage"),
        extra={k: v for k, v in data.items() if k not in _RUN_FIELDS},
    )


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


def create_dataset(
    name: str,
    *,
    input_config: dict[str, Any],
    format_type: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DatasetResult:
    """Create a DataBrew dataset.

    Args:
        name: Name for the dataset.
        input_config: Input configuration dict.
        format_type: Optional format type (e.g. ``"CSV"``).
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {"Name": name, "Input": input_config}
    if format_type is not None:
        kwargs["Format"] = format_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_dataset failed for {name!r}") from exc
    return DatasetResult(name=resp.get("Name", name))


def describe_dataset(
    name: str,
    *,
    region_name: str | None = None,
) -> DatasetResult:
    """Describe a DataBrew dataset.

    Args:
        name: Name of the dataset.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        resp = client.describe_dataset(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_dataset failed for {name!r}") from exc
    return _parse_dataset(resp)


def list_datasets(
    *,
    region_name: str | None = None,
) -> list[DatasetResult]:
    """List all DataBrew datasets.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`DatasetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    datasets: list[DatasetResult] = []
    try:
        paginator = client.get_paginator("list_datasets")
        for page in paginator.paginate():
            for item in page.get("Datasets", []):
                datasets.append(_parse_dataset(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_datasets failed") from exc
    return datasets


def delete_dataset(
    name: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Delete a DataBrew dataset.

    Args:
        name: Name of the dataset.
        region_name: AWS region override.

    Returns:
        A dict with the dataset name.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        client.delete_dataset(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_dataset failed for {name!r}") from exc
    return {"name": name}


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


def create_project(
    name: str,
    *,
    dataset_name: str,
    recipe_name: str,
    role_arn: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ProjectResult:
    """Create a DataBrew project.

    Args:
        name: Name for the project.
        dataset_name: Name of the dataset.
        recipe_name: Name of the recipe.
        role_arn: IAM role ARN.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ProjectResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "DatasetName": dataset_name,
        "RecipeName": recipe_name,
        "RoleArn": role_arn,
    }
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_project failed for {name!r}") from exc
    return ProjectResult(name=resp.get("Name", name))


def describe_project(
    name: str,
    *,
    region_name: str | None = None,
) -> ProjectResult:
    """Describe a DataBrew project.

    Args:
        name: Name of the project.
        region_name: AWS region override.

    Returns:
        A :class:`ProjectResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        resp = client.describe_project(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_project failed for {name!r}") from exc
    return _parse_project(resp)


def list_projects(
    *,
    region_name: str | None = None,
) -> list[ProjectResult]:
    """List all DataBrew projects.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ProjectResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    projects: list[ProjectResult] = []
    try:
        paginator = client.get_paginator("list_projects")
        for page in paginator.paginate():
            for item in page.get("Projects", []):
                projects.append(_parse_project(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_projects failed") from exc
    return projects


def delete_project(
    name: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Delete a DataBrew project.

    Args:
        name: Name of the project.
        region_name: AWS region override.

    Returns:
        A dict with the project name.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        client.delete_project(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_project failed for {name!r}") from exc
    return {"name": name}


# ---------------------------------------------------------------------------
# Recipe operations
# ---------------------------------------------------------------------------


def create_recipe(
    name: str,
    *,
    steps: list[dict[str, Any]],
    description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> RecipeResult:
    """Create a DataBrew recipe.

    Args:
        name: Name for the recipe.
        steps: List of recipe step dicts.
        description: Optional description.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`RecipeResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {"Name": name, "Steps": steps}
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_recipe(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_recipe failed for {name!r}") from exc
    return RecipeResult(name=resp.get("Name", name))


def list_recipes(
    *,
    region_name: str | None = None,
) -> list[RecipeResult]:
    """List all DataBrew recipes.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`RecipeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    recipes: list[RecipeResult] = []
    try:
        paginator = client.get_paginator("list_recipes")
        for page in paginator.paginate():
            for item in page.get("Recipes", []):
                recipes.append(_parse_recipe(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_recipes failed") from exc
    return recipes


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


def create_recipe_job(
    name: str,
    *,
    role_arn: str,
    dataset_name: str | None = None,
    project_name: str | None = None,
    outputs: list[dict[str, Any]] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> JobResult:
    """Create a DataBrew recipe job.

    Args:
        name: Name for the job.
        role_arn: IAM role ARN.
        dataset_name: Optional dataset name.
        project_name: Optional project name.
        outputs: Optional list of output configurations.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`JobResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "RoleArn": role_arn,
        "Type": "RECIPE",
    }
    if dataset_name is not None:
        kwargs["DatasetName"] = dataset_name
    if project_name is not None:
        kwargs["ProjectName"] = project_name
    if outputs is not None:
        kwargs["Outputs"] = outputs
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_recipe_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_recipe_job failed for {name!r}") from exc
    return JobResult(name=resp.get("Name", name))


def describe_job(
    name: str,
    *,
    region_name: str | None = None,
) -> JobResult:
    """Describe a DataBrew job.

    Args:
        name: Name of the job.
        region_name: AWS region override.

    Returns:
        A :class:`JobResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        resp = client.describe_job(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_job failed for {name!r}") from exc
    return _parse_job(resp)


def list_jobs(
    *,
    region_name: str | None = None,
) -> list[JobResult]:
    """List all DataBrew jobs.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`JobResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    jobs: list[JobResult] = []
    try:
        paginator = client.get_paginator("list_jobs")
        for page in paginator.paginate():
            for item in page.get("Jobs", []):
                jobs.append(_parse_job(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return jobs


def start_job_run(
    name: str,
    *,
    region_name: str | None = None,
) -> str:
    """Start a DataBrew job run.

    Args:
        name: Name of the job to run.
        region_name: AWS region override.

    Returns:
        The run ID string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    try:
        resp = client.start_job_run(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_job_run failed for {name!r}") from exc
    return resp.get("RunId", "")


def list_job_runs(
    name: str,
    *,
    region_name: str | None = None,
) -> list[JobRunResult]:
    """List runs for a DataBrew job.

    Args:
        name: Name of the job.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobRunResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    runs: list[JobRunResult] = []
    try:
        paginator = client.get_paginator("list_job_runs")
        for page in paginator.paginate(Name=name):
            for item in page.get("JobRuns", []):
                runs.append(_parse_job_run(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_job_runs failed") from exc
    return runs


class BatchDeleteRecipeVersionResult(BaseModel):
    """Result of batch_delete_recipe_version."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    errors: list[dict[str, Any]] | None = None


class CreateProfileJobResult(BaseModel):
    """Result of create_profile_job."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class CreateRulesetResult(BaseModel):
    """Result of create_ruleset."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class CreateScheduleResult(BaseModel):
    """Result of create_schedule."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class DeleteJobResult(BaseModel):
    """Result of delete_job."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class DeleteRecipeVersionResult(BaseModel):
    """Result of delete_recipe_version."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    recipe_version: str | None = None


class DeleteRulesetResult(BaseModel):
    """Result of delete_ruleset."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class DeleteScheduleResult(BaseModel):
    """Result of delete_schedule."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class DescribeJobRunResult(BaseModel):
    """Result of describe_job_run."""

    model_config = ConfigDict(frozen=True)

    attempt: int | None = None
    completed_on: str | None = None
    dataset_name: str | None = None
    error_message: str | None = None
    execution_time: int | None = None
    job_name: str | None = None
    profile_configuration: dict[str, Any] | None = None
    validation_configurations: list[dict[str, Any]] | None = None
    run_id: str | None = None
    state: str | None = None
    log_subscription: str | None = None
    log_group_name: str | None = None
    outputs: list[dict[str, Any]] | None = None
    data_catalog_outputs: list[dict[str, Any]] | None = None
    database_outputs: list[dict[str, Any]] | None = None
    recipe_reference: dict[str, Any] | None = None
    started_by: str | None = None
    started_on: str | None = None
    job_sample: dict[str, Any] | None = None


class DescribeRecipeResult(BaseModel):
    """Result of describe_recipe."""

    model_config = ConfigDict(frozen=True)

    created_by: str | None = None
    create_date: str | None = None
    last_modified_by: str | None = None
    last_modified_date: str | None = None
    project_name: str | None = None
    published_by: str | None = None
    published_date: str | None = None
    description: str | None = None
    name: str | None = None
    steps: list[dict[str, Any]] | None = None
    tags: dict[str, Any] | None = None
    resource_arn: str | None = None
    recipe_version: str | None = None


class DescribeRulesetResult(BaseModel):
    """Result of describe_ruleset."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    target_arn: str | None = None
    rules: list[dict[str, Any]] | None = None
    create_date: str | None = None
    created_by: str | None = None
    last_modified_by: str | None = None
    last_modified_date: str | None = None
    resource_arn: str | None = None
    tags: dict[str, Any] | None = None


class DescribeScheduleResult(BaseModel):
    """Result of describe_schedule."""

    model_config = ConfigDict(frozen=True)

    create_date: str | None = None
    created_by: str | None = None
    job_names: list[str] | None = None
    last_modified_by: str | None = None
    last_modified_date: str | None = None
    resource_arn: str | None = None
    cron_expression: str | None = None
    tags: dict[str, Any] | None = None
    name: str | None = None


class ListRecipeVersionsResult(BaseModel):
    """Result of list_recipe_versions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    recipes: list[dict[str, Any]] | None = None


class ListRulesetsResult(BaseModel):
    """Result of list_rulesets."""

    model_config = ConfigDict(frozen=True)

    rulesets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSchedulesResult(BaseModel):
    """Result of list_schedules."""

    model_config = ConfigDict(frozen=True)

    schedules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class PublishRecipeResult(BaseModel):
    """Result of publish_recipe."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class SendProjectSessionActionResult(BaseModel):
    """Result of send_project_session_action."""

    model_config = ConfigDict(frozen=True)

    result: str | None = None
    name: str | None = None
    action_id: int | None = None


class StartProjectSessionResult(BaseModel):
    """Result of start_project_session."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    client_session_id: str | None = None


class StopJobRunResult(BaseModel):
    """Result of stop_job_run."""

    model_config = ConfigDict(frozen=True)

    run_id: str | None = None


class UpdateDatasetResult(BaseModel):
    """Result of update_dataset."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class UpdateProfileJobResult(BaseModel):
    """Result of update_profile_job."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class UpdateProjectResult(BaseModel):
    """Result of update_project."""

    model_config = ConfigDict(frozen=True)

    last_modified_date: str | None = None
    name: str | None = None


class UpdateRecipeResult(BaseModel):
    """Result of update_recipe."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class UpdateRecipeJobResult(BaseModel):
    """Result of update_recipe_job."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class UpdateRulesetResult(BaseModel):
    """Result of update_ruleset."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


class UpdateScheduleResult(BaseModel):
    """Result of update_schedule."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None


def batch_delete_recipe_version(
    name: str,
    recipe_versions: list[str],
    region_name: str | None = None,
) -> BatchDeleteRecipeVersionResult:
    """Batch delete recipe version.

    Args:
        name: Name.
        recipe_versions: Recipe versions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RecipeVersions"] = recipe_versions
    try:
        resp = client.batch_delete_recipe_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete recipe version") from exc
    return BatchDeleteRecipeVersionResult(
        name=resp.get("Name"),
        errors=resp.get("Errors"),
    )


def create_profile_job(
    dataset_name: str,
    name: str,
    output_location: dict[str, Any],
    role_arn: str,
    *,
    encryption_key_arn: str | None = None,
    encryption_mode: str | None = None,
    log_subscription: str | None = None,
    max_capacity: int | None = None,
    max_retries: int | None = None,
    configuration: dict[str, Any] | None = None,
    validation_configurations: list[dict[str, Any]] | None = None,
    tags: dict[str, Any] | None = None,
    timeout: int | None = None,
    job_sample: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateProfileJobResult:
    """Create profile job.

    Args:
        dataset_name: Dataset name.
        name: Name.
        output_location: Output location.
        role_arn: Role arn.
        encryption_key_arn: Encryption key arn.
        encryption_mode: Encryption mode.
        log_subscription: Log subscription.
        max_capacity: Max capacity.
        max_retries: Max retries.
        configuration: Configuration.
        validation_configurations: Validation configurations.
        tags: Tags.
        timeout: Timeout.
        job_sample: Job sample.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatasetName"] = dataset_name
    kwargs["Name"] = name
    kwargs["OutputLocation"] = output_location
    kwargs["RoleArn"] = role_arn
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    if encryption_mode is not None:
        kwargs["EncryptionMode"] = encryption_mode
    if log_subscription is not None:
        kwargs["LogSubscription"] = log_subscription
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if validation_configurations is not None:
        kwargs["ValidationConfigurations"] = validation_configurations
    if tags is not None:
        kwargs["Tags"] = tags
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if job_sample is not None:
        kwargs["JobSample"] = job_sample
    try:
        resp = client.create_profile_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create profile job") from exc
    return CreateProfileJobResult(
        name=resp.get("Name"),
    )


def create_ruleset(
    name: str,
    target_arn: str,
    rules: list[dict[str, Any]],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateRulesetResult:
    """Create ruleset.

    Args:
        name: Name.
        target_arn: Target arn.
        rules: Rules.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["TargetArn"] = target_arn
    kwargs["Rules"] = rules
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_ruleset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create ruleset") from exc
    return CreateRulesetResult(
        name=resp.get("Name"),
    )


def create_schedule(
    cron_expression: str,
    name: str,
    *,
    job_names: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateScheduleResult:
    """Create schedule.

    Args:
        cron_expression: Cron expression.
        name: Name.
        job_names: Job names.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CronExpression"] = cron_expression
    kwargs["Name"] = name
    if job_names is not None:
        kwargs["JobNames"] = job_names
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create schedule") from exc
    return CreateScheduleResult(
        name=resp.get("Name"),
    )


def delete_job(
    name: str,
    region_name: str | None = None,
) -> DeleteJobResult:
    """Delete job.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.delete_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete job") from exc
    return DeleteJobResult(
        name=resp.get("Name"),
    )


def delete_recipe_version(
    name: str,
    recipe_version: str,
    region_name: str | None = None,
) -> DeleteRecipeVersionResult:
    """Delete recipe version.

    Args:
        name: Name.
        recipe_version: Recipe version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RecipeVersion"] = recipe_version
    try:
        resp = client.delete_recipe_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete recipe version") from exc
    return DeleteRecipeVersionResult(
        name=resp.get("Name"),
        recipe_version=resp.get("RecipeVersion"),
    )


def delete_ruleset(
    name: str,
    region_name: str | None = None,
) -> DeleteRulesetResult:
    """Delete ruleset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.delete_ruleset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete ruleset") from exc
    return DeleteRulesetResult(
        name=resp.get("Name"),
    )


def delete_schedule(
    name: str,
    region_name: str | None = None,
) -> DeleteScheduleResult:
    """Delete schedule.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.delete_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete schedule") from exc
    return DeleteScheduleResult(
        name=resp.get("Name"),
    )


def describe_job_run(
    name: str,
    run_id: str,
    region_name: str | None = None,
) -> DescribeJobRunResult:
    """Describe job run.

    Args:
        name: Name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        resp = client.describe_job_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe job run") from exc
    return DescribeJobRunResult(
        attempt=resp.get("Attempt"),
        completed_on=resp.get("CompletedOn"),
        dataset_name=resp.get("DatasetName"),
        error_message=resp.get("ErrorMessage"),
        execution_time=resp.get("ExecutionTime"),
        job_name=resp.get("JobName"),
        profile_configuration=resp.get("ProfileConfiguration"),
        validation_configurations=resp.get("ValidationConfigurations"),
        run_id=resp.get("RunId"),
        state=resp.get("State"),
        log_subscription=resp.get("LogSubscription"),
        log_group_name=resp.get("LogGroupName"),
        outputs=resp.get("Outputs"),
        data_catalog_outputs=resp.get("DataCatalogOutputs"),
        database_outputs=resp.get("DatabaseOutputs"),
        recipe_reference=resp.get("RecipeReference"),
        started_by=resp.get("StartedBy"),
        started_on=resp.get("StartedOn"),
        job_sample=resp.get("JobSample"),
    )


def describe_recipe(
    name: str,
    *,
    recipe_version: str | None = None,
    region_name: str | None = None,
) -> DescribeRecipeResult:
    """Describe recipe.

    Args:
        name: Name.
        recipe_version: Recipe version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if recipe_version is not None:
        kwargs["RecipeVersion"] = recipe_version
    try:
        resp = client.describe_recipe(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe recipe") from exc
    return DescribeRecipeResult(
        created_by=resp.get("CreatedBy"),
        create_date=resp.get("CreateDate"),
        last_modified_by=resp.get("LastModifiedBy"),
        last_modified_date=resp.get("LastModifiedDate"),
        project_name=resp.get("ProjectName"),
        published_by=resp.get("PublishedBy"),
        published_date=resp.get("PublishedDate"),
        description=resp.get("Description"),
        name=resp.get("Name"),
        steps=resp.get("Steps"),
        tags=resp.get("Tags"),
        resource_arn=resp.get("ResourceArn"),
        recipe_version=resp.get("RecipeVersion"),
    )


def describe_ruleset(
    name: str,
    region_name: str | None = None,
) -> DescribeRulesetResult:
    """Describe ruleset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_ruleset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe ruleset") from exc
    return DescribeRulesetResult(
        name=resp.get("Name"),
        description=resp.get("Description"),
        target_arn=resp.get("TargetArn"),
        rules=resp.get("Rules"),
        create_date=resp.get("CreateDate"),
        created_by=resp.get("CreatedBy"),
        last_modified_by=resp.get("LastModifiedBy"),
        last_modified_date=resp.get("LastModifiedDate"),
        resource_arn=resp.get("ResourceArn"),
        tags=resp.get("Tags"),
    )


def describe_schedule(
    name: str,
    region_name: str | None = None,
) -> DescribeScheduleResult:
    """Describe schedule.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe schedule") from exc
    return DescribeScheduleResult(
        create_date=resp.get("CreateDate"),
        created_by=resp.get("CreatedBy"),
        job_names=resp.get("JobNames"),
        last_modified_by=resp.get("LastModifiedBy"),
        last_modified_date=resp.get("LastModifiedDate"),
        resource_arn=resp.get("ResourceArn"),
        cron_expression=resp.get("CronExpression"),
        tags=resp.get("Tags"),
        name=resp.get("Name"),
    )


def list_recipe_versions(
    name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRecipeVersionsResult:
    """List recipe versions.

    Args:
        name: Name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_recipe_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list recipe versions") from exc
    return ListRecipeVersionsResult(
        next_token=resp.get("NextToken"),
        recipes=resp.get("Recipes"),
    )


def list_rulesets(
    *,
    target_arn: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRulesetsResult:
    """List rulesets.

    Args:
        target_arn: Target arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_rulesets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rulesets") from exc
    return ListRulesetsResult(
        rulesets=resp.get("Rulesets"),
        next_token=resp.get("NextToken"),
    )


def list_schedules(
    *,
    job_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSchedulesResult:
    """List schedules.

    Args:
        job_name: Job name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    if job_name is not None:
        kwargs["JobName"] = job_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_schedules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list schedules") from exc
    return ListSchedulesResult(
        schedules=resp.get("Schedules"),
        next_token=resp.get("NextToken"),
    )


def list_tags_for_resource(
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
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def publish_recipe(
    name: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> PublishRecipeResult:
    """Publish recipe.

    Args:
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.publish_recipe(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish recipe") from exc
    return PublishRecipeResult(
        name=resp.get("Name"),
    )


def send_project_session_action(
    name: str,
    *,
    preview: bool | None = None,
    recipe_step: dict[str, Any] | None = None,
    step_index: int | None = None,
    client_session_id: str | None = None,
    view_frame: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SendProjectSessionActionResult:
    """Send project session action.

    Args:
        name: Name.
        preview: Preview.
        recipe_step: Recipe step.
        step_index: Step index.
        client_session_id: Client session id.
        view_frame: View frame.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if preview is not None:
        kwargs["Preview"] = preview
    if recipe_step is not None:
        kwargs["RecipeStep"] = recipe_step
    if step_index is not None:
        kwargs["StepIndex"] = step_index
    if client_session_id is not None:
        kwargs["ClientSessionId"] = client_session_id
    if view_frame is not None:
        kwargs["ViewFrame"] = view_frame
    try:
        resp = client.send_project_session_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send project session action") from exc
    return SendProjectSessionActionResult(
        result=resp.get("Result"),
        name=resp.get("Name"),
        action_id=resp.get("ActionId"),
    )


def start_project_session(
    name: str,
    *,
    assume_control: bool | None = None,
    region_name: str | None = None,
) -> StartProjectSessionResult:
    """Start project session.

    Args:
        name: Name.
        assume_control: Assume control.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if assume_control is not None:
        kwargs["AssumeControl"] = assume_control
    try:
        resp = client.start_project_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start project session") from exc
    return StartProjectSessionResult(
        name=resp.get("Name"),
        client_session_id=resp.get("ClientSessionId"),
    )


def stop_job_run(
    name: str,
    run_id: str,
    region_name: str | None = None,
) -> StopJobRunResult:
    """Stop job run.

    Args:
        name: Name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        resp = client.stop_job_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop job run") from exc
    return StopJobRunResult(
        run_id=resp.get("RunId"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
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
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
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
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_dataset(
    name: str,
    input: dict[str, Any],
    *,
    format: str | None = None,
    format_options: dict[str, Any] | None = None,
    path_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDatasetResult:
    """Update dataset.

    Args:
        name: Name.
        input: Input.
        format: Format.
        format_options: Format options.
        path_options: Path options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Input"] = input
    if format is not None:
        kwargs["Format"] = format
    if format_options is not None:
        kwargs["FormatOptions"] = format_options
    if path_options is not None:
        kwargs["PathOptions"] = path_options
    try:
        resp = client.update_dataset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update dataset") from exc
    return UpdateDatasetResult(
        name=resp.get("Name"),
    )


def update_profile_job(
    name: str,
    output_location: dict[str, Any],
    role_arn: str,
    *,
    configuration: dict[str, Any] | None = None,
    encryption_key_arn: str | None = None,
    encryption_mode: str | None = None,
    log_subscription: str | None = None,
    max_capacity: int | None = None,
    max_retries: int | None = None,
    validation_configurations: list[dict[str, Any]] | None = None,
    timeout: int | None = None,
    job_sample: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateProfileJobResult:
    """Update profile job.

    Args:
        name: Name.
        output_location: Output location.
        role_arn: Role arn.
        configuration: Configuration.
        encryption_key_arn: Encryption key arn.
        encryption_mode: Encryption mode.
        log_subscription: Log subscription.
        max_capacity: Max capacity.
        max_retries: Max retries.
        validation_configurations: Validation configurations.
        timeout: Timeout.
        job_sample: Job sample.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["OutputLocation"] = output_location
    kwargs["RoleArn"] = role_arn
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    if encryption_mode is not None:
        kwargs["EncryptionMode"] = encryption_mode
    if log_subscription is not None:
        kwargs["LogSubscription"] = log_subscription
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    if validation_configurations is not None:
        kwargs["ValidationConfigurations"] = validation_configurations
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if job_sample is not None:
        kwargs["JobSample"] = job_sample
    try:
        resp = client.update_profile_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update profile job") from exc
    return UpdateProfileJobResult(
        name=resp.get("Name"),
    )


def update_project(
    role_arn: str,
    name: str,
    *,
    sample: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateProjectResult:
    """Update project.

    Args:
        role_arn: Role arn.
        name: Name.
        sample: Sample.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleArn"] = role_arn
    kwargs["Name"] = name
    if sample is not None:
        kwargs["Sample"] = sample
    try:
        resp = client.update_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update project") from exc
    return UpdateProjectResult(
        last_modified_date=resp.get("LastModifiedDate"),
        name=resp.get("Name"),
    )


def update_recipe(
    name: str,
    *,
    description: str | None = None,
    steps: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateRecipeResult:
    """Update recipe.

    Args:
        name: Name.
        description: Description.
        steps: Steps.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if steps is not None:
        kwargs["Steps"] = steps
    try:
        resp = client.update_recipe(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update recipe") from exc
    return UpdateRecipeResult(
        name=resp.get("Name"),
    )


def update_recipe_job(
    name: str,
    role_arn: str,
    *,
    encryption_key_arn: str | None = None,
    encryption_mode: str | None = None,
    log_subscription: str | None = None,
    max_capacity: int | None = None,
    max_retries: int | None = None,
    outputs: list[dict[str, Any]] | None = None,
    data_catalog_outputs: list[dict[str, Any]] | None = None,
    database_outputs: list[dict[str, Any]] | None = None,
    timeout: int | None = None,
    region_name: str | None = None,
) -> UpdateRecipeJobResult:
    """Update recipe job.

    Args:
        name: Name.
        role_arn: Role arn.
        encryption_key_arn: Encryption key arn.
        encryption_mode: Encryption mode.
        log_subscription: Log subscription.
        max_capacity: Max capacity.
        max_retries: Max retries.
        outputs: Outputs.
        data_catalog_outputs: Data catalog outputs.
        database_outputs: Database outputs.
        timeout: Timeout.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RoleArn"] = role_arn
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    if encryption_mode is not None:
        kwargs["EncryptionMode"] = encryption_mode
    if log_subscription is not None:
        kwargs["LogSubscription"] = log_subscription
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    if outputs is not None:
        kwargs["Outputs"] = outputs
    if data_catalog_outputs is not None:
        kwargs["DataCatalogOutputs"] = data_catalog_outputs
    if database_outputs is not None:
        kwargs["DatabaseOutputs"] = database_outputs
    if timeout is not None:
        kwargs["Timeout"] = timeout
    try:
        resp = client.update_recipe_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update recipe job") from exc
    return UpdateRecipeJobResult(
        name=resp.get("Name"),
    )


def update_ruleset(
    name: str,
    rules: list[dict[str, Any]],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateRulesetResult:
    """Update ruleset.

    Args:
        name: Name.
        rules: Rules.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Rules"] = rules
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_ruleset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update ruleset") from exc
    return UpdateRulesetResult(
        name=resp.get("Name"),
    )


def update_schedule(
    cron_expression: str,
    name: str,
    *,
    job_names: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateScheduleResult:
    """Update schedule.

    Args:
        cron_expression: Cron expression.
        name: Name.
        job_names: Job names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CronExpression"] = cron_expression
    kwargs["Name"] = name
    if job_names is not None:
        kwargs["JobNames"] = job_names
    try:
        resp = client.update_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update schedule") from exc
    return UpdateScheduleResult(
        name=resp.get("Name"),
    )
