"""Tests for aws_util.aio.ecs — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.ecs import (
    ECSService,
    ECSTask,
    ECSTaskDefinition,
    describe_services,
    describe_task_definition,
    describe_tasks,
    list_clusters,
    list_tasks,
    run_task,
    run_task_and_wait,
    stop_task,
    update_service,
    wait_for_service_stable,
    wait_for_task,
    create_capacity_provider,
    create_cluster,
    create_service,
    create_task_set,
    delete_account_setting,
    delete_attributes,
    delete_capacity_provider,
    delete_cluster,
    delete_service,
    delete_task_definitions,
    delete_task_set,
    deregister_container_instance,
    deregister_task_definition,
    describe_capacity_providers,
    describe_clusters,
    describe_container_instances,
    describe_service_deployments,
    describe_service_revisions,
    describe_task_sets,
    discover_poll_endpoint,
    execute_command,
    get_task_protection,
    list_account_settings,
    list_attributes,
    list_container_instances,
    list_service_deployments,
    list_services,
    list_services_by_namespace,
    list_tags_for_resource,
    list_task_definition_families,
    list_task_definitions,
    put_account_setting,
    put_account_setting_default,
    put_attributes,
    put_cluster_capacity_providers,
    register_container_instance,
    register_task_definition,
    start_task,
    stop_service_deployment,
    submit_attachment_state_changes,
    submit_container_state_change,
    submit_task_state_change,
    tag_resource,
    untag_resource,
    update_capacity_provider,
    update_cluster,
    update_cluster_settings,
    update_container_agent,
    update_container_instances_state,
    update_service_primary_task_set,
    update_task_protection,
    update_task_set,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _task_dict(
    task_arn: str = "arn:aws:ecs:us-east-1:123:task/cluster/abc",
    last_status: str = "RUNNING",
    desired_status: str = "RUNNING",
) -> dict:
    return {
        "taskArn": task_arn,
        "taskDefinitionArn": "arn:aws:ecs:us-east-1:123:task-definition/my-td:1",
        "clusterArn": "arn:aws:ecs:us-east-1:123:cluster/my-cluster",
        "lastStatus": last_status,
        "desiredStatus": desired_status,
        "launchType": "FARGATE",
        "cpu": "256",
        "memory": "512",
        "group": "service:my-svc",
    }


def _service_dict(
    service_name: str = "my-svc",
    desired_count: int = 2,
    running_count: int = 2,
    pending_count: int = 0,
) -> dict:
    return {
        "serviceArn": f"arn:aws:ecs:us-east-1:123:service/cluster/{service_name}",
        "serviceName": service_name,
        "clusterArn": "arn:aws:ecs:us-east-1:123:cluster/my-cluster",
        "status": "ACTIVE",
        "desiredCount": desired_count,
        "runningCount": running_count,
        "pendingCount": pending_count,
        "taskDefinition": "arn:aws:ecs:us-east-1:123:task-definition/my-td:1",
        "launchType": "FARGATE",
    }


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------


async def test_list_clusters_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [
        "arn:aws:ecs:us-east-1:123:cluster/c1",
        "arn:aws:ecs:us-east-1:123:cluster/c2",
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await list_clusters()
    assert len(result) == 2


async def test_list_clusters_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_clusters()


async def test_list_clusters_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_clusters failed"):
        await list_clusters()


# ---------------------------------------------------------------------------
# run_task
# ---------------------------------------------------------------------------


async def test_run_task_success_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "tasks": [_task_dict()],
        "failures": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task("my-cluster", "my-td:1")
    assert len(result) == 1
    assert result[0].task_arn == "arn:aws:ecs:us-east-1:123:task/cluster/abc"


async def test_run_task_with_network_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()], "failures": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task(
        "my-cluster",
        "my-td:1",
        subnets=["subnet-1"],
        security_groups=["sg-1"],
        assign_public_ip="ENABLED",
    )
    assert len(result) == 1
    call_kwargs = mock_client.call.call_args[1]
    assert "networkConfiguration" in call_kwargs
    assert call_kwargs["networkConfiguration"]["awsvpcConfiguration"]["subnets"] == ["subnet-1"]


async def test_run_task_with_subnets_only(monkeypatch):
    """Only subnets provided, security_groups defaults to []."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()], "failures": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task("cluster", "td:1", subnets=["subnet-1"])
    call_kwargs = mock_client.call.call_args[1]
    net_cfg = call_kwargs["networkConfiguration"]["awsvpcConfiguration"]
    assert net_cfg["securityGroups"] == []


