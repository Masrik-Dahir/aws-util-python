"""Tests for aws_util.stepfunctions module."""
from __future__ import annotations

import json
import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.stepfunctions as sfn_mod
from aws_util.stepfunctions import (
    SFNExecution,
    StateMachine,
    start_execution,
    describe_execution,
    stop_execution,
    list_executions,
    wait_for_execution,
    list_state_machines,
    run_and_wait,
    get_execution_history,
    create_activity,
    create_state_machine,
    create_state_machine_alias,
    delete_activity,
    delete_state_machine,
    delete_state_machine_alias,
    delete_state_machine_version,
    describe_activity,
    describe_map_run,
    describe_state_machine,
    describe_state_machine_alias,
    describe_state_machine_for_execution,
    get_activity_task,
    list_activities,
    list_map_runs,
    list_state_machine_aliases,
    list_state_machine_versions,
    list_tags_for_resource,
    publish_state_machine_version,
    redrive_execution,
    run_state,
    send_task_failure,
    send_task_heartbeat,
    send_task_success,
    start_sync_execution,
    tag_resource,
    untag_resource,
    update_map_run,
    update_state_machine,
    update_state_machine_alias,
    validate_state_machine_definition,
)

REGION = "us-east-1"
ROLE_ARN = "arn:aws:iam::123456789012:role/StepFunctionsRole"
SM_DEFINITION = json.dumps({
    "Comment": "Simple pass state",
    "StartAt": "Pass",
    "States": {
        "Pass": {
            "Type": "Pass",
            "End": True,
        }
    },
})


@pytest.fixture
def state_machine():
    import json as _json
    iam = boto3.client("iam", region_name=REGION)
    try:
        role = iam.create_role(
            RoleName="SFNRole",
            AssumeRolePolicyDocument=_json.dumps({
                "Version": "2012-10-17",
                "Statement": [{"Effect": "Allow", "Principal": {"Service": "states.amazonaws.com"}, "Action": "sts:AssumeRole"}],
            }),
        )
        role_arn = role["Role"]["Arn"]
    except Exception:
        role_arn = ROLE_ARN

    client = boto3.client("stepfunctions", region_name=REGION)
    resp = client.create_state_machine(
        name="test-sm",
        definition=SM_DEFINITION,
        roleArn=role_arn,
    )
    return resp["stateMachineArn"]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_sfn_execution_properties():
    ex = SFNExecution(
        execution_arn="arn:...",
        state_machine_arn="arn:...",
        name="test",
        status="SUCCEEDED",
    )
    assert ex.succeeded is True
    assert ex.finished is True


def test_sfn_execution_running():
    ex = SFNExecution(
        execution_arn="arn:...",
        state_machine_arn="arn:...",
        name="test",
        status="RUNNING",
    )
    assert ex.succeeded is False
    assert ex.finished is False


def test_state_machine_model():
    sm = StateMachine(
        state_machine_arn="arn:...",
        name="my-sm",
        type="STANDARD",
        status="ACTIVE",
    )
    assert sm.name == "my-sm"


# ---------------------------------------------------------------------------
# start_execution
# ---------------------------------------------------------------------------

def test_start_execution_returns_execution(state_machine):
    result = start_execution(state_machine, input_data={"key": "val"}, region_name=REGION)
    assert isinstance(result, SFNExecution)
    assert result.status == "RUNNING"
    assert result.execution_arn


def test_start_execution_with_name(state_machine):
    result = start_execution(state_machine, name="my-exec", region_name=REGION)
    assert result.execution_arn


def test_start_execution_no_input(state_machine):
    result = start_execution(state_machine, region_name=REGION)
    assert result.execution_arn


