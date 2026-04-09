from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.cloudformation import (
    CFNStack,
    create_stack,
    delete_stack,
    deploy_stack,
    describe_stack,
    get_export_value,
    get_stack_outputs,
    list_stacks,
    update_stack,
    wait_for_stack,
    activate_organizations_access,
    activate_type,
    batch_describe_type_configurations,
    cancel_update_stack,
    continue_update_rollback,
    create_change_set,
    create_generated_template,
    create_stack_instances,
    create_stack_refactor,
    create_stack_set,
    deactivate_organizations_access,
    deactivate_type,
    delete_change_set,
    delete_generated_template,
    delete_stack_instances,
    delete_stack_set,
    deregister_type,
    describe_account_limits,
    describe_change_set,
    describe_change_set_hooks,
    describe_generated_template,
    describe_organizations_access,
    describe_publisher,
    describe_resource_scan,
    describe_stack_drift_detection_status,
    describe_stack_events,
    describe_stack_instance,
    describe_stack_refactor,
    describe_stack_resource,
    describe_stack_resource_drifts,
    describe_stack_resources,
    describe_stack_set,
    describe_stack_set_operation,
    describe_stacks,
    describe_type,
    describe_type_registration,
    detect_stack_drift,
    detect_stack_resource_drift,
    detect_stack_set_drift,
    estimate_template_cost,
    execute_change_set,
    execute_stack_refactor,
    get_generated_template,
    get_hook_result,
    get_stack_policy,
    get_template,
    get_template_summary,
    import_stacks_to_stack_set,
    list_change_sets,
    list_exports,
    list_generated_templates,
    list_hook_results,
    list_imports,
    list_resource_scan_related_resources,
    list_resource_scan_resources,
    list_resource_scans,
    list_stack_instance_resource_drifts,
    list_stack_instances,
    list_stack_refactor_actions,
    list_stack_refactors,
    list_stack_resources,
    list_stack_set_auto_deployment_targets,
    list_stack_set_operation_results,
    list_stack_set_operations,
    list_stack_sets,
    list_type_registrations,
    list_type_versions,
    list_types,
    publish_type,
    record_handler_progress,
    register_publisher,
    register_type,
    rollback_stack,
    run_type,
    set_stack_policy,
    set_type_configuration,
    set_type_default_version,
    signal_resource,
    start_resource_scan,
    stop_stack_set_operation,
    update_generated_template,
    update_stack_instances,
    update_stack_set,
    update_termination_protection,
    validate_template,
)


_STACK_RESP = {
    "Stacks": [
        {
            "StackId": "arn:aws:cfn:us-east-1:123:stack/my/guid",
            "StackName": "my-stack",
            "StackStatus": "CREATE_COMPLETE",
            "Outputs": [{"OutputKey": "Url", "OutputValue": "https://x"}],
            "Parameters": [
                {"ParameterKey": "Env", "ParameterValue": "prod"}
            ],
            "Tags": [{"Key": "team", "Value": "eng"}],
        }
    ]
}


# ---------------------------------------------------------------------------
# describe_stack
# ---------------------------------------------------------------------------


async def test_describe_stack_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _STACK_RESP
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    stack = await describe_stack("my-stack")
    assert stack is not None
    assert stack.stack_name == "my-stack"
    assert stack.outputs == {"Url": "https://x"}


async def test_describe_stack_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("Stack does not exist")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_stack("nope")
    assert result is None


async def test_describe_stack_empty_stacks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Stacks": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_stack("empty")
    assert result is None


async def test_describe_stack_other_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await describe_stack("my-stack")


# ---------------------------------------------------------------------------
# list_stacks
# ---------------------------------------------------------------------------


async def test_list_stacks_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StackSummaries": [
            {
                "StackId": "id-1",
                "StackName": "stack-1",
                "StackStatus": "CREATE_COMPLETE",
                "StackStatusReason": "done",
                "CreationTime": "2024-01-01",
                "LastUpdatedTime": "2024-01-02",
            }
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_stacks()
    assert len(result) == 1
    assert result[0].stack_name == "stack-1"


