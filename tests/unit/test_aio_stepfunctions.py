from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.stepfunctions import (
    SFNExecution,
    StateMachine,
    describe_execution,
    get_execution_history,
    list_executions,
    list_state_machines,
    run_and_wait,
    start_execution,
    stop_execution,
    wait_for_execution,
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


_SM_ARN = "arn:aws:states:us-east-1:123:stateMachine:TestSM"
_EXEC_ARN = "arn:aws:states:us-east-1:123:execution:TestSM:run-1"


# ---------------------------------------------------------------------------
# start_execution
# ---------------------------------------------------------------------------


async def test_start_execution_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "executionArn": _EXEC_ARN,
        "startDate": "2024-01-01T00:00:00Z",
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_execution(_SM_ARN)
    assert result.execution_arn == _EXEC_ARN
    assert result.status == "RUNNING"


async def test_start_execution_with_name(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "executionArn": _EXEC_ARN,
        "startDate": "2024-01-01",
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await start_execution(_SM_ARN, input_data={"k": "v"}, name="my-run")
    assert result.execution_arn == _EXEC_ARN


async def test_start_execution_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_execution(_SM_ARN)


async def test_start_execution_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to start execution"):
        await start_execution(_SM_ARN)


# ---------------------------------------------------------------------------
# describe_execution
# ---------------------------------------------------------------------------


async def test_describe_execution_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "executionArn": _EXEC_ARN,
        "stateMachineArn": _SM_ARN,
        "name": "run-1",
        "status": "SUCCEEDED",
        "input": '{"key": "val"}',
        "output": '{"result": 1}',
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_execution(_EXEC_ARN)
    assert result.status == "SUCCEEDED"


async def test_describe_execution_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await describe_execution(_EXEC_ARN)


async def test_describe_execution_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_execution failed"):
        await describe_execution(_EXEC_ARN)


# ---------------------------------------------------------------------------
# stop_execution
# ---------------------------------------------------------------------------


async def test_stop_execution_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_execution(_EXEC_ARN)
    mock_client.call.assert_awaited_once()


async def test_stop_execution_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await stop_execution(_EXEC_ARN)


async def test_stop_execution_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="stop_execution failed"):
        await stop_execution(_EXEC_ARN)


# ---------------------------------------------------------------------------
# list_executions
# ---------------------------------------------------------------------------


async def test_list_executions_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "executions": [
            {
                "executionArn": _EXEC_ARN,
                "stateMachineArn": _SM_ARN,
                "name": "run-1",
                "status": "SUCCEEDED",
                "startDate": "2024-01-01",
                "stopDate": "2024-01-01",
            }
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_executions(_SM_ARN)
    assert len(result) == 1
    assert result[0].status == "SUCCEEDED"


async def test_list_executions_with_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"executions": []}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_executions(_SM_ARN, status_filter="RUNNING")
    assert result == []


async def test_list_executions_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "executions": [
                    {
                        "executionArn": f"{_EXEC_ARN}:a",
                        "stateMachineArn": _SM_ARN,
                        "name": "a",
                        "status": "RUNNING",
                    }
                ],
                "nextToken": "tok",
            }
        return {
            "executions": [
                {
                    "executionArn": f"{_EXEC_ARN}:b",
                    "stateMachineArn": _SM_ARN,
                    "name": "b",
                    "status": "SUCCEEDED",
                }
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_executions(_SM_ARN)
    assert len(result) == 2


async def test_list_executions_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_executions(_SM_ARN)


async def test_list_executions_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_executions failed"):
        await list_executions(_SM_ARN)


# ---------------------------------------------------------------------------
# wait_for_execution
# ---------------------------------------------------------------------------


async def test_wait_for_execution_immediate(monkeypatch: pytest.MonkeyPatch) -> None:
    finished_exec = SFNExecution(
        execution_arn=_EXEC_ARN,
        state_machine_arn=_SM_ARN,
        name="run-1",
        status="SUCCEEDED",
    )

    async def _fake_describe(arn, region_name=None):
        return finished_exec

    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.describe_execution", _fake_describe
    )
    monkeypatch.setattr("aws_util.aio.stepfunctions.asyncio.sleep", AsyncMock())
    result = await wait_for_execution(_EXEC_ARN)
    assert result.status == "SUCCEEDED"


async def test_wait_for_execution_becomes_finished(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0

    async def _fake_describe(arn, region_name=None):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return SFNExecution(
                execution_arn=arn,
                state_machine_arn=_SM_ARN,
                name="r",
                status="RUNNING",
            )
        return SFNExecution(
            execution_arn=arn,
            state_machine_arn=_SM_ARN,
            name="r",
            status="SUCCEEDED",
        )

    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.describe_execution", _fake_describe
    )
    monkeypatch.setattr("aws_util.aio.stepfunctions.asyncio.sleep", AsyncMock())
    result = await wait_for_execution(_EXEC_ARN, timeout=60.0)
    assert result.status == "SUCCEEDED"


async def test_wait_for_execution_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _fake_describe(arn, region_name=None):
        return SFNExecution(
            execution_arn=arn,
            state_machine_arn=_SM_ARN,
            name="r",
            status="RUNNING",
        )

    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.describe_execution", _fake_describe
    )
    monkeypatch.setattr("aws_util.aio.stepfunctions.asyncio.sleep", AsyncMock())
    with pytest.raises(TimeoutError, match="did not finish"):
        await wait_for_execution(_EXEC_ARN, timeout=0.0)