def test_start_execution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_execution.side_effect = ClientError(
        {"Error": {"Code": "StateMachineDoesNotExist", "Message": "not found"}}, "StartExecution"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start execution"):
        start_execution("arn:nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_execution
# ---------------------------------------------------------------------------

def test_describe_execution_returns_status(state_machine):
    ex = start_execution(state_machine, region_name=REGION)
    result = describe_execution(ex.execution_arn, region_name=REGION)
    assert isinstance(result, SFNExecution)
    assert result.execution_arn == ex.execution_arn


def test_describe_execution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_execution.side_effect = ClientError(
        {"Error": {"Code": "ExecutionDoesNotExist", "Message": "not found"}}, "DescribeExecution"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_execution failed"):
        describe_execution("arn:nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# stop_execution
# ---------------------------------------------------------------------------

def test_stop_execution_success(state_machine):
    ex = start_execution(state_machine, region_name=REGION)
    stop_execution(ex.execution_arn, error="TestStop", cause="Test", region_name=REGION)


def test_stop_execution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_execution.side_effect = ClientError(
        {"Error": {"Code": "ExecutionDoesNotExist", "Message": "not found"}}, "StopExecution"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="stop_execution failed"):
        stop_execution("arn:nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# list_executions
# ---------------------------------------------------------------------------

def test_list_executions_returns_list(state_machine):
    start_execution(state_machine, region_name=REGION)
    result = list_executions(state_machine, region_name=REGION)
    assert isinstance(result, list)
    assert len(result) >= 1


def test_list_executions_with_status_filter(state_machine):
    start_execution(state_machine, region_name=REGION)
    result = list_executions(state_machine, status_filter="RUNNING", region_name=REGION)
    assert isinstance(result, list)


def test_list_executions_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "StateMachineDoesNotExist", "Message": "not found"}}, "ListExecutions"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_executions failed"):
        list_executions("arn:nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# list_state_machines
# ---------------------------------------------------------------------------

def test_list_state_machines_returns_list(state_machine):
    result = list_state_machines(region_name=REGION)
    assert isinstance(result, list)
    assert any(sm.name == "test-sm" for sm in result)


def test_list_state_machines_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListStateMachines"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_state_machines failed"):
        list_state_machines(region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_execution
# ---------------------------------------------------------------------------

def test_wait_for_execution_already_finished(monkeypatch):
    finished = SFNExecution(
        execution_arn="arn:...",
        state_machine_arn="arn:...",
        name="test",
        status="SUCCEEDED",
    )
    monkeypatch.setattr(sfn_mod, "describe_execution", lambda arn, region_name=None: finished)
    result = wait_for_execution("arn:...", timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.succeeded


def test_wait_for_execution_timeout(monkeypatch):
    running = SFNExecution(
        execution_arn="arn:...",
        state_machine_arn="arn:...",
        name="test",
        status="RUNNING",
    )
    monkeypatch.setattr(sfn_mod, "describe_execution", lambda arn, region_name=None: running)
    with pytest.raises(TimeoutError):
        wait_for_execution("arn:...", timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# get_execution_history
# ---------------------------------------------------------------------------

def test_get_execution_history_returns_events(state_machine):
    ex = start_execution(state_machine, region_name=REGION)
    events = get_execution_history(ex.execution_arn, region_name=REGION)
    assert isinstance(events, list)


def test_get_execution_history_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "ExecutionDoesNotExist", "Message": "not found"}}, "GetExecutionHistory"
    )
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_execution_history failed"):
        get_execution_history("arn:nonexistent", region_name=REGION)


def test_wait_for_execution_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_execution (line 225)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_describe(arn, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return SFNExecution(
                execution_arn=arn, state_machine_arn="arn:...", name="t", status="RUNNING"
            )
        return SFNExecution(
            execution_arn=arn, state_machine_arn="arn:...", name="t", status="SUCCEEDED"
        )

    monkeypatch.setattr(sfn_mod, "describe_execution", fake_describe)
    result = wait_for_execution("arn:...", timeout=10.0, poll_interval=0.001, region_name=REGION)
    assert result.succeeded


def test_parse_execution_non_json_input(monkeypatch):
    """Covers json.JSONDecodeError branch in _parse_execution (lines 273-274)."""
    mock_client = MagicMock()
    mock_client.describe_execution.return_value = {
        "executionArn": "arn:exe:1",
        "stateMachineArn": "arn:sm:1",
        "name": "test",
        "status": "SUCCEEDED",
        "input": "not json {{{{",
        "output": "also not json",
    }
    monkeypatch.setattr(sfn_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_execution("arn:exe:1", region_name=REGION)
    assert result.input == "not json {{{{"
    assert result.output == "also not json"


def test_run_and_wait(monkeypatch):
    """Covers run_and_wait (lines 323-326)."""
    execution = SFNExecution(
        execution_arn="arn:exe:1", state_machine_arn="arn:sm:1", name="run1", status="SUCCEEDED"
    )
    monkeypatch.setattr(sfn_mod, "start_execution", lambda *a, **kw: execution)
    monkeypatch.setattr(sfn_mod, "wait_for_execution", lambda *a, **kw: execution)
    result = run_and_wait("arn:sm:1", input_data={"key": "val"}, region_name=REGION)
    assert result.succeeded


def test_create_activity(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_activity.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_activity("test-name", region_name=REGION)
    mock_client.create_activity.assert_called_once()


def test_create_activity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_activity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_activity",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create activity"):
        create_activity("test-name", region_name=REGION)


def test_create_state_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_state_machine("test-name", "test-definition", "test-role_arn", region_name=REGION)
    mock_client.create_state_machine.assert_called_once()


def test_create_state_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_state_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_state_machine",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create state machine"):
        create_state_machine("test-name", "test-definition", "test-role_arn", region_name=REGION)


def test_create_state_machine_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_state_machine_alias("test-name", [], region_name=REGION)
    mock_client.create_state_machine_alias.assert_called_once()


def test_create_state_machine_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_state_machine_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_state_machine_alias",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create state machine alias"):
        create_state_machine_alias("test-name", [], region_name=REGION)


def test_delete_activity(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_activity.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    delete_activity("test-activity_arn", region_name=REGION)
    mock_client.delete_activity.assert_called_once()


def test_delete_activity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_activity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_activity",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete activity"):
        delete_activity("test-activity_arn", region_name=REGION)


def test_delete_state_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    delete_state_machine("test-state_machine_arn", region_name=REGION)
    mock_client.delete_state_machine.assert_called_once()


def test_delete_state_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_state_machine",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete state machine"):
        delete_state_machine("test-state_machine_arn", region_name=REGION)


def test_delete_state_machine_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    delete_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)
    mock_client.delete_state_machine_alias.assert_called_once()


def test_delete_state_machine_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_state_machine_alias",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete state machine alias"):
        delete_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)