async def test_list_stacks_with_filter(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackSummaries": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_stacks(status_filter=["CREATE_COMPLETE"])
    assert result == []


async def test_list_stacks_pagination(monkeypatch):
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "StackSummaries": [
                    {
                        "StackId": "id1",
                        "StackName": "s1",
                        "StackStatus": "CREATE_COMPLETE",
                    }
                ],
                "NextToken": "tok",
            }
        return {
            "StackSummaries": [
                {
                    "StackId": "id2",
                    "StackName": "s2",
                    "StackStatus": "UPDATE_COMPLETE",
                }
            ],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_stacks()
    assert len(result) == 2


async def test_list_stacks_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stacks()


async def test_list_stacks_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_stacks failed"):
        await list_stacks()


# ---------------------------------------------------------------------------
# get_stack_outputs
# ---------------------------------------------------------------------------


async def test_get_stack_outputs_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _STACK_RESP
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    outputs = await get_stack_outputs("my-stack")
    assert outputs == {"Url": "https://x"}


async def test_get_stack_outputs_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("does not exist")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="not found"):
        await get_stack_outputs("nope")


# ---------------------------------------------------------------------------
# create_stack
# ---------------------------------------------------------------------------


async def test_create_stack_string_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "new-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_stack("s", "{}")
    assert result == "new-id"


async def test_create_stack_dict_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "new-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_stack(
        "s", {"AWSTemplateFormatVersion": "2010-09-09"}
    )
    assert result == "new-id"


async def test_create_stack_with_params_and_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "new-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_stack(
        "s",
        "{}",
        parameters={"Env": "prod"},
        capabilities=["CAPABILITY_IAM"],
        tags={"team": "eng"},
    )
    assert result == "new-id"


async def test_create_stack_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await create_stack("s", "{}")


async def test_create_stack_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to create stack"):
        await create_stack("s", "{}")


# ---------------------------------------------------------------------------
# update_stack
# ---------------------------------------------------------------------------


async def test_update_stack_string(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "upd-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_stack("s", "{}")
    assert result == "upd-id"


async def test_update_stack_dict(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "upd-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_stack("s", {"key": "val"})
    assert result == "upd-id"


async def test_update_stack_with_params(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"StackId": "upd-id"}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_stack(
        "s",
        "{}",
        parameters={"Env": "staging"},
        capabilities=["CAPABILITY_NAMED_IAM"],
    )
    assert result == "upd-id"


async def test_update_stack_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await update_stack("s", "{}")


async def test_update_stack_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to update stack"):
        await update_stack("s", "{}")


# ---------------------------------------------------------------------------
# delete_stack
# ---------------------------------------------------------------------------


async def test_delete_stack_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stack("my-stack")
    mock_client.call.assert_awaited_once()


async def test_delete_stack_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="fail"):
        await delete_stack("s")


async def test_delete_stack_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to delete stack"):
        await delete_stack("s")


# ---------------------------------------------------------------------------
# wait_for_stack
# ---------------------------------------------------------------------------


async def test_wait_for_stack_immediate_stable(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _STACK_RESP
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.asyncio.sleep", AsyncMock()
    )
    stack = await wait_for_stack("my-stack")
    assert stack.status == "CREATE_COMPLETE"


async def test_wait_for_stack_becomes_stable(monkeypatch):
    call_count = 0

    async def _fake_describe(name, region_name=None):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return CFNStack(
                stack_id="id",
                stack_name=name,
                status="CREATE_IN_PROGRESS",
            )
        return CFNStack(
            stack_id="id",
            stack_name=name,
            status="CREATE_COMPLETE",
        )

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.asyncio.sleep", AsyncMock()
    )
    stack = await wait_for_stack("s", timeout=60.0)
    assert stack.status == "CREATE_COMPLETE"


async def test_wait_for_stack_not_found(monkeypatch):
    async def _fake_describe(name, region_name=None):
        return None

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.asyncio.sleep", AsyncMock()
    )
    with pytest.raises(RuntimeError, match="not found during wait"):
        await wait_for_stack("s")


async def test_wait_for_stack_timeout(monkeypatch):
    async def _fake_describe(name, region_name=None):
        return CFNStack(
            stack_id="id",
            stack_name=name,
            status="CREATE_IN_PROGRESS",
        )

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.asyncio.sleep", AsyncMock()
    )
    with pytest.raises(TimeoutError, match="did not stabilise"):
        await wait_for_stack("s", timeout=0.0)


# ---------------------------------------------------------------------------
# deploy_stack
# ---------------------------------------------------------------------------


async def test_deploy_stack_create_new(monkeypatch):
    async def _fake_describe(name, region_name=None):
        return None

    async def _fake_create(name, body, **kwargs):
        return "new-id"

    healthy_stack = CFNStack(
        stack_id="new-id",
        stack_name="s",
        status="CREATE_COMPLETE",
    )

    async def _fake_wait(name, timeout=1800.0, region_name=None):
        return healthy_stack

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.create_stack", _fake_create
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.wait_for_stack", _fake_wait
    )
    result = await deploy_stack("s", "{}")
    assert result.status == "CREATE_COMPLETE"