async def test_run_task_with_security_groups_only(monkeypatch):
    """Only security_groups provided, subnets defaults to []."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()], "failures": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task("cluster", "td:1", security_groups=["sg-1"])
    call_kwargs = mock_client.call.call_args[1]
    net_cfg = call_kwargs["networkConfiguration"]["awsvpcConfiguration"]
    assert net_cfg["subnets"] == []


async def test_run_task_with_overrides(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()], "failures": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    overrides = {"containerOverrides": [{"name": "c", "command": ["echo"]}]}
    result = await run_task("cluster", "td:1", overrides=overrides)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["overrides"] == overrides


async def test_run_task_no_network_no_overrides(monkeypatch):
    """No subnets, no security_groups, no overrides — no extra keys."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()], "failures": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    await run_task("cluster", "td:1")
    call_kwargs = mock_client.call.call_args[1]
    assert "networkConfiguration" not in call_kwargs
    assert "overrides" not in call_kwargs


async def test_run_task_failures(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "tasks": [],
        "failures": [{"arn": "arn:...", "reason": "capacity"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="ECS run_task failures"):
        await run_task("cluster", "td:1")


async def test_run_task_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await run_task("cluster", "td:1")


async def test_run_task_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="run_task failed"):
        await run_task("cluster", "td:1")


# ---------------------------------------------------------------------------
# stop_task
# ---------------------------------------------------------------------------


async def test_stop_task_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    await stop_task("cluster", "arn:task", reason="done")
    mock_client.call.assert_awaited_once()


async def test_stop_task_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="denied"):
        await stop_task("cluster", "arn:task")


async def test_stop_task_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="stop_task failed"):
        await stop_task("cluster", "arn:task")


# ---------------------------------------------------------------------------
# describe_tasks
# ---------------------------------------------------------------------------


async def test_describe_tasks_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": [_task_dict()]}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_tasks("cluster", ["arn:task"])
    assert len(result) == 1
    assert isinstance(result[0], ECSTask)


async def test_describe_tasks_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_tasks("cluster", ["arn:task"])
    assert result == []


async def test_describe_tasks_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="fail"):
        await describe_tasks("cluster", ["arn:task"])


async def test_describe_tasks_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_tasks failed"):
        await describe_tasks("cluster", ["arn:task"])


# ---------------------------------------------------------------------------
# list_tasks
# ---------------------------------------------------------------------------


async def test_list_tasks_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["arn:task1", "arn:task2"]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await list_tasks("cluster")
    assert result == ["arn:task1", "arn:task2"]


async def test_list_tasks_with_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["arn:task1"]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await list_tasks("cluster", service_name="my-svc")
    assert len(result) == 1
    call_kwargs = mock_client.paginate.call_args[1]
    assert call_kwargs["serviceName"] == "my-svc"


async def test_list_tasks_no_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = []
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await list_tasks("cluster", desired_status="STOPPED")
    assert result == []
    call_kwargs = mock_client.paginate.call_args[1]
    assert "serviceName" not in call_kwargs


async def test_list_tasks_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("no")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="no"):
        await list_tasks("cluster")


async def test_list_tasks_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_tasks failed"):
        await list_tasks("cluster")


# ---------------------------------------------------------------------------
# describe_services
# ---------------------------------------------------------------------------


