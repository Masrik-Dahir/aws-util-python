from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "ActivateTypeResult",
    "BatchDescribeTypeConfigurationsResult",
    "CFNStack",
    "CreateChangeSetResult",
    "CreateGeneratedTemplateResult",
    "CreateStackInstancesResult",
    "CreateStackRefactorResult",
    "CreateStackSetResult",
    "DeleteStackInstancesResult",
    "DescribeAccountLimitsResult",
    "DescribeChangeSetHooksResult",
    "DescribeChangeSetResult",
    "DescribeGeneratedTemplateResult",
    "DescribeOrganizationsAccessResult",
    "DescribePublisherResult",
    "DescribeResourceScanResult",
    "DescribeStackDriftDetectionStatusResult",
    "DescribeStackEventsResult",
    "DescribeStackInstanceResult",
    "DescribeStackRefactorResult",
    "DescribeStackResourceDriftsResult",
    "DescribeStackResourceResult",
    "DescribeStackResourcesResult",
    "DescribeStackSetOperationResult",
    "DescribeStackSetResult",
    "DescribeStacksResult",
    "DescribeTypeRegistrationResult",
    "DescribeTypeResult",
    "DetectStackDriftResult",
    "DetectStackResourceDriftResult",
    "DetectStackSetDriftResult",
    "EstimateTemplateCostResult",
    "GetGeneratedTemplateResult",
    "GetHookResultResult",
    "GetStackPolicyResult",
    "GetTemplateResult",
    "GetTemplateSummaryResult",
    "ImportStacksToStackSetResult",
    "ListChangeSetsResult",
    "ListExportsResult",
    "ListGeneratedTemplatesResult",
    "ListHookResultsResult",
    "ListImportsResult",
    "ListResourceScanRelatedResourcesResult",
    "ListResourceScanResourcesResult",
    "ListResourceScansResult",
    "ListStackInstanceResourceDriftsResult",
    "ListStackInstancesResult",
    "ListStackRefactorActionsResult",
    "ListStackRefactorsResult",
    "ListStackResourcesResult",
    "ListStackSetAutoDeploymentTargetsResult",
    "ListStackSetOperationResultsResult",
    "ListStackSetOperationsResult",
    "ListStackSetsResult",
    "ListTypeRegistrationsResult",
    "ListTypeVersionsResult",
    "ListTypesResult",
    "PublishTypeResult",
    "RegisterPublisherResult",
    "RegisterTypeResult",
    "RollbackStackResult",
    "RunTypeResult",
    "SetTypeConfigurationResult",
    "StartResourceScanResult",
    "UpdateGeneratedTemplateResult",
    "UpdateStackInstancesResult",
    "UpdateStackSetResult",
    "UpdateTerminationProtectionResult",
    "ValidateTemplateResult",
    "activate_organizations_access",
    "activate_type",
    "batch_describe_type_configurations",
    "cancel_update_stack",
    "continue_update_rollback",
    "create_change_set",
    "create_generated_template",
    "create_stack",
    "create_stack_instances",
    "create_stack_refactor",
    "create_stack_set",
    "deactivate_organizations_access",
    "deactivate_type",
    "delete_change_set",
    "delete_generated_template",
    "delete_stack",
    "delete_stack_instances",
    "delete_stack_set",
    "deploy_stack",
    "deregister_type",
    "describe_account_limits",
    "describe_change_set",
    "describe_change_set_hooks",
    "describe_generated_template",
    "describe_organizations_access",
    "describe_publisher",
    "describe_resource_scan",
    "describe_stack",
    "describe_stack_drift_detection_status",
    "describe_stack_events",
    "describe_stack_instance",
    "describe_stack_refactor",
    "describe_stack_resource",
    "describe_stack_resource_drifts",
    "describe_stack_resources",
    "describe_stack_set",
    "describe_stack_set_operation",
    "describe_stacks",
    "describe_type",
    "describe_type_registration",
    "detect_stack_drift",
    "detect_stack_resource_drift",
    "detect_stack_set_drift",
    "estimate_template_cost",
    "execute_change_set",
    "execute_stack_refactor",
    "get_export_value",
    "get_generated_template",
    "get_hook_result",
    "get_stack_outputs",
    "get_stack_policy",
    "get_template",
    "get_template_summary",
    "import_stacks_to_stack_set",
    "list_change_sets",
    "list_exports",
    "list_generated_templates",
    "list_hook_results",
    "list_imports",
    "list_resource_scan_related_resources",
    "list_resource_scan_resources",
    "list_resource_scans",
    "list_stack_instance_resource_drifts",
    "list_stack_instances",
    "list_stack_refactor_actions",
    "list_stack_refactors",
    "list_stack_resources",
    "list_stack_set_auto_deployment_targets",
    "list_stack_set_operation_results",
    "list_stack_set_operations",
    "list_stack_sets",
    "list_stacks",
    "list_type_registrations",
    "list_type_versions",
    "list_types",
    "publish_type",
    "record_handler_progress",
    "register_publisher",
    "register_type",
    "rollback_stack",
    "run_type",
    "set_stack_policy",
    "set_type_configuration",
    "set_type_default_version",
    "signal_resource",
    "start_resource_scan",
    "stop_stack_set_operation",
    "update_generated_template",
    "update_stack",
    "update_stack_instances",
    "update_stack_set",
    "update_termination_protection",
    "validate_template",
    "wait_for_stack",
]

_TERMINAL_STATUSES = {
    "CREATE_COMPLETE",
    "CREATE_FAILED",
    "ROLLBACK_COMPLETE",
    "ROLLBACK_FAILED",
    "UPDATE_COMPLETE",
    "UPDATE_FAILED",
    "UPDATE_ROLLBACK_COMPLETE",
    "UPDATE_ROLLBACK_FAILED",
    "DELETE_COMPLETE",
    "DELETE_FAILED",
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CFNStack(BaseModel):
    """A CloudFormation stack."""

    model_config = ConfigDict(frozen=True)

    stack_id: str
    stack_name: str
    status: str
    status_reason: str | None = None
    creation_time: datetime | None = None
    last_updated_time: datetime | None = None
    outputs: dict[str, str] = {}
    parameters: dict[str, str] = {}
    tags: dict[str, str] = {}

    @property
    def is_stable(self) -> bool:
        """``True`` if the stack is in a terminal state."""
        return self.status in _TERMINAL_STATUSES

    @property
    def is_healthy(self) -> bool:
        """``True`` if the stack completed successfully."""
        return self.status in {
            "CREATE_COMPLETE",
            "UPDATE_COMPLETE",
            "UPDATE_ROLLBACK_COMPLETE",
        }


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def describe_stack(
    stack_name: str,
    region_name: str | None = None,
) -> CFNStack | None:
    """Describe a single CloudFormation stack.

    Args:
        stack_name: Stack name or stack ID.
        region_name: AWS region override.

    Returns:
        A :class:`CFNStack`, or ``None`` if not found.

    Raises:
        RuntimeError: If the API call fails for a reason other than not found.
    """
    client = get_client("cloudformation", region_name)
    try:
        resp = client.describe_stacks(StackName=stack_name)
    except ClientError as exc:
        if "does not exist" in str(exc):
            return None
        raise wrap_aws_error(exc, f"describe_stack failed for {stack_name!r}") from exc
    stacks = resp.get("Stacks", [])
    return _parse_stack(stacks[0]) if stacks else None


def list_stacks(
    status_filter: list[str] | None = None,
    region_name: str | None = None,
) -> list[CFNStack]:
    """List CloudFormation stacks, optionally filtered by status.

    Args:
        status_filter: List of stack status values to include.  Defaults to
            all active stacks (excludes ``DELETE_COMPLETE``).
        region_name: AWS region override.

    Returns:
        A list of :class:`CFNStack` summaries.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    default_filter = [
        "CREATE_IN_PROGRESS",
        "CREATE_FAILED",
        "CREATE_COMPLETE",
        "ROLLBACK_IN_PROGRESS",
        "ROLLBACK_FAILED",
        "ROLLBACK_COMPLETE",
        "UPDATE_IN_PROGRESS",
        "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
        "UPDATE_COMPLETE",
        "UPDATE_FAILED",
        "UPDATE_ROLLBACK_IN_PROGRESS",
        "UPDATE_ROLLBACK_FAILED",
        "UPDATE_ROLLBACK_COMPLETE",
    ]
    kwargs: dict[str, Any] = {"StackStatusFilter": status_filter or default_filter}
    stacks: list[CFNStack] = []
    try:
        paginator = client.get_paginator("list_stacks")
        for page in paginator.paginate(**kwargs):
            for summary in page.get("StackSummaries", []):
                stacks.append(
                    CFNStack(
                        stack_id=summary.get("StackId", ""),
                        stack_name=summary["StackName"],
                        status=summary["StackStatus"],
                        status_reason=summary.get("StackStatusReason"),
                        creation_time=summary.get("CreationTime"),
                        last_updated_time=summary.get("LastUpdatedTime"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_stacks failed") from exc
    return stacks


def get_stack_outputs(
    stack_name: str,
    region_name: str | None = None,
) -> dict[str, str]:
    """Return the output key/value pairs of a CloudFormation stack.

    Args:
        stack_name: Stack name or stack ID.
        region_name: AWS region override.

    Returns:
        A dict mapping output key → output value.

    Raises:
        RuntimeError: If the stack is not found or the call fails.
    """
    stack = describe_stack(stack_name, region_name=region_name)
    if stack is None:
        raise AwsServiceError(f"Stack {stack_name!r} not found")
    return stack.outputs


def create_stack(
    stack_name: str,
    template_body: str | dict,
    parameters: dict[str, str] | None = None,
    capabilities: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a CloudFormation stack.

    Args:
        stack_name: Name for the new stack.
        template_body: Template as a JSON/YAML string or a dict (auto-serialised
            to JSON).
        parameters: Stack parameters as ``{key: value}``.
        capabilities: IAM capabilities, e.g.
            ``["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"]``.
        tags: Stack tags as ``{key: value}``.
        region_name: AWS region override.

    Returns:
        The new stack ID.

    Raises:
        RuntimeError: If stack creation fails.
    """
    client = get_client("cloudformation", region_name)
    if isinstance(template_body, dict):
        template_body = json.dumps(template_body)

    kwargs: dict[str, Any] = {
        "StackName": stack_name,
        "TemplateBody": template_body,
        "Capabilities": capabilities or [],
    }
    if parameters:
        kwargs["Parameters"] = [
            {"ParameterKey": k, "ParameterValue": v} for k, v in parameters.items()
        ]
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]

    try:
        resp = client.create_stack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create stack {stack_name!r}") from exc
    return resp["StackId"]


