"""Tests for aws_util.aio.codebuild module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codebuild import (
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
}

_RAW_BUILD = {
    "id": BUILD_ID,
    "arn": BUILD_ARN,
    "projectName": PROJECT_NAME,
    "buildStatus": "IN_PROGRESS",
    "currentPhase": "BUILD",
    "startTime": "2024-01-01T00:00:00Z",
    "sourceVersion": "main",
    "logs": {"groupName": "/aws/codebuild/test"},
}


# ---------------------------------------------------------------------------
# create_project
# ---------------------------------------------------------------------------


async def test_create_project_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"project": _RAW_PROJECT}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await create_project(
        PROJECT_NAME,
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        service_role=SERVICE_ROLE,
        description="A test project",
    )
    assert isinstance(result, ProjectResult)
    assert result.name == PROJECT_NAME


async def test_create_project_no_description(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    raw = {**_RAW_PROJECT, "description": None}
    mock_client.call.return_value = {"project": raw}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await create_project(
        PROJECT_NAME,
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
        service_role=SERVICE_ROLE,
    )
    assert result.description is None


async def test_create_project_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_project(
            PROJECT_NAME,
            source=_SOURCE,
            artifacts=_ARTIFACTS,
            environment=_ENVIRONMENT,
            service_role=SERVICE_ROLE,
        )


async def test_create_project_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_project failed"):
        await create_project(
            PROJECT_NAME,
            source=_SOURCE,
            artifacts=_ARTIFACTS,
            environment=_ENVIRONMENT,
            service_role=SERVICE_ROLE,
        )


# ---------------------------------------------------------------------------
# batch_get_projects
# ---------------------------------------------------------------------------


async def test_batch_get_projects_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"projects": [_RAW_PROJECT]}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await batch_get_projects([PROJECT_NAME])
    assert len(result) == 1
    assert result[0].name == PROJECT_NAME


async def test_batch_get_projects_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"projects": []}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await batch_get_projects(["nonexistent"])
    assert result == []


async def test_batch_get_projects_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_projects([PROJECT_NAME])


async def test_batch_get_projects_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="batch_get_projects failed"):
        await batch_get_projects([PROJECT_NAME])


# ---------------------------------------------------------------------------
# list_projects
# ---------------------------------------------------------------------------


async def test_list_projects_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"projects": ["proj-a", "proj-b"]}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_projects()
    assert result == ["proj-a", "proj-b"]


async def test_list_projects_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"projects": ["proj-a"], "nextToken": "tok"}
        return {"projects": ["proj-b"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_projects(
        sort_by="CREATED_TIME", sort_order="DESCENDING"
    )
    assert result == ["proj-a", "proj-b"]


async def test_list_projects_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_projects()


async def test_list_projects_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_projects failed"):
        await list_projects()


# ---------------------------------------------------------------------------
# update_project
# ---------------------------------------------------------------------------


async def test_update_project_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    updated = {**_RAW_PROJECT, "description": "Updated"}
    mock_client.call.return_value = {"project": updated}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await update_project(
        PROJECT_NAME,
        description="Updated",
        source=_SOURCE,
        artifacts=_ARTIFACTS,
        environment=_ENVIRONMENT,
    )
    assert result.description == "Updated"


async def test_update_project_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"project": _RAW_PROJECT}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await update_project(PROJECT_NAME)
    assert result.name == PROJECT_NAME


async def test_update_project_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_project(PROJECT_NAME)


async def test_update_project_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="update_project failed"):
        await update_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# delete_project
# ---------------------------------------------------------------------------


async def test_delete_project_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    await delete_project(PROJECT_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_project_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_project(PROJECT_NAME)


async def test_delete_project_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_project failed"):
        await delete_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# start_build
# ---------------------------------------------------------------------------


async def test_start_build_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"build": _RAW_BUILD}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await start_build(PROJECT_NAME)
    assert isinstance(result, BuildResult)
    assert result.id == BUILD_ID


async def test_start_build_with_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"build": _RAW_BUILD}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await start_build(
        PROJECT_NAME,
        source_version="feature-branch",
        environment_variables_override=[{"name": "X", "value": "1"}],
    )
    assert result.id == BUILD_ID


async def test_start_build_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_build(PROJECT_NAME)


async def test_start_build_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_build failed"):
        await start_build(PROJECT_NAME)


# ---------------------------------------------------------------------------
# batch_get_builds
# ---------------------------------------------------------------------------


async def test_batch_get_builds_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"builds": [_RAW_BUILD]}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await batch_get_builds([BUILD_ID])
    assert len(result) == 1
    assert result[0].id == BUILD_ID


async def test_batch_get_builds_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"builds": []}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await batch_get_builds(["nonexistent"])
    assert result == []


async def test_batch_get_builds_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_builds([BUILD_ID])


async def test_batch_get_builds_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="batch_get_builds failed"):
        await batch_get_builds([BUILD_ID])


# ---------------------------------------------------------------------------
# list_builds
# ---------------------------------------------------------------------------


async def test_list_builds_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"ids": [BUILD_ID, "proj:build-2"]}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_builds()
    assert result == [BUILD_ID, "proj:build-2"]


async def test_list_builds_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"ids": [BUILD_ID], "nextToken": "tok"}
        return {"ids": ["proj:build-2"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_builds(sort_order="ASCENDING")
    assert result == [BUILD_ID, "proj:build-2"]


async def test_list_builds_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_builds()


async def test_list_builds_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_builds failed"):
        await list_builds()


# ---------------------------------------------------------------------------
# list_builds_for_project
# ---------------------------------------------------------------------------


async def test_list_builds_for_project_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"ids": [BUILD_ID]}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_builds_for_project(PROJECT_NAME)
    assert result == [BUILD_ID]


async def test_list_builds_for_project_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"ids": [BUILD_ID], "nextToken": "tok"}
        return {"ids": ["proj:build-2"]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await list_builds_for_project(
        PROJECT_NAME, sort_order="ASCENDING"
    )
    assert result == [BUILD_ID, "proj:build-2"]


async def test_list_builds_for_project_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_builds_for_project(PROJECT_NAME)


async def test_list_builds_for_project_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_builds_for_project failed"):
        await list_builds_for_project(PROJECT_NAME)


# ---------------------------------------------------------------------------
# stop_build
# ---------------------------------------------------------------------------


async def test_stop_build_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    stopped = {**_RAW_BUILD, "buildStatus": "STOPPED"}
    mock_client.call.return_value = {"build": stopped}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await stop_build(BUILD_ID)
    assert result.build_status == "STOPPED"


async def test_stop_build_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_build(BUILD_ID)


async def test_stop_build_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="stop_build failed"):
        await stop_build(BUILD_ID)


# ---------------------------------------------------------------------------
# retry_build
# ---------------------------------------------------------------------------


async def test_retry_build_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    retried = {**_RAW_BUILD, "id": "test-project:build-456"}
    mock_client.call.return_value = {"build": retried}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await retry_build(BUILD_ID)
    assert result.id == "test-project:build-456"


async def test_retry_build_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retry_build(BUILD_ID)


async def test_retry_build_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="retry_build failed"):
        await retry_build(BUILD_ID)


# ---------------------------------------------------------------------------
# wait_for_build
# ---------------------------------------------------------------------------


async def test_wait_for_build_immediate_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    succeeded = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="SUCCEEDED",
    )

    async def _fake_batch_get(ids, region_name=None):
        return [succeeded]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codebuild.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_build(BUILD_ID)
    assert result.build_status == "SUCCEEDED"


async def test_wait_for_build_becomes_finished(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_count = 0

    async def _fake_batch_get(ids, region_name=None):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
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

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codebuild.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_build(BUILD_ID, timeout=60.0)
    assert result.build_status == "SUCCEEDED"


async def test_wait_for_build_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_batch_get(ids, region_name=None):
        return [
            BuildResult(
                id=BUILD_ID,
                arn=BUILD_ARN,
                project_name=PROJECT_NAME,
                build_status="IN_PROGRESS",
            )
        ]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codebuild.asyncio.sleep", AsyncMock()
    )
    with pytest.raises(AwsTimeoutError, match="did not finish"):
        await wait_for_build(BUILD_ID, timeout=0.0)


async def test_wait_for_build_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_batch_get(ids, region_name=None):
        return [
            BuildResult(
                id=BUILD_ID,
                arn=BUILD_ARN,
                project_name=PROJECT_NAME,
                build_status="FAILED",
            )
        ]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    with pytest.raises(RuntimeError, match="failed"):
        await wait_for_build(BUILD_ID)


async def test_wait_for_build_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_batch_get(ids, region_name=None):
        return []

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_build(BUILD_ID)


async def test_wait_for_build_stopped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stopped = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="STOPPED",
    )

    async def _fake_batch_get(ids, region_name=None):
        return [stopped]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    result = await wait_for_build(BUILD_ID)
    assert result.build_status == "STOPPED"


async def test_wait_for_build_fault(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fault = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="FAULT",
    )

    async def _fake_batch_get(ids, region_name=None):
        return [fault]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    result = await wait_for_build(BUILD_ID)
    assert result.build_status == "FAULT"


async def test_wait_for_build_timed_out_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    timed_out = BuildResult(
        id=BUILD_ID,
        arn=BUILD_ARN,
        project_name=PROJECT_NAME,
        build_status="TIMED_OUT",
    )

    async def _fake_batch_get(ids, region_name=None):
        return [timed_out]

    monkeypatch.setattr(
        "aws_util.aio.codebuild.batch_get_builds", _fake_batch_get
    )
    result = await wait_for_build(BUILD_ID)
    assert result.build_status == "TIMED_OUT"


# ---------------------------------------------------------------------------
# start_build_and_wait
# ---------------------------------------------------------------------------


async def test_start_build_and_wait_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

    async def _fake_start(pn, **kwargs):
        return started

    async def _fake_wait(bid, **kwargs):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codebuild.start_build", _fake_start
    )
    monkeypatch.setattr(
        "aws_util.aio.codebuild.wait_for_build", _fake_wait
    )
    result = await start_build_and_wait(
        PROJECT_NAME,
        source_version="main",
        environment_variables_override=[{"name": "X", "value": "1"}],
    )
    assert result.build_status == "SUCCEEDED"


async def test_start_build_and_wait_no_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

    async def _fake_start(pn, **kwargs):
        return started

    async def _fake_wait(bid, **kwargs):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codebuild.start_build", _fake_start
    )
    monkeypatch.setattr(
        "aws_util.aio.codebuild.wait_for_build", _fake_wait
    )
    result = await start_build_and_wait(PROJECT_NAME)
    assert result.build_status == "SUCCEEDED"


async def test_batch_delete_builds(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_builds([], )
    mock_client.call.assert_called_once()


async def test_batch_delete_builds_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_builds([], )


async def test_batch_get_build_batches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_build_batches([], )
    mock_client.call.assert_called_once()


async def test_batch_get_build_batches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_build_batches([], )


async def test_batch_get_command_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_command_executions("test-sandbox_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_command_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_command_executions("test-sandbox_id", [], )


async def test_batch_get_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_fleets([], )
    mock_client.call.assert_called_once()


async def test_batch_get_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_fleets([], )


async def test_batch_get_report_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_report_groups([], )
    mock_client.call.assert_called_once()


async def test_batch_get_report_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_report_groups([], )


async def test_batch_get_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_reports([], )
    mock_client.call.assert_called_once()


async def test_batch_get_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_reports([], )


async def test_batch_get_sandboxes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_sandboxes([], )
    mock_client.call.assert_called_once()


async def test_batch_get_sandboxes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_sandboxes([], )


async def test_create_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_fleet("test-name", 1, "test-environment_type", "test-compute_type", )
    mock_client.call.assert_called_once()


async def test_create_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_fleet("test-name", 1, "test-environment_type", "test-compute_type", )


async def test_create_report_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_report_group("test-name", "test-type_value", {}, )
    mock_client.call.assert_called_once()


async def test_create_report_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_report_group("test-name", "test-type_value", {}, )


async def test_create_webhook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_webhook("test-project_name", )
    mock_client.call.assert_called_once()


async def test_create_webhook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_webhook("test-project_name", )


async def test_delete_build_batch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_build_batch("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_build_batch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_build_batch("test-id", )


async def test_delete_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fleet("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fleet("test-arn", )


async def test_delete_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_report("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_report("test-arn", )


async def test_delete_report_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_report_group("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_report_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_report_group("test-arn", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_source_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_source_credentials("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_source_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_source_credentials("test-arn", )


async def test_delete_webhook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_webhook("test-project_name", )
    mock_client.call.assert_called_once()


async def test_delete_webhook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_webhook("test-project_name", )


async def test_describe_code_coverages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_code_coverages("test-report_arn", )
    mock_client.call.assert_called_once()


async def test_describe_code_coverages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_code_coverages("test-report_arn", )


async def test_describe_test_cases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_test_cases("test-report_arn", )
    mock_client.call.assert_called_once()


async def test_describe_test_cases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_test_cases("test-report_arn", )


async def test_get_report_group_trend(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_report_group_trend("test-report_group_arn", "test-trend_field", )
    mock_client.call.assert_called_once()


async def test_get_report_group_trend_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_report_group_trend("test-report_group_arn", "test-trend_field", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_import_source_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_source_credentials("test-token", "test-server_type", "test-auth_type", )
    mock_client.call.assert_called_once()


async def test_import_source_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_source_credentials("test-token", "test-server_type", "test-auth_type", )


async def test_invalidate_project_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await invalidate_project_cache("test-project_name", )
    mock_client.call.assert_called_once()


async def test_invalidate_project_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await invalidate_project_cache("test-project_name", )


async def test_list_build_batches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_build_batches()
    mock_client.call.assert_called_once()


async def test_list_build_batches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_build_batches()


async def test_list_build_batches_for_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_build_batches_for_project()
    mock_client.call.assert_called_once()


async def test_list_build_batches_for_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_build_batches_for_project()


async def test_list_command_executions_for_sandbox(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_command_executions_for_sandbox("test-sandbox_id", )
    mock_client.call.assert_called_once()


async def test_list_command_executions_for_sandbox_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_command_executions_for_sandbox("test-sandbox_id", )


async def test_list_curated_environment_images(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_curated_environment_images()
    mock_client.call.assert_called_once()


async def test_list_curated_environment_images_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_curated_environment_images()


async def test_list_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_fleets()
    mock_client.call.assert_called_once()


async def test_list_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_fleets()


async def test_list_report_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_report_groups()
    mock_client.call.assert_called_once()


async def test_list_report_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_report_groups()


async def test_list_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_reports()
    mock_client.call.assert_called_once()


async def test_list_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_reports()


async def test_list_reports_for_report_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_reports_for_report_group("test-report_group_arn", )
    mock_client.call.assert_called_once()


async def test_list_reports_for_report_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_reports_for_report_group("test-report_group_arn", )


async def test_list_sandboxes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sandboxes()
    mock_client.call.assert_called_once()


async def test_list_sandboxes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sandboxes()


async def test_list_sandboxes_for_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sandboxes_for_project("test-project_name", )
    mock_client.call.assert_called_once()


async def test_list_sandboxes_for_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sandboxes_for_project("test-project_name", )


async def test_list_shared_projects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_shared_projects()
    mock_client.call.assert_called_once()


async def test_list_shared_projects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_shared_projects()


async def test_list_shared_report_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_shared_report_groups()
    mock_client.call.assert_called_once()


async def test_list_shared_report_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_shared_report_groups()


async def test_list_source_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_source_credentials()
    mock_client.call.assert_called_once()


async def test_list_source_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_source_credentials()


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-policy", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-policy", "test-resource_arn", )


async def test_retry_build_batch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await retry_build_batch()
    mock_client.call.assert_called_once()


async def test_retry_build_batch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retry_build_batch()


async def test_start_build_batch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_build_batch("test-project_name", )
    mock_client.call.assert_called_once()


async def test_start_build_batch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_build_batch("test-project_name", )


async def test_start_command_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_command_execution("test-sandbox_id", "test-command", )
    mock_client.call.assert_called_once()


async def test_start_command_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_command_execution("test-sandbox_id", "test-command", )


async def test_start_sandbox(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_sandbox()
    mock_client.call.assert_called_once()


async def test_start_sandbox_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_sandbox()


async def test_start_sandbox_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_sandbox_connection("test-sandbox_id", )
    mock_client.call.assert_called_once()


async def test_start_sandbox_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_sandbox_connection("test-sandbox_id", )


async def test_stop_build_batch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_build_batch("test-id", )
    mock_client.call.assert_called_once()


async def test_stop_build_batch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_build_batch("test-id", )


async def test_stop_sandbox(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_sandbox("test-id", )
    mock_client.call.assert_called_once()


async def test_stop_sandbox_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_sandbox("test-id", )


async def test_update_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_fleet("test-arn", )
    mock_client.call.assert_called_once()


async def test_update_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_fleet("test-arn", )


async def test_update_project_visibility(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_project_visibility("test-project_arn", "test-project_visibility", )
    mock_client.call.assert_called_once()


async def test_update_project_visibility_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_project_visibility("test-project_arn", "test-project_visibility", )


async def test_update_report_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_report_group("test-arn", )
    mock_client.call.assert_called_once()


async def test_update_report_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_report_group("test-arn", )


async def test_update_webhook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_webhook("test-project_name", )
    mock_client.call.assert_called_once()


async def test_update_webhook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codebuild.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_webhook("test-project_name", )


@pytest.mark.asyncio
async def test_create_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import create_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await create_fleet("test-name", "test-base_capacity", "test-environment_type", "test-compute_type", compute_configuration={}, scaling_configuration={}, overflow_behavior="test-overflow_behavior", vpc_config={}, proxy_configuration={}, image_id="test-image_id", fleet_service_role="test-fleet_service_role", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_report_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import create_report_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await create_report_group("test-name", "test-type_value", 1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_webhook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import create_webhook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await create_webhook("test-project_name", branch_filter=[{}], filter_groups="test-filter_groups", build_type="test-build_type", manual_creation="test-manual_creation", scope_configuration={}, pull_request_build_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_report_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import delete_report_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await delete_report_group("test-arn", delete_reports=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_code_coverages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import describe_code_coverages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await describe_code_coverages(1, next_token="test-next_token", max_results=1, sort_order="test-sort_order", sort_by="test-sort_by", min_line_coverage_percentage="test-min_line_coverage_percentage", max_line_coverage_percentage=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_test_cases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import describe_test_cases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await describe_test_cases(1, next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_report_group_trend_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import get_report_group_trend
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await get_report_group_trend(1, "test-trend_field", num_of_reports=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_source_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import import_source_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await import_source_credentials("test-token", "test-server_type", "test-auth_type", username="test-username", should_overwrite="test-should_overwrite", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_build_batches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_build_batches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_build_batches(filter="test-filter", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_build_batches_for_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_build_batches_for_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_build_batches_for_project(project_name="test-project_name", filter="test-filter", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_command_executions_for_sandbox_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_command_executions_for_sandbox
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_command_executions_for_sandbox("test-sandbox_id", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_fleets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_fleets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_fleets(next_token="test-next_token", max_results=1, sort_order="test-sort_order", sort_by="test-sort_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_report_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_report_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_report_groups(sort_order="test-sort_order", sort_by="test-sort_by", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_reports(sort_order="test-sort_order", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_reports_for_report_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_reports_for_report_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_reports_for_report_group(1, next_token="test-next_token", sort_order="test-sort_order", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sandboxes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_sandboxes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_sandboxes(max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sandboxes_for_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_sandboxes_for_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_sandboxes_for_project("test-project_name", max_results=1, sort_order="test-sort_order", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_shared_projects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_shared_projects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_shared_projects(sort_by="test-sort_by", sort_order="test-sort_order", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_shared_report_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import list_shared_report_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await list_shared_report_groups(sort_order="test-sort_order", sort_by="test-sort_by", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_retry_build_batch_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import retry_build_batch
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await retry_build_batch(id="test-id", idempotency_token="test-idempotency_token", retry_type="test-retry_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_build_batch_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import start_build_batch
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await start_build_batch("test-project_name", secondary_sources_override="test-secondary_sources_override", secondary_sources_version_override="test-secondary_sources_version_override", source_version="test-source_version", artifacts_override="test-artifacts_override", secondary_artifacts_override="test-secondary_artifacts_override", environment_variables_override="test-environment_variables_override", source_type_override="test-source_type_override", source_location_override="test-source_location_override", source_auth_override="test-source_auth_override", git_clone_depth_override="test-git_clone_depth_override", git_submodules_config_override={}, buildspec_override="test-buildspec_override", insecure_ssl_override="test-insecure_ssl_override", report_build_batch_status_override=1, environment_type_override="test-environment_type_override", image_override="test-image_override", compute_type_override="test-compute_type_override", certificate_override="test-certificate_override", cache_override="test-cache_override", service_role_override="test-service_role_override", privileged_mode_override="test-privileged_mode_override", build_timeout_in_minutes_override=1, queued_timeout_in_minutes_override=1, encryption_key_override="test-encryption_key_override", idempotency_token="test-idempotency_token", logs_config_override={}, registry_credential_override="test-registry_credential_override", image_pull_credentials_type_override="test-image_pull_credentials_type_override", build_batch_config_override={}, debug_session_enabled="test-debug_session_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_command_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import start_command_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await start_command_execution("test-sandbox_id", "test-command", type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_sandbox_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import start_sandbox
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await start_sandbox(project_name="test-project_name", idempotency_token="test-idempotency_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_fleet_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import update_fleet
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await update_fleet("test-arn", base_capacity="test-base_capacity", environment_type="test-environment_type", compute_type="test-compute_type", compute_configuration={}, scaling_configuration={}, overflow_behavior="test-overflow_behavior", vpc_config={}, proxy_configuration={}, image_id="test-image_id", fleet_service_role="test-fleet_service_role", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_project_visibility_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import update_project_visibility
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await update_project_visibility("test-project_arn", "test-project_visibility", resource_access_role="test-resource_access_role", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_report_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import update_report_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await update_report_group("test-arn", export_config=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_webhook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codebuild import update_webhook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codebuild.async_client", lambda *a, **kw: mock_client)
    await update_webhook("test-project_name", branch_filter=[{}], rotate_secret="test-rotate_secret", filter_groups="test-filter_groups", build_type="test-build_type", pull_request_build_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()
