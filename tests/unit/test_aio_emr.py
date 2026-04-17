"""Tests for aws_util.aio.emr module."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.emr import (
    BootstrapActionResult,
    ClusterResult,
    InstanceGroupResult,
    SecurityConfigurationResult,
    StepResult,
    _READY_STATES,
    _TERMINAL_STATES,
    add_instance_groups,
    add_job_flow_steps,
    create_security_configuration,
    describe_cluster,
    describe_step,
    list_bootstrap_actions,
    list_clusters,
    list_instance_groups,
    list_security_configurations,
    list_steps,
    modify_instance_groups,
    put_auto_scaling_policy,
    run_and_wait,
    run_job_flow,
    set_termination_protection,
    terminate_job_flows,
    wait_for_cluster,
    add_instance_fleet,
    add_tags,
    cancel_steps,
    create_persistent_app_ui,
    create_studio,
    create_studio_session_mapping,
    delete_security_configuration,
    delete_studio,
    delete_studio_session_mapping,
    describe_job_flows,
    describe_notebook_execution,
    describe_persistent_app_ui,
    describe_release_label,
    describe_security_configuration,
    describe_studio,
    get_auto_termination_policy,
    get_block_public_access_configuration,
    get_cluster_session_credentials,
    get_managed_scaling_policy,
    get_on_cluster_app_ui_presigned_url,
    get_persistent_app_ui_presigned_url,
    get_studio_session_mapping,
    list_instance_fleets,
    list_instances,
    list_notebook_executions,
    list_release_labels,
    list_studio_session_mappings,
    list_studios,
    list_supported_instance_types,
    modify_cluster,
    modify_instance_fleet,
    put_auto_termination_policy,
    put_block_public_access_configuration,
    put_managed_scaling_policy,
    remove_auto_scaling_policy,
    remove_auto_termination_policy,
    remove_managed_scaling_policy,
    remove_tags,
    set_keep_job_flow_alive_when_no_steps,
    set_unhealthy_node_replacement,
    set_visible_to_all_users,
    start_notebook_execution,
    stop_notebook_execution,
    update_studio,
    update_studio_session_mapping,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError



REGION = "us-east-1"

CLUSTER_ID = "j-ABCDEF12345"
STEP_ID = "s-STEP12345"
IG_ID = "ig-IG12345"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _cluster_dict(**overrides):
    d = {
        "Id": CLUSTER_ID,
        "Name": "test-cluster",
        "Status": {"State": "WAITING", "StateChangeReason": {}},
        "NormalizedInstanceHours": 100,
        "LogUri": "s3://logs/emr/",
        "ReleaseLabel": "emr-6.15.0",
        "AutoTerminate": False,
        "TerminationProtected": True,
        "Tags": [{"Key": "env", "Value": "test"}],
    }
    d.update(overrides)
    return d


def _step_dict(**overrides):
    d = {
        "Id": STEP_ID,
        "Name": "MyStep",
        "Status": {"State": "COMPLETED"},
        "ActionOnFailure": "CONTINUE",
    }
    d.update(overrides)
    return d


def _ig_dict(**overrides):
    d = {
        "Id": IG_ID,
        "Name": "Core",
        "Market": "ON_DEMAND",
        "InstanceGroupType": "CORE",
        "InstanceType": "m5.xlarge",
        "RequestedInstanceCount": 2,
        "RunningInstanceCount": 2,
        "Status": {"State": "RUNNING"},
    }
    d.update(overrides)
    return d


def _sec_config_dict(**overrides):
    d = {"Name": "my-sec-config", "CreationDateTime": "2024-01-01T00:00:00Z"}
    d.update(overrides)
    return d


def _bootstrap_dict(**overrides):
    d = {
        "Name": "MyBootstrap",
        "ScriptBootstrapAction": {
            "Path": "s3://bucket/bootstrap.sh",
            "Args": ["--flag"],
        },
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# run_job_flow
# ---------------------------------------------------------------------------


async def test_run_job_flow_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"JobFlowId": CLUSTER_ID}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await run_job_flow("test", region_name=REGION)
    assert result == CLUSTER_ID


async def test_run_job_flow_all_options(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"JobFlowId": CLUSTER_ID}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await run_job_flow(
        "test",
        log_uri="s3://logs",
        release_label="emr-6.15.0",
        instances={"InstanceGroups": []},
        steps=[],
        applications=[{"Name": "Spark"}],
        configurations=[],
        service_role="role1",
        job_flow_role="role2",
        tags=[{"Key": "k", "Value": "v"}],
        visible_to_all_users=False,
        region_name=REGION,
    )
    assert result == CLUSTER_ID


async def test_run_job_flow_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await run_job_flow("test", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_cluster
# ---------------------------------------------------------------------------


async def test_describe_cluster_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Cluster": _cluster_dict()}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await describe_cluster(CLUSTER_ID, region_name=REGION)
    assert result.cluster_id == CLUSTER_ID


async def test_describe_cluster_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_cluster(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------


async def test_list_clusters_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_cluster_dict()]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_clusters(region_name=REGION)
    assert len(result) == 1


async def test_list_clusters_with_states(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = []
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_clusters(
        cluster_states=["WAITING"], region_name=REGION,
    )
    assert result == []


async def test_list_clusters_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_clusters(region_name=REGION)


# ---------------------------------------------------------------------------
# terminate_job_flows
# ---------------------------------------------------------------------------


async def test_terminate_job_flows_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    await terminate_job_flows([CLUSTER_ID], region_name=REGION)


async def test_terminate_job_flows_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await terminate_job_flows([CLUSTER_ID], region_name=REGION)


# ---------------------------------------------------------------------------
# add_job_flow_steps / list_steps / describe_step
# ---------------------------------------------------------------------------


async def test_add_job_flow_steps_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"StepIds": [STEP_ID]}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await add_job_flow_steps(CLUSTER_ID, [{}], region_name=REGION)
    assert result == [STEP_ID]


async def test_add_job_flow_steps_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await add_job_flow_steps(CLUSTER_ID, [{}], region_name=REGION)


async def test_list_steps_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_step_dict()]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_steps(CLUSTER_ID, region_name=REGION)
    assert len(result) == 1


async def test_list_steps_with_states(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = []
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_steps(
        CLUSTER_ID, step_states=["COMPLETED"], region_name=REGION,
    )
    assert result == []


async def test_list_steps_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_steps(CLUSTER_ID, region_name=REGION)


async def test_describe_step_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Step": _step_dict()}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await describe_step(CLUSTER_ID, STEP_ID, region_name=REGION)
    assert result.step_id == STEP_ID


async def test_describe_step_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_step(CLUSTER_ID, STEP_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Instance groups
# ---------------------------------------------------------------------------


async def test_add_instance_groups_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"InstanceGroupIds": [IG_ID]}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await add_instance_groups(CLUSTER_ID, [{}], region_name=REGION)
    assert result == [IG_ID]


async def test_add_instance_groups_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await add_instance_groups(CLUSTER_ID, [{}], region_name=REGION)


async def test_list_instance_groups_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_ig_dict()]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_instance_groups(CLUSTER_ID, region_name=REGION)
    assert len(result) == 1


async def test_list_instance_groups_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_instance_groups(CLUSTER_ID, region_name=REGION)


async def test_modify_instance_groups_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    await modify_instance_groups([{}], cluster_id=CLUSTER_ID, region_name=REGION)


async def test_modify_instance_groups_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await modify_instance_groups([{}], region_name=REGION)


# ---------------------------------------------------------------------------
# Security config
# ---------------------------------------------------------------------------


async def test_create_security_configuration_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = _sec_config_dict()
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await create_security_configuration(
        "my-sec", "{}", region_name=REGION,
    )
    assert result.name == "my-sec-config"


async def test_create_security_configuration_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_security_configuration("x", "{}", region_name=REGION)


async def test_list_security_configurations_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_sec_config_dict()]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_security_configurations(region_name=REGION)
    assert len(result) == 1


async def test_list_security_configurations_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_security_configurations(region_name=REGION)


# ---------------------------------------------------------------------------
# Termination protection & auto-scaling
# ---------------------------------------------------------------------------


async def test_set_termination_protection_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    await set_termination_protection(
        [CLUSTER_ID], True, region_name=REGION,
    )


async def test_set_termination_protection_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await set_termination_protection(
            [CLUSTER_ID], True, region_name=REGION,
        )


async def test_put_auto_scaling_policy_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"ClusterId": CLUSTER_ID}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await put_auto_scaling_policy(
        CLUSTER_ID, IG_ID, {"Rules": []}, region_name=REGION,
    )
    assert result["ClusterId"] == CLUSTER_ID


async def test_put_auto_scaling_policy_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await put_auto_scaling_policy(
            CLUSTER_ID, IG_ID, {}, region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Bootstrap actions
# ---------------------------------------------------------------------------


async def test_list_bootstrap_actions_success(monkeypatch):
    client = AsyncMock()
    client.paginate.return_value = [_bootstrap_dict()]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    result = await list_bootstrap_actions(CLUSTER_ID, region_name=REGION)
    assert len(result) == 1


async def test_list_bootstrap_actions_error(monkeypatch):
    client = AsyncMock()
    client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await list_bootstrap_actions(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cluster_ready(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Cluster": _cluster_dict(Status={"State": "WAITING", "StateChangeReason": {}})}
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_cluster(CLUSTER_ID, timeout=10, region_name=REGION)
    assert result.status == "WAITING"


async def test_wait_for_cluster_terminal(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Cluster": _cluster_dict(
            Status={"State": "TERMINATED_WITH_ERRORS", "StateChangeReason": {}},
        ),
    }
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    with pytest.raises(AwsServiceError):
        await wait_for_cluster(CLUSTER_ID, timeout=10, region_name=REGION)


async def test_wait_for_cluster_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Cluster": _cluster_dict(
            Status={"State": "STARTING", "StateChangeReason": {}},
        ),
    }
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    import time as _time

    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(_time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_cluster(
            CLUSTER_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_cluster_poll_then_ready(monkeypatch):
    """Cover the sleep branch: first poll STARTING, second WAITING."""
    client = AsyncMock()
    client.call.side_effect = [
        {
            "Cluster": _cluster_dict(
                Status={"State": "STARTING", "StateChangeReason": {}},
            ),
        },
        {
            "Cluster": _cluster_dict(
                Status={"State": "WAITING", "StateChangeReason": {}},
            ),
        },
    ]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_cluster(
        CLUSTER_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert result.status == "WAITING"


# ---------------------------------------------------------------------------
# run_and_wait
# ---------------------------------------------------------------------------


async def test_run_and_wait_success(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"JobFlowId": CLUSTER_ID},
        {"Cluster": _cluster_dict(Status={"State": "WAITING", "StateChangeReason": {}})},
    ]
    monkeypatch.setattr("aws_util.aio.emr.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await run_and_wait("test", timeout=10, region_name=REGION)
    assert result.cluster_id == CLUSTER_ID


async def test_add_instance_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_instance_fleet("test-cluster_id", {}, )
    mock_client.call.assert_called_once()


async def test_add_instance_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_instance_fleet("test-cluster_id", {}, )


async def test_add_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags("test-resource_id", [], )


async def test_cancel_steps(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_steps("test-cluster_id", [], )
    mock_client.call.assert_called_once()


async def test_cancel_steps_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_steps("test-cluster_id", [], )


async def test_create_persistent_app_ui(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_persistent_app_ui("test-target_resource_arn", )
    mock_client.call.assert_called_once()


async def test_create_persistent_app_ui_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_persistent_app_ui("test-target_resource_arn", )


async def test_create_studio(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_studio("test-name", "test-auth_mode", "test-vpc_id", [], "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", )
    mock_client.call.assert_called_once()


async def test_create_studio_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_studio("test-name", "test-auth_mode", "test-vpc_id", [], "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", )


async def test_create_studio_session_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", )
    mock_client.call.assert_called_once()


async def test_create_studio_session_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", )


async def test_delete_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_security_configuration("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_security_configuration("test-name", )


async def test_delete_studio(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_studio("test-studio_id", )
    mock_client.call.assert_called_once()


async def test_delete_studio_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_studio("test-studio_id", )


async def test_delete_studio_session_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_studio_session_mapping("test-studio_id", "test-identity_type", )
    mock_client.call.assert_called_once()


async def test_delete_studio_session_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_studio_session_mapping("test-studio_id", "test-identity_type", )


async def test_describe_job_flows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_job_flows()
    mock_client.call.assert_called_once()


async def test_describe_job_flows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_job_flows()


async def test_describe_notebook_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_notebook_execution("test-notebook_execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_notebook_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_notebook_execution("test-notebook_execution_id", )


async def test_describe_persistent_app_ui(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_persistent_app_ui("test-persistent_app_ui_id", )
    mock_client.call.assert_called_once()


async def test_describe_persistent_app_ui_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_persistent_app_ui("test-persistent_app_ui_id", )


async def test_describe_release_label(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_release_label()
    mock_client.call.assert_called_once()


async def test_describe_release_label_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_release_label()


async def test_describe_security_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_configuration("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_security_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_configuration("test-name", )


async def test_describe_studio(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_studio("test-studio_id", )
    mock_client.call.assert_called_once()


async def test_describe_studio_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_studio("test-studio_id", )


async def test_get_auto_termination_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_auto_termination_policy("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_get_auto_termination_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_auto_termination_policy("test-cluster_id", )


async def test_get_block_public_access_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_block_public_access_configuration()
    mock_client.call.assert_called_once()


async def test_get_block_public_access_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_block_public_access_configuration()


async def test_get_cluster_session_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cluster_session_credentials("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_get_cluster_session_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cluster_session_credentials("test-cluster_id", )


async def test_get_managed_scaling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_managed_scaling_policy("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_get_managed_scaling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_managed_scaling_policy("test-cluster_id", )


async def test_get_on_cluster_app_ui_presigned_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_on_cluster_app_ui_presigned_url("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_get_on_cluster_app_ui_presigned_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_on_cluster_app_ui_presigned_url("test-cluster_id", )


async def test_get_persistent_app_ui_presigned_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", )
    mock_client.call.assert_called_once()


async def test_get_persistent_app_ui_presigned_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", )


async def test_get_studio_session_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_studio_session_mapping("test-studio_id", "test-identity_type", )
    mock_client.call.assert_called_once()


async def test_get_studio_session_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_studio_session_mapping("test-studio_id", "test-identity_type", )


async def test_list_instance_fleets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_fleets("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_list_instance_fleets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_fleets("test-cluster_id", )


async def test_list_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instances("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_list_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instances("test-cluster_id", )


async def test_list_notebook_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_notebook_executions()
    mock_client.call.assert_called_once()


async def test_list_notebook_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_notebook_executions()


async def test_list_release_labels(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_release_labels()
    mock_client.call.assert_called_once()


async def test_list_release_labels_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_release_labels()


async def test_list_studio_session_mappings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_studio_session_mappings()
    mock_client.call.assert_called_once()


async def test_list_studio_session_mappings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_studio_session_mappings()


async def test_list_studios(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_studios()
    mock_client.call.assert_called_once()


async def test_list_studios_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_studios()


async def test_list_supported_instance_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_supported_instance_types("test-release_label", )
    mock_client.call.assert_called_once()


async def test_list_supported_instance_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_supported_instance_types("test-release_label", )


async def test_modify_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cluster("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_modify_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cluster("test-cluster_id", )


async def test_modify_instance_fleet(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_instance_fleet("test-cluster_id", {}, )
    mock_client.call.assert_called_once()


async def test_modify_instance_fleet_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_instance_fleet("test-cluster_id", {}, )


async def test_put_auto_termination_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_auto_termination_policy("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_put_auto_termination_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_auto_termination_policy("test-cluster_id", )


async def test_put_block_public_access_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_block_public_access_configuration({}, )
    mock_client.call.assert_called_once()


async def test_put_block_public_access_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_block_public_access_configuration({}, )


async def test_put_managed_scaling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_managed_scaling_policy("test-cluster_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_managed_scaling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_managed_scaling_policy("test-cluster_id", {}, )


async def test_remove_auto_scaling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_auto_scaling_policy("test-cluster_id", "test-instance_group_id", )
    mock_client.call.assert_called_once()


async def test_remove_auto_scaling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_auto_scaling_policy("test-cluster_id", "test-instance_group_id", )


async def test_remove_auto_termination_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_auto_termination_policy("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_remove_auto_termination_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_auto_termination_policy("test-cluster_id", )


async def test_remove_managed_scaling_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_managed_scaling_policy("test-cluster_id", )
    mock_client.call.assert_called_once()


async def test_remove_managed_scaling_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_managed_scaling_policy("test-cluster_id", )


async def test_remove_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags("test-resource_id", [], )


async def test_set_keep_job_flow_alive_when_no_steps(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_keep_job_flow_alive_when_no_steps([], True, )
    mock_client.call.assert_called_once()


async def test_set_keep_job_flow_alive_when_no_steps_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_keep_job_flow_alive_when_no_steps([], True, )


async def test_set_unhealthy_node_replacement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_unhealthy_node_replacement([], True, )
    mock_client.call.assert_called_once()


async def test_set_unhealthy_node_replacement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_unhealthy_node_replacement([], True, )


async def test_set_visible_to_all_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_visible_to_all_users([], True, )
    mock_client.call.assert_called_once()


async def test_set_visible_to_all_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_visible_to_all_users([], True, )


async def test_start_notebook_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_notebook_execution({}, "test-service_role", )
    mock_client.call.assert_called_once()


async def test_start_notebook_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_notebook_execution({}, "test-service_role", )


async def test_stop_notebook_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_notebook_execution("test-notebook_execution_id", )
    mock_client.call.assert_called_once()


async def test_stop_notebook_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_notebook_execution("test-notebook_execution_id", )


async def test_update_studio(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_studio("test-studio_id", )
    mock_client.call.assert_called_once()


async def test_update_studio_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_studio("test-studio_id", )


async def test_update_studio_session_mapping(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", )
    mock_client.call.assert_called_once()


async def test_update_studio_session_mapping_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.emr.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", )


@pytest.mark.asyncio
async def test_modify_instance_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import modify_instance_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await modify_instance_groups("test-instance_groups", cluster_id="test-cluster_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_steps_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import cancel_steps
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await cancel_steps("test-cluster_id", "test-step_ids", step_cancellation_option="test-step_cancellation_option", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_persistent_app_ui_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import create_persistent_app_ui
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await create_persistent_app_ui("test-target_resource_arn", emr_containers_config={}, tags=[{"Key": "k", "Value": "v"}], x_referer="test-x_referer", profiler_type="test-profiler_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_studio_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import create_studio
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await create_studio("test-name", "test-auth_mode", "test-vpc_id", "test-subnet_ids", "test-service_role", "test-workspace_security_group_id", "test-engine_security_group_id", "test-default_s3_location", description="test-description", user_role="test-user_role", idp_auth_url="test-idp_auth_url", idp_relay_state_parameter_name="test-idp_relay_state_parameter_name", tags=[{"Key": "k", "Value": "v"}], trusted_identity_propagation_enabled="test-trusted_identity_propagation_enabled", idc_user_assignment="test-idc_user_assignment", idc_instance_arn="test-idc_instance_arn", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import create_studio_session_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await create_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import delete_studio_session_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await delete_studio_session_mapping("test-studio_id", "test-identity_type", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_job_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import describe_job_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await describe_job_flows(created_after="test-created_after", created_before="test-created_before", job_flow_ids="test-job_flow_ids", job_flow_states="test-job_flow_states", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_release_label_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import describe_release_label
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await describe_release_label(release_label="test-release_label", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cluster_session_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import get_cluster_session_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await get_cluster_session_credentials("test-cluster_id", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_on_cluster_app_ui_presigned_url_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import get_on_cluster_app_ui_presigned_url
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await get_on_cluster_app_ui_presigned_url("test-cluster_id", on_cluster_app_ui_type="test-on_cluster_app_ui_type", application_id="test-application_id", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_persistent_app_ui_presigned_url_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import get_persistent_app_ui_presigned_url
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await get_persistent_app_ui_presigned_url("test-persistent_app_ui_id", persistent_app_ui_type="test-persistent_app_ui_type", application_id="test-application_id", auth_proxy_call="test-auth_proxy_call", execution_role_arn="test-execution_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import get_studio_session_mapping
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await get_studio_session_mapping("test-studio_id", "test-identity_type", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_fleets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_instance_fleets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_instance_fleets("test-cluster_id", marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_instances("test-cluster_id", instance_group_id="test-instance_group_id", instance_group_types="test-instance_group_types", instance_fleet_id="test-instance_fleet_id", instance_fleet_type="test-instance_fleet_type", instance_states="test-instance_states", marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_notebook_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_notebook_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_notebook_executions(editor_id="test-editor_id", status="test-status", from_value="test-from_value", to="test-to", marker="test-marker", execution_engine_id="test-execution_engine_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_release_labels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_release_labels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_release_labels(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_studio_session_mappings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_studio_session_mappings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_studio_session_mappings(studio_id="test-studio_id", identity_type="test-identity_type", marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_studios_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_studios
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_studios(marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_supported_instance_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import list_supported_instance_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await list_supported_instance_types("test-release_label", marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import modify_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await modify_cluster("test-cluster_id", step_concurrency_level="test-step_concurrency_level", extended_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_auto_termination_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import put_auto_termination_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await put_auto_termination_policy("test-cluster_id", auto_termination_policy=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_notebook_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import start_notebook_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await start_notebook_execution("test-execution_engine", "test-service_role", editor_id="test-editor_id", relative_path="test-relative_path", notebook_execution_name="test-notebook_execution_name", notebook_params="test-notebook_params", notebook_instance_security_group_id="test-notebook_instance_security_group_id", tags=[{"Key": "k", "Value": "v"}], notebook_s3_location="test-notebook_s3_location", output_notebook_s3_location="test-output_notebook_s3_location", output_notebook_format="test-output_notebook_format", environment_variables="test-environment_variables", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_studio_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import update_studio
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await update_studio("test-studio_id", name="test-name", description="test-description", subnet_ids="test-subnet_ids", default_s3_location="test-default_s3_location", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_studio_session_mapping_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.emr import update_studio_session_mapping



    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.emr.async_client", lambda *a, **kw: mock_client)
    await update_studio_session_mapping("test-studio_id", "test-identity_type", "test-session_policy_arn", identity_id="test-identity_id", identity_name="test-identity_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
