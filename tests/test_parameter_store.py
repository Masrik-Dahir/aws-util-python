"""Tests for aws_util.parameter_store module."""
from __future__ import annotations

from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.parameter_store import (
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

REGION = "us-east-1"


@pytest.fixture
def ssm(ssm_client):
    ssm_client.put_parameter(Name="/app/db/host", Value="db.example.com", Type="String")
    ssm_client.put_parameter(Name="/app/db/port", Value="5432", Type="String")
    ssm_client.put_parameter(Name="/app/secret", Value="s3cr3t", Type="SecureString")
    return ssm_client


# ---------------------------------------------------------------------------
# get_parameters_by_path
# ---------------------------------------------------------------------------


def test_get_parameters_by_path_returns_all(ssm):
    result = get_parameters_by_path("/app/db", region_name=REGION)
    assert result["/app/db/host"] == "db.example.com"
    assert result["/app/db/port"] == "5432"


def test_get_parameters_by_path_empty_path(ssm_client):
    result = get_parameters_by_path("/nonexistent/path", region_name=REGION)
    assert result == {}


def test_get_parameters_by_path_recursive_default(ssm):
    # recursive=True is default; should find nested params
    result = get_parameters_by_path("/app", region_name=REGION)
    assert "/app/db/host" in result


def test_get_parameters_by_path_with_decryption(ssm):
    # /app/secret is stored under /app; GetParametersByPath needs a prefix, not exact name
    result = get_parameters_by_path("/app", region_name=REGION, with_decryption=True)
    assert result["/app/secret"] == "s3cr3t"


def test_get_parameters_by_path_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "Denied"}},
        "GetParametersByPath",
    )
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_parameters_by_path failed"):
        get_parameters_by_path("/app", region_name=REGION)


# ---------------------------------------------------------------------------
# get_parameters_batch
# ---------------------------------------------------------------------------


def test_get_parameters_batch_returns_found(ssm):
    result = get_parameters_batch(["/app/db/host", "/app/db/port"], region_name=REGION)
    assert result["/app/db/host"] == "db.example.com"
    assert result["/app/db/port"] == "5432"


def test_get_parameters_batch_omits_missing(ssm):
    result = get_parameters_batch(["/app/db/host", "/nonexistent"], region_name=REGION)
    assert "/app/db/host" in result
    assert "/nonexistent" not in result


def test_get_parameters_batch_too_many_raises():
    with pytest.raises(ValueError, match="at most 10"):
        get_parameters_batch([f"/p/{i}" for i in range(11)], region_name=REGION)


def test_get_parameters_batch_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_client.get_parameters.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "GetParameters",
    )
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_parameters_batch failed"):
        get_parameters_batch(["/x"], region_name=REGION)


# ---------------------------------------------------------------------------
# put_parameter
# ---------------------------------------------------------------------------


def test_put_parameter_creates_parameter(ssm_client):
    put_parameter("/new/param", "newval", region_name=REGION)
    resp = ssm_client.get_parameter(Name="/new/param")
    assert resp["Parameter"]["Value"] == "newval"


def test_put_parameter_with_description(ssm_client):
    put_parameter(
        "/new/desc",
        "val",
        description="A description",
        region_name=REGION,
    )
    resp = ssm_client.describe_parameters(
        ParameterFilters=[{"Key": "Name", "Values": ["/new/desc"]}]
    )
    assert resp["Parameters"][0]["Description"] == "A description"


def test_put_parameter_overwrite(ssm_client):
    ssm_client.put_parameter(Name="/ow/param", Value="old", Type="String")
    put_parameter("/ow/param", "new", overwrite=True, region_name=REGION)
    resp = ssm_client.get_parameter(Name="/ow/param")
    assert resp["Parameter"]["Value"] == "new"


def test_put_parameter_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_client.put_parameter.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "Denied"}},
        "PutParameter",
    )
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put SSM parameter"):
        put_parameter("/x", "v", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_parameter
# ---------------------------------------------------------------------------


def test_delete_parameter_removes(ssm_client):
    ssm_client.put_parameter(Name="/del/param", Value="v", Type="String")
    delete_parameter("/del/param", region_name=REGION)
    resp = ssm_client.get_parameters(Names=["/del/param"])
    assert resp["Parameters"] == []


def test_delete_parameter_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_client.delete_parameter.side_effect = ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Not found"}},
        "DeleteParameter",
    )
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete SSM parameter"):
        delete_parameter("/nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# get_parameter
# ---------------------------------------------------------------------------


def test_get_parameter_returns_value(ssm_client):
    ssm_client.put_parameter(Name="/single/p", Value="hello", Type="String")
    result = get_parameter("/single/p", region_name=REGION)
    assert result == "hello"


def test_get_parameter_runtime_error_on_missing(ssm_client):
    with pytest.raises(RuntimeError, match="Error resolving SSM parameter"):
        get_parameter("/nonexistent/param", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_parameters
# ---------------------------------------------------------------------------


def test_describe_parameters_returns_all(ssm):
    result = describe_parameters(region_name=REGION)
    names = [p["Name"] for p in result]
    assert "/app/db/host" in names
    assert "/app/db/port" in names
    assert "/app/secret" in names


def test_describe_parameters_filters_begins_with(ssm):
    result = describe_parameters(
        filters=[{"Key": "Name", "Option": "BeginsWith", "Values": ["/app/db"]}],
        region_name=REGION,
    )
    names = [p["Name"] for p in result]
    assert "/app/db/host" in names
    assert "/app/db/port" in names
    assert "/app/secret" not in names


def test_describe_parameters_empty_results(ssm):
    result = describe_parameters(
        filters=[
            {"Key": "Name", "Option": "BeginsWith", "Values": ["/nonexistent/"]}
        ],
        region_name=REGION,
    )
    assert result == []


def test_describe_parameters_pagination(monkeypatch):
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    page1 = {
        "Parameters": [{"Name": "/a"}],
        "NextToken": "tok1",
    }
    page2 = {
        "Parameters": [{"Name": "/b"}],
    }
    mock_client = MagicMock()
    mock_client.describe_parameters.side_effect = [page1, page2]
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    result = describe_parameters(region_name=REGION)
    assert len(result) == 2
    assert result[0]["Name"] == "/a"
    assert result[1]["Name"] == "/b"
    assert mock_client.describe_parameters.call_count == 2


def test_describe_parameters_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_client.describe_parameters.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "Denied"}},
        "DescribeParameters",
    )
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_parameters failed"):
        describe_parameters(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_parameters (batch)
# ---------------------------------------------------------------------------


def test_delete_parameters_removes_and_returns(ssm):
    result = delete_parameters(
        ["/app/db/host", "/app/db/port"], region_name=REGION
    )
    assert sorted(result) == ["/app/db/host", "/app/db/port"]
    # Verify they are actually gone
    resp = ssm.get_parameters(Names=["/app/db/host", "/app/db/port"])
    assert resp["Parameters"] == []


def test_delete_parameters_too_many_raises():
    with pytest.raises(ValueError, match="at most 10"):
        delete_parameters([f"/p/{i}" for i in range(11)], region_name=REGION)


def test_delete_parameters_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.parameter_store as ps

    mock_client = MagicMock()
    mock_client.delete_parameters.side_effect = ClientError(
        {"Error": {"Code": "InternalServerError", "Message": "err"}},
        "DeleteParameters",
    )
    monkeypatch.setattr(ps, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_parameters failed"):
        delete_parameters(["/x"], region_name=REGION)


def test_add_tags_to_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    add_tags_to_resource("test-resource_type", "test-resource_id", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


def test_add_tags_to_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_type", "test-resource_id", [], region_name=REGION)


def test_associate_ops_item_related_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ops_item_related_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    associate_ops_item_related_item("test-ops_item_id", "test-association_type", "test-resource_type", "test-resource_uri", region_name=REGION)
    mock_client.associate_ops_item_related_item.assert_called_once()


def test_associate_ops_item_related_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_ops_item_related_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_ops_item_related_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate ops item related item"):
        associate_ops_item_related_item("test-ops_item_id", "test-association_type", "test-resource_type", "test-resource_uri", region_name=REGION)


def test_cancel_command(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_command.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    cancel_command("test-command_id", region_name=REGION)
    mock_client.cancel_command.assert_called_once()


def test_cancel_command_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_command",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel command"):
        cancel_command("test-command_id", region_name=REGION)


def test_cancel_maintenance_window_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_maintenance_window_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    cancel_maintenance_window_execution("test-window_execution_id", region_name=REGION)
    mock_client.cancel_maintenance_window_execution.assert_called_once()


def test_cancel_maintenance_window_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_maintenance_window_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_maintenance_window_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel maintenance window execution"):
        cancel_maintenance_window_execution("test-window_execution_id", region_name=REGION)


def test_create_activation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_activation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_activation("test-iam_role", region_name=REGION)
    mock_client.create_activation.assert_called_once()


def test_create_activation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_activation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_activation",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create activation"):
        create_activation("test-iam_role", region_name=REGION)


def test_create_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_association("test-name", region_name=REGION)
    mock_client.create_association.assert_called_once()


def test_create_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_association",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create association"):
        create_association("test-name", region_name=REGION)


def test_create_association_batch(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_association_batch.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_association_batch([], region_name=REGION)
    mock_client.create_association_batch.assert_called_once()


def test_create_association_batch_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_association_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_association_batch",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create association batch"):
        create_association_batch([], region_name=REGION)


def test_create_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_document("test-content", "test-name", region_name=REGION)
    mock_client.create_document.assert_called_once()


def test_create_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_document",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create document"):
        create_document("test-content", "test-name", region_name=REGION)