def test_delete_state_machine_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine_version.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    delete_state_machine_version("test-state_machine_version_arn", region_name=REGION)
    mock_client.delete_state_machine_version.assert_called_once()


def test_delete_state_machine_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_state_machine_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_state_machine_version",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete state machine version"):
        delete_state_machine_version("test-state_machine_version_arn", region_name=REGION)


def test_describe_activity(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_activity.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_activity("test-activity_arn", region_name=REGION)
    mock_client.describe_activity.assert_called_once()


def test_describe_activity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_activity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_activity",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe activity"):
        describe_activity("test-activity_arn", region_name=REGION)


def test_describe_map_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_map_run.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_map_run("test-map_run_arn", region_name=REGION)
    mock_client.describe_map_run.assert_called_once()


def test_describe_map_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_map_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_map_run",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe map run"):
        describe_map_run("test-map_run_arn", region_name=REGION)


def test_describe_state_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_state_machine("test-state_machine_arn", region_name=REGION)
    mock_client.describe_state_machine.assert_called_once()


def test_describe_state_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_state_machine",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe state machine"):
        describe_state_machine("test-state_machine_arn", region_name=REGION)


def test_describe_state_machine_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)
    mock_client.describe_state_machine_alias.assert_called_once()


def test_describe_state_machine_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_state_machine_alias",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe state machine alias"):
        describe_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)


def test_describe_state_machine_for_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine_for_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_state_machine_for_execution("test-execution_arn", region_name=REGION)
    mock_client.describe_state_machine_for_execution.assert_called_once()


def test_describe_state_machine_for_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_state_machine_for_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_state_machine_for_execution",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe state machine for execution"):
        describe_state_machine_for_execution("test-execution_arn", region_name=REGION)


def test_get_activity_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_activity_task.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    get_activity_task("test-activity_arn", region_name=REGION)
    mock_client.get_activity_task.assert_called_once()


def test_get_activity_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_activity_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_activity_task",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get activity task"):
        get_activity_task("test-activity_arn", region_name=REGION)


def test_list_activities(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_activities.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_activities(region_name=REGION)
    mock_client.list_activities.assert_called_once()


def test_list_activities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_activities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_activities",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list activities"):
        list_activities(region_name=REGION)


def test_list_map_runs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_map_runs.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_map_runs("test-execution_arn", region_name=REGION)
    mock_client.list_map_runs.assert_called_once()


def test_list_map_runs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_map_runs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_map_runs",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list map runs"):
        list_map_runs("test-execution_arn", region_name=REGION)


def test_list_state_machine_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_state_machine_aliases.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_state_machine_aliases("test-state_machine_arn", region_name=REGION)
    mock_client.list_state_machine_aliases.assert_called_once()


def test_list_state_machine_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_state_machine_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_state_machine_aliases",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list state machine aliases"):
        list_state_machine_aliases("test-state_machine_arn", region_name=REGION)


