"""Tests for aws_util.aio.codepipeline module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codepipeline import (
    PipelineExecutionResult,
    PipelineResult,
    StageStateResult,
    create_pipeline,
    delete_pipeline,
    disable_stage_transition,
    enable_stage_transition,
    get_pipeline,
    get_pipeline_execution,
    get_pipeline_state,
    list_pipeline_executions,
    list_pipelines,
    put_approval_result,
    retry_stage_execution,
    run_pipeline_and_wait,
    start_pipeline_execution,
    stop_pipeline_execution,
    update_pipeline,
    wait_for_pipeline_execution,
    acknowledge_job,
    acknowledge_third_party_job,
    create_custom_action_type,
    delete_custom_action_type,
    delete_webhook,
    deregister_webhook_with_third_party,
    get_action_type,
    get_job_details,
    get_third_party_job_details,
    list_action_executions,
    list_action_types,
    list_deploy_action_execution_targets,
    list_rule_executions,
    list_rule_types,
    list_tags_for_resource,
    list_webhooks,
    override_stage_condition,
    poll_for_jobs,
    poll_for_third_party_jobs,
    put_action_revision,
    put_job_failure_result,
    put_job_success_result,
    put_third_party_job_failure_result,
    put_third_party_job_success_result,
    put_webhook,
    register_webhook_with_third_party,
    rollback_stage,
    tag_resource,
    untag_resource,
    update_action_type,
)

PIPELINE_NAME = "test-pipeline"
EXECUTION_ID = "exec-12345"
ROLE_ARN = "arn:aws:iam::123456789012:role/PipelineRole"

_STAGES = [
    {
        "name": "Source",
        "actions": [
            {
                "name": "SourceAction",
                "actionTypeId": {
                    "category": "Source",
                    "owner": "AWS",
                    "provider": "S3",
                    "version": "1",
                },
            }
        ],
    },
    {
        "name": "Deploy",
        "actions": [
            {
                "name": "DeployAction",
                "actionTypeId": {
                    "category": "Deploy",
                    "owner": "AWS",
                    "provider": "S3",
                    "version": "1",
                },
            }
        ],
    },
]


# ---------------------------------------------------------------------------
# create_pipeline
# ---------------------------------------------------------------------------


async def test_create_pipeline_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 1,
        },
        "metadata": {
            "pipelineArn": "arn:pipe:1",
            "created": "2024-01-01",
            "updated": "2024-01-01",
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_pipeline(
        PIPELINE_NAME, role_arn=ROLE_ARN, stages=_STAGES
    )
    assert result.name == PIPELINE_NAME
    assert result.arn == "arn:pipe:1"


async def test_create_pipeline_with_artifact_store(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 1,
            "artifactStore": {"type": "S3", "location": "bucket"},
        },
        "metadata": {},
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_pipeline(
        PIPELINE_NAME,
        role_arn=ROLE_ARN,
        stages=_STAGES,
        artifact_store={"type": "S3", "location": "bucket"},
    )
    assert isinstance(result, PipelineResult)


async def test_create_pipeline_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_pipeline(
            PIPELINE_NAME, role_arn=ROLE_ARN, stages=_STAGES
        )


async def test_create_pipeline_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_pipeline failed"):
        await create_pipeline(
            PIPELINE_NAME, role_arn=ROLE_ARN, stages=_STAGES
        )


# ---------------------------------------------------------------------------
# get_pipeline
# ---------------------------------------------------------------------------


async def test_get_pipeline_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 2,
        },
        "metadata": {"pipelineArn": "arn:pipe:1"},
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_pipeline(PIPELINE_NAME)
    assert result.name == PIPELINE_NAME
    assert result.version == 2


async def test_get_pipeline_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_pipeline(PIPELINE_NAME)


async def test_get_pipeline_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_pipeline failed"):
        await get_pipeline(PIPELINE_NAME)


# ---------------------------------------------------------------------------
# list_pipelines
# ---------------------------------------------------------------------------


async def test_list_pipelines_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelines": [
            {"name": "a", "version": 1, "created": "2024-01-01"},
            {"name": "b", "version": 2},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipelines()
    assert len(result) == 2
    assert result[0]["name"] == "a"
    assert result[1]["created"] is None


async def test_list_pipelines_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "pipelines": [{"name": "a"}],
                "nextToken": "tok",
            }
        return {"pipelines": [{"name": "b"}]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipelines()
    assert len(result) == 2


async def test_list_pipelines_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"pipelines": []}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipelines()
    assert result == []


async def test_list_pipelines_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_pipelines()


async def test_list_pipelines_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_pipelines failed"):
        await list_pipelines()


# ---------------------------------------------------------------------------
# update_pipeline
# ---------------------------------------------------------------------------


async def test_update_pipeline_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    pipeline_def = {
        "name": PIPELINE_NAME,
        "roleArn": ROLE_ARN,
        "stages": _STAGES,
        "version": 3,
    }
    mock_client.call.return_value = {
        "pipeline": pipeline_def,
        "metadata": {},
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_pipeline(pipeline=pipeline_def)
    assert result.version == 3


async def test_update_pipeline_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await update_pipeline(pipeline={"name": "x"})


async def test_update_pipeline_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="update_pipeline failed"):
        await update_pipeline(pipeline={"name": "x"})


# ---------------------------------------------------------------------------
# delete_pipeline
# ---------------------------------------------------------------------------


async def test_delete_pipeline_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_pipeline(PIPELINE_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_pipeline_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await delete_pipeline(PIPELINE_NAME)


async def test_delete_pipeline_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_pipeline failed"):
        await delete_pipeline(PIPELINE_NAME)


# ---------------------------------------------------------------------------
# start_pipeline_execution
# ---------------------------------------------------------------------------


async def test_start_pipeline_execution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecutionId": EXECUTION_ID,
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_pipeline_execution(PIPELINE_NAME)
    assert result == EXECUTION_ID


async def test_start_pipeline_execution_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_pipeline_execution(PIPELINE_NAME)


async def test_start_pipeline_execution_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_pipeline_execution failed"):
        await start_pipeline_execution(PIPELINE_NAME)


# ---------------------------------------------------------------------------
# get_pipeline_execution
# ---------------------------------------------------------------------------


async def test_get_pipeline_execution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecution": {
            "pipelineName": PIPELINE_NAME,
            "pipelineExecutionId": EXECUTION_ID,
            "status": "Succeeded",
            "artifactRevisions": [{"revisionId": "r1"}],
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)
    assert result.status == "Succeeded"
    assert result.execution_id == EXECUTION_ID


async def test_get_pipeline_execution_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)


async def test_get_pipeline_execution_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="get_pipeline_execution failed"
    ):
        await get_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)


# ---------------------------------------------------------------------------
# list_pipeline_executions
# ---------------------------------------------------------------------------


async def test_list_pipeline_executions_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecutionSummaries": [
            {
                "pipelineExecutionId": "e1",
                "status": "Succeeded",
                "sourceRevisions": [{"revisionId": "r1"}],
            },
            {
                "pipelineExecutionId": "e2",
                "status": "Failed",
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipeline_executions(PIPELINE_NAME)
    assert len(result) == 2
    assert result[0].execution_id == "e1"


async def test_list_pipeline_executions_with_max_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecutionSummaries": [
            {"pipelineExecutionId": "e1", "status": "Succeeded"},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipeline_executions(
        PIPELINE_NAME, max_results=1
    )
    assert len(result) == 1


async def test_list_pipeline_executions_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "pipelineExecutionSummaries": [
                    {"pipelineExecutionId": "e1", "status": "Succeeded"},
                ],
                "nextToken": "tok",
            }
        return {
            "pipelineExecutionSummaries": [
                {"pipelineExecutionId": "e2", "status": "Failed"},
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_pipeline_executions(PIPELINE_NAME)
    assert len(result) == 2


async def test_list_pipeline_executions_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_pipeline_executions(PIPELINE_NAME)


async def test_list_pipeline_executions_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="list_pipeline_executions failed"
    ):
        await list_pipeline_executions(PIPELINE_NAME)


# ---------------------------------------------------------------------------
# stop_pipeline_execution
# ---------------------------------------------------------------------------


async def test_stop_pipeline_execution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_pipeline_execution(
        PIPELINE_NAME, EXECUTION_ID, reason="test", abandon=True
    )
    mock_client.call.assert_awaited_once()


async def test_stop_pipeline_execution_no_reason(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)
    mock_client.call.assert_awaited_once()


async def test_stop_pipeline_execution_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await stop_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)


async def test_stop_pipeline_execution_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="stop_pipeline_execution failed"
    ):
        await stop_pipeline_execution(PIPELINE_NAME, EXECUTION_ID)


# ---------------------------------------------------------------------------
# get_pipeline_state
# ---------------------------------------------------------------------------


async def test_get_pipeline_state_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "stageStates": [
            {
                "stageName": "Source",
                "inboundExecution": {"status": "InProgress"},
                "actionStates": [{"actionName": "S"}],
            },
            {
                "stageName": "Deploy",
                "inboundTransitionState": {"enabled": True},
                "actionStates": [],
            },
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_pipeline_state(PIPELINE_NAME)
    assert len(result) == 2
    assert result[0].stage_name == "Source"
    assert result[1].inbound_execution == {"enabled": True}


async def test_get_pipeline_state_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"stageStates": []}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_pipeline_state(PIPELINE_NAME)
    assert result == []


async def test_get_pipeline_state_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await get_pipeline_state(PIPELINE_NAME)


async def test_get_pipeline_state_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_pipeline_state failed"):
        await get_pipeline_state(PIPELINE_NAME)


# ---------------------------------------------------------------------------
# retry_stage_execution
# ---------------------------------------------------------------------------


async def test_retry_stage_execution_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecutionId": "new-exec",
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await retry_stage_execution(
        PIPELINE_NAME,
        "Deploy",
        EXECUTION_ID,
        retry_mode="ALL_ACTIONS",
    )
    assert result == "new-exec"


async def test_retry_stage_execution_default_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "pipelineExecutionId": "new-exec",
    }
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await retry_stage_execution(
        PIPELINE_NAME, "Deploy", EXECUTION_ID
    )
    assert result == "new-exec"


async def test_retry_stage_execution_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await retry_stage_execution(
            PIPELINE_NAME, "Deploy", EXECUTION_ID
        )


async def test_retry_stage_execution_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="retry_stage_execution failed"
    ):
        await retry_stage_execution(
            PIPELINE_NAME, "Deploy", EXECUTION_ID
        )


# ---------------------------------------------------------------------------
# enable_stage_transition
# ---------------------------------------------------------------------------


async def test_enable_stage_transition_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_stage_transition(PIPELINE_NAME, "Deploy")
    mock_client.call.assert_awaited_once()


async def test_enable_stage_transition_outbound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_stage_transition(
        PIPELINE_NAME, "Deploy", transition_type="Outbound"
    )
    mock_client.call.assert_awaited_once()


async def test_enable_stage_transition_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await enable_stage_transition(PIPELINE_NAME, "Deploy")


async def test_enable_stage_transition_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="enable_stage_transition failed"
    ):
        await enable_stage_transition(PIPELINE_NAME, "Deploy")


# ---------------------------------------------------------------------------
# disable_stage_transition
# ---------------------------------------------------------------------------


async def test_disable_stage_transition_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_stage_transition(
        PIPELINE_NAME, "Deploy", reason="maintenance"
    )
    mock_client.call.assert_awaited_once()


async def test_disable_stage_transition_outbound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_stage_transition(
        PIPELINE_NAME, "Deploy", transition_type="Outbound"
    )
    mock_client.call.assert_awaited_once()


async def test_disable_stage_transition_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await disable_stage_transition(PIPELINE_NAME, "Deploy")


async def test_disable_stage_transition_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(
        RuntimeError, match="disable_stage_transition failed"
    ):
        await disable_stage_transition(PIPELINE_NAME, "Deploy")


# ---------------------------------------------------------------------------
# put_approval_result
# ---------------------------------------------------------------------------


async def test_put_approval_result_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_approval_result(
        PIPELINE_NAME,
        "Approval",
        "ManualApproval",
        result={"summary": "ok", "status": "Approved"},
        token="tok-123",
    )
    mock_client.call.assert_awaited_once()


async def test_put_approval_result_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await put_approval_result(
            PIPELINE_NAME,
            "Approval",
            "ManualApproval",
            result={"summary": "ok", "status": "Approved"},
            token="tok",
        )


async def test_put_approval_result_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="put_approval_result failed"):
        await put_approval_result(
            PIPELINE_NAME,
            "Approval",
            "ManualApproval",
            result={"summary": "ok", "status": "Approved"},
            token="tok",
        )


# ---------------------------------------------------------------------------
# wait_for_pipeline_execution
# ---------------------------------------------------------------------------


async def test_wait_immediate_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finished = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Succeeded",
    )

    async def _fake_get(name, eid, region_name=None):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.get_pipeline_execution", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_pipeline_execution(
        PIPELINE_NAME, EXECUTION_ID
    )
    assert result.status == "Succeeded"


async def test_wait_polls_then_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    call_count = 0

    async def _fake_get(name, eid, region_name=None):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return PipelineExecutionResult(
                pipeline_name=name,
                execution_id=eid,
                status="InProgress",
            )
        return PipelineExecutionResult(
            pipeline_name=name,
            execution_id=eid,
            status="Succeeded",
        )

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.get_pipeline_execution", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.asyncio.sleep", AsyncMock()
    )
    result = await wait_for_pipeline_execution(
        PIPELINE_NAME, EXECUTION_ID, timeout=60.0
    )
    assert result.status == "Succeeded"


async def test_wait_failure_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    failed = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Failed",
    )

    async def _fake_get(name, eid, region_name=None):
        return failed

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.get_pipeline_execution", _fake_get
    )
    with pytest.raises(RuntimeError, match="entered failure status"):
        await wait_for_pipeline_execution(
            PIPELINE_NAME, EXECUTION_ID
        )


async def test_wait_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    running = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="InProgress",
    )

    async def _fake_get(name, eid, region_name=None):
        return running

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.get_pipeline_execution", _fake_get
    )
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.asyncio.sleep", AsyncMock()
    )
    from aws_util.exceptions import AwsTimeoutError

    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_pipeline_execution(
            PIPELINE_NAME, EXECUTION_ID, timeout=0.0
        )


async def test_wait_custom_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stopped = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Stopped",
    )

    async def _fake_get(name, eid, region_name=None):
        return stopped

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.get_pipeline_execution", _fake_get
    )
    result = await wait_for_pipeline_execution(
        PIPELINE_NAME,
        EXECUTION_ID,
        target_statuses=("Stopped",),
        failure_statuses=("Failed",),
    )
    assert result.status == "Stopped"


# ---------------------------------------------------------------------------
# run_pipeline_and_wait
# ---------------------------------------------------------------------------


async def test_run_pipeline_and_wait_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def _fake_start(name, region_name=None):
        return EXECUTION_ID

    finished = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Succeeded",
    )

    async def _fake_wait(name, eid, **kwargs):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.codepipeline.start_pipeline_execution",
        _fake_start,
    )
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.wait_for_pipeline_execution",
        _fake_wait,
    )
    result = await run_pipeline_and_wait(PIPELINE_NAME)
    assert result.status == "Succeeded"
    assert result.execution_id == EXECUTION_ID


async def test_acknowledge_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await acknowledge_job("test-job_id", "test-nonce", )
    mock_client.call.assert_called_once()


async def test_acknowledge_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await acknowledge_job("test-job_id", "test-nonce", )


async def test_acknowledge_third_party_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await acknowledge_third_party_job("test-job_id", "test-nonce", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_acknowledge_third_party_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await acknowledge_third_party_job("test-job_id", "test-nonce", "test-client_token", )


async def test_create_custom_action_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_action_type("test-category", "test-provider", "test-version", {}, {}, )
    mock_client.call.assert_called_once()


async def test_create_custom_action_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_action_type("test-category", "test-provider", "test-version", {}, {}, )


async def test_delete_custom_action_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_action_type("test-category", "test-provider", "test-version", )
    mock_client.call.assert_called_once()


async def test_delete_custom_action_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_action_type("test-category", "test-provider", "test-version", )


async def test_delete_webhook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_webhook("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_webhook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_webhook("test-name", )


async def test_deregister_webhook_with_third_party(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_webhook_with_third_party()
    mock_client.call.assert_called_once()


async def test_deregister_webhook_with_third_party_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_webhook_with_third_party()


async def test_get_action_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_action_type("test-category", "test-owner", "test-provider", "test-version", )
    mock_client.call.assert_called_once()


async def test_get_action_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_action_type("test-category", "test-owner", "test-provider", "test-version", )


async def test_get_job_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_job_details("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_job_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_job_details("test-job_id", )


async def test_get_third_party_job_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_third_party_job_details("test-job_id", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_get_third_party_job_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_third_party_job_details("test-job_id", "test-client_token", )


async def test_list_action_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_action_executions("test-pipeline_name", )
    mock_client.call.assert_called_once()


async def test_list_action_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_action_executions("test-pipeline_name", )


async def test_list_action_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_action_types()
    mock_client.call.assert_called_once()


async def test_list_action_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_action_types()


async def test_list_deploy_action_execution_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_deploy_action_execution_targets("test-action_execution_id", )
    mock_client.call.assert_called_once()


async def test_list_deploy_action_execution_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_deploy_action_execution_targets("test-action_execution_id", )


async def test_list_rule_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rule_executions("test-pipeline_name", )
    mock_client.call.assert_called_once()


async def test_list_rule_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rule_executions("test-pipeline_name", )


async def test_list_rule_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rule_types()
    mock_client.call.assert_called_once()


async def test_list_rule_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rule_types()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_webhooks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_webhooks()
    mock_client.call.assert_called_once()


async def test_list_webhooks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_webhooks()


async def test_override_stage_condition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await override_stage_condition("test-pipeline_name", "test-stage_name", "test-pipeline_execution_id", "test-condition_type", )
    mock_client.call.assert_called_once()


async def test_override_stage_condition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await override_stage_condition("test-pipeline_name", "test-stage_name", "test-pipeline_execution_id", "test-condition_type", )


async def test_poll_for_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await poll_for_jobs({}, )
    mock_client.call.assert_called_once()


async def test_poll_for_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await poll_for_jobs({}, )


async def test_poll_for_third_party_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await poll_for_third_party_jobs({}, )
    mock_client.call.assert_called_once()


async def test_poll_for_third_party_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await poll_for_third_party_jobs({}, )


async def test_put_action_revision(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_action_revision("test-pipeline_name", "test-stage_name", "test-action_name", {}, )
    mock_client.call.assert_called_once()


async def test_put_action_revision_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_action_revision("test-pipeline_name", "test-stage_name", "test-action_name", {}, )


async def test_put_job_failure_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_job_failure_result("test-job_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_job_failure_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_job_failure_result("test-job_id", {}, )


async def test_put_job_success_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_job_success_result("test-job_id", )
    mock_client.call.assert_called_once()


async def test_put_job_success_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_job_success_result("test-job_id", )


async def test_put_third_party_job_failure_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_third_party_job_failure_result("test-job_id", "test-client_token", {}, )
    mock_client.call.assert_called_once()


async def test_put_third_party_job_failure_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_third_party_job_failure_result("test-job_id", "test-client_token", {}, )


async def test_put_third_party_job_success_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_third_party_job_success_result("test-job_id", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_put_third_party_job_success_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_third_party_job_success_result("test-job_id", "test-client_token", )


async def test_put_webhook(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_webhook({}, )
    mock_client.call.assert_called_once()


async def test_put_webhook_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_webhook({}, )


async def test_register_webhook_with_third_party(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_webhook_with_third_party()
    mock_client.call.assert_called_once()


async def test_register_webhook_with_third_party_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_webhook_with_third_party()


async def test_rollback_stage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await rollback_stage("test-pipeline_name", "test-stage_name", "test-target_pipeline_execution_id", )
    mock_client.call.assert_called_once()


async def test_rollback_stage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rollback_stage("test-pipeline_name", "test-stage_name", "test-target_pipeline_execution_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_action_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_action_type({}, )
    mock_client.call.assert_called_once()


async def test_update_action_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codepipeline.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_action_type({}, )


@pytest.mark.asyncio
async def test_list_pipeline_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_pipeline_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_pipeline_executions("test-name", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_pipeline_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import stop_pipeline_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await stop_pipeline_execution("test-name", "test-execution_id", reason="test-reason", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_action_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import create_custom_action_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await create_custom_action_type("test-category", "test-provider", "test-version", "test-input_artifact_details", "test-output_artifact_details", settings={}, configuration_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_webhook_with_third_party_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import deregister_webhook_with_third_party
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await deregister_webhook_with_third_party(webhook_name="test-webhook_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_action_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_action_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_action_executions("test-pipeline_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_action_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_action_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_action_types(action_owner_filter=[{}], next_token="test-next_token", region_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_deploy_action_execution_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_deploy_action_execution_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_deploy_action_execution_targets("test-action_execution_id", pipeline_name="test-pipeline_name", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rule_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_rule_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_rule_executions("test-pipeline_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rule_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_rule_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_rule_types(rule_owner_filter=[{}], region_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_webhooks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import list_webhooks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await list_webhooks(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_poll_for_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import poll_for_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await poll_for_jobs("test-action_type_id", max_batch_size=1, query_param="test-query_param", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_poll_for_third_party_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import poll_for_third_party_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await poll_for_third_party_jobs("test-action_type_id", max_batch_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_job_success_result_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import put_job_success_result
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await put_job_success_result("test-job_id", current_revision="test-current_revision", continuation_token="test-continuation_token", execution_details="test-execution_details", output_variables="test-output_variables", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_third_party_job_success_result_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import put_third_party_job_success_result
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await put_third_party_job_success_result("test-job_id", "test-client_token", current_revision="test-current_revision", continuation_token="test-continuation_token", execution_details="test-execution_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_webhook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import put_webhook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await put_webhook("test-webhook", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_webhook_with_third_party_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codepipeline import register_webhook_with_third_party
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codepipeline.async_client", lambda *a, **kw: mock_client)
    await register_webhook_with_third_party(webhook_name="test-webhook_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
