"""Tests for aws_util.cloudformation module."""
from __future__ import annotations

import json
import pytest
import boto3
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

import aws_util.cloudformation as cfn_mod
from aws_util.cloudformation import (
    CFNStack,
    describe_stack,
    list_stacks,
    get_stack_outputs,
    create_stack,
    update_stack,
    delete_stack,
    wait_for_stack,
    deploy_stack,
    get_export_value,
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

REGION = "us-east-1"
STACK_NAME = "test-stack"
TEMPLATE = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
        }
    },
}


# ---------------------------------------------------------------------------
# CFNStack model
# ---------------------------------------------------------------------------

def test_cfnstack_is_stable():
    stack = CFNStack(stack_id="arn:...", stack_name="s", status="CREATE_COMPLETE")
    assert stack.is_stable is True
    assert stack.is_healthy is True


def test_cfnstack_not_stable():
    stack = CFNStack(stack_id="arn:...", stack_name="s", status="CREATE_IN_PROGRESS")
    assert stack.is_stable is False
    assert stack.is_healthy is False


def test_cfnstack_failed_is_stable_not_healthy():
    stack = CFNStack(stack_id="arn:...", stack_name="s", status="CREATE_FAILED")
    assert stack.is_stable is True
    assert stack.is_healthy is False


# ---------------------------------------------------------------------------
# describe_stack
# ---------------------------------------------------------------------------

def test_describe_stack_returns_stack(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    client.create_stack(StackName=STACK_NAME, TemplateBody=json.dumps(TEMPLATE))
    result = describe_stack(STACK_NAME, region_name=REGION)
    assert result is not None
    assert result.stack_name == STACK_NAME


def test_describe_stack_returns_none_when_not_exists(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stacks.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "Stack nonexistent does not exist"}},
        "DescribeStacks",
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_stack("nonexistent", region_name=REGION)
    assert result is None


def test_describe_stack_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stacks.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}}, "DescribeStacks"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_stack failed"):
        describe_stack("any-stack", region_name=REGION)


# ---------------------------------------------------------------------------
# list_stacks
# ---------------------------------------------------------------------------

def test_list_stacks_returns_list(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    client.create_stack(StackName=STACK_NAME, TemplateBody=json.dumps(TEMPLATE))
    result = list_stacks(region_name=REGION)
    assert isinstance(result, list)
    assert any(s.stack_name == STACK_NAME for s in result)


def test_list_stacks_with_status_filter(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    client.create_stack(StackName=STACK_NAME, TemplateBody=json.dumps(TEMPLATE))
    result = list_stacks(status_filter=["CREATE_COMPLETE"], region_name=REGION)
    assert isinstance(result, list)


def test_list_stacks_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}}, "ListStacks"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_stacks failed"):
        list_stacks(region_name=REGION)


# ---------------------------------------------------------------------------
# get_stack_outputs
# ---------------------------------------------------------------------------

def test_get_stack_outputs_returns_dict(monkeypatch):
    stack = CFNStack(
        stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_COMPLETE",
        outputs={"MyKey": "MyValue"},
    )
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: stack)
    result = get_stack_outputs(STACK_NAME, region_name=REGION)
    assert result["MyKey"] == "MyValue"