async def test_deploy_stack_update_existing(monkeypatch):
    existing = CFNStack(
        stack_id="id",
        stack_name="s",
        status="CREATE_COMPLETE",
    )

    async def _fake_describe(name, region_name=None):
        return existing

    async def _fake_update(name, body, **kwargs):
        return "id"

    updated = CFNStack(
        stack_id="id",
        stack_name="s",
        status="UPDATE_COMPLETE",
    )

    async def _fake_wait(name, timeout=1800.0, region_name=None):
        return updated

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.update_stack", _fake_update
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.wait_for_stack", _fake_wait
    )
    result = await deploy_stack("s", "{}")
    assert result.status == "UPDATE_COMPLETE"


async def test_deploy_stack_no_updates(monkeypatch):
    existing = CFNStack(
        stack_id="id",
        stack_name="s",
        status="CREATE_COMPLETE",
    )

    async def _fake_describe(name, region_name=None):
        return existing

    async def _fake_update(name, body, **kwargs):
        raise RuntimeError("No updates are to be performed")

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.update_stack", _fake_update
    )
    result = await deploy_stack("s", "{}")
    assert result is existing


async def test_deploy_stack_update_error(monkeypatch):
    existing = CFNStack(
        stack_id="id",
        stack_name="s",
        status="CREATE_COMPLETE",
    )

    async def _fake_describe(name, region_name=None):
        return existing

    async def _fake_update(name, body, **kwargs):
        raise RuntimeError("real error")

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.update_stack", _fake_update
    )
    with pytest.raises(RuntimeError, match="real error"):
        await deploy_stack("s", "{}")


async def test_deploy_stack_unhealthy(monkeypatch):
    async def _fake_describe(name, region_name=None):
        return None

    async def _fake_create(name, body, **kwargs):
        return "id"

    unhealthy = CFNStack(
        stack_id="id",
        stack_name="s",
        status="CREATE_FAILED",
        status_reason="boom",
    )

    async def _fake_wait(name, timeout=1800.0, region_name=None):
        return unhealthy

    monkeypatch.setattr(
        "aws_util.aio.cloudformation.describe_stack", _fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.create_stack", _fake_create
    )
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.wait_for_stack", _fake_wait
    )
    with pytest.raises(RuntimeError, match="deployment failed"):
        await deploy_stack("s", "{}")


# ---------------------------------------------------------------------------
# get_export_value
# ---------------------------------------------------------------------------


async def test_get_export_value_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Exports": [
            {"Name": "VpcId", "Value": "vpc-123"},
            {"Name": "SubnetId", "Value": "subnet-456"},
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_export_value("VpcId")
    assert result == "vpc-123"


async def test_get_export_value_not_found(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Exports": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(KeyError, match="not found"):
        await get_export_value("Missing")


async def test_get_export_value_pagination(monkeypatch):
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "Exports": [{"Name": "A", "Value": "a"}],
                "NextToken": "tok",
            }
        return {
            "Exports": [{"Name": "B", "Value": "b"}],
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_export_value("B")
    assert result == "b"


async def test_get_export_value_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_export_value("X")


async def test_get_export_value_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="get_export_value failed"):
        await get_export_value("X")


async def test_activate_organizations_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await activate_organizations_access()
    mock_client.call.assert_called_once()


async def test_activate_organizations_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await activate_organizations_access()


async def test_activate_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await activate_type()
    mock_client.call.assert_called_once()


async def test_activate_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await activate_type()


async def test_batch_describe_type_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_describe_type_configurations([], )
    mock_client.call.assert_called_once()


async def test_batch_describe_type_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_describe_type_configurations([], )


