from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.glue import (
    GlueJob,
    GlueJobRun,
    _parse_run,
    get_job,
    get_job_run,
    list_job_runs,
    list_jobs,
    run_job_and_wait,
    start_job_run,
    stop_job_run,
    wait_for_job_run,
    batch_create_partition,
    batch_delete_connection,
    batch_delete_partition,
    batch_delete_table,
    batch_delete_table_version,
    batch_get_blueprints,
    batch_get_crawlers,
    batch_get_custom_entity_types,
    batch_get_data_quality_result,
    batch_get_dev_endpoints,
    batch_get_jobs,
    batch_get_partition,
    batch_get_table_optimizer,
    batch_get_triggers,
    batch_get_workflows,
    batch_put_data_quality_statistic_annotation,
    batch_stop_job_run,
    batch_update_partition,
    cancel_data_quality_rule_recommendation_run,
    cancel_data_quality_ruleset_evaluation_run,
    cancel_ml_task_run,
    cancel_statement,
    check_schema_version_validity,
    create_blueprint,
    create_catalog,
    create_classifier,
    create_column_statistics_task_settings,
    create_connection,
    create_crawler,
    create_custom_entity_type,
    create_data_quality_ruleset,
    create_database,
    create_dev_endpoint,
    create_glue_identity_center_configuration,
    create_integration,
    create_integration_resource_property,
    create_integration_table_properties,
    create_job,
    create_ml_transform,
    create_partition,
    create_partition_index,
    create_registry,
    create_schema,
    create_script,
    create_security_configuration,
    create_session,
    create_table,
    create_table_optimizer,
    create_trigger,
    create_usage_profile,
    create_user_defined_function,
    create_workflow,
    delete_blueprint,
    delete_catalog,
    delete_classifier,
    delete_column_statistics_for_partition,
    delete_column_statistics_for_table,
    delete_column_statistics_task_settings,
    delete_connection,
    delete_crawler,
    delete_custom_entity_type,
    delete_data_quality_ruleset,
    delete_database,
    delete_dev_endpoint,
    delete_glue_identity_center_configuration,
    delete_integration,
    delete_integration_table_properties,
    delete_job,
    delete_ml_transform,
    delete_partition,
    delete_partition_index,
    delete_registry,
    delete_resource_policy,
    delete_schema,
    delete_schema_versions,
    delete_security_configuration,
    delete_session,
    delete_table,
    delete_table_optimizer,
    delete_table_version,
    delete_trigger,
    delete_usage_profile,
    delete_user_defined_function,
    delete_workflow,
    describe_connection_type,
    describe_entity,
    describe_inbound_integrations,
    describe_integrations,
    get_blueprint,
    get_blueprint_run,
    get_blueprint_runs,
    get_catalog,
    get_catalog_import_status,
    get_catalogs,
    get_classifier,
    get_classifiers,
    get_column_statistics_for_partition,
    get_column_statistics_for_table,
    get_column_statistics_task_run,
    get_column_statistics_task_runs,
    get_column_statistics_task_settings,
    get_connection,
    get_connections,
    get_crawler,
    get_crawler_metrics,
    get_crawlers,
    get_custom_entity_type,
    get_data_catalog_encryption_settings,
    get_data_quality_model,
    get_data_quality_model_result,
    get_data_quality_result,
    get_data_quality_rule_recommendation_run,
    get_data_quality_ruleset,
    get_data_quality_ruleset_evaluation_run,
    get_database,
    get_databases,
    get_dataflow_graph,
    get_dev_endpoint,
    get_dev_endpoints,
    get_entity_records,
    get_glue_identity_center_configuration,
    get_integration_resource_property,
    get_integration_table_properties,
    get_job_bookmark,
    get_job_runs,
    get_jobs,
    get_mapping,
    get_ml_task_run,
    get_ml_task_runs,
    get_ml_transform,
    get_ml_transforms,
    get_partition,
    get_partition_indexes,
    get_partitions,
    get_plan,
    get_registry,
    get_resource_policies,
    get_resource_policy,
    get_schema,
    get_schema_by_definition,
    get_schema_version,
    get_schema_versions_diff,
    get_security_configuration,
    get_security_configurations,
    get_session,
    get_statement,
    get_table,
    get_table_optimizer,
    get_table_version,
    get_table_versions,
    get_tables,
    get_tags,
    get_trigger,
    get_triggers,
    get_unfiltered_partition_metadata,
    get_unfiltered_partitions_metadata,
    get_unfiltered_table_metadata,
    get_usage_profile,
    get_user_defined_function,
    get_user_defined_functions,
    get_workflow,
    get_workflow_run,
    get_workflow_run_properties,
    get_workflow_runs,
    import_catalog_to_glue,
    list_blueprints,
    list_column_statistics_task_runs,
    list_connection_types,
    list_crawlers,
    list_crawls,
    list_custom_entity_types,
    list_data_quality_results,
    list_data_quality_rule_recommendation_runs,
    list_data_quality_ruleset_evaluation_runs,
    list_data_quality_rulesets,
    list_data_quality_statistic_annotations,
    list_data_quality_statistics,
    list_dev_endpoints,
    list_entities,
    list_ml_transforms,
    list_registries,
    list_schema_versions,
    list_schemas,
    list_sessions,
    list_statements,
    list_table_optimizer_runs,
    list_triggers,
    list_usage_profiles,
    list_workflows,
    modify_integration,
    put_data_catalog_encryption_settings,
    put_data_quality_profile_annotation,
    put_resource_policy,
    put_schema_version_metadata,
    put_workflow_run_properties,
    query_schema_version_metadata,
    register_schema_version,
    remove_schema_version_metadata,
    reset_job_bookmark,
    resume_workflow_run,
    run_connection,
    run_statement,
    search_tables,
    start_blueprint_run,
    start_column_statistics_task_run,
    start_column_statistics_task_run_schedule,
    start_crawler,
    start_crawler_schedule,
    start_data_quality_rule_recommendation_run,
    start_data_quality_ruleset_evaluation_run,
    start_export_labels_task_run,
    start_import_labels_task_run,
    start_ml_evaluation_task_run,
    start_ml_labeling_set_generation_task_run,
    start_trigger,
    start_workflow_run,
    stop_column_statistics_task_run,
    stop_column_statistics_task_run_schedule,
    stop_crawler,
    stop_crawler_schedule,
    stop_session,
    stop_trigger,
    stop_workflow_run,
    tag_resource,
    untag_resource,
    update_blueprint,
    update_catalog,
    update_classifier,
    update_column_statistics_for_partition,
    update_column_statistics_for_table,
    update_column_statistics_task_settings,
    update_connection,
    update_crawler,
    update_crawler_schedule,
    update_data_quality_ruleset,
    update_database,
    update_dev_endpoint,
    update_glue_identity_center_configuration,
    update_integration_resource_property,
    update_integration_table_properties,
    update_job,
    update_job_from_source_control,
    update_ml_transform,
    update_partition,
    update_registry,
    update_schema,
    update_source_control_from_job,
    update_table,
    update_table_optimizer,
    update_trigger,
    update_usage_profile,
    update_user_defined_function,
    update_workflow,
)


# ---------------------------------------------------------------------------
# _parse_run helper
# ---------------------------------------------------------------------------


def test_parse_run_full() -> None:
    raw = {
        "Id": "jr-1",
        "JobName": "my-job",
        "JobRunState": "SUCCEEDED",
        "StartedOn": "2024-01-01T00:00:00Z",
        "CompletedOn": "2024-01-01T01:00:00Z",
        "ExecutionTime": 3600,
        "ErrorMessage": None,
        "Arguments": {"--key": "val"},
    }
    run = _parse_run(raw)
    assert run.job_run_id == "jr-1"
    assert run.job_name == "my-job"
    assert run.job_run_state == "SUCCEEDED"
    assert run.arguments == {"--key": "val"}


def test_parse_run_minimal() -> None:
    raw = {"Id": "jr-2", "JobName": "j", "JobRunState": "RUNNING"}
    run = _parse_run(raw)
    assert run.started_on is None
    assert run.completed_on is None
    assert run.execution_time is None
    assert run.error_message is None
    assert run.arguments == {}


# ---------------------------------------------------------------------------
# start_job_run
# ---------------------------------------------------------------------------


async def test_start_job_run_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"JobRunId": "jr-1"}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await start_job_run("my-job")
    assert result == "jr-1"


async def test_start_job_run_with_opts(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"JobRunId": "jr-2"}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await start_job_run(
        "my-job",
        arguments={"--key": "val"},
        worker_type="G.1X",
        number_of_workers=5,
        region_name="eu-west-1",
    )
    assert result == "jr-2"


async def test_start_job_run_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="Failed to start Glue job"):
        await start_job_run("my-job")