def test_get_stack_outputs_raises_when_not_found(monkeypatch):
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: None)
    with pytest.raises(RuntimeError, match="not found"):
        get_stack_outputs("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# create_stack
# ---------------------------------------------------------------------------

def test_create_stack_returns_stack_id(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    stack_id = create_stack(STACK_NAME, TEMPLATE, region_name=REGION)
    assert "arn:aws:cloudformation" in stack_id


def test_create_stack_with_dict_template(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    stack_id = create_stack("dict-stack", TEMPLATE, region_name=REGION)
    assert stack_id


def test_create_stack_with_parameters_and_tags(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    stack_id = create_stack(
        "param-stack", TEMPLATE,
        tags={"env": "test"},
        region_name=REGION,
    )
    assert stack_id


def test_create_stack_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack.side_effect = ClientError(
        {"Error": {"Code": "AlreadyExistsException", "Message": "already exists"}}, "CreateStack"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stack"):
        create_stack(STACK_NAME, TEMPLATE, region_name=REGION)


# ---------------------------------------------------------------------------
# update_stack
# ---------------------------------------------------------------------------

def test_update_stack_returns_stack_id(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    client.create_stack(StackName=STACK_NAME, TemplateBody=json.dumps(TEMPLATE))
    # moto returns stack ID on update
    try:
        stack_id = update_stack(STACK_NAME, TEMPLATE, region_name=REGION)
        assert stack_id
    except RuntimeError:
        pass  # "No updates" is fine


def test_update_stack_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stack.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "does not exist"}}, "UpdateStack"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stack"):
        update_stack("nonexistent", TEMPLATE, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_stack
# ---------------------------------------------------------------------------

def test_delete_stack_succeeds(monkeypatch):
    client = boto3.client("cloudformation", region_name=REGION)
    client.create_stack(StackName=STACK_NAME, TemplateBody=json.dumps(TEMPLATE))
    delete_stack(STACK_NAME, region_name=REGION)


def test_delete_stack_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stack.side_effect = ClientError(
        {"Error": {"Code": "ValidationError", "Message": "not found"}}, "DeleteStack"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stack"):
        delete_stack("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_stack
# ---------------------------------------------------------------------------

def test_wait_for_stack_immediately_stable(monkeypatch):
    stable_stack = CFNStack(
        stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_COMPLETE"
    )
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: stable_stack)
    result = wait_for_stack(STACK_NAME, timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.is_stable


def test_wait_for_stack_not_found(monkeypatch):
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: None)
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_stack(STACK_NAME, timeout=1.0, region_name=REGION)


def test_wait_for_stack_timeout(monkeypatch):
    in_progress = CFNStack(
        stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_IN_PROGRESS"
    )
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: in_progress)
    with pytest.raises(TimeoutError):
        wait_for_stack(STACK_NAME, timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# deploy_stack
# ---------------------------------------------------------------------------

def test_deploy_stack_creates_new(monkeypatch):
    stable = CFNStack(stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_COMPLETE")
    monkeypatch.setattr(cfn_mod, "describe_stack",
                        lambda name, region_name=None: None if name == STACK_NAME else stable)
    monkeypatch.setattr(cfn_mod, "create_stack", lambda *a, **kw: "arn:stack-id")
    monkeypatch.setattr(cfn_mod, "wait_for_stack", lambda *a, **kw: stable)
    result = deploy_stack(STACK_NAME, TEMPLATE, region_name=REGION)
    assert result.is_healthy


def test_deploy_stack_updates_existing(monkeypatch):
    existing = CFNStack(stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_COMPLETE")
    stable = CFNStack(stack_id="arn:...", stack_name=STACK_NAME, status="UPDATE_COMPLETE")
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: existing)
    monkeypatch.setattr(cfn_mod, "update_stack", lambda *a, **kw: "arn:stack-id")
    monkeypatch.setattr(cfn_mod, "wait_for_stack", lambda *a, **kw: stable)
    result = deploy_stack(STACK_NAME, TEMPLATE, region_name=REGION)
    assert result.is_healthy


def test_deploy_stack_no_update(monkeypatch):
    existing = CFNStack(stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_COMPLETE")
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: existing)
    monkeypatch.setattr(cfn_mod, "update_stack",
                        lambda *a, **kw: (_ for _ in ()).throw(
                            RuntimeError("No updates are to be performed")))
    result = deploy_stack(STACK_NAME, TEMPLATE, region_name=REGION)
    assert result.stack_name == STACK_NAME


def test_deploy_stack_unhealthy_raises(monkeypatch):
    monkeypatch.setattr(cfn_mod, "describe_stack", lambda name, region_name=None: None)
    monkeypatch.setattr(cfn_mod, "create_stack", lambda *a, **kw: "arn:stack-id")
    failed = CFNStack(
        stack_id="arn:...", stack_name=STACK_NAME, status="CREATE_FAILED",
        status_reason="Template error"
    )
    monkeypatch.setattr(cfn_mod, "wait_for_stack", lambda *a, **kw: failed)
    with pytest.raises(RuntimeError, match="deployment failed"):
        deploy_stack(STACK_NAME, TEMPLATE, region_name=REGION)


# ---------------------------------------------------------------------------
# get_export_value
# ---------------------------------------------------------------------------

def test_get_export_value_found(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {"Exports": [{"Name": "MyExport", "Value": "MyValue"}]}
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_export_value("MyExport", region_name=REGION)
    assert result == "MyValue"


def test_get_export_value_not_found(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"Exports": []}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(KeyError):
        get_export_value("NonexistentExport", region_name=REGION)


def test_get_export_value_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}}, "ListExports"
    )
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_export_value failed"):
        get_export_value("AnyExport", region_name=REGION)


def test_create_stack_with_parameters(monkeypatch):
    """Covers parameters kwarg in create_stack (lines 206-208)."""
    mock_client = MagicMock()
    mock_client.create_stack.return_value = {"StackId": "arn:stack:1"}
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    stack_id = create_stack(
        STACK_NAME, TEMPLATE,
        parameters={"Env": "prod", "Region": "us-east-1"},
        region_name=REGION,
    )
    assert stack_id == "arn:stack:1"
    call_kwargs = mock_client.create_stack.call_args[1]
    assert "Parameters" in call_kwargs


def test_update_stack_with_parameters(monkeypatch):
    """Covers parameters kwarg in update_stack (lines 251-253)."""
    mock_client = MagicMock()
    mock_client.update_stack.return_value = {"StackId": "arn:stack:1"}
    monkeypatch.setattr(cfn_mod, "get_client", lambda *a, **kw: mock_client)
    stack_id = update_stack(
        STACK_NAME, TEMPLATE,
        parameters={"Env": "prod"},
        region_name=REGION,
    )
    assert stack_id == "arn:stack:1"
    call_kwargs = mock_client.update_stack.call_args[1]
    assert "Parameters" in call_kwargs


def test_wait_for_stack_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_stack (line 314)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    call_count = {"n": 0}

    def fake_describe(stack_name, region_name=None):
        from aws_util.cloudformation import CFNStack
        call_count["n"] += 1
        if call_count["n"] < 2:
            return CFNStack(stack_id="arn:1", stack_name=stack_name, status="UPDATE_IN_PROGRESS")
        return CFNStack(stack_id="arn:1", stack_name=stack_name, status="UPDATE_COMPLETE")

    monkeypatch.setattr(cfn_mod, "describe_stack", fake_describe)
    from aws_util.cloudformation import wait_for_stack
    result = wait_for_stack(STACK_NAME, timeout=10.0, poll_interval=0.001, region_name=REGION)
    assert result.status == "UPDATE_COMPLETE"


def test_deploy_or_update_stack_update_non_noop_error(monkeypatch):
    """Covers re-raise when update error is not 'No updates' (line 400)."""
    def fake_describe(stack_name, region_name=None):
        from aws_util.cloudformation import CFNStack
        return CFNStack(stack_id="arn:1", stack_name=stack_name, status="UPDATE_COMPLETE")

    def fake_update(stack_name, *a, **kw):
        raise RuntimeError("Some other error occurred")

    monkeypatch.setattr(cfn_mod, "describe_stack", fake_describe)
    monkeypatch.setattr(cfn_mod, "update_stack", fake_update)
    monkeypatch.setattr(cfn_mod, "wait_for_stack", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("unreachable")))
    from aws_util.cloudformation import deploy_stack
    with pytest.raises(RuntimeError, match="Some other error"):
        deploy_stack(
            STACK_NAME, TEMPLATE,
            region_name=REGION,
        )


def test_activate_organizations_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    activate_organizations_access(region_name=REGION)
    mock_client.activate_organizations_access.assert_called_once()


def test_activate_organizations_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_organizations_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "activate_organizations_access",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to activate organizations access"):
        activate_organizations_access(region_name=REGION)


def test_activate_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    activate_type(region_name=REGION)
    mock_client.activate_type.assert_called_once()


def test_activate_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "activate_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to activate type"):
        activate_type(region_name=REGION)


def test_batch_describe_type_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_describe_type_configurations.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    batch_describe_type_configurations([], region_name=REGION)
    mock_client.batch_describe_type_configurations.assert_called_once()


def test_batch_describe_type_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_describe_type_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_describe_type_configurations",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch describe type configurations"):
        batch_describe_type_configurations([], region_name=REGION)


def test_cancel_update_stack(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_update_stack.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    cancel_update_stack("test-stack_name", region_name=REGION)
    mock_client.cancel_update_stack.assert_called_once()


def test_cancel_update_stack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_update_stack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_update_stack",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel update stack"):
        cancel_update_stack("test-stack_name", region_name=REGION)


def test_continue_update_rollback(monkeypatch):
    mock_client = MagicMock()
    mock_client.continue_update_rollback.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    continue_update_rollback("test-stack_name", region_name=REGION)
    mock_client.continue_update_rollback.assert_called_once()


def test_continue_update_rollback_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.continue_update_rollback.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "continue_update_rollback",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to continue update rollback"):
        continue_update_rollback("test-stack_name", region_name=REGION)


def test_create_change_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_change_set("test-stack_name", "test-change_set_name", region_name=REGION)
    mock_client.create_change_set.assert_called_once()


def test_create_change_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_change_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_change_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create change set"):
        create_change_set("test-stack_name", "test-change_set_name", region_name=REGION)


def test_create_generated_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_generated_template("test-generated_template_name", region_name=REGION)
    mock_client.create_generated_template.assert_called_once()


def test_create_generated_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_generated_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_generated_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create generated template"):
        create_generated_template("test-generated_template_name", region_name=REGION)


def test_create_stack_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_instances("test-stack_set_name", [], region_name=REGION)
    mock_client.create_stack_instances.assert_called_once()


def test_create_stack_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stack_instances",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stack instances"):
        create_stack_instances("test-stack_set_name", [], region_name=REGION)


def test_create_stack_refactor(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_refactor.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_refactor([], region_name=REGION)
    mock_client.create_stack_refactor.assert_called_once()


def test_create_stack_refactor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_refactor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stack_refactor",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stack refactor"):
        create_stack_refactor([], region_name=REGION)


def test_create_stack_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_set("test-stack_set_name", region_name=REGION)
    mock_client.create_stack_set.assert_called_once()


def test_create_stack_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stack_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stack_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stack set"):
        create_stack_set("test-stack_set_name", region_name=REGION)


def test_deactivate_organizations_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    deactivate_organizations_access(region_name=REGION)
    mock_client.deactivate_organizations_access.assert_called_once()


def test_deactivate_organizations_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_organizations_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_organizations_access",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate organizations access"):
        deactivate_organizations_access(region_name=REGION)


