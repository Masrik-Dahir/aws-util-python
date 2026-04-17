"""Native async Parameter Store utilities — real non-blocking I/O via :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.parameter_store import (
    AssociateOpsItemRelatedItemResult,
    CancelMaintenanceWindowExecutionResult,
    CreateActivationResult,
    CreateAssociationBatchResult,
    CreateAssociationResult,
    CreateDocumentResult,
    CreateMaintenanceWindowResult,
    CreateOpsItemResult,
    CreateOpsMetadataResult,
    CreatePatchBaselineResult,
    DeleteInventoryResult,
    DeleteMaintenanceWindowResult,
    DeletePatchBaselineResult,
    DeregisterPatchBaselineForPatchGroupResult,
    DeregisterTargetFromMaintenanceWindowResult,
    DeregisterTaskFromMaintenanceWindowResult,
    DescribeActivationsResult,
    DescribeAssociationExecutionsResult,
    DescribeAssociationExecutionTargetsResult,
    DescribeAssociationResult,
    DescribeAutomationExecutionsResult,
    DescribeAutomationStepExecutionsResult,
    DescribeAvailablePatchesResult,
    DescribeDocumentPermissionResult,
    DescribeDocumentResult,
    DescribeEffectiveInstanceAssociationsResult,
    DescribeEffectivePatchesForPatchBaselineResult,
    DescribeInstanceAssociationsStatusResult,
    DescribeInstanceInformationResult,
    DescribeInstancePatchesResult,
    DescribeInstancePatchStatesForPatchGroupResult,
    DescribeInstancePatchStatesResult,
    DescribeInstancePropertiesResult,
    DescribeInventoryDeletionsResult,
    DescribeMaintenanceWindowExecutionsResult,
    DescribeMaintenanceWindowExecutionTaskInvocationsResult,
    DescribeMaintenanceWindowExecutionTasksResult,
    DescribeMaintenanceWindowScheduleResult,
    DescribeMaintenanceWindowsForTargetResult,
    DescribeMaintenanceWindowsResult,
    DescribeMaintenanceWindowTargetsResult,
    DescribeMaintenanceWindowTasksResult,
    DescribeOpsItemsResult,
    DescribePatchBaselinesResult,
    DescribePatchGroupsResult,
    DescribePatchGroupStateResult,
    DescribePatchPropertiesResult,
    DescribeSessionsResult,
    GetAccessTokenResult,
    GetAutomationExecutionResult,
    GetCalendarStateResult,
    GetCommandInvocationResult,
    GetConnectionStatusResult,
    GetDefaultPatchBaselineResult,
    GetDeployablePatchSnapshotForInstanceResult,
    GetDocumentResult,
    GetExecutionPreviewResult,
    GetInventoryResult,
    GetInventorySchemaResult,
    GetMaintenanceWindowExecutionResult,
    GetMaintenanceWindowExecutionTaskInvocationResult,
    GetMaintenanceWindowExecutionTaskResult,
    GetMaintenanceWindowResult,
    GetMaintenanceWindowTaskResult,
    GetOpsItemResult,
    GetOpsMetadataResult,
    GetOpsSummaryResult,
    GetParameterHistoryResult,
    GetParametersResult,
    GetPatchBaselineForPatchGroupResult,
    GetPatchBaselineResult,
    GetResourcePoliciesResult,
    GetServiceSettingResult,
    LabelParameterVersionResult,
    ListAssociationsResult,
    ListAssociationVersionsResult,
    ListCommandInvocationsResult,
    ListCommandsResult,
    ListComplianceItemsResult,
    ListComplianceSummariesResult,
    ListDocumentMetadataHistoryResult,
    ListDocumentsResult,
    ListDocumentVersionsResult,
    ListInventoryEntriesResult,
    ListNodesResult,
    ListNodesSummaryResult,
    ListOpsItemEventsResult,
    ListOpsItemRelatedItemsResult,
    ListOpsMetadataResult,
    ListResourceComplianceSummariesResult,
    ListResourceDataSyncResult,
    ListTagsForResourceResult,
    PutInventoryResult,
    PutResourcePolicyResult,
    RegisterDefaultPatchBaselineResult,
    RegisterPatchBaselineForPatchGroupResult,
    RegisterTargetWithMaintenanceWindowResult,
    RegisterTaskWithMaintenanceWindowResult,
    ResetServiceSettingResult,
    ResumeSessionResult,
    SendCommandResult,
    StartAccessRequestResult,
    StartAutomationExecutionResult,
    StartChangeRequestExecutionResult,
    StartExecutionPreviewResult,
    StartSessionResult,
    TerminateSessionResult,
    UnlabelParameterVersionResult,
    UpdateAssociationResult,
    UpdateAssociationStatusResult,
    UpdateDocumentDefaultVersionResult,
    UpdateDocumentResult,
    UpdateMaintenanceWindowResult,
    UpdateMaintenanceWindowTargetResult,
    UpdateMaintenanceWindowTaskResult,
    UpdateOpsMetadataResult,
    UpdatePatchBaselineResult,
)

__all__ = [
    "AssociateOpsItemRelatedItemResult",
    "CancelMaintenanceWindowExecutionResult",
    "CreateActivationResult",
    "CreateAssociationBatchResult",
    "CreateAssociationResult",
    "CreateDocumentResult",
    "CreateMaintenanceWindowResult",
    "CreateOpsItemResult",
    "CreateOpsMetadataResult",
    "CreatePatchBaselineResult",
    "DeleteInventoryResult",
    "DeleteMaintenanceWindowResult",
    "DeletePatchBaselineResult",
    "DeregisterPatchBaselineForPatchGroupResult",
    "DeregisterTargetFromMaintenanceWindowResult",
    "DeregisterTaskFromMaintenanceWindowResult",
    "DescribeActivationsResult",
    "DescribeAssociationExecutionTargetsResult",
    "DescribeAssociationExecutionsResult",
    "DescribeAssociationResult",
    "DescribeAutomationExecutionsResult",
    "DescribeAutomationStepExecutionsResult",
    "DescribeAvailablePatchesResult",
    "DescribeDocumentPermissionResult",
    "DescribeDocumentResult",
    "DescribeEffectiveInstanceAssociationsResult",
    "DescribeEffectivePatchesForPatchBaselineResult",
    "DescribeInstanceAssociationsStatusResult",
    "DescribeInstanceInformationResult",
    "DescribeInstancePatchStatesForPatchGroupResult",
    "DescribeInstancePatchStatesResult",
    "DescribeInstancePatchesResult",
    "DescribeInstancePropertiesResult",
    "DescribeInventoryDeletionsResult",
    "DescribeMaintenanceWindowExecutionTaskInvocationsResult",
    "DescribeMaintenanceWindowExecutionTasksResult",
    "DescribeMaintenanceWindowExecutionsResult",
    "DescribeMaintenanceWindowScheduleResult",
    "DescribeMaintenanceWindowTargetsResult",
    "DescribeMaintenanceWindowTasksResult",
    "DescribeMaintenanceWindowsForTargetResult",
    "DescribeMaintenanceWindowsResult",
    "DescribeOpsItemsResult",
    "DescribePatchBaselinesResult",
    "DescribePatchGroupStateResult",
    "DescribePatchGroupsResult",
    "DescribePatchPropertiesResult",
    "DescribeSessionsResult",
    "GetAccessTokenResult",
    "GetAutomationExecutionResult",
    "GetCalendarStateResult",
    "GetCommandInvocationResult",
    "GetConnectionStatusResult",
    "GetDefaultPatchBaselineResult",
    "GetDeployablePatchSnapshotForInstanceResult",
    "GetDocumentResult",
    "GetExecutionPreviewResult",
    "GetInventoryResult",
    "GetInventorySchemaResult",
    "GetMaintenanceWindowExecutionResult",
    "GetMaintenanceWindowExecutionTaskInvocationResult",
    "GetMaintenanceWindowExecutionTaskResult",
    "GetMaintenanceWindowResult",
    "GetMaintenanceWindowTaskResult",
    "GetOpsItemResult",
    "GetOpsMetadataResult",
    "GetOpsSummaryResult",
    "GetParameterHistoryResult",
    "GetParametersResult",
    "GetPatchBaselineForPatchGroupResult",
    "GetPatchBaselineResult",
    "GetResourcePoliciesResult",
    "GetServiceSettingResult",
    "LabelParameterVersionResult",
    "ListAssociationVersionsResult",
    "ListAssociationsResult",
    "ListCommandInvocationsResult",
    "ListCommandsResult",
    "ListComplianceItemsResult",
    "ListComplianceSummariesResult",
    "ListDocumentMetadataHistoryResult",
    "ListDocumentVersionsResult",
    "ListDocumentsResult",
    "ListInventoryEntriesResult",
    "ListNodesResult",
    "ListNodesSummaryResult",
    "ListOpsItemEventsResult",
    "ListOpsItemRelatedItemsResult",
    "ListOpsMetadataResult",
    "ListResourceComplianceSummariesResult",
    "ListResourceDataSyncResult",
    "ListTagsForResourceResult",
    "PutInventoryResult",
    "PutResourcePolicyResult",
    "RegisterDefaultPatchBaselineResult",
    "RegisterPatchBaselineForPatchGroupResult",
    "RegisterTargetWithMaintenanceWindowResult",
    "RegisterTaskWithMaintenanceWindowResult",
    "ResetServiceSettingResult",
    "ResumeSessionResult",
    "SendCommandResult",
    "StartAccessRequestResult",
    "StartAutomationExecutionResult",
    "StartChangeRequestExecutionResult",
    "StartExecutionPreviewResult",
    "StartSessionResult",
    "TerminateSessionResult",
    "UnlabelParameterVersionResult",
    "UpdateAssociationResult",
    "UpdateAssociationStatusResult",
    "UpdateDocumentDefaultVersionResult",
    "UpdateDocumentResult",
    "UpdateMaintenanceWindowResult",
    "UpdateMaintenanceWindowTargetResult",
    "UpdateMaintenanceWindowTaskResult",
    "UpdateOpsMetadataResult",
    "UpdatePatchBaselineResult",
    "add_tags_to_resource",
    "associate_ops_item_related_item",
    "cancel_command",
    "cancel_maintenance_window_execution",
    "create_activation",
    "create_association",
    "create_association_batch",
    "create_document",
    "create_maintenance_window",
    "create_ops_item",
    "create_ops_metadata",
    "create_patch_baseline",
    "create_resource_data_sync",
    "delete_activation",
    "delete_association",
    "delete_document",
    "delete_inventory",
    "delete_maintenance_window",
    "delete_ops_item",
    "delete_ops_metadata",
    "delete_parameter",
    "delete_parameters",
    "delete_patch_baseline",
    "delete_resource_data_sync",
    "delete_resource_policy",
    "deregister_managed_instance",
    "deregister_patch_baseline_for_patch_group",
    "deregister_target_from_maintenance_window",
    "deregister_task_from_maintenance_window",
    "describe_activations",
    "describe_association",
    "describe_association_execution_targets",
    "describe_association_executions",
    "describe_automation_executions",
    "describe_automation_step_executions",
    "describe_available_patches",
    "describe_document",
    "describe_document_permission",
    "describe_effective_instance_associations",
    "describe_effective_patches_for_patch_baseline",
    "describe_instance_associations_status",
    "describe_instance_information",
    "describe_instance_patch_states",
    "describe_instance_patch_states_for_patch_group",
    "describe_instance_patches",
    "describe_instance_properties",
    "describe_inventory_deletions",
    "describe_maintenance_window_execution_task_invocations",
    "describe_maintenance_window_execution_tasks",
    "describe_maintenance_window_executions",
    "describe_maintenance_window_schedule",
    "describe_maintenance_window_targets",
    "describe_maintenance_window_tasks",
    "describe_maintenance_windows",
    "describe_maintenance_windows_for_target",
    "describe_ops_items",
    "describe_parameters",
    "describe_patch_baselines",
    "describe_patch_group_state",
    "describe_patch_groups",
    "describe_patch_properties",
    "describe_sessions",
    "disassociate_ops_item_related_item",
    "get_access_token",
    "get_automation_execution",
    "get_calendar_state",
    "get_command_invocation",
    "get_connection_status",
    "get_default_patch_baseline",
    "get_deployable_patch_snapshot_for_instance",
    "get_document",
    "get_execution_preview",
    "get_inventory",
    "get_inventory_schema",
    "get_maintenance_window",
    "get_maintenance_window_execution",
    "get_maintenance_window_execution_task",
    "get_maintenance_window_execution_task_invocation",
    "get_maintenance_window_task",
    "get_ops_item",
    "get_ops_metadata",
    "get_ops_summary",
    "get_parameter",
    "get_parameter_history",
    "get_parameters",
    "get_parameters_batch",
    "get_parameters_by_path",
    "get_patch_baseline",
    "get_patch_baseline_for_patch_group",
    "get_resource_policies",
    "get_service_setting",
    "label_parameter_version",
    "list_association_versions",
    "list_associations",
    "list_command_invocations",
    "list_commands",
    "list_compliance_items",
    "list_compliance_summaries",
    "list_document_metadata_history",
    "list_document_versions",
    "list_documents",
    "list_inventory_entries",
    "list_nodes",
    "list_nodes_summary",
    "list_ops_item_events",
    "list_ops_item_related_items",
    "list_ops_metadata",
    "list_resource_compliance_summaries",
    "list_resource_data_sync",
    "list_tags_for_resource",
    "modify_document_permission",
    "put_compliance_items",
    "put_inventory",
    "put_parameter",
    "put_resource_policy",
    "register_default_patch_baseline",
    "register_patch_baseline_for_patch_group",
    "register_target_with_maintenance_window",
    "register_task_with_maintenance_window",
    "remove_tags_from_resource",
    "reset_service_setting",
    "resume_session",
    "send_automation_signal",
    "send_command",
    "start_access_request",
    "start_associations_once",
    "start_automation_execution",
    "start_change_request_execution",
    "start_execution_preview",
    "start_session",
    "stop_automation_execution",
    "terminate_session",
    "unlabel_parameter_version",
    "update_association",
    "update_association_status",
    "update_document",
    "update_document_default_version",
    "update_document_metadata",
    "update_maintenance_window",
    "update_maintenance_window_target",
    "update_maintenance_window_task",
    "update_managed_instance_role",
    "update_ops_item",
    "update_ops_metadata",
    "update_patch_baseline",
    "update_resource_data_sync",
    "update_service_setting",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def get_parameters_by_path(
    path: str,
    recursive: bool = True,
    with_decryption: bool = True,
    region_name: str | None = None,
) -> dict[str, str]:
    """Fetch all parameters whose path starts with *path* from SSM.

    Uses the ``GetParametersByPath`` API with automatic pagination.

    Args:
        path: SSM path prefix, e.g. ``"/myapp/prod/"``.
        recursive: If ``True`` (default), include parameters in sub-paths.
        with_decryption: Decrypt ``SecureString`` parameters (default ``True``).
        region_name: AWS region override.

    Returns:
        A dict mapping the full parameter name -> value for every parameter
        under *path*.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        client = async_client("ssm", region_name)
        raw_items = await client.paginate(
            "GetParametersByPath",
            result_key="Parameters",
            Path=path,
            Recursive=recursive,
            WithDecryption=with_decryption,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_parameters_by_path failed for path {path!r}") from exc
    return {p["Name"]: p["Value"] for p in raw_items}


async def get_parameters_batch(
    names: list[str],
    with_decryption: bool = True,
    region_name: str | None = None,
) -> dict[str, str]:
    """Fetch up to 10 SSM parameters by name in a single API call.

    Args:
        names: List of parameter names (up to 10).
        with_decryption: Decrypt ``SecureString`` parameters (default ``True``).
        region_name: AWS region override.

    Returns:
        A dict mapping parameter name -> value.  Parameters that do not exist
        are silently omitted.

    Raises:
        ValueError: If more than 10 names are supplied.
        RuntimeError: If the API call fails.
    """
    if len(names) > 10:
        raise ValueError("get_parameters_batch supports at most 10 names per call")
    try:
        client = async_client("ssm", region_name)
        resp = await client.call(
            "GetParameters",
            Names=names,
            WithDecryption=with_decryption,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "get_parameters_batch failed") from exc
    return {p["Name"]: p["Value"] for p in resp.get("Parameters", [])}


async def put_parameter(
    name: str,
    value: str,
    param_type: str = "String",
    overwrite: bool = True,
    description: str = "",
    region_name: str | None = None,
) -> None:
    """Create or update an SSM Parameter Store parameter.

    Args:
        name: Full parameter name, e.g. ``"/myapp/db/host"``.
        value: Parameter value.
        param_type: ``"String"`` (default), ``"StringList"``, or
            ``"SecureString"``.
        overwrite: If ``True`` (default), overwrite an existing parameter.
        description: Human-readable description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the put operation fails.
    """
    kwargs: dict[str, Any] = {
        "Name": name,
        "Value": value,
        "Type": param_type,
        "Overwrite": overwrite,
    }
    if description:
        kwargs["Description"] = description
    try:
        client = async_client("ssm", region_name)
        await client.call("PutParameter", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to put SSM parameter {name!r}") from exc


async def delete_parameter(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete a single SSM parameter.

    Args:
        name: Full parameter name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails.
    """
    try:
        client = async_client("ssm", region_name)
        await client.call("DeleteParameter", Name=name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to delete SSM parameter {name!r}") from exc


async def get_parameter(
    name: str,
    with_decryption: bool = True,
    region_name: str | None = None,
) -> str:
    """Fetch a single parameter from AWS SSM Parameter Store.

    Decryption is enabled by default so that ``SecureString`` parameters are
    returned in plaintext.  Caching is intentionally omitted here; use
    :func:`aws_util.placeholder.retrieve` (which wraps this with
    ``lru_cache``) when you need cache-aware resolution.

    Args:
        name: Full SSM parameter path, e.g. ``"/myapp/db/username"``.
        with_decryption: Decrypt ``SecureString`` parameters.  Ignored for
            ``String`` and ``StringList`` types.
        region_name: AWS region override.  Defaults to the boto3-resolved
            region.

    Returns:
        The parameter value as a string.

    Raises:
        RuntimeError: If the SSM API call fails (parameter not found,
            permission denied, etc.).
    """
    try:
        client = async_client("ssm", region_name)
        resp = await client.call("GetParameter", Name=name, WithDecryption=with_decryption)
        return resp["Parameter"]["Value"]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Error resolving SSM parameter {name!r}") from exc


async def describe_parameters(
    filters: list[dict[str, object]] | None = None,
    max_results: int = 50,
    region_name: str | None = None,
) -> list[dict[str, object]]:
    """List SSM parameters with optional filters.

    Uses ``DescribeParameters`` with automatic pagination.

    Args:
        filters: Optional list of SSM ``ParameterFilters`` dicts.
        max_results: Page size per API call (1–50, default ``50``).
        region_name: AWS region override.

    Returns:
        A list of parameter metadata dicts as returned by SSM.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        client = async_client("ssm", region_name)
        kwargs: dict[str, Any] = {"MaxResults": max_results}
        if filters:
            kwargs["ParameterFilters"] = filters
        items = await client.paginate(
            "DescribeParameters",
            result_key="Parameters",
            **kwargs,
        )
        return items
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_parameters failed") from exc


async def delete_parameters(
    names: list[str],
    region_name: str | None = None,
) -> list[str]:
    """Delete up to 10 SSM parameters in a single API call.

    Args:
        names: List of parameter names to delete (up to 10).
        region_name: AWS region override.

    Returns:
        List of parameter names that were successfully deleted.

    Raises:
        ValueError: If more than 10 names are supplied.
        RuntimeError: If the API call fails.
    """
    if len(names) > 10:
        raise ValueError("delete_parameters supports at most 10 names per call")
    try:
        client = async_client("ssm", region_name)
        resp = await client.call("DeleteParameters", Names=names)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"delete_parameters failed for {names!r}") from exc
    return resp.get("DeletedParameters", [])


async def add_tags_to_resource(
    resource_type: str,
    resource_id: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags to resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    kwargs["Tags"] = tags
    try:
        await client.call("AddTagsToResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags to resource") from exc
    return None


async def associate_ops_item_related_item(
    ops_item_id: str,
    association_type: str,
    resource_type: str,
    resource_uri: str,
    region_name: str | None = None,
) -> AssociateOpsItemRelatedItemResult:
    """Associate ops item related item.

    Args:
        ops_item_id: Ops item id.
        association_type: Association type.
        resource_type: Resource type.
        resource_uri: Resource uri.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsItemId"] = ops_item_id
    kwargs["AssociationType"] = association_type
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceUri"] = resource_uri
    try:
        resp = await client.call("AssociateOpsItemRelatedItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate ops item related item") from exc
    return AssociateOpsItemRelatedItemResult(
        association_id=resp.get("AssociationId"),
    )


async def cancel_command(
    command_id: str,
    *,
    instance_ids: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Cancel command.

    Args:
        command_id: Command id.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CommandId"] = command_id
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    try:
        await client.call("CancelCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel command") from exc
    return None


async def cancel_maintenance_window_execution(
    window_execution_id: str,
    region_name: str | None = None,
) -> CancelMaintenanceWindowExecutionResult:
    """Cancel maintenance window execution.

    Args:
        window_execution_id: Window execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    try:
        resp = await client.call("CancelMaintenanceWindowExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel maintenance window execution") from exc
    return CancelMaintenanceWindowExecutionResult(
        window_execution_id=resp.get("WindowExecutionId"),
    )


async def create_activation(
    iam_role: str,
    *,
    description: str | None = None,
    default_instance_name: str | None = None,
    registration_limit: int | None = None,
    expiration_date: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    registration_metadata: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateActivationResult:
    """Create activation.

    Args:
        iam_role: Iam role.
        description: Description.
        default_instance_name: Default instance name.
        registration_limit: Registration limit.
        expiration_date: Expiration date.
        tags: Tags.
        registration_metadata: Registration metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IamRole"] = iam_role
    if description is not None:
        kwargs["Description"] = description
    if default_instance_name is not None:
        kwargs["DefaultInstanceName"] = default_instance_name
    if registration_limit is not None:
        kwargs["RegistrationLimit"] = registration_limit
    if expiration_date is not None:
        kwargs["ExpirationDate"] = expiration_date
    if tags is not None:
        kwargs["Tags"] = tags
    if registration_metadata is not None:
        kwargs["RegistrationMetadata"] = registration_metadata
    try:
        resp = await client.call("CreateActivation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create activation") from exc
    return CreateActivationResult(
        activation_id=resp.get("ActivationId"),
        activation_code=resp.get("ActivationCode"),
    )


async def create_association(
    name: str,
    *,
    document_version: str | None = None,
    instance_id: str | None = None,
    parameters: dict[str, Any] | None = None,
    targets: list[dict[str, Any]] | None = None,
    schedule_expression: str | None = None,
    output_location: dict[str, Any] | None = None,
    association_name: str | None = None,
    automation_target_parameter_name: str | None = None,
    max_errors: str | None = None,
    max_concurrency: str | None = None,
    compliance_severity: str | None = None,
    sync_compliance: str | None = None,
    apply_only_at_cron_interval: bool | None = None,
    calendar_names: list[str] | None = None,
    target_locations: list[dict[str, Any]] | None = None,
    schedule_offset: int | None = None,
    duration: int | None = None,
    target_maps: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAssociationResult:
    """Create association.

    Args:
        name: Name.
        document_version: Document version.
        instance_id: Instance id.
        parameters: Parameters.
        targets: Targets.
        schedule_expression: Schedule expression.
        output_location: Output location.
        association_name: Association name.
        automation_target_parameter_name: Automation target parameter name.
        max_errors: Max errors.
        max_concurrency: Max concurrency.
        compliance_severity: Compliance severity.
        sync_compliance: Sync compliance.
        apply_only_at_cron_interval: Apply only at cron interval.
        calendar_names: Calendar names.
        target_locations: Target locations.
        schedule_offset: Schedule offset.
        duration: Duration.
        target_maps: Target maps.
        tags: Tags.
        alarm_configuration: Alarm configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if targets is not None:
        kwargs["Targets"] = targets
    if schedule_expression is not None:
        kwargs["ScheduleExpression"] = schedule_expression
    if output_location is not None:
        kwargs["OutputLocation"] = output_location
    if association_name is not None:
        kwargs["AssociationName"] = association_name
    if automation_target_parameter_name is not None:
        kwargs["AutomationTargetParameterName"] = automation_target_parameter_name
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if compliance_severity is not None:
        kwargs["ComplianceSeverity"] = compliance_severity
    if sync_compliance is not None:
        kwargs["SyncCompliance"] = sync_compliance
    if apply_only_at_cron_interval is not None:
        kwargs["ApplyOnlyAtCronInterval"] = apply_only_at_cron_interval
    if calendar_names is not None:
        kwargs["CalendarNames"] = calendar_names
    if target_locations is not None:
        kwargs["TargetLocations"] = target_locations
    if schedule_offset is not None:
        kwargs["ScheduleOffset"] = schedule_offset
    if duration is not None:
        kwargs["Duration"] = duration
    if target_maps is not None:
        kwargs["TargetMaps"] = target_maps
    if tags is not None:
        kwargs["Tags"] = tags
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    try:
        resp = await client.call("CreateAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create association") from exc
    return CreateAssociationResult(
        association_description=resp.get("AssociationDescription"),
    )


async def create_association_batch(
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> CreateAssociationBatchResult:
    """Create association batch.

    Args:
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Entries"] = entries
    try:
        resp = await client.call("CreateAssociationBatch", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create association batch") from exc
    return CreateAssociationBatchResult(
        successful=resp.get("Successful"),
        failed=resp.get("Failed"),
    )


async def create_document(
    content: str,
    name: str,
    *,
    requires: list[dict[str, Any]] | None = None,
    attachments: list[dict[str, Any]] | None = None,
    display_name: str | None = None,
    version_name: str | None = None,
    document_type: str | None = None,
    document_format: str | None = None,
    target_type: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDocumentResult:
    """Create document.

    Args:
        content: Content.
        name: Name.
        requires: Requires.
        attachments: Attachments.
        display_name: Display name.
        version_name: Version name.
        document_type: Document type.
        document_format: Document format.
        target_type: Target type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Content"] = content
    kwargs["Name"] = name
    if requires is not None:
        kwargs["Requires"] = requires
    if attachments is not None:
        kwargs["Attachments"] = attachments
    if display_name is not None:
        kwargs["DisplayName"] = display_name
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if document_type is not None:
        kwargs["DocumentType"] = document_type
    if document_format is not None:
        kwargs["DocumentFormat"] = document_format
    if target_type is not None:
        kwargs["TargetType"] = target_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create document") from exc
    return CreateDocumentResult(
        document_description=resp.get("DocumentDescription"),
    )


async def create_maintenance_window(
    name: str,
    schedule: str,
    duration: int,
    cutoff: int,
    allow_unassociated_targets: bool,
    *,
    description: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    schedule_timezone: str | None = None,
    schedule_offset: int | None = None,
    client_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMaintenanceWindowResult:
    """Create maintenance window.

    Args:
        name: Name.
        schedule: Schedule.
        duration: Duration.
        cutoff: Cutoff.
        allow_unassociated_targets: Allow unassociated targets.
        description: Description.
        start_date: Start date.
        end_date: End date.
        schedule_timezone: Schedule timezone.
        schedule_offset: Schedule offset.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Schedule"] = schedule
    kwargs["Duration"] = duration
    kwargs["Cutoff"] = cutoff
    kwargs["AllowUnassociatedTargets"] = allow_unassociated_targets
    if description is not None:
        kwargs["Description"] = description
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    if schedule_timezone is not None:
        kwargs["ScheduleTimezone"] = schedule_timezone
    if schedule_offset is not None:
        kwargs["ScheduleOffset"] = schedule_offset
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create maintenance window") from exc
    return CreateMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
    )


async def create_ops_item(
    description: str,
    source: str,
    title: str,
    *,
    ops_item_type: str | None = None,
    operational_data: dict[str, Any] | None = None,
    notifications: list[dict[str, Any]] | None = None,
    priority: int | None = None,
    related_ops_items: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    category: str | None = None,
    severity: str | None = None,
    actual_start_time: str | None = None,
    actual_end_time: str | None = None,
    planned_start_time: str | None = None,
    planned_end_time: str | None = None,
    account_id: str | None = None,
    region_name: str | None = None,
) -> CreateOpsItemResult:
    """Create ops item.

    Args:
        description: Description.
        source: Source.
        title: Title.
        ops_item_type: Ops item type.
        operational_data: Operational data.
        notifications: Notifications.
        priority: Priority.
        related_ops_items: Related ops items.
        tags: Tags.
        category: Category.
        severity: Severity.
        actual_start_time: Actual start time.
        actual_end_time: Actual end time.
        planned_start_time: Planned start time.
        planned_end_time: Planned end time.
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Description"] = description
    kwargs["Source"] = source
    kwargs["Title"] = title
    if ops_item_type is not None:
        kwargs["OpsItemType"] = ops_item_type
    if operational_data is not None:
        kwargs["OperationalData"] = operational_data
    if notifications is not None:
        kwargs["Notifications"] = notifications
    if priority is not None:
        kwargs["Priority"] = priority
    if related_ops_items is not None:
        kwargs["RelatedOpsItems"] = related_ops_items
    if tags is not None:
        kwargs["Tags"] = tags
    if category is not None:
        kwargs["Category"] = category
    if severity is not None:
        kwargs["Severity"] = severity
    if actual_start_time is not None:
        kwargs["ActualStartTime"] = actual_start_time
    if actual_end_time is not None:
        kwargs["ActualEndTime"] = actual_end_time
    if planned_start_time is not None:
        kwargs["PlannedStartTime"] = planned_start_time
    if planned_end_time is not None:
        kwargs["PlannedEndTime"] = planned_end_time
    if account_id is not None:
        kwargs["AccountId"] = account_id
    try:
        resp = await client.call("CreateOpsItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ops item") from exc
    return CreateOpsItemResult(
        ops_item_id=resp.get("OpsItemId"),
        ops_item_arn=resp.get("OpsItemArn"),
    )


async def create_ops_metadata(
    resource_id: str,
    *,
    metadata: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateOpsMetadataResult:
    """Create ops metadata.

    Args:
        resource_id: Resource id.
        metadata: Metadata.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    if metadata is not None:
        kwargs["Metadata"] = metadata
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateOpsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ops metadata") from exc
    return CreateOpsMetadataResult(
        ops_metadata_arn=resp.get("OpsMetadataArn"),
    )


async def create_patch_baseline(
    name: str,
    *,
    operating_system: str | None = None,
    global_filters: dict[str, Any] | None = None,
    approval_rules: dict[str, Any] | None = None,
    approved_patches: list[str] | None = None,
    approved_patches_compliance_level: str | None = None,
    approved_patches_enable_non_security: bool | None = None,
    rejected_patches: list[str] | None = None,
    rejected_patches_action: str | None = None,
    description: str | None = None,
    sources: list[dict[str, Any]] | None = None,
    available_security_updates_compliance_status: str | None = None,
    client_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreatePatchBaselineResult:
    """Create patch baseline.

    Args:
        name: Name.
        operating_system: Operating system.
        global_filters: Global filters.
        approval_rules: Approval rules.
        approved_patches: Approved patches.
        approved_patches_compliance_level: Approved patches compliance level.
        approved_patches_enable_non_security: Approved patches enable non security.
        rejected_patches: Rejected patches.
        rejected_patches_action: Rejected patches action.
        description: Description.
        sources: Sources.
        available_security_updates_compliance_status: Available security updates compliance status.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if operating_system is not None:
        kwargs["OperatingSystem"] = operating_system
    if global_filters is not None:
        kwargs["GlobalFilters"] = global_filters
    if approval_rules is not None:
        kwargs["ApprovalRules"] = approval_rules
    if approved_patches is not None:
        kwargs["ApprovedPatches"] = approved_patches
    if approved_patches_compliance_level is not None:
        kwargs["ApprovedPatchesComplianceLevel"] = approved_patches_compliance_level
    if approved_patches_enable_non_security is not None:
        kwargs["ApprovedPatchesEnableNonSecurity"] = approved_patches_enable_non_security
    if rejected_patches is not None:
        kwargs["RejectedPatches"] = rejected_patches
    if rejected_patches_action is not None:
        kwargs["RejectedPatchesAction"] = rejected_patches_action
    if description is not None:
        kwargs["Description"] = description
    if sources is not None:
        kwargs["Sources"] = sources
    if available_security_updates_compliance_status is not None:
        kwargs["AvailableSecurityUpdatesComplianceStatus"] = (
            available_security_updates_compliance_status
        )
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreatePatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create patch baseline") from exc
    return CreatePatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
    )


async def create_resource_data_sync(
    sync_name: str,
    *,
    s3_destination: dict[str, Any] | None = None,
    sync_type: str | None = None,
    sync_source: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create resource data sync.

    Args:
        sync_name: Sync name.
        s3_destination: S3 destination.
        sync_type: Sync type.
        sync_source: Sync source.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncName"] = sync_name
    if s3_destination is not None:
        kwargs["S3Destination"] = s3_destination
    if sync_type is not None:
        kwargs["SyncType"] = sync_type
    if sync_source is not None:
        kwargs["SyncSource"] = sync_source
    try:
        await client.call("CreateResourceDataSync", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create resource data sync") from exc
    return None


async def delete_activation(
    activation_id: str,
    region_name: str | None = None,
) -> None:
    """Delete activation.

    Args:
        activation_id: Activation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActivationId"] = activation_id
    try:
        await client.call("DeleteActivation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete activation") from exc
    return None


async def delete_association(
    *,
    name: str | None = None,
    instance_id: str | None = None,
    association_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete association.

    Args:
        name: Name.
        instance_id: Instance id.
        association_id: Association id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if association_id is not None:
        kwargs["AssociationId"] = association_id
    try:
        await client.call("DeleteAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete association") from exc
    return None


async def delete_document(
    name: str,
    *,
    document_version: str | None = None,
    version_name: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete document.

    Args:
        name: Name.
        document_version: Document version.
        version_name: Version name.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if force is not None:
        kwargs["Force"] = force
    try:
        await client.call("DeleteDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete document") from exc
    return None


async def delete_inventory(
    type_name: str,
    *,
    schema_delete_option: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> DeleteInventoryResult:
    """Delete inventory.

    Args:
        type_name: Type name.
        schema_delete_option: Schema delete option.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TypeName"] = type_name
    if schema_delete_option is not None:
        kwargs["SchemaDeleteOption"] = schema_delete_option
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("DeleteInventory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete inventory") from exc
    return DeleteInventoryResult(
        deletion_id=resp.get("DeletionId"),
        type_name=resp.get("TypeName"),
        deletion_summary=resp.get("DeletionSummary"),
    )


async def delete_maintenance_window(
    window_id: str,
    region_name: str | None = None,
) -> DeleteMaintenanceWindowResult:
    """Delete maintenance window.

    Args:
        window_id: Window id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    try:
        resp = await client.call("DeleteMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete maintenance window") from exc
    return DeleteMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
    )


async def delete_ops_item(
    ops_item_id: str,
    region_name: str | None = None,
) -> None:
    """Delete ops item.

    Args:
        ops_item_id: Ops item id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsItemId"] = ops_item_id
    try:
        await client.call("DeleteOpsItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ops item") from exc
    return None


async def delete_ops_metadata(
    ops_metadata_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete ops metadata.

    Args:
        ops_metadata_arn: Ops metadata arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsMetadataArn"] = ops_metadata_arn
    try:
        await client.call("DeleteOpsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ops metadata") from exc
    return None


async def delete_patch_baseline(
    baseline_id: str,
    region_name: str | None = None,
) -> DeletePatchBaselineResult:
    """Delete patch baseline.

    Args:
        baseline_id: Baseline id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    try:
        resp = await client.call("DeletePatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete patch baseline") from exc
    return DeletePatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
    )


async def delete_resource_data_sync(
    sync_name: str,
    *,
    sync_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete resource data sync.

    Args:
        sync_name: Sync name.
        sync_type: Sync type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncName"] = sync_name
    if sync_type is not None:
        kwargs["SyncType"] = sync_type
    try:
        await client.call("DeleteResourceDataSync", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource data sync") from exc
    return None


async def delete_resource_policy(
    resource_arn: str,
    policy_id: str,
    policy_hash: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        policy_id: Policy id.
        policy_hash: Policy hash.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["PolicyId"] = policy_id
    kwargs["PolicyHash"] = policy_hash
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def deregister_managed_instance(
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Deregister managed instance.

    Args:
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    try:
        await client.call("DeregisterManagedInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister managed instance") from exc
    return None


async def deregister_patch_baseline_for_patch_group(
    baseline_id: str,
    patch_group: str,
    region_name: str | None = None,
) -> DeregisterPatchBaselineForPatchGroupResult:
    """Deregister patch baseline for patch group.

    Args:
        baseline_id: Baseline id.
        patch_group: Patch group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    kwargs["PatchGroup"] = patch_group
    try:
        resp = await client.call("DeregisterPatchBaselineForPatchGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister patch baseline for patch group") from exc
    return DeregisterPatchBaselineForPatchGroupResult(
        baseline_id=resp.get("BaselineId"),
        patch_group=resp.get("PatchGroup"),
    )


async def deregister_target_from_maintenance_window(
    window_id: str,
    window_target_id: str,
    *,
    safe: bool | None = None,
    region_name: str | None = None,
) -> DeregisterTargetFromMaintenanceWindowResult:
    """Deregister target from maintenance window.

    Args:
        window_id: Window id.
        window_target_id: Window target id.
        safe: Safe.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["WindowTargetId"] = window_target_id
    if safe is not None:
        kwargs["Safe"] = safe
    try:
        resp = await client.call("DeregisterTargetFromMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister target from maintenance window") from exc
    return DeregisterTargetFromMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
        window_target_id=resp.get("WindowTargetId"),
    )


async def deregister_task_from_maintenance_window(
    window_id: str,
    window_task_id: str,
    region_name: str | None = None,
) -> DeregisterTaskFromMaintenanceWindowResult:
    """Deregister task from maintenance window.

    Args:
        window_id: Window id.
        window_task_id: Window task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["WindowTaskId"] = window_task_id
    try:
        resp = await client.call("DeregisterTaskFromMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister task from maintenance window") from exc
    return DeregisterTaskFromMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
        window_task_id=resp.get("WindowTaskId"),
    )


async def describe_activations(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeActivationsResult:
    """Describe activations.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeActivations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe activations") from exc
    return DescribeActivationsResult(
        activation_list=resp.get("ActivationList"),
        next_token=resp.get("NextToken"),
    )


async def describe_association(
    *,
    name: str | None = None,
    instance_id: str | None = None,
    association_id: str | None = None,
    association_version: str | None = None,
    region_name: str | None = None,
) -> DescribeAssociationResult:
    """Describe association.

    Args:
        name: Name.
        instance_id: Instance id.
        association_id: Association id.
        association_version: Association version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if association_id is not None:
        kwargs["AssociationId"] = association_id
    if association_version is not None:
        kwargs["AssociationVersion"] = association_version
    try:
        resp = await client.call("DescribeAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe association") from exc
    return DescribeAssociationResult(
        association_description=resp.get("AssociationDescription"),
    )


async def describe_association_execution_targets(
    association_id: str,
    execution_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAssociationExecutionTargetsResult:
    """Describe association execution targets.

    Args:
        association_id: Association id.
        execution_id: Execution id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    kwargs["ExecutionId"] = execution_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeAssociationExecutionTargets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe association execution targets") from exc
    return DescribeAssociationExecutionTargetsResult(
        association_execution_targets=resp.get("AssociationExecutionTargets"),
        next_token=resp.get("NextToken"),
    )


async def describe_association_executions(
    association_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAssociationExecutionsResult:
    """Describe association executions.

    Args:
        association_id: Association id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeAssociationExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe association executions") from exc
    return DescribeAssociationExecutionsResult(
        association_executions=resp.get("AssociationExecutions"),
        next_token=resp.get("NextToken"),
    )


async def describe_automation_executions(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAutomationExecutionsResult:
    """Describe automation executions.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeAutomationExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe automation executions") from exc
    return DescribeAutomationExecutionsResult(
        automation_execution_metadata_list=resp.get("AutomationExecutionMetadataList"),
        next_token=resp.get("NextToken"),
    )


async def describe_automation_step_executions(
    automation_execution_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    reverse_order: bool | None = None,
    region_name: str | None = None,
) -> DescribeAutomationStepExecutionsResult:
    """Describe automation step executions.

    Args:
        automation_execution_id: Automation execution id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        reverse_order: Reverse order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationExecutionId"] = automation_execution_id
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if reverse_order is not None:
        kwargs["ReverseOrder"] = reverse_order
    try:
        resp = await client.call("DescribeAutomationStepExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe automation step executions") from exc
    return DescribeAutomationStepExecutionsResult(
        step_executions=resp.get("StepExecutions"),
        next_token=resp.get("NextToken"),
    )


async def describe_available_patches(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAvailablePatchesResult:
    """Describe available patches.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeAvailablePatches", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe available patches") from exc
    return DescribeAvailablePatchesResult(
        patches=resp.get("Patches"),
        next_token=resp.get("NextToken"),
    )


async def describe_document(
    name: str,
    *,
    document_version: str | None = None,
    version_name: str | None = None,
    region_name: str | None = None,
) -> DescribeDocumentResult:
    """Describe document.

    Args:
        name: Name.
        document_version: Document version.
        version_name: Version name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if version_name is not None:
        kwargs["VersionName"] = version_name
    try:
        resp = await client.call("DescribeDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe document") from exc
    return DescribeDocumentResult(
        document=resp.get("Document"),
    )


async def describe_document_permission(
    name: str,
    permission_type: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeDocumentPermissionResult:
    """Describe document permission.

    Args:
        name: Name.
        permission_type: Permission type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["PermissionType"] = permission_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeDocumentPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe document permission") from exc
    return DescribeDocumentPermissionResult(
        account_ids=resp.get("AccountIds"),
        account_sharing_info_list=resp.get("AccountSharingInfoList"),
        next_token=resp.get("NextToken"),
    )


async def describe_effective_instance_associations(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeEffectiveInstanceAssociationsResult:
    """Describe effective instance associations.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeEffectiveInstanceAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe effective instance associations") from exc
    return DescribeEffectiveInstanceAssociationsResult(
        associations=resp.get("Associations"),
        next_token=resp.get("NextToken"),
    )


async def describe_effective_patches_for_patch_baseline(
    baseline_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeEffectivePatchesForPatchBaselineResult:
    """Describe effective patches for patch baseline.

    Args:
        baseline_id: Baseline id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeEffectivePatchesForPatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to describe effective patches for patch baseline"
        ) from exc
    return DescribeEffectivePatchesForPatchBaselineResult(
        effective_patches=resp.get("EffectivePatches"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_associations_status(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeInstanceAssociationsStatusResult:
    """Describe instance associations status.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeInstanceAssociationsStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance associations status") from exc
    return DescribeInstanceAssociationsStatusResult(
        instance_association_status_infos=resp.get("InstanceAssociationStatusInfos"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_information(
    *,
    instance_information_filter_list: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeInstanceInformationResult:
    """Describe instance information.

    Args:
        instance_information_filter_list: Instance information filter list.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if instance_information_filter_list is not None:
        kwargs["InstanceInformationFilterList"] = instance_information_filter_list
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeInstanceInformation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance information") from exc
    return DescribeInstanceInformationResult(
        instance_information_list=resp.get("InstanceInformationList"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_patch_states(
    instance_ids: list[str],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeInstancePatchStatesResult:
    """Describe instance patch states.

    Args:
        instance_ids: Instance ids.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceIds"] = instance_ids
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeInstancePatchStates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance patch states") from exc
    return DescribeInstancePatchStatesResult(
        instance_patch_states=resp.get("InstancePatchStates"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_patch_states_for_patch_group(
    patch_group: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeInstancePatchStatesForPatchGroupResult:
    """Describe instance patch states for patch group.

    Args:
        patch_group: Patch group.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PatchGroup"] = patch_group
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeInstancePatchStatesForPatchGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to describe instance patch states for patch group"
        ) from exc
    return DescribeInstancePatchStatesForPatchGroupResult(
        instance_patch_states=resp.get("InstancePatchStates"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_patches(
    instance_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeInstancePatchesResult:
    """Describe instance patches.

    Args:
        instance_id: Instance id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeInstancePatches", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance patches") from exc
    return DescribeInstancePatchesResult(
        patches=resp.get("Patches"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_properties(
    *,
    instance_property_filter_list: list[dict[str, Any]] | None = None,
    filters_with_operator: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeInstancePropertiesResult:
    """Describe instance properties.

    Args:
        instance_property_filter_list: Instance property filter list.
        filters_with_operator: Filters with operator.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if instance_property_filter_list is not None:
        kwargs["InstancePropertyFilterList"] = instance_property_filter_list
    if filters_with_operator is not None:
        kwargs["FiltersWithOperator"] = filters_with_operator
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeInstanceProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance properties") from exc
    return DescribeInstancePropertiesResult(
        instance_properties=resp.get("InstanceProperties"),
        next_token=resp.get("NextToken"),
    )


async def describe_inventory_deletions(
    *,
    deletion_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeInventoryDeletionsResult:
    """Describe inventory deletions.

    Args:
        deletion_id: Deletion id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if deletion_id is not None:
        kwargs["DeletionId"] = deletion_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeInventoryDeletions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe inventory deletions") from exc
    return DescribeInventoryDeletionsResult(
        inventory_deletions=resp.get("InventoryDeletions"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_execution_task_invocations(
    window_execution_id: str,
    task_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowExecutionTaskInvocationsResult:
    """Describe maintenance window execution task invocations.

    Args:
        window_execution_id: Window execution id.
        task_id: Task id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    kwargs["TaskId"] = task_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowExecutionTaskInvocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to describe maintenance window execution task invocations"
        ) from exc
    return DescribeMaintenanceWindowExecutionTaskInvocationsResult(
        window_execution_task_invocation_identities=resp.get(
            "WindowExecutionTaskInvocationIdentities"
        ),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_execution_tasks(
    window_execution_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowExecutionTasksResult:
    """Describe maintenance window execution tasks.

    Args:
        window_execution_id: Window execution id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowExecutionTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance window execution tasks") from exc
    return DescribeMaintenanceWindowExecutionTasksResult(
        window_execution_task_identities=resp.get("WindowExecutionTaskIdentities"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_executions(
    window_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowExecutionsResult:
    """Describe maintenance window executions.

    Args:
        window_id: Window id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance window executions") from exc
    return DescribeMaintenanceWindowExecutionsResult(
        window_executions=resp.get("WindowExecutions"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_schedule(
    *,
    window_id: str | None = None,
    targets: list[dict[str, Any]] | None = None,
    resource_type: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowScheduleResult:
    """Describe maintenance window schedule.

    Args:
        window_id: Window id.
        targets: Targets.
        resource_type: Resource type.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if window_id is not None:
        kwargs["WindowId"] = window_id
    if targets is not None:
        kwargs["Targets"] = targets
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance window schedule") from exc
    return DescribeMaintenanceWindowScheduleResult(
        scheduled_window_executions=resp.get("ScheduledWindowExecutions"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_targets(
    window_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowTargetsResult:
    """Describe maintenance window targets.

    Args:
        window_id: Window id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowTargets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance window targets") from exc
    return DescribeMaintenanceWindowTargetsResult(
        targets=resp.get("Targets"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_window_tasks(
    window_id: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowTasksResult:
    """Describe maintenance window tasks.

    Args:
        window_id: Window id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance window tasks") from exc
    return DescribeMaintenanceWindowTasksResult(
        tasks=resp.get("Tasks"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_windows(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowsResult:
    """Describe maintenance windows.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindows", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance windows") from exc
    return DescribeMaintenanceWindowsResult(
        window_identities=resp.get("WindowIdentities"),
        next_token=resp.get("NextToken"),
    )


async def describe_maintenance_windows_for_target(
    targets: list[dict[str, Any]],
    resource_type: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMaintenanceWindowsForTargetResult:
    """Describe maintenance windows for target.

    Args:
        targets: Targets.
        resource_type: Resource type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Targets"] = targets
    kwargs["ResourceType"] = resource_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeMaintenanceWindowsForTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance windows for target") from exc
    return DescribeMaintenanceWindowsForTargetResult(
        window_identities=resp.get("WindowIdentities"),
        next_token=resp.get("NextToken"),
    )


async def describe_ops_items(
    *,
    ops_item_filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeOpsItemsResult:
    """Describe ops items.

    Args:
        ops_item_filters: Ops item filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if ops_item_filters is not None:
        kwargs["OpsItemFilters"] = ops_item_filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeOpsItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe ops items") from exc
    return DescribeOpsItemsResult(
        next_token=resp.get("NextToken"),
        ops_item_summaries=resp.get("OpsItemSummaries"),
    )


async def describe_patch_baselines(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribePatchBaselinesResult:
    """Describe patch baselines.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribePatchBaselines", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe patch baselines") from exc
    return DescribePatchBaselinesResult(
        baseline_identities=resp.get("BaselineIdentities"),
        next_token=resp.get("NextToken"),
    )


async def describe_patch_group_state(
    patch_group: str,
    region_name: str | None = None,
) -> DescribePatchGroupStateResult:
    """Describe patch group state.

    Args:
        patch_group: Patch group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PatchGroup"] = patch_group
    try:
        resp = await client.call("DescribePatchGroupState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe patch group state") from exc
    return DescribePatchGroupStateResult(
        instances=resp.get("Instances"),
        instances_with_installed_patches=resp.get("InstancesWithInstalledPatches"),
        instances_with_installed_other_patches=resp.get("InstancesWithInstalledOtherPatches"),
        instances_with_installed_pending_reboot_patches=resp.get(
            "InstancesWithInstalledPendingRebootPatches"
        ),
        instances_with_installed_rejected_patches=resp.get("InstancesWithInstalledRejectedPatches"),
        instances_with_missing_patches=resp.get("InstancesWithMissingPatches"),
        instances_with_failed_patches=resp.get("InstancesWithFailedPatches"),
        instances_with_not_applicable_patches=resp.get("InstancesWithNotApplicablePatches"),
        instances_with_unreported_not_applicable_patches=resp.get(
            "InstancesWithUnreportedNotApplicablePatches"
        ),
        instances_with_critical_non_compliant_patches=resp.get(
            "InstancesWithCriticalNonCompliantPatches"
        ),
        instances_with_security_non_compliant_patches=resp.get(
            "InstancesWithSecurityNonCompliantPatches"
        ),
        instances_with_other_non_compliant_patches=resp.get(
            "InstancesWithOtherNonCompliantPatches"
        ),
        instances_with_available_security_updates=resp.get("InstancesWithAvailableSecurityUpdates"),
    )


async def describe_patch_groups(
    *,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribePatchGroupsResult:
    """Describe patch groups.

    Args:
        max_results: Max results.
        filters: Filters.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribePatchGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe patch groups") from exc
    return DescribePatchGroupsResult(
        mappings=resp.get("Mappings"),
        next_token=resp.get("NextToken"),
    )


async def describe_patch_properties(
    operating_system: str,
    property: str,
    *,
    patch_set: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribePatchPropertiesResult:
    """Describe patch properties.

    Args:
        operating_system: Operating system.
        property: Property.
        patch_set: Patch set.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OperatingSystem"] = operating_system
    kwargs["Property"] = property
    if patch_set is not None:
        kwargs["PatchSet"] = patch_set
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribePatchProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe patch properties") from exc
    return DescribePatchPropertiesResult(
        properties=resp.get("Properties"),
        next_token=resp.get("NextToken"),
    )


async def describe_sessions(
    state: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeSessionsResult:
    """Describe sessions.

    Args:
        state: State.
        max_results: Max results.
        next_token: Next token.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["State"] = state
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe sessions") from exc
    return DescribeSessionsResult(
        sessions=resp.get("Sessions"),
        next_token=resp.get("NextToken"),
    )


async def disassociate_ops_item_related_item(
    ops_item_id: str,
    association_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate ops item related item.

    Args:
        ops_item_id: Ops item id.
        association_id: Association id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsItemId"] = ops_item_id
    kwargs["AssociationId"] = association_id
    try:
        await client.call("DisassociateOpsItemRelatedItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate ops item related item") from exc
    return None


async def get_access_token(
    access_request_id: str,
    region_name: str | None = None,
) -> GetAccessTokenResult:
    """Get access token.

    Args:
        access_request_id: Access request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessRequestId"] = access_request_id
    try:
        resp = await client.call("GetAccessToken", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get access token") from exc
    return GetAccessTokenResult(
        credentials=resp.get("Credentials"),
        access_request_status=resp.get("AccessRequestStatus"),
    )


async def get_automation_execution(
    automation_execution_id: str,
    region_name: str | None = None,
) -> GetAutomationExecutionResult:
    """Get automation execution.

    Args:
        automation_execution_id: Automation execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationExecutionId"] = automation_execution_id
    try:
        resp = await client.call("GetAutomationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get automation execution") from exc
    return GetAutomationExecutionResult(
        automation_execution=resp.get("AutomationExecution"),
    )


async def get_calendar_state(
    calendar_names: list[str],
    *,
    at_time: str | None = None,
    region_name: str | None = None,
) -> GetCalendarStateResult:
    """Get calendar state.

    Args:
        calendar_names: Calendar names.
        at_time: At time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CalendarNames"] = calendar_names
    if at_time is not None:
        kwargs["AtTime"] = at_time
    try:
        resp = await client.call("GetCalendarState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get calendar state") from exc
    return GetCalendarStateResult(
        state=resp.get("State"),
        at_time=resp.get("AtTime"),
        next_transition_time=resp.get("NextTransitionTime"),
    )


async def get_command_invocation(
    command_id: str,
    instance_id: str,
    *,
    plugin_name: str | None = None,
    region_name: str | None = None,
) -> GetCommandInvocationResult:
    """Get command invocation.

    Args:
        command_id: Command id.
        instance_id: Instance id.
        plugin_name: Plugin name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CommandId"] = command_id
    kwargs["InstanceId"] = instance_id
    if plugin_name is not None:
        kwargs["PluginName"] = plugin_name
    try:
        resp = await client.call("GetCommandInvocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get command invocation") from exc
    return GetCommandInvocationResult(
        command_id=resp.get("CommandId"),
        instance_id=resp.get("InstanceId"),
        comment=resp.get("Comment"),
        document_name=resp.get("DocumentName"),
        document_version=resp.get("DocumentVersion"),
        plugin_name=resp.get("PluginName"),
        response_code=resp.get("ResponseCode"),
        execution_start_date_time=resp.get("ExecutionStartDateTime"),
        execution_elapsed_time=resp.get("ExecutionElapsedTime"),
        execution_end_date_time=resp.get("ExecutionEndDateTime"),
        status=resp.get("Status"),
        status_details=resp.get("StatusDetails"),
        standard_output_content=resp.get("StandardOutputContent"),
        standard_output_url=resp.get("StandardOutputUrl"),
        standard_error_content=resp.get("StandardErrorContent"),
        standard_error_url=resp.get("StandardErrorUrl"),
        cloud_watch_output_config=resp.get("CloudWatchOutputConfig"),
    )


async def get_connection_status(
    target: str,
    region_name: str | None = None,
) -> GetConnectionStatusResult:
    """Get connection status.

    Args:
        target: Target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Target"] = target
    try:
        resp = await client.call("GetConnectionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connection status") from exc
    return GetConnectionStatusResult(
        target=resp.get("Target"),
        status=resp.get("Status"),
    )


async def get_default_patch_baseline(
    *,
    operating_system: str | None = None,
    region_name: str | None = None,
) -> GetDefaultPatchBaselineResult:
    """Get default patch baseline.

    Args:
        operating_system: Operating system.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if operating_system is not None:
        kwargs["OperatingSystem"] = operating_system
    try:
        resp = await client.call("GetDefaultPatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get default patch baseline") from exc
    return GetDefaultPatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
        operating_system=resp.get("OperatingSystem"),
    )


async def get_deployable_patch_snapshot_for_instance(
    instance_id: str,
    snapshot_id: str,
    *,
    baseline_override: dict[str, Any] | None = None,
    use_s3_dual_stack_endpoint: bool | None = None,
    region_name: str | None = None,
) -> GetDeployablePatchSnapshotForInstanceResult:
    """Get deployable patch snapshot for instance.

    Args:
        instance_id: Instance id.
        snapshot_id: Snapshot id.
        baseline_override: Baseline override.
        use_s3_dual_stack_endpoint: Use s3 dual stack endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["SnapshotId"] = snapshot_id
    if baseline_override is not None:
        kwargs["BaselineOverride"] = baseline_override
    if use_s3_dual_stack_endpoint is not None:
        kwargs["UseS3DualStackEndpoint"] = use_s3_dual_stack_endpoint
    try:
        resp = await client.call("GetDeployablePatchSnapshotForInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get deployable patch snapshot for instance") from exc
    return GetDeployablePatchSnapshotForInstanceResult(
        instance_id=resp.get("InstanceId"),
        snapshot_id=resp.get("SnapshotId"),
        snapshot_download_url=resp.get("SnapshotDownloadUrl"),
        product=resp.get("Product"),
    )


async def get_document(
    name: str,
    *,
    version_name: str | None = None,
    document_version: str | None = None,
    document_format: str | None = None,
    region_name: str | None = None,
) -> GetDocumentResult:
    """Get document.

    Args:
        name: Name.
        version_name: Version name.
        document_version: Document version.
        document_format: Document format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if document_format is not None:
        kwargs["DocumentFormat"] = document_format
    try:
        resp = await client.call("GetDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get document") from exc
    return GetDocumentResult(
        name=resp.get("Name"),
        created_date=resp.get("CreatedDate"),
        display_name=resp.get("DisplayName"),
        version_name=resp.get("VersionName"),
        document_version=resp.get("DocumentVersion"),
        status=resp.get("Status"),
        status_information=resp.get("StatusInformation"),
        content=resp.get("Content"),
        document_type=resp.get("DocumentType"),
        document_format=resp.get("DocumentFormat"),
        requires=resp.get("Requires"),
        attachments_content=resp.get("AttachmentsContent"),
        review_status=resp.get("ReviewStatus"),
    )


async def get_execution_preview(
    execution_preview_id: str,
    region_name: str | None = None,
) -> GetExecutionPreviewResult:
    """Get execution preview.

    Args:
        execution_preview_id: Execution preview id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExecutionPreviewId"] = execution_preview_id
    try:
        resp = await client.call("GetExecutionPreview", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get execution preview") from exc
    return GetExecutionPreviewResult(
        execution_preview_id=resp.get("ExecutionPreviewId"),
        ended_at=resp.get("EndedAt"),
        status=resp.get("Status"),
        status_message=resp.get("StatusMessage"),
        execution_preview=resp.get("ExecutionPreview"),
    )


async def get_inventory(
    *,
    filters: list[dict[str, Any]] | None = None,
    aggregators: list[dict[str, Any]] | None = None,
    result_attributes: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetInventoryResult:
    """Get inventory.

    Args:
        filters: Filters.
        aggregators: Aggregators.
        result_attributes: Result attributes.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if aggregators is not None:
        kwargs["Aggregators"] = aggregators
    if result_attributes is not None:
        kwargs["ResultAttributes"] = result_attributes
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetInventory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get inventory") from exc
    return GetInventoryResult(
        entities=resp.get("Entities"),
        next_token=resp.get("NextToken"),
    )


async def get_inventory_schema(
    *,
    type_name: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    aggregator: bool | None = None,
    sub_type: bool | None = None,
    region_name: str | None = None,
) -> GetInventorySchemaResult:
    """Get inventory schema.

    Args:
        type_name: Type name.
        next_token: Next token.
        max_results: Max results.
        aggregator: Aggregator.
        sub_type: Sub type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if type_name is not None:
        kwargs["TypeName"] = type_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if aggregator is not None:
        kwargs["Aggregator"] = aggregator
    if sub_type is not None:
        kwargs["SubType"] = sub_type
    try:
        resp = await client.call("GetInventorySchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get inventory schema") from exc
    return GetInventorySchemaResult(
        schemas=resp.get("Schemas"),
        next_token=resp.get("NextToken"),
    )


async def get_maintenance_window(
    window_id: str,
    region_name: str | None = None,
) -> GetMaintenanceWindowResult:
    """Get maintenance window.

    Args:
        window_id: Window id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    try:
        resp = await client.call("GetMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get maintenance window") from exc
    return GetMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        start_date=resp.get("StartDate"),
        end_date=resp.get("EndDate"),
        schedule=resp.get("Schedule"),
        schedule_timezone=resp.get("ScheduleTimezone"),
        schedule_offset=resp.get("ScheduleOffset"),
        next_execution_time=resp.get("NextExecutionTime"),
        duration=resp.get("Duration"),
        cutoff=resp.get("Cutoff"),
        allow_unassociated_targets=resp.get("AllowUnassociatedTargets"),
        enabled=resp.get("Enabled"),
        created_date=resp.get("CreatedDate"),
        modified_date=resp.get("ModifiedDate"),
    )


async def get_maintenance_window_execution(
    window_execution_id: str,
    region_name: str | None = None,
) -> GetMaintenanceWindowExecutionResult:
    """Get maintenance window execution.

    Args:
        window_execution_id: Window execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    try:
        resp = await client.call("GetMaintenanceWindowExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get maintenance window execution") from exc
    return GetMaintenanceWindowExecutionResult(
        window_execution_id=resp.get("WindowExecutionId"),
        task_ids=resp.get("TaskIds"),
        status=resp.get("Status"),
        status_details=resp.get("StatusDetails"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
    )


async def get_maintenance_window_execution_task(
    window_execution_id: str,
    task_id: str,
    region_name: str | None = None,
) -> GetMaintenanceWindowExecutionTaskResult:
    """Get maintenance window execution task.

    Args:
        window_execution_id: Window execution id.
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    kwargs["TaskId"] = task_id
    try:
        resp = await client.call("GetMaintenanceWindowExecutionTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get maintenance window execution task") from exc
    return GetMaintenanceWindowExecutionTaskResult(
        window_execution_id=resp.get("WindowExecutionId"),
        task_execution_id=resp.get("TaskExecutionId"),
        task_arn=resp.get("TaskArn"),
        service_role=resp.get("ServiceRole"),
        type_value=resp.get("Type"),
        task_parameters=resp.get("TaskParameters"),
        priority=resp.get("Priority"),
        max_concurrency=resp.get("MaxConcurrency"),
        max_errors=resp.get("MaxErrors"),
        status=resp.get("Status"),
        status_details=resp.get("StatusDetails"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
        alarm_configuration=resp.get("AlarmConfiguration"),
        triggered_alarms=resp.get("TriggeredAlarms"),
    )


async def get_maintenance_window_execution_task_invocation(
    window_execution_id: str,
    task_id: str,
    invocation_id: str,
    region_name: str | None = None,
) -> GetMaintenanceWindowExecutionTaskInvocationResult:
    """Get maintenance window execution task invocation.

    Args:
        window_execution_id: Window execution id.
        task_id: Task id.
        invocation_id: Invocation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowExecutionId"] = window_execution_id
    kwargs["TaskId"] = task_id
    kwargs["InvocationId"] = invocation_id
    try:
        resp = await client.call("GetMaintenanceWindowExecutionTaskInvocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to get maintenance window execution task invocation"
        ) from exc
    return GetMaintenanceWindowExecutionTaskInvocationResult(
        window_execution_id=resp.get("WindowExecutionId"),
        task_execution_id=resp.get("TaskExecutionId"),
        invocation_id=resp.get("InvocationId"),
        execution_id=resp.get("ExecutionId"),
        task_type=resp.get("TaskType"),
        parameters=resp.get("Parameters"),
        status=resp.get("Status"),
        status_details=resp.get("StatusDetails"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
        owner_information=resp.get("OwnerInformation"),
        window_target_id=resp.get("WindowTargetId"),
    )


async def get_maintenance_window_task(
    window_id: str,
    window_task_id: str,
    region_name: str | None = None,
) -> GetMaintenanceWindowTaskResult:
    """Get maintenance window task.

    Args:
        window_id: Window id.
        window_task_id: Window task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["WindowTaskId"] = window_task_id
    try:
        resp = await client.call("GetMaintenanceWindowTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get maintenance window task") from exc
    return GetMaintenanceWindowTaskResult(
        window_id=resp.get("WindowId"),
        window_task_id=resp.get("WindowTaskId"),
        targets=resp.get("Targets"),
        task_arn=resp.get("TaskArn"),
        service_role_arn=resp.get("ServiceRoleArn"),
        task_type=resp.get("TaskType"),
        task_parameters=resp.get("TaskParameters"),
        task_invocation_parameters=resp.get("TaskInvocationParameters"),
        priority=resp.get("Priority"),
        max_concurrency=resp.get("MaxConcurrency"),
        max_errors=resp.get("MaxErrors"),
        logging_info=resp.get("LoggingInfo"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        cutoff_behavior=resp.get("CutoffBehavior"),
        alarm_configuration=resp.get("AlarmConfiguration"),
    )


async def get_ops_item(
    ops_item_id: str,
    *,
    ops_item_arn: str | None = None,
    region_name: str | None = None,
) -> GetOpsItemResult:
    """Get ops item.

    Args:
        ops_item_id: Ops item id.
        ops_item_arn: Ops item arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsItemId"] = ops_item_id
    if ops_item_arn is not None:
        kwargs["OpsItemArn"] = ops_item_arn
    try:
        resp = await client.call("GetOpsItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ops item") from exc
    return GetOpsItemResult(
        ops_item=resp.get("OpsItem"),
    )


async def get_ops_metadata(
    ops_metadata_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetOpsMetadataResult:
    """Get ops metadata.

    Args:
        ops_metadata_arn: Ops metadata arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsMetadataArn"] = ops_metadata_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetOpsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ops metadata") from exc
    return GetOpsMetadataResult(
        resource_id=resp.get("ResourceId"),
        metadata=resp.get("Metadata"),
        next_token=resp.get("NextToken"),
    )


async def get_ops_summary(
    *,
    sync_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    aggregators: list[dict[str, Any]] | None = None,
    result_attributes: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetOpsSummaryResult:
    """Get ops summary.

    Args:
        sync_name: Sync name.
        filters: Filters.
        aggregators: Aggregators.
        result_attributes: Result attributes.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if sync_name is not None:
        kwargs["SyncName"] = sync_name
    if filters is not None:
        kwargs["Filters"] = filters
    if aggregators is not None:
        kwargs["Aggregators"] = aggregators
    if result_attributes is not None:
        kwargs["ResultAttributes"] = result_attributes
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetOpsSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ops summary") from exc
    return GetOpsSummaryResult(
        entities=resp.get("Entities"),
        next_token=resp.get("NextToken"),
    )


async def get_parameter_history(
    name: str,
    *,
    with_decryption: bool | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetParameterHistoryResult:
    """Get parameter history.

    Args:
        name: Name.
        with_decryption: With decryption.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if with_decryption is not None:
        kwargs["WithDecryption"] = with_decryption
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetParameterHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get parameter history") from exc
    return GetParameterHistoryResult(
        parameters=resp.get("Parameters"),
        next_token=resp.get("NextToken"),
    )


async def get_parameters(
    names: list[str],
    *,
    with_decryption: bool | None = None,
    region_name: str | None = None,
) -> GetParametersResult:
    """Get parameters.

    Args:
        names: Names.
        with_decryption: With decryption.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    if with_decryption is not None:
        kwargs["WithDecryption"] = with_decryption
    try:
        resp = await client.call("GetParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get parameters") from exc
    return GetParametersResult(
        parameters=resp.get("Parameters"),
        invalid_parameters=resp.get("InvalidParameters"),
    )


async def get_patch_baseline(
    baseline_id: str,
    region_name: str | None = None,
) -> GetPatchBaselineResult:
    """Get patch baseline.

    Args:
        baseline_id: Baseline id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    try:
        resp = await client.call("GetPatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get patch baseline") from exc
    return GetPatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
        name=resp.get("Name"),
        operating_system=resp.get("OperatingSystem"),
        global_filters=resp.get("GlobalFilters"),
        approval_rules=resp.get("ApprovalRules"),
        approved_patches=resp.get("ApprovedPatches"),
        approved_patches_compliance_level=resp.get("ApprovedPatchesComplianceLevel"),
        approved_patches_enable_non_security=resp.get("ApprovedPatchesEnableNonSecurity"),
        rejected_patches=resp.get("RejectedPatches"),
        rejected_patches_action=resp.get("RejectedPatchesAction"),
        patch_groups=resp.get("PatchGroups"),
        created_date=resp.get("CreatedDate"),
        modified_date=resp.get("ModifiedDate"),
        description=resp.get("Description"),
        sources=resp.get("Sources"),
        available_security_updates_compliance_status=resp.get(
            "AvailableSecurityUpdatesComplianceStatus"
        ),
    )


async def get_patch_baseline_for_patch_group(
    patch_group: str,
    *,
    operating_system: str | None = None,
    region_name: str | None = None,
) -> GetPatchBaselineForPatchGroupResult:
    """Get patch baseline for patch group.

    Args:
        patch_group: Patch group.
        operating_system: Operating system.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PatchGroup"] = patch_group
    if operating_system is not None:
        kwargs["OperatingSystem"] = operating_system
    try:
        resp = await client.call("GetPatchBaselineForPatchGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get patch baseline for patch group") from exc
    return GetPatchBaselineForPatchGroupResult(
        baseline_id=resp.get("BaselineId"),
        patch_group=resp.get("PatchGroup"),
        operating_system=resp.get("OperatingSystem"),
    )


async def get_resource_policies(
    resource_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetResourcePoliciesResult:
    """Get resource policies.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetResourcePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policies") from exc
    return GetResourcePoliciesResult(
        next_token=resp.get("NextToken"),
        policies=resp.get("Policies"),
    )


async def get_service_setting(
    setting_id: str,
    region_name: str | None = None,
) -> GetServiceSettingResult:
    """Get service setting.

    Args:
        setting_id: Setting id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SettingId"] = setting_id
    try:
        resp = await client.call("GetServiceSetting", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get service setting") from exc
    return GetServiceSettingResult(
        service_setting=resp.get("ServiceSetting"),
    )


async def label_parameter_version(
    name: str,
    labels: list[str],
    *,
    parameter_version: int | None = None,
    region_name: str | None = None,
) -> LabelParameterVersionResult:
    """Label parameter version.

    Args:
        name: Name.
        labels: Labels.
        parameter_version: Parameter version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Labels"] = labels
    if parameter_version is not None:
        kwargs["ParameterVersion"] = parameter_version
    try:
        resp = await client.call("LabelParameterVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to label parameter version") from exc
    return LabelParameterVersionResult(
        invalid_labels=resp.get("InvalidLabels"),
        parameter_version=resp.get("ParameterVersion"),
    )


async def list_association_versions(
    association_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAssociationVersionsResult:
    """List association versions.

    Args:
        association_id: Association id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListAssociationVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list association versions") from exc
    return ListAssociationVersionsResult(
        association_versions=resp.get("AssociationVersions"),
        next_token=resp.get("NextToken"),
    )


async def list_associations(
    *,
    association_filter_list: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAssociationsResult:
    """List associations.

    Args:
        association_filter_list: Association filter list.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if association_filter_list is not None:
        kwargs["AssociationFilterList"] = association_filter_list
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list associations") from exc
    return ListAssociationsResult(
        associations=resp.get("Associations"),
        next_token=resp.get("NextToken"),
    )


async def list_command_invocations(
    *,
    command_id: str | None = None,
    instance_id: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    details: bool | None = None,
    region_name: str | None = None,
) -> ListCommandInvocationsResult:
    """List command invocations.

    Args:
        command_id: Command id.
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        filters: Filters.
        details: Details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if command_id is not None:
        kwargs["CommandId"] = command_id
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filters is not None:
        kwargs["Filters"] = filters
    if details is not None:
        kwargs["Details"] = details
    try:
        resp = await client.call("ListCommandInvocations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list command invocations") from exc
    return ListCommandInvocationsResult(
        command_invocations=resp.get("CommandInvocations"),
        next_token=resp.get("NextToken"),
    )


async def list_commands(
    *,
    command_id: str | None = None,
    instance_id: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListCommandsResult:
    """List commands.

    Args:
        command_id: Command id.
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if command_id is not None:
        kwargs["CommandId"] = command_id
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListCommands", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list commands") from exc
    return ListCommandsResult(
        commands=resp.get("Commands"),
        next_token=resp.get("NextToken"),
    )


async def list_compliance_items(
    *,
    filters: list[dict[str, Any]] | None = None,
    resource_ids: list[str] | None = None,
    resource_types: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListComplianceItemsResult:
    """List compliance items.

    Args:
        filters: Filters.
        resource_ids: Resource ids.
        resource_types: Resource types.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if resource_ids is not None:
        kwargs["ResourceIds"] = resource_ids
    if resource_types is not None:
        kwargs["ResourceTypes"] = resource_types
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListComplianceItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list compliance items") from exc
    return ListComplianceItemsResult(
        compliance_items=resp.get("ComplianceItems"),
        next_token=resp.get("NextToken"),
    )


async def list_compliance_summaries(
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListComplianceSummariesResult:
    """List compliance summaries.

    Args:
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListComplianceSummaries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list compliance summaries") from exc
    return ListComplianceSummariesResult(
        compliance_summary_items=resp.get("ComplianceSummaryItems"),
        next_token=resp.get("NextToken"),
    )


async def list_document_metadata_history(
    name: str,
    metadata: str,
    *,
    document_version: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDocumentMetadataHistoryResult:
    """List document metadata history.

    Args:
        name: Name.
        metadata: Metadata.
        document_version: Document version.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Metadata"] = metadata
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDocumentMetadataHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list document metadata history") from exc
    return ListDocumentMetadataHistoryResult(
        name=resp.get("Name"),
        document_version=resp.get("DocumentVersion"),
        author=resp.get("Author"),
        metadata=resp.get("Metadata"),
        next_token=resp.get("NextToken"),
    )


async def list_document_versions(
    name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDocumentVersionsResult:
    """List document versions.

    Args:
        name: Name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListDocumentVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list document versions") from exc
    return ListDocumentVersionsResult(
        document_versions=resp.get("DocumentVersions"),
        next_token=resp.get("NextToken"),
    )


async def list_documents(
    *,
    document_filter_list: list[dict[str, Any]] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDocumentsResult:
    """List documents.

    Args:
        document_filter_list: Document filter list.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if document_filter_list is not None:
        kwargs["DocumentFilterList"] = document_filter_list
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListDocuments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list documents") from exc
    return ListDocumentsResult(
        document_identifiers=resp.get("DocumentIdentifiers"),
        next_token=resp.get("NextToken"),
    )


async def list_inventory_entries(
    instance_id: str,
    type_name: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInventoryEntriesResult:
    """List inventory entries.

    Args:
        instance_id: Instance id.
        type_name: Type name.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["TypeName"] = type_name
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListInventoryEntries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list inventory entries") from exc
    return ListInventoryEntriesResult(
        type_name=resp.get("TypeName"),
        instance_id=resp.get("InstanceId"),
        schema_version=resp.get("SchemaVersion"),
        capture_time=resp.get("CaptureTime"),
        entries=resp.get("Entries"),
        next_token=resp.get("NextToken"),
    )


async def list_nodes(
    *,
    sync_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListNodesResult:
    """List nodes.

    Args:
        sync_name: Sync name.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if sync_name is not None:
        kwargs["SyncName"] = sync_name
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListNodes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list nodes") from exc
    return ListNodesResult(
        nodes=resp.get("Nodes"),
        next_token=resp.get("NextToken"),
    )


async def list_nodes_summary(
    aggregators: list[dict[str, Any]],
    *,
    sync_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListNodesSummaryResult:
    """List nodes summary.

    Args:
        aggregators: Aggregators.
        sync_name: Sync name.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Aggregators"] = aggregators
    if sync_name is not None:
        kwargs["SyncName"] = sync_name
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListNodesSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list nodes summary") from exc
    return ListNodesSummaryResult(
        summary=resp.get("Summary"),
        next_token=resp.get("NextToken"),
    )


async def list_ops_item_events(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListOpsItemEventsResult:
    """List ops item events.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListOpsItemEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ops item events") from exc
    return ListOpsItemEventsResult(
        next_token=resp.get("NextToken"),
        summaries=resp.get("Summaries"),
    )


async def list_ops_item_related_items(
    *,
    ops_item_id: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListOpsItemRelatedItemsResult:
    """List ops item related items.

    Args:
        ops_item_id: Ops item id.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if ops_item_id is not None:
        kwargs["OpsItemId"] = ops_item_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListOpsItemRelatedItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ops item related items") from exc
    return ListOpsItemRelatedItemsResult(
        next_token=resp.get("NextToken"),
        summaries=resp.get("Summaries"),
    )


async def list_ops_metadata(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListOpsMetadataResult:
    """List ops metadata.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListOpsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ops metadata") from exc
    return ListOpsMetadataResult(
        ops_metadata_list=resp.get("OpsMetadataList"),
        next_token=resp.get("NextToken"),
    )


async def list_resource_compliance_summaries(
    *,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListResourceComplianceSummariesResult:
    """List resource compliance summaries.

    Args:
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListResourceComplianceSummaries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list resource compliance summaries") from exc
    return ListResourceComplianceSummariesResult(
        resource_compliance_summary_items=resp.get("ResourceComplianceSummaryItems"),
        next_token=resp.get("NextToken"),
    )


async def list_resource_data_sync(
    *,
    sync_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListResourceDataSyncResult:
    """List resource data sync.

    Args:
        sync_type: Sync type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    if sync_type is not None:
        kwargs["SyncType"] = sync_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListResourceDataSync", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list resource data sync") from exc
    return ListResourceDataSyncResult(
        resource_data_sync_items=resp.get("ResourceDataSyncItems"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
    resource_type: str,
    resource_id: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tag_list=resp.get("TagList"),
    )


async def modify_document_permission(
    name: str,
    permission_type: str,
    *,
    account_ids_to_add: list[str] | None = None,
    account_ids_to_remove: list[str] | None = None,
    shared_document_version: str | None = None,
    region_name: str | None = None,
) -> None:
    """Modify document permission.

    Args:
        name: Name.
        permission_type: Permission type.
        account_ids_to_add: Account ids to add.
        account_ids_to_remove: Account ids to remove.
        shared_document_version: Shared document version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["PermissionType"] = permission_type
    if account_ids_to_add is not None:
        kwargs["AccountIdsToAdd"] = account_ids_to_add
    if account_ids_to_remove is not None:
        kwargs["AccountIdsToRemove"] = account_ids_to_remove
    if shared_document_version is not None:
        kwargs["SharedDocumentVersion"] = shared_document_version
    try:
        await client.call("ModifyDocumentPermission", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify document permission") from exc
    return None


async def put_compliance_items(
    resource_id: str,
    resource_type: str,
    compliance_type: str,
    execution_summary: dict[str, Any],
    items: list[dict[str, Any]],
    *,
    item_content_hash: str | None = None,
    upload_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put compliance items.

    Args:
        resource_id: Resource id.
        resource_type: Resource type.
        compliance_type: Compliance type.
        execution_summary: Execution summary.
        items: Items.
        item_content_hash: Item content hash.
        upload_type: Upload type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["ResourceType"] = resource_type
    kwargs["ComplianceType"] = compliance_type
    kwargs["ExecutionSummary"] = execution_summary
    kwargs["Items"] = items
    if item_content_hash is not None:
        kwargs["ItemContentHash"] = item_content_hash
    if upload_type is not None:
        kwargs["UploadType"] = upload_type
    try:
        await client.call("PutComplianceItems", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put compliance items") from exc
    return None


async def put_inventory(
    instance_id: str,
    items: list[dict[str, Any]],
    region_name: str | None = None,
) -> PutInventoryResult:
    """Put inventory.

    Args:
        instance_id: Instance id.
        items: Items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Items"] = items
    try:
        resp = await client.call("PutInventory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put inventory") from exc
    return PutInventoryResult(
        message=resp.get("Message"),
    )


async def put_resource_policy(
    resource_arn: str,
    policy: str,
    *,
    policy_id: str | None = None,
    policy_hash: str | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        policy_id: Policy id.
        policy_hash: Policy hash.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Policy"] = policy
    if policy_id is not None:
        kwargs["PolicyId"] = policy_id
    if policy_hash is not None:
        kwargs["PolicyHash"] = policy_hash
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        policy_id=resp.get("PolicyId"),
        policy_hash=resp.get("PolicyHash"),
    )


async def register_default_patch_baseline(
    baseline_id: str,
    region_name: str | None = None,
) -> RegisterDefaultPatchBaselineResult:
    """Register default patch baseline.

    Args:
        baseline_id: Baseline id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    try:
        resp = await client.call("RegisterDefaultPatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register default patch baseline") from exc
    return RegisterDefaultPatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
    )


async def register_patch_baseline_for_patch_group(
    baseline_id: str,
    patch_group: str,
    region_name: str | None = None,
) -> RegisterPatchBaselineForPatchGroupResult:
    """Register patch baseline for patch group.

    Args:
        baseline_id: Baseline id.
        patch_group: Patch group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    kwargs["PatchGroup"] = patch_group
    try:
        resp = await client.call("RegisterPatchBaselineForPatchGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register patch baseline for patch group") from exc
    return RegisterPatchBaselineForPatchGroupResult(
        baseline_id=resp.get("BaselineId"),
        patch_group=resp.get("PatchGroup"),
    )


async def register_target_with_maintenance_window(
    window_id: str,
    resource_type: str,
    targets: list[dict[str, Any]],
    *,
    owner_information: str | None = None,
    name: str | None = None,
    description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> RegisterTargetWithMaintenanceWindowResult:
    """Register target with maintenance window.

    Args:
        window_id: Window id.
        resource_type: Resource type.
        targets: Targets.
        owner_information: Owner information.
        name: Name.
        description: Description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["ResourceType"] = resource_type
    kwargs["Targets"] = targets
    if owner_information is not None:
        kwargs["OwnerInformation"] = owner_information
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("RegisterTargetWithMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register target with maintenance window") from exc
    return RegisterTargetWithMaintenanceWindowResult(
        window_target_id=resp.get("WindowTargetId"),
    )


async def register_task_with_maintenance_window(
    window_id: str,
    task_arn: str,
    task_type: str,
    *,
    targets: list[dict[str, Any]] | None = None,
    service_role_arn: str | None = None,
    task_parameters: dict[str, Any] | None = None,
    task_invocation_parameters: dict[str, Any] | None = None,
    priority: int | None = None,
    max_concurrency: str | None = None,
    max_errors: str | None = None,
    logging_info: dict[str, Any] | None = None,
    name: str | None = None,
    description: str | None = None,
    client_token: str | None = None,
    cutoff_behavior: str | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RegisterTaskWithMaintenanceWindowResult:
    """Register task with maintenance window.

    Args:
        window_id: Window id.
        task_arn: Task arn.
        task_type: Task type.
        targets: Targets.
        service_role_arn: Service role arn.
        task_parameters: Task parameters.
        task_invocation_parameters: Task invocation parameters.
        priority: Priority.
        max_concurrency: Max concurrency.
        max_errors: Max errors.
        logging_info: Logging info.
        name: Name.
        description: Description.
        client_token: Client token.
        cutoff_behavior: Cutoff behavior.
        alarm_configuration: Alarm configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["TaskArn"] = task_arn
    kwargs["TaskType"] = task_type
    if targets is not None:
        kwargs["Targets"] = targets
    if service_role_arn is not None:
        kwargs["ServiceRoleArn"] = service_role_arn
    if task_parameters is not None:
        kwargs["TaskParameters"] = task_parameters
    if task_invocation_parameters is not None:
        kwargs["TaskInvocationParameters"] = task_invocation_parameters
    if priority is not None:
        kwargs["Priority"] = priority
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if logging_info is not None:
        kwargs["LoggingInfo"] = logging_info
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if cutoff_behavior is not None:
        kwargs["CutoffBehavior"] = cutoff_behavior
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    try:
        resp = await client.call("RegisterTaskWithMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register task with maintenance window") from exc
    return RegisterTaskWithMaintenanceWindowResult(
        window_task_id=resp.get("WindowTaskId"),
    )


async def remove_tags_from_resource(
    resource_type: str,
    resource_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags from resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("RemoveTagsFromResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return None


async def reset_service_setting(
    setting_id: str,
    region_name: str | None = None,
) -> ResetServiceSettingResult:
    """Reset service setting.

    Args:
        setting_id: Setting id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SettingId"] = setting_id
    try:
        resp = await client.call("ResetServiceSetting", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset service setting") from exc
    return ResetServiceSettingResult(
        service_setting=resp.get("ServiceSetting"),
    )


async def resume_session(
    session_id: str,
    region_name: str | None = None,
) -> ResumeSessionResult:
    """Resume session.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("ResumeSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resume session") from exc
    return ResumeSessionResult(
        session_id=resp.get("SessionId"),
        token_value=resp.get("TokenValue"),
        stream_url=resp.get("StreamUrl"),
    )


async def send_automation_signal(
    automation_execution_id: str,
    signal_type: str,
    *,
    payload: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Send automation signal.

    Args:
        automation_execution_id: Automation execution id.
        signal_type: Signal type.
        payload: Payload.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationExecutionId"] = automation_execution_id
    kwargs["SignalType"] = signal_type
    if payload is not None:
        kwargs["Payload"] = payload
    try:
        await client.call("SendAutomationSignal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send automation signal") from exc
    return None


async def send_command(
    document_name: str,
    *,
    instance_ids: list[str] | None = None,
    targets: list[dict[str, Any]] | None = None,
    document_version: str | None = None,
    document_hash: str | None = None,
    document_hash_type: str | None = None,
    timeout_seconds: int | None = None,
    comment: str | None = None,
    parameters: dict[str, Any] | None = None,
    output_s3_region: str | None = None,
    output_s3_bucket_name: str | None = None,
    output_s3_key_prefix: str | None = None,
    max_concurrency: str | None = None,
    max_errors: str | None = None,
    service_role_arn: str | None = None,
    notification_config: dict[str, Any] | None = None,
    cloud_watch_output_config: dict[str, Any] | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SendCommandResult:
    """Send command.

    Args:
        document_name: Document name.
        instance_ids: Instance ids.
        targets: Targets.
        document_version: Document version.
        document_hash: Document hash.
        document_hash_type: Document hash type.
        timeout_seconds: Timeout seconds.
        comment: Comment.
        parameters: Parameters.
        output_s3_region: Output s3 region.
        output_s3_bucket_name: Output s3 bucket name.
        output_s3_key_prefix: Output s3 key prefix.
        max_concurrency: Max concurrency.
        max_errors: Max errors.
        service_role_arn: Service role arn.
        notification_config: Notification config.
        cloud_watch_output_config: Cloud watch output config.
        alarm_configuration: Alarm configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentName"] = document_name
    if instance_ids is not None:
        kwargs["InstanceIds"] = instance_ids
    if targets is not None:
        kwargs["Targets"] = targets
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if document_hash is not None:
        kwargs["DocumentHash"] = document_hash
    if document_hash_type is not None:
        kwargs["DocumentHashType"] = document_hash_type
    if timeout_seconds is not None:
        kwargs["TimeoutSeconds"] = timeout_seconds
    if comment is not None:
        kwargs["Comment"] = comment
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if output_s3_region is not None:
        kwargs["OutputS3Region"] = output_s3_region
    if output_s3_bucket_name is not None:
        kwargs["OutputS3BucketName"] = output_s3_bucket_name
    if output_s3_key_prefix is not None:
        kwargs["OutputS3KeyPrefix"] = output_s3_key_prefix
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if service_role_arn is not None:
        kwargs["ServiceRoleArn"] = service_role_arn
    if notification_config is not None:
        kwargs["NotificationConfig"] = notification_config
    if cloud_watch_output_config is not None:
        kwargs["CloudWatchOutputConfig"] = cloud_watch_output_config
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    try:
        resp = await client.call("SendCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to send command") from exc
    return SendCommandResult(
        command=resp.get("Command"),
    )


async def start_access_request(
    reason: str,
    targets: list[dict[str, Any]],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartAccessRequestResult:
    """Start access request.

    Args:
        reason: Reason.
        targets: Targets.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Reason"] = reason
    kwargs["Targets"] = targets
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("StartAccessRequest", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start access request") from exc
    return StartAccessRequestResult(
        access_request_id=resp.get("AccessRequestId"),
    )


async def start_associations_once(
    association_ids: list[str],
    region_name: str | None = None,
) -> None:
    """Start associations once.

    Args:
        association_ids: Association ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationIds"] = association_ids
    try:
        await client.call("StartAssociationsOnce", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start associations once") from exc
    return None


async def start_automation_execution(
    document_name: str,
    *,
    document_version: str | None = None,
    parameters: dict[str, Any] | None = None,
    client_token: str | None = None,
    mode: str | None = None,
    target_parameter_name: str | None = None,
    targets: list[dict[str, Any]] | None = None,
    target_maps: list[dict[str, Any]] | None = None,
    max_concurrency: str | None = None,
    max_errors: str | None = None,
    target_locations: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    target_locations_url: str | None = None,
    region_name: str | None = None,
) -> StartAutomationExecutionResult:
    """Start automation execution.

    Args:
        document_name: Document name.
        document_version: Document version.
        parameters: Parameters.
        client_token: Client token.
        mode: Mode.
        target_parameter_name: Target parameter name.
        targets: Targets.
        target_maps: Target maps.
        max_concurrency: Max concurrency.
        max_errors: Max errors.
        target_locations: Target locations.
        tags: Tags.
        alarm_configuration: Alarm configuration.
        target_locations_url: Target locations url.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentName"] = document_name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if mode is not None:
        kwargs["Mode"] = mode
    if target_parameter_name is not None:
        kwargs["TargetParameterName"] = target_parameter_name
    if targets is not None:
        kwargs["Targets"] = targets
    if target_maps is not None:
        kwargs["TargetMaps"] = target_maps
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if target_locations is not None:
        kwargs["TargetLocations"] = target_locations
    if tags is not None:
        kwargs["Tags"] = tags
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    if target_locations_url is not None:
        kwargs["TargetLocationsURL"] = target_locations_url
    try:
        resp = await client.call("StartAutomationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start automation execution") from exc
    return StartAutomationExecutionResult(
        automation_execution_id=resp.get("AutomationExecutionId"),
    )


async def start_change_request_execution(
    document_name: str,
    runbooks: list[dict[str, Any]],
    *,
    scheduled_time: str | None = None,
    document_version: str | None = None,
    parameters: dict[str, Any] | None = None,
    change_request_name: str | None = None,
    client_token: str | None = None,
    auto_approve: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    scheduled_end_time: str | None = None,
    change_details: str | None = None,
    region_name: str | None = None,
) -> StartChangeRequestExecutionResult:
    """Start change request execution.

    Args:
        document_name: Document name.
        runbooks: Runbooks.
        scheduled_time: Scheduled time.
        document_version: Document version.
        parameters: Parameters.
        change_request_name: Change request name.
        client_token: Client token.
        auto_approve: Auto approve.
        tags: Tags.
        scheduled_end_time: Scheduled end time.
        change_details: Change details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentName"] = document_name
    kwargs["Runbooks"] = runbooks
    if scheduled_time is not None:
        kwargs["ScheduledTime"] = scheduled_time
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if change_request_name is not None:
        kwargs["ChangeRequestName"] = change_request_name
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if auto_approve is not None:
        kwargs["AutoApprove"] = auto_approve
    if tags is not None:
        kwargs["Tags"] = tags
    if scheduled_end_time is not None:
        kwargs["ScheduledEndTime"] = scheduled_end_time
    if change_details is not None:
        kwargs["ChangeDetails"] = change_details
    try:
        resp = await client.call("StartChangeRequestExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start change request execution") from exc
    return StartChangeRequestExecutionResult(
        automation_execution_id=resp.get("AutomationExecutionId"),
    )


async def start_execution_preview(
    document_name: str,
    *,
    document_version: str | None = None,
    execution_inputs: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartExecutionPreviewResult:
    """Start execution preview.

    Args:
        document_name: Document name.
        document_version: Document version.
        execution_inputs: Execution inputs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DocumentName"] = document_name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if execution_inputs is not None:
        kwargs["ExecutionInputs"] = execution_inputs
    try:
        resp = await client.call("StartExecutionPreview", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start execution preview") from exc
    return StartExecutionPreviewResult(
        execution_preview_id=resp.get("ExecutionPreviewId"),
    )


async def start_session(
    target: str,
    *,
    document_name: str | None = None,
    reason: str | None = None,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartSessionResult:
    """Start session.

    Args:
        target: Target.
        document_name: Document name.
        reason: Reason.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Target"] = target
    if document_name is not None:
        kwargs["DocumentName"] = document_name
    if reason is not None:
        kwargs["Reason"] = reason
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = await client.call("StartSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start session") from exc
    return StartSessionResult(
        session_id=resp.get("SessionId"),
        token_value=resp.get("TokenValue"),
        stream_url=resp.get("StreamUrl"),
    )


async def stop_automation_execution(
    automation_execution_id: str,
    *,
    type_value: str | None = None,
    region_name: str | None = None,
) -> None:
    """Stop automation execution.

    Args:
        automation_execution_id: Automation execution id.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationExecutionId"] = automation_execution_id
    if type_value is not None:
        kwargs["Type"] = type_value
    try:
        await client.call("StopAutomationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop automation execution") from exc
    return None


async def terminate_session(
    session_id: str,
    region_name: str | None = None,
) -> TerminateSessionResult:
    """Terminate session.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("TerminateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to terminate session") from exc
    return TerminateSessionResult(
        session_id=resp.get("SessionId"),
    )


async def unlabel_parameter_version(
    name: str,
    parameter_version: int,
    labels: list[str],
    region_name: str | None = None,
) -> UnlabelParameterVersionResult:
    """Unlabel parameter version.

    Args:
        name: Name.
        parameter_version: Parameter version.
        labels: Labels.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ParameterVersion"] = parameter_version
    kwargs["Labels"] = labels
    try:
        resp = await client.call("UnlabelParameterVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to unlabel parameter version") from exc
    return UnlabelParameterVersionResult(
        removed_labels=resp.get("RemovedLabels"),
        invalid_labels=resp.get("InvalidLabels"),
    )


async def update_association(
    association_id: str,
    *,
    parameters: dict[str, Any] | None = None,
    document_version: str | None = None,
    schedule_expression: str | None = None,
    output_location: dict[str, Any] | None = None,
    name: str | None = None,
    targets: list[dict[str, Any]] | None = None,
    association_name: str | None = None,
    association_version: str | None = None,
    automation_target_parameter_name: str | None = None,
    max_errors: str | None = None,
    max_concurrency: str | None = None,
    compliance_severity: str | None = None,
    sync_compliance: str | None = None,
    apply_only_at_cron_interval: bool | None = None,
    calendar_names: list[str] | None = None,
    target_locations: list[dict[str, Any]] | None = None,
    schedule_offset: int | None = None,
    duration: int | None = None,
    target_maps: list[dict[str, Any]] | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateAssociationResult:
    """Update association.

    Args:
        association_id: Association id.
        parameters: Parameters.
        document_version: Document version.
        schedule_expression: Schedule expression.
        output_location: Output location.
        name: Name.
        targets: Targets.
        association_name: Association name.
        association_version: Association version.
        automation_target_parameter_name: Automation target parameter name.
        max_errors: Max errors.
        max_concurrency: Max concurrency.
        compliance_severity: Compliance severity.
        sync_compliance: Sync compliance.
        apply_only_at_cron_interval: Apply only at cron interval.
        calendar_names: Calendar names.
        target_locations: Target locations.
        schedule_offset: Schedule offset.
        duration: Duration.
        target_maps: Target maps.
        alarm_configuration: Alarm configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if schedule_expression is not None:
        kwargs["ScheduleExpression"] = schedule_expression
    if output_location is not None:
        kwargs["OutputLocation"] = output_location
    if name is not None:
        kwargs["Name"] = name
    if targets is not None:
        kwargs["Targets"] = targets
    if association_name is not None:
        kwargs["AssociationName"] = association_name
    if association_version is not None:
        kwargs["AssociationVersion"] = association_version
    if automation_target_parameter_name is not None:
        kwargs["AutomationTargetParameterName"] = automation_target_parameter_name
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if compliance_severity is not None:
        kwargs["ComplianceSeverity"] = compliance_severity
    if sync_compliance is not None:
        kwargs["SyncCompliance"] = sync_compliance
    if apply_only_at_cron_interval is not None:
        kwargs["ApplyOnlyAtCronInterval"] = apply_only_at_cron_interval
    if calendar_names is not None:
        kwargs["CalendarNames"] = calendar_names
    if target_locations is not None:
        kwargs["TargetLocations"] = target_locations
    if schedule_offset is not None:
        kwargs["ScheduleOffset"] = schedule_offset
    if duration is not None:
        kwargs["Duration"] = duration
    if target_maps is not None:
        kwargs["TargetMaps"] = target_maps
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    try:
        resp = await client.call("UpdateAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update association") from exc
    return UpdateAssociationResult(
        association_description=resp.get("AssociationDescription"),
    )


async def update_association_status(
    name: str,
    instance_id: str,
    association_status: dict[str, Any],
    region_name: str | None = None,
) -> UpdateAssociationStatusResult:
    """Update association status.

    Args:
        name: Name.
        instance_id: Instance id.
        association_status: Association status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["InstanceId"] = instance_id
    kwargs["AssociationStatus"] = association_status
    try:
        resp = await client.call("UpdateAssociationStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update association status") from exc
    return UpdateAssociationStatusResult(
        association_description=resp.get("AssociationDescription"),
    )


async def update_document(
    content: str,
    name: str,
    *,
    attachments: list[dict[str, Any]] | None = None,
    display_name: str | None = None,
    version_name: str | None = None,
    document_version: str | None = None,
    document_format: str | None = None,
    target_type: str | None = None,
    region_name: str | None = None,
) -> UpdateDocumentResult:
    """Update document.

    Args:
        content: Content.
        name: Name.
        attachments: Attachments.
        display_name: Display name.
        version_name: Version name.
        document_version: Document version.
        document_format: Document format.
        target_type: Target type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Content"] = content
    kwargs["Name"] = name
    if attachments is not None:
        kwargs["Attachments"] = attachments
    if display_name is not None:
        kwargs["DisplayName"] = display_name
    if version_name is not None:
        kwargs["VersionName"] = version_name
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    if document_format is not None:
        kwargs["DocumentFormat"] = document_format
    if target_type is not None:
        kwargs["TargetType"] = target_type
    try:
        resp = await client.call("UpdateDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update document") from exc
    return UpdateDocumentResult(
        document_description=resp.get("DocumentDescription"),
    )


async def update_document_default_version(
    name: str,
    document_version: str,
    region_name: str | None = None,
) -> UpdateDocumentDefaultVersionResult:
    """Update document default version.

    Args:
        name: Name.
        document_version: Document version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["DocumentVersion"] = document_version
    try:
        resp = await client.call("UpdateDocumentDefaultVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update document default version") from exc
    return UpdateDocumentDefaultVersionResult(
        description=resp.get("Description"),
    )


async def update_document_metadata(
    name: str,
    document_reviews: dict[str, Any],
    *,
    document_version: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update document metadata.

    Args:
        name: Name.
        document_reviews: Document reviews.
        document_version: Document version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["DocumentReviews"] = document_reviews
    if document_version is not None:
        kwargs["DocumentVersion"] = document_version
    try:
        await client.call("UpdateDocumentMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update document metadata") from exc
    return None


async def update_maintenance_window(
    window_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    schedule: str | None = None,
    schedule_timezone: str | None = None,
    schedule_offset: int | None = None,
    duration: int | None = None,
    cutoff: int | None = None,
    allow_unassociated_targets: bool | None = None,
    enabled: bool | None = None,
    replace: bool | None = None,
    region_name: str | None = None,
) -> UpdateMaintenanceWindowResult:
    """Update maintenance window.

    Args:
        window_id: Window id.
        name: Name.
        description: Description.
        start_date: Start date.
        end_date: End date.
        schedule: Schedule.
        schedule_timezone: Schedule timezone.
        schedule_offset: Schedule offset.
        duration: Duration.
        cutoff: Cutoff.
        allow_unassociated_targets: Allow unassociated targets.
        enabled: Enabled.
        replace: Replace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if schedule_timezone is not None:
        kwargs["ScheduleTimezone"] = schedule_timezone
    if schedule_offset is not None:
        kwargs["ScheduleOffset"] = schedule_offset
    if duration is not None:
        kwargs["Duration"] = duration
    if cutoff is not None:
        kwargs["Cutoff"] = cutoff
    if allow_unassociated_targets is not None:
        kwargs["AllowUnassociatedTargets"] = allow_unassociated_targets
    if enabled is not None:
        kwargs["Enabled"] = enabled
    if replace is not None:
        kwargs["Replace"] = replace
    try:
        resp = await client.call("UpdateMaintenanceWindow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update maintenance window") from exc
    return UpdateMaintenanceWindowResult(
        window_id=resp.get("WindowId"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        start_date=resp.get("StartDate"),
        end_date=resp.get("EndDate"),
        schedule=resp.get("Schedule"),
        schedule_timezone=resp.get("ScheduleTimezone"),
        schedule_offset=resp.get("ScheduleOffset"),
        duration=resp.get("Duration"),
        cutoff=resp.get("Cutoff"),
        allow_unassociated_targets=resp.get("AllowUnassociatedTargets"),
        enabled=resp.get("Enabled"),
    )


async def update_maintenance_window_target(
    window_id: str,
    window_target_id: str,
    *,
    targets: list[dict[str, Any]] | None = None,
    owner_information: str | None = None,
    name: str | None = None,
    description: str | None = None,
    replace: bool | None = None,
    region_name: str | None = None,
) -> UpdateMaintenanceWindowTargetResult:
    """Update maintenance window target.

    Args:
        window_id: Window id.
        window_target_id: Window target id.
        targets: Targets.
        owner_information: Owner information.
        name: Name.
        description: Description.
        replace: Replace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["WindowTargetId"] = window_target_id
    if targets is not None:
        kwargs["Targets"] = targets
    if owner_information is not None:
        kwargs["OwnerInformation"] = owner_information
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if replace is not None:
        kwargs["Replace"] = replace
    try:
        resp = await client.call("UpdateMaintenanceWindowTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update maintenance window target") from exc
    return UpdateMaintenanceWindowTargetResult(
        window_id=resp.get("WindowId"),
        window_target_id=resp.get("WindowTargetId"),
        targets=resp.get("Targets"),
        owner_information=resp.get("OwnerInformation"),
        name=resp.get("Name"),
        description=resp.get("Description"),
    )


async def update_maintenance_window_task(
    window_id: str,
    window_task_id: str,
    *,
    targets: list[dict[str, Any]] | None = None,
    task_arn: str | None = None,
    service_role_arn: str | None = None,
    task_parameters: dict[str, Any] | None = None,
    task_invocation_parameters: dict[str, Any] | None = None,
    priority: int | None = None,
    max_concurrency: str | None = None,
    max_errors: str | None = None,
    logging_info: dict[str, Any] | None = None,
    name: str | None = None,
    description: str | None = None,
    replace: bool | None = None,
    cutoff_behavior: str | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateMaintenanceWindowTaskResult:
    """Update maintenance window task.

    Args:
        window_id: Window id.
        window_task_id: Window task id.
        targets: Targets.
        task_arn: Task arn.
        service_role_arn: Service role arn.
        task_parameters: Task parameters.
        task_invocation_parameters: Task invocation parameters.
        priority: Priority.
        max_concurrency: Max concurrency.
        max_errors: Max errors.
        logging_info: Logging info.
        name: Name.
        description: Description.
        replace: Replace.
        cutoff_behavior: Cutoff behavior.
        alarm_configuration: Alarm configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WindowId"] = window_id
    kwargs["WindowTaskId"] = window_task_id
    if targets is not None:
        kwargs["Targets"] = targets
    if task_arn is not None:
        kwargs["TaskArn"] = task_arn
    if service_role_arn is not None:
        kwargs["ServiceRoleArn"] = service_role_arn
    if task_parameters is not None:
        kwargs["TaskParameters"] = task_parameters
    if task_invocation_parameters is not None:
        kwargs["TaskInvocationParameters"] = task_invocation_parameters
    if priority is not None:
        kwargs["Priority"] = priority
    if max_concurrency is not None:
        kwargs["MaxConcurrency"] = max_concurrency
    if max_errors is not None:
        kwargs["MaxErrors"] = max_errors
    if logging_info is not None:
        kwargs["LoggingInfo"] = logging_info
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if replace is not None:
        kwargs["Replace"] = replace
    if cutoff_behavior is not None:
        kwargs["CutoffBehavior"] = cutoff_behavior
    if alarm_configuration is not None:
        kwargs["AlarmConfiguration"] = alarm_configuration
    try:
        resp = await client.call("UpdateMaintenanceWindowTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update maintenance window task") from exc
    return UpdateMaintenanceWindowTaskResult(
        window_id=resp.get("WindowId"),
        window_task_id=resp.get("WindowTaskId"),
        targets=resp.get("Targets"),
        task_arn=resp.get("TaskArn"),
        service_role_arn=resp.get("ServiceRoleArn"),
        task_parameters=resp.get("TaskParameters"),
        task_invocation_parameters=resp.get("TaskInvocationParameters"),
        priority=resp.get("Priority"),
        max_concurrency=resp.get("MaxConcurrency"),
        max_errors=resp.get("MaxErrors"),
        logging_info=resp.get("LoggingInfo"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        cutoff_behavior=resp.get("CutoffBehavior"),
        alarm_configuration=resp.get("AlarmConfiguration"),
    )


async def update_managed_instance_role(
    instance_id: str,
    iam_role: str,
    region_name: str | None = None,
) -> None:
    """Update managed instance role.

    Args:
        instance_id: Instance id.
        iam_role: Iam role.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IamRole"] = iam_role
    try:
        await client.call("UpdateManagedInstanceRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update managed instance role") from exc
    return None


async def update_ops_item(
    ops_item_id: str,
    *,
    description: str | None = None,
    operational_data: dict[str, Any] | None = None,
    operational_data_to_delete: list[str] | None = None,
    notifications: list[dict[str, Any]] | None = None,
    priority: int | None = None,
    related_ops_items: list[dict[str, Any]] | None = None,
    status: str | None = None,
    title: str | None = None,
    category: str | None = None,
    severity: str | None = None,
    actual_start_time: str | None = None,
    actual_end_time: str | None = None,
    planned_start_time: str | None = None,
    planned_end_time: str | None = None,
    ops_item_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update ops item.

    Args:
        ops_item_id: Ops item id.
        description: Description.
        operational_data: Operational data.
        operational_data_to_delete: Operational data to delete.
        notifications: Notifications.
        priority: Priority.
        related_ops_items: Related ops items.
        status: Status.
        title: Title.
        category: Category.
        severity: Severity.
        actual_start_time: Actual start time.
        actual_end_time: Actual end time.
        planned_start_time: Planned start time.
        planned_end_time: Planned end time.
        ops_item_arn: Ops item arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsItemId"] = ops_item_id
    if description is not None:
        kwargs["Description"] = description
    if operational_data is not None:
        kwargs["OperationalData"] = operational_data
    if operational_data_to_delete is not None:
        kwargs["OperationalDataToDelete"] = operational_data_to_delete
    if notifications is not None:
        kwargs["Notifications"] = notifications
    if priority is not None:
        kwargs["Priority"] = priority
    if related_ops_items is not None:
        kwargs["RelatedOpsItems"] = related_ops_items
    if status is not None:
        kwargs["Status"] = status
    if title is not None:
        kwargs["Title"] = title
    if category is not None:
        kwargs["Category"] = category
    if severity is not None:
        kwargs["Severity"] = severity
    if actual_start_time is not None:
        kwargs["ActualStartTime"] = actual_start_time
    if actual_end_time is not None:
        kwargs["ActualEndTime"] = actual_end_time
    if planned_start_time is not None:
        kwargs["PlannedStartTime"] = planned_start_time
    if planned_end_time is not None:
        kwargs["PlannedEndTime"] = planned_end_time
    if ops_item_arn is not None:
        kwargs["OpsItemArn"] = ops_item_arn
    try:
        await client.call("UpdateOpsItem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ops item") from exc
    return None


async def update_ops_metadata(
    ops_metadata_arn: str,
    *,
    metadata_to_update: dict[str, Any] | None = None,
    keys_to_delete: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateOpsMetadataResult:
    """Update ops metadata.

    Args:
        ops_metadata_arn: Ops metadata arn.
        metadata_to_update: Metadata to update.
        keys_to_delete: Keys to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpsMetadataArn"] = ops_metadata_arn
    if metadata_to_update is not None:
        kwargs["MetadataToUpdate"] = metadata_to_update
    if keys_to_delete is not None:
        kwargs["KeysToDelete"] = keys_to_delete
    try:
        resp = await client.call("UpdateOpsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ops metadata") from exc
    return UpdateOpsMetadataResult(
        ops_metadata_arn=resp.get("OpsMetadataArn"),
    )


async def update_patch_baseline(
    baseline_id: str,
    *,
    name: str | None = None,
    global_filters: dict[str, Any] | None = None,
    approval_rules: dict[str, Any] | None = None,
    approved_patches: list[str] | None = None,
    approved_patches_compliance_level: str | None = None,
    approved_patches_enable_non_security: bool | None = None,
    rejected_patches: list[str] | None = None,
    rejected_patches_action: str | None = None,
    description: str | None = None,
    sources: list[dict[str, Any]] | None = None,
    available_security_updates_compliance_status: str | None = None,
    replace: bool | None = None,
    region_name: str | None = None,
) -> UpdatePatchBaselineResult:
    """Update patch baseline.

    Args:
        baseline_id: Baseline id.
        name: Name.
        global_filters: Global filters.
        approval_rules: Approval rules.
        approved_patches: Approved patches.
        approved_patches_compliance_level: Approved patches compliance level.
        approved_patches_enable_non_security: Approved patches enable non security.
        rejected_patches: Rejected patches.
        rejected_patches_action: Rejected patches action.
        description: Description.
        sources: Sources.
        available_security_updates_compliance_status: Available security updates compliance status.
        replace: Replace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BaselineId"] = baseline_id
    if name is not None:
        kwargs["Name"] = name
    if global_filters is not None:
        kwargs["GlobalFilters"] = global_filters
    if approval_rules is not None:
        kwargs["ApprovalRules"] = approval_rules
    if approved_patches is not None:
        kwargs["ApprovedPatches"] = approved_patches
    if approved_patches_compliance_level is not None:
        kwargs["ApprovedPatchesComplianceLevel"] = approved_patches_compliance_level
    if approved_patches_enable_non_security is not None:
        kwargs["ApprovedPatchesEnableNonSecurity"] = approved_patches_enable_non_security
    if rejected_patches is not None:
        kwargs["RejectedPatches"] = rejected_patches
    if rejected_patches_action is not None:
        kwargs["RejectedPatchesAction"] = rejected_patches_action
    if description is not None:
        kwargs["Description"] = description
    if sources is not None:
        kwargs["Sources"] = sources
    if available_security_updates_compliance_status is not None:
        kwargs["AvailableSecurityUpdatesComplianceStatus"] = (
            available_security_updates_compliance_status
        )
    if replace is not None:
        kwargs["Replace"] = replace
    try:
        resp = await client.call("UpdatePatchBaseline", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update patch baseline") from exc
    return UpdatePatchBaselineResult(
        baseline_id=resp.get("BaselineId"),
        name=resp.get("Name"),
        operating_system=resp.get("OperatingSystem"),
        global_filters=resp.get("GlobalFilters"),
        approval_rules=resp.get("ApprovalRules"),
        approved_patches=resp.get("ApprovedPatches"),
        approved_patches_compliance_level=resp.get("ApprovedPatchesComplianceLevel"),
        approved_patches_enable_non_security=resp.get("ApprovedPatchesEnableNonSecurity"),
        rejected_patches=resp.get("RejectedPatches"),
        rejected_patches_action=resp.get("RejectedPatchesAction"),
        created_date=resp.get("CreatedDate"),
        modified_date=resp.get("ModifiedDate"),
        description=resp.get("Description"),
        sources=resp.get("Sources"),
        available_security_updates_compliance_status=resp.get(
            "AvailableSecurityUpdatesComplianceStatus"
        ),
    )


async def update_resource_data_sync(
    sync_name: str,
    sync_type: str,
    sync_source: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update resource data sync.

    Args:
        sync_name: Sync name.
        sync_type: Sync type.
        sync_source: Sync source.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SyncName"] = sync_name
    kwargs["SyncType"] = sync_type
    kwargs["SyncSource"] = sync_source
    try:
        await client.call("UpdateResourceDataSync", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update resource data sync") from exc
    return None


async def update_service_setting(
    setting_id: str,
    setting_value: str,
    region_name: str | None = None,
) -> None:
    """Update service setting.

    Args:
        setting_id: Setting id.
        setting_value: Setting value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ssm", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SettingId"] = setting_id
    kwargs["SettingValue"] = setting_value
    try:
        await client.call("UpdateServiceSetting", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update service setting") from exc
    return None