def test_create_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_maintenance_window("test-name", "test-schedule", 1, 1, True, region_name=REGION)
    mock_client.create_maintenance_window.assert_called_once()


def test_create_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create maintenance window"):
        create_maintenance_window("test-name", "test-schedule", 1, 1, True, region_name=REGION)


def test_create_ops_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_ops_item("test-description", "test-source", "test-title", region_name=REGION)
    mock_client.create_ops_item.assert_called_once()


def test_create_ops_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ops_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ops_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ops item"):
        create_ops_item("test-description", "test-source", "test-title", region_name=REGION)


def test_create_ops_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_ops_metadata("test-resource_id", region_name=REGION)
    mock_client.create_ops_metadata.assert_called_once()


def test_create_ops_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ops_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ops_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ops metadata"):
        create_ops_metadata("test-resource_id", region_name=REGION)


def test_create_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_patch_baseline("test-name", region_name=REGION)
    mock_client.create_patch_baseline.assert_called_once()


def test_create_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create patch baseline"):
        create_patch_baseline("test-name", region_name=REGION)


def test_create_resource_data_sync(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_resource_data_sync("test-sync_name", region_name=REGION)
    mock_client.create_resource_data_sync.assert_called_once()


def test_create_resource_data_sync_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_data_sync.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_data_sync",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create resource data sync"):
        create_resource_data_sync("test-sync_name", region_name=REGION)


def test_delete_activation(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_activation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_activation("test-activation_id", region_name=REGION)
    mock_client.delete_activation.assert_called_once()


def test_delete_activation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_activation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_activation",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete activation"):
        delete_activation("test-activation_id", region_name=REGION)


def test_delete_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_association(region_name=REGION)
    mock_client.delete_association.assert_called_once()


def test_delete_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_association",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete association"):
        delete_association(region_name=REGION)


def test_delete_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_document("test-name", region_name=REGION)
    mock_client.delete_document.assert_called_once()


def test_delete_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_document",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete document"):
        delete_document("test-name", region_name=REGION)


def test_delete_inventory(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_inventory.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_inventory("test-type_name", region_name=REGION)
    mock_client.delete_inventory.assert_called_once()


def test_delete_inventory_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_inventory.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_inventory",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete inventory"):
        delete_inventory("test-type_name", region_name=REGION)


def test_delete_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_maintenance_window("test-window_id", region_name=REGION)
    mock_client.delete_maintenance_window.assert_called_once()


def test_delete_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete maintenance window"):
        delete_maintenance_window("test-window_id", region_name=REGION)


def test_delete_ops_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_ops_item("test-ops_item_id", region_name=REGION)
    mock_client.delete_ops_item.assert_called_once()


def test_delete_ops_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ops_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ops_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ops item"):
        delete_ops_item("test-ops_item_id", region_name=REGION)


def test_delete_ops_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_ops_metadata("test-ops_metadata_arn", region_name=REGION)
    mock_client.delete_ops_metadata.assert_called_once()


def test_delete_ops_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ops_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ops_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ops metadata"):
        delete_ops_metadata("test-ops_metadata_arn", region_name=REGION)


def test_delete_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_patch_baseline("test-baseline_id", region_name=REGION)
    mock_client.delete_patch_baseline.assert_called_once()


def test_delete_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete patch baseline"):
        delete_patch_baseline("test-baseline_id", region_name=REGION)


def test_delete_resource_data_sync(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_resource_data_sync("test-sync_name", region_name=REGION)
    mock_client.delete_resource_data_sync.assert_called_once()


def test_delete_resource_data_sync_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_data_sync.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_data_sync",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource data sync"):
        delete_resource_data_sync("test-sync_name", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", "test-policy_id", "test-policy_hash", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", "test-policy_id", "test-policy_hash", region_name=REGION)


def test_deregister_managed_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_managed_instance.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    deregister_managed_instance("test-instance_id", region_name=REGION)
    mock_client.deregister_managed_instance.assert_called_once()


def test_deregister_managed_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_managed_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_managed_instance",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister managed instance"):
        deregister_managed_instance("test-instance_id", region_name=REGION)


def test_deregister_patch_baseline_for_patch_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_patch_baseline_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    deregister_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", region_name=REGION)
    mock_client.deregister_patch_baseline_for_patch_group.assert_called_once()


def test_deregister_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_patch_baseline_for_patch_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_patch_baseline_for_patch_group",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister patch baseline for patch group"):
        deregister_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", region_name=REGION)


def test_deregister_target_from_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_target_from_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", region_name=REGION)
    mock_client.deregister_target_from_maintenance_window.assert_called_once()


def test_deregister_target_from_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_target_from_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_target_from_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister target from maintenance window"):
        deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", region_name=REGION)


def test_deregister_task_from_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_task_from_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    deregister_task_from_maintenance_window("test-window_id", "test-window_task_id", region_name=REGION)
    mock_client.deregister_task_from_maintenance_window.assert_called_once()


def test_deregister_task_from_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_task_from_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_task_from_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister task from maintenance window"):
        deregister_task_from_maintenance_window("test-window_id", "test-window_task_id", region_name=REGION)


def test_describe_activations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_activations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_activations(region_name=REGION)
    mock_client.describe_activations.assert_called_once()


def test_describe_activations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_activations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_activations",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe activations"):
        describe_activations(region_name=REGION)


def test_describe_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association(region_name=REGION)
    mock_client.describe_association.assert_called_once()


def test_describe_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_association",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe association"):
        describe_association(region_name=REGION)


def test_describe_association_execution_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association_execution_targets.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association_execution_targets("test-association_id", "test-execution_id", region_name=REGION)
    mock_client.describe_association_execution_targets.assert_called_once()


def test_describe_association_execution_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association_execution_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_association_execution_targets",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe association execution targets"):
        describe_association_execution_targets("test-association_id", "test-execution_id", region_name=REGION)


def test_describe_association_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association_executions("test-association_id", region_name=REGION)
    mock_client.describe_association_executions.assert_called_once()


def test_describe_association_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_association_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_association_executions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe association executions"):
        describe_association_executions("test-association_id", region_name=REGION)


def test_describe_automation_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_automation_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_automation_executions(region_name=REGION)
    mock_client.describe_automation_executions.assert_called_once()


def test_describe_automation_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_automation_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_automation_executions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe automation executions"):
        describe_automation_executions(region_name=REGION)


def test_describe_automation_step_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_automation_step_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_automation_step_executions("test-automation_execution_id", region_name=REGION)
    mock_client.describe_automation_step_executions.assert_called_once()


def test_describe_automation_step_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_automation_step_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_automation_step_executions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe automation step executions"):
        describe_automation_step_executions("test-automation_execution_id", region_name=REGION)


def test_describe_available_patches(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_available_patches.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_available_patches(region_name=REGION)
    mock_client.describe_available_patches.assert_called_once()


def test_describe_available_patches_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_available_patches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_available_patches",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe available patches"):
        describe_available_patches(region_name=REGION)


def test_describe_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_document("test-name", region_name=REGION)
    mock_client.describe_document.assert_called_once()


def test_describe_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_document",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe document"):
        describe_document("test-name", region_name=REGION)


def test_describe_document_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_permission.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_document_permission("test-name", "test-permission_type", region_name=REGION)
    mock_client.describe_document_permission.assert_called_once()


def test_describe_document_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_document_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_document_permission",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe document permission"):
        describe_document_permission("test-name", "test-permission_type", region_name=REGION)


def test_describe_effective_instance_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_instance_associations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_effective_instance_associations("test-instance_id", region_name=REGION)
    mock_client.describe_effective_instance_associations.assert_called_once()


def test_describe_effective_instance_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_instance_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_effective_instance_associations",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe effective instance associations"):
        describe_effective_instance_associations("test-instance_id", region_name=REGION)


def test_describe_effective_patches_for_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_patches_for_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_effective_patches_for_patch_baseline("test-baseline_id", region_name=REGION)
    mock_client.describe_effective_patches_for_patch_baseline.assert_called_once()


def test_describe_effective_patches_for_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_patches_for_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_effective_patches_for_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe effective patches for patch baseline"):
        describe_effective_patches_for_patch_baseline("test-baseline_id", region_name=REGION)


def test_describe_instance_associations_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_associations_status.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_associations_status("test-instance_id", region_name=REGION)
    mock_client.describe_instance_associations_status.assert_called_once()


def test_describe_instance_associations_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_associations_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_associations_status",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance associations status"):
        describe_instance_associations_status("test-instance_id", region_name=REGION)


def test_describe_instance_information(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_information.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_information(region_name=REGION)
    mock_client.describe_instance_information.assert_called_once()


def test_describe_instance_information_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_information.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_information",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance information"):
        describe_instance_information(region_name=REGION)


def test_describe_instance_patch_states(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patch_states([], region_name=REGION)
    mock_client.describe_instance_patch_states.assert_called_once()


def test_describe_instance_patch_states_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_patch_states",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance patch states"):
        describe_instance_patch_states([], region_name=REGION)


def test_describe_instance_patch_states_for_patch_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patch_states_for_patch_group("test-patch_group", region_name=REGION)
    mock_client.describe_instance_patch_states_for_patch_group.assert_called_once()