# ---------------------------------------------------------------------------
# get_job_run
# ---------------------------------------------------------------------------


async def test_get_job_run_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobRun": {
            "Id": "jr-1",
            "JobName": "my-job",
            "JobRunState": "SUCCEEDED",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await get_job_run("my-job", "jr-1")
    assert isinstance(result, GlueJobRun)
    assert result.job_run_id == "jr-1"


async def test_get_job_run_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="get_job_run failed"):
        await get_job_run("my-job", "jr-1")


# ---------------------------------------------------------------------------
# get_job
# ---------------------------------------------------------------------------


async def test_get_job_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Job": {
            "Name": "my-job",
            "Description": "desc",
            "Role": "arn:role",
            "GlueVersion": "3.0",
            "WorkerType": "G.1X",
            "NumberOfWorkers": 10,
            "MaxRetries": 2,
            "Timeout": 120,
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await get_job("my-job")
    assert isinstance(result, GlueJob)
    assert result.job_name == "my-job"
    assert result.description == "desc"
    assert result.max_retries == 2
    assert result.timeout == 120


async def test_get_job_minimal(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Job": {"Name": "j"}}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await get_job("j")
    assert result.description is None
    assert result.max_retries == 0


async def test_get_job_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="get_job failed"):
        await get_job("my-job")


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------


async def test_list_jobs_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [{"Name": "j1"}, {"Name": "j2"}]
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await list_jobs()
    assert result == ["j1", "j2"]


async def test_list_jobs_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="list_jobs failed"):
        await list_jobs()


# ---------------------------------------------------------------------------
# list_job_runs
# ---------------------------------------------------------------------------


async def test_list_job_runs_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [
        {"Id": "jr-1", "JobName": "my-job", "JobRunState": "SUCCEEDED"},
        {"Id": "jr-2", "JobName": "my-job", "JobRunState": "FAILED"},
    ]
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    result = await list_job_runs("my-job")
    assert len(result) == 2
    assert result[0].job_run_id == "jr-1"


async def test_list_job_runs_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="list_job_runs failed"):
        await list_job_runs("my-job")


# ---------------------------------------------------------------------------
# wait_for_job_run
# ---------------------------------------------------------------------------


async def test_wait_for_job_run_immediate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobRun": {
            "Id": "jr-1",
            "JobName": "my-job",
            "JobRunState": "SUCCEEDED",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.glue.asyncio.sleep", AsyncMock())
    result = await wait_for_job_run("my-job", "jr-1")
    assert result.finished is True


async def test_wait_for_job_run_polls_then_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"JobRun": {"Id": "jr-1", "JobName": "my-job", "JobRunState": "RUNNING"}},
        {"JobRun": {"Id": "jr-1", "JobName": "my-job", "JobRunState": "SUCCEEDED"}},
    ]
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.glue.asyncio.sleep", AsyncMock())
    result = await wait_for_job_run("my-job", "jr-1")
    assert result.succeeded is True


async def test_wait_for_job_run_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "JobRun": {
            "Id": "jr-1",
            "JobName": "my-job",
            "JobRunState": "RUNNING",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.glue.asyncio.sleep", AsyncMock())

    # Make time.monotonic return values that exceed the deadline
    call_count = 0
    original_monotonic = time.monotonic

    def fake_monotonic() -> float:
        nonlocal call_count
        call_count += 1
        if call_count <= 1:
            return 0.0  # initial deadline calculation
        return 100.0  # past deadline

    monkeypatch.setattr("aws_util.aio.glue.time.monotonic", fake_monotonic)
    with pytest.raises(TimeoutError, match="did not finish"):
        await wait_for_job_run("my-job", "jr-1", timeout=1.0)


# ---------------------------------------------------------------------------
# run_job_and_wait
# ---------------------------------------------------------------------------


async def test_run_job_and_wait_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"JobRunId": "jr-1"},  # start_job_run
        {  # get_job_run (wait_for_job_run)
            "JobRun": {
                "Id": "jr-1",
                "JobName": "my-job",
                "JobRunState": "SUCCEEDED",
            }
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.glue.asyncio.sleep", AsyncMock())
    result = await run_job_and_wait(
        "my-job",
        arguments={"--key": "val"},
        worker_type="G.2X",
        number_of_workers=10,
    )
    assert result.succeeded is True


# ---------------------------------------------------------------------------
# stop_job_run
# ---------------------------------------------------------------------------


async def test_stop_job_run_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    await stop_job_run("my-job", "jr-1")


async def test_stop_job_run_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="stop_job_run failed"):
        await stop_job_run("my-job", "jr-1")


async def test_batch_create_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_create_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_create_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_create_partition("test-database_name", "test-table_name", [], )


async def test_batch_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_connection([], )
    mock_client.call.assert_called_once()


async def test_batch_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_connection([], )


async def test_batch_delete_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_partition("test-database_name", "test-table_name", [], )


