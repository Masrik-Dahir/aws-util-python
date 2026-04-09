"""aws_util.codepipeline --- AWS CodePipeline management utilities.

Provides high-level helpers for creating, managing, and monitoring
AWS CodePipeline pipelines, including polling-based waiters and a
composite ``run_pipeline_and_wait`` convenience function.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AcknowledgeJobResult",
    "AcknowledgeThirdPartyJobResult",
    "CreateCustomActionTypeResult",
    "GetActionTypeResult",
    "GetJobDetailsResult",
    "GetThirdPartyJobDetailsResult",
    "ListActionExecutionsResult",
    "ListActionTypesResult",
    "ListDeployActionExecutionTargetsResult",
    "ListRuleExecutionsResult",
    "ListRuleTypesResult",
    "ListTagsForResourceResult",
    "ListWebhooksResult",
    "PipelineExecutionResult",
    "PipelineResult",
    "PollForJobsResult",
    "PollForThirdPartyJobsResult",
    "PutActionRevisionResult",
    "PutWebhookResult",
    "RollbackStageResult",
    "StageStateResult",
    "acknowledge_job",
    "acknowledge_third_party_job",
    "create_custom_action_type",
    "create_pipeline",
    "delete_custom_action_type",
    "delete_pipeline",
    "delete_webhook",
    "deregister_webhook_with_third_party",
    "disable_stage_transition",
    "enable_stage_transition",
    "get_action_type",
    "get_job_details",
    "get_pipeline",
    "get_pipeline_execution",
    "get_pipeline_state",
    "get_third_party_job_details",
    "list_action_executions",
    "list_action_types",
    "list_deploy_action_execution_targets",
    "list_pipeline_executions",
    "list_pipelines",
    "list_rule_executions",
    "list_rule_types",
    "list_tags_for_resource",
    "list_webhooks",
    "override_stage_condition",
    "poll_for_jobs",
    "poll_for_third_party_jobs",
    "put_action_revision",
    "put_approval_result",
    "put_job_failure_result",
    "put_job_success_result",
    "put_third_party_job_failure_result",
    "put_third_party_job_success_result",
    "put_webhook",
    "register_webhook_with_third_party",
    "retry_stage_execution",
    "rollback_stage",
    "run_pipeline_and_wait",
    "start_pipeline_execution",
    "stop_pipeline_execution",
    "tag_resource",
    "untag_resource",
    "update_action_type",
    "update_pipeline",
    "wait_for_pipeline_execution",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class PipelineResult(BaseModel):
    """Metadata for a CodePipeline pipeline."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str | None = None
    role_arn: str = ""
    stages: list[dict[str, Any]] = Field(default_factory=list)
    version: int | None = None
    created: str | None = None
    updated: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class PipelineExecutionResult(BaseModel):
    """A CodePipeline pipeline execution."""

    model_config = ConfigDict(frozen=True)

    pipeline_name: str
    execution_id: str
    status: str
    artifact_revisions: list[dict[str, Any]] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class StageStateResult(BaseModel):
    """State information for a single pipeline stage."""

    model_config = ConfigDict(frozen=True)

    stage_name: str
    inbound_execution: dict[str, Any] | None = None
    action_states: list[dict[str, Any]] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_pipeline(resp: dict[str, Any]) -> PipelineResult:
    """Build a :class:`PipelineResult` from an AWS response."""
    pipeline = resp.get("pipeline", resp)
    metadata = resp.get("metadata", {})
    return PipelineResult(
        name=pipeline.get("name", ""),
        arn=metadata.get("pipelineArn") or pipeline.get("pipelineArn"),
        role_arn=pipeline.get("roleArn", ""),
        stages=pipeline.get("stages", []),
        version=pipeline.get("version"),
        created=str(metadata["created"]) if "created" in metadata else None,
        updated=str(metadata["updated"]) if "updated" in metadata else None,
        extra={
            k: v
            for k, v in pipeline.items()
            if k not in {"name", "roleArn", "stages", "version", "pipelineArn"}
        },
    )