# ---------------------------------------------------------------------------
# list_state_machines
# ---------------------------------------------------------------------------


async def test_list_state_machines_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "stateMachines": [
            {
                "stateMachineArn": _SM_ARN,
                "name": "TestSM",
                "type": "STANDARD",
                "status": "ACTIVE",
                "creationDate": "2024-01-01",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_state_machines()
    assert len(result) == 1
    assert result[0].name == "TestSM"


async def test_list_state_machines_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"stateMachines": []}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_state_machines()
    assert result == []


async def test_list_state_machines_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "stateMachines": [
                    {
                        "stateMachineArn": f"{_SM_ARN}:a",
                        "name": "A",
                    }
                ],
                "nextToken": "tok",
            }
        return {
            "stateMachines": [
                {
                    "stateMachineArn": f"{_SM_ARN}:b",
                    "name": "B",
                }
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_state_machines()
    assert len(result) == 2


async def test_list_state_machines_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_state_machines()


async def test_list_state_machines_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_state_machines failed"):
        await list_state_machines()


# ---------------------------------------------------------------------------
# run_and_wait
# ---------------------------------------------------------------------------


async def test_run_and_wait_success(monkeypatch: pytest.MonkeyPatch) -> None:
    started = SFNExecution(
        execution_arn=_EXEC_ARN,
        state_machine_arn=_SM_ARN,
        name="run-1",
        status="RUNNING",
    )
    finished = SFNExecution(
        execution_arn=_EXEC_ARN,
        state_machine_arn=_SM_ARN,
        name="run-1",
        status="SUCCEEDED",
    )

    async def _fake_start(arn, input_data=None, name=None, region_name=None):
        return started

    async def _fake_wait(arn, poll_interval=5.0, timeout=600.0, region_name=None):
        return finished

    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.start_execution", _fake_start
    )
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.wait_for_execution", _fake_wait
    )
    result = await run_and_wait(_SM_ARN, input_data={"x": 1}, name="r")
    assert result.status == "SUCCEEDED"


# ---------------------------------------------------------------------------
# get_execution_history
# ---------------------------------------------------------------------------