def test_list_state_machine_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_state_machine_versions.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_state_machine_versions("test-state_machine_arn", region_name=REGION)
    mock_client.list_state_machine_versions.assert_called_once()


def test_list_state_machine_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_state_machine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_state_machine_versions",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list state machine versions"):
        list_state_machine_versions("test-state_machine_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_publish_state_machine_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_state_machine_version.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    publish_state_machine_version("test-state_machine_arn", region_name=REGION)
    mock_client.publish_state_machine_version.assert_called_once()


def test_publish_state_machine_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_state_machine_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_state_machine_version",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to publish state machine version"):
        publish_state_machine_version("test-state_machine_arn", region_name=REGION)


def test_redrive_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.redrive_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    redrive_execution("test-execution_arn", region_name=REGION)
    mock_client.redrive_execution.assert_called_once()


def test_redrive_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.redrive_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "redrive_execution",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to redrive execution"):
        redrive_execution("test-execution_arn", region_name=REGION)


def test_run_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_state.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    run_state("test-definition", region_name=REGION)
    mock_client.test_state.assert_called_once()


def test_run_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_state",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run state"):
        run_state("test-definition", region_name=REGION)


def test_send_task_failure(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_failure.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    send_task_failure("test-task_token", region_name=REGION)
    mock_client.send_task_failure.assert_called_once()


def test_send_task_failure_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_failure.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_task_failure",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send task failure"):
        send_task_failure("test-task_token", region_name=REGION)


def test_send_task_heartbeat(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_heartbeat.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    send_task_heartbeat("test-task_token", region_name=REGION)
    mock_client.send_task_heartbeat.assert_called_once()


def test_send_task_heartbeat_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_heartbeat.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_task_heartbeat",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send task heartbeat"):
        send_task_heartbeat("test-task_token", region_name=REGION)


def test_send_task_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_success.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    send_task_success("test-task_token", "test-output", region_name=REGION)
    mock_client.send_task_success.assert_called_once()


def test_send_task_success_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_task_success.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_task_success",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send task success"):
        send_task_success("test-task_token", "test-output", region_name=REGION)


def test_start_sync_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_sync_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    start_sync_execution("test-state_machine_arn", region_name=REGION)
    mock_client.start_sync_execution.assert_called_once()


def test_start_sync_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_sync_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_sync_execution",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start sync execution"):
        start_sync_execution("test-state_machine_arn", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_map_run(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_map_run.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_map_run("test-map_run_arn", region_name=REGION)
    mock_client.update_map_run.assert_called_once()


def test_update_map_run_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_map_run.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_map_run",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update map run"):
        update_map_run("test-map_run_arn", region_name=REGION)


def test_update_state_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_state_machine("test-state_machine_arn", region_name=REGION)
    mock_client.update_state_machine.assert_called_once()


def test_update_state_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_state_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_state_machine",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update state machine"):
        update_state_machine("test-state_machine_arn", region_name=REGION)


def test_update_state_machine_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)
    mock_client.update_state_machine_alias.assert_called_once()


def test_update_state_machine_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_state_machine_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_state_machine_alias",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update state machine alias"):
        update_state_machine_alias("test-state_machine_alias_arn", region_name=REGION)


def test_validate_state_machine_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_state_machine_definition.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    validate_state_machine_definition("test-definition", region_name=REGION)
    mock_client.validate_state_machine_definition.assert_called_once()


def test_validate_state_machine_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_state_machine_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_state_machine_definition",
    )
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to validate state machine definition"):
        validate_state_machine_definition("test-definition", region_name=REGION)


def test_create_activity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import create_activity
    mock_client = MagicMock()
    mock_client.create_activity.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_activity("test-name", tags=[{"Key": "k", "Value": "v"}], encryption_configuration={}, region_name="us-east-1")
    mock_client.create_activity.assert_called_once()

def test_create_state_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import create_state_machine
    mock_client = MagicMock()
    mock_client.create_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_state_machine("test-name", {}, "test-role_arn", type_value="test-type_value", logging_configuration={}, tags=[{"Key": "k", "Value": "v"}], tracing_configuration={}, publish=True, version_description="test-version_description", encryption_configuration={}, region_name="us-east-1")
    mock_client.create_state_machine.assert_called_once()

def test_create_state_machine_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import create_state_machine_alias
    mock_client = MagicMock()
    mock_client.create_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    create_state_machine_alias("test-name", {}, description="test-description", region_name="us-east-1")
    mock_client.create_state_machine_alias.assert_called_once()