def test_describe_instance_patch_states_for_patch_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states_for_patch_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_patch_states_for_patch_group",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance patch states for patch group"):
        describe_instance_patch_states_for_patch_group("test-patch_group", region_name=REGION)


def test_describe_instance_patches(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patches.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patches("test-instance_id", region_name=REGION)
    mock_client.describe_instance_patches.assert_called_once()


def test_describe_instance_patches_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_patches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_patches",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance patches"):
        describe_instance_patches("test-instance_id", region_name=REGION)


def test_describe_instance_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_properties.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_properties(region_name=REGION)
    mock_client.describe_instance_properties.assert_called_once()


def test_describe_instance_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_properties",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance properties"):
        describe_instance_properties(region_name=REGION)


def test_describe_inventory_deletions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inventory_deletions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_inventory_deletions(region_name=REGION)
    mock_client.describe_inventory_deletions.assert_called_once()


def test_describe_inventory_deletions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inventory_deletions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_inventory_deletions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe inventory deletions"):
        describe_inventory_deletions(region_name=REGION)


def test_describe_maintenance_window_execution_task_invocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_task_invocations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", region_name=REGION)
    mock_client.describe_maintenance_window_execution_task_invocations.assert_called_once()


def test_describe_maintenance_window_execution_task_invocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_task_invocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_execution_task_invocations",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window execution task invocations"):
        describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", region_name=REGION)


def test_describe_maintenance_window_execution_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_tasks.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_execution_tasks("test-window_execution_id", region_name=REGION)
    mock_client.describe_maintenance_window_execution_tasks.assert_called_once()


def test_describe_maintenance_window_execution_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_execution_tasks",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window execution tasks"):
        describe_maintenance_window_execution_tasks("test-window_execution_id", region_name=REGION)


def test_describe_maintenance_window_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_executions("test-window_id", region_name=REGION)
    mock_client.describe_maintenance_window_executions.assert_called_once()


def test_describe_maintenance_window_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_executions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window executions"):
        describe_maintenance_window_executions("test-window_id", region_name=REGION)


def test_describe_maintenance_window_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_schedule.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_schedule(region_name=REGION)
    mock_client.describe_maintenance_window_schedule.assert_called_once()


def test_describe_maintenance_window_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_schedule",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window schedule"):
        describe_maintenance_window_schedule(region_name=REGION)


def test_describe_maintenance_window_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_targets.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_targets("test-window_id", region_name=REGION)
    mock_client.describe_maintenance_window_targets.assert_called_once()


def test_describe_maintenance_window_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_targets",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window targets"):
        describe_maintenance_window_targets("test-window_id", region_name=REGION)


def test_describe_maintenance_window_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_tasks.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_tasks("test-window_id", region_name=REGION)
    mock_client.describe_maintenance_window_tasks.assert_called_once()


def test_describe_maintenance_window_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_window_tasks",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance window tasks"):
        describe_maintenance_window_tasks("test-window_id", region_name=REGION)


def test_describe_maintenance_windows(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_windows(region_name=REGION)
    mock_client.describe_maintenance_windows.assert_called_once()


def test_describe_maintenance_windows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_windows",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance windows"):
        describe_maintenance_windows(region_name=REGION)


def test_describe_maintenance_windows_for_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows_for_target.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_windows_for_target([], "test-resource_type", region_name=REGION)
    mock_client.describe_maintenance_windows_for_target.assert_called_once()


def test_describe_maintenance_windows_for_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows_for_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_windows_for_target",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance windows for target"):
        describe_maintenance_windows_for_target([], "test-resource_type", region_name=REGION)


def test_describe_ops_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ops_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_ops_items(region_name=REGION)
    mock_client.describe_ops_items.assert_called_once()


def test_describe_ops_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ops_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ops_items",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ops items"):
        describe_ops_items(region_name=REGION)


def test_describe_patch_baselines(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_baselines.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_baselines(region_name=REGION)
    mock_client.describe_patch_baselines.assert_called_once()


def test_describe_patch_baselines_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_baselines.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_patch_baselines",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe patch baselines"):
        describe_patch_baselines(region_name=REGION)


def test_describe_patch_group_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_group_state.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_group_state("test-patch_group", region_name=REGION)
    mock_client.describe_patch_group_state.assert_called_once()


def test_describe_patch_group_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_group_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_patch_group_state",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe patch group state"):
        describe_patch_group_state("test-patch_group", region_name=REGION)


def test_describe_patch_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_groups.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_groups(region_name=REGION)
    mock_client.describe_patch_groups.assert_called_once()


def test_describe_patch_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_patch_groups",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe patch groups"):
        describe_patch_groups(region_name=REGION)


def test_describe_patch_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_properties.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_properties("test-operating_system", "test-property", region_name=REGION)
    mock_client.describe_patch_properties.assert_called_once()


def test_describe_patch_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_patch_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_patch_properties",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe patch properties"):
        describe_patch_properties("test-operating_system", "test-property", region_name=REGION)


def test_describe_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_sessions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_sessions("test-state", region_name=REGION)
    mock_client.describe_sessions.assert_called_once()


def test_describe_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_sessions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe sessions"):
        describe_sessions("test-state", region_name=REGION)


def test_disassociate_ops_item_related_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ops_item_related_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    disassociate_ops_item_related_item("test-ops_item_id", "test-association_id", region_name=REGION)
    mock_client.disassociate_ops_item_related_item.assert_called_once()


def test_disassociate_ops_item_related_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_ops_item_related_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_ops_item_related_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate ops item related item"):
        disassociate_ops_item_related_item("test-ops_item_id", "test-association_id", region_name=REGION)


def test_get_access_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_token.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_access_token("test-access_request_id", region_name=REGION)
    mock_client.get_access_token.assert_called_once()


def test_get_access_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_access_token",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get access token"):
        get_access_token("test-access_request_id", region_name=REGION)


def test_get_automation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automation_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_automation_execution("test-automation_execution_id", region_name=REGION)
    mock_client.get_automation_execution.assert_called_once()


def test_get_automation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automation_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get automation execution"):
        get_automation_execution("test-automation_execution_id", region_name=REGION)


def test_get_calendar_state(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calendar_state.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_calendar_state([], region_name=REGION)
    mock_client.get_calendar_state.assert_called_once()


def test_get_calendar_state_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calendar_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_calendar_state",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get calendar state"):
        get_calendar_state([], region_name=REGION)


def test_get_command_invocation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_command_invocation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_command_invocation("test-command_id", "test-instance_id", region_name=REGION)
    mock_client.get_command_invocation.assert_called_once()


def test_get_command_invocation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_command_invocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_command_invocation",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get command invocation"):
        get_command_invocation("test-command_id", "test-instance_id", region_name=REGION)


def test_get_connection_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_status.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_connection_status("test-target", region_name=REGION)
    mock_client.get_connection_status.assert_called_once()


def test_get_connection_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connection_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connection_status",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connection status"):
        get_connection_status("test-target", region_name=REGION)


def test_get_default_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_default_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_default_patch_baseline(region_name=REGION)
    mock_client.get_default_patch_baseline.assert_called_once()


def test_get_default_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_default_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_default_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get default patch baseline"):
        get_default_patch_baseline(region_name=REGION)


def test_get_deployable_patch_snapshot_for_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployable_patch_snapshot_for_instance.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", region_name=REGION)
    mock_client.get_deployable_patch_snapshot_for_instance.assert_called_once()


def test_get_deployable_patch_snapshot_for_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployable_patch_snapshot_for_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deployable_patch_snapshot_for_instance",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get deployable patch snapshot for instance"):
        get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", region_name=REGION)


def test_get_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_document("test-name", region_name=REGION)
    mock_client.get_document.assert_called_once()


def test_get_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_document",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get document"):
        get_document("test-name", region_name=REGION)


def test_get_execution_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_execution_preview.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_execution_preview("test-execution_preview_id", region_name=REGION)
    mock_client.get_execution_preview.assert_called_once()


def test_get_execution_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_execution_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_execution_preview",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get execution preview"):
        get_execution_preview("test-execution_preview_id", region_name=REGION)


def test_get_inventory(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inventory.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_inventory(region_name=REGION)
    mock_client.get_inventory.assert_called_once()


def test_get_inventory_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inventory.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_inventory",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get inventory"):
        get_inventory(region_name=REGION)


def test_get_inventory_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inventory_schema.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_inventory_schema(region_name=REGION)
    mock_client.get_inventory_schema.assert_called_once()


def test_get_inventory_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_inventory_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_inventory_schema",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get inventory schema"):
        get_inventory_schema(region_name=REGION)


def test_get_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_maintenance_window("test-window_id", region_name=REGION)
    mock_client.get_maintenance_window.assert_called_once()


def test_get_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get maintenance window"):
        get_maintenance_window("test-window_id", region_name=REGION)


def test_get_maintenance_window_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_maintenance_window_execution("test-window_execution_id", region_name=REGION)
    mock_client.get_maintenance_window_execution.assert_called_once()


def test_get_maintenance_window_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_maintenance_window_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get maintenance window execution"):
        get_maintenance_window_execution("test-window_execution_id", region_name=REGION)


def test_get_maintenance_window_execution_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution_task.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_maintenance_window_execution_task("test-window_execution_id", "test-task_id", region_name=REGION)
    mock_client.get_maintenance_window_execution_task.assert_called_once()


