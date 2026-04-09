"""Tests for aws_util.codepipeline module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.codepipeline as cp_mod
from aws_util.codepipeline import (
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

REGION = "us-east-1"
ROLE_ARN = "arn:aws:iam::123456789012:role/PipelineRole"
PIPELINE_NAME = "test-pipeline"
EXECUTION_ID = "exec-12345"

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
                "configuration": {
                    "S3Bucket": "my-bucket",
                    "S3ObjectKey": "source.zip",
                },
                "outputArtifacts": [{"name": "SourceOutput"}],
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
                "configuration": {
                    "BucketName": "deploy-bucket",
                    "Extract": "false",
                },
                "inputArtifacts": [{"name": "SourceOutput"}],
            }
        ],
    },
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_pipeline_result_model():
    pr = PipelineResult(
        name="my-pipe",
        arn="arn:...",
        role_arn=ROLE_ARN,
        stages=_STAGES,
        version=1,
    )
    assert pr.name == "my-pipe"
    assert pr.version == 1
    assert len(pr.stages) == 2


def test_pipeline_result_defaults():
    pr = PipelineResult(name="minimal")
    assert pr.arn is None
    assert pr.role_arn == ""
    assert pr.stages == []
    assert pr.version is None
    assert pr.created is None
    assert pr.updated is None
    assert pr.extra == {}


def test_pipeline_execution_result_model():
    per = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Succeeded",
        artifact_revisions=[{"revisionId": "abc"}],
    )
    assert per.status == "Succeeded"
    assert len(per.artifact_revisions) == 1


def test_pipeline_execution_result_defaults():
    per = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="InProgress",
    )
    assert per.artifact_revisions == []
    assert per.extra == {}


def test_stage_state_result_model():
    ssr = StageStateResult(
        stage_name="Source",
        inbound_execution={"status": "InProgress"},
        action_states=[{"actionName": "SourceAction"}],
    )
    assert ssr.stage_name == "Source"
    assert ssr.inbound_execution is not None


def test_stage_state_result_defaults():
    ssr = StageStateResult(stage_name="Deploy")
    assert ssr.inbound_execution is None
    assert ssr.action_states == []
    assert ssr.extra == {}


# ---------------------------------------------------------------------------
# create_pipeline
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_create_pipeline_success(mock_gc):
    mock_client = MagicMock()
    mock_client.create_pipeline.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 1,
        },
        "metadata": {
            "pipelineArn": "arn:aws:codepipeline:us-east-1:123:test-pipeline",
            "created": "2024-01-01T00:00:00Z",
            "updated": "2024-01-01T00:00:00Z",
        },
    }
    mock_gc.return_value = mock_client

    result = create_pipeline(
        PIPELINE_NAME,
        role_arn=ROLE_ARN,
        stages=_STAGES,
        region_name=REGION,
    )
    assert isinstance(result, PipelineResult)
    assert result.name == PIPELINE_NAME
    assert result.arn == "arn:aws:codepipeline:us-east-1:123:test-pipeline"
    assert result.version == 1


@patch("aws_util.codepipeline.get_client")
def test_create_pipeline_with_artifact_store(mock_gc):
    mock_client = MagicMock()
    mock_client.create_pipeline.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 1,
            "artifactStore": {"type": "S3", "location": "my-bucket"},
        },
        "metadata": {},
    }
    mock_gc.return_value = mock_client

    result = create_pipeline(
        PIPELINE_NAME,
        role_arn=ROLE_ARN,
        stages=_STAGES,
        artifact_store={"type": "S3", "location": "my-bucket"},
        region_name=REGION,
    )
    assert isinstance(result, PipelineResult)
    mock_client.create_pipeline.assert_called_once()
    call_kwargs = mock_client.create_pipeline.call_args[1]
    assert "artifactStore" in call_kwargs["pipeline"]


@patch("aws_util.codepipeline.get_client")
def test_create_pipeline_error(mock_gc):
    mock_client = MagicMock()
    mock_client.create_pipeline.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "invalid"}},
        "CreatePipeline",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="create_pipeline failed"):
        create_pipeline(
            PIPELINE_NAME,
            role_arn=ROLE_ARN,
            stages=_STAGES,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# get_pipeline
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline.return_value = {
        "pipeline": {
            "name": PIPELINE_NAME,
            "roleArn": ROLE_ARN,
            "stages": _STAGES,
            "version": 2,
        },
        "metadata": {
            "pipelineArn": "arn:pipe:1",
            "created": "2024-01-01",
            "updated": "2024-01-02",
        },
    }
    mock_gc.return_value = mock_client

    result = get_pipeline(PIPELINE_NAME, region_name=REGION)
    assert result.name == PIPELINE_NAME
    assert result.version == 2
    assert result.created == "2024-01-01"
    assert result.updated == "2024-01-02"


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "GetPipeline",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="get_pipeline failed"):
        get_pipeline(PIPELINE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# list_pipelines
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_list_pipelines_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
            "pipelines": [
                {
                    "name": "pipe-a",
                    "version": 1,
                    "created": "2024-01-01",
                    "updated": "2024-01-02",
                },
                {
                    "name": "pipe-b",
                    "version": 2,
                },
            ]
        }
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_pipelines(region_name=REGION)
    assert len(result) == 2
    assert result[0]["name"] == "pipe-a"
    assert result[0]["created"] == "2024-01-01"
    assert result[1]["name"] == "pipe-b"
    assert result[1]["created"] is None


@patch("aws_util.codepipeline.get_client")
def test_list_pipelines_empty(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"pipelines": []}]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_pipelines(region_name=REGION)
    assert result == []


@patch("aws_util.codepipeline.get_client")
def test_list_pipelines_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}},
        "ListPipelines",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="list_pipelines failed"):
        list_pipelines(region_name=REGION)


# ---------------------------------------------------------------------------
# update_pipeline
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_update_pipeline_success(mock_gc):
    mock_client = MagicMock()
    pipeline_def = {
        "name": PIPELINE_NAME,
        "roleArn": ROLE_ARN,
        "stages": _STAGES,
        "version": 2,
    }
    mock_client.update_pipeline.return_value = {
        "pipeline": pipeline_def,
        "metadata": {},
    }
    mock_gc.return_value = mock_client

    result = update_pipeline(pipeline=pipeline_def, region_name=REGION)
    assert result.name == PIPELINE_NAME
    assert result.version == 2


@patch("aws_util.codepipeline.get_client")
def test_update_pipeline_error(mock_gc):
    mock_client = MagicMock()
    mock_client.update_pipeline.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "bad"}},
        "UpdatePipeline",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="update_pipeline failed"):
        update_pipeline(pipeline={"name": "x"}, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_pipeline
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_delete_pipeline_success(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_pipeline.return_value = {}
    mock_gc.return_value = mock_client

    delete_pipeline(PIPELINE_NAME, region_name=REGION)
    mock_client.delete_pipeline.assert_called_once_with(name=PIPELINE_NAME)


@patch("aws_util.codepipeline.get_client")
def test_delete_pipeline_error(mock_gc):
    mock_client = MagicMock()
    mock_client.delete_pipeline.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "DeletePipeline",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="delete_pipeline failed"):
        delete_pipeline(PIPELINE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# start_pipeline_execution
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_start_pipeline_execution_success(mock_gc):
    mock_client = MagicMock()
    mock_client.start_pipeline_execution.return_value = {
        "pipelineExecutionId": EXECUTION_ID,
    }
    mock_gc.return_value = mock_client

    result = start_pipeline_execution(PIPELINE_NAME, region_name=REGION)
    assert result == EXECUTION_ID


@patch("aws_util.codepipeline.get_client")
def test_start_pipeline_execution_error(mock_gc):
    mock_client = MagicMock()
    mock_client.start_pipeline_execution.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "StartPipelineExecution",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="start_pipeline_execution failed"):
        start_pipeline_execution(PIPELINE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# get_pipeline_execution
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_execution_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline_execution.return_value = {
        "pipelineExecution": {
            "pipelineName": PIPELINE_NAME,
            "pipelineExecutionId": EXECUTION_ID,
            "status": "Succeeded",
            "artifactRevisions": [{"revisionId": "r1"}],
        }
    }
    mock_gc.return_value = mock_client

    result = get_pipeline_execution(
        PIPELINE_NAME, EXECUTION_ID, region_name=REGION
    )
    assert result.status == "Succeeded"
    assert result.execution_id == EXECUTION_ID
    assert len(result.artifact_revisions) == 1


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_execution_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline_execution.side_effect = ClientError(
        {"Error": {"Code": "PipelineExecutionNotFoundException", "Message": "nope"}},
        "GetPipelineExecution",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="get_pipeline_execution failed"):
        get_pipeline_execution(PIPELINE_NAME, EXECUTION_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# list_pipeline_executions
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_list_pipeline_executions_success(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
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
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_pipeline_executions(PIPELINE_NAME, region_name=REGION)
    assert len(result) == 2
    assert result[0].execution_id == "e1"
    assert result[0].status == "Succeeded"
    assert result[1].status == "Failed"


@patch("aws_util.codepipeline.get_client")
def test_list_pipeline_executions_with_max_results(mock_gc):
    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
            "pipelineExecutionSummaries": [
                {
                    "pipelineExecutionId": "e1",
                    "status": "Succeeded",
                },
            ]
        }
    ]
    mock_client.get_paginator.return_value = mock_paginator
    mock_gc.return_value = mock_client

    result = list_pipeline_executions(
        PIPELINE_NAME, max_results=1, region_name=REGION
    )
    assert len(result) == 1


@patch("aws_util.codepipeline.get_client")
def test_list_pipeline_executions_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "ListPipelineExecutions",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="list_pipeline_executions failed"):
        list_pipeline_executions(PIPELINE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# stop_pipeline_execution
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_stop_pipeline_execution_success(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_pipeline_execution.return_value = {}
    mock_gc.return_value = mock_client

    stop_pipeline_execution(
        PIPELINE_NAME,
        EXECUTION_ID,
        reason="testing",
        abandon=True,
        region_name=REGION,
    )
    mock_client.stop_pipeline_execution.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_stop_pipeline_execution_no_reason(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_pipeline_execution.return_value = {}
    mock_gc.return_value = mock_client

    stop_pipeline_execution(PIPELINE_NAME, EXECUTION_ID, region_name=REGION)
    call_kwargs = mock_client.stop_pipeline_execution.call_args[1]
    assert "reason" not in call_kwargs


@patch("aws_util.codepipeline.get_client")
def test_stop_pipeline_execution_error(mock_gc):
    mock_client = MagicMock()
    mock_client.stop_pipeline_execution.side_effect = ClientError(
        {"Error": {"Code": "PipelineExecutionNotStoppableException", "Message": "nope"}},
        "StopPipelineExecution",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="stop_pipeline_execution failed"):
        stop_pipeline_execution(PIPELINE_NAME, EXECUTION_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# get_pipeline_state
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_state_success(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline_state.return_value = {
        "stageStates": [
            {
                "stageName": "Source",
                "inboundExecution": {"status": "InProgress"},
                "actionStates": [
                    {"actionName": "SourceAction", "latestExecution": {}},
                ],
            },
            {
                "stageName": "Deploy",
                "inboundTransitionState": {"enabled": True},
                "actionStates": [],
            },
        ]
    }
    mock_gc.return_value = mock_client

    result = get_pipeline_state(PIPELINE_NAME, region_name=REGION)
    assert len(result) == 2
    assert result[0].stage_name == "Source"
    assert result[0].inbound_execution == {"status": "InProgress"}
    assert len(result[0].action_states) == 1
    # Second stage uses inboundTransitionState fallback
    assert result[1].stage_name == "Deploy"
    assert result[1].inbound_execution == {"enabled": True}


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_state_empty(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline_state.return_value = {"stageStates": []}
    mock_gc.return_value = mock_client

    result = get_pipeline_state(PIPELINE_NAME, region_name=REGION)
    assert result == []


@patch("aws_util.codepipeline.get_client")
def test_get_pipeline_state_error(mock_gc):
    mock_client = MagicMock()
    mock_client.get_pipeline_state.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "GetPipelineState",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="get_pipeline_state failed"):
        get_pipeline_state(PIPELINE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# retry_stage_execution
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_retry_stage_execution_success(mock_gc):
    mock_client = MagicMock()
    mock_client.retry_stage_execution.return_value = {
        "pipelineExecutionId": "new-exec-id",
    }
    mock_gc.return_value = mock_client

    result = retry_stage_execution(
        PIPELINE_NAME,
        "Deploy",
        EXECUTION_ID,
        retry_mode="ALL_ACTIONS",
        region_name=REGION,
    )
    assert result == "new-exec-id"


@patch("aws_util.codepipeline.get_client")
def test_retry_stage_execution_default_mode(mock_gc):
    mock_client = MagicMock()
    mock_client.retry_stage_execution.return_value = {
        "pipelineExecutionId": "new-exec",
    }
    mock_gc.return_value = mock_client

    result = retry_stage_execution(
        PIPELINE_NAME, "Deploy", EXECUTION_ID, region_name=REGION
    )
    assert result == "new-exec"
    call_kwargs = mock_client.retry_stage_execution.call_args[1]
    assert call_kwargs["retryMode"] == "FAILED_ACTIONS"


@patch("aws_util.codepipeline.get_client")
def test_retry_stage_execution_error(mock_gc):
    mock_client = MagicMock()
    mock_client.retry_stage_execution.side_effect = ClientError(
        {"Error": {"Code": "StageNotRetryableException", "Message": "nope"}},
        "RetryStageExecution",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="retry_stage_execution failed"):
        retry_stage_execution(
            PIPELINE_NAME, "Deploy", EXECUTION_ID, region_name=REGION
        )


# ---------------------------------------------------------------------------
# enable_stage_transition
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_enable_stage_transition_success(mock_gc):
    mock_client = MagicMock()
    mock_client.enable_stage_transition.return_value = {}
    mock_gc.return_value = mock_client

    enable_stage_transition(PIPELINE_NAME, "Deploy", region_name=REGION)
    mock_client.enable_stage_transition.assert_called_once_with(
        pipelineName=PIPELINE_NAME,
        stageName="Deploy",
        transitionType="Inbound",
    )


@patch("aws_util.codepipeline.get_client")
def test_enable_stage_transition_outbound(mock_gc):
    mock_client = MagicMock()
    mock_client.enable_stage_transition.return_value = {}
    mock_gc.return_value = mock_client

    enable_stage_transition(
        PIPELINE_NAME,
        "Deploy",
        transition_type="Outbound",
        region_name=REGION,
    )
    call_kwargs = mock_client.enable_stage_transition.call_args[1]
    assert call_kwargs["transitionType"] == "Outbound"


@patch("aws_util.codepipeline.get_client")
def test_enable_stage_transition_error(mock_gc):
    mock_client = MagicMock()
    mock_client.enable_stage_transition.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "EnableStageTransition",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="enable_stage_transition failed"):
        enable_stage_transition(PIPELINE_NAME, "Deploy", region_name=REGION)


# ---------------------------------------------------------------------------
# disable_stage_transition
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_disable_stage_transition_success(mock_gc):
    mock_client = MagicMock()
    mock_client.disable_stage_transition.return_value = {}
    mock_gc.return_value = mock_client

    disable_stage_transition(
        PIPELINE_NAME,
        "Deploy",
        reason="maintenance",
        region_name=REGION,
    )
    mock_client.disable_stage_transition.assert_called_once_with(
        pipelineName=PIPELINE_NAME,
        stageName="Deploy",
        transitionType="Inbound",
        reason="maintenance",
    )


@patch("aws_util.codepipeline.get_client")
def test_disable_stage_transition_outbound(mock_gc):
    mock_client = MagicMock()
    mock_client.disable_stage_transition.return_value = {}
    mock_gc.return_value = mock_client

    disable_stage_transition(
        PIPELINE_NAME,
        "Deploy",
        transition_type="Outbound",
        region_name=REGION,
    )
    call_kwargs = mock_client.disable_stage_transition.call_args[1]
    assert call_kwargs["transitionType"] == "Outbound"


@patch("aws_util.codepipeline.get_client")
def test_disable_stage_transition_error(mock_gc):
    mock_client = MagicMock()
    mock_client.disable_stage_transition.side_effect = ClientError(
        {"Error": {"Code": "PipelineNotFoundException", "Message": "nope"}},
        "DisableStageTransition",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="disable_stage_transition failed"):
        disable_stage_transition(PIPELINE_NAME, "Deploy", region_name=REGION)


# ---------------------------------------------------------------------------
# put_approval_result
# ---------------------------------------------------------------------------


@patch("aws_util.codepipeline.get_client")
def test_put_approval_result_success(mock_gc):
    mock_client = MagicMock()
    mock_client.put_approval_result.return_value = {}
    mock_gc.return_value = mock_client

    put_approval_result(
        PIPELINE_NAME,
        "Approval",
        "ManualApproval",
        result={"summary": "Approved", "status": "Approved"},
        token="tok-123",
        region_name=REGION,
    )
    mock_client.put_approval_result.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_approval_result_error(mock_gc):
    mock_client = MagicMock()
    mock_client.put_approval_result.side_effect = ClientError(
        {"Error": {"Code": "InvalidApprovalTokenException", "Message": "bad"}},
        "PutApprovalResult",
    )
    mock_gc.return_value = mock_client
    with pytest.raises(RuntimeError, match="put_approval_result failed"):
        put_approval_result(
            PIPELINE_NAME,
            "Approval",
            "ManualApproval",
            result={"summary": "ok", "status": "Approved"},
            token="bad-tok",
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# wait_for_pipeline_execution
# ---------------------------------------------------------------------------


def test_wait_for_pipeline_execution_immediate_success(monkeypatch):
    result = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Succeeded",
    )
    monkeypatch.setattr(
        cp_mod,
        "get_pipeline_execution",
        lambda name, eid, region_name=None: result,
    )
    got = wait_for_pipeline_execution(
        PIPELINE_NAME,
        EXECUTION_ID,
        timeout=5.0,
        poll_interval=0.01,
        region_name=REGION,
    )
    assert got.status == "Succeeded"


def test_wait_for_pipeline_execution_failure_status(monkeypatch):
    result = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Failed",
    )
    monkeypatch.setattr(
        cp_mod,
        "get_pipeline_execution",
        lambda name, eid, region_name=None: result,
    )
    with pytest.raises(RuntimeError, match="entered failure status"):
        wait_for_pipeline_execution(
            PIPELINE_NAME,
            EXECUTION_ID,
            timeout=5.0,
            poll_interval=0.01,
            region_name=REGION,
        )


def test_wait_for_pipeline_execution_timeout(monkeypatch):
    result = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="InProgress",
    )
    monkeypatch.setattr(
        cp_mod,
        "get_pipeline_execution",
        lambda name, eid, region_name=None: result,
    )
    from aws_util.exceptions import AwsTimeoutError

    with pytest.raises(AwsTimeoutError, match="did not reach"):
        wait_for_pipeline_execution(
            PIPELINE_NAME,
            EXECUTION_ID,
            timeout=0.0,
            poll_interval=0.0,
            region_name=REGION,
        )


def test_wait_for_pipeline_execution_polls_then_succeeds(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_get(name, eid, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 3:
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

    monkeypatch.setattr(cp_mod, "get_pipeline_execution", fake_get)
    got = wait_for_pipeline_execution(
        PIPELINE_NAME,
        EXECUTION_ID,
        timeout=60.0,
        poll_interval=0.001,
        region_name=REGION,
    )
    assert got.status == "Succeeded"
    assert call_count["n"] == 3


def test_wait_for_pipeline_execution_custom_target(monkeypatch):
    result = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Stopped",
    )
    monkeypatch.setattr(
        cp_mod,
        "get_pipeline_execution",
        lambda name, eid, region_name=None: result,
    )
    got = wait_for_pipeline_execution(
        PIPELINE_NAME,
        EXECUTION_ID,
        target_statuses=("Stopped",),
        failure_statuses=("Failed",),
        timeout=5.0,
        region_name=REGION,
    )
    assert got.status == "Stopped"


# ---------------------------------------------------------------------------
# run_pipeline_and_wait
# ---------------------------------------------------------------------------


def test_run_pipeline_and_wait_success(monkeypatch):
    monkeypatch.setattr(
        cp_mod,
        "start_pipeline_execution",
        lambda name, region_name=None: EXECUTION_ID,
    )
    result = PipelineExecutionResult(
        pipeline_name=PIPELINE_NAME,
        execution_id=EXECUTION_ID,
        status="Succeeded",
    )
    monkeypatch.setattr(
        cp_mod,
        "wait_for_pipeline_execution",
        lambda name, eid, **kw: result,
    )
    got = run_pipeline_and_wait(PIPELINE_NAME, region_name=REGION)
    assert got.status == "Succeeded"
    assert got.execution_id == EXECUTION_ID


# ---------------------------------------------------------------------------
# _parse_pipeline edge cases
# ---------------------------------------------------------------------------


def test_parse_pipeline_no_metadata():
    """Covers _parse_pipeline when no metadata key is present."""
    from aws_util.codepipeline import _parse_pipeline

    result = _parse_pipeline(
        {
            "pipeline": {
                "name": "p",
                "roleArn": "arn:role",
                "stages": [],
                "version": 1,
                "pipelineArn": "arn:pipe",
            }
        }
    )
    assert result.arn == "arn:pipe"
    assert result.created is None


def test_parse_pipeline_flat_dict():
    """Covers _parse_pipeline when response is a flat pipeline dict."""
    from aws_util.codepipeline import _parse_pipeline

    result = _parse_pipeline(
        {
            "name": "flat",
            "roleArn": "arn:role",
            "stages": [],
            "version": 3,
        }
    )
    assert result.name == "flat"
    assert result.version == 3


# ---------------------------------------------------------------------------
# _parse_execution edge cases
# ---------------------------------------------------------------------------


def test_parse_execution_flat_dict():
    """Covers _parse_execution when response is a flat execution dict."""
    from aws_util.codepipeline import _parse_execution

    result = _parse_execution(
        {
            "pipelineName": "p",
            "pipelineExecutionId": "e1",
            "status": "Succeeded",
            "artifactRevisions": [],
            "trigger": {"triggerType": "Manual"},
        },
        pipeline_name="p",
    )
    assert result.execution_id == "e1"
    assert "trigger" in result.extra


def test_parse_execution_uses_fallback_name():
    """Covers _parse_execution when pipelineName is missing."""
    from aws_util.codepipeline import _parse_execution

    result = _parse_execution(
        {
            "pipelineExecutionId": "e2",
            "status": "InProgress",
        },
        pipeline_name="fallback",
    )
    assert result.pipeline_name == "fallback"


@patch("aws_util.codepipeline.get_client")
def test_acknowledge_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.acknowledge_job.return_value = {}
    acknowledge_job("test-job_id", "test-nonce", region_name=REGION)
    mock_client.acknowledge_job.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_acknowledge_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.acknowledge_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "acknowledge_job",
    )
    with pytest.raises(RuntimeError, match="Failed to acknowledge job"):
        acknowledge_job("test-job_id", "test-nonce", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_acknowledge_third_party_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.acknowledge_third_party_job.return_value = {}
    acknowledge_third_party_job("test-job_id", "test-nonce", "test-client_token", region_name=REGION)
    mock_client.acknowledge_third_party_job.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_acknowledge_third_party_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.acknowledge_third_party_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "acknowledge_third_party_job",
    )
    with pytest.raises(RuntimeError, match="Failed to acknowledge third party job"):
        acknowledge_third_party_job("test-job_id", "test-nonce", "test-client_token", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_create_custom_action_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_action_type.return_value = {}
    create_custom_action_type("test-category", "test-provider", "test-version", {}, {}, region_name=REGION)
    mock_client.create_custom_action_type.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_create_custom_action_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_action_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_action_type",
    )
    with pytest.raises(RuntimeError, match="Failed to create custom action type"):
        create_custom_action_type("test-category", "test-provider", "test-version", {}, {}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_delete_custom_action_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_action_type.return_value = {}
    delete_custom_action_type("test-category", "test-provider", "test-version", region_name=REGION)
    mock_client.delete_custom_action_type.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_delete_custom_action_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_action_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_action_type",
    )
    with pytest.raises(RuntimeError, match="Failed to delete custom action type"):
        delete_custom_action_type("test-category", "test-provider", "test-version", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_delete_webhook(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_webhook.return_value = {}
    delete_webhook("test-name", region_name=REGION)
    mock_client.delete_webhook.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_delete_webhook_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_webhook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_webhook",
    )
    with pytest.raises(RuntimeError, match="Failed to delete webhook"):
        delete_webhook("test-name", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_deregister_webhook_with_third_party(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deregister_webhook_with_third_party.return_value = {}
    deregister_webhook_with_third_party(region_name=REGION)
    mock_client.deregister_webhook_with_third_party.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_deregister_webhook_with_third_party_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deregister_webhook_with_third_party.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_webhook_with_third_party",
    )
    with pytest.raises(RuntimeError, match="Failed to deregister webhook with third party"):
        deregister_webhook_with_third_party(region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_get_action_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_action_type.return_value = {}
    get_action_type("test-category", "test-owner", "test-provider", "test-version", region_name=REGION)
    mock_client.get_action_type.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_get_action_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_action_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_action_type",
    )
    with pytest.raises(RuntimeError, match="Failed to get action type"):
        get_action_type("test-category", "test-owner", "test-provider", "test-version", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_get_job_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_job_details.return_value = {}
    get_job_details("test-job_id", region_name=REGION)
    mock_client.get_job_details.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_get_job_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_job_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_job_details",
    )
    with pytest.raises(RuntimeError, match="Failed to get job details"):
        get_job_details("test-job_id", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_get_third_party_job_details(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_third_party_job_details.return_value = {}
    get_third_party_job_details("test-job_id", "test-client_token", region_name=REGION)
    mock_client.get_third_party_job_details.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_get_third_party_job_details_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_third_party_job_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_third_party_job_details",
    )
    with pytest.raises(RuntimeError, match="Failed to get third party job details"):
        get_third_party_job_details("test-job_id", "test-client_token", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_action_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_action_executions.return_value = {}
    list_action_executions("test-pipeline_name", region_name=REGION)
    mock_client.list_action_executions.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_action_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_action_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_action_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list action executions"):
        list_action_executions("test-pipeline_name", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_action_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_action_types.return_value = {}
    list_action_types(region_name=REGION)
    mock_client.list_action_types.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_action_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_action_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_action_types",
    )
    with pytest.raises(RuntimeError, match="Failed to list action types"):
        list_action_types(region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_deploy_action_execution_targets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deploy_action_execution_targets.return_value = {}
    list_deploy_action_execution_targets("test-action_execution_id", region_name=REGION)
    mock_client.list_deploy_action_execution_targets.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_deploy_action_execution_targets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_deploy_action_execution_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_deploy_action_execution_targets",
    )
    with pytest.raises(RuntimeError, match="Failed to list deploy action execution targets"):
        list_deploy_action_execution_targets("test-action_execution_id", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_rule_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rule_executions.return_value = {}
    list_rule_executions("test-pipeline_name", region_name=REGION)
    mock_client.list_rule_executions.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_rule_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rule_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rule_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list rule executions"):
        list_rule_executions("test-pipeline_name", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_rule_types(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rule_types.return_value = {}
    list_rule_types(region_name=REGION)
    mock_client.list_rule_types.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_rule_types_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_rule_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rule_types",
    )
    with pytest.raises(RuntimeError, match="Failed to list rule types"):
        list_rule_types(region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_list_webhooks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_webhooks.return_value = {}
    list_webhooks(region_name=REGION)
    mock_client.list_webhooks.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_list_webhooks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_webhooks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_webhooks",
    )
    with pytest.raises(RuntimeError, match="Failed to list webhooks"):
        list_webhooks(region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_override_stage_condition(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.override_stage_condition.return_value = {}
    override_stage_condition("test-pipeline_name", "test-stage_name", "test-pipeline_execution_id", "test-condition_type", region_name=REGION)
    mock_client.override_stage_condition.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_override_stage_condition_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.override_stage_condition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "override_stage_condition",
    )
    with pytest.raises(RuntimeError, match="Failed to override stage condition"):
        override_stage_condition("test-pipeline_name", "test-stage_name", "test-pipeline_execution_id", "test-condition_type", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_poll_for_jobs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.poll_for_jobs.return_value = {}
    poll_for_jobs({}, region_name=REGION)
    mock_client.poll_for_jobs.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_poll_for_jobs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.poll_for_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "poll_for_jobs",
    )
    with pytest.raises(RuntimeError, match="Failed to poll for jobs"):
        poll_for_jobs({}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_poll_for_third_party_jobs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.poll_for_third_party_jobs.return_value = {}
    poll_for_third_party_jobs({}, region_name=REGION)
    mock_client.poll_for_third_party_jobs.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_poll_for_third_party_jobs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.poll_for_third_party_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "poll_for_third_party_jobs",
    )
    with pytest.raises(RuntimeError, match="Failed to poll for third party jobs"):
        poll_for_third_party_jobs({}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_action_revision(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_action_revision.return_value = {}
    put_action_revision("test-pipeline_name", "test-stage_name", "test-action_name", {}, region_name=REGION)
    mock_client.put_action_revision.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_action_revision_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_action_revision.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_action_revision",
    )
    with pytest.raises(RuntimeError, match="Failed to put action revision"):
        put_action_revision("test-pipeline_name", "test-stage_name", "test-action_name", {}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_job_failure_result(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_job_failure_result.return_value = {}
    put_job_failure_result("test-job_id", {}, region_name=REGION)
    mock_client.put_job_failure_result.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_job_failure_result_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_job_failure_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_job_failure_result",
    )
    with pytest.raises(RuntimeError, match="Failed to put job failure result"):
        put_job_failure_result("test-job_id", {}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_job_success_result(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_job_success_result.return_value = {}
    put_job_success_result("test-job_id", region_name=REGION)
    mock_client.put_job_success_result.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_job_success_result_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_job_success_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_job_success_result",
    )
    with pytest.raises(RuntimeError, match="Failed to put job success result"):
        put_job_success_result("test-job_id", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_third_party_job_failure_result(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_third_party_job_failure_result.return_value = {}
    put_third_party_job_failure_result("test-job_id", "test-client_token", {}, region_name=REGION)
    mock_client.put_third_party_job_failure_result.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_third_party_job_failure_result_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_third_party_job_failure_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_third_party_job_failure_result",
    )
    with pytest.raises(RuntimeError, match="Failed to put third party job failure result"):
        put_third_party_job_failure_result("test-job_id", "test-client_token", {}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_third_party_job_success_result(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_third_party_job_success_result.return_value = {}
    put_third_party_job_success_result("test-job_id", "test-client_token", region_name=REGION)
    mock_client.put_third_party_job_success_result.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_third_party_job_success_result_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_third_party_job_success_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_third_party_job_success_result",
    )
    with pytest.raises(RuntimeError, match="Failed to put third party job success result"):
        put_third_party_job_success_result("test-job_id", "test-client_token", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_put_webhook(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_webhook.return_value = {}
    put_webhook({}, region_name=REGION)
    mock_client.put_webhook.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_put_webhook_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_webhook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_webhook",
    )
    with pytest.raises(RuntimeError, match="Failed to put webhook"):
        put_webhook({}, region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_register_webhook_with_third_party(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_webhook_with_third_party.return_value = {}
    register_webhook_with_third_party(region_name=REGION)
    mock_client.register_webhook_with_third_party.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_register_webhook_with_third_party_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_webhook_with_third_party.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_webhook_with_third_party",
    )
    with pytest.raises(RuntimeError, match="Failed to register webhook with third party"):
        register_webhook_with_third_party(region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_rollback_stage(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.rollback_stage.return_value = {}
    rollback_stage("test-pipeline_name", "test-stage_name", "test-target_pipeline_execution_id", region_name=REGION)
    mock_client.rollback_stage.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_rollback_stage_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.rollback_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rollback_stage",
    )
    with pytest.raises(RuntimeError, match="Failed to rollback stage"):
        rollback_stage("test-pipeline_name", "test-stage_name", "test-target_pipeline_execution_id", region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codepipeline.get_client")
def test_update_action_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_action_type.return_value = {}
    update_action_type({}, region_name=REGION)
    mock_client.update_action_type.assert_called_once()


@patch("aws_util.codepipeline.get_client")
def test_update_action_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_action_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_action_type",
    )
    with pytest.raises(RuntimeError, match="Failed to update action type"):
        update_action_type({}, region_name=REGION)


def test_stop_pipeline_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import stop_pipeline_execution
    mock_client = MagicMock()
    mock_client.stop_pipeline_execution.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    stop_pipeline_execution("test-name", "test-execution_id", reason="test-reason", region_name="us-east-1")
    mock_client.stop_pipeline_execution.assert_called_once()

def test_create_custom_action_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import create_custom_action_type
    mock_client = MagicMock()
    mock_client.create_custom_action_type.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    create_custom_action_type("test-category", "test-provider", "test-version", "test-input_artifact_details", "test-output_artifact_details", settings={}, configuration_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_action_type.assert_called_once()

def test_deregister_webhook_with_third_party_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import deregister_webhook_with_third_party
    mock_client = MagicMock()
    mock_client.deregister_webhook_with_third_party.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    deregister_webhook_with_third_party(webhook_name="test-webhook_name", region_name="us-east-1")
    mock_client.deregister_webhook_with_third_party.assert_called_once()

def test_list_action_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_action_executions
    mock_client = MagicMock()
    mock_client.list_action_executions.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_action_executions("test-pipeline_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_action_executions.assert_called_once()

def test_list_action_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_action_types
    mock_client = MagicMock()
    mock_client.list_action_types.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_action_types(action_owner_filter=[{}], next_token="test-next_token", region_filter=[{}], region_name="us-east-1")
    mock_client.list_action_types.assert_called_once()

def test_list_deploy_action_execution_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_deploy_action_execution_targets
    mock_client = MagicMock()
    mock_client.list_deploy_action_execution_targets.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_deploy_action_execution_targets("test-action_execution_id", pipeline_name="test-pipeline_name", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_deploy_action_execution_targets.assert_called_once()

def test_list_rule_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_rule_executions
    mock_client = MagicMock()
    mock_client.list_rule_executions.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_rule_executions("test-pipeline_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_rule_executions.assert_called_once()

def test_list_rule_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_rule_types
    mock_client = MagicMock()
    mock_client.list_rule_types.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_rule_types(rule_owner_filter=[{}], region_filter=[{}], region_name="us-east-1")
    mock_client.list_rule_types.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_webhooks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import list_webhooks
    mock_client = MagicMock()
    mock_client.list_webhooks.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    list_webhooks(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_webhooks.assert_called_once()

def test_poll_for_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import poll_for_jobs
    mock_client = MagicMock()
    mock_client.poll_for_jobs.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    poll_for_jobs("test-action_type_id", max_batch_size=1, query_param="test-query_param", region_name="us-east-1")
    mock_client.poll_for_jobs.assert_called_once()

def test_poll_for_third_party_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import poll_for_third_party_jobs
    mock_client = MagicMock()
    mock_client.poll_for_third_party_jobs.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    poll_for_third_party_jobs("test-action_type_id", max_batch_size=1, region_name="us-east-1")
    mock_client.poll_for_third_party_jobs.assert_called_once()

def test_put_job_success_result_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import put_job_success_result
    mock_client = MagicMock()
    mock_client.put_job_success_result.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    put_job_success_result("test-job_id", current_revision="test-current_revision", continuation_token="test-continuation_token", execution_details="test-execution_details", output_variables="test-output_variables", region_name="us-east-1")
    mock_client.put_job_success_result.assert_called_once()

def test_put_third_party_job_success_result_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import put_third_party_job_success_result
    mock_client = MagicMock()
    mock_client.put_third_party_job_success_result.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    put_third_party_job_success_result("test-job_id", "test-client_token", current_revision="test-current_revision", continuation_token="test-continuation_token", execution_details="test-execution_details", region_name="us-east-1")
    mock_client.put_third_party_job_success_result.assert_called_once()

def test_put_webhook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import put_webhook
    mock_client = MagicMock()
    mock_client.put_webhook.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    put_webhook("test-webhook", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.put_webhook.assert_called_once()

def test_register_webhook_with_third_party_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codepipeline import register_webhook_with_third_party
    mock_client = MagicMock()
    mock_client.register_webhook_with_third_party.return_value = {}
    monkeypatch.setattr("aws_util.codepipeline.get_client", lambda *a, **kw: mock_client)
    register_webhook_with_third_party(webhook_name="test-webhook_name", region_name="us-east-1")
    mock_client.register_webhook_with_third_party.assert_called_once()
