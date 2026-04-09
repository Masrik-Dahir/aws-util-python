"""Tests for aws_util.glue module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.glue as glue_mod
from aws_util.glue import (
    GlueJob,
    GlueJobRun,
    start_job_run,
    get_job_run,
    get_job,
    list_jobs,
    list_job_runs,
    wait_for_job_run,
    run_job_and_wait,
    stop_job_run,
    _parse_run,
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

REGION = "us-east-1"
JOB_NAME = "my-etl-job"
RUN_ID = "jr_abc123"


def _mock_run_dict(state: str = "SUCCEEDED") -> dict:
    return {
        "Id": RUN_ID,
        "JobName": JOB_NAME,
        "JobRunState": state,
        "StartedOn": None,
        "CompletedOn": None,
        "ExecutionTime": 120,
        "ErrorMessage": None,
        "Arguments": {},
    }


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_glue_job_model():
    job = GlueJob(job_name=JOB_NAME, description="ETL job", max_retries=2)
    assert job.job_name == JOB_NAME
    assert job.max_retries == 2


def test_glue_job_run_succeeded():
    run = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="SUCCEEDED")
    assert run.succeeded is True
    assert run.finished is True


def test_glue_job_run_failed():
    run = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="FAILED")
    assert run.succeeded is False
    assert run.finished is True


def test_glue_job_run_running():
    run = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="RUNNING")
    assert run.succeeded is False
    assert run.finished is False


def test_glue_job_run_timeout():
    run = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="TIMEOUT")
    assert run.finished is True


# ---------------------------------------------------------------------------
# _parse_run
# ---------------------------------------------------------------------------

def test_parse_run():
    run = _parse_run(_mock_run_dict())
    assert run.job_run_id == RUN_ID
    assert run.job_name == JOB_NAME
    assert run.job_run_state == "SUCCEEDED"
    assert run.execution_time == 120


# ---------------------------------------------------------------------------
# start_job_run
# ---------------------------------------------------------------------------

def test_start_job_run_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_job_run.return_value = {"JobRunId": RUN_ID}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_job_run(JOB_NAME, region_name=REGION)
    assert result == RUN_ID


def test_start_job_run_with_arguments(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_job_run.return_value = {"JobRunId": RUN_ID}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_job_run(JOB_NAME, arguments={"--input": "s3://bucket/key"}, region_name=REGION)
    assert result == RUN_ID
    call_kwargs = mock_client.start_job_run.call_args[1]
    assert call_kwargs["Arguments"] == {"--input": "s3://bucket/key"}


def test_start_job_run_with_worker_override(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_job_run.return_value = {"JobRunId": RUN_ID}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_job_run(JOB_NAME, worker_type="G.2X", number_of_workers=5, region_name=REGION)
    assert result == RUN_ID


def test_start_job_run_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_job_run.side_effect = ClientError(
        {"Error": {"Code": "EntityNotFoundException", "Message": "not found"}}, "StartJobRun"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start Glue job"):
        start_job_run("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# get_job_run
# ---------------------------------------------------------------------------

def test_get_job_run_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_run.return_value = {"JobRun": _mock_run_dict()}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_job_run(JOB_NAME, RUN_ID, region_name=REGION)
    assert isinstance(result, GlueJobRun)
    assert result.succeeded


def test_get_job_run_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_run.side_effect = ClientError(
        {"Error": {"Code": "EntityNotFoundException", "Message": "not found"}}, "GetJobRun"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_job_run failed"):
        get_job_run(JOB_NAME, "bad-run-id", region_name=REGION)


# ---------------------------------------------------------------------------
# get_job
# ---------------------------------------------------------------------------

def test_get_job_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job.return_value = {
        "Job": {
            "Name": JOB_NAME,
            "Description": "ETL",
            "Role": "arn:aws:iam::123:role/GlueRole",
            "GlueVersion": "3.0",
            "WorkerType": "G.1X",
            "NumberOfWorkers": 10,
            "MaxRetries": 0,
        }
    }
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_job(JOB_NAME, region_name=REGION)
    assert isinstance(result, GlueJob)
    assert result.job_name == JOB_NAME
    assert result.glue_version == "3.0"


def test_get_job_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job.side_effect = ClientError(
        {"Error": {"Code": "EntityNotFoundException", "Message": "not found"}}, "GetJob"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_job failed"):
        get_job("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------

def test_list_jobs_success(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"Jobs": [{"Name": "job-a"}, {"Name": "job-b"}]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_jobs(region_name=REGION)
    assert result == ["job-a", "job-b"]


def test_list_jobs_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "GetJobs"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_jobs failed"):
        list_jobs(region_name=REGION)


# ---------------------------------------------------------------------------
# list_job_runs
# ---------------------------------------------------------------------------

def test_list_job_runs_success(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"JobRuns": [_mock_run_dict("SUCCEEDED"), _mock_run_dict("FAILED")]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_job_runs(JOB_NAME, region_name=REGION)
    assert len(result) == 2
    assert all(isinstance(r, GlueJobRun) for r in result)


def test_list_job_runs_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "EntityNotFoundException", "Message": "not found"}}, "GetJobRuns"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_job_runs failed"):
        list_job_runs("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_job_run
# ---------------------------------------------------------------------------

def test_wait_for_job_run_already_done(monkeypatch):
    finished = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="SUCCEEDED")
    monkeypatch.setattr(glue_mod, "get_job_run", lambda jn, rid, region_name=None: finished)
    result = wait_for_job_run(JOB_NAME, RUN_ID, timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.succeeded


def test_wait_for_job_run_timeout(monkeypatch):
    running = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="RUNNING")
    monkeypatch.setattr(glue_mod, "get_job_run", lambda jn, rid, region_name=None: running)
    with pytest.raises(TimeoutError):
        wait_for_job_run(JOB_NAME, RUN_ID, timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# run_job_and_wait
# ---------------------------------------------------------------------------

def test_run_job_and_wait_success(monkeypatch):
    monkeypatch.setattr(glue_mod, "start_job_run", lambda *a, **kw: RUN_ID)
    finished = GlueJobRun(job_run_id=RUN_ID, job_name=JOB_NAME, job_run_state="SUCCEEDED")
    monkeypatch.setattr(glue_mod, "wait_for_job_run", lambda *a, **kw: finished)
    result = run_job_and_wait(JOB_NAME, region_name=REGION)
    assert result.succeeded


# ---------------------------------------------------------------------------
# stop_job_run
# ---------------------------------------------------------------------------

def test_stop_job_run_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_job_run.return_value = {"SuccessfulSubmissions": [{"JobName": JOB_NAME, "JobRunId": RUN_ID}]}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_job_run(JOB_NAME, RUN_ID, region_name=REGION)
    mock_client.batch_stop_job_run.assert_called_once()


def test_stop_job_run_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_job_run.side_effect = ClientError(
        {"Error": {"Code": "EntityNotFoundException", "Message": "not found"}}, "BatchStopJobRun"
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="stop_job_run failed"):
        stop_job_run("nonexistent", "bad-id", region_name=REGION)


def test_wait_for_job_run_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_job_run (line 243)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    import aws_util.glue as glue_mod
    from aws_util.glue import GlueJobRun, wait_for_job_run

    call_count = {"n": 0}

    def fake_get(job_name, run_id, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return GlueJobRun(job_name=job_name, job_run_id=run_id, job_run_state="RUNNING")
        return GlueJobRun(job_name=job_name, job_run_id=run_id, job_run_state="SUCCEEDED")

    monkeypatch.setattr(glue_mod, "get_job_run", fake_get)
    result = wait_for_job_run("my-job", "jr_1", timeout=10.0, poll_interval=0.001, region_name="us-east-1")
    assert result.job_run_state == "SUCCEEDED"


def test_batch_create_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_create_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_create_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.batch_create_partition.assert_called_once()


def test_batch_create_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_create_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_create_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch create partition"):
        batch_create_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_batch_delete_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_delete_connection([], region_name=REGION)
    mock_client.batch_delete_connection.assert_called_once()


def test_batch_delete_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete connection"):
        batch_delete_connection([], region_name=REGION)


def test_batch_delete_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_delete_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.batch_delete_partition.assert_called_once()


def test_batch_delete_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete partition"):
        batch_delete_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_batch_delete_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_delete_table("test-database_name", [], region_name=REGION)
    mock_client.batch_delete_table.assert_called_once()


def test_batch_delete_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete table"):
        batch_delete_table("test-database_name", [], region_name=REGION)


def test_batch_delete_table_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_table_version.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_delete_table_version("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.batch_delete_table_version.assert_called_once()


def test_batch_delete_table_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_table_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_table_version",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete table version"):
        batch_delete_table_version("test-database_name", "test-table_name", [], region_name=REGION)


def test_batch_get_blueprints(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_blueprints.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_blueprints([], region_name=REGION)
    mock_client.batch_get_blueprints.assert_called_once()


def test_batch_get_blueprints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_blueprints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_blueprints",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get blueprints"):
        batch_get_blueprints([], region_name=REGION)


def test_batch_get_crawlers(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_crawlers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_crawlers([], region_name=REGION)
    mock_client.batch_get_crawlers.assert_called_once()


def test_batch_get_crawlers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_crawlers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_crawlers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get crawlers"):
        batch_get_crawlers([], region_name=REGION)


def test_batch_get_custom_entity_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_custom_entity_types.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_custom_entity_types([], region_name=REGION)
    mock_client.batch_get_custom_entity_types.assert_called_once()


def test_batch_get_custom_entity_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_custom_entity_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_custom_entity_types",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get custom entity types"):
        batch_get_custom_entity_types([], region_name=REGION)


def test_batch_get_data_quality_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_data_quality_result.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_data_quality_result([], region_name=REGION)
    mock_client.batch_get_data_quality_result.assert_called_once()


def test_batch_get_data_quality_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_data_quality_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_data_quality_result",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get data quality result"):
        batch_get_data_quality_result([], region_name=REGION)


def test_batch_get_dev_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_dev_endpoints.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_dev_endpoints([], region_name=REGION)
    mock_client.batch_get_dev_endpoints.assert_called_once()


def test_batch_get_dev_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_dev_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_dev_endpoints",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get dev endpoints"):
        batch_get_dev_endpoints([], region_name=REGION)


def test_batch_get_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_jobs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_jobs([], region_name=REGION)
    mock_client.batch_get_jobs.assert_called_once()


def test_batch_get_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_jobs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get jobs"):
        batch_get_jobs([], region_name=REGION)


def test_batch_get_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.batch_get_partition.assert_called_once()


def test_batch_get_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get partition"):
        batch_get_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_batch_get_table_optimizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_table_optimizer.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_table_optimizer([], region_name=REGION)
    mock_client.batch_get_table_optimizer.assert_called_once()


def test_batch_get_table_optimizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_table_optimizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_table_optimizer",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get table optimizer"):
        batch_get_table_optimizer([], region_name=REGION)


def test_batch_get_triggers(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_triggers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_triggers([], region_name=REGION)
    mock_client.batch_get_triggers.assert_called_once()


def test_batch_get_triggers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_triggers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get triggers"):
        batch_get_triggers([], region_name=REGION)


def test_batch_get_workflows(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_workflows.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_workflows([], region_name=REGION)
    mock_client.batch_get_workflows.assert_called_once()


def test_batch_get_workflows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_workflows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_workflows",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get workflows"):
        batch_get_workflows([], region_name=REGION)


def test_batch_put_data_quality_statistic_annotation(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_data_quality_statistic_annotation.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_put_data_quality_statistic_annotation([], region_name=REGION)
    mock_client.batch_put_data_quality_statistic_annotation.assert_called_once()


def test_batch_put_data_quality_statistic_annotation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_data_quality_statistic_annotation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_put_data_quality_statistic_annotation",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch put data quality statistic annotation"):
        batch_put_data_quality_statistic_annotation([], region_name=REGION)


def test_batch_stop_job_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_job_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_stop_job_run("test-job_name", [], region_name=REGION)
    mock_client.batch_stop_job_run.assert_called_once()


def test_batch_stop_job_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_job_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_stop_job_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch stop job run"):
        batch_stop_job_run("test-job_name", [], region_name=REGION)


def test_batch_update_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    batch_update_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.batch_update_partition.assert_called_once()


def test_batch_update_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update partition"):
        batch_update_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_cancel_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_data_quality_rule_recommendation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_data_quality_rule_recommendation_run("test-run_id", region_name=REGION)
    mock_client.cancel_data_quality_rule_recommendation_run.assert_called_once()


def test_cancel_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_data_quality_rule_recommendation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_data_quality_rule_recommendation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel data quality rule recommendation run"):
        cancel_data_quality_rule_recommendation_run("test-run_id", region_name=REGION)


def test_cancel_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_data_quality_ruleset_evaluation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_data_quality_ruleset_evaluation_run("test-run_id", region_name=REGION)
    mock_client.cancel_data_quality_ruleset_evaluation_run.assert_called_once()


def test_cancel_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_data_quality_ruleset_evaluation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_data_quality_ruleset_evaluation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel data quality ruleset evaluation run"):
        cancel_data_quality_ruleset_evaluation_run("test-run_id", region_name=REGION)


def test_cancel_ml_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_ml_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_ml_task_run("test-transform_id", "test-task_run_id", region_name=REGION)
    mock_client.cancel_ml_task_run.assert_called_once()


def test_cancel_ml_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_ml_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_ml_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel ml task run"):
        cancel_ml_task_run("test-transform_id", "test-task_run_id", region_name=REGION)


def test_cancel_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_statement.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_statement("test-session_id", 1, region_name=REGION)
    mock_client.cancel_statement.assert_called_once()


def test_cancel_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_statement",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel statement"):
        cancel_statement("test-session_id", 1, region_name=REGION)


def test_check_schema_version_validity(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_schema_version_validity.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    check_schema_version_validity("test-data_format", "test-schema_definition", region_name=REGION)
    mock_client.check_schema_version_validity.assert_called_once()


def test_check_schema_version_validity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.check_schema_version_validity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "check_schema_version_validity",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to check schema version validity"):
        check_schema_version_validity("test-data_format", "test-schema_definition", region_name=REGION)


def test_create_blueprint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_blueprint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_blueprint("test-name", "test-blueprint_location", region_name=REGION)
    mock_client.create_blueprint.assert_called_once()


def test_create_blueprint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_blueprint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_blueprint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create blueprint"):
        create_blueprint("test-name", "test-blueprint_location", region_name=REGION)


def test_create_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_catalog.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_catalog("test-name", {}, region_name=REGION)
    mock_client.create_catalog.assert_called_once()


def test_create_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_catalog",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create catalog"):
        create_catalog("test-name", {}, region_name=REGION)


def test_create_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_classifier.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_classifier(region_name=REGION)
    mock_client.create_classifier.assert_called_once()


def test_create_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_classifier",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create classifier"):
        create_classifier(region_name=REGION)


def test_create_column_statistics_task_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", region_name=REGION)
    mock_client.create_column_statistics_task_settings.assert_called_once()


def test_create_column_statistics_task_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_column_statistics_task_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_column_statistics_task_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create column statistics task settings"):
        create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", region_name=REGION)


def test_create_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_connection({}, region_name=REGION)
    mock_client.create_connection.assert_called_once()


def test_create_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create connection"):
        create_connection({}, region_name=REGION)


def test_create_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_crawler("test-name", "test-role", {}, region_name=REGION)
    mock_client.create_crawler.assert_called_once()


def test_create_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create crawler"):
        create_crawler("test-name", "test-role", {}, region_name=REGION)


def test_create_custom_entity_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_entity_type.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_custom_entity_type("test-name", "test-regex_string", region_name=REGION)
    mock_client.create_custom_entity_type.assert_called_once()


def test_create_custom_entity_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_entity_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_entity_type",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom entity type"):
        create_custom_entity_type("test-name", "test-regex_string", region_name=REGION)


def test_create_data_quality_ruleset(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_quality_ruleset.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_data_quality_ruleset("test-name", "test-ruleset", region_name=REGION)
    mock_client.create_data_quality_ruleset.assert_called_once()


def test_create_data_quality_ruleset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_quality_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_quality_ruleset",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create data quality ruleset"):
        create_data_quality_ruleset("test-name", "test-ruleset", region_name=REGION)


def test_create_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_database.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_database({}, region_name=REGION)
    mock_client.create_database.assert_called_once()


def test_create_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_database",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create database"):
        create_database({}, region_name=REGION)


def test_create_dev_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dev_endpoint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_dev_endpoint("test-endpoint_name", "test-role_arn", region_name=REGION)
    mock_client.create_dev_endpoint.assert_called_once()


def test_create_dev_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dev_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dev_endpoint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dev endpoint"):
        create_dev_endpoint("test-endpoint_name", "test-role_arn", region_name=REGION)


def test_create_glue_identity_center_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_glue_identity_center_configuration("test-instance_arn", region_name=REGION)
    mock_client.create_glue_identity_center_configuration.assert_called_once()


def test_create_glue_identity_center_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_glue_identity_center_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_glue_identity_center_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create glue identity center configuration"):
        create_glue_identity_center_configuration("test-instance_arn", region_name=REGION)


def test_create_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_integration("test-integration_name", "test-source_arn", "test-target_arn", region_name=REGION)
    mock_client.create_integration.assert_called_once()


def test_create_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration"):
        create_integration("test-integration_name", "test-source_arn", "test-target_arn", region_name=REGION)


def test_create_integration_resource_property(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_resource_property.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_integration_resource_property("test-resource_arn", region_name=REGION)
    mock_client.create_integration_resource_property.assert_called_once()


def test_create_integration_resource_property_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_resource_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration_resource_property",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration resource property"):
        create_integration_resource_property("test-resource_arn", region_name=REGION)


def test_create_integration_table_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_table_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)
    mock_client.create_integration_table_properties.assert_called_once()


def test_create_integration_table_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_table_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration_table_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration table properties"):
        create_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)


def test_create_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_job.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_job("test-name", "test-role", {}, region_name=REGION)
    mock_client.create_job.assert_called_once()


def test_create_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_job",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create job"):
        create_job("test-name", "test-role", {}, region_name=REGION)


def test_create_ml_transform(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ml_transform.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_ml_transform("test-name", [], {}, "test-role", region_name=REGION)
    mock_client.create_ml_transform.assert_called_once()


def test_create_ml_transform_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ml_transform.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ml_transform",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ml transform"):
        create_ml_transform("test-name", [], {}, "test-role", region_name=REGION)


def test_create_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_partition("test-database_name", "test-table_name", {}, region_name=REGION)
    mock_client.create_partition.assert_called_once()


def test_create_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create partition"):
        create_partition("test-database_name", "test-table_name", {}, region_name=REGION)


def test_create_partition_index(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partition_index.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_partition_index("test-database_name", "test-table_name", {}, region_name=REGION)
    mock_client.create_partition_index.assert_called_once()


def test_create_partition_index_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_partition_index.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_partition_index",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create partition index"):
        create_partition_index("test-database_name", "test-table_name", {}, region_name=REGION)


def test_create_registry(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_registry.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_registry("test-registry_name", region_name=REGION)
    mock_client.create_registry.assert_called_once()


def test_create_registry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_registry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_registry",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create registry"):
        create_registry("test-registry_name", region_name=REGION)


def test_create_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_schema.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_schema("test-schema_name", "test-data_format", region_name=REGION)
    mock_client.create_schema.assert_called_once()


def test_create_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_schema",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create schema"):
        create_schema("test-schema_name", "test-data_format", region_name=REGION)


def test_create_script(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_script.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_script(region_name=REGION)
    mock_client.create_script.assert_called_once()


def test_create_script_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_script.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_script",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create script"):
        create_script(region_name=REGION)


def test_create_security_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_security_configuration("test-name", {}, region_name=REGION)
    mock_client.create_security_configuration.assert_called_once()


def test_create_security_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_security_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create security configuration"):
        create_security_configuration("test-name", {}, region_name=REGION)


def test_create_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_session("test-id", "test-role", {}, region_name=REGION)
    mock_client.create_session.assert_called_once()


def test_create_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_session",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create session"):
        create_session("test-id", "test-role", {}, region_name=REGION)


def test_create_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_table("test-database_name", region_name=REGION)
    mock_client.create_table.assert_called_once()


def test_create_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create table"):
        create_table("test-database_name", region_name=REGION)


def test_create_table_optimizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table_optimizer.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, region_name=REGION)
    mock_client.create_table_optimizer.assert_called_once()


def test_create_table_optimizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_table_optimizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_table_optimizer",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create table optimizer"):
        create_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, region_name=REGION)


def test_create_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_trigger("test-name", "test-type_value", [], region_name=REGION)
    mock_client.create_trigger.assert_called_once()


def test_create_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create trigger"):
        create_trigger("test-name", "test-type_value", [], region_name=REGION)


def test_create_usage_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_profile.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_usage_profile("test-name", {}, region_name=REGION)
    mock_client.create_usage_profile.assert_called_once()


def test_create_usage_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_usage_profile",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create usage profile"):
        create_usage_profile("test-name", {}, region_name=REGION)


def test_create_user_defined_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_defined_function.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_user_defined_function("test-database_name", {}, region_name=REGION)
    mock_client.create_user_defined_function.assert_called_once()


def test_create_user_defined_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_defined_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_defined_function",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user defined function"):
        create_user_defined_function("test-database_name", {}, region_name=REGION)


def test_create_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_workflow.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    create_workflow("test-name", region_name=REGION)
    mock_client.create_workflow.assert_called_once()


def test_create_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_workflow",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create workflow"):
        create_workflow("test-name", region_name=REGION)


def test_delete_blueprint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_blueprint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_blueprint("test-name", region_name=REGION)
    mock_client.delete_blueprint.assert_called_once()


def test_delete_blueprint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_blueprint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_blueprint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete blueprint"):
        delete_blueprint("test-name", region_name=REGION)


def test_delete_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_catalog.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_catalog("test-catalog_id", region_name=REGION)
    mock_client.delete_catalog.assert_called_once()


def test_delete_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_catalog",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete catalog"):
        delete_catalog("test-catalog_id", region_name=REGION)


def test_delete_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_classifier.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_classifier("test-name", region_name=REGION)
    mock_client.delete_classifier.assert_called_once()


def test_delete_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_classifier",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete classifier"):
        delete_classifier("test-name", region_name=REGION)


def test_delete_column_statistics_for_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_column_statistics_for_partition("test-database_name", "test-table_name", [], "test-column_name", region_name=REGION)
    mock_client.delete_column_statistics_for_partition.assert_called_once()


def test_delete_column_statistics_for_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_column_statistics_for_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete column statistics for partition"):
        delete_column_statistics_for_partition("test-database_name", "test-table_name", [], "test-column_name", region_name=REGION)


def test_delete_column_statistics_for_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", region_name=REGION)
    mock_client.delete_column_statistics_for_table.assert_called_once()


def test_delete_column_statistics_for_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_column_statistics_for_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete column statistics for table"):
        delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", region_name=REGION)


def test_delete_column_statistics_task_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)
    mock_client.delete_column_statistics_task_settings.assert_called_once()


def test_delete_column_statistics_task_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_column_statistics_task_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_column_statistics_task_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete column statistics task settings"):
        delete_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)


def test_delete_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_connection("test-connection_name", region_name=REGION)
    mock_client.delete_connection.assert_called_once()


def test_delete_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connection"):
        delete_connection("test-connection_name", region_name=REGION)


def test_delete_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_crawler("test-name", region_name=REGION)
    mock_client.delete_crawler.assert_called_once()


def test_delete_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete crawler"):
        delete_crawler("test-name", region_name=REGION)


def test_delete_custom_entity_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_entity_type.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_custom_entity_type("test-name", region_name=REGION)
    mock_client.delete_custom_entity_type.assert_called_once()


def test_delete_custom_entity_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_entity_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_entity_type",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom entity type"):
        delete_custom_entity_type("test-name", region_name=REGION)


def test_delete_data_quality_ruleset(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_quality_ruleset.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_data_quality_ruleset("test-name", region_name=REGION)
    mock_client.delete_data_quality_ruleset.assert_called_once()


def test_delete_data_quality_ruleset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_quality_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_quality_ruleset",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data quality ruleset"):
        delete_data_quality_ruleset("test-name", region_name=REGION)


def test_delete_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_database.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_database("test-name", region_name=REGION)
    mock_client.delete_database.assert_called_once()


def test_delete_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_database",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete database"):
        delete_database("test-name", region_name=REGION)


def test_delete_dev_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dev_endpoint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_dev_endpoint("test-endpoint_name", region_name=REGION)
    mock_client.delete_dev_endpoint.assert_called_once()


def test_delete_dev_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dev_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dev_endpoint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dev endpoint"):
        delete_dev_endpoint("test-endpoint_name", region_name=REGION)


def test_delete_glue_identity_center_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_glue_identity_center_configuration(region_name=REGION)
    mock_client.delete_glue_identity_center_configuration.assert_called_once()


def test_delete_glue_identity_center_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_glue_identity_center_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_glue_identity_center_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete glue identity center configuration"):
        delete_glue_identity_center_configuration(region_name=REGION)


def test_delete_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_integration("test-integration_identifier", region_name=REGION)
    mock_client.delete_integration.assert_called_once()


def test_delete_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete integration"):
        delete_integration("test-integration_identifier", region_name=REGION)


def test_delete_integration_table_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_table_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)
    mock_client.delete_integration_table_properties.assert_called_once()


def test_delete_integration_table_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_table_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration_table_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete integration table properties"):
        delete_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)


def test_delete_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_job.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_job("test-job_name", region_name=REGION)
    mock_client.delete_job.assert_called_once()


def test_delete_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete job"):
        delete_job("test-job_name", region_name=REGION)


def test_delete_ml_transform(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ml_transform.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_ml_transform("test-transform_id", region_name=REGION)
    mock_client.delete_ml_transform.assert_called_once()


def test_delete_ml_transform_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ml_transform.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ml_transform",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ml transform"):
        delete_ml_transform("test-transform_id", region_name=REGION)


def test_delete_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.delete_partition.assert_called_once()


def test_delete_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete partition"):
        delete_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_delete_partition_index(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partition_index.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_partition_index("test-database_name", "test-table_name", "test-index_name", region_name=REGION)
    mock_client.delete_partition_index.assert_called_once()


def test_delete_partition_index_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partition_index.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_partition_index",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete partition index"):
        delete_partition_index("test-database_name", "test-table_name", "test-index_name", region_name=REGION)


def test_delete_registry(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_registry.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_registry({}, region_name=REGION)
    mock_client.delete_registry.assert_called_once()


def test_delete_registry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_registry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_registry",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete registry"):
        delete_registry({}, region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_resource_policy(region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy(region_name=REGION)


def test_delete_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_schema({}, region_name=REGION)
    mock_client.delete_schema.assert_called_once()


def test_delete_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_schema",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete schema"):
        delete_schema({}, region_name=REGION)


def test_delete_schema_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema_versions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_schema_versions({}, "test-versions", region_name=REGION)
    mock_client.delete_schema_versions.assert_called_once()


def test_delete_schema_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_schema_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_schema_versions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete schema versions"):
        delete_schema_versions({}, "test-versions", region_name=REGION)


def test_delete_security_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_security_configuration("test-name", region_name=REGION)
    mock_client.delete_security_configuration.assert_called_once()


def test_delete_security_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_security_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete security configuration"):
        delete_security_configuration("test-name", region_name=REGION)


def test_delete_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_session.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_session("test-id", region_name=REGION)
    mock_client.delete_session.assert_called_once()


def test_delete_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_session",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete session"):
        delete_session("test-id", region_name=REGION)


def test_delete_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_table("test-database_name", "test-name", region_name=REGION)
    mock_client.delete_table.assert_called_once()


def test_delete_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete table"):
        delete_table("test-database_name", "test-name", region_name=REGION)


def test_delete_table_optimizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table_optimizer.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)
    mock_client.delete_table_optimizer.assert_called_once()


def test_delete_table_optimizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table_optimizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_table_optimizer",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete table optimizer"):
        delete_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)


def test_delete_table_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table_version.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_table_version("test-database_name", "test-table_name", "test-version_id", region_name=REGION)
    mock_client.delete_table_version.assert_called_once()


def test_delete_table_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_table_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_table_version",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete table version"):
        delete_table_version("test-database_name", "test-table_name", "test-version_id", region_name=REGION)


def test_delete_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_trigger("test-name", region_name=REGION)
    mock_client.delete_trigger.assert_called_once()


def test_delete_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete trigger"):
        delete_trigger("test-name", region_name=REGION)


def test_delete_usage_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_profile.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_usage_profile("test-name", region_name=REGION)
    mock_client.delete_usage_profile.assert_called_once()


def test_delete_usage_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_usage_profile",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete usage profile"):
        delete_usage_profile("test-name", region_name=REGION)


def test_delete_user_defined_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_defined_function.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user_defined_function("test-database_name", "test-function_name", region_name=REGION)
    mock_client.delete_user_defined_function.assert_called_once()


def test_delete_user_defined_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_defined_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_defined_function",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user defined function"):
        delete_user_defined_function("test-database_name", "test-function_name", region_name=REGION)


def test_delete_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_workflow.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    delete_workflow("test-name", region_name=REGION)
    mock_client.delete_workflow.assert_called_once()


def test_delete_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_workflow",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete workflow"):
        delete_workflow("test-name", region_name=REGION)


def test_describe_connection_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connection_type.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    describe_connection_type("test-connection_type", region_name=REGION)
    mock_client.describe_connection_type.assert_called_once()


def test_describe_connection_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_connection_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_connection_type",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe connection type"):
        describe_connection_type("test-connection_type", region_name=REGION)


def test_describe_entity(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entity.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    describe_entity("test-connection_name", "test-entity_name", region_name=REGION)
    mock_client.describe_entity.assert_called_once()


def test_describe_entity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_entity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_entity",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe entity"):
        describe_entity("test-connection_name", "test-entity_name", region_name=REGION)


def test_describe_inbound_integrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    describe_inbound_integrations(region_name=REGION)
    mock_client.describe_inbound_integrations.assert_called_once()


def test_describe_inbound_integrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_inbound_integrations",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe inbound integrations"):
        describe_inbound_integrations(region_name=REGION)


def test_describe_integrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    describe_integrations(region_name=REGION)
    mock_client.describe_integrations.assert_called_once()


def test_describe_integrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_integrations",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe integrations"):
        describe_integrations(region_name=REGION)


def test_get_blueprint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_blueprint("test-name", region_name=REGION)
    mock_client.get_blueprint.assert_called_once()


def test_get_blueprint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_blueprint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get blueprint"):
        get_blueprint("test-name", region_name=REGION)


def test_get_blueprint_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_blueprint_run("test-blueprint_name", "test-run_id", region_name=REGION)
    mock_client.get_blueprint_run.assert_called_once()


def test_get_blueprint_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_blueprint_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get blueprint run"):
        get_blueprint_run("test-blueprint_name", "test-run_id", region_name=REGION)


def test_get_blueprint_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_blueprint_runs("test-blueprint_name", region_name=REGION)
    mock_client.get_blueprint_runs.assert_called_once()


def test_get_blueprint_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_blueprint_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_blueprint_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get blueprint runs"):
        get_blueprint_runs("test-blueprint_name", region_name=REGION)


def test_get_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalog.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_catalog("test-catalog_id", region_name=REGION)
    mock_client.get_catalog.assert_called_once()


def test_get_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_catalog",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get catalog"):
        get_catalog("test-catalog_id", region_name=REGION)


def test_get_catalog_import_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalog_import_status.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_catalog_import_status(region_name=REGION)
    mock_client.get_catalog_import_status.assert_called_once()


def test_get_catalog_import_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalog_import_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_catalog_import_status",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get catalog import status"):
        get_catalog_import_status(region_name=REGION)


def test_get_catalogs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalogs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_catalogs(region_name=REGION)
    mock_client.get_catalogs.assert_called_once()


def test_get_catalogs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_catalogs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_catalogs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get catalogs"):
        get_catalogs(region_name=REGION)


def test_get_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_classifier.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_classifier("test-name", region_name=REGION)
    mock_client.get_classifier.assert_called_once()


def test_get_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_classifier",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get classifier"):
        get_classifier("test-name", region_name=REGION)


def test_get_classifiers(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_classifiers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_classifiers(region_name=REGION)
    mock_client.get_classifiers.assert_called_once()


def test_get_classifiers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_classifiers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_classifiers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get classifiers"):
        get_classifiers(region_name=REGION)


def test_get_column_statistics_for_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_column_statistics_for_partition("test-database_name", "test-table_name", [], [], region_name=REGION)
    mock_client.get_column_statistics_for_partition.assert_called_once()


def test_get_column_statistics_for_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_column_statistics_for_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get column statistics for partition"):
        get_column_statistics_for_partition("test-database_name", "test-table_name", [], [], region_name=REGION)


def test_get_column_statistics_for_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_column_statistics_for_table("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.get_column_statistics_for_table.assert_called_once()


def test_get_column_statistics_for_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_column_statistics_for_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get column statistics for table"):
        get_column_statistics_for_table("test-database_name", "test-table_name", [], region_name=REGION)


def test_get_column_statistics_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_column_statistics_task_run("test-column_statistics_task_run_id", region_name=REGION)
    mock_client.get_column_statistics_task_run.assert_called_once()


def test_get_column_statistics_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_column_statistics_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get column statistics task run"):
        get_column_statistics_task_run("test-column_statistics_task_run_id", region_name=REGION)


def test_get_column_statistics_task_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_column_statistics_task_runs("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_column_statistics_task_runs.assert_called_once()


def test_get_column_statistics_task_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_column_statistics_task_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get column statistics task runs"):
        get_column_statistics_task_runs("test-database_name", "test-table_name", region_name=REGION)


def test_get_column_statistics_task_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_column_statistics_task_settings.assert_called_once()


def test_get_column_statistics_task_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_column_statistics_task_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get column statistics task settings"):
        get_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)


def test_get_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_connection("test-name", region_name=REGION)
    mock_client.get_connection.assert_called_once()


def test_get_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connection"):
        get_connection("test-name", region_name=REGION)


def test_get_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connections.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_connections(region_name=REGION)
    mock_client.get_connections.assert_called_once()


def test_get_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connections",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connections"):
        get_connections(region_name=REGION)


def test_get_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_crawler("test-name", region_name=REGION)
    mock_client.get_crawler.assert_called_once()


def test_get_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get crawler"):
        get_crawler("test-name", region_name=REGION)


def test_get_crawler_metrics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawler_metrics.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_crawler_metrics(region_name=REGION)
    mock_client.get_crawler_metrics.assert_called_once()


def test_get_crawler_metrics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawler_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_crawler_metrics",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get crawler metrics"):
        get_crawler_metrics(region_name=REGION)


def test_get_crawlers(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawlers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_crawlers(region_name=REGION)
    mock_client.get_crawlers.assert_called_once()


def test_get_crawlers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_crawlers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_crawlers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get crawlers"):
        get_crawlers(region_name=REGION)


def test_get_custom_entity_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_entity_type.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_custom_entity_type("test-name", region_name=REGION)
    mock_client.get_custom_entity_type.assert_called_once()


def test_get_custom_entity_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_entity_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_entity_type",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get custom entity type"):
        get_custom_entity_type("test-name", region_name=REGION)


def test_get_data_catalog_encryption_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_catalog_encryption_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_catalog_encryption_settings(region_name=REGION)
    mock_client.get_data_catalog_encryption_settings.assert_called_once()


def test_get_data_catalog_encryption_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_catalog_encryption_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_catalog_encryption_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data catalog encryption settings"):
        get_data_catalog_encryption_settings(region_name=REGION)


def test_get_data_quality_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_model.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_model("test-profile_id", region_name=REGION)
    mock_client.get_data_quality_model.assert_called_once()


def test_get_data_quality_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_model",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality model"):
        get_data_quality_model("test-profile_id", region_name=REGION)


def test_get_data_quality_model_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_model_result.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_model_result("test-statistic_id", "test-profile_id", region_name=REGION)
    mock_client.get_data_quality_model_result.assert_called_once()


def test_get_data_quality_model_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_model_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_model_result",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality model result"):
        get_data_quality_model_result("test-statistic_id", "test-profile_id", region_name=REGION)


def test_get_data_quality_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_result.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_result("test-result_id", region_name=REGION)
    mock_client.get_data_quality_result.assert_called_once()


def test_get_data_quality_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_result",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality result"):
        get_data_quality_result("test-result_id", region_name=REGION)


def test_get_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_rule_recommendation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_rule_recommendation_run("test-run_id", region_name=REGION)
    mock_client.get_data_quality_rule_recommendation_run.assert_called_once()


def test_get_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_rule_recommendation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_rule_recommendation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality rule recommendation run"):
        get_data_quality_rule_recommendation_run("test-run_id", region_name=REGION)


def test_get_data_quality_ruleset(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_ruleset.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_ruleset("test-name", region_name=REGION)
    mock_client.get_data_quality_ruleset.assert_called_once()


def test_get_data_quality_ruleset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_ruleset",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality ruleset"):
        get_data_quality_ruleset("test-name", region_name=REGION)


def test_get_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_ruleset_evaluation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_quality_ruleset_evaluation_run("test-run_id", region_name=REGION)
    mock_client.get_data_quality_ruleset_evaluation_run.assert_called_once()


def test_get_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_quality_ruleset_evaluation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_quality_ruleset_evaluation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data quality ruleset evaluation run"):
        get_data_quality_ruleset_evaluation_run("test-run_id", region_name=REGION)


def test_get_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_database.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_database("test-name", region_name=REGION)
    mock_client.get_database.assert_called_once()


def test_get_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_database",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get database"):
        get_database("test-name", region_name=REGION)


def test_get_databases(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_databases.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_databases(region_name=REGION)
    mock_client.get_databases.assert_called_once()


def test_get_databases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_databases",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get databases"):
        get_databases(region_name=REGION)


def test_get_dataflow_graph(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dataflow_graph.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_dataflow_graph(region_name=REGION)
    mock_client.get_dataflow_graph.assert_called_once()


def test_get_dataflow_graph_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dataflow_graph.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dataflow_graph",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dataflow graph"):
        get_dataflow_graph(region_name=REGION)


def test_get_dev_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dev_endpoint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_dev_endpoint("test-endpoint_name", region_name=REGION)
    mock_client.get_dev_endpoint.assert_called_once()


def test_get_dev_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dev_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dev_endpoint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dev endpoint"):
        get_dev_endpoint("test-endpoint_name", region_name=REGION)


def test_get_dev_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dev_endpoints.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_dev_endpoints(region_name=REGION)
    mock_client.get_dev_endpoints.assert_called_once()


def test_get_dev_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dev_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dev_endpoints",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dev endpoints"):
        get_dev_endpoints(region_name=REGION)


def test_get_entity_records(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_entity_records.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_entity_records("test-entity_name", 1, region_name=REGION)
    mock_client.get_entity_records.assert_called_once()


def test_get_entity_records_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_entity_records.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_entity_records",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get entity records"):
        get_entity_records("test-entity_name", 1, region_name=REGION)


def test_get_glue_identity_center_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_glue_identity_center_configuration(region_name=REGION)
    mock_client.get_glue_identity_center_configuration.assert_called_once()


def test_get_glue_identity_center_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_glue_identity_center_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_glue_identity_center_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get glue identity center configuration"):
        get_glue_identity_center_configuration(region_name=REGION)


def test_get_integration_resource_property(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_resource_property.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_integration_resource_property("test-resource_arn", region_name=REGION)
    mock_client.get_integration_resource_property.assert_called_once()


def test_get_integration_resource_property_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_resource_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_integration_resource_property",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get integration resource property"):
        get_integration_resource_property("test-resource_arn", region_name=REGION)


def test_get_integration_table_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_table_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)
    mock_client.get_integration_table_properties.assert_called_once()


def test_get_integration_table_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_table_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_integration_table_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get integration table properties"):
        get_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)


def test_get_job_bookmark(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_bookmark.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_job_bookmark("test-job_name", region_name=REGION)
    mock_client.get_job_bookmark.assert_called_once()


def test_get_job_bookmark_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_bookmark.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_job_bookmark",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get job bookmark"):
        get_job_bookmark("test-job_name", region_name=REGION)


def test_get_job_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_job_runs("test-job_name", region_name=REGION)
    mock_client.get_job_runs.assert_called_once()


def test_get_job_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_job_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_job_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get job runs"):
        get_job_runs("test-job_name", region_name=REGION)


def test_get_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_jobs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_jobs(region_name=REGION)
    mock_client.get_jobs.assert_called_once()


def test_get_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_jobs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get jobs"):
        get_jobs(region_name=REGION)


def test_get_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_mapping.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_mapping({}, region_name=REGION)
    mock_client.get_mapping.assert_called_once()


def test_get_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_mapping",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get mapping"):
        get_mapping({}, region_name=REGION)


def test_get_ml_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_ml_task_run("test-transform_id", "test-task_run_id", region_name=REGION)
    mock_client.get_ml_task_run.assert_called_once()


def test_get_ml_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ml_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ml task run"):
        get_ml_task_run("test-transform_id", "test-task_run_id", region_name=REGION)


def test_get_ml_task_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_task_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_ml_task_runs("test-transform_id", region_name=REGION)
    mock_client.get_ml_task_runs.assert_called_once()


def test_get_ml_task_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_task_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ml_task_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ml task runs"):
        get_ml_task_runs("test-transform_id", region_name=REGION)


def test_get_ml_transform(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_transform.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_ml_transform("test-transform_id", region_name=REGION)
    mock_client.get_ml_transform.assert_called_once()


def test_get_ml_transform_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_transform.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ml_transform",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ml transform"):
        get_ml_transform("test-transform_id", region_name=REGION)


def test_get_ml_transforms(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_transforms.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_ml_transforms(region_name=REGION)
    mock_client.get_ml_transforms.assert_called_once()


def test_get_ml_transforms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ml_transforms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ml_transforms",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ml transforms"):
        get_ml_transforms(region_name=REGION)


def test_get_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_partition("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.get_partition.assert_called_once()


def test_get_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get partition"):
        get_partition("test-database_name", "test-table_name", [], region_name=REGION)


def test_get_partition_indexes(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partition_indexes.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_partition_indexes("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_partition_indexes.assert_called_once()


def test_get_partition_indexes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partition_indexes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_partition_indexes",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get partition indexes"):
        get_partition_indexes("test-database_name", "test-table_name", region_name=REGION)


def test_get_partitions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partitions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_partitions("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_partitions.assert_called_once()


def test_get_partitions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_partitions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_partitions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get partitions"):
        get_partitions("test-database_name", "test-table_name", region_name=REGION)


def test_get_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_plan.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_plan([], {}, region_name=REGION)
    mock_client.get_plan.assert_called_once()


def test_get_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_plan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_plan",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get plan"):
        get_plan([], {}, region_name=REGION)


def test_get_registry(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_registry({}, region_name=REGION)
    mock_client.get_registry.assert_called_once()


def test_get_registry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_registry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_registry",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get registry"):
        get_registry({}, region_name=REGION)


def test_get_resource_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policies.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_resource_policies(region_name=REGION)
    mock_client.get_resource_policies.assert_called_once()


def test_get_resource_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policies",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policies"):
        get_resource_policies(region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_resource_policy(region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy(region_name=REGION)


def test_get_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_schema({}, region_name=REGION)
    mock_client.get_schema.assert_called_once()


def test_get_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_schema",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get schema"):
        get_schema({}, region_name=REGION)


def test_get_schema_by_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_by_definition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_schema_by_definition({}, "test-schema_definition", region_name=REGION)
    mock_client.get_schema_by_definition.assert_called_once()


def test_get_schema_by_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_by_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_schema_by_definition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get schema by definition"):
        get_schema_by_definition({}, "test-schema_definition", region_name=REGION)


def test_get_schema_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_version.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_schema_version(region_name=REGION)
    mock_client.get_schema_version.assert_called_once()


def test_get_schema_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_schema_version",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get schema version"):
        get_schema_version(region_name=REGION)


def test_get_schema_versions_diff(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_versions_diff.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_schema_versions_diff({}, {}, {}, "test-schema_diff_type", region_name=REGION)
    mock_client.get_schema_versions_diff.assert_called_once()


def test_get_schema_versions_diff_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_schema_versions_diff.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_schema_versions_diff",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get schema versions diff"):
        get_schema_versions_diff({}, {}, {}, "test-schema_diff_type", region_name=REGION)


def test_get_security_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_security_configuration("test-name", region_name=REGION)
    mock_client.get_security_configuration.assert_called_once()


def test_get_security_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_security_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get security configuration"):
        get_security_configuration("test-name", region_name=REGION)


def test_get_security_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_configurations.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_security_configurations(region_name=REGION)
    mock_client.get_security_configurations.assert_called_once()


def test_get_security_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_security_configurations",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get security configurations"):
        get_security_configurations(region_name=REGION)


def test_get_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_session("test-id", region_name=REGION)
    mock_client.get_session.assert_called_once()


def test_get_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session"):
        get_session("test-id", region_name=REGION)


def test_get_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_statement.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_statement("test-session_id", 1, region_name=REGION)
    mock_client.get_statement.assert_called_once()


def test_get_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_statement",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get statement"):
        get_statement("test-session_id", 1, region_name=REGION)


def test_get_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_table("test-database_name", "test-name", region_name=REGION)
    mock_client.get_table.assert_called_once()


def test_get_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table"):
        get_table("test-database_name", "test-name", region_name=REGION)


def test_get_table_optimizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_optimizer.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)
    mock_client.get_table_optimizer.assert_called_once()


def test_get_table_optimizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_optimizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_optimizer",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table optimizer"):
        get_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)


def test_get_table_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_version.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_table_version("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_table_version.assert_called_once()


def test_get_table_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_version",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table version"):
        get_table_version("test-database_name", "test-table_name", region_name=REGION)


def test_get_table_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_versions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_table_versions("test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_table_versions.assert_called_once()


def test_get_table_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_versions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table versions"):
        get_table_versions("test-database_name", "test-table_name", region_name=REGION)


def test_get_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tables.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_tables("test-database_name", region_name=REGION)
    mock_client.get_tables.assert_called_once()


def test_get_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_tables",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get tables"):
        get_tables("test-database_name", region_name=REGION)


def test_get_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tags.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_tags("test-resource_arn", region_name=REGION)
    mock_client.get_tags.assert_called_once()


def test_get_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_tags",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get tags"):
        get_tags("test-resource_arn", region_name=REGION)


def test_get_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_trigger("test-name", region_name=REGION)
    mock_client.get_trigger.assert_called_once()


def test_get_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get trigger"):
        get_trigger("test-name", region_name=REGION)


def test_get_triggers(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_triggers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_triggers(region_name=REGION)
    mock_client.get_triggers.assert_called_once()


def test_get_triggers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_triggers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get triggers"):
        get_triggers(region_name=REGION)


def test_get_unfiltered_partition_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_partition_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", [], [], region_name=REGION)
    mock_client.get_unfiltered_partition_metadata.assert_called_once()


def test_get_unfiltered_partition_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_partition_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_unfiltered_partition_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get unfiltered partition metadata"):
        get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", [], [], region_name=REGION)


def test_get_unfiltered_partitions_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_partitions_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.get_unfiltered_partitions_metadata.assert_called_once()


def test_get_unfiltered_partitions_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_partitions_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_unfiltered_partitions_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get unfiltered partitions metadata"):
        get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", [], region_name=REGION)


def test_get_unfiltered_table_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_table_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", [], region_name=REGION)
    mock_client.get_unfiltered_table_metadata.assert_called_once()


def test_get_unfiltered_table_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_unfiltered_table_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_unfiltered_table_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get unfiltered table metadata"):
        get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", [], region_name=REGION)


def test_get_usage_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_profile.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_usage_profile("test-name", region_name=REGION)
    mock_client.get_usage_profile.assert_called_once()


def test_get_usage_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_profile",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get usage profile"):
        get_usage_profile("test-name", region_name=REGION)


def test_get_user_defined_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_defined_function.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_user_defined_function("test-database_name", "test-function_name", region_name=REGION)
    mock_client.get_user_defined_function.assert_called_once()


def test_get_user_defined_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_defined_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_defined_function",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user defined function"):
        get_user_defined_function("test-database_name", "test-function_name", region_name=REGION)


def test_get_user_defined_functions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_defined_functions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_user_defined_functions("test-pattern", region_name=REGION)
    mock_client.get_user_defined_functions.assert_called_once()


def test_get_user_defined_functions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_defined_functions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_defined_functions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user defined functions"):
        get_user_defined_functions("test-pattern", region_name=REGION)


def test_get_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_workflow("test-name", region_name=REGION)
    mock_client.get_workflow.assert_called_once()


def test_get_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_workflow",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get workflow"):
        get_workflow("test-name", region_name=REGION)


def test_get_workflow_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_workflow_run("test-name", "test-run_id", region_name=REGION)
    mock_client.get_workflow_run.assert_called_once()


def test_get_workflow_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_workflow_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get workflow run"):
        get_workflow_run("test-name", "test-run_id", region_name=REGION)


def test_get_workflow_run_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_run_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_workflow_run_properties("test-name", "test-run_id", region_name=REGION)
    mock_client.get_workflow_run_properties.assert_called_once()


def test_get_workflow_run_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_run_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_workflow_run_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get workflow run properties"):
        get_workflow_run_properties("test-name", "test-run_id", region_name=REGION)


def test_get_workflow_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    get_workflow_runs("test-name", region_name=REGION)
    mock_client.get_workflow_runs.assert_called_once()


def test_get_workflow_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_workflow_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_workflow_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get workflow runs"):
        get_workflow_runs("test-name", region_name=REGION)


def test_import_catalog_to_glue(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_catalog_to_glue.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    import_catalog_to_glue(region_name=REGION)
    mock_client.import_catalog_to_glue.assert_called_once()


def test_import_catalog_to_glue_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_catalog_to_glue.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_catalog_to_glue",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import catalog to glue"):
        import_catalog_to_glue(region_name=REGION)


def test_list_blueprints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_blueprints.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_blueprints(region_name=REGION)
    mock_client.list_blueprints.assert_called_once()


def test_list_blueprints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_blueprints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_blueprints",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list blueprints"):
        list_blueprints(region_name=REGION)


def test_list_column_statistics_task_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_column_statistics_task_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_column_statistics_task_runs(region_name=REGION)
    mock_client.list_column_statistics_task_runs.assert_called_once()


def test_list_column_statistics_task_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_column_statistics_task_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_column_statistics_task_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list column statistics task runs"):
        list_column_statistics_task_runs(region_name=REGION)


def test_list_connection_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connection_types.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_connection_types(region_name=REGION)
    mock_client.list_connection_types.assert_called_once()


def test_list_connection_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connection_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_connection_types",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list connection types"):
        list_connection_types(region_name=REGION)


def test_list_crawlers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_crawlers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_crawlers(region_name=REGION)
    mock_client.list_crawlers.assert_called_once()


def test_list_crawlers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_crawlers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_crawlers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list crawlers"):
        list_crawlers(region_name=REGION)


def test_list_crawls(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_crawls.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_crawls("test-crawler_name", region_name=REGION)
    mock_client.list_crawls.assert_called_once()


def test_list_crawls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_crawls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_crawls",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list crawls"):
        list_crawls("test-crawler_name", region_name=REGION)


def test_list_custom_entity_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_entity_types.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_custom_entity_types(region_name=REGION)
    mock_client.list_custom_entity_types.assert_called_once()


def test_list_custom_entity_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_entity_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_entity_types",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list custom entity types"):
        list_custom_entity_types(region_name=REGION)


def test_list_data_quality_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_results.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_results(region_name=REGION)
    mock_client.list_data_quality_results.assert_called_once()


def test_list_data_quality_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_results",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality results"):
        list_data_quality_results(region_name=REGION)


def test_list_data_quality_rule_recommendation_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_rule_recommendation_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_rule_recommendation_runs(region_name=REGION)
    mock_client.list_data_quality_rule_recommendation_runs.assert_called_once()


def test_list_data_quality_rule_recommendation_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_rule_recommendation_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_rule_recommendation_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality rule recommendation runs"):
        list_data_quality_rule_recommendation_runs(region_name=REGION)


def test_list_data_quality_ruleset_evaluation_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_ruleset_evaluation_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_ruleset_evaluation_runs(region_name=REGION)
    mock_client.list_data_quality_ruleset_evaluation_runs.assert_called_once()


def test_list_data_quality_ruleset_evaluation_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_ruleset_evaluation_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_ruleset_evaluation_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality ruleset evaluation runs"):
        list_data_quality_ruleset_evaluation_runs(region_name=REGION)


def test_list_data_quality_rulesets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_rulesets.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_rulesets(region_name=REGION)
    mock_client.list_data_quality_rulesets.assert_called_once()


def test_list_data_quality_rulesets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_rulesets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_rulesets",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality rulesets"):
        list_data_quality_rulesets(region_name=REGION)


def test_list_data_quality_statistic_annotations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_statistic_annotations.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_statistic_annotations(region_name=REGION)
    mock_client.list_data_quality_statistic_annotations.assert_called_once()


def test_list_data_quality_statistic_annotations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_statistic_annotations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_statistic_annotations",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality statistic annotations"):
        list_data_quality_statistic_annotations(region_name=REGION)


def test_list_data_quality_statistics(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_statistics.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_quality_statistics(region_name=REGION)
    mock_client.list_data_quality_statistics.assert_called_once()


def test_list_data_quality_statistics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_quality_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_quality_statistics",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data quality statistics"):
        list_data_quality_statistics(region_name=REGION)


def test_list_dev_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dev_endpoints.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_dev_endpoints(region_name=REGION)
    mock_client.list_dev_endpoints.assert_called_once()


def test_list_dev_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dev_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dev_endpoints",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dev endpoints"):
        list_dev_endpoints(region_name=REGION)


def test_list_entities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_entities(region_name=REGION)
    mock_client.list_entities.assert_called_once()


def test_list_entities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_entities",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list entities"):
        list_entities(region_name=REGION)


def test_list_ml_transforms(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ml_transforms.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_ml_transforms(region_name=REGION)
    mock_client.list_ml_transforms.assert_called_once()


def test_list_ml_transforms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ml_transforms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ml_transforms",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ml transforms"):
        list_ml_transforms(region_name=REGION)


def test_list_registries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_registries.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_registries(region_name=REGION)
    mock_client.list_registries.assert_called_once()


def test_list_registries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_registries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_registries",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list registries"):
        list_registries(region_name=REGION)


def test_list_schema_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schema_versions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_schema_versions({}, region_name=REGION)
    mock_client.list_schema_versions.assert_called_once()


def test_list_schema_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schema_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_schema_versions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list schema versions"):
        list_schema_versions({}, region_name=REGION)


def test_list_schemas(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_schemas(region_name=REGION)
    mock_client.list_schemas.assert_called_once()


def test_list_schemas_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_schemas",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list schemas"):
        list_schemas(region_name=REGION)


def test_list_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_sessions(region_name=REGION)
    mock_client.list_sessions.assert_called_once()


def test_list_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sessions",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list sessions"):
        list_sessions(region_name=REGION)


def test_list_statements(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_statements.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_statements("test-session_id", region_name=REGION)
    mock_client.list_statements.assert_called_once()


def test_list_statements_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_statements.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_statements",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list statements"):
        list_statements("test-session_id", region_name=REGION)


def test_list_table_optimizer_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_optimizer_runs.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)
    mock_client.list_table_optimizer_runs.assert_called_once()


def test_list_table_optimizer_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_optimizer_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_table_optimizer_runs",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list table optimizer runs"):
        list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", region_name=REGION)


def test_list_triggers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_triggers.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_triggers(region_name=REGION)
    mock_client.list_triggers.assert_called_once()


def test_list_triggers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_triggers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_triggers",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list triggers"):
        list_triggers(region_name=REGION)


def test_list_usage_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_usage_profiles.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_usage_profiles(region_name=REGION)
    mock_client.list_usage_profiles.assert_called_once()


def test_list_usage_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_usage_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_usage_profiles",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list usage profiles"):
        list_usage_profiles(region_name=REGION)


def test_list_workflows(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_workflows.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    list_workflows(region_name=REGION)
    mock_client.list_workflows.assert_called_once()


def test_list_workflows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_workflows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_workflows",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list workflows"):
        list_workflows(region_name=REGION)


def test_modify_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_identifier", region_name=REGION)
    mock_client.modify_integration.assert_called_once()


def test_modify_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_integration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify integration"):
        modify_integration("test-integration_identifier", region_name=REGION)


def test_put_data_catalog_encryption_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_catalog_encryption_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    put_data_catalog_encryption_settings({}, region_name=REGION)
    mock_client.put_data_catalog_encryption_settings.assert_called_once()


def test_put_data_catalog_encryption_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_catalog_encryption_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_data_catalog_encryption_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put data catalog encryption settings"):
        put_data_catalog_encryption_settings({}, region_name=REGION)


def test_put_data_quality_profile_annotation(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_quality_profile_annotation.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    put_data_quality_profile_annotation("test-profile_id", "test-inclusion_annotation", region_name=REGION)
    mock_client.put_data_quality_profile_annotation.assert_called_once()


def test_put_data_quality_profile_annotation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_quality_profile_annotation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_data_quality_profile_annotation",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put data quality profile annotation"):
        put_data_quality_profile_annotation("test-profile_id", "test-inclusion_annotation", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-policy_in_json", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-policy_in_json", region_name=REGION)


def test_put_schema_version_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_schema_version_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    put_schema_version_metadata({}, region_name=REGION)
    mock_client.put_schema_version_metadata.assert_called_once()


def test_put_schema_version_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_schema_version_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_schema_version_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put schema version metadata"):
        put_schema_version_metadata({}, region_name=REGION)


def test_put_workflow_run_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_workflow_run_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    put_workflow_run_properties("test-name", "test-run_id", {}, region_name=REGION)
    mock_client.put_workflow_run_properties.assert_called_once()


def test_put_workflow_run_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_workflow_run_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_workflow_run_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put workflow run properties"):
        put_workflow_run_properties("test-name", "test-run_id", {}, region_name=REGION)


def test_query_schema_version_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.query_schema_version_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    query_schema_version_metadata(region_name=REGION)
    mock_client.query_schema_version_metadata.assert_called_once()


def test_query_schema_version_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.query_schema_version_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "query_schema_version_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to query schema version metadata"):
        query_schema_version_metadata(region_name=REGION)


def test_register_schema_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_schema_version.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    register_schema_version({}, "test-schema_definition", region_name=REGION)
    mock_client.register_schema_version.assert_called_once()


def test_register_schema_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_schema_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_schema_version",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register schema version"):
        register_schema_version({}, "test-schema_definition", region_name=REGION)


def test_remove_schema_version_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_schema_version_metadata.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    remove_schema_version_metadata({}, region_name=REGION)
    mock_client.remove_schema_version_metadata.assert_called_once()


def test_remove_schema_version_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_schema_version_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_schema_version_metadata",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove schema version metadata"):
        remove_schema_version_metadata({}, region_name=REGION)


def test_reset_job_bookmark(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_job_bookmark.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    reset_job_bookmark("test-job_name", region_name=REGION)
    mock_client.reset_job_bookmark.assert_called_once()


def test_reset_job_bookmark_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_job_bookmark.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_job_bookmark",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset job bookmark"):
        reset_job_bookmark("test-job_name", region_name=REGION)


def test_resume_workflow_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_workflow_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    resume_workflow_run("test-name", "test-run_id", [], region_name=REGION)
    mock_client.resume_workflow_run.assert_called_once()


def test_resume_workflow_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_workflow_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_workflow_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume workflow run"):
        resume_workflow_run("test-name", "test-run_id", [], region_name=REGION)


def test_run_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    run_connection(region_name=REGION)
    mock_client.test_connection.assert_called_once()


def test_run_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run connection"):
        run_connection(region_name=REGION)


def test_run_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_statement.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    run_statement("test-session_id", "test-code", region_name=REGION)
    mock_client.run_statement.assert_called_once()


def test_run_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_statement",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run statement"):
        run_statement("test-session_id", "test-code", region_name=REGION)


def test_search_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_tables.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    search_tables(region_name=REGION)
    mock_client.search_tables.assert_called_once()


def test_search_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_tables",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search tables"):
        search_tables(region_name=REGION)


def test_start_blueprint_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_blueprint_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_blueprint_run("test-blueprint_name", "test-role_arn", region_name=REGION)
    mock_client.start_blueprint_run.assert_called_once()


def test_start_blueprint_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_blueprint_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_blueprint_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start blueprint run"):
        start_blueprint_run("test-blueprint_name", "test-role_arn", region_name=REGION)


def test_start_column_statistics_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_column_statistics_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", region_name=REGION)
    mock_client.start_column_statistics_task_run.assert_called_once()


def test_start_column_statistics_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_column_statistics_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_column_statistics_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start column statistics task run"):
        start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", region_name=REGION)


def test_start_column_statistics_task_run_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_column_statistics_task_run_schedule.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_column_statistics_task_run_schedule("test-database_name", "test-table_name", region_name=REGION)
    mock_client.start_column_statistics_task_run_schedule.assert_called_once()


def test_start_column_statistics_task_run_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_column_statistics_task_run_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_column_statistics_task_run_schedule",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start column statistics task run schedule"):
        start_column_statistics_task_run_schedule("test-database_name", "test-table_name", region_name=REGION)


def test_start_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_crawler("test-name", region_name=REGION)
    mock_client.start_crawler.assert_called_once()


def test_start_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start crawler"):
        start_crawler("test-name", region_name=REGION)


def test_start_crawler_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_crawler_schedule.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_crawler_schedule("test-crawler_name", region_name=REGION)
    mock_client.start_crawler_schedule.assert_called_once()


def test_start_crawler_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_crawler_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_crawler_schedule",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start crawler schedule"):
        start_crawler_schedule("test-crawler_name", region_name=REGION)


def test_start_data_quality_rule_recommendation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_data_quality_rule_recommendation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_data_quality_rule_recommendation_run({}, "test-role", region_name=REGION)
    mock_client.start_data_quality_rule_recommendation_run.assert_called_once()


def test_start_data_quality_rule_recommendation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_data_quality_rule_recommendation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_data_quality_rule_recommendation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start data quality rule recommendation run"):
        start_data_quality_rule_recommendation_run({}, "test-role", region_name=REGION)


def test_start_data_quality_ruleset_evaluation_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_data_quality_ruleset_evaluation_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_data_quality_ruleset_evaluation_run({}, "test-role", [], region_name=REGION)
    mock_client.start_data_quality_ruleset_evaluation_run.assert_called_once()


def test_start_data_quality_ruleset_evaluation_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_data_quality_ruleset_evaluation_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_data_quality_ruleset_evaluation_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start data quality ruleset evaluation run"):
        start_data_quality_ruleset_evaluation_run({}, "test-role", [], region_name=REGION)


def test_start_export_labels_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_labels_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_export_labels_task_run("test-transform_id", "test-output_s3_path", region_name=REGION)
    mock_client.start_export_labels_task_run.assert_called_once()


def test_start_export_labels_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_labels_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_export_labels_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start export labels task run"):
        start_export_labels_task_run("test-transform_id", "test-output_s3_path", region_name=REGION)


def test_start_import_labels_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import_labels_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_import_labels_task_run("test-transform_id", "test-input_s3_path", region_name=REGION)
    mock_client.start_import_labels_task_run.assert_called_once()


def test_start_import_labels_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import_labels_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_import_labels_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start import labels task run"):
        start_import_labels_task_run("test-transform_id", "test-input_s3_path", region_name=REGION)


def test_start_ml_evaluation_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_ml_evaluation_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_ml_evaluation_task_run("test-transform_id", region_name=REGION)
    mock_client.start_ml_evaluation_task_run.assert_called_once()


def test_start_ml_evaluation_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_ml_evaluation_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_ml_evaluation_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start ml evaluation task run"):
        start_ml_evaluation_task_run("test-transform_id", region_name=REGION)


def test_start_ml_labeling_set_generation_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_ml_labeling_set_generation_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_ml_labeling_set_generation_task_run("test-transform_id", "test-output_s3_path", region_name=REGION)
    mock_client.start_ml_labeling_set_generation_task_run.assert_called_once()


def test_start_ml_labeling_set_generation_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_ml_labeling_set_generation_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_ml_labeling_set_generation_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start ml labeling set generation task run"):
        start_ml_labeling_set_generation_task_run("test-transform_id", "test-output_s3_path", region_name=REGION)


def test_start_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_trigger("test-name", region_name=REGION)
    mock_client.start_trigger.assert_called_once()


def test_start_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start trigger"):
        start_trigger("test-name", region_name=REGION)


def test_start_workflow_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_workflow_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    start_workflow_run("test-name", region_name=REGION)
    mock_client.start_workflow_run.assert_called_once()


def test_start_workflow_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_workflow_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_workflow_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start workflow run"):
        start_workflow_run("test-name", region_name=REGION)


def test_stop_column_statistics_task_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_column_statistics_task_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_column_statistics_task_run("test-database_name", "test-table_name", region_name=REGION)
    mock_client.stop_column_statistics_task_run.assert_called_once()


def test_stop_column_statistics_task_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_column_statistics_task_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_column_statistics_task_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop column statistics task run"):
        stop_column_statistics_task_run("test-database_name", "test-table_name", region_name=REGION)


def test_stop_column_statistics_task_run_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_column_statistics_task_run_schedule.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_column_statistics_task_run_schedule("test-database_name", "test-table_name", region_name=REGION)
    mock_client.stop_column_statistics_task_run_schedule.assert_called_once()


def test_stop_column_statistics_task_run_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_column_statistics_task_run_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_column_statistics_task_run_schedule",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop column statistics task run schedule"):
        stop_column_statistics_task_run_schedule("test-database_name", "test-table_name", region_name=REGION)


def test_stop_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_crawler("test-name", region_name=REGION)
    mock_client.stop_crawler.assert_called_once()


def test_stop_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop crawler"):
        stop_crawler("test-name", region_name=REGION)


def test_stop_crawler_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_crawler_schedule.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_crawler_schedule("test-crawler_name", region_name=REGION)
    mock_client.stop_crawler_schedule.assert_called_once()


def test_stop_crawler_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_crawler_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_crawler_schedule",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop crawler schedule"):
        stop_crawler_schedule("test-crawler_name", region_name=REGION)


def test_stop_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_session.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_session("test-id", region_name=REGION)
    mock_client.stop_session.assert_called_once()


def test_stop_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_session",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop session"):
        stop_session("test-id", region_name=REGION)


def test_stop_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_trigger("test-name", region_name=REGION)
    mock_client.stop_trigger.assert_called_once()


def test_stop_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop trigger"):
        stop_trigger("test-name", region_name=REGION)


def test_stop_workflow_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_workflow_run.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    stop_workflow_run("test-name", "test-run_id", region_name=REGION)
    mock_client.stop_workflow_run.assert_called_once()


def test_stop_workflow_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_workflow_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_workflow_run",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop workflow run"):
        stop_workflow_run("test-name", "test-run_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_blueprint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_blueprint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_blueprint("test-name", "test-blueprint_location", region_name=REGION)
    mock_client.update_blueprint.assert_called_once()


def test_update_blueprint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_blueprint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_blueprint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update blueprint"):
        update_blueprint("test-name", "test-blueprint_location", region_name=REGION)


def test_update_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_catalog.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_catalog("test-catalog_id", {}, region_name=REGION)
    mock_client.update_catalog.assert_called_once()


def test_update_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_catalog",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update catalog"):
        update_catalog("test-catalog_id", {}, region_name=REGION)


def test_update_classifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_classifier.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_classifier(region_name=REGION)
    mock_client.update_classifier.assert_called_once()


def test_update_classifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_classifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_classifier",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update classifier"):
        update_classifier(region_name=REGION)


def test_update_column_statistics_for_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_column_statistics_for_partition("test-database_name", "test-table_name", [], [], region_name=REGION)
    mock_client.update_column_statistics_for_partition.assert_called_once()


def test_update_column_statistics_for_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_column_statistics_for_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update column statistics for partition"):
        update_column_statistics_for_partition("test-database_name", "test-table_name", [], [], region_name=REGION)


def test_update_column_statistics_for_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_column_statistics_for_table("test-database_name", "test-table_name", [], region_name=REGION)
    mock_client.update_column_statistics_for_table.assert_called_once()


def test_update_column_statistics_for_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_column_statistics_for_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update column statistics for table"):
        update_column_statistics_for_table("test-database_name", "test-table_name", [], region_name=REGION)


def test_update_column_statistics_task_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)
    mock_client.update_column_statistics_task_settings.assert_called_once()


def test_update_column_statistics_task_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_column_statistics_task_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_column_statistics_task_settings",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update column statistics task settings"):
        update_column_statistics_task_settings("test-database_name", "test-table_name", region_name=REGION)


def test_update_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_connection("test-name", {}, region_name=REGION)
    mock_client.update_connection.assert_called_once()


def test_update_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connection",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connection"):
        update_connection("test-name", {}, region_name=REGION)


def test_update_crawler(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_crawler.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_crawler("test-name", region_name=REGION)
    mock_client.update_crawler.assert_called_once()


def test_update_crawler_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_crawler.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_crawler",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update crawler"):
        update_crawler("test-name", region_name=REGION)


def test_update_crawler_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_crawler_schedule.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_crawler_schedule("test-crawler_name", region_name=REGION)
    mock_client.update_crawler_schedule.assert_called_once()


def test_update_crawler_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_crawler_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_crawler_schedule",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update crawler schedule"):
        update_crawler_schedule("test-crawler_name", region_name=REGION)


def test_update_data_quality_ruleset(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_quality_ruleset.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_data_quality_ruleset("test-name", region_name=REGION)
    mock_client.update_data_quality_ruleset.assert_called_once()


def test_update_data_quality_ruleset_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_quality_ruleset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_quality_ruleset",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data quality ruleset"):
        update_data_quality_ruleset("test-name", region_name=REGION)


def test_update_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_database.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_database("test-name", {}, region_name=REGION)
    mock_client.update_database.assert_called_once()


def test_update_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_database",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update database"):
        update_database("test-name", {}, region_name=REGION)


def test_update_dev_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dev_endpoint.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_dev_endpoint("test-endpoint_name", region_name=REGION)
    mock_client.update_dev_endpoint.assert_called_once()


def test_update_dev_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dev_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dev_endpoint",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dev endpoint"):
        update_dev_endpoint("test-endpoint_name", region_name=REGION)


def test_update_glue_identity_center_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_glue_identity_center_configuration(region_name=REGION)
    mock_client.update_glue_identity_center_configuration.assert_called_once()


def test_update_glue_identity_center_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_glue_identity_center_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_glue_identity_center_configuration",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update glue identity center configuration"):
        update_glue_identity_center_configuration(region_name=REGION)


def test_update_integration_resource_property(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_resource_property.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_integration_resource_property("test-resource_arn", region_name=REGION)
    mock_client.update_integration_resource_property.assert_called_once()


def test_update_integration_resource_property_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_resource_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_integration_resource_property",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update integration resource property"):
        update_integration_resource_property("test-resource_arn", region_name=REGION)


def test_update_integration_table_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_table_properties.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)
    mock_client.update_integration_table_properties.assert_called_once()


def test_update_integration_table_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_table_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_integration_table_properties",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update integration table properties"):
        update_integration_table_properties("test-resource_arn", "test-table_name", region_name=REGION)


def test_update_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_job.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_job("test-job_name", {}, region_name=REGION)
    mock_client.update_job.assert_called_once()


def test_update_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_job",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update job"):
        update_job("test-job_name", {}, region_name=REGION)


def test_update_job_from_source_control(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_job_from_source_control.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_job_from_source_control(region_name=REGION)
    mock_client.update_job_from_source_control.assert_called_once()


def test_update_job_from_source_control_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_job_from_source_control.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_job_from_source_control",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update job from source control"):
        update_job_from_source_control(region_name=REGION)


def test_update_ml_transform(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ml_transform.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_ml_transform("test-transform_id", region_name=REGION)
    mock_client.update_ml_transform.assert_called_once()


def test_update_ml_transform_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ml_transform.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ml_transform",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update ml transform"):
        update_ml_transform("test-transform_id", region_name=REGION)


def test_update_partition(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_partition.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_partition("test-database_name", "test-table_name", [], {}, region_name=REGION)
    mock_client.update_partition.assert_called_once()


def test_update_partition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_partition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_partition",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update partition"):
        update_partition("test-database_name", "test-table_name", [], {}, region_name=REGION)


def test_update_registry(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_registry.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_registry({}, "test-description", region_name=REGION)
    mock_client.update_registry.assert_called_once()


def test_update_registry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_registry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_registry",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update registry"):
        update_registry({}, "test-description", region_name=REGION)


def test_update_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_schema.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_schema({}, region_name=REGION)
    mock_client.update_schema.assert_called_once()


def test_update_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_schema",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update schema"):
        update_schema({}, region_name=REGION)


def test_update_source_control_from_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_source_control_from_job.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_source_control_from_job(region_name=REGION)
    mock_client.update_source_control_from_job.assert_called_once()


def test_update_source_control_from_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_source_control_from_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_source_control_from_job",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update source control from job"):
        update_source_control_from_job(region_name=REGION)


def test_update_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_table("test-database_name", region_name=REGION)
    mock_client.update_table.assert_called_once()


def test_update_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_table",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update table"):
        update_table("test-database_name", region_name=REGION)


def test_update_table_optimizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table_optimizer.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, region_name=REGION)
    mock_client.update_table_optimizer.assert_called_once()


def test_update_table_optimizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_table_optimizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_table_optimizer",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update table optimizer"):
        update_table_optimizer("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", {}, region_name=REGION)


def test_update_trigger(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_trigger.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_trigger("test-name", {}, region_name=REGION)
    mock_client.update_trigger.assert_called_once()


def test_update_trigger_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_trigger.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_trigger",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update trigger"):
        update_trigger("test-name", {}, region_name=REGION)


def test_update_usage_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_profile.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_usage_profile("test-name", {}, region_name=REGION)
    mock_client.update_usage_profile.assert_called_once()


def test_update_usage_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_usage_profile",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update usage profile"):
        update_usage_profile("test-name", {}, region_name=REGION)


def test_update_user_defined_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_defined_function.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_user_defined_function("test-database_name", "test-function_name", {}, region_name=REGION)
    mock_client.update_user_defined_function.assert_called_once()


def test_update_user_defined_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_defined_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_defined_function",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user defined function"):
        update_user_defined_function("test-database_name", "test-function_name", {}, region_name=REGION)


def test_update_workflow(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_workflow.return_value = {}
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    update_workflow("test-name", region_name=REGION)
    mock_client.update_workflow.assert_called_once()


def test_update_workflow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_workflow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_workflow",
    )
    monkeypatch.setattr(glue_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update workflow"):
        update_workflow("test-name", region_name=REGION)


def test_batch_create_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_create_partition
    mock_client = MagicMock()
    mock_client.batch_create_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_create_partition("test-database_name", "test-table_name", "test-partition_input_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_create_partition.assert_called_once()

def test_batch_delete_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_delete_connection
    mock_client = MagicMock()
    mock_client.batch_delete_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_delete_connection("test-connection_name_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_delete_connection.assert_called_once()

def test_batch_delete_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_delete_partition
    mock_client = MagicMock()
    mock_client.batch_delete_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_delete_partition("test-database_name", "test-table_name", "test-partitions_to_delete", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_delete_partition.assert_called_once()

def test_batch_delete_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_delete_table
    mock_client = MagicMock()
    mock_client.batch_delete_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_delete_table("test-database_name", "test-tables_to_delete", catalog_id="test-catalog_id", transaction_id="test-transaction_id", region_name="us-east-1")
    mock_client.batch_delete_table.assert_called_once()

def test_batch_delete_table_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_delete_table_version
    mock_client = MagicMock()
    mock_client.batch_delete_table_version.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_delete_table_version("test-database_name", "test-table_name", "test-version_ids", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_delete_table_version.assert_called_once()

def test_batch_get_blueprints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_get_blueprints
    mock_client = MagicMock()
    mock_client.batch_get_blueprints.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_get_blueprints("test-names", include_blueprint=True, include_parameter_spec=True, region_name="us-east-1")
    mock_client.batch_get_blueprints.assert_called_once()

def test_batch_get_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_get_partition
    mock_client = MagicMock()
    mock_client.batch_get_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_get_partition("test-database_name", "test-table_name", "test-partitions_to_get", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_get_partition.assert_called_once()

def test_batch_get_workflows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_get_workflows
    mock_client = MagicMock()
    mock_client.batch_get_workflows.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_get_workflows("test-names", include_graph=True, region_name="us-east-1")
    mock_client.batch_get_workflows.assert_called_once()

def test_batch_put_data_quality_statistic_annotation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_put_data_quality_statistic_annotation
    mock_client = MagicMock()
    mock_client.batch_put_data_quality_statistic_annotation.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_put_data_quality_statistic_annotation("test-inclusion_annotations", client_token="test-client_token", region_name="us-east-1")
    mock_client.batch_put_data_quality_statistic_annotation.assert_called_once()

def test_batch_update_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import batch_update_partition
    mock_client = MagicMock()
    mock_client.batch_update_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    batch_update_partition("test-database_name", "test-table_name", "test-entries", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.batch_update_partition.assert_called_once()

def test_cancel_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import cancel_statement
    mock_client = MagicMock()
    mock_client.cancel_statement.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    cancel_statement("test-session_id", "test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.cancel_statement.assert_called_once()

def test_create_blueprint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_blueprint
    mock_client = MagicMock()
    mock_client.create_blueprint.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_blueprint("test-name", "test-blueprint_location", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_blueprint.assert_called_once()

def test_create_catalog_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_catalog
    mock_client = MagicMock()
    mock_client.create_catalog.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_catalog("test-name", "test-catalog_input", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_catalog.assert_called_once()

def test_create_classifier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_classifier
    mock_client = MagicMock()
    mock_client.create_classifier.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_classifier(grok_classifier="test-grok_classifier", xml_classifier="test-xml_classifier", json_classifier="test-json_classifier", csv_classifier="test-csv_classifier", region_name="us-east-1")
    mock_client.create_classifier.assert_called_once()

def test_create_column_statistics_task_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_column_statistics_task_settings
    mock_client = MagicMock()
    mock_client.create_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_column_statistics_task_settings("test-database_name", "test-table_name", "test-role", schedule="test-schedule", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_column_statistics_task_settings.assert_called_once()

def test_create_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_connection
    mock_client = MagicMock()
    mock_client.create_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_connection("test-connection_input", catalog_id="test-catalog_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_connection.assert_called_once()

def test_create_crawler_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_crawler
    mock_client = MagicMock()
    mock_client.create_crawler.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_crawler("test-name", "test-role", "test-targets", database_name="test-database_name", description="test-description", schedule="test-schedule", classifiers="test-classifiers", table_prefix="test-table_prefix", schema_change_policy="{}", recrawl_policy="{}", lineage_configuration={}, lake_formation_configuration={}, configuration={}, crawler_security_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_crawler.assert_called_once()

def test_create_custom_entity_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_custom_entity_type
    mock_client = MagicMock()
    mock_client.create_custom_entity_type.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_custom_entity_type("test-name", "test-regex_string", context_words={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_entity_type.assert_called_once()

def test_create_data_quality_ruleset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_data_quality_ruleset
    mock_client = MagicMock()
    mock_client.create_data_quality_ruleset.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_data_quality_ruleset("test-name", "test-ruleset", description="test-description", tags=[{"Key": "k", "Value": "v"}], target_table="test-target_table", data_quality_security_configuration={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_data_quality_ruleset.assert_called_once()

def test_create_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_database
    mock_client = MagicMock()
    mock_client.create_database.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_database("test-database_input", catalog_id="test-catalog_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_database.assert_called_once()

def test_create_dev_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_dev_endpoint
    mock_client = MagicMock()
    mock_client.create_dev_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_dev_endpoint("test-endpoint_name", "test-role_arn", security_group_ids="test-security_group_ids", subnet_id="test-subnet_id", public_key="test-public_key", public_keys="test-public_keys", number_of_nodes="test-number_of_nodes", worker_type="test-worker_type", glue_version="test-glue_version", number_of_workers="test-number_of_workers", extra_python_libs_s3_path="test-extra_python_libs_s3_path", extra_jars_s3_path="test-extra_jars_s3_path", security_configuration={}, tags=[{"Key": "k", "Value": "v"}], arguments="test-arguments", region_name="us-east-1")
    mock_client.create_dev_endpoint.assert_called_once()

def test_create_glue_identity_center_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_glue_identity_center_configuration
    mock_client = MagicMock()
    mock_client.create_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_glue_identity_center_configuration("test-instance_arn", scopes="test-scopes", user_background_sessions_enabled="test-user_background_sessions_enabled", region_name="us-east-1")
    mock_client.create_glue_identity_center_configuration.assert_called_once()

def test_create_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_integration
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_integration("test-integration_name", "test-source_arn", "test-target_arn", description="test-description", data_filter=[{}], kms_key_id="test-kms_key_id", additional_encryption_context={}, tags=[{"Key": "k", "Value": "v"}], integration_config={}, region_name="us-east-1")
    mock_client.create_integration.assert_called_once()

def test_create_integration_resource_property_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_integration_resource_property
    mock_client = MagicMock()
    mock_client.create_integration_resource_property.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_integration_resource_property("test-resource_arn", source_processing_properties={}, target_processing_properties={}, region_name="us-east-1")
    mock_client.create_integration_resource_property.assert_called_once()

def test_create_integration_table_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_integration_table_properties
    mock_client = MagicMock()
    mock_client.create_integration_table_properties.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_integration_table_properties("test-resource_arn", "test-table_name", source_table_config={}, target_table_config={}, region_name="us-east-1")
    mock_client.create_integration_table_properties.assert_called_once()

def test_create_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_job
    mock_client = MagicMock()
    mock_client.create_job.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_job("test-name", "test-role", "test-command", job_mode="test-job_mode", job_run_queuing_enabled="test-job_run_queuing_enabled", description="test-description", log_uri="test-log_uri", execution_property="test-execution_property", default_arguments="test-default_arguments", non_overridable_arguments="test-non_overridable_arguments", connections="test-connections", max_retries=1, allocated_capacity="test-allocated_capacity", timeout=1, max_capacity=1, security_configuration={}, tags=[{"Key": "k", "Value": "v"}], notification_property="test-notification_property", glue_version="test-glue_version", number_of_workers="test-number_of_workers", worker_type="test-worker_type", code_gen_configuration_nodes={}, execution_class="test-execution_class", source_control_details="test-source_control_details", maintenance_window="test-maintenance_window", region_name="us-east-1")
    mock_client.create_job.assert_called_once()

def test_create_ml_transform_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_ml_transform
    mock_client = MagicMock()
    mock_client.create_ml_transform.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_ml_transform("test-name", "test-input_record_tables", "test-parameters", "test-role", description="test-description", glue_version="test-glue_version", max_capacity=1, worker_type="test-worker_type", number_of_workers="test-number_of_workers", timeout=1, max_retries=1, tags=[{"Key": "k", "Value": "v"}], transform_encryption="test-transform_encryption", region_name="us-east-1")
    mock_client.create_ml_transform.assert_called_once()

def test_create_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_partition
    mock_client = MagicMock()
    mock_client.create_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_partition("test-database_name", "test-table_name", "test-partition_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.create_partition.assert_called_once()

def test_create_partition_index_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_partition_index
    mock_client = MagicMock()
    mock_client.create_partition_index.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_partition_index("test-database_name", "test-table_name", "test-partition_index", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.create_partition_index.assert_called_once()

def test_create_registry_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_registry
    mock_client = MagicMock()
    mock_client.create_registry.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_registry("test-registry_name", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_registry.assert_called_once()

def test_create_schema_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_schema
    mock_client = MagicMock()
    mock_client.create_schema.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_schema("test-schema_name", "test-data_format", registry_id="test-registry_id", compatibility="test-compatibility", description="test-description", tags=[{"Key": "k", "Value": "v"}], schema_definition={}, region_name="us-east-1")
    mock_client.create_schema.assert_called_once()

def test_create_script_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_script
    mock_client = MagicMock()
    mock_client.create_script.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_script(dag_nodes="test-dag_nodes", dag_edges="test-dag_edges", language="test-language", region_name="us-east-1")
    mock_client.create_script.assert_called_once()

def test_create_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_session
    mock_client = MagicMock()
    mock_client.create_session.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_session("test-id", "test-role", "test-command", description="test-description", timeout=1, idle_timeout=1, default_arguments="test-default_arguments", connections="test-connections", max_capacity=1, number_of_workers="test-number_of_workers", worker_type="test-worker_type", security_configuration={}, glue_version="test-glue_version", tags=[{"Key": "k", "Value": "v"}], request_origin="test-request_origin", region_name="us-east-1")
    mock_client.create_session.assert_called_once()

def test_create_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_table
    mock_client = MagicMock()
    mock_client.create_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_table("test-database_name", catalog_id="test-catalog_id", name="test-name", table_input="test-table_input", partition_indexes="test-partition_indexes", transaction_id="test-transaction_id", open_table_format_input="test-open_table_format_input", region_name="us-east-1")
    mock_client.create_table.assert_called_once()

def test_create_trigger_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_trigger
    mock_client = MagicMock()
    mock_client.create_trigger.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_trigger("test-name", "test-type_value", "test-actions", workflow_name="test-workflow_name", schedule="test-schedule", predicate="test-predicate", description="test-description", start_on_creation="test-start_on_creation", tags=[{"Key": "k", "Value": "v"}], event_batching_condition="test-event_batching_condition", region_name="us-east-1")
    mock_client.create_trigger.assert_called_once()

def test_create_usage_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_usage_profile
    mock_client = MagicMock()
    mock_client.create_usage_profile.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_usage_profile("test-name", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_usage_profile.assert_called_once()

def test_create_user_defined_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_user_defined_function
    mock_client = MagicMock()
    mock_client.create_user_defined_function.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_user_defined_function("test-database_name", "test-function_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.create_user_defined_function.assert_called_once()

def test_create_workflow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import create_workflow
    mock_client = MagicMock()
    mock_client.create_workflow.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    create_workflow("test-name", description="test-description", default_run_properties={}, tags=[{"Key": "k", "Value": "v"}], max_concurrent_runs=1, region_name="us-east-1")
    mock_client.create_workflow.assert_called_once()

def test_delete_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_column_statistics_for_partition
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_column_statistics_for_partition.assert_called_once()

def test_delete_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_column_statistics_for_table
    mock_client = MagicMock()
    mock_client.delete_column_statistics_for_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_column_statistics_for_table("test-database_name", "test-table_name", "test-column_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_column_statistics_for_table.assert_called_once()

def test_delete_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_connection
    mock_client = MagicMock()
    mock_client.delete_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_connection("test-connection_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_connection.assert_called_once()

def test_delete_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_database
    mock_client = MagicMock()
    mock_client.delete_database.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_database("test-name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_database.assert_called_once()

def test_delete_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_partition
    mock_client = MagicMock()
    mock_client.delete_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_partition("test-database_name", "test-table_name", "test-partition_values", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_partition.assert_called_once()

def test_delete_partition_index_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_partition_index
    mock_client = MagicMock()
    mock_client.delete_partition_index.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_partition_index("test-database_name", "test-table_name", "test-index_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_partition_index.assert_called_once()

def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_resource_policy
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy(policy_hash_condition="test-policy_hash_condition", resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.delete_resource_policy.assert_called_once()

def test_delete_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_session
    mock_client = MagicMock()
    mock_client.delete_session.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.delete_session.assert_called_once()

def test_delete_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_table
    mock_client = MagicMock()
    mock_client.delete_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_table("test-database_name", "test-name", catalog_id="test-catalog_id", transaction_id="test-transaction_id", region_name="us-east-1")
    mock_client.delete_table.assert_called_once()

def test_delete_table_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_table_version
    mock_client = MagicMock()
    mock_client.delete_table_version.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_table_version("test-database_name", "test-table_name", "test-version_id", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_table_version.assert_called_once()

def test_delete_user_defined_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import delete_user_defined_function
    mock_client = MagicMock()
    mock_client.delete_user_defined_function.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    delete_user_defined_function("test-database_name", "test-function_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.delete_user_defined_function.assert_called_once()

def test_describe_entity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import describe_entity
    mock_client = MagicMock()
    mock_client.describe_entity.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    describe_entity("test-connection_name", "test-entity_name", catalog_id="test-catalog_id", next_token="test-next_token", data_store_api_version="test-data_store_api_version", region_name="us-east-1")
    mock_client.describe_entity.assert_called_once()

def test_describe_inbound_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import describe_inbound_integrations
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    describe_inbound_integrations(integration_arn="test-integration_arn", marker="test-marker", max_records=1, target_arn="test-target_arn", region_name="us-east-1")
    mock_client.describe_inbound_integrations.assert_called_once()

def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import describe_integrations
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    describe_integrations(integration_identifier="test-integration_identifier", marker="test-marker", max_records=1, filters=[{}], region_name="us-east-1")
    mock_client.describe_integrations.assert_called_once()

def test_get_blueprint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_blueprint
    mock_client = MagicMock()
    mock_client.get_blueprint.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_blueprint("test-name", include_blueprint=True, include_parameter_spec=True, region_name="us-east-1")
    mock_client.get_blueprint.assert_called_once()

def test_get_blueprint_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_blueprint_runs
    mock_client = MagicMock()
    mock_client.get_blueprint_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_blueprint_runs("test-blueprint_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_blueprint_runs.assert_called_once()

def test_get_catalog_import_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_catalog_import_status
    mock_client = MagicMock()
    mock_client.get_catalog_import_status.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_catalog_import_status(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_catalog_import_status.assert_called_once()

def test_get_catalogs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_catalogs
    mock_client = MagicMock()
    mock_client.get_catalogs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_catalogs(parent_catalog_id="test-parent_catalog_id", next_token="test-next_token", max_results=1, recursive=True, include_root=True, region_name="us-east-1")
    mock_client.get_catalogs.assert_called_once()

def test_get_classifiers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_classifiers
    mock_client = MagicMock()
    mock_client.get_classifiers.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_classifiers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_classifiers.assert_called_once()

def test_get_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_column_statistics_for_partition
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_names", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_column_statistics_for_partition.assert_called_once()

def test_get_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_column_statistics_for_table
    mock_client = MagicMock()
    mock_client.get_column_statistics_for_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_column_statistics_for_table("test-database_name", "test-table_name", "test-column_names", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_column_statistics_for_table.assert_called_once()

def test_get_column_statistics_task_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_column_statistics_task_runs
    mock_client = MagicMock()
    mock_client.get_column_statistics_task_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_column_statistics_task_runs("test-database_name", "test-table_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_column_statistics_task_runs.assert_called_once()

def test_get_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_connection
    mock_client = MagicMock()
    mock_client.get_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_connection("test-name", catalog_id="test-catalog_id", hide_password="test-hide_password", apply_override_for_compute_environment=True, region_name="us-east-1")
    mock_client.get_connection.assert_called_once()

def test_get_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_connections
    mock_client = MagicMock()
    mock_client.get_connections.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_connections(catalog_id="test-catalog_id", filter="test-filter", hide_password="test-hide_password", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_connections.assert_called_once()

def test_get_crawler_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_crawler_metrics
    mock_client = MagicMock()
    mock_client.get_crawler_metrics.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_crawler_metrics(crawler_name_list="test-crawler_name_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_crawler_metrics.assert_called_once()

def test_get_crawlers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_crawlers
    mock_client = MagicMock()
    mock_client.get_crawlers.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_crawlers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_crawlers.assert_called_once()

def test_get_data_catalog_encryption_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_data_catalog_encryption_settings
    mock_client = MagicMock()
    mock_client.get_data_catalog_encryption_settings.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_data_catalog_encryption_settings(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_data_catalog_encryption_settings.assert_called_once()

def test_get_data_quality_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_data_quality_model
    mock_client = MagicMock()
    mock_client.get_data_quality_model.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_data_quality_model("test-profile_id", statistic_id="test-statistic_id", region_name="us-east-1")
    mock_client.get_data_quality_model.assert_called_once()

def test_get_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_database
    mock_client = MagicMock()
    mock_client.get_database.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_database("test-name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_database.assert_called_once()

def test_get_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_databases
    mock_client = MagicMock()
    mock_client.get_databases.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_databases(catalog_id="test-catalog_id", next_token="test-next_token", max_results=1, resource_share_type="test-resource_share_type", attributes_to_get="test-attributes_to_get", region_name="us-east-1")
    mock_client.get_databases.assert_called_once()

def test_get_dataflow_graph_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_dataflow_graph
    mock_client = MagicMock()
    mock_client.get_dataflow_graph.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_dataflow_graph(python_script="test-python_script", region_name="us-east-1")
    mock_client.get_dataflow_graph.assert_called_once()

def test_get_dev_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_dev_endpoints
    mock_client = MagicMock()
    mock_client.get_dev_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_dev_endpoints(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_dev_endpoints.assert_called_once()

def test_get_entity_records_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_entity_records
    mock_client = MagicMock()
    mock_client.get_entity_records.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_entity_records("test-entity_name", 1, connection_name="test-connection_name", catalog_id="test-catalog_id", next_token="test-next_token", data_store_api_version="test-data_store_api_version", connection_options={}, filter_predicate="test-filter_predicate", order_by="test-order_by", selected_fields="test-selected_fields", region_name="us-east-1")
    mock_client.get_entity_records.assert_called_once()

def test_get_job_bookmark_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_job_bookmark
    mock_client = MagicMock()
    mock_client.get_job_bookmark.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_job_bookmark("test-job_name", run_id="test-run_id", region_name="us-east-1")
    mock_client.get_job_bookmark.assert_called_once()

def test_get_job_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_job_runs
    mock_client = MagicMock()
    mock_client.get_job_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_job_runs("test-job_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_job_runs.assert_called_once()

def test_get_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_jobs
    mock_client = MagicMock()
    mock_client.get_jobs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_jobs(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_jobs.assert_called_once()

def test_get_mapping_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_mapping
    mock_client = MagicMock()
    mock_client.get_mapping.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_mapping("test-source", sinks="test-sinks", location="test-location", region_name="us-east-1")
    mock_client.get_mapping.assert_called_once()

def test_get_ml_task_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_ml_task_runs
    mock_client = MagicMock()
    mock_client.get_ml_task_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_ml_task_runs("test-transform_id", next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", region_name="us-east-1")
    mock_client.get_ml_task_runs.assert_called_once()

def test_get_ml_transforms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_ml_transforms
    mock_client = MagicMock()
    mock_client.get_ml_transforms.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_ml_transforms(next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", region_name="us-east-1")
    mock_client.get_ml_transforms.assert_called_once()

def test_get_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_partition
    mock_client = MagicMock()
    mock_client.get_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_partition("test-database_name", "test-table_name", "test-partition_values", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_partition.assert_called_once()

def test_get_partition_indexes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_partition_indexes
    mock_client = MagicMock()
    mock_client.get_partition_indexes.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_partition_indexes("test-database_name", "test-table_name", catalog_id="test-catalog_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.get_partition_indexes.assert_called_once()

def test_get_partitions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_partitions
    mock_client = MagicMock()
    mock_client.get_partitions.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_partitions("test-database_name", "test-table_name", catalog_id="test-catalog_id", expression="test-expression", next_token="test-next_token", segment="test-segment", max_results=1, exclude_column_schema="test-exclude_column_schema", transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", region_name="us-east-1")
    mock_client.get_partitions.assert_called_once()

def test_get_plan_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_plan
    mock_client = MagicMock()
    mock_client.get_plan.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_plan({}, "test-source", sinks="test-sinks", location="test-location", language="test-language", additional_plan_options_map={}, region_name="us-east-1")
    mock_client.get_plan.assert_called_once()

def test_get_resource_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_resource_policies
    mock_client = MagicMock()
    mock_client.get_resource_policies.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_resource_policies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_resource_policies.assert_called_once()

def test_get_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_resource_policy
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_resource_policy(resource_arn="test-resource_arn", region_name="us-east-1")
    mock_client.get_resource_policy.assert_called_once()

def test_get_schema_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_schema_version
    mock_client = MagicMock()
    mock_client.get_schema_version.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_schema_version(schema_id="test-schema_id", schema_version_id="test-schema_version_id", schema_version_number="test-schema_version_number", region_name="us-east-1")
    mock_client.get_schema_version.assert_called_once()

def test_get_security_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_security_configurations
    mock_client = MagicMock()
    mock_client.get_security_configurations.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_security_configurations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_security_configurations.assert_called_once()

def test_get_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_session
    mock_client = MagicMock()
    mock_client.get_session.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.get_session.assert_called_once()

def test_get_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_statement
    mock_client = MagicMock()
    mock_client.get_statement.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_statement("test-session_id", "test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.get_statement.assert_called_once()

def test_get_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_table
    mock_client = MagicMock()
    mock_client.get_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_table("test-database_name", "test-name", catalog_id="test-catalog_id", transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", audit_context={}, include_status_details=True, region_name="us-east-1")
    mock_client.get_table.assert_called_once()

def test_get_table_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_table_version
    mock_client = MagicMock()
    mock_client.get_table_version.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_table_version("test-database_name", "test-table_name", catalog_id="test-catalog_id", version_id="test-version_id", region_name="us-east-1")
    mock_client.get_table_version.assert_called_once()

def test_get_table_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_table_versions
    mock_client = MagicMock()
    mock_client.get_table_versions.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_table_versions("test-database_name", "test-table_name", catalog_id="test-catalog_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_table_versions.assert_called_once()

def test_get_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_tables
    mock_client = MagicMock()
    mock_client.get_tables.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_tables("test-database_name", catalog_id="test-catalog_id", expression="test-expression", next_token="test-next_token", max_results=1, transaction_id="test-transaction_id", query_as_of_time="test-query_as_of_time", audit_context={}, include_status_details=True, attributes_to_get="test-attributes_to_get", region_name="us-east-1")
    mock_client.get_tables.assert_called_once()

def test_get_triggers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_triggers
    mock_client = MagicMock()
    mock_client.get_triggers.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_triggers(next_token="test-next_token", dependent_job_name="test-dependent_job_name", max_results=1, region_name="us-east-1")
    mock_client.get_triggers.assert_called_once()

def test_get_unfiltered_partition_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_unfiltered_partition_metadata
    mock_client = MagicMock()
    mock_client.get_unfiltered_partition_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_unfiltered_partition_metadata("test-catalog_id", "test-database_name", "test-table_name", "test-partition_values", 1, region="test-region", audit_context={}, query_session_context={}, region_name="us-east-1")
    mock_client.get_unfiltered_partition_metadata.assert_called_once()

def test_get_unfiltered_partitions_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_unfiltered_partitions_metadata
    mock_client = MagicMock()
    mock_client.get_unfiltered_partitions_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_unfiltered_partitions_metadata("test-catalog_id", "test-database_name", "test-table_name", 1, region="test-region", expression="test-expression", audit_context={}, next_token="test-next_token", segment="test-segment", max_results=1, query_session_context={}, region_name="us-east-1")
    mock_client.get_unfiltered_partitions_metadata.assert_called_once()

def test_get_unfiltered_table_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_unfiltered_table_metadata
    mock_client = MagicMock()
    mock_client.get_unfiltered_table_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_unfiltered_table_metadata("test-catalog_id", "test-database_name", "test-name", 1, region="test-region", audit_context={}, parent_resource_arn="test-parent_resource_arn", root_resource_arn="test-root_resource_arn", supported_dialect=1, permissions="test-permissions", query_session_context={}, region_name="us-east-1")
    mock_client.get_unfiltered_table_metadata.assert_called_once()

def test_get_user_defined_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_user_defined_function
    mock_client = MagicMock()
    mock_client.get_user_defined_function.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_user_defined_function("test-database_name", "test-function_name", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.get_user_defined_function.assert_called_once()

def test_get_user_defined_functions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_user_defined_functions
    mock_client = MagicMock()
    mock_client.get_user_defined_functions.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_user_defined_functions("test-pattern", catalog_id="test-catalog_id", database_name="test-database_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_user_defined_functions.assert_called_once()

def test_get_workflow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_workflow
    mock_client = MagicMock()
    mock_client.get_workflow.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_workflow("test-name", include_graph=True, region_name="us-east-1")
    mock_client.get_workflow.assert_called_once()

def test_get_workflow_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_workflow_run
    mock_client = MagicMock()
    mock_client.get_workflow_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_workflow_run("test-name", "test-run_id", include_graph=True, region_name="us-east-1")
    mock_client.get_workflow_run.assert_called_once()

def test_get_workflow_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import get_workflow_runs
    mock_client = MagicMock()
    mock_client.get_workflow_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    get_workflow_runs("test-name", include_graph=True, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_workflow_runs.assert_called_once()

def test_import_catalog_to_glue_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import import_catalog_to_glue
    mock_client = MagicMock()
    mock_client.import_catalog_to_glue.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    import_catalog_to_glue(catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.import_catalog_to_glue.assert_called_once()

def test_list_blueprints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_blueprints
    mock_client = MagicMock()
    mock_client.list_blueprints.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_blueprints(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_blueprints.assert_called_once()

def test_list_column_statistics_task_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_column_statistics_task_runs
    mock_client = MagicMock()
    mock_client.list_column_statistics_task_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_column_statistics_task_runs(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_column_statistics_task_runs.assert_called_once()

def test_list_connection_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_connection_types
    mock_client = MagicMock()
    mock_client.list_connection_types.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_connection_types(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_connection_types.assert_called_once()

def test_list_crawlers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_crawlers
    mock_client = MagicMock()
    mock_client.list_crawlers.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_crawlers(max_results=1, next_token="test-next_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_crawlers.assert_called_once()

def test_list_crawls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_crawls
    mock_client = MagicMock()
    mock_client.list_crawls.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_crawls("test-crawler_name", max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.list_crawls.assert_called_once()

def test_list_custom_entity_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_custom_entity_types
    mock_client = MagicMock()
    mock_client.list_custom_entity_types.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_custom_entity_types(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_custom_entity_types.assert_called_once()

def test_list_data_quality_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_results
    mock_client = MagicMock()
    mock_client.list_data_quality_results.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_results(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_data_quality_results.assert_called_once()

def test_list_data_quality_rule_recommendation_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_rule_recommendation_runs
    mock_client = MagicMock()
    mock_client.list_data_quality_rule_recommendation_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_rule_recommendation_runs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_data_quality_rule_recommendation_runs.assert_called_once()

def test_list_data_quality_ruleset_evaluation_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_ruleset_evaluation_runs
    mock_client = MagicMock()
    mock_client.list_data_quality_ruleset_evaluation_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_ruleset_evaluation_runs(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_data_quality_ruleset_evaluation_runs.assert_called_once()

def test_list_data_quality_rulesets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_rulesets
    mock_client = MagicMock()
    mock_client.list_data_quality_rulesets.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_rulesets(next_token="test-next_token", max_results=1, filter="test-filter", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_data_quality_rulesets.assert_called_once()

def test_list_data_quality_statistic_annotations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_statistic_annotations
    mock_client = MagicMock()
    mock_client.list_data_quality_statistic_annotations.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_statistic_annotations(statistic_id="test-statistic_id", profile_id="test-profile_id", timestamp_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_data_quality_statistic_annotations.assert_called_once()

def test_list_data_quality_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_data_quality_statistics
    mock_client = MagicMock()
    mock_client.list_data_quality_statistics.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_data_quality_statistics(statistic_id="test-statistic_id", profile_id="test-profile_id", timestamp_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_data_quality_statistics.assert_called_once()

def test_list_dev_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_dev_endpoints
    mock_client = MagicMock()
    mock_client.list_dev_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_dev_endpoints(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_dev_endpoints.assert_called_once()

def test_list_entities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_entities
    mock_client = MagicMock()
    mock_client.list_entities.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_entities(connection_name="test-connection_name", catalog_id="test-catalog_id", parent_entity_name="test-parent_entity_name", next_token="test-next_token", data_store_api_version="test-data_store_api_version", region_name="us-east-1")
    mock_client.list_entities.assert_called_once()

def test_list_ml_transforms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_ml_transforms
    mock_client = MagicMock()
    mock_client.list_ml_transforms.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_ml_transforms(next_token="test-next_token", max_results=1, filter="test-filter", sort="test-sort", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_ml_transforms.assert_called_once()

def test_list_registries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_registries
    mock_client = MagicMock()
    mock_client.list_registries.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_registries(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_registries.assert_called_once()

def test_list_schema_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_schema_versions
    mock_client = MagicMock()
    mock_client.list_schema_versions.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_schema_versions("test-schema_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_schema_versions.assert_called_once()

def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_schemas
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_schemas(registry_id="test-registry_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_schemas.assert_called_once()

def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_sessions
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_sessions(next_token="test-next_token", max_results=1, tags=[{"Key": "k", "Value": "v"}], request_origin="test-request_origin", region_name="us-east-1")
    mock_client.list_sessions.assert_called_once()

def test_list_statements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_statements
    mock_client = MagicMock()
    mock_client.list_statements.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_statements("test-session_id", request_origin="test-request_origin", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_statements.assert_called_once()

def test_list_table_optimizer_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_table_optimizer_runs
    mock_client = MagicMock()
    mock_client.list_table_optimizer_runs.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_table_optimizer_runs("test-catalog_id", "test-database_name", "test-table_name", "test-type_value", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_table_optimizer_runs.assert_called_once()

def test_list_triggers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_triggers
    mock_client = MagicMock()
    mock_client.list_triggers.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_triggers(next_token="test-next_token", dependent_job_name="test-dependent_job_name", max_results=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.list_triggers.assert_called_once()

def test_list_usage_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_usage_profiles
    mock_client = MagicMock()
    mock_client.list_usage_profiles.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_usage_profiles(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_usage_profiles.assert_called_once()

def test_list_workflows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import list_workflows
    mock_client = MagicMock()
    mock_client.list_workflows.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    list_workflows(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_workflows.assert_called_once()

def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import modify_integration
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_identifier", description="test-description", data_filter=[{}], integration_config={}, integration_name="test-integration_name", region_name="us-east-1")
    mock_client.modify_integration.assert_called_once()

def test_put_data_catalog_encryption_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import put_data_catalog_encryption_settings
    mock_client = MagicMock()
    mock_client.put_data_catalog_encryption_settings.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    put_data_catalog_encryption_settings({}, catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.put_data_catalog_encryption_settings.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-policy_in_json", resource_arn="test-resource_arn", policy_hash_condition="test-policy_hash_condition", policy_exists_condition="test-policy_exists_condition", enable_hybrid=True, region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_put_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import put_schema_version_metadata
    mock_client = MagicMock()
    mock_client.put_schema_version_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    put_schema_version_metadata("test-metadata_key_value", schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", region_name="us-east-1")
    mock_client.put_schema_version_metadata.assert_called_once()

def test_query_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import query_schema_version_metadata
    mock_client = MagicMock()
    mock_client.query_schema_version_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    query_schema_version_metadata(schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", metadata_list="test-metadata_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.query_schema_version_metadata.assert_called_once()

def test_remove_schema_version_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import remove_schema_version_metadata
    mock_client = MagicMock()
    mock_client.remove_schema_version_metadata.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    remove_schema_version_metadata("test-metadata_key_value", schema_id="test-schema_id", schema_version_number="test-schema_version_number", schema_version_id="test-schema_version_id", region_name="us-east-1")
    mock_client.remove_schema_version_metadata.assert_called_once()

def test_reset_job_bookmark_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import reset_job_bookmark
    mock_client = MagicMock()
    mock_client.reset_job_bookmark.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    reset_job_bookmark("test-job_name", run_id="test-run_id", region_name="us-east-1")
    mock_client.reset_job_bookmark.assert_called_once()

def test_run_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import run_connection
    mock_client = MagicMock()
    mock_client.test_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    run_connection(connection_name="test-connection_name", catalog_id="test-catalog_id", run_connection_input="test-run_connection_input", region_name="us-east-1")
    mock_client.test_connection.assert_called_once()

def test_run_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import run_statement
    mock_client = MagicMock()
    mock_client.run_statement.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    run_statement("test-session_id", "test-code", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.run_statement.assert_called_once()

def test_search_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import search_tables
    mock_client = MagicMock()
    mock_client.search_tables.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    search_tables(catalog_id="test-catalog_id", next_token="test-next_token", filters=[{}], search_text="test-search_text", sort_criteria="test-sort_criteria", max_results=1, resource_share_type="test-resource_share_type", include_status_details=True, region_name="us-east-1")
    mock_client.search_tables.assert_called_once()

def test_start_blueprint_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_blueprint_run
    mock_client = MagicMock()
    mock_client.start_blueprint_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_blueprint_run("test-blueprint_name", "test-role_arn", parameters="test-parameters", region_name="us-east-1")
    mock_client.start_blueprint_run.assert_called_once()

def test_start_column_statistics_task_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_column_statistics_task_run
    mock_client = MagicMock()
    mock_client.start_column_statistics_task_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_column_statistics_task_run("test-database_name", "test-table_name", "test-role", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, region_name="us-east-1")
    mock_client.start_column_statistics_task_run.assert_called_once()

def test_start_data_quality_rule_recommendation_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_data_quality_rule_recommendation_run
    mock_client = MagicMock()
    mock_client.start_data_quality_rule_recommendation_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_data_quality_rule_recommendation_run("test-data_source", "test-role", number_of_workers="test-number_of_workers", timeout=1, created_ruleset_name="test-created_ruleset_name", data_quality_security_configuration={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.start_data_quality_rule_recommendation_run.assert_called_once()

def test_start_data_quality_ruleset_evaluation_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_data_quality_ruleset_evaluation_run
    mock_client = MagicMock()
    mock_client.start_data_quality_ruleset_evaluation_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_data_quality_ruleset_evaluation_run("test-data_source", "test-role", "test-ruleset_names", number_of_workers="test-number_of_workers", timeout=1, client_token="test-client_token", additional_run_options={}, additional_data_sources="test-additional_data_sources", region_name="us-east-1")
    mock_client.start_data_quality_ruleset_evaluation_run.assert_called_once()

def test_start_import_labels_task_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_import_labels_task_run
    mock_client = MagicMock()
    mock_client.start_import_labels_task_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_import_labels_task_run("test-transform_id", "test-input_s3_path", replace_all_labels="test-replace_all_labels", region_name="us-east-1")
    mock_client.start_import_labels_task_run.assert_called_once()

def test_start_workflow_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import start_workflow_run
    mock_client = MagicMock()
    mock_client.start_workflow_run.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    start_workflow_run("test-name", run_properties={}, region_name="us-east-1")
    mock_client.start_workflow_run.assert_called_once()

def test_stop_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import stop_session
    mock_client = MagicMock()
    mock_client.stop_session.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    stop_session("test-id", request_origin="test-request_origin", region_name="us-east-1")
    mock_client.stop_session.assert_called_once()

def test_update_blueprint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_blueprint
    mock_client = MagicMock()
    mock_client.update_blueprint.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_blueprint("test-name", "test-blueprint_location", description="test-description", region_name="us-east-1")
    mock_client.update_blueprint.assert_called_once()

def test_update_classifier_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_classifier
    mock_client = MagicMock()
    mock_client.update_classifier.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_classifier(grok_classifier="test-grok_classifier", xml_classifier="test-xml_classifier", json_classifier="test-json_classifier", csv_classifier="test-csv_classifier", region_name="us-east-1")
    mock_client.update_classifier.assert_called_once()

def test_update_column_statistics_for_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_column_statistics_for_partition
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_column_statistics_for_partition("test-database_name", "test-table_name", "test-partition_values", "test-column_statistics_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_column_statistics_for_partition.assert_called_once()

def test_update_column_statistics_for_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_column_statistics_for_table
    mock_client = MagicMock()
    mock_client.update_column_statistics_for_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_column_statistics_for_table("test-database_name", "test-table_name", "test-column_statistics_list", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_column_statistics_for_table.assert_called_once()

def test_update_column_statistics_task_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_column_statistics_task_settings
    mock_client = MagicMock()
    mock_client.update_column_statistics_task_settings.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_column_statistics_task_settings("test-database_name", "test-table_name", role="test-role", schedule="test-schedule", column_name_list="test-column_name_list", sample_size=1, catalog_id="test-catalog_id", security_configuration={}, region_name="us-east-1")
    mock_client.update_column_statistics_task_settings.assert_called_once()

def test_update_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_connection
    mock_client = MagicMock()
    mock_client.update_connection.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_connection("test-name", "test-connection_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_connection.assert_called_once()

def test_update_crawler_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_crawler
    mock_client = MagicMock()
    mock_client.update_crawler.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_crawler("test-name", role="test-role", database_name="test-database_name", description="test-description", targets="test-targets", schedule="test-schedule", classifiers="test-classifiers", table_prefix="test-table_prefix", schema_change_policy="{}", recrawl_policy="{}", lineage_configuration={}, lake_formation_configuration={}, configuration={}, crawler_security_configuration={}, region_name="us-east-1")
    mock_client.update_crawler.assert_called_once()

def test_update_crawler_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_crawler_schedule
    mock_client = MagicMock()
    mock_client.update_crawler_schedule.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_crawler_schedule("test-crawler_name", schedule="test-schedule", region_name="us-east-1")
    mock_client.update_crawler_schedule.assert_called_once()

def test_update_data_quality_ruleset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_data_quality_ruleset
    mock_client = MagicMock()
    mock_client.update_data_quality_ruleset.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_data_quality_ruleset("test-name", description="test-description", ruleset="test-ruleset", region_name="us-east-1")
    mock_client.update_data_quality_ruleset.assert_called_once()

def test_update_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_database
    mock_client = MagicMock()
    mock_client.update_database.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_database("test-name", "test-database_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_database.assert_called_once()

def test_update_dev_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_dev_endpoint
    mock_client = MagicMock()
    mock_client.update_dev_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_dev_endpoint("test-endpoint_name", public_key="test-public_key", add_public_keys="test-add_public_keys", delete_public_keys=True, custom_libraries="test-custom_libraries", update_etl_libraries="test-update_etl_libraries", delete_arguments=True, add_arguments="test-add_arguments", region_name="us-east-1")
    mock_client.update_dev_endpoint.assert_called_once()

def test_update_glue_identity_center_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_glue_identity_center_configuration
    mock_client = MagicMock()
    mock_client.update_glue_identity_center_configuration.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_glue_identity_center_configuration(scopes="test-scopes", user_background_sessions_enabled="test-user_background_sessions_enabled", region_name="us-east-1")
    mock_client.update_glue_identity_center_configuration.assert_called_once()

def test_update_integration_resource_property_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_integration_resource_property
    mock_client = MagicMock()
    mock_client.update_integration_resource_property.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_integration_resource_property("test-resource_arn", source_processing_properties={}, target_processing_properties={}, region_name="us-east-1")
    mock_client.update_integration_resource_property.assert_called_once()

def test_update_integration_table_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_integration_table_properties
    mock_client = MagicMock()
    mock_client.update_integration_table_properties.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_integration_table_properties("test-resource_arn", "test-table_name", source_table_config={}, target_table_config={}, region_name="us-east-1")
    mock_client.update_integration_table_properties.assert_called_once()

def test_update_job_from_source_control_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_job_from_source_control
    mock_client = MagicMock()
    mock_client.update_job_from_source_control.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_job_from_source_control(job_name="test-job_name", provider="test-provider", repository_name="test-repository_name", repository_owner="test-repository_owner", branch_name="test-branch_name", folder="test-folder", commit_id="test-commit_id", auth_strategy="test-auth_strategy", auth_token="test-auth_token", region_name="us-east-1")
    mock_client.update_job_from_source_control.assert_called_once()

def test_update_ml_transform_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_ml_transform
    mock_client = MagicMock()
    mock_client.update_ml_transform.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_ml_transform("test-transform_id", name="test-name", description="test-description", parameters="test-parameters", role="test-role", glue_version="test-glue_version", max_capacity=1, worker_type="test-worker_type", number_of_workers="test-number_of_workers", timeout=1, max_retries=1, region_name="us-east-1")
    mock_client.update_ml_transform.assert_called_once()

def test_update_partition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_partition
    mock_client = MagicMock()
    mock_client.update_partition.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_partition("test-database_name", "test-table_name", "test-partition_value_list", "test-partition_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_partition.assert_called_once()

def test_update_schema_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_schema
    mock_client = MagicMock()
    mock_client.update_schema.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_schema("test-schema_id", schema_version_number="test-schema_version_number", compatibility="test-compatibility", description="test-description", region_name="us-east-1")
    mock_client.update_schema.assert_called_once()

def test_update_source_control_from_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_source_control_from_job
    mock_client = MagicMock()
    mock_client.update_source_control_from_job.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_source_control_from_job(job_name="test-job_name", provider="test-provider", repository_name="test-repository_name", repository_owner="test-repository_owner", branch_name="test-branch_name", folder="test-folder", commit_id="test-commit_id", auth_strategy="test-auth_strategy", auth_token="test-auth_token", region_name="us-east-1")
    mock_client.update_source_control_from_job.assert_called_once()

def test_update_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_table
    mock_client = MagicMock()
    mock_client.update_table.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_table("test-database_name", catalog_id="test-catalog_id", name="test-name", table_input="test-table_input", skip_archive=True, transaction_id="test-transaction_id", version_id="test-version_id", view_update_action="test-view_update_action", force=True, update_open_table_format_input="test-update_open_table_format_input", region_name="us-east-1")
    mock_client.update_table.assert_called_once()

def test_update_usage_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_usage_profile
    mock_client = MagicMock()
    mock_client.update_usage_profile.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_usage_profile("test-name", {}, description="test-description", region_name="us-east-1")
    mock_client.update_usage_profile.assert_called_once()

def test_update_user_defined_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_user_defined_function
    mock_client = MagicMock()
    mock_client.update_user_defined_function.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_user_defined_function("test-database_name", "test-function_name", "test-function_input", catalog_id="test-catalog_id", region_name="us-east-1")
    mock_client.update_user_defined_function.assert_called_once()

def test_update_workflow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.glue import update_workflow
    mock_client = MagicMock()
    mock_client.update_workflow.return_value = {}
    monkeypatch.setattr("aws_util.glue.get_client", lambda *a, **kw: mock_client)
    update_workflow("test-name", description="test-description", default_run_properties={}, max_concurrent_runs=1, region_name="us-east-1")
    mock_client.update_workflow.assert_called_once()
