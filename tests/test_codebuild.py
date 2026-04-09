"""Tests for aws_util.codebuild module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.codebuild as cb_mod
from aws_util.codebuild import (
    BuildResult,
    ProjectResult,
    batch_get_builds,
    batch_get_projects,
    create_project,
    delete_project,
    list_builds,
    list_builds_for_project,
    list_projects,
    retry_build,
    start_build,
    start_build_and_wait,
    stop_build,
    update_project,
    wait_for_build,
    batch_delete_builds,
    batch_get_build_batches,
    batch_get_command_executions,
    batch_get_fleets,
    batch_get_report_groups,
    batch_get_reports,
    batch_get_sandboxes,
    create_fleet,
    create_report_group,
    create_webhook,
    delete_build_batch,
    delete_fleet,
    delete_report,
    delete_report_group,
    delete_resource_policy,
    delete_source_credentials,
    delete_webhook,
    describe_code_coverages,
    describe_test_cases,
    get_report_group_trend,
    get_resource_policy,
    import_source_credentials,
    invalidate_project_cache,
    list_build_batches,
    list_build_batches_for_project,
    list_command_executions_for_sandbox,
    list_curated_environment_images,
    list_fleets,
    list_report_groups,
    list_reports,
    list_reports_for_report_group,
    list_sandboxes,
    list_sandboxes_for_project,
    list_shared_projects,
    list_shared_report_groups,
    list_source_credentials,
    put_resource_policy,
    retry_build_batch,
    start_build_batch,
    start_command_execution,
    start_sandbox,
    start_sandbox_connection,
    stop_build_batch,
    stop_sandbox,
    update_fleet,
    update_project_visibility,
    update_report_group,
    update_webhook,
)
from aws_util.exceptions import AwsTimeoutError

REGION = "us-east-1"
PROJECT_NAME = "test-project"
BUILD_ID = "test-project:build-123"
PROJECT_ARN = "arn:aws:codebuild:us-east-1:123456789012:project/test-project"
BUILD_ARN = "arn:aws:codebuild:us-east-1:123456789012:build/test-project:build-123"
SERVICE_ROLE = "arn:aws:iam::123456789012:role/CodeBuildRole"

_SOURCE = {"type": "GITHUB", "location": "https://github.com/test/repo.git"}
_ARTIFACTS = {"type": "NO_ARTIFACTS"}
_ENVIRONMENT = {
    "type": "LINUX_CONTAINER",
    "computeType": "BUILD_GENERAL1_SMALL",
    "image": "aws/codebuild/standard:7.0",
}

_RAW_PROJECT = {
    "name": PROJECT_NAME,
    "arn": PROJECT_ARN,
    "description": "A test project",
    "source": _SOURCE,
    "artifacts": _ARTIFACTS,
    "environment": _ENVIRONMENT,
    "serviceRole": SERVICE_ROLE,
    "created": "2024-01-01T00:00:00Z",
    "lastModified": "2024-06-01T00:00:00Z",
    "tags": [{"key": "env", "value": "test"}],
}

_RAW_BUILD = {
    "id": BUILD_ID,
    "arn": BUILD_ARN,
    "projectName": PROJECT_NAME,
    "buildStatus": "IN_PROGRESS",
    "currentPhase": "BUILD",
    "startTime": "2024-01-01T00:00:00Z",
    "endTime": None,
    "sourceVersion": "main",
    "logs": {"groupName": "/aws/codebuild/test"},
    "phases": [{"phaseType": "SUBMITTED"}],
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_project_result_model():
    p = ProjectResult(
        name="p1",
        arn="arn:...",
        source={"type": "S3"},
        environment={"type": "LINUX_CONTAINER"},
    )
    assert p.name == "p1"
    assert p.description is None
    assert p.artifacts is None
    assert p.service_role is None
    assert p.created is None
    assert p.last_modified is None
    assert p.extra == {}


def test_project_result_model_full():
    p = ProjectResult(
        name="p1",
        arn="arn:...",
        description="desc",
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        service_role=SERVICE_ROLE,
        created="2024-01-01",
        last_modified="2024-06-01",
        extra={"tags": []},
    )
    assert p.description == "desc"
    assert p.service_role == SERVICE_ROLE


def test_build_result_model():
    b = BuildResult(
        id="b1",
        arn="arn:...",
        project_name="proj",
        build_status="SUCCEEDED",
    )
    assert b.id == "b1"
    assert b.current_phase is None
    assert b.start_time is None
    assert b.end_time is None
    assert b.source_version is None
    assert b.logs is None
    assert b.extra == {}


def test_build_result_model_full():
    b = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="IN_PROGRESS",
        current_phase="BUILD",
        start_time="2024-01-01",
        end_time="2024-01-02",
        source_version="main",
        logs={"groupName": "/log"},
        extra={"phases": []},
    )
    assert b.current_phase == "BUILD"
    assert b.source_version == "main"


# ---------------------------------------------------------------------------
# create_project
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_create_project_success(mock_gc):
    client = MagicMock()
    client.create_project.return_value = {"project": _RAW_PROJECT}
    mock_gc.return_value = client

    result = create_project(
        PROJECT_NAME,
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        service_role=SERVICE_ROLE,
        description="A test project",
        region_name=REGION,
    )
    assert isinstance(result, ProjectResult)
    assert result.name == PROJECT_NAME
    assert result.description == "A test project"
    client.create_project.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_create_project_no_description(mock_gc):
    client = MagicMock()
    raw = {**_RAW_PROJECT, "description": None}
    client.create_project.return_value = {"project": raw}
    mock_gc.return_value = client

    result = create_project(
        PROJECT_NAME,
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        service_role=SERVICE_ROLE,
        region_name=REGION,
    )
    assert result.description is None


@patch("aws_util.codebuild.get_client")
def test_create_project_error(mock_gc):
    client = MagicMock()
    client.create_project.side_effect = ClientError(
        {"Error": {"Code": "ResourceAlreadyExistsException", "Message": "exists"}},
        "CreateProject",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="create_project failed"):
        create_project(
            PROJECT_NAME,
            source=_SOURCE,
            artifacts=_ARTIFACTS,
            environment=_ENVIRONMENT,
            service_role=SERVICE_ROLE,
        )


# ---------------------------------------------------------------------------
# batch_get_projects
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_batch_get_projects_success(mock_gc):
    client = MagicMock()
    client.batch_get_projects.return_value = {"projects": [_RAW_PROJECT]}
    mock_gc.return_value = client

    result = batch_get_projects([PROJECT_NAME], region_name=REGION)
    assert len(result) == 1
    assert result[0].name == PROJECT_NAME


@patch("aws_util.codebuild.get_client")
def test_batch_get_projects_empty(mock_gc):
    client = MagicMock()
    client.batch_get_projects.return_value = {"projects": []}
    mock_gc.return_value = client

    result = batch_get_projects(["nonexistent"])
    assert result == []


@patch("aws_util.codebuild.get_client")
def test_batch_get_projects_error(mock_gc):
    client = MagicMock()
    client.batch_get_projects.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "BatchGetProjects",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="batch_get_projects failed"):
        batch_get_projects([PROJECT_NAME])


# ---------------------------------------------------------------------------
# list_projects
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_list_projects_success(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"projects": ["proj-a", "proj-b"]}]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_projects(region_name=REGION)
    assert result == ["proj-a", "proj-b"]


@patch("aws_util.codebuild.get_client")
def test_list_projects_pagination(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"projects": ["proj-a"]},
        {"projects": ["proj-b"]},
    ]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_projects(sort_by="CREATED_TIME", sort_order="DESCENDING")
    assert result == ["proj-a", "proj-b"]


@patch("aws_util.codebuild.get_client")
def test_list_projects_error(mock_gc):
    client = MagicMock()
    client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}},
        "ListProjects",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="list_projects failed"):
        list_projects()


# ---------------------------------------------------------------------------
# update_project
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_update_project_success(mock_gc):
    client = MagicMock()
    updated = {**_RAW_PROJECT, "description": "Updated"}
    client.update_project.return_value = {"project": updated}
    mock_gc.return_value = client

    result = update_project(
        PROJECT_NAME,
        description="Updated",
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        region_name=REGION,
    )
    assert result.description == "Updated"


@patch("aws_util.codebuild.get_client")
def test_update_project_minimal(mock_gc):
    client = MagicMock()
    client.update_project.return_value = {"project": _RAW_PROJECT}
    mock_gc.return_value = client

    result = update_project(PROJECT_NAME, region_name=REGION)
    assert result.name == PROJECT_NAME
    call_kwargs = client.update_project.call_args[1]
    assert "source" not in call_kwargs
    assert "artifacts" not in call_kwargs
    assert "environment" not in call_kwargs
    assert "description" not in call_kwargs


@patch("aws_util.codebuild.get_client")
def test_update_project_error(mock_gc):
    client = MagicMock()
    client.update_project.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "UpdateProject",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="update_project failed"):
        update_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# delete_project
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_delete_project_success(mock_gc):
    client = MagicMock()
    client.delete_project.return_value = {}
    mock_gc.return_value = client

    delete_project(PROJECT_NAME, region_name=REGION)
    client.delete_project.assert_called_once_with(name=PROJECT_NAME)


@patch("aws_util.codebuild.get_client")
def test_delete_project_error(mock_gc):
    client = MagicMock()
    client.delete_project.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DeleteProject",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="delete_project failed"):
        delete_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# start_build
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_start_build_success(mock_gc):
    client = MagicMock()
    client.start_build.return_value = {"build": _RAW_BUILD}
    mock_gc.return_value = client

    result = start_build(PROJECT_NAME, region_name=REGION)
    assert isinstance(result, BuildResult)
    assert result.id == BUILD_ID
    assert result.build_status == "IN_PROGRESS"


@patch("aws_util.codebuild.get_client")
def test_start_build_with_overrides(mock_gc):
    client = MagicMock()
    client.start_build.return_value = {"build": _RAW_BUILD}
    mock_gc.return_value = client

    env_vars = [{"name": "FOO", "value": "bar", "type": "PLAINTEXT"}]
    result = start_build(
        PROJECT_NAME,
        source_version="feature-branch",
        environment_variables_override=env_vars,
        region_name=REGION,
    )
    assert result.id == BUILD_ID
    call_kwargs = client.start_build.call_args[1]
    assert call_kwargs["sourceVersion"] == "feature-branch"
    assert call_kwargs["environmentVariablesOverride"] == env_vars


@patch("aws_util.codebuild.get_client")
def test_start_build_error(mock_gc):
    client = MagicMock()
    client.start_build.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "StartBuild",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="start_build failed"):
        start_build(PROJECT_NAME)


# ---------------------------------------------------------------------------
# batch_get_builds
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_batch_get_builds_success(mock_gc):
    client = MagicMock()
    client.batch_get_builds.return_value = {"builds": [_RAW_BUILD]}
    mock_gc.return_value = client

    result = batch_get_builds([BUILD_ID], region_name=REGION)
    assert len(result) == 1
    assert result[0].id == BUILD_ID


@patch("aws_util.codebuild.get_client")
def test_batch_get_builds_empty(mock_gc):
    client = MagicMock()
    client.batch_get_builds.return_value = {"builds": []}
    mock_gc.return_value = client

    result = batch_get_builds(["nonexistent"])
    assert result == []


@patch("aws_util.codebuild.get_client")
def test_batch_get_builds_error(mock_gc):
    client = MagicMock()
    client.batch_get_builds.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad input"}},
        "BatchGetBuilds",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="batch_get_builds failed"):
        batch_get_builds([BUILD_ID])


# ---------------------------------------------------------------------------
# list_builds
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_list_builds_success(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"ids": [BUILD_ID, "proj:build-2"]}]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_builds(region_name=REGION)
    assert result == [BUILD_ID, "proj:build-2"]


@patch("aws_util.codebuild.get_client")
def test_list_builds_pagination(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"ids": [BUILD_ID]},
        {"ids": ["proj:build-2"]},
    ]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_builds(sort_order="ASCENDING")
    assert result == [BUILD_ID, "proj:build-2"]


@patch("aws_util.codebuild.get_client")
def test_list_builds_error(mock_gc):
    client = MagicMock()
    client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "InvalidInputException", "Message": "bad"}},
        "ListBuilds",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="list_builds failed"):
        list_builds()


# ---------------------------------------------------------------------------
# list_builds_for_project
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_list_builds_for_project_success(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"ids": [BUILD_ID]}]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_builds_for_project(PROJECT_NAME, region_name=REGION)
    assert result == [BUILD_ID]


@patch("aws_util.codebuild.get_client")
def test_list_builds_for_project_pagination(mock_gc):
    client = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"ids": [BUILD_ID]},
        {"ids": ["proj:build-2"]},
    ]
    client.get_paginator.return_value = paginator
    mock_gc.return_value = client

    result = list_builds_for_project(PROJECT_NAME, sort_order="ASCENDING")
    assert result == [BUILD_ID, "proj:build-2"]


@patch("aws_util.codebuild.get_client")
def test_list_builds_for_project_error(mock_gc):
    client = MagicMock()
    client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "ListBuildsForProject",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="list_builds_for_project failed"):
        list_builds_for_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# stop_build
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_stop_build_success(mock_gc):
    client = MagicMock()
    stopped = {**_RAW_BUILD, "buildStatus": "STOPPED"}
    client.stop_build.return_value = {"build": stopped}
    mock_gc.return_value = client

    result = stop_build(BUILD_ID, region_name=REGION)
    assert result.build_status == "STOPPED"


@patch("aws_util.codebuild.get_client")
def test_stop_build_error(mock_gc):
    client = MagicMock()
    client.stop_build.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "StopBuild",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="stop_build failed"):
        stop_build(BUILD_ID)


# ---------------------------------------------------------------------------
# retry_build
# ---------------------------------------------------------------------------


@patch("aws_util.codebuild.get_client")
def test_retry_build_success(mock_gc):
    client = MagicMock()
    retried = {**_RAW_BUILD, "id": "test-project:build-456"}
    client.retry_build.return_value = {"build": retried}
    mock_gc.return_value = client

    result = retry_build(BUILD_ID, region_name=REGION)
    assert result.id == "test-project:build-456"


@patch("aws_util.codebuild.get_client")
def test_retry_build_error(mock_gc):
    client = MagicMock()
    client.retry_build.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "RetryBuild",
    )
    mock_gc.return_value = client

    with pytest.raises(RuntimeError, match="retry_build failed"):
        retry_build(BUILD_ID)


# ---------------------------------------------------------------------------
# wait_for_build
# ---------------------------------------------------------------------------


def test_wait_for_build_already_succeeded(monkeypatch):
    succeeded = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="SUCCEEDED",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [succeeded],
    )
    result = wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)
    assert result.build_status == "SUCCEEDED"


def test_wait_for_build_stopped(monkeypatch):
    stopped = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="STOPPED",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [stopped],
    )
    result = wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)
    assert result.build_status == "STOPPED"


def test_wait_for_build_failed_raises(monkeypatch):
    failed = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="FAILED",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [failed],
    )
    with pytest.raises(RuntimeError, match="failed"):
        wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)


def test_wait_for_build_timeout(monkeypatch):
    running = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="IN_PROGRESS",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [running],
    )
    with pytest.raises(AwsTimeoutError, match="did not finish"):
        wait_for_build(BUILD_ID, timeout=0.0, poll_interval=0.0)


def test_wait_for_build_not_found(monkeypatch):
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [],
    )
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)


def test_wait_for_build_poll_loop(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_batch_get(ids, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 3:
            return [
                BuildResult(
                    id=BUILD_ID,
                    arn=BUILD_ARN,
                    project_name=PROJECT_NAME,
                    build_status="IN_PROGRESS",
                )
            ]
        return [
            BuildResult(
                id=BUILD_ID,
                arn=BUILD_ARN,
                project_name=PROJECT_NAME,
                build_status="SUCCEEDED",
            )
        ]

    monkeypatch.setattr(cb_mod, "batch_get_builds", fake_batch_get)
    result = wait_for_build(
        BUILD_ID, timeout=60.0, poll_interval=0.001, region_name=REGION
    )
    assert result.build_status == "SUCCEEDED"
    assert call_count["n"] == 3


def test_wait_for_build_fault_terminal(monkeypatch):
    fault = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="FAULT",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [fault],
    )
    result = wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)
    assert result.build_status == "FAULT"


def test_wait_for_build_timed_out_terminal(monkeypatch):
    timed_out = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="TIMED_OUT",
    )
    monkeypatch.setattr(
        cb_mod,
        "batch_get_builds",
        lambda ids, region_name=None: [timed_out],
    )
    result = wait_for_build(BUILD_ID, timeout=5.0, poll_interval=0.01)
    assert result.build_status == "TIMED_OUT"


# ---------------------------------------------------------------------------
# start_build_and_wait
# ---------------------------------------------------------------------------


def test_start_build_and_wait_success(monkeypatch):
    started = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="IN_PROGRESS",
    )
    finished = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="SUCCEEDED",
    )
    monkeypatch.setattr(cb_mod, "start_build", lambda *a, **kw: started)
    monkeypatch.setattr(cb_mod, "wait_for_build", lambda *a, **kw: finished)

    result = start_build_and_wait(
        PROJECT_NAME,
        source_version="main",
        environment_variables_override=[{"name": "X", "value": "1"}],
        timeout=60,
        poll_interval=1,
        region_name=REGION,
    )
    assert result.build_status == "SUCCEEDED"


def test_start_build_and_wait_no_overrides(monkeypatch):
    started = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="IN_PROGRESS",
    )
    finished = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="SUCCEEDED",
    )
    monkeypatch.setattr(cb_mod, "start_build", lambda *a, **kw: started)
    monkeypatch.setattr(cb_mod, "wait_for_build", lambda *a, **kw: finished)

    result = start_build_and_wait(PROJECT_NAME)
    assert result.build_status == "SUCCEEDED"


# ---------------------------------------------------------------------------
# _parse_project / _parse_build edge cases
# ---------------------------------------------------------------------------


def test_parse_project_minimal():
    from aws_util.codebuild import _parse_project

    raw = {"name": "p1", "arn": "arn:...", "source": {}, "environment": {}}
    p = _parse_project(raw)
    assert p.name == "p1"
    assert p.description is None
    assert p.artifacts is None
    assert p.service_role is None
    assert p.created is None
    assert p.last_modified is None


def test_parse_build_minimal():
    from aws_util.codebuild import _parse_build

    raw = {"id": "b1", "arn": "arn:..."}
    b = _parse_build(raw)
    assert b.id == "b1"
    assert b.project_name == ""
    assert b.build_status == "UNKNOWN"
    assert b.current_phase is None
    assert b.start_time is None
    assert b.end_time is None
    assert b.source_version is None
    assert b.logs is None


def test_parse_project_extra_fields():
    from aws_util.codebuild import _parse_project

    raw = {
        **_RAW_PROJECT,
        "webhook": {"url": "https://..."},
    }
    p = _parse_project(raw)
    assert "webhook" in p.extra
    assert "tags" in p.extra


def test_parse_build_extra_fields():
    from aws_util.codebuild import _parse_build

    raw = {
        **_RAW_BUILD,
        "cache": {"type": "NO_CACHE"},
    }
    b = _parse_build(raw)
    assert "cache" in b.extra
    assert "phases" in b.extra


@patch("aws_util.codebuild.get_client")
def test_batch_delete_builds(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_builds.return_value = {}
    batch_delete_builds([], region_name=REGION)
    mock_client.batch_delete_builds.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_delete_builds_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_delete_builds.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_builds",
    )
    with pytest.raises(RuntimeError, match="Failed to batch delete builds"):
        batch_delete_builds([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_build_batches(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_build_batches.return_value = {}
    batch_get_build_batches([], region_name=REGION)
    mock_client.batch_get_build_batches.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_build_batches_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_build_batches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_build_batches",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get build batches"):
        batch_get_build_batches([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_command_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_command_executions.return_value = {}
    batch_get_command_executions("test-sandbox_id", [], region_name=REGION)
    mock_client.batch_get_command_executions.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_command_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_command_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_command_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get command executions"):
        batch_get_command_executions("test-sandbox_id", [], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_fleets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_fleets.return_value = {}
    batch_get_fleets([], region_name=REGION)
    mock_client.batch_get_fleets.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_fleets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_fleets",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get fleets"):
        batch_get_fleets([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_report_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_report_groups.return_value = {}
    batch_get_report_groups([], region_name=REGION)
    mock_client.batch_get_report_groups.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_report_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_report_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_report_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get report groups"):
        batch_get_report_groups([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_reports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_reports.return_value = {}
    batch_get_reports([], region_name=REGION)
    mock_client.batch_get_reports.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_reports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_reports",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get reports"):
        batch_get_reports([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_batch_get_sandboxes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_sandboxes.return_value = {}
    batch_get_sandboxes([], region_name=REGION)
    mock_client.batch_get_sandboxes.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_batch_get_sandboxes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_sandboxes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_sandboxes",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get sandboxes"):
        batch_get_sandboxes([], region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_create_fleet(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet.return_value = {}
    create_fleet("test-name", 1, "test-environment_type", "test-compute_type", region_name=REGION)
    mock_client.create_fleet.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_create_fleet_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_fleet",
    )
    with pytest.raises(RuntimeError, match="Failed to create fleet"):
        create_fleet("test-name", 1, "test-environment_type", "test-compute_type", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_create_report_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_report_group.return_value = {}
    create_report_group("test-name", "test-type_value", {}, region_name=REGION)
    mock_client.create_report_group.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_create_report_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_report_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_report_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create report group"):
        create_report_group("test-name", "test-type_value", {}, region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_create_webhook(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_webhook.return_value = {}
    create_webhook("test-project_name", region_name=REGION)
    mock_client.create_webhook.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_create_webhook_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_webhook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_webhook",
    )
    with pytest.raises(RuntimeError, match="Failed to create webhook"):
        create_webhook("test-project_name", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_build_batch(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_build_batch.return_value = {}
    delete_build_batch("test-id", region_name=REGION)
    mock_client.delete_build_batch.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_build_batch_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_build_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_build_batch",
    )
    with pytest.raises(RuntimeError, match="Failed to delete build batch"):
        delete_build_batch("test-id", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_fleet(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet.return_value = {}
    delete_fleet("test-arn", region_name=REGION)
    mock_client.delete_fleet.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_fleet_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fleet",
    )
    with pytest.raises(RuntimeError, match="Failed to delete fleet"):
        delete_fleet("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_report(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_report.return_value = {}
    delete_report("test-arn", region_name=REGION)
    mock_client.delete_report.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_report_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_report",
    )
    with pytest.raises(RuntimeError, match="Failed to delete report"):
        delete_report("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_report_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_report_group.return_value = {}
    delete_report_group("test-arn", region_name=REGION)
    mock_client.delete_report_group.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_report_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_report_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_report_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete report group"):
        delete_report_group("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy.return_value = {}
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_source_credentials(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_source_credentials.return_value = {}
    delete_source_credentials("test-arn", region_name=REGION)
    mock_client.delete_source_credentials.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_source_credentials_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_source_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_source_credentials",
    )
    with pytest.raises(RuntimeError, match="Failed to delete source credentials"):
        delete_source_credentials("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_delete_webhook(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_webhook.return_value = {}
    delete_webhook("test-project_name", region_name=REGION)
    mock_client.delete_webhook.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_delete_webhook_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_webhook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_webhook",
    )
    with pytest.raises(RuntimeError, match="Failed to delete webhook"):
        delete_webhook("test-project_name", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_describe_code_coverages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_code_coverages.return_value = {}
    describe_code_coverages("test-report_arn", region_name=REGION)
    mock_client.describe_code_coverages.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_describe_code_coverages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_code_coverages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_code_coverages",
    )
    with pytest.raises(RuntimeError, match="Failed to describe code coverages"):
        describe_code_coverages("test-report_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_describe_test_cases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_cases.return_value = {}
    describe_test_cases("test-report_arn", region_name=REGION)
    mock_client.describe_test_cases.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_describe_test_cases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_test_cases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_test_cases",
    )
    with pytest.raises(RuntimeError, match="Failed to describe test cases"):
        describe_test_cases("test-report_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_get_report_group_trend(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_report_group_trend.return_value = {}
    get_report_group_trend("test-report_group_arn", "test-trend_field", region_name=REGION)
    mock_client.get_report_group_trend.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_get_report_group_trend_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_report_group_trend.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_report_group_trend",
    )
    with pytest.raises(RuntimeError, match="Failed to get report group trend"):
        get_report_group_trend("test-report_group_arn", "test-trend_field", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_get_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_policy.return_value = {}
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_get_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_import_source_credentials(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_source_credentials.return_value = {}
    import_source_credentials("test-token", "test-server_type", "test-auth_type", region_name=REGION)
    mock_client.import_source_credentials.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_import_source_credentials_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_source_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_source_credentials",
    )
    with pytest.raises(RuntimeError, match="Failed to import source credentials"):
        import_source_credentials("test-token", "test-server_type", "test-auth_type", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_invalidate_project_cache(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.invalidate_project_cache.return_value = {}
    invalidate_project_cache("test-project_name", region_name=REGION)
    mock_client.invalidate_project_cache.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_invalidate_project_cache_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.invalidate_project_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "invalidate_project_cache",
    )
    with pytest.raises(RuntimeError, match="Failed to invalidate project cache"):
        invalidate_project_cache("test-project_name", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_build_batches(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_build_batches.return_value = {}
    list_build_batches(region_name=REGION)
    mock_client.list_build_batches.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_build_batches_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_build_batches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_build_batches",
    )
    with pytest.raises(RuntimeError, match="Failed to list build batches"):
        list_build_batches(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_build_batches_for_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_build_batches_for_project.return_value = {}
    list_build_batches_for_project(region_name=REGION)
    mock_client.list_build_batches_for_project.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_build_batches_for_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_build_batches_for_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_build_batches_for_project",
    )
    with pytest.raises(RuntimeError, match="Failed to list build batches for project"):
        list_build_batches_for_project(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_command_executions_for_sandbox(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_command_executions_for_sandbox.return_value = {}
    list_command_executions_for_sandbox("test-sandbox_id", region_name=REGION)
    mock_client.list_command_executions_for_sandbox.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_command_executions_for_sandbox_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_command_executions_for_sandbox.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_command_executions_for_sandbox",
    )
    with pytest.raises(RuntimeError, match="Failed to list command executions for sandbox"):
        list_command_executions_for_sandbox("test-sandbox_id", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_curated_environment_images(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_curated_environment_images.return_value = {}
    list_curated_environment_images(region_name=REGION)
    mock_client.list_curated_environment_images.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_curated_environment_images_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_curated_environment_images.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_curated_environment_images",
    )
    with pytest.raises(RuntimeError, match="Failed to list curated environment images"):
        list_curated_environment_images(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_fleets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_fleets.return_value = {}
    list_fleets(region_name=REGION)
    mock_client.list_fleets.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_fleets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_fleets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_fleets",
    )
    with pytest.raises(RuntimeError, match="Failed to list fleets"):
        list_fleets(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_report_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_report_groups.return_value = {}
    list_report_groups(region_name=REGION)
    mock_client.list_report_groups.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_report_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_report_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_report_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to list report groups"):
        list_report_groups(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_reports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_reports.return_value = {}
    list_reports(region_name=REGION)
    mock_client.list_reports.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_reports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reports",
    )
    with pytest.raises(RuntimeError, match="Failed to list reports"):
        list_reports(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_reports_for_report_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_reports_for_report_group.return_value = {}
    list_reports_for_report_group("test-report_group_arn", region_name=REGION)
    mock_client.list_reports_for_report_group.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_reports_for_report_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_reports_for_report_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_reports_for_report_group",
    )
    with pytest.raises(RuntimeError, match="Failed to list reports for report group"):
        list_reports_for_report_group("test-report_group_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_sandboxes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sandboxes.return_value = {}
    list_sandboxes(region_name=REGION)
    mock_client.list_sandboxes.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_sandboxes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sandboxes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sandboxes",
    )
    with pytest.raises(RuntimeError, match="Failed to list sandboxes"):
        list_sandboxes(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_sandboxes_for_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sandboxes_for_project.return_value = {}
    list_sandboxes_for_project("test-project_name", region_name=REGION)
    mock_client.list_sandboxes_for_project.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_sandboxes_for_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sandboxes_for_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sandboxes_for_project",
    )
    with pytest.raises(RuntimeError, match="Failed to list sandboxes for project"):
        list_sandboxes_for_project("test-project_name", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_shared_projects(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_shared_projects.return_value = {}
    list_shared_projects(region_name=REGION)
    mock_client.list_shared_projects.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_shared_projects_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_shared_projects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_shared_projects",
    )
    with pytest.raises(RuntimeError, match="Failed to list shared projects"):
        list_shared_projects(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_shared_report_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_shared_report_groups.return_value = {}
    list_shared_report_groups(region_name=REGION)
    mock_client.list_shared_report_groups.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_shared_report_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_shared_report_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_shared_report_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to list shared report groups"):
        list_shared_report_groups(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_list_source_credentials(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_source_credentials.return_value = {}
    list_source_credentials(region_name=REGION)
    mock_client.list_source_credentials.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_list_source_credentials_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_source_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_source_credentials",
    )
    with pytest.raises(RuntimeError, match="Failed to list source credentials"):
        list_source_credentials(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_put_resource_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_resource_policy.return_value = {}
    put_resource_policy("test-policy", "test-resource_arn", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_put_resource_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-policy", "test-resource_arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_retry_build_batch(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.retry_build_batch.return_value = {}
    retry_build_batch(region_name=REGION)
    mock_client.retry_build_batch.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_retry_build_batch_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.retry_build_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retry_build_batch",
    )
    with pytest.raises(RuntimeError, match="Failed to retry build batch"):
        retry_build_batch(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_start_build_batch(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_build_batch.return_value = {}
    start_build_batch("test-project_name", region_name=REGION)
    mock_client.start_build_batch.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_start_build_batch_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_build_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_build_batch",
    )
    with pytest.raises(RuntimeError, match="Failed to start build batch"):
        start_build_batch("test-project_name", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_start_command_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_command_execution.return_value = {}
    start_command_execution("test-sandbox_id", "test-command", region_name=REGION)
    mock_client.start_command_execution.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_start_command_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_command_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_command_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to start command execution"):
        start_command_execution("test-sandbox_id", "test-command", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_start_sandbox(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_sandbox.return_value = {}
    start_sandbox(region_name=REGION)
    mock_client.start_sandbox.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_start_sandbox_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_sandbox.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_sandbox",
    )
    with pytest.raises(RuntimeError, match="Failed to start sandbox"):
        start_sandbox(region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_start_sandbox_connection(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_sandbox_connection.return_value = {}
    start_sandbox_connection("test-sandbox_id", region_name=REGION)
    mock_client.start_sandbox_connection.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_start_sandbox_connection_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_sandbox_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_sandbox_connection",
    )
    with pytest.raises(RuntimeError, match="Failed to start sandbox connection"):
        start_sandbox_connection("test-sandbox_id", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_stop_build_batch(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_build_batch.return_value = {}
    stop_build_batch("test-id", region_name=REGION)
    mock_client.stop_build_batch.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_stop_build_batch_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_build_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_build_batch",
    )
    with pytest.raises(RuntimeError, match="Failed to stop build batch"):
        stop_build_batch("test-id", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_stop_sandbox(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_sandbox.return_value = {}
    stop_sandbox("test-id", region_name=REGION)
    mock_client.stop_sandbox.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_stop_sandbox_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_sandbox.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_sandbox",
    )
    with pytest.raises(RuntimeError, match="Failed to stop sandbox"):
        stop_sandbox("test-id", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_update_fleet(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_fleet.return_value = {}
    update_fleet("test-arn", region_name=REGION)
    mock_client.update_fleet.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_update_fleet_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_fleet.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_fleet",
    )
    with pytest.raises(RuntimeError, match="Failed to update fleet"):
        update_fleet("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_update_project_visibility(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project_visibility.return_value = {}
    update_project_visibility("test-project_arn", "test-project_visibility", region_name=REGION)
    mock_client.update_project_visibility.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_update_project_visibility_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project_visibility.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_project_visibility",
    )
    with pytest.raises(RuntimeError, match="Failed to update project visibility"):
        update_project_visibility("test-project_arn", "test-project_visibility", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_update_report_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_report_group.return_value = {}
    update_report_group("test-arn", region_name=REGION)
    mock_client.update_report_group.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_update_report_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_report_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_report_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update report group"):
        update_report_group("test-arn", region_name=REGION)


@patch("aws_util.codebuild.get_client")
def test_update_webhook(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_webhook.return_value = {}
    update_webhook("test-project_name", region_name=REGION)
    mock_client.update_webhook.assert_called_once()


@patch("aws_util.codebuild.get_client")
def test_update_webhook_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_webhook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_webhook",
    )
    with pytest.raises(RuntimeError, match="Failed to update webhook"):
        update_webhook("test-project_name", region_name=REGION)


def test_create_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import create_fleet
    mock_client = MagicMock()
    mock_client.create_fleet.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    create_fleet("test-name", "test-base_capacity", "test-environment_type", "test-compute_type", compute_configuration={}, scaling_configuration={}, overflow_behavior="test-overflow_behavior", vpc_config={}, proxy_configuration={}, image_id="test-image_id", fleet_service_role="test-fleet_service_role", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_fleet.assert_called_once()

def test_create_report_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import create_report_group
    mock_client = MagicMock()
    mock_client.create_report_group.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    create_report_group("test-name", "test-type_value", 1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_report_group.assert_called_once()

def test_create_webhook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import create_webhook
    mock_client = MagicMock()
    mock_client.create_webhook.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    create_webhook("test-project_name", branch_filter=[{}], filter_groups="test-filter_groups", build_type="test-build_type", manual_creation="test-manual_creation", scope_configuration={}, pull_request_build_policy="{}", region_name="us-east-1")
    mock_client.create_webhook.assert_called_once()

def test_delete_report_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import delete_report_group
    mock_client = MagicMock()
    mock_client.delete_report_group.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    delete_report_group("test-arn", delete_reports=True, region_name="us-east-1")
    mock_client.delete_report_group.assert_called_once()

def test_describe_code_coverages_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import describe_code_coverages
    mock_client = MagicMock()
    mock_client.describe_code_coverages.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    describe_code_coverages(1, next_token="test-next_token", max_results=1, sort_order="test-sort_order", sort_by="test-sort_by", min_line_coverage_percentage="test-min_line_coverage_percentage", max_line_coverage_percentage=1, region_name="us-east-1")
    mock_client.describe_code_coverages.assert_called_once()

def test_describe_test_cases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import describe_test_cases
    mock_client = MagicMock()
    mock_client.describe_test_cases.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    describe_test_cases(1, next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.describe_test_cases.assert_called_once()

def test_get_report_group_trend_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import get_report_group_trend
    mock_client = MagicMock()
    mock_client.get_report_group_trend.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    get_report_group_trend(1, "test-trend_field", num_of_reports=1, region_name="us-east-1")
    mock_client.get_report_group_trend.assert_called_once()

def test_import_source_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import import_source_credentials
    mock_client = MagicMock()
    mock_client.import_source_credentials.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    import_source_credentials("test-token", "test-server_type", "test-auth_type", username="test-username", should_overwrite="test-should_overwrite", region_name="us-east-1")
    mock_client.import_source_credentials.assert_called_once()

def test_list_build_batches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_build_batches
    mock_client = MagicMock()
    mock_client.list_build_batches.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_build_batches(filter="test-filter", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_build_batches.assert_called_once()

def test_list_build_batches_for_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_build_batches_for_project
    mock_client = MagicMock()
    mock_client.list_build_batches_for_project.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_build_batches_for_project(project_name="test-project_name", filter="test-filter", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_build_batches_for_project.assert_called_once()

def test_list_command_executions_for_sandbox_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_command_executions_for_sandbox
    mock_client = MagicMock()
    mock_client.list_command_executions_for_sandbox.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_command_executions_for_sandbox("test-sandbox_id", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_command_executions_for_sandbox.assert_called_once()

def test_list_fleets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_fleets
    mock_client = MagicMock()
    mock_client.list_fleets.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_fleets(next_token="test-next_token", max_results=1, sort_order="test-sort_order", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.list_fleets.assert_called_once()

def test_list_report_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_report_groups
    mock_client = MagicMock()
    mock_client.list_report_groups.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_report_groups(sort_order="test-sort_order", sort_by="test-sort_by", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_report_groups.assert_called_once()

def test_list_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_reports
    mock_client = MagicMock()
    mock_client.list_reports.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_reports(sort_order="test-sort_order", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.list_reports.assert_called_once()

def test_list_reports_for_report_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_reports_for_report_group
    mock_client = MagicMock()
    mock_client.list_reports_for_report_group.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_reports_for_report_group(1, next_token="test-next_token", sort_order="test-sort_order", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.list_reports_for_report_group.assert_called_once()

def test_list_sandboxes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_sandboxes
    mock_client = MagicMock()
    mock_client.list_sandboxes.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_sandboxes(max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sandboxes.assert_called_once()

def test_list_sandboxes_for_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_sandboxes_for_project
    mock_client = MagicMock()
    mock_client.list_sandboxes_for_project.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_sandboxes_for_project("test-project_name", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sandboxes_for_project.assert_called_once()

def test_list_shared_projects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_shared_projects
    mock_client = MagicMock()
    mock_client.list_shared_projects.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_shared_projects(sort_by="test-sort_by", sort_order="test-sort_order", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_shared_projects.assert_called_once()

def test_list_shared_report_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import list_shared_report_groups
    mock_client = MagicMock()
    mock_client.list_shared_report_groups.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    list_shared_report_groups(sort_order="test-sort_order", sort_by="test-sort_by", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_shared_report_groups.assert_called_once()

def test_retry_build_batch_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import retry_build_batch
    mock_client = MagicMock()
    mock_client.retry_build_batch.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    retry_build_batch(id="test-id", idempotency_token="test-idempotency_token", retry_type="test-retry_type", region_name="us-east-1")
    mock_client.retry_build_batch.assert_called_once()

def test_start_build_batch_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import start_build_batch
    mock_client = MagicMock()
    mock_client.start_build_batch.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    start_build_batch("test-project_name", secondary_sources_override="test-secondary_sources_override", secondary_sources_version_override="test-secondary_sources_version_override", source_version="test-source_version", artifacts_override="test-artifacts_override", secondary_artifacts_override="test-secondary_artifacts_override", environment_variables_override="test-environment_variables_override", source_type_override="test-source_type_override", source_location_override="test-source_location_override", source_auth_override="test-source_auth_override", git_clone_depth_override="test-git_clone_depth_override", git_submodules_config_override={}, buildspec_override="test-buildspec_override", insecure_ssl_override="test-insecure_ssl_override", report_build_batch_status_override=1, environment_type_override="test-environment_type_override", image_override="test-image_override", compute_type_override="test-compute_type_override", certificate_override="test-certificate_override", cache_override="test-cache_override", service_role_override="test-service_role_override", privileged_mode_override="test-privileged_mode_override", build_timeout_in_minutes_override=1, queued_timeout_in_minutes_override=1, encryption_key_override="test-encryption_key_override", idempotency_token="test-idempotency_token", logs_config_override={}, registry_credential_override="test-registry_credential_override", image_pull_credentials_type_override="test-image_pull_credentials_type_override", build_batch_config_override={}, debug_session_enabled="test-debug_session_enabled", region_name="us-east-1")
    mock_client.start_build_batch.assert_called_once()

def test_start_command_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import start_command_execution
    mock_client = MagicMock()
    mock_client.start_command_execution.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    start_command_execution("test-sandbox_id", "test-command", type_value="test-type_value", region_name="us-east-1")
    mock_client.start_command_execution.assert_called_once()

def test_start_sandbox_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import start_sandbox
    mock_client = MagicMock()
    mock_client.start_sandbox.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    start_sandbox(project_name="test-project_name", idempotency_token="test-idempotency_token", region_name="us-east-1")
    mock_client.start_sandbox.assert_called_once()

def test_update_fleet_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import update_fleet
    mock_client = MagicMock()
    mock_client.update_fleet.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    update_fleet("test-arn", base_capacity="test-base_capacity", environment_type="test-environment_type", compute_type="test-compute_type", compute_configuration={}, scaling_configuration={}, overflow_behavior="test-overflow_behavior", vpc_config={}, proxy_configuration={}, image_id="test-image_id", fleet_service_role="test-fleet_service_role", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.update_fleet.assert_called_once()

def test_update_project_visibility_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import update_project_visibility
    mock_client = MagicMock()
    mock_client.update_project_visibility.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    update_project_visibility("test-project_arn", "test-project_visibility", resource_access_role="test-resource_access_role", region_name="us-east-1")
    mock_client.update_project_visibility.assert_called_once()

def test_update_report_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import update_report_group
    mock_client = MagicMock()
    mock_client.update_report_group.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    update_report_group("test-arn", export_config=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.update_report_group.assert_called_once()

def test_update_webhook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codebuild import update_webhook
    mock_client = MagicMock()
    mock_client.update_webhook.return_value = {}
    monkeypatch.setattr("aws_util.codebuild.get_client", lambda *a, **kw: mock_client)
    update_webhook("test-project_name", branch_filter=[{}], rotate_secret="test-rotate_secret", filter_groups="test-filter_groups", build_type="test-build_type", pull_request_build_policy="{}", region_name="us-east-1")
    mock_client.update_webhook.assert_called_once()
