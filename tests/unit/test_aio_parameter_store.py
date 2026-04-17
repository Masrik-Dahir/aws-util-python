"""Tests for aws_util.aio.parameter_store — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.parameter_store import (
    delete_parameter,
    delete_parameters,
    describe_parameters,
    get_parameter,
    get_parameters_batch,
    get_parameters_by_path,
    put_parameter,
    add_tags_to_resource,
    associate_ops_item_related_item,
    cancel_command,
    cancel_maintenance_window_execution,
    create_activation,
    create_association,
    create_association_batch,
    create_document,
    create_maintenance_window,
    create_ops_item,
    create_ops_metadata,
    create_patch_baseline,
    create_resource_data_sync,
    delete_activation,
    delete_association,
    delete_document,
    delete_inventory,
    delete_maintenance_window,
    delete_ops_item,
    delete_ops_metadata,
    delete_patch_baseline,
    delete_resource_data_sync,
    delete_resource_policy,
    deregister_managed_instance,
    deregister_patch_baseline_for_patch_group,
    deregister_target_from_maintenance_window,
    deregister_task_from_maintenance_window,
    describe_activations,
    describe_association,
    describe_association_execution_targets,
    describe_association_executions,
    describe_automation_executions,
    describe_automation_step_executions,
    describe_available_patches,
    describe_document,
    describe_document_permission,
    describe_effective_instance_associations,
    describe_effective_patches_for_patch_baseline,
    describe_instance_associations_status,
    describe_instance_information,
    describe_instance_patch_states,
    describe_instance_patch_states_for_patch_group,
    describe_instance_patches,
    describe_instance_properties,
    describe_inventory_deletions,
    describe_maintenance_window_execution_task_invocations,
    describe_maintenance_window_execution_tasks,
    describe_maintenance_window_executions,
    describe_maintenance_window_schedule,
    describe_maintenance_window_targets,
    describe_maintenance_window_tasks,
    describe_maintenance_windows,
    describe_maintenance_windows_for_target,
    describe_ops_items,
    describe_patch_baselines,
    describe_patch_group_state,
    describe_patch_groups,
    describe_patch_properties,
    describe_sessions,
    disassociate_ops_item_related_item,
    get_access_token,
    get_automation_execution,
    get_calendar_state,
    get_command_invocation,
    get_connection_status,
    get_default_patch_baseline,
    get_deployable_patch_snapshot_for_instance,
    get_document,
    get_execution_preview,
    get_inventory,
    get_inventory_schema,
    get_maintenance_window,
    get_maintenance_window_execution,
    get_maintenance_window_execution_task,
    get_maintenance_window_execution_task_invocation,
    get_maintenance_window_task,
    get_ops_item,
    get_ops_metadata,
    get_ops_summary,
    get_parameter_history,
    get_parameters,
    get_patch_baseline,
    get_patch_baseline_for_patch_group,
    get_resource_policies,
    get_service_setting,
    label_parameter_version,
    list_association_versions,
    list_associations,
    list_command_invocations,
    list_commands,
    list_compliance_items,
    list_compliance_summaries,
    list_document_metadata_history,
    list_document_versions,
    list_documents,
    list_inventory_entries,
    list_nodes,
    list_nodes_summary,
    list_ops_item_events,
    list_ops_item_related_items,
    list_ops_metadata,
    list_resource_compliance_summaries,
    list_resource_data_sync,
    list_tags_for_resource,
    modify_document_permission,
    put_compliance_items,
    put_inventory,
    put_resource_policy,
    register_default_patch_baseline,
    register_patch_baseline_for_patch_group,
    register_target_with_maintenance_window,
    register_task_with_maintenance_window,
    remove_tags_from_resource,
    reset_service_setting,
    resume_session,
    send_automation_signal,
    send_command,
    start_access_request,
    start_associations_once,
    start_automation_execution,
    start_change_request_execution,
    start_execution_preview,
    start_session,
    stop_automation_execution,
    terminate_session,
    unlabel_parameter_version,
    update_association,
    update_association_status,
    update_document,
    update_document_default_version,
    update_document_metadata,
    update_maintenance_window,
    update_maintenance_window_target,
    update_maintenance_window_task,
    update_managed_instance_role,
    update_ops_item,
    update_ops_metadata,
    update_patch_baseline,
    update_resource_data_sync,
    update_service_setting,
)


def _mc(return_value=None, side_effect=None):
    c = AsyncMock()
    if side_effect:
        c.call.side_effect = side_effect
        c.paginate.side_effect = side_effect
    else:
        c.call.return_value = return_value or {}
        c.paginate.return_value = return_value if isinstance(return_value, list) else []
    return c


# ---------------------------------------------------------------------------
# get_parameters_by_path
# ---------------------------------------------------------------------------


async def test_get_parameters_by_path(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = [
        {"Name": "/app/db/host", "Value": "localhost"},
        {"Name": "/app/db/port", "Value": "5432"},
    ]
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    r = await get_parameters_by_path("/app/db/")
    assert r == {"/app/db/host": "localhost", "/app/db/port": "5432"}


async def test_get_parameters_by_path_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_parameters_by_path failed"):
        await get_parameters_by_path("/app/")


# ---------------------------------------------------------------------------
# get_parameters_batch
# ---------------------------------------------------------------------------


async def test_get_parameters_batch(monkeypatch):
    mc = _mc({"Parameters": [{"Name": "a", "Value": "1"}, {"Name": "b", "Value": "2"}]})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    r = await get_parameters_batch(["a", "b"])
    assert r == {"a": "1", "b": "2"}


async def test_get_parameters_batch_empty(monkeypatch):
    mc = _mc({})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    r = await get_parameters_batch(["a"])
    assert r == {}


async def test_get_parameters_batch_too_many():
    with pytest.raises(ValueError, match="at most 10"):
        await get_parameters_batch([f"p{i}" for i in range(11)])


async def test_get_parameters_batch_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_parameters_batch failed"):
        await get_parameters_batch(["a"])


# ---------------------------------------------------------------------------
# put_parameter
# ---------------------------------------------------------------------------


async def test_put_parameter(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    await put_parameter("/app/key", "val")
    mc.call.assert_called_once()


async def test_put_parameter_with_description(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    await put_parameter("/app/key", "val", description="desc")
    assert mc.call.call_args[1]["Description"] == "desc"


async def test_put_parameter_no_description(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    await put_parameter("/app/key", "val", description="")
    assert "Description" not in mc.call.call_args[1]


async def test_put_parameter_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to put SSM parameter"):
        await put_parameter("/x", "v")


# ---------------------------------------------------------------------------
# delete_parameter
# ---------------------------------------------------------------------------


async def test_delete_parameter(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    await delete_parameter("/app/key")
    mc.call.assert_called_once()


async def test_delete_parameter_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to delete SSM parameter"):
        await delete_parameter("/x")


# ---------------------------------------------------------------------------
# get_parameter
# ---------------------------------------------------------------------------


async def test_get_parameter(monkeypatch):
    mc = _mc({"Parameter": {"Value": "myval"}})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    assert await get_parameter("/app/key") == "myval"


async def test_get_parameter_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Error resolving SSM parameter"):
        await get_parameter("/x")


# ---------------------------------------------------------------------------
# describe_parameters
# ---------------------------------------------------------------------------


async def test_describe_parameters(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = [
        {"Name": "/app/key1", "Type": "String"},
        {"Name": "/app/key2", "Type": "SecureString"},
    ]
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    r = await describe_parameters()
    assert r == [
        {"Name": "/app/key1", "Type": "String"},
        {"Name": "/app/key2", "Type": "SecureString"},
    ]


async def test_describe_parameters_with_filters(monkeypatch):
    mc = _mc()
    mc.paginate.return_value = [{"Name": "/app/key1", "Type": "String"}]
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    filters = [{"Key": "Name", "Values": ["/app/key1"]}]
    r = await describe_parameters(filters=filters)
    assert r == [{"Name": "/app/key1", "Type": "String"}]
    mc.paginate.assert_called_once()
    call_kwargs = mc.paginate.call_args[1]
    assert call_kwargs["ParameterFilters"] == filters


async def test_describe_parameters_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_parameters failed"):
        await describe_parameters()


# ---------------------------------------------------------------------------
# delete_parameters
# ---------------------------------------------------------------------------


async def test_delete_parameters(monkeypatch):
    mc = _mc({"DeletedParameters": ["/app/a", "/app/b"]})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    r = await delete_parameters(["/app/a", "/app/b"])
    assert r == ["/app/a", "/app/b"]


async def test_delete_parameters_too_many():
    with pytest.raises(ValueError, match="at most 10"):
        await delete_parameters([f"/p{i}" for i in range(11)])


async def test_delete_parameters_error(monkeypatch):
    mc = _mc(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_parameters failed"):
        await delete_parameters(["/x"])


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_type", "test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_type", "test-resource_id", [], )


async def test_associate_ops_item_related_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_ops_item_related_item("test-ops_item_id", "test-association_type", "test-resource_type", "test-resource_uri", )
    mock_client.call.assert_called_once()


async def test_associate_ops_item_related_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_ops_item_related_item("test-ops_item_id", "test-association_type", "test-resource_type", "test-resource_uri", )


async def test_cancel_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_command("test-command_id", )
    mock_client.call.assert_called_once()


async def test_cancel_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_command("test-command_id", )


async def test_cancel_maintenance_window_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_maintenance_window_execution("test-window_execution_id", )
    mock_client.call.assert_called_once()


async def test_cancel_maintenance_window_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_maintenance_window_execution("test-window_execution_id", )


async def test_create_activation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_activation("test-iam_role", )
    mock_client.call.assert_called_once()


async def test_create_activation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_activation("test-iam_role", )


async def test_create_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_association("test-name", )
    mock_client.call.assert_called_once()


async def test_create_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_association("test-name", )


async def test_create_association_batch(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_association_batch([], )
    mock_client.call.assert_called_once()


async def test_create_association_batch_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_association_batch([], )


async def test_create_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_document("test-content", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_document("test-content", "test-name", )


async def test_create_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_maintenance_window("test-name", "test-schedule", 1, 1, True, )
    mock_client.call.assert_called_once()


async def test_create_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_maintenance_window("test-name", "test-schedule", 1, 1, True, )


async def test_create_ops_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ops_item("test-description", "test-source", "test-title", )
    mock_client.call.assert_called_once()


async def test_create_ops_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ops_item("test-description", "test-source", "test-title", )


async def test_create_ops_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ops_metadata("test-resource_id", )
    mock_client.call.assert_called_once()


async def test_create_ops_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ops_metadata("test-resource_id", )


async def test_create_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_patch_baseline("test-name", )
    mock_client.call.assert_called_once()


async def test_create_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_patch_baseline("test-name", )


async def test_create_resource_data_sync(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_resource_data_sync("test-sync_name", )
    mock_client.call.assert_called_once()


async def test_create_resource_data_sync_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_data_sync("test-sync_name", )


async def test_delete_activation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_activation("test-activation_id", )
    mock_client.call.assert_called_once()


async def test_delete_activation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_activation("test-activation_id", )


async def test_delete_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_association()
    mock_client.call.assert_called_once()


async def test_delete_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_association()


async def test_delete_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_document("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_document("test-name", )


async def test_delete_inventory(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_inventory("test-type_name", )
    mock_client.call.assert_called_once()


async def test_delete_inventory_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_inventory("test-type_name", )


async def test_delete_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_maintenance_window("test-window_id", )
    mock_client.call.assert_called_once()


async def test_delete_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_maintenance_window("test-window_id", )


async def test_delete_ops_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ops_item("test-ops_item_id", )
    mock_client.call.assert_called_once()


async def test_delete_ops_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ops_item("test-ops_item_id", )


async def test_delete_ops_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ops_metadata("test-ops_metadata_arn", )
    mock_client.call.assert_called_once()


async def test_delete_ops_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ops_metadata("test-ops_metadata_arn", )


async def test_delete_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_patch_baseline("test-baseline_id", )
    mock_client.call.assert_called_once()


async def test_delete_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_patch_baseline("test-baseline_id", )


async def test_delete_resource_data_sync(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_data_sync("test-sync_name", )
    mock_client.call.assert_called_once()


async def test_delete_resource_data_sync_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_data_sync("test-sync_name", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", "test-policy_id", "test-policy_hash", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", "test-policy_id", "test-policy_hash", )


async def test_deregister_managed_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_managed_instance("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_deregister_managed_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_managed_instance("test-instance_id", )


async def test_deregister_patch_baseline_for_patch_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", )
    mock_client.call.assert_called_once()


async def test_deregister_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", )


async def test_deregister_target_from_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", )
    mock_client.call.assert_called_once()


async def test_deregister_target_from_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", )


async def test_deregister_task_from_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_task_from_maintenance_window("test-window_id", "test-window_task_id", )
    mock_client.call.assert_called_once()


async def test_deregister_task_from_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_task_from_maintenance_window("test-window_id", "test-window_task_id", )


async def test_describe_activations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_activations()
    mock_client.call.assert_called_once()


async def test_describe_activations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_activations()


async def test_describe_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_association()
    mock_client.call.assert_called_once()


async def test_describe_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_association()


async def test_describe_association_execution_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_association_execution_targets("test-association_id", "test-execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_association_execution_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_association_execution_targets("test-association_id", "test-execution_id", )


async def test_describe_association_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_association_executions("test-association_id", )
    mock_client.call.assert_called_once()


async def test_describe_association_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_association_executions("test-association_id", )


async def test_describe_automation_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_automation_executions()
    mock_client.call.assert_called_once()


async def test_describe_automation_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_automation_executions()


async def test_describe_automation_step_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_automation_step_executions("test-automation_execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_automation_step_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_automation_step_executions("test-automation_execution_id", )


async def test_describe_available_patches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_available_patches()
    mock_client.call.assert_called_once()


async def test_describe_available_patches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_available_patches()


async def test_describe_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_document("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_document("test-name", )


async def test_describe_document_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_document_permission("test-name", "test-permission_type", )
    mock_client.call.assert_called_once()


async def test_describe_document_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_document_permission("test-name", "test-permission_type", )


async def test_describe_effective_instance_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_effective_instance_associations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_effective_instance_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_effective_instance_associations("test-instance_id", )


async def test_describe_effective_patches_for_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_effective_patches_for_patch_baseline("test-baseline_id", )
    mock_client.call.assert_called_once()


async def test_describe_effective_patches_for_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_effective_patches_for_patch_baseline("test-baseline_id", )


async def test_describe_instance_associations_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_associations_status("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_instance_associations_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_associations_status("test-instance_id", )


async def test_describe_instance_information(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_information()
    mock_client.call.assert_called_once()


async def test_describe_instance_information_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_information()


async def test_describe_instance_patch_states(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_patch_states([], )
    mock_client.call.assert_called_once()


async def test_describe_instance_patch_states_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_patch_states([], )


async def test_describe_instance_patch_states_for_patch_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_patch_states_for_patch_group("test-patch_group", )
    mock_client.call.assert_called_once()


async def test_describe_instance_patch_states_for_patch_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_patch_states_for_patch_group("test-patch_group", )


async def test_describe_instance_patches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_patches("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_instance_patches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_patches("test-instance_id", )


async def test_describe_instance_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_properties()
    mock_client.call.assert_called_once()


async def test_describe_instance_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_properties()


async def test_describe_inventory_deletions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_inventory_deletions()
    mock_client.call.assert_called_once()


async def test_describe_inventory_deletions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_inventory_deletions()


async def test_describe_maintenance_window_execution_task_invocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_execution_task_invocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", )


async def test_describe_maintenance_window_execution_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_execution_tasks("test-window_execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_execution_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_execution_tasks("test-window_execution_id", )


async def test_describe_maintenance_window_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_executions("test-window_id", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_executions("test-window_id", )


async def test_describe_maintenance_window_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_schedule()
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_schedule()


async def test_describe_maintenance_window_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_targets("test-window_id", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_targets("test-window_id", )


async def test_describe_maintenance_window_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_window_tasks("test-window_id", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_window_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_window_tasks("test-window_id", )


async def test_describe_maintenance_windows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_windows()
    mock_client.call.assert_called_once()


async def test_describe_maintenance_windows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_windows()


async def test_describe_maintenance_windows_for_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_windows_for_target([], "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_windows_for_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_windows_for_target([], "test-resource_type", )


async def test_describe_ops_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ops_items()
    mock_client.call.assert_called_once()


async def test_describe_ops_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ops_items()


async def test_describe_patch_baselines(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_patch_baselines()
    mock_client.call.assert_called_once()


async def test_describe_patch_baselines_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_patch_baselines()


async def test_describe_patch_group_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_patch_group_state("test-patch_group", )
    mock_client.call.assert_called_once()


async def test_describe_patch_group_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_patch_group_state("test-patch_group", )


async def test_describe_patch_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_patch_groups()
    mock_client.call.assert_called_once()


async def test_describe_patch_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_patch_groups()


async def test_describe_patch_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_patch_properties("test-operating_system", "test-property", )
    mock_client.call.assert_called_once()


async def test_describe_patch_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_patch_properties("test-operating_system", "test-property", )


async def test_describe_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_sessions("test-state", )
    mock_client.call.assert_called_once()


async def test_describe_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_sessions("test-state", )


async def test_disassociate_ops_item_related_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_ops_item_related_item("test-ops_item_id", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_ops_item_related_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_ops_item_related_item("test-ops_item_id", "test-association_id", )


async def test_get_access_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_access_token("test-access_request_id", )
    mock_client.call.assert_called_once()


async def test_get_access_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_access_token("test-access_request_id", )


async def test_get_automation_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_automation_execution("test-automation_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_automation_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_automation_execution("test-automation_execution_id", )


async def test_get_calendar_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_calendar_state([], )
    mock_client.call.assert_called_once()


async def test_get_calendar_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_calendar_state([], )


async def test_get_command_invocation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_command_invocation("test-command_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_command_invocation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_command_invocation("test-command_id", "test-instance_id", )


async def test_get_connection_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_connection_status("test-target", )
    mock_client.call.assert_called_once()


async def test_get_connection_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_connection_status("test-target", )


async def test_get_default_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_default_patch_baseline()
    mock_client.call.assert_called_once()


async def test_get_default_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_default_patch_baseline()


async def test_get_deployable_patch_snapshot_for_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_get_deployable_patch_snapshot_for_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", )


async def test_get_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_document("test-name", )
    mock_client.call.assert_called_once()


async def test_get_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_document("test-name", )


async def test_get_execution_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_execution_preview("test-execution_preview_id", )
    mock_client.call.assert_called_once()


async def test_get_execution_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_execution_preview("test-execution_preview_id", )


async def test_get_inventory(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_inventory()
    mock_client.call.assert_called_once()


async def test_get_inventory_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_inventory()


async def test_get_inventory_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_inventory_schema()
    mock_client.call.assert_called_once()


async def test_get_inventory_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_inventory_schema()


async def test_get_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_maintenance_window("test-window_id", )
    mock_client.call.assert_called_once()


async def test_get_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_maintenance_window("test-window_id", )


async def test_get_maintenance_window_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_maintenance_window_execution("test-window_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_maintenance_window_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_maintenance_window_execution("test-window_execution_id", )


async def test_get_maintenance_window_execution_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_maintenance_window_execution_task("test-window_execution_id", "test-task_id", )
    mock_client.call.assert_called_once()


async def test_get_maintenance_window_execution_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_maintenance_window_execution_task("test-window_execution_id", "test-task_id", )


async def test_get_maintenance_window_execution_task_invocation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_maintenance_window_execution_task_invocation("test-window_execution_id", "test-task_id", "test-invocation_id", )
    mock_client.call.assert_called_once()


async def test_get_maintenance_window_execution_task_invocation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_maintenance_window_execution_task_invocation("test-window_execution_id", "test-task_id", "test-invocation_id", )


async def test_get_maintenance_window_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_maintenance_window_task("test-window_id", "test-window_task_id", )
    mock_client.call.assert_called_once()


async def test_get_maintenance_window_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_maintenance_window_task("test-window_id", "test-window_task_id", )


async def test_get_ops_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ops_item("test-ops_item_id", )
    mock_client.call.assert_called_once()


async def test_get_ops_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ops_item("test-ops_item_id", )


async def test_get_ops_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ops_metadata("test-ops_metadata_arn", )
    mock_client.call.assert_called_once()


async def test_get_ops_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ops_metadata("test-ops_metadata_arn", )


async def test_get_ops_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ops_summary()
    mock_client.call.assert_called_once()


async def test_get_ops_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ops_summary()


async def test_get_parameter_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_parameter_history("test-name", )
    mock_client.call.assert_called_once()


async def test_get_parameter_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_parameter_history("test-name", )


async def test_get_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_parameters([], )
    mock_client.call.assert_called_once()


async def test_get_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_parameters([], )


async def test_get_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_patch_baseline("test-baseline_id", )
    mock_client.call.assert_called_once()


async def test_get_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_patch_baseline("test-baseline_id", )


async def test_get_patch_baseline_for_patch_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_patch_baseline_for_patch_group("test-patch_group", )
    mock_client.call.assert_called_once()


async def test_get_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_patch_baseline_for_patch_group("test-patch_group", )


async def test_get_resource_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policies("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policies("test-resource_arn", )


async def test_get_service_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_setting("test-setting_id", )
    mock_client.call.assert_called_once()


async def test_get_service_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_setting("test-setting_id", )


async def test_label_parameter_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await label_parameter_version("test-name", [], )
    mock_client.call.assert_called_once()


async def test_label_parameter_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await label_parameter_version("test-name", [], )


async def test_list_association_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_association_versions("test-association_id", )
    mock_client.call.assert_called_once()


async def test_list_association_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_association_versions("test-association_id", )


async def test_list_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associations()
    mock_client.call.assert_called_once()


async def test_list_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associations()


async def test_list_command_invocations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_command_invocations()
    mock_client.call.assert_called_once()


async def test_list_command_invocations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_command_invocations()


async def test_list_commands(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_commands()
    mock_client.call.assert_called_once()


async def test_list_commands_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_commands()


async def test_list_compliance_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_compliance_items()
    mock_client.call.assert_called_once()


async def test_list_compliance_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_compliance_items()


async def test_list_compliance_summaries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_compliance_summaries()
    mock_client.call.assert_called_once()


async def test_list_compliance_summaries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_compliance_summaries()


async def test_list_document_metadata_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_document_metadata_history("test-name", "test-metadata", )
    mock_client.call.assert_called_once()


async def test_list_document_metadata_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_document_metadata_history("test-name", "test-metadata", )


async def test_list_document_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_document_versions("test-name", )
    mock_client.call.assert_called_once()


async def test_list_document_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_document_versions("test-name", )


async def test_list_documents(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_documents()
    mock_client.call.assert_called_once()


async def test_list_documents_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_documents()


async def test_list_inventory_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_inventory_entries("test-instance_id", "test-type_name", )
    mock_client.call.assert_called_once()


async def test_list_inventory_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_inventory_entries("test-instance_id", "test-type_name", )


async def test_list_nodes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_nodes()
    mock_client.call.assert_called_once()


async def test_list_nodes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_nodes()


async def test_list_nodes_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_nodes_summary([], )
    mock_client.call.assert_called_once()


async def test_list_nodes_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_nodes_summary([], )


async def test_list_ops_item_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ops_item_events()
    mock_client.call.assert_called_once()


async def test_list_ops_item_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ops_item_events()


async def test_list_ops_item_related_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ops_item_related_items()
    mock_client.call.assert_called_once()


async def test_list_ops_item_related_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ops_item_related_items()


async def test_list_ops_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ops_metadata()
    mock_client.call.assert_called_once()


async def test_list_ops_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ops_metadata()


async def test_list_resource_compliance_summaries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_compliance_summaries()
    mock_client.call.assert_called_once()


async def test_list_resource_compliance_summaries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_compliance_summaries()


async def test_list_resource_data_sync(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_resource_data_sync()
    mock_client.call.assert_called_once()


async def test_list_resource_data_sync_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_data_sync()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_type", "test-resource_id", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_type", "test-resource_id", )


async def test_modify_document_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_document_permission("test-name", "test-permission_type", )
    mock_client.call.assert_called_once()


async def test_modify_document_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_document_permission("test-name", "test-permission_type", )


async def test_put_compliance_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", {}, [], )
    mock_client.call.assert_called_once()


async def test_put_compliance_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", {}, [], )


async def test_put_inventory(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_inventory("test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_put_inventory_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_inventory("test-instance_id", [], )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy", )


async def test_register_default_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_default_patch_baseline("test-baseline_id", )
    mock_client.call.assert_called_once()


async def test_register_default_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_default_patch_baseline("test-baseline_id", )


async def test_register_patch_baseline_for_patch_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", )
    mock_client.call.assert_called_once()


async def test_register_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", )


async def test_register_target_with_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_target_with_maintenance_window("test-window_id", "test-resource_type", [], )
    mock_client.call.assert_called_once()


async def test_register_target_with_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_target_with_maintenance_window("test-window_id", "test-resource_type", [], )


async def test_register_task_with_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", )
    mock_client.call.assert_called_once()


async def test_register_task_with_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_type", "test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_type", "test-resource_id", [], )


async def test_reset_service_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_service_setting("test-setting_id", )
    mock_client.call.assert_called_once()


async def test_reset_service_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_service_setting("test-setting_id", )


async def test_resume_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_session("test-session_id", )
    mock_client.call.assert_called_once()


async def test_resume_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_session("test-session_id", )


async def test_send_automation_signal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_automation_signal("test-automation_execution_id", "test-signal_type", )
    mock_client.call.assert_called_once()


async def test_send_automation_signal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_automation_signal("test-automation_execution_id", "test-signal_type", )


async def test_send_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_command("test-document_name", )
    mock_client.call.assert_called_once()


async def test_send_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_command("test-document_name", )


async def test_start_access_request(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_access_request("test-reason", [], )
    mock_client.call.assert_called_once()


async def test_start_access_request_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_access_request("test-reason", [], )


async def test_start_associations_once(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_associations_once([], )
    mock_client.call.assert_called_once()


async def test_start_associations_once_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_associations_once([], )


async def test_start_automation_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_automation_execution("test-document_name", )
    mock_client.call.assert_called_once()


async def test_start_automation_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_automation_execution("test-document_name", )


async def test_start_change_request_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_change_request_execution("test-document_name", [], )
    mock_client.call.assert_called_once()


async def test_start_change_request_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_change_request_execution("test-document_name", [], )


async def test_start_execution_preview(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_execution_preview("test-document_name", )
    mock_client.call.assert_called_once()


async def test_start_execution_preview_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_execution_preview("test-document_name", )


async def test_start_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_session("test-target", )
    mock_client.call.assert_called_once()


async def test_start_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_session("test-target", )


async def test_stop_automation_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_automation_execution("test-automation_execution_id", )
    mock_client.call.assert_called_once()


async def test_stop_automation_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_automation_execution("test-automation_execution_id", )


async def test_terminate_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await terminate_session("test-session_id", )
    mock_client.call.assert_called_once()


async def test_terminate_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await terminate_session("test-session_id", )


async def test_unlabel_parameter_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await unlabel_parameter_version("test-name", 1, [], )
    mock_client.call.assert_called_once()


async def test_unlabel_parameter_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unlabel_parameter_version("test-name", 1, [], )


async def test_update_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_association("test-association_id", )
    mock_client.call.assert_called_once()


async def test_update_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_association("test-association_id", )


async def test_update_association_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_association_status("test-name", "test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_association_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_association_status("test-name", "test-instance_id", {}, )


async def test_update_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_document("test-content", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_document("test-content", "test-name", )


async def test_update_document_default_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_document_default_version("test-name", "test-document_version", )
    mock_client.call.assert_called_once()


async def test_update_document_default_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_document_default_version("test-name", "test-document_version", )


async def test_update_document_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_document_metadata("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_document_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_document_metadata("test-name", {}, )


async def test_update_maintenance_window(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_maintenance_window("test-window_id", )
    mock_client.call.assert_called_once()


async def test_update_maintenance_window_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_maintenance_window("test-window_id", )


async def test_update_maintenance_window_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_maintenance_window_target("test-window_id", "test-window_target_id", )
    mock_client.call.assert_called_once()


async def test_update_maintenance_window_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_maintenance_window_target("test-window_id", "test-window_target_id", )


async def test_update_maintenance_window_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_maintenance_window_task("test-window_id", "test-window_task_id", )
    mock_client.call.assert_called_once()


async def test_update_maintenance_window_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_maintenance_window_task("test-window_id", "test-window_task_id", )


async def test_update_managed_instance_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_managed_instance_role("test-instance_id", "test-iam_role", )
    mock_client.call.assert_called_once()


async def test_update_managed_instance_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_managed_instance_role("test-instance_id", "test-iam_role", )


async def test_update_ops_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ops_item("test-ops_item_id", )
    mock_client.call.assert_called_once()


async def test_update_ops_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ops_item("test-ops_item_id", )


async def test_update_ops_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ops_metadata("test-ops_metadata_arn", )
    mock_client.call.assert_called_once()


async def test_update_ops_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ops_metadata("test-ops_metadata_arn", )


async def test_update_patch_baseline(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_patch_baseline("test-baseline_id", )
    mock_client.call.assert_called_once()


async def test_update_patch_baseline_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_patch_baseline("test-baseline_id", )


async def test_update_resource_data_sync(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_resource_data_sync("test-sync_name", "test-sync_type", {}, )
    mock_client.call.assert_called_once()


async def test_update_resource_data_sync_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_data_sync("test-sync_name", "test-sync_type", {}, )


async def test_update_service_setting(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_service_setting("test-setting_id", "test-setting_value", )
    mock_client.call.assert_called_once()


async def test_update_service_setting_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.parameter_store.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_service_setting("test-setting_id", "test-setting_value", )


@pytest.mark.asyncio
async def test_cancel_command_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import cancel_command
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await cancel_command("test-command_id", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_activation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_activation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_activation("test-iam_role", description="test-description", default_instance_name="test-default_instance_name", registration_limit=1, expiration_date="test-expiration_date", tags=[{"Key": "k", "Value": "v"}], registration_metadata="test-registration_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_association("test-name", document_version="test-document_version", instance_id="test-instance_id", parameters="test-parameters", targets="test-targets", schedule_expression="test-schedule_expression", output_location="test-output_location", association_name="test-association_name", automation_target_parameter_name=True, max_errors=1, max_concurrency=1, compliance_severity="test-compliance_severity", sync_compliance="test-sync_compliance", apply_only_at_cron_interval=True, calendar_names="test-calendar_names", target_locations="test-target_locations", schedule_offset="test-schedule_offset", duration=1, target_maps="test-target_maps", tags=[{"Key": "k", "Value": "v"}], alarm_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_document("test-content", "test-name", requires=True, attachments="test-attachments", display_name="test-display_name", version_name="test-version_name", document_type="test-document_type", document_format="test-document_format", target_type="test-target_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_maintenance_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_maintenance_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_maintenance_window("test-name", "test-schedule", 1, "test-cutoff", True, description="test-description", start_date="test-start_date", end_date="test-end_date", schedule_timezone="test-schedule_timezone", schedule_offset="test-schedule_offset", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ops_item_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_ops_item
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_ops_item("test-description", "test-source", "test-title", ops_item_type="test-ops_item_type", operational_data="test-operational_data", notifications="test-notifications", priority="test-priority", related_ops_items="test-related_ops_items", tags=[{"Key": "k", "Value": "v"}], category="test-category", severity="test-severity", actual_start_time="test-actual_start_time", actual_end_time="test-actual_end_time", planned_start_time="test-planned_start_time", planned_end_time="test-planned_end_time", account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ops_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_ops_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_ops_metadata("test-resource_id", metadata="test-metadata", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_patch_baseline_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_patch_baseline
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_patch_baseline("test-name", operating_system="test-operating_system", global_filters="test-global_filters", approval_rules="test-approval_rules", approved_patches=True, approved_patches_compliance_level=True, approved_patches_enable_non_security=True, rejected_patches="test-rejected_patches", rejected_patches_action="test-rejected_patches_action", description="test-description", sources="test-sources", available_security_updates_compliance_status="test-available_security_updates_compliance_status", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import create_resource_data_sync
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await create_resource_data_sync("test-sync_name", s3_destination="test-s3_destination", sync_type="test-sync_type", sync_source="test-sync_source", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import delete_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await delete_association(name="test-name", instance_id="test-instance_id", association_id="test-association_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import delete_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await delete_document("test-name", document_version="test-document_version", version_name="test-version_name", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_inventory_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import delete_inventory
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await delete_inventory("test-type_name", schema_delete_option="test-schema_delete_option", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import delete_resource_data_sync
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await delete_resource_data_sync("test-sync_name", sync_type="test-sync_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_target_from_maintenance_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import deregister_target_from_maintenance_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", safe="test-safe", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_activations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_activations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_activations(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_association(name="test-name", instance_id="test-instance_id", association_id="test-association_id", association_version="test-association_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_association_execution_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_association_execution_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_association_execution_targets("test-association_id", "test-execution_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_association_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_association_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_association_executions("test-association_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_automation_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_automation_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_automation_executions(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_automation_step_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_automation_step_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_automation_step_executions(True, filters=[{}], next_token="test-next_token", max_results=1, reverse_order="test-reverse_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_available_patches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_available_patches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_available_patches(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_document("test-name", document_version="test-document_version", version_name="test-version_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_document_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_document_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_document_permission("test-name", "test-permission_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_effective_instance_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_effective_instance_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_effective_instance_associations("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_effective_patches_for_patch_baseline_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_effective_patches_for_patch_baseline
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_effective_patches_for_patch_baseline("test-baseline_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_associations_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_associations_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_associations_status("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_information_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_information
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_information(instance_information_filter_list="test-instance_information_filter_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_patch_states_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_patch_states
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_patch_states("test-instance_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_patch_states_for_patch_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_patch_states_for_patch_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_patch_states_for_patch_group("test-patch_group", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_patches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_patches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_patches("test-instance_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_instance_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_instance_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_instance_properties(instance_property_filter_list="test-instance_property_filter_list", filters_with_operator="test-filters_with_operator", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_inventory_deletions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_inventory_deletions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_inventory_deletions(deletion_id="test-deletion_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_execution_task_invocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_execution_task_invocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_execution_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_execution_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_execution_tasks("test-window_execution_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_executions("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_schedule(window_id="test-window_id", targets="test-targets", resource_type="test-resource_type", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_targets("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_window_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_window_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_window_tasks("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_windows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_windows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_windows(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_maintenance_windows_for_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_maintenance_windows_for_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_maintenance_windows_for_target("test-targets", "test-resource_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_ops_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_ops_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_ops_items(ops_item_filters="test-ops_item_filters", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_patch_baselines_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_patch_baselines
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_patch_baselines(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_patch_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_patch_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_patch_groups(max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_patch_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_patch_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_patch_properties("test-operating_system", "test-property", patch_set="test-patch_set", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import describe_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await describe_sessions("test-state", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_calendar_state_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_calendar_state
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_calendar_state("test-calendar_names", at_time="test-at_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_command_invocation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_command_invocation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_command_invocation("test-command_id", "test-instance_id", plugin_name="test-plugin_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_default_patch_baseline_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_default_patch_baseline
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_default_patch_baseline(operating_system="test-operating_system", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_deployable_patch_snapshot_for_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_deployable_patch_snapshot_for_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", baseline_override="test-baseline_override", use_s3_dual_stack_endpoint=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_document("test-name", version_name="test-version_name", document_version="test-document_version", document_format="test-document_format", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_inventory_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_inventory
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_inventory(filters=[{}], aggregators="test-aggregators", result_attributes="test-result_attributes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_inventory_schema_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_inventory_schema
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_inventory_schema(type_name="test-type_name", next_token="test-next_token", max_results=1, aggregator="test-aggregator", sub_type="test-sub_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ops_item_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_ops_item
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_ops_item("test-ops_item_id", ops_item_arn="test-ops_item_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ops_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_ops_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_ops_metadata("test-ops_metadata_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ops_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_ops_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_ops_summary(sync_name="test-sync_name", filters=[{}], aggregators="test-aggregators", result_attributes="test-result_attributes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_parameter_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_parameter_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_parameter_history("test-name", with_decryption="test-with_decryption", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_parameters("test-names", with_decryption="test-with_decryption", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_patch_baseline_for_patch_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_patch_baseline_for_patch_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_patch_baseline_for_patch_group("test-patch_group", operating_system="test-operating_system", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resource_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import get_resource_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await get_resource_policies("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_label_parameter_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import label_parameter_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await label_parameter_version("test-name", "test-labels", parameter_version="test-parameter_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_association_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_association_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_association_versions("test-association_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_associations(association_filter_list="test-association_filter_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_command_invocations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_command_invocations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_command_invocations(command_id="test-command_id", instance_id="test-instance_id", max_results=1, next_token="test-next_token", filters=[{}], details="test-details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_commands_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_commands
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_commands(command_id="test-command_id", instance_id="test-instance_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_compliance_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_compliance_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_compliance_items(filters=[{}], resource_ids="test-resource_ids", resource_types="test-resource_types", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_compliance_summaries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_compliance_summaries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_compliance_summaries(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_document_metadata_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_document_metadata_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_document_metadata_history("test-name", "test-metadata", document_version="test-document_version", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_document_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_document_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_document_versions("test-name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_documents_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_documents
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_documents(document_filter_list="test-document_filter_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_inventory_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_inventory_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_inventory_entries("test-instance_id", "test-type_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_nodes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_nodes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_nodes(sync_name="test-sync_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_nodes_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_nodes_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_nodes_summary("test-aggregators", sync_name="test-sync_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ops_item_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_ops_item_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_ops_item_events(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ops_item_related_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_ops_item_related_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_ops_item_related_items(ops_item_id="test-ops_item_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ops_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_ops_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_ops_metadata(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_compliance_summaries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_resource_compliance_summaries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_resource_compliance_summaries(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import list_resource_data_sync
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await list_resource_data_sync(sync_type="test-sync_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_document_permission_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import modify_document_permission
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await modify_document_permission("test-name", "test-permission_type", account_ids_to_add=1, account_ids_to_remove=1, shared_document_version="test-shared_document_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_compliance_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import put_compliance_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", "test-execution_summary", "test-items", item_content_hash="test-item_content_hash", upload_type="test-upload_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-resource_arn", "{}", policy_id="test-policy_id", policy_hash="test-policy_hash", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_target_with_maintenance_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import register_target_with_maintenance_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await register_target_with_maintenance_window("test-window_id", "test-resource_type", "test-targets", owner_information="test-owner_information", name="test-name", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_task_with_maintenance_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import register_task_with_maintenance_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", targets="test-targets", service_role_arn="test-service_role_arn", task_parameters="test-task_parameters", task_invocation_parameters="test-task_invocation_parameters", priority="test-priority", max_concurrency=1, max_errors=1, logging_info="test-logging_info", name="test-name", description="test-description", client_token="test-client_token", cutoff_behavior="test-cutoff_behavior", alarm_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_automation_signal_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import send_automation_signal
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await send_automation_signal(True, "test-signal_type", payload="test-payload", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_command_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import send_command
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await send_command("test-document_name", instance_ids="test-instance_ids", targets="test-targets", document_version="test-document_version", document_hash="test-document_hash", document_hash_type="test-document_hash_type", timeout_seconds=1, comment="test-comment", parameters="test-parameters", output_s3_region="test-output_s3_region", output_s3_bucket_name="test-output_s3_bucket_name", output_s3_key_prefix="test-output_s3_key_prefix", max_concurrency=1, max_errors=1, service_role_arn="test-service_role_arn", notification_config={}, cloud_watch_output_config={}, alarm_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_access_request_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import start_access_request
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await start_access_request("test-reason", "test-targets", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_automation_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import start_automation_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await start_automation_execution("test-document_name", document_version="test-document_version", parameters="test-parameters", client_token="test-client_token", mode="test-mode", target_parameter_name="test-target_parameter_name", targets="test-targets", target_maps="test-target_maps", max_concurrency=1, max_errors=1, target_locations="test-target_locations", tags=[{"Key": "k", "Value": "v"}], alarm_configuration={}, target_locations_url="test-target_locations_url", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_change_request_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import start_change_request_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await start_change_request_execution("test-document_name", "test-runbooks", scheduled_time="test-scheduled_time", document_version="test-document_version", parameters="test-parameters", change_request_name="test-change_request_name", client_token="test-client_token", auto_approve=True, tags=[{"Key": "k", "Value": "v"}], scheduled_end_time="test-scheduled_end_time", change_details="test-change_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_execution_preview_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import start_execution_preview
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await start_execution_preview("test-document_name", document_version="test-document_version", execution_inputs="test-execution_inputs", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import start_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await start_session("test-target", document_name="test-document_name", reason="test-reason", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_automation_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import stop_automation_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await stop_automation_execution(True, type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_association("test-association_id", parameters="test-parameters", document_version="test-document_version", schedule_expression="test-schedule_expression", output_location="test-output_location", name="test-name", targets="test-targets", association_name="test-association_name", association_version="test-association_version", automation_target_parameter_name=True, max_errors=1, max_concurrency=1, compliance_severity="test-compliance_severity", sync_compliance="test-sync_compliance", apply_only_at_cron_interval=True, calendar_names="test-calendar_names", target_locations="test-target_locations", schedule_offset="test-schedule_offset", duration=1, target_maps="test-target_maps", alarm_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_document("test-content", "test-name", attachments="test-attachments", display_name="test-display_name", version_name="test-version_name", document_version="test-document_version", document_format="test-document_format", target_type="test-target_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_document_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_document_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_document_metadata("test-name", "test-document_reviews", document_version="test-document_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_maintenance_window_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_maintenance_window
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_maintenance_window("test-window_id", name="test-name", description="test-description", start_date="test-start_date", end_date="test-end_date", schedule="test-schedule", schedule_timezone="test-schedule_timezone", schedule_offset="test-schedule_offset", duration=1, cutoff="test-cutoff", allow_unassociated_targets=True, enabled=True, replace="test-replace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_maintenance_window_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_maintenance_window_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_maintenance_window_target("test-window_id", "test-window_target_id", targets="test-targets", owner_information="test-owner_information", name="test-name", description="test-description", replace="test-replace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_maintenance_window_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_maintenance_window_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_maintenance_window_task("test-window_id", "test-window_task_id", targets="test-targets", task_arn="test-task_arn", service_role_arn="test-service_role_arn", task_parameters="test-task_parameters", task_invocation_parameters="test-task_invocation_parameters", priority="test-priority", max_concurrency=1, max_errors=1, logging_info="test-logging_info", name="test-name", description="test-description", replace="test-replace", cutoff_behavior="test-cutoff_behavior", alarm_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ops_item_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_ops_item
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_ops_item("test-ops_item_id", description="test-description", operational_data="test-operational_data", operational_data_to_delete="test-operational_data_to_delete", notifications="test-notifications", priority="test-priority", related_ops_items="test-related_ops_items", status="test-status", title="test-title", category="test-category", severity="test-severity", actual_start_time="test-actual_start_time", actual_end_time="test-actual_end_time", planned_start_time="test-planned_start_time", planned_end_time="test-planned_end_time", ops_item_arn="test-ops_item_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ops_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_ops_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_ops_metadata("test-ops_metadata_arn", metadata_to_update="test-metadata_to_update", keys_to_delete="test-keys_to_delete", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_patch_baseline_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.parameter_store import update_patch_baseline
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.parameter_store.async_client", lambda *a, **kw: mock_client)
    await update_patch_baseline("test-baseline_id", name="test-name", global_filters="test-global_filters", approval_rules="test-approval_rules", approved_patches=True, approved_patches_compliance_level=True, approved_patches_enable_non_security=True, rejected_patches="test-rejected_patches", rejected_patches_action="test-rejected_patches_action", description="test-description", sources="test-sources", available_security_updates_compliance_status="test-available_security_updates_compliance_status", replace="test-replace", region_name="us-east-1")
    mock_client.call.assert_called_once()