async def test_describe_services_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "services": [_service_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_services("cluster", ["my-svc"])
    assert len(result) == 1
    assert isinstance(result[0], ECSService)
    assert result[0].service_name == "my-svc"
    assert result[0].launch_type == "FARGATE"


async def test_describe_services_no_launch_type(monkeypatch):
    svc = _service_dict()
    del svc["launchType"]
    mock_client = AsyncMock()
    mock_client.call.return_value = {"services": [svc]}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_services("cluster", ["my-svc"])
    assert result[0].launch_type is None


async def test_describe_services_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_services("cluster", ["my-svc"])


async def test_describe_services_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_services failed"):
        await describe_services("cluster", ["my-svc"])


# ---------------------------------------------------------------------------
# update_service
# ---------------------------------------------------------------------------


async def test_update_service_all_params(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await update_service(
        "cluster",
        "my-svc",
        desired_count=3,
        task_definition="td:2",
        force_new_deployment=True,
    )
    assert isinstance(result, ECSService)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["desiredCount"] == 3
    assert call_kwargs["taskDefinition"] == "td:2"
    assert call_kwargs["forceNewDeployment"] is True


async def test_update_service_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"service": _service_dict()}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await update_service("cluster", "my-svc")
    call_kwargs = mock_client.call.call_args[1]
    assert "desiredCount" not in call_kwargs
    assert "taskDefinition" not in call_kwargs


async def test_update_service_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("deny")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="deny"):
        await update_service("cluster", "svc")


async def test_update_service_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_service failed"):
        await update_service("cluster", "svc")


# ---------------------------------------------------------------------------
# describe_task_definition
# ---------------------------------------------------------------------------