def test_get_maintenance_window_execution_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_maintenance_window_execution_task",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get maintenance window execution task"):
        get_maintenance_window_execution_task("test-window_execution_id", "test-task_id", region_name=REGION)


def test_get_maintenance_window_execution_task_invocation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution_task_invocation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_maintenance_window_execution_task_invocation("test-window_execution_id", "test-task_id", "test-invocation_id", region_name=REGION)
    mock_client.get_maintenance_window_execution_task_invocation.assert_called_once()


def test_get_maintenance_window_execution_task_invocation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_execution_task_invocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_maintenance_window_execution_task_invocation",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get maintenance window execution task invocation"):
        get_maintenance_window_execution_task_invocation("test-window_execution_id", "test-task_id", "test-invocation_id", region_name=REGION)


def test_get_maintenance_window_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_task.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_maintenance_window_task("test-window_id", "test-window_task_id", region_name=REGION)
    mock_client.get_maintenance_window_task.assert_called_once()


def test_get_maintenance_window_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_maintenance_window_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_maintenance_window_task",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get maintenance window task"):
        get_maintenance_window_task("test-window_id", "test-window_task_id", region_name=REGION)


def test_get_ops_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_item("test-ops_item_id", region_name=REGION)
    mock_client.get_ops_item.assert_called_once()


def test_get_ops_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ops_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ops item"):
        get_ops_item("test-ops_item_id", region_name=REGION)


def test_get_ops_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_metadata("test-ops_metadata_arn", region_name=REGION)
    mock_client.get_ops_metadata.assert_called_once()


def test_get_ops_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ops_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ops metadata"):
        get_ops_metadata("test-ops_metadata_arn", region_name=REGION)


def test_get_ops_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_summary.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_summary(region_name=REGION)
    mock_client.get_ops_summary.assert_called_once()


def test_get_ops_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ops_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ops_summary",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ops summary"):
        get_ops_summary(region_name=REGION)


def test_get_parameter_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameter_history.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_parameter_history("test-name", region_name=REGION)
    mock_client.get_parameter_history.assert_called_once()


def test_get_parameter_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameter_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_parameter_history",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get parameter history"):
        get_parameter_history("test-name", region_name=REGION)


def test_get_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameters.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_parameters([], region_name=REGION)
    mock_client.get_parameters.assert_called_once()


def test_get_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_parameters",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get parameters"):
        get_parameters([], region_name=REGION)


def test_get_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_patch_baseline("test-baseline_id", region_name=REGION)
    mock_client.get_patch_baseline.assert_called_once()


def test_get_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get patch baseline"):
        get_patch_baseline("test-baseline_id", region_name=REGION)


def test_get_patch_baseline_for_patch_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_patch_baseline_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_patch_baseline_for_patch_group("test-patch_group", region_name=REGION)
    mock_client.get_patch_baseline_for_patch_group.assert_called_once()


def test_get_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_patch_baseline_for_patch_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_patch_baseline_for_patch_group",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get patch baseline for patch group"):
        get_patch_baseline_for_patch_group("test-patch_group", region_name=REGION)


def test_get_resource_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policies.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_resource_policies("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policies.assert_called_once()


def test_get_resource_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policies",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policies"):
        get_resource_policies("test-resource_arn", region_name=REGION)


def test_get_service_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_setting.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_service_setting("test-setting_id", region_name=REGION)
    mock_client.get_service_setting.assert_called_once()


def test_get_service_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_setting",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service setting"):
        get_service_setting("test-setting_id", region_name=REGION)


def test_label_parameter_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.label_parameter_version.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    label_parameter_version("test-name", [], region_name=REGION)
    mock_client.label_parameter_version.assert_called_once()


def test_label_parameter_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.label_parameter_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "label_parameter_version",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to label parameter version"):
        label_parameter_version("test-name", [], region_name=REGION)


def test_list_association_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_association_versions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_association_versions("test-association_id", region_name=REGION)
    mock_client.list_association_versions.assert_called_once()


def test_list_association_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_association_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_association_versions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list association versions"):
        list_association_versions("test-association_id", region_name=REGION)


def test_list_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_associations(region_name=REGION)
    mock_client.list_associations.assert_called_once()


def test_list_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associations",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list associations"):
        list_associations(region_name=REGION)


def test_list_command_invocations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_command_invocations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_command_invocations(region_name=REGION)
    mock_client.list_command_invocations.assert_called_once()


def test_list_command_invocations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_command_invocations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_command_invocations",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list command invocations"):
        list_command_invocations(region_name=REGION)


def test_list_commands(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_commands.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_commands(region_name=REGION)
    mock_client.list_commands.assert_called_once()


def test_list_commands_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_commands.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_commands",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list commands"):
        list_commands(region_name=REGION)


def test_list_compliance_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_compliance_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_compliance_items(region_name=REGION)
    mock_client.list_compliance_items.assert_called_once()


def test_list_compliance_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_compliance_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_compliance_items",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list compliance items"):
        list_compliance_items(region_name=REGION)


def test_list_compliance_summaries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_compliance_summaries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_compliance_summaries(region_name=REGION)
    mock_client.list_compliance_summaries.assert_called_once()


def test_list_compliance_summaries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_compliance_summaries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_compliance_summaries",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list compliance summaries"):
        list_compliance_summaries(region_name=REGION)


def test_list_document_metadata_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_metadata_history.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_document_metadata_history("test-name", "test-metadata", region_name=REGION)
    mock_client.list_document_metadata_history.assert_called_once()


def test_list_document_metadata_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_metadata_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_document_metadata_history",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list document metadata history"):
        list_document_metadata_history("test-name", "test-metadata", region_name=REGION)


def test_list_document_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_versions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_document_versions("test-name", region_name=REGION)
    mock_client.list_document_versions.assert_called_once()


def test_list_document_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_document_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_document_versions",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list document versions"):
        list_document_versions("test-name", region_name=REGION)


def test_list_documents(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_documents.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_documents(region_name=REGION)
    mock_client.list_documents.assert_called_once()


def test_list_documents_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_documents.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_documents",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list documents"):
        list_documents(region_name=REGION)


def test_list_inventory_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_inventory_entries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_inventory_entries("test-instance_id", "test-type_name", region_name=REGION)
    mock_client.list_inventory_entries.assert_called_once()


def test_list_inventory_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_inventory_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_inventory_entries",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list inventory entries"):
        list_inventory_entries("test-instance_id", "test-type_name", region_name=REGION)


def test_list_nodes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_nodes.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_nodes(region_name=REGION)
    mock_client.list_nodes.assert_called_once()


def test_list_nodes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_nodes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_nodes",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list nodes"):
        list_nodes(region_name=REGION)


def test_list_nodes_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_nodes_summary.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_nodes_summary([], region_name=REGION)
    mock_client.list_nodes_summary.assert_called_once()


def test_list_nodes_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_nodes_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_nodes_summary",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list nodes summary"):
        list_nodes_summary([], region_name=REGION)


def test_list_ops_item_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_item_events.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_item_events(region_name=REGION)
    mock_client.list_ops_item_events.assert_called_once()


def test_list_ops_item_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_item_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ops_item_events",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ops item events"):
        list_ops_item_events(region_name=REGION)


def test_list_ops_item_related_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_item_related_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_item_related_items(region_name=REGION)
    mock_client.list_ops_item_related_items.assert_called_once()


def test_list_ops_item_related_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_item_related_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ops_item_related_items",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ops item related items"):
        list_ops_item_related_items(region_name=REGION)


def test_list_ops_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_metadata(region_name=REGION)
    mock_client.list_ops_metadata.assert_called_once()


def test_list_ops_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ops_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ops_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ops metadata"):
        list_ops_metadata(region_name=REGION)


def test_list_resource_compliance_summaries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_compliance_summaries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_resource_compliance_summaries(region_name=REGION)
    mock_client.list_resource_compliance_summaries.assert_called_once()


def test_list_resource_compliance_summaries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_compliance_summaries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_compliance_summaries",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource compliance summaries"):
        list_resource_compliance_summaries(region_name=REGION)


def test_list_resource_data_sync(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_resource_data_sync(region_name=REGION)
    mock_client.list_resource_data_sync.assert_called_once()


def test_list_resource_data_sync_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_data_sync.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_data_sync",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource data sync"):
        list_resource_data_sync(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_type", "test-resource_id", region_name=REGION)


def test_modify_document_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_document_permission.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    modify_document_permission("test-name", "test-permission_type", region_name=REGION)
    mock_client.modify_document_permission.assert_called_once()


def test_modify_document_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_document_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_document_permission",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify document permission"):
        modify_document_permission("test-name", "test-permission_type", region_name=REGION)


def test_put_compliance_items(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_compliance_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", {}, [], region_name=REGION)
    mock_client.put_compliance_items.assert_called_once()


def test_put_compliance_items_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_compliance_items.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_compliance_items",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put compliance items"):
        put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", {}, [], region_name=REGION)


