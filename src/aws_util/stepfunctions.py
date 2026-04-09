from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CreateActivityResult",
    "CreateStateMachineAliasResult",
    "CreateStateMachineResult",
    "DescribeActivityResult",
    "DescribeMapRunResult",
    "DescribeStateMachineAliasResult",
    "DescribeStateMachineForExecutionResult",
    "DescribeStateMachineResult",
    "GetActivityTaskResult",
    "ListActivitiesResult",
    "ListMapRunsResult",
    "ListStateMachineAliasesResult",
    "ListStateMachineVersionsResult",
    "ListTagsForResourceResult",
    "PublishStateMachineVersionResult",
    "RedriveExecutionResult",
    "RunStateResult",
    "SFNExecution",
    "StartSyncExecutionResult",
    "StateMachine",
    "UpdateStateMachineAliasResult",
    "UpdateStateMachineResult",
    "ValidateStateMachineDefinitionResult",
    "create_activity",
    "create_state_machine",
    "create_state_machine_alias",
    "delete_activity",
    "delete_state_machine",
    "delete_state_machine_alias",
    "delete_state_machine_version",
    "describe_activity",
    "describe_execution",
    "describe_map_run",
    "describe_state_machine",
    "describe_state_machine_alias",
    "describe_state_machine_for_execution",
    "get_activity_task",
    "get_execution_history",
    "list_activities",
    "list_executions",
    "list_map_runs",
    "list_state_machine_aliases",
    "list_state_machine_versions",
    "list_state_machines",
    "list_tags_for_resource",
    "publish_state_machine_version",
    "redrive_execution",
    "run_and_wait",
    "run_state",
    "send_task_failure",
    "send_task_heartbeat",
    "send_task_success",
    "start_execution",
    "start_sync_execution",
    "stop_execution",
    "tag_resource",
    "untag_resource",
    "update_map_run",
    "update_state_machine",
    "update_state_machine_alias",
    "validate_state_machine_definition",
    "wait_for_execution",
]

_TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class SFNExecution(BaseModel):
    """A Step Functions state machine execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str
    state_machine_arn: str
    name: str
    status: str
    start_date: datetime | None = None
    stop_date: datetime | None = None
    input: dict | str | None = None
    output: dict | str | None = None
    error: str | None = None
    cause: str | None = None

    @property
    def succeeded(self) -> bool:
        """``True`` if the execution completed successfully."""
        return self.status == "SUCCEEDED"

    @property
    def finished(self) -> bool:
        """``True`` if the execution reached a terminal state."""
        return self.status in _TERMINAL_STATUSES


class StateMachine(BaseModel):
    """Metadata for a Step Functions state machine."""

    model_config = ConfigDict(frozen=True)

    state_machine_arn: str
    name: str
    type: str
    status: str
    creation_date: datetime | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def start_execution(
    state_machine_arn: str,
    input_data: dict[str, Any] | None = None,
    name: str | None = None,
    region_name: str | None = None,
) -> SFNExecution:
    """Start a new Step Functions state machine execution.

    Args:
        state_machine_arn: ARN of the state machine to execute.
        input_data: Input payload as a dict.  ``None`` sends ``{}``.
        name: Optional unique execution name.  If omitted, AWS generates one.
        region_name: AWS region override.

    Returns:
        An :class:`SFNExecution` with the new execution's ARN and start time.

    Raises:
        RuntimeError: If the start request fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {
        "stateMachineArn": state_machine_arn,
        "input": json.dumps(input_data or {}),
    }
    if name:
        kwargs["name"] = name
    try:
        resp = client.start_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start execution for {state_machine_arn!r}") from exc
    return SFNExecution(
        execution_arn=resp["executionArn"],
        state_machine_arn=state_machine_arn,
        name=resp["executionArn"].split(":")[-1],
        status="RUNNING",
        start_date=resp.get("startDate"),
    )


