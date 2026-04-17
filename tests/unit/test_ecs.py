"""Tests for aws_util.ecs module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

import aws_util.ecs as ecs_mod
from aws_util.ecs import (
    ECSTask,
    ECSService,
    ECSTaskDefinition,
    list_clusters,
    run_task,
    stop_task,
    describe_tasks,
    list_tasks,
    describe_services,
    update_service,
    describe_task_definition,
    wait_for_task,
    run_task_and_wait,
    wait_for_service_stable,
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

REGION = "us-east-1"
CLUSTER = "test-cluster"
TASK_DEF = "test-task-def:1"
TASK_ARN = "arn:aws:ecs:us-east-1:123456789012:task/test-cluster/abc123"
SERVICE_NAME = "test-service"


def _make_task_dict(**kwargs) -> dict:
    defaults = {
        "taskArn": TASK_ARN,
        "taskDefinitionArn": f"arn:aws:ecs:us-east-1:123456789012:task-definition/{TASK_DEF}",
        "clusterArn": f"arn:aws:ecs:us-east-1:123456789012:cluster/{CLUSTER}",
        "lastStatus": "RUNNING",
        "desiredStatus": "RUNNING",
        "launchType": "FARGATE",
    }
    defaults.update(kwargs)
    return defaults


def _make_task(**kwargs) -> ECSTask:
    """Build an ECSTask using snake_case field names (for direct construction)."""
    defaults = {
        "task_arn": TASK_ARN,
        "task_definition_arn": f"arn:aws:ecs:us-east-1:123456789012:task-definition/{TASK_DEF}",
        "cluster_arn": f"arn:aws:ecs:us-east-1:123456789012:cluster/{CLUSTER}",
        "last_status": "RUNNING",
        "desired_status": "RUNNING",
        "launch_type": "FARGATE",
    }
    defaults.update(kwargs)
    return ECSTask(**defaults)


def _make_service_dict(**kwargs) -> dict:
    defaults = {
        "serviceArn": f"arn:aws:ecs:us-east-1:123456789012:service/{SERVICE_NAME}",
        "serviceName": SERVICE_NAME,
        "clusterArn": f"arn:aws:ecs:us-east-1:123456789012:cluster/{CLUSTER}",
        "status": "ACTIVE",
        "desiredCount": 1,
        "runningCount": 1,
        "pendingCount": 0,
        "taskDefinition": TASK_DEF,
        "launchType": "FARGATE",
    }
    defaults.update(kwargs)
    return defaults


def _make_service(**kwargs) -> ECSService:
    """Build an ECSService using snake_case field names (for direct construction)."""
    defaults = {
        "service_arn": f"arn:aws:ecs:us-east-1:123456789012:service/{SERVICE_NAME}",
        "service_name": SERVICE_NAME,
        "cluster_arn": f"arn:aws:ecs:us-east-1:123456789012:cluster/{CLUSTER}",
        "status": "ACTIVE",
        "desired_count": 1,
        "running_count": 1,
        "pending_count": 0,
        "task_definition": TASK_DEF,
        "launch_type": "FARGATE",
    }
    defaults.update(kwargs)
    return ECSService(**defaults)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_ecs_task_model():
    task = ECSTask(
        task_arn=TASK_ARN,
        task_definition_arn="arn:...",
        cluster_arn="arn:...",
        last_status="RUNNING",
        desired_status="RUNNING",
    )
    assert task.last_status == "RUNNING"
    assert task.launch_type is None


def test_ecs_service_model():
    svc = ECSService(
        service_arn="arn:...",
        service_name="svc",
        cluster_arn="arn:...",
        status="ACTIVE",
        desired_count=2,
        running_count=2,
        pending_count=0,
        task_definition=TASK_DEF,
    )
    assert svc.desired_count == 2


def test_ecs_task_definition_model():
    td = ECSTaskDefinition(
        task_definition_arn="arn:...",
        family="my-family",
        revision=1,
        status="ACTIVE",
    )
    assert td.revision == 1


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------

def test_list_clusters_returns_arns(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"clusterArns": ["arn:aws:ecs:us-east-1:123:cluster/c1"]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = list_clusters(region_name=REGION)
    assert "arn:aws:ecs:us-east-1:123:cluster/c1" in result


def test_list_clusters_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListClusters"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_clusters failed"):
        list_clusters(region_name=REGION)


# ---------------------------------------------------------------------------
# run_task
# ---------------------------------------------------------------------------

def test_run_task_returns_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_task.return_value = {
        "tasks": [_make_task_dict()],
        "failures": [],
    }
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = run_task(CLUSTER, TASK_DEF, region_name=REGION)
    assert len(tasks) == 1
    assert isinstance(tasks[0], ECSTask)


def test_run_task_with_network_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_task.return_value = {
        "tasks": [_make_task_dict()],
        "failures": [],
    }
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = run_task(
        CLUSTER, TASK_DEF,
        subnets=["subnet-1"],
        security_groups=["sg-1"],
        assign_public_ip="ENABLED",
        region_name=REGION,
    )
    assert len(tasks) == 1


def test_run_task_with_overrides(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_task.return_value = {"tasks": [_make_task_dict()], "failures": []}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    tasks = run_task(
        CLUSTER, TASK_DEF,
        overrides={"containerOverrides": []},
        region_name=REGION,
    )
    assert len(tasks) == 1


def test_run_task_failures_raises(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_task.return_value = {
        "tasks": [],
        "failures": [{"arn": TASK_ARN, "reason": "RESOURCE:CPU"}],
    }
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="ECS run_task failures"):
        run_task(CLUSTER, TASK_DEF, region_name=REGION)


def test_run_task_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.run_task.side_effect = ClientError(
        {"Error": {"Code": "ClusterNotFoundException", "Message": "not found"}}, "RunTask"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="run_task failed"):
        run_task(CLUSTER, TASK_DEF, region_name=REGION)


# ---------------------------------------------------------------------------
# stop_task
# ---------------------------------------------------------------------------

def test_stop_task_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_task.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    stop_task(CLUSTER, TASK_ARN, reason="Test", region_name=REGION)
    mock_client.stop_task.assert_called_once()


def test_stop_task_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_task.side_effect = ClientError(
        {"Error": {"Code": "TaskNotFoundException", "Message": "not found"}}, "StopTask"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="stop_task failed"):
        stop_task(CLUSTER, TASK_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_tasks
# ---------------------------------------------------------------------------

def test_describe_tasks_returns_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tasks.return_value = {"tasks": [_make_task_dict()]}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_tasks(CLUSTER, [TASK_ARN], region_name=REGION)
    assert len(result) == 1
    assert result[0].task_arn == TASK_ARN


def test_describe_tasks_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tasks.side_effect = ClientError(
        {"Error": {"Code": "ClusterNotFoundException", "Message": "not found"}}, "DescribeTasks"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_tasks failed"):
        describe_tasks(CLUSTER, [TASK_ARN], region_name=REGION)


# ---------------------------------------------------------------------------
# list_tasks
# ---------------------------------------------------------------------------

def test_list_tasks_returns_arns(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"taskArns": [TASK_ARN]}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = list_tasks(CLUSTER, region_name=REGION)
    assert TASK_ARN in result


def test_list_tasks_with_service_filter(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"taskArns": [TASK_ARN]}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = list_tasks(CLUSTER, service_name=SERVICE_NAME, region_name=REGION)
    assert len(result) == 1


def test_list_tasks_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "ClusterNotFoundException", "Message": "not found"}}, "ListTasks"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_tasks failed"):
        list_tasks(CLUSTER, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_services
# ---------------------------------------------------------------------------

def test_describe_services_returns_services(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_services.return_value = {"services": [_make_service_dict()]}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = describe_services(CLUSTER, [SERVICE_NAME], region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], ECSService)
    assert result[0].service_name == SERVICE_NAME


def test_describe_services_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_services.side_effect = ClientError(
        {"Error": {"Code": "ClusterNotFoundException", "Message": "not found"}}, "DescribeServices"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_services failed"):
        describe_services(CLUSTER, [SERVICE_NAME], region_name=REGION)


# ---------------------------------------------------------------------------
# update_service
# ---------------------------------------------------------------------------

def test_update_service_returns_service(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.return_value = {"service": _make_service_dict(desiredCount=2)}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = update_service(CLUSTER, SERVICE_NAME, desired_count=2, region_name=REGION)
    assert isinstance(result, ECSService)
    assert result.desired_count == 2


def test_update_service_with_task_def(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.return_value = {"service": _make_service_dict()}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_service(CLUSTER, SERVICE_NAME, task_definition="new-task:2", region_name=REGION)


def test_update_service_force_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.return_value = {"service": _make_service_dict()}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_service(CLUSTER, SERVICE_NAME, force_new_deployment=True, region_name=REGION)


def test_update_service_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceNotFoundException", "Message": "not found"}}, "UpdateService"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="update_service failed"):
        update_service(CLUSTER, SERVICE_NAME, desired_count=1, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_task_definition
# ---------------------------------------------------------------------------

def test_describe_task_definition_returns_td(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_task_definition.return_value = {
        "taskDefinition": {
            "taskDefinitionArn": f"arn:aws:ecs:us-east-1:123:task-definition/{TASK_DEF}",
            "family": "test-task-def",
            "revision": 1,
            "status": "ACTIVE",
            "cpu": "256",
            "memory": "512",
        }
    }
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)

    result = describe_task_definition(TASK_DEF, region_name=REGION)
    assert isinstance(result, ECSTaskDefinition)
    assert result.family == "test-task-def"


def test_describe_task_definition_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_task_definition.side_effect = ClientError(
        {"Error": {"Code": "ClientException", "Message": "not found"}}, "DescribeTaskDefinition"
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_task_definition failed"):
        describe_task_definition("nonexistent:99", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_task
# ---------------------------------------------------------------------------

def test_wait_for_task_already_stopped(monkeypatch):
    stopped_task = _make_task(last_status="STOPPED", desired_status="STOPPED")
    monkeypatch.setattr(ecs_mod, "describe_tasks", lambda *a, **kw: [stopped_task])
    result = wait_for_task(CLUSTER, TASK_ARN, target_status="STOPPED", timeout=5.0,
                           poll_interval=0.01, region_name=REGION)
    assert result.last_status == "STOPPED"


def test_wait_for_task_not_found(monkeypatch):
    monkeypatch.setattr(ecs_mod, "describe_tasks", lambda *a, **kw: [])
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_task(CLUSTER, "nonexistent-task", timeout=1.0, region_name=REGION)


def test_wait_for_task_timeout(monkeypatch):
    running_task = _make_task()
    monkeypatch.setattr(ecs_mod, "describe_tasks", lambda *a, **kw: [running_task])
    with pytest.raises(TimeoutError):
        wait_for_task(CLUSTER, TASK_ARN, target_status="STOPPED",
                      timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_service_stable
# ---------------------------------------------------------------------------

def test_wait_for_service_stable_already_stable(monkeypatch):
    stable_svc = _make_service()
    monkeypatch.setattr(ecs_mod, "describe_services", lambda *a, **kw: [stable_svc])
    result = wait_for_service_stable(CLUSTER, SERVICE_NAME, timeout=5.0,
                                      poll_interval=0.01, region_name=REGION)
    assert result.running_count == result.desired_count


def test_wait_for_service_stable_not_found(monkeypatch):
    monkeypatch.setattr(ecs_mod, "describe_services", lambda *a, **kw: [])
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_service_stable(CLUSTER, "nonexistent-svc", timeout=1.0, region_name=REGION)


def test_wait_for_service_stable_timeout(monkeypatch):
    unstable_svc = _make_service(running_count=0, pending_count=1)
    monkeypatch.setattr(ecs_mod, "describe_services", lambda *a, **kw: [unstable_svc])
    with pytest.raises(TimeoutError):
        wait_for_service_stable(CLUSTER, SERVICE_NAME, timeout=0.0,
                                poll_interval=0.0, region_name=REGION)


def test_wait_for_task_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_task (line 426)."""
    import time as _t
    monkeypatch.setattr(_t, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_describe_tasks(cluster, task_arns, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return [_make_task(last_status="RUNNING")]
        return [_make_task(last_status="STOPPED", desired_status="STOPPED")]

    monkeypatch.setattr(ecs_mod, "describe_tasks", fake_describe_tasks)
    result = wait_for_task(
        CLUSTER, TASK_ARN, target_status="STOPPED", timeout=10.0,
        poll_interval=0.001, region_name=REGION
    )
    assert result.last_status == "STOPPED"


def test_wait_for_service_stable_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_service_stable (line 515)."""
    import time as _t
    monkeypatch.setattr(_t, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_describe_services(cluster, services, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return [_make_service(running_count=0, pending_count=1)]
        return [_make_service()]

    monkeypatch.setattr(ecs_mod, "describe_services", fake_describe_services)
    result = wait_for_service_stable(
        CLUSTER, SERVICE_NAME, timeout=10.0, poll_interval=0.001, region_name=REGION
    )
    assert result.running_count == result.desired_count


def test_run_task_and_wait(monkeypatch):
    """Covers run_task_and_wait (lines 460-470)."""
    stopped_task = _make_task(last_status="STOPPED", desired_status="STOPPED")
    monkeypatch.setattr(ecs_mod, "run_task", lambda *a, **kw: [stopped_task])
    monkeypatch.setattr(ecs_mod, "wait_for_task", lambda *a, **kw: stopped_task)
    result = run_task_and_wait(CLUSTER, TASK_DEF, timeout=5.0, region_name=REGION)
    assert result.last_status == "STOPPED"


def test_create_capacity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_provider.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    create_capacity_provider("test-name", region_name=REGION)
    mock_client.create_capacity_provider.assert_called_once()


def test_create_capacity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_provider",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity provider"):
        create_capacity_provider("test-name", region_name=REGION)


def test_create_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    create_cluster(region_name=REGION)
    mock_client.create_cluster.assert_called_once()


def test_create_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cluster",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cluster"):
        create_cluster(region_name=REGION)


def test_create_service(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    create_service("test-service_name", region_name=REGION)
    mock_client.create_service.assert_called_once()


def test_create_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service"):
        create_service("test-service_name", region_name=REGION)


def test_create_task_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_task_set.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    create_task_set("test-service", "test-cluster", "test-task_definition", region_name=REGION)
    mock_client.create_task_set.assert_called_once()


def test_create_task_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_task_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_task_set",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create task set"):
        create_task_set("test-service", "test-cluster", "test-task_definition", region_name=REGION)


def test_delete_account_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_setting.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_account_setting("test-name", region_name=REGION)
    mock_client.delete_account_setting.assert_called_once()


def test_delete_account_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_setting",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account setting"):
        delete_account_setting("test-name", region_name=REGION)


def test_delete_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_attributes.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_attributes([], region_name=REGION)
    mock_client.delete_attributes.assert_called_once()


def test_delete_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_attributes",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete attributes"):
        delete_attributes([], region_name=REGION)


def test_delete_capacity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_provider.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_capacity_provider("test-capacity_provider", region_name=REGION)
    mock_client.delete_capacity_provider.assert_called_once()


def test_delete_capacity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_capacity_provider",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete capacity provider"):
        delete_capacity_provider("test-capacity_provider", region_name=REGION)


def test_delete_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_cluster("test-cluster", region_name=REGION)
    mock_client.delete_cluster.assert_called_once()


def test_delete_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cluster",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cluster"):
        delete_cluster("test-cluster", region_name=REGION)


def test_delete_service(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_service("test-service", region_name=REGION)
    mock_client.delete_service.assert_called_once()


def test_delete_service_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service"):
        delete_service("test-service", region_name=REGION)


def test_delete_task_definitions(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_definitions.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_task_definitions([], region_name=REGION)
    mock_client.delete_task_definitions.assert_called_once()


def test_delete_task_definitions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_definitions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_task_definitions",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete task definitions"):
        delete_task_definitions([], region_name=REGION)


def test_delete_task_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_set.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_task_set("test-cluster", "test-service", "test-task_set", region_name=REGION)
    mock_client.delete_task_set.assert_called_once()


def test_delete_task_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_task_set",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete task set"):
        delete_task_set("test-cluster", "test-service", "test-task_set", region_name=REGION)


def test_deregister_container_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_container_instance.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    deregister_container_instance("test-container_instance", region_name=REGION)
    mock_client.deregister_container_instance.assert_called_once()


def test_deregister_container_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_container_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_container_instance",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister container instance"):
        deregister_container_instance("test-container_instance", region_name=REGION)


def test_deregister_task_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_task_definition.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    deregister_task_definition("test-task_definition", region_name=REGION)
    mock_client.deregister_task_definition.assert_called_once()


def test_deregister_task_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_task_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_task_definition",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister task definition"):
        deregister_task_definition("test-task_definition", region_name=REGION)


def test_describe_capacity_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_providers.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_capacity_providers(region_name=REGION)
    mock_client.describe_capacity_providers.assert_called_once()


def test_describe_capacity_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_capacity_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_capacity_providers",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe capacity providers"):
        describe_capacity_providers(region_name=REGION)


def test_describe_clusters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_clusters.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_clusters(region_name=REGION)
    mock_client.describe_clusters.assert_called_once()


def test_describe_clusters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_clusters",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe clusters"):
        describe_clusters(region_name=REGION)


def test_describe_container_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_container_instances.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_container_instances([], region_name=REGION)
    mock_client.describe_container_instances.assert_called_once()


def test_describe_container_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_container_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_container_instances",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe container instances"):
        describe_container_instances([], region_name=REGION)


def test_describe_service_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_deployments.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_service_deployments([], region_name=REGION)
    mock_client.describe_service_deployments.assert_called_once()


def test_describe_service_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_deployments",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service deployments"):
        describe_service_deployments([], region_name=REGION)


def test_describe_service_revisions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_revisions.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_service_revisions([], region_name=REGION)
    mock_client.describe_service_revisions.assert_called_once()


def test_describe_service_revisions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_revisions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_revisions",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service revisions"):
        describe_service_revisions([], region_name=REGION)


def test_describe_task_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_task_sets.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_task_sets("test-cluster", "test-service", region_name=REGION)
    mock_client.describe_task_sets.assert_called_once()


def test_describe_task_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_task_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_task_sets",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe task sets"):
        describe_task_sets("test-cluster", "test-service", region_name=REGION)


def test_discover_poll_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.discover_poll_endpoint.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    discover_poll_endpoint(region_name=REGION)
    mock_client.discover_poll_endpoint.assert_called_once()


def test_discover_poll_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.discover_poll_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "discover_poll_endpoint",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to discover poll endpoint"):
        discover_poll_endpoint(region_name=REGION)


def test_execute_command(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_command.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    execute_command("test-command", True, "test-task", region_name=REGION)
    mock_client.execute_command.assert_called_once()


def test_execute_command_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_command",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute command"):
        execute_command("test-command", True, "test-task", region_name=REGION)


def test_get_task_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_task_protection.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    get_task_protection("test-cluster", region_name=REGION)
    mock_client.get_task_protection.assert_called_once()


def test_get_task_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_task_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_task_protection",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get task protection"):
        get_task_protection("test-cluster", region_name=REGION)


def test_list_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_settings.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_account_settings(region_name=REGION)
    mock_client.list_account_settings.assert_called_once()


def test_list_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_settings",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list account settings"):
        list_account_settings(region_name=REGION)


def test_list_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attributes.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_attributes("test-target_type", region_name=REGION)
    mock_client.list_attributes.assert_called_once()


def test_list_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_attributes",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list attributes"):
        list_attributes("test-target_type", region_name=REGION)


def test_list_container_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_container_instances.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_container_instances(region_name=REGION)
    mock_client.list_container_instances.assert_called_once()


def test_list_container_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_container_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_container_instances",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list container instances"):
        list_container_instances(region_name=REGION)


def test_list_service_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_deployments.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_service_deployments("test-service", region_name=REGION)
    mock_client.list_service_deployments.assert_called_once()


def test_list_service_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_deployments",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service deployments"):
        list_service_deployments("test-service", region_name=REGION)


def test_list_services(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_services(region_name=REGION)
    mock_client.list_services.assert_called_once()


def test_list_services_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_services",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list services"):
        list_services(region_name=REGION)


def test_list_services_by_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services_by_namespace.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_services_by_namespace("test-namespace", region_name=REGION)
    mock_client.list_services_by_namespace.assert_called_once()


def test_list_services_by_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_services_by_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_services_by_namespace",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list services by namespace"):
        list_services_by_namespace("test-namespace", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_task_definition_families(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_definition_families.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_task_definition_families(region_name=REGION)
    mock_client.list_task_definition_families.assert_called_once()


def test_list_task_definition_families_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_definition_families.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_task_definition_families",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list task definition families"):
        list_task_definition_families(region_name=REGION)


def test_list_task_definitions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_definitions.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    list_task_definitions(region_name=REGION)
    mock_client.list_task_definitions.assert_called_once()


def test_list_task_definitions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_definitions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_task_definitions",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list task definitions"):
        list_task_definitions(region_name=REGION)


def test_put_account_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    put_account_setting("test-name", "test-value", region_name=REGION)
    mock_client.put_account_setting.assert_called_once()


def test_put_account_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_setting",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account setting"):
        put_account_setting("test-name", "test-value", region_name=REGION)


def test_put_account_setting_default(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting_default.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    put_account_setting_default("test-name", "test-value", region_name=REGION)
    mock_client.put_account_setting_default.assert_called_once()


def test_put_account_setting_default_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_setting_default.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_setting_default",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account setting default"):
        put_account_setting_default("test-name", "test-value", region_name=REGION)


def test_put_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_attributes.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    put_attributes([], region_name=REGION)
    mock_client.put_attributes.assert_called_once()


def test_put_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_attributes",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put attributes"):
        put_attributes([], region_name=REGION)


def test_put_cluster_capacity_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_cluster_capacity_providers.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    put_cluster_capacity_providers("test-cluster", [], [], region_name=REGION)
    mock_client.put_cluster_capacity_providers.assert_called_once()


def test_put_cluster_capacity_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_cluster_capacity_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_cluster_capacity_providers",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put cluster capacity providers"):
        put_cluster_capacity_providers("test-cluster", [], [], region_name=REGION)


def test_register_container_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_container_instance.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    register_container_instance(region_name=REGION)
    mock_client.register_container_instance.assert_called_once()


def test_register_container_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_container_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_container_instance",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register container instance"):
        register_container_instance(region_name=REGION)


def test_register_task_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_task_definition.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    register_task_definition("test-family", [], region_name=REGION)
    mock_client.register_task_definition.assert_called_once()


def test_register_task_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_task_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_task_definition",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register task definition"):
        register_task_definition("test-family", [], region_name=REGION)


def test_start_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_task.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    start_task([], "test-task_definition", region_name=REGION)
    mock_client.start_task.assert_called_once()


def test_start_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_task",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start task"):
        start_task([], "test-task_definition", region_name=REGION)


def test_stop_service_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_service_deployment.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    stop_service_deployment("test-service_deployment_arn", region_name=REGION)
    mock_client.stop_service_deployment.assert_called_once()


def test_stop_service_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_service_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_service_deployment",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop service deployment"):
        stop_service_deployment("test-service_deployment_arn", region_name=REGION)


def test_submit_attachment_state_changes(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_attachment_state_changes.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    submit_attachment_state_changes([], region_name=REGION)
    mock_client.submit_attachment_state_changes.assert_called_once()


def test_submit_attachment_state_changes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_attachment_state_changes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "submit_attachment_state_changes",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to submit attachment state changes"):
        submit_attachment_state_changes([], region_name=REGION)


def test_submit_container_state_change(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_container_state_change.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    submit_container_state_change(region_name=REGION)
    mock_client.submit_container_state_change.assert_called_once()


def test_submit_container_state_change_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_container_state_change.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "submit_container_state_change",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to submit container state change"):
        submit_container_state_change(region_name=REGION)


def test_submit_task_state_change(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_task_state_change.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    submit_task_state_change(region_name=REGION)
    mock_client.submit_task_state_change.assert_called_once()


def test_submit_task_state_change_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_task_state_change.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "submit_task_state_change",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to submit task state change"):
        submit_task_state_change(region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_capacity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_provider.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_capacity_provider("test-name", region_name=REGION)
    mock_client.update_capacity_provider.assert_called_once()


def test_update_capacity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_capacity_provider",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update capacity provider"):
        update_capacity_provider("test-name", region_name=REGION)


def test_update_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_cluster("test-cluster", region_name=REGION)
    mock_client.update_cluster.assert_called_once()


def test_update_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cluster",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update cluster"):
        update_cluster("test-cluster", region_name=REGION)


def test_update_cluster_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster_settings.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_cluster_settings("test-cluster", [], region_name=REGION)
    mock_client.update_cluster_settings.assert_called_once()


def test_update_cluster_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cluster_settings",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update cluster settings"):
        update_cluster_settings("test-cluster", [], region_name=REGION)


def test_update_container_agent(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_container_agent.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_container_agent("test-container_instance", region_name=REGION)
    mock_client.update_container_agent.assert_called_once()


def test_update_container_agent_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_container_agent.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_container_agent",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update container agent"):
        update_container_agent("test-container_instance", region_name=REGION)


def test_update_container_instances_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_container_instances_state.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_container_instances_state([], "test-status", region_name=REGION)
    mock_client.update_container_instances_state.assert_called_once()


def test_update_container_instances_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_container_instances_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_container_instances_state",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update container instances state"):
        update_container_instances_state([], "test-status", region_name=REGION)


def test_update_service_primary_task_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_primary_task_set.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_service_primary_task_set("test-cluster", "test-service", "test-primary_task_set", region_name=REGION)
    mock_client.update_service_primary_task_set.assert_called_once()


def test_update_service_primary_task_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_primary_task_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_service_primary_task_set",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update service primary task set"):
        update_service_primary_task_set("test-cluster", "test-service", "test-primary_task_set", region_name=REGION)


def test_update_task_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_protection.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_task_protection("test-cluster", [], True, region_name=REGION)
    mock_client.update_task_protection.assert_called_once()


def test_update_task_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_task_protection",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update task protection"):
        update_task_protection("test-cluster", [], True, region_name=REGION)


def test_update_task_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_set.return_value = {}
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    update_task_set("test-cluster", "test-service", "test-task_set", {}, region_name=REGION)
    mock_client.update_task_set.assert_called_once()


def test_update_task_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_task_set",
    )
    monkeypatch.setattr(ecs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update task set"):
        update_task_set("test-cluster", "test-service", "test-task_set", {}, region_name=REGION)


def test_create_capacity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import create_capacity_provider
    mock_client = MagicMock()
    mock_client.create_capacity_provider.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    create_capacity_provider("test-name", cluster="test-cluster", auto_scaling_group_provider=True, managed_instances_provider="test-managed_instances_provider", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_capacity_provider.assert_called_once()

def test_create_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import create_cluster
    mock_client = MagicMock()
    mock_client.create_cluster.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    create_cluster(cluster_name="test-cluster_name", tags=[{"Key": "k", "Value": "v"}], settings={}, configuration={}, capacity_providers="test-capacity_providers", default_capacity_provider_strategy="test-default_capacity_provider_strategy", service_connect_defaults="test-service_connect_defaults", region_name="us-east-1")
    mock_client.create_cluster.assert_called_once()

def test_create_service_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import create_service
    mock_client = MagicMock()
    mock_client.create_service.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    create_service("test-service_name", cluster="test-cluster", task_definition={}, availability_zone_rebalancing="test-availability_zone_rebalancing", load_balancers="test-load_balancers", service_registries="test-service_registries", desired_count=1, client_token="test-client_token", launch_type="test-launch_type", capacity_provider_strategy="test-capacity_provider_strategy", platform_version="test-platform_version", role="test-role", deployment_configuration={}, placement_constraints="test-placement_constraints", placement_strategy="test-placement_strategy", network_configuration={}, health_check_grace_period_seconds="test-health_check_grace_period_seconds", scheduling_strategy="test-scheduling_strategy", deployment_controller="test-deployment_controller", tags=[{"Key": "k", "Value": "v"}], enable_ecs_managed_tags=True, propagate_tags=[{"Key": "k", "Value": "v"}], enable_execute_command=True, service_connect_configuration={}, volume_configurations={}, vpc_lattice_configurations={}, region_name="us-east-1")
    mock_client.create_service.assert_called_once()

def test_create_task_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import create_task_set
    mock_client = MagicMock()
    mock_client.create_task_set.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    create_task_set("test-service", "test-cluster", {}, external_id="test-external_id", network_configuration={}, load_balancers="test-load_balancers", service_registries="test-service_registries", launch_type="test-launch_type", capacity_provider_strategy="test-capacity_provider_strategy", platform_version="test-platform_version", scale="test-scale", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_task_set.assert_called_once()

def test_delete_account_setting_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import delete_account_setting
    mock_client = MagicMock()
    mock_client.delete_account_setting.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    delete_account_setting("test-name", principal_arn="test-principal_arn", region_name="us-east-1")
    mock_client.delete_account_setting.assert_called_once()

def test_delete_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import delete_attributes
    mock_client = MagicMock()
    mock_client.delete_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    delete_attributes("test-attributes", cluster="test-cluster", region_name="us-east-1")
    mock_client.delete_attributes.assert_called_once()

def test_delete_capacity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import delete_capacity_provider
    mock_client = MagicMock()
    mock_client.delete_capacity_provider.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    delete_capacity_provider("test-capacity_provider", cluster="test-cluster", region_name="us-east-1")
    mock_client.delete_capacity_provider.assert_called_once()

def test_delete_service_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import delete_service
    mock_client = MagicMock()
    mock_client.delete_service.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    delete_service("test-service", cluster="test-cluster", force=True, region_name="us-east-1")
    mock_client.delete_service.assert_called_once()

def test_delete_task_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import delete_task_set
    mock_client = MagicMock()
    mock_client.delete_task_set.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    delete_task_set("test-cluster", "test-service", "test-task_set", force=True, region_name="us-east-1")
    mock_client.delete_task_set.assert_called_once()

def test_deregister_container_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import deregister_container_instance
    mock_client = MagicMock()
    mock_client.deregister_container_instance.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    deregister_container_instance("test-container_instance", cluster="test-cluster", force=True, region_name="us-east-1")
    mock_client.deregister_container_instance.assert_called_once()

def test_describe_capacity_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import describe_capacity_providers
    mock_client = MagicMock()
    mock_client.describe_capacity_providers.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    describe_capacity_providers(capacity_providers="test-capacity_providers", cluster="test-cluster", include=True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_capacity_providers.assert_called_once()

def test_describe_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import describe_clusters
    mock_client = MagicMock()
    mock_client.describe_clusters.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    describe_clusters(clusters="test-clusters", include=True, region_name="us-east-1")
    mock_client.describe_clusters.assert_called_once()

def test_describe_container_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import describe_container_instances
    mock_client = MagicMock()
    mock_client.describe_container_instances.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    describe_container_instances("test-container_instances", cluster="test-cluster", include=True, region_name="us-east-1")
    mock_client.describe_container_instances.assert_called_once()

def test_describe_task_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import describe_task_sets
    mock_client = MagicMock()
    mock_client.describe_task_sets.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    describe_task_sets("test-cluster", "test-service", task_sets="test-task_sets", include=True, region_name="us-east-1")
    mock_client.describe_task_sets.assert_called_once()

def test_discover_poll_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import discover_poll_endpoint
    mock_client = MagicMock()
    mock_client.discover_poll_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    discover_poll_endpoint(container_instance="test-container_instance", cluster="test-cluster", region_name="us-east-1")
    mock_client.discover_poll_endpoint.assert_called_once()

def test_execute_command_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import execute_command
    mock_client = MagicMock()
    mock_client.execute_command.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    execute_command("test-command", "test-interactive", "test-task", cluster="test-cluster", container="test-container", region_name="us-east-1")
    mock_client.execute_command.assert_called_once()

def test_get_task_protection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import get_task_protection
    mock_client = MagicMock()
    mock_client.get_task_protection.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    get_task_protection("test-cluster", tasks="test-tasks", region_name="us-east-1")
    mock_client.get_task_protection.assert_called_once()

def test_list_account_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_account_settings
    mock_client = MagicMock()
    mock_client.list_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_account_settings(name="test-name", value="test-value", principal_arn="test-principal_arn", effective_settings={}, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_account_settings.assert_called_once()

def test_list_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_attributes
    mock_client = MagicMock()
    mock_client.list_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_attributes("test-target_type", cluster="test-cluster", attribute_name="test-attribute_name", attribute_value="test-attribute_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_attributes.assert_called_once()

def test_list_container_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_container_instances
    mock_client = MagicMock()
    mock_client.list_container_instances.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_container_instances(cluster="test-cluster", filter="test-filter", next_token="test-next_token", max_results=1, status="test-status", region_name="us-east-1")
    mock_client.list_container_instances.assert_called_once()

def test_list_service_deployments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_service_deployments
    mock_client = MagicMock()
    mock_client.list_service_deployments.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_service_deployments("test-service", cluster="test-cluster", status="test-status", created_at="test-created_at", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_service_deployments.assert_called_once()

def test_list_services_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_services
    mock_client = MagicMock()
    mock_client.list_services.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_services(cluster="test-cluster", next_token="test-next_token", max_results=1, launch_type="test-launch_type", scheduling_strategy="test-scheduling_strategy", region_name="us-east-1")
    mock_client.list_services.assert_called_once()

def test_list_services_by_namespace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_services_by_namespace
    mock_client = MagicMock()
    mock_client.list_services_by_namespace.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_services_by_namespace("test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_services_by_namespace.assert_called_once()

def test_list_task_definition_families_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_task_definition_families
    mock_client = MagicMock()
    mock_client.list_task_definition_families.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_task_definition_families(family_prefix="test-family_prefix", status="test-status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_task_definition_families.assert_called_once()

def test_list_task_definitions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import list_task_definitions
    mock_client = MagicMock()
    mock_client.list_task_definitions.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    list_task_definitions(family_prefix="test-family_prefix", status="test-status", sort="test-sort", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_task_definitions.assert_called_once()

def test_put_account_setting_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import put_account_setting
    mock_client = MagicMock()
    mock_client.put_account_setting.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    put_account_setting("test-name", "test-value", principal_arn="test-principal_arn", region_name="us-east-1")
    mock_client.put_account_setting.assert_called_once()

def test_put_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import put_attributes
    mock_client = MagicMock()
    mock_client.put_attributes.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    put_attributes("test-attributes", cluster="test-cluster", region_name="us-east-1")
    mock_client.put_attributes.assert_called_once()

def test_register_container_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import register_container_instance
    mock_client = MagicMock()
    mock_client.register_container_instance.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    register_container_instance(cluster="test-cluster", instance_identity_document="test-instance_identity_document", instance_identity_document_signature="test-instance_identity_document_signature", total_resources="test-total_resources", version_info="test-version_info", container_instance_arn="test-container_instance_arn", attributes="test-attributes", platform_devices="test-platform_devices", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.register_container_instance.assert_called_once()

def test_register_task_definition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import register_task_definition
    mock_client = MagicMock()
    mock_client.register_task_definition.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    register_task_definition("test-family", {}, task_role_arn="test-task_role_arn", execution_role_arn="test-execution_role_arn", network_mode="test-network_mode", volumes="test-volumes", placement_constraints="test-placement_constraints", requires_compatibilities=True, cpu="test-cpu", memory="test-memory", tags=[{"Key": "k", "Value": "v"}], pid_mode="test-pid_mode", ipc_mode="test-ipc_mode", proxy_configuration={}, inference_accelerators="test-inference_accelerators", ephemeral_storage="test-ephemeral_storage", runtime_platform="test-runtime_platform", enable_fault_injection=True, region_name="us-east-1")
    mock_client.register_task_definition.assert_called_once()

def test_start_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import start_task
    mock_client = MagicMock()
    mock_client.start_task.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    start_task("test-container_instances", {}, cluster="test-cluster", enable_ecs_managed_tags=True, enable_execute_command=True, group="test-group", network_configuration={}, overrides="test-overrides", propagate_tags=[{"Key": "k", "Value": "v"}], reference_id="test-reference_id", started_by="test-started_by", tags=[{"Key": "k", "Value": "v"}], volume_configurations={}, region_name="us-east-1")
    mock_client.start_task.assert_called_once()

def test_stop_service_deployment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import stop_service_deployment
    mock_client = MagicMock()
    mock_client.stop_service_deployment.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    stop_service_deployment("test-service_deployment_arn", stop_type="test-stop_type", region_name="us-east-1")
    mock_client.stop_service_deployment.assert_called_once()

def test_submit_attachment_state_changes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import submit_attachment_state_changes
    mock_client = MagicMock()
    mock_client.submit_attachment_state_changes.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    submit_attachment_state_changes("test-attachments", cluster="test-cluster", region_name="us-east-1")
    mock_client.submit_attachment_state_changes.assert_called_once()

def test_submit_container_state_change_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import submit_container_state_change
    mock_client = MagicMock()
    mock_client.submit_container_state_change.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    submit_container_state_change(cluster="test-cluster", task="test-task", container_name="test-container_name", runtime_id="test-runtime_id", status="test-status", exit_code="test-exit_code", reason="test-reason", network_bindings="test-network_bindings", region_name="us-east-1")
    mock_client.submit_container_state_change.assert_called_once()

def test_submit_task_state_change_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import submit_task_state_change
    mock_client = MagicMock()
    mock_client.submit_task_state_change.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    submit_task_state_change(cluster="test-cluster", task="test-task", status="test-status", reason="test-reason", containers="test-containers", attachments="test-attachments", managed_agents="test-managed_agents", pull_started_at="test-pull_started_at", pull_stopped_at="test-pull_stopped_at", execution_stopped_at="test-execution_stopped_at", region_name="us-east-1")
    mock_client.submit_task_state_change.assert_called_once()

def test_update_capacity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import update_capacity_provider
    mock_client = MagicMock()
    mock_client.update_capacity_provider.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    update_capacity_provider("test-name", cluster="test-cluster", auto_scaling_group_provider=True, managed_instances_provider="test-managed_instances_provider", region_name="us-east-1")
    mock_client.update_capacity_provider.assert_called_once()

def test_update_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import update_cluster
    mock_client = MagicMock()
    mock_client.update_cluster.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    update_cluster("test-cluster", settings={}, configuration={}, service_connect_defaults="test-service_connect_defaults", region_name="us-east-1")
    mock_client.update_cluster.assert_called_once()

def test_update_container_agent_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import update_container_agent
    mock_client = MagicMock()
    mock_client.update_container_agent.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    update_container_agent("test-container_instance", cluster="test-cluster", region_name="us-east-1")
    mock_client.update_container_agent.assert_called_once()

def test_update_container_instances_state_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import update_container_instances_state
    mock_client = MagicMock()
    mock_client.update_container_instances_state.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    update_container_instances_state("test-container_instances", "test-status", cluster="test-cluster", region_name="us-east-1")
    mock_client.update_container_instances_state.assert_called_once()

def test_update_task_protection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ecs import update_task_protection
    mock_client = MagicMock()
    mock_client.update_task_protection.return_value = {}
    monkeypatch.setattr("aws_util.ecs.get_client", lambda *a, **kw: mock_client)
    update_task_protection("test-cluster", "test-tasks", "test-protection_enabled", expires_in_minutes="test-expires_in_minutes", region_name="us-east-1")
    mock_client.update_task_protection.assert_called_once()
