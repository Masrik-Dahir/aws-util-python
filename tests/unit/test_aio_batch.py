"""Tests for aws_util.aio.batch — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.batch import (
    ComputeEnvironmentResult,
    JobDefinitionResult,
    JobQueueResult,
    JobResult,
    cancel_job,
    create_compute_environment,
    create_job_queue,
    delete_compute_environment,
    delete_job_queue,
    deregister_job_definition,
    describe_compute_environments,
    describe_job_definitions,
    describe_job_queues,
    describe_jobs,
    list_jobs,
    register_job_definition,
    submit_and_wait,
    submit_job,
    terminate_job,
    update_compute_environment,
    update_job_queue,
    wait_for_job,
    create_consumable_resource,
    create_scheduling_policy,
    create_service_environment,
    delete_consumable_resource,
    delete_scheduling_policy,
    delete_service_environment,
    describe_consumable_resource,
    describe_scheduling_policies,
    describe_service_environments,
    describe_service_job,
    get_job_queue_snapshot,
    list_consumable_resources,
    list_jobs_by_consumable_resource,
    list_scheduling_policies,
    list_service_jobs,
    list_tags_for_resource,
    submit_service_job,
    tag_resource,
    terminate_service_job,
    untag_resource,
    update_consumable_resource,
    update_scheduling_policy,
    update_service_environment,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError


REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


CE_NAME = "test-ce"
CE_ARN = "arn:aws:batch:us-east-1:123456789012:compute-environment/test-ce"
JQ_NAME = "test-jq"
JQ_ARN = "arn:aws:batch:us-east-1:123456789012:job-queue/test-jq"
JD_NAME = "test-jd"
JD_ARN = "arn:aws:batch:us-east-1:123456789012:job-definition/test-jd:1"
JOB_ID = "job-12345"
JOB_NAME = "test-job"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _ce_dict(**kwargs) -> dict:
    defaults = {
        "computeEnvironmentName": CE_NAME,
        "computeEnvironmentArn": CE_ARN,
        "type": "MANAGED",
        "state": "ENABLED",
        "status": "VALID",
        "computeResources": {"type": "EC2", "minvCpus": 0},
        "serviceRole": "arn:aws:iam::123:role/Batch",
    }
    defaults.update(kwargs)
    return defaults


def _jq_dict(**kwargs) -> dict:
    defaults = {
        "jobQueueName": JQ_NAME,
        "jobQueueArn": JQ_ARN,
        "state": "ENABLED",
        "status": "VALID",
        "priority": 1,
        "computeEnvironmentOrder": [
            {"computeEnvironment": CE_ARN, "order": 1}
        ],
    }
    defaults.update(kwargs)
    return defaults


def _jd_dict(**kwargs) -> dict:
    defaults = {
        "jobDefinitionName": JD_NAME,
        "jobDefinitionArn": JD_ARN,
        "revision": 1,
        "type": "container",
        "status": "ACTIVE",
        "containerProperties": {"image": "busybox", "vcpus": 1, "memory": 512},
    }
    defaults.update(kwargs)
    return defaults


def _job_dict(**kwargs) -> dict:
    defaults = {
        "jobId": JOB_ID,
        "jobName": JOB_NAME,
        "jobQueue": JQ_ARN,
        "status": "SUBMITTED",
        "createdAt": 1609459200,
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# create_compute_environment
# ---------------------------------------------------------------------------


async def test_create_ce_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "computeEnvironmentArn": CE_ARN,
        "computeEnvironmentName": CE_NAME,
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await create_compute_environment(CE_NAME)
    assert isinstance(result, ComputeEnvironmentResult)
    assert result.arn == CE_ARN


async def test_create_ce_with_resources_and_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "computeEnvironmentArn": CE_ARN,
        "computeEnvironmentName": CE_NAME,
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await create_compute_environment(
        CE_NAME,
        compute_resources={"type": "EC2"},
        service_role="arn:aws:iam::123:role/Batch",
    )
    assert result.compute_resources == {"type": "EC2"}
    assert result.service_role == "arn:aws:iam::123:role/Batch"
    call_kwargs = mock_client.call.call_args[1]
    assert "computeResources" in call_kwargs
    assert "serviceRole" in call_kwargs


async def test_create_ce_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_compute_environment(CE_NAME)


async def test_create_ce_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_compute_environment failed"):
        await create_compute_environment(CE_NAME)


# ---------------------------------------------------------------------------
# describe_compute_environments
# ---------------------------------------------------------------------------


async def test_describe_ce_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "computeEnvironments": [_ce_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_compute_environments(names=[CE_NAME])
    assert len(result) == 1
    assert result[0].name == CE_NAME


async def test_describe_ce_without_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"computeEnvironments": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_compute_environments()
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert "computeEnvironments" not in call_kwargs


async def test_describe_ce_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_compute_environments()


async def test_describe_ce_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_compute_environments failed"):
        await describe_compute_environments()


# ---------------------------------------------------------------------------
# update_compute_environment
# ---------------------------------------------------------------------------


async def test_update_ce_with_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"computeEnvironmentArn": CE_ARN},  # update
        {"computeEnvironments": [_ce_dict(state="DISABLED")]},  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_compute_environment(CE_NAME, state="DISABLED")
    assert result.state == "DISABLED"


async def test_update_ce_with_compute_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"computeEnvironmentArn": CE_ARN},  # update
        {"computeEnvironments": [_ce_dict()]},  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_compute_environment(
        CE_NAME, compute_resources={"maxvCpus": 10}
    )
    assert isinstance(result, ComputeEnvironmentResult)
    call_kwargs = mock_client.call.call_args_list[0][1]
    assert "computeResources" in call_kwargs


async def test_update_ce_fallback_empty_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"computeEnvironmentArn": CE_ARN},  # update
        {"computeEnvironments": []},  # describe returns empty
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_compute_environment(CE_NAME)
    assert result.name == CE_NAME
    assert result.state == "ENABLED"


async def test_update_ce_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await update_compute_environment(CE_NAME)


async def test_update_ce_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_compute_environment failed"):
        await update_compute_environment(CE_NAME)


# ---------------------------------------------------------------------------
# delete_compute_environment
# ---------------------------------------------------------------------------


async def test_delete_ce_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await delete_compute_environment(CE_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_ce_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_compute_environment(CE_NAME)


async def test_delete_ce_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_compute_environment failed"):
        await delete_compute_environment(CE_NAME)


# ---------------------------------------------------------------------------
# create_job_queue
# ---------------------------------------------------------------------------


async def test_create_jq_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobQueueArn": JQ_ARN,
        "jobQueueName": JQ_NAME,
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    ce_order = [{"computeEnvironment": CE_ARN, "order": 1}]
    result = await create_job_queue(JQ_NAME, compute_environments=ce_order)
    assert isinstance(result, JobQueueResult)
    assert result.arn == JQ_ARN


async def test_create_jq_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_job_queue(JQ_NAME, compute_environments=[])


async def test_create_jq_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_job_queue failed"):
        await create_job_queue(JQ_NAME, compute_environments=[])


# ---------------------------------------------------------------------------
# describe_job_queues
# ---------------------------------------------------------------------------


async def test_describe_jq_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobQueues": [_jq_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_job_queues(names=[JQ_NAME])
    assert len(result) == 1


async def test_describe_jq_without_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobQueues": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_job_queues()
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert "jobQueues" not in call_kwargs


async def test_describe_jq_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_job_queues()


async def test_describe_jq_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_job_queues failed"):
        await describe_job_queues()


# ---------------------------------------------------------------------------
# update_job_queue
# ---------------------------------------------------------------------------


async def test_update_jq_with_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobQueueArn": JQ_ARN},  # update
        {"jobQueues": [_jq_dict(state="DISABLED")]},  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_job_queue(JQ_NAME, state="DISABLED")
    assert result.state == "DISABLED"


async def test_update_jq_with_priority_and_ce(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobQueueArn": JQ_ARN},  # update
        {"jobQueues": [_jq_dict(priority=5)]},  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_job_queue(
        JQ_NAME, priority=5,
        compute_environments=[{"computeEnvironment": CE_ARN, "order": 1}],
    )
    assert result.priority == 5
    call_kwargs = mock_client.call.call_args_list[0][1]
    assert "priority" in call_kwargs
    assert "computeEnvironmentOrder" in call_kwargs


async def test_update_jq_fallback_empty_describe(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobQueueArn": JQ_ARN},  # update
        {"jobQueues": []},  # describe returns empty
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await update_job_queue(JQ_NAME)
    assert result.name == JQ_NAME


async def test_update_jq_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await update_job_queue(JQ_NAME)


async def test_update_jq_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_job_queue failed"):
        await update_job_queue(JQ_NAME)


# ---------------------------------------------------------------------------
# delete_job_queue
# ---------------------------------------------------------------------------


async def test_delete_jq_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await delete_job_queue(JQ_NAME)
    mock_client.call.assert_awaited_once()


async def test_delete_jq_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_job_queue(JQ_NAME)


async def test_delete_jq_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_job_queue failed"):
        await delete_job_queue(JQ_NAME)


# ---------------------------------------------------------------------------
# register_job_definition
# ---------------------------------------------------------------------------


async def test_register_jd_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobDefinitionArn": JD_ARN,
        "jobDefinitionName": JD_NAME,
        "revision": 1,
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await register_job_definition(JD_NAME)
    assert isinstance(result, JobDefinitionResult)
    assert result.arn == JD_ARN


async def test_register_jd_with_container_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobDefinitionArn": JD_ARN,
        "jobDefinitionName": JD_NAME,
        "revision": 1,
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    props = {"image": "busybox", "vcpus": 1, "memory": 512}
    result = await register_job_definition(
        JD_NAME, container_properties=props,
    )
    assert result.container_properties == props
    call_kwargs = mock_client.call.call_args[1]
    assert "containerProperties" in call_kwargs


async def test_register_jd_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await register_job_definition(JD_NAME)


async def test_register_jd_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="register_job_definition failed"):
        await register_job_definition(JD_NAME)


# ---------------------------------------------------------------------------
# describe_job_definitions
# ---------------------------------------------------------------------------


async def test_describe_jd_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobDefinitions": [_jd_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_job_definitions(names=[JD_NAME])
    assert len(result) == 1


async def test_describe_jd_without_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobDefinitions": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_job_definitions()
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert "jobDefinitions" not in call_kwargs


async def test_describe_jd_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_job_definitions()


async def test_describe_jd_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_job_definitions failed"):
        await describe_job_definitions()


# ---------------------------------------------------------------------------
# deregister_job_definition
# ---------------------------------------------------------------------------


async def test_deregister_jd_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await deregister_job_definition(JD_ARN)
    mock_client.call.assert_awaited_once()


async def test_deregister_jd_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await deregister_job_definition(JD_ARN)


async def test_deregister_jd_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="deregister_job_definition failed"):
        await deregister_job_definition(JD_ARN)


# ---------------------------------------------------------------------------
# submit_job
# ---------------------------------------------------------------------------


async def test_submit_job_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobId": JOB_ID, "jobName": JOB_NAME}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await submit_job(
        JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
    )
    assert result == JOB_ID


async def test_submit_job_with_params_and_overrides(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobId": JOB_ID, "jobName": JOB_NAME}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await submit_job(
        JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
        parameters={"key": "val"},
        container_overrides={"vcpus": 2},
    )
    assert result == JOB_ID
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["parameters"] == {"key": "val"}
    assert call_kwargs["containerOverrides"] == {"vcpus": 2}


async def test_submit_job_no_params_no_overrides(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobId": JOB_ID, "jobName": JOB_NAME}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await submit_job(JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME)
    call_kwargs = mock_client.call.call_args[1]
    assert "parameters" not in call_kwargs
    assert "containerOverrides" not in call_kwargs


async def test_submit_job_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await submit_job(JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME)


async def test_submit_job_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="submit_job failed"):
        await submit_job(JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME)


# ---------------------------------------------------------------------------
# describe_jobs
# ---------------------------------------------------------------------------


async def test_describe_jobs_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobs": [_job_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_jobs([JOB_ID])
    assert len(result) == 1
    assert result[0].job_id == JOB_ID


async def test_describe_jobs_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobs": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await describe_jobs(["nonexistent"])
    assert result == []


async def test_describe_jobs_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_jobs([JOB_ID])


async def test_describe_jobs_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_jobs failed"):
        await describe_jobs([JOB_ID])


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------


async def test_list_jobs_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobSummaryList": [_job_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await list_jobs(JQ_NAME)
    assert len(result) == 1


async def test_list_jobs_with_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobSummaryList": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await list_jobs(JQ_NAME, job_status="RUNNING")
    assert result == []
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["jobStatus"] == "RUNNING"


async def test_list_jobs_no_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobSummaryList": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await list_jobs(JQ_NAME)
    call_kwargs = mock_client.call.call_args[1]
    assert "jobStatus" not in call_kwargs


async def test_list_jobs_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_jobs(JQ_NAME)


async def test_list_jobs_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_jobs failed"):
        await list_jobs(JQ_NAME)


# ---------------------------------------------------------------------------
# cancel_job
# ---------------------------------------------------------------------------


async def test_cancel_job_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await cancel_job(JOB_ID, reason="Testing")
    mock_client.call.assert_awaited_once()


async def test_cancel_job_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await cancel_job(JOB_ID, reason="Testing")


async def test_cancel_job_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="cancel_job failed"):
        await cancel_job(JOB_ID, reason="Testing")


# ---------------------------------------------------------------------------
# terminate_job
# ---------------------------------------------------------------------------


async def test_terminate_job_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    await terminate_job(JOB_ID, reason="Testing")
    mock_client.call.assert_awaited_once()


async def test_terminate_job_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await terminate_job(JOB_ID, reason="Testing")


async def test_terminate_job_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="terminate_job failed"):
        await terminate_job(JOB_ID, reason="Testing")


# ---------------------------------------------------------------------------
# wait_for_job
# ---------------------------------------------------------------------------


async def test_wait_for_job_immediate_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobs": [_job_dict(status="SUCCEEDED")]
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_job(JOB_ID)
    assert result.status == "SUCCEEDED"


async def test_wait_for_job_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobs": [_job_dict(status="RUNNING")]},
        {"jobs": [_job_dict(status="SUCCEEDED")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.batch.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_job(
            JOB_ID, timeout=300, poll_interval=0.01,
        )
    assert result.status == "SUCCEEDED"


async def test_wait_for_job_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"jobs": []}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_job(JOB_ID)


async def test_wait_for_job_failure_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobs": [_job_dict(status="FAILED", statusReason="OOM")]
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="failure status"):
        await wait_for_job(JOB_ID)


async def test_wait_for_job_failure_no_reason(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobs": [_job_dict(status="FAILED")]
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="no reason"):
        await wait_for_job(JOB_ID)


async def test_wait_for_job_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "jobs": [_job_dict(status="RUNNING")]
    }
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.batch.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises((TimeoutError, AwsTimeoutError)):
            await wait_for_job(
                JOB_ID, timeout=0.0, poll_interval=0.001,
            )


# ---------------------------------------------------------------------------
# submit_and_wait
# ---------------------------------------------------------------------------


async def test_submit_and_wait_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobId": JOB_ID, "jobName": JOB_NAME},  # submit
        {"jobs": [_job_dict(status="SUCCEEDED")]},  # describe (wait_for_job)
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await submit_and_wait(
        JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
    )
    assert result.status == "SUCCEEDED"


async def test_submit_and_wait_with_params(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"jobId": JOB_ID, "jobName": JOB_NAME},  # submit
        {"jobs": [_job_dict(status="SUCCEEDED")]},  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client", _mock_factory(mock_client)
    )
    result = await submit_and_wait(
        JOB_NAME, job_queue=JQ_NAME, job_definition=JD_NAME,
        parameters={"key": "val"},
        container_overrides={"vcpus": 2},
        timeout=30, poll_interval=1,
    )
    assert result.status == "SUCCEEDED"


async def test_create_consumable_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_consumable_resource("test-consumable_resource_name", )
    mock_client.call.assert_called_once()


async def test_create_consumable_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_consumable_resource("test-consumable_resource_name", )


async def test_create_scheduling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_scheduling_policy("test-name", )
    mock_client.call.assert_called_once()


async def test_create_scheduling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_scheduling_policy("test-name", )


async def test_create_service_environment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_environment("test-service_environment_name", "test-service_environment_type", [], )
    mock_client.call.assert_called_once()


async def test_create_service_environment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_environment("test-service_environment_name", "test-service_environment_type", [], )


async def test_delete_consumable_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_consumable_resource("test-consumable_resource", )
    mock_client.call.assert_called_once()


async def test_delete_consumable_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_consumable_resource("test-consumable_resource", )


async def test_delete_scheduling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_scheduling_policy("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_scheduling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_scheduling_policy("test-arn", )


async def test_delete_service_environment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_environment("test-service_environment", )
    mock_client.call.assert_called_once()


async def test_delete_service_environment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_environment("test-service_environment", )


async def test_describe_consumable_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_consumable_resource("test-consumable_resource", )
    mock_client.call.assert_called_once()


async def test_describe_consumable_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_consumable_resource("test-consumable_resource", )


async def test_describe_scheduling_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduling_policies([], )
    mock_client.call.assert_called_once()


async def test_describe_scheduling_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduling_policies([], )


async def test_describe_service_environments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_environments()
    mock_client.call.assert_called_once()


async def test_describe_service_environments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_environments()


async def test_describe_service_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_service_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_job("test-job_id", )


async def test_get_job_queue_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_job_queue_snapshot("test-job_queue", )
    mock_client.call.assert_called_once()


async def test_get_job_queue_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_job_queue_snapshot("test-job_queue", )


async def test_list_consumable_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_consumable_resources()
    mock_client.call.assert_called_once()


async def test_list_consumable_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_consumable_resources()


async def test_list_jobs_by_consumable_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_jobs_by_consumable_resource("test-consumable_resource", )
    mock_client.call.assert_called_once()


async def test_list_jobs_by_consumable_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_jobs_by_consumable_resource("test-consumable_resource", )


async def test_list_scheduling_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_scheduling_policies()
    mock_client.call.assert_called_once()


async def test_list_scheduling_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_scheduling_policies()


async def test_list_service_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_jobs()
    mock_client.call.assert_called_once()


async def test_list_service_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_jobs()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_submit_service_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", )
    mock_client.call.assert_called_once()


async def test_submit_service_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_terminate_service_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await terminate_service_job("test-job_id", "test-reason", )
    mock_client.call.assert_called_once()


async def test_terminate_service_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await terminate_service_job("test-job_id", "test-reason", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_consumable_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_consumable_resource("test-consumable_resource", )
    mock_client.call.assert_called_once()


async def test_update_consumable_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_consumable_resource("test-consumable_resource", )


async def test_update_scheduling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_scheduling_policy("test-arn", )
    mock_client.call.assert_called_once()


async def test_update_scheduling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_scheduling_policy("test-arn", )


async def test_update_service_environment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_service_environment("test-service_environment", )
    mock_client.call.assert_called_once()


async def test_update_service_environment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.batch.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_service_environment("test-service_environment", )


@pytest.mark.asyncio
async def test_describe_compute_environments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import describe_compute_environments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await describe_compute_environments(names="test-names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_job_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import describe_job_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await describe_job_queues(names="test-names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_job_definitions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import describe_job_definitions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await describe_job_definitions(names="test-names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import list_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await list_jobs("test-job_queue", job_status="test-job_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_consumable_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import create_consumable_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await create_consumable_resource("test-consumable_resource_name", total_quantity="test-total_quantity", resource_type="test-resource_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_scheduling_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import create_scheduling_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await create_scheduling_policy("test-name", fairshare_policy="{}", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_environment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import create_service_environment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await create_service_environment("test-service_environment_name", "test-service_environment_type", 1, state="test-state", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_service_environments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import describe_service_environments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await describe_service_environments(service_environments="test-service_environments", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_consumable_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import list_consumable_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await list_consumable_resources(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_jobs_by_consumable_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import list_jobs_by_consumable_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await list_jobs_by_consumable_resource("test-consumable_resource", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_scheduling_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import list_scheduling_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await list_scheduling_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import list_service_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await list_service_jobs(job_queue="test-job_queue", job_status="test-job_status", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_submit_service_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import submit_service_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await submit_service_job("test-job_name", "test-job_queue", "test-service_request_payload", "test-service_job_type", retry_strategy="test-retry_strategy", scheduling_priority="test-scheduling_priority", share_identifier="test-share_identifier", timeout_config=1, tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_consumable_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import update_consumable_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await update_consumable_resource("test-consumable_resource", operation="test-operation", quantity="test-quantity", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_scheduling_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import update_scheduling_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await update_scheduling_policy("test-arn", fairshare_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_service_environment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.batch import update_service_environment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.batch.async_client", lambda *a, **kw: mock_client)
    await update_service_environment("test-service_environment", state="test-state", capacity_limits=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