async def test_cancel_update_stack(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_update_stack("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_cancel_update_stack_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_update_stack("test-stack_name", )


async def test_continue_update_rollback(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await continue_update_rollback("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_continue_update_rollback_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await continue_update_rollback("test-stack_name", )


async def test_create_change_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_change_set("test-stack_name", "test-change_set_name", )
    mock_client.call.assert_called_once()


async def test_create_change_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_change_set("test-stack_name", "test-change_set_name", )


async def test_create_generated_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_generated_template("test-generated_template_name", )
    mock_client.call.assert_called_once()


async def test_create_generated_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_generated_template("test-generated_template_name", )


async def test_create_stack_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stack_instances("test-stack_set_name", [], )
    mock_client.call.assert_called_once()


async def test_create_stack_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stack_instances("test-stack_set_name", [], )


async def test_create_stack_refactor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stack_refactor([], )
    mock_client.call.assert_called_once()


async def test_create_stack_refactor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stack_refactor([], )


async def test_create_stack_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stack_set("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_create_stack_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stack_set("test-stack_set_name", )


async def test_deactivate_organizations_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_organizations_access()
    mock_client.call.assert_called_once()


async def test_deactivate_organizations_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_organizations_access()


async def test_deactivate_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_type()
    mock_client.call.assert_called_once()


async def test_deactivate_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_type()


async def test_delete_change_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_change_set("test-change_set_name", )
    mock_client.call.assert_called_once()


async def test_delete_change_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_change_set("test-change_set_name", )


async def test_delete_generated_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_generated_template("test-generated_template_name", )
    mock_client.call.assert_called_once()


async def test_delete_generated_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_generated_template("test-generated_template_name", )


async def test_delete_stack_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stack_instances("test-stack_set_name", [], True, )
    mock_client.call.assert_called_once()


async def test_delete_stack_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stack_instances("test-stack_set_name", [], True, )


async def test_delete_stack_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stack_set("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_delete_stack_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stack_set("test-stack_set_name", )


async def test_deregister_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_type()
    mock_client.call.assert_called_once()


async def test_deregister_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_type()


async def test_describe_account_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_limits()
    mock_client.call.assert_called_once()


async def test_describe_account_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_limits()


async def test_describe_change_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_change_set("test-change_set_name", )
    mock_client.call.assert_called_once()


async def test_describe_change_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_change_set("test-change_set_name", )


async def test_describe_change_set_hooks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_change_set_hooks("test-change_set_name", )
    mock_client.call.assert_called_once()


async def test_describe_change_set_hooks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_change_set_hooks("test-change_set_name", )


async def test_describe_generated_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_generated_template("test-generated_template_name", )
    mock_client.call.assert_called_once()


async def test_describe_generated_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_generated_template("test-generated_template_name", )


async def test_describe_organizations_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_organizations_access()
    mock_client.call.assert_called_once()


async def test_describe_organizations_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organizations_access()


async def test_describe_publisher(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_publisher()
    mock_client.call.assert_called_once()


async def test_describe_publisher_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_publisher()


async def test_describe_resource_scan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_resource_scan("test-resource_scan_id", )
    mock_client.call.assert_called_once()


async def test_describe_resource_scan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resource_scan("test-resource_scan_id", )


async def test_describe_stack_drift_detection_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_drift_detection_status("test-stack_drift_detection_id", )
    mock_client.call.assert_called_once()


async def test_describe_stack_drift_detection_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_drift_detection_status("test-stack_drift_detection_id", )


async def test_describe_stack_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_events("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_describe_stack_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_events("test-stack_name", )


async def test_describe_stack_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_instance("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", )
    mock_client.call.assert_called_once()


async def test_describe_stack_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_instance("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", )


async def test_describe_stack_refactor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_refactor("test-stack_refactor_id", )
    mock_client.call.assert_called_once()


async def test_describe_stack_refactor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_refactor("test-stack_refactor_id", )


async def test_describe_stack_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_resource("test-stack_name", "test-logical_resource_id", )
    mock_client.call.assert_called_once()


async def test_describe_stack_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_resource("test-stack_name", "test-logical_resource_id", )


async def test_describe_stack_resource_drifts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_resource_drifts("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_describe_stack_resource_drifts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_resource_drifts("test-stack_name", )


async def test_describe_stack_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_resources()
    mock_client.call.assert_called_once()


async def test_describe_stack_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_resources()


async def test_describe_stack_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_set("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_describe_stack_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_set("test-stack_set_name", )


async def test_describe_stack_set_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stack_set_operation("test-stack_set_name", "test-operation_id", )
    mock_client.call.assert_called_once()


async def test_describe_stack_set_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stack_set_operation("test-stack_set_name", "test-operation_id", )


async def test_describe_stacks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stacks()
    mock_client.call.assert_called_once()


async def test_describe_stacks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stacks()


async def test_describe_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_type()
    mock_client.call.assert_called_once()


async def test_describe_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_type()


async def test_describe_type_registration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_type_registration("test-registration_token", )
    mock_client.call.assert_called_once()


async def test_describe_type_registration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_type_registration("test-registration_token", )


async def test_detect_stack_drift(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await detect_stack_drift("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_detect_stack_drift_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detect_stack_drift("test-stack_name", )


async def test_detect_stack_resource_drift(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await detect_stack_resource_drift("test-stack_name", "test-logical_resource_id", )
    mock_client.call.assert_called_once()


async def test_detect_stack_resource_drift_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detect_stack_resource_drift("test-stack_name", "test-logical_resource_id", )


async def test_detect_stack_set_drift(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await detect_stack_set_drift("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_detect_stack_set_drift_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detect_stack_set_drift("test-stack_set_name", )


async def test_estimate_template_cost(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await estimate_template_cost()
    mock_client.call.assert_called_once()


async def test_estimate_template_cost_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await estimate_template_cost()


async def test_execute_change_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_change_set("test-change_set_name", )
    mock_client.call.assert_called_once()


async def test_execute_change_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_change_set("test-change_set_name", )


async def test_execute_stack_refactor(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_stack_refactor("test-stack_refactor_id", )
    mock_client.call.assert_called_once()


async def test_execute_stack_refactor_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_stack_refactor("test-stack_refactor_id", )


async def test_get_generated_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_generated_template("test-generated_template_name", )
    mock_client.call.assert_called_once()


async def test_get_generated_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_generated_template("test-generated_template_name", )


async def test_get_hook_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_hook_result()
    mock_client.call.assert_called_once()


async def test_get_hook_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_hook_result()


async def test_get_stack_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_stack_policy("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_get_stack_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_stack_policy("test-stack_name", )


async def test_get_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_template()
    mock_client.call.assert_called_once()


async def test_get_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_template()


async def test_get_template_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_template_summary()
    mock_client.call.assert_called_once()


async def test_get_template_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_template_summary()


async def test_import_stacks_to_stack_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_stacks_to_stack_set("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_import_stacks_to_stack_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_stacks_to_stack_set("test-stack_set_name", )


async def test_list_change_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_change_sets("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_list_change_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_change_sets("test-stack_name", )


async def test_list_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_exports()
    mock_client.call.assert_called_once()


async def test_list_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_exports()


async def test_list_generated_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_generated_templates()
    mock_client.call.assert_called_once()


async def test_list_generated_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_generated_templates()


async def test_list_hook_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_hook_results()
    mock_client.call.assert_called_once()


async def test_list_hook_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_hook_results()


async def test_list_imports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_imports("test-export_name", )
    mock_client.call.assert_called_once()


async def test_list_imports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_imports("test-export_name", )


async def test_list_resource_scan_related_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_scan_related_resources("test-resource_scan_id", [], )
    mock_client.call.assert_called_once()


async def test_list_resource_scan_related_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_scan_related_resources("test-resource_scan_id", [], )


async def test_list_resource_scan_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_scan_resources("test-resource_scan_id", )
    mock_client.call.assert_called_once()


async def test_list_resource_scan_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_scan_resources("test-resource_scan_id", )


async def test_list_resource_scans(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_scans()
    mock_client.call.assert_called_once()


async def test_list_resource_scans_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_scans()


async def test_list_stack_instance_resource_drifts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_instance_resource_drifts("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", "test-operation_id", )
    mock_client.call.assert_called_once()


async def test_list_stack_instance_resource_drifts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_instance_resource_drifts("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", "test-operation_id", )


async def test_list_stack_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_instances("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_list_stack_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_instances("test-stack_set_name", )


async def test_list_stack_refactor_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_refactor_actions("test-stack_refactor_id", )
    mock_client.call.assert_called_once()


async def test_list_stack_refactor_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_refactor_actions("test-stack_refactor_id", )


async def test_list_stack_refactors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_refactors()
    mock_client.call.assert_called_once()


async def test_list_stack_refactors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_refactors()


async def test_list_stack_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_resources("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_list_stack_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_resources("test-stack_name", )


async def test_list_stack_set_auto_deployment_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_set_auto_deployment_targets("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_list_stack_set_auto_deployment_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_set_auto_deployment_targets("test-stack_set_name", )


async def test_list_stack_set_operation_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_set_operation_results("test-stack_set_name", "test-operation_id", )
    mock_client.call.assert_called_once()


async def test_list_stack_set_operation_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_set_operation_results("test-stack_set_name", "test-operation_id", )


async def test_list_stack_set_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_set_operations("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_list_stack_set_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_set_operations("test-stack_set_name", )


async def test_list_stack_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stack_sets()
    mock_client.call.assert_called_once()


async def test_list_stack_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stack_sets()


async def test_list_type_registrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_type_registrations()
    mock_client.call.assert_called_once()


async def test_list_type_registrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_type_registrations()


async def test_list_type_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_type_versions()
    mock_client.call.assert_called_once()


async def test_list_type_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_type_versions()


async def test_list_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_types()
    mock_client.call.assert_called_once()


async def test_list_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_types()


async def test_publish_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await publish_type()
    mock_client.call.assert_called_once()


async def test_publish_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await publish_type()


async def test_record_handler_progress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await record_handler_progress("test-bearer_token", "test-operation_status", )
    mock_client.call.assert_called_once()


async def test_record_handler_progress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await record_handler_progress("test-bearer_token", "test-operation_status", )


async def test_register_publisher(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_publisher()
    mock_client.call.assert_called_once()


async def test_register_publisher_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_publisher()


async def test_register_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_type("test-type_name", "test-schema_handler_package", )
    mock_client.call.assert_called_once()


async def test_register_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_type("test-type_name", "test-schema_handler_package", )


async def test_rollback_stack(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await rollback_stack("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_rollback_stack_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rollback_stack("test-stack_name", )


async def test_run_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_type()
    mock_client.call.assert_called_once()


async def test_run_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_type()


async def test_set_stack_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_stack_policy("test-stack_name", )
    mock_client.call.assert_called_once()


async def test_set_stack_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_stack_policy("test-stack_name", )


async def test_set_type_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_type_configuration("test-configuration", )
    mock_client.call.assert_called_once()


async def test_set_type_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_type_configuration("test-configuration", )


async def test_set_type_default_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_type_default_version()
    mock_client.call.assert_called_once()


async def test_set_type_default_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_type_default_version()


async def test_signal_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await signal_resource("test-stack_name", "test-logical_resource_id", "test-unique_id", "test-status", )
    mock_client.call.assert_called_once()


async def test_signal_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await signal_resource("test-stack_name", "test-logical_resource_id", "test-unique_id", "test-status", )


async def test_start_resource_scan(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_resource_scan()
    mock_client.call.assert_called_once()


async def test_start_resource_scan_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_resource_scan()


async def test_stop_stack_set_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_stack_set_operation("test-stack_set_name", "test-operation_id", )
    mock_client.call.assert_called_once()


async def test_stop_stack_set_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_stack_set_operation("test-stack_set_name", "test-operation_id", )


async def test_update_generated_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_generated_template("test-generated_template_name", )
    mock_client.call.assert_called_once()


async def test_update_generated_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_generated_template("test-generated_template_name", )


async def test_update_stack_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stack_instances("test-stack_set_name", [], )
    mock_client.call.assert_called_once()


async def test_update_stack_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stack_instances("test-stack_set_name", [], )


async def test_update_stack_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stack_set("test-stack_set_name", )
    mock_client.call.assert_called_once()


async def test_update_stack_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stack_set("test-stack_set_name", )


async def test_update_termination_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_termination_protection(True, "test-stack_name", )
    mock_client.call.assert_called_once()


async def test_update_termination_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_termination_protection(True, "test-stack_name", )


async def test_validate_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_template()
    mock_client.call.assert_called_once()


async def test_validate_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudformation.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_template()


@pytest.mark.asyncio
async def test_activate_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import activate_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await activate_type(type_value="test-type_value", public_type_arn="test-public_type_arn", publisher_id=True, type_name="test-type_name", type_name_alias="test-type_name_alias", auto_update=True, logging_config={}, execution_role_arn="test-execution_role_arn", version_bump="test-version_bump", major_version="test-major_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_update_stack_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import cancel_update_stack
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await cancel_update_stack("test-stack_name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_continue_update_rollback_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import continue_update_rollback
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await continue_update_rollback("test-stack_name", role_arn="test-role_arn", resources_to_skip="test-resources_to_skip", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_change_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import create_change_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await create_change_set("test-stack_name", "test-change_set_name", template_body="test-template_body", template_url="test-template_url", use_previous_template=True, parameters="test-parameters", capabilities="test-capabilities", resource_types="test-resource_types", role_arn="test-role_arn", rollback_configuration={}, notification_ar_ns="test-notification_ar_ns", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", description="test-description", change_set_type="test-change_set_type", resources_to_import=1, include_nested_stacks=True, on_stack_failure="test-on_stack_failure", import_existing_resources=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_generated_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import create_generated_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await create_generated_template("test-generated_template_name", resources="test-resources", stack_name="test-stack_name", template_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stack_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import create_stack_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await create_stack_instances("test-stack_set_name", "test-regions", accounts=1, deployment_targets="test-deployment_targets", parameter_overrides="test-parameter_overrides", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stack_refactor_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import create_stack_refactor
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await create_stack_refactor({}, description="test-description", enable_stack_creation=True, resource_mappings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stack_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import create_stack_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await create_stack_set("test-stack_set_name", description="test-description", template_body="test-template_body", template_url="test-template_url", stack_id="test-stack_id", parameters="test-parameters", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], administration_role_arn="test-administration_role_arn", execution_role_name="test-execution_role_name", permission_model="test-permission_model", auto_deployment=True, call_as="test-call_as", client_request_token="test-client_request_token", managed_execution="test-managed_execution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deactivate_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import deactivate_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await deactivate_type(type_name="test-type_name", type_value="test-type_value", arn="test-arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_change_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import delete_change_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await delete_change_set("test-change_set_name", stack_name="test-stack_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_stack_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import delete_stack_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await delete_stack_instances("test-stack_set_name", "test-regions", "test-retain_stacks", accounts=1, deployment_targets="test-deployment_targets", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_stack_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import delete_stack_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await delete_stack_set("test-stack_set_name", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import deregister_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await deregister_type(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_limits_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_account_limits
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_account_limits(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_change_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_change_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_change_set("test-change_set_name", stack_name="test-stack_name", next_token="test-next_token", include_property_values=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_change_set_hooks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_change_set_hooks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_change_set_hooks("test-change_set_name", stack_name="test-stack_name", next_token="test-next_token", logical_resource_id="test-logical_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_organizations_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_organizations_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_organizations_access(call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_publisher_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_publisher
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_publisher(publisher_id=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_events("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_instance("test-stack_set_name", 1, "test-stack_instance_region", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_resource_drifts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_resource_drifts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_resource_drifts("test-stack_name", stack_resource_drift_status_filters="test-stack_resource_drift_status_filters", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_resources(stack_name="test-stack_name", logical_resource_id="test-logical_resource_id", physical_resource_id="test-physical_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_set("test-stack_set_name", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stack_set_operation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stack_set_operation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stack_set_operation("test-stack_set_name", "test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stacks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_stacks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_stacks(stack_name="test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import describe_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await describe_type(type_value="test-type_value", type_name="test-type_name", arn="test-arn", version_id="test-version_id", publisher_id=True, public_version_number="test-public_version_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detect_stack_drift_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import detect_stack_drift
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await detect_stack_drift("test-stack_name", logical_resource_ids="test-logical_resource_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detect_stack_set_drift_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import detect_stack_set_drift
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await detect_stack_set_drift("test-stack_set_name", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_estimate_template_cost_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import estimate_template_cost
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await estimate_template_cost(template_body="test-template_body", template_url="test-template_url", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_change_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import execute_change_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await execute_change_set("test-change_set_name", stack_name="test-stack_name", client_request_token="test-client_request_token", disable_rollback=True, retain_except_on_create="test-retain_except_on_create", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_generated_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import get_generated_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await get_generated_template("test-generated_template_name", format="test-format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_hook_result_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import get_hook_result
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await get_hook_result(hook_result_id="test-hook_result_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import get_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await get_template(stack_name="test-stack_name", change_set_name="test-change_set_name", template_stage="test-template_stage", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_template_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import get_template_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await get_template_summary(template_body="test-template_body", template_url="test-template_url", stack_name="test-stack_name", stack_set_name="test-stack_set_name", call_as="test-call_as", template_summary_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_stacks_to_stack_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import import_stacks_to_stack_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await import_stacks_to_stack_set("test-stack_set_name", stack_ids="test-stack_ids", stack_ids_url="test-stack_ids_url", organizational_unit_ids="test-organizational_unit_ids", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_change_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_change_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_change_sets("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_exports(next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_generated_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_generated_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_generated_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_hook_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_hook_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_hook_results(target_type="test-target_type", target_id="test-target_id", type_arn="test-type_arn", status="test-status", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_imports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_imports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_imports(1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_scan_related_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_resource_scan_related_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_resource_scan_related_resources("test-resource_scan_id", "test-resources", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_scan_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_resource_scan_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_resource_scan_resources("test-resource_scan_id", resource_identifier="test-resource_identifier", resource_type_prefix="test-resource_type_prefix", tag_key="test-tag_key", tag_value="test-tag_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_scans_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_resource_scans
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_resource_scans(next_token="test-next_token", max_results=1, scan_type_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_instance_resource_drifts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_instance_resource_drifts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_instance_resource_drifts("test-stack_set_name", 1, "test-stack_instance_region", "test-operation_id", next_token="test-next_token", max_results=1, stack_instance_resource_drift_statuses="test-stack_instance_resource_drift_statuses", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_instances("test-stack_set_name", next_token="test-next_token", max_results=1, filters=[{}], stack_instance_account=1, stack_instance_region="test-stack_instance_region", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_refactor_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_refactor_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_refactor_actions("test-stack_refactor_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_refactors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_refactors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_refactors(execution_status_filter=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_resources("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_set_auto_deployment_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_set_auto_deployment_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_set_auto_deployment_targets("test-stack_set_name", next_token="test-next_token", max_results=1, call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_set_operation_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_set_operation_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_set_operation_results("test-stack_set_name", "test-operation_id", next_token="test-next_token", max_results=1, call_as="test-call_as", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_set_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_set_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_set_operations("test-stack_set_name", next_token="test-next_token", max_results=1, call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stack_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_stack_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_stack_sets(next_token="test-next_token", max_results=1, status="test-status", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_type_registrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_type_registrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_type_registrations(type_value="test-type_value", type_name="test-type_name", type_arn="test-type_arn", registration_status_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_type_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_type_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_type_versions(type_value="test-type_value", type_name="test-type_name", arn="test-arn", max_results=1, next_token="test-next_token", deprecated_status="test-deprecated_status", publisher_id=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import list_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await list_types(visibility="test-visibility", provisioning_type="test-provisioning_type", deprecated_status="test-deprecated_status", type_value="test-type_value", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_publish_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import publish_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await publish_type(type_value="test-type_value", arn="test-arn", type_name="test-type_name", public_version_number="test-public_version_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_record_handler_progress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import record_handler_progress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await record_handler_progress("test-bearer_token", "test-operation_status", current_operation_status="test-current_operation_status", status_message="test-status_message", error_code="test-error_code", resource_model="test-resource_model", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_publisher_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import register_publisher
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await register_publisher(accept_terms_and_conditions="test-accept_terms_and_conditions", connection_arn="test-connection_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import register_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await register_type("test-type_name", "test-schema_handler_package", type_value="test-type_value", logging_config={}, execution_role_arn="test-execution_role_arn", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_rollback_stack_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import rollback_stack
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await rollback_stack("test-stack_name", role_arn="test-role_arn", client_request_token="test-client_request_token", retain_except_on_create="test-retain_except_on_create", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import run_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await run_type(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", log_delivery_bucket="test-log_delivery_bucket", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_stack_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import set_stack_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await set_stack_policy("test-stack_name", stack_policy_body="test-stack_policy_body", stack_policy_url="test-stack_policy_url", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_type_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import set_type_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await set_type_configuration({}, type_arn="test-type_arn", configuration_alias={}, type_name="test-type_name", type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_type_default_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import set_type_default_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await set_type_default_version(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_resource_scan_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import start_resource_scan
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await start_resource_scan(client_request_token="test-client_request_token", scan_filters="test-scan_filters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_stack_set_operation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import stop_stack_set_operation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await stop_stack_set_operation("test-stack_set_name", "test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_generated_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import update_generated_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await update_generated_template("test-generated_template_name", new_generated_template_name="test-new_generated_template_name", add_resources="test-add_resources", remove_resources="test-remove_resources", refresh_all_resources="test-refresh_all_resources", template_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stack_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import update_stack_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await update_stack_instances("test-stack_set_name", "test-regions", accounts=1, deployment_targets="test-deployment_targets", parameter_overrides="test-parameter_overrides", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stack_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import update_stack_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await update_stack_set("test-stack_set_name", description="test-description", template_body="test-template_body", template_url="test-template_url", use_previous_template=True, parameters="test-parameters", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], operation_preferences="test-operation_preferences", administration_role_arn="test-administration_role_arn", execution_role_name="test-execution_role_name", deployment_targets="test-deployment_targets", permission_model="test-permission_model", auto_deployment=True, operation_id="test-operation_id", accounts=1, regions="test-regions", call_as="test-call_as", managed_execution="test-managed_execution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_validate_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudformation import validate_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudformation.async_client", lambda *a, **kw: mock_client)
    await validate_template(template_body="test-template_body", template_url="test-template_url", region_name="us-east-1")
    mock_client.call.assert_called_once()