def test_deactivate_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    deactivate_type(region_name=REGION)
    mock_client.deactivate_type.assert_called_once()


def test_deactivate_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate type"):
        deactivate_type(region_name=REGION)


def test_delete_change_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_change_set("test-change_set_name", region_name=REGION)
    mock_client.delete_change_set.assert_called_once()


def test_delete_change_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_change_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_change_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete change set"):
        delete_change_set("test-change_set_name", region_name=REGION)


def test_delete_generated_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_generated_template("test-generated_template_name", region_name=REGION)
    mock_client.delete_generated_template.assert_called_once()


def test_delete_generated_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_generated_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_generated_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete generated template"):
        delete_generated_template("test-generated_template_name", region_name=REGION)


def test_delete_stack_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_stack_instances("test-stack_set_name", [], True, region_name=REGION)
    mock_client.delete_stack_instances.assert_called_once()


def test_delete_stack_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stack_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stack_instances",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stack instances"):
        delete_stack_instances("test-stack_set_name", [], True, region_name=REGION)


def test_delete_stack_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_stack_set("test-stack_set_name", region_name=REGION)
    mock_client.delete_stack_set.assert_called_once()


def test_delete_stack_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stack_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stack_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stack set"):
        delete_stack_set("test-stack_set_name", region_name=REGION)


def test_deregister_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    deregister_type(region_name=REGION)
    mock_client.deregister_type.assert_called_once()


def test_deregister_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister type"):
        deregister_type(region_name=REGION)


def test_describe_account_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_account_limits(region_name=REGION)
    mock_client.describe_account_limits.assert_called_once()


def test_describe_account_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_limits",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account limits"):
        describe_account_limits(region_name=REGION)


def test_describe_change_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_change_set("test-change_set_name", region_name=REGION)
    mock_client.describe_change_set.assert_called_once()


def test_describe_change_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_change_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_change_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe change set"):
        describe_change_set("test-change_set_name", region_name=REGION)


def test_describe_change_set_hooks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_change_set_hooks.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_change_set_hooks("test-change_set_name", region_name=REGION)
    mock_client.describe_change_set_hooks.assert_called_once()


def test_describe_change_set_hooks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_change_set_hooks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_change_set_hooks",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe change set hooks"):
        describe_change_set_hooks("test-change_set_name", region_name=REGION)


def test_describe_generated_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_generated_template("test-generated_template_name", region_name=REGION)
    mock_client.describe_generated_template.assert_called_once()


def test_describe_generated_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_generated_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_generated_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe generated template"):
        describe_generated_template("test-generated_template_name", region_name=REGION)


def test_describe_organizations_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_organizations_access(region_name=REGION)
    mock_client.describe_organizations_access.assert_called_once()


def test_describe_organizations_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organizations_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organizations_access",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organizations access"):
        describe_organizations_access(region_name=REGION)


def test_describe_publisher(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_publisher.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_publisher(region_name=REGION)
    mock_client.describe_publisher.assert_called_once()


def test_describe_publisher_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_publisher.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_publisher",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe publisher"):
        describe_publisher(region_name=REGION)


def test_describe_resource_scan(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_scan.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_resource_scan("test-resource_scan_id", region_name=REGION)
    mock_client.describe_resource_scan.assert_called_once()


def test_describe_resource_scan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_scan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resource_scan",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe resource scan"):
        describe_resource_scan("test-resource_scan_id", region_name=REGION)


def test_describe_stack_drift_detection_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_drift_detection_status.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_drift_detection_status("test-stack_drift_detection_id", region_name=REGION)
    mock_client.describe_stack_drift_detection_status.assert_called_once()


def test_describe_stack_drift_detection_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_drift_detection_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_drift_detection_status",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack drift detection status"):
        describe_stack_drift_detection_status("test-stack_drift_detection_id", region_name=REGION)


def test_describe_stack_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_events.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_events("test-stack_name", region_name=REGION)
    mock_client.describe_stack_events.assert_called_once()


def test_describe_stack_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_events",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack events"):
        describe_stack_events("test-stack_name", region_name=REGION)


def test_describe_stack_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_instance.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_instance("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", region_name=REGION)
    mock_client.describe_stack_instance.assert_called_once()


def test_describe_stack_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_instance",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack instance"):
        describe_stack_instance("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", region_name=REGION)


def test_describe_stack_refactor(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_refactor.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_refactor("test-stack_refactor_id", region_name=REGION)
    mock_client.describe_stack_refactor.assert_called_once()


def test_describe_stack_refactor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_refactor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_refactor",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack refactor"):
        describe_stack_refactor("test-stack_refactor_id", region_name=REGION)


def test_describe_stack_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_resource("test-stack_name", "test-logical_resource_id", region_name=REGION)
    mock_client.describe_stack_resource.assert_called_once()


def test_describe_stack_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_resource",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack resource"):
        describe_stack_resource("test-stack_name", "test-logical_resource_id", region_name=REGION)


def test_describe_stack_resource_drifts(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resource_drifts.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_resource_drifts("test-stack_name", region_name=REGION)
    mock_client.describe_stack_resource_drifts.assert_called_once()


def test_describe_stack_resource_drifts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resource_drifts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_resource_drifts",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack resource drifts"):
        describe_stack_resource_drifts("test-stack_name", region_name=REGION)


def test_describe_stack_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_resources(region_name=REGION)
    mock_client.describe_stack_resources.assert_called_once()


def test_describe_stack_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_resources",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack resources"):
        describe_stack_resources(region_name=REGION)


def test_describe_stack_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_set("test-stack_set_name", region_name=REGION)
    mock_client.describe_stack_set.assert_called_once()


def test_describe_stack_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack set"):
        describe_stack_set("test-stack_set_name", region_name=REGION)


def test_describe_stack_set_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_set_operation.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_set_operation("test-stack_set_name", "test-operation_id", region_name=REGION)
    mock_client.describe_stack_set_operation.assert_called_once()


def test_describe_stack_set_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stack_set_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stack_set_operation",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stack set operation"):
        describe_stack_set_operation("test-stack_set_name", "test-operation_id", region_name=REGION)


def test_describe_stacks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stacks.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stacks(region_name=REGION)
    mock_client.describe_stacks.assert_called_once()


def test_describe_stacks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stacks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stacks",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stacks"):
        describe_stacks(region_name=REGION)


def test_describe_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_type(region_name=REGION)
    mock_client.describe_type.assert_called_once()