def test_describe_state_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import describe_state_machine
    mock_client = MagicMock()
    mock_client.describe_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_state_machine("test-state_machine_arn", included_data=True, region_name="us-east-1")
    mock_client.describe_state_machine.assert_called_once()

def test_describe_state_machine_for_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import describe_state_machine_for_execution
    mock_client = MagicMock()
    mock_client.describe_state_machine_for_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    describe_state_machine_for_execution("test-execution_arn", included_data=True, region_name="us-east-1")
    mock_client.describe_state_machine_for_execution.assert_called_once()

def test_get_activity_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import get_activity_task
    mock_client = MagicMock()
    mock_client.get_activity_task.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    get_activity_task("test-activity_arn", worker_name="test-worker_name", region_name="us-east-1")
    mock_client.get_activity_task.assert_called_once()

def test_list_activities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import list_activities
    mock_client = MagicMock()
    mock_client.list_activities.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_activities(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_activities.assert_called_once()

def test_list_map_runs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import list_map_runs
    mock_client = MagicMock()
    mock_client.list_map_runs.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_map_runs("test-execution_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_map_runs.assert_called_once()

def test_list_state_machine_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import list_state_machine_aliases
    mock_client = MagicMock()
    mock_client.list_state_machine_aliases.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_state_machine_aliases("test-state_machine_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_state_machine_aliases.assert_called_once()

def test_list_state_machine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import list_state_machine_versions
    mock_client = MagicMock()
    mock_client.list_state_machine_versions.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    list_state_machine_versions("test-state_machine_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_state_machine_versions.assert_called_once()

def test_publish_state_machine_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import publish_state_machine_version
    mock_client = MagicMock()
    mock_client.publish_state_machine_version.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    publish_state_machine_version("test-state_machine_arn", revision_id="test-revision_id", description="test-description", region_name="us-east-1")
    mock_client.publish_state_machine_version.assert_called_once()

def test_redrive_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import redrive_execution
    mock_client = MagicMock()
    mock_client.redrive_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    redrive_execution("test-execution_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.redrive_execution.assert_called_once()

def test_run_state_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import run_state
    mock_client = MagicMock()
    mock_client.test_state.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    run_state({}, role_arn="test-role_arn", input="test-input", inspection_level="test-inspection_level", reveal_secrets="test-reveal_secrets", variables="test-variables", region_name="us-east-1")
    mock_client.test_state.assert_called_once()

def test_send_task_failure_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import send_task_failure
    mock_client = MagicMock()
    mock_client.send_task_failure.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    send_task_failure("test-task_token", error="test-error", cause="test-cause", region_name="us-east-1")
    mock_client.send_task_failure.assert_called_once()

def test_start_sync_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import start_sync_execution
    mock_client = MagicMock()
    mock_client.start_sync_execution.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    start_sync_execution("test-state_machine_arn", name="test-name", input="test-input", trace_header="test-trace_header", included_data=True, region_name="us-east-1")
    mock_client.start_sync_execution.assert_called_once()

def test_update_map_run_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import update_map_run
    mock_client = MagicMock()
    mock_client.update_map_run.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_map_run("test-map_run_arn", max_concurrency=1, tolerated_failure_percentage="test-tolerated_failure_percentage", tolerated_failure_count=1, region_name="us-east-1")
    mock_client.update_map_run.assert_called_once()

def test_update_state_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import update_state_machine
    mock_client = MagicMock()
    mock_client.update_state_machine.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_state_machine("test-state_machine_arn", definition={}, role_arn="test-role_arn", logging_configuration={}, tracing_configuration={}, publish=True, version_description="test-version_description", encryption_configuration={}, region_name="us-east-1")
    mock_client.update_state_machine.assert_called_once()

def test_update_state_machine_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import update_state_machine_alias
    mock_client = MagicMock()
    mock_client.update_state_machine_alias.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    update_state_machine_alias("test-state_machine_alias_arn", description="test-description", routing_configuration={}, region_name="us-east-1")
    mock_client.update_state_machine_alias.assert_called_once()

def test_validate_state_machine_definition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.stepfunctions import validate_state_machine_definition
    mock_client = MagicMock()
    mock_client.validate_state_machine_definition.return_value = {}
    monkeypatch.setattr("aws_util.stepfunctions.get_client", lambda *a, **kw: mock_client)
    validate_state_machine_definition({}, type_value="test-type_value", severity="test-severity", max_results=1, region_name="us-east-1")
    mock_client.validate_state_machine_definition.assert_called_once()