async def test_batch_delete_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_table("test-database_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_table("test-database_name", [], )


async def test_batch_delete_table_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_table_version("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_delete_table_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_table_version("test-database_name", "test-table_name", [], )


async def test_batch_get_blueprints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_blueprints([], )
    mock_client.call.assert_called_once()


async def test_batch_get_blueprints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_blueprints([], )


async def test_batch_get_crawlers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_crawlers([], )
    mock_client.call.assert_called_once()


async def test_batch_get_crawlers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_crawlers([], )


async def test_batch_get_custom_entity_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_custom_entity_types([], )
    mock_client.call.assert_called_once()


async def test_batch_get_custom_entity_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_custom_entity_types([], )


async def test_batch_get_data_quality_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_data_quality_result([], )
    mock_client.call.assert_called_once()


async def test_batch_get_data_quality_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_data_quality_result([], )


async def test_batch_get_dev_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_dev_endpoints([], )
    mock_client.call.assert_called_once()


async def test_batch_get_dev_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_dev_endpoints([], )


async def test_batch_get_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_jobs([], )
    mock_client.call.assert_called_once()


async def test_batch_get_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_jobs([], )


async def test_batch_get_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_partition("test-database_name", "test-table_name", [], )


async def test_batch_get_table_optimizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_table_optimizer([], )
    mock_client.call.assert_called_once()


async def test_batch_get_table_optimizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_table_optimizer([], )


async def test_batch_get_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_triggers([], )
    mock_client.call.assert_called_once()


async def test_batch_get_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_triggers([], )


async def test_batch_get_workflows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_workflows([], )
    mock_client.call.assert_called_once()


async def test_batch_get_workflows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_workflows([], )


async def test_batch_put_data_quality_statistic_annotation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_put_data_quality_statistic_annotation([], )
    mock_client.call.assert_called_once()


async def test_batch_put_data_quality_statistic_annotation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_put_data_quality_statistic_annotation([], )


async def test_batch_stop_job_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_stop_job_run("test-job_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_stop_job_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_stop_job_run("test-job_name", [], )


async def test_batch_update_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_update_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_partition("test-database_name", "test-table_name", [], )


async def test_cancel_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_data_quality_rule_recommendation_run("test-run_id", )
    mock_client.call.assert_called_once()


async def test_cancel_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_data_quality_rule_recommendation_run("test-run_id", )


async def test_cancel_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_data_quality_ruleset_evaluation_run("test-run_id", )
    mock_client.call.assert_called_once()


async def test_cancel_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_data_quality_ruleset_evaluation_run("test-run_id", )


async def test_cancel_ml_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_ml_task_run("test-transform_id", "test-task_run_id", )
    mock_client.call.assert_called_once()


async def test_cancel_ml_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_ml_task_run("test-transform_id", "test-task_run_id", )


async def test_cancel_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_statement("test-session_id", 1, )
    mock_client.call.assert_called_once()


async def test_cancel_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_statement("test-session_id", 1, )


async def test_check_schema_version_validity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await check_schema_version_validity("test-data_format", "test-schema_definition", )
    mock_client.call.assert_called_once()


async def test_check_schema_version_validity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await check_schema_version_validity("test-data_format", "test-schema_definition", )


async def test_create_blueprint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_blueprint("test-name", "test-blueprint_location", )
    mock_client.call.assert_called_once()


async def test_create_blueprint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_blueprint("test-name", "test-blueprint_location", )


async def test_create_catalog(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_catalog("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_catalog_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_catalog("test-name", {}, )


async def test_create_classifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_classifier()
    mock_client.call.assert_called_once()


async def test_create_classifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_classifier()


async def test_create_column_statistics_task_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", )
    mock_client.call.assert_called_once()


async def test_create_column_statistics_task_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", )


async def test_create_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_connection({}, )
    mock_client.call.assert_called_once()


async def test_create_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_connection({}, )


async def test_create_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_crawler("test-name", "test-role", {}, )
    mock_client.call.assert_called_once()


async def test_create_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_crawler("test-name", "test-role", {}, )


async def test_create_custom_entity_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_entity_type("test-name", "test-regex_string", )
    mock_client.call.assert_called_once()


async def test_create_custom_entity_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_entity_type("test-name", "test-regex_string", )


async def test_create_data_quality_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_data_quality_ruleset("test-name", "test-ruleset", )
    mock_client.call.assert_called_once()


async def test_create_data_quality_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_quality_ruleset("test-name", "test-ruleset", )


async def test_create_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_database({}, )
    mock_client.call.assert_called_once()


async def test_create_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_database({}, )


async def test_create_dev_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dev_endpoint("test-endpoint_name", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_dev_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dev_endpoint("test-endpoint_name", "test-role_arn", )


async def test_create_glue_identity_center_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_glue_identity_center_configuration("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_create_glue_identity_center_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_glue_identity_center_configuration("test-instance_arn", )


async def test_create_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration("test-integration_name", "test-source_arn", "test-target_arn", )
    mock_client.call.assert_called_once()


async def test_create_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration("test-integration_name", "test-source_arn", "test-target_arn", )


async def test_create_integration_resource_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration_resource_property("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_create_integration_resource_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration_resource_property("test-resource_arn", )


async def test_create_integration_table_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration_table_properties("test-resource_arn", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_create_integration_table_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration_table_properties("test-resource_arn", "test-table_name", )


async def test_create_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_job("test-name", "test-role", {}, )
    mock_client.call.assert_called_once()


async def test_create_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_job("test-name", "test-role", {}, )


async def test_create_ml_transform(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ml_transform("test-name", [], {}, "test-role", )
    mock_client.call.assert_called_once()


async def test_create_ml_transform_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ml_transform("test-name", [], {}, "test-role", )


async def test_create_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_partition("test-database_name", "test-table_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_partition("test-database_name", "test-table_name", {}, )


async def test_create_partition_index(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_partition_index("test-database_name", "test-table_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_partition_index_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_partition_index("test-database_name", "test-table_name", {}, )


async def test_create_registry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_registry("test-registry_name", )
    mock_client.call.assert_called_once()


async def test_create_registry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_registry("test-registry_name", )


async def test_create_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_schema("test-schema_name", "test-data_format", )
    mock_client.call.assert_called_once()


async def test_create_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_schema("test-schema_name", "test-data_format", )


async def test_create_script(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_script()
    mock_client.call.assert_called_once()


async def test_create_script_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_script()


async def test_create_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_security_configuration("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_security_configuration("test-name", {}, )


async def test_create_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_session("test-id", "test-role", {}, )
    mock_client.call.assert_called_once()


async def test_create_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_session("test-id", "test-role", {}, )


async def test_create_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_table("test-database_name", )
    mock_client.call.assert_called_once()


async def test_create_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_table("test-database_name", )


async def test_create_table_optimizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, )
    mock_client.call.assert_called_once()


async def test_create_table_optimizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, )


async def test_create_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_trigger("test-name", "test-type_value", [], )
    mock_client.call.assert_called_once()


async def test_create_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_trigger("test-name", "test-type_value", [], )


async def test_create_usage_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_usage_profile("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_usage_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_usage_profile("test-name", {}, )


async def test_create_user_defined_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user_defined_function("test-database_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_user_defined_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_defined_function("test-database_name", {}, )


async def test_create_workflow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_workflow("test-name", )
    mock_client.call.assert_called_once()


async def test_create_workflow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_workflow("test-name", )


async def test_delete_blueprint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_blueprint("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_blueprint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_blueprint("test-name", )


async def test_delete_catalog(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_catalog("test-catalog_id", )
    mock_client.call.assert_called_once()


async def test_delete_catalog_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_catalog("test-catalog_id", )


async def test_delete_classifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_classifier("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_classifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_classifier("test-name", )


async def test_delete_column_statistics_for_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_column_statistics_for_partition("test-database_name", "test-table_name", [], "test-column_name", )
    mock_client.call.assert_called_once()


async def test_delete_column_statistics_for_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_column_statistics_for_partition("test-database_name", "test-table_name", [], "test-column_name", )


async def test_delete_column_statistics_for_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", )
    mock_client.call.assert_called_once()


async def test_delete_column_statistics_for_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", )


async def test_delete_column_statistics_task_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_column_statistics_task_settings("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_delete_column_statistics_task_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_column_statistics_task_settings("test-database_name", "test-table_name", )


async def test_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connection("test-connection_name", )
    mock_client.call.assert_called_once()


async def test_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection("test-connection_name", )


async def test_delete_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_crawler("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_crawler("test-name", )


async def test_delete_custom_entity_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_entity_type("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_entity_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_entity_type("test-name", )


async def test_delete_data_quality_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_quality_ruleset("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_data_quality_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_quality_ruleset("test-name", )


async def test_delete_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_database("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_database("test-name", )


async def test_delete_dev_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dev_endpoint("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_delete_dev_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dev_endpoint("test-endpoint_name", )


async def test_delete_glue_identity_center_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_glue_identity_center_configuration()
    mock_client.call.assert_called_once()


async def test_delete_glue_identity_center_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_glue_identity_center_configuration()


async def test_delete_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_integration("test-integration_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_integration("test-integration_identifier", )


async def test_delete_integration_table_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_integration_table_properties("test-resource_arn", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_delete_integration_table_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_integration_table_properties("test-resource_arn", "test-table_name", )


async def test_delete_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job("test-job_name", )
    mock_client.call.assert_called_once()


async def test_delete_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job("test-job_name", )


async def test_delete_ml_transform(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ml_transform("test-transform_id", )
    mock_client.call.assert_called_once()


async def test_delete_ml_transform_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ml_transform("test-transform_id", )


async def test_delete_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_delete_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_partition("test-database_name", "test-table_name", [], )


async def test_delete_partition_index(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_partition_index("test-database_name", "test-table_name", "test-index_name", )
    mock_client.call.assert_called_once()


async def test_delete_partition_index_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_partition_index("test-database_name", "test-table_name", "test-index_name", )


async def test_delete_registry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_registry({}, )
    mock_client.call.assert_called_once()


async def test_delete_registry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_registry({}, )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy()
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy()


async def test_delete_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_schema({}, )
    mock_client.call.assert_called_once()


async def test_delete_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_schema({}, )


async def test_delete_schema_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_schema_versions({}, "test-versions", )
    mock_client.call.assert_called_once()


async def test_delete_schema_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_schema_versions({}, "test-versions", )


async def test_delete_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_security_configuration("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_security_configuration("test-name", )


async def test_delete_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_session("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_session("test-id", )


async def test_delete_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_table("test-database_name", "test-name", )
    mock_client.call.assert_called_once()


async def test_delete_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_table("test-database_name", "test-name", )


async def test_delete_table_optimizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_delete_table_optimizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )


async def test_delete_table_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_table_version("test-database_name", "test-table_name", "test-version_id", )
    mock_client.call.assert_called_once()


async def test_delete_table_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_table_version("test-database_name", "test-table_name", "test-version_id", )


async def test_delete_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_trigger("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_trigger("test-name", )


async def test_delete_usage_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_usage_profile("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_usage_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_usage_profile("test-name", )


async def test_delete_user_defined_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_defined_function("test-database_name", "test-function_name", )
    mock_client.call.assert_called_once()


async def test_delete_user_defined_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_defined_function("test-database_name", "test-function_name", )


async def test_delete_workflow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_workflow("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_workflow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_workflow("test-name", )


async def test_describe_connection_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_connection_type("test-connection_type", )
    mock_client.call.assert_called_once()


async def test_describe_connection_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_connection_type("test-connection_type", )


async def test_describe_entity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_entity("test-connection_name", "test-entity_name", )
    mock_client.call.assert_called_once()


async def test_describe_entity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_entity("test-connection_name", "test-entity_name", )


async def test_describe_inbound_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_inbound_integrations()
    mock_client.call.assert_called_once()


async def test_describe_inbound_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_inbound_integrations()


async def test_describe_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_integrations()
    mock_client.call.assert_called_once()


async def test_describe_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_integrations()


async def test_get_blueprint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_blueprint("test-name", )
    mock_client.call.assert_called_once()


async def test_get_blueprint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_blueprint("test-name", )


async def test_get_blueprint_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_blueprint_run("test-blueprint_name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_get_blueprint_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_blueprint_run("test-blueprint_name", "test-run_id", )


async def test_get_blueprint_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_blueprint_runs("test-blueprint_name", )
    mock_client.call.assert_called_once()


async def test_get_blueprint_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_blueprint_runs("test-blueprint_name", )


async def test_get_catalog(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_catalog("test-catalog_id", )
    mock_client.call.assert_called_once()


async def test_get_catalog_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_catalog("test-catalog_id", )


async def test_get_catalog_import_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_catalog_import_status()
    mock_client.call.assert_called_once()


async def test_get_catalog_import_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_catalog_import_status()


async def test_get_catalogs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_catalogs()
    mock_client.call.assert_called_once()


async def test_get_catalogs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_catalogs()


async def test_get_classifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_classifier("test-name", )
    mock_client.call.assert_called_once()


async def test_get_classifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_classifier("test-name", )


async def test_get_classifiers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_classifiers()
    mock_client.call.assert_called_once()


async def test_get_classifiers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_classifiers()


async def test_get_column_statistics_for_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_column_statistics_for_partition("test-database_name", "test-table_name", [], [], )
    mock_client.call.assert_called_once()


async def test_get_column_statistics_for_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_column_statistics_for_partition("test-database_name", "test-table_name", [], [], )


async def test_get_column_statistics_for_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_column_statistics_for_table("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_get_column_statistics_for_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_column_statistics_for_table("test-database_name", "test-table_name", [], )


async def test_get_column_statistics_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_column_statistics_task_run("test-column_statistics_task_run_id", )
    mock_client.call.assert_called_once()


async def test_get_column_statistics_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_column_statistics_task_run("test-column_statistics_task_run_id", )


async def test_get_column_statistics_task_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_column_statistics_task_runs("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_column_statistics_task_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_column_statistics_task_runs("test-database_name", "test-table_name", )


async def test_get_column_statistics_task_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_column_statistics_task_settings("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_column_statistics_task_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_column_statistics_task_settings("test-database_name", "test-table_name", )


async def test_get_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_connection("test-name", )
    mock_client.call.assert_called_once()


async def test_get_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_connection("test-name", )


async def test_get_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_connections()
    mock_client.call.assert_called_once()


async def test_get_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_connections()


async def test_get_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_crawler("test-name", )
    mock_client.call.assert_called_once()


async def test_get_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_crawler("test-name", )


async def test_get_crawler_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_crawler_metrics()
    mock_client.call.assert_called_once()


async def test_get_crawler_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_crawler_metrics()


async def test_get_crawlers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_crawlers()
    mock_client.call.assert_called_once()


async def test_get_crawlers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_crawlers()


async def test_get_custom_entity_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_custom_entity_type("test-name", )
    mock_client.call.assert_called_once()


async def test_get_custom_entity_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_entity_type("test-name", )


async def test_get_data_catalog_encryption_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_catalog_encryption_settings()
    mock_client.call.assert_called_once()


async def test_get_data_catalog_encryption_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_catalog_encryption_settings()


async def test_get_data_quality_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_model("test-profile_id", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_model("test-profile_id", )


async def test_get_data_quality_model_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_model_result("test-statistic_id", "test-profile_id", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_model_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_model_result("test-statistic_id", "test-profile_id", )


async def test_get_data_quality_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_result("test-result_id", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_result("test-result_id", )


async def test_get_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_rule_recommendation_run("test-run_id", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_rule_recommendation_run("test-run_id", )


async def test_get_data_quality_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_ruleset("test-name", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_ruleset("test-name", )


async def test_get_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_data_quality_ruleset_evaluation_run("test-run_id", )
    mock_client.call.assert_called_once()


async def test_get_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_quality_ruleset_evaluation_run("test-run_id", )


async def test_get_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_database("test-name", )
    mock_client.call.assert_called_once()


async def test_get_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_database("test-name", )


async def test_get_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_databases()
    mock_client.call.assert_called_once()


async def test_get_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_databases()


async def test_get_dataflow_graph(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dataflow_graph()
    mock_client.call.assert_called_once()


async def test_get_dataflow_graph_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dataflow_graph()


async def test_get_dev_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dev_endpoint("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_get_dev_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dev_endpoint("test-endpoint_name", )


async def test_get_dev_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dev_endpoints()
    mock_client.call.assert_called_once()


async def test_get_dev_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dev_endpoints()


async def test_get_entity_records(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_entity_records("test-entity_name", 1, )
    mock_client.call.assert_called_once()


async def test_get_entity_records_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_entity_records("test-entity_name", 1, )


async def test_get_glue_identity_center_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_glue_identity_center_configuration()
    mock_client.call.assert_called_once()


async def test_get_glue_identity_center_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_glue_identity_center_configuration()


async def test_get_integration_resource_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_integration_resource_property("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_integration_resource_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_integration_resource_property("test-resource_arn", )


async def test_get_integration_table_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_integration_table_properties("test-resource_arn", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_integration_table_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_integration_table_properties("test-resource_arn", "test-table_name", )


async def test_get_job_bookmark(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_job_bookmark("test-job_name", )
    mock_client.call.assert_called_once()


async def test_get_job_bookmark_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_job_bookmark("test-job_name", )


async def test_get_job_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_job_runs("test-job_name", )
    mock_client.call.assert_called_once()


async def test_get_job_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_job_runs("test-job_name", )


async def test_get_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_jobs()
    mock_client.call.assert_called_once()


async def test_get_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_jobs()


async def test_get_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_mapping({}, )
    mock_client.call.assert_called_once()


async def test_get_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_mapping({}, )


async def test_get_ml_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ml_task_run("test-transform_id", "test-task_run_id", )
    mock_client.call.assert_called_once()


async def test_get_ml_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ml_task_run("test-transform_id", "test-task_run_id", )


async def test_get_ml_task_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ml_task_runs("test-transform_id", )
    mock_client.call.assert_called_once()


async def test_get_ml_task_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ml_task_runs("test-transform_id", )


async def test_get_ml_transform(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ml_transform("test-transform_id", )
    mock_client.call.assert_called_once()


async def test_get_ml_transform_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ml_transform("test-transform_id", )


async def test_get_ml_transforms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ml_transforms()
    mock_client.call.assert_called_once()


async def test_get_ml_transforms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ml_transforms()


async def test_get_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_partition("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_get_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_partition("test-database_name", "test-table_name", [], )


async def test_get_partition_indexes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_partition_indexes("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_partition_indexes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_partition_indexes("test-database_name", "test-table_name", )


async def test_get_partitions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_partitions("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_partitions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_partitions("test-database_name", "test-table_name", )


async def test_get_plan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_plan([], {}, )
    mock_client.call.assert_called_once()


async def test_get_plan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_plan([], {}, )


async def test_get_registry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_registry({}, )
    mock_client.call.assert_called_once()


async def test_get_registry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_registry({}, )


async def test_get_resource_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policies()
    mock_client.call.assert_called_once()


async def test_get_resource_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policies()


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy()
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy()


async def test_get_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_schema({}, )
    mock_client.call.assert_called_once()


async def test_get_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_schema({}, )


async def test_get_schema_by_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_schema_by_definition({}, "test-schema_definition", )
    mock_client.call.assert_called_once()


async def test_get_schema_by_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_schema_by_definition({}, "test-schema_definition", )


async def test_get_schema_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_schema_version()
    mock_client.call.assert_called_once()


async def test_get_schema_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_schema_version()


async def test_get_schema_versions_diff(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_schema_versions_diff({}, {}, {}, "test-schema_diff_type", )
    mock_client.call.assert_called_once()


async def test_get_schema_versions_diff_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_schema_versions_diff({}, {}, {}, "test-schema_diff_type", )


async def test_get_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_security_configuration("test-name", )
    mock_client.call.assert_called_once()


async def test_get_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_security_configuration("test-name", )


async def test_get_security_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_security_configurations()
    mock_client.call.assert_called_once()


async def test_get_security_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_security_configurations()


async def test_get_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_session("test-id", )
    mock_client.call.assert_called_once()


async def test_get_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_session("test-id", )


async def test_get_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_statement("test-session_id", 1, )
    mock_client.call.assert_called_once()


async def test_get_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_statement("test-session_id", 1, )


async def test_get_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table("test-database_name", "test-name", )
    mock_client.call.assert_called_once()


async def test_get_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table("test-database_name", "test-name", )


async def test_get_table_optimizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_get_table_optimizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )


async def test_get_table_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table_version("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_table_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_version("test-database_name", "test-table_name", )


async def test_get_table_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table_versions("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_table_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_versions("test-database_name", "test-table_name", )


async def test_get_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_tables("test-database_name", )
    mock_client.call.assert_called_once()


async def test_get_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_tables("test-database_name", )


async def test_get_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_tags("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_tags("test-resource_arn", )


async def test_get_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_trigger("test-name", )
    mock_client.call.assert_called_once()


async def test_get_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_trigger("test-name", )


async def test_get_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_triggers()
    mock_client.call.assert_called_once()


async def test_get_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_triggers()


async def test_get_unfiltered_partition_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", [], [], )
    mock_client.call.assert_called_once()


async def test_get_unfiltered_partition_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", [], [], )


async def test_get_unfiltered_partitions_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_get_unfiltered_partitions_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", [], )


async def test_get_unfiltered_table_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", [], )
    mock_client.call.assert_called_once()


async def test_get_unfiltered_table_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", [], )


async def test_get_usage_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_usage_profile("test-name", )
    mock_client.call.assert_called_once()


async def test_get_usage_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_usage_profile("test-name", )


async def test_get_user_defined_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_user_defined_function("test-database_name", "test-function_name", )
    mock_client.call.assert_called_once()


async def test_get_user_defined_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_defined_function("test-database_name", "test-function_name", )


async def test_get_user_defined_functions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_user_defined_functions("test-pattern", )
    mock_client.call.assert_called_once()


async def test_get_user_defined_functions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_defined_functions("test-pattern", )


async def test_get_workflow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_workflow("test-name", )
    mock_client.call.assert_called_once()


async def test_get_workflow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_workflow("test-name", )


async def test_get_workflow_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_workflow_run("test-name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_get_workflow_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_workflow_run("test-name", "test-run_id", )


async def test_get_workflow_run_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_workflow_run_properties("test-name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_get_workflow_run_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_workflow_run_properties("test-name", "test-run_id", )


async def test_get_workflow_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_workflow_runs("test-name", )
    mock_client.call.assert_called_once()


async def test_get_workflow_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_workflow_runs("test-name", )


async def test_import_catalog_to_glue(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_catalog_to_glue()
    mock_client.call.assert_called_once()


async def test_import_catalog_to_glue_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_catalog_to_glue()


async def test_list_blueprints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_blueprints()
    mock_client.call.assert_called_once()


async def test_list_blueprints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_blueprints()


async def test_list_column_statistics_task_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_column_statistics_task_runs()
    mock_client.call.assert_called_once()


async def test_list_column_statistics_task_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_column_statistics_task_runs()


async def test_list_connection_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_connection_types()
    mock_client.call.assert_called_once()


async def test_list_connection_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_connection_types()


async def test_list_crawlers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_crawlers()
    mock_client.call.assert_called_once()


async def test_list_crawlers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_crawlers()


async def test_list_crawls(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_crawls("test-crawler_name", )
    mock_client.call.assert_called_once()


async def test_list_crawls_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_crawls("test-crawler_name", )


async def test_list_custom_entity_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_entity_types()
    mock_client.call.assert_called_once()


async def test_list_custom_entity_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_entity_types()


async def test_list_data_quality_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_results()
    mock_client.call.assert_called_once()


async def test_list_data_quality_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_results()


async def test_list_data_quality_rule_recommendation_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_rule_recommendation_runs()
    mock_client.call.assert_called_once()


async def test_list_data_quality_rule_recommendation_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_rule_recommendation_runs()


async def test_list_data_quality_ruleset_evaluation_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_ruleset_evaluation_runs()
    mock_client.call.assert_called_once()


async def test_list_data_quality_ruleset_evaluation_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_ruleset_evaluation_runs()


async def test_list_data_quality_rulesets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_rulesets()
    mock_client.call.assert_called_once()


async def test_list_data_quality_rulesets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_rulesets()


async def test_list_data_quality_statistic_annotations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_statistic_annotations()
    mock_client.call.assert_called_once()


async def test_list_data_quality_statistic_annotations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_statistic_annotations()


async def test_list_data_quality_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_quality_statistics()
    mock_client.call.assert_called_once()


async def test_list_data_quality_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_quality_statistics()


async def test_list_dev_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dev_endpoints()
    mock_client.call.assert_called_once()


async def test_list_dev_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dev_endpoints()


async def test_list_entities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_entities()
    mock_client.call.assert_called_once()


async def test_list_entities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_entities()


async def test_list_ml_transforms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ml_transforms()
    mock_client.call.assert_called_once()


async def test_list_ml_transforms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ml_transforms()


async def test_list_registries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_registries()
    mock_client.call.assert_called_once()


async def test_list_registries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_registries()


async def test_list_schema_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_schema_versions({}, )
    mock_client.call.assert_called_once()


async def test_list_schema_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_schema_versions({}, )


async def test_list_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_schemas()
    mock_client.call.assert_called_once()


async def test_list_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_schemas()


async def test_list_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sessions()
    mock_client.call.assert_called_once()


async def test_list_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sessions()


async def test_list_statements(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_statements("test-session_id", )
    mock_client.call.assert_called_once()


async def test_list_statements_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_statements("test-session_id", )


async def test_list_table_optimizer_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_list_table_optimizer_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", )


async def test_list_triggers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_triggers()
    mock_client.call.assert_called_once()


async def test_list_triggers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_triggers()


async def test_list_usage_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_usage_profiles()
    mock_client.call.assert_called_once()


async def test_list_usage_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_usage_profiles()


async def test_list_workflows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_workflows()
    mock_client.call.assert_called_once()


async def test_list_workflows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_workflows()


async def test_modify_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_integration("test-integration_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_integration("test-integration_identifier", )


async def test_put_data_catalog_encryption_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_data_catalog_encryption_settings({}, )
    mock_client.call.assert_called_once()


async def test_put_data_catalog_encryption_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_data_catalog_encryption_settings({}, )


async def test_put_data_quality_profile_annotation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_data_quality_profile_annotation("test-profile_id", "test-inclusion_annotation", )
    mock_client.call.assert_called_once()


async def test_put_data_quality_profile_annotation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_data_quality_profile_annotation("test-profile_id", "test-inclusion_annotation", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-policy_in_json", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-policy_in_json", )


async def test_put_schema_version_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_schema_version_metadata({}, )
    mock_client.call.assert_called_once()


async def test_put_schema_version_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_schema_version_metadata({}, )


async def test_put_workflow_run_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_workflow_run_properties("test-name", "test-run_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_workflow_run_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_workflow_run_properties("test-name", "test-run_id", {}, )


async def test_query_schema_version_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await query_schema_version_metadata()
    mock_client.call.assert_called_once()


async def test_query_schema_version_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await query_schema_version_metadata()


async def test_register_schema_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_schema_version({}, "test-schema_definition", )
    mock_client.call.assert_called_once()


async def test_register_schema_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_schema_version({}, "test-schema_definition", )


async def test_remove_schema_version_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_schema_version_metadata({}, )
    mock_client.call.assert_called_once()


async def test_remove_schema_version_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_schema_version_metadata({}, )


async def test_reset_job_bookmark(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_job_bookmark("test-job_name", )
    mock_client.call.assert_called_once()


async def test_reset_job_bookmark_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_job_bookmark("test-job_name", )


async def test_resume_workflow_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_workflow_run("test-name", "test-run_id", [], )
    mock_client.call.assert_called_once()


async def test_resume_workflow_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_workflow_run("test-name", "test-run_id", [], )


async def test_run_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_connection()
    mock_client.call.assert_called_once()


async def test_run_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_connection()


async def test_run_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_statement("test-session_id", "test-code", )
    mock_client.call.assert_called_once()


async def test_run_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_statement("test-session_id", "test-code", )


async def test_search_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_tables()
    mock_client.call.assert_called_once()


async def test_search_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_tables()


async def test_start_blueprint_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_blueprint_run("test-blueprint_name", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_start_blueprint_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_blueprint_run("test-blueprint_name", "test-role_arn", )


async def test_start_column_statistics_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", )
    mock_client.call.assert_called_once()


async def test_start_column_statistics_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", )


async def test_start_column_statistics_task_run_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_column_statistics_task_run_schedule("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_start_column_statistics_task_run_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_column_statistics_task_run_schedule("test-database_name", "test-table_name", )


async def test_start_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_crawler("test-name", )
    mock_client.call.assert_called_once()


async def test_start_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_crawler("test-name", )


async def test_start_crawler_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_crawler_schedule("test-crawler_name", )
    mock_client.call.assert_called_once()


async def test_start_crawler_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_crawler_schedule("test-crawler_name", )


async def test_start_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_data_quality_rule_recommendation_run({}, "test-role", )
    mock_client.call.assert_called_once()


async def test_start_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_data_quality_rule_recommendation_run({}, "test-role", )


async def test_start_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_data_quality_ruleset_evaluation_run({}, "test-role", [], )
    mock_client.call.assert_called_once()


async def test_start_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_data_quality_ruleset_evaluation_run({}, "test-role", [], )


async def test_start_export_labels_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_export_labels_task_run("test-transform_id", "test-output_s3_path", )
    mock_client.call.assert_called_once()


async def test_start_export_labels_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_export_labels_task_run("test-transform_id", "test-output_s3_path", )


async def test_start_import_labels_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_import_labels_task_run("test-transform_id", "test-input_s3_path", )
    mock_client.call.assert_called_once()


async def test_start_import_labels_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_import_labels_task_run("test-transform_id", "test-input_s3_path", )


async def test_start_ml_evaluation_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_ml_evaluation_task_run("test-transform_id", )
    mock_client.call.assert_called_once()


async def test_start_ml_evaluation_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_ml_evaluation_task_run("test-transform_id", )


async def test_start_ml_labeling_set_generation_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_ml_labeling_set_generation_task_run("test-transform_id", "test-output_s3_path", )
    mock_client.call.assert_called_once()


async def test_start_ml_labeling_set_generation_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_ml_labeling_set_generation_task_run("test-transform_id", "test-output_s3_path", )


async def test_start_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_trigger("test-name", )
    mock_client.call.assert_called_once()


async def test_start_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_trigger("test-name", )


async def test_start_workflow_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_workflow_run("test-name", )
    mock_client.call.assert_called_once()


async def test_start_workflow_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_workflow_run("test-name", )


async def test_stop_column_statistics_task_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_column_statistics_task_run("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_stop_column_statistics_task_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_column_statistics_task_run("test-database_name", "test-table_name", )


async def test_stop_column_statistics_task_run_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_column_statistics_task_run_schedule("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_stop_column_statistics_task_run_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_column_statistics_task_run_schedule("test-database_name", "test-table_name", )


async def test_stop_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_crawler("test-name", )
    mock_client.call.assert_called_once()


async def test_stop_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_crawler("test-name", )


async def test_stop_crawler_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_crawler_schedule("test-crawler_name", )
    mock_client.call.assert_called_once()


async def test_stop_crawler_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_crawler_schedule("test-crawler_name", )


async def test_stop_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_session("test-id", )
    mock_client.call.assert_called_once()


async def test_stop_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_session("test-id", )


async def test_stop_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_trigger("test-name", )
    mock_client.call.assert_called_once()


async def test_stop_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_trigger("test-name", )


async def test_stop_workflow_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_workflow_run("test-name", "test-run_id", )
    mock_client.call.assert_called_once()


async def test_stop_workflow_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_workflow_run("test-name", "test-run_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_blueprint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_blueprint("test-name", "test-blueprint_location", )
    mock_client.call.assert_called_once()


async def test_update_blueprint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_blueprint("test-name", "test-blueprint_location", )


async def test_update_catalog(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_catalog("test-catalog_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_catalog_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_catalog("test-catalog_id", {}, )


async def test_update_classifier(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_classifier()
    mock_client.call.assert_called_once()


async def test_update_classifier_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_classifier()


async def test_update_column_statistics_for_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_column_statistics_for_partition("test-database_name", "test-table_name", [], [], )
    mock_client.call.assert_called_once()


async def test_update_column_statistics_for_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_column_statistics_for_partition("test-database_name", "test-table_name", [], [], )


async def test_update_column_statistics_for_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_column_statistics_for_table("test-database_name", "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_update_column_statistics_for_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_column_statistics_for_table("test-database_name", "test-table_name", [], )


async def test_update_column_statistics_task_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_column_statistics_task_settings("test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_update_column_statistics_task_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_column_statistics_task_settings("test-database_name", "test-table_name", )


async def test_update_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_connection("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_connection("test-name", {}, )


async def test_update_crawler(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_crawler("test-name", )
    mock_client.call.assert_called_once()


async def test_update_crawler_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_crawler("test-name", )


async def test_update_crawler_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_crawler_schedule("test-crawler_name", )
    mock_client.call.assert_called_once()


async def test_update_crawler_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_crawler_schedule("test-crawler_name", )


async def test_update_data_quality_ruleset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_quality_ruleset("test-name", )
    mock_client.call.assert_called_once()


async def test_update_data_quality_ruleset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_quality_ruleset("test-name", )


async def test_update_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_database("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_database("test-name", {}, )


async def test_update_dev_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dev_endpoint("test-endpoint_name", )
    mock_client.call.assert_called_once()


async def test_update_dev_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dev_endpoint("test-endpoint_name", )


async def test_update_glue_identity_center_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_glue_identity_center_configuration()
    mock_client.call.assert_called_once()


async def test_update_glue_identity_center_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_glue_identity_center_configuration()


async def test_update_integration_resource_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_integration_resource_property("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_update_integration_resource_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_integration_resource_property("test-resource_arn", )


async def test_update_integration_table_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_integration_table_properties("test-resource_arn", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_update_integration_table_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_integration_table_properties("test-resource_arn", "test-table_name", )


async def test_update_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_job("test-job_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_job("test-job_name", {}, )


async def test_update_job_from_source_control(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_job_from_source_control()
    mock_client.call.assert_called_once()


async def test_update_job_from_source_control_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_job_from_source_control()


async def test_update_ml_transform(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ml_transform("test-transform_id", )
    mock_client.call.assert_called_once()


async def test_update_ml_transform_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ml_transform("test-transform_id", )


async def test_update_partition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_partition("test-database_name", "test-table_name", [], {}, )
    mock_client.call.assert_called_once()


async def test_update_partition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_partition("test-database_name", "test-table_name", [], {}, )


async def test_update_registry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_registry({}, "test-description", )
    mock_client.call.assert_called_once()


async def test_update_registry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_registry({}, "test-description", )


async def test_update_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_schema({}, )
    mock_client.call.assert_called_once()


async def test_update_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_schema({}, )


async def test_update_source_control_from_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_source_control_from_job()
    mock_client.call.assert_called_once()


async def test_update_source_control_from_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_source_control_from_job()


async def test_update_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_table("test-database_name", )
    mock_client.call.assert_called_once()


async def test_update_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_table("test-database_name", )


async def test_update_table_optimizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, )
    mock_client.call.assert_called_once()


async def test_update_table_optimizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, )


async def test_update_trigger(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_trigger("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_trigger_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_trigger("test-name", {}, )


async def test_update_usage_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_usage_profile("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_usage_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_usage_profile("test-name", {}, )


async def test_update_user_defined_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_defined_function("test-database_name", "test-function_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_user_defined_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_defined_function("test-database_name", "test-function_name", {}, )


async def test_update_workflow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_workflow("test-name", )
    mock_client.call.assert_called_once()


async def test_update_workflow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.glue.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_workflow("test-name", )


@pytest.mark.asyncio
async def test_batch_create_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_create_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_create_partition("test-database_name", "test-table_name", "test-partition_input_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_delete_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_delete_connection("test-connection_name_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_delete_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_delete_partition("test-database_name", "test-table_name", "test-partitions_to_delete", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_delete_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_delete_table("test-database_name", "test-tables_to_delete", catalog_id="test-catalog_id", transaction_id="test-transaction_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_table_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_delete_table_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_delete_table_version("test-database_name", "test-table_name", "test-version_ids", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_blueprints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_get_blueprints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_get_blueprints("test-names", include_blueprint=True, include_parameter_spec=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_get_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_get_partition("test-database_name", "test-table_name", "test-partitions_to_get", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_workflows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_get_workflows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_get_workflows("test-names", include_graph=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_put_data_quality_statistic_annotation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_put_data_quality_statistic_annotation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_put_data_quality_statistic_annotation("test-inclusion_annotations", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_update_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import batch_update_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await batch_update_partition("test-database_name", "test-table_name", "test-entries", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import cancel_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await cancel_statement("test-session_id", "test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_blueprint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_blueprint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_blueprint("test-name", "test-blueprint_location", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_catalog_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_catalog
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_catalog("test-name", "test-catalog_input", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_classifier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_classifier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_classifier(grok_classifier="test-grok_classifier", xml_classifier="test-xml_classifier", json_classifier="test-json_classifier", csv_classifier="test-csv_classifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_column_statistics_task_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_column_statistics_task_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", schedule="test-schedule", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_connection("test-connection_input", catalog_id="test-catalog_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_crawler_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_crawler
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_crawler("test-name", "test-role", "test-targets", database_name="test-database_name", description="test-description", schedule="test-schedule", classifiers="test-classifiers", table_prefix="test-table_prefix", schema_change_policy="{}", recrawl_policy="{}", lineage_configuration={}, lake_formation_configuration={}, configuration={}, crawler_security_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_entity_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_custom_entity_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_custom_entity_type("test-name", "test-regex_string", context_words={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_quality_ruleset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_data_quality_ruleset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_data_quality_ruleset("test-name", "test-ruleset", description="test-description", tags=[{"Key": "k", "Value": "v"}], target_table="test-target_table", data_quality_security_configuration={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_database("test-database_input", catalog_id="test-catalog_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dev_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_dev_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_dev_endpoint("test-endpoint_name", "test-role_arn", security_group_ids="test-security_group_ids", subnet_id="test-subnet_id", public_key="test-public_key", public_keys="test-public_keys", number_of_nodes="test-number_of_nodes", worker_type="test-worker_type", glue_version="test-glue_version", number_of_workers="test-number_of_workers", extra_python_libs_s3_path="test-extra_python_libs_s3_path", extra_jars_s3_path="test-extra_jars_s3_path", security_configuration={}, tags=[{"Key": "k", "Value": "v"}], arguments="test-arguments", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_glue_identity_center_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_glue_identity_center_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_glue_identity_center_configuration("test-instance_arn", scopes="test-scopes", user_background_sessions_enabled="test-user_background_sessions_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_integration("test-integration_name", "test-source_arn", "test-target_arn", description="test-description", data_filter=[{}], kms_key_id="test-kms_key_id", additional_encryption_context={}, tags=[{"Key": "k", "Value": "v"}], integration_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_resource_property_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_integration_resource_property
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_integration_resource_property("test-resource_arn", source_processing_properties={}, target_processing_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_table_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_integration_table_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_integration_table_properties("test-resource_arn", "test-table_name", source_table_config={}, target_table_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_job("test-name", "test-role", "test-command", job_mode="test-job_mode", job_run_queuing_enabled="test-job_run_queuing_enabled", description="test-description", log_uri="test-log_uri", execution_property="test-execution_property", default_arguments="test-default_arguments", non_overridable_arguments="test-non_overridable_arguments", connections="test-connections", max_retries=1, allocated_capacity="test-allocated_capacity", timeout=1, max_capacity=1, security_configuration={}, tags=[{"Key": "k", "Value": "v"}], notification_property="test-notification_property", glue_version="test-glue_version", number_of_workers="test-number_of_workers", worker_type="test-worker_type", code_gen_configuration_nodes={}, execution_class="test-execution_class", source_control_details="test-source_control_details", maintenance_window="test-maintenance_window", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ml_transform_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_ml_transform
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_ml_transform("test-name", "test-input_record_tables", "test-parameters", "test-role", description="test-description", glue_version="test-glue_version", max_capacity=1, worker_type="test-worker_type", number_of_workers="test-number_of_workers", timeout=1, max_retries=1, tags=[{"Key": "k", "Value": "v"}], transform_encryption="test-transform_encryption", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_partition("test-database_name", "test-table_name", "test-partition_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_partition_index_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_partition_index
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_partition_index("test-database_name", "test-table_name", "test-partition_index", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_registry_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_registry
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_registry("test-registry_name", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_schema_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_schema
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_schema("test-schema_name", "test-data_format", registry_id="test-registry_id", compatibility="test-compatibility", description="test-description", tags=[{"Key": "k", "Value": "v"}], schema_definition={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_script_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_script
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_script(dag_nodes="test-dag_nodes", dag_edges="test-dag_edges", language="test-language", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_session("test-id", "test-role", "test-command", description="test-description", timeout=1, idle_timeout=1, default_arguments="test-default_arguments", connections="test-connections", max_capacity=1, number_of_workers="test-number_of_workers", worker_type="test-worker_type", security_configuration={}, glue_version="test-glue_version", tags=[{"Key": "k", "Value": "v"}], request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_table("test-database_name", catalog_id="test-catalog_id", name="test-name", table_input="test-table_input", partition_indexes="test-partition_indexes", transaction_id="test-transaction_id", open_table_format_input="test-open_table_format_input", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_trigger_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_trigger
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_trigger("test-name", "test-type_value", "test-actions", workflow_name="test-workflow_name", schedule="test-schedule", predicate="test-predicate", description="test-description", start_on_creation="test-start_on_creation", tags=[{"Key": "k", "Value": "v"}], event_batching_condition="test-event_batching_condition", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_usage_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_usage_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_usage_profile("test-name", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_defined_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_user_defined_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_user_defined_function("test-database_name", "test-function_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_workflow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import create_workflow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await create_workflow("test-name", description="test-description", default_run_properties={}, tags=[{"Key": "k", "Value": "v"}], max_concurrent_runs=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_column_statistics_for_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_column_statistics_for_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_connection("test-connection_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_database("test-name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_partition("test-database_name", "test-table_name", "test-partition_values", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_partition_index_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_partition_index
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_partition_index("test-database_name", "test-table_name", "test-index_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_resource_policy(policy_hash_condition="test-policy_hash_condition", resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_table("test-database_name", "test-name", catalog_id="test-catalog_id", transaction_id="test-transaction_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_table_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_table_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_table_version("test-database_name", "test-table_name", "test-version_id", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_user_defined_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import delete_user_defined_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await delete_user_defined_function("test-database_name", "test-function_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_entity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import describe_entity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await describe_entity("test-connection_name", "test-entity_name", catalog_id="test-catalog_id", next_token="test-next_token", data_store_api_version="test-data_store_api_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_inbound_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import describe_inbound_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await describe_inbound_integrations(integration_arn="test-integration_arn", marker="test-marker", max_records=1, target_arn="test-target_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import describe_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await describe_integrations(integration_identifier="test-integration_identifier", marker="test-marker", max_records=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_blueprint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_blueprint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_blueprint("test-name", include_blueprint=True, include_parameter_spec=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_blueprint_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_blueprint_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_blueprint_runs("test-blueprint_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_catalog_import_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_catalog_import_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_catalog_import_status(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_catalogs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_catalogs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_catalogs(parent_catalog_id="test-parent_catalog_id", next_token="test-next_token", max_results=1, recursive=True, include_root=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_classifiers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_classifiers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_classifiers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_column_statistics_for_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_names", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_column_statistics_for_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_column_statistics_for_table("test-database_name", "test-table_name", "test-column_names", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_column_statistics_task_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_column_statistics_task_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_column_statistics_task_runs("test-database_name", "test-table_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_connection("test-name", catalog_id="test-catalog_id", hide_password="test-hide_password", apply_override_for_compute_environment=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_connections(catalog_id="test-catalog_id", filter="test-filter", hide_password="test-hide_password", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_crawler_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_crawler_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_crawler_metrics(crawler_name_list="test-crawler_name_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_crawlers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_crawlers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_crawlers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_data_catalog_encryption_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_data_catalog_encryption_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_data_catalog_encryption_settings(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_data_quality_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_data_quality_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_data_quality_model("test-profile_id", statistic_id="test-statistic_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_database("test-name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_databases(catalog_id="test-catalog_id", next_token="test-next_token", max_results=1, resource_share_type="test-resource_share_type", attributes_to_get="test-attributes_to_get", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_dataflow_graph_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_dataflow_graph
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_dataflow_graph(python_script="test-python_script", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_dev_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_dev_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_dev_endpoints(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_entity_records_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_entity_records
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_entity_records("test-entity_name", 1, connection_name="test-connection_name", catalog_id="test-catalog_id", next_token="test-next_token", data_store_api_version="test-data_store_api_version", connection_options={}, filter_predicate="test-filter_predicate", order_by="test-order_by", selected_fields="test-selected_fields", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_job_bookmark_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_job_bookmark
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_job_bookmark("test-job_name", run_id="test-run_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_job_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_job_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_job_runs("test-job_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_jobs(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_mapping("test-source", sinks="test-sinks", location="test-location", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ml_task_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_ml_task_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_ml_task_runs("test-transform_id", next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ml_transforms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_ml_transforms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_ml_transforms(next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_partition("test-database_name", "test-table_name", "test-partition_values", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_partition_indexes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_partition_indexes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_partition_indexes("test-database_name", "test-table_name", catalog_id="test-catalog_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_partitions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_partitions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_partitions("test-database_name", "test-table_name", catalog_id="test-catalog_id", expression="test-expression", next_token="test-next_token", segment="test-segment", max_results=1, exclude_column_schema="test-exclude_column_schema", transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_plan_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_plan
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_plan({}, "test-source", sinks="test-sinks", location="test-location", language="test-language", additional_plan_options_map={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resource_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_resource_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_resource_policies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_resource_policy(resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_schema_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_schema_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_schema_version(schema_id="test-schema_id", schema_version_id="test-schema_version_id", schema_version_number="test-schema_version_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_security_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_security_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_security_configurations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_statement("test-session_id", "test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_table("test-database_name", "test-name", catalog_id="test-catalog_id", transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", audit_context={}, include_status_details=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_table_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_table_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_table_version("test-database_name", "test-table_name", catalog_id="test-catalog_id", version_id="test-version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_table_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_table_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_table_versions("test-database_name", "test-table_name", catalog_id="test-catalog_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_tables("test-database_name", catalog_id="test-catalog_id", expression="test-expression", next_token="test-next_token", max_results=1, transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", audit_context={}, include_status_details=True, attributes_to_get="test-attributes_to_get", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_triggers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_triggers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_triggers(next_token="test-next_token", dependent_job_name="test-dependent_job_name", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_unfiltered_partition_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_unfiltered_partition_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", "test-partition_values", 1, region="test-region", audit_context={}, query_session_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_unfiltered_partitions_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_unfiltered_partitions_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", 1, region="test-region", expression="test-expression", audit_context={}, next_token="test-next_token", segment="test-segment", max_results=1, query_session_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_unfiltered_table_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_unfiltered_table_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", 1, region="test-region", audit_context={}, parent_resource_arn="test-parent_resource_arn", root_resource_arn="test-root_resource_arn", supported_dialect=1, permissions="test-permissions", query_session_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_defined_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_user_defined_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_user_defined_function("test-database_name", "test-function_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_defined_functions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_user_defined_functions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_user_defined_functions("test-pattern", catalog_id="test-catalog_id", database_name="test-database_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_workflow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_workflow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_workflow("test-name", include_graph=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_workflow_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_workflow_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_workflow_run("test-name", "test-run_id", include_graph=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_workflow_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import get_workflow_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await get_workflow_runs("test-name", include_graph=True, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_catalog_to_glue_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import import_catalog_to_glue
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await import_catalog_to_glue(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_blueprints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_blueprints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_blueprints(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_column_statistics_task_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_column_statistics_task_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_column_statistics_task_runs(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_connection_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_connection_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_connection_types(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_crawlers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_crawlers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_crawlers(max_results=1, next_token="test-next_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_crawls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_crawls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_crawls("test-crawler_name", max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_entity_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_custom_entity_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_custom_entity_types(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_results(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_rule_recommendation_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_rule_recommendation_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_rule_recommendation_runs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_ruleset_evaluation_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_ruleset_evaluation_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_ruleset_evaluation_runs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_rulesets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_rulesets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_rulesets(next_token="test-next_token", max_results=1, filter="test-filter", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_statistic_annotations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_statistic_annotations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_statistic_annotations(statistic_id="test-statistic_id", profile_id="test-profile_id", timestamp_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_quality_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_data_quality_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_data_quality_statistics(statistic_id="test-statistic_id", profile_id="test-profile_id", timestamp_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dev_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_dev_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_dev_endpoints(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_entities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_entities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_entities(connection_name="test-connection_name", catalog_id="test-catalog_id", parent_entity_name="test-parent_entity_name", next_token="test-next_token", data_store_api_version="test-data_store_api_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ml_transforms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_ml_transforms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_ml_transforms(next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_registries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_registries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_registries(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_schema_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_schema_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_schema_versions("test-schema_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_schemas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_schemas(registry_id="test-registry_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_sessions(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_statements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_statements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_statements("test-session_id", request_origin="test-request_origin", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_table_optimizer_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_table_optimizer_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_triggers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_triggers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_triggers(next_token="test-next_token", dependent_job_name="test-dependent_job_name", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_usage_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_usage_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_usage_profiles(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_workflows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import list_workflows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await list_workflows(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import modify_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await modify_integration("test-integration_identifier", description="test-description", data_filter=[{}], integration_config={}, integration_name="test-integration_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_data_catalog_encryption_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import put_data_catalog_encryption_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await put_data_catalog_encryption_settings({}, catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-policy_in_json", resource_arn="test-resource_arn", policy_hash_condition="test-policy_hash_condition", policy_exists_condition="test-policy_exists_condition", enable_hybrid=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import put_schema_version_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await put_schema_version_metadata("test-metadata_key_value", schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_query_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import query_schema_version_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await query_schema_version_metadata(schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", metadata_list="test-metadata_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import remove_schema_version_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await remove_schema_version_metadata("test-metadata_key_value", schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_job_bookmark_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import reset_job_bookmark
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await reset_job_bookmark("test-job_name", run_id="test-run_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import run_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await run_connection(connection_name="test-connection_name", catalog_id="test-catalog_id", run_connection_input="test-run_connection_input", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import run_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await run_statement("test-session_id", "test-code", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import search_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await search_tables(catalog_id="test-catalog_id", next_token="test-next_token", filters=[{}], search_text="test-search_text", sort_criteria="test-sort_criteria", max_results=1, resource_share_type="test-resource_share_type", include_status_details=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_blueprint_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_blueprint_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_blueprint_run("test-blueprint_name", "test-role_arn", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_column_statistics_task_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_column_statistics_task_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_data_quality_rule_recommendation_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_data_quality_rule_recommendation_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_data_quality_rule_recommendation_run("test-data_source", "test-role", number_of_workers="test-number_of_workers", timeout=1, created_ruleset_name="test-created_ruleset_name", data_quality_security_configuration={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_data_quality_ruleset_evaluation_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_data_quality_ruleset_evaluation_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_data_quality_ruleset_evaluation_run("test-data_source", "test-role", "test-ruleset_names", number_of_workers="test-number_of_workers", timeout=1, client_token="test-client_token", additional_run_options={}, additional_data_sources="test-additional_data_sources", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_import_labels_task_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_import_labels_task_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_import_labels_task_run("test-transform_id", "test-input_s3_path", replace_all_labels="test-replace_all_labels", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_workflow_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import start_workflow_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await start_workflow_run("test-name", run_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import stop_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await stop_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_blueprint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_blueprint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_blueprint("test-name", "test-blueprint_location", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_classifier_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_classifier
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_classifier(grok_classifier="test-grok_classifier", xml_classifier="test-xml_classifier", json_classifier="test-json_classifier", csv_classifier="test-csv_classifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_column_statistics_for_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_statistics_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_column_statistics_for_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_column_statistics_for_table("test-database_name", "test-table_name", "test-column_statistics_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_column_statistics_task_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_column_statistics_task_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_column_statistics_task_settings("test-database_name", "test-table_name", role="test-role", schedule="test-schedule", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_connection("test-name", "test-connection_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_crawler_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_crawler
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_crawler("test-name", role="test-role", database_name="test-database_name", description="test-description", targets="test-targets", schedule="test-schedule", classifiers="test-classifiers", table_prefix="test-table_prefix", schema_change_policy="{}", recrawl_policy="{}", lineage_configuration={}, lake_formation_configuration={}, configuration={}, crawler_security_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_crawler_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_crawler_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_crawler_schedule("test-crawler_name", schedule="test-schedule", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_quality_ruleset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_data_quality_ruleset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_data_quality_ruleset("test-name", description="test-description", ruleset="test-ruleset", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_database("test-name", "test-database_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dev_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_dev_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_dev_endpoint("test-endpoint_name", public_key="test-public_key", add_public_keys="test-add_public_keys", delete_public_keys=True, custom_libraries="test-custom_libraries", update_etl_libraries="test-update_etl_libraries", delete_arguments=True, add_arguments="test-add_arguments", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_glue_identity_center_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_glue_identity_center_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_glue_identity_center_configuration(scopes="test-scopes", user_background_sessions_enabled="test-user_background_sessions_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_integration_resource_property_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_integration_resource_property
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_integration_resource_property("test-resource_arn", source_processing_properties={}, target_processing_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_integration_table_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_integration_table_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_integration_table_properties("test-resource_arn", "test-table_name", source_table_config={}, target_table_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_job_from_source_control_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_job_from_source_control
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_job_from_source_control(job_name="test-job_name", provider="test-provider", repository_name="test-repository_name", repository_owner="test-repository_owner", branch_name="test-branch_name", folder="test-folder", commit_id="test-commit_id", auth_strategy="test-auth_strategy", auth_token="test-auth_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ml_transform_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_ml_transform
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_ml_transform("test-transform_id", name="test-name", description="test-description", parameters="test-parameters", role="test-role", glue_version="test-glue_version", max_capacity=1, worker_type="test-worker_type", number_of_workers="test-number_of_workers", timeout=1, max_retries=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_partition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_partition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_partition("test-database_name", "test-table_name", "test-partition_value_list", "test-partition_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_schema_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_schema
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_schema("test-schema_id", schema_version_number="test-schema_version_number", compatibility="test-compatibility", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_source_control_from_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_source_control_from_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_source_control_from_job(job_name="test-job_name", provider="test-provider", repository_name="test-repository_name", repository_owner="test-repository_owner", branch_name="test-branch_name", folder="test-folder", commit_id="test-commit_id", auth_strategy="test-auth_strategy", auth_token="test-auth_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_table("test-database_name", catalog_id="test-catalog_id", name="test-name", table_input="test-table_input", skip_archive=True, transaction_id="test-transaction_id", version_id="test-version_id", view_update_action="test-view_update_action", force=True, update_open_table_format_input="test-update_open_table_format_input", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_usage_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_usage_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_usage_profile("test-name", {}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_defined_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_user_defined_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_user_defined_function("test-database_name", "test-function_name", "test-function_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_workflow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.glue import update_workflow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.glue.async_client", lambda *a, **kw: mock_client)
    await update_workflow("test-name", description="test-description", default_run_properties={}, max_concurrent_runs=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