def test_describe_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe type"):
        describe_type(region_name=REGION)


def test_describe_type_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_type_registration.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_type_registration("test-registration_token", region_name=REGION)
    mock_client.describe_type_registration.assert_called_once()


def test_describe_type_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_type_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_type_registration",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe type registration"):
        describe_type_registration("test-registration_token", region_name=REGION)


def test_detect_stack_drift(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_drift.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    detect_stack_drift("test-stack_name", region_name=REGION)
    mock_client.detect_stack_drift.assert_called_once()


def test_detect_stack_drift_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_drift.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_stack_drift",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect stack drift"):
        detect_stack_drift("test-stack_name", region_name=REGION)


def test_detect_stack_resource_drift(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_resource_drift.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    detect_stack_resource_drift("test-stack_name", "test-logical_resource_id", region_name=REGION)
    mock_client.detect_stack_resource_drift.assert_called_once()


def test_detect_stack_resource_drift_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_resource_drift.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_stack_resource_drift",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect stack resource drift"):
        detect_stack_resource_drift("test-stack_name", "test-logical_resource_id", region_name=REGION)


def test_detect_stack_set_drift(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_set_drift.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    detect_stack_set_drift("test-stack_set_name", region_name=REGION)
    mock_client.detect_stack_set_drift.assert_called_once()


def test_detect_stack_set_drift_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detect_stack_set_drift.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detect_stack_set_drift",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detect stack set drift"):
        detect_stack_set_drift("test-stack_set_name", region_name=REGION)


def test_estimate_template_cost(monkeypatch):
    mock_client = MagicMock()
    mock_client.estimate_template_cost.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    estimate_template_cost(region_name=REGION)
    mock_client.estimate_template_cost.assert_called_once()


def test_estimate_template_cost_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.estimate_template_cost.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "estimate_template_cost",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to estimate template cost"):
        estimate_template_cost(region_name=REGION)


def test_execute_change_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    execute_change_set("test-change_set_name", region_name=REGION)
    mock_client.execute_change_set.assert_called_once()


def test_execute_change_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_change_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_change_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute change set"):
        execute_change_set("test-change_set_name", region_name=REGION)


def test_execute_stack_refactor(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_stack_refactor.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    execute_stack_refactor("test-stack_refactor_id", region_name=REGION)
    mock_client.execute_stack_refactor.assert_called_once()


def test_execute_stack_refactor_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_stack_refactor.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_stack_refactor",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute stack refactor"):
        execute_stack_refactor("test-stack_refactor_id", region_name=REGION)


def test_get_generated_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_generated_template("test-generated_template_name", region_name=REGION)
    mock_client.get_generated_template.assert_called_once()


def test_get_generated_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_generated_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_generated_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get generated template"):
        get_generated_template("test-generated_template_name", region_name=REGION)


def test_get_hook_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hook_result.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_hook_result(region_name=REGION)
    mock_client.get_hook_result.assert_called_once()


def test_get_hook_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_hook_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_hook_result",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get hook result"):
        get_hook_result(region_name=REGION)


def test_get_stack_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stack_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_stack_policy("test-stack_name", region_name=REGION)
    mock_client.get_stack_policy.assert_called_once()


def test_get_stack_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stack_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_stack_policy",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get stack policy"):
        get_stack_policy("test-stack_name", region_name=REGION)


def test_get_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_template(region_name=REGION)
    mock_client.get_template.assert_called_once()


def test_get_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get template"):
        get_template(region_name=REGION)


def test_get_template_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template_summary.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_template_summary(region_name=REGION)
    mock_client.get_template_summary.assert_called_once()


def test_get_template_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_template_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_template_summary",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get template summary"):
        get_template_summary(region_name=REGION)


def test_import_stacks_to_stack_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_stacks_to_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    import_stacks_to_stack_set("test-stack_set_name", region_name=REGION)
    mock_client.import_stacks_to_stack_set.assert_called_once()


def test_import_stacks_to_stack_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_stacks_to_stack_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_stacks_to_stack_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import stacks to stack set"):
        import_stacks_to_stack_set("test-stack_set_name", region_name=REGION)


def test_list_change_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_change_sets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_change_sets("test-stack_name", region_name=REGION)
    mock_client.list_change_sets.assert_called_once()


def test_list_change_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_change_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_change_sets",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list change sets"):
        list_change_sets("test-stack_name", region_name=REGION)


def test_list_exports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_exports.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_exports(region_name=REGION)
    mock_client.list_exports.assert_called_once()


def test_list_exports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_exports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_exports",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list exports"):
        list_exports(region_name=REGION)


def test_list_generated_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_generated_templates.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_generated_templates(region_name=REGION)
    mock_client.list_generated_templates.assert_called_once()


def test_list_generated_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_generated_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_generated_templates",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list generated templates"):
        list_generated_templates(region_name=REGION)


def test_list_hook_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hook_results.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_hook_results(region_name=REGION)
    mock_client.list_hook_results.assert_called_once()


def test_list_hook_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hook_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_hook_results",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list hook results"):
        list_hook_results(region_name=REGION)


def test_list_imports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_imports("test-export_name", region_name=REGION)
    mock_client.list_imports.assert_called_once()


def test_list_imports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_imports",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list imports"):
        list_imports("test-export_name", region_name=REGION)


def test_list_resource_scan_related_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scan_related_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scan_related_resources("test-resource_scan_id", [], region_name=REGION)
    mock_client.list_resource_scan_related_resources.assert_called_once()


def test_list_resource_scan_related_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scan_related_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_scan_related_resources",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource scan related resources"):
        list_resource_scan_related_resources("test-resource_scan_id", [], region_name=REGION)


def test_list_resource_scan_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scan_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scan_resources("test-resource_scan_id", region_name=REGION)
    mock_client.list_resource_scan_resources.assert_called_once()


def test_list_resource_scan_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scan_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_scan_resources",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource scan resources"):
        list_resource_scan_resources("test-resource_scan_id", region_name=REGION)


def test_list_resource_scans(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scans.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scans(region_name=REGION)
    mock_client.list_resource_scans.assert_called_once()


def test_list_resource_scans_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_scans.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_scans",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource scans"):
        list_resource_scans(region_name=REGION)


def test_list_stack_instance_resource_drifts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_instance_resource_drifts.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_instance_resource_drifts("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", "test-operation_id", region_name=REGION)
    mock_client.list_stack_instance_resource_drifts.assert_called_once()


def test_list_stack_instance_resource_drifts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_instance_resource_drifts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_instance_resource_drifts",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack instance resource drifts"):
        list_stack_instance_resource_drifts("test-stack_set_name", "test-stack_instance_account", "test-stack_instance_region", "test-operation_id", region_name=REGION)


def test_list_stack_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_instances("test-stack_set_name", region_name=REGION)
    mock_client.list_stack_instances.assert_called_once()


def test_list_stack_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_instances",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack instances"):
        list_stack_instances("test-stack_set_name", region_name=REGION)


def test_list_stack_refactor_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_refactor_actions.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_refactor_actions("test-stack_refactor_id", region_name=REGION)
    mock_client.list_stack_refactor_actions.assert_called_once()