def test_put_inventory(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_inventory.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    put_inventory("test-instance_id", [], region_name=REGION)
    mock_client.put_inventory.assert_called_once()


def test_put_inventory_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_inventory.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_inventory",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put inventory"):
        put_inventory("test-instance_id", [], region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


def test_register_default_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_default_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_default_patch_baseline("test-baseline_id", region_name=REGION)
    mock_client.register_default_patch_baseline.assert_called_once()


def test_register_default_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_default_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_default_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register default patch baseline"):
        register_default_patch_baseline("test-baseline_id", region_name=REGION)


def test_register_patch_baseline_for_patch_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_patch_baseline_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", region_name=REGION)
    mock_client.register_patch_baseline_for_patch_group.assert_called_once()


def test_register_patch_baseline_for_patch_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_patch_baseline_for_patch_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_patch_baseline_for_patch_group",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register patch baseline for patch group"):
        register_patch_baseline_for_patch_group("test-baseline_id", "test-patch_group", region_name=REGION)


def test_register_target_with_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_target_with_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_target_with_maintenance_window("test-window_id", "test-resource_type", [], region_name=REGION)
    mock_client.register_target_with_maintenance_window.assert_called_once()


def test_register_target_with_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_target_with_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_target_with_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register target with maintenance window"):
        register_target_with_maintenance_window("test-window_id", "test-resource_type", [], region_name=REGION)


def test_register_task_with_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_task_with_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", region_name=REGION)
    mock_client.register_task_with_maintenance_window.assert_called_once()


def test_register_task_with_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_task_with_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_task_with_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register task with maintenance window"):
        register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", region_name=REGION)


def test_remove_tags_from_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    remove_tags_from_resource("test-resource_type", "test-resource_id", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_type", "test-resource_id", [], region_name=REGION)


def test_reset_service_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_service_setting.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    reset_service_setting("test-setting_id", region_name=REGION)
    mock_client.reset_service_setting.assert_called_once()


def test_reset_service_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_service_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_service_setting",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset service setting"):
        reset_service_setting("test-setting_id", region_name=REGION)


def test_resume_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_session.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    resume_session("test-session_id", region_name=REGION)
    mock_client.resume_session.assert_called_once()


def test_resume_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_session",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume session"):
        resume_session("test-session_id", region_name=REGION)


def test_send_automation_signal(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_automation_signal.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    send_automation_signal("test-automation_execution_id", "test-signal_type", region_name=REGION)
    mock_client.send_automation_signal.assert_called_once()


def test_send_automation_signal_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_automation_signal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_automation_signal",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send automation signal"):
        send_automation_signal("test-automation_execution_id", "test-signal_type", region_name=REGION)


def test_send_command(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_command.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    send_command("test-document_name", region_name=REGION)
    mock_client.send_command.assert_called_once()


def test_send_command_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_command",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send command"):
        send_command("test-document_name", region_name=REGION)


def test_start_access_request(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_access_request.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_access_request("test-reason", [], region_name=REGION)
    mock_client.start_access_request.assert_called_once()


def test_start_access_request_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_access_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_access_request",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start access request"):
        start_access_request("test-reason", [], region_name=REGION)


def test_start_associations_once(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_associations_once.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_associations_once([], region_name=REGION)
    mock_client.start_associations_once.assert_called_once()


def test_start_associations_once_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_associations_once.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_associations_once",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start associations once"):
        start_associations_once([], region_name=REGION)


def test_start_automation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automation_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_automation_execution("test-document_name", region_name=REGION)
    mock_client.start_automation_execution.assert_called_once()


def test_start_automation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_automation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_automation_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start automation execution"):
        start_automation_execution("test-document_name", region_name=REGION)


def test_start_change_request_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_change_request_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_change_request_execution("test-document_name", [], region_name=REGION)
    mock_client.start_change_request_execution.assert_called_once()


def test_start_change_request_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_change_request_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_change_request_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start change request execution"):
        start_change_request_execution("test-document_name", [], region_name=REGION)


def test_start_execution_preview(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_execution_preview.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_execution_preview("test-document_name", region_name=REGION)
    mock_client.start_execution_preview.assert_called_once()


def test_start_execution_preview_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_execution_preview.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_execution_preview",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start execution preview"):
        start_execution_preview("test-document_name", region_name=REGION)


def test_start_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_session.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_session("test-target", region_name=REGION)
    mock_client.start_session.assert_called_once()


def test_start_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_session",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start session"):
        start_session("test-target", region_name=REGION)


def test_stop_automation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_automation_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    stop_automation_execution("test-automation_execution_id", region_name=REGION)
    mock_client.stop_automation_execution.assert_called_once()


def test_stop_automation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_automation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_automation_execution",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop automation execution"):
        stop_automation_execution("test-automation_execution_id", region_name=REGION)


def test_terminate_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_session.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    terminate_session("test-session_id", region_name=REGION)
    mock_client.terminate_session.assert_called_once()


def test_terminate_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "terminate_session",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate session"):
        terminate_session("test-session_id", region_name=REGION)


def test_unlabel_parameter_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.unlabel_parameter_version.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    unlabel_parameter_version("test-name", 1, [], region_name=REGION)
    mock_client.unlabel_parameter_version.assert_called_once()


def test_unlabel_parameter_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.unlabel_parameter_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unlabel_parameter_version",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to unlabel parameter version"):
        unlabel_parameter_version("test-name", 1, [], region_name=REGION)


def test_update_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_association("test-association_id", region_name=REGION)
    mock_client.update_association.assert_called_once()


def test_update_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_association",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update association"):
        update_association("test-association_id", region_name=REGION)


def test_update_association_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_association_status.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_association_status("test-name", "test-instance_id", {}, region_name=REGION)
    mock_client.update_association_status.assert_called_once()


def test_update_association_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_association_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_association_status",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update association status"):
        update_association_status("test-name", "test-instance_id", {}, region_name=REGION)


def test_update_document(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_document("test-content", "test-name", region_name=REGION)
    mock_client.update_document.assert_called_once()


def test_update_document_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_document",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update document"):
        update_document("test-content", "test-name", region_name=REGION)


def test_update_document_default_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document_default_version.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_document_default_version("test-name", "test-document_version", region_name=REGION)
    mock_client.update_document_default_version.assert_called_once()


def test_update_document_default_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document_default_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_document_default_version",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update document default version"):
        update_document_default_version("test-name", "test-document_version", region_name=REGION)


def test_update_document_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_document_metadata("test-name", {}, region_name=REGION)
    mock_client.update_document_metadata.assert_called_once()


def test_update_document_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_document_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_document_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update document metadata"):
        update_document_metadata("test-name", {}, region_name=REGION)


def test_update_maintenance_window(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window("test-window_id", region_name=REGION)
    mock_client.update_maintenance_window.assert_called_once()


def test_update_maintenance_window_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_maintenance_window",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update maintenance window"):
        update_maintenance_window("test-window_id", region_name=REGION)


def test_update_maintenance_window_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window_target.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window_target("test-window_id", "test-window_target_id", region_name=REGION)
    mock_client.update_maintenance_window_target.assert_called_once()


def test_update_maintenance_window_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_maintenance_window_target",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update maintenance window target"):
        update_maintenance_window_target("test-window_id", "test-window_target_id", region_name=REGION)


def test_update_maintenance_window_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window_task.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window_task("test-window_id", "test-window_task_id", region_name=REGION)
    mock_client.update_maintenance_window_task.assert_called_once()


def test_update_maintenance_window_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_window_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_maintenance_window_task",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update maintenance window task"):
        update_maintenance_window_task("test-window_id", "test-window_task_id", region_name=REGION)


def test_update_managed_instance_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_managed_instance_role.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_managed_instance_role("test-instance_id", "test-iam_role", region_name=REGION)
    mock_client.update_managed_instance_role.assert_called_once()


def test_update_managed_instance_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_managed_instance_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_managed_instance_role",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update managed instance role"):
        update_managed_instance_role("test-instance_id", "test-iam_role", region_name=REGION)


def test_update_ops_item(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_ops_item("test-ops_item_id", region_name=REGION)
    mock_client.update_ops_item.assert_called_once()


def test_update_ops_item_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ops_item.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ops_item",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update ops item"):
        update_ops_item("test-ops_item_id", region_name=REGION)


def test_update_ops_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_ops_metadata("test-ops_metadata_arn", region_name=REGION)
    mock_client.update_ops_metadata.assert_called_once()


def test_update_ops_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ops_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ops_metadata",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update ops metadata"):
        update_ops_metadata("test-ops_metadata_arn", region_name=REGION)


def test_update_patch_baseline(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_patch_baseline("test-baseline_id", region_name=REGION)
    mock_client.update_patch_baseline.assert_called_once()


def test_update_patch_baseline_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_patch_baseline.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_patch_baseline",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update patch baseline"):
        update_patch_baseline("test-baseline_id", region_name=REGION)


def test_update_resource_data_sync(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_resource_data_sync("test-sync_name", "test-sync_type", {}, region_name=REGION)
    mock_client.update_resource_data_sync.assert_called_once()


def test_update_resource_data_sync_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_data_sync.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_data_sync",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update resource data sync"):
        update_resource_data_sync("test-sync_name", "test-sync_type", {}, region_name=REGION)


def test_update_service_setting(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_setting.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_service_setting("test-setting_id", "test-setting_value", region_name=REGION)
    mock_client.update_service_setting.assert_called_once()


def test_update_service_setting_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_setting.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_service_setting",
    )
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update service setting"):
        update_service_setting("test-setting_id", "test-setting_value", region_name=REGION)


def test_cancel_command_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import cancel_command
    mock_client = MagicMock()
    mock_client.cancel_command.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    cancel_command("test-command_id", instance_ids="test-instance_ids", region_name="us-east-1")
    mock_client.cancel_command.assert_called_once()