async def test_describe_task_definition_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "taskDefinition": {
            "taskDefinitionArn": "arn:...:task-definition/td:1",
            "family": "td",
            "revision": 1,
            "status": "ACTIVE",
            "cpu": "256",
            "memory": "512",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_task_definition("td:1")
    assert isinstance(result, ECSTaskDefinition)
    assert result.family == "td"
    assert result.cpu == "256"


async def test_describe_task_definition_no_cpu_memory(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "taskDefinition": {
            "taskDefinitionArn": "arn:...:task-definition/td:1",
            "family": "td",
            "revision": 1,
            "status": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await describe_task_definition("td:1")
    assert result.cpu is None
    assert result.memory is None


async def test_describe_task_definition_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_task_definition("td:1")


async def test_describe_task_definition_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_task_definition failed"):
        await describe_task_definition("td:1")


# ---------------------------------------------------------------------------
# wait_for_task
# ---------------------------------------------------------------------------


async def test_wait_for_task_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "tasks": [_task_dict(last_status="STOPPED", desired_status="STOPPED")]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_task("cluster", "arn:task")
    assert result.last_status == "STOPPED"


async def test_wait_for_task_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"tasks": [_task_dict(last_status="RUNNING")]},
        {"tasks": [_task_dict(last_status="STOPPED", desired_status="STOPPED")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ecs.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_task(
            "cluster", "arn:task", timeout=300, poll_interval=0.01
        )
    assert result.last_status == "STOPPED"


async def test_wait_for_task_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"tasks": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_task("cluster", "arn:task")


async def test_wait_for_task_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "tasks": [_task_dict(last_status="RUNNING")]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ecs.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(TimeoutError, match="did not reach status"):
            await wait_for_task(
                "cluster", "arn:task", timeout=0.0, poll_interval=0.001
            )


# ---------------------------------------------------------------------------
# run_task_and_wait
# ---------------------------------------------------------------------------


async def test_run_task_and_wait_success(monkeypatch):
    mock_client = AsyncMock()
    # First call: run_task
    # Second call: describe_tasks (for wait_for_task)
    mock_client.call.side_effect = [
        {"tasks": [_task_dict()], "failures": []},
        {"tasks": [_task_dict(last_status="STOPPED", desired_status="STOPPED")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task_and_wait(
        "cluster",
        "td:1",
        timeout=300,
        subnets=["subnet-1"],
        security_groups=["sg-1"],
        overrides={"containerOverrides": []},
    )
    assert result.last_status == "STOPPED"


async def test_run_task_and_wait_no_network(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"tasks": [_task_dict()], "failures": []},
        {"tasks": [_task_dict(last_status="STOPPED", desired_status="STOPPED")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await run_task_and_wait("cluster", "td:1")
    assert result.last_status == "STOPPED"


# ---------------------------------------------------------------------------
# wait_for_service_stable
# ---------------------------------------------------------------------------


async def test_wait_for_service_stable_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "services": [_service_dict(desired_count=2, running_count=2, pending_count=0)]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_service_stable("cluster", "my-svc")
    assert result.running_count == 2


async def test_wait_for_service_stable_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"services": [_service_dict(desired_count=2, running_count=1, pending_count=1)]},
        {"services": [_service_dict(desired_count=2, running_count=2, pending_count=0)]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ecs.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_service_stable(
            "cluster", "my-svc", timeout=300, poll_interval=0.01
        )
    assert result.running_count == 2


async def test_wait_for_service_stable_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"services": []}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_service_stable("cluster", "my-svc")


async def test_wait_for_service_stable_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "services": [_service_dict(desired_count=2, running_count=0, pending_count=2)]
    }
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.ecs.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(TimeoutError, match="did not stabilise"):
            await wait_for_service_stable(
                "cluster", "my-svc", timeout=0.0, poll_interval=0.001
            )


async def test_create_capacity_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_capacity_provider("test-name", )
    mock_client.call.assert_called_once()


async def test_create_capacity_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_provider("test-name", )


async def test_create_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cluster()
    mock_client.call.assert_called_once()


async def test_create_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster()


async def test_create_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service("test-service_name", )
    mock_client.call.assert_called_once()


async def test_create_service_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service("test-service_name", )


async def test_create_task_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_task_set("test-service", "test-cluster", "test-task_definition", )
    mock_client.call.assert_called_once()


async def test_create_task_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_task_set("test-service", "test-cluster", "test-task_definition", )


async def test_delete_account_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_setting("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_account_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_setting("test-name", )


async def test_delete_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_attributes([], )
    mock_client.call.assert_called_once()


async def test_delete_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_attributes([], )


async def test_delete_capacity_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_capacity_provider("test-capacity_provider", )
    mock_client.call.assert_called_once()


async def test_delete_capacity_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_capacity_provider("test-capacity_provider", )


async def test_delete_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cluster("test-cluster", )
    mock_client.call.assert_called_once()


async def test_delete_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster("test-cluster", )


async def test_delete_service(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service("test-service", )
    mock_client.call.assert_called_once()


async def test_delete_service_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service("test-service", )


async def test_delete_task_definitions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_task_definitions([], )
    mock_client.call.assert_called_once()


async def test_delete_task_definitions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_task_definitions([], )


async def test_delete_task_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_task_set("test-cluster", "test-service", "test-task_set", )
    mock_client.call.assert_called_once()


async def test_delete_task_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_task_set("test-cluster", "test-service", "test-task_set", )


async def test_deregister_container_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_container_instance("test-container_instance", )
    mock_client.call.assert_called_once()


async def test_deregister_container_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_container_instance("test-container_instance", )


async def test_deregister_task_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_task_definition("test-task_definition", )
    mock_client.call.assert_called_once()


async def test_deregister_task_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_task_definition("test-task_definition", )


async def test_describe_capacity_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_capacity_providers()
    mock_client.call.assert_called_once()


async def test_describe_capacity_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_capacity_providers()


async def test_describe_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_clusters()
    mock_client.call.assert_called_once()


async def test_describe_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_clusters()


async def test_describe_container_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_container_instances([], )
    mock_client.call.assert_called_once()


async def test_describe_container_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_container_instances([], )


async def test_describe_service_deployments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_deployments([], )
    mock_client.call.assert_called_once()


async def test_describe_service_deployments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_deployments([], )


async def test_describe_service_revisions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_revisions([], )
    mock_client.call.assert_called_once()


async def test_describe_service_revisions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_revisions([], )


async def test_describe_task_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_task_sets("test-cluster", "test-service", )
    mock_client.call.assert_called_once()


async def test_describe_task_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_task_sets("test-cluster", "test-service", )


async def test_discover_poll_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await discover_poll_endpoint()
    mock_client.call.assert_called_once()


async def test_discover_poll_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await discover_poll_endpoint()


async def test_execute_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_command("test-command", True, "test-task", )
    mock_client.call.assert_called_once()


async def test_execute_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_command("test-command", True, "test-task", )


async def test_get_task_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_task_protection("test-cluster", )
    mock_client.call.assert_called_once()


async def test_get_task_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_task_protection("test-cluster", )


async def test_list_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_settings()
    mock_client.call.assert_called_once()


async def test_list_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_settings()


async def test_list_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_attributes("test-target_type", )
    mock_client.call.assert_called_once()


async def test_list_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_attributes("test-target_type", )


async def test_list_container_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_container_instances()
    mock_client.call.assert_called_once()


async def test_list_container_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_container_instances()


async def test_list_service_deployments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_deployments("test-service", )
    mock_client.call.assert_called_once()


async def test_list_service_deployments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_deployments("test-service", )


async def test_list_services(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_services()
    mock_client.call.assert_called_once()


async def test_list_services_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_services()


async def test_list_services_by_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_services_by_namespace("test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_services_by_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_services_by_namespace("test-namespace", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_task_definition_families(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_task_definition_families()
    mock_client.call.assert_called_once()


async def test_list_task_definition_families_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_task_definition_families()


async def test_list_task_definitions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_task_definitions()
    mock_client.call.assert_called_once()


async def test_list_task_definitions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_task_definitions()


async def test_put_account_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_account_setting("test-name", "test-value", )
    mock_client.call.assert_called_once()


async def test_put_account_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_setting("test-name", "test-value", )


async def test_put_account_setting_default(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_account_setting_default("test-name", "test-value", )
    mock_client.call.assert_called_once()


async def test_put_account_setting_default_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_setting_default("test-name", "test-value", )


async def test_put_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_attributes([], )
    mock_client.call.assert_called_once()


async def test_put_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_attributes([], )


async def test_put_cluster_capacity_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_cluster_capacity_providers("test-cluster", [], [], )
    mock_client.call.assert_called_once()


async def test_put_cluster_capacity_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_cluster_capacity_providers("test-cluster", [], [], )


async def test_register_container_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_container_instance()
    mock_client.call.assert_called_once()


async def test_register_container_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_container_instance()


async def test_register_task_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_task_definition("test-family", [], )
    mock_client.call.assert_called_once()


async def test_register_task_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_task_definition("test-family", [], )


async def test_start_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_task([], "test-task_definition", )
    mock_client.call.assert_called_once()


async def test_start_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_task([], "test-task_definition", )


async def test_stop_service_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_service_deployment("test-service_deployment_arn", )
    mock_client.call.assert_called_once()


async def test_stop_service_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_service_deployment("test-service_deployment_arn", )


async def test_submit_attachment_state_changes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await submit_attachment_state_changes([], )
    mock_client.call.assert_called_once()


async def test_submit_attachment_state_changes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await submit_attachment_state_changes([], )


async def test_submit_container_state_change(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await submit_container_state_change()
    mock_client.call.assert_called_once()


async def test_submit_container_state_change_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await submit_container_state_change()


async def test_submit_task_state_change(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await submit_task_state_change()
    mock_client.call.assert_called_once()


async def test_submit_task_state_change_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await submit_task_state_change()


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_capacity_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_capacity_provider("test-name", )
    mock_client.call.assert_called_once()


async def test_update_capacity_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_capacity_provider("test-name", )


async def test_update_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_cluster("test-cluster", )
    mock_client.call.assert_called_once()


async def test_update_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_cluster("test-cluster", )


async def test_update_cluster_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_cluster_settings("test-cluster", [], )
    mock_client.call.assert_called_once()


async def test_update_cluster_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_cluster_settings("test-cluster", [], )


async def test_update_container_agent(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_container_agent("test-container_instance", )
    mock_client.call.assert_called_once()


async def test_update_container_agent_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_container_agent("test-container_instance", )


async def test_update_container_instances_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_container_instances_state([], "test-status", )
    mock_client.call.assert_called_once()


async def test_update_container_instances_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_container_instances_state([], "test-status", )


async def test_update_service_primary_task_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_service_primary_task_set("test-cluster", "test-service", "test-primary_task_set", )
    mock_client.call.assert_called_once()


async def test_update_service_primary_task_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_service_primary_task_set("test-cluster", "test-service", "test-primary_task_set", )


async def test_update_task_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_task_protection("test-cluster", [], True, )
    mock_client.call.assert_called_once()


async def test_update_task_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_task_protection("test-cluster", [], True, )


async def test_update_task_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_task_set("test-cluster", "test-service", "test-task_set", {}, )
    mock_client.call.assert_called_once()


async def test_update_task_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ecs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_task_set("test-cluster", "test-service", "test-task_set", {}, )


@pytest.mark.asyncio
async def test_create_capacity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import create_capacity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await create_capacity_provider("test-name", cluster="test-cluster", auto_scaling_group_provider=True, managed_instances_provider="test-managed_instances_provider", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import create_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await create_cluster(cluster_name="test-cluster_name", tags=[{"Key": "k", "Value": "v"}], settings={}, configuration={}, capacity_providers="test-capacity_providers", default_capacity_provider_strategy="test-default_capacity_provider_strategy", service_connect_defaults="test-service_connect_defaults", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import create_service
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await create_service("test-service_name", cluster="test-cluster", task_definition={}, availability_zone_rebalancing="test-availability_zone_rebalancing", load_balancers="test-load_balancers", service_registries="test-service_registries", desired_count=1, client_token="test-client_token", launch_type="test-launch_type", capacity_provider_strategy="test-capacity_provider_strategy", platform_version="test-platform_version", role="test-role", deployment_configuration={}, placement_constraints="test-placement_constraints", placement_strategy="test-placement_strategy", network_configuration={}, health_check_grace_period_seconds="test-health_check_grace_period_seconds", scheduling_strategy="test-scheduling_strategy", deployment_controller="test-deployment_controller", tags=[{"Key": "k", "Value": "v"}], enable_ecs_managed_tags=True, propagate_tags=[{"Key": "k", "Value": "v"}], enable_execute_command=True, service_connect_configuration={}, volume_configurations={}, vpc_lattice_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_task_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import create_task_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await create_task_set("test-service", "test-cluster", {}, external_id="test-external_id", network_configuration={}, load_balancers="test-load_balancers", service_registries="test-service_registries", launch_type="test-launch_type", capacity_provider_strategy="test-capacity_provider_strategy", platform_version="test-platform_version", scale="test-scale", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_account_setting_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import delete_account_setting
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await delete_account_setting("test-name", principal_arn="test-principal_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import delete_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await delete_attributes("test-attributes", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_capacity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import delete_capacity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await delete_capacity_provider("test-capacity_provider", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_service_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import delete_service
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await delete_service("test-service", cluster="test-cluster", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_task_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import delete_task_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await delete_task_set("test-cluster", "test-service", "test-task_set", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_container_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import deregister_container_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await deregister_container_instance("test-container_instance", cluster="test-cluster", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_capacity_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import describe_capacity_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await describe_capacity_providers(capacity_providers="test-capacity_providers", cluster="test-cluster", include=True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import describe_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await describe_clusters(clusters="test-clusters", include=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_container_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import describe_container_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await describe_container_instances("test-container_instances", cluster="test-cluster", include=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_task_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import describe_task_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await describe_task_sets("test-cluster", "test-service", task_sets="test-task_sets", include=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_discover_poll_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import discover_poll_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await discover_poll_endpoint(container_instance="test-container_instance", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_command_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import execute_command
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await execute_command("test-command", "test-interactive", "test-task", cluster="test-cluster", container="test-container", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_protection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import get_task_protection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await get_task_protection("test-cluster", tasks="test-tasks", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_account_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_account_settings(name="test-name", value="test-value", principal_arn="test-principal_arn", effective_settings={}, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_attributes("test-target_type", cluster="test-cluster", attribute_name="test-attribute_name", attribute_value="test-attribute_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_container_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_container_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_container_instances(cluster="test-cluster", filter="test-filter", next_token="test-next_token", max_results=1, status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_deployments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_service_deployments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_service_deployments("test-service", cluster="test-cluster", status="test-status", created_at="test-created_at", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_services_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_services
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_services(cluster="test-cluster", next_token="test-next_token", max_results=1, launch_type="test-launch_type", scheduling_strategy="test-scheduling_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_services_by_namespace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_services_by_namespace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_services_by_namespace("test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_task_definition_families_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_task_definition_families
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_task_definition_families(family_prefix="test-family_prefix", status="test-status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_task_definitions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import list_task_definitions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await list_task_definitions(family_prefix="test-family_prefix", status="test-status", sort="test-sort", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_account_setting_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import put_account_setting
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await put_account_setting("test-name", "test-value", principal_arn="test-principal_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import put_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await put_attributes("test-attributes", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_container_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import register_container_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await register_container_instance(cluster="test-cluster", instance_identity_document="test-instance_identity_document", instance_identity_document_signature="test-instance_identity_document_signature", total_resources="test-total_resources", version_info="test-version_info", container_instance_arn="test-container_instance_arn", attributes="test-attributes", platform_devices="test-platform_devices", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_task_definition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import register_task_definition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await register_task_definition("test-family", {}, task_role_arn="test-task_role_arn", execution_role_arn="test-execution_role_arn", network_mode="test-network_mode", volumes="test-volumes", placement_constraints="test-placement_constraints", requires_compatibilities=True, cpu="test-cpu", memory="test-memory", tags=[{"Key": "k", "Value": "v"}], pid_mode="test-pid_mode", ipc_mode="test-ipc_mode", proxy_configuration={}, inference_accelerators="test-inference_accelerators", ephemeral_storage="test-ephemeral_storage", runtime_platform="test-runtime_platform", enable_fault_injection=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import start_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await start_task("test-container_instances", {}, cluster="test-cluster", enable_ecs_managed_tags=True, enable_execute_command=True, group="test-group", network_configuration={}, overrides="test-overrides", propagate_tags=[{"Key": "k", "Value": "v"}], reference_id="test-reference_id", started_by="test-started_by", tags=[{"Key": "k", "Value": "v"}], volume_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_service_deployment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import stop_service_deployment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await stop_service_deployment("test-service_deployment_arn", stop_type="test-stop_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_submit_attachment_state_changes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import submit_attachment_state_changes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await submit_attachment_state_changes("test-attachments", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_submit_container_state_change_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import submit_container_state_change
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await submit_container_state_change(cluster="test-cluster", task="test-task", container_name="test-container_name", runtime_id="test-runtime_id", status="test-status", exit_code="test-exit_code", reason="test-reason", network_bindings="test-network_bindings", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_submit_task_state_change_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import submit_task_state_change
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await submit_task_state_change(cluster="test-cluster", task="test-task", status="test-status", reason="test-reason", containers="test-containers", attachments="test-attachments", managed_agents="test-managed_agents", pull_started_at="test-pull_started_at", pull_stopped_at="test-pull_stopped_at", execution_stopped_at="test-execution_stopped_at", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_capacity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import update_capacity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await update_capacity_provider("test-name", cluster="test-cluster", auto_scaling_group_provider=True, managed_instances_provider="test-managed_instances_provider", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import update_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await update_cluster("test-cluster", settings={}, configuration={}, service_connect_defaults="test-service_connect_defaults", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_container_agent_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import update_container_agent
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await update_container_agent("test-container_instance", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_container_instances_state_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import update_container_instances_state
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await update_container_instances_state("test-container_instances", "test-status", cluster="test-cluster", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_task_protection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ecs import update_task_protection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ecs.async_client", lambda *a, **kw: mock_client)
    await update_task_protection("test-cluster", "test-tasks", "test-protection_enabled", expires_in_minutes="test-expires_in_minutes", region_name="us-east-1")
    mock_client.call.assert_called_once()