def test_list_stack_refactor_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_refactor_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_refactor_actions",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack refactor actions"):
        list_stack_refactor_actions("test-stack_refactor_id", region_name=REGION)


def test_list_stack_refactors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_refactors.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_refactors(region_name=REGION)
    mock_client.list_stack_refactors.assert_called_once()


def test_list_stack_refactors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_refactors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_refactors",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack refactors"):
        list_stack_refactors(region_name=REGION)


def test_list_stack_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_resources("test-stack_name", region_name=REGION)
    mock_client.list_stack_resources.assert_called_once()


def test_list_stack_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_resources",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack resources"):
        list_stack_resources("test-stack_name", region_name=REGION)


def test_list_stack_set_auto_deployment_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_auto_deployment_targets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_auto_deployment_targets("test-stack_set_name", region_name=REGION)
    mock_client.list_stack_set_auto_deployment_targets.assert_called_once()


def test_list_stack_set_auto_deployment_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_auto_deployment_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_set_auto_deployment_targets",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack set auto deployment targets"):
        list_stack_set_auto_deployment_targets("test-stack_set_name", region_name=REGION)


def test_list_stack_set_operation_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_operation_results.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_operation_results("test-stack_set_name", "test-operation_id", region_name=REGION)
    mock_client.list_stack_set_operation_results.assert_called_once()


def test_list_stack_set_operation_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_operation_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_set_operation_results",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack set operation results"):
        list_stack_set_operation_results("test-stack_set_name", "test-operation_id", region_name=REGION)


def test_list_stack_set_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_operations.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_operations("test-stack_set_name", region_name=REGION)
    mock_client.list_stack_set_operations.assert_called_once()


def test_list_stack_set_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_set_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_set_operations",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack set operations"):
        list_stack_set_operations("test-stack_set_name", region_name=REGION)


def test_list_stack_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_sets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_sets(region_name=REGION)
    mock_client.list_stack_sets.assert_called_once()


def test_list_stack_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stack_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stack_sets",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stack sets"):
        list_stack_sets(region_name=REGION)


def test_list_type_registrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_type_registrations.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_type_registrations(region_name=REGION)
    mock_client.list_type_registrations.assert_called_once()


def test_list_type_registrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_type_registrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_type_registrations",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list type registrations"):
        list_type_registrations(region_name=REGION)


def test_list_type_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_type_versions.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_type_versions(region_name=REGION)
    mock_client.list_type_versions.assert_called_once()


def test_list_type_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_type_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_type_versions",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list type versions"):
        list_type_versions(region_name=REGION)


def test_list_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_types.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_types(region_name=REGION)
    mock_client.list_types.assert_called_once()


def test_list_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_types",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list types"):
        list_types(region_name=REGION)


def test_publish_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    publish_type(region_name=REGION)
    mock_client.publish_type.assert_called_once()


def test_publish_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.publish_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "publish_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to publish type"):
        publish_type(region_name=REGION)


def test_record_handler_progress(monkeypatch):
    mock_client = MagicMock()
    mock_client.record_handler_progress.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    record_handler_progress("test-bearer_token", "test-operation_status", region_name=REGION)
    mock_client.record_handler_progress.assert_called_once()


def test_record_handler_progress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.record_handler_progress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "record_handler_progress",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to record handler progress"):
        record_handler_progress("test-bearer_token", "test-operation_status", region_name=REGION)


def test_register_publisher(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_publisher.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    register_publisher(region_name=REGION)
    mock_client.register_publisher.assert_called_once()


def test_register_publisher_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_publisher.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_publisher",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register publisher"):
        register_publisher(region_name=REGION)


def test_register_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    register_type("test-type_name", "test-schema_handler_package", region_name=REGION)
    mock_client.register_type.assert_called_once()


def test_register_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register type"):
        register_type("test-type_name", "test-schema_handler_package", region_name=REGION)


def test_rollback_stack(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_stack.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    rollback_stack("test-stack_name", region_name=REGION)
    mock_client.rollback_stack.assert_called_once()


def test_rollback_stack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_stack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rollback_stack",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rollback stack"):
        rollback_stack("test-stack_name", region_name=REGION)


def test_run_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    run_type(region_name=REGION)
    mock_client.test_type.assert_called_once()


def test_run_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_type",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run type"):
        run_type(region_name=REGION)


def test_set_stack_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_stack_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_stack_policy("test-stack_name", region_name=REGION)
    mock_client.set_stack_policy.assert_called_once()


def test_set_stack_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_stack_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_stack_policy",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set stack policy"):
        set_stack_policy("test-stack_name", region_name=REGION)


def test_set_type_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_type_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_type_configuration("test-configuration", region_name=REGION)
    mock_client.set_type_configuration.assert_called_once()


def test_set_type_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_type_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_type_configuration",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set type configuration"):
        set_type_configuration("test-configuration", region_name=REGION)


def test_set_type_default_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_type_default_version.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_type_default_version(region_name=REGION)
    mock_client.set_type_default_version.assert_called_once()


def test_set_type_default_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_type_default_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_type_default_version",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set type default version"):
        set_type_default_version(region_name=REGION)


def test_signal_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.signal_resource.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    signal_resource("test-stack_name", "test-logical_resource_id", "test-unique_id", "test-status", region_name=REGION)
    mock_client.signal_resource.assert_called_once()


def test_signal_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.signal_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "signal_resource",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to signal resource"):
        signal_resource("test-stack_name", "test-logical_resource_id", "test-unique_id", "test-status", region_name=REGION)


def test_start_resource_scan(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_resource_scan.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    start_resource_scan(region_name=REGION)
    mock_client.start_resource_scan.assert_called_once()


def test_start_resource_scan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_resource_scan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_resource_scan",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start resource scan"):
        start_resource_scan(region_name=REGION)


def test_stop_stack_set_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stack_set_operation.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    stop_stack_set_operation("test-stack_set_name", "test-operation_id", region_name=REGION)
    mock_client.stop_stack_set_operation.assert_called_once()


def test_stop_stack_set_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stack_set_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_stack_set_operation",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop stack set operation"):
        stop_stack_set_operation("test-stack_set_name", "test-operation_id", region_name=REGION)


def test_update_generated_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_generated_template("test-generated_template_name", region_name=REGION)
    mock_client.update_generated_template.assert_called_once()


def test_update_generated_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_generated_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_generated_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update generated template"):
        update_generated_template("test-generated_template_name", region_name=REGION)


def test_update_stack_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_stack_instances("test-stack_set_name", [], region_name=REGION)
    mock_client.update_stack_instances.assert_called_once()


def test_update_stack_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stack_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stack_instances",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stack instances"):
        update_stack_instances("test-stack_set_name", [], region_name=REGION)


def test_update_stack_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_stack_set("test-stack_set_name", region_name=REGION)
    mock_client.update_stack_set.assert_called_once()


def test_update_stack_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stack_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stack_set",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stack set"):
        update_stack_set("test-stack_set_name", region_name=REGION)


def test_update_termination_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_termination_protection.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_termination_protection(True, "test-stack_name", region_name=REGION)
    mock_client.update_termination_protection.assert_called_once()