def test_create_activation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_activation
    mock_client = MagicMock()
    mock_client.create_activation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_activation("test-iam_role", description="test-description", default_instance_name="test-default_instance_name", registration_limit=1, expiration_date="test-expiration_date", tags=[{"Key": "k", "Value": "v"}], registration_metadata="test-registration_metadata", region_name="us-east-1")
    mock_client.create_activation.assert_called_once()

def test_create_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_association
    mock_client = MagicMock()
    mock_client.create_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_association("test-name", document_version="test-document_version", instance_id="test-instance_id", parameters="test-parameters", targets="test-targets", schedule_expression="test-schedule_expression", output_location="test-output_location", association_name="test-association_name", automation_target_parameter_name=True, max_errors=1, max_concurrency=1, compliance_severity="test-compliance_severity", sync_compliance="test-sync_compliance", apply_only_at_cron_interval=True, calendar_names="test-calendar_names", target_locations="test-target_locations", schedule_offset="test-schedule_offset", duration=1, target_maps="test-target_maps", tags=[{"Key": "k", "Value": "v"}], alarm_configuration={}, region_name="us-east-1")
    mock_client.create_association.assert_called_once()

def test_create_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_document
    mock_client = MagicMock()
    mock_client.create_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_document("test-content", "test-name", requires=True, attachments="test-attachments", display_name="test-display_name", version_name="test-version_name", document_type="test-document_type", document_format="test-document_format", target_type="test-target_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_document.assert_called_once()

def test_create_maintenance_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_maintenance_window
    mock_client = MagicMock()
    mock_client.create_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_maintenance_window("test-name", "test-schedule", 1, "test-cutoff", True, description="test-description", start_date="test-start_date", end_date="test-end_date", schedule_timezone="test-schedule_timezone", schedule_offset="test-schedule_offset", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_maintenance_window.assert_called_once()

def test_create_ops_item_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_ops_item
    mock_client = MagicMock()
    mock_client.create_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_ops_item("test-description", "test-source", "test-title", ops_item_type="test-ops_item_type", operational_data="test-operational_data", notifications="test-notifications", priority="test-priority", related_ops_items="test-related_ops_items", tags=[{"Key": "k", "Value": "v"}], category="test-category", severity="test-severity", actual_start_time="test-actual_start_time", actual_end_time="test-actual_end_time", planned_start_time="test-planned_start_time", planned_end_time="test-planned_end_time", account_id=1, region_name="us-east-1")
    mock_client.create_ops_item.assert_called_once()

def test_create_ops_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_ops_metadata
    mock_client = MagicMock()
    mock_client.create_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_ops_metadata("test-resource_id", metadata="test-metadata", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_ops_metadata.assert_called_once()

def test_create_patch_baseline_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_patch_baseline
    mock_client = MagicMock()
    mock_client.create_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_patch_baseline("test-name", operating_system="test-operating_system", global_filters="test-global_filters", approval_rules="test-approval_rules", approved_patches=True, approved_patches_compliance_level=True, approved_patches_enable_non_security=True, rejected_patches="test-rejected_patches", rejected_patches_action="test-rejected_patches_action", description="test-description", sources="test-sources", available_security_updates_compliance_status="test-available_security_updates_compliance_status", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_patch_baseline.assert_called_once()

def test_create_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import create_resource_data_sync
    mock_client = MagicMock()
    mock_client.create_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    create_resource_data_sync("test-sync_name", s3_destination="test-s3_destination", sync_type="test-sync_type", sync_source="test-sync_source", region_name="us-east-1")
    mock_client.create_resource_data_sync.assert_called_once()

def test_delete_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import delete_association
    mock_client = MagicMock()
    mock_client.delete_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_association(name="test-name", instance_id="test-instance_id", association_id="test-association_id", region_name="us-east-1")
    mock_client.delete_association.assert_called_once()

def test_delete_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import delete_document
    mock_client = MagicMock()
    mock_client.delete_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_document("test-name", document_version="test-document_version", version_name="test-version_name", force=True, region_name="us-east-1")
    mock_client.delete_document.assert_called_once()

def test_delete_inventory_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import delete_inventory
    mock_client = MagicMock()
    mock_client.delete_inventory.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_inventory("test-type_name", schema_delete_option="test-schema_delete_option", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_inventory.assert_called_once()

def test_delete_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import delete_resource_data_sync
    mock_client = MagicMock()
    mock_client.delete_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    delete_resource_data_sync("test-sync_name", sync_type="test-sync_type", region_name="us-east-1")
    mock_client.delete_resource_data_sync.assert_called_once()

def test_deregister_target_from_maintenance_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import deregister_target_from_maintenance_window
    mock_client = MagicMock()
    mock_client.deregister_target_from_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    deregister_target_from_maintenance_window("test-window_id", "test-window_target_id", safe="test-safe", region_name="us-east-1")
    mock_client.deregister_target_from_maintenance_window.assert_called_once()

def test_describe_activations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_activations
    mock_client = MagicMock()
    mock_client.describe_activations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_activations(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_activations.assert_called_once()

def test_describe_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_association
    mock_client = MagicMock()
    mock_client.describe_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association(name="test-name", instance_id="test-instance_id", association_id="test-association_id", association_version="test-association_version", region_name="us-east-1")
    mock_client.describe_association.assert_called_once()

def test_describe_association_execution_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_association_execution_targets
    mock_client = MagicMock()
    mock_client.describe_association_execution_targets.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association_execution_targets("test-association_id", "test-execution_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_association_execution_targets.assert_called_once()

def test_describe_association_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_association_executions
    mock_client = MagicMock()
    mock_client.describe_association_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_association_executions("test-association_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_association_executions.assert_called_once()

def test_describe_automation_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_automation_executions
    mock_client = MagicMock()
    mock_client.describe_automation_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_automation_executions(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_automation_executions.assert_called_once()

def test_describe_automation_step_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_automation_step_executions
    mock_client = MagicMock()
    mock_client.describe_automation_step_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_automation_step_executions(True, filters=[{}], next_token="test-next_token", max_results=1, reverse_order="test-reverse_order", region_name="us-east-1")
    mock_client.describe_automation_step_executions.assert_called_once()

def test_describe_available_patches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_available_patches
    mock_client = MagicMock()
    mock_client.describe_available_patches.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_available_patches(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_available_patches.assert_called_once()

def test_describe_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_document
    mock_client = MagicMock()
    mock_client.describe_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_document("test-name", document_version="test-document_version", version_name="test-version_name", region_name="us-east-1")
    mock_client.describe_document.assert_called_once()

def test_describe_document_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_document_permission
    mock_client = MagicMock()
    mock_client.describe_document_permission.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_document_permission("test-name", "test-permission_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_document_permission.assert_called_once()

def test_describe_effective_instance_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_effective_instance_associations
    mock_client = MagicMock()
    mock_client.describe_effective_instance_associations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_effective_instance_associations("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_effective_instance_associations.assert_called_once()

def test_describe_effective_patches_for_patch_baseline_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_effective_patches_for_patch_baseline
    mock_client = MagicMock()
    mock_client.describe_effective_patches_for_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_effective_patches_for_patch_baseline("test-baseline_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_effective_patches_for_patch_baseline.assert_called_once()

def test_describe_instance_associations_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_associations_status
    mock_client = MagicMock()
    mock_client.describe_instance_associations_status.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_associations_status("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_associations_status.assert_called_once()

def test_describe_instance_information_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_information
    mock_client = MagicMock()
    mock_client.describe_instance_information.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_information(instance_information_filter_list="test-instance_information_filter_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_information.assert_called_once()

def test_describe_instance_patch_states_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_patch_states
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patch_states("test-instance_ids", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_instance_patch_states.assert_called_once()

def test_describe_instance_patch_states_for_patch_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_patch_states_for_patch_group
    mock_client = MagicMock()
    mock_client.describe_instance_patch_states_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patch_states_for_patch_group("test-patch_group", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_instance_patch_states_for_patch_group.assert_called_once()

def test_describe_instance_patches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_patches
    mock_client = MagicMock()
    mock_client.describe_instance_patches.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_patches("test-instance_id", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_instance_patches.assert_called_once()

def test_describe_instance_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_instance_properties
    mock_client = MagicMock()
    mock_client.describe_instance_properties.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_instance_properties(instance_property_filter_list="test-instance_property_filter_list", filters_with_operator="test-filters_with_operator", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_instance_properties.assert_called_once()

def test_describe_inventory_deletions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_inventory_deletions
    mock_client = MagicMock()
    mock_client.describe_inventory_deletions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_inventory_deletions(deletion_id="test-deletion_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_inventory_deletions.assert_called_once()

def test_describe_maintenance_window_execution_task_invocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_execution_task_invocations
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_task_invocations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_execution_task_invocations("test-window_execution_id", "test-task_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_execution_task_invocations.assert_called_once()

def test_describe_maintenance_window_execution_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_execution_tasks
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_execution_tasks.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_execution_tasks("test-window_execution_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_execution_tasks.assert_called_once()

def test_describe_maintenance_window_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_executions
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_executions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_executions("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_executions.assert_called_once()

def test_describe_maintenance_window_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_schedule
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_schedule.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_schedule(window_id="test-window_id", targets="test-targets", resource_type="test-resource_type", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_schedule.assert_called_once()

def test_describe_maintenance_window_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_targets
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_targets.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_targets("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_targets.assert_called_once()

def test_describe_maintenance_window_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_window_tasks
    mock_client = MagicMock()
    mock_client.describe_maintenance_window_tasks.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_window_tasks("test-window_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_window_tasks.assert_called_once()

def test_describe_maintenance_windows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_windows
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_windows(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_windows.assert_called_once()

def test_describe_maintenance_windows_for_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_maintenance_windows_for_target
    mock_client = MagicMock()
    mock_client.describe_maintenance_windows_for_target.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_windows_for_target("test-targets", "test-resource_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_maintenance_windows_for_target.assert_called_once()

def test_describe_ops_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_ops_items
    mock_client = MagicMock()
    mock_client.describe_ops_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_ops_items(ops_item_filters="test-ops_item_filters", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_ops_items.assert_called_once()

def test_describe_patch_baselines_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_patch_baselines
    mock_client = MagicMock()
    mock_client.describe_patch_baselines.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_baselines(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_patch_baselines.assert_called_once()

def test_describe_patch_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_patch_groups
    mock_client = MagicMock()
    mock_client.describe_patch_groups.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_groups(max_results=1, filters=[{}], next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_patch_groups.assert_called_once()

def test_describe_patch_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_patch_properties
    mock_client = MagicMock()
    mock_client.describe_patch_properties.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_patch_properties("test-operating_system", "test-property", patch_set="test-patch_set", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_patch_properties.assert_called_once()

def test_describe_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import describe_sessions
    mock_client = MagicMock()
    mock_client.describe_sessions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    describe_sessions("test-state", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.describe_sessions.assert_called_once()

def test_get_calendar_state_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_calendar_state
    mock_client = MagicMock()
    mock_client.get_calendar_state.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_calendar_state("test-calendar_names", at_time="test-at_time", region_name="us-east-1")
    mock_client.get_calendar_state.assert_called_once()

def test_get_command_invocation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_command_invocation
    mock_client = MagicMock()
    mock_client.get_command_invocation.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_command_invocation("test-command_id", "test-instance_id", plugin_name="test-plugin_name", region_name="us-east-1")
    mock_client.get_command_invocation.assert_called_once()

def test_get_default_patch_baseline_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_default_patch_baseline
    mock_client = MagicMock()
    mock_client.get_default_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_default_patch_baseline(operating_system="test-operating_system", region_name="us-east-1")
    mock_client.get_default_patch_baseline.assert_called_once()

def test_get_deployable_patch_snapshot_for_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_deployable_patch_snapshot_for_instance
    mock_client = MagicMock()
    mock_client.get_deployable_patch_snapshot_for_instance.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_deployable_patch_snapshot_for_instance("test-instance_id", "test-snapshot_id", baseline_override="test-baseline_override", use_s3_dual_stack_endpoint=True, region_name="us-east-1")
    mock_client.get_deployable_patch_snapshot_for_instance.assert_called_once()

def test_get_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_document
    mock_client = MagicMock()
    mock_client.get_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_document("test-name", version_name="test-version_name", document_version="test-document_version", document_format="test-document_format", region_name="us-east-1")
    mock_client.get_document.assert_called_once()

def test_get_inventory_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_inventory
    mock_client = MagicMock()
    mock_client.get_inventory.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_inventory(filters=[{}], aggregators="test-aggregators", result_attributes="test-result_attributes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_inventory.assert_called_once()

def test_get_inventory_schema_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_inventory_schema
    mock_client = MagicMock()
    mock_client.get_inventory_schema.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_inventory_schema(type_name="test-type_name", next_token="test-next_token", max_results=1, aggregator="test-aggregator", sub_type="test-sub_type", region_name="us-east-1")
    mock_client.get_inventory_schema.assert_called_once()

def test_get_ops_item_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_ops_item
    mock_client = MagicMock()
    mock_client.get_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_item("test-ops_item_id", ops_item_arn="test-ops_item_arn", region_name="us-east-1")
    mock_client.get_ops_item.assert_called_once()

def test_get_ops_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_ops_metadata
    mock_client = MagicMock()
    mock_client.get_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_metadata("test-ops_metadata_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_ops_metadata.assert_called_once()

def test_get_ops_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_ops_summary
    mock_client = MagicMock()
    mock_client.get_ops_summary.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_ops_summary(sync_name="test-sync_name", filters=[{}], aggregators="test-aggregators", result_attributes="test-result_attributes", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_ops_summary.assert_called_once()

def test_get_parameter_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_parameter_history
    mock_client = MagicMock()
    mock_client.get_parameter_history.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_parameter_history("test-name", with_decryption="test-with_decryption", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_parameter_history.assert_called_once()

def test_get_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_parameters
    mock_client = MagicMock()
    mock_client.get_parameters.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_parameters("test-names", with_decryption="test-with_decryption", region_name="us-east-1")
    mock_client.get_parameters.assert_called_once()

def test_get_patch_baseline_for_patch_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_patch_baseline_for_patch_group
    mock_client = MagicMock()
    mock_client.get_patch_baseline_for_patch_group.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_patch_baseline_for_patch_group("test-patch_group", operating_system="test-operating_system", region_name="us-east-1")
    mock_client.get_patch_baseline_for_patch_group.assert_called_once()

def test_get_resource_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import get_resource_policies
    mock_client = MagicMock()
    mock_client.get_resource_policies.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    get_resource_policies("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_resource_policies.assert_called_once()

def test_label_parameter_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import label_parameter_version
    mock_client = MagicMock()
    mock_client.label_parameter_version.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    label_parameter_version("test-name", "test-labels", parameter_version="test-parameter_version", region_name="us-east-1")
    mock_client.label_parameter_version.assert_called_once()

def test_list_association_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_association_versions
    mock_client = MagicMock()
    mock_client.list_association_versions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_association_versions("test-association_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_association_versions.assert_called_once()

def test_list_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_associations
    mock_client = MagicMock()
    mock_client.list_associations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_associations(association_filter_list="test-association_filter_list", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_associations.assert_called_once()

def test_list_command_invocations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_command_invocations
    mock_client = MagicMock()
    mock_client.list_command_invocations.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_command_invocations(command_id="test-command_id", instance_id="test-instance_id", max_results=1, next_token="test-next_token", filters=[{}], details="test-details", region_name="us-east-1")
    mock_client.list_command_invocations.assert_called_once()

def test_list_commands_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_commands
    mock_client = MagicMock()
    mock_client.list_commands.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_commands(command_id="test-command_id", instance_id="test-instance_id", max_results=1, next_token="test-next_token", filters=[{}], region_name="us-east-1")
    mock_client.list_commands.assert_called_once()

def test_list_compliance_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_compliance_items
    mock_client = MagicMock()
    mock_client.list_compliance_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_compliance_items(filters=[{}], resource_ids="test-resource_ids", resource_types="test-resource_types", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_compliance_items.assert_called_once()

def test_list_compliance_summaries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_compliance_summaries
    mock_client = MagicMock()
    mock_client.list_compliance_summaries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_compliance_summaries(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_compliance_summaries.assert_called_once()

def test_list_document_metadata_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_document_metadata_history
    mock_client = MagicMock()
    mock_client.list_document_metadata_history.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_document_metadata_history("test-name", "test-metadata", document_version="test-document_version", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_document_metadata_history.assert_called_once()

def test_list_document_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_document_versions
    mock_client = MagicMock()
    mock_client.list_document_versions.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_document_versions("test-name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_document_versions.assert_called_once()

def test_list_documents_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_documents
    mock_client = MagicMock()
    mock_client.list_documents.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_documents(document_filter_list="test-document_filter_list", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_documents.assert_called_once()

def test_list_inventory_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_inventory_entries
    mock_client = MagicMock()
    mock_client.list_inventory_entries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_inventory_entries("test-instance_id", "test-type_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_inventory_entries.assert_called_once()

def test_list_nodes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_nodes
    mock_client = MagicMock()
    mock_client.list_nodes.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_nodes(sync_name="test-sync_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_nodes.assert_called_once()

def test_list_nodes_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_nodes_summary
    mock_client = MagicMock()
    mock_client.list_nodes_summary.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_nodes_summary("test-aggregators", sync_name="test-sync_name", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_nodes_summary.assert_called_once()

def test_list_ops_item_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_ops_item_events
    mock_client = MagicMock()
    mock_client.list_ops_item_events.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_item_events(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_ops_item_events.assert_called_once()

def test_list_ops_item_related_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_ops_item_related_items
    mock_client = MagicMock()
    mock_client.list_ops_item_related_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_item_related_items(ops_item_id="test-ops_item_id", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_ops_item_related_items.assert_called_once()

def test_list_ops_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_ops_metadata
    mock_client = MagicMock()
    mock_client.list_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_ops_metadata(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_ops_metadata.assert_called_once()

def test_list_resource_compliance_summaries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_resource_compliance_summaries
    mock_client = MagicMock()
    mock_client.list_resource_compliance_summaries.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_resource_compliance_summaries(filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_resource_compliance_summaries.assert_called_once()

def test_list_resource_data_sync_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import list_resource_data_sync
    mock_client = MagicMock()
    mock_client.list_resource_data_sync.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    list_resource_data_sync(sync_type="test-sync_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_resource_data_sync.assert_called_once()

def test_modify_document_permission_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import modify_document_permission
    mock_client = MagicMock()
    mock_client.modify_document_permission.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    modify_document_permission("test-name", "test-permission_type", account_ids_to_add=1, account_ids_to_remove=1, shared_document_version="test-shared_document_version", region_name="us-east-1")
    mock_client.modify_document_permission.assert_called_once()

def test_put_compliance_items_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import put_compliance_items
    mock_client = MagicMock()
    mock_client.put_compliance_items.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    put_compliance_items("test-resource_id", "test-resource_type", "test-compliance_type", "test-execution_summary", "test-items", item_content_hash="test-item_content_hash", upload_type="test-upload_type", region_name="us-east-1")
    mock_client.put_compliance_items.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "{}", policy_id="test-policy_id", policy_hash="test-policy_hash", region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_register_target_with_maintenance_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import register_target_with_maintenance_window
    mock_client = MagicMock()
    mock_client.register_target_with_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_target_with_maintenance_window("test-window_id", "test-resource_type", "test-targets", owner_information="test-owner_information", name="test-name", description="test-description", client_token="test-client_token", region_name="us-east-1")
    mock_client.register_target_with_maintenance_window.assert_called_once()

def test_register_task_with_maintenance_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import register_task_with_maintenance_window
    mock_client = MagicMock()
    mock_client.register_task_with_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    register_task_with_maintenance_window("test-window_id", "test-task_arn", "test-task_type", targets="test-targets", service_role_arn="test-service_role_arn", task_parameters="test-task_parameters", task_invocation_parameters="test-task_invocation_parameters", priority="test-priority", max_concurrency=1, max_errors=1, logging_info="test-logging_info", name="test-name", description="test-description", client_token="test-client_token", cutoff_behavior="test-cutoff_behavior", alarm_configuration={}, region_name="us-east-1")
    mock_client.register_task_with_maintenance_window.assert_called_once()

def test_send_automation_signal_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import send_automation_signal
    mock_client = MagicMock()
    mock_client.send_automation_signal.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    send_automation_signal(True, "test-signal_type", payload="test-payload", region_name="us-east-1")
    mock_client.send_automation_signal.assert_called_once()

def test_send_command_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import send_command
    mock_client = MagicMock()
    mock_client.send_command.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    send_command("test-document_name", instance_ids="test-instance_ids", targets="test-targets", document_version="test-document_version", document_hash="test-document_hash", document_hash_type="test-document_hash_type", timeout_seconds=1, comment="test-comment", parameters="test-parameters", output_s3_region="test-output_s3_region", output_s3_bucket_name="test-output_s3_bucket_name", output_s3_key_prefix="test-output_s3_key_prefix", max_concurrency=1, max_errors=1, service_role_arn="test-service_role_arn", notification_config={}, cloud_watch_output_config={}, alarm_configuration={}, region_name="us-east-1")
    mock_client.send_command.assert_called_once()

def test_start_access_request_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import start_access_request
    mock_client = MagicMock()
    mock_client.start_access_request.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_access_request("test-reason", "test-targets", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_access_request.assert_called_once()

def test_start_automation_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import start_automation_execution
    mock_client = MagicMock()
    mock_client.start_automation_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_automation_execution("test-document_name", document_version="test-document_version", parameters="test-parameters", client_token="test-client_token", mode="test-mode", target_parameter_name="test-target_parameter_name", targets="test-targets", target_maps="test-target_maps", max_concurrency=1, max_errors=1, target_locations="test-target_locations", tags=[{"Key": "k", "Value": "v"}], alarm_configuration={}, target_locations_url="test-target_locations_url", region_name="us-east-1")
    mock_client.start_automation_execution.assert_called_once()

def test_start_change_request_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import start_change_request_execution
    mock_client = MagicMock()
    mock_client.start_change_request_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_change_request_execution("test-document_name", "test-runbooks", scheduled_time="test-scheduled_time", document_version="test-document_version", parameters="test-parameters", change_request_name="test-change_request_name", client_token="test-client_token", auto_approve=True, tags=[{"Key": "k", "Value": "v"}], scheduled_end_time="test-scheduled_end_time", change_details="test-change_details", region_name="us-east-1")
    mock_client.start_change_request_execution.assert_called_once()

def test_start_execution_preview_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import start_execution_preview
    mock_client = MagicMock()
    mock_client.start_execution_preview.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_execution_preview("test-document_name", document_version="test-document_version", execution_inputs="test-execution_inputs", region_name="us-east-1")
    mock_client.start_execution_preview.assert_called_once()

def test_start_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import start_session
    mock_client = MagicMock()
    mock_client.start_session.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    start_session("test-target", document_name="test-document_name", reason="test-reason", parameters="test-parameters", region_name="us-east-1")
    mock_client.start_session.assert_called_once()

def test_stop_automation_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import stop_automation_execution
    mock_client = MagicMock()
    mock_client.stop_automation_execution.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    stop_automation_execution(True, type_value="test-type_value", region_name="us-east-1")
    mock_client.stop_automation_execution.assert_called_once()

def test_update_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_association
    mock_client = MagicMock()
    mock_client.update_association.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_association("test-association_id", parameters="test-parameters", document_version="test-document_version", schedule_expression="test-schedule_expression", output_location="test-output_location", name="test-name", targets="test-targets", association_name="test-association_name", association_version="test-association_version", automation_target_parameter_name=True, max_errors=1, max_concurrency=1, compliance_severity="test-compliance_severity", sync_compliance="test-sync_compliance", apply_only_at_cron_interval=True, calendar_names="test-calendar_names", target_locations="test-target_locations", schedule_offset="test-schedule_offset", duration=1, target_maps="test-target_maps", alarm_configuration={}, region_name="us-east-1")
    mock_client.update_association.assert_called_once()

def test_update_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_document
    mock_client = MagicMock()
    mock_client.update_document.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_document("test-content", "test-name", attachments="test-attachments", display_name="test-display_name", version_name="test-version_name", document_version="test-document_version", document_format="test-document_format", target_type="test-target_type", region_name="us-east-1")
    mock_client.update_document.assert_called_once()

def test_update_document_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_document_metadata
    mock_client = MagicMock()
    mock_client.update_document_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_document_metadata("test-name", "test-document_reviews", document_version="test-document_version", region_name="us-east-1")
    mock_client.update_document_metadata.assert_called_once()

def test_update_maintenance_window_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_maintenance_window
    mock_client = MagicMock()
    mock_client.update_maintenance_window.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window("test-window_id", name="test-name", description="test-description", start_date="test-start_date", end_date="test-end_date", schedule="test-schedule", schedule_timezone="test-schedule_timezone", schedule_offset="test-schedule_offset", duration=1, cutoff="test-cutoff", allow_unassociated_targets=True, enabled=True, replace="test-replace", region_name="us-east-1")
    mock_client.update_maintenance_window.assert_called_once()

def test_update_maintenance_window_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_maintenance_window_target
    mock_client = MagicMock()
    mock_client.update_maintenance_window_target.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window_target("test-window_id", "test-window_target_id", targets="test-targets", owner_information="test-owner_information", name="test-name", description="test-description", replace="test-replace", region_name="us-east-1")
    mock_client.update_maintenance_window_target.assert_called_once()

def test_update_maintenance_window_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_maintenance_window_task
    mock_client = MagicMock()
    mock_client.update_maintenance_window_task.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_maintenance_window_task("test-window_id", "test-window_task_id", targets="test-targets", task_arn="test-task_arn", service_role_arn="test-service_role_arn", task_parameters="test-task_parameters", task_invocation_parameters="test-task_invocation_parameters", priority="test-priority", max_concurrency=1, max_errors=1, logging_info="test-logging_info", name="test-name", description="test-description", replace="test-replace", cutoff_behavior="test-cutoff_behavior", alarm_configuration={}, region_name="us-east-1")
    mock_client.update_maintenance_window_task.assert_called_once()

def test_update_ops_item_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_ops_item
    mock_client = MagicMock()
    mock_client.update_ops_item.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_ops_item("test-ops_item_id", description="test-description", operational_data="test-operational_data", operational_data_to_delete="test-operational_data_to_delete", notifications="test-notifications", priority="test-priority", related_ops_items="test-related_ops_items", status="test-status", title="test-title", category="test-category", severity="test-severity", actual_start_time="test-actual_start_time", actual_end_time="test-actual_end_time", planned_start_time="test-planned_start_time", planned_end_time="test-planned_end_time", ops_item_arn="test-ops_item_arn", region_name="us-east-1")
    mock_client.update_ops_item.assert_called_once()

def test_update_ops_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_ops_metadata
    mock_client = MagicMock()
    mock_client.update_ops_metadata.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_ops_metadata("test-ops_metadata_arn", metadata_to_update="test-metadata_to_update", keys_to_delete="test-keys_to_delete", region_name="us-east-1")
    mock_client.update_ops_metadata.assert_called_once()

def test_update_patch_baseline_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.parameter_store import update_patch_baseline
    mock_client = MagicMock()
    mock_client.update_patch_baseline.return_value = {}
    monkeypatch.setattr("aws_util.parameter_store.get_client", lambda *a, **kw: mock_client)
    update_patch_baseline("test-baseline_id", name="test-name", global_filters="test-global_filters", approval_rules="test-approval_rules", approved_patches=True, approved_patches_compliance_level=True, approved_patches_enable_non_security=True, rejected_patches="test-rejected_patches", rejected_patches_action="test-rejected_patches_action", description="test-description", sources="test-sources", available_security_updates_compliance_status="test-available_security_updates_compliance_status", replace="test-replace", region_name="us-east-1")
    mock_client.update_patch_baseline.assert_called_once()