def update_stack(
    stack_name: str,
    template_body: str | dict,
    parameters: dict[str, str] | None = None,
    capabilities: list[str] | None = None,
    region_name: str | None = None,
) -> str:
    """Update an existing CloudFormation stack.

    Args:
        stack_name: Stack name or stack ID.
        template_body: Updated template as a string or dict.
        parameters: Updated parameters.
        capabilities: IAM capabilities.
        region_name: AWS region override.

    Returns:
        The stack ID.

    Raises:
        RuntimeError: If the update fails.
    """
    client = get_client("cloudformation", region_name)
    if isinstance(template_body, dict):
        template_body = json.dumps(template_body)

    kwargs: dict[str, Any] = {
        "StackName": stack_name,
        "TemplateBody": template_body,
        "Capabilities": capabilities or [],
    }
    if parameters:
        kwargs["Parameters"] = [
            {"ParameterKey": k, "ParameterValue": v} for k, v in parameters.items()
        ]
    try:
        resp = client.update_stack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update stack {stack_name!r}") from exc
    return resp["StackId"]


def delete_stack(
    stack_name: str,
    region_name: str | None = None,
) -> None:
    """Delete a CloudFormation stack.

    Args:
        stack_name: Stack name or stack ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    client = get_client("cloudformation", region_name)
    try:
        client.delete_stack(StackName=stack_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete stack {stack_name!r}") from exc


def wait_for_stack(
    stack_name: str,
    poll_interval: float = 10.0,
    timeout: float = 1800.0,
    region_name: str | None = None,
) -> CFNStack:
    """Poll until a CloudFormation stack reaches a stable state.

    Args:
        stack_name: Stack name or stack ID.
        poll_interval: Seconds between status polls (default ``10``).
        timeout: Maximum seconds to wait (default ``1800`` / 30 min).
        region_name: AWS region override.

    Returns:
        The :class:`CFNStack` in its final state.

    Raises:
        TimeoutError: If the stack does not stabilise within *timeout*.
        RuntimeError: If the stack is not found or the describe call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        stack = describe_stack(stack_name, region_name=region_name)
        if stack is None:
            raise AwsServiceError(f"Stack {stack_name!r} not found during wait")
        if stack.is_stable:
            return stack
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Stack {stack_name!r} did not stabilise within {timeout}s "
                f"(current status: {stack.status})"
            )
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_stack(stack: dict) -> CFNStack:
    outputs = {o["OutputKey"]: o["OutputValue"] for o in stack.get("Outputs", [])}
    parameters = {
        p["ParameterKey"]: p.get("ParameterValue", "") for p in stack.get("Parameters", [])
    }
    tags = {t["Key"]: t["Value"] for t in stack.get("Tags", [])}
    return CFNStack(
        stack_id=stack.get("StackId", ""),
        stack_name=stack["StackName"],
        status=stack["StackStatus"],
        status_reason=stack.get("StackStatusReason"),
        creation_time=stack.get("CreationTime"),
        last_updated_time=stack.get("LastUpdatedTime"),
        outputs=outputs,
        parameters=parameters,
        tags=tags,
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def deploy_stack(
    stack_name: str,
    template_body: str | dict,
    parameters: dict[str, str] | None = None,
    capabilities: list[str] | None = None,
    tags: dict[str, str] | None = None,
    timeout: float = 1800.0,
    region_name: str | None = None,
) -> CFNStack:
    """Create or update a CloudFormation stack and wait for completion.

    Detects whether the stack exists and calls ``create_stack`` or
    ``update_stack`` accordingly.  Waits for the operation to reach a
    stable state before returning.

    Args:
        stack_name: Stack name.
        template_body: Template as a string or dict.
        parameters: Stack parameters.
        capabilities: IAM capabilities, e.g. ``["CAPABILITY_IAM"]``.
        tags: Stack tags.
        timeout: Maximum seconds to wait for stability (default ``1800``).
        region_name: AWS region override.

    Returns:
        The final :class:`CFNStack` after the operation completes.

    Raises:
        RuntimeError: If the stack ends in a failed state.
        TimeoutError: If the operation does not complete within *timeout*.
    """
    existing = describe_stack(stack_name, region_name=region_name)
    if existing is None:
        create_stack(
            stack_name,
            template_body,
            parameters=parameters,
            capabilities=capabilities,
            tags=tags,
            region_name=region_name,
        )
    else:
        try:
            update_stack(
                stack_name,
                template_body,
                parameters=parameters,
                capabilities=capabilities,
                region_name=region_name,
            )
        except RuntimeError as exc:
            # No-op if there's nothing to update
            if "No updates are to be performed" in str(exc):
                return existing
            raise

    stack = wait_for_stack(stack_name, timeout=timeout, region_name=region_name)
    if not stack.is_healthy:
        raise AwsServiceError(
            f"Stack {stack_name!r} deployment failed with status "
            f"{stack.status!r}: {stack.status_reason}"
        )
    return stack


def get_export_value(
    export_name: str,
    region_name: str | None = None,
) -> str:
    """Retrieve the value of a CloudFormation stack export by name.

    Exports are declared in a stack's ``Outputs`` section with an
    ``Export.Name`` field and can be imported by other stacks with
    ``!ImportValue``.

    Args:
        export_name: The ``Export.Name`` value to look up.
        region_name: AWS region override.

    Returns:
        The export value as a string.

    Raises:
        KeyError: If no export with *export_name* exists.
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    try:
        paginator = client.get_paginator("list_exports")
        for page in paginator.paginate():
            for export in page.get("Exports", []):
                if export["Name"] == export_name:
                    return export["Value"]
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_export_value failed") from exc

    raise KeyError(f"CloudFormation export {export_name!r} not found")


class ActivateTypeResult(BaseModel):
    """Result of activate_type."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None


class BatchDescribeTypeConfigurationsResult(BaseModel):
    """Result of batch_describe_type_configurations."""

    model_config = ConfigDict(frozen=True)

    errors: list[dict[str, Any]] | None = None
    unprocessed_type_configurations: list[dict[str, Any]] | None = None
    type_configurations: list[dict[str, Any]] | None = None


class CreateChangeSetResult(BaseModel):
    """Result of create_change_set."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    stack_id: str | None = None


class CreateGeneratedTemplateResult(BaseModel):
    """Result of create_generated_template."""

    model_config = ConfigDict(frozen=True)

    generated_template_id: str | None = None


class CreateStackInstancesResult(BaseModel):
    """Result of create_stack_instances."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class CreateStackRefactorResult(BaseModel):
    """Result of create_stack_refactor."""

    model_config = ConfigDict(frozen=True)

    stack_refactor_id: str | None = None


class CreateStackSetResult(BaseModel):
    """Result of create_stack_set."""

    model_config = ConfigDict(frozen=True)

    stack_set_id: str | None = None


class DeleteStackInstancesResult(BaseModel):
    """Result of delete_stack_instances."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class DescribeAccountLimitsResult(BaseModel):
    """Result of describe_account_limits."""

    model_config = ConfigDict(frozen=True)

    account_limits: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeChangeSetResult(BaseModel):
    """Result of describe_change_set."""

    model_config = ConfigDict(frozen=True)

    change_set_name: str | None = None
    change_set_id: str | None = None
    stack_id: str | None = None
    stack_name: str | None = None
    description: str | None = None
    parameters: list[dict[str, Any]] | None = None
    creation_time: str | None = None
    execution_status: str | None = None
    status: str | None = None
    status_reason: str | None = None
    notification_ar_ns: list[str] | None = None
    rollback_configuration: dict[str, Any] | None = None
    capabilities: list[str] | None = None
    tags: list[dict[str, Any]] | None = None
    changes: list[dict[str, Any]] | None = None
    next_token: str | None = None
    include_nested_stacks: bool | None = None
    parent_change_set_id: str | None = None
    root_change_set_id: str | None = None
    on_stack_failure: str | None = None
    import_existing_resources: bool | None = None


class DescribeChangeSetHooksResult(BaseModel):
    """Result of describe_change_set_hooks."""

    model_config = ConfigDict(frozen=True)

    change_set_id: str | None = None
    change_set_name: str | None = None
    hooks: list[dict[str, Any]] | None = None
    status: str | None = None
    next_token: str | None = None
    stack_id: str | None = None
    stack_name: str | None = None


class DescribeGeneratedTemplateResult(BaseModel):
    """Result of describe_generated_template."""

    model_config = ConfigDict(frozen=True)

    generated_template_id: str | None = None
    generated_template_name: str | None = None
    resources: list[dict[str, Any]] | None = None
    status: str | None = None
    status_reason: str | None = None
    creation_time: str | None = None
    last_updated_time: str | None = None
    progress: dict[str, Any] | None = None
    stack_id: str | None = None
    template_configuration: dict[str, Any] | None = None
    total_warnings: int | None = None


class DescribeOrganizationsAccessResult(BaseModel):
    """Result of describe_organizations_access."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class DescribePublisherResult(BaseModel):
    """Result of describe_publisher."""

    model_config = ConfigDict(frozen=True)

    publisher_id: str | None = None
    publisher_status: str | None = None
    identity_provider: str | None = None
    publisher_profile: str | None = None


class DescribeResourceScanResult(BaseModel):
    """Result of describe_resource_scan."""

    model_config = ConfigDict(frozen=True)

    resource_scan_id: str | None = None
    status: str | None = None
    status_reason: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    percentage_completed: float | None = None
    resource_types: list[str] | None = None
    resources_scanned: int | None = None
    resources_read: int | None = None
    scan_filters: list[dict[str, Any]] | None = None


class DescribeStackDriftDetectionStatusResult(BaseModel):
    """Result of describe_stack_drift_detection_status."""

    model_config = ConfigDict(frozen=True)

    stack_id: str | None = None
    stack_drift_detection_id: str | None = None
    stack_drift_status: str | None = None
    detection_status: str | None = None
    detection_status_reason: str | None = None
    drifted_stack_resource_count: int | None = None
    timestamp: str | None = None


class DescribeStackEventsResult(BaseModel):
    """Result of describe_stack_events."""

    model_config = ConfigDict(frozen=True)

    stack_events: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeStackInstanceResult(BaseModel):
    """Result of describe_stack_instance."""

    model_config = ConfigDict(frozen=True)

    stack_instance: dict[str, Any] | None = None


class DescribeStackRefactorResult(BaseModel):
    """Result of describe_stack_refactor."""

    model_config = ConfigDict(frozen=True)

    description: str | None = None
    stack_refactor_id: str | None = None
    stack_ids: list[str] | None = None
    execution_status: str | None = None
    execution_status_reason: str | None = None
    status: str | None = None
    status_reason: str | None = None


class DescribeStackResourceResult(BaseModel):
    """Result of describe_stack_resource."""

    model_config = ConfigDict(frozen=True)

    stack_resource_detail: dict[str, Any] | None = None


class DescribeStackResourceDriftsResult(BaseModel):
    """Result of describe_stack_resource_drifts."""

    model_config = ConfigDict(frozen=True)

    stack_resource_drifts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeStackResourcesResult(BaseModel):
    """Result of describe_stack_resources."""

    model_config = ConfigDict(frozen=True)

    stack_resources: list[dict[str, Any]] | None = None


class DescribeStackSetResult(BaseModel):
    """Result of describe_stack_set."""

    model_config = ConfigDict(frozen=True)

    stack_set: dict[str, Any] | None = None


class DescribeStackSetOperationResult(BaseModel):
    """Result of describe_stack_set_operation."""

    model_config = ConfigDict(frozen=True)

    stack_set_operation: dict[str, Any] | None = None


class DescribeStacksResult(BaseModel):
    """Result of describe_stacks."""

    model_config = ConfigDict(frozen=True)

    stacks: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeTypeResult(BaseModel):
    """Result of describe_type."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    type_value: str | None = None
    type_name: str | None = None
    default_version_id: str | None = None
    is_default_version: bool | None = None
    type_tests_status: str | None = None
    type_tests_status_description: str | None = None
    description: str | None = None
    model_schema: str | None = None
    provisioning_type: str | None = None
    deprecated_status: str | None = None
    logging_config: dict[str, Any] | None = None
    required_activated_types: list[dict[str, Any]] | None = None
    execution_role_arn: str | None = None
    visibility: str | None = None
    source_url: str | None = None
    documentation_url: str | None = None
    last_updated: str | None = None
    time_created: str | None = None
    configuration_schema: str | None = None
    publisher_id: str | None = None
    original_type_name: str | None = None
    original_type_arn: str | None = None
    public_version_number: str | None = None
    latest_public_version: str | None = None
    is_activated: bool | None = None
    auto_update: bool | None = None


class DescribeTypeRegistrationResult(BaseModel):
    """Result of describe_type_registration."""

    model_config = ConfigDict(frozen=True)

    progress_status: str | None = None
    description: str | None = None
    type_arn: str | None = None
    type_version_arn: str | None = None


class DetectStackDriftResult(BaseModel):
    """Result of detect_stack_drift."""

    model_config = ConfigDict(frozen=True)

    stack_drift_detection_id: str | None = None


class DetectStackResourceDriftResult(BaseModel):
    """Result of detect_stack_resource_drift."""

    model_config = ConfigDict(frozen=True)

    stack_resource_drift: dict[str, Any] | None = None


class DetectStackSetDriftResult(BaseModel):
    """Result of detect_stack_set_drift."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class EstimateTemplateCostResult(BaseModel):
    """Result of estimate_template_cost."""

    model_config = ConfigDict(frozen=True)

    url: str | None = None


class GetGeneratedTemplateResult(BaseModel):
    """Result of get_generated_template."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    template_body: str | None = None


class GetHookResultResult(BaseModel):
    """Result of get_hook_result."""

    model_config = ConfigDict(frozen=True)

    hook_result_id: str | None = None
    invocation_point: str | None = None
    failure_mode: str | None = None
    type_name: str | None = None
    original_type_name: str | None = None
    type_version_id: str | None = None
    type_configuration_version_id: str | None = None
    type_arn: str | None = None
    status: str | None = None
    hook_status_reason: str | None = None
    invoked_at: str | None = None
    target: dict[str, Any] | None = None
    annotations: list[dict[str, Any]] | None = None


class GetStackPolicyResult(BaseModel):
    """Result of get_stack_policy."""

    model_config = ConfigDict(frozen=True)

    stack_policy_body: str | None = None


class GetTemplateResult(BaseModel):
    """Result of get_template."""

    model_config = ConfigDict(frozen=True)

    template_body: str | None = None
    stages_available: list[str] | None = None


class GetTemplateSummaryResult(BaseModel):
    """Result of get_template_summary."""

    model_config = ConfigDict(frozen=True)

    parameters: list[dict[str, Any]] | None = None
    description: str | None = None
    capabilities: list[str] | None = None
    capabilities_reason: str | None = None
    resource_types: list[str] | None = None
    version: str | None = None
    metadata: str | None = None
    declared_transforms: list[str] | None = None
    resource_identifier_summaries: list[dict[str, Any]] | None = None
    warnings: dict[str, Any] | None = None


class ImportStacksToStackSetResult(BaseModel):
    """Result of import_stacks_to_stack_set."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class ListChangeSetsResult(BaseModel):
    """Result of list_change_sets."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListExportsResult(BaseModel):
    """Result of list_exports."""

    model_config = ConfigDict(frozen=True)

    exports: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListGeneratedTemplatesResult(BaseModel):
    """Result of list_generated_templates."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListHookResultsResult(BaseModel):
    """Result of list_hook_results."""

    model_config = ConfigDict(frozen=True)

    target_type: str | None = None
    target_id: str | None = None
    hook_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListImportsResult(BaseModel):
    """Result of list_imports."""

    model_config = ConfigDict(frozen=True)

    imports: list[str] | None = None
    next_token: str | None = None


class ListResourceScanRelatedResourcesResult(BaseModel):
    """Result of list_resource_scan_related_resources."""

    model_config = ConfigDict(frozen=True)

    related_resources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceScanResourcesResult(BaseModel):
    """Result of list_resource_scan_resources."""

    model_config = ConfigDict(frozen=True)

    resources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceScansResult(BaseModel):
    """Result of list_resource_scans."""

    model_config = ConfigDict(frozen=True)

    resource_scan_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackInstanceResourceDriftsResult(BaseModel):
    """Result of list_stack_instance_resource_drifts."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackInstancesResult(BaseModel):
    """Result of list_stack_instances."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackRefactorActionsResult(BaseModel):
    """Result of list_stack_refactor_actions."""

    model_config = ConfigDict(frozen=True)

    stack_refactor_actions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackRefactorsResult(BaseModel):
    """Result of list_stack_refactors."""

    model_config = ConfigDict(frozen=True)

    stack_refactor_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackResourcesResult(BaseModel):
    """Result of list_stack_resources."""

    model_config = ConfigDict(frozen=True)

    stack_resource_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackSetAutoDeploymentTargetsResult(BaseModel):
    """Result of list_stack_set_auto_deployment_targets."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackSetOperationResultsResult(BaseModel):
    """Result of list_stack_set_operation_results."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackSetOperationsResult(BaseModel):
    """Result of list_stack_set_operations."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStackSetsResult(BaseModel):
    """Result of list_stack_sets."""

    model_config = ConfigDict(frozen=True)

    summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTypeRegistrationsResult(BaseModel):
    """Result of list_type_registrations."""

    model_config = ConfigDict(frozen=True)

    registration_token_list: list[str] | None = None
    next_token: str | None = None


class ListTypeVersionsResult(BaseModel):
    """Result of list_type_versions."""

    model_config = ConfigDict(frozen=True)

    type_version_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTypesResult(BaseModel):
    """Result of list_types."""

    model_config = ConfigDict(frozen=True)

    type_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PublishTypeResult(BaseModel):
    """Result of publish_type."""

    model_config = ConfigDict(frozen=True)

    public_type_arn: str | None = None


class RegisterPublisherResult(BaseModel):
    """Result of register_publisher."""

    model_config = ConfigDict(frozen=True)

    publisher_id: str | None = None


class RegisterTypeResult(BaseModel):
    """Result of register_type."""

    model_config = ConfigDict(frozen=True)

    registration_token: str | None = None


class RollbackStackResult(BaseModel):
    """Result of rollback_stack."""

    model_config = ConfigDict(frozen=True)

    stack_id: str | None = None


class RunTypeResult(BaseModel):
    """Result of run_type."""

    model_config = ConfigDict(frozen=True)

    type_version_arn: str | None = None


class SetTypeConfigurationResult(BaseModel):
    """Result of set_type_configuration."""

    model_config = ConfigDict(frozen=True)

    configuration_arn: str | None = None


class StartResourceScanResult(BaseModel):
    """Result of start_resource_scan."""

    model_config = ConfigDict(frozen=True)

    resource_scan_id: str | None = None


class UpdateGeneratedTemplateResult(BaseModel):
    """Result of update_generated_template."""

    model_config = ConfigDict(frozen=True)

    generated_template_id: str | None = None


class UpdateStackInstancesResult(BaseModel):
    """Result of update_stack_instances."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class UpdateStackSetResult(BaseModel):
    """Result of update_stack_set."""

    model_config = ConfigDict(frozen=True)

    operation_id: str | None = None


class UpdateTerminationProtectionResult(BaseModel):
    """Result of update_termination_protection."""

    model_config = ConfigDict(frozen=True)

    stack_id: str | None = None


class ValidateTemplateResult(BaseModel):
    """Result of validate_template."""

    model_config = ConfigDict(frozen=True)

    parameters: list[dict[str, Any]] | None = None
    description: str | None = None
    capabilities: list[str] | None = None
    capabilities_reason: str | None = None
    declared_transforms: list[str] | None = None


def activate_organizations_access(
    region_name: str | None = None,
) -> None:
    """Activate organizations access.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.activate_organizations_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to activate organizations access") from exc
    return None


def activate_type(
    *,
    type_value: str | None = None,
    public_type_arn: str | None = None,
    publisher_id: str | None = None,
    type_name: str | None = None,
    type_name_alias: str | None = None,
    auto_update: bool | None = None,
    logging_config: dict[str, Any] | None = None,
    execution_role_arn: str | None = None,
    version_bump: str | None = None,
    major_version: int | None = None,
    region_name: str | None = None,
) -> ActivateTypeResult:
    """Activate type.

    Args:
        type_value: Type value.
        public_type_arn: Public type arn.
        publisher_id: Publisher id.
        type_name: Type name.
        type_name_alias: Type name alias.
        auto_update: Auto update.
        logging_config: Logging config.
        execution_role_arn: Execution role arn.
        version_bump: Version bump.
        major_version: Major version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if public_type_arn is not None:
        kwargs["PublicTypeArn"] = public_type_arn
    if publisher_id is not None:
        kwargs["PublisherId"] = publisher_id
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if type_name_alias is not None:
        kwargs["TypeNameAlias"] = type_name_alias
    if auto_update is not None:
        kwargs["AutoUpdate"] = auto_update
    if logging_config is not None:
        kwargs["LoggingConfig"] = logging_config
    if execution_role_arn is not None:
        kwargs["ExecutionRoleArn"] = execution_role_arn
    if version_bump is not None:
        kwargs["VersionBump"] = version_bump
    if major_version is not None:
        kwargs["MajorVersion"] = major_version
    try:
        resp = client.activate_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to activate type") from exc
    return ActivateTypeResult(
        arn=resp.get("Arn"),
    )


def batch_describe_type_configurations(
    type_configuration_identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchDescribeTypeConfigurationsResult:
    """Batch describe type configurations.

    Args:
        type_configuration_identifiers: Type configuration identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TypeConfigurationIdentifiers"] = type_configuration_identifiers
    try:
        resp = client.batch_describe_type_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch describe type configurations") from exc
    return BatchDescribeTypeConfigurationsResult(
        errors=resp.get("Errors"),
        unprocessed_type_configurations=resp.get("UnprocessedTypeConfigurations"),
        type_configurations=resp.get("TypeConfigurations"),
    )


def cancel_update_stack(
    stack_name: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Cancel update stack.

    Args:
        stack_name: Stack name.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        client.cancel_update_stack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel update stack") from exc
    return None


def continue_update_rollback(
    stack_name: str,
    *,
    role_arn: str | None = None,
    resources_to_skip: list[str] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Continue update rollback.

    Args:
        stack_name: Stack name.
        role_arn: Role arn.
        resources_to_skip: Resources to skip.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if role_arn is not None:
        kwargs["RoleARN"] = role_arn
    if resources_to_skip is not None:
        kwargs["ResourcesToSkip"] = resources_to_skip
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        client.continue_update_rollback(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to continue update rollback") from exc
    return None


def create_change_set(
    stack_name: str,
    change_set_name: str,
    *,
    template_body: str | None = None,
    template_url: str | None = None,
    use_previous_template: bool | None = None,
    parameters: list[dict[str, Any]] | None = None,
    capabilities: list[str] | None = None,
    resource_types: list[str] | None = None,
    role_arn: str | None = None,
    rollback_configuration: dict[str, Any] | None = None,
    notification_ar_ns: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    client_token: str | None = None,
    description: str | None = None,
    change_set_type: str | None = None,
    resources_to_import: list[dict[str, Any]] | None = None,
    include_nested_stacks: bool | None = None,
    on_stack_failure: str | None = None,
    import_existing_resources: bool | None = None,
    region_name: str | None = None,
) -> CreateChangeSetResult:
    """Create change set.

    Args:
        stack_name: Stack name.
        change_set_name: Change set name.
        template_body: Template body.
        template_url: Template url.
        use_previous_template: Use previous template.
        parameters: Parameters.
        capabilities: Capabilities.
        resource_types: Resource types.
        role_arn: Role arn.
        rollback_configuration: Rollback configuration.
        notification_ar_ns: Notification ar ns.
        tags: Tags.
        client_token: Client token.
        description: Description.
        change_set_type: Change set type.
        resources_to_import: Resources to import.
        include_nested_stacks: Include nested stacks.
        on_stack_failure: On stack failure.
        import_existing_resources: Import existing resources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    kwargs["ChangeSetName"] = change_set_name
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    if use_previous_template is not None:
        kwargs["UsePreviousTemplate"] = use_previous_template
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if capabilities is not None:
        kwargs["Capabilities"] = capabilities
    if resource_types is not None:
        kwargs["ResourceTypes"] = resource_types
    if role_arn is not None:
        kwargs["RoleARN"] = role_arn
    if rollback_configuration is not None:
        kwargs["RollbackConfiguration"] = rollback_configuration
    if notification_ar_ns is not None:
        kwargs["NotificationARNs"] = notification_ar_ns
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if description is not None:
        kwargs["Description"] = description
    if change_set_type is not None:
        kwargs["ChangeSetType"] = change_set_type
    if resources_to_import is not None:
        kwargs["ResourcesToImport"] = resources_to_import
    if include_nested_stacks is not None:
        kwargs["IncludeNestedStacks"] = include_nested_stacks
    if on_stack_failure is not None:
        kwargs["OnStackFailure"] = on_stack_failure
    if import_existing_resources is not None:
        kwargs["ImportExistingResources"] = import_existing_resources
    try:
        resp = client.create_change_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create change set") from exc
    return CreateChangeSetResult(
        id=resp.get("Id"),
        stack_id=resp.get("StackId"),
    )


def create_generated_template(
    generated_template_name: str,
    *,
    resources: list[dict[str, Any]] | None = None,
    stack_name: str | None = None,
    template_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateGeneratedTemplateResult:
    """Create generated template.

    Args:
        generated_template_name: Generated template name.
        resources: Resources.
        stack_name: Stack name.
        template_configuration: Template configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GeneratedTemplateName"] = generated_template_name
    if resources is not None:
        kwargs["Resources"] = resources
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if template_configuration is not None:
        kwargs["TemplateConfiguration"] = template_configuration
    try:
        resp = client.create_generated_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create generated template") from exc
    return CreateGeneratedTemplateResult(
        generated_template_id=resp.get("GeneratedTemplateId"),
    )


def create_stack_instances(
    stack_set_name: str,
    regions: list[str],
    *,
    accounts: list[str] | None = None,
    deployment_targets: dict[str, Any] | None = None,
    parameter_overrides: list[dict[str, Any]] | None = None,
    operation_preferences: dict[str, Any] | None = None,
    operation_id: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> CreateStackInstancesResult:
    """Create stack instances.

    Args:
        stack_set_name: Stack set name.
        regions: Regions.
        accounts: Accounts.
        deployment_targets: Deployment targets.
        parameter_overrides: Parameter overrides.
        operation_preferences: Operation preferences.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["Regions"] = regions
    if accounts is not None:
        kwargs["Accounts"] = accounts
    if deployment_targets is not None:
        kwargs["DeploymentTargets"] = deployment_targets
    if parameter_overrides is not None:
        kwargs["ParameterOverrides"] = parameter_overrides
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.create_stack_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create stack instances") from exc
    return CreateStackInstancesResult(
        operation_id=resp.get("OperationId"),
    )


def create_stack_refactor(
    stack_definitions: list[dict[str, Any]],
    *,
    description: str | None = None,
    enable_stack_creation: bool | None = None,
    resource_mappings: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateStackRefactorResult:
    """Create stack refactor.

    Args:
        stack_definitions: Stack definitions.
        description: Description.
        enable_stack_creation: Enable stack creation.
        resource_mappings: Resource mappings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackDefinitions"] = stack_definitions
    if description is not None:
        kwargs["Description"] = description
    if enable_stack_creation is not None:
        kwargs["EnableStackCreation"] = enable_stack_creation
    if resource_mappings is not None:
        kwargs["ResourceMappings"] = resource_mappings
    try:
        resp = client.create_stack_refactor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create stack refactor") from exc
    return CreateStackRefactorResult(
        stack_refactor_id=resp.get("StackRefactorId"),
    )


def create_stack_set(
    stack_set_name: str,
    *,
    description: str | None = None,
    template_body: str | None = None,
    template_url: str | None = None,
    stack_id: str | None = None,
    parameters: list[dict[str, Any]] | None = None,
    capabilities: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    administration_role_arn: str | None = None,
    execution_role_name: str | None = None,
    permission_model: str | None = None,
    auto_deployment: dict[str, Any] | None = None,
    call_as: str | None = None,
    client_request_token: str | None = None,
    managed_execution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateStackSetResult:
    """Create stack set.

    Args:
        stack_set_name: Stack set name.
        description: Description.
        template_body: Template body.
        template_url: Template url.
        stack_id: Stack id.
        parameters: Parameters.
        capabilities: Capabilities.
        tags: Tags.
        administration_role_arn: Administration role arn.
        execution_role_name: Execution role name.
        permission_model: Permission model.
        auto_deployment: Auto deployment.
        call_as: Call as.
        client_request_token: Client request token.
        managed_execution: Managed execution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if description is not None:
        kwargs["Description"] = description
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    if stack_id is not None:
        kwargs["StackId"] = stack_id
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if capabilities is not None:
        kwargs["Capabilities"] = capabilities
    if tags is not None:
        kwargs["Tags"] = tags
    if administration_role_arn is not None:
        kwargs["AdministrationRoleARN"] = administration_role_arn
    if execution_role_name is not None:
        kwargs["ExecutionRoleName"] = execution_role_name
    if permission_model is not None:
        kwargs["PermissionModel"] = permission_model
    if auto_deployment is not None:
        kwargs["AutoDeployment"] = auto_deployment
    if call_as is not None:
        kwargs["CallAs"] = call_as
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if managed_execution is not None:
        kwargs["ManagedExecution"] = managed_execution
    try:
        resp = client.create_stack_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create stack set") from exc
    return CreateStackSetResult(
        stack_set_id=resp.get("StackSetId"),
    )


def deactivate_organizations_access(
    region_name: str | None = None,
) -> None:
    """Deactivate organizations access.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.deactivate_organizations_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deactivate organizations access") from exc
    return None


def deactivate_type(
    *,
    type_name: str | None = None,
    type_value: str | None = None,
    arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Deactivate type.

    Args:
        type_name: Type name.
        type_value: Type value.
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if type_value is not None:
        kwargs["Type"] = type_value
    if arn is not None:
        kwargs["Arn"] = arn
    try:
        client.deactivate_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deactivate type") from exc
    return None


def delete_change_set(
    change_set_name: str,
    *,
    stack_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete change set.

    Args:
        change_set_name: Change set name.
        stack_name: Stack name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ChangeSetName"] = change_set_name
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    try:
        client.delete_change_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete change set") from exc
    return None


def delete_generated_template(
    generated_template_name: str,
    region_name: str | None = None,
) -> None:
    """Delete generated template.

    Args:
        generated_template_name: Generated template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GeneratedTemplateName"] = generated_template_name
    try:
        client.delete_generated_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete generated template") from exc
    return None


def delete_stack_instances(
    stack_set_name: str,
    regions: list[str],
    retain_stacks: bool,
    *,
    accounts: list[str] | None = None,
    deployment_targets: dict[str, Any] | None = None,
    operation_preferences: dict[str, Any] | None = None,
    operation_id: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DeleteStackInstancesResult:
    """Delete stack instances.

    Args:
        stack_set_name: Stack set name.
        regions: Regions.
        retain_stacks: Retain stacks.
        accounts: Accounts.
        deployment_targets: Deployment targets.
        operation_preferences: Operation preferences.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["Regions"] = regions
    kwargs["RetainStacks"] = retain_stacks
    if accounts is not None:
        kwargs["Accounts"] = accounts
    if deployment_targets is not None:
        kwargs["DeploymentTargets"] = deployment_targets
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.delete_stack_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete stack instances") from exc
    return DeleteStackInstancesResult(
        operation_id=resp.get("OperationId"),
    )


def delete_stack_set(
    stack_set_name: str,
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete stack set.

    Args:
        stack_set_name: Stack set name.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        client.delete_stack_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete stack set") from exc
    return None


def deregister_type(
    *,
    arn: str | None = None,
    type_value: str | None = None,
    type_name: str | None = None,
    version_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Deregister type.

    Args:
        arn: Arn.
        type_value: Type value.
        type_name: Type name.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if arn is not None:
        kwargs["Arn"] = arn
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if version_id is not None:
        kwargs["VersionId"] = version_id
    try:
        client.deregister_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister type") from exc
    return None


def describe_account_limits(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAccountLimitsResult:
    """Describe account limits.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_account_limits(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account limits") from exc
    return DescribeAccountLimitsResult(
        account_limits=resp.get("AccountLimits"),
        next_token=resp.get("NextToken"),
    )


def describe_change_set(
    change_set_name: str,
    *,
    stack_name: str | None = None,
    next_token: str | None = None,
    include_property_values: bool | None = None,
    region_name: str | None = None,
) -> DescribeChangeSetResult:
    """Describe change set.

    Args:
        change_set_name: Change set name.
        stack_name: Stack name.
        next_token: Next token.
        include_property_values: Include property values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ChangeSetName"] = change_set_name
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if include_property_values is not None:
        kwargs["IncludePropertyValues"] = include_property_values
    try:
        resp = client.describe_change_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe change set") from exc
    return DescribeChangeSetResult(
        change_set_name=resp.get("ChangeSetName"),
        change_set_id=resp.get("ChangeSetId"),
        stack_id=resp.get("StackId"),
        stack_name=resp.get("StackName"),
        description=resp.get("Description"),
        parameters=resp.get("Parameters"),
        creation_time=resp.get("CreationTime"),
        execution_status=resp.get("ExecutionStatus"),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        notification_ar_ns=resp.get("NotificationARNs"),
        rollback_configuration=resp.get("RollbackConfiguration"),
        capabilities=resp.get("Capabilities"),
        tags=resp.get("Tags"),
        changes=resp.get("Changes"),
        next_token=resp.get("NextToken"),
        include_nested_stacks=resp.get("IncludeNestedStacks"),
        parent_change_set_id=resp.get("ParentChangeSetId"),
        root_change_set_id=resp.get("RootChangeSetId"),
        on_stack_failure=resp.get("OnStackFailure"),
        import_existing_resources=resp.get("ImportExistingResources"),
    )


def describe_change_set_hooks(
    change_set_name: str,
    *,
    stack_name: str | None = None,
    next_token: str | None = None,
    logical_resource_id: str | None = None,
    region_name: str | None = None,
) -> DescribeChangeSetHooksResult:
    """Describe change set hooks.

    Args:
        change_set_name: Change set name.
        stack_name: Stack name.
        next_token: Next token.
        logical_resource_id: Logical resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ChangeSetName"] = change_set_name
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if logical_resource_id is not None:
        kwargs["LogicalResourceId"] = logical_resource_id
    try:
        resp = client.describe_change_set_hooks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe change set hooks") from exc
    return DescribeChangeSetHooksResult(
        change_set_id=resp.get("ChangeSetId"),
        change_set_name=resp.get("ChangeSetName"),
        hooks=resp.get("Hooks"),
        status=resp.get("Status"),
        next_token=resp.get("NextToken"),
        stack_id=resp.get("StackId"),
        stack_name=resp.get("StackName"),
    )


def describe_generated_template(
    generated_template_name: str,
    region_name: str | None = None,
) -> DescribeGeneratedTemplateResult:
    """Describe generated template.

    Args:
        generated_template_name: Generated template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GeneratedTemplateName"] = generated_template_name
    try:
        resp = client.describe_generated_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe generated template") from exc
    return DescribeGeneratedTemplateResult(
        generated_template_id=resp.get("GeneratedTemplateId"),
        generated_template_name=resp.get("GeneratedTemplateName"),
        resources=resp.get("Resources"),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        creation_time=resp.get("CreationTime"),
        last_updated_time=resp.get("LastUpdatedTime"),
        progress=resp.get("Progress"),
        stack_id=resp.get("StackId"),
        template_configuration=resp.get("TemplateConfiguration"),
        total_warnings=resp.get("TotalWarnings"),
    )


def describe_organizations_access(
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DescribeOrganizationsAccessResult:
    """Describe organizations access.

    Args:
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.describe_organizations_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organizations access") from exc
    return DescribeOrganizationsAccessResult(
        status=resp.get("Status"),
    )


def describe_publisher(
    *,
    publisher_id: str | None = None,
    region_name: str | None = None,
) -> DescribePublisherResult:
    """Describe publisher.

    Args:
        publisher_id: Publisher id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if publisher_id is not None:
        kwargs["PublisherId"] = publisher_id
    try:
        resp = client.describe_publisher(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe publisher") from exc
    return DescribePublisherResult(
        publisher_id=resp.get("PublisherId"),
        publisher_status=resp.get("PublisherStatus"),
        identity_provider=resp.get("IdentityProvider"),
        publisher_profile=resp.get("PublisherProfile"),
    )


def describe_resource_scan(
    resource_scan_id: str,
    region_name: str | None = None,
) -> DescribeResourceScanResult:
    """Describe resource scan.

    Args:
        resource_scan_id: Resource scan id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceScanId"] = resource_scan_id
    try:
        resp = client.describe_resource_scan(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe resource scan") from exc
    return DescribeResourceScanResult(
        resource_scan_id=resp.get("ResourceScanId"),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
        percentage_completed=resp.get("PercentageCompleted"),
        resource_types=resp.get("ResourceTypes"),
        resources_scanned=resp.get("ResourcesScanned"),
        resources_read=resp.get("ResourcesRead"),
        scan_filters=resp.get("ScanFilters"),
    )


def describe_stack_drift_detection_status(
    stack_drift_detection_id: str,
    region_name: str | None = None,
) -> DescribeStackDriftDetectionStatusResult:
    """Describe stack drift detection status.

    Args:
        stack_drift_detection_id: Stack drift detection id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackDriftDetectionId"] = stack_drift_detection_id
    try:
        resp = client.describe_stack_drift_detection_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack drift detection status") from exc
    return DescribeStackDriftDetectionStatusResult(
        stack_id=resp.get("StackId"),
        stack_drift_detection_id=resp.get("StackDriftDetectionId"),
        stack_drift_status=resp.get("StackDriftStatus"),
        detection_status=resp.get("DetectionStatus"),
        detection_status_reason=resp.get("DetectionStatusReason"),
        drifted_stack_resource_count=resp.get("DriftedStackResourceCount"),
        timestamp=resp.get("Timestamp"),
    )


def describe_stack_events(
    stack_name: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeStackEventsResult:
    """Describe stack events.

    Args:
        stack_name: Stack name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_stack_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack events") from exc
    return DescribeStackEventsResult(
        stack_events=resp.get("StackEvents"),
        next_token=resp.get("NextToken"),
    )


def describe_stack_instance(
    stack_set_name: str,
    stack_instance_account: str,
    stack_instance_region: str,
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DescribeStackInstanceResult:
    """Describe stack instance.

    Args:
        stack_set_name: Stack set name.
        stack_instance_account: Stack instance account.
        stack_instance_region: Stack instance region.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["StackInstanceAccount"] = stack_instance_account
    kwargs["StackInstanceRegion"] = stack_instance_region
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.describe_stack_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack instance") from exc
    return DescribeStackInstanceResult(
        stack_instance=resp.get("StackInstance"),
    )


def describe_stack_refactor(
    stack_refactor_id: str,
    region_name: str | None = None,
) -> DescribeStackRefactorResult:
    """Describe stack refactor.

    Args:
        stack_refactor_id: Stack refactor id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackRefactorId"] = stack_refactor_id
    try:
        resp = client.describe_stack_refactor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack refactor") from exc
    return DescribeStackRefactorResult(
        description=resp.get("Description"),
        stack_refactor_id=resp.get("StackRefactorId"),
        stack_ids=resp.get("StackIds"),
        execution_status=resp.get("ExecutionStatus"),
        execution_status_reason=resp.get("ExecutionStatusReason"),
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
    )


def describe_stack_resource(
    stack_name: str,
    logical_resource_id: str,
    region_name: str | None = None,
) -> DescribeStackResourceResult:
    """Describe stack resource.

    Args:
        stack_name: Stack name.
        logical_resource_id: Logical resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    kwargs["LogicalResourceId"] = logical_resource_id
    try:
        resp = client.describe_stack_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack resource") from exc
    return DescribeStackResourceResult(
        stack_resource_detail=resp.get("StackResourceDetail"),
    )


def describe_stack_resource_drifts(
    stack_name: str,
    *,
    stack_resource_drift_status_filters: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeStackResourceDriftsResult:
    """Describe stack resource drifts.

    Args:
        stack_name: Stack name.
        stack_resource_drift_status_filters: Stack resource drift status filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if stack_resource_drift_status_filters is not None:
        kwargs["StackResourceDriftStatusFilters"] = stack_resource_drift_status_filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_stack_resource_drifts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack resource drifts") from exc
    return DescribeStackResourceDriftsResult(
        stack_resource_drifts=resp.get("StackResourceDrifts"),
        next_token=resp.get("NextToken"),
    )


def describe_stack_resources(
    *,
    stack_name: str | None = None,
    logical_resource_id: str | None = None,
    physical_resource_id: str | None = None,
    region_name: str | None = None,
) -> DescribeStackResourcesResult:
    """Describe stack resources.

    Args:
        stack_name: Stack name.
        logical_resource_id: Logical resource id.
        physical_resource_id: Physical resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if logical_resource_id is not None:
        kwargs["LogicalResourceId"] = logical_resource_id
    if physical_resource_id is not None:
        kwargs["PhysicalResourceId"] = physical_resource_id
    try:
        resp = client.describe_stack_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack resources") from exc
    return DescribeStackResourcesResult(
        stack_resources=resp.get("StackResources"),
    )


def describe_stack_set(
    stack_set_name: str,
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DescribeStackSetResult:
    """Describe stack set.

    Args:
        stack_set_name: Stack set name.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.describe_stack_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack set") from exc
    return DescribeStackSetResult(
        stack_set=resp.get("StackSet"),
    )


def describe_stack_set_operation(
    stack_set_name: str,
    operation_id: str,
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DescribeStackSetOperationResult:
    """Describe stack set operation.

    Args:
        stack_set_name: Stack set name.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.describe_stack_set_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stack set operation") from exc
    return DescribeStackSetOperationResult(
        stack_set_operation=resp.get("StackSetOperation"),
    )


def describe_stacks(
    *,
    stack_name: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeStacksResult:
    """Describe stacks.

    Args:
        stack_name: Stack name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_stacks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe stacks") from exc
    return DescribeStacksResult(
        stacks=resp.get("Stacks"),
        next_token=resp.get("NextToken"),
    )


def describe_type(
    *,
    type_value: str | None = None,
    type_name: str | None = None,
    arn: str | None = None,
    version_id: str | None = None,
    publisher_id: str | None = None,
    public_version_number: str | None = None,
    region_name: str | None = None,
) -> DescribeTypeResult:
    """Describe type.

    Args:
        type_value: Type value.
        type_name: Type name.
        arn: Arn.
        version_id: Version id.
        publisher_id: Publisher id.
        public_version_number: Public version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if arn is not None:
        kwargs["Arn"] = arn
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if publisher_id is not None:
        kwargs["PublisherId"] = publisher_id
    if public_version_number is not None:
        kwargs["PublicVersionNumber"] = public_version_number
    try:
        resp = client.describe_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe type") from exc
    return DescribeTypeResult(
        arn=resp.get("Arn"),
        type_value=resp.get("Type"),
        type_name=resp.get("TypeName"),
        default_version_id=resp.get("DefaultVersionId"),
        is_default_version=resp.get("IsDefaultVersion"),
        type_tests_status=resp.get("TypeTestsStatus"),
        type_tests_status_description=resp.get("TypeTestsStatusDescription"),
        description=resp.get("Description"),
        model_schema=resp.get("Schema"),
        provisioning_type=resp.get("ProvisioningType"),
        deprecated_status=resp.get("DeprecatedStatus"),
        logging_config=resp.get("LoggingConfig"),
        required_activated_types=resp.get("RequiredActivatedTypes"),
        execution_role_arn=resp.get("ExecutionRoleArn"),
        visibility=resp.get("Visibility"),
        source_url=resp.get("SourceUrl"),
        documentation_url=resp.get("DocumentationUrl"),
        last_updated=resp.get("LastUpdated"),
        time_created=resp.get("TimeCreated"),
        configuration_schema=resp.get("ConfigurationSchema"),
        publisher_id=resp.get("PublisherId"),
        original_type_name=resp.get("OriginalTypeName"),
        original_type_arn=resp.get("OriginalTypeArn"),
        public_version_number=resp.get("PublicVersionNumber"),
        latest_public_version=resp.get("LatestPublicVersion"),
        is_activated=resp.get("IsActivated"),
        auto_update=resp.get("AutoUpdate"),
    )


def describe_type_registration(
    registration_token: str,
    region_name: str | None = None,
) -> DescribeTypeRegistrationResult:
    """Describe type registration.

    Args:
        registration_token: Registration token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegistrationToken"] = registration_token
    try:
        resp = client.describe_type_registration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe type registration") from exc
    return DescribeTypeRegistrationResult(
        progress_status=resp.get("ProgressStatus"),
        description=resp.get("Description"),
        type_arn=resp.get("TypeArn"),
        type_version_arn=resp.get("TypeVersionArn"),
    )


def detect_stack_drift(
    stack_name: str,
    *,
    logical_resource_ids: list[str] | None = None,
    region_name: str | None = None,
) -> DetectStackDriftResult:
    """Detect stack drift.

    Args:
        stack_name: Stack name.
        logical_resource_ids: Logical resource ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if logical_resource_ids is not None:
        kwargs["LogicalResourceIds"] = logical_resource_ids
    try:
        resp = client.detect_stack_drift(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect stack drift") from exc
    return DetectStackDriftResult(
        stack_drift_detection_id=resp.get("StackDriftDetectionId"),
    )


def detect_stack_resource_drift(
    stack_name: str,
    logical_resource_id: str,
    region_name: str | None = None,
) -> DetectStackResourceDriftResult:
    """Detect stack resource drift.

    Args:
        stack_name: Stack name.
        logical_resource_id: Logical resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    kwargs["LogicalResourceId"] = logical_resource_id
    try:
        resp = client.detect_stack_resource_drift(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect stack resource drift") from exc
    return DetectStackResourceDriftResult(
        stack_resource_drift=resp.get("StackResourceDrift"),
    )


def detect_stack_set_drift(
    stack_set_name: str,
    *,
    operation_preferences: dict[str, Any] | None = None,
    operation_id: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> DetectStackSetDriftResult:
    """Detect stack set drift.

    Args:
        stack_set_name: Stack set name.
        operation_preferences: Operation preferences.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.detect_stack_set_drift(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detect stack set drift") from exc
    return DetectStackSetDriftResult(
        operation_id=resp.get("OperationId"),
    )


def estimate_template_cost(
    *,
    template_body: str | None = None,
    template_url: str | None = None,
    parameters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> EstimateTemplateCostResult:
    """Estimate template cost.

    Args:
        template_body: Template body.
        template_url: Template url.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = client.estimate_template_cost(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to estimate template cost") from exc
    return EstimateTemplateCostResult(
        url=resp.get("Url"),
    )


def execute_change_set(
    change_set_name: str,
    *,
    stack_name: str | None = None,
    client_request_token: str | None = None,
    disable_rollback: bool | None = None,
    retain_except_on_create: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Execute change set.

    Args:
        change_set_name: Change set name.
        stack_name: Stack name.
        client_request_token: Client request token.
        disable_rollback: Disable rollback.
        retain_except_on_create: Retain except on create.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ChangeSetName"] = change_set_name
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if disable_rollback is not None:
        kwargs["DisableRollback"] = disable_rollback
    if retain_except_on_create is not None:
        kwargs["RetainExceptOnCreate"] = retain_except_on_create
    try:
        client.execute_change_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute change set") from exc
    return None


def execute_stack_refactor(
    stack_refactor_id: str,
    region_name: str | None = None,
) -> None:
    """Execute stack refactor.

    Args:
        stack_refactor_id: Stack refactor id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackRefactorId"] = stack_refactor_id
    try:
        client.execute_stack_refactor(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute stack refactor") from exc
    return None


def get_generated_template(
    generated_template_name: str,
    *,
    format: str | None = None,
    region_name: str | None = None,
) -> GetGeneratedTemplateResult:
    """Get generated template.

    Args:
        generated_template_name: Generated template name.
        format: Format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GeneratedTemplateName"] = generated_template_name
    if format is not None:
        kwargs["Format"] = format
    try:
        resp = client.get_generated_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get generated template") from exc
    return GetGeneratedTemplateResult(
        status=resp.get("Status"),
        template_body=resp.get("TemplateBody"),
    )


def get_hook_result(
    *,
    hook_result_id: str | None = None,
    region_name: str | None = None,
) -> GetHookResultResult:
    """Get hook result.

    Args:
        hook_result_id: Hook result id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if hook_result_id is not None:
        kwargs["HookResultId"] = hook_result_id
    try:
        resp = client.get_hook_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get hook result") from exc
    return GetHookResultResult(
        hook_result_id=resp.get("HookResultId"),
        invocation_point=resp.get("InvocationPoint"),
        failure_mode=resp.get("FailureMode"),
        type_name=resp.get("TypeName"),
        original_type_name=resp.get("OriginalTypeName"),
        type_version_id=resp.get("TypeVersionId"),
        type_configuration_version_id=resp.get("TypeConfigurationVersionId"),
        type_arn=resp.get("TypeArn"),
        status=resp.get("Status"),
        hook_status_reason=resp.get("HookStatusReason"),
        invoked_at=resp.get("InvokedAt"),
        target=resp.get("Target"),
        annotations=resp.get("Annotations"),
    )


def get_stack_policy(
    stack_name: str,
    region_name: str | None = None,
) -> GetStackPolicyResult:
    """Get stack policy.

    Args:
        stack_name: Stack name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    try:
        resp = client.get_stack_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get stack policy") from exc
    return GetStackPolicyResult(
        stack_policy_body=resp.get("StackPolicyBody"),
    )


def get_template(
    *,
    stack_name: str | None = None,
    change_set_name: str | None = None,
    template_stage: str | None = None,
    region_name: str | None = None,
) -> GetTemplateResult:
    """Get template.

    Args:
        stack_name: Stack name.
        change_set_name: Change set name.
        template_stage: Template stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if change_set_name is not None:
        kwargs["ChangeSetName"] = change_set_name
    if template_stage is not None:
        kwargs["TemplateStage"] = template_stage
    try:
        resp = client.get_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get template") from exc
    return GetTemplateResult(
        template_body=resp.get("TemplateBody"),
        stages_available=resp.get("StagesAvailable"),
    )


def get_template_summary(
    *,
    template_body: str | None = None,
    template_url: str | None = None,
    stack_name: str | None = None,
    stack_set_name: str | None = None,
    call_as: str | None = None,
    template_summary_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetTemplateSummaryResult:
    """Get template summary.

    Args:
        template_body: Template body.
        template_url: Template url.
        stack_name: Stack name.
        stack_set_name: Stack set name.
        call_as: Call as.
        template_summary_config: Template summary config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    if stack_name is not None:
        kwargs["StackName"] = stack_name
    if stack_set_name is not None:
        kwargs["StackSetName"] = stack_set_name
    if call_as is not None:
        kwargs["CallAs"] = call_as
    if template_summary_config is not None:
        kwargs["TemplateSummaryConfig"] = template_summary_config
    try:
        resp = client.get_template_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get template summary") from exc
    return GetTemplateSummaryResult(
        parameters=resp.get("Parameters"),
        description=resp.get("Description"),
        capabilities=resp.get("Capabilities"),
        capabilities_reason=resp.get("CapabilitiesReason"),
        resource_types=resp.get("ResourceTypes"),
        version=resp.get("Version"),
        metadata=resp.get("Metadata"),
        declared_transforms=resp.get("DeclaredTransforms"),
        resource_identifier_summaries=resp.get("ResourceIdentifierSummaries"),
        warnings=resp.get("Warnings"),
    )


def import_stacks_to_stack_set(
    stack_set_name: str,
    *,
    stack_ids: list[str] | None = None,
    stack_ids_url: str | None = None,
    organizational_unit_ids: list[str] | None = None,
    operation_preferences: dict[str, Any] | None = None,
    operation_id: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ImportStacksToStackSetResult:
    """Import stacks to stack set.

    Args:
        stack_set_name: Stack set name.
        stack_ids: Stack ids.
        stack_ids_url: Stack ids url.
        organizational_unit_ids: Organizational unit ids.
        operation_preferences: Operation preferences.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if stack_ids is not None:
        kwargs["StackIds"] = stack_ids
    if stack_ids_url is not None:
        kwargs["StackIdsUrl"] = stack_ids_url
    if organizational_unit_ids is not None:
        kwargs["OrganizationalUnitIds"] = organizational_unit_ids
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.import_stacks_to_stack_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import stacks to stack set") from exc
    return ImportStacksToStackSetResult(
        operation_id=resp.get("OperationId"),
    )


def list_change_sets(
    stack_name: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListChangeSetsResult:
    """List change sets.

    Args:
        stack_name: Stack name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_change_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list change sets") from exc
    return ListChangeSetsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_exports(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListExportsResult:
    """List exports.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_exports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list exports") from exc
    return ListExportsResult(
        exports=resp.get("Exports"),
        next_token=resp.get("NextToken"),
    )


def list_generated_templates(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListGeneratedTemplatesResult:
    """List generated templates.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_generated_templates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list generated templates") from exc
    return ListGeneratedTemplatesResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_hook_results(
    *,
    target_type: str | None = None,
    target_id: str | None = None,
    type_arn: str | None = None,
    status: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListHookResultsResult:
    """List hook results.

    Args:
        target_type: Target type.
        target_id: Target id.
        type_arn: Type arn.
        status: Status.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if target_type is not None:
        kwargs["TargetType"] = target_type
    if target_id is not None:
        kwargs["TargetId"] = target_id
    if type_arn is not None:
        kwargs["TypeArn"] = type_arn
    if status is not None:
        kwargs["Status"] = status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_hook_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list hook results") from exc
    return ListHookResultsResult(
        target_type=resp.get("TargetType"),
        target_id=resp.get("TargetId"),
        hook_results=resp.get("HookResults"),
        next_token=resp.get("NextToken"),
    )


def list_imports(
    export_name: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListImportsResult:
    """List imports.

    Args:
        export_name: Export name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExportName"] = export_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_imports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list imports") from exc
    return ListImportsResult(
        imports=resp.get("Imports"),
        next_token=resp.get("NextToken"),
    )


def list_resource_scan_related_resources(
    resource_scan_id: str,
    resources: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListResourceScanRelatedResourcesResult:
    """List resource scan related resources.

    Args:
        resource_scan_id: Resource scan id.
        resources: Resources.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceScanId"] = resource_scan_id
    kwargs["Resources"] = resources
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_resource_scan_related_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource scan related resources") from exc
    return ListResourceScanRelatedResourcesResult(
        related_resources=resp.get("RelatedResources"),
        next_token=resp.get("NextToken"),
    )


def list_resource_scan_resources(
    resource_scan_id: str,
    *,
    resource_identifier: str | None = None,
    resource_type_prefix: str | None = None,
    tag_key: str | None = None,
    tag_value: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListResourceScanResourcesResult:
    """List resource scan resources.

    Args:
        resource_scan_id: Resource scan id.
        resource_identifier: Resource identifier.
        resource_type_prefix: Resource type prefix.
        tag_key: Tag key.
        tag_value: Tag value.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceScanId"] = resource_scan_id
    if resource_identifier is not None:
        kwargs["ResourceIdentifier"] = resource_identifier
    if resource_type_prefix is not None:
        kwargs["ResourceTypePrefix"] = resource_type_prefix
    if tag_key is not None:
        kwargs["TagKey"] = tag_key
    if tag_value is not None:
        kwargs["TagValue"] = tag_value
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_resource_scan_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource scan resources") from exc
    return ListResourceScanResourcesResult(
        resources=resp.get("Resources"),
        next_token=resp.get("NextToken"),
    )


def list_resource_scans(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    scan_type_filter: str | None = None,
    region_name: str | None = None,
) -> ListResourceScansResult:
    """List resource scans.

    Args:
        next_token: Next token.
        max_results: Max results.
        scan_type_filter: Scan type filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if scan_type_filter is not None:
        kwargs["ScanTypeFilter"] = scan_type_filter
    try:
        resp = client.list_resource_scans(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource scans") from exc
    return ListResourceScansResult(
        resource_scan_summaries=resp.get("ResourceScanSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_instance_resource_drifts(
    stack_set_name: str,
    stack_instance_account: str,
    stack_instance_region: str,
    operation_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    stack_instance_resource_drift_statuses: list[str] | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ListStackInstanceResourceDriftsResult:
    """List stack instance resource drifts.

    Args:
        stack_set_name: Stack set name.
        stack_instance_account: Stack instance account.
        stack_instance_region: Stack instance region.
        operation_id: Operation id.
        next_token: Next token.
        max_results: Max results.
        stack_instance_resource_drift_statuses: Stack instance resource drift statuses.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["StackInstanceAccount"] = stack_instance_account
    kwargs["StackInstanceRegion"] = stack_instance_region
    kwargs["OperationId"] = operation_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if stack_instance_resource_drift_statuses is not None:
        kwargs["StackInstanceResourceDriftStatuses"] = stack_instance_resource_drift_statuses
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.list_stack_instance_resource_drifts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack instance resource drifts") from exc
    return ListStackInstanceResourceDriftsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_instances(
    stack_set_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    stack_instance_account: str | None = None,
    stack_instance_region: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ListStackInstancesResult:
    """List stack instances.

    Args:
        stack_set_name: Stack set name.
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        stack_instance_account: Stack instance account.
        stack_instance_region: Stack instance region.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    if stack_instance_account is not None:
        kwargs["StackInstanceAccount"] = stack_instance_account
    if stack_instance_region is not None:
        kwargs["StackInstanceRegion"] = stack_instance_region
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.list_stack_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack instances") from exc
    return ListStackInstancesResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_refactor_actions(
    stack_refactor_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStackRefactorActionsResult:
    """List stack refactor actions.

    Args:
        stack_refactor_id: Stack refactor id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackRefactorId"] = stack_refactor_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_stack_refactor_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack refactor actions") from exc
    return ListStackRefactorActionsResult(
        stack_refactor_actions=resp.get("StackRefactorActions"),
        next_token=resp.get("NextToken"),
    )


def list_stack_refactors(
    *,
    execution_status_filter: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStackRefactorsResult:
    """List stack refactors.

    Args:
        execution_status_filter: Execution status filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if execution_status_filter is not None:
        kwargs["ExecutionStatusFilter"] = execution_status_filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_stack_refactors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack refactors") from exc
    return ListStackRefactorsResult(
        stack_refactor_summaries=resp.get("StackRefactorSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_resources(
    stack_name: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListStackResourcesResult:
    """List stack resources.

    Args:
        stack_name: Stack name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_stack_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack resources") from exc
    return ListStackResourcesResult(
        stack_resource_summaries=resp.get("StackResourceSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_set_auto_deployment_targets(
    stack_set_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ListStackSetAutoDeploymentTargetsResult:
    """List stack set auto deployment targets.

    Args:
        stack_set_name: Stack set name.
        next_token: Next token.
        max_results: Max results.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.list_stack_set_auto_deployment_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack set auto deployment targets") from exc
    return ListStackSetAutoDeploymentTargetsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_set_operation_results(
    stack_set_name: str,
    operation_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    call_as: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListStackSetOperationResultsResult:
    """List stack set operation results.

    Args:
        stack_set_name: Stack set name.
        operation_id: Operation id.
        next_token: Next token.
        max_results: Max results.
        call_as: Call as.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["OperationId"] = operation_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if call_as is not None:
        kwargs["CallAs"] = call_as
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.list_stack_set_operation_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack set operation results") from exc
    return ListStackSetOperationResultsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_set_operations(
    stack_set_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ListStackSetOperationsResult:
    """List stack set operations.

    Args:
        stack_set_name: Stack set name.
        next_token: Next token.
        max_results: Max results.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.list_stack_set_operations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack set operations") from exc
    return ListStackSetOperationsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_stack_sets(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    status: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> ListStackSetsResult:
    """List stack sets.

    Args:
        next_token: Next token.
        max_results: Max results.
        status: Status.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if status is not None:
        kwargs["Status"] = status
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.list_stack_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stack sets") from exc
    return ListStackSetsResult(
        summaries=resp.get("Summaries"),
        next_token=resp.get("NextToken"),
    )


def list_type_registrations(
    *,
    type_value: str | None = None,
    type_name: str | None = None,
    type_arn: str | None = None,
    registration_status_filter: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTypeRegistrationsResult:
    """List type registrations.

    Args:
        type_value: Type value.
        type_name: Type name.
        type_arn: Type arn.
        registration_status_filter: Registration status filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if type_arn is not None:
        kwargs["TypeArn"] = type_arn
    if registration_status_filter is not None:
        kwargs["RegistrationStatusFilter"] = registration_status_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_type_registrations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list type registrations") from exc
    return ListTypeRegistrationsResult(
        registration_token_list=resp.get("RegistrationTokenList"),
        next_token=resp.get("NextToken"),
    )


def list_type_versions(
    *,
    type_value: str | None = None,
    type_name: str | None = None,
    arn: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    deprecated_status: str | None = None,
    publisher_id: str | None = None,
    region_name: str | None = None,
) -> ListTypeVersionsResult:
    """List type versions.

    Args:
        type_value: Type value.
        type_name: Type name.
        arn: Arn.
        max_results: Max results.
        next_token: Next token.
        deprecated_status: Deprecated status.
        publisher_id: Publisher id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if arn is not None:
        kwargs["Arn"] = arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if deprecated_status is not None:
        kwargs["DeprecatedStatus"] = deprecated_status
    if publisher_id is not None:
        kwargs["PublisherId"] = publisher_id
    try:
        resp = client.list_type_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list type versions") from exc
    return ListTypeVersionsResult(
        type_version_summaries=resp.get("TypeVersionSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_types(
    *,
    visibility: str | None = None,
    provisioning_type: str | None = None,
    deprecated_status: str | None = None,
    type_value: str | None = None,
    filters: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTypesResult:
    """List types.

    Args:
        visibility: Visibility.
        provisioning_type: Provisioning type.
        deprecated_status: Deprecated status.
        type_value: Type value.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if visibility is not None:
        kwargs["Visibility"] = visibility
    if provisioning_type is not None:
        kwargs["ProvisioningType"] = provisioning_type
    if deprecated_status is not None:
        kwargs["DeprecatedStatus"] = deprecated_status
    if type_value is not None:
        kwargs["Type"] = type_value
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list types") from exc
    return ListTypesResult(
        type_summaries=resp.get("TypeSummaries"),
        next_token=resp.get("NextToken"),
    )


def publish_type(
    *,
    type_value: str | None = None,
    arn: str | None = None,
    type_name: str | None = None,
    public_version_number: str | None = None,
    region_name: str | None = None,
) -> PublishTypeResult:
    """Publish type.

    Args:
        type_value: Type value.
        arn: Arn.
        type_name: Type name.
        public_version_number: Public version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if type_value is not None:
        kwargs["Type"] = type_value
    if arn is not None:
        kwargs["Arn"] = arn
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if public_version_number is not None:
        kwargs["PublicVersionNumber"] = public_version_number
    try:
        resp = client.publish_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish type") from exc
    return PublishTypeResult(
        public_type_arn=resp.get("PublicTypeArn"),
    )


def record_handler_progress(
    bearer_token: str,
    operation_status: str,
    *,
    current_operation_status: str | None = None,
    status_message: str | None = None,
    error_code: str | None = None,
    resource_model: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Record handler progress.

    Args:
        bearer_token: Bearer token.
        operation_status: Operation status.
        current_operation_status: Current operation status.
        status_message: Status message.
        error_code: Error code.
        resource_model: Resource model.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BearerToken"] = bearer_token
    kwargs["OperationStatus"] = operation_status
    if current_operation_status is not None:
        kwargs["CurrentOperationStatus"] = current_operation_status
    if status_message is not None:
        kwargs["StatusMessage"] = status_message
    if error_code is not None:
        kwargs["ErrorCode"] = error_code
    if resource_model is not None:
        kwargs["ResourceModel"] = resource_model
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        client.record_handler_progress(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to record handler progress") from exc
    return None


def register_publisher(
    *,
    accept_terms_and_conditions: bool | None = None,
    connection_arn: str | None = None,
    region_name: str | None = None,
) -> RegisterPublisherResult:
    """Register publisher.

    Args:
        accept_terms_and_conditions: Accept terms and conditions.
        connection_arn: Connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if accept_terms_and_conditions is not None:
        kwargs["AcceptTermsAndConditions"] = accept_terms_and_conditions
    if connection_arn is not None:
        kwargs["ConnectionArn"] = connection_arn
    try:
        resp = client.register_publisher(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register publisher") from exc
    return RegisterPublisherResult(
        publisher_id=resp.get("PublisherId"),
    )


def register_type(
    type_name: str,
    schema_handler_package: str,
    *,
    type_value: str | None = None,
    logging_config: dict[str, Any] | None = None,
    execution_role_arn: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> RegisterTypeResult:
    """Register type.

    Args:
        type_name: Type name.
        schema_handler_package: Schema handler package.
        type_value: Type value.
        logging_config: Logging config.
        execution_role_arn: Execution role arn.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TypeName"] = type_name
    kwargs["SchemaHandlerPackage"] = schema_handler_package
    if type_value is not None:
        kwargs["Type"] = type_value
    if logging_config is not None:
        kwargs["LoggingConfig"] = logging_config
    if execution_role_arn is not None:
        kwargs["ExecutionRoleArn"] = execution_role_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.register_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register type") from exc
    return RegisterTypeResult(
        registration_token=resp.get("RegistrationToken"),
    )


def rollback_stack(
    stack_name: str,
    *,
    role_arn: str | None = None,
    client_request_token: str | None = None,
    retain_except_on_create: bool | None = None,
    region_name: str | None = None,
) -> RollbackStackResult:
    """Rollback stack.

    Args:
        stack_name: Stack name.
        role_arn: Role arn.
        client_request_token: Client request token.
        retain_except_on_create: Retain except on create.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if role_arn is not None:
        kwargs["RoleARN"] = role_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if retain_except_on_create is not None:
        kwargs["RetainExceptOnCreate"] = retain_except_on_create
    try:
        resp = client.rollback_stack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rollback stack") from exc
    return RollbackStackResult(
        stack_id=resp.get("StackId"),
    )


def run_type(
    *,
    arn: str | None = None,
    type_value: str | None = None,
    type_name: str | None = None,
    version_id: str | None = None,
    log_delivery_bucket: str | None = None,
    region_name: str | None = None,
) -> RunTypeResult:
    """Run type.

    Args:
        arn: Arn.
        type_value: Type value.
        type_name: Type name.
        version_id: Version id.
        log_delivery_bucket: Log delivery bucket.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if arn is not None:
        kwargs["Arn"] = arn
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if log_delivery_bucket is not None:
        kwargs["LogDeliveryBucket"] = log_delivery_bucket
    try:
        resp = client.test_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run type") from exc
    return RunTypeResult(
        type_version_arn=resp.get("TypeVersionArn"),
    )


def set_stack_policy(
    stack_name: str,
    *,
    stack_policy_body: str | None = None,
    stack_policy_url: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set stack policy.

    Args:
        stack_name: Stack name.
        stack_policy_body: Stack policy body.
        stack_policy_url: Stack policy url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    if stack_policy_body is not None:
        kwargs["StackPolicyBody"] = stack_policy_body
    if stack_policy_url is not None:
        kwargs["StackPolicyURL"] = stack_policy_url
    try:
        client.set_stack_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set stack policy") from exc
    return None


def set_type_configuration(
    configuration: str,
    *,
    type_arn: str | None = None,
    configuration_alias: str | None = None,
    type_name: str | None = None,
    type_value: str | None = None,
    region_name: str | None = None,
) -> SetTypeConfigurationResult:
    """Set type configuration.

    Args:
        configuration: Configuration.
        type_arn: Type arn.
        configuration_alias: Configuration alias.
        type_name: Type name.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Configuration"] = configuration
    if type_arn is not None:
        kwargs["TypeArn"] = type_arn
    if configuration_alias is not None:
        kwargs["ConfigurationAlias"] = configuration_alias
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if type_value is not None:
        kwargs["Type"] = type_value
    try:
        resp = client.set_type_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set type configuration") from exc
    return SetTypeConfigurationResult(
        configuration_arn=resp.get("ConfigurationArn"),
    )


def set_type_default_version(
    *,
    arn: str | None = None,
    type_value: str | None = None,
    type_name: str | None = None,
    version_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set type default version.

    Args:
        arn: Arn.
        type_value: Type value.
        type_name: Type name.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if arn is not None:
        kwargs["Arn"] = arn
    if type_value is not None:
        kwargs["Type"] = type_value
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if version_id is not None:
        kwargs["VersionId"] = version_id
    try:
        client.set_type_default_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set type default version") from exc
    return None


def signal_resource(
    stack_name: str,
    logical_resource_id: str,
    unique_id: str,
    status: str,
    region_name: str | None = None,
) -> None:
    """Signal resource.

    Args:
        stack_name: Stack name.
        logical_resource_id: Logical resource id.
        unique_id: Unique id.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackName"] = stack_name
    kwargs["LogicalResourceId"] = logical_resource_id
    kwargs["UniqueId"] = unique_id
    kwargs["Status"] = status
    try:
        client.signal_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to signal resource") from exc
    return None


def start_resource_scan(
    *,
    client_request_token: str | None = None,
    scan_filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartResourceScanResult:
    """Start resource scan.

    Args:
        client_request_token: Client request token.
        scan_filters: Scan filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if scan_filters is not None:
        kwargs["ScanFilters"] = scan_filters
    try:
        resp = client.start_resource_scan(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start resource scan") from exc
    return StartResourceScanResult(
        resource_scan_id=resp.get("ResourceScanId"),
    )


def stop_stack_set_operation(
    stack_set_name: str,
    operation_id: str,
    *,
    call_as: str | None = None,
    region_name: str | None = None,
) -> None:
    """Stop stack set operation.

    Args:
        stack_set_name: Stack set name.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        client.stop_stack_set_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop stack set operation") from exc
    return None


def update_generated_template(
    generated_template_name: str,
    *,
    new_generated_template_name: str | None = None,
    add_resources: list[dict[str, Any]] | None = None,
    remove_resources: list[str] | None = None,
    refresh_all_resources: bool | None = None,
    template_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateGeneratedTemplateResult:
    """Update generated template.

    Args:
        generated_template_name: Generated template name.
        new_generated_template_name: New generated template name.
        add_resources: Add resources.
        remove_resources: Remove resources.
        refresh_all_resources: Refresh all resources.
        template_configuration: Template configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GeneratedTemplateName"] = generated_template_name
    if new_generated_template_name is not None:
        kwargs["NewGeneratedTemplateName"] = new_generated_template_name
    if add_resources is not None:
        kwargs["AddResources"] = add_resources
    if remove_resources is not None:
        kwargs["RemoveResources"] = remove_resources
    if refresh_all_resources is not None:
        kwargs["RefreshAllResources"] = refresh_all_resources
    if template_configuration is not None:
        kwargs["TemplateConfiguration"] = template_configuration
    try:
        resp = client.update_generated_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update generated template") from exc
    return UpdateGeneratedTemplateResult(
        generated_template_id=resp.get("GeneratedTemplateId"),
    )


def update_stack_instances(
    stack_set_name: str,
    regions: list[str],
    *,
    accounts: list[str] | None = None,
    deployment_targets: dict[str, Any] | None = None,
    parameter_overrides: list[dict[str, Any]] | None = None,
    operation_preferences: dict[str, Any] | None = None,
    operation_id: str | None = None,
    call_as: str | None = None,
    region_name: str | None = None,
) -> UpdateStackInstancesResult:
    """Update stack instances.

    Args:
        stack_set_name: Stack set name.
        regions: Regions.
        accounts: Accounts.
        deployment_targets: Deployment targets.
        parameter_overrides: Parameter overrides.
        operation_preferences: Operation preferences.
        operation_id: Operation id.
        call_as: Call as.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    kwargs["Regions"] = regions
    if accounts is not None:
        kwargs["Accounts"] = accounts
    if deployment_targets is not None:
        kwargs["DeploymentTargets"] = deployment_targets
    if parameter_overrides is not None:
        kwargs["ParameterOverrides"] = parameter_overrides
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if call_as is not None:
        kwargs["CallAs"] = call_as
    try:
        resp = client.update_stack_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update stack instances") from exc
    return UpdateStackInstancesResult(
        operation_id=resp.get("OperationId"),
    )


def update_stack_set(
    stack_set_name: str,
    *,
    description: str | None = None,
    template_body: str | None = None,
    template_url: str | None = None,
    use_previous_template: bool | None = None,
    parameters: list[dict[str, Any]] | None = None,
    capabilities: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    operation_preferences: dict[str, Any] | None = None,
    administration_role_arn: str | None = None,
    execution_role_name: str | None = None,
    deployment_targets: dict[str, Any] | None = None,
    permission_model: str | None = None,
    auto_deployment: dict[str, Any] | None = None,
    operation_id: str | None = None,
    accounts: list[str] | None = None,
    regions: list[str] | None = None,
    call_as: str | None = None,
    managed_execution: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateStackSetResult:
    """Update stack set.

    Args:
        stack_set_name: Stack set name.
        description: Description.
        template_body: Template body.
        template_url: Template url.
        use_previous_template: Use previous template.
        parameters: Parameters.
        capabilities: Capabilities.
        tags: Tags.
        operation_preferences: Operation preferences.
        administration_role_arn: Administration role arn.
        execution_role_name: Execution role name.
        deployment_targets: Deployment targets.
        permission_model: Permission model.
        auto_deployment: Auto deployment.
        operation_id: Operation id.
        accounts: Accounts.
        regions: Regions.
        call_as: Call as.
        managed_execution: Managed execution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StackSetName"] = stack_set_name
    if description is not None:
        kwargs["Description"] = description
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    if use_previous_template is not None:
        kwargs["UsePreviousTemplate"] = use_previous_template
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if capabilities is not None:
        kwargs["Capabilities"] = capabilities
    if tags is not None:
        kwargs["Tags"] = tags
    if operation_preferences is not None:
        kwargs["OperationPreferences"] = operation_preferences
    if administration_role_arn is not None:
        kwargs["AdministrationRoleARN"] = administration_role_arn
    if execution_role_name is not None:
        kwargs["ExecutionRoleName"] = execution_role_name
    if deployment_targets is not None:
        kwargs["DeploymentTargets"] = deployment_targets
    if permission_model is not None:
        kwargs["PermissionModel"] = permission_model
    if auto_deployment is not None:
        kwargs["AutoDeployment"] = auto_deployment
    if operation_id is not None:
        kwargs["OperationId"] = operation_id
    if accounts is not None:
        kwargs["Accounts"] = accounts
    if regions is not None:
        kwargs["Regions"] = regions
    if call_as is not None:
        kwargs["CallAs"] = call_as
    if managed_execution is not None:
        kwargs["ManagedExecution"] = managed_execution
    try:
        resp = client.update_stack_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update stack set") from exc
    return UpdateStackSetResult(
        operation_id=resp.get("OperationId"),
    )


def update_termination_protection(
    enable_termination_protection: bool,
    stack_name: str,
    region_name: str | None = None,
) -> UpdateTerminationProtectionResult:
    """Update termination protection.

    Args:
        enable_termination_protection: Enable termination protection.
        stack_name: Stack name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EnableTerminationProtection"] = enable_termination_protection
    kwargs["StackName"] = stack_name
    try:
        resp = client.update_termination_protection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update termination protection") from exc
    return UpdateTerminationProtectionResult(
        stack_id=resp.get("StackId"),
    )


def validate_template(
    *,
    template_body: str | None = None,
    template_url: str | None = None,
    region_name: str | None = None,
) -> ValidateTemplateResult:
    """Validate template.

    Args:
        template_body: Template body.
        template_url: Template url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudformation", region_name)
    kwargs: dict[str, Any] = {}
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if template_url is not None:
        kwargs["TemplateURL"] = template_url
    try:
        resp = client.validate_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to validate template") from exc
    return ValidateTemplateResult(
        parameters=resp.get("Parameters"),
        description=resp.get("Description"),
        capabilities=resp.get("Capabilities"),
        capabilities_reason=resp.get("CapabilitiesReason"),
        declared_transforms=resp.get("DeclaredTransforms"),
    )