async def test_get_execution_history_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "events": [
            {"id": 1, "type": "ExecutionStarted"},
            {"id": 2, "type": "TaskStateEntered"},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_execution_history(_EXEC_ARN)
    assert len(result) == 2


async def test_get_execution_history_no_data(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "events": [{"id": 1, "type": "ExecutionStarted"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_execution_history(_EXEC_ARN, include_execution_data=False)
    assert len(result) == 1


async def test_get_execution_history_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "events": [{"id": 1}],
                "nextToken": "tok",
            }
        return {"events": [{"id": 2}]}

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_execution_history(_EXEC_ARN)
    assert len(result) == 2


async def test_get_execution_history_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_execution_history(_EXEC_ARN)


async def test_get_execution_history_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_execution_history failed"):
        await get_execution_history(_EXEC_ARN)


async def test_create_activity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_activity("test-name", )
    mock_client.call.assert_called_once()


async def test_create_activity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_activity("test-name", )


async def test_create_state_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_state_machine("test-name", "test-definition", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_state_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_state_machine("test-name", "test-definition", "test-role_arn", )


async def test_create_state_machine_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_state_machine_alias("test-name", [], )
    mock_client.call.assert_called_once()


async def test_create_state_machine_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_state_machine_alias("test-name", [], )


async def test_delete_activity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_activity("test-activity_arn", )
    mock_client.call.assert_called_once()


async def test_delete_activity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_activity("test-activity_arn", )


async def test_delete_state_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_state_machine("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_delete_state_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_state_machine("test-state_machine_arn", )


async def test_delete_state_machine_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_state_machine_alias("test-state_machine_alias_arn", )
    mock_client.call.assert_called_once()


async def test_delete_state_machine_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_state_machine_alias("test-state_machine_alias_arn", )


async def test_delete_state_machine_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_state_machine_version("test-state_machine_version_arn", )
    mock_client.call.assert_called_once()


async def test_delete_state_machine_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_state_machine_version("test-state_machine_version_arn", )


async def test_describe_activity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_activity("test-activity_arn", )
    mock_client.call.assert_called_once()


async def test_describe_activity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_activity("test-activity_arn", )


async def test_describe_map_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_map_run("test-map_run_arn", )
    mock_client.call.assert_called_once()


async def test_describe_map_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_map_run("test-map_run_arn", )


async def test_describe_state_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_state_machine("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_describe_state_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_state_machine("test-state_machine_arn", )


async def test_describe_state_machine_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_state_machine_alias("test-state_machine_alias_arn", )
    mock_client.call.assert_called_once()


async def test_describe_state_machine_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_state_machine_alias("test-state_machine_alias_arn", )


async def test_describe_state_machine_for_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_state_machine_for_execution("test-execution_arn", )
    mock_client.call.assert_called_once()


async def test_describe_state_machine_for_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_state_machine_for_execution("test-execution_arn", )


async def test_get_activity_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_activity_task("test-activity_arn", )
    mock_client.call.assert_called_once()


async def test_get_activity_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_activity_task("test-activity_arn", )


async def test_list_activities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_activities()
    mock_client.call.assert_called_once()


async def test_list_activities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_activities()


async def test_list_map_runs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_map_runs("test-execution_arn", )
    mock_client.call.assert_called_once()


async def test_list_map_runs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_map_runs("test-execution_arn", )


async def test_list_state_machine_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_state_machine_aliases("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_list_state_machine_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_state_machine_aliases("test-state_machine_arn", )


async def test_list_state_machine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_state_machine_versions("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_list_state_machine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_state_machine_versions("test-state_machine_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_publish_state_machine_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_state_machine_version("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_publish_state_machine_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_state_machine_version("test-state_machine_arn", )


async def test_redrive_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await redrive_execution("test-execution_arn", )
    mock_client.call.assert_called_once()


async def test_redrive_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await redrive_execution("test-execution_arn", )


async def test_run_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_state("test-definition", )
    mock_client.call.assert_called_once()


async def test_run_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_state("test-definition", )


async def test_send_task_failure(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_task_failure("test-task_token", )
    mock_client.call.assert_called_once()


async def test_send_task_failure_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_task_failure("test-task_token", )


async def test_send_task_heartbeat(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_task_heartbeat("test-task_token", )
    mock_client.call.assert_called_once()


async def test_send_task_heartbeat_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_task_heartbeat("test-task_token", )


async def test_send_task_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_task_success("test-task_token", "test-output", )
    mock_client.call.assert_called_once()


async def test_send_task_success_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_task_success("test-task_token", "test-output", )


async def test_start_sync_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_sync_execution("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_start_sync_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_sync_execution("test-state_machine_arn", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_map_run(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_map_run("test-map_run_arn", )
    mock_client.call.assert_called_once()


async def test_update_map_run_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_map_run("test-map_run_arn", )


async def test_update_state_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_state_machine("test-state_machine_arn", )
    mock_client.call.assert_called_once()


async def test_update_state_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_state_machine("test-state_machine_arn", )


async def test_update_state_machine_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_state_machine_alias("test-state_machine_alias_arn", )
    mock_client.call.assert_called_once()


async def test_update_state_machine_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_state_machine_alias("test-state_machine_alias_arn", )


async def test_validate_state_machine_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_state_machine_definition("test-definition", )
    mock_client.call.assert_called_once()


async def test_validate_state_machine_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.stepfunctions.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_state_machine_definition("test-definition", )


@pytest.mark.asyncio
async def test_create_activity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import create_activity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await create_activity("test-name", tags=[{"Key": "k", "Value": "v"}], encryption_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_state_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import create_state_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await create_state_machine("test-name", {}, "test-role_arn", type_value="test-type_value", logging_configuration={}, tags=[{"Key": "k", "Value": "v"}], tracing_configuration={}, publish=True, version_description="test-version_description", encryption_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_state_machine_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import create_state_machine_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await create_state_machine_alias("test-name", {}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_state_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import describe_state_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await describe_state_machine("test-state_machine_arn", included_data=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_state_machine_for_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import describe_state_machine_for_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await describe_state_machine_for_execution("test-execution_arn", included_data=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_activity_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import get_activity_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await get_activity_task("test-activity_arn", worker_name="test-worker_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_activities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import list_activities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await list_activities(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_map_runs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import list_map_runs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await list_map_runs("test-execution_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_state_machine_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import list_state_machine_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await list_state_machine_aliases("test-state_machine_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_state_machine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import list_state_machine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await list_state_machine_versions("test-state_machine_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_state_machine_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import publish_state_machine_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await publish_state_machine_version("test-state_machine_arn", revision_id="test-revision_id", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_redrive_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import redrive_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await redrive_execution("test-execution_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_state_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import run_state
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await run_state({}, role_arn="test-role_arn", input="test-input", inspection_level="test-inspection_level", reveal_secrets="test-reveal_secrets", variables="test-variables", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_task_failure_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import send_task_failure
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await send_task_failure("test-task_token", error="test-error", cause="test-cause", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_sync_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import start_sync_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await start_sync_execution("test-state_machine_arn", name="test-name", input="test-input", trace_header="test-trace_header", included_data=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_map_run_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import update_map_run
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await update_map_run("test-map_run_arn", max_concurrency=1, tolerated_failure_percentage="test-tolerated_failure_percentage", tolerated_failure_count=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_state_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import update_state_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await update_state_machine("test-state_machine_arn", definition={}, role_arn="test-role_arn", logging_configuration={}, tracing_configuration={}, publish=True, version_description="test-version_description", encryption_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_state_machine_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import update_state_machine_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await update_state_machine_alias("test-state_machine_alias_arn", description="test-description", routing_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_state_machine_definition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.stepfunctions import validate_state_machine_definition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.stepfunctions.async_client", lambda *a, **kw: mock_client)
    await validate_state_machine_definition({}, type_value="test-type_value", severity="test-severity", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