def test_update_termination_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_termination_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_termination_protection",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update termination protection"):
        update_termination_protection(True, "test-stack_name", region_name=REGION)


def test_validate_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    validate_template(region_name=REGION)
    mock_client.validate_template.assert_called_once()


def test_validate_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.validate_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_template",
    )
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to validate template"):
        validate_template(region_name=REGION)


def test_activate_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import activate_type
    mock_client = MagicMock()
    mock_client.activate_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    activate_type(type_value="test-type_value", public_type_arn="test-public_type_arn", publisher_id=True, type_name="test-type_name", type_name_alias="test-type_name_alias", auto_update=True, logging_config={}, execution_role_arn="test-execution_role_arn", version_bump="test-version_bump", major_version="test-major_version", region_name="us-east-1")
    mock_client.activate_type.assert_called_once()

def test_cancel_update_stack_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import cancel_update_stack
    mock_client = MagicMock()
    mock_client.cancel_update_stack.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    cancel_update_stack("test-stack_name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.cancel_update_stack.assert_called_once()

def test_continue_update_rollback_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import continue_update_rollback
    mock_client = MagicMock()
    mock_client.continue_update_rollback.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    continue_update_rollback("test-stack_name", role_arn="test-role_arn", resources_to_skip="test-resources_to_skip", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.continue_update_rollback.assert_called_once()

def test_create_change_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import create_change_set
    mock_client = MagicMock()
    mock_client.create_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_change_set("test-stack_name", "test-change_set_name", template_body="test-template_body", template_url="test-template_url", use_previous_template=True, parameters="test-parameters", capabilities="test-capabilities", resource_types="test-resource_types", role_arn="test-role_arn", rollback_configuration={}, notification_ar_ns="test-notification_ar_ns", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", description="test-description", change_set_type="test-change_set_type", resources_to_import=1, include_nested_stacks=True, on_stack_failure="test-on_stack_failure", import_existing_resources=1, region_name="us-east-1")
    mock_client.create_change_set.assert_called_once()

def test_create_generated_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import create_generated_template
    mock_client = MagicMock()
    mock_client.create_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_generated_template("test-generated_template_name", resources="test-resources", stack_name="test-stack_name", template_configuration={}, region_name="us-east-1")
    mock_client.create_generated_template.assert_called_once()

def test_create_stack_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import create_stack_instances
    mock_client = MagicMock()
    mock_client.create_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_instances("test-stack_set_name", "test-regions", accounts=1, deployment_targets="test-deployment_targets", parameter_overrides="test-parameter_overrides", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.create_stack_instances.assert_called_once()

def test_create_stack_refactor_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import create_stack_refactor
    mock_client = MagicMock()
    mock_client.create_stack_refactor.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_refactor({}, description="test-description", enable_stack_creation=True, resource_mappings={}, region_name="us-east-1")
    mock_client.create_stack_refactor.assert_called_once()

def test_create_stack_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import create_stack_set
    mock_client = MagicMock()
    mock_client.create_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    create_stack_set("test-stack_set_name", description="test-description", template_body="test-template_body", template_url="test-template_url", stack_id="test-stack_id", parameters="test-parameters", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], administration_role_arn="test-administration_role_arn", execution_role_name="test-execution_role_name", permission_model="test-permission_model", auto_deployment=True, call_as="test-call_as", client_request_token="test-client_request_token", managed_execution="test-managed_execution", region_name="us-east-1")
    mock_client.create_stack_set.assert_called_once()

def test_deactivate_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import deactivate_type
    mock_client = MagicMock()
    mock_client.deactivate_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    deactivate_type(type_name="test-type_name", type_value="test-type_value", arn="test-arn", region_name="us-east-1")
    mock_client.deactivate_type.assert_called_once()

def test_delete_change_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import delete_change_set
    mock_client = MagicMock()
    mock_client.delete_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_change_set("test-change_set_name", stack_name="test-stack_name", region_name="us-east-1")
    mock_client.delete_change_set.assert_called_once()

def test_delete_stack_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import delete_stack_instances
    mock_client = MagicMock()
    mock_client.delete_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_stack_instances("test-stack_set_name", "test-regions", "test-retain_stacks", accounts=1, deployment_targets="test-deployment_targets", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.delete_stack_instances.assert_called_once()

def test_delete_stack_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import delete_stack_set
    mock_client = MagicMock()
    mock_client.delete_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    delete_stack_set("test-stack_set_name", call_as="test-call_as", region_name="us-east-1")
    mock_client.delete_stack_set.assert_called_once()

def test_deregister_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import deregister_type
    mock_client = MagicMock()
    mock_client.deregister_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    deregister_type(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", region_name="us-east-1")
    mock_client.deregister_type.assert_called_once()

def test_describe_account_limits_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_account_limits
    mock_client = MagicMock()
    mock_client.describe_account_limits.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_account_limits(next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_account_limits.assert_called_once()

def test_describe_change_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_change_set
    mock_client = MagicMock()
    mock_client.describe_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_change_set("test-change_set_name", stack_name="test-stack_name", next_token="test-next_token", include_property_values=True, region_name="us-east-1")
    mock_client.describe_change_set.assert_called_once()

def test_describe_change_set_hooks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_change_set_hooks
    mock_client = MagicMock()
    mock_client.describe_change_set_hooks.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_change_set_hooks("test-change_set_name", stack_name="test-stack_name", next_token="test-next_token", logical_resource_id="test-logical_resource_id", region_name="us-east-1")
    mock_client.describe_change_set_hooks.assert_called_once()

def test_describe_organizations_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_organizations_access
    mock_client = MagicMock()
    mock_client.describe_organizations_access.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_organizations_access(call_as="test-call_as", region_name="us-east-1")
    mock_client.describe_organizations_access.assert_called_once()

def test_describe_publisher_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_publisher
    mock_client = MagicMock()
    mock_client.describe_publisher.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_publisher(publisher_id=True, region_name="us-east-1")
    mock_client.describe_publisher.assert_called_once()

def test_describe_stack_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_events
    mock_client = MagicMock()
    mock_client.describe_stack_events.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_events("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_stack_events.assert_called_once()

def test_describe_stack_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_instance
    mock_client = MagicMock()
    mock_client.describe_stack_instance.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_instance("test-stack_set_name", 1, "test-stack_instance_region", call_as="test-call_as", region_name="us-east-1")
    mock_client.describe_stack_instance.assert_called_once()

def test_describe_stack_resource_drifts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_resource_drifts
    mock_client = MagicMock()
    mock_client.describe_stack_resource_drifts.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_resource_drifts("test-stack_name", stack_resource_drift_status_filters="test-stack_resource_drift_status_filters", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_stack_resource_drifts.assert_called_once()

def test_describe_stack_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_resources
    mock_client = MagicMock()
    mock_client.describe_stack_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_resources(stack_name="test-stack_name", logical_resource_id="test-logical_resource_id", physical_resource_id="test-physical_resource_id", region_name="us-east-1")
    mock_client.describe_stack_resources.assert_called_once()

def test_describe_stack_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_set
    mock_client = MagicMock()
    mock_client.describe_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_set("test-stack_set_name", call_as="test-call_as", region_name="us-east-1")
    mock_client.describe_stack_set.assert_called_once()

def test_describe_stack_set_operation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stack_set_operation
    mock_client = MagicMock()
    mock_client.describe_stack_set_operation.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stack_set_operation("test-stack_set_name", "test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.describe_stack_set_operation.assert_called_once()

def test_describe_stacks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_stacks
    mock_client = MagicMock()
    mock_client.describe_stacks.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_stacks(stack_name="test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_stacks.assert_called_once()

def test_describe_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import describe_type
    mock_client = MagicMock()
    mock_client.describe_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    describe_type(type_value="test-type_value", type_name="test-type_name", arn="test-arn", version_id="test-version_id", publisher_id=True, public_version_number="test-public_version_number", region_name="us-east-1")
    mock_client.describe_type.assert_called_once()

def test_detect_stack_drift_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import detect_stack_drift
    mock_client = MagicMock()
    mock_client.detect_stack_drift.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    detect_stack_drift("test-stack_name", logical_resource_ids="test-logical_resource_ids", region_name="us-east-1")
    mock_client.detect_stack_drift.assert_called_once()

def test_detect_stack_set_drift_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import detect_stack_set_drift
    mock_client = MagicMock()
    mock_client.detect_stack_set_drift.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    detect_stack_set_drift("test-stack_set_name", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.detect_stack_set_drift.assert_called_once()

def test_estimate_template_cost_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import estimate_template_cost
    mock_client = MagicMock()
    mock_client.estimate_template_cost.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    estimate_template_cost(template_body="test-template_body", template_url="test-template_url", parameters="test-parameters", region_name="us-east-1")
    mock_client.estimate_template_cost.assert_called_once()

def test_execute_change_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import execute_change_set
    mock_client = MagicMock()
    mock_client.execute_change_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    execute_change_set("test-change_set_name", stack_name="test-stack_name", client_request_token="test-client_request_token", disable_rollback=True, retain_except_on_create="test-retain_except_on_create", region_name="us-east-1")
    mock_client.execute_change_set.assert_called_once()

def test_get_generated_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import get_generated_template
    mock_client = MagicMock()
    mock_client.get_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_generated_template("test-generated_template_name", format="test-format", region_name="us-east-1")
    mock_client.get_generated_template.assert_called_once()

def test_get_hook_result_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import get_hook_result
    mock_client = MagicMock()
    mock_client.get_hook_result.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_hook_result(hook_result_id="test-hook_result_id", region_name="us-east-1")
    mock_client.get_hook_result.assert_called_once()

def test_get_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import get_template
    mock_client = MagicMock()
    mock_client.get_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_template(stack_name="test-stack_name", change_set_name="test-change_set_name", template_stage="test-template_stage", region_name="us-east-1")
    mock_client.get_template.assert_called_once()

def test_get_template_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import get_template_summary
    mock_client = MagicMock()
    mock_client.get_template_summary.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    get_template_summary(template_body="test-template_body", template_url="test-template_url", stack_name="test-stack_name", stack_set_name="test-stack_set_name", call_as="test-call_as", template_summary_config={}, region_name="us-east-1")
    mock_client.get_template_summary.assert_called_once()

def test_import_stacks_to_stack_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import import_stacks_to_stack_set
    mock_client = MagicMock()
    mock_client.import_stacks_to_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    import_stacks_to_stack_set("test-stack_set_name", stack_ids="test-stack_ids", stack_ids_url="test-stack_ids_url", organizational_unit_ids="test-organizational_unit_ids", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.import_stacks_to_stack_set.assert_called_once()

def test_list_change_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_change_sets
    mock_client = MagicMock()
    mock_client.list_change_sets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_change_sets("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_change_sets.assert_called_once()

def test_list_exports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_exports
    mock_client = MagicMock()
    mock_client.list_exports.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_exports(next_token="test-next_token", region_name="us-east-1")
    mock_client.list_exports.assert_called_once()

def test_list_generated_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_generated_templates
    mock_client = MagicMock()
    mock_client.list_generated_templates.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_generated_templates(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_generated_templates.assert_called_once()

def test_list_hook_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_hook_results
    mock_client = MagicMock()
    mock_client.list_hook_results.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_hook_results(target_type="test-target_type", target_id="test-target_id", type_arn="test-type_arn", status="test-status", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_hook_results.assert_called_once()

def test_list_imports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_imports
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_imports(1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_imports.assert_called_once()

def test_list_resource_scan_related_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_resource_scan_related_resources
    mock_client = MagicMock()
    mock_client.list_resource_scan_related_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scan_related_resources("test-resource_scan_id", "test-resources", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_resource_scan_related_resources.assert_called_once()

def test_list_resource_scan_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_resource_scan_resources
    mock_client = MagicMock()
    mock_client.list_resource_scan_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scan_resources("test-resource_scan_id", resource_identifier="test-resource_identifier", resource_type_prefix="test-resource_type_prefix", tag_key="test-tag_key", tag_value="test-tag_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_resource_scan_resources.assert_called_once()

def test_list_resource_scans_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_resource_scans
    mock_client = MagicMock()
    mock_client.list_resource_scans.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_resource_scans(next_token="test-next_token", max_results=1, scan_type_filter=[{}], region_name="us-east-1")
    mock_client.list_resource_scans.assert_called_once()

def test_list_stack_instance_resource_drifts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_instance_resource_drifts
    mock_client = MagicMock()
    mock_client.list_stack_instance_resource_drifts.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_instance_resource_drifts("test-stack_set_name", 1, "test-stack_instance_region", "test-operation_id", next_token="test-next_token", max_results=1, stack_instance_resource_drift_statuses="test-stack_instance_resource_drift_statuses", call_as="test-call_as", region_name="us-east-1")
    mock_client.list_stack_instance_resource_drifts.assert_called_once()

def test_list_stack_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_instances
    mock_client = MagicMock()
    mock_client.list_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_instances("test-stack_set_name", next_token="test-next_token", max_results=1, filters=[{}], stack_instance_account=1, stack_instance_region="test-stack_instance_region", call_as="test-call_as", region_name="us-east-1")
    mock_client.list_stack_instances.assert_called_once()

def test_list_stack_refactor_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_refactor_actions
    mock_client = MagicMock()
    mock_client.list_stack_refactor_actions.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_refactor_actions("test-stack_refactor_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_stack_refactor_actions.assert_called_once()

def test_list_stack_refactors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_refactors
    mock_client = MagicMock()
    mock_client.list_stack_refactors.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_refactors(execution_status_filter=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_stack_refactors.assert_called_once()

def test_list_stack_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_resources
    mock_client = MagicMock()
    mock_client.list_stack_resources.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_resources("test-stack_name", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_stack_resources.assert_called_once()

def test_list_stack_set_auto_deployment_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_set_auto_deployment_targets
    mock_client = MagicMock()
    mock_client.list_stack_set_auto_deployment_targets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_auto_deployment_targets("test-stack_set_name", next_token="test-next_token", max_results=1, call_as="test-call_as", region_name="us-east-1")
    mock_client.list_stack_set_auto_deployment_targets.assert_called_once()

def test_list_stack_set_operation_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_set_operation_results
    mock_client = MagicMock()
    mock_client.list_stack_set_operation_results.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_operation_results("test-stack_set_name", "test-operation_id", next_token="test-next_token", max_results=1, call_as="test-call_as", filters=[{}], region_name="us-east-1")
    mock_client.list_stack_set_operation_results.assert_called_once()

def test_list_stack_set_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_set_operations
    mock_client = MagicMock()
    mock_client.list_stack_set_operations.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_set_operations("test-stack_set_name", next_token="test-next_token", max_results=1, call_as="test-call_as", region_name="us-east-1")
    mock_client.list_stack_set_operations.assert_called_once()

def test_list_stack_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_stack_sets
    mock_client = MagicMock()
    mock_client.list_stack_sets.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_stack_sets(next_token="test-next_token", max_results=1, status="test-status", call_as="test-call_as", region_name="us-east-1")
    mock_client.list_stack_sets.assert_called_once()

def test_list_type_registrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_type_registrations
    mock_client = MagicMock()
    mock_client.list_type_registrations.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_type_registrations(type_value="test-type_value", type_name="test-type_name", type_arn="test-type_arn", registration_status_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_type_registrations.assert_called_once()

def test_list_type_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_type_versions
    mock_client = MagicMock()
    mock_client.list_type_versions.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_type_versions(type_value="test-type_value", type_name="test-type_name", arn="test-arn", max_results=1, next_token="test-next_token", deprecated_status="test-deprecated_status", publisher_id=True, region_name="us-east-1")
    mock_client.list_type_versions.assert_called_once()

def test_list_types_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import list_types
    mock_client = MagicMock()
    mock_client.list_types.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    list_types(visibility="test-visibility", provisioning_type="test-provisioning_type", deprecated_status="test-deprecated_status", type_value="test-type_value", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_types.assert_called_once()

def test_publish_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import publish_type
    mock_client = MagicMock()
    mock_client.publish_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    publish_type(type_value="test-type_value", arn="test-arn", type_name="test-type_name", public_version_number="test-public_version_number", region_name="us-east-1")
    mock_client.publish_type.assert_called_once()

def test_record_handler_progress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import record_handler_progress
    mock_client = MagicMock()
    mock_client.record_handler_progress.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    record_handler_progress("test-bearer_token", "test-operation_status", current_operation_status="test-current_operation_status", status_message="test-status_message", error_code="test-error_code", resource_model="test-resource_model", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.record_handler_progress.assert_called_once()

def test_register_publisher_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import register_publisher
    mock_client = MagicMock()
    mock_client.register_publisher.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    register_publisher(accept_terms_and_conditions="test-accept_terms_and_conditions", connection_arn="test-connection_arn", region_name="us-east-1")
    mock_client.register_publisher.assert_called_once()

def test_register_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import register_type
    mock_client = MagicMock()
    mock_client.register_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    register_type("test-type_name", "test-schema_handler_package", type_value="test-type_value", logging_config={}, execution_role_arn="test-execution_role_arn", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.register_type.assert_called_once()

def test_rollback_stack_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import rollback_stack
    mock_client = MagicMock()
    mock_client.rollback_stack.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    rollback_stack("test-stack_name", role_arn="test-role_arn", client_request_token="test-client_request_token", retain_except_on_create="test-retain_except_on_create", region_name="us-east-1")
    mock_client.rollback_stack.assert_called_once()

def test_run_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import run_type
    mock_client = MagicMock()
    mock_client.test_type.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    run_type(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", log_delivery_bucket="test-log_delivery_bucket", region_name="us-east-1")
    mock_client.test_type.assert_called_once()

def test_set_stack_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import set_stack_policy
    mock_client = MagicMock()
    mock_client.set_stack_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_stack_policy("test-stack_name", stack_policy_body="test-stack_policy_body", stack_policy_url="test-stack_policy_url", region_name="us-east-1")
    mock_client.set_stack_policy.assert_called_once()

def test_set_type_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import set_type_configuration
    mock_client = MagicMock()
    mock_client.set_type_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_type_configuration({}, type_arn="test-type_arn", configuration_alias={}, type_name="test-type_name", type_value="test-type_value", region_name="us-east-1")
    mock_client.set_type_configuration.assert_called_once()

def test_set_type_default_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import set_type_default_version
    mock_client = MagicMock()
    mock_client.set_type_default_version.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    set_type_default_version(arn="test-arn", type_value="test-type_value", type_name="test-type_name", version_id="test-version_id", region_name="us-east-1")
    mock_client.set_type_default_version.assert_called_once()

def test_start_resource_scan_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import start_resource_scan
    mock_client = MagicMock()
    mock_client.start_resource_scan.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    start_resource_scan(client_request_token="test-client_request_token", scan_filters="test-scan_filters", region_name="us-east-1")
    mock_client.start_resource_scan.assert_called_once()

def test_stop_stack_set_operation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import stop_stack_set_operation
    mock_client = MagicMock()
    mock_client.stop_stack_set_operation.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    stop_stack_set_operation("test-stack_set_name", "test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.stop_stack_set_operation.assert_called_once()

def test_update_generated_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import update_generated_template
    mock_client = MagicMock()
    mock_client.update_generated_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_generated_template("test-generated_template_name", new_generated_template_name="test-new_generated_template_name", add_resources="test-add_resources", remove_resources="test-remove_resources", refresh_all_resources="test-refresh_all_resources", template_configuration={}, region_name="us-east-1")
    mock_client.update_generated_template.assert_called_once()

def test_update_stack_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import update_stack_instances
    mock_client = MagicMock()
    mock_client.update_stack_instances.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_stack_instances("test-stack_set_name", "test-regions", accounts=1, deployment_targets="test-deployment_targets", parameter_overrides="test-parameter_overrides", operation_preferences="test-operation_preferences", operation_id="test-operation_id", call_as="test-call_as", region_name="us-east-1")
    mock_client.update_stack_instances.assert_called_once()

def test_update_stack_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import update_stack_set
    mock_client = MagicMock()
    mock_client.update_stack_set.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    update_stack_set("test-stack_set_name", description="test-description", template_body="test-template_body", template_url="test-template_url", use_previous_template=True, parameters="test-parameters", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], operation_preferences="test-operation_preferences", administration_role_arn="test-administration_role_arn", execution_role_name="test-execution_role_name", deployment_targets="test-deployment_targets", permission_model="test-permission_model", auto_deployment=True, operation_id="test-operation_id", accounts=1, regions="test-regions", call_as="test-call_as", managed_execution="test-managed_execution", region_name="us-east-1")
    mock_client.update_stack_set.assert_called_once()

def test_validate_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudformation import validate_template
    mock_client = MagicMock()
    mock_client.validate_template.return_value = {}
    monkeypatch.setattr("aws_util.cloudformation.get_client", lambda *a, **kw: mock_client)
    validate_template(template_body="test-template_body", template_url="test-template_url", region_name="us-east-1")
    mock_client.validate_template.assert_called_once()
