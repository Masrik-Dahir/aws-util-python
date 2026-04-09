"""Native async DataBrew utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.databrew import (
    BatchDeleteRecipeVersionResult,
    CreateProfileJobResult,
    CreateRulesetResult,
    CreateScheduleResult,
    DatasetResult,
    DeleteJobResult,
    DeleteRecipeVersionResult,
    DeleteRulesetResult,
    DeleteScheduleResult,
    DescribeJobRunResult,
    DescribeRecipeResult,
    DescribeRulesetResult,
    DescribeScheduleResult,
    JobResult,
    JobRunResult,
    ListRecipeVersionsResult,
    ListRulesetsResult,
    ListSchedulesResult,
    ListTagsForResourceResult,
    ProjectResult,
    PublishRecipeResult,
    RecipeResult,
    SendProjectSessionActionResult,
    StartProjectSessionResult,
    StopJobRunResult,
    UpdateDatasetResult,
    UpdateProfileJobResult,
    UpdateProjectResult,
    UpdateRecipeJobResult,
    UpdateRecipeResult,
    UpdateRulesetResult,
    UpdateScheduleResult,
    _parse_dataset,
    _parse_job,
    _parse_job_run,
    _parse_project,
    _parse_recipe,
)
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
# Dataset operations
# ---------------------------------------------------------------------------


async def create_dataset(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {"Name": name, "Input": input_config}
    if format_type is not None:
        kwargs["Format"] = format_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDataset", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_dataset failed for {name!r}") from exc
    return DatasetResult(name=resp.get("Name", name))


async def describe_dataset(
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
    client = async_client("databrew", region_name)
    try:
        resp = await client.call("DescribeDataset", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_dataset failed for {name!r}") from exc
    return _parse_dataset(resp)


async def list_datasets(
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
    client = async_client("databrew", region_name)
    datasets: list[DatasetResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListDatasets", **kwargs)
            for item in resp.get("Datasets", []):
                datasets.append(_parse_dataset(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_datasets failed") from exc
    return datasets


async def delete_dataset(
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
    client = async_client("databrew", region_name)
    try:
        await client.call("DeleteDataset", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_dataset failed for {name!r}") from exc
    return {"name": name}


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


async def create_project(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "DatasetName": dataset_name,
        "RecipeName": recipe_name,
        "RoleArn": role_arn,
    }
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateProject", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_project failed for {name!r}") from exc
    return ProjectResult(name=resp.get("Name", name))


async def describe_project(
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
    client = async_client("databrew", region_name)
    try:
        resp = await client.call("DescribeProject", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_project failed for {name!r}") from exc
    return _parse_project(resp)


async def list_projects(
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
    client = async_client("databrew", region_name)
    projects: list[ProjectResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListProjects", **kwargs)
            for item in resp.get("Projects", []):
                projects.append(_parse_project(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_projects failed") from exc
    return projects


async def delete_project(
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
    client = async_client("databrew", region_name)
    try:
        await client.call("DeleteProject", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_project failed for {name!r}") from exc
    return {"name": name}


# ---------------------------------------------------------------------------
# Recipe operations
# ---------------------------------------------------------------------------


async def create_recipe(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {"Name": name, "Steps": steps}
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateRecipe", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_recipe failed for {name!r}") from exc
    return RecipeResult(name=resp.get("Name", name))


async def list_recipes(
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
    client = async_client("databrew", region_name)
    recipes: list[RecipeResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListRecipes", **kwargs)
            for item in resp.get("Recipes", []):
                recipes.append(_parse_recipe(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_recipes failed") from exc
    return recipes


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


async def create_recipe_job(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("CreateRecipeJob", **kwargs)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_recipe_job failed for {name!r}") from exc
    return JobResult(name=resp.get("Name", name))


async def describe_job(
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
    client = async_client("databrew", region_name)
    try:
        resp = await client.call("DescribeJob", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_job failed for {name!r}") from exc
    return _parse_job(resp)


async def list_jobs(
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
    client = async_client("databrew", region_name)
    jobs: list[JobResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListJobs", **kwargs)
            for item in resp.get("Jobs", []):
                jobs.append(_parse_job(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return jobs


async def start_job_run(
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
    client = async_client("databrew", region_name)
    try:
        resp = await client.call("StartJobRun", Name=name)
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, f"start_job_run failed for {name!r}") from exc
    return resp.get("RunId", "")


async def list_job_runs(
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
    client = async_client("databrew", region_name)
    runs: list[JobRunResult] = []
    kwargs: dict[str, Any] = {"Name": name}
    try:
        while True:
            resp = await client.call("ListJobRuns", **kwargs)
            for item in resp.get("JobRuns", []):
                runs.append(_parse_job_run(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except RuntimeError:
        raise
    except Exception as exc:
        raise wrap_aws_error(exc, "list_job_runs failed") from exc
    return runs


async def batch_delete_recipe_version(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RecipeVersions"] = recipe_versions
    try:
        resp = await client.call("BatchDeleteRecipeVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete recipe version") from exc
    return BatchDeleteRecipeVersionResult(
        name=resp.get("Name"),
        errors=resp.get("Errors"),
    )


async def create_profile_job(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("CreateProfileJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create profile job") from exc
    return CreateProfileJobResult(
        name=resp.get("Name"),
    )


async def create_ruleset(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["TargetArn"] = target_arn
    kwargs["Rules"] = rules
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ruleset") from exc
    return CreateRulesetResult(
        name=resp.get("Name"),
    )


async def create_schedule(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CronExpression"] = cron_expression
    kwargs["Name"] = name
    if job_names is not None:
        kwargs["JobNames"] = job_names
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create schedule") from exc
    return CreateScheduleResult(
        name=resp.get("Name"),
    )


async def delete_job(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete job") from exc
    return DeleteJobResult(
        name=resp.get("Name"),
    )


async def delete_recipe_version(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RecipeVersion"] = recipe_version
    try:
        resp = await client.call("DeleteRecipeVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete recipe version") from exc
    return DeleteRecipeVersionResult(
        name=resp.get("Name"),
        recipe_version=resp.get("RecipeVersion"),
    )


async def delete_ruleset(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ruleset") from exc
    return DeleteRulesetResult(
        name=resp.get("Name"),
    )


async def delete_schedule(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete schedule") from exc
    return DeleteScheduleResult(
        name=resp.get("Name"),
    )


async def describe_job_run(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("DescribeJobRun", **kwargs)
    except Exception as exc:
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


async def describe_recipe(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if recipe_version is not None:
        kwargs["RecipeVersion"] = recipe_version
    try:
        resp = await client.call("DescribeRecipe", **kwargs)
    except Exception as exc:
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


async def describe_ruleset(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DescribeRuleset", **kwargs)
    except Exception as exc:
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


async def describe_schedule(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DescribeSchedule", **kwargs)
    except Exception as exc:
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


async def list_recipe_versions(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListRecipeVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recipe versions") from exc
    return ListRecipeVersionsResult(
        next_token=resp.get("NextToken"),
        recipes=resp.get("Recipes"),
    )


async def list_rulesets(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListRulesets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list rulesets") from exc
    return ListRulesetsResult(
        rulesets=resp.get("Rulesets"),
        next_token=resp.get("NextToken"),
    )


async def list_schedules(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    if job_name is not None:
        kwargs["JobName"] = job_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSchedules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list schedules") from exc
    return ListSchedulesResult(
        schedules=resp.get("Schedules"),
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def publish_recipe(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("PublishRecipe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to publish recipe") from exc
    return PublishRecipeResult(
        name=resp.get("Name"),
    )


async def send_project_session_action(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("SendProjectSessionAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send project session action") from exc
    return SendProjectSessionActionResult(
        result=resp.get("Result"),
        name=resp.get("Name"),
        action_id=resp.get("ActionId"),
    )


async def start_project_session(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if assume_control is not None:
        kwargs["AssumeControl"] = assume_control
    try:
        resp = await client.call("StartProjectSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start project session") from exc
    return StartProjectSessionResult(
        name=resp.get("Name"),
        client_session_id=resp.get("ClientSessionId"),
    )


async def stop_job_run(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("StopJobRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop job run") from exc
    return StopJobRunResult(
        run_id=resp.get("RunId"),
    )


async def tag_resource(
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
    client = async_client("databrew", region_name)
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_dataset(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("UpdateDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dataset") from exc
    return UpdateDatasetResult(
        name=resp.get("Name"),
    )


async def update_profile_job(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("UpdateProfileJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update profile job") from exc
    return UpdateProfileJobResult(
        name=resp.get("Name"),
    )


async def update_project(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleArn"] = role_arn
    kwargs["Name"] = name
    if sample is not None:
        kwargs["Sample"] = sample
    try:
        resp = await client.call("UpdateProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update project") from exc
    return UpdateProjectResult(
        last_modified_date=resp.get("LastModifiedDate"),
        name=resp.get("Name"),
    )


async def update_recipe(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if steps is not None:
        kwargs["Steps"] = steps
    try:
        resp = await client.call("UpdateRecipe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update recipe") from exc
    return UpdateRecipeResult(
        name=resp.get("Name"),
    )


async def update_recipe_job(
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
    client = async_client("databrew", region_name)
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
        resp = await client.call("UpdateRecipeJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update recipe job") from exc
    return UpdateRecipeJobResult(
        name=resp.get("Name"),
    )


async def update_ruleset(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Rules"] = rules
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ruleset") from exc
    return UpdateRulesetResult(
        name=resp.get("Name"),
    )


async def update_schedule(
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
    client = async_client("databrew", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CronExpression"] = cron_expression
    kwargs["Name"] = name
    if job_names is not None:
        kwargs["JobNames"] = job_names
    try:
        resp = await client.call("UpdateSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update schedule") from exc
    return UpdateScheduleResult(
        name=resp.get("Name"),
    )