def describe_execution(
    execution_arn: str,
    region_name: str | None = None,
) -> SFNExecution:
    """Describe the current state of a Step Functions execution.

    Args:
        execution_arn: ARN of the execution to describe.
        region_name: AWS region override.

    Returns:
        An :class:`SFNExecution` with current status and I/O.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    try:
        resp = client.describe_execution(executionArn=execution_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_execution failed for {execution_arn!r}") from exc
    return _parse_execution(resp)


def stop_execution(
    execution_arn: str,
    error: str = "",
    cause: str = "",
    region_name: str | None = None,
) -> None:
    """Stop a running Step Functions execution.

    Args:
        execution_arn: ARN of the execution to stop.
        error: Error code to record (optional).
        cause: Human-readable cause (optional).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the stop request fails.
    """
    client = get_client("stepfunctions", region_name)
    try:
        client.stop_execution(executionArn=execution_arn, error=error, cause=cause)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_execution failed for {execution_arn!r}") from exc


def list_executions(
    state_machine_arn: str,
    status_filter: str | None = None,
    region_name: str | None = None,
) -> list[SFNExecution]:
    """List executions for a state machine.

    Args:
        state_machine_arn: ARN of the state machine.
        status_filter: Optional status filter: ``"RUNNING"``,
            ``"SUCCEEDED"``, ``"FAILED"``, ``"TIMED_OUT"``, ``"ABORTED"``.
        region_name: AWS region override.

    Returns:
        A list of :class:`SFNExecution` summaries (no I/O fields).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {"stateMachineArn": state_machine_arn}
    if status_filter:
        kwargs["statusFilter"] = status_filter

    executions: list[SFNExecution] = []
    try:
        paginator = client.get_paginator("list_executions")
        for page in paginator.paginate(**kwargs):
            for ex in page.get("executions", []):
                executions.append(
                    SFNExecution(
                        execution_arn=ex["executionArn"],
                        state_machine_arn=ex["stateMachineArn"],
                        name=ex["name"],
                        status=ex["status"],
                        start_date=ex.get("startDate"),
                        stop_date=ex.get("stopDate"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_executions failed") from exc
    return executions


def wait_for_execution(
    execution_arn: str,
    poll_interval: float = 5.0,
    timeout: float = 600.0,
    region_name: str | None = None,
) -> SFNExecution:
    """Poll until a Step Functions execution reaches a terminal state.

    Args:
        execution_arn: ARN of the execution to wait for.
        poll_interval: Seconds between status checks (default ``5``).
        timeout: Maximum seconds to wait before raising (default ``600``).
        region_name: AWS region override.

    Returns:
        The final :class:`SFNExecution` (SUCCEEDED, FAILED, etc.).

    Raises:
        TimeoutError: If the execution does not finish within *timeout*.
        RuntimeError: If the describe call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        execution = describe_execution(execution_arn, region_name=region_name)
        if execution.finished:
            return execution
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Execution {execution_arn!r} did not finish within {timeout}s")
        time.sleep(poll_interval)


def list_state_machines(
    region_name: str | None = None,
) -> list[StateMachine]:
    """List all Step Functions state machines in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`StateMachine` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    machines: list[StateMachine] = []
    try:
        paginator = client.get_paginator("list_state_machines")
        for page in paginator.paginate():
            for sm in page.get("stateMachines", []):
                machines.append(
                    StateMachine(
                        state_machine_arn=sm["stateMachineArn"],
                        name=sm["name"],
                        type=sm.get("type", "STANDARD"),
                        status=sm.get("status", "ACTIVE"),
                        creation_date=sm.get("creationDate"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_state_machines failed") from exc
    return machines


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_execution(resp: dict) -> SFNExecution:
    def _try_json(s: str | None) -> dict | str | None:
        if not s:
            return None
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s

    return SFNExecution(
        execution_arn=resp["executionArn"],
        state_machine_arn=resp["stateMachineArn"],
        name=resp["name"],
        status=resp["status"],
        start_date=resp.get("startDate"),
        stop_date=resp.get("stopDate"),
        input=_try_json(resp.get("input")),
        output=_try_json(resp.get("output")),
        error=resp.get("error"),
        cause=resp.get("cause"),
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def run_and_wait(
    state_machine_arn: str,
    input_data: dict[str, Any] | None = None,
    name: str | None = None,
    timeout: float = 600.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> SFNExecution:
    """Start a Step Functions execution and wait until it reaches a terminal state.

    Combines :func:`start_execution` and :func:`wait_for_execution`.

    Args:
        state_machine_arn: ARN of the state machine.
        input_data: Input payload as a dict.
        name: Optional unique execution name.
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between status checks.
        region_name: AWS region override.

    Returns:
        The final :class:`SFNExecution`.

    Raises:
        RuntimeError: If the start fails or the execution ends in a non-SUCCESS
            terminal state and you want to inspect the result.
        TimeoutError: If the execution does not finish within *timeout*.
    """
    execution = start_execution(
        state_machine_arn, input_data=input_data, name=name, region_name=region_name
    )
    return wait_for_execution(
        execution.execution_arn,
        poll_interval=poll_interval,
        timeout=timeout,
        region_name=region_name,
    )


def get_execution_history(
    execution_arn: str,
    include_execution_data: bool = True,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Retrieve the full event history of a Step Functions execution.

    Useful for debugging failures — the history shows every state transition,
    retry, and error.

    Args:
        execution_arn: ARN of the execution.
        include_execution_data: Include input/output data in each event.
        region_name: AWS region override.

    Returns:
        A list of event dicts in chronological order.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    events: list[dict[str, Any]] = []
    kwargs: dict[str, Any] = {
        "executionArn": execution_arn,
        "includeExecutionData": include_execution_data,
    }
    try:
        paginator = client.get_paginator("get_execution_history")
        for page in paginator.paginate(**kwargs):
            events.extend(page.get("events", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_execution_history failed for {execution_arn!r}") from exc
    return events


class CreateActivityResult(BaseModel):
    """Result of create_activity."""

    model_config = ConfigDict(frozen=True)

    activity_arn: str | None = None
    creation_date: str | None = None


class CreateStateMachineResult(BaseModel):
    """Result of create_state_machine."""

    model_config = ConfigDict(frozen=True)

    state_machine_arn: str | None = None
    creation_date: str | None = None
    state_machine_version_arn: str | None = None


class CreateStateMachineAliasResult(BaseModel):
    """Result of create_state_machine_alias."""

    model_config = ConfigDict(frozen=True)

    state_machine_alias_arn: str | None = None
    creation_date: str | None = None


class DescribeActivityResult(BaseModel):
    """Result of describe_activity."""

    model_config = ConfigDict(frozen=True)

    activity_arn: str | None = None
    name: str | None = None
    creation_date: str | None = None
    encryption_configuration: dict[str, Any] | None = None


class DescribeMapRunResult(BaseModel):
    """Result of describe_map_run."""

    model_config = ConfigDict(frozen=True)

    map_run_arn: str | None = None
    execution_arn: str | None = None
    status: str | None = None
    start_date: str | None = None
    stop_date: str | None = None
    max_concurrency: int | None = None
    tolerated_failure_percentage: float | None = None
    tolerated_failure_count: int | None = None
    item_counts: dict[str, Any] | None = None
    execution_counts: dict[str, Any] | None = None
    redrive_count: int | None = None
    redrive_date: str | None = None


class DescribeStateMachineResult(BaseModel):
    """Result of describe_state_machine."""

    model_config = ConfigDict(frozen=True)

    state_machine_arn: str | None = None
    name: str | None = None
    status: str | None = None
    definition: str | None = None
    role_arn: str | None = None
    type_value: str | None = None
    creation_date: str | None = None
    logging_configuration: dict[str, Any] | None = None
    tracing_configuration: dict[str, Any] | None = None
    label: str | None = None
    revision_id: str | None = None
    description: str | None = None
    encryption_configuration: dict[str, Any] | None = None
    variable_references: dict[str, Any] | None = None


class DescribeStateMachineAliasResult(BaseModel):
    """Result of describe_state_machine_alias."""

    model_config = ConfigDict(frozen=True)

    state_machine_alias_arn: str | None = None
    name: str | None = None
    description: str | None = None
    routing_configuration: list[dict[str, Any]] | None = None
    creation_date: str | None = None
    update_date: str | None = None


class DescribeStateMachineForExecutionResult(BaseModel):
    """Result of describe_state_machine_for_execution."""

    model_config = ConfigDict(frozen=True)

    state_machine_arn: str | None = None
    name: str | None = None
    definition: str | None = None
    role_arn: str | None = None
    update_date: str | None = None
    logging_configuration: dict[str, Any] | None = None
    tracing_configuration: dict[str, Any] | None = None
    map_run_arn: str | None = None
    label: str | None = None
    revision_id: str | None = None
    encryption_configuration: dict[str, Any] | None = None
    variable_references: dict[str, Any] | None = None


class GetActivityTaskResult(BaseModel):
    """Result of get_activity_task."""

    model_config = ConfigDict(frozen=True)

    task_token: str | None = None
    input: str | None = None


class ListActivitiesResult(BaseModel):
    """Result of list_activities."""

    model_config = ConfigDict(frozen=True)

    activities: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListMapRunsResult(BaseModel):
    """Result of list_map_runs."""

    model_config = ConfigDict(frozen=True)

    map_runs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStateMachineAliasesResult(BaseModel):
    """Result of list_state_machine_aliases."""

    model_config = ConfigDict(frozen=True)

    state_machine_aliases: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStateMachineVersionsResult(BaseModel):
    """Result of list_state_machine_versions."""

    model_config = ConfigDict(frozen=True)

    state_machine_versions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class PublishStateMachineVersionResult(BaseModel):
    """Result of publish_state_machine_version."""

    model_config = ConfigDict(frozen=True)

    creation_date: str | None = None
    state_machine_version_arn: str | None = None


class RedriveExecutionResult(BaseModel):
    """Result of redrive_execution."""

    model_config = ConfigDict(frozen=True)

    redrive_date: str | None = None


class RunStateResult(BaseModel):
    """Result of run_state."""

    model_config = ConfigDict(frozen=True)

    output: str | None = None
    error: str | None = None
    cause: str | None = None
    inspection_data: dict[str, Any] | None = None
    next_state: str | None = None
    status: str | None = None


class StartSyncExecutionResult(BaseModel):
    """Result of start_sync_execution."""

    model_config = ConfigDict(frozen=True)

    execution_arn: str | None = None
    state_machine_arn: str | None = None
    name: str | None = None
    start_date: str | None = None
    stop_date: str | None = None
    status: str | None = None
    error: str | None = None
    cause: str | None = None
    input: str | None = None
    input_details: dict[str, Any] | None = None
    output: str | None = None
    output_details: dict[str, Any] | None = None
    trace_header: str | None = None
    billing_details: dict[str, Any] | None = None


class UpdateStateMachineResult(BaseModel):
    """Result of update_state_machine."""

    model_config = ConfigDict(frozen=True)

    update_date: str | None = None
    revision_id: str | None = None
    state_machine_version_arn: str | None = None


class UpdateStateMachineAliasResult(BaseModel):
    """Result of update_state_machine_alias."""

    model_config = ConfigDict(frozen=True)

    update_date: str | None = None


class ValidateStateMachineDefinitionResult(BaseModel):
    """Result of validate_state_machine_definition."""

    model_config = ConfigDict(frozen=True)

    result: str | None = None
    diagnostics: list[dict[str, Any]] | None = None
    truncated: bool | None = None


def create_activity(
    name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateActivityResult:
    """Create activity.

    Args:
        name: Name.
        tags: Tags.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    try:
        resp = client.create_activity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create activity") from exc
    return CreateActivityResult(
        activity_arn=resp.get("activityArn"),
        creation_date=resp.get("creationDate"),
    )


def create_state_machine(
    name: str,
    definition: str,
    role_arn: str,
    *,
    type_value: str | None = None,
    logging_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    tracing_configuration: dict[str, Any] | None = None,
    publish: bool | None = None,
    version_description: str | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateStateMachineResult:
    """Create state machine.

    Args:
        name: Name.
        definition: Definition.
        role_arn: Role arn.
        type_value: Type value.
        logging_configuration: Logging configuration.
        tags: Tags.
        tracing_configuration: Tracing configuration.
        publish: Publish.
        version_description: Version description.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["definition"] = definition
    kwargs["roleArn"] = role_arn
    if type_value is not None:
        kwargs["type"] = type_value
    if logging_configuration is not None:
        kwargs["loggingConfiguration"] = logging_configuration
    if tags is not None:
        kwargs["tags"] = tags
    if tracing_configuration is not None:
        kwargs["tracingConfiguration"] = tracing_configuration
    if publish is not None:
        kwargs["publish"] = publish
    if version_description is not None:
        kwargs["versionDescription"] = version_description
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    try:
        resp = client.create_state_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create state machine") from exc
    return CreateStateMachineResult(
        state_machine_arn=resp.get("stateMachineArn"),
        creation_date=resp.get("creationDate"),
        state_machine_version_arn=resp.get("stateMachineVersionArn"),
    )


def create_state_machine_alias(
    name: str,
    routing_configuration: list[dict[str, Any]],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateStateMachineAliasResult:
    """Create state machine alias.

    Args:
        name: Name.
        routing_configuration: Routing configuration.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["routingConfiguration"] = routing_configuration
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_state_machine_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create state machine alias") from exc
    return CreateStateMachineAliasResult(
        state_machine_alias_arn=resp.get("stateMachineAliasArn"),
        creation_date=resp.get("creationDate"),
    )


def delete_activity(
    activity_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete activity.

    Args:
        activity_arn: Activity arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["activityArn"] = activity_arn
    try:
        client.delete_activity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete activity") from exc
    return None


def delete_state_machine(
    state_machine_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete state machine.

    Args:
        state_machine_arn: State machine arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    try:
        client.delete_state_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete state machine") from exc
    return None


def delete_state_machine_alias(
    state_machine_alias_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete state machine alias.

    Args:
        state_machine_alias_arn: State machine alias arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineAliasArn"] = state_machine_alias_arn
    try:
        client.delete_state_machine_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete state machine alias") from exc
    return None


def delete_state_machine_version(
    state_machine_version_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete state machine version.

    Args:
        state_machine_version_arn: State machine version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineVersionArn"] = state_machine_version_arn
    try:
        client.delete_state_machine_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete state machine version") from exc
    return None


def describe_activity(
    activity_arn: str,
    region_name: str | None = None,
) -> DescribeActivityResult:
    """Describe activity.

    Args:
        activity_arn: Activity arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["activityArn"] = activity_arn
    try:
        resp = client.describe_activity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe activity") from exc
    return DescribeActivityResult(
        activity_arn=resp.get("activityArn"),
        name=resp.get("name"),
        creation_date=resp.get("creationDate"),
        encryption_configuration=resp.get("encryptionConfiguration"),
    )


def describe_map_run(
    map_run_arn: str,
    region_name: str | None = None,
) -> DescribeMapRunResult:
    """Describe map run.

    Args:
        map_run_arn: Map run arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["mapRunArn"] = map_run_arn
    try:
        resp = client.describe_map_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe map run") from exc
    return DescribeMapRunResult(
        map_run_arn=resp.get("mapRunArn"),
        execution_arn=resp.get("executionArn"),
        status=resp.get("status"),
        start_date=resp.get("startDate"),
        stop_date=resp.get("stopDate"),
        max_concurrency=resp.get("maxConcurrency"),
        tolerated_failure_percentage=resp.get("toleratedFailurePercentage"),
        tolerated_failure_count=resp.get("toleratedFailureCount"),
        item_counts=resp.get("itemCounts"),
        execution_counts=resp.get("executionCounts"),
        redrive_count=resp.get("redriveCount"),
        redrive_date=resp.get("redriveDate"),
    )


def describe_state_machine(
    state_machine_arn: str,
    *,
    included_data: str | None = None,
    region_name: str | None = None,
) -> DescribeStateMachineResult:
    """Describe state machine.

    Args:
        state_machine_arn: State machine arn.
        included_data: Included data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if included_data is not None:
        kwargs["includedData"] = included_data
    try:
        resp = client.describe_state_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe state machine") from exc
    return DescribeStateMachineResult(
        state_machine_arn=resp.get("stateMachineArn"),
        name=resp.get("name"),
        status=resp.get("status"),
        definition=resp.get("definition"),
        role_arn=resp.get("roleArn"),
        type_value=resp.get("type"),
        creation_date=resp.get("creationDate"),
        logging_configuration=resp.get("loggingConfiguration"),
        tracing_configuration=resp.get("tracingConfiguration"),
        label=resp.get("label"),
        revision_id=resp.get("revisionId"),
        description=resp.get("description"),
        encryption_configuration=resp.get("encryptionConfiguration"),
        variable_references=resp.get("variableReferences"),
    )


def describe_state_machine_alias(
    state_machine_alias_arn: str,
    region_name: str | None = None,
) -> DescribeStateMachineAliasResult:
    """Describe state machine alias.

    Args:
        state_machine_alias_arn: State machine alias arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineAliasArn"] = state_machine_alias_arn
    try:
        resp = client.describe_state_machine_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe state machine alias") from exc
    return DescribeStateMachineAliasResult(
        state_machine_alias_arn=resp.get("stateMachineAliasArn"),
        name=resp.get("name"),
        description=resp.get("description"),
        routing_configuration=resp.get("routingConfiguration"),
        creation_date=resp.get("creationDate"),
        update_date=resp.get("updateDate"),
    )


def describe_state_machine_for_execution(
    execution_arn: str,
    *,
    included_data: str | None = None,
    region_name: str | None = None,
) -> DescribeStateMachineForExecutionResult:
    """Describe state machine for execution.

    Args:
        execution_arn: Execution arn.
        included_data: Included data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionArn"] = execution_arn
    if included_data is not None:
        kwargs["includedData"] = included_data
    try:
        resp = client.describe_state_machine_for_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe state machine for execution") from exc
    return DescribeStateMachineForExecutionResult(
        state_machine_arn=resp.get("stateMachineArn"),
        name=resp.get("name"),
        definition=resp.get("definition"),
        role_arn=resp.get("roleArn"),
        update_date=resp.get("updateDate"),
        logging_configuration=resp.get("loggingConfiguration"),
        tracing_configuration=resp.get("tracingConfiguration"),
        map_run_arn=resp.get("mapRunArn"),
        label=resp.get("label"),
        revision_id=resp.get("revisionId"),
        encryption_configuration=resp.get("encryptionConfiguration"),
        variable_references=resp.get("variableReferences"),
    )


def get_activity_task(
    activity_arn: str,
    *,
    worker_name: str | None = None,
    region_name: str | None = None,
) -> GetActivityTaskResult:
    """Get activity task.

    Args:
        activity_arn: Activity arn.
        worker_name: Worker name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["activityArn"] = activity_arn
    if worker_name is not None:
        kwargs["workerName"] = worker_name
    try:
        resp = client.get_activity_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get activity task") from exc
    return GetActivityTaskResult(
        task_token=resp.get("taskToken"),
        input=resp.get("input"),
    )


def list_activities(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListActivitiesResult:
    """List activities.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_activities(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list activities") from exc
    return ListActivitiesResult(
        activities=resp.get("activities"),
        next_token=resp.get("nextToken"),
    )


def list_map_runs(
    execution_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListMapRunsResult:
    """List map runs.

    Args:
        execution_arn: Execution arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionArn"] = execution_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_map_runs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list map runs") from exc
    return ListMapRunsResult(
        map_runs=resp.get("mapRuns"),
        next_token=resp.get("nextToken"),
    )


def list_state_machine_aliases(
    state_machine_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStateMachineAliasesResult:
    """List state machine aliases.

    Args:
        state_machine_arn: State machine arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_state_machine_aliases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list state machine aliases") from exc
    return ListStateMachineAliasesResult(
        state_machine_aliases=resp.get("stateMachineAliases"),
        next_token=resp.get("nextToken"),
    )


def list_state_machine_versions(
    state_machine_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStateMachineVersionsResult:
    """List state machine versions.

    Args:
        state_machine_arn: State machine arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_state_machine_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list state machine versions") from exc
    return ListStateMachineVersionsResult(
        state_machine_versions=resp.get("stateMachineVersions"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def publish_state_machine_version(
    state_machine_arn: str,
    *,
    revision_id: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> PublishStateMachineVersionResult:
    """Publish state machine version.

    Args:
        state_machine_arn: State machine arn.
        revision_id: Revision id.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if revision_id is not None:
        kwargs["revisionId"] = revision_id
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.publish_state_machine_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to publish state machine version") from exc
    return PublishStateMachineVersionResult(
        creation_date=resp.get("creationDate"),
        state_machine_version_arn=resp.get("stateMachineVersionArn"),
    )


def redrive_execution(
    execution_arn: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> RedriveExecutionResult:
    """Redrive execution.

    Args:
        execution_arn: Execution arn.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionArn"] = execution_arn
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.redrive_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to redrive execution") from exc
    return RedriveExecutionResult(
        redrive_date=resp.get("redriveDate"),
    )


def run_state(
    definition: str,
    *,
    role_arn: str | None = None,
    input: str | None = None,
    inspection_level: str | None = None,
    reveal_secrets: bool | None = None,
    variables: str | None = None,
    region_name: str | None = None,
) -> RunStateResult:
    """Run state.

    Args:
        definition: Definition.
        role_arn: Role arn.
        input: Input.
        inspection_level: Inspection level.
        reveal_secrets: Reveal secrets.
        variables: Variables.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["definition"] = definition
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if input is not None:
        kwargs["input"] = input
    if inspection_level is not None:
        kwargs["inspectionLevel"] = inspection_level
    if reveal_secrets is not None:
        kwargs["revealSecrets"] = reveal_secrets
    if variables is not None:
        kwargs["variables"] = variables
    try:
        resp = client.test_state(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run state") from exc
    return RunStateResult(
        output=resp.get("output"),
        error=resp.get("error"),
        cause=resp.get("cause"),
        inspection_data=resp.get("inspectionData"),
        next_state=resp.get("nextState"),
        status=resp.get("status"),
    )


def send_task_failure(
    task_token: str,
    *,
    error: str | None = None,
    cause: str | None = None,
    region_name: str | None = None,
) -> None:
    """Send task failure.

    Args:
        task_token: Task token.
        error: Error.
        cause: Cause.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskToken"] = task_token
    if error is not None:
        kwargs["error"] = error
    if cause is not None:
        kwargs["cause"] = cause
    try:
        client.send_task_failure(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send task failure") from exc
    return None


def send_task_heartbeat(
    task_token: str,
    region_name: str | None = None,
) -> None:
    """Send task heartbeat.

    Args:
        task_token: Task token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskToken"] = task_token
    try:
        client.send_task_heartbeat(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send task heartbeat") from exc
    return None


def send_task_success(
    task_token: str,
    output: str,
    region_name: str | None = None,
) -> None:
    """Send task success.

    Args:
        task_token: Task token.
        output: Output.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskToken"] = task_token
    kwargs["output"] = output
    try:
        client.send_task_success(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send task success") from exc
    return None


def start_sync_execution(
    state_machine_arn: str,
    *,
    name: str | None = None,
    input: str | None = None,
    trace_header: str | None = None,
    included_data: str | None = None,
    region_name: str | None = None,
) -> StartSyncExecutionResult:
    """Start sync execution.

    Args:
        state_machine_arn: State machine arn.
        name: Name.
        input: Input.
        trace_header: Trace header.
        included_data: Included data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if name is not None:
        kwargs["name"] = name
    if input is not None:
        kwargs["input"] = input
    if trace_header is not None:
        kwargs["traceHeader"] = trace_header
    if included_data is not None:
        kwargs["includedData"] = included_data
    try:
        resp = client.start_sync_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start sync execution") from exc
    return StartSyncExecutionResult(
        execution_arn=resp.get("executionArn"),
        state_machine_arn=resp.get("stateMachineArn"),
        name=resp.get("name"),
        start_date=resp.get("startDate"),
        stop_date=resp.get("stopDate"),
        status=resp.get("status"),
        error=resp.get("error"),
        cause=resp.get("cause"),
        input=resp.get("input"),
        input_details=resp.get("inputDetails"),
        output=resp.get("output"),
        output_details=resp.get("outputDetails"),
        trace_header=resp.get("traceHeader"),
        billing_details=resp.get("billingDetails"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_map_run(
    map_run_arn: str,
    *,
    max_concurrency: int | None = None,
    tolerated_failure_percentage: float | None = None,
    tolerated_failure_count: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update map run.

    Args:
        map_run_arn: Map run arn.
        max_concurrency: Max concurrency.
        tolerated_failure_percentage: Tolerated failure percentage.
        tolerated_failure_count: Tolerated failure count.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["mapRunArn"] = map_run_arn
    if max_concurrency is not None:
        kwargs["maxConcurrency"] = max_concurrency
    if tolerated_failure_percentage is not None:
        kwargs["toleratedFailurePercentage"] = tolerated_failure_percentage
    if tolerated_failure_count is not None:
        kwargs["toleratedFailureCount"] = tolerated_failure_count
    try:
        client.update_map_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update map run") from exc
    return None


def update_state_machine(
    state_machine_arn: str,
    *,
    definition: str | None = None,
    role_arn: str | None = None,
    logging_configuration: dict[str, Any] | None = None,
    tracing_configuration: dict[str, Any] | None = None,
    publish: bool | None = None,
    version_description: str | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateStateMachineResult:
    """Update state machine.

    Args:
        state_machine_arn: State machine arn.
        definition: Definition.
        role_arn: Role arn.
        logging_configuration: Logging configuration.
        tracing_configuration: Tracing configuration.
        publish: Publish.
        version_description: Version description.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineArn"] = state_machine_arn
    if definition is not None:
        kwargs["definition"] = definition
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if logging_configuration is not None:
        kwargs["loggingConfiguration"] = logging_configuration
    if tracing_configuration is not None:
        kwargs["tracingConfiguration"] = tracing_configuration
    if publish is not None:
        kwargs["publish"] = publish
    if version_description is not None:
        kwargs["versionDescription"] = version_description
    if encryption_configuration is not None:
        kwargs["encryptionConfiguration"] = encryption_configuration
    try:
        resp = client.update_state_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update state machine") from exc
    return UpdateStateMachineResult(
        update_date=resp.get("updateDate"),
        revision_id=resp.get("revisionId"),
        state_machine_version_arn=resp.get("stateMachineVersionArn"),
    )


def update_state_machine_alias(
    state_machine_alias_arn: str,
    *,
    description: str | None = None,
    routing_configuration: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateStateMachineAliasResult:
    """Update state machine alias.

    Args:
        state_machine_alias_arn: State machine alias arn.
        description: Description.
        routing_configuration: Routing configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["stateMachineAliasArn"] = state_machine_alias_arn
    if description is not None:
        kwargs["description"] = description
    if routing_configuration is not None:
        kwargs["routingConfiguration"] = routing_configuration
    try:
        resp = client.update_state_machine_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update state machine alias") from exc
    return UpdateStateMachineAliasResult(
        update_date=resp.get("updateDate"),
    )


def validate_state_machine_definition(
    definition: str,
    *,
    type_value: str | None = None,
    severity: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ValidateStateMachineDefinitionResult:
    """Validate state machine definition.

    Args:
        definition: Definition.
        type_value: Type value.
        severity: Severity.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("stepfunctions", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["definition"] = definition
    if type_value is not None:
        kwargs["type"] = type_value
    if severity is not None:
        kwargs["severity"] = severity
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.validate_state_machine_definition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to validate state machine definition") from exc
    return ValidateStateMachineDefinitionResult(
        result=resp.get("result"),
        diagnostics=resp.get("diagnostics"),
        truncated=resp.get("truncated"),
    )