def _parse_execution(
    resp: dict[str, Any],
    pipeline_name: str = "",
) -> PipelineExecutionResult:
    """Build a :class:`PipelineExecutionResult` from an AWS response."""
    pe = resp.get("pipelineExecution", resp)
    return PipelineExecutionResult(
        pipeline_name=pe.get("pipelineName", pipeline_name),
        execution_id=pe.get("pipelineExecutionId", ""),
        status=pe.get("status", ""),
        artifact_revisions=pe.get("artifactRevisions", []),
        extra={
            k: v
            for k, v in pe.items()
            if k
            not in {
                "pipelineName",
                "pipelineExecutionId",
                "status",
                "artifactRevisions",
            }
        },
    )


# ---------------------------------------------------------------------------
# Pipeline CRUD
# ---------------------------------------------------------------------------


def create_pipeline(
    name: str,
    *,
    role_arn: str,
    stages: list[dict[str, Any]],
    artifact_store: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PipelineResult:
    """Create a new CodePipeline pipeline.

    Args:
        name: Pipeline name.
        role_arn: IAM role ARN for the pipeline.
        stages: List of stage definitions (each a dict with ``name`` and
            ``actions``).
        artifact_store: Optional artifact store configuration (dict with
            ``type`` and ``location``).
        region_name: AWS region override.

    Returns:
        A :class:`PipelineResult` describing the created pipeline.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    pipeline_def: dict[str, Any] = {
        "name": name,
        "roleArn": role_arn,
        "stages": stages,
    }
    if artifact_store is not None:
        pipeline_def["artifactStore"] = artifact_store
    try:
        resp = client.create_pipeline(pipeline=pipeline_def)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_pipeline failed for {name!r}") from exc
    return _parse_pipeline(resp)


def get_pipeline(
    name: str,
    *,
    region_name: str | None = None,
) -> PipelineResult:
    """Retrieve a CodePipeline pipeline definition.

    Args:
        name: Pipeline name.
        region_name: AWS region override.

    Returns:
        A :class:`PipelineResult` with the pipeline configuration.

    Raises:
        RuntimeError: If the pipeline does not exist or the call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.get_pipeline(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_pipeline failed for {name!r}") from exc
    return _parse_pipeline(resp)


def list_pipelines(
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List all CodePipeline pipelines in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of dicts with ``name``, ``version``, ``created``, and
        ``updated`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    pipelines: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("list_pipelines")
        for page in paginator.paginate():
            for p in page.get("pipelines", []):
                pipelines.append(
                    {
                        "name": p.get("name", ""),
                        "version": p.get("version"),
                        "created": str(p["created"]) if "created" in p else None,
                        "updated": str(p["updated"]) if "updated" in p else None,
                    }
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_pipelines failed") from exc
    return pipelines


def update_pipeline(
    *,
    pipeline: dict[str, Any],
    region_name: str | None = None,
) -> PipelineResult:
    """Update an existing CodePipeline pipeline.

    Args:
        pipeline: Full pipeline definition dict (as returned by
            ``get_pipeline`` or constructed manually).
        region_name: AWS region override.

    Returns:
        A :class:`PipelineResult` with the updated pipeline.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.update_pipeline(pipeline=pipeline)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"update_pipeline failed for {pipeline.get('name', '?')!r}",
        ) from exc
    return _parse_pipeline(resp)


def delete_pipeline(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CodePipeline pipeline.

    Args:
        name: Pipeline name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        client.delete_pipeline(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_pipeline failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Execution management
# ---------------------------------------------------------------------------


def start_pipeline_execution(
    name: str,
    *,
    region_name: str | None = None,
) -> str:
    """Start a new execution of a CodePipeline pipeline.

    Args:
        name: Pipeline name.
        region_name: AWS region override.

    Returns:
        The pipeline execution ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.start_pipeline_execution(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_pipeline_execution failed for {name!r}") from exc
    return resp["pipelineExecutionId"]


def get_pipeline_execution(
    name: str,
    execution_id: str,
    *,
    region_name: str | None = None,
) -> PipelineExecutionResult:
    """Describe a specific pipeline execution.

    Args:
        name: Pipeline name.
        execution_id: The execution ID to describe.
        region_name: AWS region override.

    Returns:
        A :class:`PipelineExecutionResult` with the execution details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.get_pipeline_execution(
            pipelineName=name,
            pipelineExecutionId=execution_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_pipeline_execution failed for {name!r}/{execution_id!r}",
        ) from exc
    return _parse_execution(resp, pipeline_name=name)


def list_pipeline_executions(
    name: str,
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[PipelineExecutionResult]:
    """List recent executions of a pipeline.

    Args:
        name: Pipeline name.
        max_results: Maximum number of results to return.  ``None``
            retrieves all available executions via pagination.
        region_name: AWS region override.

    Returns:
        A list of :class:`PipelineExecutionResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    executions: list[PipelineExecutionResult] = []
    try:
        paginator = client.get_paginator("list_pipeline_executions")
        kwargs: dict[str, Any] = {"pipelineName": name}
        if max_results is not None:
            kwargs["maxResults"] = max_results
        for page in paginator.paginate(**kwargs):
            for ex in page.get("pipelineExecutionSummaries", []):
                executions.append(
                    PipelineExecutionResult(
                        pipeline_name=name,
                        execution_id=ex.get("pipelineExecutionId", ""),
                        status=ex.get("status", ""),
                        artifact_revisions=ex.get("sourceRevisions", []),
                        extra={
                            k: v
                            for k, v in ex.items()
                            if k
                            not in {
                                "pipelineExecutionId",
                                "status",
                                "sourceRevisions",
                            }
                        },
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_pipeline_executions failed for {name!r}") from exc
    return executions


def stop_pipeline_execution(
    name: str,
    execution_id: str,
    *,
    reason: str | None = None,
    abandon: bool = False,
    region_name: str | None = None,
) -> None:
    """Stop a running pipeline execution.

    Args:
        name: Pipeline name.
        execution_id: Execution ID to stop.
        reason: Optional human-readable reason for stopping.
        abandon: If ``True``, abandon the execution instead of stopping
            it gracefully.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {
        "pipelineName": name,
        "pipelineExecutionId": execution_id,
        "abandon": abandon,
    }
    if reason is not None:
        kwargs["reason"] = reason
    try:
        client.stop_pipeline_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"stop_pipeline_execution failed for {name!r}/{execution_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Stage management
# ---------------------------------------------------------------------------


def get_pipeline_state(
    name: str,
    *,
    region_name: str | None = None,
) -> list[StageStateResult]:
    """Get the current state of all stages in a pipeline.

    Args:
        name: Pipeline name.
        region_name: AWS region override.

    Returns:
        A list of :class:`StageStateResult` objects, one per stage.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.get_pipeline_state(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_pipeline_state failed for {name!r}") from exc
    results: list[StageStateResult] = []
    for stage in resp.get("stageStates", []):
        results.append(
            StageStateResult(
                stage_name=stage.get("stageName", ""),
                inbound_execution=stage.get(
                    "inboundExecution",
                    stage.get("inboundTransitionState"),
                ),
                action_states=stage.get("actionStates", []),
                extra={
                    k: v
                    for k, v in stage.items()
                    if k
                    not in {
                        "stageName",
                        "inboundExecution",
                        "inboundTransitionState",
                        "actionStates",
                    }
                },
            )
        )
    return results


def retry_stage_execution(
    name: str,
    stage_name: str,
    execution_id: str,
    *,
    retry_mode: str = "FAILED_ACTIONS",
    region_name: str | None = None,
) -> str:
    """Retry a failed stage execution.

    Args:
        name: Pipeline name.
        stage_name: Name of the stage to retry.
        execution_id: The execution ID to retry.
        retry_mode: Retry mode (``"FAILED_ACTIONS"`` or
            ``"ALL_ACTIONS"``).
        region_name: AWS region override.

    Returns:
        The new pipeline execution ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        resp = client.retry_stage_execution(
            pipelineName=name,
            stageName=stage_name,
            pipelineExecutionId=execution_id,
            retryMode=retry_mode,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"retry_stage_execution failed for {name!r}/{stage_name!r}",
        ) from exc
    return resp["pipelineExecutionId"]


def enable_stage_transition(
    name: str,
    stage_name: str,
    *,
    transition_type: str = "Inbound",
    region_name: str | None = None,
) -> None:
    """Enable a stage transition in a pipeline.

    Args:
        name: Pipeline name.
        stage_name: Name of the stage.
        transition_type: ``"Inbound"`` or ``"Outbound"``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        client.enable_stage_transition(
            pipelineName=name,
            stageName=stage_name,
            transitionType=transition_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"enable_stage_transition failed for {name!r}/{stage_name!r}",
        ) from exc


def disable_stage_transition(
    name: str,
    stage_name: str,
    *,
    transition_type: str = "Inbound",
    reason: str = "",
    region_name: str | None = None,
) -> None:
    """Disable a stage transition in a pipeline.

    Args:
        name: Pipeline name.
        stage_name: Name of the stage.
        transition_type: ``"Inbound"`` or ``"Outbound"``.
        reason: Reason for disabling the transition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        client.disable_stage_transition(
            pipelineName=name,
            stageName=stage_name,
            transitionType=transition_type,
            reason=reason,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"disable_stage_transition failed for {name!r}/{stage_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Approval
# ---------------------------------------------------------------------------


def put_approval_result(
    name: str,
    stage_name: str,
    action_name: str,
    *,
    result: dict[str, str],
    token: str,
    region_name: str | None = None,
) -> None:
    """Submit an approval result for a manual approval action.

    Args:
        name: Pipeline name.
        stage_name: Name of the stage containing the approval action.
        action_name: Name of the approval action.
        result: Dict with ``summary`` and ``status`` (``"Approved"`` or
            ``"Rejected"``).
        token: The approval token from the action execution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    try:
        client.put_approval_result(
            pipelineName=name,
            stageName=stage_name,
            actionName=action_name,
            result=result,
            token=token,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"put_approval_result failed for {name!r}/{stage_name!r}/{action_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


_TERMINAL_STATUSES = frozenset({"Succeeded", "Failed", "Stopped", "Superseded", "Cancelled"})


def wait_for_pipeline_execution(
    name: str,
    execution_id: str,
    *,
    target_statuses: tuple[str, ...] = ("Succeeded",),
    failure_statuses: tuple[str, ...] = ("Failed", "Stopped"),
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> PipelineExecutionResult:
    """Poll until a pipeline execution reaches a target or failure status.

    Args:
        name: Pipeline name.
        execution_id: The execution ID to monitor.
        target_statuses: Statuses considered successful.
        failure_statuses: Statuses considered failed (raises immediately).
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between polls (default ``15``).
        region_name: AWS region override.

    Returns:
        A :class:`PipelineExecutionResult` in one of the *target_statuses*.

    Raises:
        AwsTimeoutError: If the execution does not reach a target status
            within *timeout*.
        RuntimeError: If the execution enters a *failure_statuses* status
            or the describe call fails.
    """
    deadline = time.monotonic() + timeout
    while True:
        execution = get_pipeline_execution(name, execution_id, region_name=region_name)
        if execution.status in target_statuses:
            return execution
        if execution.status in failure_statuses:
            raise RuntimeError(
                f"Pipeline {name!r} execution {execution_id!r} "
                f"entered failure status: {execution.status}"
            )
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Pipeline {name!r} execution {execution_id!r} "
                f"did not reach {target_statuses} within {timeout}s "
                f"(last status: {execution.status})"
            )
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Composite utilities
# ---------------------------------------------------------------------------


def run_pipeline_and_wait(
    name: str,
    *,
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> PipelineExecutionResult:
    """Start a pipeline execution and wait for it to complete.

    Combines :func:`start_pipeline_execution` and
    :func:`wait_for_pipeline_execution`.

    Args:
        name: Pipeline name.
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between polls (default ``15``).
        region_name: AWS region override.

    Returns:
        A :class:`PipelineExecutionResult` for the completed execution.

    Raises:
        AwsTimeoutError: If the execution does not complete within
            *timeout*.
        RuntimeError: If the start or describe call fails, or the
            execution enters a failure status.
    """
    execution_id = start_pipeline_execution(name, region_name=region_name)
    return wait_for_pipeline_execution(
        name,
        execution_id,
        timeout=timeout,
        poll_interval=poll_interval,
        region_name=region_name,
    )


class AcknowledgeJobResult(BaseModel):
    """Result of acknowledge_job."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class AcknowledgeThirdPartyJobResult(BaseModel):
    """Result of acknowledge_third_party_job."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None


class CreateCustomActionTypeResult(BaseModel):
    """Result of create_custom_action_type."""

    model_config = ConfigDict(frozen=True)

    action_type: dict[str, Any] | None = None
    tags: list[dict[str, Any]] | None = None


class GetActionTypeResult(BaseModel):
    """Result of get_action_type."""

    model_config = ConfigDict(frozen=True)

    action_type: dict[str, Any] | None = None


class GetJobDetailsResult(BaseModel):
    """Result of get_job_details."""

    model_config = ConfigDict(frozen=True)

    job_details: dict[str, Any] | None = None


class GetThirdPartyJobDetailsResult(BaseModel):
    """Result of get_third_party_job_details."""

    model_config = ConfigDict(frozen=True)

    job_details: dict[str, Any] | None = None


class ListActionExecutionsResult(BaseModel):
    """Result of list_action_executions."""

    model_config = ConfigDict(frozen=True)

    action_execution_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListActionTypesResult(BaseModel):
    """Result of list_action_types."""

    model_config = ConfigDict(frozen=True)

    action_types: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDeployActionExecutionTargetsResult(BaseModel):
    """Result of list_deploy_action_execution_targets."""

    model_config = ConfigDict(frozen=True)

    targets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRuleExecutionsResult(BaseModel):
    """Result of list_rule_executions."""

    model_config = ConfigDict(frozen=True)

    rule_execution_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRuleTypesResult(BaseModel):
    """Result of list_rule_types."""

    model_config = ConfigDict(frozen=True)

    rule_types: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListWebhooksResult(BaseModel):
    """Result of list_webhooks."""

    model_config = ConfigDict(frozen=True)

    webhooks: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PollForJobsResult(BaseModel):
    """Result of poll_for_jobs."""

    model_config = ConfigDict(frozen=True)

    jobs: list[dict[str, Any]] | None = None


class PollForThirdPartyJobsResult(BaseModel):
    """Result of poll_for_third_party_jobs."""

    model_config = ConfigDict(frozen=True)

    jobs: list[dict[str, Any]] | None = None


class PutActionRevisionResult(BaseModel):
    """Result of put_action_revision."""

    model_config = ConfigDict(frozen=True)

    new_revision: bool | None = None
    pipeline_execution_id: str | None = None


class PutWebhookResult(BaseModel):
    """Result of put_webhook."""

    model_config = ConfigDict(frozen=True)

    webhook: dict[str, Any] | None = None


class RollbackStageResult(BaseModel):
    """Result of rollback_stage."""

    model_config = ConfigDict(frozen=True)

    pipeline_execution_id: str | None = None


def acknowledge_job(
    job_id: str,
    nonce: str,
    region_name: str | None = None,
) -> AcknowledgeJobResult:
    """Acknowledge job.

    Args:
        job_id: Job id.
        nonce: Nonce.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["nonce"] = nonce
    try:
        resp = client.acknowledge_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to acknowledge job") from exc
    return AcknowledgeJobResult(
        status=resp.get("status"),
    )


def acknowledge_third_party_job(
    job_id: str,
    nonce: str,
    client_token: str,
    region_name: str | None = None,
) -> AcknowledgeThirdPartyJobResult:
    """Acknowledge third party job.

    Args:
        job_id: Job id.
        nonce: Nonce.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["nonce"] = nonce
    kwargs["clientToken"] = client_token
    try:
        resp = client.acknowledge_third_party_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to acknowledge third party job") from exc
    return AcknowledgeThirdPartyJobResult(
        status=resp.get("status"),
    )


def create_custom_action_type(
    category: str,
    provider: str,
    version: str,
    input_artifact_details: dict[str, Any],
    output_artifact_details: dict[str, Any],
    *,
    settings: dict[str, Any] | None = None,
    configuration_properties: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCustomActionTypeResult:
    """Create custom action type.

    Args:
        category: Category.
        provider: Provider.
        version: Version.
        input_artifact_details: Input artifact details.
        output_artifact_details: Output artifact details.
        settings: Settings.
        configuration_properties: Configuration properties.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["category"] = category
    kwargs["provider"] = provider
    kwargs["version"] = version
    kwargs["inputArtifactDetails"] = input_artifact_details
    kwargs["outputArtifactDetails"] = output_artifact_details
    if settings is not None:
        kwargs["settings"] = settings
    if configuration_properties is not None:
        kwargs["configurationProperties"] = configuration_properties
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_custom_action_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create custom action type") from exc
    return CreateCustomActionTypeResult(
        action_type=resp.get("actionType"),
        tags=resp.get("tags"),
    )


def delete_custom_action_type(
    category: str,
    provider: str,
    version: str,
    region_name: str | None = None,
) -> None:
    """Delete custom action type.

    Args:
        category: Category.
        provider: Provider.
        version: Version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["category"] = category
    kwargs["provider"] = provider
    kwargs["version"] = version
    try:
        client.delete_custom_action_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete custom action type") from exc
    return None


def delete_webhook(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete webhook.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        client.delete_webhook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete webhook") from exc
    return None


def deregister_webhook_with_third_party(
    *,
    webhook_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Deregister webhook with third party.

    Args:
        webhook_name: Webhook name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    if webhook_name is not None:
        kwargs["webhookName"] = webhook_name
    try:
        client.deregister_webhook_with_third_party(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister webhook with third party") from exc
    return None


def get_action_type(
    category: str,
    owner: str,
    provider: str,
    version: str,
    region_name: str | None = None,
) -> GetActionTypeResult:
    """Get action type.

    Args:
        category: Category.
        owner: Owner.
        provider: Provider.
        version: Version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["category"] = category
    kwargs["owner"] = owner
    kwargs["provider"] = provider
    kwargs["version"] = version
    try:
        resp = client.get_action_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get action type") from exc
    return GetActionTypeResult(
        action_type=resp.get("actionType"),
    )


def get_job_details(
    job_id: str,
    region_name: str | None = None,
) -> GetJobDetailsResult:
    """Get job details.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    try:
        resp = client.get_job_details(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get job details") from exc
    return GetJobDetailsResult(
        job_details=resp.get("jobDetails"),
    )


def get_third_party_job_details(
    job_id: str,
    client_token: str,
    region_name: str | None = None,
) -> GetThirdPartyJobDetailsResult:
    """Get third party job details.

    Args:
        job_id: Job id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["clientToken"] = client_token
    try:
        resp = client.get_third_party_job_details(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get third party job details") from exc
    return GetThirdPartyJobDetailsResult(
        job_details=resp.get("jobDetails"),
    )


def list_action_executions(
    pipeline_name: str,
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListActionExecutionsResult:
    """List action executions.

    Args:
        pipeline_name: Pipeline name.
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pipelineName"] = pipeline_name
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_action_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list action executions") from exc
    return ListActionExecutionsResult(
        action_execution_details=resp.get("actionExecutionDetails"),
        next_token=resp.get("nextToken"),
    )


def list_action_types(
    *,
    action_owner_filter: str | None = None,
    next_token: str | None = None,
    region_filter: str | None = None,
    region_name: str | None = None,
) -> ListActionTypesResult:
    """List action types.

    Args:
        action_owner_filter: Action owner filter.
        next_token: Next token.
        region_filter: Region filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    if action_owner_filter is not None:
        kwargs["actionOwnerFilter"] = action_owner_filter
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if region_filter is not None:
        kwargs["regionFilter"] = region_filter
    try:
        resp = client.list_action_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list action types") from exc
    return ListActionTypesResult(
        action_types=resp.get("actionTypes"),
        next_token=resp.get("nextToken"),
    )


def list_deploy_action_execution_targets(
    action_execution_id: str,
    *,
    pipeline_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDeployActionExecutionTargetsResult:
    """List deploy action execution targets.

    Args:
        action_execution_id: Action execution id.
        pipeline_name: Pipeline name.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionExecutionId"] = action_execution_id
    if pipeline_name is not None:
        kwargs["pipelineName"] = pipeline_name
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_deploy_action_execution_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list deploy action execution targets") from exc
    return ListDeployActionExecutionTargetsResult(
        targets=resp.get("targets"),
        next_token=resp.get("nextToken"),
    )


def list_rule_executions(
    pipeline_name: str,
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRuleExecutionsResult:
    """List rule executions.

    Args:
        pipeline_name: Pipeline name.
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pipelineName"] = pipeline_name
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_rule_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rule executions") from exc
    return ListRuleExecutionsResult(
        rule_execution_details=resp.get("ruleExecutionDetails"),
        next_token=resp.get("nextToken"),
    )


def list_rule_types(
    *,
    rule_owner_filter: str | None = None,
    region_filter: str | None = None,
    region_name: str | None = None,
) -> ListRuleTypesResult:
    """List rule types.

    Args:
        rule_owner_filter: Rule owner filter.
        region_filter: Region filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    if rule_owner_filter is not None:
        kwargs["ruleOwnerFilter"] = rule_owner_filter
    if region_filter is not None:
        kwargs["regionFilter"] = region_filter
    try:
        resp = client.list_rule_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rule types") from exc
    return ListRuleTypesResult(
        rule_types=resp.get("ruleTypes"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
        next_token=resp.get("nextToken"),
    )


def list_webhooks(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListWebhooksResult:
    """List webhooks.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_webhooks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list webhooks") from exc
    return ListWebhooksResult(
        webhooks=resp.get("webhooks"),
        next_token=resp.get("NextToken"),
    )


def override_stage_condition(
    pipeline_name: str,
    stage_name: str,
    pipeline_execution_id: str,
    condition_type: str,
    region_name: str | None = None,
) -> None:
    """Override stage condition.

    Args:
        pipeline_name: Pipeline name.
        stage_name: Stage name.
        pipeline_execution_id: Pipeline execution id.
        condition_type: Condition type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pipelineName"] = pipeline_name
    kwargs["stageName"] = stage_name
    kwargs["pipelineExecutionId"] = pipeline_execution_id
    kwargs["conditionType"] = condition_type
    try:
        client.override_stage_condition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to override stage condition") from exc
    return None


def poll_for_jobs(
    action_type_id: dict[str, Any],
    *,
    max_batch_size: int | None = None,
    query_param: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PollForJobsResult:
    """Poll for jobs.

    Args:
        action_type_id: Action type id.
        max_batch_size: Max batch size.
        query_param: Query param.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionTypeId"] = action_type_id
    if max_batch_size is not None:
        kwargs["maxBatchSize"] = max_batch_size
    if query_param is not None:
        kwargs["queryParam"] = query_param
    try:
        resp = client.poll_for_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to poll for jobs") from exc
    return PollForJobsResult(
        jobs=resp.get("jobs"),
    )


def poll_for_third_party_jobs(
    action_type_id: dict[str, Any],
    *,
    max_batch_size: int | None = None,
    region_name: str | None = None,
) -> PollForThirdPartyJobsResult:
    """Poll for third party jobs.

    Args:
        action_type_id: Action type id.
        max_batch_size: Max batch size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionTypeId"] = action_type_id
    if max_batch_size is not None:
        kwargs["maxBatchSize"] = max_batch_size
    try:
        resp = client.poll_for_third_party_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to poll for third party jobs") from exc
    return PollForThirdPartyJobsResult(
        jobs=resp.get("jobs"),
    )


def put_action_revision(
    pipeline_name: str,
    stage_name: str,
    action_name: str,
    action_revision: dict[str, Any],
    region_name: str | None = None,
) -> PutActionRevisionResult:
    """Put action revision.

    Args:
        pipeline_name: Pipeline name.
        stage_name: Stage name.
        action_name: Action name.
        action_revision: Action revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pipelineName"] = pipeline_name
    kwargs["stageName"] = stage_name
    kwargs["actionName"] = action_name
    kwargs["actionRevision"] = action_revision
    try:
        resp = client.put_action_revision(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put action revision") from exc
    return PutActionRevisionResult(
        new_revision=resp.get("newRevision"),
        pipeline_execution_id=resp.get("pipelineExecutionId"),
    )


def put_job_failure_result(
    job_id: str,
    failure_details: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put job failure result.

    Args:
        job_id: Job id.
        failure_details: Failure details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["failureDetails"] = failure_details
    try:
        client.put_job_failure_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put job failure result") from exc
    return None


def put_job_success_result(
    job_id: str,
    *,
    current_revision: dict[str, Any] | None = None,
    continuation_token: str | None = None,
    execution_details: dict[str, Any] | None = None,
    output_variables: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put job success result.

    Args:
        job_id: Job id.
        current_revision: Current revision.
        continuation_token: Continuation token.
        execution_details: Execution details.
        output_variables: Output variables.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if current_revision is not None:
        kwargs["currentRevision"] = current_revision
    if continuation_token is not None:
        kwargs["continuationToken"] = continuation_token
    if execution_details is not None:
        kwargs["executionDetails"] = execution_details
    if output_variables is not None:
        kwargs["outputVariables"] = output_variables
    try:
        client.put_job_success_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put job success result") from exc
    return None


def put_third_party_job_failure_result(
    job_id: str,
    client_token: str,
    failure_details: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put third party job failure result.

    Args:
        job_id: Job id.
        client_token: Client token.
        failure_details: Failure details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["clientToken"] = client_token
    kwargs["failureDetails"] = failure_details
    try:
        client.put_third_party_job_failure_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put third party job failure result") from exc
    return None


def put_third_party_job_success_result(
    job_id: str,
    client_token: str,
    *,
    current_revision: dict[str, Any] | None = None,
    continuation_token: str | None = None,
    execution_details: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put third party job success result.

    Args:
        job_id: Job id.
        client_token: Client token.
        current_revision: Current revision.
        continuation_token: Continuation token.
        execution_details: Execution details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["clientToken"] = client_token
    if current_revision is not None:
        kwargs["currentRevision"] = current_revision
    if continuation_token is not None:
        kwargs["continuationToken"] = continuation_token
    if execution_details is not None:
        kwargs["executionDetails"] = execution_details
    try:
        client.put_third_party_job_success_result(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put third party job success result") from exc
    return None


def put_webhook(
    webhook: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutWebhookResult:
    """Put webhook.

    Args:
        webhook: Webhook.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["webhook"] = webhook
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.put_webhook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put webhook") from exc
    return PutWebhookResult(
        webhook=resp.get("webhook"),
    )


def register_webhook_with_third_party(
    *,
    webhook_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Register webhook with third party.

    Args:
        webhook_name: Webhook name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    if webhook_name is not None:
        kwargs["webhookName"] = webhook_name
    try:
        client.register_webhook_with_third_party(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register webhook with third party") from exc
    return None


def rollback_stage(
    pipeline_name: str,
    stage_name: str,
    target_pipeline_execution_id: str,
    region_name: str | None = None,
) -> RollbackStageResult:
    """Rollback stage.

    Args:
        pipeline_name: Pipeline name.
        stage_name: Stage name.
        target_pipeline_execution_id: Target pipeline execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["pipelineName"] = pipeline_name
    kwargs["stageName"] = stage_name
    kwargs["targetPipelineExecutionId"] = target_pipeline_execution_id
    try:
        resp = client.rollback_stage(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rollback stage") from exc
    return RollbackStageResult(
        pipeline_execution_id=resp.get("pipelineExecutionId"),
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
    client = get_client("codepipeline", region_name)
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
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_action_type(
    action_type: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update action type.

    Args:
        action_type: Action type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codepipeline", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionType"] = action_type
    try:
        client.update_action_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update action type") from exc
    return None
